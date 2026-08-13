# Changelog

All notable changes to this project will be documented in this file.

## [1.18.0] - 2026-08-13

Closes the one thing v1.17.0 shipped unresolved: the fixed exploration space (acceptance criterion A3). Verified by six live runs — three of an identical prompt plus health, marketplace and education — scored by an independent gate, which passed all six criteria with no blocking issues.

### Changed
- **Step 5.5 draws two of its three candidate directions from a catalog instead of inventing them.** D1 is the conventional baseline implied by `docs/patterns-catalog.md` and the domain pack; D2 is a named compositional school and D3 a named point-of-view product, both from the 13 entries in `docs/inspiration-sources.md`. Selection is a rule rather than a preference: discard the entries each `Do NOT use for` line disqualifies for this domain, audience and use context, then from the survivors take the entry whose token consequences differ **most** from the baseline — not the first that fits.

  The diagnosis behind the change: v1.17.0 told the model to use the catalog "for the vocabulary", which nothing required it to do, so it generated three candidates from its own prior. **A free-generated candidate set is unimodal.** Four runs of one prompt produced the same two rejects and one owned asset under three names. Two rounds of instruction text failed to move it; making the step a retrieval worked on the first pass.
- **Every direction carries `from:` provenance into the output, including the committed one.** A bypassed catalog is now visible in the response rather than hidden in the reasoning, and labelling only the rejects would leave the third candidate slot unverifiable.
- **The asset-class rule now argues against the surface, not against the golden.** The committed direction's owned asset still may not share an asset class with the nearest golden's, but the response must name the class it chose and say why at least two of the other five fit this surface worse. Picking whichever class the golden did not use is how a six-class palette collapses into two. The rule also states the real test: three answers reaching for the same notch-on-a-track under three token names is one retrieved asset wearing three labels — the objects must differ, not the names.
- `docs/inspiration-sources.md` is a **required load** for step 5.5 rather than an optional vocabulary reference, and states the sampling contract in the file the step actually loads. It also now defines the six asset classes.

### Added
- `validate_direction_provenance()` parses the catalog entry names out of `docs/inspiration-sources.md` rather than hard-coding them, so adding a school or a point-of-view product automatically widens what provenance is accepted, and requires the committed examples to cite real entries. Verified by injection in three directions: provenance stripped, provenance naming something outside the catalog, and the catalog itself gutted.
- `Direction:` and `Dimension read:` slots in Templates A/C/F, both enforced, so the committed direction's provenance and the score's derivation are auditable from the response.

### Acceptance
- **The option set moves with the domain.** The four different-domain runs cite disjoint catalog sets — 7 distinct entries out of 13 — and the disqualification filter visibly does the work rather than decorating: a streak mechanic discarded for a medication screen because "a streak turns a missed dose into a broken achievement", an expressive direction discarded for a marketplace because "its own `Do NOT use for` line excludes any screen whose hierarchy must stay unambiguous under stress".
- The v1.17.0 layout-structure meter is absent from all six runs, and outputs now argue their asset class explicitly.
- No quality regression: no expressive direction was committed anywhere, and every run kept a full accessibility section, a full state set, and an honestly derived score.

### Known limits
- Two runs of the *identical* budgeting prompt converged on the same catalog entry with near-identical token sets. The third drew a different entry from the same prompt, and the cross-domain spread rules out a frozen set, so this is not the v1.17.0 failure recurring — but within-prompt divergence remains unmeasured and is the metric this repo's own planning called premature for lack of a sampling-temperature contract.
- Across the runs sampled, only two of the six asset classes appeared. Colour, motion signature and illustration remain unrepresented in practice.
- Dimension reads still cluster on 3 and 4, so a derived median lands on 4 more often than a five-point scale implies. The fix is upstream in the rubric's willingness to score 2 or 5, not in the median rule.

## [1.17.0] - 2026-08-13

Theme: **the ceiling comes off.** The structural work landed and is verified by live acceptance; cross-run design variance is **not** achieved and is tracked for 1.18.0 — see *Known limits* below before reading the diversity items as solved. A six-dimension audit with an adversarial verification pass produced 38 surviving findings; the plan of record, the causes, and the explicit non-goals are recorded in [`docs/proposals/quality-and-diversity-upgrade.md`](docs/proposals/quality-and-diversity-upgrade.md).

