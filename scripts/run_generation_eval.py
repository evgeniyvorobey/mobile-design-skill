#!/usr/bin/env python3
"""
Score what the skill actually generates, not what a maintainer committed.

Every other check in this repository reads markdown a human wrote. This one asks a
model to answer real prompts and holds the answers to exactly the contract the
committed examples are held to — `check_response()` is imported from
`validate_repo.py`, not reimplemented, so the two can never drift.

Three acceptance passes during the 1.17.0 release found defects that every
structural validator passed over. This script is that acceptance loop, made
repeatable.

The generation half needs a model; the scoring half does not. That split is
deliberate: CI can prove the adapter and the scorer deterministically, while real
semantic calibration runs during maintenance with a model behind the command.

Usage:
    python3 scripts/run_generation_eval.py --dry-run
    python3 scripts/run_generation_eval.py --export-requests /tmp/requests.jsonl
    python3 scripts/run_generation_eval.py --responses /tmp/responses.jsonl
    python3 scripts/run_generation_eval.py \\
        --generate-command "python3 scripts/generation_oracle_agent.py"

Response JSONL contract — one object per line:
    {"id": "<prompt id>", "response": "<the full skill response, verbatim>"}
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_repo import (  # noqa: E402
    BANNED_RESPONSE_PATTERNS,
    MODE_REQUIREMENTS,
    catalog_entry_tokens,
    check_response,
    extract_section,
    label_body,
)

ROOT = Path(__file__).resolve().parents[1]
PROMPT_PACK = ROOT / "examples/evals/generation-prompts.json"
REQUEST_SCHEMA_VERSION = "generation-eval-request/v1"
EXAMPLE_OUTPUT_RE = re.compile(r"## Example output\s*\n\s*```md\n(?P<body>.*?)\n```", re.DOTALL)


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def load_prompts() -> list[dict[str, Any]]:
    try:
        pack = json.loads(PROMPT_PACK.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Missing prompt pack: {PROMPT_PACK}")
    except json.JSONDecodeError as exc:
        fail(f"{PROMPT_PACK}: invalid JSON ({exc})")

    prompts = pack.get("prompts")
    if not isinstance(prompts, list) or not prompts:
        fail(f"{PROMPT_PACK}: `prompts` must be a non-empty list")

    seen: set[str] = set()
    for entry in prompts:
        for field in ("id", "mode", "prompt", "expects"):
            if field not in entry:
                fail(f"{PROMPT_PACK}: prompt is missing `{field}`: {entry.get('id', entry)}")
        if entry["id"] in seen:
            fail(f"{PROMPT_PACK}: duplicate prompt id `{entry['id']}`")
        seen.add(entry["id"])
        mode = entry["mode"]
        if mode not in MODE_REQUIREMENTS and mode != "outside the standard six":
            fail(f"{PROMPT_PACK}: `{entry['id']}` names unknown mode `{mode}`")
    return prompts


def build_system_prompt() -> str:
    return (
        "You are executing the mobile-design-skill in this repository. Read SKILL.md "
        "first and follow it literally — it is the always-loaded entrypoint. Load the "
        "conditional references it tells you to load, when its triggers fire. Do not "
        "shortcut the workflow, do not improvise a format, and do not read "
        "docs/proposals/ or CHANGELOG.md: they describe intent, and this run tests "
        "whether the instructions themselves work. Return only the skill response."
    )


def build_request_record(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": REQUEST_SCHEMA_VERSION,
        "id": entry["id"],
        "expected_mode": entry["mode"],
        "system": build_system_prompt(),
        "user": entry["prompt"],
        "reference_example": entry.get("reference_example"),
    }


def render_request_jsonl(prompts: list[dict[str, Any]]) -> str:
    return "".join(
        json.dumps(build_request_record(e), ensure_ascii=False) + "\n" for e in prompts
    )


def parse_responses_text(text: str, source: str) -> dict[str, str]:
    responses: dict[str, str] = {}
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{source}: line {number} is not valid JSON ({exc})")
        if not isinstance(record, dict) or "id" not in record or "response" not in record:
            fail(f"{source}: line {number} must be an object with `id` and `response`")
        responses[str(record["id"])] = str(record["response"])
    if not responses:
        fail(f"{source}: no response records found")
    return responses


# --- eval-only checks: things a corpus file cannot be wrong about, but a live run can ---


def check_derived_score(response: str, label: str) -> list[str]:
    """The stated score must equal the median of the dimensions the response prints.

    This is the check that needs no model and catches the defect three acceptance
    passes chased: a score asserted rather than derived. If a response prints a
    dimension read at all, the arithmetic has to hold.
    """
    for section in ("Design quality calibration", "Design quality requirements", "Design quality rationale"):
        body = extract_section(response, section)
        if not body:
            continue
        read = label_body(body, "Dimension read:")
        stated = re.search(r"Quality target:\s*\[?([1-5])/5", body)
        if not read or not stated:
            return []
        scores = [int(n) for n in re.findall(r"\b([1-5])\b(?!\s*/)", read)]
        if len(scores) < 5:
            return [
                f"{label}: `Dimension read:` lists {len(scores)} dimension scores; "
                "the rubric has nine, so the median cannot be checked"
            ]
        median = int(statistics.median(sorted(scores)))
        claimed = int(stated.group(1))
        if claimed > median:
            return [
                f"{label}: `Quality target: {claimed}/5` is above the median of the "
                f"dimensions it prints ({median}); the score is the median lowered by "
                "caps, never raised above it"
            ]
    return []


def check_provenance(response: str, label: str, tokens: set[str]) -> list[str]:
    """Rejected directions must cite a real catalog entry, not an invented one."""
    body = extract_section(response, "Alternatives considered") or extract_section(
        response, "Key decision tradeoffs"
    )
    if not body:
        return []
    errors: list[str] = []
    sources = re.findall(r"from:\s*([^)\n,;]+)", body, re.IGNORECASE)
    for source in sources:
        normalized = re.sub(r"[*_`]", "", source).strip().lower()
        if not any(tok in normalized or normalized in tok for tok in tokens):
            errors.append(
                f"{label}: `from: {source.strip()}` is not an entry in the direction "
                "catalog in docs/inspiration-sources.md"
            )
    return errors


def check_expectations(response: str, entry: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    expects = entry.get("expects", {})

    wanted = expects.get("device_class")
    if wanted:
        found = re.search(r"^Device class:\s*(?P<value>\S.*)$", response, re.MULTILINE)
        if not found:
            errors.append(f"{label}: missing `Device class:` line")
        elif wanted.lower() not in found.group("value").lower():
            errors.append(
                f"{label}: prompt expects device class `{wanted}` but the response says "
                f"`{found.group('value').strip()}`"
            )

    if expects.get("no_fit_branch"):
        if not response.startswith("Mode: outside the standard six"):
            errors.append(
                f"{label}: this request fits no mode; the response must open "
                "`Mode: outside the standard six — …` rather than round to a template"
            )
    return errors


def score_response(entry: dict[str, Any], response: str, tokens: set[str]) -> list[str]:
    label = entry["id"]
    if not response.strip():
        return [f"{label}: empty response"]

    errors = check_expectations(response, entry, label)

    if entry["mode"] in MODE_REQUIREMENTS:
        errors.extend(check_response(response, entry["mode"], label))
    else:
        # The no-fit branch keeps only the header lines and Next actions.
        for marker in ("Platform scope:", "Device class:", "Assumptions:"):
            if not re.search(rf"^{re.escape(marker)}", response, re.MULTILINE):
                errors.append(f"{label}: missing `{marker}` line")
        if not re.search(r"^## Next actions\s*$", response, re.MULTILINE):
            errors.append(f"{label}: missing `## Next actions` section")
        for pattern in BANNED_RESPONSE_PATTERNS:
            if re.search(pattern, response, re.IGNORECASE):
                errors.append(f"{label}: banned response phrase /{pattern}/")

    errors.extend(check_derived_score(response, label))
    errors.extend(check_provenance(response, label, tokens))
    return errors


def score_all(prompts: list[dict[str, Any]], responses: dict[str, str]) -> None:
    tokens = catalog_entry_tokens()
    missing = [e["id"] for e in prompts if e["id"] not in responses]
    if missing:
        fail("No response for prompt(s): " + ", ".join(missing))

    failures: dict[str, list[str]] = {}
    for entry in prompts:
        errors = score_response(entry, responses[entry["id"]], tokens)
        status = "PASS" if not errors else f"FAIL ({len(errors)})"
        print(f"- {entry['id']}: {status}")
        if errors:
            failures[entry["id"]] = errors

    if failures:
        detail = "\n".join(
            f"\n{prompt_id}:\n  " + "\n  ".join(errors) for prompt_id, errors in failures.items()
        )
        fail(f"{len(failures)} of {len(prompts)} generated responses failed the contract:{detail}")

    print(f"[OK] {len(prompts)} generated responses satisfy the response contract.")


def run_generate_command(
    prompts: list[dict[str, Any]], command: str, timeout_seconds: int, output_path: Path | None
) -> None:
    parts = shlex.split(command)
    if not parts:
        fail("--generate-command must not be empty")
    if timeout_seconds <= 0:
        fail("--generate-command-timeout must be greater than 0")

    try:
        completed = subprocess.run(
            parts,
            input=render_request_jsonl(prompts),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
        )
    except FileNotFoundError:
        fail(f"Generate command not found: {parts[0]}")
    except subprocess.TimeoutExpired:
        fail(f"Generate command timed out after {timeout_seconds}s: {command}")

    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        fail(
            f"Generate command exited with code {completed.returncode}: {command}"
            + (f"\nSTDERR:\n{stderr}" if stderr else "")
        )
    if not completed.stdout.strip():
        fail("Generate command produced no stdout. It must write response JSONL to stdout.")

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(completed.stdout, encoding="utf-8")
        print(f"[OK] Wrote generate command output: {output_path}")

    score_all(prompts, parse_responses_text(completed.stdout, f"stdout from `{command}`"))


def print_dry_run(prompts: list[dict[str, Any]]) -> None:
    replayable = sum(1 for e in prompts if e.get("reference_example"))
    print(f"[OK] Loaded {len(prompts)} generation prompts ({replayable} oracle-replayable)")
    for entry in prompts:
        marker = "replayable" if entry.get("reference_example") else "model-only"
        print(f"- {entry['id']} [{entry['mode']}] ({marker})")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Score generated skill responses against the response contract."
    )
    parser.add_argument("--dry-run", action="store_true", help="List the prompt pack and exit.")
    parser.add_argument("--export-requests", type=Path, help="Write generation-request JSONL.")
    parser.add_argument("--responses", type=Path, help="Score a response JSONL file.")
    parser.add_argument("--generate-command", help="Command that reads request JSONL on stdin and writes response JSONL on stdout.")
    parser.add_argument("--generate-command-output", type=Path, help="Save the command's stdout.")
    parser.add_argument("--generate-command-timeout", type=int, default=900)
    parser.add_argument(
        "--replayable-only",
        action="store_true",
        help="Restrict to prompts with a `reference_example`, so the deterministic "
        "oracle can cover the whole set. CI uses this; a real model run should not.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prompts = load_prompts()
    if args.replayable_only:
        prompts = [e for e in prompts if e.get("reference_example")]
        if not prompts:
            fail("--replayable-only left no prompts; every entry lacks a reference_example")

    if args.export_requests:
        args.export_requests.parent.mkdir(parents=True, exist_ok=True)
        args.export_requests.write_text(render_request_jsonl(prompts), encoding="utf-8")
        print(f"[OK] Wrote {len(prompts)} generation requests: {args.export_requests}")

    if args.generate_command:
        run_generate_command(
            prompts,
            args.generate_command,
            args.generate_command_timeout,
            args.generate_command_output,
        )
        return

    if args.responses:
        score_all(prompts, parse_responses_text(args.responses.read_text(encoding="utf-8"), str(args.responses)))
        return

    if args.dry_run or not args.export_requests:
        print_dry_run(prompts)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover
        fail(f"Unexpected generation eval error: {exc}")
