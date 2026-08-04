from __future__ import annotations

from typing import Protocol

from myelinmesh.models import EvidenceRecord


class EvidenceAdapter(Protocol):
    name: str

    def can_handle(self, payload: dict[str, object]) -> bool: ...

    def convert(self, payload: dict[str, object]) -> list[EvidenceRecord]: ...
