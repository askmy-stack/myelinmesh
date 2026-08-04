from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from myelinmesh.hashing import compute_content_hash, verify_content_hash, with_content_hash
from myelinmesh.models import EvidenceRecord

EXAMPLES = Path("examples/records")


@pytest.mark.parametrize("path", sorted(EXAMPLES.glob("*.json")))
def test_example_records_validate(path: Path) -> None:
    record = EvidenceRecord.model_validate(json.loads(path.read_text(encoding="utf-8")))
    assert record.schema_version == "0.1.0"


def test_hash_is_deterministic() -> None:
    payload = json.loads((EXAMPLES / "tool-semantic-drift.mer.json").read_text())
    record = EvidenceRecord.model_validate(payload)
    assert compute_content_hash(record) == compute_content_hash(record)
    hashed = with_content_hash(record)
    assert verify_content_hash(hashed)


def test_reproduction_count_cannot_exceed_replays() -> None:
    payload = json.loads((EXAMPLES / "runtime-recovery.mer.json").read_text())
    payload["validation"]["replay_count"] = 2
    payload["validation"]["reproduced_count"] = 3
    with pytest.raises(ValidationError):
        EvidenceRecord.model_validate(payload)
