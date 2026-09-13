from __future__ import annotations

from argus.core.models import ExecutionPlan, Intent, PlanStep


class Planner:
    def build(self, intent: Intent) -> ExecutionPlan:
        steps: list[PlanStep] = []
        for index, action in enumerate(intent.requested_actions, start=1):
            steps.append(
                PlanStep(
                    id=f"step-{index}",
                    action=action,
                    description=f"Execute '{action}' for objective: {intent.objective}",
                )
            )

        steps.append(
            PlanStep(
                id=f"step-{len(steps) + 1}",
                action="verify",
                description="Verify that the execution result addresses the objective.",
            )
        )
        return ExecutionPlan(objective=intent.objective, steps=steps)
