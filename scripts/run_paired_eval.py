#!/usr/bin/env python3
"""Compare two arms of skill output by forced-choice paired comparison.

Every other instrument in this repository scores one artifact against a written
standard, and each asks whether something is *stated*. Measured against a corpus
of six designs and six deliberately worse twins, the rubric's nine boundary
questions returned the identical band 12 paired scorings out of 12 — against an
instrument with a measured 17% jitter on unchanged text. On the same twelve pairs
a rubric-free forced choice returned 12 of 12 and named the injected mechanism
every time. See `docs/paired-comparison.md` and proposal sections 34-35.

So this harness exists to answer the one question nineteen sections of that
proposal could not: **did the output get better?**

Two structural refusals, both learned the hard way and both enforced here rather
than left to whoever runs it:

  - **A contrast without null pairs is not reported.** A judge offered two
    documents will find a winner. The only way to see that is to hand it two
    documents that describe the same design in different words and watch what it
    does. Nulls are required, not encouraged.
  - **A contrast whose own control failed is reported as unreadable**, and exits
    non-zero. A win rate measured by an instrument that also "wins" on identical
    designs is not a result, and no run should have to notice that by hand.

The judging half needs a model; the reporting half does not. That split is
deliberate and matches `run_rubric_judge.py`: CI proves the adapter and the
report deterministically, and real comparisons run during maintenance with a
model behind `--judge-command`.

Usage:
    python3 scripts/run_paired_eval.py --self-test
    python3 scripts/run_paired_eval.py --dry-run --arm-a A.jsonl --arm-b B.jsonl --nulls N.jsonl
    python3 scripts/run_paired_eval.py --arm-a A.jsonl --arm-b B.jsonl --nulls N.jsonl \\
        --export-requests /tmp/pairs.jsonl
    python3 scripts/run_paired_eval.py --arm-a A.jsonl --arm-b B.jsonl --nulls N.jsonl \\
        --verdicts /tmp/verdicts.jsonl

Arm JSONL, one object per line:   {"id": "<prompt id>", "response": "<full text>"}
Nulls JSONL, same shape: a cosmetic rewrite of the arm-A response for that id —
same design, same decisions, same values, different prose.
Verdict JSONL: {"pair": "<pair id>", "verdict": "document-1"|"document-2"|"no-meaningful-difference"}
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import shlex
import subprocess
import sys
from math import comb
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "examples/evals/paired-comparison-fixtures.json"
REQUEST_SCHEMA_VERSION = "paired-eval-request/v1"

VERDICTS = ("document-1", "document-2", "no-meaningful-difference")

# From the validation record: nulls drew an agreed winner in 0 of 3 pairs. One in
# three is the most that can happen before the instrument's own control is failing.
NULL_AGREED_WINNER_MAX = 1 / 3
MIN_NULL_PAIRS = 3
# One null for every three signal pairs. A single null among twenty signal pairs
# cannot see a judge that always finds a winner.
MIN_NULL_RATIO = 1 / 3


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def load_responses(path: Path, label: str) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"Missing {label}: {path}")
    out: dict[str, str] = {}
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{path}: line {number} is not valid JSON ({exc})")
        if not isinstance(record, dict) or "id" not in record or "response" not in record:
            fail(f"{path}: line {number} must be an object with `id` and `response`")
        out[str(record["id"])] = str(record["response"])
    if not out:
        fail(f"{path}: no records found")
    return out


def request_id(internal: str) -> str:
    """The id a judge sees. Opaque on purpose: the internal id (`null-p3-ab`) names the
    control pairs and the presentation order, so a judge that read it could pass the
    control and pick an arm without reading either document."""
    return "r-" + hashlib.sha256(("paired-eval-request:" + internal).encode()).hexdigest()[:12]


def build_pairs(
    arm_a: dict[str, str], arm_b: dict[str, str], nulls: dict[str, str]
) -> list[dict[str, Any]]:
    """One pair per shared id, plus one null pair per id with a cosmetic rewrite.

    Every pair is presented in both orders, by different judges, so order bias and
    inter-judge agreement fall out of the same design rather than needing a second.
    """
    shared = sorted(set(arm_a) & set(arm_b))
    if not shared:
        fail("arm A and arm B share no ids; there is nothing to compare")

    unmatched = sorted((set(arm_a) | set(arm_b)) - set(shared))
    if unmatched:
        print(f"[note] {len(unmatched)} id(s) in one arm only, skipped: {', '.join(unmatched)}")

    null_ids = sorted(set(nulls) & set(arm_a))
    missing = sorted(set(nulls) - set(arm_a))
    if missing:
        fail(f"null rewrite(s) with no arm-A response to pair against: {', '.join(missing)}")

    if len(null_ids) < MIN_NULL_PAIRS:
        fail(
            f"{len(null_ids)} null pair(s); at least {MIN_NULL_PAIRS} are required. "
            "A judge handed two documents will find a winner, and a run with no null "
            "pairs cannot see that happening. Supply cosmetic rewrites — same design, "
            "same decisions, same values, different prose."
        )
    if len(null_ids) < len(shared) * MIN_NULL_RATIO:
        fail(
            f"{len(null_ids)} null pair(s) against {len(shared)} signal pairs; at least "
            f"one null per {int(1 / MIN_NULL_RATIO)} signal pairs is required, so the "
            "control can carry the contrast it is guarding."
        )

    identical = [pid for pid in null_ids if " ".join(nulls[pid].split()) == " ".join(arm_a[pid].split())]
    if identical:
        fail(
            f"null rewrite(s) identical to their arm-A response: {', '.join(identical)}. Identical "
            "text is a trivial null that any judge passes; a null must be a cosmetic rewrite of "
            "the same design in different words."
        )

    pairs: list[dict[str, Any]] = []
    for pid in shared:
        pairs.append({"id": pid, "kind": "signal", "a": arm_a[pid], "b": arm_b[pid],
                      "a_role": "arm-a", "b_role": "arm-b"})
    for pid in null_ids:
        pairs.append({"id": pid, "kind": "null", "a": arm_a[pid], "b": nulls[pid],
                      "a_role": "arm-a", "b_role": "cosmetic-rewrite"})

    presented: list[dict[str, Any]] = []
    for pair in pairs:
        for order in ("ab", "ba"):
            first, second = (("a", "b") if order == "ab" else ("b", "a"))
            internal = f"{pair['kind']}-{pair['id']}-{order}"
            presented.append({
                "pair": internal,
                "request_id": request_id(internal),
                "id": pair["id"],
                "kind": pair["kind"],
                "document_1": pair[first],
                "document_2": pair[second],
                "doc1_role": pair[f"{first}_role"],
                "doc2_role": pair[f"{second}_role"],
            })
    # Deterministic shuffle: consecutive requests must not alternate by kind or by
    # which arm leads, or a judge reading them in order can infer the design.
    presented.sort(key=lambda r: hashlib.sha256(r["pair"].encode()).hexdigest())
    return presented


def build_system_prompt() -> str:
    return (
        "You are an experienced mobile designer judging which of two documents "
        "describes the better design. Judge the screen each one describes, not the "
        "document: ignore prose style, wording, thoroughness of explanation and "
        "length. A longer document is not a better design, and a document that "
        "names more values — more tokens, more durations, more measurements — is "
        "not thereby describing a better screen. Two documents can describe the "
        "same design in different words; if "
        "that is what you find, say so. Answer with one of `document-1`, "
        "`document-2`, or `no-meaningful-difference`. All three are ordinary "
        "answers — do not reach for a winner. Do not apply a rubric or a checklist; "
        "your own judgement is what is being asked for. Then name the single "
        "difference in the design that decided it and what it costs a user."
    )


def render_request_jsonl(presented: list[dict[str, Any]]) -> str:
    lines = []
    for record in presented:
        lines.append(json.dumps({
            "schema": REQUEST_SCHEMA_VERSION,
            "pair": record["request_id"],
            "system": build_system_prompt(),
            "document_1": record["document_1"],
            "document_2": record["document_2"],
        }, ensure_ascii=False) + "\n")
    return "".join(lines)


def parse_verdicts(text: str, source: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{source}: line {number} is not valid JSON ({exc})")
        if not isinstance(record, dict) or "pair" not in record or "verdict" not in record:
            fail(f"{source}: line {number} must be an object with `pair` and `verdict`")
        verdict = str(record["verdict"])
        if verdict not in VERDICTS:
            fail(f"{source}: line {number} has unknown verdict `{verdict}`; expected one of {', '.join(VERDICTS)}")
        out[str(record["pair"])] = verdict
    if not out:
        fail(f"{source}: no verdicts found")
    return out


def binomial_p(wins: int, decided: int) -> float:
    """One-sided probability of `wins` or more out of `decided` under a fair coin."""
    if decided == 0:
        return 1.0
    return sum(comb(decided, k) for k in range(wins, decided + 1)) / 2 ** decided


def verdict_for(record: dict[str, Any], verdicts: dict[str, str]) -> str | None:
    # Judges answer with the opaque request id; fixture packs are keyed by the internal id.
    return verdicts.get(record["request_id"], verdicts.get(record["pair"]))


def sign_test_two_sided(wins: int, losses: int) -> float:
    """Exact two-sided sign test over decided pairs (ties dropped)."""
    decided = wins + losses
    if decided == 0:
        return 1.0
    return min(1.0, 2 * binomial_p(max(wins, losses), decided))


def measure(presented: list[dict[str, Any]], verdicts: dict[str, str]) -> dict[str, Any]:
    missing = [r["pair"] for r in presented if verdict_for(r, verdicts) is None]
    if missing:
        fail(
            f"{len(missing)} presented pair(s) have no verdict, so order counterbalancing "
            f"is incomplete: {', '.join(missing[:5])}"
            + (" …" if len(missing) > 5 else "")
        )

    by_pair: dict[tuple[str, str], list[str]] = {}
    for record in presented:
        verdict = verdict_for(record, verdicts)
        if verdict == "no-meaningful-difference":
            picked = "none"
        else:
            picked = record["doc1_role"] if verdict == "document-1" else record["doc2_role"]
        by_pair.setdefault((record["kind"], record["id"]), []).append(picked)

    signal = {k: v for k, v in by_pair.items() if k[0] == "signal"}
    nulls = {k: v for k, v in by_pair.items() if k[0] == "null"}

    a_wins = sum(1 for picks in signal.values() for p in picks if p == "arm-a")
    b_wins = sum(1 for picks in signal.values() for p in picks if p == "arm-b")
    ties = sum(1 for picks in signal.values() for p in picks if p == "none")

    # The unit of inference is the pair, not the judgement. Both presentation orders of
    # one pair judge the same two documents, so counting them as independent coin flips
    # (and testing one-sided toward whichever arm happens to lead) reported p < 0.05 in
    # up to ~29% of runs with equal arms.
    pair_a = sum(1 for picks in signal.values() if picks.count("arm-a") > picks.count("arm-b"))
    pair_b = sum(1 for picks in signal.values() if picks.count("arm-b") > picks.count("arm-a"))
    pair_tied = len(signal) - pair_a - pair_b
    leader = "arm-a" if pair_a > pair_b else "arm-b" if pair_b > pair_a else "none"

    order_invariant = sum(1 for picks in signal.values() if picks[0] == picks[1] != "none")
    null_agreed_winner = sum(1 for picks in nulls.values() if picks[0] == picks[1] != "none")
    null_none = sum(1 for picks in nulls.values() for p in picks if p == "none")

    null_rate = null_agreed_winner / len(nulls) if nulls else 1.0
    readable = null_rate <= NULL_AGREED_WINNER_MAX

    return {
        "signal_pairs": len(signal),
        "null_pairs": len(nulls),
        "arm_a_wins": a_wins,
        "arm_b_wins": b_wins,
        "ties": ties,
        "pair_a_wins": pair_a,
        "pair_b_wins": pair_b,
        "pair_ties": pair_tied,
        "leader": leader,
        "p_value": sign_test_two_sided(pair_a, pair_b),
        "order_invariant": order_invariant,
        "null_agreed_winner": null_agreed_winner,
        "null_agreed_winner_rate": null_rate,
        "null_no_difference_judgements": null_none,
        "readable": readable,
    }


def report(result: dict[str, Any]) -> None:
    # The control is printed first and a failed control stops the report before any win
    # rate or p-value reaches stdout: a number printed next to a refusal still gets read.
    print("== Control ==")
    print(f"  null pairs          : {result['null_pairs']}")
    print(f"  no-difference calls : {result['null_no_difference_judgements']}/{result['null_pairs'] * 2} judgements")
    print(f"  agreed winner on a null pair: {result['null_agreed_winner']}/{result['null_pairs']}"
          f" ({result['null_agreed_winner_rate']:.0%}, ceiling {NULL_AGREED_WINNER_MAX:.0%})")

    if not result["readable"]:
        print("[UNREADABLE] The control failed; the contrast is withheld.")
        fail(
            "The control failed: this judge picks a winner between two documents that "
            "describe the same design. The contrast is UNREADABLE and no win rate from it "
            "means anything. Fix the judge before reading the arms."
        )

    print("== Paired comparison ==")
    print(f"  signal pairs        : {result['signal_pairs']} ({result['signal_pairs'] * 2} judgements)")
    print(f"  pairs A / B / tied  : {result['pair_a_wins']} / {result['pair_b_wins']} / {result['pair_ties']}")
    print(f"  judgements A / B / no-difference: {result['arm_a_wins']} / {result['arm_b_wins']} / {result['ties']}")
    print(f"  order-invariant     : {result['order_invariant']}/{result['signal_pairs']} pairs")
    print(f"  two-sided sign test (pairs): p = {result['p_value']:.5f} (leader: {result['leader']})")
    print("[OK] Control held; the contrast is readable.")


def self_test() -> None:
    """Prove the report separates, and that it refuses a run whose control failed.

    A self-test that only proves the pipe works is worth nothing — this repository
    shipped a green oracle over a broken function once already. So the fixture pack
    holds three corpora and the test asserts the harness tells them apart: one where
    an arm genuinely wins, one where the arms are indistinguishable, and one whose
    null pairs draw agreed winners and must be refused.
    """
    try:
        pack = json.loads(FIXTURES.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Missing fixtures: {FIXTURES}")

    errors: list[str] = []

    def measured(name: str) -> dict[str, Any]:
        case = pack[name]
        presented = build_pairs(case["arm_a"], case["arm_b"], case["nulls"])
        return measure(presented, case["verdicts"])

    separating = measured("separating")
    indistinguishable = measured("indistinguishable")
    broken_control = measured("broken_control")

    if not separating["readable"]:
        errors.append("`separating`: the control fails on a corpus whose nulls are all called the same")
    if separating["p_value"] >= 0.05:
        errors.append(f"`separating`: p = {separating['p_value']:.3f}; a corpus with a real winner does not reach significance")
    if separating["order_invariant"] != separating["signal_pairs"]:
        errors.append("`separating`: order invariance is not detected where every pair agrees across both orders")

    if not indistinguishable["readable"]:
        errors.append("`indistinguishable`: the control fails where it should hold")
    if indistinguishable["p_value"] < 0.05:
        errors.append(
            f"`indistinguishable`: p = {indistinguishable['p_value']:.3f}; the report claims a "
            "winner between two arms judged the same"
        )
    if indistinguishable["p_value"] <= separating["p_value"]:
        errors.append("the report does not separate a real contrast from a null one")

    if broken_control["readable"]:
        errors.append(
            "`broken_control`: a run whose judge picks winners between identical designs is "
            "reported as readable. The refusal is the point of this harness"
        )

    # The refusals themselves, run rather than read: each must exit non-zero, and the
    # failed control must not print a contrast on its way out. Reading the constants
    # cannot see a refusal that has been widened into a no-op; running it can.
    def refuses(action) -> tuple[bool, str]:
        out, err = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                action()
        except SystemExit as exc:
            return bool(exc.code), out.getvalue()
        return False, out.getvalue()

    refused, printed = refuses(lambda: report(broken_control))
    if not refused:
        errors.append("report(): a failed control exits 0; the refusal has been widened into a no-op")
    if "p =" in printed or "pairs A / B" in printed:
        errors.append("report(): a failed control still prints the contrast to stdout")

    case = pack["separating"]
    refused, _ = refuses(lambda: build_pairs(case["arm_a"], case["arm_b"], {pid: case["arm_a"][pid] for pid in case["nulls"]}))
    if not refused:
        errors.append("build_pairs(): byte-identical nulls are accepted as a control")
    many = {f"x{i}": f"design {i}" for i in range(3 * MIN_NULL_PAIRS + 3)}
    few_nulls = {pid: many[pid] + " (reworded)" for pid in list(many)[:MIN_NULL_PAIRS]}
    refused, _ = refuses(lambda: build_pairs(many, {pid: v + " b" for pid, v in many.items()}, few_nulls))
    if not refused:
        errors.append("build_pairs(): too few nulls for the number of signal pairs is accepted")

    # The unit of inference is the pair: three pairs won by one arm in both orders is a
    # two-sided sign test of 3/3 (p = 0.25), not six independent judgements (p = 0.016).
    three = {f"t{i}": f"three-pair design {i}" for i in range(3)}
    three_nulls = {pid: text + " (reworded)" for pid, text in three.items()}
    three_presented = build_pairs(three, {pid: text + " worse" for pid, text in three.items()}, three_nulls)
    three_verdicts = {}
    for record in three_presented:
        if record["kind"] == "null":
            three_verdicts[record["pair"]] = "no-meaningful-difference"
        else:
            three_verdicts[record["pair"]] = "document-1" if record["doc1_role"] == "arm-b" else "document-2"
    three_result = measure(three_presented, three_verdicts)
    if three_result["p_value"] < 0.2:
        errors.append(
            f"p-value: three pairs won in both orders report p = {three_result['p_value']:.4f}; "
            "the two orders of one pair are being counted as independent judgements"
        )

    # What the judge actually receives, not what this module calls it internally.
    sent = [json.loads(line)["pair"] for line in render_request_jsonl(build_pairs(case["arm_a"], case["arm_b"], case["nulls"])).splitlines()]
    leaked = [pid for pid in sent if pid.startswith(("signal", "null")) or pid.endswith(("-ab", "-ba"))]
    if leaked:
        errors.append(f"requests sent to the judge reveal the pair kind or order: {', '.join(leaked[:3])}")

    if errors:
        fail("Paired-comparison self-test failed:\n" + "\n".join(f"  - {e}" for e in errors))
    print("[OK] Paired comparison separates a real contrast from a null one, and refuses a failed control.")


def run_judge_command(command: str, presented: list[dict[str, Any]]) -> dict[str, str]:
    process = subprocess.run(
        shlex.split(command),
        input=render_request_jsonl(presented),
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        fail(f"judge command exited {process.returncode}:\n{process.stderr.strip()}")
    return parse_verdicts(process.stdout, "judge command output")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--arm-a", type=Path, help="JSONL responses for arm A")
    parser.add_argument("--arm-b", type=Path, help="JSONL responses for arm B")
    parser.add_argument("--nulls", type=Path, help="JSONL cosmetic rewrites of arm-A responses")
    parser.add_argument("--export-requests", type=Path, help="write judge requests and stop")
    parser.add_argument("--verdicts", type=Path, help="JSONL verdicts to score")
    parser.add_argument("--judge-command", help="command that reads request JSONL on stdin and writes verdict JSONL")
    parser.add_argument("--fixture-arms", help="load arms from the committed fixture pack instead of files, so the judge adapter can be proven without a corpus")
    parser.add_argument("--dry-run", action="store_true", help="build the pairs and print the shape; no model needed")
    parser.add_argument("--self-test", action="store_true", help="prove the report discriminates and refuses a failed control")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.self_test or len(sys.argv) == 1:
        self_test()
        return
    if not (args.arm_a or args.arm_b or args.fixture_arms):
        # Falling back to the self-test here used to print [OK] and exit 0 for
        # `--verdicts missing.jsonl` or `--judge-command ...` with no arms: a passed
        # comparison that never read the data or ran the judge.
        fail("supply --arm-a, --arm-b and --nulls (or --fixture-arms); use --self-test for the self-test")

    if args.fixture_arms:
        pack = json.loads(FIXTURES.read_text(encoding="utf-8"))
        if args.fixture_arms not in pack:
            fail(f"unknown fixture corpus `{args.fixture_arms}`")
        case = pack[args.fixture_arms]
        presented = build_pairs(case["arm_a"], case["arm_b"], case["nulls"])
    else:
        if not (args.arm_a and args.arm_b and args.nulls):
            fail("--arm-a, --arm-b and --nulls are all required")
        presented = build_pairs(
            load_responses(args.arm_a, "arm A"),
            load_responses(args.arm_b, "arm B"),
            load_responses(args.nulls, "null rewrites"),
        )

    if args.export_requests:
        args.export_requests.write_text(render_request_jsonl(presented), encoding="utf-8")
        print(f"[OK] wrote {len(presented)} judge requests to {args.export_requests}")
        return

    if args.dry_run:
        signal = sum(1 for r in presented if r["kind"] == "signal") // 2
        null = sum(1 for r in presented if r["kind"] == "null") // 2
        print(f"[OK] {signal} signal pairs and {null} null pairs -> {len(presented)} judgements, both orders each.")
        return

    if args.judge_command:
        verdicts = run_judge_command(args.judge_command, presented)
    elif args.verdicts:
        verdicts = parse_verdicts(args.verdicts.read_text(encoding="utf-8"), str(args.verdicts))
    else:
        fail("supply --verdicts, --judge-command, --export-requests or --dry-run")

    report(measure(presented, verdicts))


if __name__ == "__main__":
    main()
