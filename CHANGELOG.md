# Changelog

## 0.3.0 (development; not tagged or released)

### Changed

- **Breaking:** local trace persistence is now explicitly opt-in. Pass `--remember` on the CLI or `persist_memory=True` when constructing `Orchestrator`.
- The CLI supports `--memory-path` and respects `ARGUS_MEMORY_PATH`.
- `verification_method=non_empty_response_only` identifies the current non-semantic verification check.
- A persisted record now correctly marks `memory_written=true`.

### Hardening

- New JSONL journals request owner-only permissions on POSIX systems.
- Direct symbolic-link journal targets are refused.
- `tail(limit)` reads only the requested number of lines and validates limits.
- Added regression tests, a three-version Python CI matrix, and contributor/privacy documentation.

### Known limits

- No semantic or factual verification; no general-purpose tool-execution sandbox.
- Existing journal permissions and Windows ACLs are not modified.
- No live Nebius integration test or external user adoption is asserted.

## 0.2.0 (previous development milestone)

- Initial CLI, deterministic stub, Nebius Token Factory provider, route selection, and JSONL trace journal.
