# Reproducibility & Audit Checklist

A reviewer can check the repository in under two minutes:

- [ ] **Environment:** Python 3.11 is specified and all packages in `requirements.txt` use exact version pins.
- [ ] **Configuration:** `configs/analysis_config.json` contains paths, alpha, sample sizes, metric settings, and data-quality guardrails.
- [ ] **Executable measurement tool:** `python src/main.py` reads the sample files and writes `results/sample/sample_results.json` plus `run_log.txt`.
- [ ] **Test data:** `data/sample/` contains only synthetic micro-data; real participant data are excluded by `.gitignore`.
- [ ] **Documentation:** README includes research questions, structure, system requirements, 2–3 command Quickstart, planned measurements, citation, and license.
