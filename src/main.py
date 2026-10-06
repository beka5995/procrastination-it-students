from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

# Allow imports when this file is executed as: python src/main.py
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data_cleaning import clean_questionnaire, clean_controlled_task
from src.analysis import (
    cronbach_alpha,
    friedman_distraction_test,
    paired_condition_test,
    paired_cohens_d,
    spearman_test,
)


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def safe_number(value):
    if value is None:
        return None
    if isinstance(value, (float, np.floating)) and (np.isnan(value) or np.isinf(value)):
        return None
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    return value


def missing_rate(df: pd.DataFrame) -> float:
    if df.empty:
        return 1.0
    return float(df.isna().sum().sum() / (df.shape[0] * df.shape[1]))


def run(config_path: Path) -> dict:
    cfg = load_config(config_path)
    paths = cfg["paths"]

    q_path = ROOT / paths["questionnaire_sample"]
    c_path = ROOT / paths["controlled_task_sample"]
    output_dir = ROOT / paths["output_directory"]
    output_dir.mkdir(parents=True, exist_ok=True)

    if not q_path.exists() or not c_path.exists():
        raise FileNotFoundError("Sample data files are missing. Check data/sample/ and config paths.")

    q_raw = pd.read_csv(q_path)
    c_raw = pd.read_csv(c_path)
    q = clean_questionnaire(q_raw)
    c = clean_controlled_task(c_raw)

    cli_items = cfg["cli_items"]
    pi_items = cfg["pi_items"]
    distraction_cols = cfg["distraction_frequency_items"]

    # RQ1: compare reported distraction frequencies.
    rq1 = friedman_distraction_test(q, distraction_cols)
    distraction_means = q[distraction_cols].mean().sort_values(ascending=False)

    # Scale quality checks.
    cli_alpha = cronbach_alpha(q[cli_items])
    pi_alpha = cronbach_alpha(q[pi_items])

    # RQ2 survey: context switching and cognitive load.
    rq2_survey = spearman_test(q["context_switch_count_per_hour"], q["cli"])

    # RQ3: cognitive load and procrastination.
    rq3 = spearman_test(q["cli"], q["pi"])

    # RQ2 controlled task: focused baseline vs interrupted condition.
    rq2_controlled = paired_condition_test(c)
    wide = c.pivot_table(index="participant_id", columns="condition", values="cli", aggfunc="mean")
    effect_size = paired_cohens_d(wide["focused"], wide["interrupted"])

    guardrails = cfg["guardrails"]
    q_missing = missing_rate(q)
    duplicate_ids = int(q_raw["participant_id"].duplicated().sum())

    results = {
        "run_type": "synthetic_sample_smoke_test",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "alpha": cfg["alpha"],
        "sample_sizes": {
            "questionnaire_rows": int(len(q)),
            "controlled_task_rows": int(len(c)),
            "controlled_task_participants": int(c["participant_id"].nunique()),
        },
        "primary_metric": {
            "name": "delta_cli_interrupted_minus_focused",
            "value": safe_number(rq2_controlled.get("mean_difference")),
            "paired_test": rq2_controlled.get("test"),
            "p_value": safe_number(rq2_controlled.get("p_value")),
            "effect_size_paired_cohens_d": safe_number(effect_size),
        },
        "rq1": {
            "friedman_statistic": safe_number(rq1.get("statistic")),
            "p_value": safe_number(rq1.get("p_value")),
            "mean_frequency_by_distraction": {k: safe_number(v) for k, v in distraction_means.to_dict().items()},
        },
        "rq2_survey": {
            "spearman_rho": safe_number(rq2_survey.get("rho")),
            "p_value": safe_number(rq2_survey.get("p_value")),
        },
        "rq3": {
            "spearman_rho": safe_number(rq3.get("rho")),
            "p_value": safe_number(rq3.get("p_value")),
        },
        "guardrails": {
            "questionnaire_missing_rate": safe_number(q_missing),
            "missing_rate_limit": guardrails["max_missing_rate"],
            "missing_rate_pass": bool(q_missing <= guardrails["max_missing_rate"]),
            "cli_cronbach_alpha": safe_number(cli_alpha),
            "pi_cronbach_alpha": safe_number(pi_alpha),
            "cronbach_alpha_target": guardrails["cronbach_alpha_target"],
            "duplicate_participant_ids": duplicate_ids,
            "duplicate_id_check_pass": bool(duplicate_ids == 0),
        },
        "note": "These values come from synthetic sample data and are only used to test the pipeline. They are not research findings.",
    }

    json_path = output_dir / "sample_results.json"
    log_path = output_dir / "run_log.txt"

    json_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    log_lines = [
        "TASK 2 SAMPLE PIPELINE RUN",
        "==========================",
        f"Questionnaire rows: {len(q)}",
        f"Controlled-task rows: {len(c)}",
        f"Controlled-task participants: {c['participant_id'].nunique()}",
        f"Primary metric Delta CLI: {results['primary_metric']['value']}",
        f"Paired test: {results['primary_metric']['paired_test']}",
        f"p-value: {results['primary_metric']['p_value']}",
        f"Paired Cohen's d: {results['primary_metric']['effect_size_paired_cohens_d']}",
        f"Missing-rate check: {results['guardrails']['missing_rate_pass']}",
        f"Duplicate-ID check: {results['guardrails']['duplicate_id_check_pass']}",
        "",
        "IMPORTANT: this is a smoke test using synthetic sample data, not a final research result.",
    ]
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print("Sample pipeline completed successfully.")
    print(f"Primary metric (Delta CLI): {results['primary_metric']['value']}")
    print(f"Saved: {json_path.relative_to(ROOT)}")
    print(f"Saved: {log_path.relative_to(ROOT)}")
    print("Synthetic sample only — do not report these values as research findings.")

    return results


def main():
    parser = argparse.ArgumentParser(description="Run the Task 2 sample measurement pipeline.")
    parser.add_argument(
        "--config",
        default="configs/analysis_config.json",
        help="Path to JSON configuration file relative to the project root.",
    )
    args = parser.parse_args()
    run(ROOT / args.config)


if __name__ == "__main__":
    main()
