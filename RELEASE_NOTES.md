# Task 3 Release Notes

Suggested release tag: `v0.3-task3`

Included:
- warm-up-filtered JSONL processing;
- aggregated statistics with median, p95, p99, and bootstrapped 95% CI;
- error-rate guardrail;
- fully executed Jupyter Notebook;
- C4-style domain model;
- two scientific figures in PDF and 300 DPI PNG;
- updated README and LMS-ready Markdown report.

Before tagging a final empirical release, replace synthetic pilot data with real anonymized Week 7-8 observations if those observations are available.

Suggested commands:

```bash
git add .
git commit -m "Add Task 3 analysis, statistics, and scientific figures"
git push origin main
git tag -a v0.3-task3 -m "Task 3 research results and visualization"
git push origin v0.3-task3
```
