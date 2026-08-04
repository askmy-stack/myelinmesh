# Data Governance

## Scope

This policy covers evidence records, traces, prompts, simulation artifacts, MCAP bags, model outputs, human reviews, and linked datasets.

## Data classes

- **Public:** intentionally published examples and public benchmark data.
- **Internal:** non-public engineering evidence without regulated data.
- **Sensitive:** personal data, customer interactions, proprietary system details, or security-relevant traces.
- **Restricted:** protected health information, secrets, credentials, export-controlled data, or data subject to contractual restrictions.

The open repository may contain only Public data.

## Contributor responsibilities

Contributors must verify that they have the right to redistribute every record and artifact. Synthetic examples must be labeled. Redaction must occur before contribution, not after publication.

## Provenance requirements

Every record should identify source type, producer, version, date, applicable environment, and any dataset license or restrictions.

## Retention and deletion

The local core does not impose retention. Hosted implementations must support documented retention, erasure, access control, and audit workflows.

## Model training

Evidence must not be used for model training unless its license and privacy classification permit it. Evaluation splits must prevent duplicate and derived-incident leakage.
