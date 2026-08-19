# Evaluation Criteria

This document defines concrete evaluation criteria for the `mobile-design-skill` output by mode. It enables automated and human-judged quality checks, regression testing, and consistent feedback across iterations.

Use this document when:

- reviewing a skill response before shipping
- building evals for LLM-as-judge scoring
- regression-testing prompt or skill changes
- assessing whether a mode output meets the contract

Every mode is evaluated across three layers:

1. **Structural validation** — mechanical checks that can be automated via regex, parsing, or validators.
2. **Content validation** — semantic checks that require a human or LLM-as-judge.
3. **Fail conditions** — hard stops that invalidate the response regardless of other scores.

---

## Shared structural validation (all modes)

Every response must satisfy the following, regardless of mode:

- [ ] Starts with `Mode: [exact mode name]`
- [ ] Contains `Platform scope: [iOS | Android | Cross-platform | Assumed: <description>]`
- [ ] Contains `Assumptions:` section with at least 2 items
- [ ] Contains the mode-specific accessibility section with at least 3 concrete items:
  - Mode A / E: `## Accessibility considerations`
  - Mode B: `## Accessibility and usability risks`
  - Mode C: `## Accessibility requirements`
  - Mode D: `## Findings` containing at least one finding with `Lens: Accessibility`
  - Mode F: `## Accessibility and usability considerations`
- [ ] Contains a `## Next actions` section with at least 2 specific, testable items
- [ ] Does not contain the compliance-claim tokens: `compliant`, `WCAG-compliant`, `passes accessibility` unless the user provided verified evidence
- [ ] Does not contain fabricated quantitative research claims (regex: `\d+%`, `users completed`, `testing proved`, `research shows`) unless sourced
- [ ] If the response asks clarifying questions, it contains at most 3 questions and explains why the answers block reliable output
- [ ] If the request used `--judge` and produced a substantive artifact, the final response includes a compact `Judge summary`

## Shared fail conditions (all modes)

Any of the following invalidates the response:

- Missing the mode-specific accessibility section
- `Next actions` are generic (examples: "test it", "validate", "iterate", "improve")
- Hallucinated platform rule (example: "iOS requires X" without source or "recommendation" framing)
- Blended iOS and Android guidance where conventions materially differ
- Aesthetic-only recommendation without usability, readability, accessibility, or implementation justification
- Visual polish, brand expression, motion, or illustration used to hide weak hierarchy, missing states, or inaccessible interaction
- Compliance claim echoed from user input without "cannot independently verify" qualifier
- Inspiration source used as evidence for usability, accessibility, platform correctness, compliance, or user preference
- Template-complete but decision-empty output: required sections exist, but recommendations have no choices, rejected alternatives, context-specific reasons, or buildable mechanisms
- Non-blocking clarification: response asks questions instead of producing a useful artifact when safe assumptions would have worked
- More than three clarifying questions in one response
- `--judge` response asks the user to run `scripts/run_rubric_judge.py` manually instead of using the interactive judged-mode workflow

## Clarification validation

Use [`clarification-policy.md`](clarification-policy.md) when a response asks questions or proceeds with underspecified input.

- [ ] Blocking questions are tied to platform, primary task, safety/accessibility, compliance, visual evidence, or implementation.
- [ ] Non-blocking gaps are handled through labeled assumptions, unresolved assumptions, open questions, or next actions.
- [ ] A clarification-only response still includes Mode, Platform scope, Assumptions, Clarifying questions, Why this blocks, optional Fast path, and Next actions.
- [ ] The response does not ask cosmetic/style questions before structural blockers.
- [ ] The response offers a fast path when a provisional draft would still be useful.

## Known weakness validation

Use [`weaknesses.md`](weaknesses.md) as the regression map for content review.

For every evaluated response:

