#!/usr/bin/env bash
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required." >&2
  exit 1
fi

git init
git branch -M main
git add .
if ! git diff --cached --quiet; then
  git commit -m "feat: initialize MyelinMesh"
fi

gh repo create askmy-stack/MyelinMesh \
  --public \
  --description "Open-source reliability evidence mesh for AI systems—connecting changes, tests, traces, failures, diagnoses, and recoveries." \
  --source=. \
  --remote=origin \
  --push
