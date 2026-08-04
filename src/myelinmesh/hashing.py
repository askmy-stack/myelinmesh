from __future__ import annotations

import hashlib
import json
from typing import Any

from myelinmesh.models import EvidenceRecord


def canonical_payload(record: EvidenceRecord) -> bytes:
    data: dict[str, Any] = record.model_dump(mode="json", exclude={"content_hash"}, by_alias=True)
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def compute_content_hash(record: EvidenceRecord) -> str:
    return "sha256:" + hashlib.sha256(canonical_payload(record)).hexdigest()


def with_content_hash(record: EvidenceRecord) -> EvidenceRecord:
    return record.model_copy(update={"content_hash": compute_content_hash(record)})


def verify_content_hash(record: EvidenceRecord) -> bool:
    return record.content_hash is not None and record.content_hash == compute_content_hash(record)
