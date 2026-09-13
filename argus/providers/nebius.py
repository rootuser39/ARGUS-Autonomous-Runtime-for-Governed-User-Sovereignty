from __future__ import annotations

import os
from time import perf_counter
from typing import Any

from openai import OpenAI

from argus.providers.base import InferenceResult


DEFAULT_BASE_URL = "https://api.tokenfactory.nebius.com/v1"
DEFAULT_MODELS = {
    "nemotron-nano": "nvidia/Nemotron-3_5-Lightning",
    "nemotron-super": "nvidia/nemotron-3-super-120b-a12b",
    "nemotron-ultra": "nvidia/Nemotron-3-Ultra-550b-a55b",
}


class NebiusProvider:
    """Nebius Token Factory adapter using its OpenAI-compatible API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        models: dict[str, str] | None = None,
        timeout: float = 90.0,
    ) -> None:
        key = api_key or os.getenv("NEBIUS_API_KEY")
        if not key:
            raise RuntimeError(
                "NEBIUS_API_KEY is required when ARGUS uses the Nebius provider"
            )

        self.base_url = base_url or os.getenv("NEBIUS_BASE_URL", DEFAULT_BASE_URL)
        self.models = {
            "nemotron-nano": os.getenv(
                "ARGUS_NEMOTRON_NANO_MODEL", DEFAULT_MODELS["nemotron-nano"]
            ),
            "nemotron-super": os.getenv(
                "ARGUS_NEMOTRON_SUPER_MODEL", DEFAULT_MODELS["nemotron-super"]
            ),
            "nemotron-ultra": os.getenv(
                "ARGUS_NEMOTRON_ULTRA_MODEL", DEFAULT_MODELS["nemotron-ultra"]
            ),
        }
        if models:
            self.models.update(models)

        self.client = OpenAI(api_key=key, base_url=self.base_url, timeout=timeout)

    def generate(self, prompt: str, model_tier: str) -> InferenceResult:
        try:
            model = self.models[model_tier]
        except KeyError as exc:
            raise ValueError(f"Unsupported ARGUS model tier: {model_tier}") from exc

        started = perf_counter()
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are ARGUS, an execution-oriented personal AI runtime. "
                        "Answer the user's objective directly and precisely."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        latency_ms = (perf_counter() - started) * 1000

        message = response.choices[0].message.content if response.choices else ""
        text = message if isinstance(message, str) else str(message or "")
        usage = response.usage
        metadata: dict[str, Any] = {}
        if usage is not None and hasattr(usage, "model_dump"):
            metadata["usage"] = usage.model_dump()

        return InferenceResult(
            text=text,
            provider="nebius-token-factory",
            model=model,
            latency_ms=latency_ms,
            input_tokens=getattr(usage, "prompt_tokens", None),
            output_tokens=getattr(usage, "completion_tokens", None),
            metadata=metadata,
        )

    def list_models(self) -> list[str]:
        """Return model IDs currently visible to the configured Token Factory key."""
        return sorted(model.id for model in self.client.models.list().data)
