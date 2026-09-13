# ARGUS

**Autonomous Runtime for Governed User Sovereignty**

ARGUS is a sovereign personal-AI runtime designed around one core execution spine:

`request -> intent -> plan -> model route -> execute -> verify -> remember`

This repository is being built for the Nebius x NVIDIA Global AI Hackathon 2026, while remaining a standalone subsystem of the broader CORTEX architecture.

## Current milestone

The first live inference path now exists:

1. Parse a user request into structured intent.
2. Convert intent into an execution plan.
3. Select an NVIDIA Nemotron tier.
4. Execute through either the deterministic stub or Nebius Token Factory.
5. Capture provider/model/latency/token telemetry.
6. Persist verified output into memory.
7. Return an auditable execution trace.

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
Inference Provider
  |-- StubProvider
  `-- NebiusProvider -> Token Factory -> Nemotron
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
- `argus/providers` — inference provider adapters
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
pip install -e ".[dev]"

# deterministic local path
argus "Analyze my AI fabric project and identify the most important missing component"
```

### Nebius Token Factory

Set your key locally. Never commit it.

```bash
export NEBIUS_API_KEY="..."
argus --provider nebius "Analyze my AI fabric project"
```

On Windows PowerShell:

```powershell
$env:NEBIUS_API_KEY="..."
argus --provider nebius "Analyze my AI fabric project"
```

To inspect the model IDs currently visible to your Token Factory account:

```bash
argus --provider nebius --list-models
```

Model IDs are configurable through environment variables because Token Factory availability changes by account and model IDs are case-sensitive. See `.env.example`.

## Current routing defaults

| ARGUS tier | Token Factory model |
| --- | --- |
| `nemotron-nano` | `nvidia/Nemotron-3_5-Lightning` |
| `nemotron-super` | `nvidia/nemotron-3-super-120b-a12b` |
| `nemotron-ultra` | `nvidia/Nemotron-3-Ultra-550b-a55b` |

These defaults can be overridden without changing source code.

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
