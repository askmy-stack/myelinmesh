# Release Checklist

## Quality

- [ ] `pytest` passes
- [ ] `ruff check .` passes
- [ ] `ruff format --check .` passes
- [ ] `mypy src` passes
- [ ] generated JSON Schema is unchanged after regeneration
- [ ] examples validate and demo succeeds

## Compatibility

- [ ] schema change classified as patch, minor, or major
- [ ] migrations documented when needed
- [ ] adapters tested against representative producer outputs

## Security and data

- [ ] no secrets, PII, PHI, proprietary traces, or private URLs
- [ ] dependency and CodeQL checks reviewed
- [ ] security limitations updated

## Documentation

- [ ] changelog updated
- [ ] version updated in package and citation file
- [ ] roadmap status updated
- [ ] release notes describe limitations

## Publication

- [ ] exact project and package names rechecked
- [ ] signed Git tag created
- [ ] GitHub release published
- [ ] package publication tested in a clean environment
