from __future__ import annotations

import json
from pathlib import Path

from myelinmesh.adapters import (
    GitHubAdapter,
    MyelinMeshAdapter,
    OpenTelemetryAdapter,
    ParallaxAdapter,
    Ros2McapAdapter,
    ToolSemanticsAdapter,
)


def load(name: str) -> dict[str, object]:
    return json.loads((Path("examples/adapters") / name).read_text(encoding="utf-8"))


def test_tool_semantics_adapter() -> None:
    adapter = ToolSemanticsAdapter()
    payload = load("tool-semantics-report.json")
    assert adapter.can_handle(payload)
    record = adapter.convert(payload)[0]
    assert record.failure is not None and record.failure.detected


def test_myelinmesh_adapter() -> None:
    adapter = MyelinMeshAdapter()
    payload = load("myelinmesh-report.json")
    assert adapter.can_handle(payload)
    record = adapter.convert(payload)[0]
    assert record.context.domain.value == "physical_ai"


def test_parallax_adapter() -> None:
    adapter = ParallaxAdapter()
    payload = load("parallax-report.json")
    assert adapter.can_handle(payload)
    record = adapter.convert(payload)[0]
    assert record.recovery is not None and record.recovery.successful


def test_opentelemetry_adapter() -> None:
    payload = {
        "producer": "opentelemetry",
        "resourceSpans": [{"name": "predict"}],
        "service": "agent",
    }
    record = OpenTelemetryAdapter().convert(payload)[0]
    assert record.provenance.producer == "opentelemetry"


def test_github_adapter() -> None:
    payload = {
        "producer": "github",
        "repository": "askmy-stack/MyelinMesh",
        "pull_request": {"number": 42, "title": "change"},
    }
    record = GitHubAdapter().convert(payload)[0]
    assert record.change is not None and record.change.artifact == "github:pr/42"


def test_ros2_mcap_adapter() -> None:
    record = Ros2McapAdapter().convert(
        {"format": "mcap", "uri": "file:///run.mcap", "topics": ["/scan"]}
    )[0]
    assert (
        record.execution is not None
        and record.execution.artifacts[0].media_type == "application/vnd.mcap"
    )
