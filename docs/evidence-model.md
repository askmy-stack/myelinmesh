# MyelinMesh Evidence Record

The **MyelinMesh Evidence Record (MER)** is the atomic interoperable unit.

## Sections

### Identity

Uniquely identifies the record and when it was captured.

### Provenance

Records the source type, producer, producer version, repository, commit, dataset, and environment.

### Context

Describes the domain, system, task, and environment where the evidence applies.

### Change

Optionally describes a software, model, prompt, tool, configuration, firmware, or data change.

### Execution

Identifies the run, scenario, model, seed, tools, and linked artifacts.

#### Artifact manifests

Each linked artifact is a reference, not an upload instruction. Producers can
include a `manifest_version`, `media_type`, `size_bytes`, and an explicit
`checksum_algorithm`/`checksum` pair. SHA-256 is the interoperable baseline;
the legacy `sha256` field remains valid for v0.1 records. Consumers should
resolve URIs according to their own trust and access policy, verify the digest
before use, and never assume that a reachable URI is immutable. MyelinMesh
does not fetch, copy, or execute referenced content.

### Observations

Stores structured measurements. Values should be factual outputs rather than interpretations when possible.

### Failure

Records whether a failure was detected, its class, severity, confidence, and supporting evidence references.

### Diagnosis

Separates supported facts, plausible hypotheses, unsupported hypotheses, and the method used.

### Recovery

Records the attempted recovery, outcome, applicability, and negative evidence.

### Validation

Records human review, replay counts, reproduction counts, synthetic/real status, and notes.

## Content hash

The SDK calculates a SHA-256 hash over canonical JSON while excluding the `content_hash` field. The hash detects accidental mutation; it is not a digital signature.

## Severity vocabulary

- `info`
- `warning`
- `breaking`
- `critical`
- `unknown`

## Source vocabulary

- `real`
- `simulation`
- `benchmark`
- `synthetic`
- `human_review`
- `imported`

## Schema compatibility

The `schema_version` follows semantic versioning:

- Patch: clarifications that do not change validation
- Minor: backward-compatible optional fields or enum additions
- Major: incompatible field or semantic changes

The full compatibility matrix, migration invariants, supported version window,
and failure behavior are defined in [ADR 0003](adr/0003-mer-compatibility-policy.md).
Consumers must fail closed for unknown major versions and must never treat a
successful migration as proof that the underlying evidence is true.

## File naming

Recommended extension:

```text
<evidence-id>.mer.json
```

The normative machine-readable schema is in `schemas/myelinmesh-evidence-record.v0.1.schema.json`.
