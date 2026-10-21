# Task 3 Data Note

`test_run.jsonl` in this package is a **deterministic synthetic pilot dataset** generated with random seed 42.

It exists so that:
- the full Task 3 pipeline can be executed and reviewed;
- warm-up filtering can be demonstrated;
- statistics and confidence intervals can be checked;
- the notebook can remain in a fully executed state;
- the required PDF/PNG figures can be generated reproducibly.

It is **not** empirical participant data and must not be described as real findings about IT students.

For a final empirical submission, replace the synthetic JSONL file with anonymized Week 7-8 observations that use the same schema, then rerun:

```bash
python src/process_data.py
python src/visualize.py
```

After that, open `notebooks/01_data_analysis.ipynb` and use **Restart Kernel and Run All**.