### Fixed
- **The v1.16.0 Mode D contract never reached `SKILL.md`.** The causal `Findings` block, the `current → projected` score and the `Bold move` block shipped into `skill/modes.md`, `skill/templates.md`, `docs/self-review.md`, `docs/evals.md` and `scripts/validate_repo.py` — but `SKILL.md`, the only always-loaded file, kept the pre-1.16 bucket shape (`Usability issues` / `Accessibility issues` / `Severity or priority` / `Recommended fixes`). A model drafted the old shape from the entrypoint, then the mandatory self-review failed it and forced a blind rewrite toward a target the entrypoint never described. This was the **second consecutive release in which the entrypoint was the file the feature forgot**; `validate_mode_parity()` now makes that class of drift a CI failure, and it caught a second, unnoticed divergence in Mode C on its first run.
- `docs/self-review.md` and `docs/workflow.md` held stale third and fourth copies of the Mode D score rule. The self-review prompt now carries the flat-median contract; the workflow bullet became a pointer.
- `docs/design-quality.md` declared a 200–500 ms motion "personality band" while `docs/quality-bars.md` capped full-screen navigation at 400 ms, so a motion signature had no legal room.
- `validate_synthetic_case_studies()` required the literal string `4/5` in every case study — a validator that made "every case study is 4/5" a CI rule. Relaxed to any `[1-5]/5`.

### Added
- **Device class as a second scope axis** (phone / tablet / foldable / adaptive), with a 20-signal trigger list, a `Device class:` line in the output contract and all six templates, a fourth Platform-policy branch, a conditional `## Adaptive behavior` block, and a new `docs/adaptive-layout.md` covering width classes, canonical layouts and their collapse rules, navigation by width, multitasking, and additive input. `docs/quality-bars.md` gains `## Large-screen and adaptive bars` (600/840 dp classes, reading column 640–720 pt, list pane 320–400 pt, rail 80 dp, sidebar 240–360 dp, margins, column counts). Answers the standing question of whether the skill can design tablet apps: before this release, only as a five-row table that nothing triggered.
- **Step 5.5 "Set the design direction"** for Modes 1/3/5: three candidate directions, each a thesis plus five token consequences (base unit and ratio, type role split, colour-construction rule, one composition move, motion signature), ranked and reduced to one, with the two rejects populating `Alternatives considered` or `Key decision tradeoffs`. Internal, perceptual-only, and required to differ in at least two token fields.
- **Ninth rubric dimension, `Distinctiveness and owned assets`**, with an `n/v` marker excluded from the median, a `3 → 4 (inert cap)` ladder rung stating the cap's own exit, and a `Signature move:` slot in Templates A/C/F.
- **A `Mode: outside the standard six` branch** so paywall architecture, whole-app IA, notification strategy and design-system governance stop being rounded into a screen-concept template. Anti-pattern 9 shows the case both ways.
- **Guardrail 16**: do not describe a source you cannot open (Mobbin, Page Flows, UI Sources and Pttrns are behind sign-in or paywalls and are lookups for the user, never narrated), and do not state a version-bound default as timeless.
- Token consequences for the four compositional schools and the nine point-of-view products in `docs/inspiration-sources.md`, which were previously a reading list.
- `### Signature transition` in `docs/quality-bars.md`: one signature per product, top of its own band, 400 ms ceiling, never applied to tap feedback.
- An adversarial rubric fixture (`examples/evals/rubric-score-2-adversarial.json`) whose dimensions median at 3 while a cap drags it to 2/5 — the first fixture that separates a judge applying the rubric from a judge reporting an average.

### Changed
- **The quality ceiling is no longer nailed shut at 4/5.** `skill/templates.md` pre-printed `Quality target: [4/5 by default unless context blocks it]`, and 21 of 23 values in the calibration corpus were 4/5. The score is now derived rather than prescribed: a visible per-dimension read, its median, then caps. The target line names the dimension blocking the next level and what would lift it, and the rubric states that 4/5 is the usual outcome of a good draft — not a number to aim at, and not a ceiling.
- **The inspiration gate is no longer narrower than the layer it guards.** `SKILL.md` listed four trigger signals while `docs/inspiration-sources.md` declared nine — so "make it feel premium" never reached the layer whose own trigger list names that phrase. All nine now appear at the gate, kept in sync by `validate_inspiration_gate_parity()`.
- `Alternatives considered` (Mode 1) and `Key decision tradeoffs` (Mode 3) added to `SKILL.md` and `skill/modes.md`: `MODE_REQUIREMENTS` and the committed examples already demanded these sections, so the instructions had been requiring less than the validator enforced.
- Sections are a maximum, not a minimum: only `Mode:`, `Platform scope:`, `Device class:`, `Assumptions:` and `Next actions:` are unconditional; anything else is omitted — never stubbed — when the input does not support a decision.
- Phone-first is now stated as a reversible assumption rather than a closed statement in `skill/skill.md`, `docs/clarification-policy.md` and `examples/generate-screen.md`.
- All six golden examples carry a distinct owned asset expressed as a token with named repeat locations. The corpus score distribution moved from 21/23 at 4/5 (91 %) to four distinct scores with a 74 % maximum share.
- CI steps that ran the deterministic oracle are renamed to say they are self-tests and not quality checks, with a new section in `docs/llm-judge-runner.md` stating that no model runs in CI and a `SKILL.md` change that degrades live output cannot fail those steps.

