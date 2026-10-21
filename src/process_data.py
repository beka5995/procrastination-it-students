from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "configs" / "task3_analysis_config.json"


def load_config(path: Path = CONFIG_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> pd.DataFrame:
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return pd.DataFrame(records)


def bootstrap_ci(values: Iterable[float], seed: int = 42, n_boot: int = 5000,
                 confidence: float = 0.95, statistic: str = "median") -> tuple[float, float]:
    x = np.asarray(list(values), dtype=float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return (float("nan"), float("nan"))

    rng = np.random.default_rng(seed)
    samples = rng.choice(x, size=(n_boot, len(x)), replace=True)

    if statistic == "mean":
        boot_stats = np.mean(samples, axis=1)
    else:
        boot_stats = np.median(samples, axis=1)

    alpha = 1 - confidence
    low, high = np.quantile(boot_stats, [alpha / 2, 1 - alpha / 2])
    return float(low), float(high)


def summarize_metric(values: pd.Series, seed: int, n_boot: int) -> dict:
    x = pd.to_numeric(values, errors="coerce").dropna().astype(float)
    ci_low, ci_high = bootstrap_ci(x, seed=seed, n_boot=n_boot, statistic="median")
    return {
        "n": int(x.size),
        "mean": float(x.mean()),
        "sd": float(x.std(ddof=1)) if x.size > 1 else 0.0,
        "median": float(x.median()),
        "p25": float(x.quantile(0.25)),
        "p75": float(x.quantile(0.75)),
        "p95": float(x.quantile(0.95)),
        "p99": float(x.quantile(0.99)),
        "median_ci95_low": ci_low,
        "median_ci95_high": ci_high,
    }


def analyze_dataframe(df: pd.DataFrame, cfg: dict) -> tuple[pd.DataFrame, dict]:
    required = {
        "participant_id", "phase", "condition", "completion_time_sec",
        "accuracy_pct", "cli", "context_switches", "task_error"
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    warmup = df[df["phase"] == "warmup"].copy()
    evaluation = df[df["phase"] == "evaluation"].copy()

    # Guardrail errors are tracked, but excluded from the primary comparison.
    error_rates = (
        evaluation.groupby("condition")["task_error"]
        .mean()
        .mul(100)
        .to_dict()
    )

    clean = evaluation[evaluation["task_error"] == 0].copy()

    metric_names = list(cfg["metrics"].keys())
    summary_rows = []
    for condition in cfg["evaluation_conditions"]:
        subset = clean[clean["condition"] == condition]
        for metric in metric_names:
            result = summarize_metric(
                subset[metric],
                seed=int(cfg["random_seed"]),
                n_boot=int(cfg["bootstrap_resamples"]),
            )
            summary_rows.append({
                "condition": condition,
                "metric": metric,
                **result
            })

    summary = pd.DataFrame(summary_rows)

    # Primary paired CLI comparison: only participants with valid values in both conditions.
    cli_wide = (
        clean.pivot_table(
            index="participant_id",
            columns="condition",
            values="cli",
            aggfunc="first",
        )
        .dropna(subset=["focused", "interrupted"])
    )
    delta = cli_wide["interrupted"] - cli_wide["focused"]
    delta_ci = bootstrap_ci(
        delta,
        seed=int(cfg["random_seed"]),
        n_boot=int(cfg["bootstrap_resamples"]),
        statistic="mean",
    )

    if len(delta) >= 3:
        shapiro_w, shapiro_p = stats.shapiro(delta)
    else:
        shapiro_w, shapiro_p = float("nan"), float("nan")

    if len(delta) >= 2 and (not np.isnan(shapiro_p)) and shapiro_p >= 0.05:
        test_name = "paired_t_test"
        test = stats.ttest_rel(cli_wide["interrupted"], cli_wide["focused"])
        statistic = float(test.statistic)
        p_value = float(test.pvalue)
    elif len(delta) >= 2:
        test_name = "wilcoxon_signed_rank"
        test = stats.wilcoxon(
            cli_wide["interrupted"],
            cli_wide["focused"],
            alternative="greater",
            zero_method="wilcox",
        )
        statistic = float(test.statistic)
        p_value = float(test.pvalue)
    else:
        test_name = "not_available"
        statistic = float("nan")
        p_value = float("nan")

    delta_sd = float(delta.std(ddof=1)) if len(delta) > 1 else float("nan")
    cohens_dz = float(delta.mean() / delta_sd) if delta_sd and np.isfinite(delta_sd) else float("nan")

    statistics = {
        "data_origin": sorted(df.get("data_origin", pd.Series(dtype=str)).dropna().unique().tolist()),
        "raw_rows": int(len(df)),
        "warmup_rows_filtered": int(len(warmup)),
        "evaluation_rows_before_guardrail_filter": int(len(evaluation)),
        "evaluation_rows_after_guardrail_filter": int(len(clean)),
        "error_rate_pct": {k: round(float(v), 3) for k, v in error_rates.items()},
        "complete_pairs_for_primary_cli": int(len(cli_wide)),
        "primary_metric": "Delta CLI = CLI(interrupted) - CLI(focused)",
        "delta_cli_mean": float(delta.mean()),
        "delta_cli_median": float(delta.median()),
        "delta_cli_mean_ci95": [float(delta_ci[0]), float(delta_ci[1])],
        "delta_cli_sd": delta_sd,
        "cohens_dz": cohens_dz,
        "normality_shapiro_w": float(shapiro_w),
        "normality_shapiro_p": float(shapiro_p),
        "inferential_test": test_name,
        "test_statistic": statistic,
        "p_value_two_sided_or_test_default": p_value,
        "alpha": float(cfg["alpha"]),
        "interpretation_guardrail": (
            "The bundled dataset is synthetic pilot data for reproducibility testing. "
            "These statistics must not be reported as empirical findings about real students."
        ),
    }
    return summary, statistics


def main() -> None:
    cfg = load_config()
    raw_path = ROOT / cfg["raw_data_path"]
    out_csv = ROOT / cfg["processed_summary_path"]
    out_json = ROOT / cfg["statistics_output_path"]

    df = load_jsonl(raw_path)
    summary, statistics = analyze_dataframe(df, cfg)

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    summary.to_csv(out_csv, index=False)
    out_json.write_text(json.dumps(statistics, indent=2), encoding="utf-8")

    print("Task 3 data processing completed.")
    print(f"Raw rows: {statistics['raw_rows']}")
    print(f"Warm-up rows filtered: {statistics['warmup_rows_filtered']}")
    print(f"Complete paired observations: {statistics['complete_pairs_for_primary_cli']}")
    print(f"Delta CLI (mean): {statistics['delta_cli_mean']:.3f}")
    print(f"Saved: {out_csv.relative_to(ROOT)}")
    print(f"Saved: {out_json.relative_to(ROOT)}")
    print("NOTE: bundled data are synthetic pilot data, not empirical research findings.")


if __name__ == "__main__":
    main()
