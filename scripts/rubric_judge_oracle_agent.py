#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

FIXTURE_DIR = Path(__file__).resolve().parents[1] / "examples" / "evals"


REQUEST_SCHEMA_VERSION = "rubric-judge-request/v1"


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def load_fixtures() -> dict[str, dict[str, Any]]:
    # The request carries no answer key (a judge handed one can copy it), so the oracle
    # reads the fixture pack itself. It is the only "judge" allowed to.
    fixtures: dict[str, dict[str, Any]] = {}
    for path in sorted(FIXTURE_DIR.glob("rubric-score-*.json")):
        fixture = json.loads(path.read_text(encoding="utf-8"))
        fixtures[fixture["id"]] = fixture
    return fixtures


def build_oracle_judgement(record: dict[str, Any], fixtures: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if "expected" in record:
        fail(f"{record.get('id', '<missing id>')}: the request carries an answer key; requests must not")
    fixture = fixtures.get(record.get("id", ""))
    if fixture is None:
        fail(f"{record.get('id', '<missing id>')}: no fixture with that id in {FIXTURE_DIR}")

    return {
        "score": fixture["expected_score"],
        "verdict": fixture["expected_verdict"],
        "cap": fixture["expected_cap"],
        "hard_limits": fixture["hard_limits"],
        "dimension_scores": fixture["dimension_scores"],
        "failed_dimensions": fixture["expected_failed_dimensions"],
        "rationale": "Oracle self-test output generated from the fixture pack.",
        "improvement_suggestions": [
            "Use a real external judge agent for semantic evaluation.",
            "Keep fixture expectations aligned with the design-quality rubric.",
        ],
    }


def main() -> None:
    fixtures = load_fixtures()
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
            "judge": build_oracle_judgement(record, fixtures),
        }
        print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
