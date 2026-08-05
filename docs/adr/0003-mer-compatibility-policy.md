# ADR 0003: Version MER compatibility explicitly

## Status

Accepted for MER 0.1.0 and later schema versions.

## Context

MyelinMesh records are exchanged between producers, adapters, local stores, and
future consumers. A schema version alone is not enough unless producers and
consumers share the same compatibility and migration expectations.

## Decision

MER uses semantic versioning with these meanings:

| Change | Compatibility | Required action |
| --- | --- | --- |
| Patch | Clarification, constraint tightening that rejects no valid record, or documentation-only change | Consumers may continue reading and writing the same shape. |
| Minor | New optional field, new optional enum value, or additive metadata | Older consumers must ignore unknown optional fields; writers must not require them from older readers. |
| Major | Required field, removed or renamed field, changed meaning, or incompatible enum behavior | Publish a migration path or explicitly reject the transition. |

Consumers must accept the exact version they implement. They may accept newer
minor and patch records only when their validator is configured to ignore the
new optional data. Unknown major versions and unknown required fields fail
closed with an actionable error.

Migrations are explicit, deterministic functions from one supported version to
another. A migration must preserve evidence identity, provenance, and
uncertainty unless the target schema documents why a transformation is
required. Migrations must be idempotent, must never silently discard data, and
must validate both input and output. The original record remains available
unless a caller explicitly chooses replacement.

The supported migration window is the current major version and the immediately
preceding major version. A release that drops a migration path must document
the removal in the changelog and release notes.

## Examples

- Adding optional `context.environment` is a minor change.
- Correcting a description or adding a validation example is a patch change.
- Renaming `failure.severity` or making `validation.replay_count` required is a
  major change.

## Consequences

- Producers can evolve without silently changing the meaning of stored evidence.
- Consumers have a predictable failure mode for versions they cannot interpret.
- Every breaking schema change carries implementation and documentation work.
- Content hashes are recomputed for migrated canonical content; a signature is
  not implied by a successful migration.
