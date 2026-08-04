# Start Here

## 1. Create the repository

```bash
git init
git branch -M main
git add .
git commit -m "feat: initialize MyelinMesh"

gh auth login
gh repo create askmy-stack/MyelinMesh \
  --public \
  --description "Open-source reliability evidence mesh for AI systems—connecting changes, tests, traces, failures, diagnoses, and recoveries." \
  --source=. \
  --remote=origin \
  --push
```

## 2. Configure repository metadata

Suggested GitHub topics:

```text
ai-reliability
reliable-ai
physical-ai
ai-agents
observability
provenance
failure-analysis
mcp
robotics
ros2
mlops
open-source
```

Enable:

- Issues
- Discussions
- Security advisories
- Dependabot alerts
- Branch protection for `main`
- Required `CI / test` checks
- Squash merging

## 3. Run locally

```bash
./scripts/bootstrap.sh
source .venv/bin/activate
make demo
```

## 4. First development issues

1. Add a batch adapter command and adapter discovery registry.
2. Add schema migration tests and a compatibility policy checker.
3. Add OpenTelemetry JSON export ingestion.
4. Add GitHub pull-request change evidence ingestion.
5. Add artifact checksum verification.
6. Build the first history-aware ImpactForge benchmark fixture.
7. Build usage-weighted Tool-Semantics severity fixtures.
8. Build Parallax incident-retrieval benchmark fixtures.

## 5. First release target

Publish `v0.1.0` only after:

- CI passes on Python 3.11–3.13.
- JSON Schema matches the Pydantic model.
- All examples validate.
- Security and privacy limitations are visible.
- The package installs in a clean virtual environment.
- The repository name and package name are rechecked immediately before publication.
