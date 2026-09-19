"""Deterministic freshness and decay evaluation for evidence records.

Policies annotate retrieval context only. They never rewrite stored MER files
or SQLite rows.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime

from myelinmesh.models import EvidenceRecord


@dataclass(frozen=True)
class FreshnessPolicy:
    """Configurable age window and optional exponential decay half-life."""

    max_age_days: float
    half_life_days: float | None = None
    as_of: datetime | None = None

    def __post_init__(self) -> None:
        if self.max_age_days < 0:
            raise ValueError("max_age_days must be non-negative")
        if self.half_life_days is not None and self.half_life_days <= 0:
            raise ValueError("half_life_days must be positive when set")


@dataclass(frozen=True)
class FreshnessAssessment:
    evidence_id: str
    age_days: float
    status: str
    weight: float
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class FreshnessReport:
    assessments: tuple[FreshnessAssessment, ...]

    @property
    def fresh(self) -> tuple[FreshnessAssessment, ...]:
        return tuple(item for item in self.assessments if item.status == "fresh")

    @property
    def stale(self) -> tuple[FreshnessAssessment, ...]:
        return tuple(item for item in self.assessments if item.status == "stale")


def _ensure_aware(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def evaluate_record(record: EvidenceRecord, policy: FreshnessPolicy) -> FreshnessAssessment:
    """Evaluate one record against a freshness policy without mutating it."""
    as_of = _ensure_aware(policy.as_of or datetime.now(UTC))
    captured = _ensure_aware(record.identity.captured_at)
    age_seconds = max(0.0, (as_of - captured).total_seconds())
    age_days = age_seconds / 86_400.0
    reasons: list[str] = []
    if age_days > policy.max_age_days:
        status = "stale"
        reasons.append(f"age {age_days:.4f}d exceeds max_age_days {policy.max_age_days:.4f}d")
    else:
        status = "fresh"
        reasons.append(f"age {age_days:.4f}d within max_age_days {policy.max_age_days:.4f}d")

    if policy.half_life_days is None:
        weight = 0.0 if status == "stale" else 1.0
        reasons.append("decay disabled; weight is 1.0 when fresh else 0.0")
    else:
        weight = 0.5 ** (age_days / policy.half_life_days)
        reasons.append(
            f"decay weight {weight:.6f} using half_life_days {policy.half_life_days:.4f}d"
        )

    return FreshnessAssessment(
        evidence_id=record.identity.evidence_id,
        age_days=age_days,
        status=status,
        weight=weight,
        reasons=tuple(reasons),
    )


def evaluate_records(records: Iterable[EvidenceRecord], policy: FreshnessPolicy) -> FreshnessReport:
    """Evaluate records in deterministic evidence_id order."""
    assessments = tuple(
        evaluate_record(record, policy)
        for record in sorted(records, key=lambda item: item.identity.evidence_id)
    )
    return FreshnessReport(assessments)
