# Security Policy

## Supported versions

Only the latest minor release receives security fixes during the foundation phase.

## Reporting

Report vulnerabilities privately through GitHub Security Advisories after the repository is published. Until then, contact the repository owner through a private channel listed on the GitHub profile.

## Sensitive-data policy

Evidence records can reference traces, prompts, robot telemetry, customer interactions, and human reviews. Never commit:

- API keys, tokens, credentials, or private endpoints
- Protected health information
- Personally identifiable information without explicit authorization
- Proprietary MCAP bags or production traces
- Unredacted customer messages
- Internal repository URLs or commit metadata that must remain confidential

## Trust boundaries

MyelinMesh treats all imported records as untrusted input. Producers may be compromised or mistaken. Ingestion validates structure but does not prove factual correctness.

## Current limitations

- No cryptographic signatures are implemented in v0.1.
- Local files are not encrypted by MyelinMesh.
- The CLI does not yet provide automated secret or PII scanning.
- Similarity search must not be used as an automatic authorization or safety decision.
