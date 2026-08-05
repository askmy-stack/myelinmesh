"""Fast, deterministic release-readiness gate used by maintainers and CI."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    required = [ROOT / "README.md", ROOT / "ROADMAP.md", ROOT / "RELEASE_CHECKLIST.md"]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    schema = ROOT / "schemas/myelinmesh-evidence-record.v0.1.schema.json"
    try:
        json.loads(schema.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"release gate failed: invalid schema: {exc}")
        return 1
    if missing:
        print("release gate failed: missing " + ", ".join(missing))
        return 1
    print("release gate passed: docs, schema, and repository metadata are present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
