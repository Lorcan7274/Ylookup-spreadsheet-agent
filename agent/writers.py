"""Append-only writers for the /out artifacts. jsonl appends of one line are atomic
enough for our concurrency (single process, small writes)."""

import json
import os
from pathlib import Path


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def log(out_dir: Path, line: str) -> None:
    print(line, flush=True)
    # The Docker entrypoint captures complete stdout/stderr with tee. Writing here
    # too would duplicate lines and let two processes append to run.log at once.
    if os.environ.get("CAPTURE_STDIO_RUN_LOG") == "1":
        return
    with (out_dir / "run.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
