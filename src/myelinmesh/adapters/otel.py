from __future__ import annotations

from myelinmesh.adapters.common import captured_at, object_dict
from myelinmesh.models import (
    Context,
    Domain,
    EvidenceRecord,
    ExecutionEvidence,
    Identity,
    Provenance,
    SourceType,
    ValidationEvidence,
)


class OpenTelemetryAdapter:
    name = "opentelemetry"

    def can_handle(self, payload: dict[str, object]) -> bool:
        return "resourceSpans" in payload or payload.get("producer") in {"otel", "opentelemetry"}

    def convert(self, payload: dict[str, object]) -> list[EvidenceRecord]:
        resource = object_dict(payload.get("resource"))
        spans = payload.get("spans", payload.get("resourceSpans", []))
        return [
            EvidenceRecord(
                identity=Identity(
                    evidence_id=str(payload.get("evidence_id", "otel-import")),
                    project="opentelemetry",
                    captured_at=captured_at(payload),
                ),
                provenance=Provenance(
                    source_type=SourceType.IMPORTED,
                    producer="opentelemetry",
                    producer_version=str(payload.get("version", "unknown")),
                    environment=resource,
                ),
                context=Context(
                    domain=Domain.ML_SYSTEM,
                    system=str(resource.get("service.name", payload.get("service", "unknown"))),
                    task="trace-span import",
                ),
                execution=ExecutionEvidence(
                    run_id=str(payload.get("trace_id", "otel-trace")), tools=["opentelemetry"]
                ),
                observations={
                    "spans": spans if isinstance(spans, list) else [],
                    "resource": resource,
                },
                validation=ValidationEvidence(real_or_synthetic=SourceType.IMPORTED),
                tags=["opentelemetry", "trace", "adapter-import"],
            )
        ]
