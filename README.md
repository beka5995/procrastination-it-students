# Procrastination Triggers in the Digital Environment

**How Context Switching and Micro-Habits Affect the Concentration of IT Students**

**Authors:** Mashat Bekzhan, Nursultan Sultan  
**Course:** Research Methods  
**Group:** SCOM3001-ENG-9  
**University:** Narxoz University  
**Status:** Research design and reproducibility setup  
**License:** MIT (code)

---

## Project Overview

This research examines how disruptive digital habits among IT students are connected with context switching, cognitive load, loss of concentration, and academic procrastination.

The project continues the research design developed in Task 1 and SS5. It uses two components:

1. **Questionnaire study** — used to describe common digital distractions and examine relationships between context switching, cognitive load, and procrastination.
2. **Small controlled coding task** — used to compare a focused condition with an interrupted condition during a short programming / algorithmic task.

No final empirical results are included in this repository yet. Tables under **Expected Results** are placeholders to be completed after data collection.

## Research Aim

The aim is to identify the most common disruptive digital habits among IT students and examine how context switching and multitasking are related to cognitive load, reduced concentration, and academic procrastination.

## Research Questions

**RQ1.** Which disruptive digital habits (notifications, switching between browser tabs and an IDE, background messaging, and similar behaviors) are most common among IT students during academic and practical tasks?

**RQ2.** How do frequent context switching and multitasking affect perceived cognitive load and mental fatigue among IT students when they are writing code or solving algorithmic problems?

**RQ3.** How is cognitive overload caused by digital distractions related to the transition from academic work to academic procrastination?

## Core Hypotheses

- **RQ1 H1:** Some types of digital distraction occur significantly more frequently than others.
- **RQ2 H1:** Higher context-switching frequency and multitasking are associated with higher perceived cognitive load and mental fatigue. In the controlled task, the interrupted condition is expected to produce higher cognitive load than the focused condition.
- **RQ3 H1:** Higher perceived cognitive load is associated with more frequent and more intense academic procrastination.

The questionnaire part is interpreted as **association**, not proof of causation. Stronger causal interpretation is limited to the controlled focused-vs-interrupted comparison.

## Repository Structure

```text
procrastination-it-students/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── REPRODUCIBILITY_CHECKLIST.md
│
├── configs/
│   └── analysis_config.json
├── data/
│   ├── README.md
│   ├── raw/
│   │   ├── questionnaire_template.csv
│   │   └── controlled_task_template.csv
│   └── processed/
├── docs/
│   ├── questionnaire.md
│   ├── research_design.md
│   └── git_workflow.md
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   └── 02_statistical_analysis.ipynb
├── scripts/
│   └── run_analysis.py
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py
│   └── analysis.py
└── results/
    ├── README.md
    ├── figures/
    └── tables/
```

## System Requirements

- Python **3.11**
- Windows 10/11, macOS, or Linux
- 4 GB RAM minimum
- No GPU is required
- JupyterLab for notebook execution

This project does not require CUDA, PyTorch, or a dedicated GPU because the planned analysis is statistical rather than deep-learning based.

## Quickstart & Reproducibility Guide

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
jupyter lab
```

### macOS / Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate && pip install -r requirements.txt
jupyter lab
```

After JupyterLab opens:

1. Run `notebooks/01_data_preparation.ipynb`
2. Run `notebooks/02_statistical_analysis.ipynb`

The notebooks are designed to stop safely and explain what is missing if real research data have not been added yet.

## Data Files

Raw participant data are **not committed to GitHub**.

Use the templates in `data/raw/`:

- `questionnaire_template.csv`
- `controlled_task_template.csv`

Create local copies for real data collection. The `.gitignore` prevents accidental upload of participant datasets.

## Main Variables

### RQ1
- Digital distraction type
- Distraction frequency
- Habit strength
- Task complexity
- Study format
- Device setup
- Academic motivation

### RQ2
- Context-switching frequency
- Background multitasking
- Focused vs interrupted condition
- Cognitive Load Index (CLI)
- Mental fatigue
- Task accuracy
- Completion time
- Programming experience
- Sleep quality

### RQ3
- Cognitive Load Index (CLI)
- Procrastination Index (PI)
- Unrelated-task switching
- Motivation
- Task difficulty / importance
- Deadline proximity
- Sleep
- Overall workload

## Evaluation Metrics

| Metric | Role | Interpretation |
|---|---|---|
| Distraction frequency | Primary, RQ1 | Identifies common distraction types |
| Context Switch Rate | Primary, RQ2 | Attention switches per hour |
| Cognitive Load Index (CLI) | Primary, RQ2/RQ3 | Mean of four 1–5 cognitive-load items |
| Procrastination Index (PI) | Primary, RQ3 | Mean of four 1–5 procrastination items |
| Spearman rho | Primary statistical | Association between ordinal/behavioral variables |
| Paired t-test / Wilcoxon | Primary statistical | Focused vs interrupted comparison |
| Effect size | Secondary | Practical size of the condition difference |
| Cronbach's alpha | Quality check | Internal consistency of multi-item indices |

## Planned Statistical Analysis

- **RQ1:** descriptive statistics + Friedman test across distraction categories.
- **RQ2 survey:** Spearman correlation; optional multiple regression with control variables.
- **RQ2 controlled task:** paired t-test if the difference scores are approximately normal; otherwise Wilcoxon signed-rank test.
- **RQ3:** Spearman correlation + multiple regression including relevant control variables.
- Statistical significance threshold: **alpha = 0.05**.
- Results should be reported with descriptive statistics and effect size, not p-values alone.

## Expected Results / Benchmark Table

The table below is intentionally a placeholder. It must be filled only after real data are collected and analyzed.

| Research Question | Main Metric | Expected Output | Final Value |
|---|---|---|---|
| RQ1 | Distraction frequency | Ranking of the most common digital distractions | TBD |
| RQ2 | Spearman rho | Direction and strength of switching-load association | TBD |
| RQ2 controlled task | Delta CLI / p-value / effect size | Focused vs interrupted difference | TBD |
| RQ3 | Spearman rho / regression coefficient | Association between cognitive load and procrastination | TBD |
| Scale quality | Cronbach's alpha | Internal consistency of CLI and PI | TBD |

## Reproducibility Notes

- The questionnaire structure is fixed before final analysis.
- The controlled-task timing is standardized.
- The order of focused/interrupted conditions should be counterbalanced.
- Hypotheses should not be changed after inspecting final results.
- Raw participant data must remain private.
- Processed/anonymized data may be shared only if permitted by the research context.

## Citation

```bibtex
@misc{mashat_sultan_2026_procrastination,
  author       = {Mashat, Bekzhan and Sultan, Nursultan},
  title        = {Procrastination Triggers in the Digital Environment:
                  How Context Switching and Micro-Habits Affect the Concentration of IT Students},
  year         = {2026},
  institution  = {Narxoz University},
  note         = {Research Methods student project}
}
```

## License

The source code in this repository is released under the **MIT License**.

Participant-level research data are not covered by the software license and are not included in the public repository.
