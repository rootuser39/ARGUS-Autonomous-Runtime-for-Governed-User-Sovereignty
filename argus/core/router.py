from __future__ import annotations

from argus.core.models import ExecutionPlan, Intent, RouteDecision


class ModelRouter:
    """Bootstrap routing policy for Nemotron tiers.

    The policy is deliberately transparent so routing decisions can be audited
    and benchmarked before adaptive routing is introduced.
    """

    def choose(self, intent: Intent, plan: ExecutionPlan) -> RouteDecision:
        complex_actions = {"analyze", "research", "compare", "build"}
        action_set = set(intent.requested_actions)

        if len(plan.steps) >= 5 or len(complex_actions & action_set) >= 2:
            return RouteDecision(
                model_tier="nemotron-ultra",
                reason="multi-step or multi-domain reasoning required",
            )

        if complex_actions & action_set:
            return RouteDecision(
                model_tier="nemotron-super",
                reason="general reasoning or technical execution required",
            )

        return RouteDecision(
            model_tier="nemotron-nano",
            reason="low-complexity request suitable for fast inference",
        )
