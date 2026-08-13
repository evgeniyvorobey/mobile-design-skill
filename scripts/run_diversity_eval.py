#!/usr/bin/env python3
"""
Measure whether the skill's answers differ from each other, or only look like they do.

Sameness was the owner-reported symptom this whole line of work started from, and
until now it has only ever been measured by reading outputs by hand. This script
extracts a **decision vector** from each generated response — the catalog entries it
sampled, the asset class it committed to, the score it derived, the dimension it named
as the blocker, the base units and ratios it emitted — and reports the spread.

Why vectors and not prose: a pairwise 5-gram similarity over the calibration bodies was
specified once and measured at a median of 0.0, because those blocks describe different
domains in different words. Word-level overlap cannot see structural sameness. A small
structured vector can.

**Thresholds are asserted only where this repository has measured data.** Everything
else is reported. Guessing a threshold produces either a check that passes vacuously
forever or one that forces dishonest output; both have already happened here once.

Usage:
    python3 scripts/run_diversity_eval.py --self-test
    python3 scripts/run_diversity_eval.py --responses /tmp/responses.jsonl
    python3 scripts/run_diversity_eval.py --responses /tmp/responses.jsonl --assert
    python3 scripts/run_diversity_eval.py --responses /tmp/responses.jsonl --baseline
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_repo import extract_section, label_body  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "examples/evals/diversity-fixtures.json"

CALIBRATION_SECTIONS = (
    "Design quality calibration",
    "Design quality requirements",
    "Design quality rationale",
)

# Token namespaces map to the six asset classes named in SKILL.md. The fallback keyword
# scan exists because a response may name the class in prose instead of a token prefix.
ASSET_NAMESPACES = {
    "layout": "layout structure",
    "grid": "layout structure",
    "type": "type treatment",
    "text": "type treatment",
    "motion": "motion signature",
    "anim": "motion signature",
    "color": "colour",
    "colour": "colour",
    "accent": "colour",
    "shape": "geometry",
    "fill": "geometry",
    "marker": "geometry",
    "rail": "geometry",
    "meter": "geometry",
    "bar": "geometry",
    "icon": "illustration",
    "illo": "illustration",
    "mascot": "illustration",
}
ASSET_KEYWORDS = {
    "layout structure": ("layout structure",),
    "type treatment": ("type treatment", "typographic treatment"),
    "motion signature": ("motion signature",),
    "colour": ("colour asset", "color asset"),
    "geometry": ("geometry", "shape asset"),
    "illustration": ("illustration", "mascot"),
}

# Measured during the 1.17.0 and 1.18.0 live acceptance passes. These are the only
# numbers in this file that are not guesses, so they are the only ones asserted.
THRESHOLDS = {
    "score_concentration": {
        "max": 0.75,
        "measured": "4 of 4 runs scored 4/5 (concentration 1.00) in the 1.17.0 pass",
    },
    "provenance_concentration": {
        "max": 0.50,
        "measured": "7 distinct catalog entries across 4 domain runs in the 1.18.0 pass",
    },
    "blocker_concentration": {
        "max": 0.75,
        "measured": "2 distinct blocking dimensions across 4 runs in the 1.17.0 pass",
    },
}
# The dimension read is the second thing this eval has to see. Until now it read only the
# derived median, so a corpus where every dimension is 3 or 4 -- and every median therefore
# 4 -- registered as score_concentration 1.0 with no explanation of why. All six fields
# below are reported and none is asserted: no live run has ever produced a baseline for
# them, and inventing one is how this repository already shipped a threshold that failed by
# construction. The self-test asserts something different and cheaper to be honest about --
# that the metric SEPARATES a uniform corpus from a varied one, which is a property of the
# metric, not a claim about the model.
DIMENSION_FIELDS = (
    "distinct_dimension_bands",
    "dimension_min",
    "dimension_max",
    "adjacent_pair_share",
    "dimension_range_median",
    "flat_vector_share",
)

DIMENSION_READ_LINE = re.compile(r"Dimension read:(?P<body>[^\n]*)")
DIMENSION_READ_PAIR = re.compile(r"^(?P<name>.+?)[:\s]\s*(?P<band>[1-5]|n/v)$", re.IGNORECASE)


def dimension_read(body: str) -> list[int | None]:
    """Bands from a `Dimension read:` line; `None` for `n/v`, excluded from every measure.

    Hazards in the committed shape: the trailing `Median of the assessable = N.`
    restatement on the same line, `colour/state` carrying a slash, and
    `context & brand fit` carrying an ampersand.
    """
    match = DIMENSION_READ_LINE.search(body)
    if not match:
        return []
    core = re.split(r"Median of", match.group("body"), maxsplit=1)[0]
    bands: list[int | None] = []
    for chunk in core.split(","):
        # First band token in the chunk, not the whole chunk anchored. A live run appended
        # prose after the last dimension ("... distinctiveness 5. All nine assessable --
        # nothing is `n/v` ...") and an anchored match dropped that dimension silently,
        # which is the failure mode where a parser under-counts instead of erroring.
        pair = re.search(r"\b([1-5]|n/v)\b(?=[.,;]|\s|$)", chunk.strip(), re.IGNORECASE)
        if pair:
            band = pair.group(1).lower()
            bands.append(None if band == "n/v" else int(band))
    return bands


# Reported, never asserted. `vector_similarity` has no baseline at all.
# `asset_class_count` has one — 2 of 6 classes across 6 runs in the 1.18.0 pass — but
# that measurement is the FLOOR we want to move, not a bar the output already clears.
# Asserting 3 here would fail by construction on the next honest run, which is the
# same mistake as asserting a threshold nobody measured.
UNASSERTED = ("vector_similarity", "asset_class_count") + DIMENSION_FIELDS


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def calibration_body(response: str) -> str:
    for section in CALIBRATION_SECTIONS:
        body = extract_section(response, section)
        if body:
            return body
    return ""


def classify_asset(signature: str) -> str | None:
    token = re.search(r"`(?P<token>[a-z][a-z0-9]*)[.\-][a-z0-9-]+`", signature, re.IGNORECASE)
    if token:
        namespace = token.group("token").lower()
        if namespace in ASSET_NAMESPACES:
            return ASSET_NAMESPACES[namespace]
    lowered = signature.lower()
    for asset_class, needles in ASSET_KEYWORDS.items():
        if any(needle in lowered for needle in needles):
            return asset_class
    if lowered.lstrip().startswith("none"):
        return "none/inert"
    return None


def decision_vector(response: str, label: str) -> dict[str, Any]:
    body = calibration_body(response)
    signature = label_body(body, "Signature move:")
    score = re.search(r"Quality target:\s*\[?([1-5])/5", body)
    blocker = re.search(r"blocked from\s*\[?[1-5]\]?/5\s*by\s*\**([^*(—\-.;\n]+)", body, re.IGNORECASE)

    alternatives = extract_section(response, "Alternatives considered") or extract_section(
        response, "Key decision tradeoffs"
    )
    provenance = {
        re.sub(r"[*_`]", "", src).strip().lower()
        for src in re.findall(r"from:\s*([^)\n,;]+)", body + "\n" + alternatives, re.IGNORECASE)
    }

    return {
        "id": label,
        "provenance": sorted(p for p in provenance if p and p != "baseline"),
        "dimensions": dimension_read(body) or dimension_read(response),
        "asset_class": classify_asset(signature),
        "score": score.group(1) if score else None,
        "blocker": blocker.group(1).strip().lower() if blocker else None,
        "base_units": sorted(set(re.findall(r"base unit\s*(\d+)", response, re.IGNORECASE))),
        "ratios": sorted(set(re.findall(r"ratio\s*(\d\.\d+)", response, re.IGNORECASE))),
    }


def vector_tokens(vector: dict[str, Any]) -> set[str]:
    tokens: set[str] = set()
    for name in ("provenance", "base_units", "ratios"):
        tokens.update(f"{name}:{v}" for v in vector.get(name) or [])
    for name in ("asset_class", "score", "blocker"):
        value = vector.get(name)
        if value:
            tokens.add(f"{name}:{value}")
    return tokens


def concentration(values: list[Any]) -> float:
    present = [v for v in values if v]
    if not present:
        return 0.0
    return Counter(present).most_common(1)[0][1] / len(present)


def measure(vectors: list[dict[str, Any]]) -> dict[str, Any]:
    provenance = [p for v in vectors for p in v["provenance"]]
    reads = [[b for b in (v.get("dimensions") or []) if b is not None] for v in vectors]
    reads = [r for r in reads if r]
    bands = [b for r in reads for b in r]
    ranges = [max(r) - min(r) for r in reads]
    token_sets = [vector_tokens(v) for v in vectors]
    similarities = [
        len(a & b) / len(a | b)
        for a, b in itertools.combinations(token_sets, 2)
        if a | b
    ]
    return {
        "samples": len(vectors),
        "score_concentration": round(concentration([v["score"] for v in vectors]), 3),
        "provenance_concentration": round(concentration(provenance), 3),
        "blocker_concentration": round(concentration([v["blocker"] for v in vectors]), 3),
        "asset_class_count": len({v["asset_class"] for v in vectors if v["asset_class"]}),
        "distinct_provenance": len(set(provenance)),
        "vector_similarity": round(statistics.median(similarities), 3) if similarities else 0.0,
        "distinct_dimension_bands": len(set(bands)),
        "dimension_min": min(bands) if bands else 0,
        "dimension_max": max(bands) if bands else 0,
        # How much of the scale the answers never use, stated without assuming WHERE the
        # collapse sits. The first version of this field counted the share on bands 3 and 4,
        # which is the shape the defect had when it was found -- and the live acceptance run
        # for this release came back 93% on bands 4 and 5, a collapse the field could not
        # see. Largest share held by any two adjacent bands, so it catches either end.
        "adjacent_pair_share": round(
            max(
                (sum(1 for b in bands if b in (low, low + 1)) for low in (1, 2, 3, 4)),
                default=0,
            ) / len(bands),
            3,
        ) if bands else 0.0,
        # Within-response flatness, independent of spread across responses.
        "dimension_range_median": round(statistics.median(ranges), 3) if ranges else 0.0,
        "flat_vector_share": round(sum(1 for r in ranges if r == 0) / len(ranges), 3) if ranges else 0.0,
    }


def check(metrics: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    for name, rule in THRESHOLDS.items():
        value = metrics[name]
        if "max" in rule and value > rule["max"]:
            problems.append(
                f"{name} = {value} exceeds {rule['max']} — measured baseline: {rule['measured']}"
            )
        if "min" in rule:
            if metrics["samples"] < rule.get("min_samples", 0):
                continue
            if value < rule["min"]:
                problems.append(
                    f"{name} = {value} is below {rule['min']} across {metrics['samples']} "
                    f"samples — measured baseline: {rule['measured']}"
                )
    return problems


def report(metrics: dict[str, Any], enforce: bool) -> None:
    print(f"[OK] Decision vectors extracted from {metrics['samples']} responses")
    for name, value in metrics.items():
        if name == "samples":
            continue
        mark = " (reported, not asserted — no baseline)" if name in UNASSERTED else ""
        print(f"  {name}: {value}{mark}")

    problems = check(metrics)
    if not problems:
        print("[OK] Diversity thresholds satisfied.")
        return
    body = "\n".join(f"  - {p}" for p in problems)
    if enforce:
        fail(f"Diversity thresholds not met:\n{body}")
    print(f"[WARN] Diversity thresholds not met (reporting only; pass --assert to enforce):\n{body}")


def load_responses(path: Path) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{path}: line {number} is not valid JSON ({exc})")
        items.append((str(record.get("id", f"line-{number}")), str(record.get("response", ""))))
    if not items:
        fail(f"{path}: no response records found")
    return items


def self_test() -> None:
    """Prove the metric discriminates, and the extractor reads a real response.

    A self-test that only proves the pipe works is worth nothing — this repository
    has shipped a green oracle over a broken function once already. So the fixture
    pack holds one deliberately uniform corpus and one deliberately varied corpus,
    and the test asserts the measurements separate them.
    """
    try:
        pack = json.loads(FIXTURES.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Missing fixtures: {FIXTURES}")

    errors: list[str] = []

    uniform = measure(pack["uniform"])
    varied = measure(pack["varied"])
    if not check(uniform):
        errors.append("the `uniform` fixture corpus passes the thresholds; the metric does not discriminate")
    if check(varied):
        errors.append(
            "the `varied` fixture corpus fails the thresholds: "
            + "; ".join(check(varied))
        )
    for name in ("score_concentration", "provenance_concentration", "adjacent_pair_share"):
        if uniform[name] <= varied[name]:
            errors.append(
                f"{name} does not separate the corpora "
                f"(uniform {uniform[name]} vs varied {varied[name]})"
            )
    # These run the other way: the varied corpus should read higher, not lower.
    for name in ("distinct_dimension_bands", "dimension_range_median"):
        if uniform[name] >= varied[name]:
            errors.append(
                f"{name} does not separate the corpora "
                f"(uniform {uniform[name]} vs varied {varied[name]})"
            )

    # The extractor has to work on a real committed response, not only on fixtures.
    example = (ROOT / "examples/generate-screen.md").read_text(encoding="utf-8")
    match = re.search(r"## Example output\s*\n\s*```md\n(?P<body>.*?)\n```", example, re.DOTALL)
    if not match:
        errors.append("examples/generate-screen.md: no `## Example output` block to extract from")
    else:
        vector = decision_vector(match.group("body"), "generate-screen")
        if vector["score"] != "3":
            errors.append(f"extractor read score `{vector['score']}` from generate-screen.md, expected `3`")
        if not vector["provenance"]:
            errors.append("extractor found no catalog provenance in generate-screen.md")
        if not vector["blocker"]:
            errors.append("extractor found no blocking dimension in generate-screen.md")
        # Re-derive rather than replay: the median is computed from the parsed vector and
        # checked against the independently parsed printed score, so either parser breaking
        # fails the test.
        parsed = [b for b in vector["dimensions"] if b is not None]
        if len(parsed) != 9:
            errors.append(
                f"extractor read {len(parsed)} dimension bands from generate-screen.md, expected 9"
            )
        elif vector["score"] and int(statistics.median(sorted(parsed))) != int(vector["score"]):
            errors.append(
                "extractor's dimension median "
                f"({int(statistics.median(sorted(parsed)))}) disagrees with the printed "
                f"Quality target ({vector['score']}) in generate-screen.md"
            )

    if errors:
        fail("Diversity self-test failed:\n" + "\n".join(f"  - {e}" for e in errors))

    print("[OK] Metric separates the uniform and varied fixture corpora:")
    print(f"     uniform  {ck(uniform)}")
    print(f"     varied   {ck(varied)}")
    print("[OK] Extractor reads score, provenance and blocker from a committed response.")


def ck(metrics: dict[str, Any]) -> str:
    return (
        f"score_conc={metrics['score_concentration']} "
        f"prov_conc={metrics['provenance_concentration']} "
        f"classes={metrics['asset_class_count']} "
        f"similarity={metrics['vector_similarity']} "
        f"bands={metrics['distinct_dimension_bands']} "
        f"pair_share={metrics['adjacent_pair_share']} "
        f"range={metrics['dimension_range_median']}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure decision diversity across generated responses.")
    parser.add_argument("--responses", type=Path, help="Response JSONL, as produced for run_generation_eval.py.")
    parser.add_argument("--assert", dest="enforce", action="store_true", help="Exit non-zero when a threshold with a measured baseline is not met.")
    parser.add_argument("--baseline", action="store_true", help="Print the raw decision vectors as JSON, for calibrating thresholds.")
    parser.add_argument("--self-test", action="store_true", help="Prove the metric discriminates and the extractor works. Needs no model.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.self_test or not args.responses:
        self_test()
        return

    vectors = [decision_vector(response, label) for label, response in load_responses(args.responses)]
    if args.baseline:
        print(json.dumps(vectors, indent=2, ensure_ascii=False))
        return
    report(measure(vectors), args.enforce)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover
        fail(f"Unexpected diversity eval error: {exc}")
