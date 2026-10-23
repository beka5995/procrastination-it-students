# Procrastination Triggers in the Digital Environment

## How Context Switching and Micro-Habits Affect the Concentration of IT Students

**Authors:** Mashat Bekzhan, Nursultan Sultan  
**Course:** Research Methods  
**Group:** SCOM3001-ENG-9  
**University:** Narxoz University  
**License:** MIT (code)

> **Current assessment stage (Task 3):** Research Results, Data Analysis, and Scientific Visualization. The repository contains the required processing pipeline, executed notebook, statistical summaries, domain model, and publication-ready figures.

> **Data transparency:** `data/raw/test_run.jsonl` is a deterministic synthetic pilot dataset used only to validate reproducibility. It is not empirical participant data and must not be presented as real findings about students.

## Project Overview

This quantitative research studies how digital distractions and context switching are related to cognitive load, concentration, and academic procrastination among IT students.

The current controlled analysis focuses on **RQ2b**, comparing two within-subject conditions:
- **Focused baseline:** notifications disabled and no unrelated switching.
- **Interrupted condition:** a comparable technical task with standardized interruption signals.

The pipeline filters warm-up rows, tracks task-error rate as a guardrail, calculates descriptive statistics and bootstrapped confidence intervals, and exports scientific figures in PDF and 300 DPI PNG formats.

## Research Questions

**RQ1.** Which disruptive digital habits are most common among IT students during academic and practical tasks?

**RQ2.** How do frequent context switching and multitasking affect perceived cognitive load and mental fatigue while students write code or solve algorithmic problems?

**RQ3.** How is cognitive overload caused by digital distractions related to the transition from academic work to academic procrastination?

### RQ2 hypotheses

**RQ2a — association**
- **H0a:** There is no positive association between context-switch frequency and CLI (`Spearman ρ ≤ 0`).
- **H1a:** Higher context-switch frequency is positively associated with higher CLI (`Spearman ρ > 0`).

**RQ2b — controlled comparison**
- **H0b:** The mean paired difference is not positive (`Delta CLI ≤ 0`).
- **H1b:** The interrupted condition produces higher CLI (`Delta CLI > 0`).

The bundled pilot analysis evaluates the **RQ2b workflow**. It does not provide empirical evidence for RQ2a.

Primary metric:

`Delta CLI = CLI(interrupted) - CLI(focused)`

## Repository Structure

```text
procrastination-it-students/
├── configs/
│   └── research_analysis_config.json
├── data/
│   ├── raw/
│   │   ├── README.md
│   │   └── test_run.jsonl
│   └── processed/
│       └── metrics_summary.csv
├── docs/
│   ├── methodology_passport.md
│   └── domain_model.md
├── notebooks/
│   └── 01_data_analysis.ipynb
├── reports/
│   ├── report.md
│   └── figures/
│       ├── fig1_cognitive_load_comparison.pdf
│       ├── fig1_cognitive_load_comparison.png
│       ├── fig2_completion_time_boxplot.pdf
│       └── fig2_completion_time_boxplot.png
├── results/
│   └── analysis_statistics.json
├── scripts/
│   └── validate.py
├── src/
│   ├── process_data.py
│   └── visualize.py
├── .gitignore
├── requirements.txt
└── README.md
```

## System Requirements

- Python 3.11
- Windows 10/11, macOS, or Linux
- No GPU required

## Quickstart

From the repository root:

```bash
python -m pip install -r requirements.txt
python src/process_data.py
python src/visualize.py
python scripts/validate.py
```

Then open:

```text
notebooks/01_data_analysis.ipynb
```

and use **Restart Kernel and Run All**.


## Data Processing and Statistical Rules

1. Raw records are read from `data/raw/test_run.jsonl`.
2. Rows with `phase = warmup` are removed before evaluation statistics.
3. Task-error rows remain available for guardrail reporting but are excluded from the primary paired comparison.
4. For each condition, the pipeline reports mean, SD, median, p25, p75, p95, p99, and a bootstrapped 95% CI around the median.
5. The paired CLI comparison uses participants with valid measurements in both conditions.
6. Random seed is fixed at **42**.
7. Statistical alpha is **0.05**.

