# Reproducibility & Audit Checklist

A reviewer should be able to check the following points in under two minutes:

- [ ] **Repository structure is clear.** README, source code, notebooks, configuration, data templates, and results folders are present.
- [ ] **Environment is reproducible.** Python 3.11 is specified and package versions are pinned in `requirements.txt`.
- [ ] **Private data are protected.** Real participant files are excluded by `.gitignore`; only empty templates are committed.
- [ ] **Analysis procedure is documented.** RQ1–RQ3, variables, metrics, statistical tests, and alpha = 0.05 are described in the README and research design.
- [ ] **Execution path is simple.** A reviewer can install dependencies and run the two notebooks in order.
