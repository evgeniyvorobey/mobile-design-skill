# Changelog

All notable changes to this project will be documented in this file.

## [1.25.2] - 2026-08-14

**Two claims from 1.25.1 are corrected, and the per-dimension levels §16 and §17 were trying to produce now exist.**

Six briefs in fresh domains through `SKILL.md` at 1.25.1, nine dimensions each, situations written from the brief alone by agents holding the `4 -> 5` question, 54 cells and 162 blind judgements. **53 of 54 situations landed on-scope**, against 0 of 12 for the procedure every measurement since section 14 had used.

| dimension | closed |
|---|---|
| Distinctiveness and owned assets | 5/5 |
| Typography craft | 5/6 |
| Interaction polish and motion | 4/6 |
| Attention path and hierarchy | 3/6 |
| Density and rhythm | 3/6 |
| Color, state, and contrast | 2/6 |
| Composition and spacing | 1/6 |
| Context and brand fit | 1/6 |
| Production readiness | 1/6 |
| pooled | 25/53 = 47.2% |

**Section 14's null does not reproduce.** Sorted by the band each artifact assigned itself, cases close at 16.7% on band 3, 41.2% on band 4 and 76.9% on band 5 — band 5 against band <=4 is +39.4 pp, Fisher p = 0.0235, where section 14 measured +3.3 pp at p = 0.52 with the sign inverting under adjustment. Half of that is dimension mix: stratified on dimension the odds ratio falls 5.56 to 1.80, shrinking but not flipping. The instrument and two releases of closure-test discipline are confounded here and this design cannot separate them.

**The gate under-fires at both surfaces, and it is not about who runs it.** All six artifacts were independently re-banded by three `mobile-design-judge` agents. Against the same blind ground truth the artifact's own claim scores phi +0.340 and the judge majority +0.280, McNemar p = 1.000 paired on cell — and the judge returns the identical band on 47 of 53 cells. Both under-claim: 25 cells close for a blind reader, the drafting side claims 13. That is the opposite of the over-claiming this repository has been chasing since 1.22.0.

### Fixed
- `docs/proposals/quality-and-diversity-upgrade.md` section 18 now carries a correction note, and section 19 records what replaces the two claims. **`Production readiness`'s 3/12 was withdrawn and should not have been** — live output closes 1 of 6 on-scope against section 17's 3 of 12, so the level reproduces. What section 18 established and what it inferred came apart: the cell is satisfiable at 6/6 *and* live output is thin, and the broken instrument is what made those indistinguishable. **"Per-dimension levels are not readable as properties of a dimension" was too strong** — all three flagged dimensions reproduce directionally; what was lost was resolution and attribution, not direction.

### Added
- Section 19 — the level table, the section 14 non-reproduction with its dimension-mix adjustment and its stated confound, the judged-mode arm, and the recomputation showing section 17's null constrains the true effect only to [-63, +76] pp.

### Changed
- Nothing behavioral, for the second release running. Three findings here would each motivate an instruction change; each needs its own measurement of the shipped configuration first, which is what 1.24.0 cost.

## [1.25.1] - 2026-08-14

> **Two claims below are corrected in 1.25.2.** `Production readiness`'s 3/12 was withdrawn and should not have been — live output closes 1 of 6 on-scope, so the level reproduces; what stands is the narrower finding that the cell is satisfiable and the corpus is thin. And "per-dimension levels are not readable as properties of a dimension" was too strong: all three flagged dimensions reproduce directionally. Everything else here stands.

**Backlog item 1 measured. Nothing ships to instruction text, and one of the two floors it was about is withdrawn.**

The two situation families that produced `context & brand fit` 1/12 and `production readiness` 3/12 were re-measured against a fixed product outside the corpus, with five statement arms matched to 146-149 words, two probe conditions, two screeners and three blind appliers over 60 pairs.

| | on-scope by both screeners |
|---|---|
| situations written from the brief and the dimension name | **0 of 12** |
| situations written with the `4 -> 5` question in front of the writer | **12 of 12** |