- [ ] The likely weakness pattern is prevented by the response, not merely absent from wording.
- [ ] The output is specific to the user's product, task, audience, platform, or constraints.
- [ ] Major decisions include a chosen option, a rejected alternative where relevant, and a concrete reason.
- [ ] Evidence boundaries are clear: facts, assumptions, recommendations, and unverifiable items are separated where risk exists.
- [ ] The response is buildable enough for the requested mode: states, behaviors, values, tokens, QA checks, or validation focus are present as appropriate.
- [ ] The 1-5 design-quality rubric from [`design-quality-rubric.md`](design-quality-rubric.md) is applied when the response proposes, specifies, reviews, or rationalizes a design artifact.
- [ ] Relevant synthetic case studies, visual-review fixtures, domain packs, benchmark report format, or rendered-output QA guidance are used for calibration when the task matches those surfaces.

Hard-fail the response if it matches a P0 or P1 weakness in `docs/weaknesses.md`.

---

## Mode A: Generate mobile screen concept

### Structural validation
- [ ] Response begins with `Mode: Generate mobile screen concept`
- [ ] Contains sections: `Screen goal`, `Primary user task`, `Information hierarchy`, `Recommended layout structure`, `Suggested components`, `Empty / loading / error states`, `Design quality calibration`
- [ ] Contains `Alternatives considered` with at least one rejected alternative and reason
- [ ] Information hierarchy is ordered (numbered or bulleted with priority)
- [ ] All three edge states (empty, loading, error) are explicitly addressed
- [ ] If platform-specific notes are included, they are split per platform (not merged)

### Content validation
- [ ] Primary user task is singular and explicit (not a list of three tasks)
- [ ] Hierarchy is task-driven (by user need), not visual-first (by prominence)
- [ ] Suggested components are buildable on the named platform (native or common UI kit)
- [ ] Rationale connects each major choice to user goal, accessibility, or implementation
- [ ] Design quality calibration defines attention path, composition/spacing, typography, color/state, interaction polish, and production checks where relevant
- [ ] Accessibility considerations are specific to the screen (not generic "use labels")
- [ ] No invented research findings; no quantitative claims without source

### Fail conditions
- Primary user task is ambiguous or absent
- Empty/loading/error states missing
- Hallucinated component (named pattern that does not exist on the target platform)
- Generic accessibility section copied across responses

---

## Mode B: Design mobile user flow

### Structural validation
- [ ] Response begins with `Mode: Design mobile user flow`
- [ ] Contains sections: `Flow goal`, `Entry points`, `Ordered steps/screens`, `Decision points`, `Back-navigation logic`, `Failure and recovery paths`
- [ ] Ordered steps are numbered or sequenced
- [ ] Decision points are explicit (not implied in step descriptions)
- [ ] At least one failure path is defined

### Content validation
- [ ] Success path is end-to-end (entry → success state)
- [ ] Back-navigation behavior is defined for every step, not just the last one
- [ ] Recovery paths cover at least one of: network failure, user abandonment, input validation error
- [ ] No desktop-specific assumptions (example: no hover states, no keyboard-first flows unless explicit)
- [ ] Each step scopes what the user sees, what they can do, and what happens next
- [ ] Simplification opportunities are flagged separately from the flow

### Fail conditions
- Back-navigation logic missing or vague ("user goes back")
- No recovery path defined for the primary failure mode
- Flow assumes desktop conventions (hover-to-reveal, right-click, long-form keyboard entry)
- Invented business rules not flagged as assumptions

---

## Mode C: Create platform-aware UI spec

### Structural validation
- [ ] Response begins with `Mode: Create platform-aware UI spec`
- [ ] Contains sections: `Structural zones`, `Components by section`, `State definitions`, `Behavior rules`, `Spacing and layout notes`, `Typography rules`, `Accessibility requirements`, `Design quality requirements`, `Key decision tradeoffs`
- [ ] For cross-platform specs: contains `iOS-specific implementation notes` AND `Android-specific implementation notes` OR an explicit statement that conventions align
- [ ] State definitions cover at minimum: default, loading, empty, error
- [ ] Spacing values are concrete (example: "16 dp" or "space-4 token"), not relative ("more spacing")

