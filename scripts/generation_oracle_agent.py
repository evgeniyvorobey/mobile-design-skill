#!/usr/bin/env python3
"""
Deterministic stand-in for a model, so CI can prove the generation-eval adapter.

Reads generation-request JSONL on stdin and writes response JSONL on stdout. For a
request that names a `reference_example`, it replays that committed example's
`## Example output` block; for the rest it emits nothing.

What this proves: the stdin/stdout contract, the JSONL parser, and that the scorer
accepts a response the repository already considers correct. What it does NOT prove:
anything about a model's output. No model runs here — that is the whole point of
having it in CI, and the reason a green badge is not evidence of design quality.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_OUTPUT_RE = re.compile(r"## Example output\s*\n\s*```md\n(?P<body>.*?)\n```", re.DOTALL)


def main() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        request = json.loads(line)
        reference = request.get("reference_example")
        if not reference:
            continue
        match = EXAMPLE_OUTPUT_RE.search((ROOT / reference).read_text(encoding="utf-8"))
        if not match:
            print(f"no `## Example output` block in {reference}", file=sys.stderr)
            raise SystemExit(1)
        sys.stdout.write(
            json.dumps(
                {"id": request["id"], "response": match.group("body").strip()},
                ensure_ascii=False,
            )
            + "\n"
        )


if __name__ == "__main__":
    main()
