# MyelinMesh Project Charter

## Mission

Build an open, interoperable evidence layer that helps AI engineers make reliability claims traceable, testable, and reusable across development, deployment, and recovery.

## Core thesis

AI systems repeatedly lose reliability knowledge because changes, tests, traces, incidents, and recoveries are stored in incompatible formats. A shared evidence record and provenance-aware mesh can reduce repeated investigation, improve test selection, and make uncertainty visible.

## Principles

1. **Evidence before explanation.** Explanations must point to records, measurements, or controlled experiments.
2. **Provenance by default.** Every claim must identify its source, producer, version, and relevant environment.
3. **Uncertainty is first-class.** Similarity, association, diagnosis, and causality are different concepts.
4. **Local-first and open.** The core must work without a hosted service.
5. **Adapters over replacement.** Preserve MCAP, OpenTelemetry, Git, benchmark, and experiment artifacts; index rather than duplicate them unnecessarily.
6. **Version-aware reuse.** Evidence must record where it applies and when it should be considered stale.
7. **Human review remains visible.** Human judgments are evidence with provenance, not unquestionable truth.
8. **No certification claims.** MyelinMesh supports assurance work but does not certify safety or regulatory compliance.

## Initial users

- Reliable-AI researchers
- Agent infrastructure engineers
- Robotics and Physical AI teams
- Open-source maintainers building evaluation and incident tools
- ML platform teams studying model and system regressions

## Initial outputs

- MER schema and JSON Schema
- Python SDK and CLI
- Local evidence store
- Three first-party adapters
- Reproducible example corpus
- Research benchmark plan

## Success criteria for the first six months

- Three external producers successfully emit valid MER records.
- At least 1,000 records can be ingested and queried locally.
- Schema compatibility is maintained through documented migrations.
- A benchmark demonstrates measurable improvement in one use case: physical test selection, tool-regression prioritization, or incident retrieval.
- External contributors add at least two adapters or datasets.
