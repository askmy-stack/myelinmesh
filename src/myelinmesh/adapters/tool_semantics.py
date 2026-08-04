from __future__ import annotations

from myelinmesh.adapters.common import captured_at
from myelinmesh.models import (
    ChangeEvidence,
    Context,
    DiagnosisEvidence,
    Domain,
    EvidenceRecord,
    FailureEvidence,
    Identity,
    Provenance,
    Severity,
    SourceType,
    ValidationEvidence,
)


class ToolSemanticsAdapter:
    name = "tool-semantics"

    def can_handle(self, payload: dict[str, object]) -> bool:
        return "changes" in payload and (
            "is_compatible" in payload or payload.get("producer") == "tool-semantics"
        )

    def convert(self, payload: dict[str, object]) -> list[EvidenceRecord]:
        data = payload  # narrowed locally for readability
        evidence_id = str(data.get("evidence_id", "tool-semantics-import"))
        changes = data.get("changes", [])
        is_compatible = bool(data.get("is_compatible", True))
        failure_class = None if is_compatible else "tool_interface_regression"
        return [
            EvidenceRecord(
                identity=Identity(
                    evidence_id=evidence_id,
                    project="tool-semantics",
                    captured_at=captured_at(data),
                ),
                provenance=Provenance(
                    source_type=SourceType.IMPORTED,
                    producer="tool-semantics",
                    producer_version=str(data.get("version", "unknown")),
                ),
                context=Context(
                    domain=Domain.AGENT,
                    system=str(data.get("system", "unknown-agent-system")),
                    task=str(data.get("task")) if data.get("task") is not None else None,
                ),
                change=ChangeEvidence(
                    change_type="tool_interface",
                    artifact=str(data.get("artifact", "tool-manifest")),
                    summary=f"Imported {len(changes) if isinstance(changes, list) else 0} changes",
                ),
                observations={"changes": changes, "is_compatible": is_compatible},
                failure=FailureEvidence(
                    detected=not is_compatible,
                    failure_class=failure_class,
                    severity=Severity.BREAKING if not is_compatible else Severity.INFO,
                ),
                diagnosis=DiagnosisEvidence(
                    method="tool-semantics deterministic comparison",
                    supported_facts=["Producer reported compatibility result"],
                ),
                validation=ValidationEvidence(real_or_synthetic=SourceType.IMPORTED),
                tags=["tool-semantics", "adapter-import"],
            )
        ]
