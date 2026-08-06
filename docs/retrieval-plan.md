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

Issue #34 is implemented by `EvidenceStore.filter()` and the CLI
`myelinmesh filter` command. Filters are exact-match and composable; repeated
`--tag` options require every requested tag. Empty filters return the newest
records deterministically.
