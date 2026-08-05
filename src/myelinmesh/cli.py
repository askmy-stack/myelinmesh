from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from myelinmesh import __version__
from myelinmesh.adapters import MyelinMeshAdapter, ParallaxAdapter, ToolSemanticsAdapter
from myelinmesh.adapters.base import EvidenceAdapter
from myelinmesh.hashing import compute_content_hash, verify_content_hash
from myelinmesh.io import EvidenceFileError, read_record, write_record
from myelinmesh.migrations import MigrationError, migrate_record
from myelinmesh.store import EvidenceStore, EvidenceSummary

app = typer.Typer(
    name="myelinmesh",
    help="Local-first reliability evidence mesh for AI systems.",
    no_args_is_help=True,
)
console = Console(width=160)


def version_callback(value: bool) -> None:
    if value:
        console.print(f"myelinmesh {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option("--version", callback=version_callback, is_eager=True, help="Show version."),
    ] = None,
) -> None:
    """MyelinMesh command-line interface."""


@app.command("init")
def initialize(
    path: Annotated[Path, typer.Argument(help="Store directory.")] = Path(".myelinmesh"),
) -> None:
    store = EvidenceStore(path)
    store.initialize()
    console.print(f"Initialized MyelinMesh store at [bold]{path}[/bold]")


@app.command()
def validate(
    record_file: Annotated[Path, typer.Argument(exists=True, readable=True)],
) -> None:
    try:
        record = read_record(record_file)
    except EvidenceFileError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=2) from exc

    digest = compute_content_hash(record)
    hash_status = "absent"
    if record.content_hash:
        hash_status = "valid" if verify_content_hash(record) else "INVALID"
    console.print(f"Valid MER: [bold]{record.identity.evidence_id}[/bold]")
    console.print(f"Computed hash: {digest}")
    console.print(f"Stored hash: {hash_status}")


@app.command()
def migrate(
    record_file: Annotated[Path, typer.Argument(exists=True, readable=True)],
    target_version: Annotated[str, typer.Option("--to", help="Target MER schema version.")],
    output: Annotated[Path | None, typer.Option("--output", help="Destination MER file.")] = None,
    in_place: Annotated[
        bool, typer.Option("--in-place", help="Replace the input file explicitly.")
    ] = False,
) -> None:
    """Migrate one MER record through the registered compatibility path."""
    if output is not None and in_place:
        raise typer.BadParameter("Use either --output or --in-place, not both.")
    destination = (
        record_file
        if in_place
        else output
        if output is not None
        else record_file.with_name(f"{record_file.stem}.migrated-{target_version}.mer.json")
    )
    if destination == record_file and not in_place:
        raise typer.BadParameter("Output must differ from input unless --in-place is used.")
    try:
        record = read_record(record_file)
        migrated = migrate_record(record, target_version)
        write_record(migrated, destination)
    except (EvidenceFileError, MigrationError, OSError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=2) from exc
    console.print(f"Migrated {record_file} -> {destination} ({target_version})")


@app.command()
def ingest(
    record_file: Annotated[Path, typer.Argument(exists=True, readable=True)],
    store_path: Annotated[Path, typer.Option("--store", envvar="MYELINMESH_STORE")] = Path(
        ".myelinmesh"
    ),
    replace: Annotated[
        bool, typer.Option(help="Replace an existing record with the same id.")
    ] = False,
) -> None:
    try:
        record = read_record(record_file)
        stored = EvidenceStore(store_path).ingest(record, replace=replace)
    except (EvidenceFileError, FileExistsError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=2) from exc
    console.print(
        f"Ingested [bold]{stored.identity.evidence_id}[/bold] ({stored.content_hash}) into {store_path}"
    )


def _expand_batch_paths(paths: list[Path]) -> list[Path]:
    expanded: set[Path] = set()
    for path in paths:
        if path.is_file():
            expanded.add(path)
        elif path.is_dir():
            expanded.update(
                candidate for candidate in path.rglob("*.mer.json") if candidate.is_file()
            )
        else:
            raise typer.BadParameter(f"Path does not exist: {path}")
    return sorted(expanded, key=lambda item: str(item))