### Content validation
- [ ] An engineer can begin implementation from this spec without asking for missing structural information
- [ ] Component names match the named design system or a reasonable default (Material, iOS native, custom)
- [ ] Behaviors are described as rules ("If X, then Y"), not narrative
- [ ] Typography rules specify role-to-size mapping (not just a list of sizes)
- [ ] Accessibility requirements include specific targets: touch size, label behavior, focus order, contrast
- [ ] Design quality requirements include concrete attention path, composition/spacing, typography, color/state, interaction polish, and production checks
- [ ] Platform-specific notes reflect actual platform behavior, not stereotypes

### Fail conditions
- States missing or only "default" defined
- Spacing/typography vague ("appropriate", "modern", "comfortable")
- Cross-platform spec collapses iOS and Android into one without stating conventions align
- Invented component names not tied to any design system or explicit assumption

---

## Mode D: Review screen for usability/accessibility

### Structural validation
- [ ] Response begins with `Mode: Review screen for usability/accessibility`
- [ ] Contains sections: `Quick summary`, `Strengths`, `Findings`, `Design quality score (current → projected)`, `Severity index`, `Unresolved assumptions`
- [ ] Sub-case is classified in the opening (visual / description-only / problem-statement / context-change)
- [ ] Severity uses the Nielsen 0–4 scale per finding
- [ ] At least one strength is identified (not only negatives)

### Content validation
- [ ] Each finding is one causal chain: observation → violated principle → user consequence → change → predicted effect (no issue split from its fix)
- [ ] Every finding names the violated principle (heuristic/law), not "feels off"
- [ ] Every predicted effect names a user outcome, stated directionally with a confidence level and no fabricated percentages
- [ ] Findings are concrete, not aesthetic opinions ("form is too long without grouping" vs "feels cluttered")
- [ ] Both a current and a projected score are present; the projection is conditional (IF fixes land AND assumptions hold) and capped at 4/5 unless resilience is named
- [ ] Unresolved assumptions list what cannot be verified from the provided material
- [ ] For description-only reviews: visual/aesthetic claims are qualified ("cannot verify from description"), and visual dimensions are not projected upward
- [ ] Findings do not assert color, spacing, balance, contrast, or visual weight from text-only input without qualifier
- [ ] For problem-statement reviews: diagnosis is differentiated from assessment
- [ ] If a Bold move is present: trigger met, all fields complete, kept separate from required fixes
- [ ] Compliance language avoided (see shared fail conditions)

### Fail conditions
- Review asserts visual properties (color, contrast, spacing) from text-only input without qualifier
- No strengths section or "no strengths found"
- A finding splits the issue from its fix, or a change is stated without a predicted effect
- Projected score asserted without conditional phrasing (IF fixes land AND assumptions hold), or a P0/Fail projected up to a number
- Bold move offered without its trigger met, or missing required fields (deviation, JTBD job, validation path)
- Compliance claim without verified evidence

---

## Mode E: Create typography and spacing system

### Structural validation
- [ ] Response begins with `Mode: Create typography and spacing system`
- [ ] Contains sections: `Type roles`, `Size hierarchy`, `Weight usage`, `Line-height guidance`, `Spacing scale`, `Density rules`, `Visual rhythm rules`, `Touch-target implications`
- [ ] Type roles are named (not just sizes): Display, Title, Body, Caption, Label, etc.
- [ ] Size hierarchy includes concrete sizes (`pt` / `sp` / token-equivalent)
- [ ] Line-height guidance includes concrete ratios or values
- [ ] Spacing scale is systematic (powers of 2, 4-based, or named token scale)
- [ ] Touch-target minimum is stated (44 pt iOS / 48 dp Android or equivalent)

### Content validation
- [ ] Roles map to use cases, not just to components
- [ ] Line-height values are specified per role, not one-size-fits-all
- [ ] Density rules explain when to use tighter vs looser spacing based on task
- [ ] Visual rhythm rules explain how spacing, type roles, and grouping should repeat across screens
- [ ] Accessibility considerations include dynamic type / large-text scaling behavior
- [ ] If multilingual support was requested, script-specific adjustments (CJK, Arabic, Devanagari) are called out
- [ ] Examples show roles applied to common screen areas (header, body, form, list)

### Fail conditions
- Type roles are absent, only a size list
- Touch-target minimum missing
- Dynamic type / scaling behavior not addressed
- Multilingual requested but no script-specific notes

