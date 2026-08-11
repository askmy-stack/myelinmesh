# CLAUDE.md

Guidance for Claude Code (and other agents) working in this repository.

## Project summary

MyelinMesh is an open-source evidence layer that connects software/model
changes, agent trajectories, physical tests, runtime incidents, diagnoses,
recoveries, and human reviews into reusable reliability knowledge. It defines
a versioned record format (the **MyelinMesh Evidence Record**, or MER),
validates and content-hashes records, and stores them locally (JSON + SQLite)
behind a CLI. It does not certify safety or prove causality — it preserves
provenance and exposes uncertainty.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Common commands

All defined in `Makefile`:

| Command | Purpose |
| --- | --- |
| `make test` | `pytest --cov=myelinmesh --cov-report=term-missing` |
| `make lint` | `ruff check .` + `ruff format --check .` |
| `make format` | `ruff check --fix .` + `ruff format .` |
| `make typecheck` | `mypy src` |
| `make schema` | Regenerate `schemas/myelinmesh-evidence-record.v0.1.schema.json` from the Pydantic models |
| `make demo` | Ingest the three example MER records into an isolated `.myelinmesh-demo` store and print stats |
| `make release-gate` | `python scripts/release_gate.py` |
| `make benchmark` | `python scripts/benchmark_local.py` |
| `make clean` | Remove caches, coverage, build, and demo-store artifacts |

## CI expectations (`.github/workflows/ci.yml`)

On every push to `main` and every PR:

- `ruff check .` and `ruff format --check .`
- `mypy src`
- `pytest --cov=myelinmesh --cov-report=xml` on Python 3.11, 3.12, and 3.13
- Schema regeneration check: `scripts/export_schema.py` must produce a
  byte-identical `schemas/myelinmesh-evidence-record.v0.1.schema.json` — if
  you change `src/myelinmesh/models.py`, run `make schema` and commit the
  regenerated file.
- CodeQL analysis (`.github/workflows/codeql.yml`)

A change is not done until it passes `make lint`, `make typecheck`, and
`make test` locally — CI runs the same checks and will block merge otherwise.

## Architecture

```
Producers (GitHub · Tool-Semantics · MyelinMesh · Parallax · ROS 2 · OTel)
        │
        ▼
Adapter + validation layer (src/myelinmesh/adapters/)
        │
        ▼
MyelinMesh Evidence Record (MER) — src/myelinmesh/models.py
        │
   ┌────┴────┐
   ▼         ▼
 hashing.py  store.py (JSON + SQLite under .myelinmesh/)
        │
        ▼
 cli.py — init, validate, migrate, ingest, ingest-batch, list, search, show, stats, adapt
```

Key modules under `src/myelinmesh/`:

- `models.py` — Pydantic MER schema (source of truth; JSON Schema is generated from it).
- `hashing.py` — deterministic canonical-JSON content hashing.
- `io.py` / `store.py` — local JSON file + SQLite index persistence.
- `migrations.py` — registered, deterministic schema migration paths (`myelinmesh migrate`).
- `signing.py` — signed provenance envelopes.
- `cli.py` — Typer-based CLI entry point (`myelinmesh` console script).
- `adapters/` — one module per producer (`github.py`, `mcap.py`, `myelinmesh.py`, `otel.py`, `parallax.py`, `tool_semantics.py`), sharing `base.py` and `common.py`.

For deeper detail see `docs/architecture.md` and `docs/evidence-model.md`.
Tests live in `tests/` mirroring these modules (`test_models.py`,
`test_store.py`, `test_migrations.py`, `test_adapters.py`, `test_cli.py`,
`test_signing.py`).

## Conventions (from `CONTRIBUTING.md`)

- Add or update tests for any behavioral change.
- Update `CHANGELOG.md` for user-visible changes.
- Schema fields cannot be renamed or removed in a minor release — see
  `CONTRIBUTING.md`'s "Schema changes" section before touching `models.py` or
  the JSON Schema.
- Never commit secrets, private traces, protected health information, or
  proprietary robot data; mark generated/synthetic fixtures clearly.
- Preserve uncertainty rather than presenting inferred diagnoses as fact —
  this is a project principle (`PROJECT_CHARTER.md`), not just a style note.

## Branch / PR flow

- `main` is protected: all CI jobs must pass, and the PR branch must include
  the latest `main`.
- If a PR falls behind `main`:

  ```bash
  git fetch origin
  git rebase origin/main
  git push --force-with-lease
  ```

- For an untouched Dependabot PR, comment `@dependabot rebase` instead of
  rebasing manually.
