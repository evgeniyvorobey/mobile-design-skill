# Proposal: quality ceiling and design diversity upgrade

Status: **complete through v1.20.0.** Every P0, every P1 and P2-1/P2-2 have shipped; see §§7–11 for what each release achieved and §12 for what remains. Releases: v1.17.0 (ceiling, tablet, honesty), v1.18.0 (A3 — catalog retrieval), v1.18.1 (`skill/skill.md` retired), v1.19.0 (generation eval), v1.20.0 (diversity eval).

**Read §12 first if you are picking this up cold.** The P-tables below record the plan as written; several rows were corrected after measurement and the correction, not the row, is what shipped.
Baseline: v1.16.0 (`b192ecd`).
Target release: v1.17.0 — *"the ceiling comes off"*.

Companion record to [`review-mode-upgrade.md`](review-mode-upgrade.md), which shipped the Mode D causal-review format in v1.16.0.

---

## 1. Why

Two owner-reported symptoms, one audit:

1. **Output quality plateaus.** Every generated artifact lands at the same competence level.
2. **Designs are interchangeable.** Two runs of the same prompt produce the same screen.

A six-dimension audit (design diversity, tablet/adaptive capability, runtime reachability, craft depth,
enforcement machinery, comparative scope) with an adversarial verification pass produced 38 findings that
survived refutation. This proposal records the causes, the fix order, and the explicit non-goals.

The audit's own bias check: the previous release already survived a senior review that caught over-claiming
(`b192ecd`). Nothing here weakens the evidence discipline — the fixes add generators and instruments, they do
not relax guardrails.

---

## 2. Root causes

### 2.1 The v1.16.0 Mode D contract never reached the entrypoint

`SKILL.md` is the always-loaded file. `skill/modes.md` loads conditionally. The v1.16.0 Mode D rewrite landed
in `skill/modes.md`, `skill/templates.md`, `docs/self-review.md`, `docs/evals.md` and
`scripts/validate_repo.py` — but `SKILL.md`'s `## Mode output requirements` kept the pre-1.16 bucket shape
(`Usability issues` / `Accessibility issues` / … / `Severity or priority` / `Recommended fixes`).

Consequence: the model drafts the old shape from the entrypoint, then the mandatory self-review
(`SKILL.md` step 10 → `docs/self-review.md`) fails it and forces a blind rewrite toward a target the
entrypoint never described. Wasted draft, under-specified target.

This is the second consecutive release in which the entrypoint was the file the feature forgot. The structural
condition is that three files each claim to describe the workflow (`SKILL.md`, `skill/skill.md`,
`skill/modes.md`) with no parity check between them.

### 2.2 The quality ceiling is nailed shut at 4/5

`skill/templates.md` pre-prints `- Quality target: [4/5 by default unless context blocks it]`;
`docs/design-quality.md` repeats `- Quality target: 4/5`. A model filling a slot that already contains the
number does not compute a different one. In the committed calibration corpus, 32 of 33 `Quality target:`
values are `4/5`. The only revision trigger fires from below (`SKILL.md`: revise if 3/5 or lower). The system
is a floor mechanism with the ceiling welded on.

### 2.3 Convergence is enforced four times; divergence zero times