---

## Mode F: Prepare design rationale / handoff

### Structural validation
- [ ] Response begins with `Mode: Prepare design rationale / handoff`
- [ ] Contains sections: `Design objective`, `Target users and context`, `Key design decisions`, `Pattern choices and why`, `Design quality rationale`, `Platform alignment`, `States and edge cases`, `Implementation notes`, `Open questions`, `Validation plan or recommended testing focus`
- [ ] Each key decision is separated from its justification
- [ ] Open questions list at least one genuinely open item (not filler)

### Content validation
- [ ] Rationale connects decisions to user goals, context, or constraints, not to aesthetic preference
- [ ] Pattern choices reference official guidance or established convention
- [ ] Design quality rationale connects visual hierarchy, composition, density, brand expression, or motion to the product context with concrete mechanisms
- [ ] Platform alignment is substantive, not "follows platform best practices"
- [ ] Validation plan specifies WHAT to test and HOW (method, metric, or acceptance criterion)
- [ ] Implementation notes address at least one concern engineering actually faces (state management, accessibility semantics, analytics, performance)

### Fail conditions
- Rationale is reverse-engineered from the task with no actual design shown or referenced
- Validation plan is "test with users" without specifics
- Open questions list is empty or synthetic
- Fabricated research findings used as justification

---

## Scoring rubric

For evals, score each response across three dimensions:

| Dimension | Weight | Scoring |
|-----------|--------|---------|
| Structural validation | 30% | Pass rate across the mode's structural checks |
| Content validation | 50% | Count of content checks passing / total |
| Hallucination & safety | 20% | Binary pass/fail on shared fail conditions + mode fail conditions |

A response that fails any hard fail condition receives an overall score of **Fail** regardless of the weighted score.

## Design quality rubric

Use [`design-quality-rubric.md`](design-quality-rubric.md) for the design-quality score.

Structural/content evals answer "does the response satisfy the skill contract?" The design-quality rubric answers "how strong is the design artifact itself?"

For generated concepts, UI specs, typography systems, and handoff:

- [ ] The score is derived from a visible dimension read, not asserted. (Identical scores across unrelated artifacts are **not** evidence of retrieval — this scale returns the same band to a design and a deliberately worse twin, 12 paired scorings of 12, and concentrates by output mode. See `design-quality-rubric.md`.)
- [ ] The `Quality target` line names the dimension blocking the next level and what would lift it, rather than printing a bare number — or, at the top band, says that nothing blocks it instead of manufacturing a blocker.
- [ ] Every dimension whose failed boundary question the available input could answer was lifted and re-derived; every dimension left where it is has its missing input named. A band is reported at whatever the artifact states, including a low one.
- [ ] The output does not average away a serious flaw such as missing states, weak accessibility behavior, or platform flattening.
- [ ] The dimension read spans more than one band, or the response says what made every dimension agree.

For reviews:

- [ ] `Design quality score (current → projected)` includes both a current score and a projected score, each on its own `Current:` / `Projected:` line. Both are flat medians of the assessable dimensions — the current over the bands as found, the projected over the bands once the fixes land — not "up to"; any higher post-visual-pass figure is confined to a `Ceiling note`.
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

## How to run evals

### Automated structural checks

Run:

```bash
python3 scripts/validate_repo.py
```

The repository validator checks required files, relative links, root skill frontmatter, and the committed example outputs in `examples/`. It extracts each `## Example output` fenced block and verifies the mode-specific structural contract, including assumptions, required sections, accessibility sections, concrete numeric values where required, decision tradeoffs, and non-generic next actions.

These checks are intentionally structural. They catch contract drift and missing sections, but they do not replace human or LLM-as-judge content review.

### Human or LLM-as-judge content checks

For content validation:

1. Provide the response alongside the mode-specific criteria from this file.
2. Score each content check as pass / partial / fail.
3. Record the rationale for any non-pass, so the pattern is visible across runs.

### Regression testing with examples

The files in `examples/` are treated as regression targets. The compact golden examples in [`../examples/golden/`](../examples/golden/) are taste and domain calibration targets, not full structural examples.

