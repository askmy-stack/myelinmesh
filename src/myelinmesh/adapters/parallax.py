from __future__ import annotations

from myelinmesh.adapters.common import captured_at, object_dict, optional_float, string_list
from myelinmesh.models import (
    Context,
    DiagnosisEvidence,
    Domain,
    EvidenceRecord,
    FailureEvidence,
    Identity,
    Provenance,
    RecoveryEvidence,
    Severity,
    SourceType,
    ValidationEvidence,
)


class ParallaxAdapter:
    name = "parallax"

    def can_handle(self, payload: dict[str, object]) -> bool:
        return "failure" in payload and (
            "recovery" in payload or payload.get("producer") == "parallax"
        )

    def convert(self, payload: dict[str, object]) -> list[EvidenceRecord]:
        failure = object_dict(payload.get("failure"))
        recovery = object_dict(payload.get("recovery"))
        diagnosis = object_dict(payload.get("diagnosis"))
        detected = bool(failure.get("detected", True))
        return [
            EvidenceRecord(
                identity=Identity(
                    evidence_id=str(payload.get("evidence_id", "parallax-import")),
                    project="parallax",
                    captured_at=captured_at(payload),
                ),
                provenance=Provenance(
                    source_type=SourceType.IMPORTED,
                    producer="parallax",
                    producer_version=str(payload.get("version", "unknown")),
                ),
                context=Context(
                    domain=Domain(str(payload.get("domain", "agent"))),
                    system=str(payload.get("system", "unknown-autonomous-system")),
                    task=str(payload.get("task")) if payload.get("task") is not None else None,
                ),
                observations={
                    "trace": payload.get("trace", []),
                    "signals": payload.get("signals", {}),
                },
                failure=FailureEvidence(
                    detected=detected,
                    failure_class=str(failure.get("class")) if failure.get("class") else None,
                    severity=Severity(str(failure.get("severity", "unknown"))),
                    confidence=optional_float(failure.get("confidence")),
                    supported_by=string_list(failure.get("supported_by")),
                ),
                diagnosis=DiagnosisEvidence(
                    method=str(diagnosis.get("method")) if diagnosis.get("method") else None,
                    supported_facts=string_list(diagnosis.get("supported_facts")),
                    hypotheses=string_list(diagnosis.get("hypotheses")),
                    confidence=optional_float(diagnosis.get("confidence")),
                ),
                recovery=RecoveryEvidence(
                    action=str(recovery.get("action", "none-recorded")),
                    successful=bool(recovery["successful"])
                    if recovery.get("successful") is not None
                    else None,
                    outcome=str(recovery.get("outcome")) if recovery.get("outcome") else None,
                ),
                validation=ValidationEvidence(real_or_synthetic=SourceType.IMPORTED),
                tags=["parallax", "runtime-reliability", "adapter-import"],
            )
        ]
