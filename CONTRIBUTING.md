# Contributing to ARGUS

ARGUS is an early-stage open-source Python project. Contributions should improve reproducibility, governed execution, testing, or clear evidence of what the runtime can and cannot do.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest -q
argus --provider stub "Summarize this note"
```

Windows PowerShell: activate with `.venv\Scripts\Activate.ps1`.

`stub` requires no API key. Never include credentials, confidential prompts, or real user records in tests.

## Propose a change

1. Open an issue describing a specific failure, behavior change, or experiment with a reproducible example.
2. Make a focused branch and add tests for changed behavior.
3. Run `python -m pytest -q` and a stub CLI smoke test.
4. Explain observed results, assumptions, limits, and any change to memory persistence or external data transfer in your pull request.
5. Provide opt-in behavior for any new side effect or external tool access.

The maintainers may ask for changes before merging. No claim of current community size, production validation, or cross-platform security audit is made.

## Contribution priorities

- Semantic verification independent of the inference provider.
- Permissioned tools with human approval for state-changing actions.
- Privacy controls: selective retention, redaction, deletion, export, and encryption options.
- Measured model routing and reproducible benchmarks.
- Better documentation and meaningful bug reports.

## License

By contributing, you agree your contribution can be distributed under the repository's MIT license.
