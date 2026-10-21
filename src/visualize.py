from __future__ import annotations

from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from process_data import ROOT, load_config, load_jsonl, bootstrap_ci


def _save(fig, path_base: Path) -> None:
    path_base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path_base.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(path_base.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


def create_figures() -> list[Path]:
    cfg = load_config()
    df = load_jsonl(ROOT / cfg["raw_data_path"])
    evaluation = df[(df["phase"] == "evaluation") & (df["task_error"] == 0)].copy()

    cmap = plt.cm.viridis
    focused_color = cmap(0.22)
    interrupted_color = cmap(0.78)
    colors = {"focused": focused_color, "interrupted": interrupted_color}
    markers = {"focused": "o", "interrupted": "s"}

    # Figure 1: paired CLI observations + median with bootstrapped 95% CI.
    wide = (
        evaluation.pivot_table(index="participant_id", columns="condition", values="cli", aggfunc="first")
        .dropna(subset=["focused", "interrupted"])
    )

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    x = np.array([0, 1])
    for _, row in wide.iterrows():
        ax.plot(x, [row["focused"], row["interrupted"]],
                color="0.75", linewidth=0.8, alpha=0.55, linestyle="-")

    for xpos, condition in zip(x, ["focused", "interrupted"]):
        vals = wide[condition].to_numpy(dtype=float)
        median = float(np.median(vals))
        ci_low, ci_high = bootstrap_ci(
            vals,
            seed=int(cfg["random_seed"]),
            n_boot=int(cfg["bootstrap_resamples"]),
            statistic="median",
        )
        ax.errorbar(
            xpos, median,
            yerr=[[median - ci_low], [ci_high - median]],
            fmt=markers[condition],
            markersize=9,
            capsize=5,
            linewidth=2,
            color=colors[condition],
            markeredgecolor="black",
            label=f"{condition.title()} median (95% CI)",
        )

    ax.set_xticks([0, 1], ["Focused", "Interrupted"])
    ax.set_ylabel("Cognitive Load Index (1-5 Likert scale)")
    ax.set_xlabel("Experimental condition")
    ax.set_title("Cognitive load under focused and interrupted conditions")
    ax.set_ylim(1, 5)
    ax.grid(axis="y", alpha=0.25, linestyle=":")
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()

    fig1_base = ROOT / cfg["figures_dir"] / "fig1_cognitive_load_comparison"
    _save(fig, fig1_base)

    # Figure 2: completion-time distribution + median 95% CI.
    conditions = ["focused", "interrupted"]
    data = [
        evaluation.loc[evaluation["condition"] == c, "completion_time_sec"].to_numpy(dtype=float)
        for c in conditions
    ]

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    bp = ax.boxplot(
        data,
        tick_labels=["Focused", "Interrupted"],
        patch_artist=True,
        showfliers=True,
        widths=0.48,
        medianprops={"color": "black", "linewidth": 1.6},
        whiskerprops={"linestyle": "--", "linewidth": 1.2},
        capprops={"linewidth": 1.2},
    )
    hatches = ["///", "..."]
    for patch, c, hatch in zip(bp["boxes"], conditions, hatches):
        patch.set_facecolor(colors[c])
        patch.set_alpha(0.55)
        patch.set_hatch(hatch)

    for xpos, (condition, vals) in enumerate(zip(conditions, data), start=1):
        median = float(np.median(vals))
        ci_low, ci_high = bootstrap_ci(
            vals,
            seed=int(cfg["random_seed"]),
            n_boot=int(cfg["bootstrap_resamples"]),
            statistic="median",
        )
        ax.errorbar(
            xpos, median,
            yerr=[[median - ci_low], [ci_high - median]],
            fmt=markers[condition],
            markersize=8,
            capsize=5,
            linewidth=2,
            color=colors[condition],
            markeredgecolor="black",
        )

    ax.set_ylabel("Task Completion Time (seconds)")
    ax.set_xlabel("Experimental condition")
    ax.set_title("Task completion-time distribution with median 95% CI")
    ax.grid(axis="y", alpha=0.25, linestyle=":")
    fig.tight_layout()

    fig2_base = ROOT / cfg["figures_dir"] / "fig2_completion_time_boxplot"
    _save(fig, fig2_base)

    return [
        fig1_base.with_suffix(".png"),
        fig1_base.with_suffix(".pdf"),
        fig2_base.with_suffix(".png"),
        fig2_base.with_suffix(".pdf"),
    ]


def main() -> None:
    outputs = create_figures()
    print("Task 3 figures created:")
    for p in outputs:
        print(f" - {p.relative_to(ROOT)}")
    print("PNG files are saved at 300 DPI; PDF files are vector exports.")


if __name__ == "__main__":
    main()