### Known limits (verified by live acceptance, not by validators)

Three acceptance passes were run against the released instructions — five and then twice four live generations, scored by an independent gate. What the passes established:

- **Verified working**: the tablet layer end to end (`Device class: Tablet`, breakpoints, a named canonical layout, navigation per width, and an explicit refusal to shrink touch targets because a keyboard is attached); the `Mode: outside the standard six` branch on a paywall-architecture request; no claimed consultation of auth-walled sources; no accessibility-compliance claims; direction-level alternatives carrying token consequences; and a score derived from a visible per-dimension read whose median matches the stated number, with the blocking dimension varying across runs.
- **Not achieved: cross-run design variance.** Four runs of the same prompt generate the same candidate pair (a category/envelope grid and a transaction/ledger feed) and commit to the same winner. Step 5.5's "differ in at least two token fields" is a within-run constraint; nothing in the skill widens the option set across invocations. The owned assets also converge — `rail.pace`, `meter.runway` and `meter.remaining` are one linear-track-with-pace-tick under three names, which means the Distinctiveness dimension can be satisfied by renaming a retrieved asset. **The machinery this release adds fires; the variance it was meant to produce does not yet follow.** Tracked for 1.18.0.
- **Secondary**: across 36 dimension scores in four runs, every value was a 3 or a 4. With that compressed range the median cannot land anywhere but 4, so the derived score is near-structurally locked even though the derivation is now real and visible. The fix is upstream in the rubric's willingness to score 2 or 5, not in the median rule.

Two defects introduced earlier in this same release were found by acceptance and fixed before tagging: the slot receiving the rejected directions still asked for "layout approaches" while step 5.5 produced token consequences, and a filled-in illustrative `Quality target` line in two reference docs was being reproduced near-verbatim by three of four runs — a pre-filled example outweighs a prose instruction to derive.

### Validation
- Eight new cross-file contract checks in `scripts/validate_repo.py`, each verified by injection: mode parity, inspiration-gate parity, motion-band consistency, projected-score shape, skill-entrypoint contract, unreadable-source honesty, calibration-corpus diversity, and the `Device class:` / `## Adaptive behavior` pairing.
- Two checks specified in the proposal were **corrected after measurement rather than implemented as written**, and the reasons are recorded in the validator source: a pairwise 5-gram Jaccard threshold of 0.15 (measured median in the real corpus is 0.0, so it would pass vacuously forever) and a positive next-action test requiring a digit or proper noun (it failed thirteen specific, well-written actions and would reward inserting a number).
- The rubric eval pack now asserts `expected_score ≤ floor(median)` always, `== floor(median)` when no cap is recorded, and that at least two fixtures carry a dimension spread ≥ 2. Previous spreads were 0, 1, 1, 0, 0 — the median rule had never been exercised.

## [1.16.0] - 2026-05-29

### Added
- Mode D review: a causal **Findings** block (observation → violated principle → user consequence → change → predicted effect → Nielsen 0–4 severity → dimension moved), replacing the split issue/fix sections.
- Mode D review: a **current → projected** design-quality score (conditional, capped at 4/5, doubly-provisional for text-only D2/D3) with a per-dimension before/after table.
- Mode D review: an optional **Bold move** block for product-contradicting recommendations, gated by trigger and required fields (deviation, JTBD job, upside, risk, validation path, score impact, conviction).
- Distinctiveness levers and the "inert-screen test" in `docs/design-quality.md`, with a matching rubric cap so a competent-but-forgettable screen scores 3/5 with an upside note rather than a quiet 4/5.
- Heuristics: Cognitive Load Theory (Sweller), form-design principles (Wroblewski), and the Nielsen 0–4 severity scale in `docs/heuristics.md`.
- Inspiration: a derivation layer (production-reasoning sources, editorial/craft schools, and point-of-view products beyond Apple/Google), a generative direction method (JTBD → How-Might-We → Crazy Eights → de Bono → SCAMPER → translate-to-mechanism), and a reference→mechanism discipline in `docs/inspiration-sources.md`.
- Anti-pattern 8 (bold move vs aesthetic laundering); creative-range references and ideation-method links in `docs/sources.md`; NN/g benchmark citations in `docs/visual-benchmark-playbooks.md`.
- Proposal record at `docs/proposals/review-mode-upgrade.md`.

### Changed
- Mode D output contract updated across `skill/templates.md`, `skill/skill.md`, `skill/modes.md`, `docs/design-quality-rubric.md`, `docs/self-review.md`, `docs/evals.md`, `docs/workflow.md`, and `scripts/validate_repo.py`.
- Guardrail #4 carve-out: a product-contradicting recommendation is not aesthetic laundering when justified by a named usability/accessibility/hierarchy mechanism and surfaced in the Bold move block with its tradeoff and validation path.
- Regenerated Mode D calibration to the new format: `examples/review-screen.md`, `examples/golden/settings.md`, all `examples/visual-review-fixtures/`, and `examples/case-studies/social-privacy-settings.md`.

