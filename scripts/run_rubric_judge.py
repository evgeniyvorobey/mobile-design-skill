#!/usr/bin/env python3
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


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_PATH = ROOT / "docs" / "design-quality-rubric.md"
EVALS_PATH = ROOT / "docs" / "evals.md"
FIXTURE_DIR = ROOT / "examples" / "evals"

DIMENSIONS = [
    "attention_path_and_hierarchy",
    "composition_and_spacing",
    "typography_craft",
    "color_state_and_contrast",
    "density_and_rhythm",
    "interaction_polish_and_motion",
    "context_and_brand_fit",
    "production_readiness",
    "distinctiveness_and_owned_assets",
]

REQUEST_SCHEMA_VERSION = "rubric-judge-request/v1"

REQUIRED_JUDGE_FIELDS = {
    "score",
    "verdict",
    "cap",
    "hard_limits",
    "dimension_scores",
    "failed_dimensions",
    "rationale",
    "improvement_suggestions",
}


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def load_fixtures() -> list[dict[str, Any]]:
    fixtures: list[dict[str, Any]] = []
    for path in sorted(FIXTURE_DIR.glob("rubric-score-*.json")):
        fixtures.append(json.loads(path.read_text(encoding="utf-8")))
    if not fixtures:
        fail(f"No rubric fixtures found in {FIXTURE_DIR.relative_to(ROOT)}")
    return fixtures


def build_system_prompt() -> str:
    return (
        "You are a strict mobile design-quality judge. "
        "Score the response with the provided 1-5 rubric. "
        "Apply caps and hard limits before assigning the final score. "
        "Do not reward stylish language when states, accessibility, platform behavior, "
        "or production readiness are weak. "
        "Return only valid JSON with the requested schema."
    )


def build_user_prompt(fixture: dict[str, Any]) -> str:
    rubric = RUBRIC_PATH.read_text(encoding="utf-8")
    evals = EVALS_PATH.read_text(encoding="utf-8")
    return (
        "# Task\n"
        "Judge the mobile design response below against the rubric.\n\n"
        "# Rubric\n"
        f"{rubric}\n\n"
        "# Eval criteria\n"
        f"{evals}\n\n"
        "# Fixture input\n"
        f"Mode: {fixture['mode']}\n"
        f"Prompt: {fixture['prompt']}\n\n"
        "# Response excerpt to judge\n"
        f"{fixture['response_excerpt']}\n\n"
        # Every number here is a placeholder, never a literal. A filled example
        # outweighs a prose instruction, and this skeleton is the slot the judge
        # fills -- shipping `1` nine times taught the judge what a vector looks like.
        "# Required JSON output\n"
        "Replace every <...> placeholder. Derive each dimension score from the "
        "rubric's boundary questions, then take their median for `score`.\n"
        "{\n"
        '  "score": <1-5>,\n'
        '  "verdict": "fail | needs major revision | acceptable baseline | strong and shippable | excellent and resilient",\n'
        '  "cap": "string describing cap or No cap",\n'
        '  "hard_limits": ["string"],\n'
        '  "dimension_scores": {\n'
        + ",\n".join(f'    "{dimension}": <1-5>' for dimension in DIMENSIONS)
        + "\n"
        "  },\n"
        '  "failed_dimensions": ["string"],\n'
        '  "rationale": "short evidence-based rationale",\n'
        '  "improvement_suggestions": ["specific suggestion", "specific suggestion"]\n'
        "}\n"
    )


def build_request_record(fixture: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": REQUEST_SCHEMA_VERSION,
        "id": fixture["id"],
        "messages": [
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": build_user_prompt(fixture)},
        ],
        "expected": {
            "score": fixture["expected_score"],
            "verdict": fixture["expected_verdict"],
            "cap": fixture["expected_cap"],
            "hard_limits": fixture["hard_limits"],
            "dimension_scores": fixture["dimension_scores"],
            "failed_dimensions": fixture["expected_failed_dimensions"],
        },
    }


def render_request_jsonl(fixtures: list[dict[str, Any]]) -> str:
    return "\n".join(
        json.dumps(build_request_record(fixture), ensure_ascii=False)
        for fixture in fixtures
    ) + "\n"


def export_jsonl(fixtures: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_request_jsonl(fixtures), encoding="utf-8")
    print(f"[OK] Wrote judge requests: {output_path}")


