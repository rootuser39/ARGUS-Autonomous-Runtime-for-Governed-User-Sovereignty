from __future__ import annotations

from dataclasses import replace

from argus.core.intent import IntentEngine
from argus.core.memory import JsonlMemory
from argus.core.models import ExecutionTrace
from argus.core.planner import Planner
from argus.core.router import ModelRouter


class StubExecutor:
    """Local deterministic executor used until Nebius integration is wired."""

    def run(self, request: str, model_tier: str) -> str:
        return f"[{model_tier}] ARGUS accepted objective: {request}"


class Orchestrator:
    def __init__(
        self,
        *,
        intent_engine: IntentEngine | None = None,
        planner: Planner | None = None,
        router: ModelRouter | None = None,
        executor: StubExecutor | None = None,
        memory: JsonlMemory | None = None,
    ) -> None:
        self.intent_engine = intent_engine or IntentEngine()
        self.planner = planner or Planner()
        self.router = router or ModelRouter()
        self.executor = executor or StubExecutor()
        self.memory = memory or JsonlMemory()

    def handle(self, request: str) -> ExecutionTrace:
        intent = self.intent_engine.parse(request)
        plan = self.planner.build(intent)
        route = self.router.choose(intent, plan)
        result = self.executor.run(intent.objective, route.model_tier)

        verified = bool(result.strip()) and intent.objective in result
        trace = ExecutionTrace(
            intent=intent,
            plan=plan,
            route=route,
            result=result,
            verified=verified,
            memory_written=False,
        )

        if verified:
            self.memory.write(trace)
            trace = replace(trace, memory_written=True)

        return trace
