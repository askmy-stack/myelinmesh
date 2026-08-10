# v0.3 retrieval plan

The v0.3 milestone is deliberately split into independently reviewable slices.
Issues [#34](https://github.com/askmy-stack/MyelinMesh/issues/34) through
[#40](https://github.com/askmy-stack/MyelinMesh/issues/40) cover filters,
storage, ranking, consistency, freshness, and a read-only explorer.

The dependency order is:

1. Structured filters (#34) establish the query contract.
2. Applicability filtering (#37) consumes that contract before ranking.
3. PostgreSQL (#35) and pgvector (#36) remain optional backends.
4. Contradiction/duplicate detection (#38) and freshness policies (#39) add
   explainable ranking context.
5. The web explorer (#40) is last and is read-only by design.

Every slice must preserve the local-first default, deterministic results,
content-hash integrity, and the rule that evidence retrieval is not proof.

Issue #38 is implemented as a report-only consistency audit. Duplicate
payloads are grouped by content hash; contradictions are reported when records
share a stable claim key but disagree about `failure.detected`. The API is
`audit_records()`/`EvidenceStore.audit_consistency()`, and the CLI command is
`myelinmesh audit`. No records are deleted or rewritten.
