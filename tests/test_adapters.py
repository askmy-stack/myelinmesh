from __future__ import annotations

import json
from pathlib import Path

from myelinmesh.adapters import ImpactForgeAdapter, ParallaxAdapter, ToolSemanticsAdapter


def load(name: str) -> dict[str, object]:
    return json.loads((Path("examples/adapters") / name).read_text(encoding="utf-8"))


def test_tool_semantics_adapter() -> None:
    adapter = ToolSemanticsAdapter()
    payload = load("tool-semantics-report.json")
    assert adapter.can_handle(payload)
    record = adapter.convert(payload)[0]
    assert record.failure is not None and record.failure.detected


def test_impactforge_adapter() -> None:
    adapter = ImpactForgeAdapter()
    payload = load("impactforge-report.json")
    assert adapter.can_handle(payload)
    record = adapter.convert(payload)[0]
    assert record.context.domain.value == "physical_ai"


def test_parallax_adapter() -> None:
    adapter = ParallaxAdapter()
    payload = load("parallax-report.json")
    assert adapter.can_handle(payload)
    record = adapter.convert(payload)[0]
    assert record.recovery is not None and record.recovery.successful
