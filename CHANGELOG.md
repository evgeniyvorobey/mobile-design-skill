# Changelog

All notable changes to this project will be documented in this file.

## [1.36.0] - 2026-08-26

**The release gate had never run, and nothing had ever read an install.** Every check that only `validate_release.py` performs — version parity across five places, the CHANGELOG top entry, the paired-comparison self-test — was unexecuted in CI for the entire history of this repository, and defects rode through underneath it. Separately, every validator in this repository reads the repository; none had ever looked at the tree a user installs, where `scripts/run_rubric_judge.py` has been dangling since 1.12.0 and `scripts/run_generation_eval.py` since 1.19.0.

### Fixed
- **`release-validate.yml` now triggers on a pushed `v*` tag.** It carried `workflow_dispatch` alone, so it had never run once: `gh run list --workflow=release-validate.yml` returns empty across every tag. The tag is passed through as `--tag-or-ref`, so a tag that disagrees with `skill/metadata.yaml` now fails the run instead of being skipped.
- **The CHANGELOG top entry can no longer be satisfied by an empty placeholder.** `read_changelog_top_version()` checked one thing — that the first `## [x.y.z]` label parses as semver. A release with zero lines of description passed. It now also fails on an empty body (section headings and bare bullets only), on the unfilled `## [Unreleased]` placeholder, and on any version that heads two entries.
- **Removed four duplicate CHANGELOG headings.** `1.35.1`, `1.35.0`, `1.34.0` and `1.33.5` each appeared twice — an empty `bump_version.py` placeholder left in place above the real entry, four releases running. The gate now refuses that shape.
- **`bump_version.py` writes `## [Unreleased]` instead of a placeholder already labelled with the new version.** A placeholder carrying the version is structurally indistinguishable from a finished entry, which is how the four duplicates formed. An unversioned placeholder cannot be mistaken for a release: the gate rejects a non-semver top heading, so the entry has to be written before the version can be tagged.
- **`README_MUST_ENUMERATE` now reaches `scripts/`, `examples/*.md`, `examples/case-studies/`, `examples/evals/` and `examples/rendered-output-qa/`.** The guard added in 1.31.0 covered four globs and missed the directory holding shipped code: `SKILL.md` sends the reader to `scripts/run_generation_eval.py` and the README named neither it, `run_diversity_eval.py`, `generation_oracle_agent.py`, nor six of the eleven eval fixtures. All nine are now in the architecture tree.
- **`.playwright-mcp/` is untracked and ignored.** 32 files, 168 KB of console logs and accessibility snapshots from a local Playwright session, committed in `f008f2e`. Content checked before removal: only `http://127.0.0.1` URLs, no secrets — refuse, not leak.

### Added
- **`docs/paired-comparison.md` is in the canonical `SKILL.md` reference list.** Its siblings `docs/evals.md` and `docs/llm-judge-runner.md` were already there; the one instrument that answers *which of two designs is better* was reachable only through the README. The Claude Code wrapper listed it in one downstream copy and not in this repository's own.
- **The Claude Code wrapper now mirrors the canonical reference list, in the same order.** It was missing five documents the canon names — `motion-system.md`, `adaptive-layout.md`, `evals.md`, `llm-judge-runner.md` and `paired-comparison.md` — so `/mobile-design-skill` and a direct read of `SKILL.md` loaded different document sets.
- **`validate_skill_entrypoint_enumerates_docs()` in `validate_repo.py`**, the mirror of the README guard for the document the *model* starts from: every `docs/*.md` must be named in `SKILL.md`, and the wrapper must name every doc the canon names. The four process docs (`commands`, `github-publishing`, `release-automation`, `versioning`) are excluded by name, each carrying the reason, so a fifth cannot be added silently.
- **`scripts/verify_install.py`, and a CI step that runs it.** Nothing in this repository had ever looked at an install. `install.sh --method copy` inlines a subset of the tree next to a rewritten wrapper, so a reference valid in the working copy can dangle in what a user loads. The script performs a real install in both methods into a throwaway directory and resolves every path either wrapper names against what actually landed.
- **`install.sh --method copy` now copies `scripts/`.** `SKILL.md` has named `scripts/run_rubric_judge.py` since 1.12.0 and `scripts/run_generation_eval.py` since 1.19.0, while the copy install placed no `scripts/` directory at all — three dangling references in every copy install, which is what the new verifier reports the moment the copy line is removed.
- **`run_paired_eval.py --self-test` runs on every push**, alongside its judge adapter, next to the three neighbouring self-tests that were already there. On pushes the refusal was previously guarded by `validate_paired_eval_falsifier()`, which reads the source for two constants; deleting the refusal itself (`readable = null_rate <= NULL_AGREED_WINNER_MAX` → `readable = True`) leaves both constants intact, and `validate_repo.py` stayed green on that mutation. The new step goes red. A harness whose only value is declining to report a failed control was shipping with a disableable refusal.

### Changed
- `docs/release-automation.md` no longer calls the workflow manual, and its check list now matches what `validate_release.py` actually runs — the diversity, generation and paired-comparison steps were absent from the document.
- `docs/versioning.md` and the README maintenance block describe the `## [Unreleased]` ritual and what the gate rejects.

### Not changed
- **No rule, bar, band, template or mode contract moves, and no guidance text is edited.** The audit that produced this release was scoped to the harness and states outright that it says nothing about the quality of the guides. This is MINOR rather than PATCH for one reason: `docs/paired-comparison.md` enters the runtime reading list and the wrapper gains five documents, so the set of files the model may load is larger than it was.
- `validate_paired_eval_falsifier()` is kept. With a real run in CI it is a fast structural check on the fixture corpus; it was never evidence that the refusal refuses.

## [1.35.1] - 2026-08-20

**Item C re-opened and answered. An implementer obeys 81.1% of the rules a spec explicitly states, and the gap is structured by the grammatical form of the rule.**

### Measured
- **Obedience to stated rules: 81.1%** (107 obeyed, 25 violated), 95% CI [74.4%, 87.7%], with **zero** `cannot-tell` verdicts across 132 checks. Roughly one stated rule in five is violated by a competent implementer working from the document alone.
- **The gap is structured by rule form**, which is the finding: presence ("the screen has X") **14/14 = 100%**; prohibition ("X never appears") 35/42 = 83.3%; value ("X is 24dp") 48/60 = 80.0%; **relation ("X exceeds Y", "aligned to one edge") 10/16 = 62.5%**. Relations are violated at nearly twice the rate of values (17.5 pp, Fisher exact p = 0.187 - a direction on a 16-cell, and P4 was registered as underpowered before the data). Naming a thing survives implementation; relating two things does not.
- **Ten of 66 rules were violated by BOTH independent implementations** - not implementer noise but a form that does not survive: zone spacing intervals, row minimum height, the money role, the 8dp scale, "no cards, no elevation, no fills".
- **Obedience does not explain judged quality.** The render section 43's judges preferred in all four pairs and both orders obeys 82%; the loser obeys 80%. Following the spec and being the better screen are two axes.
- **23% of stated rules are unreachable from a static default-state render** - loading and error states, motion, focus order, screen reader, large text, dark mode - and were excluded with reasons rather than counted as passes.

### Instrument
- **Falsifier passed 10/10.** Three violations were injected mechanically into a copy of each r1, ground truth fixed in advance. The checker caught 10 of 12; hand-adjudication showed the two misses were bad injections, verified mechanically - one edited a class that does not match the money elements (the checker identified the injection and explained why it does not touch the money column), the other targeted a class with zero elements on the page. Both figures are reported.
- **Checker test-retest measured in the same run: 93%** (50/54 agreement on rules the injections did not touch), above the ~84% ceiling every other instrument in this series sits at.
- **All 87 extracted rule quotes verified verbatim against source, 0 mismatches**, and the 66-rule set frozen with a SHA-256 before any checker saw it.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` **section 44**, with the design, the falsifier and its hand-adjudication, the per-form decomposition, and **rule 39 - the form of a rule predicts whether it survives implementation: naming survives, relating does not.**

### Not changed
- **No rule, bar, band, template or mode contract moves.** P4 is not significant and rule 15 requires measuring a change on the surface it ships to; the direction is recorded and the instruction text is untouched.
- Nothing measurement-shaped is committed. Section 40's item C is annotated as answered.

## [1.35.0] - 2026-08-19

**Backlog item C gated before it was built. A rendered contrast measures the renderer, and the reason is that a spec's stated rules do not survive implementation.**

### Changed
- **`docs/design-quality-rubric.md` no longer claims that stating values makes two implementers produce the same screen.** Band 4/5 and the `Production readiness` 3 -> 4 cell both said so; four specs that state their values, tokens, spacing ladders and alignment rules produced **8 of 8 structurally different judgements** between two blind implementations. Both sites now say the implementers have the same **decisions in front of them**, and band 4 records what stating does not buy. The boundary cell stays a question - the repo validator refused a first edit that turned it into a statement.

### Measured
- **The render gate: 8 of 8 judgements named a winner between two renderings of ONE document**, every one marked structural, order-invariant across all four documents, mean confidence 3.50. A rendered contrast between two skill versions would measure the renderer rather than the skill, so **item C's phase 2 is refuted** for the cost of twenty-four agents.
- **Hand-adjudication changed what that means.** Every structural difference the judges named is explicitly stated in the source spec - the money column "right-aligned to the single money column edge" stated three times, the 24dp/12dp and 32/16/4 proximity ladders stated outright. The specs did not leave these open; a competent blind implementer did not obey them.
- **A fidelity measure that had to be rebuilt before it could be believed.** Asking what share of each render's spacing sits on its spec's stated scale first returned "the judged-worse render is more faithful, 4 of 4"; the renders express spacing through CSS custom properties, so a raw px regex saw 5 of 30 declarations. With variables resolved and validated against declaration counts, it is **2 of 4 each way** - and scale fidelity predicts nothing about which render was judged better, because every deciding difference is a relation rather than a value.
- **The first render run was voided and is reported, not replaced.** The prompt did not forbid previewing; four of eight agents started local HTTP servers, two outlived their agents, and preview use split within pairs on two of four documents - a process asymmetry inside the measured variable. The re-run forbade it and was verified per tool call at 0 attempts in 20 calls.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` **section 43**, with the audit, the voided run and its cause, the gate, the hand-adjudication, and **rule 38 - a value on the stated scale is not the rule the scale exists to serve; checking membership instead of relation is the presence trap one level down.**

