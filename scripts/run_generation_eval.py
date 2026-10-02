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
    find_section,
    parse_dimension_read,
    primary_device_class,
    provenance_matches,
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
    for section in ("Design quality calibration", "Design quality requirements", "Design quality rationale", "Visual rhythm rules"):
        present, body = find_section(response, section)
        if not present or not body:
            continue
        # The same parser the corpus checks use: it drops the line's own
        # `Median of the assessable = N` restatement, which this check used to count as
        # a band, and it reads bold labels.
        bands = [band for band in parse_dimension_read(body) if band is not None]
        stated = re.search(r"Quality target:\**\s*\**\s*\[?([1-5])/5", body)
        if not bands or not stated:
            return []
        if len(bands) < 5:
            return [
                f"{label}: `Dimension read:` lists {len(bands)} dimension scores; "
                "the rubric has nine, so the median cannot be checked"
            ]
        # The rubric: "With an even number of assessable dimensions the median falls
        # between two bands: report the lower one." statistics.median averaged them.
        ordered = sorted(bands)
        median = ordered[(len(ordered) - 1) // 2]
        claimed = int(stated.group(1))
        if claimed > median:
            return [
                f"{label}: `Quality target: {claimed}/5` is above the median of the "
                f"dimensions it prints ({median}); the score is the median lowered by "
                "caps, never raised above it"
            ]
    return []


def check_provenance(response: str, label: str, tokens: set[str]) -> list[str]:
    """Rejected directions, and the committed one, must cite a real catalog entry."""
    body = extract_section(response, "Alternatives considered") or extract_section(
        response, "Key decision tradeoffs"
    )
    # The committed direction's `(from: ...)` is the slot SKILL.md calls the one that must
    # be verifiable; it used to be checked for shape only. Mode 6 is exempt: its direction
    # is the user's delivered design, not a catalog sample.
    for section in ("Design quality calibration", "Design quality requirements", "Visual rhythm rules"):
        committed = re.search(r"Direction:[^\n]*\(from:\s*([^)\n,;]*)", find_section(response, section)[1])
        if committed:
            body = (body or "") + f"\n(from: {committed.group(1)})"
    if not body:
        return []
    errors: list[str] = []
    sources = re.findall(r"from:\s*([^)\n,;]*)", body, re.IGNORECASE)
    for source in sources:
        if not provenance_matches(source, tokens):
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
        elif primary_device_class(found.group("value")) != wanted.lower():
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


def self_check_eval_checks() -> None:
    """The eval-only checks must catch what they exist for, on shapes live output uses.

    Each case is a response shape that used to slip through: the restated median counted
    as a band, an even count averaged instead of taking the lower band, bold labels, a
    blank or invented `from:` on the committed direction, and a phone answer to a tablet
    prompt passing because the value mentioned 'tablet'.
    """
    def calibration(read: str, target: str, direction: str = "baseline") -> str:
        return (
            "## Design quality calibration\n"
            f"- Direction: thesis (from: {direction})\n"
            f"- Dimension read: {read}\n"
            f"- Quality target: {target}\n"
        )

    nine = "attention path {0}, composition and spacing {1}, typography craft {2}, colour, state and contrast {3}, density and rhythm {4}, interaction polish and motion {5}, context and brand fit n/v, production readiness {6}, distinctiveness and owned assets {7}"
    errors: list[str] = []
    must_flag = {
        "restated median counted as a band": calibration(nine.format(3, 3, 3, 3, 4, 4, 4, 4) + ". Median of the assessable = 4.", "4/5 — blocked from 5/5 by typography craft until x"),
        "even count averaged, not the lower band": calibration(nine.format(2, 2, 2, 2, 4, 4, 4, 4) + ".", "3/5 — blocked from 4/5 by typography craft until x"),
        "bold Dimension read label": calibration(nine.format(3, 3, 3, 3, 3, 3, 3, 3) + ".", "5/5 — nothing blocks 5/5 — x").replace("- Dimension read:", "- **Dimension read:**"),
        "bold score": calibration(nine.format(3, 3, 3, 3, 3, 3, 3, 3) + ".", "**5/5** — nothing blocks 5/5 — x"),
    }
    for case, response in must_flag.items():
        if not check_derived_score(response, "probe"):
            errors.append(f"check_derived_score misses: {case}")
    if check_derived_score(calibration(nine.format(3, 3, 3, 3, 4, 4, 4, 4) + ". Median of the assessable = 3.", "3/5 — blocked from 4/5 by x until y"), "probe"):
        errors.append("check_derived_score flags a correctly derived score")

    tokens = catalog_entry_tokens()
    for source, should_pass in (("Arc", True), ("baseline", True), ("", False), ("Zorblax Hypergrid Studio", False)):
        flagged = bool(check_provenance(calibration(nine.format(3, 3, 3, 3, 3, 3, 3, 3), "3/5", direction=source), "probe", tokens))
        if flagged == should_pass:
            errors.append(f"check_provenance {'rejects' if flagged else 'accepts'} committed direction `from: {source}`")

    tablet_prompt = {"expects": {"device_class": "tablet"}}
    if not check_expectations("Device class: Phone (compact only; a tablet layout can be added on request)\n", tablet_prompt, "probe"):
        errors.append("check_expectations accepts a phone answer to a tablet prompt")
    if check_expectations("Device class: Tablet (iPad), with a phone fallback in Slide Over\n", tablet_prompt, "probe"):
        errors.append("check_expectations rejects a tablet answer that mentions a phone fallback")

    if errors:
        fail("Generation eval checks are not catching what they exist for:\n" + "\n".join(f"  - {e}" for e in errors))


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
        self_check_eval_checks()
        print_dry_run(prompts)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover
        fail(f"Unexpected generation eval error: {exc}")
