from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict

from argus.core.orchestrator import Orchestrator
from argus.providers import NebiusProvider, StubProvider


def _build_provider(name: str):
    if name == "nebius":
        return NebiusProvider()
    return StubProvider()


def main() -> None:
    parser = argparse.ArgumentParser(prog="argus")
    parser.add_argument("request", nargs="?", help="Objective for ARGUS to process")
    parser.add_argument(
        "--provider",
        choices=("stub", "nebius"),
        default=os.getenv("ARGUS_PROVIDER", "stub"),
        help="Inference backend (default: ARGUS_PROVIDER or stub)",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List models visible to the configured Nebius Token Factory key",
    )
    args = parser.parse_args()

    provider = _build_provider(args.provider)

    if args.list_models:
        if not isinstance(provider, NebiusProvider):
            parser.error("--list-models requires --provider nebius")
        print(json.dumps(provider.list_models(), indent=2))
        return

    if not args.request:
        parser.error("request is required unless --list-models is used")

    trace = Orchestrator(provider=provider).handle(args.request)
    print(json.dumps(asdict(trace), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