### Not changed
- **No rule, bar, band, template or mode contract moves.** `docs/rendered-output-qa.md` is untouched: the finding is about what a rendered channel can measure, not about that workflow's content.
- Item C is annotated in section 40 as phase-2-refuted and re-opened as a spec-implementability check, which is the one thing this repo has never had an instrument for.

## [1.34.0] - 2026-08-19

**Backlog item A closed, bounded. P1-2 measured at eighteen pairs instead of six, and the instrument that measured it survived a diagnostic that should have killed it.**

### Changed
- **`scripts/run_paired_eval.py` carries rule 33's confound control in the tool.** The judge system prompt now states that a longer document is not a better design and that naming more values is not describing a better screen. Section 37 claimed judges were told this; the prompt stored in its own `pairs.jsonl` contains only the length half, and the phrase appears nowhere in that run's files. A claimed control that is not in the tool is not a control - this one is now generated into every request and greppable afterwards.
- **`docs/paired-comparison.md` requires a length-varied null.** A null written to hold length constant is blind to a length effect. The file now says so with both measurements, so the next contrast cannot inherit the blind spot.

### Measured
- **Item A: 18 signal pairs, 48 judgements, one fresh judge each.** Control held at **0 of 6** agreed winners with `no-meaningful-difference` on 12/12. Signal: **arm A 21 / arm B 15 / tied 0, p = 0.203**, order-invariant on 15 of 18. Section 37's arm-A lead **does not replicate at its magnitude** - 67% to **58%** - and the brief-level 95% CI is **[-0.26, +0.59]**. P1-2 neither helps nor harms by any margin this design can see; 80% power arrives only against a tree winning ~85% of briefs.
- **The diagnostic rule 36 requires, applied to the judge: the longer document won 27 of 36 signal judgements (p = 0.004)** - and the run's own six nulls could not say whether that was bias or substance, because they were written to a "within 5% of the original" instruction and differ by a median 2.3% against the contrast's 13.7%.
- **The falsifier that settles it.** Five nulls rewritten as pure verbosity across **-15.2% to +40.2%**, every numeric value, backticked token and heading verified to survive as an exact multiset (one of six rewrites drifted and was excluded, not repaired). The judge returned `no-meaningful-difference` on **10 of 10** at maximum confidence, including at +40.2%. **The instrument has no length bias**; the association is length acting as a proxy for design substance. Across both runs: 22 of 22 null judgements found no difference, 36 of 36 signal judgements found one.
- **First test-retest on real output**: re-judging section 37's six pairs reproduced 4 of 6 brief-level verdicts.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` **section 42**, with the audit, both runs, the pre-registered predictions and their outcomes, and **rule 37 - a control matched on the confound cannot test the confound; check what your null pairs hold constant before you trust them to clear anything.**

### Not changed
- **No rule, bar, band, template or mode contract moves.** P1-2 is not reverted: a bounded null is not a revert-grade finding, and section 42 says which effect size it rules out rather than claiming there is none.
- Section 40's item A is annotated closed-bounded; nothing measurement-shaped is committed.

## [1.33.5] - 2026-08-19

**Backlog item B closed, negative. The displacement hypothesis was hand-read for the first time, the measure that had refuted it was rebuilt three times better, and the null survives both.**

### Measured
- **A state-count measure rebuilt and frozen before the test corpus was opened** (SHA-256 `ea7c9ce9…`, thirteen shape fixtures, two of them asserting what it deliberately does not count). Against hand-read truth on twelve artifacts it scores **MAE 4.58, max error 12, Spearman 0.612** — against section 38's **14.08 / 30 / 0.143** — and **fails all three pre-registered validation bars**, so it reports diagnosis and settles nothing. All twelve errors are negative in both measures: a machine state count is a strict lower bound, never an over-count.
- **The hypothesis itself, tested at last.** Hand-counted across three Mode C briefs, two arms and two draws per cell, the mean between-arm delta is **+2.67** against a mean within-cell spread of **6.33**. The pre-registered readability gate fires for the second run running — and section 39's diagnosis that *"it is not generation variance, it is the measure"* does not survive: with a human reading every word the noise is still **2.4x** the effect. The spreads are 1, 1, 1, 6, 14, 15, and what splits them is whether a draw happened to write a component-level state matrix, not which arm wrote it.
- **The reason the item closes is the construct, not the sample.** Hand count against word count is **r = 0.777** while the arms are the same length (4816 against 4930 words). Eighty percent power at the observed effect would need **76 briefs, about 306 generations**, to better estimate a quantity that is 60% verbosity.
- **A third blind-spot shape**, after section 30's table row and section 39's bold em dash: a state table whose rows are components and whose cells are comma-separated state lists. Every label-shaped parser reads the first column and returns the component count.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` **section 41**, carrying the design, the freeze, the blinded hand read, the four pre-registered predictions and their outcomes, the limitations as registered, and **rule 36 — a measure repaired until it is three times better can still be unfit, and the test of fitness is what it correlates with, not how close it gets to a hand count.**

### Changed
- Section 40's open item B is annotated **closed negative**, with a pointer to section 41 and an instruction not to reopen it as a count.

### Not changed
- **No rule, bar, band, template or mode contract moves**, and nothing measurement-shaped is committed. Section 39's corpus and frozen script were reused from a session scratchpad and reproduce that section's table cell for cell.

## [1.33.4] - 2026-08-18

**Handoff release. A current "where to pick this up", and three live documents corrected where nine sections of measurement had made their text false.**

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` **section 40 — the current handoff**, replacing section 12, which describes the tree at v1.20.0, twenty sections and nineteen releases ago. Section 12 keeps its text and gains a superseded notice, because the record is append-only. Section 40 carries the state, what the last nine sections settled, the three open items specified enough to start, and the two standing items that are not on that list.

### Changed
- **`docs/design-quality-rubric.md` states what its number records.** Every boundary question asks what an artifact *states*; held against six designs and six deliberately worse twins it returned the **identical band 12 paired scorings of 12**, while showing 17% jitter on unchanged text. A band is not a verdict on which of two designs is better - `docs/paired-comparison.md` is, and the two are named as complements.
- **A diagnostic in `docs/design-quality-rubric.md` and `docs/evals.md` pointed at the wrong cause and is corrected.** Both told a reviewer to read identical scores across a corpus as evidence the score was asserted or retrieved. That is what a faithful application of this scale produces - it returns the same band to a design and a worse version of it - and output mode concentrates it further (specs 63%, concepts 28%). A reviewer following the old line would fail a response for retrieval on a pattern the instrument produces by itself, or nudge bands apart to look computed.
- **`docs/evals.md` no longer implies the generation eval has been run with a model.** `--generate-command` has never executed against one; only the `--replayable-only` oracle path has, and it proves the adapter rather than a model. No claim in this repository rests on that script having read live generated text, and the file now says so.

### Not changed
- **No rule, bar, band, template or mode contract moves.** These are corrections of statements measurement has made false, not new instructions hoping to change behaviour - which would need an outcome measurement under rule 15.
- README was audited alongside the three and found clean.

## [1.33.3] - 2026-08-18

**The count that corrected 1.33.1 was itself measuring punctuation. Its pre-registered falsifier fired, and section 38's Mode C claim is withdrawn.**

