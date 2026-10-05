# Evaluation

What this repository evaluates in 2.x, and with what.

Through 1.x this document listed, mode by mode, the sections and labels a response had to carry, and a validator checked committed examples against that list. That contract is gone: the skill no longer prescribes a format, so there is nothing structural to check in an answer. What is left is three instruments, and each answers a different question.

| Question | Instrument | Needs a model |
|---|---|---|
| Is the skill's answer at least as good as the same model's answer with no skill, with no more errors? | The release gate: `scripts/run_baseline_gate.py`, described in [`paired-comparison.md`](paired-comparison.md) | yes |
| Did a change to the instruction text make the output better? | The paired comparison: `scripts/run_paired_eval.py` | yes |
| What does one artifact state, dimension by dimension, when a score is asked for? | The 1-5 rubric: [`design-quality-rubric.md`](design-quality-rubric.md) and `scripts/run_rubric_judge.py` | yes |

`scripts/validate_repo.py` and `scripts/validate_release.py` run in CI with no model. They check that files exist, links resolve, fixtures are well formed and the instruments still refuse what they are built to refuse. They say nothing about whether an answer is good.

---

## The release gate

Run it before tagging any release that changes what the model reads: `SKILL.md`, `skill/`, or a document `SKILL.md` points to. It generates one answer per brief with the skill and one without, has blind judges compare them in both orders with a null control, audits both arms blind for errors, and applies a rule: control readable, skill share at least 0.5 with ties counted half, and no more medium-or-high errors than the answer with no skill. The result goes in the release's CHANGELOG entry, pass or fail. The procedure, the brief sets and the sealed held-out set are in [`paired-comparison.md`](paired-comparison.md).

```bash
python3 scripts/run_baseline_gate.py --self-test
python3 scripts/run_baseline_gate.py --dry-run --set core
```

What a reviewer should look for when reading the gate's answers by hand is what the judges have named in every run so far:

- whether the screen finishes its primary job or only reports on it
- whether the answer decides, or hands decisions back as open questions and placeholders
- whether the answer is the size the request asked for
- internal contradictions: a number that differs between a mockup and a table, a rule its own example breaks
- wrong platform facts for the OS version named

[`weaknesses.md`](weaknesses.md) is the longer catalogue of failure patterns, kept as a reference for reviews.

---

## Comparing two arms of output

The rubric above scores one artifact and asks what it states. It does not read whether one design is better than another: measured on six designs against six deliberately worse twins, its nine boundary questions returned the identical band **12 paired scorings out of 12**, while a rubric-free forced choice on the same pairs returned **12 of 12** judgements (6 of 6 pairs) in the right direction and named the injected mechanism every time.

Use [`paired-comparison.md`](paired-comparison.md) and `../scripts/run_paired_eval.py` when the question is whether a change made the output better — one prompt pack run against two trees.

Prove the report discriminates, with no model in the loop:

```bash
python3 scripts/run_paired_eval.py --self-test
```

Prove the judge adapter round-trips:

```bash
python3 scripts/run_paired_eval.py --fixture-arms separating \
    --judge-command "python3 scripts/paired_eval_oracle_agent.py"
```

Run a real comparison:

```bash
python3 scripts/run_paired_eval.py --arm-a before.jsonl --arm-b after.jsonl \
    --nulls cosmetic-rewrites.jsonl --export-requests tmp/pairs.jsonl
python3 scripts/run_paired_eval.py --arm-a before.jsonl --arm-b after.jsonl \
    --nulls cosmetic-rewrites.jsonl --verdicts tmp/verdicts.jsonl
```

When the question is whether the skill beats the same model with **no skill**, use `../scripts/run_baseline_gate.py`: the same instrument with a brief pack, a blind error audit and a release rule on top. The procedure and the rule are in [`paired-comparison.md`](paired-comparison.md).

```bash
python3 scripts/run_baseline_gate.py --self-test
```

**Null pairs are required, not optional.** A judge handed two documents will find a winner; a run without cosmetic-rewrite pairs cannot see that happening, and the harness refuses to report one. A run whose judge names an agreed winner on more than a third of its null pairs is reported as unreadable and exits non-zero.

---

## Design quality rubric

Use [`design-quality-rubric.md`](design-quality-rubric.md) for the design-quality score.

The design-quality rubric answers "how strong is the design artifact itself?"

For generated concepts, UI specs, typography systems, and handoff — the read and the target are printed only when a score was asked for or the response is judged; when they are absent, these items apply to the derivation behind the response:

