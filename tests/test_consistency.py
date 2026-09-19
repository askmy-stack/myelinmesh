from pathlib import Path

from myelinmesh.consistency import audit_records
from myelinmesh.io import read_record
from myelinmesh.store import EvidenceStore


def test_audit_reports_exact_duplicates_by_content_hash() -> None:
    record = read_record(Path("examples/records/tool-semantic-drift.mer.json"))
    report = audit_records([record, record])
    assert len(report.duplicates) == 1
    assert report.duplicates[0].evidence_ids == (record.identity.evidence_id,) * 2
    assert report.contradictions == ()


def test_audit_reports_conflicting_failure_claims() -> None:
    record = read_record(Path("examples/records/tool-semantic-drift.mer.json"))
    assert record.failure is not None
    opposite = record.model_copy(
        update={
            "identity": record.identity.model_copy(update={"evidence_id": "tool-drift-opposite"}),
            "failure": record.failure.model_copy(update={"detected": False}),
        }
    )
    report = audit_records([record, opposite])
    assert len(report.contradictions) == 1
    assert report.contradictions[0].evidence_ids == (
        "mer-demo-tool-drift-001",
        "tool-drift-opposite",
    )


def test_store_audit_consistency_is_report_only(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path / "store")
    record = read_record(Path("examples/records/tool-semantic-drift.mer.json"))
    store.ingest(record)
    report = store.audit_consistency()
    assert report.duplicates == ()
    assert report.contradictions == ()
    assert store.stats()["total"] == 1
