"""Small local-ingestion benchmark with a stable, reviewable threshold."""

from __future__ import annotations

import argparse
import tempfile
import time
from pathlib import Path

from myelinmesh.io import read_record
from myelinmesh.store import EvidenceStore


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=100)
    args = parser.parse_args()
    source = Path("examples/records/tool-semantic-drift.mer.json")
    record = read_record(source)
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="myelinmesh-benchmark-") as directory:
        store = EvidenceStore(Path(directory))
        store.initialize()
        for index in range(args.iterations):
            store.ingest(
                record.model_copy(
                    update={
                        "identity": record.identity.model_copy(
                            update={"evidence_id": f"benchmark-{index}"}
                        )
                    }
                )
            )
    elapsed = time.perf_counter() - started
    rate = args.iterations / elapsed if elapsed else float("inf")
    print(f"ingested={args.iterations} elapsed_seconds={elapsed:.3f} records_per_second={rate:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
