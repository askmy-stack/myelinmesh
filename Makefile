.PHONY: install test lint format typecheck schema demo clean

install:
	python -m pip install -e ".[dev]"

test:
	pytest --cov=myelinmesh --cov-report=term-missing

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .

typecheck:
	mypy src

schema:
	python scripts/export_schema.py

demo:
	rm -rf .myelinmesh-demo
	myelinmesh init .myelinmesh-demo
	myelinmesh ingest examples/records/tool-semantic-drift.mer.json --store .myelinmesh-demo
	myelinmesh ingest examples/records/physical-regression.mer.json --store .myelinmesh-demo
	myelinmesh ingest examples/records/runtime-recovery.mer.json --store .myelinmesh-demo
	myelinmesh list --store .myelinmesh-demo
	myelinmesh stats --store .myelinmesh-demo

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage dist build site .myelinmesh-demo
