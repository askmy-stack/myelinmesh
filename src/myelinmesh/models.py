from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class SourceType(StrEnum):
    REAL = "real"
    SIMULATION = "simulation"
    BENCHMARK = "benchmark"
    SYNTHETIC = "synthetic"
    HUMAN_REVIEW = "human_review"
    IMPORTED = "imported"


class Domain(StrEnum):
    AGENT = "agent"
    PHYSICAL_AI = "physical_ai"
    ML_SYSTEM = "ml_system"
    HYBRID = "hybrid"
    UNKNOWN = "unknown"


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    BREAKING = "breaking"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class ArtifactReference(StrictModel):
    """A portable pointer to an immutable evidence artifact.

    ``sha256`` remains supported for MER v0.1 producers. New producers should
    use the explicit manifest fields so consumers can negotiate algorithms.
    MyelinMesh records references only; it never fetches or uploads the URI.
    """

    uri: str
    media_type: str | None = None
    sha256: str | None = Field(default=None, pattern=r"^[a-fA-F0-9]{64}$")
    description: str | None = None
    size_bytes: int | None = Field(default=None, ge=0)
    manifest_version: str = Field(default="1.0.0", pattern=r"^\d+\.\d+\.\d+$")
    checksum_algorithm: str | None = Field(default=None, pattern=r"^[a-z0-9][a-z0-9._-]*$")
    checksum: str | None = Field(default=None, pattern=r"^[a-fA-F0-9]+$")

    @model_validator(mode="after")
    def validate_checksum_manifest(self) -> ArtifactReference:
        if self.checksum is not None and self.checksum_algorithm is None:
            raise ValueError("checksum_algorithm is required when checksum is set")
        if self.sha256 is not None:
            if self.checksum_algorithm not in (None, "sha256"):
                raise ValueError("legacy sha256 cannot be combined with another algorithm")
            if self.checksum is not None and self.checksum.lower() != self.sha256.lower():
                raise ValueError("sha256 and checksum must match when both are provided")
        if (
            self.checksum_algorithm == "sha256"
            and self.checksum is not None
            and len(self.checksum) != 64
        ):
            raise ValueError("sha256 checksum must contain 64 hexadecimal characters")
        return self

    @property
    def canonical_checksum(self) -> tuple[str, str] | None:
        """Return the algorithm and digest using the legacy field when needed."""
        if self.checksum is not None and self.checksum_algorithm is not None:
            return self.checksum_algorithm, self.checksum.lower()
        if self.sha256 is not None:
            return "sha256", self.sha256.lower()
        return None


class Identity(StrictModel):
    evidence_id: str = Field(min_length=3, max_length=200, pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
    project: str = Field(min_length=1, max_length=200)
    captured_at: datetime


class Provenance(StrictModel):
    source_type: SourceType
    producer: str = Field(min_length=1, max_length=200)
    producer_version: str | None = None
    repository_url: str | None = None
    commit_sha: str | None = Field(default=None, pattern=r"^[a-fA-F0-9]{6,64}$")
    dataset_name: str | None = None
    dataset_version: str | None = None
    environment: dict[str, Any] = Field(default_factory=dict)


class Context(StrictModel):
    domain: Domain = Domain.UNKNOWN
    system: str = Field(min_length=1, max_length=300)
    task: str | None = None
    environment: str | None = None
    subject: str | None = None


class ChangeEvidence(StrictModel):
    change_type: str = Field(min_length=1, max_length=100)
    artifact: str = Field(min_length=1, max_length=500)
    summary: str | None = None
    before_hash: str | None = Field(default=None, pattern=r"^[a-fA-F0-9]{6,64}$")
    after_hash: str | None = Field(default=None, pattern=r"^[a-fA-F0-9]{6,64}$")
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExecutionEvidence(StrictModel):
    run_id: str | None = None
    scenario: str | None = None
    model: str | None = None
    seed: int | None = None
    tools: list[str] = Field(default_factory=list)
    artifacts: list[ArtifactReference] = Field(default_factory=list)
    started_at: datetime | None = None
    ended_at: datetime | None = None

    @field_validator("ended_at")
    @classmethod
    def ended_after_started(cls, value: datetime | None, info: Any) -> datetime | None:
        started = info.data.get("started_at")
        if value is not None and started is not None and value < started:
            raise ValueError("ended_at must not be earlier than started_at")
        return value


class FailureEvidence(StrictModel):
    detected: bool
    failure_class: str | None = None
    severity: Severity = Severity.UNKNOWN
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    supported_by: list[str] = Field(default_factory=list)


class DiagnosisEvidence(StrictModel):
    method: str | None = None
    supported_facts: list[str] = Field(default_factory=list)
    hypotheses: list[str] = Field(default_factory=list)
    unsupported_hypotheses: list[str] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class RecoveryEvidence(StrictModel):
    action: str
    successful: bool | None = None
    outcome: str | None = None
    applicable_conditions: dict[str, Any] = Field(default_factory=dict)
    negative_evidence: list[str] = Field(default_factory=list)


class ValidationEvidence(StrictModel):
    human_reviewed: bool = False
    reviewer: str | None = None
    replay_count: int = Field(default=0, ge=0)
    reproduced_count: int = Field(default=0, ge=0)
    real_or_synthetic: SourceType | None = None
    notes: list[str] = Field(default_factory=list)

    @field_validator("reproduced_count")
    @classmethod
    def reproduced_not_above_replay(cls, value: int, info: Any) -> int:
        replay_count = info.data.get("replay_count", 0)
        if value > replay_count:
            raise ValueError("reproduced_count cannot exceed replay_count")
        return value


class EvidenceRecord(StrictModel):
    schema_version: str = Field(default="0.1.0", pattern=r"^\d+\.\d+\.\d+$")
    identity: Identity
    provenance: Provenance
    context: Context
    change: ChangeEvidence | None = None
    execution: ExecutionEvidence | None = None
    observations: dict[str, Any] = Field(default_factory=dict)
    failure: FailureEvidence | None = None
    diagnosis: DiagnosisEvidence | None = None
    recovery: RecoveryEvidence | None = None
    validation: ValidationEvidence = Field(default_factory=ValidationEvidence)
    tags: list[str] = Field(default_factory=list)
    related_evidence_ids: list[str] = Field(default_factory=list)
    content_hash: str | None = Field(default=None, pattern=r"^sha256:[a-f0-9]{64}$")
