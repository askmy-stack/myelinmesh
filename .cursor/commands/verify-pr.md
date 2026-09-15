Perform the final pre-PR verification for the current branch.

Follow `AGENTS.md`.

Do not add new functionality.

1. Inspect `git status`.
2. Inspect the branch diff against the default branch.
3. Check for unrelated files.
4. Check for accidental secrets or credentials.
5. Inspect dependency-file changes.
6. Run repository-appropriate validation.

For Python implementation changes, validation should normally include:

```bash
python -m pytest
ruff check .
ruff format --check .
mypy -p myelinmesh
```

Run `pre-commit run --all-files` when appropriate and available. Do not claim
success for commands that were not executed.

Return sections for Scope, Validation, Security, Dependencies, Risks, and
Recommendation. The recommendation must be exactly `READY FOR PR` or `NOT READY FOR PR`.
