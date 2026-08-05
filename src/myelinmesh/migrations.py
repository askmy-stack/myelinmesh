from __future__ import annotations

from collections import deque
from collections.abc import Callable

from myelinmesh.models import EvidenceRecord

Migration = Callable[[EvidenceRecord], EvidenceRecord]
MigrationKey = tuple[str, str]


class MigrationError(ValueError):
    """Raised when no supported migration path exists."""


MIGRATION_REGISTRY: dict[MigrationKey, Migration] = {}


def register_migration(source: str, target: str, migration: Migration) -> None:
    key = (source, target)
    if key in MIGRATION_REGISTRY:
        raise ValueError(f"Migration already registered: {source} -> {target}")
    MIGRATION_REGISTRY[key] = migration


def _identity(record: EvidenceRecord) -> EvidenceRecord:
    return record


register_migration("0.1.0", "0.1.0", _identity)


def _find_path(source: str, target: str) -> list[Migration]:
    if source == target:
        return [MIGRATION_REGISTRY[(source, target)]]

    queue: deque[tuple[str, list[Migration]]] = deque([(source, [])])
    visited = {source}
    while queue:
        version, path = queue.popleft()
        for (from_version, to_version), migration in sorted(MIGRATION_REGISTRY.items()):
            if from_version != version or to_version in visited:
                continue
            next_path = [*path, migration]
            if to_version == target:
                return next_path
            visited.add(to_version)
            queue.append((to_version, next_path))

    raise MigrationError(f"Unsupported migration path: {source} -> {target}")


def migrate_record(record: EvidenceRecord, target_version: str) -> EvidenceRecord:
    """Apply a registered migration path and validate each intermediate record."""
    migrations = _find_path(record.schema_version, target_version)
    current = record
    for migration in migrations:
        migrated = EvidenceRecord.model_validate(migration(current).model_dump(mode="json"))
        if migrated.identity != current.identity or migrated.provenance != current.provenance:
            raise MigrationError("Migration changed identity or provenance")
        current = migrated
    if current.schema_version != target_version:
        raise MigrationError(
            f"Migration produced {current.schema_version}, expected {target_version}"
        )
    return current