- [ ] A printed score is derived from a visible dimension read, not asserted. (Identical scores across unrelated artifacts are **not** evidence of retrieval — this scale returns the same band to a design and a deliberately worse twin, 12 paired scorings of 12, and concentrates by output mode. See `design-quality-rubric.md`.)
- [ ] A printed `Quality target` line names the dimension blocking the next level and what would lift it, rather than printing a bare number — or, at the top band, says that nothing blocks it instead of manufacturing a blocker.
- [ ] Every dimension whose failed boundary question the available input could answer was lifted and re-derived; every dimension left where it is has its missing input named. A band is reported at whatever the artifact states, including a low one.
- [ ] The output does not average away a serious flaw such as missing states, weak accessibility behavior, or platform flattening.
- [ ] A printed dimension read spans more than one band, or the response says what made every dimension agree.

For reviews, only when a score was asked for or the response is judged; a review carries no score otherwise:

- [ ] The score includes both a current score and a projected score, each on its own `Current:` / `Projected:` line. Both are medians of the assessable dimensions, lowered by the critical-dimension step and clamped by caps (rubric, Final scoring method) — the current over the bands as found, the projected over the bands once the fixes land — and plain numbers, not "up to"; any higher post-visual-pass figure is confined to a `Ceiling note`.
- [ ] The projection is conditional (IF fixes land AND assumptions hold) and capped at 4/5 unless resilience is named; a P0/Fail is not projected up to a number.
- [ ] Text-only reviews label both scores as structural/provisional, and visual dimensions are not projected upward.
- [ ] The per-dimension table carries all nine rubric dimensions, distinctiveness included, and the score rationale references the concrete ones it moves.

### Rubric eval fixtures

The score-calibrated fixtures live in `../examples/evals/`.

Use them as regression targets for human review or future LLM-as-judge scoring:

- `rubric-score-1.json` — should fail or score 1/5 because of hard guardrail violations
- `rubric-score-2.json` — should score 2/5 because it is structurally weak and not buildable
- `rubric-score-3.json` — should score 3/5 because it is acceptable but lacks stronger mechanisms
- `rubric-score-4.json` — should score 4/5 because it is shippable with validation notes
- `rubric-score-5.json` — should score 5/5 because it is resilient across states, accessibility, platform behavior, and handoff

The upgrade example in [`../examples/rubric-before-after.md`](../examples/rubric-before-after.md) shows how a 2/5 response becomes a 4/5 response.

### LLM-as-judge runner

Use [`llm-judge-runner.md`](llm-judge-runner.md) and `../scripts/run_rubric_judge.py` to run semantic rubric calibration.

Minimum local check:

```bash
python3 scripts/run_rubric_judge.py --dry-run
```

Export judge requests:

```bash
python3 scripts/run_rubric_judge.py --export-jsonl tmp/rubric-judge-requests.jsonl
```

Validate judge outputs:

```bash
python3 scripts/run_rubric_judge.py --judge-output tmp/rubric-judge-results.jsonl
```

Run through an external judge agent without provider keys in the repository:

```bash
python3 scripts/run_rubric_judge.py \
  --judge-command "./scripts/local_judge_agent.sh" \
  --judge-command-output tmp/rubric-judge-results.jsonl
```

The external command is LLM-agnostic: it receives versioned request JSONL on stdin and returns judge-output JSONL on stdout. It may use any model or internal gateway as long as it preserves the output contract.

Self-test the runner without an LLM:

```bash
python3 scripts/run_rubric_judge.py --export-expected-output tmp/rubric-judge-expected.jsonl --judge-output tmp/rubric-judge-expected.jsonl
```

Self-test the external command adapter without an LLM:

```bash
python3 scripts/run_rubric_judge.py --judge-command "python3 scripts/rubric_judge_oracle_agent.py"
```

---

## Calibration material

Synthetic, and used only by the rubric and by judged mode. None of it is loaded for an ordinary request.

- [`golden-examples.md`](golden-examples.md) and [`../examples/golden/`](../examples/golden/): compact taste and domain calibration targets
- [`synthetic-case-studies.md`](synthetic-case-studies.md) and [`../examples/case-studies/`](../examples/case-studies/): bad-to-good response calibration without real products or screenshots
- [`visual-review-fixtures.md`](visual-review-fixtures.md) and [`../examples/visual-review-fixtures/`](../examples/visual-review-fixtures/): Figma-like text fixtures for review evidence discipline
- [`domain-packs/index.md`](domain-packs/index.md): domain playbooks for fintech, health, SaaS, marketplace, social and education
- [`benchmark-report-format.md`](benchmark-report-format.md) and [`../examples/benchmark-report.md`](../examples/benchmark-report.md): benchmark reporting for 3-5 references
- [`rendered-output-qa.md`](rendered-output-qa.md) and [`../examples/rendered-output-qa/`](../examples/rendered-output-qa/): optional QA report structure for a built artifact

## Maintenance

- A change to what the model reads at runtime is judged by the gate, not by this repository's validators.
- When a guardrail is added to [`guardrails.md`](guardrails.md), check that `SKILL.md` section 2 still says the same thing in fewer words.
- `../examples/evals/generation-prompts.json` is the second half of the gate's `extended` brief set. It is a list of questions, not of answers.
