# Contributing

Thank you for helping build MyelinMesh.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
pytest
ruff check .
ruff format --check .
mypy src
```

## Contribution areas

- MER schema examples and validation edge cases
- Adapters for evidence producers
- Dataset cards and benchmark fixtures
- Privacy and redaction improvements
- Evidence applicability and freshness rules
- Documentation and tutorials

## Pull-request expectations

- Add or update tests.
- Explain schema changes and compatibility impact.
- Never include secrets, private traces, protected health information, or proprietary robot data.
- Mark generated or synthetic fixtures clearly.
- Preserve uncertainty rather than presenting inferred diagnoses as facts.
- Update `CHANGELOG.md` for user-visible changes.

## Schema changes

Schema fields cannot be renamed or removed in a minor release. Breaking changes require:

1. An architecture decision record.
2. A migration plan.
3. Updated JSON Schema and fixtures.
4. Compatibility tests.
5. A major schema-version increment.

## Commit style

Use conventional prefixes where practical:

- `feat:` new behavior
- `fix:` bug fix
- `docs:` documentation
- `test:` tests
- `refactor:` internal change
- `chore:` maintenance

## Reporting security issues

Do not open a public issue for sensitive vulnerabilities. Follow [SECURITY.md](SECURITY.md).