### Fixed (post senior-review hardening)
- Projected score is now a **flat median of the assessable dimensions**, not an inflated "up to N/5"; any higher post-visual-pass figure is confined to a `Ceiling note`. Corrected the arithmetic in all nine Mode D examples (five drop honestly from 4/5 to 3/5). A `must_not_contain` validator guard blocks the "up to" phrasing from returning.
- Reconciled the **Bold move trigger** with its examples: it requires current ≥3/5 AND no unresolved severity-3/4 finding. `examples/review-screen.md` (2/5) now correctly omits the Bold move; `examples/golden/settings.md` was made internally consistent (confirmed delete) so its Bold move is legitimately gated.
- Closed the **D2 visual-overclaim backdoor**: visual dimensions stay `n/v` and are never projected upward from a text-only review (fixed `settings.md` Color/state and the `review-screen.md` Composition row).
- Added a **severity crosswalk** (Nielsen 0–4 ↔ High/Med/Low ↔ P0–P3 ↔ quality-score caps) to `docs/heuristics.md`.
- Fixed stale Mode D references in `docs/evals.md` (accessibility section, projected-line label) and converted the Anti-pattern 4 "Good" fragment to the Findings format. Added a compressed-finding example and an inert-screen-test finding to `examples/golden/settings.md`.

## [1.15.0] - 2026-04-25

### Added
- Synthetic case-study calibration pack at `docs/synthetic-case-studies.md` and `examples/case-studies/`, covering 12 bad-to-good mobile design response cases without real products or screenshots.
- Text-only visual review fixture pack at `docs/visual-review-fixtures.md` and `examples/visual-review-fixtures/`, covering six Figma-like review scenarios with expected critique and prohibited overclaims.
- Benchmark report format at `docs/benchmark-report-format.md` plus `examples/benchmark-report.md` for turning 3-5 references into borrow / do-not-copy / token-component-state guidance.
- Domain packs under `docs/domain-packs/` for fintech, health, SaaS, marketplace, social, and education.
- Optional rendered-output QA workflow at `docs/rendered-output-qa.md` with report schema and sample report under `examples/rendered-output-qa/`.
- Machine-readable metadata for synthetic case studies, domain packs, visual review fixtures, benchmark reports, and rendered-output QA.

### Changed
- `SKILL.md`, the Claude Code wrapper, `skill/skill.md`, `skill/usage.md`, README, `docs/workflow.md`, `docs/evals.md`, and `docs/design-quality-rubric.md` now surface the synthetic calibration and optional QA layers.
- `scripts/validate_repo.py` now validates the new synthetic case studies, domain packs, visual review fixtures, benchmark report format, rendered-output QA schema/sample, and required references.

## [1.14.0] - 2026-04-25

### Added
- External judge command adapter in `scripts/run_rubric_judge.py` via `--judge-command`, allowing a separate agent process to receive judge requests on stdin and return judge-output JSONL on stdout.
- Interactive judged mode via `/mobile-design-skill --judge`, allowing the skill to draft, run an independent rubric judge pass in the same session when available, revise if needed, and return a compact `Judge summary`.
- Companion Claude Code custom agent at `.claude/agents/mobile-design-judge.md` for independent judged-mode scoring.
- Judged mode reference at `docs/judged-mode.md`, covering orchestration, judge prompt contract, fallback behavior, and final response shape.
- `--judge-command-output` and `--judge-command-timeout` options for saving agent output and bounding live semantic judge runs without adding provider keys to the repository.
- Deterministic oracle agent at `scripts/rubric_judge_oracle_agent.py` for CI-safe external command adapter self-tests.
- Versioned request schema marker `rubric-judge-request/v1` so external judge agents can stay stable across any LLM backend.
- Visual benchmark playbooks at `docs/visual-benchmark-playbooks.md` for Mobbin, Page Flows, Apple Design Awards, and Awwwards, with explicit inspiration-vs-evidence boundaries.
- Golden example calibration pack under `examples/golden/` for premium UI, enterprise SaaS, fintech, health, onboarding, settings, and checkout.
- Golden example index at `docs/golden-examples.md` for taste calibration and review expectations.
- Release validation command at `scripts/validate_release.py`, covering version/tag sanity, repository validation, judge dry-run, parser self-test, and external oracle self-test.
- Manual GitHub Actions release gate at `.github/workflows/release-validate.yml`.
- Release automation reference at `docs/release-automation.md`.