With the case held to the cell's scope, the closure test separates load-bearing from performative statements by **+75 pp (p = 0.0001)**; off scope, by **+25 pp (p = 0.26)** — same statements, same raters, only the case changed. Both error directions move: the strongest arm goes 1/6 to 6/6, the hollow arm goes 3/6 to 1/6.

The two dimensions have opposite diagnoses. **`Production readiness` was the instrument** — a real test closes 6/6 unanimously with zero quotation and discriminates (four hard bar, two negotiable), where a well-written enumerated list closes 0/6 on the same cases. Its 3/12 is withdrawn, and section 15's open item closes as confirmed. **`Context & brand fit` was not** — its cell is satisfiable (5/6, 4/6), but the shape live output actually carries closes 1/6, reproducing the live floor under a corrected instrument. There the broken probes were inflating the weak arm, not deflating the strong one.

**The fix was measured before it could ship, and it is inert.** A second phase tested the exact wording that would have been added to the three surfaces that run the closure test, with the judge's own band decision as the outcome and blind-applier determinacy as ground truth:

| | recall on load-bearing | awards to performative | phi |
|---|---|---|---|
| as shipped today | 14/18 | **1/12** | **+0.68** |
| plus the case-scope constraint | 14/18 | **2/12** | +0.60 |

Recall identical, awards to performative statements up by one, and the mechanism never fires: judges already choose an on-scope case 24 of 30 times unprompted, against 26 of 30 with the constraint (p = 0.73). The measuring harness deprived its situation writers of the cell text; the skill never does. The pre-registered rule vetoed the change on the precision row alone.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 18 — the full record, including the consequence that outruns the item: every measurement from section 14 on used the same name-only probe procedure, so per-dimension *levels* in sections 16 and 17 are not readable as properties of a dimension, and section 17's null was returned by an instrument separating at one third of its corrected strength. Paired arm contrasts are unaffected, since the same situations tested every arm.
- One evidence citation in `docs/design-quality-rubric.md`: the four failure shapes, previously read backwards out of statements already judged hollow, were written to on purpose and tested forwards — 2 of 18 unlisted cases closed, against 29 of 36 for statements built on a mechanism that returns something (p = 0.000001). What passes is deliberately still not listed.

### Changed
- Nothing behavioral. No boundary question was rewritten, no scoring surface changed, and no guard was added — there was no defect class in the repository to guard, because the defect was in the instrument that measures it.

## [1.25.0] - 2026-08-14

**1.24.0's change is reverted. It does not replicate.**

That release required a band-5 claim to print its closure case, on evidence from three briefs: 7/27 → 16/27 load-bearing statements, McNemar p = 0.011. Re-measured at six briefs, 54 paired cells, one rater cohort, and with the extraction step fixed:

| | load-bearing |
|---|---|
| 1.23.0 baseline | 27/54 = 50.0% |
| 1.24.0 as shipped | 28/54 = 51.9% |

McNemar exact two-sided **p = 1.000**. Power to detect the effect it shipped on was **98.8%**, the 95% CI on the paired difference is [−15.7, +18.9], no cut of briefs or dimensions favours the treated arm, and no rater ranks it first — where in the three-brief run every rater did.

**The earlier result was produced by the measuring instrument.** The extractor used to quote a rule's bolded lead-in and drop the table carrying its values, and 1.24.0's own notes called that defect symmetric across arms. It was not. Fixed, the baseline arm on the same three briefs **doubles** — 7/27 to 14/27 — while the treated arm does not move: a printed `Unlisted case: … → value` is one inline sentence that survives extraction intact, where an untreated rule more often lives in a table the extractor amputated. The +33 points measured how legible each arm's rules were to the extraction step, not how often they closed.