### Measured
- Three fresh Mode C briefs, two arms (v1.26.0 / v1.27.0), **two independent draws per cell** - the control section 38 could not have, since a single draw cannot separate a displacement from generation variance. The measure was frozen byte-for-byte with its hash recorded before generation.
- **P3 fired.** Mean within-cell draw-to-draw spread **5.50** against a mean between-arm delta of **0.17** - noise thirty-two times the effect. By the pre-registered rule the run is **unreadable** and no displacement claim follows in either direction.
- **It is not generation variance, it is the measure.** `arm-b/checkout-d1` scored **1** while defining ten well-differentiated states - Default, Loading (initial), Recalculating, Unresolved, Empty, and Error at row, screen and commit level. The measure requires `- Label:` or `| Label |`; that artifact writes `- **Label** — text`. Against a repaired diagnostic the frozen measure undercounts by **7.8 states per artifact on average**, errors from **-3 to +25**; it read 1 where the repaired count reads 26.
- **Section 38's "19 against 5, entirely a Mode C phenomenon" is withdrawn**, with an inline notice on the section. The repaired count happens to show no displacement either, and is deliberately **not** offered as the answer: an unvalidated measure does not get to settle a question because it agrees with the conclusion.
- **What still stands, and why**: section 37's 6/3/3 at p = 0.254 with the control held came from judges reading designs, not from this count; and section 37's manipulation check asks whether a token appears anywhere in a document, so it has no label shape to break on, and its 0/6 baseline reproduced section 23's independent measurement.
- **The blind spot is a repeat from the same session.** Section 30 recorded a state defined in a markdown table row being invisible to a bullet parser. That lesson was written down, and a new counting measure was written days later with the same shape of blind spot and believed immediately.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 39, and an inline withdrawal notice on section 38.
- **Rule 35: a measure written to check a hypothesis is an instrument, and rule 2 applies to it - validate it against hand-read cases before believing a single number it produces.** Rule 2 was applied to the state-coverage detector and to the paired-comparison harness, and skipped for a five-line regex because it looked like arithmetic. Rule 34 said count it before you carry it; it did not say validate the count.

## [1.33.2] - 2026-08-18

**A correction to 1.33.1, found by one regex over a corpus already on disk: section 37's mechanism paragraph generalised three judgement paragraphs into one mechanism and was wrong on two of the three.**

### Measured
- Section 37 offered a direction to test: *"all three arm-A wins turn on the granularity of degraded states."* Before spending a corpus on it, it was checked mechanically, with a pre-registered concentration prediction.
- **P1 held** - arm A carries more distinct labelled states in total, **37 against 25**. **P2 failed** - the gap is **not** concentrated in the three arm-A wins. Two of those three wins have a state-count difference of **zero**, and the largest gap in the corpus (**+9**, `spec-ipad-clinician`) produced a **tie**.
- Re-read rather than summarised, the two zero-delta wins were decided on **disclosure** (a focal slot holding one item, a collapse policy hiding unresolved doses behind a count row) and on **flow structure** (where the flow spends its screens, where the first completion physically happens). Only `spec-package-tracking` turns on degraded-state granularity, and there the count agrees with the judge exactly.
- **What survives is sharper and mode-scoped**: the displacement is **entirely a Mode C phenomenon** - specs **19 against 5**, while concepts run marginally the other way (**18 against 20**). v1.27.0's substrate does not cost state coverage in concepts; it costs it in specs, where the output budget is tightest and where state definitions are the mode's own contract.
- **A blind spot in the measure is recorded rather than smoothed over**: `flow-onboarding` reads 0 states in both arms because a label-shaped count cannot see Mode B's `failure -> recovery` contract - both arms carry 21 and 22 such arrows. That row is missing data, not evidence.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 38, and an inline correction notice on section 37's paragraph pointing at it.
- **Rule 34: a mechanism read out of judges' reasons is a summary of prose, not a measurement - count it before you carry it.** The cheapest test of a post-hoc hypothesis is whether the thing it names is even present, and it should always run first.

## [1.33.1] - 2026-08-18

**The paired-comparison instrument's first real use, pointed at this series' own flagship release: P1-2's presence gain of +45.8 pp did not produce a better design, and the nominal direction runs against the shipped version.**

### Measured
- **Arm A = v1.26.0, arm B = v1.27.0**, checked out as git worktrees, six briefs from the committed prompt pack, twelve blind writers. Ordinary product briefs, not the craft-forcing briefs section 23 selected.
- **The manipulation landed harder than the original.** On P1-2's own indicators: a named curve **0/6 -> 4/6** (reproducing section 23's zero baseline exactly - without the substrate the model never names a curve, in six responses of six), baseline grid 0/6 -> 4/6, type-to-platform-style mapping 3/6 -> 5/6. Total **3/24 -> 14/24, +45.8 pp**, against section 23's +32.5 pp. A null on quality cannot be explained by the change failing to arrive.
- **Section 23 reported flat length; on ordinary briefs arm B is 8.7% shorter.** The substrate does not add text, it displaces it.
- **Control held**: `no-meaningful-difference` on **6 of 6** null judgements, 0 of 3 null pairs drew an agreed winner.
- **Result: 6 / 3 / 3 with p = 0.254.** The presence gain did not produce a better design, and the nominal lead is **arm A**, the pre-P1-2 tree. At n = 6 this is not a claim of harm and does not ask for a revert - the run can find a large effect or rule one out, and cannot resolve a small one.
- **All three arm-A wins turn on the granularity of degraded states** - v1.27.0 collapses "we couldn't reach the carrier" and "the carrier hasn't scanned in days" into one role; v1.26.0 keeps them apart, and they are opposite next moves for a user. That is rule 18's displacement seen **on the outcome instead of on an indicator**, for the first time. n = 3, so it is a direction to test.
- **The confidence signal is now interpretable across two runs.** Null pairs 3.00, signal pairs 1.83, against section 35's 3.00 and 2.83. Confidence measures certainty of the verdict; the signal figure falling from 2.83 on gross deliberate degradations to 1.83 on two real versions of the skill is the instrument reporting, correctly, that this contrast is the harder one.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 37.
- **Rule 33: neutralise the confound the arms are made of, in the judge's instruction, before the run.** These arms differ by construction in how many values they state; a judge rewarding specification density would have voted for the substrate arm and the run would have measured presence a third time wearing a comparison's clothes.

### Changed
- Section 23's open limitation - *"a response can name `emphasized decelerate`, a 4 pt grid and a tracking table and still be an ugly screen; nothing here measures that"* - is now measured. The answer, at this power, is that the largest instruction-text effect this series has shipped does not show up as a better design on ordinary work.

## [1.33.0] - 2026-08-18

**The paired-comparison instrument validated in 1.32.6 now ships. The repository can ask, for the first time, whether a change made the output better - and it refuses to answer when its own control failed.**

### Added
- **`scripts/run_paired_eval.py`** - forced-choice paired comparison of two arms of skill output. Two structural refusals are enforced by the tool rather than left to whoever runs it: **a contrast without null pairs is not reported** (at least three, and at least one per three signal pairs), and **a contrast whose judge names an agreed winner on more than a third of null pairs is reported as unreadable and exits non-zero**. Every prior release in this series had to notice that class of failure by hand, and three of them did not.
- **`docs/paired-comparison.md`** - what the instrument is, how to build the null pairs, the validation record, and four things it cannot do.
- **`scripts/paired_eval_oracle_agent.py`** - a deliberately weak deterministic stand-in judge, so CI proves the `--judge-command` adapter without a model. It applies a presence proxy, which sections 34-35 measured at 0 of 12 on real degradations; keeping it apart from the discrimination proof is deliberate, because an oracle supplying both would be a green oracle over the thing under test.
- **`examples/evals/paired-comparison-fixtures.json`** - three corpora the `--self-test` must tell apart: one where an arm genuinely wins, one where the arms are indistinguishable, and one whose control failed and must be refused.
- **`validate_paired_eval_falsifier()`** in `validate_repo.py` - the falsifier corpus can be deleted and both refusals widened into no-ops without any other check noticing. This asserts the falsifier still falsifies and neither refusal has been neutered. Verified by four injections; asserting that the word "null" appears somewhere would have been the shape check section 27 warned about.
- Release validation runs the self-test and the adapter proof.
- `docs/proposals/quality-and-diversity-upgrade.md` section 36.

### Changed
- `docs/evals.md` gains a section on comparing two arms, with the head-to-head numbers: the rubric's nine boundary questions separate **0 of 12** paired scorings on a corpus of designs against deliberately worse twins; the rubric-free comparison separates **12 of 12**.
- README enumerates the new document, both scripts and the fixture pack - caught, as designed, by the 1.31.0 enumeration guard the moment the document landed.

### Not changed
- **No instruction text.** This is an evaluation instrument, not an authoring one: paired comparison needs two artifacts and most modes produce one. Nothing in `SKILL.md`, `skill/` or any mode contract moves in this release.

## [1.32.6] - 2026-08-18

**Backlog item 1 is answered. On the same corpus where the rubric's boundary questions separated 0 of 12, a rubric-free forced-choice paired comparison separated 12 of 12 and named the injected mechanism every time.**

