from __future__ import annotations

from myelinmesh.adapters.common import captured_at
from myelinmesh.models import (
    ChangeEvidence,
    Context,
    Domain,
    EvidenceRecord,
    Identity,
    Provenance,
    SourceType,
    ValidationEvidence,
)


class GitHubAdapter:
    name = "github"

    def can_handle(self, payload: dict[str, object]) -> bool:
        return "pull_request" in payload or payload.get("producer") == "github"

    def convert(self, payload: dict[str, object]) -> list[EvidenceRecord]:
        change = payload.get("pull_request", payload)
        data = change if isinstance(change, dict) else {}
        number = data.get("number", payload.get("number", "unknown"))
        return [
            EvidenceRecord(
                identity=Identity(
                    evidence_id=str(payload.get("evidence_id", f"github-pr-{number}")),
                    project=str(payload.get("repository", "github")),
                    captured_at=captured_at(payload),
                ),
                provenance=Provenance(
                    source_type=SourceType.IMPORTED,
                    producer="github",
                    repository_url=str(payload["repository_url"])
                    if payload.get("repository_url")
                    else None,
                ),
                context=Context(
                    domain=Domain.ML_SYSTEM,
                    system=str(payload.get("repository", "unknown-repository")),
                    task="pull-request change import",
                ),
                change=ChangeEvidence(
                    change_type="pull_request",
                    artifact=f"github:pr/{number}",
                    summary=str(data.get("title", "GitHub change")),
                    after_hash=str(data["head_sha"]) if data.get("head_sha") else None,
                ),
                observations={"action": payload.get("action"), "pull_request": data},
                validation=ValidationEvidence(real_or_synthetic=SourceType.IMPORTED),
                tags=["github", "change", "adapter-import"],
            )
        ]
