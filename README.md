# Procrastination Triggers in the Digital Environment

**How Context Switching and Micro-Habits Affect the Concentration of IT Students**

**Authors:** Mashat Bekzhan, Nursultan Sultan  
**Course:** Research Methods  
**Group:** SCOM3001-ENG-9  
**University:** Narxoz University  
**Status:** Task 2 — methodology and reproducible measurement pipeline  
**License:** MIT (code)

---

## Project Overview

This research studies how digital distractions and context switching are related to cognitive load, concentration, and academic procrastination among IT students. The design continues our Task 1 and SS5 work.

The project has two quantitative parts:

1. **Questionnaire study** — measures common digital distractions, context switching, cognitive load, and procrastination.
2. **Controlled coding task** — compares a focused condition with an interrupted condition during a short programming / algorithmic task.

The repository currently contains a **synthetic sample dataset** only for checking that the pipeline works before real data collection. Sample values are not research findings.

## Research Aim

The aim is to identify common disruptive digital habits among IT students and examine how context switching and multitasking are related to cognitive load, reduced concentration, and academic procrastination.

## Research Questions

**RQ1.** Which disruptive digital habits are most common among IT students during academic and practical tasks?

**RQ2.** How do frequent context switching and multitasking affect perceived cognitive load and mental fatigue while students write code or solve algorithmic problems?

**RQ3.** How is cognitive overload caused by digital distractions related to the transition from academic work to academic procrastination?

## Main Hypothesis for the Controlled Comparison

- **H0:** Perceived cognitive load does not significantly differ between the focused and interrupted conditions.
- **H1:** Perceived cognitive load is higher in the interrupted condition than in the focused condition.

The questionnaire analyses are interpreted as associations. Stronger causal interpretation is limited to the short controlled comparison.

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
│   ├── sample/
│   │   ├── questionnaire_sample.csv
│   │   └── controlled_task_sample.csv
│   ├── raw/
│   └── processed/
├── docs/
│   ├── methodology_passport.md
│   ├── questionnaire.md
│   ├── research_design.md
│   └── git_workflow.md
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   └── 02_statistical_analysis.ipynb
├── scripts/
│   └── run_analysis.py
├── src/
│   ├── main.py
│   ├── data_cleaning.py
│   └── analysis.py
└── results/
    ├── sample/
    ├── figures/
    └── tables/
```

## System Requirements

- Python **3.11**
- Windows 10/11, macOS, or Linux
- 4 GB RAM minimum
- No GPU is required

The analysis is statistical, so CUDA, PyTorch, and model weights are not needed.

## Quickstart — Task 2 Sample Run

### Windows PowerShell

Run these commands from the project folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src\main.py
```

The third command should print `Sample pipeline completed successfully` and create:

```text
results/sample/sample_results.json
results/sample/run_log.txt
```

### macOS / Linux

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/main.py
```

## Experiment Configuration

`configs/analysis_config.json` stores the parameters used by the sample pipeline:

- significance level (`alpha = 0.05`);
- expected sample sizes;
- paths to sample data and output;
- CLI and PI item lists;
- distraction-frequency items;
- data-quality guardrails.

## Variables and Metrics

For the controlled part of RQ2:

- **Independent variable:** focused vs interrupted condition.
- **Primary dependent variable:** Cognitive Load Index (CLI).
- **Secondary dependent variables:** mental fatigue, task accuracy, completion time.
- **Controls:** session duration, comparable task difficulty, programming experience, sleep, and counterbalanced condition order.

For the questionnaire part, context switching and digital-distraction measures are observed predictors rather than experimentally assigned variables.

### Primary Metric

**Delta CLI = CLI(interrupted) − CLI(focused)**

A positive value means higher reported cognitive load in the interrupted condition.

### Guardrail Metrics

- missing-data rate ≤ 10%;
- Likert values remain within 1–5;
- no duplicate questionnaire participant IDs;
- target Cronbach's alpha ≥ 0.70 for the CLI and PI scales on the real dataset.

### Baseline

**Focused condition (B0):** 20-minute technical task with notifications disabled and no unrelated switching.

**Interrupted condition (C1):** comparable task with standardized interruption signals.

## Planned Measurements / Benchmark Table

| Part | Metric | Method | Expected output |
|---|---|---|---|
| RQ1 | Distraction frequency | Descriptive statistics + Friedman test | Ranking and difference across distraction types |
| RQ2 survey | Context switching vs CLI | Spearman rho | Direction and strength of association |
| RQ2 controlled | Delta CLI | Paired t-test or Wilcoxon | Focused vs interrupted difference |
| RQ2 controlled | Effect size | Paired Cohen's d | Practical magnitude of the difference |
| RQ3 | CLI vs PI | Spearman rho | Association between cognitive load and procrastination |
| Data quality | Cronbach's alpha / missing rate | Reliability + quality checks | Scale consistency and clean input |

## Test Sample

`data/sample/` contains small **synthetic** files used only for a smoke test. They make it possible for a reviewer to verify the pipeline before Week 7 without using real participant data.

The executable script is:

```text
src/main.py
```

It reads the experiment configuration, cleans the sample data, calculates the planned statistics, checks guardrails, and writes a JSON result plus a short log.

## Real Data Privacy

Real participant-level data must not be pushed to the public repository. `.gitignore` excludes local raw and processed data. Names, student IDs, passwords, private messages, and message content are not collected.

## Methodology Passport

The Task 2 methodology card is available here:

```text
docs/methodology_passport.md
```

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

The source code is released under the **MIT License**. Participant-level research data are not covered by the software license and are not included in the public repository.