Against no measured benefit, the change carried measured cost: band-5 claims 15/54 → 23/54, precision 0.733 → 0.652, over-claims 4 → 8, φ 0.289 → 0.230. And the gate never fired — all 23 band-5 claims carried a case, so "a band 5 with no printed case is a band 4" demoted **0 of 23**, while 8 of the 23 it passed were underdetermined on the raters' reading.

### Changed
- Reverted the printed-case requirement across all five instruction surfaces and its guard: the rubric's closure-test block, the self-review checklist, judged mode, the judge agent, and the four `- Unlisted case:` template slots.

### Unchanged, and re-verified by injection after the revert
- The band-5 closure test itself, the four failure shapes, the `4 → 5` returning-verb guard, and the defect-class scoping of the closure gate across every band-assigning surface. Nothing in this measurement touches them.

## [1.24.0] - 2026-08-13

> **Reverted in 1.25.0.** The measurement below does not replicate: six briefs and 54 paired cells, at 98.8% power for the effect cited here, return 27/54 against 28/54 with McNemar p = 1.000. The three-brief result was produced by an extraction defect that suppressed the control arm and left the treated arm untouched.


The band-5 closure test was a **silent** gate: run it, and if the rule returns nothing, drop to band 4. Silently-run gates are not checkable, and measurement says they are also not run.

Three briefs through the skill three times, nine design-quality statements extracted per artifact, each paired with a situation **written from the brief before any artifact existed** by agents who saw no statement and no arm. The same 27 situations test all three arms, so difficulty is identical by construction, and all three arms were re-judged in one pass by one cohort of blind raters.

| arm | load-bearing | paired test vs A |
|---|---|---|
| as it ships | 7/27 = 26% | — |
| + name the case, avoid four failure shapes | 12/27 = 44% | McNemar p = 0.151 |
| **+ print the case and what the rule returns** | **16/27 = 59%** | **McNemar p = 0.011** |

The printed-case arm is the only contrast in either pass to clear the pre-registered paired test, and it survives every robustness cut — unanimity 0.046, quotation-leaks excluded 0.006, worst case 0.055 — with no sign reversal in any brief and every rater ranking it first.

### Changed
- **A band-5 claim now prints its closure case.** `- Unlisted case: [the case the artifact does not list] → [the value the rule returns for it]`, on its own line under that dimension's band. The three constraints on the case and the four failure shapes are unchanged; what changed is that the test leaves a trace a reader can check.
- **Scoped to band-5 claims only, and the reason is measured.** Requiring a case under every dimension regardless of band collapsed the score's own information: 24 of 27 dimensions came back claimed at band 5, self-scoring φ of −0.053 against 0.171 for the unmodified skill, because writing a case, seeing output and awarding 5 becomes one motion. The printed case is a gate on the top band, not a section to fill in.
- The requirement is stated on all four surfaces that assign a band, and the slot exists in the output templates, where the artifact is written rather than where it is scored.

### Fixed
- The judge now scores a band-5 claim with no printed case as a band 4, and is told to run a printed case itself rather than accept it — a case whose answer the draft already prints elsewhere was closed by quotation, not by derivation.

### Added
- Each band-assigning surface must require the case to be **printed** rather than merely run, and `skill/templates.md` must carry the slot. Verified by injection on all five sites.

### Note on an earlier number
The previous release's supporting measurement reported the "name the case" instruction at Fisher p = 0.043. Re-judged by the same rater cohort as the other arms, it is **p = 0.127**, on a drift of two statements out of 54, and it was never significant on the pre-registered paired test in either pass. That instruction's advantage was one statement wide. It ships only as the subset the printed-case requirement contains.

## [1.23.0] - 2026-08-13

Determinacy in live output varied 14%–86% **by dimension** and barely at all by band, which raised the question of whether some dimensions can reach band 5 at all as their `4 → 5` question is written. Measured: nine dimensions, one fixed product absent from the corpus (so artifact-of-origin is removed by construction rather than adjusted for), two statements each — a serious attempt at the question, and a well-written specimen of the failure shapes live output actually produces — paired against the same two situations, written from the brief alone by agents who never saw a statement or an arm.

