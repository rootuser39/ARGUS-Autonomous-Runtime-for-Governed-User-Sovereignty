from __future__ import annotations

from argus.core.models import Intent


class IntentEngine:
    """Deterministic bootstrap intent parser.

    This is intentionally simple. It provides a stable contract that can later
    be backed by Nemotron without forcing the rest of ARGUS to depend on one
    prompting strategy.
    """

    ACTION_KEYWORDS = {
        "analyze": "analyze",
        "research": "research",
        "find": "research",
        "build": "build",
        "create": "build",
        "implement": "build",
        "test": "test",
        "compare": "compare",
        "summarize": "summarize",
    }

    def parse(self, request: str) -> Intent:
        cleaned = " ".join(request.strip().split())
        if not cleaned:
            raise ValueError("request must not be empty")

        lowered = cleaned.lower()
        actions = [
            action
            for keyword, action in self.ACTION_KEYWORDS.items()
            if keyword in lowered
        ]
        actions = list(dict.fromkeys(actions)) or ["respond"]

        return Intent(
            raw=cleaned,
            objective=cleaned,
            requested_actions=actions,
            context={},
            constraints=[],
        )
