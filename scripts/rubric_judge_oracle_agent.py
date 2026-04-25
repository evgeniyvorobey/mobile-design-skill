#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from typing import Any


REQUEST_SCHEMA_VERSION = "rubric-judge-request/v1"


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def build_oracle_judgement(record: dict[str, Any]) -> dict[str, Any]:
    expected = record.get("expected")
    if not isinstance(expected, dict):
        fail(f"{record.get('id', '<missing id>')}: missing expected object")

    return {
        "score": expected["score"],
        "verdict": expected["verdict"],
        "cap": expected["cap"],
        "hard_limits": expected["hard_limits"],
        "dimension_scores": expected["dimension_scores"],
        "failed_dimensions": expected["failed_dimensions"],
        "rationale": "Oracle self-test output generated from request.expected.",
        "improvement_suggestions": [
            "Use a real external judge agent for semantic evaluation.",
            "Keep fixture expectations aligned with the design-quality rubric.",
        ],
    }


def main() -> None:
    for lineno, line in enumerate(sys.stdin, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"stdin:{lineno}: invalid JSON ({exc})")

        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            fail(f"stdin:{lineno}: missing id")

        if record.get("schema_version") != REQUEST_SCHEMA_VERSION:
            fail(
                f"stdin:{lineno}: expected schema_version "
                f"{REQUEST_SCHEMA_VERSION}"
            )

        output = {
            "id": record_id,
            "judge": build_oracle_judgement(record),
        }
        print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
