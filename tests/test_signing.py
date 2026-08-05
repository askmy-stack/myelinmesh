from datetime import UTC, datetime

from myelinmesh.models import EvidenceRecord
from myelinmesh.signing import HMACSigner


def record() -> EvidenceRecord:
    return EvidenceRecord.model_validate(
        {
            "identity": {
                "evidence_id": "signed-1",
                "project": "test",
                "captured_at": datetime.now(UTC).isoformat(),
            },
            "provenance": {"source_type": "synthetic", "producer": "test"},
            "context": {"system": "fixture"},
        }
    )


def test_hmac_sign_and_verify_excludes_signature_from_payload() -> None:
    signer = HMACSigner(b"local-test-key", "test-key")
    signed = signer.sign(record())
    assert signed.signature is not None
    assert signer.verify(signed)
    changed = signed.model_copy(update={"observations": {"changed": True}})
    assert not signer.verify(changed)


def test_unsigned_records_remain_valid() -> None:
    assert record().signature is None
