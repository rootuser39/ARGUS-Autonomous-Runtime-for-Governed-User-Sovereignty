# ARGUS

**Autonomous Runtime for Governed User Sovereignty**

ARGUS is a sovereign personal-AI runtime designed around one core execution spine:

`request -> intent -> plan -> model route -> execute -> verify -> remember`

This repository is being built for the Nebius x NVIDIA Global AI Hackathon 2026, while remaining a standalone subsystem of the broader CORTEX architecture.

## Current milestone

Build the minimum complete loop:

1. Parse a user request into structured intent.
2. Convert intent into an execution plan.
3. Select an appropriate NVIDIA/Nemotron model tier.
4. Execute through a model/tool adapter.
5. Persist a compact memory record.
6. Return an auditable execution trace.

## Architecture

```text
User
  |
  v
Intent Engine
  |
  v
Planner
  |
  v
Model Router
  |
  v
Execution / Tools
  |
  v
Verification
  |
  v
Memory
```

Planned modules:

- `argus/core/intent` — goal, constraint, context and action extraction
- `argus/core/planner` — task decomposition
- `argus/core/router` — model selection policy
- `argus/core/memory` — persistent state
- `argus/core/orchestrator` — end-to-end execution loop
- `argus/agents` — specialist agents
- `argus/tools` — governed tool adapters
- `argus/permissions` — capability and approval policy
- `argus/execution` — sandboxed execution
- `argus/api` — external API surface
- `argus/ui` — execution-graph interface
- `tests` — deterministic tests
- `benchmarks` — routing, latency and quality evaluation

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
argus "Analyze my AI fabric project and identify the most important missing component"
```

The initial implementation uses a deterministic local stub so the architecture can be tested before Nebius credentials are introduced.

## Design principles

- Runtime over chatbot.
- Explicit intent over prompt guessing.
- Governed tools over unrestricted agency.
- Observable execution over hidden chains.
- Persistent project state over disposable chat history.
- Model routing over using the largest model for everything.
- Verification before memory write.

## License

MIT