### Changed
- `docs/llm-judge-runner.md`, `docs/evals.md`, README, and metadata now document the LLM-agnostic external-agent judge workflow as the preferred open-source path.
- `SKILL.md`, the Claude Code wrapper, `skill/skill.md`, `skill/usage.md`, `docs/commands.md`, and `docs/evals.md` now surface `/mobile-design-skill --judge`.
- `SKILL.md`, the Claude Code wrapper, `skill/skill.md`, `skill/usage.md`, README, and metadata now surface visual benchmark playbooks and golden examples as quality calibration resources.
- `scripts/install.sh` now installs, reports, and uninstalls the companion `mobile-design-judge` agent alongside the skill.
- `scripts/validate_repo.py` now validates the external judge command contract, visual benchmark playbooks, golden examples, and release automation alongside JSONL export and output validation.
- GitHub Actions now self-tests the external judge command adapter without requiring model credentials.

## [1.13.1] - 2026-04-25

### Added
- Documentation hygiene validation for Markdown trailing whitespace and unexpected duplicate headings in `scripts/validate_repo.py`.

### Changed
- Canonical URL appendices in `docs/sources.md`, `docs/design-quality.md`, and `docs/inspiration-sources.md` now use normal Markdown links instead of hard-break URL formatting.
- Reference-pack documentation in `README.md`, `SKILL.md`, the Claude Code wrapper, and `skill/usage.md` now surfaces the full supporting docs set consistently.
- `docs/github-publishing.md` is now part of the required repository structure validation.

## [1.13.0] - 2026-04-25

### Added
- Clarification policy at `docs/clarification-policy.md`, defining when the skill should ask blocking questions vs proceed with labeled assumptions.
- Clarification examples at `examples/clarification-policy.md`, covering blocking visual review, non-blocking concept generation, and policy-sensitive healthcare specs.
- Machine-readable `clarification_policy` metadata and response contract fields for max questions, blocking criteria, fast path, and assumptions.

### Changed
- `SKILL.md`, `skill/skill.md`, `docs/workflow.md`, `docs/self-review.md`, `docs/guardrails.md`, `docs/evals.md`, `docs/sources.md`, `skill/modes.md`, `skill/templates.md`, and `skill/usage.md` now apply the ask-vs-assume policy.
- `scripts/validate_repo.py` now requires and validates the clarification policy layer, examples, and required references.
- `README.md`, the Claude Code wrapper, and `docs/commands.md` now surface the clarification behavior and examples.

## [1.12.0] - 2026-04-25

### Added
- Provider-agnostic LLM-as-judge runner at `scripts/run_rubric_judge.py` for exporting rubric judge JSONL requests and validating JSONL judge outputs against expected fixture scores.
- Runner documentation at `docs/llm-judge-runner.md`, including judge output contract, pass criteria, dry-run usage, JSONL export, and self-test flow.
- Machine-readable `llm_judge_runner` metadata and `llm_as_judge_runner` quality flag in `skill/metadata.yaml`.

### Changed
- `docs/evals.md` and `docs/design-quality-rubric.md` now document semantic judge calibration using `scripts/run_rubric_judge.py`.
- `scripts/validate_repo.py` now requires the runner and documentation, verifies the runner contract, and checks that CI/docs/metadata reference it.
- GitHub Actions now runs the judge runner dry-run and oracle-output parser self-test in addition to repository validation.
- `README.md`, `SKILL.md`, and `skill/usage.md` now surface the LLM-as-judge runner as a maintenance and calibration tool.

## [1.11.0] - 2026-04-25

### Added
- Rubric eval fixture pack under `examples/evals/`, covering expected design-quality scores from `1/5` through `5/5` with prompts, response excerpts, dimension scores, caps/hard limits, failed dimensions, rationales, and improvement suggestions.
- Before/after calibration example at `examples/rubric-before-after.md`, showing how a template-complete `2/5` UI spec is upgraded into a buildable `4/5` spec.
- Machine-readable rubric eval pack references under `design_quality_rubric.eval_pack` and `design_quality_rubric_eval_pack` in `skill/metadata.yaml`.

### Changed
- `docs/design-quality-rubric.md` and `docs/evals.md` now reference the fixture pack and explain how to use it for human review or future LLM-as-judge scoring.
- `scripts/validate_repo.py` now validates rubric fixtures as JSON, checks full score coverage `1..5`, verifies dimension-score keys, requires improvement suggestions, and validates the before/after example.
- `README.md`, `SKILL.md`, and `skill/usage.md` now surface the rubric eval pack as a calibration resource.

## [1.10.0] - 2026-04-25

### Added
- 1-5 design-quality scoring layer at `docs/design-quality-rubric.md`, with score levels, dimension scoring, caps/hard limits, final scoring method, improvement ladder, and self-review prompts.
- Machine-readable `design_quality_rubric` metadata and `design_quality_rubric_1_to_5` quality flag in `skill/metadata.yaml`.
- Score/target fields in relevant templates and examples: generated artifacts target 4/5; reviews expose current score with evidence limits.