**The hypothesis survives in 0 of 9 dimensions.** Restricted to the five whose cases were on-question, the serious attempts cleared 10/10 and the specimens 1/10, sign test p = 0.0039. Interaction is tied for the lowest live rate (1/7) and its best statement cleared 6/6 unanimously. The questions are satisfiable; live output is what falls short.

What the measurement did expose is that **two cells were not asking what the other seven ask.**

### Changed
- **`Color, state, and contrast`'s `4 → 5` graded the form of a statement rather than what it returns** — *"is that appearance behaviour expressed as one transform over the roles, rather than as a second hand-made set?"* The closure test asks you to write down what the statement returns, and that cell never asked for an output, so the test structurally could not be run on it: three blind readers unanimously judged a complete OKLCh transform underdetermined because the case asked something the cell never posed. Now *"Does a stated rule return the dark and increased-contrast values for a role the artifact does not list?"*
- **`Production readiness`'s `4 → 5` was a completeness test over listed values** — *"does the handoff say which values are negotiable and which are hard bars"* — which is band-4 shaped, and whose output is an authority class rather than an answer to a case. Now *"Does a stated test return hard-bar or negotiable for a value the handoff does not list?"*
- **The closure test carries three constraints on the case, not one.** It must be an instance of the unlisted thing the cell names; its answer must not already be printed in the statement (a case can be unlisted while its answer is listed, and the statement then closes it by quotation); and it must fix every input the rule needs except the one under test.

Confirmed by re-running the same statements against cases drawn from the rewritten cells, predictions registered first: colour 0/6 → 5/6, production 1/6 → 6/6, typography 0/6 → 6/6, and the typography specimen — which had been clearing 6/6 by quoting an unconditional "all numerals are tabular" — 6/6 → **0/6**. Arm separation moved from −5/18, the specimen arm outscoring the serious arm, to +14/18. One prediction was refuted: the production specimen was predicted to stay underdetermined and cleared 3/6, because its case landed inside a class the statement enumerates outright.

### Added
- A `4 → 5` cell may not use form-grading vocabulary and must carry a returning verb, so the closure test always has an output to write down. Scoped to the class rather than to the two cells that failed, and verified by injection in both directions.

## [1.22.0] - 2026-08-13

Band 5 was being awarded by reading a statement and judging whether it looked like a rule that decides unlisted cases. That was measured, twice, and it does not work.

63 statements pulled from live output were each paired with one ordinary unsettled case from their own product and handed to three readers who saw the pair and nothing else — no artifact, no dimension, no band. Statements scored 5 settled their case **11 times in 28**; statements scored 4, **9 times in 25**. Fisher one-sided p = 0.52, and 17 of the 28 band-5 statements were judged non-generative by two or more readers who never saw a score.

The first version of this experiment reported 50% against 30% and was **thrown away**: the agent that wrote each situation also knew which arm the statement came from, so probe difficulty tracked the arm. In the matched re-run both rates moved toward each other — band 5 down 10.7 pp, controls up 10.0 pp — which is the signature of the removed confound rather than of an effect appearing.

The remaining confounds all fail in the direction that *flatters* band 5: its arm carries the two highest-yield dimensions (distinctiveness 6/7, attention path 5/7) while band 4 carries composition 2/7 and interaction 1/7. Stratified on dimension, the odds ratio drops from 1.15 to 0.735 — adjusting flips the sign. The near-null is a ceiling on the band effect, not a signal under noise. Dimension identity moves determinacy 21× more than band does; artifact of origin, 17×.