## Results and Discussion

### Synthetic pilot benchmark

| Metric | Focused baseline | Interrupted condition |
|---|---:|---:|
| Cognitive Load Index (1–5), Median (p25–p75) | 2.23 (2.05–2.45) | 2.71 (2.53–3.19) |
| Completion Time (s), Median (p25–p75) | 695.2 (659.1–749.3) | 801.0 (730.3–846.1) |
| Accuracy (%), Median (p25–p75) | 88.0 (85.5–92.5) | 87.7 (78.9–93.5) |
| Context Switches (count), Median (p25–p75) | 1.0 (0.0–2.0) | 6.0 (3.8–7.0) |
| Task Error Rate (%) | 3.3 | 6.7 |

The synthetic pilot produced **27 complete pairs** after guardrail filtering. Mean Delta CLI was **0.52** with a bootstrapped 95% CI of **[0.37, 0.66]**.

The paired CLI differences passed the normality check (`Shapiro-Wilk p = 0.442`), so the pipeline selected a **one-sided paired t test** (`interrupted > focused`) for this pilot dataset.

**Interpretation boundary:** these values demonstrate the analysis procedure only. They do not support empirical claims about the real student population until the synthetic file is replaced with actual anonymized observations collected under the approved procedure.

## Scientific Figures

### Figure 1 — Cognitive Load Index with 95% CI

![Cognitive Load Plot](reports/figures/fig1_cognitive_load_comparison.png)

The y-axis reports the CLI scale (1–5). Individual paired observations are shown with the group median and bootstrapped 95% CI.

### Figure 2 — Completion-Time Distribution with 95% CI

![Completion Time Plot](reports/figures/fig2_completion_time_boxplot.png)

The y-axis reports seconds. Boxplots show dispersion, while overlaid markers show the median and bootstrapped 95% CI. Distinct hatching and markers improve monochrome readability.

Both figures are exported as vector `.pdf` and raster `.png` at 300 DPI.

## Domain Model

The research-pipeline model is available at [`docs/domain_model.md`](docs/domain_model.md). It shows the path from a participant session through metric collection, raw JSONL storage, processing, notebook analysis, visualization, and reporting.

## Reproducibility

The notebook is designed to run sequentially from top to bottom and includes:
- explanatory Markdown;
- fixed random seed;
- raw-data ingestion;
- warm-up filtering;
- statistical aggregation;
- p95/p99 and 95% CI;
- guardrail error-rate reporting;
- paired CLI comparison;
- visible figure outputs.

Reusable logic is kept in `src/process_data.py` and `src/visualize.py`.

## Submission Criteria Coverage

| Criterion | Evidence in repository |
|---|---|
| Data processing and statistics | Warm-up filtering, median, p25/p75, p95/p99, bootstrapped 95% CI, error-rate guardrail |
| Scientific visualization | Explicit units/scales, 95% CI, distinct markers/hatching, PDF + 300 DPI PNG |
| Reproducible notebook | Sequential notebook with fixed seed and visible outputs |
| Domain model | `docs/domain_model.md` |
| Repository hygiene | `.gitignore`, modular `src/`, pinned requirements, no private participant data |

## Real Data Privacy

For real data:
- use anonymous participant codes such as `P01`;
- do not store names or student IDs in GitHub;
- do not commit credentials, private messages, or identifiable records;
- keep any participant-code mapping outside the public repository.

## Citation

```bibtex
@misc{mashat_sultan_2026_procrastination,
  author      = {Mashat, Bekzhan and Sultan, Nursultan},
  title       = {Procrastination Triggers in the Digital Environment:
                  How Context Switching and Micro-Habits Affect the Concentration of IT Students},
  year        = {2026},
  institution = {Narxoz University},
  note        = {Research Methods student project}
}
```

## License

Source code is released under the MIT License. Participant-level research data are not covered by the software license.