### Changed
- `SKILL.md`, `skill/skill.md`, `docs/workflow.md`, `docs/design-quality.md`, `docs/sources.md`, `docs/self-review.md`, `docs/evals.md`, `docs/guardrails.md`, `skill/modes.md`, and `skill/templates.md` now apply the rubric when proposing, specifying, reviewing, or rationalizing design artifacts.
- `scripts/validate_repo.py` now requires `docs/design-quality-rubric.md`, verifies the layer is referenced by required surfaces, and checks committed examples for `1-5/5` quality score or target markers.
- `README.md`, the Claude Code wrapper, and `skill/usage.md` now reference `docs/design-quality-rubric.md`; version synchronized to `1.10.0`.

## [1.9.0] - 2026-04-25

### Added
- Known weaknesses and failure-mode prevention layer at `docs/weaknesses.md`, covering generic artifacts, template-complete but decision-empty output, first-idea bias, aesthetic laundering, evidence overreach, platform flattening, context blindness, happy-path-only design, visual overclaim, weak handoff, and overlong process theater.
- Machine-readable `weakness_prevention` metadata and `known_weakness_preflight` quality flag in `skill/metadata.yaml`.
- Anti-pattern calibration for template-complete but decision-empty UI specs in `examples/anti-patterns.md`.

### Changed
- `SKILL.md`, `skill/skill.md`, `docs/workflow.md`, `docs/sources.md`, `docs/self-review.md`, `docs/evals.md`, `docs/guardrails.md`, `skill/modes.md`, and `skill/templates.md` now use the weakness layer as an internal preflight before returning design output.
- `scripts/validate_repo.py` now requires `docs/weaknesses.md`, checks that required weakness patterns are present, and verifies the layer is referenced by the skill, docs, metadata, usage, and README surfaces.
- `README.md`, the Claude Code wrapper, and `skill/usage.md` now reference `docs/weaknesses.md`; version synchronized to `1.9.0`.

## [1.8.0] - 2026-04-25

### Added
- Design-quality calibration layer at `docs/design-quality.md`, grounded in Apple HIG, Material/Android, Fluent, GOV.UK, Baymard, and NN/g visual-design principles.
- New mode sections for design craft and production readiness: `Design quality calibration`, `Design quality requirements`, `Design quality issues`, `Visual rhythm rules`, and `Design quality rationale`.
- Metadata flag `design_quality_calibration` plus machine-readable design-quality dimensions in `skill/metadata.yaml`.

### Changed
- `SKILL.md`, `skill/skill.md`, `docs/workflow.md`, `docs/sources.md`, `docs/self-review.md`, and `docs/guardrails.md` now require visual hierarchy, composition, density, typography craft, color semantics, interaction polish, brand expression, and production-readiness reasoning when a response proposes or packages a design artifact.
- `skill/templates.md`, `skill/modes.md`, `docs/evals.md`, and `scripts/validate_repo.py` now enforce the design-quality sections for relevant modes.
- Golden examples for screen concept, UI spec, review, typography/spacing, and handoff now include concrete design-quality calibration rather than generic visual polish advice.
- `README.md`, the Claude Code wrapper, and `skill/usage.md` now reference `docs/design-quality.md`.

## [1.7.0] - 2026-04-25

### Added
- Inspiration/reference layer at `docs/inspiration-sources.md`, separating production UI references (Mobbin, Page Flows, UI Sources, Pttrns, Screenlane), platform/award references (Apple Design Awards, Material Design blog/case studies, Awwwards), and visual portfolio/moodboard references (Behance, Dribbble, Pinterest, Figma Community).
- Metadata support for non-authoritative inspiration sources via `inspiration_sources` and `inspiration_sources_separated_from_evidence`.
- Self-review prompts that check inspiration sources are separated from UX rationale, platform guidance, accessibility requirements, and compliance language.
- Automated example-response validation in `scripts/validate_repo.py`. The validator now extracts committed `## Example output` blocks and checks mode-specific structural contracts, accessibility sections, concrete values, decision tradeoffs, and non-generic next actions.

### Changed
- `SKILL.md`, `skill/skill.md`, and `docs/workflow.md` now instruct the skill to use inspiration sources only when requested or materially useful, and never as evidence for usability, accessibility, platform correctness, or compliance.
- `docs/sources.md`, `docs/guardrails.md`, and `docs/evals.md` now explicitly classify inspiration as a non-authoritative layer and treat misuse of inspiration as a fail condition.
- `README.md`, the Claude Code wrapper, and `scripts/validate_repo.py` now reference and require `docs/inspiration-sources.md`.
- `examples/generate-screen.md`, `examples/ui-spec.md`, `examples/review-screen.md`, `examples/typography-spacing.md`, and `examples/rationale-handoff.md` were updated to match the current templates and quality bars.
- GitHub Actions and README validation wording now reflect structure, link, and example-output validation.

## [1.6.1] - 2026-04-18