### Measured
- **18 judgments, one fresh judge each, nine pairs in two presentation orders.** Six signal pairs (clean against its verified-pure degraded twin) and three null pairs (clean against a **cosmetic rewrite of itself** - same design, same decisions, same values, different prose, verified mechanically: headings identical and in order, numeric-token multisets identical, length within +1.9% to +4.5%).
- **P1: 12/12** signal judgments named the clean artifact, p = 0.00024. **P2: 6/6** order invariance. **P3, the falsifier: `no-meaningful-difference` on 6 of 6 null judgments**, 0 of 3 null pairs drew an agreed winner.
- **The verdicts are right for the right reason.** All six signal pairs came back with the exact injected degradation class, unprompted - *"the signature spread until it stops signalling"*, *"what occupies the top of the screen and the Display type role"*, *"the number that decides the purchase is the biggest thing on the screen"*.
- **Head to head on one corpus:** the nine boundary questions separate **0 of 12** (p = 1.000); the rubric-free comparison separates **12 of 12** (p = 0.00024).
- **The confound is bounded, not eliminated.** Judge, degrader and null-writer share a model family. The null pairs are the defence and the reason they were cosmetic rewrites rather than identical text: the same family wrote those too, and the judge declined all six at high confidence. It is not detecting "an agent edited this".
- **P4 was refuted** - confidence on nulls (3.00) exceeded confidence on signal pairs (2.83), because a null verdict's confidence measures certainty that the two are the same. It was a prediction and not a gate, which is the only reason it did not void the run, and it is **the third pre-registered indicator in three sections** to fail to measure what it was written for.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 35.
- **Rule 31: when an instrument returns a null, try a differently-shaped instrument on the same corpus before concluding the property is unmeasurable.** The rubric's 0 of 12 read as "design quality is hard to measure". It was a fact about a question shape - *is it stated* - and not about the corpus, the degradations, or the property.

### Changed
- **Item 1's core question is answered: design quality is measurable here, and an instrument that reads it exists.** What could not see it was the shape of thirty-six questions asking whether something is stated.
- **The instrument is validated and not wired into the repository.** It has no home, no document, no harness and no place in any mode. That is its own change with its own pre-registration - paired comparison needs two artifacts, and most of what this skill does produces one.

## [1.32.5] - 2026-08-18

**Item 1's gate, run on a corpus verified pure: the rubric's nine boundary questions return the identical band to a design and its deliberately degraded twin, 12 paired scorings out of 12, against an instrument that changes its own answer 17% of the time on unchanged text.**

### Measured
- **The corpus is provably pure this time.** Degradation restricted to the three axes no bar reaches - ordering, emphasis allocation among conforming values, coherence. Three twins rebuilt and checked by six independent cap-checkers: **zero contradictions**. Three carried, their caps admissible because the cited values (`13 sp`, `700`, `14sp / 20dp, w500`) appear verbatim in their own clean baselines, verified by script. Building it confirmed section 33's other half: the three bar-free axes do allow a worse design that stays correct, and the other three do not.
- **Pre-cap separation is 0.0 in both passes**: clean higher 0, degraded higher 0, tied 12, p = 1.000. Not one of twelve paired scorings differs in either direction.
- **The control that makes the null readable:** across two passes with identical prompts on identical text, the pre-cap dimension read reproduces **10/12 = 83%** - matching section 25's 83.3%, now measured within one design. The instrument moves. It moves zero times out of twelve between a design and a worse version of it.
- **The contradicted-value cap is the least reproducible part of the stack**, costing **25 pp**: 83% pre-cap against **58%** post-cap. In this corpus it fired inconsistently on *pre-existing* values across three passes. Section 24 shipped it on a measured 0 -> 2 band separation; its reliability had never been measured until now.
- **A pre-registered indicator failed and is recorded, not deleted.** P4 returned 3/6 and voided the run by the letter - and it was confounded by my own change to the scorer prompt between passes, so it did not measure test-retest at all. It was replaced by P6, stated before the repeat pass and measured the only clean way (same script, same prompts, fresh agents): **10/12**. The second pre-registered indicator in a row that failed to measure what it was written for.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 34.
- **Rule 30: measure the instrument's own movement on identical text, in the same run as the effect.** A null is unreadable without it, and a null against demonstrated jitter is strong. The resolution measurement is not a limitations note - it is the control, and it belongs in the design.

### Changed
- **Item 1's premise is supported for the first time.** An artifact can pass presence and correctness and still be a worse design, and the instrument stack cannot tell: a screen that puts a definition of what a percentage is at the largest type on it and files the user's answer below six rows at row size scores exactly what its clean twin scores.
- **Phase 2 is unblocked** - a forced-choice paired comparison over this corpus, with null pairs so a judge that always finds a winner is visible. The corpus is built, verified, and carries a known direction on all six pairs.

## [1.32.4] - 2026-08-18

**Backlog item 1's gate is void, and what voided it is the finding: three of six quality degradations broke a bar without changing a single number.**

### Measured, and reported as void
- **The premise was made the gate.** Six twins were built to be worse designs while changing no value, deleting no statement, contradicting no bar, and keeping their own self-description consistent with the worse design. Then twelve artifacts - six clean, six degraded - were scored blind under opaque labels in one joint pass with the existing rubric and its contradicted-value cap.
- **P1a held: median band separation between the arms is 0.** P1b failed by its letter - the cap fired on **5 of 6** degraded artifacts against a gate of 1 - **but P1b was mis-specified**: it set an absolute threshold with no clean-arm base rate, and the cap fires on **3 of 6 clean** artifacts. A 5-versus-3 differential is not evidence the instrument reads quality. Recorded as a gap in the rule rather than backfilled into a branch that fired, following section 24.
- **Hand adjudication voids the run.** Every cap was checked against its own clean twin: two are the same pre-existing defect present in both arms, one is scorer variance on a pre-existing value, and **three were introduced by the degradation itself** - a screen title moved into an existing 13/16 role against the 22 pt minimum, existing spacing values reassigned to 12 pt between sections against the 24 pt bar, and a pattern swap that brought a different duration band with it. **Constraint 3 was violated in half the corpus**, so in half the pairs the instrument had exactly the signal it is built to catch.
- **The uncontaminated subset separates 0 of 3** - and n = 3 is below this repository's own floor of about eight cells, so it is not claimed as a result.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 33.
- **Rule 29: when you build a corpus by constraint, verify every constraint mechanically before you measure - an instruction to an agent is not a constraint.** The two constraints checked by script held perfectly (every heading and every numeric-plus-unit token survives in all six twins); the two left to the prompt did not.

### Changed
- **Item 1 stays open and is now specified.** Its premise is not refuted, but it is narrower than written: **the space of "meaningfully worse design that is still fully correct" is much smaller than the item assumes**, because the bars already encode a great deal of design quality - minimum sizes encode hierarchy, section gaps encode grouping, per-pattern duration bands encode pattern fit. The three degraders that broke a bar never changed a number; they changed which content a number applies to.
- **The redesign is concrete:** enforce the no-contradiction constraint with a checker rather than an instruction - score each twin for caps before admitting it, reject and re-degrade until it is cap-clean against its own baseline - and restrict the degradation classes to the axes no bar reaches: ordering, emphasis allocation among conforming values, and coherence.

## [1.32.3] - 2026-08-18

**Backlog items 7 and 8 rewritten. The pooled band-5 closure reproduces within 1.7 pp across two corpora; the per-dimension floor table the two items were built on does not reproduce at all.**

### Measured, not shipped
- **The hypothesis that would have merged items 7 and 8 is dead on its pre-registered rule.** The rubric's `4 -> 5` column is one question asked nine times, and section 31 found the skill writes admission criteria rather than generators - so H was that the floors are one failure shape. Nine independent raters, one per dimension, six fresh artifacts, taxonomy fixed before the run: the criterion/closed-world classes take **59.4%** of non-closures against a 70% gate and appear in **6 of 9** dimensions against a gate of 7. `no_rule_at_all` at 31% is a real competing class. H does not survive, and the items do not merge.
- **Section 31 replicated exactly.** A rater who had never seen it, and was told nothing about it, returned `Color, state, and contrast` at **0/6** - the same cell section 31 measured at 0/6. That is what makes the rest of the run readable.
- **A scoping error in this run, found by hand and reported both ways.** `docs/design-quality-rubric.md:32` exempts Mode B flows from a visual quality score; the corpus holds one flow, its rater quoted the artifact saying so, and scored nine non-closures anyway because the schema offered no `n/v`. Excluding it moves pooled closure 40.7% -> 48.9% and lifts one of P1's two clauses over its gate. **H fails the conjunction either way**, so the conclusion is robust to the error and the pre-registered numbers stand as primary.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 32.
- **Rule 28: a per-dimension rate is not a property of the dimension until it reproduces on a second corpus - and before treating any per-X rate as a property of X, check what else varied.**

