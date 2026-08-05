from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from myelinmesh.hashing import compute_content_hash, verify_content_hash, with_content_hash
from myelinmesh.models import ArtifactReference, EvidenceRecord

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


def test_artifact_manifest_supports_explicit_checksum() -> None:
    digest = "a" * 64
    artifact = ArtifactReference(
        uri="s3://bucket/run-42/result.mcap",
        media_type="application/vnd.mcap",
        size_bytes=4096,
        checksum_algorithm="sha256",
        checksum=digest,
    )
    assert artifact.canonical_checksum == ("sha256", digest)


def test_artifact_manifest_preserves_legacy_sha256() -> None:
    digest = "b" * 64
    artifact = ArtifactReference(uri="file:///tmp/result.json", sha256=digest)
    assert artifact.canonical_checksum == ("sha256", digest)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"checksum": "a" * 64},
        {"checksum_algorithm": "sha256", "checksum": "a" * 63},
        {"sha256": "a" * 64, "checksum_algorithm": "md5", "checksum": "b" * 32},
    ],
)
def test_artifact_manifest_rejects_ambiguous_checksums(kwargs: dict[str, str]) -> None:
    with pytest.raises(ValidationError):
        ArtifactReference(uri="file:///tmp/result", **kwargs)