### Added
- Project logo at `assets/logo.svg` (horizontal lockup: mark + wordmark). Logo also mirrored at `.claude/skills/mobile-design-skill/logo.svg` for the Claude Code skill wrapper.
- Centered hero block in `README.md` displays the logo above the version / license badges.

### Changed
- `README.md` repository tree now lists `assets/` and the logo file in the wrapper directory.
- `scripts/bump_version.py` now recognizes the HTML `<img>` form of the version badge and the `Current version: **X.Y.Z**` line, in addition to the markdown-image badge. Previously only the markdown badge was updated; the HTML hero layout introduced in this release would have drifted.
- `scripts/validate_repo.py` requires `assets/logo.svg`.

## [1.6.0] - 2026-04-18

### Added
- Terminal install script at `scripts/install.sh` supporting global and project-scope installation, symlink (default) and self-contained copy methods, uninstall, and status inspection. After cloning the repo, a one-liner `./scripts/install.sh` installs the skill into `~/.claude/skills/mobile-design-skill`.
- Install-script awareness in `scripts/validate_repo.py` (`scripts/install.sh` now in `REQUIRED_FILES`).

### Changed
- `README.md` rewritten end-to-end with a terminal-first installation flow. New sections: Quickstart, What this skill does, Install (Claude Code via script / Claude Code manual / Codex / Claude API Python / Claude API TypeScript / Cursor and other IDEs), Usage, Supported modes, Architecture, Updating, Uninstalling, Customization, Versioning, Contributing. Each integration path has copy-pasteable commands.
- Repository architecture tree in README updated to include all v1.2.0–v1.5.0 additions (self-review, quality-bars, context-defaults, heuristics, patterns-catalog, evals, versioning, bump_version.py, install.sh, anti-patterns).

## [1.5.0] - 2026-04-18

### Added
- Patterns catalog at `docs/patterns-catalog.md` with decision matrices (Use-when / Avoid-when / Trade-offs / Red-flag) for: primary navigation (bottom nav vs drawer vs top tabs), back behavior, presentation overlays (modal vs sheet vs full-screen, bottom sheet variants, popover, action sheet), content display (list vs grid, card vs row, pagination strategies, accordion, carousel), actions (primary action placement, destructive confirmation vs undo, bulk actions, swipe actions), input (inline vs dedicated edit, picker variants, segmented vs dropdown vs tabs, search UX, form field grouping), feedback (toast vs snackbar vs banner vs alert, loading indicators, optimistic UI, error communication), states (empty, skeleton, error), forms (single-screen vs multi-step, validation timing, save strategy, required-field marking), onboarding (walkthrough vs coach marks vs just-in-time), search, notifications, authentication, accessibility, and platform divergence
- Self-review prompt block `Pattern selection` in `docs/self-review.md` — checks that patterns were chosen via matrix, losing alternative cited, and red flags inspected in Mode D reviews
- Metadata flag `pattern_catalog_grounded` on `skill/metadata.yaml`

