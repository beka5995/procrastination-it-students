from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def cronbach_alpha(items: pd.DataFrame) -> float:
    """
    Calculate Cronbach's alpha for multi-item questionnaire scales.

    Rows = participants, columns = items.
    """
    x = items.dropna().astype(float)
    if x.shape[0] < 2 or x.shape[1] < 2:
        return float("nan")

    item_variances = x.var(axis=0, ddof=1)
    total_score = x.sum(axis=1)
    total_variance = total_score.var(ddof=1)
    k = x.shape[1]

    if total_variance == 0:
        return float("nan")

    return float((k / (k - 1)) * (1 - item_variances.sum() / total_variance))


def spearman_test(x: pd.Series, y: pd.Series) -> dict:
    """Spearman correlation with pairwise missing-value removal."""
    pair = pd.concat([x, y], axis=1).dropna()
    if len(pair) < 3:
        return {"n": len(pair), "rho": np.nan, "p_value": np.nan}

    rho, p = stats.spearmanr(pair.iloc[:, 0], pair.iloc[:, 1])
    return {"n": len(pair), "rho": float(rho), "p_value": float(p)}


def friedman_distraction_test(df: pd.DataFrame, columns: list[str]) -> dict:
    """Friedman test for repeated ratings of multiple distraction categories."""
    clean = df[columns].dropna()
    if len(clean) < 2:
        return {"n": len(clean), "statistic": np.nan, "p_value": np.nan}

    result = stats.friedmanchisquare(*[clean[c] for c in columns])
    return {
        "n": len(clean),
        "statistic": float(result.statistic),
        "p_value": float(result.pvalue),
    }


def paired_condition_test(controlled_df: pd.DataFrame) -> dict:
    """
    Compare CLI between focused and interrupted conditions.

    Uses a paired t-test when the paired difference is approximately normal
    (Shapiro p >= 0.05). Otherwise uses Wilcoxon signed-rank test.
    """
    required = {"participant_id", "condition", "cli"}
    if not required.issubset(controlled_df.columns):
        missing = sorted(required - set(controlled_df.columns))
        raise ValueError(f"Missing columns: {missing}")

    wide = controlled_df.pivot_table(
        index="participant_id",
        columns="condition",
        values="cli",
        aggfunc="mean",
    )

    if not {"focused", "interrupted"}.issubset(wide.columns):
        raise ValueError("Conditions must be named 'focused' and 'interrupted'.")

    pair = wide[["focused", "interrupted"]].dropna()
    if len(pair) < 3:
        return {
            "n": len(pair),
            "test": None,
            "statistic": np.nan,
            "p_value": np.nan,
            "mean_difference": np.nan,
        }

    difference = pair["interrupted"] - pair["focused"]
    mean_difference = float(difference.mean())

    if len(difference) >= 3:
        shapiro_p = float(stats.shapiro(difference).pvalue)
    else:
        shapiro_p = np.nan

    if not np.isnan(shapiro_p) and shapiro_p >= 0.05:
        stat, p = stats.ttest_rel(pair["interrupted"], pair["focused"])
        test = "paired_t_test"
    else:
        stat, p = stats.wilcoxon(pair["interrupted"], pair["focused"])
        test = "wilcoxon_signed_rank"

    return {
        "n": len(pair),
        "test": test,
        "statistic": float(stat),
        "p_value": float(p),
        "mean_difference": mean_difference,
        "shapiro_p": shapiro_p,
    }


def paired_cohens_d(focused: pd.Series, interrupted: pd.Series) -> float:
    """Cohen's d for paired measurements: mean difference / SD of differences."""
    pair = pd.concat([focused, interrupted], axis=1).dropna()
    if len(pair) < 2:
        return float("nan")
    diff = pair.iloc[:, 1] - pair.iloc[:, 0]
    sd = diff.std(ddof=1)
    if sd == 0 or np.isnan(sd):
        return float("nan")
    return float(diff.mean() / sd)
