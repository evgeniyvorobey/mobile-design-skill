#!/usr/bin/env python3
"""A deterministic stand-in judge, so CI can prove the `--judge-command` adapter.

This is NOT a design judge and must never be mistaken for one. It applies one
mechanical rule — name the document that states more values, call a tie
no-meaningful-difference — which is exactly the kind of presence proxy proposal
sections 34 and 35 measured at 0 of 12 on real degradations. Its only job is to
round-trip the request/verdict contract without a model in the loop.

The proof that the *report* discriminates is `run_paired_eval.py --self-test`,
which needs no judge at all. Keeping those two proofs apart is deliberate: an
oracle that also supplied the discrimination would be a green oracle over the
thing under test, which this repository has shipped once already.
"""
from __future__ import annotations

import json
import re
import sys

REQUEST_SCHEMA_VERSION = "paired-eval-request/v1"
VALUE_TOKEN = re.compile(r"\b\d+(?:\.\d+)?\s?(?:pt|dp|sp|px|ms|%|:1)\b", re.IGNORECASE)


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def stated_values(text: str) -> int:
    return len({m.group(0).replace(" ", "").lower() for m in VALUE_TOKEN.finditer(text)})


def main() -> None:
    for lineno, line in enumerate(sys.stdin, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"stdin:{lineno}: invalid JSON ({exc})")

        if record.get("schema") != REQUEST_SCHEMA_VERSION:
            fail(f"stdin:{lineno}: expected schema {REQUEST_SCHEMA_VERSION}")
        pair = record.get("pair")
        if not isinstance(pair, str) or not pair:
            fail(f"stdin:{lineno}: missing pair id")
        for field in ("document_1", "document_2"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                fail(f"stdin:{lineno}: missing {field}")

        one, two = stated_values(record["document_1"]), stated_values(record["document_2"])
        if one == two:
            verdict = "no-meaningful-difference"
        else:
            verdict = "document-1" if one > two else "document-2"

        print(json.dumps({
            "pair": pair,
            "verdict": verdict,
            "reason": "Oracle stand-in: counted distinct stated values. Not a design judgement.",
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