Synthetic calibration resources:

- [`synthetic-case-studies.md`](synthetic-case-studies.md) and [`../examples/case-studies/`](../examples/case-studies/) — bad-to-good response calibration without real products or screenshots
- [`visual-review-fixtures.md`](visual-review-fixtures.md) and [`../examples/visual-review-fixtures/`](../examples/visual-review-fixtures/) — Figma-like text review fixtures for Mode D evidence discipline
- [`domain-packs/index.md`](domain-packs/index.md) — domain-aware mobile playbooks for fintech, health, SaaS, marketplace, social, and education
- [`benchmark-report-format.md`](benchmark-report-format.md) and [`../examples/benchmark-report.md`](../examples/benchmark-report.md) — benchmark reporting for 3-5 references without copying or evidence overreach
- [`rendered-output-qa.md`](rendered-output-qa.md) and [`../examples/rendered-output-qa/`](../examples/rendered-output-qa/) — optional post-implementation QA report structure

When the skill, `modes.md`, or `templates.md` changes:

1. Re-generate each example with the updated skill.
2. Score the regenerated response against this file.
3. Compare to the committed example; any content regression should block the change.
4. Spot-check the golden examples for domain-specific regressions in premium UI, enterprise SaaS, fintech, health, onboarding, settings, checkout, and tablet list-detail.
5. Spot-check synthetic case studies, visual review fixtures, benchmark reports, and domain packs when changing prompt behavior that affects these surfaces.

---

## Maintenance

- When a new mode or section is added to `modes.md` or `templates.md`, add corresponding checks here.
- When a new guardrail is added to `guardrails.md`, add a matching shared fail condition here.
- Keep structural checks automatable; resist ambiguous criteria in that layer.
- Content checks should describe behavior, not enforce style.

---

## Generation eval — the first check that reads generated text

Everything else in this document, and every check in `scripts/validate_repo.py`, reads markdown a maintainer wrote. `scripts/run_generation_eval.py` asks a model to answer real prompts and holds the answers to **exactly** the contract the committed examples are held to: it imports `check_response()` from `validate_repo.py` rather than reimplementing it, so the corpus rules and the output rules cannot drift apart.

This exists because three acceptance passes during the 1.17.0 release found defects that every structural validator passed over — an instruction that generated token consequences while the slot receiving them still asked for layouts, and a filled-in example in a reference doc that outweighed the prose instruction telling the model to derive its score.

### The split that makes it CI-safe

Generation needs a model. **Scoring does not.** So:

- `--dry-run` lists the prompt pack and validates its shape. Runs anywhere.
- `--replayable-only --generate-command "python3 scripts/generation_oracle_agent.py"` replays committed examples through the scorer. This proves the stdin/stdout adapter, the JSONL parser, and that the scorer accepts output the repository already considers correct. **It proves nothing about a model.**
- `--generate-command "<your agent>"` with a real model behind it is the actual eval, to be run during maintenance. There are no provider keys in this repository. **It has never been run.** Only the `--replayable-only` oracle path has ever executed, and that path proves the adapter, not a model — so no claim in this repository rests on this script having read live generated text.

### Eval-only checks

Three things a committed file cannot be wrong about, but a live run can:

| Check | Catches |
|-------|---------|
| Derived score | `Quality target: N/5` above the median of the dimension scores the response itself prints. Pure arithmetic, no model needed — this is the check that would have caught the asserted-score defect immediately. |
| Provenance | A rejected direction citing a source that is not an entry in the catalog in `docs/inspiration-sources.md`. |
| Prompt expectations | A tablet prompt answered with `Device class: Phone`; a no-fit prompt rounded into a standard mode instead of opening `Mode: outside the standard six`. |

### Prompt pack

`examples/evals/generation-prompts.json` — ten prompts covering all six modes, three domains, the tablet path and the no-fit branch. An entry with a `reference_example` can be replayed by the deterministic oracle; the rest are model-only. Adding a prompt is the cheapest way to turn a bug found in the field into a standing regression check.

```bash
python3 scripts/run_generation_eval.py --dry-run
```

