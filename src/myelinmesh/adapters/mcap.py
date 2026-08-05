from __future__ import annotations

from myelinmesh.adapters.common import captured_at
from myelinmesh.models import (
    ArtifactReference,
    Context,
    Domain,
    EvidenceRecord,
    ExecutionEvidence,
    Identity,
    Provenance,
    SourceType,
    ValidationEvidence,
)


class Ros2McapAdapter:
    name = "ros2-mcap"

    def can_handle(self, payload: dict[str, object]) -> bool:
        return payload.get("format") == "mcap" or "topics" in payload

    def convert(self, payload: dict[str, object]) -> list[EvidenceRecord]:
        artifact = ArtifactReference(
            uri=str(payload.get("uri", payload.get("path", "file:///unknown.mcap"))),
            media_type="application/vnd.mcap",
            sha256=str(payload["sha256"]) if payload.get("sha256") else None,
            size_bytes=int(str(payload["size_bytes"]))
            if payload.get("size_bytes") is not None
            else None,
            description="ROS 2/MCAP recording",
        )
        return [
            EvidenceRecord(
                identity=Identity(
                    evidence_id=str(payload.get("evidence_id", "ros2-mcap-import")),
                    project="ros2-mcap",
                    captured_at=captured_at(payload),
                ),
                provenance=Provenance(source_type=SourceType.IMPORTED, producer="ros2-mcap"),
                context=Context(
                    domain=Domain.PHYSICAL_AI,
                    system=str(payload.get("system", "ros2-system")),
                    task="MCAP recording import",
                ),
                execution=ExecutionEvidence(
                    run_id=str(payload.get("run_id", "mcap-run")),
                    tools=["ros2", "mcap"],
                    artifacts=[artifact],
                ),
                observations={
                    "topics": payload.get("topics", []),
                    "message_count": payload.get("message_count"),
                },
                validation=ValidationEvidence(real_or_synthetic=SourceType.IMPORTED),
                tags=["ros2", "mcap", "physical-ai", "adapter-import"],
            )
        ]