"Never invent a novel pattern when an established one applies" is enforced in `SKILL.md`, `docs/workflow.md`,
`docs/patterns-catalog.md` and `docs/self-review.md`. **This rule is correct** for functional patterns
(Jakob's Law) and is not the bug.

The bug is that the repo's one divergence engine — the generative direction method in
`docs/inspiration-sources.md` (JTBD → HMW → Crazy Eights → de Bono → SCAMPER → translate-to-mechanism, ending
"a direction is not done until it exists as tokens, components, and states") — sits behind a gate in
`SKILL.md` listing four signals (`visual inspiration`, `moodboards`, `benchmark references`,
`best-in-class`), while the document's own trigger list has nine, including `"make it feel premium"`,
`"visual direction"` and `"explore a few styles"`.

**The gate is a strict subset of the capability it guards.** For a plain "design a screen for X" the only
exploration performed is picking a functional pattern from a catalog. Visual and compositional direction is
never enumerated, so cross-run variance equals the base model's modal mobile screen.

What *does* exist is pattern-level comparison after the fact (`docs/workflow.md`, `docs/self-review.md`,
`docs/weaknesses.md` force naming one rejected alternative from a fixed matrix). Breadth of two, from a closed
set, post-hoc. Comparison is forced; generation is not.

### 2.4 There is no token vocabulary for directions to differ in

`docs/inspiration-sources.md` names four compositional schools and nine point-of-view products — as a reading
list. No entry carries a base unit, a scale ratio, a colour-construction rule, a radius/elevation posture, a
density posture, or an icon stance. Supporting voids: no palette-construction method anywhere
(`docs/quality-bars.md` is the WCAG contrast table only); no columns/gutters/margins in the craft docs; motion
is five duration bands plus three easing names, so `docs/design-quality.md`'s "named easing curve tied to a
brand adjective" resolves to the ease-out that is already the default.

Consequence: even after 2.3 is fixed, three generated directions would differ in adjectives and not in tokens.

### 2.5 The calibration corpus is itself a sameness generator

The golden `Design quality calibration` blocks are isomorphic in shape (aphorism → hierarchy →
colour/typography → state caveat, all closing `4/5 — <adj> <noun> once <X, Y, Z> are confirmed`). No golden
block names a hue, typeface, radius, elevation, duration, or composition move. This corpus loads precisely
when taste is being decided.

### 2.6 No enforcement machinery has ever read a model output

Every check in `scripts/validate_repo.py` reads committed markdown written by hand. The CI step named like a
quality check is an oracle that echoes the expected value back. An edit to `SKILL.md` that degrades live
output cannot fail any job. There is no eval anywhere that measures diversity or distinctiveness — a perfectly
uniform corpus scores as ideal.

### 2.7 Tablet is not a platform scope

`Platform scope` is a four-value OS enum with no device class, in `SKILL.md` and all six templates. The output
contract has no `Device class:` line. `docs/patterns-catalog.md` (738 lines) has zero occurrences of
`sidebar`, `toolbar`, `list-detail`, `inspector`, `split view`, `size class` or `navigation rail`.
`docs/quality-bars.md` has no breakpoint, pane width, column count or reading-column maximum, and its thumb-reach
section is phone-only. The entire live tablet capability is a five-row table in `docs/context-defaults.md`
which — alone among the sixteen context sections — carries no `Signals:` line, so nothing triggers it.
`examples/` has no tablet artifact. Meanwhile `examples/rendered-output-qa/report-schema.json` accepts
`device_class: "tablet"`: the skill can QA a tablet layout it has no vocabulary to produce.

Verdict: **partially** — the skill can bolt a tablet note onto a phone design; it cannot design a tablet app.

Two facts that make this cheap: `docs/clarification-policy.md` already lists tablet as an ask-trigger, and the
validators do not block tablet (`Platform scope` is checked for non-emptiness, with no enum, and
`MODE_REQUIREMENTS` checks heading presence without forbidding extras). **The fix is markdown-only.**

---

## 3. Fix order

### P0 — changes output on the next run (edits inside the mandatory load set)

| # | Change | Files |
|---|--------|-------|
| P0-1 | **Un-nail the 4/5.** Replace the pre-printed target with `[score]/5 — [what makes it that, and the one dimension holding it back]`. Add a rubric rule: at 4/5, name the dimension blocking 5/5 and whether the input supports lifting it; if yes, lift it before returning. ✅ *landed in Commit 2* | `skill/templates.md`, `docs/design-quality.md`, `docs/design-quality-rubric.md` |
| P0-2 | ✅ *landed in Commit 3* **Widen the divergence gate + add Step 5.5 "Direction set."** Gate widened to the document's own nine signals. New binding step for Modes A/C/E/F: name three directions, each a thesis line plus token consequences (base unit + ratio, type role split, colour-construction rule, one composition move, motion signature); rank against task/context/platform/accessibility; commit to one; the two rejects populate `Alternatives considered`. Output stays one direction plus two named rejects. | `SKILL.md`, `docs/workflow.md`, `docs/self-review.md` |
| P0-3 | **Repair the Mode D drift at the entrypoint.** ✅ *landed in Commit 1* | `SKILL.md`, `skill/modes.md`, `docs/self-review.md`, `docs/workflow.md` |
| P0-4 | **Distinctiveness gets a score, a rung, and a slot.** Ninth rubric dimension (1–2 interchangeable once the logo is removed; 3 asserted but not tokenized; 4–5 owned asset expressed as a token with named repeat locations), `n/v` for text-only D2/D3 with the median exclusion stated explicitly. Rewrite the 3→4 ladder rung in the inert cap's own words. Add a `Signature move:` slot to the calibration blocks in Templates A/C/F. ✅ *landed in Commit 2* | `docs/design-quality-rubric.md`, `skill/templates.md`, `docs/design-quality.md` |
| P0-5 | **Sections are a maximum, not a minimum.** Only `Mode:`, `Platform scope:`, `Assumptions:`, `Next actions:` are always on; include any other section only when it carries a decision the input supports; omit — never stub — and name the omission in one line. ✅ *landed in Commit 2* | `SKILL.md`, `docs/self-review.md` |
| P0-6 | **Named output slots for alternatives** in Modes 1, 3 and 6, with Mode 1 forcing two structurally different layout approaches. ✅ *landed in Commit 2* | `SKILL.md`, `skill/modes.md`, `docs/self-review.md` |
| P0-7 | ✅ *landed in Commit 4* **Tablet MVU** — see §4. | `SKILL.md`, `skill/templates.md`, `docs/adaptive-layout.md`, `docs/quality-bars.md`, `docs/clarification-policy.md` |
| P0-8 | ✅ *landed in Commit 5* **No-fit escape hatch.** `Mode: outside the standard six — <what it is>` instead of rounding paywall/notification-frequency/whole-app-IA requests to the nearest template. | `SKILL.md`, `docs/workflow.md`, `docs/self-review.md` |
| P0-9 | ✅ *landed in Commit 5* **Auth-wall honesty.** State that Mobbin / Page Flows / UI Sources / Pttrns / Screenlane cannot be opened. Rewrite the self-review prompt that currently asks whether the model used them — it is a standing invitation to describe a screen it never saw. Add a guardrail marking version-bound rows as current-as-of-last-review. | `docs/inspiration-sources.md`, `docs/visual-benchmark-playbooks.md`, `docs/self-review.md`, `docs/guardrails.md` |

### P1 — structural, one release

| # | Change |
|---|--------|
| P1-1 | ✅ *landed in Commit 3* **Token-consequence schema for the art-direction catalog.** Convert the school/product list in place: base unit + ratio, type role split + pairing rule, colour-construction rule (neutral anchor + accent derivation + semantic roles held separate), radius/elevation/border posture, density posture, motion signature, iconography stance, "do not use for". Reconcile the motion bands first — `docs/design-quality.md` says 200–500 ms while `docs/quality-bars.md` caps navigation at 300–400 and tap feedback at 100–150, so the signature currently has no room. |
| P1-2 | **Craft substrate:** `docs/color-system.md` (platform semantic roles first, derived ramp only on user-supplied brand, any printed ratio labelled as computed); a layout section in quality bars (margins by class, baseline grid tying line-height boxes to spacing steps, columns/gutters, optical-alignment rules); motion by cited platform curves (M3 easing tokens, SwiftUI spring presets, Compose stiffness/dampingRatio) with distance/size rules and stagger caps; type-scale ratio by density anchored at body 17/16, tracking-at-size, role → iOS text style / M3 type role mapping. Broaden Mode E to "typography, spacing, and colour". |
| P1-3 | **Cross-file parity validator.** ✅ *landed in Commit 1* |
| P1-4 | ✅ *landed in Commit 6* **Rebuild the golden `Design quality calibration` blocks** to carry a named direction as tokens plus one owned asset with repeat locations, guardrail lines intact. Assert a `Signature move:` line naming a token and a repeat location, pairwise-distinct across files. Do **not** require literal hex/typeface values — that would model the invented brand specifics the skill forbids. |
| P1-5 | ✅ *landed in Commit 6* **Corpus diversity validator** over golden + example + case-study files: at most 60 % of `Quality target:` lines share a score (fails today at 32/33), and median pairwise 5-gram Jaccard of calibration-block bodies at most 0.15. First cross-response instrument in the repo. |
| P1-6 | ✅ *landed in Commit 6* **Fix the tautological CI step and the flat fixtures.** Rename the oracle step so it stops claiming to validate quality. Current rubric fixtures are 31–52 words with dimension spreads of 0,1,1,0,0 — a judge ignoring the median rule passes the whole pack. Add an adversarial fixture with spread ≥ 2 and assert `expected_score == floor(median(dimension_scores))` unless a cap is present. |
| P1-7 | ✅ *landed in Commit 6* **Shape assertions in the prose validator.** Replace bare-word matches (`\bover\b`) with bullet-count plus word-count-after-`because` assertions; replace the five-element generic-next-actions denylist with a positive test (each bullet contains a digit, a mid-sentence capitalized token, or a backticked identifier). Fix the examples, not the rules. |
| P1-8 | **Tablet full version** — see §4. |
| P1-9 | **Selection rules for the unkeyed craft bands.** Add a "Selected by" column to line length, type ratio, easing, spacing steps, edge padding, loading thresholds, skeleton-vs-spinner; add a no-bucket fallback to context defaults. Any emitted craft value names the context variable that selected it, or is labelled `default`. Do **not** add a competing numeric authority next to `docs/context-defaults.md`. |
| P1-10 | **Blocking gate in self-review.** Promote three non-template-satisfiable prompts (name the sentence you cut; name the rejected instinct; name the element that carries the direction) into a leading blocking gate answered in writing; demote the rest to a spot-check reference; cut the universal prompts to the ~8 that gate a rewrite and move the remainder to `docs/evals.md`. |
| P1-11 | ✅ *resolved: deleted in v1.18.1* **Resolve `skill/skill.md`.** 489 lines, on no load path, self-contradictory internally. Either delete it (porting the classifier hints and the "no vague advice" hard constraint into `SKILL.md`) or declare it a non-Claude-host entrypoint and bring it under the parity validator. Leaving three files that each claim to be the workflow is the condition that produced the drift in §2.1. **Owner decision required.** |

### P2 — long-horizon

| # | Change |
|---|--------|
| P2-1 | ✅ *shipped in v1.19.0* `scripts/run_generation_eval.py` reusing the proven `--judge-command` stdin/stdout contract and importing `MODE_REQUIREMENTS` unchanged; ~10 prompts × N runs. First validator that reads generated text. |
| P2-2 | ✅ *shipped in v1.20.0* `scripts/run_diversity_eval.py` — decision-vector extraction (pattern name, hierarchy sequence, component set, named alternative, emitted numbers, owned asset), cross-prompt uniqueness, rejected-alternative entropy, frame repetition. Drop within-prompt divergence from the first cut: no sampling-temperature contract exists, so a threshold is unjustifiable until baseline data exists. |
| P2-3 | **Mode G: design system + information architecture.** Destination graph, token architecture, component inventory with anatomy/variants/states/a11y contract, themeable-vs-structural split, governance, platform token mapping. Mode E stops at type and spacing, so "define our design system" currently falls into the no-fit trap and returns a type scale with no colour attached. |
| P2-4 | **Render-and-critique loop**, host-conditional: materialize a Mode A/C output as a self-contained HTML mock at 393×852 and 360×800 across default/loading/empty/error using the exact token names stated, run `docs/rendered-output-qa.md` against it, fix, return. That document is a 359-line workflow whose entry condition is an artifact the skill is never told to produce. |
| P2-5 | **`## Artifacts` block in Templates C and E** — DTCG-shaped `$value`/`$type` JSON for dimension, fontFamily, fontWeight, duration, colour, light + dark sets. Not Template A: a screen concept is pre-token by design. |
| P2-6 | **Surface axes**: glanceable (widget / Live Activity / lock screen), watch, foldable posture, RTL mirroring. Zero repo-wide hits today for RTL/bidi/mirror, watchOS, complication, always-on, while a self-review prompt fires on multilingual with no layout backing. |

---

## 4. Tablet upgrade path

### Minimum viable (six files, markdown only)

1. **Two-axis scope** at `SKILL.md` step 3: OS × device class (phone / tablet / foldable / adaptive), plus a
   signal list forcing tablet on: iPad, Split View, Stage Manager, kiosk, POS, clinician/bedside, field
   technician, classroom, Apple Pencil.
2. **`Device class:`** in the output contract, and a fourth Platform-policy branch: layout at compact *and*
   regular width plus the breakpoint, the canonical layout named, navigation per width, multitasking, input
   treated as additive.
3. **New `docs/adaptive-layout.md`** with a hard load trigger at step 3. Sources: Apple HIG Layout /
   Multitasking / Split Views; Material 3 Applying Layout + Canonical Layouts; Android window size classes.
4. **`## Large-screen and adaptive bars`** in `docs/quality-bars.md`: 600 / 840 / 1200 dp width classes (noting
   Slide Over returns iPad to compact); 640–720 pt reading column; 320–400 pt list pane; 80 dp rail;
   240–360 dp sidebar; margins 16 / 24 / 24–32; columns 2 / 4–6 / 6–8; pointer may be finer but touch minimums
   still apply (44 pt / 48 dp); resize without state loss.
5. **`Device class:`** in all six template headers, plus `## Adaptive behavior` in Templates A and C.
6. **Un-suppress the phone-first defaults**: rewrite them as reversible assumptions ("compact width only; a
   regular-width layout can be added on request") rather than closed statements.

### Full version

- `## 15. Large-screen and adaptive patterns` in `docs/patterns-catalog.md`, in the existing
  Use-when / Avoid-when / Trade-offs matrix shape: list-detail with its collapse rule, supporting pane /
  inspector, sidebar vs rail vs bottom tabs by width, popover vs sheet by size class, toolbar vs bottom bar,
  grid columns, cross-pane drag — plus rows in the platform-divergence table. **This is the item that stops
  the model confidently choosing bottom navigation at 1366 pt.**
- `examples/golden/tablet-list-detail.md` (Mode C) and one stretched-phone iPad review fixture, registered in
  the golden-example validator.
- A `Signals:` line and numeric rows on the tablet section of `docs/context-defaults.md`.
- `Device class:` in `MODE_REQUIREMENTS`; `device_classes:` in `skill/metadata.yaml`.

Do **not** lift device class above precedence rank 5 in `docs/context-defaults.md`. Precedence resolves
conflicts between context dimensions; device class rarely conflicts. The fix is a trigger, not a rank.

---

## 5. Non-goals

1. **Do not delete `SKILL.md`'s `## Mode output requirements` to force a `skill/modes.md` load.** After
   Commit 1 the six mode lists are set-identical across the two files. That section is the reason the modes
   are deterministic today; deleting it converts a working path into a conditional one and buys nothing. Lock
   the two with parity instead.
2. **Do not weaken the no-novelty rule.** It reads "never invent a *novel* pattern when an established one
   applies" — list-detail, split view, sidebar and rail are canonical HIG/M3 patterns, so the rule already
   points toward them, and `docs/patterns-catalog.md` already permits documented deviation. Sameness is a
   missing generator, not an excess of discipline.
3. **Do not enforce distinctiveness with label-presence regexes, and do not require literal hex or typeface
   values in goldens.** Adding `first instinct|initially considered|rejected:` to `MODE_REQUIREMENTS`
   reproduces exactly the defect that makes the existing shape checks weak, and a golden printing invented
   brand hexes would model the fabrication the skill forbids. Assert *shape* — bullet counts, words after
   `because`, pairwise distinctness of normalized lines — never vocabulary.
4. **Do not write a third parallel doc for anything that already exists.** Three copies of the Mode D score
   rule is what produced the drift this proposal opens with. Extend in place, or replace with a pointer. The
   same principle forbids bolting more process onto self-review: the correct move is P1-10, cutting prompts
   and adding one written gate.
5. **Do not spend effort on `skill/metadata.yaml` flags expecting behaviour change.** It is referenced only by
   README, CHANGELOG, versioning and scripts. Manifest hygiene, last.

---

## 6. Release plan (v1.17.0)

| Commit | Contents | Status |
|--------|----------|--------|
| 1 | Entrypoint repair (P0-3) + parity validator and projected-line guard (P1-3). Must land first: everything else edits the same files. | ✅ landed |
| 2 | Scoring and slots: P0-1, P0-4, P0-6, P0-5, plus the committed generation examples. | ✅ landed |
| 3 | Divergence: P0-2 immediately followed by P1-1, plus the motion-band reconciliation. | ✅ landed |
| 4 | Tablet MVU: P0-7 plus `docs/adaptive-layout.md`, the large-screen bars, `Device class:` in the six template headers and in `MODE_REQUIREMENTS`. New sources added to `docs/sources.md`. | ✅ landed |
| 5 | Honesty and scope: P0-8, P0-9. | ✅ landed |
| 6 | Corpus and CI: P1-5, P1-4, P1-6, P1-7. | ✅ landed |

Deferred at the time of writing: P1-2, P1-8, P1-9, P1-10 and the P2 tier. **Since then P1-11 (§9), P2-1 (§10) and P2-2 (§11) have all shipped**; P1-2, P1-8, P1-9, P1-10 and P2-3…P2-6 remain — see §12.

Release notes are written into `CHANGELOG.md` when the release is cut, not accumulated in an
`[Unreleased]` section: `scripts/validate_release.py` requires the top changelog entry to be a semver
version, and that gate is worth more than the convenience. Until then, per-commit notes live here.

### Commit 1 — what landed

Fixed:

- **`SKILL.md` Mode 4** replaced: the pre-1.16 bucket shape (`Usability issues` / `Accessibility issues` /
  `Hierarchy and readability issues` / `Design quality issues` / `Navigation and interaction issues` /
  `Severity or priority` / `Recommended fixes`) is gone, replaced by the eight-field structure
  (`Sub-case`, `Quick summary`, `Strengths`, `Findings`, `Design quality score (current → projected)`,
  `Severity index`, `Bold move (optional)`, `Platform-convention mismatches`, `Unresolved assumptions`) with
  the per-field contract inline and an explicit "do not use the pre-1.16 bucket shape" line.
- **`SKILL.md` scoring line** now states the projected-score rule (flat median of the assessable non-`n/v`
  dimensions, never "up to", ceiling confined to `Ceiling note`) instead of asking only for a current score.
- **`SKILL.md` step 6** is no longer an optional pointer at `skill/templates.md`. It requires the classified
  mode's `### Output structure` **and** `### Validation checklist` from `skill/modes.md`, and names
  `skill/modes.md` authoritative on disagreement.
- **`docs/self-review.md`** Mode D prompt and **`docs/workflow.md`** scoring bullet were stale third and
  fourth copies of the same rule. The self-review prompt now carries the flat-median contract; the workflow
  bullet became a pointer, removing one copy that could drift.
- **`skill/modes.md` Mode C** listed `iOS-specific and/or Android-specific implementation notes` where
  `SKILL.md`, `MODE_REQUIREMENTS` and `examples/ui-spec.md` all use `Platform-specific implementation notes`.
  Normalized, with the iOS/Android split preserved as detail after the em dash.

Added to `scripts/validate_repo.py`:

- **`validate_mode_parity()`** — parses the per-mode output fields from `SKILL.md`'s
  `## Mode output requirements` and `skill/modes.md`'s `### Output structure` blocks, normalizes them
  (detail after an em dash stripped, `/` and `or` treated alike, the four universal contract elements
  excluded) and asserts set equality per mode. This is the check that would have caught the §2.1 drift.
  It was verified by injection — reverting Mode 4 fails it, dropping a field from `skill/modes.md` fails it —
  and it caught a second, independent drift in Mode C that no one had noticed.
- **`validate_projected_score_lines()`** — every `- Projected:` line under `examples/` must state a flat
  `[1-5]/5` number and may not contain `up to` or `ceiling`. Verified by injection.

`scripts/validate_repo.py` and `scripts/validate_release.py` both green.

### Commit 2 — what landed

**P0-1 (un-nail the 4/5).** All four `Quality target:` slots in `skill/templates.md` and both snippets in
`docs/design-quality.md` now read `[1-5]/5 — [what earns this score]; blocked from [next level] by
[dimension] until [named input or fix]`. `docs/design-quality-rubric.md` gained a **Name the blocker** rule
("a 4/5 with no named blocker is a default, not a score") and its ladder now says 4/5 is the default target,
**not the ceiling**.

**P0-4 (distinctiveness gets a score, a rung, and a slot).**

- Ninth rubric dimension `Distinctiveness and owned assets`, with the `n/v` marker defined and the final
  scoring method rewritten to take the median of the **assessable** dimensions only, excluding `n/v` entirely.
- A dedicated `3 → 4 (inert cap)` ladder rung stating the cap's own exit in the cap's own words, with the cap
  and the rung cross-referencing each other so they cannot drift apart again.
- `Signature move:` slot added to Templates A, C and F and to both `docs/design-quality.md` snippets.
- The ninth dimension propagated to `RUBRIC_DIMENSIONS`, `scripts/run_rubric_judge.py`,
  `docs/llm-judge-runner.md`, `skill/metadata.yaml` and all five `examples/evals/rubric-score-*.json`
  fixtures (each set equal to its own expected score, so medians and recorded caps stay coherent — the
  adversarial spread fixture is deliberately left to Commit 6/P1-6).

**P0-6 (named output slots for alternatives).** `Alternatives considered` added to Mode 1 and
`Key decision tradeoffs` to Mode 3 in **both** `SKILL.md` and `skill/modes.md` — `MODE_REQUIREMENTS` and the
committed examples already demanded these sections, so the instructions had been requiring less than the
validator enforced. Mode 1's slot forces two *structurally different* layouts with the mechanism that kills
each. Mode 6's `Key design decisions` gained the "a decision with no rejected alternative is a default"
clause rather than a duplicate section. Matching validation-checklist and self-review prompts added.

**P0-5 (sections are a maximum).** New `### Sections are a maximum, not a minimum` block under the output
contract in `SKILL.md`, plus a universal self-review prompt. Only `Mode:` / `Platform scope:` /
`Assumptions:` / `Next actions:` are unconditional; anything else is omitted — never stubbed — when the input
does not support a decision, with the omission named in one line.

**Enforcement.** Two shape assertions in `scripts/validate_repo.py`, applied to Modes 1, 3 and 6:
`SIGNATURE_MOVE_SHAPE` (at least 8 words after the label, so the slot cannot be satisfied by the label alone)
and `QUALITY_TARGET_SHAPE` (must name what blocks the next level). These assert shape, not vocabulary, per
non-goal 3.

**Corpus.** `examples/ui-spec.md` and `examples/rationale-handoff.md` gained real owned assets — a
`motion.status-advance` token repeated in three named places, and a `color.accent-confirm` token confined to
three locations — neither of which requires inventing brand values. `examples/generate-screen.md` records the
opposite case honestly: an enterprise HR form with no brand input **is** inert, so it drops to **3/5** with
the exit condition stated. That is the first non-4/5 generation example in the corpus and the first
demonstration that the ceiling moves in both directions. `docs/evals.md` updated so a capped score is a
legitimate pass.

All three new guards were verified by injection: reverting a `Quality target` line to a bare number, reducing
`Signature move` to a label, and dropping the ninth dimension from a fixture each fail the validator. Both
validators green.

### Commit 3 — what landed

**P0-2 (widen the gate + Step 5.5 "Direction set").**

- The inspiration gate in `SKILL.md` now carries all nine signals the document itself declares, including
  `"make it feel premium"`, `"visual direction"` and `"explore a few styles"` — the three that most reliably
  mean "the user wants a direction" and that the old four-signal gate excluded.
- New `### 5.5 Set the design direction (Modes 1, 3, 5)` in `SKILL.md`, mirrored as `## Step 4.5` in
  `docs/workflow.md`. Three candidate directions, each a thesis line plus five token consequences (base unit
  and ratio, type role split, colour-construction rule, one composition move, motion signature), ranked and
  reduced to one; the two rejects populate `Alternatives considered` or `Key decision tradeoffs`.
- Four constraints keep it from becoming theatre: directions must differ in **at least two token fields**; the
  step is internal so the response never hands the user a menu; divergence is perceptual and compositional
  only, with functional pattern selection still convergent; and token values are directional defaults, never
  invented brand facts. Mode 6 names the direction the delivered design already embodies rather than
  generating new ones. Single-direction inputs are declared under `Assumptions` instead of padded with
  throwaway rejects.
- Self-review prompts added for Modes A, C and E, including one that catches the reflex 4/8/12/16/24/32/40
  spacing ladder being emitted without a reason.

**P1-1 (token-consequence schema).** The four compositional schools in `docs/inspiration-sources.md` are no
longer a reading list: each now carries base unit and ratio, type role split, colour rule, shape posture,
density, composition move, motion signature, icon stance and "do not use for". The nine point-of-view products
gained a **token consequence** column — what actually changes in the output when you take that principle. The
whole block is explicitly framed as *this skill's translation into mobile product terms, not a historical
claim about the school*, and as directional defaults overridden by any design system the user supplied.

**Motion band reconciliation.** `docs/design-quality.md` declared a 200–500 ms "personality band" while
`docs/quality-bars.md` capped full-screen navigation at 400 ms — a signature had no legal room. Quality bars
gained a `### Signature transition` section (one signature per product; top of its own band, never a band
above; never applies to tap feedback, which stays 100–150 ms; 400 ms ceiling), and the design-quality bullet
now defers to it: a brand adjective chooses *which* interaction and *which* curve, never a longer duration.

**Enforcement.** Two more cross-file contract checks in `scripts/validate_repo.py`:

- `validate_inspiration_gate_parity()` — every quoted trigger signal in the document's own list must appear in
  `SKILL.md`. This is the check that would have caught the root cause of sameness.
- `validate_motion_band_consistency()` — quality bars must define `Signature transition`, the design-quality
  motion section must defer to it, and neither file may state a motion duration above the 400 ms ceiling.

Both verified by injection: narrowing the gate back to four signals lists the seven missing signals, and
restoring the 200–500 ms band fails on both the deferral rule and the ceiling.

**Corpus.** `examples/generate-screen.md` and `examples/ui-spec.md` now show direction-level rejections with
token consequences alongside the existing pattern-level ones — the visible output of step 5.5. The shape
assertion on alternatives (word count after `because`) belongs to P1-7 in Commit 6 rather than a vocabulary
regex here.

### Commit 4 — what landed (tablet MVU, P0-7)

All six MVU items from §4, markdown-only as predicted.

1. **Two-axis scope.** `SKILL.md` step 3 is now "Determine platform scope **and device class**": platform answers *which OS*, device class answers *how much width the layout gets and what input is available*. Device class is phone / tablet / foldable / adaptive, with a 20-signal trigger list (iPad, Split View, Stage Manager, multi-window, foldable, hinge, external display, Apple Pencil, plus mounted/two-handed use contexts: kiosk, POS, clinician, field technician, warehouse, classroom, studio, control room). Stated rationale for it being a second axis rather than a fifth platform value: an iOS tablet and an Android tablet share more layout structure with each other than either shares with its own phone.
2. **`Device class:` in the output contract** and a fourth Platform-policy branch requiring layout at compact *and* regular width with the breakpoint named, a canonical layout named, navigation changing with width, multitasking behaviour, additive input, and the detail pane's own empty state. Plus the rule that breaks most tablet work: **never map a layout to a device model — map it to a width class.**
3. **New `docs/adaptive-layout.md`** (10 sections), loaded from step 3 whenever device class is not phone: device-class signals, width classes, canonical layouts with collapse rules, navigation by width, multitasking and posture, input as additive, what does not change, common failures, evidence limits, sources.
4. **`## Large-screen and adaptive bars` in `docs/quality-bars.md`**: width classes (600 / 840 dp, Android's official breakpoints, with the note that Slide Over returns a tablet to compact at runtime); reading column 640–720 pt; list pane 320–400 pt; rail 80 dp; sidebar 240–360 dp; margins 16 / 24 / 24–32; columns 2 / 4–6 / 6–8; touch minimums unchanged at every width; resize-without-state-loss.
5. **`Device class:` in all six template headers** plus a conditional `## Adaptive behavior` block in Templates A and C, mirrored into the `SKILL.md` and `skill/modes.md` mode lists (parity holds) with the conditional stated in the em-dash tail.
6. **Phone-first un-suppressed.** `skill/skill.md`'s `"phone-first flow, not tablet-first"`, `docs/clarification-policy.md`'s "can be treated as phone-first", and `examples/generate-screen.md`'s assumption are now reversible statements: *compact width only; a regular-width layout can be added on request.* Phone-first is a default, so it is flagged as one.

Also: seven canonical sources added to `docs/sources.md` under a new **Adaptive layout and large screens** heading; `adaptive_layout` block in `skill/metadata.yaml`; device-class prompts in `docs/self-review.md` and the Mode A/C validation checklists; `docs/workflow.md` step 2 resolves the axis; README reference lists updated.

**Enforcement.** The response contract check now requires a `Device class:` line, and — the part that matters — **when that line is not phone, an `## Adaptive behavior` section is required**. That directly blocks the "tablet claimed, never specified" failure: a spec that says `Device class: Tablet` with no breakpoint, canonical layout, or navigation change fails the validator. `Device class` was added to `CONTRACT_ELEMENTS` so mode parity keeps ignoring it, like `Platform scope`.

Both rules verified by injection:

```
examples/ui-spec.md: missing `Device class:` line
examples/ui-spec.md: `Device class: Tablet` requires an `## Adaptive behavior` section
```

**Known limit.** The corpus is still phone-only, so the conditional rule is proven by injection rather than by a committed artifact. The tablet golden and the stretched-phone review fixture stay in P1-8, along with `patterns-catalog.md` §15 — which remains the single highest-value tablet item after this commit, because it is what stops the model confidently choosing bottom navigation at 1366 pt.

### Commit 5 — what landed

**P0-8 (no-fit escape hatch).** `SKILL.md` and `docs/workflow.md` step 1 now carry a branch for requests that match no mode: paywall and pricing architecture, notification and re-engagement strategy, whole-app information architecture, activation strategy, competitive teardown, design-system governance, multi-brand theming. The response opens `Mode: outside the standard six — [what this actually is]`, names the closest mode and what it would lose, and answers with the workflow's reasoning steps and no template. The header lines and `Next actions` stay; the rest of the contract is advisory on this branch.

The failure being fixed is specific: rounding a strategy question to Mode 1 produces a plausible screen concept for a question nobody asked, and template completeness hides the mismatch. `examples/anti-patterns.md` gains **Anti-pattern 9** with the paywall-architecture case — the bad response is a one-screen paywall under a `Mode: Generate mobile screen concept` header, the good response is the honest branch.

**P0-9 (auth-wall honesty).** Mobbin, Page Flows, UI Sources and Pttrns sit behind sign-in or paid subscriptions; a skill run has no session for them, and even in a host with web access a fetch returns a landing page rather than the screens.

- `docs/inspiration-sources.md` gains **The skill cannot read these sources**, and `docs/visual-benchmark-playbooks.md` gains an **Evidence floor** section: name them as a lookup for the user to perform, never describe what a specific product's screen on one of them looks like, never attribute a pattern to "what Mobbin shows". A screenshot or note the user pastes is real evidence and is reviewable as normal D1 input.
- `docs/self-review.md` had a *mandatory* prompt asking whether the model had used those sources — a standing invitation to describe screens it never saw. It now asks whether a named reference was framed as a lookup.
- **Guardrail 16** covers both halves of the same root failure: describing a source that cannot be opened, and stating a version-bound default (Material version, predictive back, themed icons, OS-gated behaviour) as timeless. A matching note sits on the version-bound rows in `docs/context-defaults.md`.

**Enforcement.** Two more validators:

- `validate_skill_entrypoint_contract()` — `SKILL.md` must carry `Device class:`, `docs/adaptive-layout.md`, `5.5`, and `outside the standard six`. This is the generalized form of the Commit 1 lesson: a capability that never reaches the always-loaded file is effectively absent, so each branch that got there is now pinned.
- `validate_unreadable_source_honesty()` — both reference documents must state plainly that these sources cannot be opened, and the old "Did I use production references" prompt is blocked from returning.

Both verified by injection.

### Commit 6 — what landed

**P1-5, revised after measurement.** The specified check was "median pairwise 5-gram Jaccard of the calibration bodies ≤ 0.15". Measured against the real corpus, the median is **0.0** and the maximum is 0.043 — the blocks describe different domains in different words, so word-level n-grams cannot see the structural sameness the audit found. Shipping that threshold would have added a check that passes vacuously forever while producing false confidence. It was dropped, and the reason is recorded in the validator's own docstring so nobody re-specifies it.

What shipped instead, in `validate_calibration_corpus_diversity()`:

- **Score distribution** — at least 3 distinct `Quality target:` scores, and no single score above **75 %**. The proposal said 60 %; on a 23-value corpus that would have forced ten exemplars off 4/5 and invited dishonest scores. 75 % still fails today's monoculture (91 %) by a wide margin.
- **Signature-move distinctness** — `Signature move:` lines must be pairwise distinct after normalization. Two exemplars claiming the same owned asset is precisely the sameness failure, and this is the instrument that actually bites. Honest `none, this screen is inert` records are exempt.

**A validator was itself generating the monoculture.** `validate_synthetic_case_studies()` required the literal string `4/5` in every case study — "every case study is 4/5" was a CI rule. Relaxed to any `[1-5]/5`.

**P1-4, corpus rebuilt.** All six goldens gained a `Signature move:` line naming a distinct owned asset with repeat locations, none of which requires inventing brand values: `layout.hero-bleed` (premium-ui), `type.numeral-tabular` (fintech), `layout.value-unit-range` (health), `motion.commit` (onboarding), `layout.total-anchor` (checkout), `layout.severity-rail` (enterprise-saas). Their `Quality target` lines were rewritten to the Commit 2 shape and no longer close on the identical `4/5 — <adj> <noun> once <X, Y, Z> are confirmed` formula. `health.md` and `enterprise-saas.md` moved to **5/5** on their existing resilience content, `health-medication-refill.md` to **5/5** on its state coverage, and `search-results-filtering.md` honestly to **3/5** — a conventional search-and-filter list with no owned asset is what the inert cap is for. Distribution is now 17 × 4/5, 3 × 5/5, 2 × 3/5, 1 × 2/5 across four distinct scores.

**P1-6.** New `examples/evals/rubric-score-2-adversarial.json`: a 150-word Mode C spec with concrete spacing and type values (three dimensions at 4, median 3) whose design-quality recommendations are aesthetic-only, so the cap drags it to 2/5. It is the first fixture that separates a judge applying the rubric from a judge reporting an average. `rubric-score-3.json` gained an honest spread matching its own recorded failed dimensions. The pack now asserts `expected_score ≤ floor(median)` always, `== floor(median)` when no cap is recorded, and that at least two fixtures carry a dimension spread ≥ 2 — before this, spreads were 0, 1, 1, 0, 0 and the median rule was never exercised. Coverage relaxed from set equality to a superset test.

**P1-7.** Shape assertions replacing keyword and denylist checks:

- `Pattern choices and why` needs ≥ 3 bullets matching `X over Y because Z` with ≥ 8 words after `because`, replacing a bare `\bover\b` match.
- `alternative considered:` needs ≥ 10 words after the label.
- `Attention path:` and `Signature move:` need ≥ 12 words, scoped by a `label_body()` helper — the first regex attempt leaked across newlines and silently counted the following bullets' words, which the injection test caught.
- The five-phrase `GENERIC_NEXT_ACTIONS` denylist is gone. The positive test specified in the proposal (a digit, proper noun, or backticked identifier) was implemented and **rejected**: it failed thirteen specific, well-written next actions across five files and would have rewarded inserting a number. A ≥ 6-word minimum catches every denylist entry and passes every real action.

Only one example needed strengthening rather than a rule needing loosening — a 7-word `because` clause in `rationale-handoff.md`.

**CI honesty.** The oracle steps are renamed to *Self-test judge JSONL parser (round-trip, not a quality check)* and *Self-test judge command adapter (oracle, not a quality check)*, with inline comments and a new section in `docs/llm-judge-runner.md` stating plainly that no model runs in CI and a `SKILL.md` change that degrades live output cannot fail those steps.

### Acceptance

Automated:

- `scripts/validate_repo.py` green, including mode parity, the projected-line shape guard, `Device class:` in
  `MODE_REQUIREMENTS`, and corpus diversity.
- The rubric eval pack exercises the median rule for the first time (≥ 2 fixtures with dimension spread ≥ 2;
  `expected_score == floor(median)` unless capped).
- The CI step name no longer claims to validate quality.

Manual, three runs each:

- *"Design a home screen for a budgeting app"* → three runs produce different named directions with different
  token consequences, and at least one score that is not 4/5.
- *"Design an iPad clinician chart review"* → output carries `Device class: tablet`, a breakpoint, a named
  canonical layout, and navigation per width.
- *"Help me design our paywall pricing architecture"* → output opens `Mode: outside the standard six`.

The CHANGELOG entry must state plainly that the v1.16.0 Mode D contract never reached `SKILL.md`.


---

## 7. Acceptance outcome and what carries to v1.18.0

Three live acceptance passes ran against the released instructions, scored by an independent gate. They caught two defects that every one of the 28 structural validators passed over — which is the thesis of §2.6 demonstrated on this release's own work.

**Fixed before tagging:**

1. The slot receiving the rejected directions still said "two structurally different **layout** approaches" while step 5.5 produced token consequences. The instruction generated tokens; the slot asked for layouts, and two of four runs duly emitted layout descriptions.
2. A filled-in illustrative `Quality target: 4/5 — … blocked from 5/5 by Context & brand fit …` line sat in two reference docs and was reproduced near-verbatim by three of four runs. **A pre-filled example outweighs a prose instruction to derive.** Commit 2 had replaced a prescribed number with a prescribed sentence. Reference docs now carry only the derivation form, and a validator bans a filled score line under `docs/`.

**Carried to v1.18.0 — A3, the fixed exploration space.**

Every run generates the same candidate pair and commits to the same winner; the owned assets converge to one object under different names. Step 5.5 constrains divergence *within* a run and nothing widens the option set *across* runs. More instruction text has now failed twice at this; it needs a procedural change. Candidate mechanisms, none yet tried:

- Require the candidate set to include one direction drawn from a compositional school *other* than the one the committed direction belongs to, so the school catalog is sampled rather than bypassed.
- Forbid the owned asset from being the same asset class as the nearest golden's, forcing the Distinctiveness dimension off the retrieved default.
- Make the rejected directions record which school or point-of-view product each came from, so a fixed triple becomes visible in the output rather than hidden in the reasoning.

Note that criterion A3 as written — *the same prompt must produce different designs* — is the within-prompt divergence this proposal's own P2-2 called premature for lack of a sampling-temperature contract. The defensible defect is not that four runs agree; it is that they never consider anything else. Measure the candidate set, not the winner.

**Secondary, also for 1.18.0:** all 36 dimension scores across four runs were 3 or 4. The derivation is now real and visible, but with that compressed range the median cannot land anywhere but 4. The fix is upstream in the rubric's willingness to score 2 or 5, not in the median rule.


---

## 8. A3 resolved — v1.18.0 first item

**Mechanism.** Two of step 5.5's three directions are now retrieved from the 13-entry catalog rather than invented: D1 the conventional baseline, D2 a named compositional school, D3 a named point-of-view product. Selection is a rule — discard what each entry's `Do NOT use for` line disqualifies for the domain, then from the survivors take the entry whose token consequences differ *most* from D1. Every direction, including the committed one, carries `from:` provenance into the output, so a bypassed catalog is visible in the response. `validate_direction_provenance()` parses the entry names out of `inspiration-sources.md` rather than hard-coding them.

**Result, six live runs (three identical budgeting prompts + health, marketplace, education) scored by an independent gate: PASS on all six criteria, no blocking issues.**

- Provenance present and real in all six; 14 provenance values, zero invented names.
- **The option set moves with the domain** — the four different-domain runs cite disjoint catalog sets, 7 distinct entries out of 13, and the `Do NOT use for` filter visibly does the work ("Duolingo-style motivation mechanics — a streak turns a missed dose into a broken achievement"; "Brutalist … its own `Do NOT use for` line excludes any screen whose hierarchy must stay unambiguous under stress"). This was the primary measure.
- Asset-class spread: the v1.17.0 layout-structure meter is gone from all six, and runs now argue the class explicitly.
- No quality regression: no expressive direction committed anywhere, every run kept its accessibility section, full state set, and derived score.

**Two residuals, fixed in the same commit range:** only one of six runs labelled its *committed* direction, leaving the third candidate slot unverifiable — now required and validated; and the class was being chosen as "whatever the nearest golden did not use", which collapsed six classes into two, so the rule now requires arguing the class against the surface rather than against the golden.

**Still open, honestly:** two runs of the identical budgeting prompt converged on the same catalog entry with near-identical token sets. That is defensible — Müller-Brockmann is a well-grounded pick for a dense money surface and each run killed it on context-specific mechanisms — and the third run drew a different entry from the same prompt, so the set is not frozen. Within-prompt divergence remains the metric P2-2 called premature; the domain spread is the one that carries user-visible value.


---

## 9. P1-11 resolved — `skill/skill.md` deleted

**Decision: delete.** The alternative — declaring it a non-Claude-host entrypoint and bringing it under the parity validator — was rejected on the evidence below.

**No host loads it.** `agents/openai.yaml` contains only interface metadata (display name, short description, default prompt, invocation policy) and no file path at all. The Claude Code wrapper at `.claude/skills/mobile-design-skill/SKILL.md` explicitly reads the root `SKILL.md`. `README.md` tells Cursor users to copy the root `SKILL.md`. The first release's changelog entry — *"Main skill prompt in `skill/skill.md`"* — shows what it was: the original prompt, superseded when the root `SKILL.md` became the entrypoint, and never retired.

**It had drifted two releases behind and could not be cheaply caught up.** At the point of deletion it carried **zero** occurrences of step 5.5, `Device class`, `adaptive-layout`, `outside the standard six`, `Signature move`, `Dimension read`, direction provenance, or the Distinctiveness dimension. Catching it up would have meant re-forking a workflow that now spans `SKILL.md` plus `skill/modes.md`, `skill/templates.md` and thirty reference documents.

**It was actively generating contradictions.** Its scoring paragraph ended up holding both the new derivation rule and the obsolete pre-1.16 review rule in one sentence — *"…a score asserted without a dimension table behind it is a default, not an assessment. For reviews, expose the current design-quality score with a short reason"* — while its own output structure four hundred lines later specified `Design quality score (current → projected, with per-dimension table)`. That is the §2.1 drift class reproducing inside a single file, and every edit in this initiative had to touch it for no benefit.

**Ported before deletion:** the six worked classification examples, which are more concrete than the abstract intent cues in `docs/workflow.md`, into `SKILL.md`'s mode section. Its ban on vague advice was already covered by guardrail 4 (`docs/guardrails.md`), and its closing reminder duplicated `SKILL.md`'s.

**Guard added:** `validate_single_workflow_source()` asserts that `## Required workflow` and `## Mode output requirements` appear in `SKILL.md` and nowhere else. Three files each claiming to be the workflow is the condition that produced the v1.16.0 drift; this stops a third fork from quietly reappearing. Verified by injection.


---

## 10. P2-1 shipped — the first check that reads generated text

`scripts/run_generation_eval.py` closes the gap this whole initiative kept demonstrating: 29 structural validators, and none of them had ever read a model's output. Three acceptance passes during 1.17.0 found two defects that every one of them passed over.

**Reuse, not a parallel implementation.** `validate_example_responses()` was refactored into `check_response(response, mode, label)`, and the eval imports it. Generated output is held to *exactly* the rules the committed corpus is held to, and the two cannot drift — which matters more here than anywhere, because drift between two files claiming the same contract is the failure this repository has now shipped twice.

**Generation needs a model; scoring does not.** That split is what makes it CI-safe. The deterministic oracle replays committed examples through the scorer to prove the adapter and the parser; the step is named so nobody mistakes it for a quality signal. A real run puts a model behind `--generate-command` during maintenance.

**Three eval-only checks**, none of which a committed file can be wrong about:

- **Derived score** — `Quality target: N/5` may not exceed the median of the dimension scores the response itself prints. Pure arithmetic. This is the check that would have caught the asserted-score defect on the first pass instead of the third.
- **Provenance** — a rejected direction citing something outside the catalog.
- **Prompt expectations** — a tablet prompt answered with `Device class: Phone`, or a no-fit prompt rounded into a standard mode.

All verified by injection: an inflated score, an invented provenance, and a phone answer to the iPad prompt each produce exactly one precise failure.

**A bug the refactor introduced and injection caught:** the extracted function's `label` parameter was shadowed by the loop variable in the `label_word_counts` check, so failures were reported against `Attention path:` instead of the file. Fixed before commit. That is the second time in this initiative that a validator written to catch drift had to be tested by breaking it on purpose — the discipline is not optional.


---

## 11. P2-2 shipped — sameness is now measured, not read for

`scripts/run_diversity_eval.py` extracts a decision vector per response — catalog provenance, asset class, derived score, named blocker, base units, ratios — and reports the spread. This is only possible because v1.18.0 pushed provenance and asset class into the output as machine-readable fields; before that there was nothing to measure but prose.

**Thresholds are asserted only where measured data exists.** Four come from this session's live acceptance passes; `vector_similarity` has no baseline and is reported without assertion. The rule is stated in the script itself: guessing a threshold produces either a check that passes vacuously forever or one that forces dishonest output, and both have already happened in this repository.

**Within-prompt divergence stays unmeasured,** as §P2-2 originally required. A deterministic skill giving one well-grounded answer to one prompt is defensible; never considering anything else is not, and that is what the provenance and asset-class measures capture.

**The self-test discriminates rather than replays.** `examples/evals/diversity-fixtures.json` holds a deliberately uniform corpus reproducing the exact 1.17.0 failure and a varied one, and the test asserts the measurements separate them:

```
uniform  score_conc=1.0 prov_conc=1.0 classes=1 similarity=0.714
varied   score_conc=0.5 prov_conc=0.1 classes=5 similarity=0.077
```

It also asserts the extractor reads score, provenance and blocker out of a real committed response. Both halves were verified by injection: loosening the thresholds until the uniform corpus passes fails the test with *"the metric does not discriminate"*, and breaking the score regex fails it with *"extractor read score `None`"*. That design is a direct response to shipping a green oracle over a broken function in v1.19.0 — a self-test that only proves the pipe is worth nothing.


---

## 12. Where to pick this up

State at hand-off: `main` == `origin/main`, HEAD `68412ed` plus the pre-handoff fix commit, tags `v1.17.0` … `v1.20.0`, working tree clean, both validators green.

### Corrections that outrank the P-tables above

Three planned items were changed after measurement. The correction shipped, not the row:

- **P1-5's Jaccard check was dropped.** Measured median over the real corpus was 0.0 (max 0.043) — word-level n-grams cannot see structural sameness across domains. Signature-move distinctness replaced it. Its 60 % score-share threshold was also relaxed to 75 %, because 60 % on a 23-value corpus forces dishonest scores.
- **P1-7's positive next-action test was rejected.** Requiring a digit, proper noun or backticked identifier failed thirteen specific, well-written actions and would reward inserting a number. A ≥ 6-word minimum replaced it.
- **P2-2's within-prompt divergence stays unmeasured**, as the row itself required. Provenance and asset-class spread carry the signal instead.

### What a pre-handoff sweep found that the validators could not

The guards added across these releases were scoped to the *files* where each defect was first seen rather than to the *class* of defect, so the repository validated clean while eight instruction-level contradictions survived. All six blockers were fixed before hand-off, and each guard was widened to its defect class:

- `skill/modes.md` — the file `SKILL.md` names as authoritative — omitted `Device class` from all six `### Output structure` blocks while both scorers hard-failed any response missing it. Invisible to mode parity, which strips contract elements before comparing. Now checked by `validate_modes_carry_contract_elements()`.
- Two live "aim at 4/5" instructions survived in `skill/usage.md` and `skill/modes.md`, outside `PRESCRIBED_SCORE_SCOPE` and matching none of its patterns. Scope widened to `skill/` and `SKILL.md`, pattern added.
- `examples/anti-patterns.md` taught the banned pre-1.16 Mode D bucket shape inside two **Good response** fragments — the exact "a filled-in example beats a prose instruction" failure this release documented, live inside the file meant to demonstrate correctness. Now guarded by `validate_calibration_teaches_current_shape()`.
- `MARKDOWN_GLOBS` used `docs/*.md`, so seven required domain packs and the changelog were never link-checked.
- `install.sh --method copy` never copied `examples/`, while `SKILL.md` references it in ten places.
- `run_diversity_eval.py` asserted `asset_class_count ≥ 3` against its own recorded measurement of 2 — a threshold that fails by construction. Demoted to reported-only; the measurement is the floor to move, not a bar the output clears.

**The generalizable lesson: when a guard is added for a defect, scope it to the defect class, not to the file the defect was found in.** Every survivor above sat one directory outside a guard that would otherwise have caught it.

### Ranked backlog

1. **Compressed dimension range.** Every dimension read in live acceptance landed on 3 or 4 — no 2s, no 5s — so a derived median is structurally stuck at 4. Fix upstream in `docs/design-quality-rubric.md`'s willingness to score 2 and 5, not in the median rule.
2. **Asset-class spread** — 2 of 6 classes appeared in practice. Colour, motion signature and illustration never did.
3. **P1-8** — `docs/patterns-catalog.md` §15 in the existing Use-when / Avoid-when matrix shape, plus a tablet golden and a stretched-phone review fixture. The highest-value remaining tablet item: it is what stops the model confidently choosing bottom navigation at 1366 pt.
4. **P1-2** craft substrate — `docs/color-system.md`, a layout section in the quality bars, motion by cited platform curves, type-scale math.
5. **Consistency debt the sweep flagged as should-fix**: `docs/workflow.md` step numbering is off by one against `SKILL.md` (its direction step is `4.5`, everywhere else it is `5.5`); `Device class:` is missing from output-contract statements in `skill/usage.md`, `docs/workflow.md`, `docs/clarification-policy.md` and `docs/evals.md` — better solved by demoting those to pointers than by patching five copies; `docs/commands.md` documents the pre-1.16 Mode 4 output; Templates E and F reference an `Alternatives considered` section they do not have.
6. P1-9, P1-10, P2-3 (Mode G), P2-4 (render-and-critique loop), P2-5 (DTCG artifacts), P2-6 (surface axes).

### How to work on this repository

- **Verify every new rule by injection** — break it, watch the validator fail, restore. A green positive run proves nothing until the negative is shown. Two guards in this series were themselves broken and passing.
- **Never `git checkout <file>` to restore after an injection test on a dirty tree.** It silently reverts uncommitted work; copy to a scratchpad instead.
- **Build self-tests that discriminate**, not ones that replay a known-good answer. v1.19.0 shipped a green oracle over a variable-shadowing bug; v1.20.0's fixtures instead assert the metric separates a bad corpus from a good one.
- **Run live acceptance before any release that touches instruction text.** Agents executing `SKILL.md` against real prompts, scored by an independent judge, found every defect the validators missed.

---

## 13. Backlog item 1 shipped — the scale had three anchors for five bands

`docs/design-quality-rubric.md` asked for a number from 1 to 5 and gave three columns to pick it from: `1-2 signals | 3 signals | 4-5 signals`. Two of the three were bands, and the document supplied within-band discrimination for exactly one of them, once, in artifact-scoped language. There was **no text anywhere in the repository distinguishing 1 from 2.** The executable decision procedure was: pick a column. Reachable set `{1, 3, 4}`, and the committed corpus was exactly that.

### What the diagnosis added to the backlog line

Four things the row did not say, each of which changed the work:

1. **The collapse was bimodal.** Generation was pinned to `{3,4}`; Mode D was pinned to `{2,3}` — 20 twos and 5 threes in `Now`, zero 1s, 4s or 5s. The two regimes failed in opposite directions and the union across them looked wider than either. A guard scoped to `Dimension read:` would have covered half the defect.
2. **The base cause was arithmetic, not vocabulary.** A lone 5 cannot move a nine-element median (free but useless); a 2 trips the critical-dimension step and then the revise ratchet (expensive). So even a perfect table would not have produced either tail while the incentive stood.
3. **`docs/evals.md` carried a per-dimension floor at 4** — "Any dimension below 4/5 is either revised or clearly blocked by missing input" — handed verbatim to the fixture judge in its prompt.
4. **`QUALITY_TARGET_SHAPE` forbade 5/5 by test suite.** It required `blocked from … until` unconditionally and is a `must_contain` for Modes A and C, so a response deriving 5/5 could not satisfy it without inventing a blocker.

`validate_score_is_derived_not_prescribed()` — the guard built for this exact class — matched **zero lines inside its own scope**. All five patterns require the token `target` adjacent to `4/5`; every live anchor had drifted to "usually lands at", "4/5-style", "At 4/5,", "not a quiet 4/5".

### The scale

Four boundary questions per dimension replace the three descriptions. The band is the number of consecutive questions answered yes from the left, plus one; a later yes never rescues an earlier no. Four boundaries define five bands exhaustively, which a set of descriptions cannot — under the old table a typography treatment with sizes but no weights matched no cell at all.

The ladder separates four acts:

```
1 → 2   contradicted or absent  →  named
2 → 3   named                   →  decided for the default case
3 → 4   decided                 →  stated with values, surviving one declared variation
4 → 5   stated                  →  a rule that settles the cases the artifact does not list
```

### It took three calibrations, and the same instrument caught all three failures

| pass | result | cause |
|---|---|---|
| 1 | 46% of values on band 2; four of seven artifacts at median 2 | three `2 → 3` questions asked whether **values** were stated, which a Mode A concept fails by construction — its output contract has no section to carry them |
| 2 | 63% on band 3; all seven artifacts at median 3 | `3 → 4` cells were four-way conjunctions; `examples/ui-spec.md` states `22-24sp, 28-32sp line height` per role, `16dp`/`24dp`/`48dp` spacing and `240ms, standard-decelerate` with a named reduced-motion fallback, and read 3 on all three of those dimensions because each conjunction had one absent clause |
| 3 | converged | boundaries are single tests; where a cell names two things the second is the one declared variation the value must survive |

The diagnostic that caught passes 1 and 2 was not the distribution. It was **the count of dimensions taking more than one value across the corpus**: two constants at 4 before the release, then two constants at 2, then three constants at 3. A dimension that reads one value in every artifact is measuring the rubric, not the artifact. It is now a validator.

### Measured

| | before | after |
|---|---|---|
| 63 `Dimension read:` values | `1`×1, **`2`×0**, `3`×14, `4`×45, `5`×3 | `1`×2, `2`×4, `3`×33, `4`×20, `5`×4 |
| top-value share | 0.71 | 0.52 |
| union of bands | `{1,3,4,5}` | `{1,2,3,4,5}` |
| artifact medians | 6×4, 1×3 | 5×3, 2×4 |
| single-valued dimensions | 2 of 9 | **0 of 9** |
| lines with both a `≤2` and a `≥5` | 0 | 2 |
| `Quality target:` at 4/5 | 17 of 23 (74%) | 13 of 23 (57%) |

### Live acceptance

Seven responses through `SKILL.md`, five generation and two Mode D, three scored by an independent judge.

```
score_concentration   1.00 (1.17.0 pass)  ->  0.00
scores printed                                2/5, 3/5, 4/5
Mode D `Now`          {2,3} committed     ->  {1,2,3}, six 1s
Mode D `Projected`    {3,4} committed     ->  {1,2,3,4}
generation bands      {3,4} (1.17.0)      ->  {3,4,5}
```

The 4/5 pin is gone in both regimes and the two carriers cover 1..5 between them. The judge disagreed with one draft's own read on one dimension (`Production readiness` 5 against 4) and named the boundary that settles it, which is the disagreement being legible rather than a defect.

**Two findings from the run, both about the instruments.** `share_in_middle_bands` counted the share on bands 3 and 4 — the shape the defect had when it was found — and the live run came back 93% on bands 4 and 5, a collapse the field read as an improvement. It is now `adjacent_pair_share`, the largest share held by any two adjacent bands. And three of five responses appended prose after the last dimension, which an anchored per-chunk parser silently dropped, reading 8 bands where 9 were printed; both parsers now take the first band token per chunk. A parser that under-counts is worse than one that fails, because the measurement still prints.

### What did not resolve

**Band 5 is cheap in generation.** 23 of 42 live bands were 5, and `adjacent_pair_share` sits at 0.911 on `{4,5}` against roughly 0.94 the old corpus would have shown on `{3,4}`. The pin moved; it did not disperse. The `4 → 5` question asks for a rule that settles unlisted cases, and a model authoring its own artifact can write such a rule at will — the adversarial critique predicted exactly this and it happened. Whether those rules are load-bearing or performative needs a judge panel, not another instruction edit.

**Band 2 is absent from generation output, and that is probably correct.** The revise trigger lifts any dimension whose failed boundary the input can answer; in generation the model authors the artifact, so nearly every band-2 failure is liftable. Band 2 is a review reading, and review now produces it. This should be confirmed rather than assumed.

**The golden examples read lower than their label.** Five of seven artifacts land at median 3 — they decide but rarely state values across variations, which is what `docs/golden-examples.md` implies they demonstrate. `examples/ui-spec.md` was given the colour rules it should always have had; the rest were left alone rather than inflated.

---

## 14. Backlog item 1 (post-1.21.0) measured — the band contrast is a null

The item read: *band 5 is cheap in generation — 23 of 42 live bands were 5, `adjacent_pair_share` sits at 0.911 on `{4,5}`. Needs a judge panel to test whether those rules are load-bearing, not another instruction edit.* It also carried a second half: *confirm the hypothesis that band 2's absence from generation is correct-by-design.*

### The instrument

The `4 → 5` question asks whether a stated rule decides a case the artifact does not list. That is mechanically testable: **apply the rule.** Hand a reader the statement and one unsettled case from the same product, with no artifact, no dimension name and no band, and ask whether the statement forces one specific answer. Convergence across independent readers means load-bearing; divergence or "underdetermined" means the statement only reads like a rule.

### First design, and why its result was thrown away

24 band-5 statements against 10 controls drawn from band-3/4 dimensions, three blind readers each. Result: 50% against 30%, Fisher one-sided p = 0.25.

The adjudicator refused it and named the confound in its own design: **the agent that wrote each situation also knew which arm the statement came from.** A situation landing inside a statement's enumeration returns `determined` almost mechanically; one chosen just outside returns `underdetermined` just as mechanically. Probe difficulty was never matched between arms. Supporting evidence that the design was measuring the wrong thing: the artifact-of-origin spread was 17%–86%, larger in magnitude than the band contrast it was competing with, and the sign reversed inside two of five artifacts.

### Second design

Situations written from band-stripped copies of the artifacts — the calibration block removed and verified leak-free — one per dimension for all nine, under an instruction identical across dimensions, by agents who never saw a band, a score, or a statement. The control arm grew from 10 mixed probes to a full band-4 arm drawn from the same seven artifacts and the same nine dimensions. 63 pairs, three blind readers, 88.9% unanimous, and zero probes where two readers said `determined` but named conflicting answers — in both runs.

| arm | load-bearing | rate |
|---|---|---|
| band 5 | 11/28 | 39.3% |
| band 4 | 9/25 | 36.0% |
| band ≤3 | 5/10 | 50.0% |

Fisher one-sided p = 0.516; 95% CI on the difference +3.3 pp [−22.8, +29.4]. Band 5 would need 18/28 to reach significance against band 4 fixed at 9/25 — roughly nine times the observed gap.

Against the first run, **both rates moved toward each other**: band 5 down 10.7 pp, controls up 10.0 pp, closing 84% of the gap. Equal and opposite is the signature of a removed confound rather than of a real effect appearing or vanishing.

### Why this is a null and not "underpowered"

All three confound checks still fail, but **they fail in the direction that flatters band 5.** The band-5 arm is loaded with the two highest-yield dimensions — distinctiveness 6/7, attention path 5/7 — while the band-4 arm carries composition 2/7 and interaction 1/7. Mantel–Haenszel stratified on dimension, the odds ratio drops from 1.15 to **0.735**: adjusting flips the sign. The near-null is therefore a ceiling on the band effect, not a signal buried under noise.

The effects that are real in this corpus are not the band. Dimension identity spans 14.3%–85.7% (21× the band contrast); artifact of origin spans 22.2%–77.8% (17×). Leave-one-artifact-out moves the band gap between −7.5 pp and +15.4 pp — which artifacts are in the corpus matters about seven times more than which band a statement was given.

**What is licensed:** 17 of 28 statements scored at band 5, and 38 of all 63 statements, were judged non-generative by two or more readers who never saw a score. The weakness is at the level, not at the boundary.

**What is not licensed:** "band 5 over-claims relative to band 4" — measured and unsupported. Also unresolvable by this design: whether the `4 → 5` distinction is empty or real-but-loosely-applied, since the only band labels in existence are the scorer's own. Those two are observationally identical here.

### What shipped, and why it is not a descriptor rewrite

Nothing in the data says band 5 is *described* wrongly relative to band 4, so the descriptors were left alone. What the data says is that the question was being answered by reading. It is now answered by running a test:

> Take one ordinary case the artifact does not list. State what the statement returns for it. If you cannot write the answer, the band is 4.

Four failure shapes account for 34 of the 38 performative statements and are recorded as diagnoses — a ratio or floor with no anchor, a budget with no behaviour, a precedence ladder with no output, a requirement with no threshold. The shapes that *pass* were deliberately not listed: that would be a template to satisfy, which is the rule-1 failure this repository has shipped twice.

The gate sits on all four surfaces that assign a band — rubric, self-review checklist, judged mode, judge agent — and `validate_band_five_closure_test()` checks all four, because a gate present in the drafting instructions and absent from the judge is the file-scoped guard this series keeps rebuilding.

This also makes the next measurement informative: with the test enforced, the two surviving hypotheses stop being observationally identical.

### The second half: band 2 in generation

Two generation runs where the user's own constraint blocked a dimension from being lifted.

- **"Do not pick components — the library is being replaced"** → `production readiness 2`, on exactly the constrained dimension, with the rest of the read between 3 and 5. The hypothesis holds: band 2 appears in generation when the revise trigger genuinely cannot fire.
- **"No palette, no typeface, no motion language, no visual signature of any kind; structure and behaviour only"** → `distinctiveness 4`, with a `layout.now-next` signature move of asset class *layout structure*. On inspection this is a defensible reading rather than a violation — the constraint permitted structure, and the model found an owned asset inside the permitted space.

So the hypothesis is **supported on the one clean case** and untested by the second, which turned out not to be a constraint on the dimension it was aimed at. n = 1 is not a confirmation; a follow-up should constrain three dimensions across more runs.

### Backlog effect

"Band-5 statements are more load-bearing than band-4 statements" closes as a measured null and should not be re-run in this form. Any next measurement must stratify on dimension **by design** — fixed dimension, statements varied by shape — because at seven probes per dimension against a 71-pp dimension spread, this design cannot see a band effect smaller than 28 pp however many artifacts are added.

---

## 15. Backlog item 2 measured — the questions are fine, two of them were asking the wrong thing

The item read: *determinacy is a property of the dimension, not the band — distinctiveness 6/7 and attention path 5/7 against typography 1/7 and interaction 1/7. Worth asking whether some dimensions can reach band 5 at all as their `4 → 5` question is written.*

### Design

Two explanations were standing. **(A)** the question is unsatisfiable for that dimension; **(B)** it is satisfiable and live output does not supply what it needs. These are separable: ask for the best statement anyone can write against that question, and test it the same blind way.

Nine dimensions, **one fixed product** — an EV charging session screen, a domain absent from the corpus. Fixing the product removes artifact-of-origin, which moved determinacy 17× more than band did, by construction rather than by adjustment. Two statements per dimension: `best` (a serious attempt, by an agent that had read the rubric and the four known failure shapes) and `typical` (a well-written specimen of those shapes — a strawman proves nothing). Two situations per dimension written from the brief alone by agents who never saw a statement or an arm, and **the same two used for both arms**, so the comparison is paired on dimension and on case. Three blind appliers.

### Result

`best` 12/18 cells, `typical` 5/18. Restricted to the five dimensions whose cases were on-question: **best 10/10, typical 1/10, sign test p = 0.0039.**

| dimension | live | best | typical | |
|---|---|---|---|---|
| attention | 5/7 | 2/2 | 1/2 | satisfiable |
| density | 3/7 | 2/2 | 0/2 | satisfiable |
| composition | 2/7 | 2/2 | 0/2 | satisfiable |
| context | 2/7 | 2/2 | 0/2 | satisfiable |
| interaction | **1/7** | **2/2** | 0/2 | satisfiable |

**Explanation (A) survives in 0 of 9 dimensions.** Interaction is tied for the lowest live rate and its best statement cleared 6/6 unanimously. Satisfiability has zero variance across a 5× spread in live determinacy: the questions are fine and the corpus is thin.

The length confound was real at the arm level — `best` averaged 135 words against 85 — and is killed by the within-arm split: statements that *failed* were marginally longer in both arms (134.5 vs 136.0; 85.0 vs 86.0). Length separates the arms and predicts nothing inside them.

### The structural hypothesis was wrong, and the replacement is better

I had proposed that questions asking for **a boundary over a bounded set** are satisfiable while those asking for **a mapping from an open input space** are not. Contradicted: three of the six clearing statements are open-input mappings and cleared unanimously, and the two lowest live dimensions both have bounded output sets.

What separates perfectly is **output-type match**. Six best statements return the type their cell asks for — 36/36 judgements. Three return a different type — 1/18. No overlap, and both of the failing three carry the full generative kit (a classifier on evaluable inputs, named outputs, a residual clause, a tie-break). Having the machinery is not the thing; returning the asked-for type is.

### Two defects in the table, found by that

- **`Color, state, and contrast` graded the form of a statement rather than what it returns.** *"Is that appearance behaviour expressed as one transform over the roles, rather than as a second hand-made set?"* The closure test asks you to write down what the statement returns; that cell never asks for an output, so the test structurally could not run on it. Three readers unanimously called a complete OKLCh transform underdetermined because the case asked something the cell never posed. Replaced with *"Does a stated rule return the dark and increased-contrast values for a role the artifact does not list?"* — same intent, only a transform can pass, and now gradeable.
- **`Production readiness` was a completeness test over listed values.** *"Does the handoff say which values are negotiable and which are hard bars…"* — band-4 shaped, and its output is an authority class, not an answer to a case. Replaced with *"Does a stated test return hard-bar or negotiable for a value the handoff does not list?"*

### Confirmation, with the predictions registered first

Same six statements, new cases drawn from the rewritten cells.

| cell | before | after |
|---|---|---|
| colour-best | 0/6 | **5/6** |
| production-best | 1/6 | **6/6** |
| typography-best | 0/6 | **6/6** |
| typography-typical | **6/6** | **0/6** |
| colour-typical | 0/6 | 0/6 |
| production-typical | 0/6 | 3/6 |

Arm separation moved from **−5/18** — the typical arm outscoring the best arm — to **+14/18**.

**One prediction was refuted.** `production-typical` was predicted to stay underdetermined and cleared 3/6: the case landed inside a class the statement enumerates outright ("layout and spacing values are a considered starting point"), so it could not separate the arms. No applier erred; the premise was right about the precedence ladder and wrong about the statement, which also carried a categorical enumeration.

The typography result is the cleanest thing in either run: statements unchanged, cases changed, and the verdict inverted by twelve judgements. The previous 6/6 was won by quotation — an unconditional "All numerals are tabular" answered a figure-style case — and the appliers named the escape as closed.

### What shipped

Three constraints on the closure test's case, not one: it must be an instance of the unlisted thing the cell names; its answer must not already be printed in the statement; and it must fix every input the rule needs except the one under test. The first two are strongly evidenced; the third rests on a single 2–1 split and is recorded as the weaker of the three.

The guard is scoped to the defect class rather than the two cells: a `4 → 5` cell may not use form-grading vocabulary and must carry a returning verb, so the closure test always has an output to write down.

### What section 15 did not resolve

- **`Production readiness`'s rewrite rests on one clean case.** Its 6/6 headline is half quotation — one situation names a value the statement already enumerates. Re-run with two fresh unlisted-value cases screened against the statement's own enumerations.
- **`Typography`'s two cases are one probe run twice.** Both traverse the same two binary questions, land on the same role, and refuse a new role on the same test. Effective n = 1.
- **The non-quotability constraint is only partly enforceable in a measurement pipeline**, because a case writer blind to the statements cannot know which classes they enumerate — 2 of 6 cases leaked, a ~33% rate. It *is* enforceable in the rubric, where the model reads its own statement before picking a case. Future measurement runs need a post-write screen; the instruction does not.
- **Typography's cell is a null.** It was answered correctly by the best statement in all three readers' words and scored zero anyway because the cases probed figure style. No edit was warranted and none was made.

---

## 16. Backlog item 3 measured — the gap is closed by printing the case, not by naming the shapes

> **Superseded by §17. Three claims below are contradicted, not merely unsupported, by a six-brief re-measurement with the extraction defect fixed: that the defect was *"symmetric across arms"* (it fell on the control and doubled it); that the worked case is *"a mediator, not a quotation artifact"* (presence is a marker — mandating it moved 13/17 against 10/17, p = 0.453); and colour/state as the *"largest gain"* at 3/3 (it inverts to 2/6 against 3/6). The change §16 recommends was shipped as v1.24.0 and reverted in v1.25.0. The section is kept as written because the reasoning it records is what a reader needs in order to see how a well-run measurement produced a wrong answer.**


The item read: *live output is the thing that falls short, not the questions. Untested: whether the closure test alone closes that gap, or whether the drafting instructions need the failure shapes stated where the artifact is being written rather than where it is being scored.*

The whole closure test was written as scoring language — "band 5 is not awarded on the reading, it is awarded on a test you run". The rubric is reachable from step 5, but step 6, where the artifact is written, sees how the statement will be judged and not what to write.

### The three arms

Three briefs, run through the skill three times. Nine statements extracted per artifact, each paired with a situation **written from the brief before any artifact existed**, by agents who saw no statement and no arm. The same 27 situations test all three arms, so difficulty is identical by construction — the confound that invalidated the first run of item 1 — and any quotable case leaks into every arm equally. All three arms were re-judged in one pass by one cohort of blind raters, so rater drift is not confounded with the arm.

- **A** — the skill as it ships.
- **B** — plus a drafting-time instruction: name the case before writing the statement, and four shapes that read like rules and return nothing.
- **C** — plus a requirement to print the worked case (`Unlisted case: … → the value the rule returns`) for every dimension.

| arm | load-bearing | McNemar vs A |
|---|---|---|
| A | 7/27 = 26% | — |
| B | 12/27 = 44% | p = 0.151 |
| C | **16/27 = 59%** | **p = 0.011** |

C survives every robustness cut — unanimity 0.046, quotation-leaks excluded 0.006, distinctiveness dropped 0.019, worst case 0.055 under the most adversarial double exclusion — with no sign reversal in any brief and every rater ranking C first.

### The correction to §16's predecessor

**Arm B's headline from the first pass does not replicate.** Re-judged by the same cohort it moves from Fisher p = 0.043 to 0.127, on a drift of two statements out of 54. It was never significant on the pre-registered paired test in either pass (0.059, then 0.151). The honest restatement is not "B was wrong" but **"B's advantage was one statement wide."** Any earlier writeup citing 0.043 should carry both numbers.

B also reproduced, a second time and under new judging, the exact defect it was warned about: colour/state 0/3, all nine rater judgements underdetermined, "a ratio or floor with no anchor". Arm C recovered it 3/3 — its largest gain and its only dimension clearing in every brief.

### Mediator, not quotation — the question the previous run left open

Of C's 16 wins, **11 derive a value the worked case does not contain**, and two are the case's explicit complement, which quotation cannot produce: one case works the off-focus branch and says "no haptic" while the situation is in-focus and the raters return "instant swap plus haptic". One determination **contradicts its own worked case** and still came back determined. And the decisive datum — **11 cells that printed a case still came back open**, including one whose case was a near-verbatim answer to the situation put to the raters. Excluding all three of C's near-restatements, C is 13/24 against A's 6/24, p = 0.033.

Pooled over all three arms, worked-case presence beats arm as a predictor (25/42 vs 10/39, p = 0.002, against p = 0.034 for the arm label). And the requirement's effect sits exactly where the model would not have written a case unprompted: on the 14 dimensions arm B left without one, C is 8/14 against B's 4/14; on the 13 where B wrote one, both are 8/13. A mandate that changes nothing where the behaviour was already present is the shape a mandate should have.

### Why the blanket form did not ship

C was told to print a case for **every** dimension, and that collapsed the score's own information: **24 of 27 dimensions claimed at band 5**, self-scoring φ of −0.053 against arm A's 0.171 and arm B's 0.417. Writing a case, seeing output and awarding 5 becomes one motion. Prediction 4 — that C would be better calibrated, because a rule returning nothing is visible to its author — is **refuted**: the honesty clause fired three times, two of those three were dimensions the raters called determined anyway, and it caught none of the ten over-claims.

So the printed case shipped **scoped to band-5 claims**. It is a gate on the top band, not a section to fill in.

### The pre-registered rule, honoured rather than dodged

C vs B did not separate (6 C-only, 2 B-only, p = 0.145), and the pre-registered rule said that in the C ≈ B branch the simpler instruction wins. It did not win here, for reasons that are findings rather than rescues: B's own advantage over A failed to replicate, B reproduced its named defect a second time, and **C's instruction is a superset of B's** — B's four shapes plus one clause — so shipping C is not a bet against B. The rule is recorded as reaching its B branch on the primary test, and overridden on stated grounds.

One further asymmetry, not pre-registered: C's verdicts are far more rater-stable. Of the statements each arm won, the share won unanimously is A 7/7, **B 4/12**, C 14/16 (Fisher C vs B p = 0.005). B's wins are the ones raters disagree about, which is why C beats B decisively on strict aggregation rules (unanimity p = 0.003) and not at all on loose ones.

### What section 16 did not resolve

- **C vs B is not isolated.** Eight discordant pairs is not a test and 0.145 is not a null.
- **Three briefs floor brief-level inference at p = 0.125**, whatever the effect size. Six briefs × nine dimensions would put the paired test near 0.01 and the brief-level floor at 0.016.
- **Nothing separates "the requirement worked" from "arm C's generator happened to be better."** That needs an effort-matched control the design does not have — though C is +0.5% on length over B, so the C-vs-B contrast is at least not an effort story.
- **A measurement defect worth fixing before the next run**: where a rule lives in a table, the extractor can take the lead-in and miss the table. Verified to have cost C three cells and B at least one, symmetrically across arms, so every rate above is an underestimate and the arm contrast is compressed rather than inflated.
- **All three distinctiveness situations presuppose a placeable mark**, which is ill-formed for a type-treatment asset. Second run in a row; the dimension returned 1/6 across arms and should be rewritten before it is measured again.

---

## 17. The powered re-measurement — v1.24.0 reverted, and the instrument was the effect

§16's change shipped on three briefs. This is the six-brief run it asked for, with the three instrument defects fixed first, and it refutes the change.

**A point worth stating before the numbers: the configuration that shipped had never been measured.** The measured arm printed a worked case under *every* dimension; what shipped printed it only under band-5 claims, narrowed because the blanket form collapsed calibration. So this run tests the live configuration for the first time.

### The six-brief result

| arm | load-bearing |
|---|---|
| v1.23.0 baseline | 27/54 = 50.0% |
| shipped v1.24.0 | 28/54 = 51.9% |

McNemar exact two-sided **p = 1.000** (11 D-only against 10 A-only). 95% CI on the paired difference **[−15.7, +18.9]** points — the earlier +33.3 lies outside it. Power to detect that earlier effect: **98.8%**. Leave-one-brief-out and leave-one-dimension-out: no cut produces the treated arm ahead at p < 0.5. Four of six briefs are exact ties, one favours each arm, and no rater ranks the treated arm first — where in the three-brief run every rater did.

### Why the earlier result happened, and the note that was wrong

§16 recorded the extraction defect as *"symmetric across arms, so the arm contrast is compressed rather than inflated."* **That was wrong, and it is the whole story.**

| | earlier run | this run |
|---|---|---|
| baseline arm, briefs p1–p3 | 7/27 = 25.9% | **14/27 = 51.9%** |
| treated arm, same briefs | 16/27 = 59.3% | 14/27 = 51.9% |

The same three briefs' baseline artifacts **double** when the extractor is told to quote a rule complete, including the table its values live in. The treated arm does not move. The mechanism fits: a printed `Unlisted case: … → value` is one inline sentence that survives extraction intact, while an untreated rule more often lives in a table whose lead-in the extractor took and whose body it dropped. The +33 points measured how legible each arm's rules were to the extraction step, not how often they closed.

### The cost that was real

Against no measured benefit, the change carried measured harm, all against the concurrent control rather than against the reverted blanket form:

| | baseline | shipped |
|---|---|---|
| band-5 claim rate | 15/54 | 23/54 |
| precision | 0.733 | 0.652 |
| over-claims | 4 | 8 |
| φ | 0.289 | 0.230 |

And the gate never fired. All 23 band-5 claims carry a case, so *"a band 5 with no printed case is a band 4"* demoted **0 of 23** — while 8 of the 23 it passed are underdetermined on the raters' reading. A 100% pass rate with a 35% false-positive rate is not a gate.

Scoping the case to band-5 claims also made the two the same variable in **54 of 54** cells, so the mediation the requirement rests on is not measurable at all under the shipped form. And the mediator claim itself does not survive: presence predicts (pooled p = 0.037) while assignment does not (p = 1.000), which is the signature of a **marker**. Unprompted, the baseline printed a case in 10 cells and 7 closed. Mandated on the 17 cells where the baseline printed none, the treated arm went 13/17 against 10/17 — p = 0.453.

### Reverted

Commit `e0dfe8c` reverted in full: five instruction surfaces and the guard. **Kept:** the closure test itself, the four failure shapes, the `4 → 5` returning-verb guard, and the defect-class scoping — nothing here touches those, and all three were re-verified by injection after the revert.

### Three instrument findings, two of them new defects

- **The distinctiveness fix worked and overshot.** From 1/6 across arms twice running to **11/12 pooled**, the highest of the nine — and now at ceiling, separating nothing. All 11 wins are settled by checking whether the asked surface appears on the statement's own repeat list, which is quotation-shaped: the rewritten situations ask whether X is on a list rather than what a rule returns for an unlisted X. It is also the single largest contributor to the pooled printed-case association; removing it and context & brand fit takes that from p = 0.037 to p = 0.637.
- **Context & brand fit is the new floor at 1/12**, and it is the same class of defect. Across 11 underdetermined cells all three raters give the same reason: the situation asks about copy voice, bystander privacy or house-versus-native chrome, and the cell returns a precedence order — which decides which default wins, not what the screen looks like. A scope mismatch between the situation writer and the cell.
- **Production readiness at 3/12** is third: nine of twelve fail because the situation demands a hard-bar test most statements do not contain, and the three that close are exactly the three whose statements carry an explicit hard-bar list.

### What §17 did not resolve

- **Whether the earlier +33 is recoverable at all**, or was entirely extraction. The clean test is the blanket arm re-measured on this harness; if it also lands near 50%, the whole of §16 was instrumental.
- **Typography is the one live hypothesis** — baseline 2/6 against treated 4/6, coverage 0/6 against 4/6. Four discordant pairs, exact p = 0.625: a hypothesis, not a subgroup result.
- **Nothing separates "the requirement works" from "the generator differed."** That still needs an effort-matched control this design does not have.
- Six briefs floor brief-level inference at 0.031 two-sided even with a clean sweep; observed was 1–1–4. Per-dimension inference is impossible at six pairs each.

---

## 18. Backlog item 1 measured — one floor was the instrument, the other was not, and the fix does not reach the gate

> **Two claims below are corrected by §19, which measured live output directly on 54 on-scope cells.** First, *"§17's 3/12 is therefore not a property of live output, and is withdrawn"* — live `production readiness` closes **1 of 6** on-scope, so the level was roughly right and the withdrawal was wrong. What is right is the narrower finding it was inferred from: the cell is satisfiable at 6/6, and the broken instrument made a thin corpus and an unsatisfiable cell indistinguishable. Second, *"per-dimension levels do not [survive]"* — all three dimensions §17 flagged reproduce directionally under the corrected instrument. The levels were noisier than §17 could know, not unreadable. Everything else in this section stands, and §19 corroborates the separation finding from a second direction.

The item read: *two situation families now measure the instrument, not the artifact. `context & brand fit` returned 1/12 — the situation asks about copy voice, bystander privacy or house-versus-native chrome, while the cell returns a precedence order. `production readiness` returned 3/12, failing wherever the situation demands a hard-bar test. Both need rewriting and re-screening before any further arm contrast.*

It also absorbed §15's own open line: *`Production readiness`'s rewrite rests on one clean case; re-run with fresh unlisted-value cases screened against the statement's own enumerations.*

### The design that separates the three standing explanations

One fixed product — a hotel mobile-key and stay screen, absent from the corpus and from §15's EV charging — so artifact of origin, which moved determinacy 17× more than band did, is removed by construction.

Five statement arms, every one 146–149 words, so the length confound §15 had to kill post hoc is dead a priori. Two situation conditions, six cases each: **name-only**, which reconstructs the procedure that produced the two floors, and **cell-informed**, where the writer sees the `4 → 5` question and the rubric's three case constraints. Both conditions test every arm, so probe difficulty cannot track the arm. Two screeners, blind to condition, judge scope and quotation; three blind appliers judge 60 pairs, 180 judgements. Predictions and a decision rule were registered before any agent ran.

### The probe procedure was the defect, and it is measurable

| | on-scope by both screeners |
|---|---|
| name-only cases | **0 of 12** |
| cell-informed cases | **12 of 12** |

Two screeners, unanimous on all 24, Fisher p = 0.000001. Their reasons are the same one every time: the case asks *what decides* rather than *what the rule returns* — "asks what governs accent placement, the rule itself, rather than the treatment that rule returns"; "asks which condition combinations QA should capture, not a hard-bar-or-negotiable ruling on a measured value."

And the scope of the case, not the statement, sets what the closure test can see:

| probe condition | load-bearing arms | performative arms | separation |
|---|---|---|---|
| off-scope (name-only) | 9/18 = 50.0% | 3/12 = 25.0% | +25.0 pp, Fisher p = 0.26 |
| on-scope (cell-informed) | 15/18 = 83.3% | 1/12 = 8.3% | **+75.0 pp, Fisher p = 0.0001** |

Nothing about the statements changed between those rows. **Both error directions move the right way**: the strongest arm goes 1/6 → 6/6, and the performative arm goes 3/6 → 1/6. An off-scope case does not merely fail a working rule — it passes a hollow one.

### The two dimensions have opposite diagnoses, and the item's premise held for only one

**`Production readiness` — instrument.** On on-scope cases the best statement closes **6/6, 18/18 judgements, 6/6 unanimous, zero quotation**, and it discriminates rather than answering one way: four cases return hard bar, two negotiable. The same six cases give a well-written enumerated hard-bar list **0/6**, so the cases are not easy — they are selective. §17's 3/12 is therefore not a property of live output, and is withdrawn. §15's open item closes as confirmed on fresh screened cases.

**`Context and brand fit` — corpus.** Its cell is satisfiable too (5/6 for a precedence order with mapped outputs, 4/6 for a treatment rule), but the shape live output actually carries scores **1/6**, which reproduces §17's 1/12 almost exactly. Here the broken instrument was *inflating* the weak arm (3/6 → 1/6), not deflating the strong one (4/6 → 4/6). **The backlog line's premise was wrong for this dimension**: its floor survives a corrected instrument.

### What was predicted, and what happened

P2 held and P5 held. P1 held for `context & brand fit` and was refuted for `production readiness` — predicted ≥ 4 of 6 on-scope under name-only, observed 0 of 6. **P3 was refuted in both directions at once**: the dimension predicted to move did not (4/6 → 4/6) and the dimension predicted to hold still collapsed (1/6 → 6/6).

**P4's refutation is the useful one.** A precedence order whose terms are each mapped to a visual consequence closes **5/6**; the same skeleton without the mapping closes **1/6**, on identical cases, 4 discordant pairs to 0. The cell does not license an unclosable shape. Three appliers who never saw the rubric reproduced its own diagnosis in their own words: "the ranking names no size or face"; "ranks brand fourth but sets no surface limit or treatment".

### The four failure shapes stop being a derivation and become a prediction

§14 derived the shapes backwards, from 34 of 38 statements already judged performative. This run wrote statements *to* three of them on purpose, mixed them with six generative mechanisms, and tested all nine blind:

| | cases closed |
|---|---|
| statements written to a named failure shape | **2 of 18 = 11.1%** |
| statements built on a generative mechanism | **29 of 36 = 80.6%** |

Fisher p = 0.000001. Precedence-with-no-output 1/6, requirement-with-no-threshold 0/6, ratio-with-no-anchor 1/6. **What passes is deliberately not recorded as a list** — six mechanisms cleared, and naming them here would convert a diagnosis into a menu, which is the rule-1 failure this repository has shipped twice.

### The fix does not reach the gate, and that was measured rather than assumed

§16 shipped a configuration that had never been measured and §17 reverted it. So the second phase tested the exact text that would ship, with the **judge's own band decision** as the outcome and blind-applier determinacy as ground truth. Ten statements — the five above plus five more spanning generative and failure shapes, ground truth measured on the same on-scope cases, 6 load-bearing to 4 performative. Three judges per variant, six independent agents; variant A is the closure-test instruction exactly as it ships on the judge agent today, variant B adds the case-scope constraint.

| | band-5 awards | recall on load-bearing | awards to performative | φ |
|---|---|---|---|---|
| A (as shipped) | 15/30 | 14/18 | **1/12** | **+0.68** |
| B (plus the constraint) | 16/30 | 14/18 | **2/12** | +0.60 |

**All three predictions refuted.** Recall is identical. Awards to performative statements rose, which the pre-registered rule made a veto on its own. And the mechanism does not fire: judges under A already choose an on-scope case **24 of 30** times, against 26 of 30 under B (p = 0.73), with **zero** cases off-scope by both screeners in either variant.

The reason is structural and worth stating plainly. **The harness deprived its situation writers of the cell text; the skill never does.** Every surface that assigns a band hands the judge the dimension's four boundary questions, so the case-picker is reading the `4 → 5` question when it picks. The defect was in the measuring instrument, not in the instructions the instrument was built to test. **Nothing ships to instruction text.**

### The consequence that outruns the item: every measurement from §14 on used the broken procedure

The record says so in its own words. §14's situations were written "under an instruction identical across dimensions" — an instruction identical across dimensions cannot contain the per-dimension `4 → 5` question. §15's were "written from the brief alone". §16's were "written from the brief before any artifact existed".

§15 half-caught it and did not generalise it. Its headline was `best` 12/18 against `typical` 5/18 — a 38.9 pp gap — and **restricted to the dimensions whose cases were on-question, best 10/10 against typical 1/10, a 90 pp gap.** That is this section's +25 → +75 pp, in the repository's own earlier data, recorded as a restriction on one run rather than as a property of the instrument. §16 and §17 applied no such restriction.

What that does and does not touch:

- **Paired arm contrasts survive.** The same situations tested every arm, so an off-scope case is off-scope for all of them and the pairing holds.
- **Per-dimension levels do not.** Every rate in §16 and §17 read as a property of a dimension — the 1/12, the 3/12, the 11/12 that made distinctiveness look fixed — was measured through a procedure that scores 0/12 on scope.
- **§17's null is weaker than its power calculation says.** That calculation was derived from observed rates; it assumes the instrument separates. This section measures the same instrument separating at one third of its corrected strength. A null returned by an instrument with 25 pp of separation is not the same evidence as a null from one with 75 pp.

### Two instrument findings, one of them a new defect

- **A leak screen that reads the statement cannot tell "printed" from "computed", and it over-flags exactly the statements that work.** The screeners flagged 5 of 12 `context & brand fit` cases as quotation for the best arms; the appliers' own declared marker flagged 1. On the case both screeners called a leak, all three appliers derived the answer through the statement's classifier. §15 asked for a post-write leak screen; this is the form it must not take. **The applier-declared marker is the instrument** — it costs one clause in the rating instruction and it is made by someone who has just done the derivation.
- **`Context and brand fit`'s cell is broad enough that its on-scope cases read like other dimensions' cases.** Four of its six cell-informed cases ask for a type, contrast or weight treatment. The screeners called them on-scope and the performative arm still failed them, so the contrast stands — but this dimension's determinacy is not cleanly separable from typography and colour, and that is a caveat on its numbers, not on the two conditions being compared.

### What §18 did not resolve

- **Why the gate fails in situ.** An independent judge running the closure test on one statement agrees with blind appliers 83% of the time at φ +0.68. The drafting model scoring its own statement in §17 ran at precision 0.652 and demoted 0 of 23. Those are different settings and are not directly comparable, but they point at *who runs the gate* rather than at *how it is worded* — and more drafting-side wording is exactly what v1.24.0 tried.
- **Constraint 3 of the closure test still rests on §15's single 2–1 split.** All twelve cell-informed cases fixed every other input, so this run had no contrast to measure it with.
- **Two dimensions, one product, one agent per case family.** Cases within a family are not independent draws, and nothing here licenses a claim about the other seven dimensions beyond the procedural one.

---

## 19. The levels re-measured on-scope — §14's null does not reproduce, and two of §18's claims are corrected

The item read: *§16 and §17 must be re-run with on-scope probes. Paired arm contrasts survive; per-dimension levels do not, and §17's null was returned by an instrument separating at one third of its corrected strength.*

### What was re-run, and what was deliberately not

**The v1.24.0 arm contrast was not re-run**, and the reason is recorded so it can be argued with. Its revert stands on a finding independent of probe scope — the +33 pp was an extraction artifact, and the baseline doubled from 7/27 to 14/27 once the extractor quoted rules complete. What does not stand is v1.25.0's second claim, that the re-measurement was a *powered* null. Against the measured sensitivity of the two instruments:

| | in rate terms | in true-class terms |
|---|---|---|
| §17 observed paired difference | +1.9 pp | +7.6 pp |
| §17 95% CI | [−15.7, +18.9] | **[−62.8, +75.6]** |

That is no constraint at all, and re-running it costs a full two-arm corpus to settle whether to un-revert a change with measured calibration harm. **What was re-run is the part the roadmap depends on: the levels.**

Six briefs in domains absent from the corpus, run through `SKILL.md` at v1.25.1. Nine statements extracted per artifact, complete including the tables their values live in. Situations written from the brief alone, before any artifact existed, by agents holding the nine `4 → 5` questions and the three case constraints. Two screeners, three blind appliers, 54 cells, 162 judgements.

**The corrected procedure holds at scale: 53 of 54 situations on-scope by both screeners**, against 0 of 12 for the name-only procedure. The one exception was excluded under the pre-registered rule.

### The table §16 and §17 were trying to produce

| dimension | closed | judgements | unanimous |
|---|---|---|---|
| Distinctiveness and owned assets | 5/5 | 14/15 | 4/5 |
| Typography craft | 5/6 | 15/18 | 6/6 |
| Interaction polish and motion | 4/6 | 12/18 | 6/6 |
| Attention path and hierarchy | 3/6 | 8/18 | 5/6 |
| Density and rhythm | 3/6 | 8/18 | 5/6 |
| Color, state, and contrast | 2/6 | 4/18 | 4/6 |
| Composition and spacing | 1/6 | 7/18 | 2/6 |
| Context and brand fit | 1/6 | 3/18 | 6/6 |
| Production readiness | 1/6 | 3/18 | 6/6 |
| **pooled** | **25/53 = 47.2%** | | |

Two of the three floors are described by three blind appliers in the rubric's own vocabulary, unprompted. `Production readiness`: *"nothing assigns unlisted values to either list; the checks cover only what is listed."* `Context and brand fit`: *"the precedence only ranks categories; no stated treatment."* Those are the closed-world statement and the precedence ladder with no output, reproduced on five briefs of six.

### §14's null does not reproduce

| band the artifact assigned itself | cases closed |
|---|---|
| 3 | 1/6 = 16.7% |
| 4 | 14/34 = 41.2% |
| 5 | 10/13 = 76.9% |

Band 5 against band ≤4 is **76.9% vs 37.5%, +39.4 pp, Fisher p = 0.0235**, and the ladder is monotonic across three levels. §14 measured the same comparison at 39.3% vs 36.0%, +3.3 pp, p = 0.52, with the sign inverting once dimension was adjusted for.

**Half of that is dimension mix, and it must be said.** Band-5 claims concentrate in three dimensions — distinctiveness 4, attention 4, typography 3 — and are entirely absent from composition, colour, density and production. Mantel–Haenszel stratified on dimension the odds ratio falls from 5.56 to **1.80**: it shrinks by half but, unlike §14, does not flip. Dimension identity still moves determinacy more than the band does, by 2.1× where §14 measured 21×.

**And the two explanations are confounded.** §14's corpus predates the closure test; this one is v1.25.1 with two releases of band-5 discipline behind it. Either the instrument was hiding the separation, or the closure test created it. Both readings favour the current skill and they are different claims; nothing here separates them.

### Two claims in §18 are wrong, and the corrected versions are narrower

- **`Production readiness`'s 3/12 was withdrawn, and should not have been.** Live output closes **1 of 6** on-scope, against §17's 3 of 12. The level reproduces. What §18 established and what it inferred came apart: the *cell* is satisfiable — a serious test closed 6/6 unanimously with zero quotation — and live output does not satisfy it. Both were true at once, and the broken instrument is exactly what made them indistinguishable. The narrower finding stands; the withdrawal does not.
- **"Per-dimension levels are not readable as properties of a dimension" was too strong.** All three dimensions §17 flagged reproduce directionally under the corrected instrument: distinctiveness high, context low, production low. What the broken instrument cost was resolution and the ability to attribute a floor, not the direction.

§18's other findings are untouched, and its central one is corroborated from a second direction: an instrument that separates load-bearing from performative statements by 75 pp also separates self-assigned band 5 from band ≤4 by 39 pp, where the off-scope instrument separated it by 3.

### The gate under-fires at both surfaces, and it is not about who runs it

Every artifact prints its own band per dimension, and all six were independently re-banded by three `mobile-design-judge` agents. Against blind-applier determinacy on the same 53 cells:

| | band-5 claims | precision | over-claims | under-claims | φ |
|---|---|---|---|---|---|
| the artifact's own claim | 13/53 | 0.769 | 3 | 15 | **+0.340** |
| independent judge, majority of three | 18/53 | 0.667 | 6 | 13 | +0.280 |
| blind appliers | 25/53 | — | — | — | — |

**C2 is refuted.** The independent judge is not better calibrated — φ +0.280 against +0.340, and the three judges individually span the artifact's own value at +0.360, +0.205 and +0.322. Paired on cell, judge-correct-only 2 against artifact-correct-only 3, McNemar p = 1.000. **And the judge is barely independent: it returns the identical band on 47 of 53 cells**, and lands below the artifact's own band on exactly one.

So the hypothesis §18 left open — that the gate's problem is *who runs it* rather than how it is worded — is dead, and the failure mode is the opposite of the one this repository has been chasing. §17 measured over-claiming at precision 0.652. Here **both surfaces under-claim**: 25 cells close for a blind reader and the drafting side claims 13.

The mechanism that fits is uncomfortable and worth stating as a hypothesis rather than a result. Whoever runs the closure test on an artifact they can see **knows where its holes are, and picks a case there**; a blind writer working from the brief picks an ordinary one. The rubric guards one side of that — *"the case has to be ordinary, not an edge case chosen to be survivable"* — and does not guard the other. The measured failure is now in the unguarded direction.

### What §19 did not resolve

- **Nothing ships to instruction text, for the second release running.** Three findings here would each motivate one — thin production and context statements, a one-sided case-selection guard, distinctiveness's cheap top band — and each would need its own measurement of the shipped configuration first. That is the v1.24.0 lesson, and paying it twice is cheaper than paying the revert again.
- **Distinctiveness is at ceiling for the second measurement running**, now on fresh situations written by different agents from different briefs, so it is not an artifact of §17's rewritten probes. Its `3 → 4` already requires repeat locations named beyond the screen, which leaves its `4 → 5` little to add — a structural suspicion, untested.
- **The instrument and the intervening releases are confounded** in the §14 comparison, and this design cannot separate them. Re-scoring §14's own corpus with on-scope probes would, and that corpus no longer exists.
- **One case per cell.** A statement that closes the applier's case might not close another, so "under-claim" is measured against a single ordinary case, not against the dimension.

---

## 20. The gate's under-firing is not case selection, and enforcing the constraint that explains it makes the gate worse

The item read: *the gate under-fires and it is not about who runs it. The standing hypothesis, untested: whoever can see the artifact knows where its holes are and picks a case there, while a blind writer picks an ordinary one — and the rubric guards only the too-easy direction.*

### The design was already paid for

Every cell had one statement and two cases: the one written from the brief by an agent who never saw an artifact, and the one the judge chose for itself with the artifact in front of it. Only the chooser varies. **Both sets were re-rated in one pass by one cohort** — rating only the new set would have confounded the comparison with rater drift — and two screeners judged all 108 cases mixed and blind to origin against the rubric's own three case constraints.

### The hypothesis is wrong

| | closed |
|---|---|
| blind-written case | 23/54 = 42.6% |
| self-chosen case | 20/54 = 37.0% |

Discordant 8 to 5, McNemar **p = 0.58**. Self-chosen cases are also **not edge cases**: 49/54 ordinary against 52/54, p = 0.44. Neither half of the hypothesis survives.

What separates them is specification. Self-chosen cases run **16 words against 83**, and inside the self-chosen arm the specification screen is the only one that predicts anything:

| self-chosen case | closed |
|---|---|
| fixes every other input the rule needs | 17/36 = 47.2% |
| leaves a second input open | 3/18 = 16.7% |

Fisher p = 0.038. Scope differs between the two origins (42/54 against 54/54, p = 0.00025) and predicts **nothing** inside the self-chosen arm — 15/42 against 5/12, p = 0.74. A real difference with no consequence.

### The judge is not the problem, and the drafting side is

| | band 5 |
|---|---|
| the artifact's own claim | 13/54 = 24.1% |
| judge 1 | 18/54 = 33.3% |
| blind appliers, on the judge's own case | 20/54 = 37.0% |
| blind appliers, on a blind-written ordinary case | 23/54 = 42.6% |

**Judge 1's band decision matches the blind verdict on its own case in 48 of 54 cells — 88.9%**, against 66.7% for the artifact's own claim. And 88.9% is at this instrument's ceiling, because the same run measured the instrument against itself for the first time in the series: a fresh cohort reproduced the original cohort's verdict on 46 of 54 blind-written pairs, **85.2%**. A cell-level verdict flips about one time in seven between independent cohorts, and nothing in this series resting on fewer than about eight cells should be read as a result.

So the judge executes the closure test about as consistently as the instrument that measures it. The under-firing is 10 cells on the drafting side and 5 on the judging side, and the drafting side cannot be diagnosed the same way because it never prints its case — printing it is what v1.24.0 shipped and v1.25.0 reverted.

### The intervention hit the mechanism exactly, and moved the outcome the wrong way

Constraint 3 is the rubric's own — *"fix every input the rule needs except the one under test"* — and §15 recorded it as the weakest of the three, resting on a single 2–1 split. It sits on the rubric and on none of the three surfaces that run the closure test. Unlike the scope constraint tested in §18, which judges already satisfied 24 times in 30, this one they fail two thirds of the time, so there was room for an instruction to bind.

Six artifacts, two variants, three judges each; judge 1's 108 cases screened blind to variant and rated by one cohort.

| | A, as shipped | B, plus constraint 3 |
|---|---|---|
| case fixes every other input | 6/54 | **52/54** (p < 10⁻⁵) |
| case length | 18 words | 31 words |
| case on-scope | 50/54 | 51/54 (p = 1.00) |
| determinacy of the judge's own case | 37.0% | **42.6%** |
| band-5 award rate, three judges | 35.2% | 32.1% |
| recall against an ordinary blind case | 40/69 | **34/69** |
| over-claims | 17/93 | 18/93 |
| φ | **+0.411** | +0.317 |

**The clause binds exactly as designed and the gate gets worse.** The cases become well-specified, and their determinacy rises to 42.6% — precisely the rate of cases written by someone who never saw the artifact, which is what a fair case should look like. And the judge, holding better cases, awards *fewer* band 5s and misses six more load-bearing statements. Over-claims stay flat, so this is not a loosened gate; it is a tightened one, in the direction the rubric was not worried about.

The mechanism that fits, stated as a hypothesis: a case that names its surrounding conditions gives the judge more surface on which to notice something the statement does not cover. Constraint 3 exists to stop a case reading as undecided when only a second input is missing — to prevent false negatives. Measured at the only surface where it has ever been measured, enforcing it **produces** them.

**Nothing ships.** That is the third instruction change in three releases that was measured and withheld, and the second whose measured effect was the opposite of its intent.

### Two instrument findings

- **Applier reliability is 85.2%**, first measured here. It is the ceiling for every claim in §§14–20.
- **The specification screen is not stable across cohorts.** One cohort called 36 of 54 self-chosen cases well-specified; another called 6 of 54 on materially the same kind of case. Within-run contrasts hold, because the same screeners judged both arms — the 47.2%/16.7% split and the 6/54→52/54 shift are both within-run. **Absolute rates from this screen do not transfer between runs and should not be quoted across sections.**

### What §20 did not resolve

- **The drafting side.** It carries 10 of the 15 cells of under-firing and cannot be diagnosed without its case, and printing its case is a change this repository already shipped and reverted for unrelated reasons.
- **Why a better case makes the judge more conservative.** The hypothesis above is untested, and the natural test — vary case specification while holding the judge's instruction fixed — is a different design from this one.
- **Constraint 3's standing in the rubric is now worse than §15 left it.** It was already the weakest of the three, and the one place it has been measured it costs recall. Removing it would be an unmeasured change in the other direction, so it stays and this is recorded against it.

---

## 21. Context is a precision filter, not a suppressor — and §20's decomposition rested on one judge

The item read: *the drafting side carries the under-firing and cannot be diagnosed without its case. Printing the drafting case is what v1.24.0 shipped and v1.25.0 reverted, so a diagnosis needs a design that gets at it without that mandate.*

### The design that avoids the mandate

Do not elicit the case. **Vary the context the band is assigned in, holding the statement fixed.** Two numbers already in hand pointed the same way: judges shown a statement alone in §18 had 78% recall on load-bearing statements, judges shown the whole artifact in §20 had 58%, and the band-5 rates ordered themselves by how much the scorer held.

Three arms in one cohort — whole artifact, brief plus the nine extracted passages, passages alone — six briefs, three judges each, 54 agents, structurally identical: same ladder, same closure test, same output fields, nine cells per agent. Ground truth is the blind applier on an ordinary blind-written case, 23/54.

| scorer | band 5 | recall | over-claims | precision | φ |
|---|---|---|---|---|---|
| the artifact's own claim | 13/54 = 24.1% | 9/23 | 4 | **0.692** | **+0.340** |
| judge, whole artifact | 47/162 = 29.0% | 32/69 | 15 | 0.681 | +0.330 |
| judge, brief + passages | 53/162 = 32.7% | 31/69 | 22 | 0.585 | +0.224 |
| judge, passages only | 59/162 = 36.4% | 31/69 | 28 | 0.525 | +0.152 |

**The ordering predicted by context volume is exactly right, and it means the opposite of what was predicted.** K3 held: 24.1% < 29.0% < 32.7% < 36.4%, monotone. K1 and K2 are refuted — the passages-only arm reaches 36.4% rather than the predicted 45%, and its recall is **31/69 against 32/69**. Stripping the artifact away recovers **no** load-bearing statement. Every one of the twelve extra band-5 awards is a false positive: over-claims run 15 → 22 → 28 and precision falls 0.681 → 0.585 → 0.525.

So context is not suppressing true band-5s. It is removing false ones, and it costs nothing in recall. **The drafting side, holding more context than any judge, is the most precise scorer of the four and has the highest φ.**

### Recall does not move, for anything

| arm | recall against the blind instrument |
|---|---|
| whole artifact | 32/69 = 46% |
| brief + passages | 31/69 = 45% |
| passages only | 31/69 = 45% |
| the artifact's own claim | 9/23 = 39% |
| §20, judge with constraint 3 enforced | 34/69 = 49% |
| §20, judge as shipped | 40/69 = 58% |

Across every manipulation this series has tried — who runs the gate, how the case is picked, how specified the case is, how much context the scorer holds — recall against the blind instrument sits near half and does not respond. That looks like a property of two different questions disagreeing, not a property of any scorer, and it is the shape of the next item rather than of this one.

### Two corrections, one of them to §20

- **§20's decomposition rested on a single judge.** It reported the under-firing as *"10 cells on the drafting side and 5 on the judging side"*, taking judge 1's 18/54 as the judging surface. The median of three judges in this run is **15/54**, so the split is 10 against 8 and the drafting side does not carry it. Two cells is well inside the 1-in-7 cohort flip rate. **Rule 14 repeating: a decomposition inferred from one judge is not a decomposition.**
- **Not every band below 5 is a closure-test failure.** A dimension that fails 1 → 2, 2 → 3 or 3 → 4 never reaches the closure test, while the blind instrument only ever tests the 4 → 5 property. Of the 23 cells the blind applier called determined, **one** never reached the question (`p3/production`, three judges at band 3), so the real closure-test disagreement is **12 cells, not 15**. A small correction, and it goes the same way as the first one: the gap is narrower than §20 reported.

And the conservatism is not specific to the top band. The judges place **9 of 54** cells at band ≤ 3 where the artifact places **6** — they are harsher than the drafting side on the lower rungs too.

### Three hypotheses are now dead

| hypothesis | where | outcome |
|---|---|---|
| the gate's problem is *who runs it* | §19 | judge φ +0.280 against the artifact's +0.340; identical band on 47 of 53 cells |
| the gate picks a *harder* case | §20 | not harder (p = 0.58), not edgier (p = 0.44) |
| the surrounding artifact *suppresses* band 5 | §21 | it filters false positives; recall flat, precision falls 0.68 → 0.53 |

Each died with a measurement showing the intervention it motivated would cost something and gain nothing. **Nothing ships, for the fourth release running.**

### What §21 did not resolve

- **Who is right on the twelve.** A blind applier holding one ordinary case and a judge walking four boundary questions with the artifact in front of it are answering different questions, and neither is privileged. This design cannot adjudicate them, and the whole series has been treating the first as ground truth since §14.
- **Whether "under-firing" was ever the right frame.** The stability of recall across every arm suggests the gap is definitional rather than behavioural. Testing that means measuring the instrument against something other than itself, which no design in this series has done.
- **The drafting side's own case is still unobserved**, and this run shows the question it was wanted for was the wrong one.