### Changed
- **Items 7 and 8 lose their premise.** Two corpora, two cohorts, two tree versions: pooled closure moves **47.2% -> 48.9%**, while `Composition and spacing` - one of the four named floors - goes **1/6 -> 5/5**, and `Interaction polish and motion` goes **4/6 -> 0/5**. Only `Distinctiveness` and `Attention path` hold their place, and `Distinctiveness` is already flagged as structurally suspicious. Targeting the named dimensions would be optimising against corpus noise.
- **Output mode is a large uncontrolled factor in every per-dimension number in this series.** Mode C specs close **17/27 = 63%**, Mode A concepts **5/18 = 28%** - which is the rubric working as written four lines below its own table: *"Band 3 is where a good concept lives; band 4 is where a spec has to get to."* Section 19 records "six briefs in domains absent from the corpus" and **never records what modes they were**.
- What survives as a target is the pooled band-5 closure near **48%**, the most stable number this series has produced, read per mode - and the question worth asking is about specs at 63%, because concepts at 28% is the rubric doing its job.

## [1.32.2] - 2026-08-18

**Backlog item 3 closed. The two colour instruments never disagreed except in one place, the audit found it on paper, and the corpus measured it at total separation with a passing control.**

### Measured
- **The headline conflict was a band mismatch, refuted on paper before any corpus ran.** Three of the four scored colour indicators from section 23 (`C-role`, `C-pair`, `C-dark`) sit at the rubric's `2 -> 3` and `3 -> 4` boundaries; only `C-rule` reaches `4 -> 5`. "Colour is at 93.8%" describes band-3 and band-4 material and "colour closes 2/6" describes the band-5 closure. Both true, of different bands, never rival descriptions.
- **One dispute survived, and it is rule 8.** `C-rule` asks whether a rule is *present*; the rubric cell asks what a stated rule *returns*. Section 16 had rewritten that cell for exactly this reason - presence-shaped wording cannot be closure-tested - **seven sections before section 23 built a presence-shaped indicator for the same question**.
- **One corpus, both instruments, mutually blind, six fresh artifacts:** `C-rule` **6/6** against the rubric's `4 -> 5` **0/6**. Total separation, every artifact. The control holds: band-matched pairs agree **6/6** (`C-role` vs `2 -> 3`) and **5/6** (`C-pair` and `C-dark` vs `3 -> 4`) cell for cell, so this is not two cohorts disagreeing.
- **What the artifacts write:** all six state a rule for an unlisted colour role; none returns a value. *"A new state role must declare its three appearance values and its glyph before use."* **The skill writes admission criteria, not transforms.** A presence indicator cannot tell the two apart; the closure test cannot fail to.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 31.
- **Rule 27: a repair to one instrument does not propagate to the next instrument built beside it - check the neighbours when a cell is rewritten.** Nothing in this repository maps its instruments onto each other, which is what section 31's audit had to do by hand.

### Changed
- **Backlog item 3 is closed.**
- **A standing "do not re-assert" is corrected.** It carried *"the skill needs a colour system document - 93.8% before one existed"*. Section 23 withdrew `docs/color-system.md` on `C-dark` at 5.0/6, measured on six **craft-forcing** briefs. On six ordinary product briefs the dark transform is stated **0 times in 6** and the `3 -> 4` cell closes once. The withdrawal is not reversed on one corpus, but the evidence it rested on does not reach the case, and the question returns to the backlog as open rather than settled.

## [1.32.1] - 2026-08-16

**Backlog item 2 closes negative. The blocker 1.32.0 named turned out not to exist, the corpus it asked for was already in the repository, and a third draw with two principled repairs failed both gates from a third direction.**

### Measured, not shipped
- **1.32.0's stated blocker was wrong about this repository.** It asked for "a fresh brief set built by someone who has not seen the detector"; six of the eight goldens carry a `## Prompt` block with platform, user goal, audience and constraints, written for the calibration corpus long before this item and never run as generation prompts. Six fresh artifacts (2 x Mode A, 1 x Mode B, 3 x Mode C) were generated from them with `examples/golden/` forbidden - **verified by grepping the six transcripts**, not by the agents' self-report.
- **Two principled repairs, both confirmed on the development surfaces**: a section that argues for the design does not specify it (`Rationale for major choices`, `Alternatives considered`, `Key decision tradeoffs`, `Simplification opportunities`, `Production checks`, `Next actions` joined the stripped set); and a state synonym must name the condition or a device that exists only to express it (`progress indicator` left the `Loading` set - a budget bar is not a loading state).
- **Draw 3 failed both gates: false positives 1/6 against a gate of 0, and in-scope detection 4/6 against a gate of 5.** Three failures, three blind spots, none of them the repaired one: a state defined in a **markdown table row** was invisible to the bullet parser and flagged as missing on correct work; `"Context defaults applied"` satisfied the `Default` state; a submit `spinner` masked a deleted `Loading`.
- **2 of 5 fresh Mode C outputs render `## State definitions` as a markdown table** with zero top-level bullets, while `skill/templates.md` prescribes a bullet list. A slot check flags them and they are right - a table is the better shape for a nine-state matrix. Changing the template to make a validator's parsing easier is rejected explicitly rather than left open.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 30.
- **Rule 26: a machine check can verify that a state has a slot; it cannot verify that a state is defined.** Three consecutive principled repairs each closed one word sense and exposed another - a widget name, a design-failure noun, a heuristic citation, a configuration default, a submit affordance - and the one format-independent leg was beaten by a markdown table. When an instrument's failures keep arriving from a different direction each time, the question is not under-specified, it is out of class.

### Changed
- **Backlog item 2 is closed, negative.** State coverage is not checkable from the author's seat (7/12 and 4/12, 1.31.0) and not checkable by a keyword machine (three draws, both gates missed each time). The instrument that owns the class is the outside reviewer, measured at 6/6 on planted state deletions in section 24, and the seam for it already exists unused: `run_generation_eval.py --generate-command` has still never run with a real model behind it. A judged check, not a scanned one, is the next move.

## [1.32.0] - 2026-08-16

**A state-coverage machine check was built, wired into both seams, injection-verified on four breakages, measured against two pre-registered rules, and reverted because it met neither. Two hand-verified gaps in the calibration corpus ship on their own evidence.**

### Fixed
- **`examples/golden/checkout.md` defines an Empty state.** Its `## State definitions` section listed Default, Loading, Error and three domain states and omitted the one required state a checkout can actually reach - every item unavailable. A UI-spec exemplar whose state section skips a required state teaches the skip (rule 1).
- **`examples/golden/onboarding.md` names why its Production readiness sits at band 2**: the four recovery paths cover permission, abandonment and validation but not a failed network call at the account or sync step, and no step defines a loading treatment for the first write. The band was already 2; the derivation did not say why. The gap is kept deliberately so the corpus carries a band-2 production read.

### Measured, not shipped
- **The check does not ship.** Detection was pre-registered at >= 8/12 raw and measured 3/12 and 5/12 across two draws; a second rule fixed before the second draw asked for >= 5/6 on in-scope deletions and measured **4/6**. Pooled across draws the in-scope number is 8/10 with **0 false alarms across 16 clean opportunities** - a framing that was never registered, and two that were both fail. The detector, its seam into `check_response()`, and a golden declaration guard were written, wired, verified by four injections, and reverted.
- **Both misses are one defect**: the whole-document fallback matched a state word used in another sense - "Linear progress indicator" on a budget row read as Loading, "this surface's most common failure is over-filtering" read as Error. That fallback is what buys the zero false-positive rate, so it **buys 0/16 false alarms and costs 2 of 6 detections**. The trade is measured, not assumed.
- **The audit relocated the item before anything was written.** All five hand-verified state gaps in the repository are in `examples/golden/`; none is in the six example responses `check_response()` reads. A check wired only into that seam would have shipped green with no observed true positive.
- **A probe written from the name of the concept flags 14 of 14 artifacts**, demanding `stale` on a portfolio summary and `permission-denied` on an email field. Written with the bar text in hand it flags 6 of 14. Rule 12, reproduced on demand.
- **The goldens must not be held to the bar they calibrate.** `enterprise-saas` names its own missing loading and error states as the reason it derives 3/5. A blocking state check over the corpus would force every golden to Production readiness >= 3 and delete the low band that 1.31.0 restored. The shape that fits is a declaration check - a golden may carry a deliberate gap, it may not carry one silently - built, correct on all three live cases, and not shipped because it cannot run without the detector.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 29, and two rules.
- **Rule 24: the deletion that is easiest to hide is the deletion of a conditionally-required state, and a conditional requirement is exactly what a static check cannot enforce.** Five of six blind mutators reached for `Offline` unprompted - "leave no seam" selects for the peripheral condition and "must be mechanically checkable" rejects it. The corollary is harder: a check holding one artifact and no baseline cannot tell "this never needed an offline state" from "this used to have one".
- **Rule 25: the same text is evidence against a definition and evidence for a declaration.** An artifact's self-assessment must be stripped before asking whether a state is defined - read it, and the instrument passes every artifact honest enough to confess its own gap, which is exactly what the first build did.

## [1.31.0] - 2026-08-16

**Two goldens claimed 5/5 and derive 3/5 and 2/5. A README guard for the class that let three files ship unlisted. And a rewrite of the gate's weakest question, measured worse and reverted.**

