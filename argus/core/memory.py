from __future__ import annotations

import json
import os
from collections import deque
from dataclasses import asdict
from pathlib import Path

from argus.core.models import ExecutionTrace


class JsonlMemory:
    """Optional local trace journal; never enabled implicitly by Orchestrator."""

    def __init__(self, path: str | Path = ".argus/memory.jsonl") -> None:
        self.path = Path(path)

    def write(self, trace: ExecutionTrace) -> None:
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if self.path.is_symlink():
            raise OSError("Refusing to write memory through a symbolic link")
        flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        fd = os.open(self.path, flags, 0o600)
        with os.fdopen(fd, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(trace), ensure_ascii=False) + "\n")

    def tail(self, limit: int = 10) -> list[dict]:
        if limit < 0:
            raise ValueError("limit must be non-negative")
        if limit == 0:
            return []
        if self.path.is_symlink():
            raise OSError("Refusing to read memory through a symbolic link")
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as handle:
            lines = deque(handle, maxlen=limit)
        return [json.loads(line) for line in lines if line.strip()]
