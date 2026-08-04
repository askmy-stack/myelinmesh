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

## File naming

Recommended extension:

```text
<evidence-id>.mer.json
```

The normative machine-readable schema is in `schemas/myelinmesh-evidence-record.v0.1.schema.json`.