@app.command("ingest-batch")
def ingest_batch(
    paths: Annotated[list[Path], typer.Argument(min=1, help="MER files or directories to ingest.")],
    store_path: Annotated[Path, typer.Option("--store", envvar="MYELINMESH_STORE")] = Path(
        ".myelinmesh"
    ),
    replace: Annotated[
        bool, typer.Option(help="Replace records with the same evidence id.")
    ] = False,
    json_output: Annotated[
        bool, typer.Option("--json", help="Emit a machine-readable summary.")
    ] = False,
) -> None:
    files = _expand_batch_paths(paths)
    report = EvidenceStore(store_path).ingest_many(files, replace=replace)
    if json_output:
        console.print_json(json.dumps(report.as_dict()))
    else:
        console.print(
            "Batch ingestion: "
            f"{report.inserted} inserted, {report.duplicates} duplicates, "
            f"{report.invalid} invalid, {report.failed} failed"
        )
    if report.invalid or report.failed:
        raise typer.Exit(code=2)


@app.command()
def adapt(
    producer: Annotated[
        str, typer.Argument(help="Producer: tool-semantics, myelinmesh, or parallax.")
    ],
    input_file: Annotated[Path, typer.Argument(exists=True, readable=True)],
    output_dir: Annotated[Path, typer.Option("--output-dir")] = Path("converted-evidence"),
) -> None:
    """Convert a supported producer report into MER records."""
    adapters: dict[str, EvidenceAdapter] = {
        "tool-semantics": ToolSemanticsAdapter(),
        "myelinmesh": MyelinMeshAdapter(),
        "parallax": ParallaxAdapter(),
    }
    adapter = adapters.get(producer)
    if adapter is None:
        console.print(f"[red]Unsupported producer: {producer}[/red]")
        raise typer.Exit(code=2)
    try:
        payload = json.loads(input_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        console.print(f"[red]Unable to read producer report: {exc}[/red]")
        raise typer.Exit(code=2) from exc
    if not isinstance(payload, dict) or not adapter.can_handle(payload):
        console.print(f"[red]Input does not match the {producer} adapter contract.[/red]")
        raise typer.Exit(code=2)
    output_dir.mkdir(parents=True, exist_ok=True)
    records = adapter.convert(payload)
    for record in records:
        output = output_dir / f"{record.identity.evidence_id}.mer.json"
        write_record(record, output)
        console.print(f"Wrote [bold]{output}[/bold]")


def _render_summaries(rows: list[EvidenceSummary]) -> None:
    table = Table(show_header=True, header_style="bold")
    table.add_column("Evidence ID")
    table.add_column("Project")
    table.add_column("Domain")
    table.add_column("System")
    table.add_column("Failure")
    table.add_column("Severity")
    for row in rows:
        table.add_row(
            row.evidence_id,
            row.project,
            row.domain,
            row.system,
            row.failure_class or "—",
            row.severity or "—",
        )
    console.print(table)


@app.command("list")
def list_records(
    store_path: Annotated[Path, typer.Option("--store", envvar="MYELINMESH_STORE")] = Path(
        ".myelinmesh"
    ),
    limit: Annotated[int, typer.Option(min=1, max=10000)] = 100,
) -> None:
    _render_summaries(EvidenceStore(store_path).list(limit=limit))


@app.command()
def show(
    evidence_id: Annotated[str, typer.Argument()],
    store_path: Annotated[Path, typer.Option("--store", envvar="MYELINMESH_STORE")] = Path(
        ".myelinmesh"
    ),
) -> None:
    try:
        record = EvidenceStore(store_path).get(evidence_id)
    except KeyError as exc:
        console.print(f"[red]Unknown evidence id: {evidence_id}[/red]")
        raise typer.Exit(code=2) from exc
    console.print_json(json.dumps(record.model_dump(mode="json")))


@app.command()
def search(
    query: Annotated[str, typer.Argument(min=1)],
    store_path: Annotated[Path, typer.Option("--store", envvar="MYELINMESH_STORE")] = Path(
        ".myelinmesh"
    ),
    limit: Annotated[int, typer.Option(min=1, max=1000)] = 20,
) -> None:
    _render_summaries(EvidenceStore(store_path).search(query, limit=limit))


@app.command()
def stats(
    store_path: Annotated[Path, typer.Option("--store", envvar="MYELINMESH_STORE")] = Path(
        ".myelinmesh"
    ),
) -> None:
    console.print_json(json.dumps(EvidenceStore(store_path).stats()))
