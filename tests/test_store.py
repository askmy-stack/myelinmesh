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