### Changed
- `docs/workflow.md` Step 7 (design reasoning) now requires consulting `docs/patterns-catalog.md` for pattern-level decisions and forbids inventing novel patterns where established ones apply (Jakob's Law)
- `SKILL.md` and `skill/skill.md` updated to require pattern-catalog grounding in Step 8 / design reasoning
- `README.md` file index and repository tree reference `docs/patterns-catalog.md`
- `scripts/validate_repo.py` requires the new file

## [1.4.0] - 2026-04-18

### Added
- Context-aware defaults catalog at `docs/context-defaults.md` covering audience (older adults, children, power users, general consumer), domain (finance, health, social, e-commerce, enterprise, government, productivity, entertainment), platform (iOS, Android, cross-platform, tablet), and use-context (one-handed, outdoor, in-vehicle, emergency, at-desk), with explicit precedence for resolving conflicts across dimensions
- Heuristics catalog at `docs/heuristics.md` with mobile applications and red-flag violation patterns for Fitts, Hick, Miller, Jakob, Doherty, Tesler, Postel, Zeigarnik, Peak-End, Goal-Gradient, Serial-Position, Choice Overload, Recognition-over-Recall, Aesthetic-Usability, Von Restorff, Nielsen's 10, Gestalt principles, thumb zone, interruption-resilience, and one-screen-at-a-time
- Self-review prompts for context fit and heuristic grounding in `docs/self-review.md`
- Metadata flags `context_aware_defaults` and `heuristic_grounded_reasoning` on `skill/metadata.yaml`

### Changed
- `docs/workflow.md` Step 2 now applies context-aware defaults with documented precedence; Step 7 (design reasoning) now requires citing heuristics by name where they drive decisions
- `SKILL.md` and `skill/skill.md` updated with context-defaults precedence and heuristic-grounded reasoning requirement
- `README.md` file index and repository tree updated to reference `docs/context-defaults.md` and `docs/heuristics.md`
- `scripts/validate_repo.py` updated to require the new files

## [1.3.0] - 2026-04-18

### Added
- Semantic versioning policy at `docs/versioning.md` with bump rules and single-source-of-truth model
- Version bump automation at `scripts/bump_version.py` that synchronizes `skill/metadata.yaml`, both `SKILL.md` frontmatters, the README badge, and inserts a CHANGELOG placeholder
- `version:` field in the root `SKILL.md` frontmatter and `.claude/skills/mobile-design-skill/SKILL.md` frontmatter
- Version badge in `README.md`
- Mandatory self-review pass at `docs/self-review.md`, defining universal and mode-specific prompts the skill runs silently before returning any response
- Concrete numeric quality thresholds at `docs/quality-bars.md` covering typography (sizes, line-height, line length, scaling), touch targets (44pt iOS / 48dp Android minimums and gaps), color and contrast (WCAG 2.2 AA), motion (durations, easing, reduced-motion), spacing (canonical scale), forms, states (loading thresholds), navigation, accessibility specifics, and platform-specific anchors (iOS nav/tab bar, Android app bar / FAB)
- New workflow steps: Step 7 (apply design reasoning with explicit alternatives), Step 8 (check concrete quality bars), Step 9 (mandatory self-review); existing finalize step moved to Step 10
- `Alternatives considered` block in Mode A template
- `Key decision tradeoffs` block in Mode C template
- Alternative/reason pairing required in Mode F `Key design decisions` and `Pattern choices and why` blocks
- Metadata flags `mandatory_self_review`, `concrete_numeric_thresholds`, `design_reasoning_with_alternatives` on `skill/metadata.yaml`

### Changed
- `SKILL.md` and `skill/skill.md` updated with the new workflow steps (Apply design reasoning, Check concrete quality bars, Run mandatory self-review) and references to the new documents
- `docs/workflow.md` Step 6 (review lenses) now cross-references specific numeric bars in `docs/quality-bars.md`
- `README.md` file index and repository tree updated to reference `docs/quality-bars.md` and `docs/self-review.md`
- `scripts/validate_repo.py` updated to require the new files

## [1.2.0] - 2026-04-18

### Added
- Evaluation criteria document at `docs/evals.md` with structural, content, and hard-fail checks for each of the six modes
- Anti-pattern calibration set at `examples/anti-patterns.md` with six worked Bad / Good response pairs for underspecified input, description-only review, compliance echo, aesthetic-only advice, platform hallucination, and flows without recovery paths
- Mode D sub-case classification (D1 visual / D2 description only / D3 problem statement / D4 context change) in `skill/modes.md` with scope rules, validation checks, and fallback behavior per sub-case
- `Sub-case:` field in the Mode D output template (`skill/templates.md`)

### Changed
- `README.md` updated to reference the new `docs/evals.md` and `examples/anti-patterns.md` entries in the file index and repository structure
- `.gitignore` now excludes `.claude/vendor/` to prevent machine-specific absolute-path symlinks from being committed

### Fixed
- Removed duplicated `skill/` and `docs/` trees inside `.claude/skills/mobile-design-skill/` that contained a second level of nested duplicates; the Claude Code wrapper correctly resolves to the root `skill/` and `docs/` via relative paths

## [1.1.0] - 2026-03-26

### Added
- Canonical root `SKILL.md` with Codex-compatible frontmatter
- Claude Code project skill wrapper at `.claude/skills/mobile-design-skill/SKILL.md` for direct `/mobile-design-skill` invocation
- `agents/openai.yaml` UI metadata for Codex skill discovery
- GitHub Actions validation workflow in `.github/workflows/validate.yml`
- Repository validation script in `scripts/validate_repo.py`
- Canonical public URL appendix in `docs/sources.md`, consolidated from the external source curation document used during repo preparation
- GitHub publishing kit in `docs/github-publishing.md`
- Command reference in `docs/commands.md`

### Changed
- Updated `README.md` for GitHub-first publishing, Codex entrypoint guidance, and screenshot-free example-based presentation
- Refined maintenance guidance to keep `SKILL.md`, `skill/skill.md`, and `agents/openai.yaml` aligned

## [1.0.0] - 2026-03-26

### Added
- Initial production-ready release of `mobile-design-skill`
- Six supported modes:
  - Generate mobile screen concept
  - Design mobile user flow
  - Create platform-aware UI spec
  - Review screen for usability/accessibility
  - Create typography and spacing system
  - Prepare design rationale / handoff
- Main skill prompt in `skill/skill.md`
- Metadata file in `skill/metadata.yaml`
- Mode-by-mode requirements in `skill/modes.md`
- Output templates in `skill/templates.md`
- Usage guide in `skill/usage.md`
- Documentation set:
  - design principles
  - source hierarchy
  - guardrails
  - workflow
- Six complete worked examples
- GitHub-ready repository scaffolding
