import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

from argus.core.memory import JsonlMemory
from argus.core.orchestrator import Orchestrator
from argus.providers.base import InferenceResult


class EmptyProvider:
    def generate(self, prompt: str, model_tier: str) -> InferenceResult:
        return InferenceResult(text="   ", provider="empty", model="none", latency_ms=0.0)


def test_default_does_not_persist_even_with_memory_object(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    trace = Orchestrator(memory=JsonlMemory(path)).handle("Summarize private notes")
    assert trace.verified
    assert trace.verification_method == "non_empty_response_only"
    assert not trace.memory_written
    assert not path.exists()


def test_opt_in_persists_trace(tmp_path: Path) -> None:
    memory = JsonlMemory(tmp_path / ".argus" / "memory.jsonl")
    trace = Orchestrator(memory=memory, persist_memory=True).handle("Summarize private notes")
    assert trace.memory_written
    assert memory.tail(1)[0]["intent"]["objective"] == "Summarize private notes"


def test_empty_response_never_persists(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    trace = Orchestrator(
        provider=EmptyProvider(),
        memory=JsonlMemory(path),
        persist_memory=True,
    ).handle("Summarize private notes")
    assert not trace.verified
    assert not trace.memory_written
    assert not path.exists()


def test_memory_tail_is_bounded_and_validates_limits(tmp_path: Path) -> None:
    memory = JsonlMemory(tmp_path / "memory.jsonl")
    app = Orchestrator(memory=memory, persist_memory=True)
    for i in range(5):
        app.handle(f"Summarize note {i}")
    assert len(memory.tail(2)) == 2
    assert memory.tail(2)[0]["intent"]["objective"].endswith("3")
    assert memory.tail(0) == []
    with pytest.raises(ValueError):
        memory.tail(-1)


@pytest.mark.skipif(os.name == "nt", reason="POSIX file permissions")
def test_new_journal_is_private_on_posix(tmp_path: Path) -> None:
    memory = JsonlMemory(tmp_path / "memory.jsonl")
    Orchestrator(memory=memory, persist_memory=True).handle("Summarize note")
    assert stat.S_IMODE(memory.path.stat().st_mode) == 0o600


@pytest.mark.skipif(os.name == "nt", reason="symlink setup may require special permissions")
def test_symlink_memory_target_is_refused(tmp_path: Path) -> None:
    target = tmp_path / "target.jsonl"
    target.write_text("original\n", encoding="utf-8")
    link = tmp_path / "link.jsonl"
    link.symlink_to(target)
    with pytest.raises(OSError, match="symbolic link"):
        Orchestrator(memory=JsonlMemory(link), persist_memory=True).handle("Summarize notes")
    assert target.read_text(encoding="utf-8") == "original\n"


def test_cli_memory_flag_is_explicit(tmp_path: Path) -> None:
    path = tmp_path / "journal.jsonl"
    base = [
        sys.executable, "-m", "argus.cli", "--provider", "stub",
        "--memory-path", str(path),
    ]
    no_memory = subprocess.run(
        [*base, "Summarize my note"], capture_output=True, text=True, check=True
    )
    assert json.loads(no_memory.stdout)["memory_written"] is False
    assert not path.exists()
    with_memory = subprocess.run(
        [*base, "--remember", "Summarize my note"],
        capture_output=True, text=True, check=True,
    )
    assert json.loads(with_memory.stdout)["memory_written"] is True
    assert path.exists()
