# Research Results, Data Analysis, and Scientific Visualization

**Project:** Procrastination Triggers in the Digital Environment: How Context Switching and Micro-Habits Affect the Concentration of IT Students  
**Authors:** Mashat Bekzhan, Nursultan Sultan  
**Group:** SCOM3001-ENG-9  
**Course:** Research Methods  
**Repository:** https://github.com/beka5995/procrastination-it-students

## 1. Analysis Scope

The practical analysis focuses on **RQ2b**, the controlled within-subject comparison between a focused baseline and an interrupted condition. The primary metric is Cognitive Load Index (CLI), measured on a 1–5 scale. **RQ2a** remains a separate observational association question between context-switch frequency and CLI.

The repository contains a **synthetic pilot dataset** with anonymous IDs (`P01–P30`) to demonstrate and verify the processing workflow. These records are not empirical observations and are not interpreted as evidence about real IT students.

## 2. Data Ingestion and Warm-up Filtering

The raw file is stored as `data/raw/test_run.jsonl`.

- Raw rows: **90**
- Warm-up rows filtered: **30**
- Evaluation rows before guardrail filtering: **60**
- Evaluation rows after task-error filtering: **57**
- Complete focused/interrupted pairs for the primary CLI comparison: **27**

Warm-up rows are excluded before evaluation statistics are calculated.

## 3. Statistical Aggregation

For each condition and metric, the processing module calculates:
- mean and standard deviation;
- median;
- p25 and p75;
- p95 and p99;
- bootstrapped 95% confidence interval around the median.

Bootstrap resampling uses **5,000 resamples** with fixed random seed **42**. The task-error rate is tracked as the guardrail metric.

### Benchmark summary

| Metric | Focused baseline | Interrupted condition |
|---|---:|---:|
| Cognitive Load Index (1–5), Median (p25–p75) | 2.23 (2.05–2.45) | 2.71 (2.53–3.19) |
| Completion Time (s), Median (p25–p75) | 695.2 (659.1–749.3) | 801.0 (730.3–846.1) |
| Accuracy (%), Median (p25–p75) | 88.0 (85.5–92.5) | 87.7 (78.9–93.5) |
| Context Switches (count), Median (p25–p75) | 1.0 (0.0–2.0) | 6.0 (3.8–7.0) |
| Task Error Rate (%) | 3.3 | 6.7 |

## 4. Primary Paired Comparison

**Delta CLI = CLI(interrupted) - CLI(focused)**

For the bundled synthetic pilot:
- Mean Delta CLI: **0.52**
- Median Delta CLI: **0.41**
- Bootstrapped 95% CI for mean Delta CLI: **[0.37, 0.66]**
- Cohen's dz: **1.32**
- Shapiro-Wilk normality p-value: **0.442**
- Selected inferential test: **one-sided paired t test (interrupted > focused)**
- One-sided test p-value: **1.433e-07**

These values verify that the statistical workflow functions correctly; they are not empirical findings about students.

## 5. Scientific Visualization

Two publication-ready figures are stored under `reports/figures/`.

**Figure 1:** Cognitive Load Index under focused and interrupted conditions. The y-axis states the CLI scale (1–5), and the plot includes paired observations, the condition median, and bootstrapped 95% CI.

**Figure 2:** Task Completion Time distribution. The y-axis is measured in seconds. Boxplots represent dispersion, while overlaid points and error bars show the median and bootstrapped 95% CI.

Both figures use a perceptually uniform palette, distinct markers/hatching, and are exported as vector PDF and 300 DPI PNG.

## 6. Domain Model

`docs/domain_model.md` contains a C4-style research-pipeline model showing the controlled task, metric collection, raw JSONL store, processing module, notebook analysis, visualization module, and report outputs.

## 7. Reproducibility

The notebook `notebooks/01_data_analysis.ipynb` is designed for sequential execution and preserves visible outputs. It covers data loading, warm-up filtering, statistical aggregation, p95/p99, 95% CI, guardrail error rate, paired CLI comparison, figure generation, and limitations.

Reusable logic is refactored into `src/process_data.py` and `src/visualize.py`. Exact package pins are provided in `requirements.txt`, with a matching Python 3.11 Conda setup in `environment.yml`.

## 8. Limitations

The bundled dataset is synthetic and therefore cannot validate the substantive research hypotheses. It validates the reproducibility, statistics, and visualization workflow for RQ2b. It provides no empirical evidence for RQ1, RQ2a, or RQ3. Final empirical conclusions require anonymized real observations collected under the approved procedure.

A further limitation of the planned empirical study is convenience sampling from a limited student population, which restricts generalizability.

## 9. Conclusion

The repository provides a reproducible path from raw JSONL records to warm-up-filtered statistics, uncertainty estimates, scientific figures, a formal domain model, and a fully executed Jupyter Notebook. The workflow is ready to be rerun on real anonymized observations without changing the analysis structure.
