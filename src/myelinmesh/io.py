from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from myelinmesh.models import EvidenceRecord


class EvidenceFileError(ValueError):
    pass


def read_record(path: Path) -> EvidenceRecord:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceFileError(f"Unable to read JSON evidence record: {path}: {exc}") from exc

    try:
        return EvidenceRecord.model_validate(payload)
    except ValidationError as exc:
        raise EvidenceFileError(f"Invalid evidence record: {path}: {exc}") from exc


def write_record(record: EvidenceRecord, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(record.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
