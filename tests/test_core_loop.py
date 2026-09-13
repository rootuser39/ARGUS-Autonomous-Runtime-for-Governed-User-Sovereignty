from pathlib import Path

import pytest

from argus.core.intent import IntentEngine
from argus.core.memory import JsonlMemory
from argus.core.orchestrator import Orchestrator


def test_empty_request_is_rejected() -> None:
    with pytest.raises(ValueError):
        IntentEngine().parse("   ")


def test_complete_loop_writes_verified_memory(tmp_path: Path) -> None:
    memory = JsonlMemory(tmp_path / "memory.jsonl")
    trace = Orchestrator(memory=memory).handle(
        "Analyze my AI fabric project and identify the most important missing component"
    )

    assert trace.verified is True
    assert trace.memory_written is True
    assert trace.route.model_tier == "nemotron-super"
    assert memory.tail(1)[0]["intent"]["objective"].startswith("Analyze my AI fabric")


def test_simple_request_routes_to_nano(tmp_path: Path) -> None:
    trace = Orchestrator(memory=JsonlMemory(tmp_path / "memory.jsonl")).handle(
        "Summarize this note"
    )
    assert trace.route.model_tier == "nemotron-nano"
