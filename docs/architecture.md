# Architecture

## Design goals

- Local-first operation
- Interoperable evidence records
- Provenance and version awareness
- Artifact references rather than forced duplication
- Deterministic core behavior
- Replaceable storage and retrieval backends

## Logical layers

```text
Producer systems
  Tool-Semantics · ImpactForge · Parallax · GitHub · ROS 2 · OTel
       │
       ▼
Adapters
  Parse producer-specific output and preserve source references
       │
       ▼
Validation and normalization
  Pydantic model · JSON Schema · canonical serialization · hash
       │
       ▼
Evidence storage
  records/*.json + SQLite metadata index
       │
       ▼
Retrieval
  filters · text search · future similarity and graph traversal
       │
       ▼
Consumers
  CLI · Python SDK · future REST API · source-project feedback loops
```

## Local store layout

```text
.myelinmesh/
├── records/
│   └── <evidence-id>.mer.json
├── index.sqlite3
└── store.json
```

## Storage decisions

The foundation release uses JSON and SQLite because they are transparent, portable, and require no service. PostgreSQL, pgvector, object storage, and graph backends are roadmap extensions, not initial requirements.

## Artifact handling

Large artifacts such as MCAP bags, Parquet files, videos, and OpenTelemetry exports are referenced through `ArtifactReference` objects. The local store does not automatically copy or upload them.

## Trust model

Validation proves that a record matches the schema. It does not prove:

- The source system is honest.
- The diagnosis is correct.
- The recorded environment matches production.
- An association is causal.
- A recovery is safe outside its validated conditions.

## Extension points

- `EvidenceAdapter` for producer integration
- `EvidenceStore` for alternate storage
- Future retrieval rankers
- Future signature providers
- Future policy engines