### Changed
- **Band 5 is awarded on a closure test that gets run, not on how a statement reads.** Take one ordinary case the artifact does not list, state what the statement returns for it, and if you cannot write the answer the band is 4. The band descriptors are unchanged — nothing in the data says band 5 is described wrongly relative to band 4; the failure was in operating the question by inspection.
- Four failure shapes are recorded as **diagnoses**, accounting for 34 of the 38 non-generative statements: a ratio or floor with no anchor, a budget with no behaviour, a precedence ladder with no output, a requirement with no threshold. The shapes that *pass* are deliberately not listed — that would be a template to satisfy, which is the failure mode this repository has shipped twice.
- The gate is carried by every surface that assigns a band: the rubric, the self-review checklist, judged mode, and the judge agent.

### Added
- `validate_band_five_closure_test()` — checks the closure test is present on all four scoring surfaces and that the failure-shape list is intact. A gate present in the drafting instructions and absent from the judge is the file-scoped guard this series keeps rebuilding. Verified by injection on each surface.

## [1.21.0] - 2026-08-13

The design-quality scale asked for a number from 1 to 5 and gave **three columns to pick it from**: `1-2 signals | 3 signals | 4-5 signals`. Two of the three were bands, and the document supplied within-band discrimination for exactly one of them — there was no text anywhere in the repository distinguishing 1 from 2. So the decision procedure a model could execute was "pick a column", and the committed corpus shows the result: 63 dimension values across seven `Dimension read:` lines, holding `1`×1, **`2`×0**, `3`×14, `4`×45, `5`×3.

The collapse was bimodal and the two halves hid each other. Generation was pinned to `{3,4}`; Mode D was pinned to `{2,3}` — twenty 2s and five 3s in its `Now` column, zero 1s, 4s or 5s. The union across both carriers looked wider than either.

### Changed
- **Four boundary questions per dimension replace the three descriptions.** Each is one yes/no test against the artifact; the band is the number of consecutive questions answered yes from the left, plus one, and a later yes never rescues an earlier no. Four boundaries define five bands exhaustively — under the old table a typography treatment with sizes but no weights matched no cell at all. The ladder separates four acts: named (2), decided for the default case (3), stated with values surviving one declared variation (4), and a rule that settles the cases the artifact does not list (5).
- **5 is a per-dimension property.** The old step 5 gated every 5 behind resilience "across states, accessibility settings, platform behavior, and implementation handoff" — a four-way conjunction spanning four different dimensions, so `Typography craft` could not satisfy it and no single dimension was ever 5.
- **Caps clamp the artifact score after the median instead of before it,** and never change a dimension band. A cap applied first has nothing to clamp; a cap applied to a band destroys the evidence it was derived from.
- **`n/v` and a low band are separated on two axes:** `n/v` when the evidence channel cannot carry the question, a low band when the channel is right and the content is thin. Every visual dimension in every committed review had been routed to `n/v`, shrinking the assessable set to three or four structural dimensions that all moved on the same findings — a median over correlated values is not a median, it is the shared value.
- **Mode D gained the ninth dimension and a derivation for its current score.** `Distinctiveness and owned assets` was missing from the review template, so the one row whose old cells contained a real ladder was scored in zero of nine reviews. And `Current:` had no derivation rule while `Projected:` had one, in the same code block, across five files.
- The `1-5 score levels` table is relabelled a reading key for a derived number. It sat four lines above the dimension table describing 4/5 as "clear hierarchy, usable density, concrete states, accessibility-aware decisions, platform alignment" — a second, competing definition of the same digits.
- The whole committed corpus was re-derived under the new boundaries, and `examples/ui-spec.md` gained the colour rules a status-comprehension spec should always have had: four status roles as container/on-container pairs, contrast floors, and dark plus increased contrast as one transform over those roles.

