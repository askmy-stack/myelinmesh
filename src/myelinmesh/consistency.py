"""Report-only consistency checks for duplicate and contradictory evidence."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from myelinmesh.hashing import compute_content_hash
from myelinmesh.models import EvidenceRecord


@dataclass(frozen=True)
class ConsistencyFinding:
    kind: str
    evidence_ids: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class ConsistencyReport:
    findings: tuple[ConsistencyFinding, ...]

    @property
    def duplicates(self) -> tuple[ConsistencyFinding, ...]:
        return tuple(finding for finding in self.findings if finding.kind == "duplicate")

    @property
    def contradictions(self) -> tuple[ConsistencyFinding, ...]:
        return tuple(finding for finding in self.findings if finding.kind == "contradiction")


def audit_records(records: Iterable[EvidenceRecord]) -> ConsistencyReport:
    """Find exact duplicate payloads and conflicting failure claims.

    This is intentionally report-only: it never deletes, rewrites, or chooses
    a canonical record. Contradictions are limited to records that share a
    stable claim key (project, system, failure class, and changed artifact)
    while disagreeing about whether the failure was detected.
    """
    materialized = list(records)
    by_hash: defaultdict[str, list[str]] = defaultdict(list)
    by_claim: defaultdict[tuple[str, str, str, str], list[tuple[str, bool]]] = defaultdict(list)
    for record in materialized:
        evidence_id = record.identity.evidence_id
        by_hash[record.content_hash or compute_content_hash(record)].append(evidence_id)
        if record.failure is None or record.failure.failure_class is None:
            continue
        artifact = record.change.artifact if record.change is not None else ""
        key = (
            record.identity.project,
            record.context.system,
            record.failure.failure_class,
            artifact,
        )
        by_claim[key].append((evidence_id, record.failure.detected))

    findings: list[ConsistencyFinding] = []
    for content_hash, evidence_ids in sorted(by_hash.items()):
        if len(evidence_ids) > 1:
            findings.append(
                ConsistencyFinding(
                    kind="duplicate",
                    evidence_ids=tuple(sorted(evidence_ids)),
                    reason=f"records share content hash {content_hash}",
                )
            )
    for key, claims in sorted(by_claim.items()):
        states = {detected for _, detected in claims}
        if len(states) > 1:
            findings.append(
                ConsistencyFinding(
                    kind="contradiction",
                    evidence_ids=tuple(sorted(evidence_id for evidence_id, _ in claims)),
                    reason=(
                        "same claim key has conflicting failure.detected values "
                        f"for project={key[0]!r}, system={key[1]!r}, "
                        f"failure_class={key[2]!r}, artifact={key[3]!r}"
                    ),
                )
            )
    return ConsistencyReport(tuple(findings))
