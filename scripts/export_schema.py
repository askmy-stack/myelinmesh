from __future__ import annotations

import json
from pathlib import Path

from myelinmesh.models import EvidenceRecord

OUTPUT = Path("schemas/myelinmesh-evidence-record.v0.1.schema.json")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(
    json.dumps(EvidenceRecord.model_json_schema(), indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(OUTPUT)
