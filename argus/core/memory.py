from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from argus.core.models import ExecutionTrace


class JsonlMemory:
    def __init__(self, path: str | Path = ".argus/memory.jsonl") -> None:
        self.path = Path(path)

    def write(self, trace: ExecutionTrace) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(trace), ensure_ascii=False) + "\n")

    def tail(self, limit: int = 10) -> list[dict]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8").splitlines()[-limit:]
        return [json.loads(line) for line in lines if line.strip()]