### Added
- `validate_readme_enumerates_shipped_files()` - every `docs/*.md`, golden, visual-review fixture and domain pack must be named in `README.md`. 1.30.1 repaired three files that shipped between 1.26.0 and 1.27.0 while all 32 validators passed, because none of them reads the README's enumerations. Verified by four injections including a replay of the exact miss.
- `docs/proposals/quality-and-diversity-upgrade.md` section 28, and **rule 23: two failed attempts at the same instrument question are evidence about the question's class, not an invitation to a third wording.**

### Fixed
- **`examples/golden/enterprise-saas.md` claimed 5/5 and derives 3/5**, twice, by two independent scorings. Production readiness sits at band 2 - the spec offers "bottom sheet or detail screen" instead of choosing one, and a live-data queue defines neither a loading nor an error state. Label corrected with the blocker named.
- **`examples/golden/health.md` claimed 5/5 and derives 2/5**, twice. Context and brand fit is at 4 and the value/unit/range triad is a real owned asset; Typography craft is at band 1 with no type role named at all, Interaction polish at 1, and a network-fetched clinical value carries no fetch states. Label corrected with the blocker named.
- Both now carry a note that the number is derived and was scored twice. Rule 1 is why this matters: two exemplars claiming the top band without the bands to support it teach the model to claim it.

### Measured, not shipped
- The old backlog claim that the goldens read lower than their label was **too pessimistic**: 6 of 8 match their derivation exactly, 2 over-claim, none under-claims. The two over-claims are exactly the two 5/5 labels.
- The gate's `missing_state` question, at 7/12 in 1.29.0, was rewritten as a roll-call - enumerate the required states, point at the section defining each - and scored **4/12 at equal n**. Reverted. A roll-call gets a formal answer: the author points at where a state is mentioned without checking it is defined, and a deleted state is the only one of the four gate conditions that leaves no trace on the page. The same class scores 6/6 for an outside reviewer.
- The gate is unaffected: the categorical cell still blocks 6/6 in both new draws, carried by `invented_given` and `accessibility_hard_rule` at 6/6 each. State coverage wants a different instrument, not a third wording.

## [1.30.1] - 2026-08-16

**README drift repair: three files shipped between 1.26.0 and 1.28.0 were never added to the README's reference lists or its directory tree.**

`docs/motion-system.md` (1.27.0), `examples/golden/tablet-list-detail.md` (1.26.0) and `examples/visual-review-fixtures/ipad-team-inbox-stretched-phone.md` (1.26.0) were registered in the validators and in their own index documents, and every validator passed - none of them reads the README's enumerations, so the omission was invisible.

### Fixed
- `docs/motion-system.md` added to the README's reference list, its inline API snippet, and the directory tree.
- The tablet golden and the stretched-phone fixture added to the directory tree.

### Not guarded
- Nothing checks that the README's three enumerations match the files on disk. A validator asserting that every `docs/*.md` appears in `README.md` would have caught all three and is a genuinely mechanical check, unlike section 27's semantic gap. It is not in this release because the release is a documentation repair, and a new guard is a change that should be measured against the class it claims to cover rather than bolted onto a typo fix.

## [1.30.0] - 2026-08-16

**The repository's most common inter-instrument disagreement, closed by scoping the bar that caused it: 9/12 correct decisions to 12/12, with detection of real violations unchanged.**

Three runs produced the same argument — contiguous list rows against the 8 pt gap bar, 4 pt between chips, a 32 pt segmented control against the 44 pt minimum. Twelve probes with ground truth fixed in advance, six legitimately within scope and six genuine violations, one judge each:

| | false positives on the 6 correct decisions | detection on the 6 violations | accuracy |
|---|---|---|---|
| bars as they stood | **3/6** | 6/6 | 9/12 |
| bars scoped and annotated | **0/6** | 6/6 | **12/12** |

Every baseline false positive was the same one: the gap bar applied to a repeating structure — contiguous list rows, a calendar grid, an edge-to-edge tab bar. All three are how HIG and Material 3 ship those components.

### Changed
- **The gap bar states what it protects against**: a mis-tap that costs the user something different from what they intended. Two questions decide it — do the neighbours carry different consequences, and is either at or under the size floor. A repeating structure whose cells each clear the floor needs no inter-cell gap. Destructive-adjacent-to-primary is explicitly not waived by this.
- **The hit-region qualifier moved into the touch-target section** from a subsection forty lines below, and gained the clause the disputes needed: when the drawn size is below the minimum, **state the hit region**. "Segmented control, 32 pt" with nothing further will be read as a violation, correctly - nothing in it says otherwise.
- **Floor or default is marked** on every touch and contrast row where the distinction has been disputed, with both costs stated: a default read as a floor flags correct work, a floor read as a default ships a defect.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 27, and **rule 22: when two instruments keep disagreeing about the same rule, the rule is the defect — but audit before rewriting it, because half of these disputes are a qualifier nobody could find.** One of the three instances was already answered in the file, in its own subsection, referenced by nothing.

### Corrected
- Section 26 said the cap that flagged the 32 pt segmented control was wrong and the gate that passed it was right. The probes show a stated hit region is found by the unmodified file, so with **no** hit region stated the scorer was judging what was written and the gate was supplying a fact the draft never gave. Neither was wrong; the draft was underspecified, and that is now what the bar asks authors to fix.

### Not guarded
- No shape check reaches a bar's scope, and a validator asserting the word "floor" appears in a table would pass the next over-broad bar as easily as this one. The regression protection is the recorded measurement; the probes are not committed because nothing in the repository reads them.

## [1.29.0] - 2026-08-16

**The mandatory self-review pass can be passed again. Four blocking questions instead of forty, validated on a fresh three-cell corpus where the falsifier cell is the one the old gate failed.**

`docs/self-review.md` required "a confident yes on every applicable prompt" across ~40 questions, several unanswerable as yes by construction. 1.28.1 measured the consequence - "revise" on 9 of 9 drafts - and reverted a five-question fix that blocked 6/6 good drafts. This is the fix that passes.

The principle was written before the corpus, so the change is not fitted to the run that suggested it: **block on what is never right, score down what is usually wrong.**

Eighteen artifacts, six fresh briefs, each mutated twice. Cell B carries five contradicted-value defects per artifact and **no** categorical failure - it is the falsifier, because a gate that blocks it is the old saturated gate with fewer questions. Both draws agreeing, 17/18 = 94.4% draw-to-draw:

| cell | blocked | pre-registered |
|---|---|---|
| A good | **0/6** | <= 1 |
| **B contradicted-value only** | **0/6** | <= 2 |
| C categorical | **6/6** | >= 5 |
| improvement pass, good arm | median **12.5** edits | >= 6 |

The class the gate stopped blocking did not become unowned: the rubric cap caps **6/6** of cell B, median 2/5 against the good arm's 4/5.

### Changed
- `docs/self-review.md` runs two tiers. A **blocking gate of four questions** answered in writing - invented given, missing required state, accessibility hard rule, contract and header honesty - and everything else as an **improvement pass that never blocks**. A "no" there is the next edit, not a reason to withhold the response.
- `contradicted value` is explicitly **not** a gate question. It moves to the improvement tier with a hand-off to the contradicted-value cap in `docs/design-quality-rubric.md`, because sometimes the input requires the deviation and sometimes the bar's scope does not reach the case - and a gate that cannot tell those from an exemption plea blocks correct work.
- The maintenance rule now states the gate's entry condition: a prompt joins it only when a good draft answers it cleanly, the answer is checkable against the draft rather than judged, and the condition has no legitimate version.
- `SKILL.md` step 10 and `docs/workflow.md` mirror the two tiers; the unreachable rule is gone from all three files.
- Every prompt is kept. P1-10 proposed cutting the list; 1.28.1 measured the prompts catching 83% of planted defects and producing 9-13 real edits per draft, so the tiers changed and the prompts did not.

### Measured and not hidden
- **`missing_state` catches 7 of 12.** A deleted required state was injected into every cell-C artifact; that question found it barely more than half the time. The blocking is carried by `invented_given` and `accessibility_hard_rule`, both 12/12.
- **One false positive in 24 runs** across cells A and B: a 4 pt gap between chips, read as an accessibility hard rule in one draw and a spacing-bar contradiction in the other.
- **`0/6` on the good arm is not "the good drafts are clean."** The scorer capped two, including a real 32 pt segmented control against the 44 pt iOS minimum that the gate missed in both draws.
- **A recurring dispute now has three independent instances** - contiguous rows against the 8 pt gap bar, 4 pt between chips, and a 32 pt segmented control that is both below the 44 pt bar and the platform's own default height. Which bars are floors under every component and which are defaults a platform component may sit under is unwritten, and every instrument in the repository inherits the split.

## [1.28.1] - 2026-08-16

**The self-review pass catches 83% of planted defects. Its exit condition is unreachable, so it blocks everything. Two fixes were written, measured, and reverted; nothing ships to instruction text.**

| | detection of injected defects, same keys as 1.28.0 |
|---|---|
| Mode D review | 34/36 = 94.4% |
| self-review, author's seat | **30/36 = 83.3%** |

The prompts work. The gate does not: *"Only return the response after every applicable prompt has a confident yes"* across roughly forty questions, several unanswerable as "yes" by construction. A gate that never opens is no gate - the ways past it are an infinite loop and a silent override.

