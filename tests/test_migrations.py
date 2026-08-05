from __future__ import annotations

from pathlib import Path

import pytest

from myelinmesh.io import read_record
from myelinmesh.migrations import MigrationError, migrate_record


def test_current_schema_migration_is_deterministic() -> None:
    record = read_record(Path("examples/records/tool-semantic-drift.mer.json"))

    migrated = migrate_record(record, "0.1.0")

    assert migrated == record
    assert migrate_record(record, "0.1.0") == migrated


def test_unknown_migration_path_fails_closed() -> None:
    record = read_record(Path("examples/records/tool-semantic-drift.mer.json"))

    with pytest.raises(MigrationError, match="Unsupported migration path"):
        migrate_record(record, "0.2.0")