---

## Diversity eval — measuring sameness instead of reading for it

Sameness is the symptom this line of work started from, and it has only ever been assessed by reading outputs by hand. `scripts/run_diversity_eval.py` extracts a **decision vector** from each generated response and reports the spread across a set.

The vector is what a response now exposes machine-readably: the catalog entries it sampled (`from:`), the asset class of its `Signature move`, the score it derived, the dimension it named as the blocker, and the base units and ratios it emitted.

**Why vectors and not prose.** A pairwise 5-gram similarity over the calibration bodies was specified once during 1.17.0 and measured at a median of **0.0** — those blocks describe different domains in different words, so word-level overlap cannot see structural sameness. A small structured vector can.

### What is asserted and what is only reported

| Measure | Threshold | Where the number comes from |
|---------|-----------|------------------------------|
| `score_concentration` | ≤ 0.75 | 4 of 4 runs scored 4/5 in the 1.17.0 pass |
| `provenance_concentration` | ≤ 0.50 | 7 distinct catalog entries across 4 domain runs in the 1.18.0 pass |
| `blocker_concentration` | ≤ 0.75 | 2 distinct blocking dimensions across 4 runs in the 1.17.0 pass |
| `asset_class_count` | **none** | 2 of 6 classes across 6 runs in the 1.18.0 pass — the floor to move, not a bar the output clears, so reported only |
| `vector_similarity` | **none** | no baseline exists; reported only |
| `distinct_dimension_bands` | **none** | how many of the five bands the run's dimension reads actually use; the committed corpus used four before this release and two in live acceptance |
| `dimension_min` / `dimension_max` | **none** | which end of the scale is unused |
| `adjacent_pair_share` | **none** | the largest share held by any two adjacent bands — how much of the scale the run never uses, without assuming which end it collapses toward |
| `dimension_range_median` | **none** | within-response spread, independent of spread across responses |
| `flat_vector_share` | **none** | responses that emitted one band nine times |

The six dimension measures are reported and never asserted: no live run has produced a
baseline for any of them, and inventing one is how this repository once shipped a threshold
that failed by construction. What the self-test asserts instead is **separation** — that
`adjacent_pair_share` reads higher, and `distinct_dimension_bands` and
`dimension_range_median` read lower, on a deliberately uniform corpus than on a varied one.
That is a property of the metric rather than a claim about the model, so it needs no
measured bar. `examples/evals/diversity-fixtures.json` carries both corpora, and the uniform
one reproduces the real failure — nine bands drawn from a two-value alphabet, not nine
identical numbers.

Thresholds are asserted only where this repository has measured data. Guessing one produces either a check that passes vacuously forever or a check that forces dishonest output — both have already happened here. Report-only is the default; `--assert` enforces.

Within-prompt divergence is deliberately not measured. There is no sampling-temperature contract, so a threshold on it would be unjustifiable, and a deterministic skill giving one well-grounded answer to one prompt is defensible. What is not defensible is never considering anything else — which is what the provenance and asset-class measures capture.

### Self-test

```bash
python3 scripts/run_diversity_eval.py --self-test
```

`examples/evals/diversity-fixtures.json` holds two corpora: `uniform` reproduces the failure the 1.17.0 acceptance actually found, and `varied` is what a sampled catalog looks like. The self-test asserts the measurements **separate** them, and that the extractor reads score, provenance and blocker out of a real committed response. A self-test that only proves the pipe works is worth nothing — this repository shipped a green oracle over a broken function once already.

## Comparing two arms of output

The rubric above scores one artifact and asks what it states. It does not read whether one design is better than another: measured on six designs against six deliberately worse twins, its nine boundary questions returned the identical band **12 paired scorings out of 12**, while a rubric-free forced choice on the same pairs returned **12 of 12** in the right direction and named the injected mechanism every time.

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

**Null pairs are required, not optional.** A judge handed two documents will find a winner; a run without cosmetic-rewrite pairs cannot see that happening, and the harness refuses to report one. A run whose judge names an agreed winner on more than a third of its null pairs is reported as unreadable and exits non-zero.