A two-tier rewrite (five reachable blocking questions answered in writing, every other prompt demoted to a non-blocking improvement pass) blocked 6/6 defect-injected drafts and kept 11 improvement edits on the median good draft - and blocked **6/6 good drafts too**, against a pre-registered ceiling of one. Reverted.

Adjudicating those six by hand put the real base rate of bar contradictions in shipped-quality output at **2 of 6, not 5 of 6**. One block was a false positive worth the whole run: a draft arguing that the 8 pt gap between *independent* tap targets does not govern adjacent rows of one list carrying the same consequence. That is an argument about a bar's scope, not a request for an exemption, and 1.28.0's contradicted-value cap cannot tell them apart.

Narrowing the cap to admit a scope exit held the 2-band separation and lost a hand-verified contradiction (W05) in **both** of two draws. Reverted as well.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 25 - both phases, the hand adjudication of every good-arm block, and **rule 20: a defect observed in one instrument does not license a fix in another.** The scope conflation was real in the self-review gate; the rubric scorer never had it, and patching the text they share cost a true positive in the instrument that was working.
- **A scorer test-retest number the repository did not have: 10/12 = 83.3%** on identical text, two cells flipping by one band - almost exactly the applier's 85.2%.

### Changed
- Nothing behavioral. `docs/self-review.md`, `SKILL.md`, `docs/workflow.md` and `docs/design-quality-rubric.md` are byte-identical to 1.28.0.

### Corrected
- 1.28.0's subsidiary claim that the cap catches a contradiction in two of six real outputs rests on one draw per cell. The **defects** in those two artifacts are hand-verified and real; whether the scorer catches them on a given run is subject to the one-in-six flip rate measured here. The headline - 0 bands to 2 - is far outside that and stands.

### Still open
- The unreachable exit condition remains in the shipped `docs/self-review.md`. The diagnosis is measured; no fix has passed its own test.
- The narrower gate the phase-3 data suggests - dropping `contradicted value` from the blocking tier, keeping the four that fired on 1 of 6 good drafts - is post-hoc, computed from the run that would justify it, and needs a fresh corpus.

## [1.28.0] - 2026-08-15

**The Mode D review names 34 of 36 deliberately injected defects. The score those same reviews produce separates the arms by zero bands. One cap closes the gap: 0 -> 2 bands.**

Twelve artifacts, six of them real v1.27.0 output and six their defect-injected twins - six defects each, every one replacing a value rather than deleting a statement, so every presence indicator that fired before still fires. Ground truth known by construction.

| instrument | good | mutated | separation |
|---|---|---|---|
| Mode D review, defects named | - | **34/36 = 94.4%** | - |
| rubric score as it stood | 4 4 4 4 4 4 | 4 3 4 4 4 4 | **0 bands** |
| rubric score with the new cap | 4 4 3 3 4 4 | 2 2 2 2 2 2 | **2 bands** |

The diagnosis is in the rubric's own sentence: *"a band records what the artifact states."* All thirty-six boundary questions ask whether something is stated - named, decided, valued, generalised - and none asks whether it is right. In twelve scorings under the old text, **not one cap fired at all**.

**Two of the six real outputs were capped too, and both are true positives** checked by hand: a 1.083x adjacent-role type ratio against the 1.125x bar the same spec cites, and an action bar at safe area + 8 pt that names the 44 pt home-indicator bar it breaks. The old score gave both 4/5.

### Added
- **Contradicted-value cap** in `docs/design-quality-rubric.md`: a stated value or pattern choice that contradicts a bar in `docs/quality-bars.md`, a Use-when / Avoid-when rule in `docs/patterns-catalog.md`, a curve semantic in `docs/motion-system.md`, or the resolved default in `docs/context-defaults.md` caps at **3/5**; two or more, or any one against a touch-target, contrast, or state-coverage bar, caps at **2/5**. **A stated reason does not lift it** - every artifact that fails this way carries one, and that is what makes a wrong value read as a decided one. The only exit is a deviation the user's own input requires, named with the input that requires it.
- A line in the final scoring method: checking the caps means reading the artifact's emitted values against the bars they claim to respect. A cap nobody looked for is a cap that never fires.
- `examples/evals/rubric-score-3-contradicted-value.json` - a fixture whose nine bands are all earned, median 4, expected score 3. A judge that walks the boundary questions and never checks an emitted value returns 4 here. Registered in `RUBRIC_EVAL_FIXTURES` and verified by injection: flipping its `expected_cap` to "no cap" fails the pack.
- `docs/proposals/quality-and-diversity-upgrade.md` section 24 - the corpus, both phases, and rules 19: an instrument built out of presence questions does not become a quality instrument by being applied more carefully, and when the finding half of one instrument names 34 defects the scoring half ignores, the fix is a wire between them.

### Changed
- `docs/quality-bars.md`'s deviation policy now says what stating a reason does and does not buy, so it no longer reads as an exemption from the cap.
- Scores will move. An artifact whose emitted values contradict a bar now scores lower than the same artifact did under 1.27.0; that is the intended effect and it applies to reviews, to generated calibration blocks, and to the judge.

### Measured and not claimed
- `docs/self-review.md` returns "revise" on 9 of 9 artifacts across both arms. It discriminates nothing. Recorded as an open item rather than patched in the same release that measured it.

## [1.27.0] - 2026-08-15

**The first intervention in this series that moves the outcome it was measured on: +32.5 pp. It also costs five colour cells, and that is reported rather than absorbed.**

P1-2, the craft substrate. Fourteen indicators over six craft-forcing briefs, pre-registered with the decision rule, both arms coded together in one blind pass (156/168 = 92.9% coder agreement).

| tier | baseline | post | delta |
|---|---|---|---|
| target - the ten indicators the substrate supplies | 28.5/60 = 47.5% | **48.0/60 = 80.0%** | **+32.5 pp** |
| `C-honest` guard - no invented brand value, no ratio asserted as measured | 6.0/6 | 6.0/6 | 0.0 |

Tracking at size went 0.0 to 6.0, named platform curves 0.0 to 5.0, role-to-platform-style mapping 1.5 to 6.0, baseline grid 1.0 to 5.0.

**An early-stop gate ran before any of it was written**, and its profile redefined the item: colour - the piece the proposal lists first - was already at 93.8% before a file existed, with zero honesty violations. `docs/color-system.md` was **withdrawn on the data** rather than written, and Mode E was left alone because renaming a primary mode is a MAJOR bump that nothing here pays for.

**The lever was the request, not the document.** Named curves scored 0 of 6 because step 5.5 asked for "one recurring transition, its duration taken from `docs/quality-bars.md`" - duration only - and the bars offered "ease-out" as prose. A substrate document alone would have been inert by construction.

**The cost.** All four colour indicators fell, 22.5/24 to 17.5/24, at flat response length (23,617 words against 23,297). Half of it is one brief - a typography-and-spacing-system request where colour was never in scope and the room went to the tracking table instead. Each drop is inside the pre-registered noise band; four indicators moving together is not.

### Added
- `docs/motion-system.md` - the curves the bars never carried: M3 easing tokens with their control points and the note that `emphasized` is not a single cubic-bezier; SwiftUI spring presets with the warning that they default above this skill's ceiling; Compose `dampingRatio`/`stiffness` constants; when a spring beats a tween; how duration scales with travel distance and element size; stagger caps (20-40 ms per item, 200 ms budget, first 5-7 items); the reduced-motion replacement table. Durations stay in `docs/quality-bars.md`, which the file defers to explicitly.
- `docs/quality-bars.md`: `Role to platform text style` mapping every role to an iOS Dynamic Type style and an M3 type role; `Tracking at size` with the direction rule per size band and the requirement that a custom face supply its own table; type ratio by density anchored at body 17 pt / 16 sp; `Baseline grid` with the rule that line-height boxes round to a multiple of 4 before spacing stacks against them; `Columns and gutters`; `Optical alignment`.
- The motion-band validator now covers `docs/motion-system.md`, requires it to defer to the bars for durations, and requires the four files that route motion decisions to point at it. All three halves verified by injection.
- `docs/proposals/quality-and-diversity-upgrade.md` section 23 - the gate, the withdrawal of the colour document, the contrast, the displacement cost, and rule 18: when you add substrate to one area, measure the areas you did not touch.

### Changed
- Step 5.5's motion signature must now **name** its curve - an M3 easing token, a `cubic-bezier`, a SwiftUI spring preset, or Compose damping/stiffness. "Ease-out" is a family, not a value. Mirrored in `docs/workflow.md`, `docs/design-quality.md`, and the `Signature transition` section of the bars.
- `SKILL.md` loads `docs/motion-system.md` for motion work.

### Withdrawn
- `docs/color-system.md`, and the broadening of Mode E to colour. The gate measured colour at 93.8% before either existed. Recorded rather than deferred: the item as written in section 3 was wrong about where the gap was.

## [1.26.0] - 2026-08-14

