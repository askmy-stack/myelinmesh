from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from myelinmesh.freshness import FreshnessPolicy, evaluate_record, evaluate_records
from myelinmesh.io import read_record
from myelinmesh.store import EvidenceStore


def test_fresh_record_within_max_age() -> None:
    record = read_record(Path("examples/records/tool-semantic-drift.mer.json"))
    as_of = record.identity.captured_at + timedelta(days=7)
    assessment = evaluate_record(
        record, FreshnessPolicy(max_age_days=30, half_life_days=30, as_of=as_of)
    )
    assert assessment.status == "fresh"
    assert assessment.age_days == pytest.approx(7.0)
    assert assessment.weight == pytest.approx(0.5 ** (7 / 30))


def test_stale_record_exceeds_max_age_without_mutating() -> None:
    record = read_record(Path("examples/records/tool-semantic-drift.mer.json"))
    original = record.model_dump(mode="json")
    as_of = record.identity.captured_at + timedelta(days=45)
    assessment = evaluate_record(record, FreshnessPolicy(max_age_days=30, as_of=as_of))
    assert assessment.status == "stale"
    assert assessment.weight == 0.0
    assert "exceeds max_age_days" in assessment.reasons[0]
    assert record.model_dump(mode="json") == original


def test_evaluate_records_is_deterministic_by_evidence_id() -> None:
    first = read_record(Path("examples/records/physical-regression.mer.json"))
    second = read_record(Path("examples/records/tool-semantic-drift.mer.json"))
    as_of = datetime(2026, 9, 1, tzinfo=UTC)
    report = evaluate_records([second, first], FreshnessPolicy(max_age_days=90, as_of=as_of))
    assert [item.evidence_id for item in report.assessments] == sorted(
        [first.identity.evidence_id, second.identity.evidence_id]
    )


def test_store_evaluate_freshness(tmp_path: Path) -> None:
    store = EvidenceStore(tmp_path / "store")
    record = read_record(Path("examples/records/tool-semantic-drift.mer.json"))
    store.ingest(record)
    as_of = record.identity.captured_at + timedelta(days=1)
    report = store.evaluate_freshness(FreshnessPolicy(max_age_days=30, as_of=as_of))
    assert len(report.fresh) == 1
    assert report.stale == ()
    assert store.stats()["total"] == 1


def test_invalid_policy_rejected() -> None:
    with pytest.raises(ValueError, match="max_age_days"):
        FreshnessPolicy(max_age_days=-1)
    with pytest.raises(ValueError, match="half_life_days"):
        FreshnessPolicy(max_age_days=1, half_life_days=0)
