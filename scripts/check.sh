#!/usr/bin/env bash
set -euo pipefail

ruff check .
ruff format --check .
mypy src
pytest --cov=myelinmesh --cov-report=term-missing
cp schemas/myelinmesh-evidence-record.v0.1.schema.json /tmp/myelinmesh-schema-before.json
python scripts/export_schema.py
diff -u /tmp/myelinmesh-schema-before.json schemas/myelinmesh-evidence-record.v0.1.schema.json
