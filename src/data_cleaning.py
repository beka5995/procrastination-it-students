from __future__ import annotations

from pathlib import Path
import pandas as pd


LIKERT_COLUMNS = [
    "sleep_quality",
    "academic_motivation",
    "task_difficulty",
    "task_importance",
    "messaging_freq",
    "notifications_freq",
    "browser_tab_switch_freq",
    "ide_browser_switch_freq",
    "background_media_freq",
    "unrelated_social_freq",
    "multitasking_freq",
    "cl_mental_demand",
    "cl_effort",
    "cl_focus_difficulty",
    "cl_refocus_difficulty",
    "mental_fatigue",
    "p_delay",
    "p_avoid",
    "p_replace",
    "p_unrelated_switch",
]

CLI_ITEMS = [
    "cl_mental_demand",
    "cl_effort",
    "cl_focus_difficulty",
    "cl_refocus_difficulty",
]

PI_ITEMS = [
    "p_delay",
    "p_avoid",
    "p_replace",
    "p_unrelated_switch",
]


def read_csv(path: str | Path) -> pd.DataFrame:
    """Read a project CSV file."""
    return pd.read_csv(path)


def clean_questionnaire(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning for questionnaire data.

    - removes duplicate participant IDs;
    - converts known numeric columns to numeric values;
    - sets invalid 1-5 Likert responses to missing;
    - calculates CLI and PI.
    """
    out = df.copy()

    if "participant_id" in out.columns:
        out = out.drop_duplicates(subset=["participant_id"], keep="first")

    numeric_candidates = [
        "study_year",
        "programming_experience_semesters",
        "sleep_hours",
        "deadline_days",
        "weekly_study_hours",
        "parallel_deadlines",
        "context_switch_count_per_hour",
        *LIKERT_COLUMNS,
    ]

    for col in numeric_candidates:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    for col in LIKERT_COLUMNS:
        if col in out.columns:
            out.loc[~out[col].between(1, 5), col] = pd.NA

    if all(col in out.columns for col in CLI_ITEMS):
        out["cli"] = out[CLI_ITEMS].mean(axis=1, skipna=False)

    if all(col in out.columns for col in PI_ITEMS):
        out["pi"] = out[PI_ITEMS].mean(axis=1, skipna=False)

    return out


def clean_controlled_task(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning for the focused-vs-interrupted task data.
    """
    out = df.copy()

    numeric_cols = [
        "task_accuracy",
        "completion_time_min",
        "cl_mental_demand",
        "cl_effort",
        "cl_focus_difficulty",
        "cl_refocus_difficulty",
        "mental_fatigue",
    ]

    for col in numeric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    for col in [
        "cl_mental_demand",
        "cl_effort",
        "cl_focus_difficulty",
        "cl_refocus_difficulty",
        "mental_fatigue",
    ]:
        if col in out.columns:
            out.loc[~out[col].between(1, 5), col] = pd.NA

    cli_items = [
        "cl_mental_demand",
        "cl_effort",
        "cl_focus_difficulty",
        "cl_refocus_difficulty",
    ]
    if all(col in out.columns for col in cli_items):
        out["cli"] = out[cli_items].mean(axis=1, skipna=False)

    return out
