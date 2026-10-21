from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

required = [
    "data/raw/test_run.jsonl",
    "data/processed/metrics_summary.csv",
    "docs/domain_model.md",
    "notebooks/01_data_analysis.ipynb",
    "reports/figures/fig1_cognitive_load_comparison.pdf",
    "reports/figures/fig1_cognitive_load_comparison.png",
    "reports/figures/fig2_completion_time_boxplot.pdf",
    "reports/figures/fig2_completion_time_boxplot.png",
    "src/process_data.py",
    "src/visualize.py",
    "README.md",
    ".gitignore",
]

missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit("Missing required Task 3 artifacts:\\n- " + "\\n- ".join(missing))

for png in (ROOT / "reports/figures").glob("*.png"):
    if png.stat().st_size == 0:
        raise SystemExit(f"Empty PNG: {png}")

print("Task 3 artifact validation PASSED.")
print(f"Checked {len(required)} required artifacts.")
