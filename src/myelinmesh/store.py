from __future__ import annotations

import builtins
import json
import sqlite3
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from myelinmesh.hashing import with_content_hash
from myelinmesh.io import read_record, write_record
from myelinmesh.models import EvidenceRecord

SCHEMA = """
CREATE TABLE IF NOT EXISTS evidence (
    evidence_id TEXT PRIMARY KEY,
    project TEXT NOT NULL,
    captured_at TEXT NOT NULL,
    source_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    system TEXT NOT NULL,
    failure_class TEXT,
    severity TEXT,
    content_hash TEXT NOT NULL,
    path TEXT NOT NULL,
    searchable_text TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_evidence_project ON evidence(project);
CREATE INDEX IF NOT EXISTS idx_evidence_domain ON evidence(domain);
CREATE INDEX IF NOT EXISTS idx_evidence_failure ON evidence(failure_class);
"""


@dataclass(frozen=True)
class EvidenceSummary:
    evidence_id: str
    project: str
    captured_at: str
    source_type: str
    domain: str
    system: str
    failure_class: str | None
    severity: str | None
    content_hash: str


@dataclass(frozen=True)
class BatchIngestReport:
    inserted: int
    duplicates: int
    invalid: int
    failed: int
    results: tuple[dict[str, str], ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "inserted": self.inserted,
            "duplicates": self.duplicates,
            "invalid": self.invalid,
            "failed": self.failed,
            "results": list(self.results),
        }


class EvidenceStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.records_dir = root / "records"
        self.database_path = root / "index.sqlite3"

    def initialize(self) -> None:
        self.records_dir.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.executescript(SCHEMA)
        manifest = self.root / "store.json"
        if not manifest.exists():
            manifest.write_text(
                json.dumps({"format": "myelinmesh-store", "version": "0.1.0"}, indent=2) + "\n",
                encoding="utf-8",
            )

    def ingest(self, record: EvidenceRecord, *, replace: bool = False) -> EvidenceRecord:
        self.initialize()
        normalized = with_content_hash(record)
        record_path = self.records_dir / f"{normalized.identity.evidence_id}.mer.json"

        if record_path.exists() and not replace:
            existing = read_record(record_path)
            if existing.content_hash == normalized.content_hash:
                return existing
            raise FileExistsError(
                f"Evidence id already exists with different content: {normalized.identity.evidence_id}"
            )

        write_record(normalized, record_path)
        payload = normalized.model_dump(mode="json")
        searchable = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        failure_class = normalized.failure.failure_class if normalized.failure else None
        severity = normalized.failure.severity.value if normalized.failure else None

        statement = "INSERT OR REPLACE" if replace else "INSERT"
        with self._connect() as connection:
            connection.execute(
                f"""
                {statement} INTO evidence (
                    evidence_id, project, captured_at, source_type, domain, system,
                    failure_class, severity, content_hash, path, searchable_text
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    normalized.identity.evidence_id,
                    normalized.identity.project,
                    normalized.identity.captured_at.isoformat(),
                    normalized.provenance.source_type.value,
                    normalized.context.domain.value,
                    normalized.context.system,
                    failure_class,
                    severity,
                    normalized.content_hash,
                    str(record_path.relative_to(self.root)),
                    searchable,
                ),
            )
        return normalized

    def ingest_many(
        self,
        paths: Iterable[Path],
        *,
        replace: bool = False,
    ) -> BatchIngestReport:
        """Ingest records in deterministic path order with per-file outcomes."""
        self.initialize()
        inserted = 0
        duplicates = 0
        invalid = 0
        failed = 0
        results: list[dict[str, str]] = []

        for path in sorted({Path(path) for path in paths}, key=lambda item: str(item)):
            path_label = str(path)
            try:
                record = read_record(path)
            except ValueError as exc:
                invalid += 1
                results.append({"path": path_label, "status": "invalid", "error": str(exc)})
                continue

            normalized = with_content_hash(record)
            record_path = self.records_dir / f"{normalized.identity.evidence_id}.mer.json"
            if record_path.exists() and not replace:
                existing = read_record(record_path)
                if existing.content_hash == normalized.content_hash:
                    duplicates += 1
                    results.append({"path": path_label, "status": "duplicate"})
                else:
                    failed += 1
                    results.append(
                        {
                            "path": path_label,
                            "status": "failed",
                            "error": "evidence id already exists with different content",
                        }
                    )
                continue

            with self._connect() as connection:
                existing_hash = connection.execute(
                    "SELECT evidence_id FROM evidence WHERE content_hash = ? LIMIT 1",
                    (normalized.content_hash,),
                ).fetchone()
            if existing_hash is not None and not replace:
                duplicates += 1
                results.append(
                    {
                        "path": path_label,
                        "status": "duplicate",
                        "existing_evidence_id": str(existing_hash[0]),
                    }
                )
                continue

            try:
                self.ingest(normalized, replace=replace)
            except (OSError, sqlite3.Error, FileExistsError) as exc:
                failed += 1
                results.append({"path": path_label, "status": "failed", "error": str(exc)})
                continue
            inserted += 1
            results.append(
                {
                    "path": path_label,
                    "status": "inserted",
                    "evidence_id": normalized.identity.evidence_id,
                }
            )

        return BatchIngestReport(inserted, duplicates, invalid, failed, tuple(results))

    def get(self, evidence_id: str) -> EvidenceRecord:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT path FROM evidence WHERE evidence_id = ?", (evidence_id,)
            ).fetchone()
        if row is None:
            raise KeyError(evidence_id)
        return read_record(self.root / str(row[0]))

    def list(self, *, limit: int = 100) -> builtins.list[EvidenceSummary]:
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT evidence_id, project, captured_at, source_type, domain, system,
                       failure_class, severity, content_hash
                FROM evidence ORDER BY captured_at DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [EvidenceSummary(*row) for row in rows]

    def search(self, query: str, *, limit: int = 20) -> builtins.list[EvidenceSummary]:
        self.initialize()
        tokens = [token for token in query.lower().split() if token]
        if not tokens:
            return []
        predicates = " AND ".join("lower(searchable_text) LIKE ?" for _ in tokens)
        parameters: builtins.list[object] = [f"%{token}%" for token in tokens]
        parameters.append(limit)
        with self._connect() as connection:
            rows = connection.execute(
                f"""
                SELECT evidence_id, project, captured_at, source_type, domain, system,
                       failure_class, severity, content_hash
                FROM evidence
                WHERE {predicates}
                ORDER BY captured_at DESC LIMIT ?
                """,
                parameters,
            ).fetchall()
        return [EvidenceSummary(*row) for row in rows]

    def stats(self) -> dict[str, object]:
        self.initialize()
        with self._connect() as connection:
            total = connection.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]
            projects = connection.execute(
                "SELECT project, COUNT(*) FROM evidence GROUP BY project ORDER BY COUNT(*) DESC"
            ).fetchall()
            domains = connection.execute(
                "SELECT domain, COUNT(*) FROM evidence GROUP BY domain ORDER BY COUNT(*) DESC"
            ).fetchall()
            failures = connection.execute(
                """
                SELECT COALESCE(failure_class, 'none'), COUNT(*)
                FROM evidence GROUP BY failure_class ORDER BY COUNT(*) DESC
                """
            ).fetchall()
        return {
            "total": total,
            "projects": dict(projects),
            "domains": dict(domains),
            "failure_classes": dict(failures),
        }

    def iter_records(self) -> Iterator[EvidenceRecord]:
        for summary in self.list(limit=1_000_000):
            yield self.get(summary.evidence_id)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        self.root.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path)
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()
