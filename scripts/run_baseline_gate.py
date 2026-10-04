#!/usr/bin/env python3
"""Does the skill beat the same model with no skill?

Twenty releases of this repository measured the skill against itself. The first
comparison with the same model and no skill, on 2026-10-01, went to the baseline on
8 briefs of 8 with the null control holding. This script is that comparison made
repeatable, and the release rule that reads it.

It owns four things and nothing else:

  - the brief pack, and the two generation requests each brief yields: one telling
    the model to load the skill, one telling it to answer as it normally would;
  - the judge requests, which are `run_paired_eval.py`'s plus the brief both
    documents answer and an exploratory second question about usefulness;
  - the blind error-audit requests, both arms mixed under opaque ids;
  - the release rule.

Pair building, order counterbalancing, the null control and its refusal are imported
from `run_paired_eval.py`, not reimplemented: a gate with its own copy of the control
is a gate whose control can drift from the instrument's.

The rule, all three parts required:

  1. the null control is readable — otherwise the run is UNREADABLE, not failed;
  2. skill share = (pairs won + half the pairs tied) / pairs >= MIN_SKILL_SHARE;
  3. the skill arm carries no more medium-or-high errors than the baseline arm.

Generation, rewriting, judging and auditing need a model. Everything here is
deterministic, so CI proves the rule and maintainers run the models. The procedure
is in `docs/paired-comparison.md`.

Usage:
    python3 scripts/run_baseline_gate.py --self-test
    python3 scripts/run_baseline_gate.py --dry-run [--set core|extended|held-out]
    python3 scripts/run_baseline_gate.py --set core --export-requests gate-requests.jsonl
    python3 scripts/run_baseline_gate.py --arm-skill S.jsonl --arm-baseline B.jsonl \\
        --export-audit-requests audit.jsonl
    python3 scripts/run_baseline_gate.py --arm-skill S.jsonl --arm-baseline B.jsonl --nulls N.jsonl \\
        --export-judge-requests judge.jsonl
    python3 scripts/run_baseline_gate.py --arm-skill S.jsonl --arm-baseline B.jsonl --nulls N.jsonl \\
        --verdicts verdicts.jsonl --errors errors.jsonl

Arm and null JSONL: {"id": "<brief id>", "response": "<full text>"} — nulls are cosmetic
                    rewrites of skill-arm responses.
Verdict JSONL:      {"pair": "<request id>", "verdict": "document-1" | "document-2" |
                    "no-meaningful-difference", "usefulness": <same values, optional>}
Error JSONL:        {"doc": "<audit id>", "errors": [{"severity": "high" | "medium" | "low", ...}]}

Exit codes: 0 the gate passed, 1 it failed or the input was unusable, 2 the control
failed and the run is unreadable.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_paired_eval as paired  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BRIEF_PACK = ROOT / "examples/evals/baseline-gate-briefs.json"
GENERATION_REQUEST_SCHEMA = "gate-generation-request/v1"
# Neutral on purpose: a judge or auditor that reads `baseline` in a schema name has been
# told what the comparison is, and half of what the documents are.
JUDGE_REQUEST_SCHEMA = "design-judge-request/v1"
AUDIT_REQUEST_SCHEMA = "design-audit-request/v1"

# A draw is not a loss: the skill has to be at least as good as answering without it.
# Below this it is costing the user quality as well as time.
MIN_SKILL_SHARE = 0.5
# Low-severity errors are noise at this sample size; medium and high are rework or a shipped defect.
COUNTED_SEVERITIES = ("high", "medium")
SEVERITIES = ("high", "medium", "low")
SETS = ("core", "extended", "held-out")

# The two arms get the same framing and differ in one thing: whether the skill is loaded.
# Verbatim from the 2026-10-01 run, minus the harness's own file paths.
SKILL_ARM_SYSTEM = (
    "You are answering a user's request exactly as you would in a chat with them. Before "
    "answering, load the mobile-design-skill:\n\n"
    "1. Read SKILL.md at the root of the skill repository in full.\n"
    "2. Follow it exactly as written for this request, including every file it tells you to "
    "load for this kind of task. Relative paths in it resolve against the repository root.\n"
    "3. Read only SKILL.md and the files it (or files it points to) direct you to. Do not read "
    "docs/proposals/, CHANGELOG.md, README.md, or anything under scripts/ — those are "
    "maintenance records, not the skill.\n\n"
    "Constraints:\n"
    "- Do not use web search or web fetch.\n"
    "- Do not run any shell commands or start any servers.\n"
    "- Do not edit any file in the repository."
)
BASELINE_ARM_SYSTEM = (
    "You are answering a user's request exactly as you would in a chat with them. Answer it "
    "the way you normally would, from your own knowledge.\n\n"
    "Constraints:\n"
    "- Do not read, search, list or open any file on disk. Do not use web search or web fetch.\n"
    "- Do not run any shell commands or start any servers."
)
# Exploratory and reported, never gated: length legitimately matters to this question, so
# the null pairs do not control it.
USEFULNESS_QUESTION = (
    "Answer the question above first. Then, separately, a second question: imagine you are "
    "the person who sent the request. Which response would you rather have received — the one "
    "that would help you more, taking into account the time it takes to read and act on it? "
    "Same three possible answers."
)
AUDIT_SYSTEM = (
    "Role: blind technical reviewer of mobile design documents. Audit each document for "
    "ERRORS. Each document answers the request given with it. You are not told who wrote it "
    "or how; do not try to guess, and judge each on its own.\n\n"
    "An ERROR is one of:\n"
    "- platform-fact: a wrong statement about iOS/iPadOS, Android, Material 3, Apple HIG, an "
    "API, a component, a default value or a platform behaviour (today is {today}; current "
    "releases are {platform_releases}).\n"
    "- accessibility: a recommendation that would violate WCAG 2.2 AA or platform "
    "accessibility minimums, or a wrong accessibility claim.\n"
    "- contradiction: two parts of the same document that disagree (values, rules, "
    "behaviour), or numbers that do not add up.\n"
    "- fabrication: an invented fact presented as fact — research findings, statistics, test "
    "results, user data, legal or policy requirements stated as certain without basis.\n"
    "- harmful-ux: a recommendation that would mislead users, lose their data or money, or is "
    "a dark pattern.\n"
    "- brief-violation: ignores or contradicts something the brief explicitly stated.\n\n"
    "Not errors: matters of taste, alternative reasonable design choices, omissions, "
    "verbosity, labelled assumptions.\n\n"
    "Report only errors you are at least 80% confident are real. Severity: high = would ship "
    "a real defect or mislead a developer or designer on something that matters; medium = "
    "would likely cause rework; low = minor inaccuracy."
)
# Version-bound, like every platform fact in this repository: update it with the dated
# platform baseline in docs/adaptive-layout.md.
PLATFORM_RELEASES = "iOS 26/27 and Android 16"


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON ({exc})")


def load_briefs(set_name: str) -> list[dict[str, str]]:
    """The briefs of one set. The held-out file is opened only when it is asked for."""
    if set_name not in SETS:
        fail(f"unknown set `{set_name}`; choose one of {', '.join(SETS)}")
    pack = read_json(BRIEF_PACK)
    if set_name == "held-out":
        sealed = ROOT / pack["held_out_file"]
        try:
            digest = hashlib.sha256(sealed.read_bytes()).hexdigest()
        except FileNotFoundError:
            fail(f"missing file: {sealed}")
        if digest != pack.get("held_out_sha256"):
            # A held-out brief that can be edited quietly is a test that can be tuned.
            fail(
                f"{pack['held_out_file']} does not match the sha-256 recorded in {BRIEF_PACK.name}. "
                "Replacing the sealed set is a deliberate act: record the new hash with it."
            )
        entries = read_json(sealed)["briefs"]
    else:
        entries = list(pack["core"])
        if set_name == "extended":
            entries += read_json(ROOT / pack["extended_from"])["prompts"]

    briefs: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in entries:
        for field in ("id", "mode", "prompt"):
            if not str(entry.get(field, "")).strip():
                fail(f"{set_name} set: a brief is missing `{field}`: {entry.get('id', entry)}")
        if entry["id"] in seen:
            fail(f"{set_name} set: duplicate brief id `{entry['id']}`")
        seen.add(entry["id"])
        briefs.append({"id": entry["id"], "mode": entry["mode"], "prompt": entry["prompt"]})
    return briefs


def all_prompts() -> dict[str, str]:
    """Brief text by id, for the sets that are open. Held-out briefs join only when present
    in the arms, so scoring a core run never opens the sealed file. A held-out set that was
    opened and then replaced is an open working set: its file is named in the pack."""
    prompts = {brief["id"]: brief["prompt"] for brief in load_briefs("extended")}
    for name in read_json(BRIEF_PACK).get("opened_held_out_files", []):
        prompts.update({brief["id"]: brief["prompt"] for brief in read_json(ROOT / name)["briefs"]})
    return prompts


def prompts_for(ids: set[str]) -> dict[str, str]:
    prompts = all_prompts()
    if not ids <= set(prompts):
        prompts.update({brief["id"]: brief["prompt"] for brief in load_briefs("held-out")})
    missing = sorted(ids - set(prompts))
    if missing:
        fail(f"response id(s) that are in no brief set: {', '.join(missing)}")
    return prompts


def render_generation_requests(briefs: list[dict[str, str]]) -> str:
    lines = []
    for brief in briefs:
        for arm, system in (("skill", SKILL_ARM_SYSTEM), ("baseline", BASELINE_ARM_SYSTEM)):
            lines.append(json.dumps({
                "schema": GENERATION_REQUEST_SCHEMA,
                "id": brief["id"],
                "arm": arm,
                "system": system,
                "user": brief["prompt"],
            }, ensure_ascii=False) + "\n")
    return "".join(lines)


def render_judge_requests(presented: list[dict[str, Any]], prompts: dict[str, str]) -> str:
    lines = []
    for record in presented:
        lines.append(json.dumps({
            "schema": JUDGE_REQUEST_SCHEMA,
            "pair": record["request_id"],
            "system": paired.build_system_prompt(),
            "request": prompts[record["id"]],
            "document_1": record["document_1"],
            "document_2": record["document_2"],
            "second_question": USEFULNESS_QUESTION,
        }, ensure_ascii=False) + "\n")
    return "".join(lines)


def audit_id(brief_id: str, arm: str) -> str:
    """Opaque on purpose: an auditor who can read the arm off the id is not blind."""
    return "e-" + hashlib.sha256(f"baseline-gate-audit:{arm}:{brief_id}".encode()).hexdigest()[:10]


def render_audit_requests(
    arm_skill: dict[str, str], arm_baseline: dict[str, str], prompts: dict[str, str],
    today: str, platform_releases: str,
) -> str:
    system = AUDIT_SYSTEM.format(today=today, platform_releases=platform_releases)
    records = []
    for brief_id in sorted(set(arm_skill) & set(arm_baseline)):
        for arm, responses in (("skill", arm_skill), ("baseline", arm_baseline)):
            records.append({
                "schema": AUDIT_REQUEST_SCHEMA,
                "doc": audit_id(brief_id, arm),
                "system": system,
                "request": prompts[brief_id],
                "document": responses[brief_id],
            })
    # Sorted by the opaque id, so the two arms of a brief are not adjacent.
    records.sort(key=lambda record: record["doc"])
    return "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records)


def parse_gate_verdicts(text: str, source: str) -> tuple[dict[str, str], dict[str, str]]:
    verdicts: dict[str, str] = {}
    usefulness: dict[str, str] = {}
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{source}: line {number} is not valid JSON ({exc})")
        if not isinstance(record, dict) or "pair" not in record or "verdict" not in record:
            fail(f"{source}: line {number} must be an object with `pair` and `verdict`")
        for field, target in (("verdict", verdicts), ("usefulness", usefulness)):
            value = record.get(field)
            if value is None and field == "usefulness":
                continue
            if value not in paired.VERDICTS:
                fail(f"{source}: line {number} has {field} `{value}`; use one of {', '.join(paired.VERDICTS)}")
            target[str(record["pair"])] = value
    if not verdicts:
        fail(f"{source}: no verdict records found")
    return verdicts, usefulness


def parse_errors(text: str, source: str) -> dict[str, list[str]]:
    """Audit id -> the severities of the errors found in that document."""
    out: dict[str, list[str]] = {}
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{source}: line {number} is not valid JSON ({exc})")
        if not isinstance(record, dict) or "doc" not in record or not isinstance(record.get("errors"), list):
            fail(f"{source}: line {number} must be an object with `doc` and an `errors` list")
        severities = []
        for error in record["errors"]:
            severity = error.get("severity") if isinstance(error, dict) else None
            if severity not in SEVERITIES:
                fail(f"{source}: line {number} has an error with severity `{severity}`; use one of {', '.join(SEVERITIES)}")
            severities.append(severity)
        out[str(record["doc"])] = severities
    return out


def count_errors(ids: list[str], errors: dict[str, list[str]]) -> dict[str, int]:
    """Medium-or-high errors per arm. Every document of every compared brief must be audited:
    an arm with unaudited documents would win this half of the rule by not being read."""
    missing = [f"{brief_id}/{arm}" for brief_id in ids for arm in ("skill", "baseline")
               if audit_id(brief_id, arm) not in errors]
    if missing:
        fail(
            f"{len(missing)} document(s) have no error audit, so the error half of the rule cannot "
            f"be read: {', '.join(missing[:6])}" + (" …" if len(missing) > 6 else "")
        )
    return {
        arm: sum(1 for brief_id in ids for severity in errors[audit_id(brief_id, arm)]
                 if severity in COUNTED_SEVERITIES)
        for arm in ("skill", "baseline")
    }


def usefulness_tally(presented: list[dict[str, Any]], usefulness: dict[str, str]) -> dict[str, int] | None:
    tally = {"skill": 0, "baseline": 0, "none": 0}
    answered = 0
    for record in presented:
        if record["kind"] != "signal":
            continue
        answer = usefulness.get(record["request_id"], usefulness.get(record["pair"]))
        if answer is None:
            continue
        answered += 1
        if answer == "no-meaningful-difference":
            tally["none"] += 1
        else:
            role = record["doc1_role"] if answer == "document-1" else record["doc2_role"]
            tally["skill" if role == "arm-a" else "baseline"] += 1
    return tally if answered else None


def evaluate(
    arm_skill: dict[str, str], arm_baseline: dict[str, str], nulls: dict[str, str],
    verdicts: dict[str, str], usefulness: dict[str, str], errors: dict[str, list[str]],
) -> int:
    """Print the gate report and return the exit code."""
    presented = paired.build_pairs(arm_skill, arm_baseline, nulls)
    result = paired.measure(presented, verdicts)
    try:
        # Prints the control first and refuses, before any contrast, when it failed.
        paired.report(result)
    except SystemExit:
        print("[UNREADABLE] The gate has no verdict: its control failed. This is not a pass and not a fail.")
        return 2

    ids = sorted({record["id"] for record in presented if record["kind"] == "signal"})
    counts = count_errors(ids, errors)
    pairs = result["signal_pairs"]
    share = (result["pair_a_wins"] + 0.5 * result["pair_ties"]) / pairs

    print("== Release gate: skill versus no skill ==")
    print(f"  pairs skill / baseline / tied : {result['pair_a_wins']} / {result['pair_b_wins']} / {result['pair_ties']} of {pairs}")
    print(f"  skill share (ties count half) : {share:.2f} (minimum {MIN_SKILL_SHARE:.2f})")
    print(f"  medium+high errors            : skill {counts['skill']}, baseline {counts['baseline']} (skill must not exceed baseline)")
    tally = usefulness_tally(presented, usefulness)
    if tally:
        print(f"  usefulness, reported only     : skill {tally['skill']} / baseline {tally['baseline']} / no difference {tally['none']} judgements")

    reasons = []
    if share < MIN_SKILL_SHARE:
        reasons.append(f"skill share {share:.2f} is below {MIN_SKILL_SHARE:.2f}")
    if counts["skill"] > counts["baseline"]:
        reasons.append(f"the skill arm has more medium+high errors ({counts['skill']} against {counts['baseline']})")
    if reasons:
        print("[FAIL] The skill does not clear the gate: " + "; ".join(reasons) + ".")
        return 1
    print("[PASS] The skill is at least as good as no skill on these briefs, with no more errors.")
    return 0


def self_test() -> None:
    """Prove the rule passes what it should, fails what it should, and refuses the rest."""
    ids = [f"p{n}" for n in range(1, 7)]
    arm_skill = {i: f"skill answer for {i}: a list with a sticky action" for i in ids}
    arm_baseline = {i: f"baseline answer for {i}: a grid with a floating action" for i in ids}
    nulls = {i: f"the answer for {i}, reworded: a list whose action stays pinned" for i in ids[:3]}
    presented = paired.build_pairs(arm_skill, arm_baseline, nulls)

    def verdicts_for(signal: dict[str, str], null_winner: str | None = None) -> dict[str, str]:
        out = {}
        for record in presented:
            wanted = signal[record["id"]] if record["kind"] == "signal" else null_winner
            if wanted in (None, "none"):
                out[record["request_id"]] = "no-meaningful-difference"
            else:
                out[record["request_id"]] = "document-1" if record["doc1_role"] == wanted else "document-2"
        return out

    def audit(skill: list[str], baseline: list[str], drop: str | None = None) -> dict[str, list[str]]:
        errors = {audit_id(i, arm): [] for i in ids for arm in ("skill", "baseline")}
        errors[audit_id("p1", "skill")] = list(skill)
        errors[audit_id("p1", "baseline")] = list(baseline)
        if drop:
            del errors[drop]
        return errors

    def run(verdicts: dict[str, str], errors: dict[str, list[str]]) -> tuple[int, str]:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(io.StringIO()):
            try:
                code = evaluate(arm_skill, arm_baseline, nulls, verdicts, {}, errors)
            except SystemExit as exc:
                code = int(exc.code or 0)
        return code, buffer.getvalue()

    everyone = lambda winner: {i: winner for i in ids}  # noqa: E731
    split = {**{i: "arm-a" for i in ids[:3]}, **{i: "arm-b" for i in ids[3:]}}
    short = {**{i: "arm-a" for i in ids[:2]}, **{i: "arm-b" for i in ids[2:]}}
    cases = [
        ("the skill wins every pair", verdicts_for(everyone("arm-a")), audit([], []), 0, "[PASS]"),
        ("the baseline wins every pair", verdicts_for(everyone("arm-b")), audit([], []), 1, "[FAIL]"),
        ("an even split is a draw, and a draw passes", verdicts_for(split), audit([], []), 0, "[PASS]"),
        ("every pair tied is a draw", verdicts_for(everyone("none")), audit([], []), 0, "[PASS]"),
        ("two pairs of six is below half", verdicts_for(short), audit([], []), 1, "[FAIL]"),
        ("a failed control is unreadable even when the skill wins everything",
         verdicts_for(everyone("arm-a"), null_winner="arm-a"), audit([], []), 2, "[UNREADABLE]"),
        ("more medium errors than the baseline fails a won comparison",
         verdicts_for(everyone("arm-a")), audit(["medium", "high"], ["medium"]), 1, "[FAIL]"),
        ("low-severity errors are not counted",
         verdicts_for(everyone("arm-a")), audit(["low"] * 5, []), 0, "[PASS]"),
        ("an unaudited document refuses the verdict",
         verdicts_for(everyone("arm-a")), audit([], [], drop=audit_id("p4", "baseline")), 1, None),
    ]
    problems = []
    for name, verdicts, errors, want_code, want_line in cases:
        code, output = run(verdicts, errors)
        if code != want_code:
            problems.append(f"{name}: exit {code}, expected {want_code}")
        if want_line and want_line not in output:
            problems.append(f"{name}: `{want_line}` missing from the report")
        if want_code != 0 and "[PASS]" in output:
            problems.append(f"{name}: printed [PASS]")

    core = load_briefs("core")
    requests = [json.loads(line) for line in render_generation_requests(core).splitlines()]
    if len(requests) != 2 * len(core):
        problems.append("each brief must yield exactly one skill request and one baseline request")
    for request in requests:
        leaked = request["arm"] == "baseline" and ("skill" in request["system"].lower() or "/" in request["system"])
        if leaked:
            problems.append(f"the baseline request for {request['id']} names the skill or a path")
        if request["arm"] == "skill" and "SKILL.md" not in request["system"]:
            problems.append(f"the skill request for {request['id']} does not load SKILL.md")

    prompts = {i: f"request {i}" for i in ids}
    for line in render_judge_requests(presented, prompts).splitlines():
        record = json.loads(line)
        visible = json.dumps({k: v for k, v in record.items() if k not in ("document_1", "document_2")})
        if any(word in visible for word in ("arm-a", "arm-b", "signal", "null", "cosmetic", "baseline")):
            problems.append("a judge request names an arm or the kind of pair")
        if not record["request"]:
            problems.append("a judge request carries no brief")
    audit_records = [json.loads(line) for line in
                     render_audit_requests(arm_skill, arm_baseline, prompts, "2026-01-01", PLATFORM_RELEASES).splitlines()]
    if len(audit_records) != 2 * len(ids):
        problems.append("the audit must cover both arms of every brief")
    for record in audit_records:
        visible = json.dumps({k: v for k, v in record.items() if k not in ("document", "system", "request")})
        if set(record) & {"arm", "id"} or any(word in visible for word in ("skill", "baseline", "arm", "p1")):
            problems.append("an audit request reveals its arm or its brief id")

    global BRIEF_PACK
    original = BRIEF_PACK
    try:
        # The sealed set stays sealed: an open set must load with the held-out file absent.
        pack = read_json(original)
        pack["held_out_file"] = "examples/evals/does-not-exist.json"
        BRIEF_PACK = ROOT / "examples/evals/.baseline-gate-self-test.json"
        BRIEF_PACK.write_text(json.dumps(pack), encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()):
            try:
                load_briefs("core")
                load_briefs("extended")
            except SystemExit:
                problems.append("loading an open set opened the held-out file")
        # And it stays what it was: an edited sealed file is refused, not loaded.
        sealed = ROOT / read_json(original)["held_out_file"]
        tampered = ROOT / "examples/evals/.baseline-gate-self-test-heldout.json"
        # Any changed byte is an edit; the ids of the sealed set are not this test's business.
        tampered.write_text(sealed.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        pack["held_out_file"] = "examples/evals/.baseline-gate-self-test-heldout.json"
        BRIEF_PACK.write_text(json.dumps(pack), encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()):
            try:
                load_briefs("held-out")
                problems.append("an edited held-out file was loaded")
            except SystemExit:
                pass
        BRIEF_PACK = original
        with contextlib.redirect_stderr(io.StringIO()):
            try:
                load_briefs("held-out")
            except SystemExit:
                problems.append("the committed held-out file does not match its recorded sha-256")
    finally:
        (ROOT / "examples/evals/.baseline-gate-self-test.json").unlink(missing_ok=True)
        (ROOT / "examples/evals/.baseline-gate-self-test-heldout.json").unlink(missing_ok=True)
        BRIEF_PACK = original

    if problems:
        fail("Baseline gate self-test failed:\n" + "\n".join(f"  - {p}" for p in problems))
    print(f"[OK] Baseline gate passes, fails and refuses as specified ({len(cases)} rule cases, {len(core)} core briefs).")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--set", dest="brief_set", default="core", choices=SETS, help="brief set for --dry-run and --export-requests")
    parser.add_argument("--dry-run", action="store_true", help="list the brief set and stop")
    parser.add_argument("--export-requests", type=Path, help="write generation requests for both arms and stop")
    parser.add_argument("--arm-skill", type=Path, help="JSONL responses generated with the skill loaded")
    parser.add_argument("--arm-baseline", type=Path, help="JSONL responses generated with no skill")
    parser.add_argument("--nulls", type=Path, help="JSONL cosmetic rewrites of skill-arm responses")
    parser.add_argument("--export-judge-requests", type=Path, help="write judge requests")
    parser.add_argument("--export-audit-requests", type=Path, help="write blind error-audit requests")
    parser.add_argument("--today", default=date.today().isoformat(), help="date stated to the auditor (default: today)")
    parser.add_argument("--platform-releases", default=PLATFORM_RELEASES, help="current platform releases stated to the auditor")
    parser.add_argument("--verdicts", type=Path, help="JSONL judge verdicts to score")
    parser.add_argument("--errors", type=Path, help="JSONL error audit of both arms; required with --verdicts")
    parser.add_argument("--self-test", action="store_true", help="prove the rule; needs no model")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.self_test or len(sys.argv) == 1:
        self_test()
        return

    if args.dry_run or args.export_requests:
        briefs = load_briefs(args.brief_set)
        if args.export_requests:
            args.export_requests.write_text(render_generation_requests(briefs), encoding="utf-8")
            print(f"[OK] wrote {2 * len(briefs)} generation requests ({len(briefs)} briefs, two arms) to {args.export_requests}")
        else:
            print(f"[OK] {args.brief_set} set: {len(briefs)} briefs")
            for brief in briefs:
                print(f"- {brief['id']} [{brief['mode']}]")
        return

    if not (args.arm_skill and args.arm_baseline):
        fail("supply --arm-skill and --arm-baseline; use --self-test for the self-test")
    arm_skill = paired.load_responses(args.arm_skill, "skill arm")
    arm_baseline = paired.load_responses(args.arm_baseline, "baseline arm")

    exported = False
    if args.export_audit_requests:
        # The audit reads the two arms and nothing else, so it can start before the nulls exist.
        prompts = prompts_for(set(arm_skill) & set(arm_baseline))
        text = render_audit_requests(arm_skill, arm_baseline, prompts, args.today, args.platform_releases)
        args.export_audit_requests.write_text(text, encoding="utf-8")
        print(f"[OK] wrote {len(text.splitlines())} audit requests to {args.export_audit_requests}")
        exported = True

    if not args.nulls:
        if exported:
            return
        fail("supply --nulls: cosmetic rewrites of skill-arm responses are the control, and no comparison is read without it")
    nulls = paired.load_responses(args.nulls, "null rewrites")

    if args.export_judge_requests:
        prompts = prompts_for(set(arm_skill) & set(arm_baseline))
        presented = paired.build_pairs(arm_skill, arm_baseline, nulls)
        args.export_judge_requests.write_text(render_judge_requests(presented, prompts), encoding="utf-8")
        print(f"[OK] wrote {len(presented)} judge requests to {args.export_judge_requests}")
        exported = True
    if exported:
        return

    if not args.verdicts:
        fail("supply --verdicts and --errors to score a run, or one of the --export options")
    if not args.errors:
        fail(
            "the error audit is half of the rule; supply --errors. For the comparison alone, "
            "use scripts/run_paired_eval.py, whose result is not a gate result."
        )
    verdicts, usefulness = parse_gate_verdicts(args.verdicts.read_text(encoding="utf-8"), str(args.verdicts))
    errors = parse_errors(args.errors.read_text(encoding="utf-8"), str(args.errors))
    raise SystemExit(evaluate(arm_skill, arm_baseline, nulls, verdicts, usefulness, errors))


if __name__ == "__main__":
    main()