### Fixed
- **`QUALITY_TARGET_SHAPE` forbade 5/5 by test suite.** It required `blocked from … until` unconditionally and is a `must_contain` for Modes A and C, applied to live output through the generation eval — so a response deriving 5/5 could not satisfy it without inventing a blocker. Now score-conditional: below the top band the blocker stays mandatory; at 5/5 the response says nothing blocks it.
- **`docs/evals.md` carried a per-dimension floor at 4** — "Any dimension below 4/5 is either revised or clearly blocked by missing input" — handed verbatim to the fixture judge in its prompt. Every revision trigger is now expressed as a test on the artifact rather than a comparison against 4.
- **`validate_score_is_derived_not_prescribed()` matched zero lines inside its own scope.** All five patterns require the token `target` adjacent to `4/5`, and every live anchor had drifted to "usually lands at", "4/5-style", "At 4/5,", "not a quiet 4/5". It was a synonym list accumulated one defect at a time; the class is now stated once, with the discriminator *is this sentence's truth value knowable before the dimension read exists?*
- **`compare_judgement` never compared `dimension_scores` to anything.** A judge returning nine 3s and a score of 5 passed all fixtures.
- Dimension-set drift of 9/8/8 across `skill/metadata.yaml`, `docs/llm-judge-runner.md` and `docs/evals.md`, in every case dropping `Distinctiveness`.
- `docs/evals.md` still documented `asset_class_count` as an asserted threshold after 1.20.0 demoted it in code.