def export_expected_outputs(fixtures: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for fixture in fixtures:
            judge = {
                "score": fixture["expected_score"],
                "verdict": fixture["expected_verdict"],
                "cap": fixture["expected_cap"],
                "hard_limits": fixture["hard_limits"],
                "dimension_scores": fixture["dimension_scores"],
                "failed_dimensions": fixture["expected_failed_dimensions"],
                "rationale": fixture["expected_rationale"],
                "improvement_suggestions": fixture["improvement_suggestions"],
            }
            handle.write(
                json.dumps(
                    {
                        "id": fixture["id"],
                        "judge": judge,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
    print(f"[OK] Wrote expected judge outputs: {output_path}")


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def contains_semantic_item(needle: str, haystack_items: list[Any], extra_text: str = "") -> bool:
    normalized_needle = normalize(needle)
    haystack = " ".join(normalize(str(item)) for item in haystack_items)
    haystack = f"{haystack} {normalize(extra_text)}"
    return normalized_needle in haystack


def extract_json_from_text(text: str) -> dict[str, Any]:
    stripped = text.strip()
    try:
        value = json.loads(stripped)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in text")
    value = json.loads(stripped[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("Extracted JSON is not an object")
    return value


def extract_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict) and "text" in item:
                parts.append(str(item["text"]))
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)
    if isinstance(value, dict):
        if "content" in value:
            return extract_text(value["content"])
        if "message" in value:
            return extract_text(value["message"])
        if "body" in value:
            return extract_text(value["body"])
        if "choices" in value and isinstance(value["choices"], list) and value["choices"]:
            return extract_text(value["choices"][0])
        if "output_text" in value:
            return str(value["output_text"])
    return ""


def parse_judge_record(record: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    record_id = str(record.get("id") or record.get("custom_id") or "")
    if not record_id:
        raise ValueError("Judge output record is missing id/custom_id")

    if isinstance(record.get("judge"), dict):
        return record_id, record["judge"]

    if REQUIRED_JUDGE_FIELDS.issubset(record.keys()):
        return record_id, record

    for key in ("output", "response", "result"):
        if key not in record:
            continue
        value = record[key]
        if isinstance(value, dict) and REQUIRED_JUDGE_FIELDS.issubset(value.keys()):
            return record_id, value
        text = extract_text(value)
        if text:
            return record_id, extract_json_from_text(text)

    raise ValueError(f"{record_id}: could not find judge JSON")


def parse_judge_outputs_text(text: str, source_label: str) -> dict[str, dict[str, Any]]:
    outputs: dict[str, dict[str, Any]] = {}
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            record_id, judgement = parse_judge_record(record)
        except Exception as exc:
            fail(f"{source_label}:{lineno}: invalid judge output ({exc})")
        outputs[record_id] = judgement
    return outputs


def load_judge_outputs(path: Path) -> dict[str, dict[str, Any]]:
    return parse_judge_outputs_text(path.read_text(encoding="utf-8"), str(path))


def validate_judgement_shape(fixture_id: str, judgement: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_JUDGE_FIELDS - judgement.keys()
    if missing:
        errors.append(f"{fixture_id}: missing judge fields {', '.join(sorted(missing))}")
        return errors

    score = judgement["score"]
    if not isinstance(score, int) or score < 1 or score > 5:
        errors.append(f"{fixture_id}: score must be integer 1..5")

    dimensions = judgement["dimension_scores"]
    if not isinstance(dimensions, dict):
        errors.append(f"{fixture_id}: dimension_scores must be an object")
    else:
        for dimension in DIMENSIONS:
            value = dimensions.get(dimension)
            if not isinstance(value, int) or value < 1 or value > 5:
                errors.append(f"{fixture_id}: dimension `{dimension}` must be integer 1..5")

    for key in ("hard_limits", "failed_dimensions", "improvement_suggestions"):
        if not isinstance(judgement[key], list):
            errors.append(f"{fixture_id}: {key} must be a list")

    if isinstance(judgement.get("improvement_suggestions"), list) and len(judgement["improvement_suggestions"]) < 2:
        errors.append(f"{fixture_id}: improvement_suggestions must contain at least 2 items")

    if not str(judgement.get("rationale", "")).strip():
        errors.append(f"{fixture_id}: rationale must not be empty")

    return errors


def compare_judgement(fixture: dict[str, Any], judgement: dict[str, Any]) -> list[str]:
    fixture_id = fixture["id"]
    errors = validate_judgement_shape(fixture_id, judgement)
    if errors:
        return errors

    expected_score = fixture["expected_score"]
    actual_score = judgement["score"]
    if actual_score != expected_score:
        errors.append(f"{fixture_id}: expected score {expected_score}, got {actual_score}")

    # The judge's own arithmetic, checked against itself. Before this, `dimension_scores`
    # was validated for shape and then never compared to anything -- a judge returning nine
    # 3s and a score of 5 passed the entire pack. The score is the median of the assessable
    # bands lowered by caps, so it can sit below the judge's own median but never above it.
    bands = [band for band in judgement["dimension_scores"].values() if isinstance(band, int)]
    if bands and isinstance(actual_score, int):
        own_median = int(statistics.median(sorted(bands)))
        if actual_score > own_median:
            errors.append(
                f"{fixture_id}: score {actual_score} is above the median of the judge's own "
                f"dimension_scores ({own_median}); the score is that median lowered by caps, "
                "never raised above it"
            )

    expected_verdict = normalize(fixture["expected_verdict"])
    actual_verdict = normalize(str(judgement["verdict"]))
    if expected_verdict and expected_verdict not in actual_verdict:
        errors.append(
            f"{fixture_id}: expected verdict containing `{fixture['expected_verdict']}`, got `{judgement['verdict']}`"
        )

    cap = str(judgement["cap"])
    if fixture["expected_cap"].lower() != "no cap" and not cap.strip():
        errors.append(f"{fixture_id}: expected a non-empty cap")

    for hard_limit in fixture["hard_limits"]:
        if not contains_semantic_item(
            hard_limit,
            judgement["hard_limits"],
            extra_text=f"{judgement['cap']} {judgement['rationale']}",
        ):
            errors.append(f"{fixture_id}: missing hard limit `{hard_limit}`")

    for failed_dimension in fixture["expected_failed_dimensions"]:
        if not contains_semantic_item(
            failed_dimension,
            judgement["failed_dimensions"],
            extra_text=judgement["rationale"],
        ):
            errors.append(f"{fixture_id}: missing failed dimension `{failed_dimension}`")

    return errors


def validate_loaded_judge_outputs(
    fixtures: list[dict[str, Any]], outputs: dict[str, dict[str, Any]]
) -> None:
    errors: list[str] = []

    for fixture in fixtures:
        fixture_id = fixture["id"]
        judgement = outputs.get(fixture_id)
        if judgement is None:
            errors.append(f"{fixture_id}: missing judge output")
            continue
        errors.extend(compare_judgement(fixture, judgement))

    extra_ids = sorted(set(outputs) - {fixture["id"] for fixture in fixtures})
    for extra_id in extra_ids:
        errors.append(f"{extra_id}: output id does not match any fixture")

    if errors:
        fail("Rubric judge validation failed:\n" + "\n".join(errors))

    print(f"[OK] Judge outputs matched {len(fixtures)} rubric fixtures.")


def validate_judge_outputs(fixtures: list[dict[str, Any]], judge_output_path: Path) -> None:
    validate_loaded_judge_outputs(fixtures, load_judge_outputs(judge_output_path))


def run_judge_command(
    fixtures: list[dict[str, Any]],
    command: str,
    timeout_seconds: int,
    output_path: Path | None,
) -> None:
    command_parts = shlex.split(command)
    if not command_parts:
        fail("--judge-command must not be empty")
    if timeout_seconds <= 0:
        fail("--judge-command-timeout must be greater than 0")

    try:
        completed = subprocess.run(
            command_parts,
            input=render_request_jsonl(fixtures),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
        )
    except FileNotFoundError:
        fail(f"Judge command not found: {command_parts[0]}")
    except subprocess.TimeoutExpired:
        fail(f"Judge command timed out after {timeout_seconds}s: {command}")

    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        fail(
            f"Judge command exited with code {completed.returncode}: {command}"
            + (f"\nSTDERR:\n{stderr}" if stderr else "")
        )

    if not completed.stdout.strip():
        fail("Judge command produced no stdout. It must write judge-output JSONL to stdout.")

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(completed.stdout, encoding="utf-8")
        print(f"[OK] Wrote judge command output: {output_path}")

    outputs = parse_judge_outputs_text(completed.stdout, f"stdout from `{command}`")
    validate_loaded_judge_outputs(fixtures, outputs)


def print_dry_run_summary(fixtures: list[dict[str, Any]]) -> None:
    scores = sorted(fixture["expected_score"] for fixture in fixtures)
    print(f"[OK] Loaded {len(fixtures)} rubric fixtures covering scores: {scores}")
    for fixture in fixtures:
        print(
            f"- {fixture['id']}: expected {fixture['expected_score']}/5 "
            f"({fixture['expected_verdict']})"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export rubric judge prompts and validate LLM-as-judge JSONL outputs."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load fixtures and print expected score coverage without writing files.",
    )
    parser.add_argument(
        "--export-jsonl",
        type=Path,
        help="Write provider-agnostic JSONL judge requests to this path.",
    )
    parser.add_argument(
        "--export-expected-output",
        type=Path,
        help="Write oracle-style JSONL judge outputs for runner self-testing.",
    )
    parser.add_argument(
        "--judge-output",
        type=Path,
        help="Validate JSONL judge outputs against fixture expectations.",
    )
    parser.add_argument(
        "--judge-command",
        help=(
            "Run an external judge agent command. The command receives judge request "
            "JSONL on stdin and must write judge-output JSONL to stdout."
        ),
    )
    parser.add_argument(
        "--judge-command-timeout",
        type=int,
        default=300,
        help="Timeout in seconds for --judge-command (default: 300).",
    )
    parser.add_argument(
        "--judge-command-output",
        type=Path,
        help="Optional path for saving raw stdout from --judge-command before validation.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    fixtures = load_fixtures()

    if args.export_jsonl:
        export_jsonl(fixtures, args.export_jsonl)

    if args.export_expected_output:
        export_expected_outputs(fixtures, args.export_expected_output)

    if args.judge_output:
        validate_judge_outputs(fixtures, args.judge_output)

    if args.judge_command_output and not args.judge_command:
        fail("--judge-command-output requires --judge-command")

    if args.judge_command:
        run_judge_command(
            fixtures,
            args.judge_command,
            args.judge_command_timeout,
            args.judge_command_output,
        )

    if args.dry_run or (
        not args.export_jsonl
        and not args.export_expected_output
        and not args.judge_output
        and not args.judge_command
    ):
        print_dry_run_summary(fixtures)


if __name__ == "__main__":
    main()
