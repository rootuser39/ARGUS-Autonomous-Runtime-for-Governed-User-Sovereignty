from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Intent:
    raw: str
    objective: str
    constraints: list[str] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    requested_actions: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PlanStep:
    id: str
    action: str
    description: str
    status: str = "pending"


@dataclass(slots=True)
class ExecutionPlan:
    objective: str
    steps: list[PlanStep]


@dataclass(slots=True)
class RouteDecision:
    model_tier: str
    reason: str


@dataclass(slots=True)
class ExecutionTrace:
    intent: Intent
    plan: ExecutionPlan
    route: RouteDecision
    result: str
    verified: bool
    memory_written: bool
    provider: str = "unknown"
    model: str = "unknown"
    latency_ms: float = 0.0
    input_tokens: int | None = None
    output_tokens: int | None = None
