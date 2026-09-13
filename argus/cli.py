from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from argus.core.orchestrator import Orchestrator


def main() -> None:
    parser = argparse.ArgumentParser(prog="argus")
    parser.add_argument("request", help="Objective for ARGUS to process")
    args = parser.parse_args()

    trace = Orchestrator().handle(args.request)
    print(json.dumps(asdict(trace), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
