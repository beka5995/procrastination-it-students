from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

required = [
    "data/raw/test_run.jsonl",
    "data/processed/metrics_summary.csv",
    "docs/methodology_passport.md",
    "docs/domain_model.md",
    "notebooks/01_data_analysis.ipynb",
    "reports/figures/fig1_cognitive_load_comparison.pdf",
    "reports/figures/fig1_cognitive_load_comparison.png",
    "reports/figures/fig2_completion_time_boxplot.pdf",
    "reports/figures/fig2_completion_time_boxplot.png",
    "src/process_data.py",
    "src/visualize.py",
    "README.md",
    "requirements.txt",
    "environment.yml",
    ".gitignore",
]

missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit("Missing required research artifacts:\n- " + "\n- ".join(missing))

# Accept the current or renamed analysis configuration/statistics file.
config_files = list((ROOT / "configs").glob("*analysis_config.json"))
if not config_files:
    raise SystemExit("No analysis configuration JSON found in configs/.")

statistics_files = list((ROOT / "results").glob("*statistics.json"))
if not statistics_files:
    raise SystemExit("No analysis statistics JSON found in results/.")

# Ensure the Conda file mirrors all exact pip pins used by requirements.txt.
requirements = [
    line.strip()
    for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]
environment_text = (ROOT / "environment.yml").read_text(encoding="utf-8")
missing_pins = [pin for pin in requirements if pin not in environment_text]
if missing_pins:
    raise SystemExit("environment.yml is missing pinned dependencies:\n- " + "\n- ".join(missing_pins))

# Check that the saved notebook is executed sequentially and contains no error outputs.
notebook = json.loads((ROOT / "notebooks/01_data_analysis.ipynb").read_text(encoding="utf-8"))
code_cells = [cell for cell in notebook.get("cells", []) if cell.get("cell_type") == "code"]
execution_counts = [cell.get("execution_count") for cell in code_cells]
expected_counts = list(range(1, len(code_cells) + 1))
if execution_counts != expected_counts:
    raise SystemExit(
        f"Notebook execution counts are not sequential: {execution_counts}; expected {expected_counts}."
    )

notebook_errors = [
    output
    for cell in code_cells
    for output in cell.get("outputs", [])
    if output.get("output_type") == "error"
]
if notebook_errors:
    raise SystemExit(f"Notebook contains {len(notebook_errors)} saved error output(s).")

# Check figure files are present and non-empty.
for suffix in ("*.png", "*.pdf"):
    for figure in (ROOT / "reports/figures").glob(suffix):
        if figure.stat().st_size == 0:
            raise SystemExit(f"Empty figure file: {figure}")

# Basic repository hygiene rules should remain explicit.
gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
for rule in (".venv/", "__pycache__/", ".ipynb_checkpoints/", ".env", "*.py[cod]"):
    if rule not in gitignore:
        raise SystemExit(f".gitignore is missing expected rule: {rule}")

# The domain model must remain directly renderable on GitHub.
if "```mermaid" not in (ROOT / "docs/domain_model.md").read_text(encoding="utf-8"):
    raise SystemExit("Domain model does not contain a Mermaid diagram.")

print("Research artifact validation PASSED.")
print(f"Checked {len(required)} required artifacts, environment pins, notebook outputs, figures, and hygiene rules.")