### Added
- **Eleven validator assertions, each verified by injection**, scoped per carrier rather than to the merged set: the union of `Dimension read:` bands covers 1..5; every dimension takes more than one band across the corpus; at least one line carries both a `≤2` and a `≥5`; at least two lines span three or more bands; each Mode D column takes at least three distinct bands; no flat fixture vector; at least one fixture vector spanning `≤2` and `≥5`; every dimension taking three or more bands across the fixture pack; the judge's score never above the median of its own vector; and a band table of four boundary columns whose every cell is a question naming no score level.
- **The anchor class**, with four sub-shapes (frequency, exemplar label, presupposition, and a floor on the derivation's inputs) and three exclusions each documented beside the false positive that motivated it. Scope moved from a directory allowlist to line-shape exclusion, which is what reaches `skill/metadata.yaml` and `.claude/agents/*.md`.
- **`run_diversity_eval.py` reads the dimension vector.** Six reported-only fields; the self-test asserts the metric *separates* a uniform corpus from a varied one rather than clearing an invented bar, and the extractor check re-derives the median from its own parse instead of replaying a known answer.

## [1.20.1] - 2026-08-13

A pre-handoff sweep found the repository **validating clean while eight instruction-level contradictions survived**. Cause: every guard added across 1.17.0–1.20.0 was scoped to the *file* where its defect was first seen rather than to the *class* of defect, so each survivor sat one directory outside a check that would otherwise have caught it. That generalization is the release.

### Fixed
- **`skill/modes.md` omitted `Device class` from all six `### Output structure` blocks** — in the file `SKILL.md` names authoritative, while both the response validator and the generation eval hard-fail any response missing it. Invisible to mode parity, which strips contract elements before comparing. Now checked by `validate_modes_carry_contract_elements()`.
- **Two live "aim at 4/5" instructions** in `skill/usage.md` and `skill/modes.md`, outside `PRESCRIBED_SCORE_SCOPE` and matching none of its patterns. The 1.19.0 note that seven such sites existed was an undercount.
- **`examples/anti-patterns.md` taught the banned pre-1.16 Mode D bucket shape inside two "Good response" fragments** — the "a filled-in example outweighs a prose instruction" failure this release series documented, live inside the file meant to demonstrate correctness. Both converted to the Findings causal-chain shape.
- **`install.sh --method copy` never copied `examples/`**, while `SKILL.md` references it in ten places, so the copy install degraded silently instead of failing.
- **`run_diversity_eval.py` asserted `asset_class_count ≥ 3` against its own recorded measurement of 2** — a threshold that fails by construction. Demoted to reported-only: that measurement is the floor to move, not a bar the output clears.
- `SKILL.md` contradicted itself five lines apart on whether `Device class:` is unconditional.
- `MARKDOWN_GLOBS` used `docs/*.md`, so seven required domain packs and `CHANGELOG.md` were never link-checked.

### Changed
- `PRESCRIBED_SCORE_SCOPE` widened to `skill/` and `SKILL.md`, with a `target(ing) 4/5` pattern added. The two guards must be widened together or neither.
- Two new checks: `validate_modes_carry_contract_elements()` and `validate_calibration_teaches_current_shape()`, the latter permitting the banned Mode D headers only under `### Bad response`. 31 validators total.
- `docs/proposals/quality-and-diversity-upgrade.md` gains a **§12 hand-off**: current state, the three planned items that were corrected after measurement and therefore outrank the plan tables, the ranked backlog, and the working conventions — injection-verify every rule, never `git checkout` on a dirty tree, build self-tests that discriminate rather than replay, run live acceptance before any release touching instruction text.

## [1.20.0] - 2026-08-13

Sameness is now measured rather than read for. It was the symptom this whole line of work started from, and until this release it had only ever been assessed by a human reading outputs side by side.

### Added
- **`scripts/run_diversity_eval.py`** — extracts a **decision vector** from each generated response (the catalog entries it sampled via `from:`, the asset class of its `Signature move`, the score it derived, the dimension it named as the blocker, the base units and ratios it emitted) and reports the spread across a set. This is only possible because 1.18.0 pushed provenance and asset class into the output as machine-readable fields; before that there was nothing to measure but prose.

  **Vectors, not prose.** A pairwise 5-gram similarity over the calibration bodies was specified during 1.17.0 and measured at a median of **0.0** — those blocks describe different domains in different words, so word-level overlap cannot see structural sameness. A small structured vector can.
- **`examples/evals/diversity-fixtures.json`** — a deliberately `uniform` corpus reproducing the exact failure the 1.17.0 live acceptance found, and a `varied` one. The self-test asserts the measurements **separate** them, and that the extractor reads score, provenance and blocker out of a real committed response.

  | corpus | score conc. | provenance conc. | asset classes | vector similarity |
  |--------|-------------|------------------|---------------|-------------------|
  | uniform | 1.00 | 1.00 | 1 | 0.714 |
  | varied | 0.50 | 0.10 | 5 | 0.077 |
- A `## Diversity eval` section in `docs/evals.md`, and the self-test wired into CI and the release gate. It needs no model.

### Changed
- Thresholds are asserted **only where this repository has measured data**: score concentration, provenance concentration, blocker concentration and asset-class count each carry the acceptance run they came from, in the source. `vector_similarity` has no baseline and is reported without assertion. Report-only is the default; `--assert` enforces. Guessing a threshold produces either a check that passes vacuously forever or one that forces dishonest output, and both have already happened in this repository.
- Within-prompt divergence stays deliberately unmeasured. There is no sampling-temperature contract, and a deterministic skill giving one well-grounded answer to one prompt is defensible. Never considering anything else is not — which is what the provenance and asset-class measures capture.

### Notes
- The self-test discriminates rather than replays, and both halves were verified by injection: loosening the thresholds until the uniform corpus passes fails it with *"the metric does not discriminate"*, and breaking the extractor's score pattern fails it with *"extractor read score `None`"*. That design is a direct answer to 1.19.0, where a green oracle replay sat over a function with a variable-shadowing bug — a self-test that only proves the pipe works is worth nothing.

## [1.19.0] - 2026-08-13

The first check in this repository that reads generated text. Everything before it read markdown a maintainer wrote.

### Added
- **`scripts/run_generation_eval.py`** — asks a model to answer real prompts and holds the answers to **exactly** the contract the committed examples are held to. It imports `check_response()` from `scripts/validate_repo.py` rather than reimplementing it, so corpus rules and output rules cannot drift apart. That reuse matters here more than anywhere: drift between two files claiming one contract is the failure this repository has now shipped twice.

  It exists because three acceptance passes during 1.17.0 found two defects that all 29 structural validators passed over — an instruction that produced token consequences while the slot receiving them still asked for layouts, and a filled-in illustrative line in a reference doc that outweighed the prose instruction telling the model to derive its score.
- **Three eval-only checks**, none of which a committed file can be wrong about but a live run can:
  - *Derived score* — `Quality target: N/5` may not exceed the median of the dimension scores the response itself prints. Pure arithmetic, no model required. This is the check that would have caught the asserted-score defect on the first acceptance pass instead of the third.
  - *Provenance* — a rejected direction citing a source that is not an entry in the catalog in `docs/inspiration-sources.md`.
  - *Prompt expectations* — a tablet prompt answered with `Device class: Phone`, or a no-fit prompt rounded into a standard mode instead of opening `Mode: outside the standard six`.
- **`examples/evals/generation-prompts.json`** — ten prompts covering all six modes, three domains, the tablet path and the no-fit branch. Six carry a `reference_example` and are replayable by the deterministic oracle. Adding a prompt is the cheapest way to turn a field bug into a standing regression check.
- **`scripts/generation_oracle_agent.py`** — replays committed examples through the scorer so CI can prove the stdin/stdout adapter and the JSONL parser without a model.
- A `## Generation eval` section in `docs/evals.md`, and a `workflow_dispatch` trigger on the CI workflow for manual runs.

### Changed
- `validate_example_responses()` refactored into `check_response(response, mode, label)`. The corpus validates identically; the function is now the single definition of what a skill response must be, whether it was committed or just generated.
- The release gate (`scripts/validate_release.py`) and CI both run the prompt-pack validation and the oracle replay. Both CI steps are named so nobody reads them as evidence about design quality — **no model runs in CI**, and generation needs one while scoring does not. That split is what makes the scorer CI-safe.

### Fixed
- The refactor introduced a variable-shadowing bug that injection caught: the extracted function's `label` parameter was shadowed by the loop variable in the `label_word_counts` check, so failures were reported against `Attention path:` rather than the file being checked. The oracle replay passed green while this was broken — only the negative test exposed it.

## [1.18.1] - 2026-08-13

Retires the third file claiming to be the workflow. Cleanup plus one guard; no capability change beyond the ported classification examples.

### Removed
- **`skill/skill.md` (489 lines).** No host loaded it: `agents/openai.yaml` carries only interface metadata and no file path, the Claude Code wrapper reads the root `SKILL.md` explicitly, and `README.md` tells Cursor users to copy the root `SKILL.md`. The 1.0 changelog entry — *"Main skill prompt in `skill/skill.md`"* — records what it was: the original prompt, superseded when the root `SKILL.md` became the entrypoint, and never retired.

  It had drifted two releases behind, carrying **zero** occurrences of step 5.5, `Device class`, `adaptive-layout`, `outside the standard six`, `Signature move`, `Dimension read`, direction provenance, or the Distinctiveness dimension — so catching it up would have meant re-forking a workflow that now spans `SKILL.md`, `skill/modes.md`, `skill/templates.md` and thirty reference documents.

  It was also generating contradictions rather than sitting inert: its scoring paragraph ended up holding the current derivation rule and the obsolete pre-1.16 review rule in one sentence, while its own output structure four hundred lines later specified the `current → projected` score with a per-dimension table. That is the drift class the 1.17.0 release was spent fixing, reproducing inside a single file.

### Added
- Six worked classification examples in `SKILL.md`'s mode section, ported from the retired file — more concrete than the abstract intent cues in `docs/workflow.md`, which had no request-to-mode examples. Its ban on vague advice was already guardrail 4, and its closing reminder duplicated `SKILL.md`'s.
- `validate_single_workflow_source()` asserts that `## Required workflow` and `## Mode output requirements` appear in `SKILL.md` and nowhere else. Three files each claiming to be the workflow is the structural condition that let the 1.16.0 Mode D contract ship without reaching the entrypoint; this stops a third fork from quietly reappearing. Verified by injection.

### Changed
- Ten `skill/skill.md` entries removed from the validator's required-file and reference path lists, plus its lines in `skill/usage.md` and the `README.md` repository tree.

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
