"""Local, best-effort artifacts for inspecting a pipeline run after its terminal closes."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


class RunCache:
    def __init__(self, mode: str):
        root = Path(os.getenv("RUN_CACHE_DIR", ".run-cache"))
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.path = root / f"{timestamp}-{uuid4().hex[:8]}"
        self.path.mkdir(parents=True, exist_ok=True)
        self.write_json(
            "manifest.json",
            {"mode": mode, "started_at": datetime.now(timezone.utc).isoformat()},
        )

    def write_json(self, filename: str, value) -> None:
        def json_default(item):
            if hasattr(item, "model_dump"):
                return item.model_dump(mode="json")
            return str(item)

        try:
            (self.path / filename).write_text(
                json.dumps(value, indent=2, ensure_ascii=False, default=json_default),
                encoding="utf-8",
            )
        except OSError as exc:
            print(f"Unable to write run artifact {filename}: {exc}")

    def write_text(self, filename: str, value: str) -> None:
        try:
            (self.path / filename).write_text(value, encoding="utf-8")
        except OSError as exc:
            print(f"Unable to write run artifact {filename}: {exc}")

    def finish(self, result: dict) -> None:
        self.write_json("result.json", result)


_current_run: RunCache | None = None


def start_run(mode: str) -> RunCache:
    global _current_run
    _current_run = RunCache(mode)
    print(f"Run artifacts will be saved in {_current_run.path}")
    return _current_run


def current_run() -> RunCache | None:
    return _current_run
