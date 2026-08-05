from __future__ import annotations

from pathlib import Path

import pytest

from myelinmesh.io import read_record
from myelinmesh.store import EvidenceStore


def test_ingest_search_and_get(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path / "store")
    record = read_record(Path("examples/records/tool-semantic-drift.mer.json"))
    stored = store.ingest(record)

    assert stored.content_hash is not None
    assert store.get(record.identity.evidence_id).content_hash == stored.content_hash
    assert store.search("semantic drift")[0].evidence_id == record.identity.evidence_id
    assert store.stats()["total"] == 1


def test_duplicate_id_with_different_content_is_rejected(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path / "store")
    record = read_record(Path("examples/records/tool-semantic-drift.mer.json"))
    store.ingest(record)
    changed = record.model_copy(update={"tags": ["changed"]})
    with pytest.raises(FileExistsError):
        store.ingest(changed)


def test_batch_ingest_is_deterministic_and_deduplicates(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path / "store")
    batch = tmp_path / "batch"
    batch.mkdir()
    for name in (
        "tool-semantic-drift.mer.json",
        "physical-regression.mer.json",
        "runtime-recovery.mer.json",
    ):
        (batch / name).write_text(
            Path("examples/records", name).read_text(encoding="utf-8"), encoding="utf-8"
        )

    batch_files = [
        batch / name
        for name in (
            "tool-semantic-drift.mer.json",
            "physical-regression.mer.json",
            "runtime-recovery.mer.json",
        )
    ]
    first = store.ingest_many(batch_files)
    second = store.ingest_many(batch_files)

    assert first.inserted == 3
    assert first.duplicates == first.invalid == first.failed == 0
    assert second.inserted == 0
    assert second.duplicates == 3
    assert store.stats()["total"] == 3


def test_batch_ingest_reports_invalid_and_conflicting_records(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path / "store")
    valid = read_record(Path("examples/records/tool-semantic-drift.mer.json"))
    valid_path = tmp_path / "valid.mer.json"
    valid_path.write_text(
        Path("examples/records/tool-semantic-drift.mer.json").read_text(), encoding="utf-8"
    )
    invalid_path = tmp_path / "invalid.mer.json"
    invalid_path.write_text("not json", encoding="utf-8")
    conflict = valid.model_copy(update={"tags": ["different-content"]})
    conflict_path = tmp_path / "conflict.mer.json"
    conflict_path.write_text(conflict.model_dump_json(), encoding="utf-8")
    store.ingest(valid)

    report = store.ingest_many([invalid_path, conflict_path, valid_path])

    assert report.inserted == 0
    assert report.duplicates == 1
    assert report.invalid == 1
    assert report.failed == 1
