# Reproducibility & Audit Checklist

A reviewer can verify the project with the following checks:

- [x] **Environment:** Python 3.11 is specified; `requirements.txt` uses exact pins; `environment.yml` mirrors the pinned Python dependencies for Conda.
- [x] **Methodology:** RQ1 is stated as a testable repeated-measures comparison; RQ2a association is separated from the RQ2b controlled comparison.
- [x] **Configuration:** the repository contains analysis configuration files with paths, alpha, random seed, metrics, and data-quality settings.
- [x] **Executable pipeline:** `python src/main.py` runs the sample measurement pipeline and writes a JSON result plus run log.
- [x] **Analysis pipeline:** `python src/process_data.py` filters warm-up rows, reports guardrail error rate, and produces descriptive statistics and the paired Delta CLI comparison.
- [x] **Notebook:** `notebooks/01_data_analysis.ipynb` is sequentially executable with fixed seed 42 and visible outputs.
- [x] **Scientific figures:** `python src/visualize.py` exports vector PDF and 300 DPI PNG figures with explicit scales and 95% confidence intervals.
- [x] **Domain model:** `docs/domain_model.md` documents the controlled-task data path and metric collection points.
- [x] **Data transparency:** bundled public data are explicitly synthetic pilot/sample data; they are not presented as empirical student findings.
- [x] **Repository hygiene:** `.venv/`, caches, notebook checkpoints, credentials, and private participant data are excluded from version control.
