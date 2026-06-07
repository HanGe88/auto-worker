#!/usr/bin/env python3
"""Inspect a Claude Code auto-worker directory.

Usage:
    python inspect_worker.py <project-root> <worker-name>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def latest_log(log_dir: Path) -> Path | None:
    if not log_dir.exists():
        return None
    logs = sorted(log_dir.glob("*.log"), key=lambda item: item.stat().st_mtime, reverse=True)
    return logs[0] if logs else None


def read_last_runs(runs_path: Path, limit: int = 5) -> list[dict[str, object]]:
    if not runs_path.exists():
        return []

    records: list[dict[str, object]] = []
    for line in runs_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            records.append({"status": "unparseable", "raw": line})
    return records[-limit:]


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: python inspect_worker.py <project-root> <worker-name>", file=sys.stderr)
        return 2

    root = Path(argv[1]).resolve()
    worker_name = argv[2]
    worker_dir = root / ".claude" / "auto-worker" / worker_name

    state_path = worker_dir / "STATE.md"
    handoff_path = worker_dir / "HANDOFF.md"
    failures_path = worker_dir / "FAILURES.md"
    runs_path = worker_dir / "RUNS.jsonl"
    log_path = latest_log(worker_dir / "logs")

    result = {
        "ok": worker_dir.exists(),
        "worker_dir": str(worker_dir),
        "files": {
            "TASKS.md": (worker_dir / "TASKS.md").exists(),
            "STATE.md": state_path.exists(),
            "HANDOFF.md": handoff_path.exists(),
            "FAILURES.md": failures_path.exists(),
            "worker-prompt.md": (worker_dir / "worker-prompt.md").exists(),
            "RUNS.jsonl": runs_path.exists(),
        },
        "state_excerpt": read_text(state_path)[:2000],
        "handoff_excerpt": read_text(handoff_path)[:2000],
        "failures_excerpt": read_text(failures_path)[:1000],
        "recent_runs": read_last_runs(runs_path),
        "latest_log": str(log_path) if log_path else None,
        "latest_log_excerpt": read_text(log_path)[:2000] if log_path else "",
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
