# Governance

MyelinMesh begins as a maintainer-led open-source project.

## Roles

- **Maintainers** approve releases, schema changes, and governance updates.
- **Reviewers** regularly review specific modules or adapters.
- **Contributors** submit issues, fixtures, documentation, code, and research artifacts.

## Decision process

Routine changes use pull-request review. Changes affecting the schema, security model, licensing, or project scope require an Architecture Decision Record under `docs/adr/`.

## Release authority

Maintainers publish signed Git tags and release notes. No release should be published when CI or schema compatibility checks fail.

## Conflict of interest

Contributors should disclose when a proposed integration, benchmark, or recommendation materially benefits a commercial product they represent.

## Future evolution

After sustained multi-party contribution, the project may adopt a steering group with documented nomination and voting rules.
