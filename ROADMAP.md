# Roadmap

Current release track: **v0.2.0 — Interoperability**. The v0.1.0 foundation
and the first compatibility, batch-ingestion, and migration slices are landed;
the remaining v0.2 work is tracked in GitHub milestone issues.

## v0.1.0 — Foundation

- [x] Project charter and architecture
- [x] MER v0.1 schema
- [x] Pydantic models and validator
- [x] Deterministic content hashing
- [x] Local JSON + SQLite store
- [x] CLI: init, validate, ingest, list, show, search, stats
- [x] Initial adapters and examples
- [x] CI, contribution, security, governance, and research documents

## v0.2.0 — Interoperability

- [x] Formal schema compatibility policy
- [x] Schema migration command
- [x] OpenTelemetry trace adapter
- [x] GitHub change and pull-request adapter
- [x] ROS 2/MCAP metadata adapter
- [x] Artifact manifests with checksums and media types
- [x] Batch ingestion and deduplication
- [x] Signed provenance envelopes

## v0.3.0 — Evidence retrieval

- [ ] Structured filters for versions, systems, failure classes, and domains
- [ ] Optional PostgreSQL backend
- [ ] Optional pgvector similarity index
- [ ] Applicability filters before similarity ranking
- [ ] Contradiction and duplicate detection
- [ ] Evidence freshness and decay policies
- [ ] Minimal web explorer

## v0.4.0 — Project integrations

- [ ] Tool-Semantics usage-weighted change risk
- [ ] MyelinMesh history-aware scenario ranking
- [ ] Parallax similar-incident and recovery retrieval
- [ ] Bidirectional links from source reports to MER records
- [ ] Shared GitHub Action for publishing evidence

## v0.5.0 — Open reliability corpus

- [ ] Public dataset contribution specification
- [ ] Synthetic and real evidence labels
- [ ] Data cards and licensing metadata
- [ ] Redaction and privacy pipeline
- [ ] Dataset snapshots on object storage and Hugging Face
- [ ] Benchmark splits that prevent incident leakage

## v0.6.0 — Active evidence acquisition

- [ ] Information-gain test recommendations
- [ ] Hypothesis-separating experiment selection
- [ ] Recovery applicability and decay estimation
- [ ] Cross-domain evidence representation studies
- [ ] Human-review calibration research

## Explicitly deferred

- Automated safety certification
- Autonomous production recovery execution
- Universal causal inference
- Large distributed infrastructure before local benchmarks justify it
