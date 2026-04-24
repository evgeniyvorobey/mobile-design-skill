# LLM-as-Judge Runner

This document defines the runner for semantic evaluation of the design-quality rubric fixtures.

The structural validator checks that examples and fixtures are well formed. The judge runner checks whether an LLM judge can assign the expected rubric score and explain the failure or quality level using the same dimensions as `docs/design-quality-rubric.md`.

---

## Runner script

Use:

```bash
python3 scripts/run_rubric_judge.py --dry-run
```

This loads every fixture under `examples/evals/` and confirms score coverage.

Export provider-agnostic JSONL judge requests:

```bash
python3 scripts/run_rubric_judge.py --export-jsonl tmp/rubric-judge-requests.jsonl
```

Validate JSONL judge outputs:

```bash
python3 scripts/run_rubric_judge.py --judge-output tmp/rubric-judge-results.jsonl
```

Self-test the parser and comparison logic without calling an LLM:

```bash
python3 scripts/run_rubric_judge.py \
  --export-expected-output tmp/rubric-judge-expected.jsonl \
  --judge-output tmp/rubric-judge-expected.jsonl
```

The runner intentionally does not call a specific LLM provider. It emits a stable JSONL contract that can be used with OpenAI, Anthropic, local models, or any internal evaluation harness.

---

## Judge output contract

Each judge output line must include the fixture id and a JSON object with this shape:

```json
{
  "id": "rubric-score-3-acceptable-baseline-delivery-status",
  "judge": {
    "score": 3,
    "verdict": "acceptable baseline",
    "cap": "No cap",
    "hard_limits": [],
    "dimension_scores": {
      "attention_path_and_hierarchy": 4,
      "composition_and_spacing": 3,
      "typography_craft": 3,
      "color_state_and_contrast": 3,
      "density_and_rhythm": 3,
      "interaction_polish_and_motion": 3,
      "context_and_brand_fit": 3,
      "production_readiness": 3
    },
    "failed_dimensions": [
      "production readiness",
      "color/state specificity",
      "typography craft"
    ],
    "rationale": "The response covers the task but lacks concrete production mechanisms.",
    "improvement_suggestions": [
      "Add semantic status treatment with non-color cues.",
      "Add token-ready spacing and typography values."
    ]
  }
}
```

The runner also accepts records where the judge JSON appears under `output`, `response`, or `result`, as long as a JSON object can be extracted.

---

## Pass criteria

For every fixture:

- score must match `expected_score`
- verdict must include the expected verdict phrase
- dimension scores must include all rubric dimensions as integers from 1 to 5
- expected hard limits must appear in the judge result when the fixture defines them
- expected failed dimensions must appear in the judge result or rationale
- improvement suggestions must contain at least two concrete items

Extra output ids fail the run. Missing fixture ids fail the run.

---

## What this runner does not do

It does not replace human design judgment. It checks calibration: whether the judge applies the same rubric consistently across known examples.

It also does not make a weak generated response stronger by itself. It tells the skill maintainers when the scoring model drifts from the rubric.

---

## Maintenance

When adding a new rubric fixture:

1. Add a JSON fixture under `examples/evals/`.
2. Include every required field used by `scripts/validate_repo.py`.
3. Include all eight dimension scores.
4. Add at least two improvement suggestions.
5. Run `python3 scripts/validate_repo.py`.
6. Run `python3 scripts/run_rubric_judge.py --dry-run`.
