from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data_cleaning import clean_questionnaire, clean_controlled_task
from src.analysis import (
    cronbach_alpha,
    spearman_test,
    friedman_distraction_test,
    paired_condition_test,
)

RAW_Q = ROOT / "data" / "raw" / "questionnaire.csv"
RAW_C = ROOT / "data" / "raw" / "controlled_task.csv"
OUT_DIR = ROOT / "results" / "tables"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    if not RAW_Q.exists():
        print("Questionnaire data not found:", RAW_Q)
        print("Copy data/raw/questionnaire_template.csv to questionnaire.csv and add anonymized data.")
        return

    q = clean_questionnaire(pd.read_csv(RAW_Q))

    distraction_cols = [
        "messaging_freq",
        "notifications_freq",
        "browser_tab_switch_freq",
        "ide_browser_switch_freq",
        "background_media_freq",
        "unrelated_social_freq",
    ]

    summary = []

    # RQ1
    available = [c for c in distraction_cols if c in q.columns]
    if len(available) >= 3:
        result = friedman_distraction_test(q, available)
        summary.append({"analysis": "RQ1 Friedman", **result})

    # Scale quality
    cli_cols = ["cl_mental_demand", "cl_effort", "cl_focus_difficulty", "cl_refocus_difficulty"]
    pi_cols = ["p_delay", "p_avoid", "p_replace", "p_unrelated_switch"]

    if all(c in q.columns for c in cli_cols):
        summary.append({
            "analysis": "CLI Cronbach alpha",
            "n": q[cli_cols].dropna().shape[0],
            "statistic": cronbach_alpha(q[cli_cols]),
            "p_value": None,
        })

    if all(c in q.columns for c in pi_cols):
        summary.append({
            "analysis": "PI Cronbach alpha",
            "n": q[pi_cols].dropna().shape[0],
            "statistic": cronbach_alpha(q[pi_cols]),
            "p_value": None,
        })

    # RQ2 survey
    if {"context_switch_count_per_hour", "cli"}.issubset(q.columns):
        result = spearman_test(q["context_switch_count_per_hour"], q["cli"])
        summary.append({
            "analysis": "RQ2 Spearman: context switching vs CLI",
            "n": result["n"],
            "statistic": result["rho"],
            "p_value": result["p_value"],
        })

    # RQ3
    if {"cli", "pi"}.issubset(q.columns):
        result = spearman_test(q["cli"], q["pi"])
        summary.append({
            "analysis": "RQ3 Spearman: CLI vs PI",
            "n": result["n"],
            "statistic": result["rho"],
            "p_value": result["p_value"],
        })

    # Controlled task
    if RAW_C.exists():
        c = clean_controlled_task(pd.read_csv(RAW_C))
        try:
            result = paired_condition_test(c)
            summary.append({
                "analysis": f"RQ2 controlled: {result['test']}",
                "n": result["n"],
                "statistic": result["statistic"],
                "p_value": result["p_value"],
            })
        except ValueError as exc:
            print("Controlled task skipped:", exc)

    out = pd.DataFrame(summary)
    out.to_csv(OUT_DIR / "analysis_summary.csv", index=False)

    print(out.to_string(index=False))
    print("\nSaved:", OUT_DIR / "analysis_summary.csv")


if __name__ == "__main__":
    main()
