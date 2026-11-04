# Security and privacy

ARGUS is an experimental, pre-production personal-AI runtime, not a trusted autonomous agent.

## Data flow

- `--provider stub` never calls a remote inference API.
- `--provider nebius` sends the complete request to the configured Nebius Token Factory endpoint. Review that provider's policies before transmitting sensitive data.
- Normal CLI runs return the trace to stdout but do **not** save it to the ARGUS journal.
- `--remember` explicitly opts in to a local JSONL journal of full user requests, outputs, routing choices, and token/latency telemetry. This is **not** anonymized or encrypted storage.
- Library callers may enable the same behavior using `Orchestrator(persist_memory=True)`.

## Storage limits

- Newly created journal files request POSIX mode `0600`; new journal directories request `0700` (subject to parent-directory configuration).
- Existing files retain their pre-existing permissions. On Windows, file access is governed by Windows ACLs; ARGUS does not configure them.
- The journal refuses symbolic-link targets (including using `O_NOFOLLOW` when available). This is not a complete defense against malicious parent directories, races, backup services, or privileged local actors.
- Do not enable journaling for secrets or personal data you cannot afford to retain.
- Remove `.argus/memory.jsonl` yourself when you want to erase a local journal. Filesystem snapshots and backups may contain copies.

## Execution and verification limits

- `verified=True` currently means only `verification_method=non_empty_response_only`: output had non-whitespace text.
- This does not establish factual correctness, authorization, safety, successful action, or task completion.
- Planning is descriptive. ARGUS has no general-purpose tool-execution sandbox, policy-enforced permissions, or autonomous mutation engine in this milestone.
- The stub provider is deterministic simulation, not an LLM. A live provider requires credentials and external connectivity.

## Security reports

Do not post active credentials or detailed vulnerability exploits in public issues. Contact the maintainer privately through an available GitHub security-reporting channel when supported. Avoid sharing sensitive traces in bug reports.

## Roadmap

Before enabling live tools: implement explicit capabilities, per-action approval for side effects, sandboxing, trace redaction/retention controls, and semantic verification with adversarial tests.
