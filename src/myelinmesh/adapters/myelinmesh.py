from __future__ import annotations

from myelinmesh.adapters.common import captured_at, optional_int
from myelinmesh.models import (
    Context,
    Domain,
    EvidenceRecord,
    ExecutionEvidence,
    FailureEvidence,
    Identity,
    Provenance,
    Severity,
    SourceType,
    ValidationEvidence,
)


class MyelinMeshAdapter:
    name = "myelinmesh"

    def can_handle(self, payload: dict[str, object]) -> bool:
        return (
            "scenario" in payload
            and "metrics" in payload
            and ("release_decision" in payload or payload.get("producer") == "myelinmesh")
        )

    def convert(self, payload: dict[str, object]) -> list[EvidenceRecord]:
        decision = str(payload.get("release_decision", "unknown"))
        failed = decision.lower() in {"blocked", "failed", "reject"}
        return [
            EvidenceRecord(
                identity=Identity(
                    evidence_id=str(payload.get("evidence_id", "myelinmesh-import")),
                    project="myelinmesh",
                    captured_at=captured_at(payload),
                ),
                provenance=Provenance(
                    source_type=SourceType.SIMULATION,
                    producer="myelinmesh",
                    producer_version=str(payload.get("version", "unknown")),
                ),
                context=Context(
                    domain=Domain.PHYSICAL_AI,
                    system=str(payload.get("system", "unknown-robot-system")),
                    task=str(payload.get("task")) if payload.get("task") is not None else None,
                ),
                execution=ExecutionEvidence(
                    run_id=str(payload.get("run_id")) if payload.get("run_id") else None,
                    scenario=str(payload["scenario"]),
                    seed=optional_int(payload.get("seed")),
                ),
                observations={
                    "metrics": payload.get("metrics"),
                    "release_decision": decision,
                    "selection": payload.get("selection"),
                },
                failure=FailureEvidence(
                    detected=failed,
                    failure_class="physical_behavior_regression" if failed else None,
                    severity=Severity.CRITICAL if failed else Severity.INFO,
                ),
                validation=ValidationEvidence(real_or_synthetic=SourceType.SIMULATION),
                tags=["myelinmesh", "physical-ai", "adapter-import"],
            )
        ]
