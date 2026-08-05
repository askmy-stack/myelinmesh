from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from myelinmesh.cli import app

runner = CliRunner()


def test_cli_workflow(tmp_path: Path) -> None:
    store = tmp_path / "mesh"
    init_result = runner.invoke(app, ["init", str(store)])
    assert init_result.exit_code == 0

    example = "examples/records/tool-semantic-drift.mer.json"
    validate_result = runner.invoke(app, ["validate", example])
    assert validate_result.exit_code == 0

    ingest_result = runner.invoke(app, ["ingest", example, "--store", str(store)])
    assert ingest_result.exit_code == 0

    search_result = runner.invoke(app, ["search", "semantic", "--store", str(store)])
    assert search_result.exit_code == 0
    assert "mer-demo-tool-drift-001" in search_result.stdout


def test_cli_adapter(tmp_path: Path) -> None:
    output = tmp_path / "converted"
    result = runner.invoke(
        app,
        [
            "adapt",
            "tool-semantics",
            "examples/adapters/tool-semantics-report.json",
            "--output-dir",
            str(output),
        ],
    )
    assert result.exit_code == 0
    assert (output / "adapter-tool-semantics-001.mer.json").exists()


def test_cli_batch_ingest_json_summary(tmp_path: Path) -> None:
    store = tmp_path / "mesh"
    result = runner.invoke(
        app,
        [
            "ingest-batch",
            "examples/records",
            "--store",
            str(store),
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert '"inserted": 3' in result.stdout
    assert '"duplicates": 0' in result.stdout
