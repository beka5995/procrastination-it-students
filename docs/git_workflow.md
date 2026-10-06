# Git Workflow

## First Repository Setup

```bash
git init
git checkout -b main
git add .
git commit -m "Initial research repository"
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

## Team Workflow

Before starting new work:

```bash
git pull origin main
```

After making a small, understandable change:

```bash
git add .
git commit -m "Update questionnaire draft"
git push origin main
```

Use short commit messages that describe one change. Avoid committing real participant data, passwords, temporary files, or large unrelated files.
