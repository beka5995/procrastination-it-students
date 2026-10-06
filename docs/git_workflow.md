# Git Workflow

## Initial setup

```bash
git init
git checkout -b main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
```

## Normal pair workflow

Before starting work:

```bash
git pull origin main
```

After a meaningful change:

```bash
git add .
git commit -m "Add Task 2 sample pipeline"
git push origin main
```

Useful commit messages for the current Task 2 update:

- `Add methodology passport and experiment config`
- `Add synthetic sample data and runnable pipeline`
- `Update README quickstart for Task 2`

Do not commit real participant data, `.venv/`, secrets, Jupyter checkpoints, or cache files.