**P1-8 ships, and its premise was wrong. The model never chose bottom navigation at 1366 pt — it scored 36 of 36 on the control tier without section 15. What section 15 actually fixes is a citation the skill could not support.**

Six tablet-forcing briefs, one response per brief per arm, thirteen binary indicators pre-registered with the corpus and the decision rule before the baseline ran. Every response double-coded blind: 155 of 156 cells agreed (99.4%).

| tier | baseline | post | delta |
|---|---|---|---|
| A - the six tablet rules `SKILL.md` already states | **36/36 = 100%** | 36/36 = 100% | 0.0 pp |
| B - the seven decisions section 15 was written to add | **37.5/42 = 89.3%** | 36/42 = 85.7% | -3.6 pp |

Tier B's baseline was above the ceiling threshold in the pre-registered rule, so **the instruction-effect claim is withdrawn and no behaviour change is claimed.** The whole Tier B delta is one response moving two cells, which the pre-registration calls noise.

What the run did find: baseline responses cite `docs/patterns-catalog.md` as the source of their large-screen pattern choice - *"the list-detail/record-detail pairing `patterns-catalog.md` and the SaaS pack imply for this surface"* - while that file contained zero occurrences of `list-detail`, `sidebar`, `navigation rail`, `tablet`, or `Split View`. Step 5.5 requires that provenance; it was pointing at absent content, and every shape check in the repo passed because the citation is well-formed. Section 15 makes it true.

### Added
- `docs/patterns-catalog.md` section 15, `Large-screen and adaptive patterns` - eight decision matrices in the catalog's existing Use-when / Avoid-when / Trade-off / Red-flag shape: canonical layout with its collapse rule, detail-pane empty state, supporting pane against sheet, tab and popover, primary navigation by width, overlays by size class, action placement across pane and window toolbars, columns and reading measure, and cross-pane drag. Step 8 routes every pattern-level decision to this file and Mode D checks observed patterns against its rules.
- Five large-screen rows in the section 14 platform-divergence table, with the note that the component and API names there are library- and OS-version-bound.
- `examples/golden/tablet-list-detail.md` - a Mode C cross-platform tablet spec, registered in `docs/golden-examples.md`, `GOLDEN_EXAMPLE_FILES`, and `GOLDEN_EXAMPLE_AREAS`. Its score is derived from the dimension bands and names the two dimensions holding it there.
- `examples/visual-review-fixtures/ipad-team-inbox-stretched-phone.md` - the stretched-phone iPad fixture: a phone layout centred in 1366 pt under a full-width bottom tab bar, registered in `docs/visual-review-fixtures.md` and `VISUAL_REVIEW_FIXTURE_FILES`.
- A `Signals:` line and eleven numeric rows on the tablet section of `docs/context-defaults.md`, deferring to `docs/quality-bars.md` for the numbers it repeats.
- `validate_large_screen_coverage()` - scoped to the defect class rather than the file it was found in: every decision surface the workflow routes a design choice to must carry the device-class layer, and any width-class threshold stated anywhere must match the breakpoints in `docs/quality-bars.md`. Both halves verified by injection.
- `docs/proposals/quality-and-diversity-upgrade.md` section 22 - the pre/post design, the ceiling, the false-citation finding, and rule 17: measure a surface's coverage before writing content for it, and let the audit move the prediction rather than the conclusion.

### Changed
- `SKILL.md`, `README.md`, `docs/design-quality-rubric.md`, and `docs/evals.md` name the tablet golden in their golden-example area lists.
- `docs/adaptive-layout.md` points at section 15 for the decision matrices it does not carry.
- Nothing behavioral is claimed, for the fifth release running - but for the first time the null was predicted by a coverage audit before the run rather than found after it.

### Fixed
- `docs/adaptive-layout.md` gave the two-pane minimum at medium width as `~340 dp` while `docs/quality-bars.md` gave `>= 320 dp`. They now agree, and the new validator catches the next divergence.

## [1.25.4] - 2026-08-14

**Context is a precision filter, not a suppressor. The third hypothesis about the band-5 gate dies, and 1.25.3's decomposition is corrected.**

Three arms in one cohort — a judge holding the whole artifact, one holding the brief plus the nine extracted passages, one holding the passages alone — six briefs, three judges each, 54 agents, structurally identical. Ground truth is the blind applier on an ordinary blind-written case, 23/54.

| scorer | band 5 | recall | over-claims | precision | phi |
|---|---|---|---|---|---|
| the artifact's own claim | 13/54 = 24.1% | 9/23 | 4 | **0.692** | **+0.340** |
| judge, whole artifact | 47/162 = 29.0% | 32/69 | 15 | 0.681 | +0.330 |
| judge, brief + passages | 53/162 = 32.7% | 31/69 | 22 | 0.585 | +0.224 |
| judge, passages only | 59/162 = 36.4% | 31/69 | 28 | 0.525 | +0.152 |

The ordering predicted by context volume is exactly right and it means the opposite of what was predicted. Stripping the artifact away raises the band-5 rate and recovers **no** load-bearing statement — recall 31/69 against 32/69 — while every extra award is a false positive. Context removes false positives at no cost in recall, and the drafting side, holding more context than any judge, is the **most precise scorer of the four**.

Recall does not move for anything this series has tried: 32/69, 31/69, 31/69 here, 34/69 and 40/69 in 1.25.3, 9/23 for the drafting side. That looks like two different questions disagreeing rather than any scorer failing.

### Fixed
- 1.25.3's decomposition of the under-firing took judge 1 as the judging surface. At the median of three judges the judging side is 15/54, not 18/54, so the split is 10 cells against 8 and the drafting side does not carry it — a two-cell difference, inside the measured 1-in-7 cohort flip rate.
- Not every band below 5 is a closure-test failure: a dimension failing an earlier rung never reaches the question, while the blind instrument only tests the 4 -> 5 property. One of the 23 determined cells never reached it, so the real disagreement is 12 cells rather than 15.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 21 — the three arms, the recall-stability table across every arm in the series, and the record that three hypotheses about this gate are now dead: who runs it (1.25.2), how it picks its case (1.25.3), and how much context it holds (here).

### Changed
- Nothing behavioral, for the fourth release running.

## [1.25.3] - 2026-08-14

> **One claim below is corrected in 1.25.4.** The decomposition "10 cells on the drafting side and 5 on the judging side" took judge 1 as the judging surface; the median of three judges is 15/54, so the split is 10 against 8 and the drafting side does not carry it. Everything else here stands.

**The gate's under-firing is not case selection, and enforcing the constraint that does explain it makes the gate worse. Nothing ships.**

Each of 54 cells has one statement and two closure cases — one written from the brief by an agent who never saw an artifact, one chosen by a judge holding the artifact. Both sets were re-rated in one pass by one cohort, so the comparison is not confounded with rater drift.

**The hypothesis is wrong.** Self-chosen cases close 20/54 against the blind-written 23/54, McNemar p = 0.58, and they are not edge cases either (49/54 ordinary against 52/54, p = 0.44). What separates them is specification: 16 words against 83, and inside the self-chosen arm the cases that fix every other input close 17/36 = 47.2% while those leaving a second input open close 3/18 = 16.7% (p = 0.038). Scope differs between the origins and predicts nothing inside them (p = 0.74).

**The judge is not the problem.** Its band decision matches the blind verdict on its own case in 48 of 54 cells — and 88.9% is at the instrument's ceiling, because this run also measured the instrument against itself for the first time: a fresh cohort reproduced the original verdicts on 46 of 54 blind pairs, **85.2%**. A cell-level verdict flips about one time in seven. The under-firing is 10 cells on the drafting side and 5 on the judging side.

**The intervention hit the mechanism exactly and moved the outcome the wrong way.** Six artifacts, two instruction variants, three judges each, 108 cases screened blind to variant:

| | as shipped | plus constraint 3 |
|---|---|---|
| case fixes every other input | 6/54 | 52/54 (p < 1e-5) |
| case length | 18 words | 31 words |
| determinacy of the judge's own case | 37.0% | 42.6% |
| band-5 awards, three judges | 35.2% | 32.1% |
| recall against an ordinary blind case | 40/69 | 34/69 |
| over-claims | 17/93 | 18/93 |
| phi | +0.411 | +0.317 |

The clause binds as designed — the cases become well-specified and their determinacy rises to exactly the rate of cases written by someone who never saw the artifact. And the judge, holding better cases, awards fewer band 5s and misses six more load-bearing statements, with over-claims flat. Constraint 3 exists to prevent false negatives; at the only surface where it has ever been measured, enforcing it produces them.

### Added
- `docs/proposals/quality-and-diversity-upgrade.md` section 20 — the paired case design, the reliability measurement, the intervention arm, and the two instrument findings.

### Changed
- Nothing behavioral, for the third release running, and the second time the measured effect of a well-motivated change was the opposite of its intent.

### Note against the rubric
- Constraint 3 of the band-5 closure test stands, and its standing is worse than section 15 left it. It was already the weakest of the three, resting on one 2-1 split, and the one place it has now been measured it costs recall. Removing it would be an unmeasured change in the other direction, so it stays and this is recorded against it.

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
