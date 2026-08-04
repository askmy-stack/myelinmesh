# Security and Privacy

## Threats

- Secret leakage through prompts, logs, or configuration
- Personally identifiable information in agent trajectories
- Protected health information in biomedical evidence
- Proprietary robot maps, video, and MCAP bags
- Poisoned or fabricated evidence records
- Path traversal through artifact references
- Misuse of historical similarity as authorization
- Overconfident diagnosis based on stale versions

## Required controls

- Validate all records before ingestion
- Store artifact references as data; do not automatically execute or fetch them
- Redact sensitive fixture data
- Preserve source and version metadata
- Separate real, simulated, benchmark, and synthetic evidence
- Require explicit opt-in before uploading artifacts
- Never execute recovery actions from evidence records

## Future controls

- Signed evidence envelopes
- Secret and PII scanning
- Field-level encryption
- Access-control labels
- Tenant separation
- Retention and erasure workflows
- Tamper-evident artifact manifests
