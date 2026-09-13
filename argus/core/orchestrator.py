from __future__ import annotations

from dataclasses import replace

from argus.core.intent import IntentEngine
from argus.core.memory import JsonlMemory
from argus.core.models import ExecutionTrace
from argus.core.planner import Planner
from argus.core.router import ModelRouter
from argus.providers.base import InferenceProvider, StubProvider


class Orchestrator:
    def __init__(
        self,
        *,
        intent_engine: IntentEngine | None = None,
        planner: Planner | None = None,
        router: ModelRouter | None = None,
        provider: InferenceProvider | None = None,
        memory: JsonlMemory | None = None,
    ) -> None:
        self.intent_engine = intent_engine or IntentEngine()
        self.planner = planner or Planner()
        self.router = router or ModelRouter()
        self.provider = provider or StubProvider()
        self.memory = memory or JsonlMemory()

    def handle(self, request: str) -> ExecutionTrace:
        intent = self.intent_engine.parse(request)
        plan = self.planner.build(intent)
        route = self.router.choose(intent, plan)
        inference = self.provider.generate(intent.objective, route.model_tier)

        # Bootstrap verification: a provider must return non-empty output.
        # A semantic verifier becomes its own stage in a later milestone.
        verified = bool(inference.text.strip())
        trace = ExecutionTrace(
            intent=intent,
            plan=plan,
            route=route,
            result=inference.text,
            verified=verified,
            memory_written=False,
            provider=inference.provider,
            model=inference.model,
            latency_ms=inference.latency_ms,
            input_tokens=inference.input_tokens,
            output_tokens=inference.output_tokens,
        )

        if verified:
            self.memory.write(trace)
            trace = replace(trace, memory_written=True)

        return trace
