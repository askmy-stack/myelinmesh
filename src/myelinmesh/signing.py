from __future__ import annotations

import hashlib
import hmac
from datetime import UTC, datetime

from myelinmesh.hashing import canonical_payload
from myelinmesh.models import EvidenceRecord, SignatureEnvelope


class HMACSigner:
    """Reference signer for local workflows; use a KMS-backed provider in production."""

    algorithm = "hmac-sha256"

    def __init__(self, key: bytes, key_id: str) -> None:
        if not key:
            raise ValueError("signing key must not be empty")
        self._key = key
        self.key_id = key_id

    def sign(self, record: EvidenceRecord) -> EvidenceRecord:
        digest = hmac.new(self._key, canonical_payload(record), hashlib.sha256).hexdigest()
        envelope = SignatureEnvelope(
            algorithm=self.algorithm,
            key_id=self.key_id,
            signature=digest,
            created_at=datetime.now(UTC),
        )
        return record.model_copy(update={"signature": envelope})

    def verify(self, record: EvidenceRecord) -> bool:
        envelope = record.signature
        if envelope is None or envelope.algorithm != self.algorithm:
            return False
        expected = hmac.new(self._key, canonical_payload(record), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, envelope.signature)
