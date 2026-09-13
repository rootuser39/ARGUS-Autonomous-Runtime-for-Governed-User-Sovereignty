from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(slots=True)
class InferenceResult:
    text: str
    provider: str
    model: str
    latency_ms: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class InferenceProvider(Protocol):
    def generate(self, prompt: str, model_tier: str) -> InferenceResult: ...


class StubProvider:
    """Deterministic provider for local development and tests."""

    def generate(self, prompt: str, model_tier: str) -> InferenceResult:
        return InferenceResult(
            text=f"[{model_tier}] ARGUS accepted objective: {prompt}",
            provider="stub",
            model=f"stub/{model_tier}",
            latency_ms=0.0,
        )
