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

> **Superseded by §40.** This section describes the tree at v1.20.0 — twenty sections and nineteen
> releases ago — and its state, backlog and open questions are all stale. It is kept because the record
> is append-only. **A cold reader should start at §40.**

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

---

## 22. P1-8 shipped — the large-screen decision surface, measured pre/post on a checkable outcome

Backlog item 8. `docs/patterns-catalog.md` carried fourteen sections of phone patterns and no entry
that decides a layout at regular width, while `SKILL.md` step 8 routes every pattern-level decision
to it and Mode D checks an observed pattern against its Use-when / Avoid-when rules. A tablet
request therefore reached the catalog and found nothing.

### What the reconnaissance changed about the item

§4's framing — *"this is the item that stops the model confidently choosing bottom navigation at
1366 pt"* — was already false when it was written. `SKILL.md`'s Platform policy block states six
tablet rules in the entrypoint (breakpoint, canonical layout, bottom bar → rail → sidebar,
multitasking and resize, additive input, detail-pane empty state), and `docs/adaptive-layout.md`
expands all six. Counting those six is counting a ceiling.

A grep of the shipped corpus before the run placed each candidate indicator:

| indicator | already stated where |
|---|---|
| overlay by size class | `adaptive-layout.md` §4; `patterns-catalog.md` §2 popover entry |
| supporting pane + collapse target | `adaptive-layout.md` §3 |
| action placement at regular width | **nowhere** — "toolbar" and "inspector" appeared in no shipped file |
| columns / reading measure | `quality-bars.md`; `adaptive-layout.md` §7 |
| cross-pane drag + non-drag path | `quality-bars.md`, `adaptive-layout.md` §6; "cross-pane" nowhere |
| detail-pane empty-state content | both say to define it; neither says what it contains |

So P1-8 is a **retrieval and consolidation** change, not new knowledge — it moves large-screen
decisions onto the surface the workflow routes to, in the Use-when / Avoid-when / Red-flag form a
Mode D review can check against. Only action placement is genuinely new content.

### Design of the P1-8 measurement

Within-brief pre/post on six tablet-forcing briefs, one response per brief per arm: an iPadOS
clinical spec, an Android POS concept, a cross-platform field-service concept, an iPadOS Stage
Manager spec, an Android classroom concept, and a D2 review of a described stretched-phone iPad.
Writers ran `SKILL.md` end to end and were told nothing about what was being measured.

Thirteen binary indicators, pre-registered with the corpus and the decision rule before the baseline
ran, in two tiers:

- **Tier A** (six) — the entrypoint's own tablet rules, committed as a **control** with its ceiling
  predicted in advance.
- **Tier B** (seven) — the decisions §4 listed for §15 that no file stated: overlay by size class,
  supporting pane with a collapse target, action placement at regular width, columns or measure,
  cross-pane drag with a non-drag path, detail-pane empty-state content, and a rejected large-screen
  alternative with the mechanism that killed it.

Every response was coded twice by independent agents against the codebook, working from unlabelled
copies under opaque filenames, quoting the earning phrase for every 1.

**§15 was drafted before a single response was read**, so the section could not be shaped around the
gaps the baseline happened to show. Rule 6.

### Limitations, written before the data

- Writers are subagents on this host, not the surface the skill ships to. n = 1 per brief per arm:
  a one-cell move on a single indicator is inside noise, and only tier totals are the pre-registered
  outcome.
- Arms are confounded with run order. No re-randomisation.
- Rater blinding is imperfect — a post response can name `§15` or the new golden. Coders scored the
  codebook only and recorded any such tell.
- The author of the change chose the indicator set. Mitigated by the pre-committed control tier and
  by taking Tier B's items from §4, written before this session.
- Thirteen indicators, no multiplicity correction.
- **The post arm ran one edit behind the shipping tree.** All six post writers read the pre-edit
  `SKILL.md`, whose golden-area list did not yet name the tablet golden, and the pre-edit
  `adaptive-layout.md` row (`~340 dp` rather than `≥ 320 dp`). Verified from the six agent
  transcripts rather than assumed: the arm is homogeneous, and both differences run against the
  change — five of six writers reached the new golden through `docs/golden-examples.md` without any
  entrypoint pointer, and the sixth reached the new fixture the same way.
- **The fixture is closer to its probe than the golden is to its probes.** T6 reviews a described
  stretched-phone iPad and the committed fixture reviews a different product with the same defect
  class, so T6's post movement is partly a near-neighbour retrieval. T1–T5 have no such neighbour.

### The result

Coding was near-deterministic: **155 of 156 cells agreed between the two independent coders**
(99.4%), the single disagreement being one Tier B cell on the baseline review.

| tier | baseline | post | delta |
|---|---|---|---|
| A — the entrypoint's own six rules | **36/36 = 100%** | 36/36 = 100% | 0.0 pp |
| B — the seven §15 was written to add | **37.5/42 = 89.3%** | 36/42 = 85.7% | -3.6 pp |

Every indicator in Tier A fires in every response in both arms: 6 of 6 on breakpoint, bottom bar
confined to compact, rail or sidebar named, canonical layout with its collapse rule, multitasking
and resize, and additive input. Not a ceiling approached — a ceiling reached, twice, on 36 cells.

Tier B was already at 89.3% before §15 existed. Its three sub-ceiling indicators are brief-dependent
rather than defective: cross-pane drag is absent from both arms of the point-of-sale and
field-service briefs, where there is no second pane to drag between, and the supporting-pane
indicator is the one cell the coders split on.

The whole Tier B delta is **one response**. T3 (cross-platform field service) lost the measure rule
and the cross-pane drag path; T5 gained the supporting-pane decision; T6 lost half a cell to the
coder split. Per-brief totals out of 13: T1 12 -> 12, T2 12 -> 12, T3 13 -> 11, T4 13 -> 13,
T5 12 -> 13, T6 11.5 -> 11. Against the pre-registration, single-cell moves are noise and only the
tier totals count.

| prediction | outcome |
|---|---|
| P1 Tier A baseline >= 70% | **confirmed**, and at the maximum |
| P2 Tier B baseline <= 35% | **refuted** — 89.3%, and the amendment that saw it coming was deliberately not allowed to move the number |
| P3 Tier B post - baseline >= +20 pp | **refuted** — -3.6 pp |
| P4 Tier A within +/- 10 pp | confirmed — 0.0 pp |

**Decision rule 2 fires**: Tier B's baseline is above 70%, so this is a ceiling. The
instruction-effect claim is withdrawn. §15, the golden and the fixture ship as calibration and
lookup material, and **no behaviour change is claimed for any of them.** That is the fifth
consecutive intervention in this series measured and not credited — but the first where the null
was predicted from a coverage audit before the run rather than discovered after it.

### What the measurement did find

The baseline responses cite `docs/patterns-catalog.md` as the source of their large-screen pattern
choice. Verbatim from the v1.25.4 arm:

- T3: *"(from: baseline — the list-detail/record-detail pairing `patterns-catalog.md` and the SaaS
  pack imply for this surface)"*
- T5: *"(from: baseline — `patterns-catalog.md` list-detail + Material 3 + the education and
  enterprise packs)"*

At `5ebf8d7` that file contained **zero** occurrences of `list-detail`, `sidebar`,
`navigation rail`, `tablet`, or `Split View`. Step 5.5 defines D1 as *what
`docs/patterns-catalog.md` and the domain pack imply for this surface*, and the model was satisfying
that provenance against a file with none of the content — reaching the right answer through
`adaptive-layout.md` and `quality-bars.md`, then attributing it to the catalog.

So the defect P1-8 actually closes is not a wrong design decision. It is an **unfalsifiable
citation**: the `from:` line the skill requires pointed at a file that could not support it, and a
reader auditing the provenance would have found nothing there. §15 makes the citation true. This
series has already recorded that a candidate set with no provenance was never sampled; a provenance
naming absent content is the same failure one rung down, and it is invisible to every shape check
in the repo because the citation is well-formed.

### Rule 17

**Measure the surface's coverage before writing content for it, and let the audit move the
prediction, not the conclusion.** §4 named this the item that stops the model choosing bottom
navigation at 1366 pt. The model never chose it: 36 of 36 on the control tier, in the arm without
§15. The proposal was written when `SKILL.md` carried no tablet block, and it was never re-checked
against the corpus after v1.17.0 added one. A backlog item's premise ages, and the cheapest thing
that can be done to it is a grep.

### What §15 is worth, stated without inflation

- It makes the step 5.5 provenance line checkable for large-screen work.
- It is the only surface a Mode D review can check an observed tablet layout against with
  Use-when / Avoid-when / Red-flag rules; the post review quotes the §15 red flag directly.
- Action placement across pane and window toolbars is content that existed in no shipped file.
- None of that is a measured behaviour change, and none of it should be described as one.

### What this design cannot answer

- Whether §15 matters for a weaker model, or for a host that loads three files instead of twenty.
  The writers read `adaptive-layout.md` and `quality-bars.md` in both arms; this measures §15's
  marginal value **given the rest of the corpus is read**, which is the easiest case for a null.
- Whether the artifacts improve output *quality* at large widths. Every indicator here is a
  presence check. A response can name a breakpoint, a rail and a collapse rule and still be a bad
  tablet design, and nothing in this run would see it.
- Whether the fixture teaches or merely matches: T6 and the committed fixture share a defect class
  by construction.

---

## 23. P1-2 measured — the first intervention in this series that moves the outcome, and it costs something

Backlog item 8's successor. P1-2 as written in §3 is four pieces: `docs/color-system.md`, a layout
section in the bars, motion by cited platform curves, and type-scale math — plus broadening Mode E.

### The audit ran first this time, and the gate ran before the writing

Rule 17, applied. A grep of the corpus placed every piece before anything was written: colour
existed as principle (`design-quality.md` §4) and as contrast minimums, but nothing derived a role
from a supplied brand or said what a pair becomes in dark mode; `cubic-bezier`, `spring`,
`dampingRatio`, `stiffness`, `stagger`, `baseline grid` and optical alignment returned **zero** hits
corpus-wide; every "tracking" hit was the verb.

But P1-8 established that a hole in the corpus is not a hole in the output. So the design added an
**early-stop gate**: code the baseline first, and if the target tier is already at 70%, stop before
writing anything. Fourteen indicators, six craft-forcing briefs, pre-registered with the decision
rule; `C-honest` — no invented brand value, no contrast ratio asserted as measured — pre-registered
as a **one-way gate** in both branches.

The gate did not fire: **48.3%**. But its profile redefined the item.

| baseline, gate pass | cells of 6 |
|---|---|
| C-role, C-pair | 6.0, 6.0 |
| C-dark, C-rule | 5.0, 5.0 |
| C-honest | 6.0 — no violations |
| L-scale, T-ratio | 6.0, 5.0 |
| L-col, L-rule | 4.0, 4.5 |
| M-scale | 2.0 |
| T-map | 1.5 |
| L-grid | 1.0 |
| **T-track** | **0.0** |
| **M-curve** | **0.0** |

**Colour — the piece §3 lists first — is the one piece that was not needed.** Roles, pairs with
their required ratio, the dark transform, and a rule for an unlisted role all sit at 83–100% before
any file existed, and not one response asserted a measured ratio or invented a brand hex. Writing
`docs/color-system.md` would have repeated P1-8 exactly. It was **withdrawn from the release on the
data**, and Mode E was left alone: renaming a primary mode is a MAJOR bump under
`docs/versioning.md`, and nothing here pays for it.

### The causal lever, found by reading what the instruction asks for

`M-curve` was 0 of 6 because **the corpus asks for exactly what it got**. Step 5.5 said *"one
recurring transition, its duration taken from `docs/quality-bars.md`"* — duration only — the bars'
easing section offered "ease-out (decelerate)" as prose, and the art-direction catalog's entries say
"standard curve". A doc alone would have been inert by construction, so the release changes the
**request** as well as the substrate: the motion signature now has to name its curve as a platform
token or its control points.

### The result of the P1-2 contrast

Baseline and post were coded together in one blind pass, as pre-registered — the gate's numbers were
thrown away rather than reused. Inter-coder agreement **156/168 = 92.9%**.

| tier | baseline | post | delta |
|---|---|---|---|
| target (the ten indicators the substrate supplies) | 28.5/60 = 47.5% | **48.0/60 = 80.0%** | **+32.5 pp** |
| all thirteen non-guard | 45.0/78 = 57.7% | 64.0/78 = 82.1% | +24.4 pp |
| `C-honest` guard | 6.0/6 | 6.0/6 | 0.0 |

| indicator | baseline | post | delta |
|---|---|---|---|
| T-track | 0.0 | 6.0 | **+6.0** |
| M-curve | 0.0 | 5.0 | **+5.0** |
| T-map | 1.5 | 6.0 | **+4.5** |
| L-grid | 1.0 | 5.0 | **+4.0** |
| M-scale | 1.0 | 3.0 | +2.0 |
| L-rule | 4.5 | 6.0 | +1.5 |
| L-col | 4.0 | 4.5 | +0.5 |
| C-role | 6.0 | 5.0 | −1.0 |
| C-rule | 5.0 | 4.0 | −1.0 |
| C-pair | 6.0 | 4.5 | −1.5 |
| C-dark | 5.5 | 4.0 | −1.5 |

**Pre-registered rule 1 fires**: target tier +32.5 pp against a +15 pp threshold, the `C-honest`
guard flat at 6/6, and no non-guard indicator down more than the two-cell limit. This ships, and the
effect is claimed. **It is the first intervention in this series to move an outcome it was measured
on.**

### What it costs, and why that is not noise

Every one of the four colour indicators moved down. The colour block falls **22.5/24 to 17.5/24**.
Each individual drop is inside the pre-registered noise band, but four indicators moving the same
way is a pattern, and the totals say what it is:

- **Response length is flat** — 23,617 words baseline against 23,297 post. Nothing was truncated.
- **Half the loss is one brief.** C1, the typography-and-spacing-system request, goes 3.0 → 0.5 on
  colour. Colour is not in Mode E's scope; the baseline volunteered it, and the post arm spent that
  room on the tracking table, the platform-style mapping and the grid instead. That is the substrate
  working, not failing.
- The remaining loss is ≤ 1 cell in each of three briefs.

So: **substrate added to one craft area displaces statements in the areas it did not touch, at
constant output length.** The budget is finite and this release spent some of it.

### Rule 18

**When you add substrate to one area, measure the areas you did not touch.** A target tier that
moves +32.5 pp while an untouched tier quietly gives back five cells is a trade, and a design that
only instruments the intervention's own target cannot see the price. Every measurement in §§14–22
scored only what its change aimed at.

### Incidental: the cohort worry does not apply to this instrument

The gate pass and the contrast pass are different rater cohorts scoring the same six baseline
responses. Target tier: **48.3% against 47.5%**. The specification screen moved 36/54 against 6/54
between cohorts on materially the same cases; this instrument moves 0.8 pp. Mechanical
presence-of-a-rule checks transfer between cohorts; graded judgements do not. Do not generalise the
§21 caution to both kinds.

### What the P1-2 design cannot answer

- **Presence is not quality.** Every indicator asks whether a rule is stated, never whether it is
  the right rule. A response can name `emphasized decelerate`, a 4 pt grid and a tracking table and
  still be an ugly screen. Nothing here measures that, and it is now the top open item.
- **`M-scale` reached only 3.0/6.** The distance/size rule and the stagger cap are in the doc and
  half the responses ignored them. Available substrate is not used substrate.
- **`L-col` is the weakest indicator** — five of the twelve coder splits are on it, because a stated
  margin sits on the edge of its definition. Its +0.5 carries no weight.
- **Colour's measured floor is unreconciled.** This instrument says colour is at 93.8% before the
  change; §§16–19 measured `Color, state and contrast` at a live floor of 2/6 with a stricter
  rubric-boundary instrument. Both cannot be a full description. Which one is measuring the thing
  that matters is open, and it is the same question as backlog item 1 wearing different clothes.

---

## 24. Presence is not quality — the review reads it, the score does not, and one cap closes the gap

The top open item after §23: every indicator in §§22–23 asks whether a rule is *stated*, never
whether it is right. The backlog claimed nothing in the repo separates a presence-complete answer
from a presence-complete answer whose values are wrong. Rule 2 of this series says an instrument is
worth nothing until it is shown to separate a deliberately bad corpus from a good one, so that is
what was built — applied to the whole instrument stack rather than to one metric.

### The corpus

The good arm is **real output**: the six post-arm responses from §23, on the v1.27.0 tree. Six
mutation agents injected **six defects each** under one hard constraint — a defect replaces a value
with a wrong value and never deletes a statement, so every presence indicator that fired before
still fires. Ground truth is known by construction: each defect cites the repo file whose bar it
breaks. Headings are identical between twins; only values and their justifications changed.

The taxonomy was fixed in advance: a numeric bar violated, a pattern used against its own Use-when,
motion semantics inverted, scale incoherence, an accessibility hole **stated as a deliberate
decision**, and a context-defaults inversion. Each written the way a confident wrong designer writes
it — asserted, reasoned, internally consistent.

### Phase 1 — the premise is half right, and it is the other half

| instrument | outcome | prediction |
|---|---|---|
| **Mode D review**, defects named | **34/36 = 94.4%** — D1 6/6, D2 5/6, D3 6/6, D4 6/6, D5 6/6, D6 5/6 | ≤ 50%, **refuted** |
| **the rubric score** those same reviews produce | good median 3, mutated median 3; projected 4 and 4 — **0 bands** | < 1 band, confirmed |
| **`docs/self-review.md`** in the author's seat | "revise" on 6/6 mutated **and 3/3 good** | < half, refuted and useless |
| findings raised | 68 on the good arm, 73 on the mutated arm | — |

The review reads quality almost perfectly, including the classes predicted to be hardest — a density
inversion against the resolved context default, and a pattern used outside its Use-when. **The score
does not.** The same document lists 34 defects under `Findings` and then returns the same median.
Two reviews explicitly *praised* an injected value while catching the other five.

An isolated scoring harness — artifact plus rubric, no review — makes it starker: **4/5 to all six
good artifacts and 4/5 to five of six mutated ones**, and **not one cap applied anywhere in twelve
scorings**. The cap machinery was decorative.

The pre-registered decision rule had no branch for high detection with zero score separation. That
gap is recorded, not backfilled into a branch that "fired".

### The diagnosis is in the rubric's own sentence

> A cap clamps the artifact score downward, after the median. It never changes a dimension band — a
> band records what the artifact states.

Every one of the thirty-six boundary questions asks whether something is **stated**: named, decided,
given values, generalised into a rule. None asks whether the value is right. Correctness could only
enter through the caps, and none of the eight covered a stated value that contradicts a bar.

### Phase 2 — one cap, measured on the same corpus

Added to `docs/design-quality-rubric.md`: a **contradicted-value cap**, graduated (3/5 for one
contradiction, 2/5 for two or more or any against a touch, contrast or state-coverage bar), plus one
line in the scoring method saying that checking the caps means reading emitted values against the
bars they claim to respect.

**No deliberate-deviation escape.** Every injected defect states a reason — that is what makes a
wrong value read as a decided one. An escape keyed on "a reason was given" would neutralise the cap
against exactly the artifacts it exists for. The only exit is a deviation the *user's input*
requires, named with the input that requires it.

Same twelve artifacts, same blind scoring harness, before and after:

| | good | mutated | median separation |
|---|---|---|---|
| rubric as it stood | 4 4 4 4 4 4 (median 4) | 4 3 4 4 4 4 (median 4) | **0** |
| with the cap | 4 4 3 3 4 4 (median 4) | 2 2 2 2 2 2 (median 2) | **2** |

All three pre-registered conditions hold: separation ≥ 1 band (2), the good arm's median does not
fall (4 → 4), and 6 of 6 good artifacts stay at 3/5 or above. The mutated arm is unanimous.

### The two good-arm caps are true positives, and they are the most useful result here

W05 and W07 dropped to 3/5, and both were checked by hand against the source:

- **W05** states Label 13 pt above Numeric 12 pt — a 1.083× adjacent-role ratio against the 1.125×
  minimum in `docs/quality-bars.md`, in a spec that cites that same bar for any new role.
- **W07** puts the action bar at safe area + 8 pt, **naming** the 44 pt home-indicator bar it is
  breaking and arguing the thumb zone requires it.

Both are real. **Two of six real skill outputs, at 80% on the presence tier, contain a value that
contradicts a bar** — and the old score gave all six 4/5. The single-contradiction tier landing them
at 3/5 rather than 2/5 is the graduation working, tested by the arm it was not designed for.

W07 also exposed a contradiction inside the corpus: `docs/quality-bars.md` told authors to state a
reason when deviating, while the new cap says a reason does not lift it. The two now say the same
thing — stating the deviation keeps the artifact honest without making the value right.

### Rule 19

**An instrument built out of presence questions cannot become a quality instrument by being applied
more carefully.** The rubric's thirty-six boundary questions are well designed and they all ask the
same kind of thing. No amount of care at the dimension level produces correctness, because
correctness is not what a band records — it took a separate mechanism, at the one place the
architecture already had for "a consequence of what is stated". Before assuming an instrument is
under-applied, read what its questions are *about*.

And the corollary that made the fix work: **the finding machinery already knew.** The review named
34 of 36 defects while the score ignored all of them. When two halves of one instrument disagree
that completely, the fix is a wire between them, not a better half.

### What this cannot answer

- **Six defects per artifact.** Every mutated artifact tripped the two-or-more clause, so the
  1-vs-2 boundary is tested only by the good arm's two single-contradiction cases. A corpus with
  exactly one injected defect was never run.
- **Contestability of the exit.** W07's deviation was argued from the brief's own one-handed,
  hurried context; the scorer judged the input did not *require* it. A second scorer could differ.
  The cap moves judgement to a narrower question, it does not remove it.
- **Mutation and detection share a model family.** A defect written by one may be one the other is
  disposed to find or to miss, in an unknown direction.
- **`docs/self-review.md` returns "revise" on everything** — 9 of 9 across both arms. It was measured
  here only as a by-product and it discriminates nothing. That is now an open item, and P1-10 in §3
  proposed cutting it down long before this run gave a reason.

---

## 25. The self-review gate — the prompts work, the exit condition is unreachable, and two fixes were reverted

§24 measured `docs/self-review.md` returning "revise" on 9 of 9 artifacts, good and defect-injected
alike, and left it as the top open item. This section is that item. **Nothing ships to instruction
text; two changes were written, measured, and reverted.**

### Phase 1 — the pass is not weak

Scored against the same injected-defect keys as §24, generously, on the self-review output already
on disk:

| | detection of injected defects |
|---|---|
| the Mode D review (§24) | 34/36 = 94.4% |
| **the self-review pass, author's seat** | **30/36 = 83.3%** |

Per class the two differ where it is interesting: the review caught scale incoherence 6/6 and a
deliberately-argued accessibility hole 6/6, the author's own pass **3/6 and 4/6**. An author holds
the reasoning that produced the value and defends it; a stranger reads the value.

### The diagnosis is one sentence in the file

> Only return the response after every applicable prompt has a confident "yes."

Across ~118 prompt lines and roughly forty applicable questions — several of them unanswerable as
"yes" by construction ("Are there any sentences that could be deleted?", "Is the response too
long?") — **the exit condition is unreachable**. A gate that never opens is not a strict gate but no
gate: the only ways past are an infinite loop and a silent override, and the second is what happens.
It also teaches that a mandatory step can be stepped over.

### Phase 2 — the change, and a deliberate divergence from P1-10

§3's P1-10 proposed **cutting** the universal prompts to about eight. Phase 1 says the opposite: the
prompts produce 9-13 substantive edits per draft and catch 83% of planted defects. Cutting them
removes the working half to fix the broken one. So the change split the tiers instead — five
objectively checkable, *reachable* blocking questions answered in writing (contradicted value,
invented given, missing required state, accessibility hard rule, contract and header honesty), and
every other prompt demoted to an improvement pass that never blocks.

### Phase 3 — it fails its own pre-registered rule

| | result | threshold |
|---|---|---|
| S2 blocks the defect-injected arm | **6/6** | >= 5/6, **pass** |
| S4 keeps the improvement pass alive | median **11** changes on the good arm | >= 6, **pass** |
| S3 leaves good drafts returnable | **6/6 blocked** | <= 1/6 (+ the pre-registered W05/W07 exception), **fail** |

Blocked/not-blocked separates the arms by nothing at all. The rule written before the run says
revert, and it was reverted.

### What the six good-arm blocks actually were

Adjudicated by hand rather than counted:

| artifact | gate's reason | verdict |
|---|---|---|
| W05 | Label 13 pt over Numeric 12 pt = 1.083x against the 1.125x bar | **real** |
| W07 | action bar at safe area + 8 against the 44 pt home-indicator anchor | **real** |
| W09 | 19 sp / 24 line-height = 1.263 against a 1.25 headings ceiling | marginal, 0.013 over |
| W11 | a named `emphasized decelerate` curve described as a cross-fade | internal inconsistency, not a bar |
| W01 | `accessibility_hard_rule` fired with an empty evidence field | unsubstantiated |
| W03 | rows contiguous with no 8 pt gap | **false positive** |

W03 is the instructive one. The draft says: *"Rows are contiguous with no 8 pt gap, which is
acceptable here because adjacent rows carry the same consequence and a mis-tap is undone by one more
tap — the gap rule exists to separate targets with different outcomes."* That is an argument about
the bar's **scope**, not a request for an exemption, and the gate could not tell the difference —
because the contradicted-value cap shipped in v1.28.0 says a stated reason never lifts it.

So the base rate of contradictions in real skill output is **2 of 6 verified**, not the 5 of 6 the
gate reported.

### The second revert, and rule 20

The scope conflation is real, so the cap was narrowed to admit a second exit: a bar whose scope does
not reach the case. Measured on the same twelve artifacts, twice:

| | good | mutated | separation |
|---|---|---|---|
| v1.28.0 cap | 4 4 3 3 4 4 | 2 2 2 2 2 2 | 2 |
| with the scope clause, draw 1 | 4 4 **4** 3 4 4 | 2 2 2 **3** 2 2 | 2 |
| with the scope clause, draw 2 | **3** 4 **4** 3 4 4 | 2 2 2 2 2 2 | 2 |

Separation holds, and the clause still loses: **W05 — a hand-verified contradiction — clears in both
draws** where the unmodified cap caught it. W08's 2 → 3 in draw 1 did not reproduce, so that one was
noise. Reverted.

**Rule 20: a defect observed in one instrument does not license a fix in another.** The scope
conflation was observed in the self-review gate. The rubric scorer never had it — it did not cap W03
in any run — and patching the text they share cost a true positive in the instrument that was
working. Fix the instrument that has the defect.

### A number the repository did not have

Two draws of the same scorer over the same twelve artifacts and the identical rubric text:
**10/12 = 83.3% agreement**, two cells flipping by one band. That is a scorer test-retest ceiling,
sitting almost exactly on the applier's 85.2%.

It carries a correction back to §24. The headline there — 0 bands to 2 — is far outside a one-cell
flip and stands. The subsidiary claim, that the cap catches a contradiction in two of six real
outputs, rests on **one draw per cell**: the *defects* in W05 and W07 are hand-verified and real, but
whether the scorer catches them on any given run is subject to a one-in-six flip. Both facts are
true and they are not the same fact.

### What is still open

- The self-review gate's exit condition is still unreachable in the shipped file. The diagnosis is
  measured; no fix has passed its own test.
- The narrower gate suggested by the phase-3 data — dropping `contradicted value` from the blocking
  tier, where it fired 5/6 on good drafts, and keeping the four that fired 1/6 — is **post-hoc**,
  computed from the run it would be justified by, and untested. It needs a fresh corpus.
- Every instrument in this repository that has been checked for test-retest now sits near 84%.
  Nothing resting on a single cell of any of them is a result.

---

## 26. The self-review gate, on a fresh corpus — block on what is never right, score down what is usually wrong

§25 left the shipped `docs/self-review.md` with an unreachable exit condition and a post-hoc
hypothesis it forbade itself to act on. This section builds the corpus that hypothesis needed.

### The principle, fixed before the data

§25's phase-3 data suggested dropping `contradicted value` from the blocking tier because it fired
on 5 of 6 good drafts. Taken alone that is curve-fitting, so the change was justified by a principle
instead and the principle was written down first:

> **Block on what is never right. Score down what is usually wrong.**

An invented fact, a missing required state, a broken accessibility hard rule, a dishonest header —
none has a legitimate version. A value that contradicts a bar sometimes does: the input may require
the deviation, or the bar's scope may not reach the case. The first class belongs in a gate; the
second belongs in the contradicted-value cap, which already works (§24) and is untouched here.

### Why two cells would have proved nothing

§24's taxonomy puts exactly one accessibility defect in every mutated artifact, so a gate containing
"accessibility hard rule" blocks 6/6 of them **by construction**. Three cells instead:

| cell | carries | the gate should |
|---|---|---|
| A good (6) | nothing injected | pass |
| **B (6)** | five contradicted-value defects each, **no** categorical failure | **pass** |
| C (6) | an invented given, a deleted required state, an accessibility hard rule | block |

**B is the falsifier.** A gate that blocks B is the old saturated gate wearing four questions instead
of five. Six fresh briefs, none reused; each draft mutated twice by agents blind to the gate's
contents; cell purity verified against the keys before the run.

### The result — every prediction holds, both draws agreeing

Draw-to-draw agreement **17/18 = 94.4%**, well above the rubric scorer's 83.3%: categorical questions
are more stable than graded ones.

| | blocked, both draws | pre-registered |
|---|---|---|
| A good | **0/6** | <= 1 |
| **B contradicted-value only** | **0/6** | <= 2 |
| C categorical | **6/6** | >= 5 |
| improvement pass on the good arm | median **12.5** changes | >= 6 |

And the class the gate stopped blocking did not become unowned — the pre-registered condition that
would otherwise have withheld the change:

| | rubric score | capped |
|---|---|---|
| A good | 4 4 4 2 4 3, median **4** | 2/6 |
| B | 2 2 2 2 2 2, median **2** | **6/6** |

Two bands of separation from the cap, on a corpus it had never seen.

### What the numbers hide, stated rather than averaged

- **`missing_state` catches 7 of 12.** A deleted required state was injected into every cell-C
  artifact and the gate's own question found it barely more than half the time. The blocking is
  carried by `invented_given` (12/12) and `accessibility_hard_rule` (12/12). The gate works; one
  of its four questions is weak, and that is a live item rather than a rounding error.
- **One false positive in 24 cell-A and cell-B runs**, and it is the ambiguity the corpus check
  predicted: a 4 pt gap between passenger chips, read as an accessibility hard rule in one draw and
  as a spacing-bar contradiction in the other.
- **`0/6` on the good arm is not a claim that the good drafts are clean.** The scorer capped two of
  them, and one is a real touch-target miss the gate did not catch: H10 specifies a *"View switch —
  pinned, 32 pt. Segmented control"* against the 44 pt iOS minimum, and the gate answered "no" in
  both draws.

### The recurring dispute now has a name

H10 is the third appearance of one argument in three independent runs — §25's W03 (rows contiguous
with no 8 pt gap), H05 (4 pt between chips), and now a 32 pt segmented control that is simultaneously
**below the 44 pt bar and the platform's own default height for that component**. Every time, one
instrument applies the bar literally and another reads the bar's scope, and both readings are
defensible.

**This is the single most common source of disagreement between instruments in this repository**, and
it is not noise: it is a real question the corpus does not answer, namely which bars are floors under
every component and which are defaults a platform component may legitimately sit under. Until that is
written down, the two readings will keep splitting, and every future instrument will inherit the split.

### What shipped in the gate change

Four blocking questions answered in writing; `contradicted value` demoted to the improvement tier
with an explicit hand-off to the cap that scores it; every other prompt kept, because §25 measured
them producing 9-13 real edits and catching 83% of planted defects. P1-10 proposed cutting the
prompt list; the measurement says the prompts were never the problem, so the tiers changed and the
prompts did not.

The maintenance rule now states the entry condition for the gate: a prompt joins it only when a good
draft answers it cleanly, the answer is checkable against the draft rather than judged, and the
condition has no legitimate version. `Contradicted value` fails the third, which is exactly why it
blocked 5 of 6 good drafts in §25.

---

## 27. Floors, defaults, and what a bar governs — the repository's most common disagreement, closed

Three runs produced the same argument: §25's W03 (contiguous list rows against the 8 pt gap bar),
§26's H05 (4 pt between chips), §26's H10 (a 32 pt segmented control against the 44 pt minimum). One
instrument applied a bar literally, another read its scope, both defensible.

### The audit split the item in two, and corrected §26

`docs/quality-bars.md` already carried the answer to the segmented-control case, forty lines below
the number: *"Visual size may be smaller than the tap area as long as the hit region meets the
minimum."*

But the probe corpus shows §26's reading of H10 was too confident in the other direction. A probe
stating *"drawn 32 pt, hit region 44 pt"* is judged within scope by the unmodified file — the
qualifier is found when there is something to find. H10 said *"View switch — pinned, 32 pt"* and
stopped. **With no hit region stated, the scorer that flagged it was judging what was written, and
the gate that passed it was supplying a fact the draft never gave.** Neither was wrong; the draft
was underspecified. §26 called the cap wrong and the gate right, and that is corrected here.

The other two are a different failure: the bar reads *"minimum gap between independent tap
targets"*, list rows and filter chips genuinely are independent targets, and both HIG and Material 3
ship contiguous rows and edge-to-edge tab bars. **The bar overreached its own intent.**

### The measurement

Twelve short probes, each one spec fragment carrying one touch-or-gap decision, six legitimately
within scope and six genuine violations, ground truth fixed in advance and argued from platform
practice rather than preference. One judge per probe, reading `docs/quality-bars.md` and nothing else.

| | false positives on the 6 correct decisions | detection on the 6 violations | accuracy |
|---|---|---|---|
| bars as they stood | **3/6** | 6/6 | 9/12 |
| bars scoped and annotated | **0/6** | 6/6 | **12/12** |

Every false positive in the baseline was the same one: the gap bar applied to a repeating structure
— 60 pt contiguous list rows, a contiguous 44 pt calendar grid, a five-destination tab bar running
edge to edge. Exactly the live dispute, reproduced on demand.

### What changed in the file

- **The gap bar now states what it is for**: a mis-tap that costs the user something different from
  what they intended. Two questions decide it — do the neighbours carry different consequences, and
  is either at or under the size floor. A repeating structure whose cells each clear the floor needs
  no inter-cell gap, because that is how both platforms ship list rows, calendar cells, segments and
  tab bars.
- **The hit-region qualifier moved to the table**, and gained the clause H10 needed: when the drawn
  size is below the minimum, **state the hit region**. A spec that says "segmented control, 32 pt"
  and stops has not made the hit region reviewable and will be read as a violation, correctly.
- **Floor or default is marked** on every touch and contrast row where the distinction has been
  disputed, with the cost of each misreading stated: a default read as a floor flags correct work,
  a floor read as a default ships a defect.
- Destructive-adjacent-to-primary is explicitly not waived by the new scope.

### Rule 22

**When two instruments keep disagreeing about the same rule, the rule is the defect — but audit
before rewriting it, because half of these disputes are a qualifier nobody could find.** One of the
three instances was a clause already in the file, in its own subsection, referenced by nothing. The
other two were a bar written more broadly than its purpose. A dispute rate is a symptom; it does not
say which.

### What has no guard

No shape check reaches this class. A bar's scope is semantic, and a validator asserting the word
"floor" appears in a table would pass the next over-broad bar as easily as this one. The regression
protection here is the recorded measurement and the twelve probes, and the probes are not committed
because nothing in the repository reads them — the same rule §24 set for its own corpus. That is a
real gap, and naming it is the honest alternative to a guard that would only look like one.

---

## 28. Three cheap closures, one of them negative

Closing what could be closed without a new corpus. Three items, one shipped guard, one corrected
calibration corpus, one measured revert.

### The README guard — a class nobody was watching

v1.30.1 repaired three files shipped in 1.26.0-1.27.0 that no validator noticed were missing from
the README: `docs/motion-system.md`, the tablet golden, the stretched-phone fixture. Each was
registered in its own index and in `validate_repo.py`, and all 32 validators passed, because none of
them reads the README's enumerations.

`validate_readme_enumerates_shipped_files()` closes it — every `docs/*.md`, golden, fixture and
domain pack must be named in `README.md`. Verified by four injections, including a replay of the
exact miss. Unlike §27's bar-scope gap this one **is** mechanical, which is why it exists and that
one does not.

### The goldens against their own labels

Old backlog item: *"the golden examples read lower than their label — five of seven land at median
3."* Measured properly for the first time, each golden output block scored blind against the current
rubric with its stated label withheld from the scorer:

| | |
|---|---|
| label matches the derivation | **6 of 8** |
| label above the derivation | **2 of 8** |
| label below the derivation | 0 of 8 |

The historical claim was too pessimistic. But **both over-claims are the two blocks that claim 5/5**,
and both were confirmed by a second independent draw agreeing exactly:

- `enterprise-saas` claims 5/5, derives **3/5** twice. Production readiness sits at band 2: the spec
  offers *"bottom sheet or detail screen"* instead of choosing, and a live-data queue defines
  neither loading nor error.
- `health` claims 5/5, derives **2/5** twice. Context and brand fit is at 4 and the value/unit/range
  triad is a real owned asset — and Typography craft is at band 1 with no type role named at all,
  Interaction polish at 1, and a network-fetched clinical value carries no fetch states.

Both labels are corrected to the derived number with the blocker named, and both carry a note that
the number is derived and was scored twice. Rule 1 is the reason this matters: a filled-in example
outweighs a prose instruction, and two exemplars claiming the top band without the bands to support
it teach exactly that.

Worth recording: the one golden written this session with a deliberately honest label —
`tablet-list-detail`, claiming 4/5 — derives 4/5 and is the only one of the eight with no cap.

### `missing_state`, rewritten and reverted

§26 measured the gate's weakest question at 7 of 12. It was rewritten from "is any required state
absent" into a roll-call — enumerate the required states, point at the section defining each, and
anything you cannot point at is missing. At equal n it scored **4 of 12**. Worse, and reverted.

The likely mechanism, and the reason a third rewording is not the next move: a roll-call gets a
formal answer. The author points at the section where a state is *mentioned* without checking that
it is *defined*, and procedure does not substitute for the thing that makes this class hard — **a
deleted state is the only one of the four gate conditions that leaves no trace on the page.** The
same class scored 6/6 for an outside reviewer in §24.

The gate is unharmed: cell C still blocks 6/6 in both new draws, carried by `invented_given` and
`accessibility_hard_rule` at 6/6 each. The honest conclusion is that state coverage is not well
checked from the author's seat and wants a different instrument — Mode D, or a template-level
machine check — rather than a better question.

### Rule 23

**Two failed attempts at the same instrument question are evidence about the question's class, not
an invitation to a third wording.** Both rewrites of `missing_state` were reasonable and one made it
worse. What separates it from the three questions that work is not phrasing: those three are
answered by reading what the draft says, and this one is answered by noticing what it does not say.

---

## 29. State coverage as a machine check — measured against two pre-registered rules, and neither is met

Backlog item 2, opened by §28's honest conclusion: *"state coverage is not well checked from the
author's seat and wants a different instrument — Mode D, or a template-level machine check — rather
than a better question."* Two wordings of the gate's `missing_state` measured 7/12 and 4/12; an
outside reviewer scores 6/6; a machine check had never been tried.

**The hypothesis.** A deleted state leaves no trace *for a reader of the state section*, but it
leaves one *for a cross-reference*: the artifact names the async, live or listed surface elsewhere in
its own body, and that named surface has no matching definition. A machine holds both halves at once
and never remembers having decided.

### The audit came first, and it moved the release before a line of instruction text was written

Two passes over the same 14 committed artifacts, one blind rater each.

| | flagged |
|---|---|
| probe written from the **name** of the concept ("which states would a competent reader expect?") | **14 of 14** |
| probe written with the **bar text** in hand, both-directions strictness stated | 6 of 14, 4 not applicable |

The first pass is rule 12 reproducing on demand, and it is the most useful thing the audit produced.
It demanded `stale` on a portfolio summary, `loading` on a "Partial-day option if supported" and
`permission-denied` on an email field. **A maximalist state standard fires on 100% of real output,
including the repository's own exemplars** — so a check built on "every stateful surface must carry
every state it could plausibly need" would be worthless before it was written.

Hand-adjudicated against written authority only, **5 defects are real**, and `premium-ui`'s sixth was
rejected because the rater inferred remoteness the artifact never states:

- `health` — no loading, no error, on a value the artifact's own calibration calls network-fetched.
- `enterprise-saas` — no loading, no error, on a queue it calls live.
- `fintech` — no loading on a risk summary computed from connected holdings.
- `onboarding` — no network-failure recovery; three of the four required paths present.
- `checkout` — `## State definitions` defines Loading and Error and omits Empty.

**Every one is in `examples/golden/`. Not one is in the six example responses `check_response()`
reads.** The surface the check was designed for is clean; the surface carrying every observed true
positive is validated by `validate_golden_examples()`, which checks that three headings exist and
reads no content. A check wired only into the first seam would have shipped green, with zero observed
true positives, claiming a class was closed. Rule 17 as a procedure — gate, then write — is what
caught it.

### Two requirements were considered and refused

`permission-denied`: no bar in the repository states it. `Offline`: its own bar says *"when
applicable"*, a judgement no static check can make, and its trigger words live in QA checklists,
where the first build false-positived. **A machine check may enforce only a bar that exists and
reaches the case** — the audit's own failure mode, avoided by construction rather than after three
disputes.

### The first build was broken in both directions, and how it broke is the finding

Against the committed corpus: it flagged **4 of 6 clean example responses** and caught **0 of 5**
verified golden defects.

`health` and `enterprise-saas` both state, inside their own `Design quality calibration`, that they
carry no loading or error state. The scan matched the word "loading", found the word "state" in its
behaviour list, and counted the admission as a definition. **An instrument that reads an artifact's
self-assessment as artifact content passes exactly the artifacts that are honest about being
broken.** Fixed structurally: self-assessment sections are stripped before the scan, and a negation
standing immediately before a state word disqualifies the sentence.

Rebuilt: 0 of 6 clean examples flagged, 3 of 5 golden defects caught. It cannot reach `health` or
`fintech`, and that bounds the instrument class rather than this implementation: **recall is bounded
by whether the artifact says the thing about itself.** A cross-reference is blind to a document that
never states its own data source, and no vocabulary fixes that.

### The corpus, and the measurement

Clean arm: six real skill outputs, Modes A, B and C, generated by agents executing `SKILL.md` against
briefs taken from `examples/evals/generation-prompts.json` — written long before this item, so probe
difficulty was not chosen by the person writing the detector. Held out until the single measurement.
Mutated arm: single-state deletions by agents who ran before the detector existed, told to leave the
document reading as though coverage were complete.

**Draw 1**, twelve deletions, against the pre-registered indicators:

| indicator | prediction | result |
|---|---|---|
| false positives, held-out clean arm | ≤ 1/6 | **0/6 — confirmed** |
| detection | ≥ 8/12 | **3/12 — refuted** |
| balanced-12 accuracy | ≥ 9/12 | **7/12 — refuted**, tying the better author-seat wording exactly |
| the cross-reference tier out-contributes the section tier | — | **refuted**: it contributed nothing |

Hand adjudication changes what those numbers mean. **Eight of the twelve mutants are real bar
violations**; four are not, all of them the shape predicted in writing before the data — a state
stripped from one named surface while the artifact still defines it elsewhere. `marketplace` removed
"Loading, next page" and kept "Loading, first page". The detector passed all four, correctly. Of the
eight violations, **four are `Offline`**, and the detector caught **4 of the 4 in-scope violations**
with **0 false alarms across 16 clean opportunities**.

**Five of six deletions went to `Offline` by themselves**, and that is not luck. The instruction
demanded a deletion that leaves no seam; the state whose removal leaves no seam is the peripheral
one; the peripheral state is the conditional one — which is exactly what the check declines to
enforce. Two selection pressures met on the same state from opposite directions.

**Draw 2** was stratified to fix the first draw's specification bug (cell B asked for a *surface*
deletion while the bar is written at *artifact* level) with the decision rule fixed beforehand: ship
iff in-scope detection ≥ 5/6.

| | |
|---|---|
| stratum S — an in-scope state removed from the whole document | **4/6** |
| stratum O — `Offline` removed, documented out of scope | 1/6, and that one a collateral catch |
| false alarms | 0 |

### Both misses are one defect, and it is a measured trade rather than a bug

`budgeting-home` kept "Linear **progress indicator** on category rows" — a budget bar, matched by the
`Loading` vocabulary. `marketplace` kept "this surface's most common **failure** is over-filtering" —
a design failure mode, matched by the `Error` vocabulary. In both, the section-level check correctly
found nothing and the **whole-document fallback rescued the artifact on a word used in another
sense**.

That fallback is the component that buys the zero false-positive rate: without it, a state defined
outside its canonical section is flagged. **It buys 0/16 false alarms and costs 2 of 6 detections.**
That trade is now measured instead of assumed.

### The decision: nothing behavioural ships

| rule | written | result |
|---|---|---|
| detection ≥ 8/12, raw | before anything ran | 3/12, then 5/12 — **fails** |
| in-scope detection ≥ 5/6 | before draw 2 ran | **4/6 — fails** |
| in-scope detection pooled across draws | *never registered* | 8/10 — would pass |

**Two pre-registered rules fail and only a post-hoc framing passes**, which is precisely the
situation pre-registration exists for. The detector, the seam into `check_response()` and the golden
declaration guard were all written, wired, injection-verified on four separate breakages, and
reverted. The instrument is 8/10 on in-scope artifact-level deletions with 0/16 false alarms, and
that is not the number either rule asked for.

**What a third cycle would need, and why it was not available.** The diagnosis is specific and the
fix is a vocabulary scoping change, not a redesign — but tuning voids the draw, and a fresh draw
needs a fresh clean arm. `examples/evals/generation-prompts.json` has no unused Mode A, B or C brief
left, and writing new briefs would put probe difficulty back in the hands of the person writing the
detector. Re-using the clean arm after a narrowing fix is the one thing that cannot be done, because
narrowing makes the check fire *more* and the false-positive rate would need re-measuring on a
surface already spent. The honest cost of a real answer here is a new brief set built by someone who
has not seen the detector.

### What did ship, on its own evidence

Two hand-verified corrections to the calibration corpus, independent of the instrument:

- **`examples/golden/checkout.md`** defines an Empty state — every item unavailable, address and slot
  kept, Place order disabled with the reason attached. A UI-spec exemplar with a `## State
  definitions` section that omits a required state teaches the omission.
- **`examples/golden/onboarding.md`** names why its Production readiness sits at band 2: no recovery
  for a failed network call at the account or sync step, and no loading treatment for the first
  write. The band was already 2; the derivation did not say why.

### The guard shape that was found and not shipped, recorded because it is right

Running the detector over the goldens as a **blocking** check is wrong, and `enterprise-saas` says
why in its own calibration: *"a queue whose whole point is live data defines neither a loading nor an
error state"* is the stated reason it derives 3/5. The goldens are a calibration corpus spanning
bands 2 to 4 on purpose, and §28 corrected two labels specifically so it tells the truth about that.
A blocking state check would force every golden to Production readiness ≥ 3 and delete the low band.

The shape that fits is a **declaration** check: a golden may carry a deliberate gap; it may not carry
one silently. Built, and it failed on exactly the two undeclared gaps and passed `enterprise-saas`,
which declares. It is not shipped because it cannot run without the detector, and the detector did
not clear its rule. It is the first thing to build back if a third cycle lands.

### Rule 24

**The deletion that is easiest to hide is the deletion of a conditionally-required state, and a
conditional requirement is exactly what a static check cannot enforce.** Five of six blind mutators
reached for `Offline` unprompted, because "leave no seam" selects for the peripheral condition, and
"must be mechanically checkable" rejects it — the same state, chosen by two pressures pointing
opposite ways. The corollary is the harder half: **a check holding one artifact and no baseline
cannot tell "this never needed an offline state" from "this used to have one".** Absence of a
conditional requirement is unobservable without a diff, and no wording of the check changes that.

### Rule 25

**The same text is evidence against a definition and evidence for a declaration; which question you
are asking decides whether to strip it or read it.** An artifact's self-assessment must be stripped
before asking whether a state is *defined* — read it and the instrument passes every artifact honest
enough to confess. It must be read when asking whether a gap is *declared*. Getting that backwards
is what made the first build pass the two artifacts whose own calibration named the defect.

---

## 30. The third draw, on a corpus the repository supplied — and backlog item 2 closes negative

§29 ended by naming a blocker: a fresh brief set built by someone who has not seen the detector.
**That was wrong about the repository.** Six of the eight goldens carry a `## Prompt` block — full
briefs with platform, user goal, audience and constraints, written for the calibration corpus long
before this item. Their *outputs* were the audit corpus; the briefs had never been run as generation
prompts. Difficulty was chosen by whoever wrote the goldens, and rule 6 is satisfied without anyone
writing a line.

Six fresh artifacts were generated from them — 2 × Mode A, 1 × Mode B, 3 × Mode C, 2414 to 4559 words
— with `examples/golden/` and `docs/golden-examples.md` forbidden, **verified by grepping the six
transcripts** rather than by the agents' own say-so: no agent made a single tool call touching either.
One brief is hostile to the detector by construction: `tablet-list-detail` states *"sync is frequent
and sometimes offline"*.

### The two fixes were principles, not patches

1. **A section that argues for the design does not specify it.** `Rationale for major choices`,
   `Alternatives considered`, `Key decision tradeoffs`, `Simplification opportunities`,
   `Production checks` and `Next actions` joined the stripped set. Both draw-2 `marketplace` misses
   lived there.
2. **A state synonym must name the condition, or a device that exists only to express it.**
   `skeleton`, `spinner` and `shimmer` exist only to express waiting; a progress indicator shows the
   progress of anything, including a budget. `progress indicator` left the `Loading` set.

Both draw-2 misses were then caught, the committed corpus stayed silent, and the spent clean arm
stayed at 0/6 as a one-sided check.

### Draw 3, stratified with the deleted state assigned by rotation

| | gate | result |
|---|---|---|
| false positives, fresh clean arm | 0/6 | **1/6 — fails** |
| stratum S, an in-scope state deleted from the whole document | ≥ 5/6 | **4/6 — fails** |
| stratum O, `Offline`, out of scope by decision | reported | 1/6 |

**Three failures, three different blind spots, none of them the one that was repaired:**

- **Format.** `g-checkout` *does* define Empty — in a markdown table row: `| Empty | Cart emptied
  elsewhere, or every item became unavailable | Full-screen empty state: what happened, what it means,
  one action |`. The bullet parser reads `- Label:` entries and sees nothing. **A false positive on
  correct work**, and the structural fallback that was supposed to be the safe leg is the one that
  failed.
- **Polysemy, a new word.** `g-enterprise-saas` had its Default state deleted and passed, because
  *"Context defaults applied"* and *"the enterprise default of multi-select"* satisfy `\bdefault\b`.
- **Polysemy, marginal.** `g-checkout`'s Loading deletion was masked by a submit `spinner` surviving
  in the Submitting row.

### Why a fourth vocabulary repair is not the next move

Rule 23 says two failed attempts at the same instrument question are evidence about the question's
class. This is the third, and the sequence is unambiguous — every repair closed one word sense and
opened another:

| draw | the sense that decided the number |
|---|---|
| 1 | `state` in "defines neither a loading nor an error **state**" — the artifact's own confession |
| 2 | `progress indicator` on a budget row; `failure` as a design failure mode; `error prevention` as a Nielsen citation |
| 3 | `default` as a configuration default; `spinner` as a submit affordance; and a definition living in a table |

And the one structural leg that does not depend on vocabulary — read the canonical slot — is defeated
by format: **2 of 5 fresh Mode C outputs render `## State definitions` as a markdown table with zero
top-level bullets**, while `skill/templates.md` prescribes a bullet list. A slot check flags them, and
they are right: a table is the better shape for a nine-state matrix. Changing the template to make a
validator's parsing easier is the tail wagging the dog, and it is rejected here explicitly rather than
left as an option.

### Backlog item 2 closes, negative and on the record

State coverage is **not checkable from the author's seat** — 7/12 and 4/12 across two wordings
(§28) — and it is **not checkable by a keyword machine** — three draws, both gates missed each time,
with a distinct failure class deciding each one. Presence of a *slot* is mechanical. Whether a passage
*defines* a condition is semantic: it requires deciding whether a word names the artifact's own state
or something else, and whether a block is specification or commentary. No vocabulary decides that.

**The instrument that owns this class is the outside reviewer**, measured at 6 of 6 on planted state
deletions in §24, and the seam for it already exists and has never been used:
`run_generation_eval.py --generate-command` has still never run with a real model behind it. That is
the next move for anyone who picks this up — a judged check, not a scanned one — and its cost is a
model in the loop.

### Rule 26

**A machine check can verify that a state has a slot. It cannot verify that a state is defined.**
Three consecutive principled repairs each closed one word sense and exposed another — a widget name, a
design-failure noun, a heuristic citation, a configuration default, a submit affordance — and the one
format-independent leg was beaten by a markdown table. When an instrument's failures keep arriving
from a different direction each time, the question is not under-specified, it is out of class.

---

## 31. Backlog item 3 — the two colour instruments never disagreed, except in one place, and that place is rule 8

The backlog line: *"§23 measures colour at 93.8%; §§16–19 measured `Color, state and contrast` at a
live floor of 2/6. Both cannot be a full description."* The audit ran before the corpus, as §27
established, and it changed what needed measuring.

### The paper audit — the headline conflict is a band mismatch

| §23 gate indicator | baseline | the rubric cell it actually asks | band |
|---|---|---|---|
| `C-role` — roles | 6.0/6 | "Is each semantic role decided … rather than a palette listed?" | **2 → 3** |
| `C-pair` — pairs with their ratio | 6.0/6 | "Are the foreground/background pairs stated, and what they become in dark…" | **3 → 4** |
| `C-dark` — the dark transform | 5.0/6 | the same cell, its second half | **3 → 4** |
| `C-rule` — a rule for an unlisted role | 5.0/6 | "Does a stated rule **return** the dark and increased-contrast **values** for a role the artifact does not list?" | **4 → 5** |

Three of the four scored indicators sit at `2 → 3` and `3 → 4`. Only `C-rule` reaches `4 → 5`.
**"Colour is at 93.8%" is a statement about band-3 and band-4 material; "colour closes 2/6" is a
statement about the band-5 closure. Both are true, of different bands of one dimension.** They were
never rival descriptions, and the premise is refuted without a corpus.

### The chronology makes the surviving dispute worse than a coincidence

One dispute survives the mapping: `C-rule` **5/6 = 83%** against the rubric's `4 → 5` **2/6 = 33%**.
`C-rule` asks whether a rule is **present**; the cell asks what a stated rule **returns**. That is
rule 8.

And the cell did not always ask it. **§16 rewrote it for exactly this reason** — the old wording
never asked for an output, the closure test structurally could not run on it, and three readers
unanimously called a complete OKLCh transform underdetermined. §16 precedes §23 by seven sections in
this document. **The indicator built in §23 was written in the shape §16 had already diagnosed and
repaired, in the same file.**

### One corpus, both instruments, mutually blind

The six `clean2` artifacts — fresh output from the six golden `## Prompt` blocks at the current tree,
2 × Mode A, 1 × Mode B, 3 × Mode C. Spent for state-coverage false positives; their colour content had
never been read by anyone. Two arms of six agents, neither told the other existed.

| | presence arm | rubric arm | |
|---|---|---|---|
| `C-role` | **5/6** | `2 → 3` **5/6** | cell-for-cell agreement **6/6** |
| `C-pair` ∧ `C-dark` | **0/6** | `3 → 4` **1/6** | cell-for-cell agreement **5/6** |
| **`C-rule`** | **6/6** | **`4 → 5`** | **0/6** |

**The effect is total and the control holds.** The band-matched pairs agree 6/6 and 5/6 cell for
cell; the presence-versus-returns pair separates 6/6 against 0/6, every artifact, no exceptions.
Without the control this would be two cohorts disagreeing. With it, the disagreement is isolated to
the one pair where the two questions are not the same question.

The rubric cell is a conjunction of exactly `C-pair` and `C-dark`, so the conjunction is its
operationalization; `C-pair` alone stands 3/6, two above the cell, which is what half of a
conjunction does.

### What the artifacts actually write, which neither instrument had stated

Every one of the six states a rule covering an unlisted colour role. Not one returns a value:

- *"A new state role must declare its three appearance values and its glyph before use."*
- *"A new status role must be introduced as a (container, on-container) pair measured ≥4.5:1 for text
  and ≥3:1 for its mark in light **and** dark, and must carry a text token."*
- *"Any element whose meaning is a cost, an availability, or a failure is semantic and outside brand
  control."*

**The skill writes admission criteria, not transforms.** Each says what a new role must satisfy, or
where its authority comes from — none says what values it gets. A presence indicator cannot tell the
two apart; the closure test cannot fail to.

### The corpus-selection qualifier the backlog line never carried

`C-dark` was **5.0/6** in §23 and is **0/6** here. §23's six briefs were *craft-forcing*, chosen to
force craft statements; these six are ordinary product briefs. Absolute rates do not transfer between
sections (the standing instrument-ceiling note), so this is not a regression claim — but it does
qualify the 93.8% in a way nothing in the record did.

**And it corrects a standing "do not re-assert".** That list carried *"the skill needs a colour system
document — 93.8% before one existed"*. §23 withdrew `docs/color-system.md` on `C-dark` at 5/6. That
number is a band-3-to-4 presence rate on briefs selected to force craft. On ordinary briefs the dark
transform is stated **zero times in six** and the `3 → 4` cell closes once. The withdrawal is not
hereby reversed — one corpus does not reverse it — but **the evidence it rested on does not reach the
case, and the question goes back to the backlog as open rather than settled.**

### Rule 27

**A repair to one instrument does not propagate to the next instrument built beside it — check the
neighbours when a cell is rewritten.** §16 fixed a cell because presence-shaped wording cannot be
closure-tested, and seven sections later the same repository built a presence-shaped indicator for
the same question and read 83% where the repaired cell reads 0%. The two lived in one file, one
series, one author's hands. Nothing flagged it, because nothing in this repository maps its
instruments onto each other — which is what the audit half of this section had to do by hand.

---

## 32. Backlog items 7 and 8 — the pooled floor reproduces, the per-dimension floor table does not, and the hypothesis that would have explained it is dead

Items 7 and 8 name four floors from §19 — `Production readiness` 1/6, `Context and brand fit` 1/6,
`Composition and spacing` 1/6, `Color, state, and contrast` 2/6 — and treat them as four
dimension-specific problems to fix.

§31 suggested they might be one problem. The rubric's `4 → 5` column is one question asked nine
times — *does a stated rule produce an output for a case the artifact does not list* — and the two
floor descriptions §19 recorded in the appliers' own words have the shape §31 found in colour: a
closed-world checklist (*"the checks cover only what is listed"*) and a ranking with no output
(*"the precedence only ranks categories; no stated treatment"*). **H: the floors are one failure
shape, not nine.**

### Design of the one-shape test

Nine agents, **one per dimension**, each closure-testing all six `clean2` artifacts on that
dimension's `4 → 5` cell and classifying every non-closure against a taxonomy fixed before the run.
One rater per dimension rather than one per artifact, deliberately: a single rater answering all nine
questions about one document would produce the cross-dimension agreement H predicts, as a habit.

### H is dead, on the pre-registered rule, in both readings of the corpus

| | gate | result |
|---|---|---|
| P1a — `rule_is_a_criterion` + `rule_is_closed_world` share of non-closures | ≥ 70% | **59.4%** |
| P1b — dimensions in which those classes appear | ≥ 7/9 | **6/9** |
| P2 — colour reproduces §31 | 0 or 1 of 6 | **0/6** ✓ |
| P3 — `Typography craft`, the one cell that accepts an admission criterion, above the other eight | ≥ +2 cells | **+0.62** |

**P2 held exactly.** A rater who had never seen §31, told nothing about it, returned 0/6 on the same
cell §31 measured at 0/6. The instrument is sound, which is what makes the rest of the run readable.

**P1 and P3 failed, so H does not survive**, and the decision rule fires: items 7 and 8 do not merge.
`no_rule_at_all` at 31% is a real competing class, not a residue.

### A scoping error in this run, found by hand and reported both ways

`docs/design-quality-rubric.md:32` says **"Mode B user flows normally do not need a visual quality
score"**. The corpus contains one flow, and its rater quoted the artifact's own line — *"This is a
flow, not a visual spec — per-screen visual calibration is out of scope and deliberately omitted"* —
and then scored nine non-closures anyway, because the schema offered no `n/v`. That is my design
error, not the rater's.

| | pooled closure | P1a | P1b |
|---|---|---|---|
| primary, as pre-registered | 22/54 = **40.7%** | 59.4% | 6/9 |
| secondary, Mode B excluded per the rubric's own line | 22/45 = **48.9%** | 73.9% | **6/9** |

The secondary analysis lifts P1a over its gate and leaves P1b under it. **H fails the pre-registered
conjunction either way**, so the conclusion is robust to the error, and the primary numbers stand as
the ones registered.

### What the run actually found, which is larger than the hypothesis it killed

**The pooled level reproduces and the per-dimension table does not.**

| dimension | §19 | this run (Mode B excluded) |
|---|---|---|
| Distinctiveness and owned assets | 5/5 | 5/5 |
| Attention path and hierarchy | 3/6 | 3/5 |
| Production readiness | 1/6 | 2/5 |
| Context and brand fit | 1/6 | 2/5 |
| Density and rhythm | 3/6 | 2/5 |
| Typography craft | 5/6 | 3/5 |
| Color, state, and contrast | 2/6 | 0/5 |
| **Interaction polish and motion** | **4/6** | **0/5** |
| **Composition and spacing** | **1/6** | **5/5** |
| **pooled** | **25/53 = 47.2%** | **22/45 = 48.9%** |

Two corpora, two cohorts, two tree versions, and the pooled number moves **1.7 pp**. Meanwhile
`Composition and spacing` — one of the four floors items 7 and 8 exist to fix — goes from the bottom
of the table to the top, and `Interaction polish`, which was mid-table, goes to zero. Only
`Distinctiveness` and `Attention path` hold their place, and `Distinctiveness` is already flagged as
structurally suspicious.

**And mode is a large uncontrolled factor.** Mode C specs close **17/27 = 63%**; Mode A concepts close
**5/18 = 28%**. That is not a defect — it is the rubric working exactly as written, four lines below
the table: *"Band 3 is where a good concept lives; band 4 is where a spec has to get to. Do not fail a
concept for lacking a number its own output contract never asked for."* A corpus's mode mix therefore
sets its per-dimension numbers before any property of the skill does, and **§19 records "six briefs in
domains absent from the corpus" and never records what modes they were.**

### Items 7 and 8, rewritten

Their premise — that four named dimensions are the skill's weak points — **is not supported**. Two of
the four reversed on a fresh corpus, one by four cells. Targeting `Production readiness` or
`Composition and spacing` would be optimising against corpus noise plus an unrecorded mode mix.

What is left is real and smaller: **the pooled band-5 closure sits near 48% and is the most stable
number this series has produced.** If anything here is a target, it is that, read per mode — and the
question worth asking is about specs at 63%, because concepts at 28% is the rubric doing its job.

### Rule 28

**A per-dimension rate is not a property of the dimension until it reproduces on a second corpus —
and before treating any per-X rate as a property of X, check what else varied.** Pooled closure
reproduced within 1.7 pp across two corpora while individual cells moved by up to four of six, in both
directions. The ranking that two backlog items were built on was corpus composition, and the largest
component of that composition — output mode — was never recorded by the run that produced it.

---

## 33. Backlog item 1 — the gate is void, and why that is the most useful thing this run produced

Item 1: *"every instrument asks whether a rule is stated or whether a stated value contradicts an
authority. An artifact can pass both and still be a mediocre design."* Four releases in this series
have died on an unaudited premise, so the premise was made the gate: **score a quality degradation
with the existing instrument first, and if the instrument separates the arms, close the item.**

### The corpus item 1 has always needed

§24 built its twins by replacing values with wrong ones — that is correctness, and the
contradicted-value cap already scores it at two bands. A quality twin must change **no value**, delete
**no statement**, contradict **no bar**, keep its **own self-description consistent with the worse
design**, and still be worse. Six degradation classes, fixed in advance, one per artifact: priority
inversion, emphasis misallocation, grouping incoherence, pattern mismatch, signature dilution,
attention-path incoherence.

Two of the four constraints were verified **mechanically**: every `## ` heading and every
numeric-plus-unit token survives in all six twins — 21/21, 14/14, 5/5, 22/22, 24/24, 45/45. The
degradations are substantive and were hand-checked: `fintech` demotes the answer (`38%`, *"13 points
above the 25% limit you set"*) below six ladder rows and from Display to Title, where it is
typographically identical to the row values, and puts a definition of what a percentage is at the top
in the largest type on the screen.

### The result, and the branch the rule did not have

Twelve artifacts, opaque labels, one joint blind pass, rubric plus contradicted-value cap.

| | gate | result |
|---|---|---|
| P1a — median band separation between arms | 0 | **0** ✓ |
| P1b — contradicted-value cap on the degraded arm | ≤ 1/6 | **5/6** ✗ |

By the letter of the decision rule the gate fails and item 1 closes. **That conclusion does not
follow, because P1b was mis-specified**: it set an absolute threshold without a clean-arm base rate,
and **the cap fires on 3 of 6 clean artifacts**. A 5-versus-3 differential is not evidence that the
instrument reads quality. §24 recorded the same kind of gap rather than backfilling a branch that
fired, and this follows it.

### The hand adjudication, which voids the run

§25's precedent — *the gate reported 5 of 6, by hand it is 2 of 6* — applied to every cap, each
degraded artifact checked against its own clean twin:

| twin | cap | also in the clean twin? |
|---|---|---|
| `tablet-list-detail` | two-pane threshold ≥ 700 pt against the expanded ≥ 840 dp bar | **yes — same cap, both arms** |
| `premium-ui` (1) | Headline 17/20 and Body 17/24 while claiming 1.125× | **yes — same cap, both arms** |
| `fintech` | Android Label 13 sp → 18 sp off the 4 pt grid | value pre-existing; clean scorer missed it |
| `premium-ui` (2) | screen title at Footnote 13/16 against the 22 pt minimum | **no — introduced by the degradation** |
| `checkout` | 12 pt between zones against the 24 pt section bar | **no — introduced by the degradation** |
| `onboarding` | sheet entry in the 200–300 ms band against 250–350 ms | **no — introduced by the degradation** |

**Three of six degradations introduced a correctness defect. Constraint 3 was violated in half the
corpus, so the gate cannot answer its own question** — in half the pairs the instrument had exactly
the signal it is built to catch. The run is void as pre-registered, and is reported as void rather
than as either verdict.

### What voided it is the finding

The three degraders that broke a bar **never changed a number**. They changed which content a number
applies to — the screen title moved into an existing small role, existing spacing values were
reassigned to group differently, a legitimate pattern swap brought a different duration bar with it —
and that was enough.

**The space of "meaningfully worse design that is still fully correct" is much smaller than item 1
assumes,** because the bars already encode a great deal of design quality: minimum sizes encode
hierarchy, section gaps encode grouping, per-pattern duration bands encode pattern fit. An artifact
cannot be made much worse along those axes without becoming incorrect. Item 1's premise is not
refuted — but it is narrower than written, and the axes on which it can hold are the ones no bar
reaches: ordering, emphasis allocation among *conforming* values, and coherence.

The uncontaminated subset says as much as n = 3 can:

| pair | degradation | clean | degraded |
|---|---|---|---|
| `enterprise-saas` | attention-path incoherence | 4 | 4 |
| `tablet-list-detail` | signature dilution | 3 | 3 |
| `fintech` | priority inversion | 4 | 3 — scorer variance on a pre-existing value |

**Zero of three separated on substance.** This repository's own floor for a result is about eight
cells. It cannot carry the premise, and it is not claimed to.

### What item 1 needs next, concretely

The corpus is buildable, but **constraint 3 has to be enforced by a checker, not by an instruction**:
score each twin for caps *before* admitting it, reject and re-degrade until the twin is cap-clean
against its own clean baseline. Only then is the gate meaningful. And the degradation classes should
be restricted to the three axes no bar reaches, since the other three provably collide with bars.

### Rule 29

**When you build a corpus by constraint, verify every constraint mechanically before you measure — an
instruction to an agent is not a constraint.** Two of this corpus's four constraints were checked by
script and held perfectly; the two left to the prompt were "contradict no bar", which broke in half
the corpus, and it broke *without a single number being changed*. The same lesson as verifying a
contamination control by transcript rather than by self-report, one level up: it now applies to the
properties a corpus is defined by, not just to the behaviour of the agents building it.

---

## 34. Item 1's gate, run properly — the boundary questions return the identical band 12 times out of 12, against an instrument that demonstrably moves

§33 voided run 1: three of six degradations broke a bar without changing a number, so half the corpus
carried a correctness signal. Rule 29 said enforce the constraint with a checker. This is that run.

### The corpus, verified rather than asserted

- **Degradation restricted to the three axes no bar reaches** — ordering, emphasis allocation among
  conforming values, coherence. The three classes that collided with bars in run 1 are not reused.
- **Three twins rebuilt**, each told exactly how the previous attempt failed: *changing which content a
  value applies to can break a bar just as surely as changing the value.* Six independent
  cap-checkers, one per twin, reading only the artifact and `docs/quality-bars.md`: the three rebuilt
  twins return **zero contradictions**.
- **Three twins carried**, and their caps are admissible because the cited values — `13 sp`, `700`,
  `14sp / 20dp, w500` — appear **verbatim in their own clean baselines**, checked by script.
- Headings and numeric tokens preserved in every twin, checked by script: 14/14, 22/22, 5/5.

**The corpus is provably pure, and building it proved §33's other half too:** the three bar-free axes
do allow a design to be made worse while staying correct, and the other three do not.

### The result of the gate

Twelve artifacts, opaque labels, two independent passes with **identical prompts**, both arms scored
in each pass.

| | pass A | pass B | pooled, 12 pairs |
|---|---|---|---|
| **pre-cap band separation** (the nine boundary questions) | **0.0** | **0.0** | clean higher **0**, degraded higher **0**, tied **12** — p = 1.000 |
| post-cap final separation | 0.5 | 0.0 | clean higher 3, degraded higher 1, tied 8 — p = 0.312 |

**The rubric's nine boundary questions assign the identical band to a design and its deliberately
degraded twin, on every pair, in both passes. Not one of twelve paired scorings differs, in either
direction.**

### The control that makes the null readable

A null means nothing from an instrument that never moves. The same two passes measure exactly that,
on identical text:

| | reproduces across two identical passes |
|---|---|
| pre-cap dimension read | **10/12 = 83%** |
| post-cap final score | **7/12 = 58%** |

**The instrument moves.** It changes its answer on one artifact in six when nothing about the artifact
has changed — matching §25's 83.3% for the rubric scorer, now measured within one design instead of
across sections. And it moves **zero** times out of twelve between a design and a worse version of it.
That is not a rubber stamp returning the same number to everything; it is an instrument with real
jitter and no sensitivity to the thing item 1 is about.

### Item 1's premise is supported, for the first time

*An artifact can pass presence and correctness and still be a mediocre design* — and the instrument
stack cannot tell. `fintech` puts a definition of what a percentage is at the largest type on the
screen and files the user's answer below six rows at row size; `premium-ui` sets the fee components
larger than the total they sum to; `tablet-list-detail` runs its one decision-carrying treatment down
the sidebar, the chips and the toolbar until it marks nothing. Every one of them scores exactly what
its clean twin scores.

### A second finding, unlooked-for: the cap is the unstable component

The contradicted-value cap costs **25 pp of reproducibility** — 83% pre-cap against 58% post-cap — and
in this corpus it fired on **pre-existing** values inconsistently: `tablet-list-detail` drew it on both
arms in run 1, on one arm in pass A, and the same text drew it differently again in pass B. §24
shipped the cap on a measured 0 → 2 band separation and its *reliability* was never measured. It is
now, and it is the least reproducible part of the stack.

### The pre-registered rule, and the indicator that failed

P4 — scorer test–retest — was pre-registered against run 1's clean scores and returned **3/6**, voiding
the run by the letter. **It was confounded by my own change to the scorer prompt between passes**, so
it did not measure test–retest at all: the second pre-registered indicator in a row that failed to
measure what it was written for (§33's P1b was the first). It was replaced by **P6**, stated before
pass B ran and measured the only clean way — the same script, the same prompts, fresh agents — and it
returns 10/12. The failure is recorded rather than deleted, and the replacement is not backfilled into
the branch that fired.

### Rule 30

**Measure the instrument's own movement on identical text, in the same run as the effect. A null is
unreadable without it, and a null against demonstrated jitter is strong.** Twelve identical paired
readings would be worthless from an instrument that always says the same thing; from one that changes
its own answer 17% of the time on unchanged text, they are the finding. The resolution measurement is
not a limitation section — it is the control, and it belongs in the design.

### What is now unblocked

Phase 2 as §33 specified it: a forced-choice paired comparison over this corpus, with **null pairs**
so a judge that always finds a winner is visible. The corpus is built, verified, and carries a known
direction on all six pairs. That is the candidate instrument for reading design quality, and this run
is what makes its validation possible.

---

## 35. Phase 2 — a rubric-free paired comparison reads exactly what the rubric could not, 12 of 12

§34 established that the rubric's nine boundary questions return the identical band to a design and
its degraded twin, twelve paired scorings of twelve, against an instrument with a measured 17% jitter
on unchanged text. Phase 2 asks the obvious next question on the **same corpus**: is design quality
unmeasurable here, or was that a property of the instrument's shape?

### Design of the paired comparison

Nine pairs, two presentation orders each, **18 judgments, one fresh judge per judgment**. Order
counterbalancing supplies two independent judgments per pair from different agents, so inter-judge
agreement and position bias fall out of one design.

- **6 signal pairs** — clean against its verified-pure degraded twin, known direction.
- **3 null pairs** — clean against a **cosmetic rewrite of itself**: same design, same decisions, same
  values, different prose. Chosen over identical-text nulls because identical text is a trivial null;
  a rewrite tests whether the judge reads the design or reads the document. Verified mechanically —
  headings identical and in order, numeric-token multisets identical (37, 7, 84), length within +1.9%
  to +4.5%.

Judges got **no rubric and no boundary questions**, were told to judge the screen and explicitly to
ignore prose style, thoroughness and length, and had three verdicts available, with
`no-meaningful-difference` presented as an ordinary answer rather than a failure to decide (rule 21).

### The result of the paired comparison

| | gate | result |
|---|---|---|
| **P1** — signal pairs, clean named | ≥ 10/12 | **12/12**, p = 0.00024 |
| **P2** — both orders land on the same document | ≥ 5/6 | **6/6** |
| **P3** — null pairs where both orders agree on a winner | ≤ 1/3 | **0/3** — `no-meaningful-difference` on **6 of 6** judgments |

**And the verdicts are right for the right reason.** Each judge was asked to name the single
difference that decided it, and all six signal pairs came back with the **exact injected degradation
class**, unprompted:

| injected | the judge, unprompted |
|---|---|
| signature dilution | *"the signature spread until it stops signalling"* |
| priority inversion | *"what occupies the top of the screen and the Display type role"* |
| ordering inversion | *"Document 2 hands the above-the-fold position to the settled [zone]"* |
| emphasis misallocation | *"the number that decides the purchase is the biggest thing on the screen"* — in the other one |
| attention-path incoherence | *"document 1's first visible row is an owned incident with hours of slack"* |
| coherence / dilution | *"reserves its two emphasis devices for the moments that carry weight"* |

### Head to head, one corpus, two instruments

| | separation on six known-direction pairs |
|---|---|
| the rubric's nine boundary questions | **0 of 12** paired scorings, p = 1.000 |
| rubric-free forced-choice comparison | **12 of 12**, p = 0.00024 |

**Item 1 is answered.** Design quality is measurable in this corpus. What could not see it was the
shape of the instrument — thirty-six questions asking whether something is *stated* — and not the
question.

### The limitation that matters most, and its defence

**Judge, degrader and null-writer share a model family.** A judge disposed to recognise the kind of
change its sibling makes would produce exactly this result. The null pairs are the defence and the
reason they were built as cosmetic rewrites rather than identical text: **the same model family wrote
those too, and the judge declined all six of them at high confidence.** So the judge is not detecting
"an agent edited this document" — it declined the agent-edited nulls and caught the agent-edited
degradations. That does not eliminate the confound; it bounds it.

The channel limit is unchanged and Phase 2 does not escape it: the judge reads a document describing a
screen, not a screen. Only a rendered artifact would — which is P2-4, still unbuilt.

### P4 failed, and it is the third in a row

P4 predicted higher confidence on signal pairs than on nulls. Signal 2.83, null **3.00** — refuted.
The reason is that the verdict space includes a null verdict, so confidence on a null pair measures
*confidence that the two are the same*, and the judges were certain of it. P4 was written as though
confidence tracked effect size. **It was a prediction and not a gate, which is the only reason it did
not void the run** — and it is the third pre-registered indicator in three sections to fail to measure
what it was written for (§33's P1b, §34's P4, this). The pattern is now on the record: this series is
better at designing corpora than at designing its own indicators, and every indicator should be
checked against what it would return under the null before it is registered.

### Rule 31

**When an instrument returns a null, try a differently-shaped instrument on the same corpus before
concluding the property is unmeasurable.** The rubric's 0 of 12 read as "design quality is hard to
measure"; a rubric-free paired comparison on the identical twelve pairs returned 12 of 12 and named
the mechanism each time. The null was a fact about a question shape — *is it stated* — and not about
the corpus, the degradations, or the property.

### What this does not yet do

The instrument is validated and **not wired into the repository**. It has no home, no document, no
harness, and no place in any mode. Deciding that is its own change with its own pre-registration —
paired comparison needs two artifacts, and most of what this skill does produces one.

---

## 36. The instrument ships — as an eval, with its control welded on

§35 validated a rubric-free paired comparison at 12/12 and left it with no home. Placing it was the
open question, and the difficulty was real: **paired comparison needs two artifacts and most modes
produce one.**

### The audit answered it before any file was written

The instrument compares two outputs, so it is an **evaluation** instrument, not an authoring one. Its
home is the eval layer beside `run_rubric_judge.py` and `run_diversity_eval.py` — and once that is
said, what it is *for* becomes obvious and considerably more useful than a new mode would have been:

**it is the pre/post instrument this series never had.** Sections 13 through 35 could not ask whether
a change made the output better, so every one of them measured a proxy — presence of a rule (§23),
coverage of a tier (§22), correctness of a decision (§27), closure of a boundary (§32). Not because
the question was uninteresting, but because no instrument here could read it.

### What ships

- **`scripts/run_paired_eval.py`** — builds counterbalanced pairs from two arms, exports judge
  requests, ingests verdicts, reports a win rate with a binomial p, an order-invariance rate, and the
  null-pair control.
- **`docs/paired-comparison.md`**, **`scripts/paired_eval_oracle_agent.py`**,
  **`examples/evals/paired-comparison-fixtures.json`**, and wiring into `docs/evals.md`, the README
  and both validators.

### The two refusals are in the tool, not in the documentation

This is the whole design point. §35's protocol worked because it carried null pairs and
counterbalancing; a protocol is a habit, and habits are what this series has watched fail four times.
So:

- **A contrast without null pairs is not reported.** At least three, and at least one per three
  signal pairs, or `build_pairs()` refuses with the reason.
- **A contrast whose control failed is reported as unreadable and exits non-zero.** If the judge names
  an agreed winner on more than a third of null pairs, no win rate from that run means anything.

Rule 21 said *build the falsifier cell, or the corpus proves nothing.* This makes the falsifier
structural instead of remembered.

### Keeping the two proofs apart

The oracle judge is **deliberately weak**: it counts stated values and calls a tie no-difference —
precisely the presence proxy §§34–35 measured at 0 of 12 on real degradations. It proves the
`--judge-command` adapter round-trips and nothing else. The proof that the *report* discriminates is
`--self-test`, which needs no judge at all and asserts the harness tells three corpora apart: one
where an arm genuinely wins, one where the arms are indistinguishable, and one whose control failed
and must be refused. An oracle supplying both proofs would be a green oracle over the thing under
test, which this repository has shipped once already.

### The guard, and what it deliberately does not assert

`validate_paired_eval_falsifier()` exists because **the falsifier corpus can be deleted and both
refusals widened into no-ops while every other check in this repository stays green** — the self-test
would keep passing on the two remaining corpora, and the harness would keep printing win rates it has
no right to print.

It asserts four computable properties of the thing itself: the ceiling is a ratio strictly between 0
and 1, the null minimum is at least one, all three fixture corpora exist, and `broken_control`'s nulls
**still draw agreed winners across both orders**. Verified by four injections, each failing on its own
message and restoring clean.

What it does not do is assert that the word "null" appears somewhere. §27 named that class — *a
validator asserting the word "floor" appears in a table would pass the next over-broad bar as easily
as this one* — and the difference here is that these four properties are mechanical, so the guard is
real rather than decorative.

### What did not change, and why that is the honest scope

**No instruction text moves.** Not `SKILL.md`, not `skill/`, not a mode contract, not a template. The
instrument compares two artifacts; the skill produces one per run. Wiring it into an authoring mode
would mean asking the model to generate a variant of its own work to compete against, which is a
different change with a different cost and no measurement behind it. Naming that boundary is worth
more than crossing it on the strength of a good result elsewhere.

---

## 37. The instrument's first real use — P1-2's +45.8 pp of presence did not make the design better

§23 shipped P1-2 on a presence measurement and wrote down what it could not answer:

> **Presence is not quality.** A response can name `emphasized decelerate`, a 4 pt grid and a tracking
> table and still be an ugly screen. Nothing here measures that.

Two years of sections later there is an instrument for it, so the first thing it was pointed at is
that sentence. Arm A = **v1.26.0**, arm B = **v1.27.0**, checked out as git worktrees, same six briefs
from the committed prompt pack, twelve blind writers.

### The manipulation landed, harder than the original

The briefs are **ordinary product briefs**, not the craft-forcing briefs §23 selected — the live
question is whether the substrate helps on ordinary work. It still took, on P1-2's own indicators:

| | v1.26.0 | v1.27.0 |
|---|---|---|
| a **named curve** (`cubic-bezier`, spring params, an M3 easing token) | **0/6** | **4/6** |
| baseline grid | 0/6 | 4/6 |
| tracking | 0/6 | 1/6 |
| type role mapped to a platform style | 3/6 | 5/6 |
| **total** | **3/24** | **14/24** — **+45.8 pp** |

§23 measured +32.5 pp on its own tier; this is larger. The `M-curve` baseline reproduces §23's exactly:
**without the substrate the model never names a curve, in six responses out of six.** A null on quality
therefore cannot be explained by the change failing to arrive.

One thing §23 could not see: **arm B is 8.7% shorter** (19,908 words against 21,802). §23 reported flat
length on craft-forcing briefs. On ordinary briefs the substrate does not add text, it **displaces** it.

### The result of the first real contrast

Judges were told, in a line §35's protocol did not need, that *a longer document is not a better
design, and a document that names more values is not thereby describing a better screen* — because
here the arms differ precisely in how many values they name, and without that line the run would have
measured presence a third way.

| | gate | result |
|---|---|---|
| **P1 — control** | nulls ≤ 1/3 agreed winners | **0/3**, and `no-meaningful-difference` on **6/6** null judgements |
| **P2 — arm B reaches significance** | predicted **no** | **no**: 6 / 3 / 3, **p = 0.254** |
| **P3 — if anything moves, it moves toward B** | predicted B | **refuted — the nominal lead is arm A** |

| brief | both orders |
|---|---|
| `concept-medication-reminder` | **A (v1.26.0)** |
| `flow-onboarding` | **A (v1.26.0)** |
| `spec-package-tracking` | **A (v1.26.0)** |
| `concept-budgeting-home` | B (v1.27.0) |
| `concept-marketplace-listing` | tie |
| `spec-ipad-clinician` | split (B / tie) |

**The +45.8 pp presence gain did not produce a better design**, and the nominal direction runs against
the shipped release. At n = 6 this is nowhere near significance and is **not** a claim that P1-2 made
the output worse — the run can find a large effect or rule one out, and it cannot resolve a small one.

### What the losing pairs have in common, offered as an observation and not a result

All three arm-A wins turn on the **granularity of degraded states**, in the judges' own words:

- `spec-package-tracking` — v1.27.0 *"collapses 'we couldn't reach the carrier' and 'the carrier hasn't
  scanned in days' into a single `unknown` role"*; v1.26.0 keeps them apart, and they are opposite next
  moves for the user: wait and retry, or stop retrying and chase the sender.
- `concept-medication-reminder` — v1.26.0's dock treats a shared time window as one decision and keeps
  unresolved doses expanded; v1.27.0's focal slot *"holds exactly one item"* and hides the rest behind
  a count row, so a missed dose can sit out of sight.

That is rule 18's displacement, seen for the first time **on the outcome instead of on an indicator**.
§23 could report that colour cells were given back; it could not report what the trade bought or cost
a user. n = 3, so this is a direction to test, not a finding.

> **Corrected in §38.** This paragraph over-reads its own evidence. A mechanical count of labelled
> states shows **only one of the three arm-A wins** has any state-count difference; the other two turn
> on disclosure and on flow structure, and the largest state gap in the corpus produced a tie. What
> survives is narrower and mode-scoped: the displacement is a **Mode C** phenomenon (specs 19 against
> 5; concepts run the other way). Read §38 before carrying anything from this paragraph.

### The instrument behaved, and its confidence signal is now interpretable

Confidence on the null pairs was **3.00** — every judge certain the designs were the same — against
**1.83** on the signal pairs, where the judges hedged. §35 saw the same ordering (3.00 against 2.83) and
§35's P4 called it a failure because it had predicted confidence would track effect size. Across two
runs the pattern is consistent and it is not a defect: **confidence measures certainty of the verdict,
and both a real sameness and a genuinely close call report honestly.** The signal-arm figure falling
from 2.83 on deliberate gross degradations to 1.83 on two real versions of the skill is the instrument
saying, correctly, that this contrast is much harder than that one.

### Rule 33

**Neutralise the confound the arms are made of, in the judge's instruction, before the run.** These two
arms differ by construction in how many values they state; a judge that rewards specification density
would have voted for the substrate arm and the run would have measured presence a third time, wearing a
comparison's clothes. §24 found that an instrument reading the format one arm writes in cannot be
symmetric. Here the asymmetry was visible in advance, so it was written out of the judge rather than
discovered in the results.

### What this does not settle

- **P1-2 is not reverted and nothing here asks for that.** p = 0.254 is not evidence of harm, the
  release's presence gain is real and measured twice, and the craft substrate may well pay on the
  craft-forcing briefs it was measured against.
- **Six briefs, twelve judgements.** The honest summary is that the largest instruction-text effect
  this series has ever shipped does not show up as a better design on ordinary work at this power.
- Judge and both arms share a model family; the null pairs bound that and do not remove it.

---

## 38. §37's mechanism paragraph was an over-reading, and one count refuted it for free

§37 closed with an observation offered as a direction to test: *"All three arm-A wins turn on the
granularity of degraded states."* It was read out of three judgement paragraphs after the fact. Before
spending a corpus on it, it was checked mechanically on the corpus that already existed — and the
check cost one script.

**Pre-registered**: P1, arm A carries more distinct labelled states in total; P2, the gap is
**concentrated in the three briefs the judges gave arm A**, because if arm A simply writes more states
everywhere then the judges' reasons are a story laid over a corpus-wide difference.

### P1 holds, P2 fails

| brief | arm A | arm B | A−B | judge |
|---|---|---|---|---|
| `spec-ipad-clinician` | 10 | 1 | **+9** | **tie / split** |
| `spec-package-tracking` | 9 | 4 | **+5** | A |
| `concept-budgeting-home` | 7 | 7 | 0 | B |
| `concept-medication-reminder` | 6 | 6 | **0** | **A** |
| `flow-onboarding` | 0 | 0 | **0** | **A** |
| `concept-marketplace-listing` | 5 | 7 | −2 | tie |
| **total** | **37** | **25** | **+12** | |

**Two of the three arm-A wins have no state-count difference at all, and the largest difference in the
corpus — +9 — produced a tie.** The concentration prediction is refuted, and by the pre-registered
rule the hypothesis is weaker than §37 stated.

### What the two zero-delta wins were actually decided on

Re-read rather than summarised:

- `concept-medication-reminder` — *"it comes down to how each structures the moment the patient is
  actually in"*: a focal slot that holds exactly one item against a dock that presents a shared time
  window as one decision, and a collapse policy that hides unresolved doses behind a count row. That is
  **disclosure**, not state coverage.
- `flow-onboarding` — *"where the flow spends its screens and where the completion physically
  happens"*: a welcome screen whose only job is to advance, and a first completion performed inside a
  wizard rather than on the surface the user returns to. That is **flow structure**.

Only `spec-package-tracking` turns on degraded-state granularity, and there the count agrees with the
judge exactly. **One of three, not three of three.** §37's sentence is corrected here.

### What survives, and it is sharper than what it replaces

> **Withdrawn in §39.** The count below is produced by a measure that breaks on punctuation: it
> requires `- Label:` or `| Label |` and cannot see `- **Label** — text`, which real specs use
> constantly. Against a repaired diagnostic it undercounts by **7.8 states per artifact on average**,
> with errors to **+25** — it read 1 where the repaired count reads 26. **19 against 5 is not evidence
> of anything.** Read §39.

The state-count difference is real, and it is **entirely a Mode C phenomenon**:

| | arm A | arm B | A−B |
|---|---|---|---|
| Mode A concepts | 18 | **20** | −2 |
| Mode C specs | **19** | 5 | **+14** |

v1.27.0's substrate does not cost state coverage in concepts — concepts run marginally the other way.
It costs it **in specs**, where the output budget is tightest and where state definitions are the
mode's own contract. That is a narrower, mode-scoped claim than §37's, it rests on two briefs rather
than an inference from three paragraphs, and it is what should be tested next if anything is.

### A blind spot in the measure, recorded rather than smoothed over

`flow-onboarding` reads 0 states in **both** arms. That is the measure failing, not the artifacts: both
carry failure→recovery arrows in quantity (**21 and 22** of them). A label-shaped count cannot see
Mode B's contract, so the Mode B row is missing data and is not evidence of anything.

### Rule 34

**A mechanism read out of judges' reasons is a summary of prose, not a measurement — count it before
you carry it.** §37's paragraph generalised three qualitative paragraphs into one mechanism and was
wrong on two of the three. The check that refuted it was one regex over a corpus already on disk, run
before the hypothesis was allowed to justify a new corpus. **The cheapest test of a post-hoc
hypothesis is whether the thing it names is even present**, and it should always run first.

---

## 39. The count in §38 was measuring punctuation, and its own control says so

§38 replaced §37's over-reading with a narrower, mode-scoped claim: v1.27.0's substrate costs state
coverage **in specs** — Mode C 19 against 5. That rested on two briefs at **one draw per cell**, and a
single draw cannot separate a displacement from generation variance. This run adds the missing control.

### Design of the replication

Three fresh Mode C briefs — the golden `## Prompt` blocks for `checkout`, `enterprise-saas` and
`tablet-list-detail`, never run against these two trees. Two arms, **two independent draws per cell**,
twelve generations. The measure is §38's, **frozen byte-for-byte** with its hash recorded before
generation, because it was written after seeing the original gap and must not be tuned to defend it.

### P3, the falsifier, fires

| brief | A d1 | A d2 | B d1 | B d2 | delta |
|---|---|---|---|---|---|
| `checkout` | 11 | 10 | 1 | 3 | **+8.5** |
| `enterprise-saas` | 2 | 0 | 13 | 11 | **−11.0** |
| `tablet-list-detail` | 2 | **16** | 13 | **1** | +2.0 |
| **mean** | | | | | **−0.17** |

Mean within-cell draw-to-draw spread **5.50**, against a mean between-arm delta of **0.17** — the noise
is thirty-two times the effect. By the pre-registered rule the run is **unreadable** and no claim about
displacement follows, in either direction.

### But it is not generation variance. It is the measure.

The per-brief deltas swing to **+8.5** and **−11.0** with tight within-cell agreement on both, which is
not what noise looks like. The diagnosis is in one artifact. `arm-b/checkout-d1` scored **1**. Its
`## State definitions` reads:

> - **Default** — every row resolved, total settled, commit enabled.
> - **Loading (initial)** — rows render from cached cart data immediately; only the fee block and total show skeletons…
> - **Recalculating** — after any change: previous total stays visible…
> - **Unresolved** — a required row missing its value renders as `row.action`…
> - **Error (row-level)** / **Error (screen-level)** / **Error (commit-level)** …

Ten well-differentiated states, scored as one. The measure requires `- Label:` or `| Label |`; this
artifact writes `- **Label** — text`. **It breaks on punctuation.**

A repaired diagnostic count — accepting all three shapes, and offered as diagnosis rather than as a
result, because it is itself unvalidated — puts the frozen measure's error at **+7.8 states per
artifact on average**, ranging from **−3 to +25**. It read 1 where the repaired count reads 26.

**So §38's 19 against 5 is not evidence of anything**, and the Mode C claim is withdrawn. The repaired
count happens to show no displacement either (deltas +5.0, −0.5, −6.5), but that number is not offered
as the answer: an unvalidated measure does not get to settle a question just because it agrees with the
conclusion.

### What still stands

- **§37's headline is untouched.** 6/3/3 at p = 0.254 with the control held came from judges reading
  designs, not from this count.
- **§37's manipulation check stands**, and for a stated reason rather than by assumption: it asks
  whether a token appears *anywhere in the document*, so it has no label-shape to break on, and its
  0/6 baseline reproduced §23's independent measurement of the same indicators.

### The blind spot is a repeat, in the same session

§30 recorded exactly this class: *"a state defined in a markdown table row was invisible to the bullet
parser"* — a false positive on correct work, from a parser that read one shape while real output used
another. That lesson was written down, and then a new counting measure was written days later with the
same shape of blind spot and believed immediately.

### Rule 35

**A measure written to check a hypothesis is an instrument, and rule 2 applies to it — validate it
against hand-read cases before you believe a single number it produces.** Rule 2 was applied to the
state-coverage detector (four injections), to the paired-comparison harness (a discriminating self-test
plus four injections), and skipped for a five-line regex because it looked like arithmetic rather than
an instrument. §34 said *count it before you carry it*; it did not say *validate the count*, and one
sentence of §38 survived a day on the strength of that gap.

### The chain, kept whole because each link is cheaper than the claim it killed

§37 read three judgement paragraphs into one mechanism → §38 refuted that with a count and kept a
narrower claim → §39 finds the count was reading punctuation and withdraws that too. Three
self-corrections, each one costing less than the release it corrected, and the last of them arrived
because a falsifier was pre-registered rather than because anything looked wrong.

---

## 40. Where to pick this up — replacing §12

§12 carries this title and describes the tree at **v1.20.0**, twenty sections and nineteen releases ago.
Anything it says about state, backlog or open questions is superseded. It is kept because the record is
append-only; **start here instead.**

### State

`main` == `origin/main` at **v1.33.3**, working tree clean, both validators green. 34 validator
functions in `validate_repo.py`, 14 in `validate_release.py`, 8 rubric fixtures, plus the paired-eval
self-test and its judge-adapter proof.

**Nothing measurement-shaped is committed, by convention, and nothing needs to be.** Every corpus this
series built lives in a session scratchpad that does not survive. All of it regenerates from committed
briefs — `examples/evals/generation-prompts.json` (10 prompts) and the eight golden `## Prompt` blocks
— and no file in the repository references a scratchpad path.

### What the last nine sections settled

| | |
|---|---|
| **Item 1 — quality vs presence** | **Answered.** The rubric's nine boundary questions give a design and its degraded twin the identical band, **12 paired scorings of 12**, against an instrument with **17% jitter** on unchanged text. A rubric-free paired comparison gets **12 of 12** and names the mechanism each time. The instrument ships: `scripts/run_paired_eval.py`, `docs/paired-comparison.md`. |
| **Item 2 — state coverage** | **Closed negative.** Not checkable from the author's seat (7/12, 4/12), not by a keyword machine (three draws, both gates missed each time, a new failure class deciding each). |
| **Item 3 — the two colour instruments** | **Closed.** There was no conflict; three of four indicators sit at bands 2→3 and 3→4 and only one reaches 4→5. |
| **Items 7–8 — the live floors** | **Premise lost.** The pooled band-5 closure reproduces (47.2% → 48.9%); the per-dimension table does not (`Composition and spacing` 1/6 → 5/5). |

### The three things left open, specified enough to start

**A. CLOSED BOUNDED in §42 — 18 pairs, p = 0.203, and the effect ruled out is anything above a ~85%
brief win rate.** §37 measured P1-2 at **6/3/3, p = 0.254** on six briefs. That can find
a large effect or rule one out; it cannot resolve a small one. The same design at 12–18 briefs would.
*Cost*: roughly double §37's run. *Assets*: the harness ships; the briefs are committed; §37 records the
protocol including the confound line rule 33 requires in the judge prompt. *Trap*: rule 33 — these arms
differ by construction in how many values they state, so the judge must be told that naming more values
is not describing a better screen.

**B. Spec displacement, with a validated measure.** **CLOSED NEGATIVE in §41 — the construct is a
length proxy; do not reopen it as a count.** §38 claimed it, §39 withdrew it — **the hypothesis
was never tested, only the measure was refuted**, and it broke on punctuation (`- **Label** — text`
against `- Label:`). *First step, and it is not a corpus*: build a state-count measure and validate it
against hand-read ground truth on a dozen artifacts before it produces a number anyone believes — rule
35. *Then* re-run §39's design, which is sound: three-plus Mode C briefs, two arms, **two draws per
cell**, with the noise-versus-effect falsifier pre-registered. *Trap*: §30 and §39 hit the same
blind-spot class twice; a parser that reads one label shape while real output writes another is the
failure mode to test for first, not last.

**C. PHASE 2 REFUTED in §43; re-opened and ANSWERED in §44 — obedience to stated rules is 81.1%,
and the gap is structured by rule form: presence 100%, prohibition 83%, value 80%, relation 62.5%.**
**C. P2-4, render-and-critique.** The only route past the standing channel limit: every instrument here,
including the paired comparison, reads a document describing a screen rather than a screen.
`docs/rendered-output-qa.md` is a 359-line workflow whose entry condition is an artifact the skill is
never told to produce. *Cost*: the largest of the three, and the only one that buys a new evidence
channel rather than more of an existing one.

### Two standing items that are not on that list and should not be forgotten

- **`run_generation_eval.py --generate-command` has still never run with a real model behind it.** It is
  the seam item 2's closure points at, and the honest instrument for state coverage is a judged check
  rather than a scanned one.
- **The colour-document question is open, not settled.** §23 withdrew `docs/color-system.md` on `C-dark`
  at 5/6 measured on *craft-forcing* briefs; on ordinary briefs the dark transform is stated **0 times in
  6**. That is a corrected "do not re-assert", and re-opening it needs a pre/post on ordinary briefs.

### How to work here, in one paragraph

Audit before building — four releases in this series died on an unaudited premise and the audit cost
less than the build each time. Pre-register the corpus, the indicators, the predictions **and a
falsifier** before anything runs, and check each indicator against what it would return under the null,
because three in a row failed to measure what they were written for. Verify every constraint and every
guard mechanically, including the ones that look like arithmetic. Hand-adjudicate before believing a
rate. And when a claim is refuted, annotate the section that made it rather than editing it — the chain
from §37 to §39 is worth more intact than any of its three links.

---

## 41. Item B — the displacement hypothesis, hand-read at last, and the noise survives the repair

§38 claimed v1.27.0's craft substrate costs state coverage in Mode C specs (19 against 5). §39 refuted
**the measure** — it requires `- Label:` or `| Label |` while real specs write `- **Label** — text` — and
withdrew the claim, leaving the hypothesis itself untested. §40 listed it as open item B and named the
first step: *build a state-count measure and validate it against hand-read ground truth before it
produces a number anyone believes.*

That is what this section is. It needs no new corpus: §39's twelve artifacts — three Mode C briefs, two
arms, **two independent draws per cell** — survive on disk and were reused, so the entire cost was one
instrument and twelve careful reads.

### The wall, and the freeze

Two corpora, kept apart on purpose. The **shape-development set** is §37's twelve real-contrast
artifacts, used only to enumerate the label shapes real output writes; no hand count was taken there and
no number from it is reported. The **test set** is §39's twelve specs, not opened until the new measure
was frozen at SHA-256 `ea7c9ce9…` with thirteen passing shape fixtures beside it.

Then the test artifacts were copied to `blind/tNN.md` under a shuffled naming whose map was not read
until every hand count was on disk, and counted one at a time against a rule fixed in advance: a
condition counts when the artifact **names** it and specifies what a surface, region or component shows
or does while in it; branches of a decision rule do not count; enumerations of content values (P1–P4,
severity levels) do not count.

### What the new measure fixed, and what it did not

The shape survey alone refuted §38's design before any count ran. §38 keys on a fixed twenty-word
vocabulary, and one arm-A table carries `First load`, `Refreshing`, `No movement`, `Attention`,
`Action required`, `Delivered`, `Not found`, `Over budget` — **eight of its twelve rows are outside any
finite list**. Punctuation was the half §39 found; open vocabulary is the other half. The replacement is
structural: inside a state-definition region every top-level item counts whatever its punctuation, and
outside one a short leading state word is still required.

| | MAE | max abs error | error range | Spearman ρ |
|---|---|---|---|---|
| §38's measure, frozen | 14.08 | 30 | −30 … −4 | 0.143 |
| This measure, frozen | **4.58** | **12** | **−12 … −2** | **0.612** |
| Pre-registered bar (P3) | ≤ 2.0 | ≤ 4 | — | ≥ 0.80 |

Three times better on every axis and it **fails all three bars**, so by the pre-registered rule it
reports diagnosis and settles nothing. One property is worth keeping: all twelve errors are negative in
both measures. A machine state count is a **strict lower bound**, never an over-count.

The residual is a third distinct blind-spot shape, after §30's table-row-invisible-to-a-bullet-parser
and §39's bold-em-dash. The worst artifact (error −12) writes its component states as a table whose rows
are **components** and whose cells are comma-separated state lists — `| Slot row | Empty (required),
chosen, held-with-time, expiring within 5 minutes, expired, sold out while held |`. Every label-shaped
parser reads the first column and returns the component count. **Three shapes, three parsers, three
misses: the format of a state definition is not convergent enough for a scanner, which is what backlog
item 2 concluded in v1.32.1 and this is the same finding arriving from the count side.**

### P2 fires again — and this time it is not the measure

| brief | A d1 | A d2 | B d1 | B d2 | delta A−B |
|---|---|---|---|---|---|
| `checkout` | 37 | 22 | 17 | 18 | **+12.0** |
| `enterprise-saas` | 17 | 18 | 18 | 17 | **0.0** |
| `tablet-list-detail` | 17 | 23 | 17 | 31 | **−4.0** |

Hand-counted, the mean between-arm delta is **+2.67** against a mean within-cell spread of **6.33**. The
run is unreadable by the rule registered before the data, for the second time — but §39's diagnosis does
not survive. §39 said *"it is not generation variance, it is the measure"*; with a human reading every
word the noise is still **2.4×** the effect. The within-cell spreads are `1, 1, 1, 6, 14, 15`: three
cells agree almost exactly and three disagree enormously, and the split is not the arm. **It is whether
that draw happened to write a component-level state matrix.** One arm-A checkout draw enumerates states
for eight components and reaches 37; its twin from the same arm and brief reaches 22.

Both machine measures return the same verdict on the same corpus, and §38's reproduces §39's table cell
for cell — the corpus and the frozen script are intact, which is what makes the hand read readable
against them.

### The finding that closes the item is about the construct, not the power

Hand count against word count across the twelve: **r = 0.777**. The arms are the same length (4816
against 4930 words). **A state count is substantially a verbosity measure**, and the thing it varies
with most is a format choice orthogonal to what either arm changed.

Scaling would not rescue it. At the observed effect (+2.67) and between-brief sd (8.33), 80% power needs
**76 briefs — about 306 generations**, and it would buy a better-powered estimate of a quantity that is
60% length. **Item B is closed, negative**, and the reason is the construct rather than the sample.

### What stands, and what is now retired

- **§37's headline is untouched** for the third section running: 6/3/3 at p = 0.254 came from judges
  reading designs, not from any count.
- **§38's claim stays withdrawn**, and its hypothesis is now tested rather than merely unmeasured.
- **§39's "it is the measure, not generation variance" is corrected.** It was half right: the measure was
  broken and is now three times better, and the null it was offered to explain reproduces without it.
- **Do not build a fourth state-counting parser.** Three shapes have each defeated one, and the count
  they compete to produce is a length proxy.

### Limitations, as registered before the data

One rater, who holds the hypothesis, hand-counting under partial blinding — and the blinding **broke on
one artifact of twelve**: `t06`'s state section is the excerpt published in §39, so it was identifiable
as `arm-b/checkout-d1` on sight. Recorded rather than repaired, because the alternative is discarding a
cell. The counting rule was also tightened after reading the first artifact and before recording any
number, and the tightening is written into the pre-registration with that timestamp; each artifact's
count is stored as `core` plus `extra` so the total's sensitivity to that judgement stays recomputable.
n = 3 briefs bounds a large displacement and cannot resolve a small one — which is the whole point of the
paragraph above it.

### Rule 36

**A measure repaired until it is three times better can still be unfit, and the test of fitness is what
it correlates with — not how close it gets to a hand count.** The instrument here went from MAE 14.08 to
4.58 and from ρ 0.143 to 0.612, and the honest reading of it is not "closer" but *r = 0.777 with word
count*. Rule 2 asks whether an instrument separates a bad corpus from a good one; rule 35 asks whether it
is validated against hand-read cases; **neither asks what else it moves with, and a measure that tracks
length will produce a clean, reproducible, meaningless number forever.** The cheapest form of this check
is one correlation against document length, and it should run in the same pass as the validation.

Also from this run:
- **Reuse of a frozen corpus is worth what a fresh one costs.** Twelve artifacts, one blinding script and
  twelve reads answered a question §39 left open, because nothing measurement-shaped had been thrown
  away that could not regenerate and the arms' generation was already spent.
- **A shape survey is cheaper than a corpus and can refute a design before it runs.** Eight of twelve
  labels in one table sit outside any finite vocabulary; that alone condemned §38's approach without a
  single count.

---

## 42. Item A — P1-2 at eighteen pairs, and the instrument survives the diagnostic that should have killed it

§37 pointed the paired comparison at P1-2 and returned **6 / 3 / 3, p = 0.254, nominal lead to arm A —
the *pre*-substrate tree**. §40 asked for the same design at 12–18 briefs. This is that run, at 18, plus
a second run the first one's own diagnostic made unavoidable.

### Audit first, and it found something

§37's prose says its judges were told *"a longer document is not a better design, and a document that
names more values is not thereby describing a better screen"* — rule 33's confound control, and the
reason §37 believed its result was not presence measured a third time. **The system prompt stored in
§37's own `pairs.jsonl` contains only the length half.** The phrase appears nowhere in that session's
files, and its saved judge directories hold two documents and nothing else. **Rule 33's own release
cannot prove it applied rule 33.**

The gap runs *toward* arm B — it is the half that would have suppressed B's specification-density
advantage — and arm A led anyway, so §37's direction survives it. Its protocol claim does not. The line
now lives in `build_system_prompt()`, so it is generated into every request and greppable afterwards
(rule 32, third application). That makes this a different instrument from §37's, so **§37's twelve
verdicts are not pooled; its six pairs were re-judged from scratch.**

### The run

18 signal pairs in three sets — §37's six re-judged, §39's spec corpus of six judged for the first time,
and six fresh briefs generated from unused golden `## Prompt` blocks against worktrees at v1.26.0 and
v1.27.0. Mode mix **A 5, B 2, C 8, D 1, E 1, F 1**, recorded because rule 28 makes mode a large
uncontrolled factor. Contamination control verified by transcript, not self-report: **247 tool calls
inspected, zero with an input touching `examples/golden/`**. 48 judgements, one fresh judge each.

| | pre-registered | result |
|---|---|---|
| **P1 — control** | agreed winner on ≤ 2 of 6 nulls | **0 of 6**, `no-meaningful-difference` on **12/12**, confidence 5.00 |
| **P2 — arm B reaches significance** | predicted no | **no**; B does not lead at all |
| **P3 — §37's arm-A lead replicates at its magnitude** | predicted no | **it does not**: 67% → **58%** A of decided |
| **P4 — no per-mode concentration** | predicted none | **strained**: Mode C **11/5** (69%), the fresh non-spec modes 5/7 to B |

Pooled: **arm A 21 / arm B 15 / tied 0, p = 0.203**, order-invariant on 15 of 18 pairs. At brief level,
**A 9 / B 6 / split 3**, sign test p = 0.304.

**Item A closes as bounded, not resolved.** The brief-level 95% CI is **[−0.26, +0.59]**, and this design
reaches 80% power only against a tree winning **~85%** of briefs. P1-2 neither helps nor harms by any
margin 18 pairs can see. Mode C's 69% is p = 0.105 on its own and is **not** offered as the finding —
that is the post-hoc subgroup rescue §29 exists to forbid.

One number worth keeping: re-judging §37's own six pairs reproduced **4 of 6** brief-level verdicts.
That is the first test–retest this instrument has on *real* output rather than deliberate degradations,
and it is lower than the ~84% every other instrument here sits at — though it mixes instrument jitter
with the prompt change above.

### The diagnostic that nearly ended the instrument

Rule 36, written one release ago, says check what else a measure moves with. Applied here: **the longer
document won 27 of 36 signal judgements, two-sided p = 0.004.** Where arm A is longer it wins 83%; where
arm A is shorter it wins 33%.

And the six null pairs could not adjudicate it, because of an instruction I wrote: *"aim for a length
within 5% of the original."* The nulls differ by a median **2.3%** against the signal pairs' **13.7%**.
**A control matched on the confound is blind to the confound.** They prove the judge ignores prose
variation — what §35 built them for — and they are structurally incapable of saying anything about
length.

### The falsifier, pre-registered before it ran

Six arm-A responses rewritten as pure verbosity in both directions, every design decision frozen. The
mechanical check (rule 29 — an instruction to an agent is not a constraint) required every
numeric-plus-unit token, every backticked token and every heading to survive as an exact multiset;
**`g-fintech` drifted on four tokens and was excluded rather than repaired**, leaving five pairs, ten
judgements, spanning **−15.2% to +40.2%** with a median gap of 12.0% — the same order as the contrast.

| | |
|---|---|
| longer document won | **0 / 10** |
| shorter document won | **0 / 10** |
| `no-meaningful-difference` | **10 / 10**, confidence **5.00**, including at +40.2% |

**P5 (bias) not met. P6 (no bias) met.** The instrument has no length bias, and the 27/9 association is
length acting as a **proxy for design substance**: when two genuinely different designs are compared,
the one with more decided is described at greater length and judged better. When the design is held
identical, forty percent more words buys nothing.

Across both runs the separation is total: **22 of 22 null judgements returned no difference; 36 of 36
signal judgements found one.** The judge declines exactly when it should and never otherwise.

### Rule 37

**A control matched on the confound cannot test the confound — check what your null pairs hold constant
before you trust them to clear anything.** Rule 36 says find what else the measure moves with; it does
not say the control you already have can answer it. These nulls were built to a length-matching
instruction, which made them incapable of detecting the one correlate that mattered, and no amount of
re-reading them would have revealed it — the fix was five rewrites and ten judgements that deliberately
*moved* the thing under suspicion. **A null that answers "no difference" at 40% more words is worth more
than twenty that answer it at 2%.**

Also from this run:
- **The instrument came out stronger for being attacked.** The paired comparison is now the only
  instrument in this series with a control that varies its principal confound and clears it.
- **`docs/paired-comparison.md` now requires a length-varied null**, with both numbers, so the next
  contrast cannot inherit this blind spot.
- **A claimed control that is not in the tool is not a control.** §37's line was real in intent and
  absent from the record; the same sentence in `build_system_prompt()` is verifiable forever.
- **The mechanical check earned its cost on the first use**, at 1 of 6.

---

## 43. Item C — the rendered channel, gated before it was built, and what the gate found instead

§40 names P2-4 *"the only route past the standing channel limit"*: every instrument in this series,
including the paired comparison, reads a document describing a screen rather than a screen. Building
that channel means document → renderer → screen → judge, which inserts a **renderer** the series has
never had to control. So the renderer was measured first, before a corpus was spent on it.

### The audit, and the premise it narrowed

`docs/rendered-output-qa.md` is 359 lines and is **not** orphaned — six files reference it. What is true
is narrower: `SKILL.md:205` gates it on *"only when a rendered artifact exists"*, and nothing in the
skill produces one. The item is not "wire up a dead document"; it is "does a rendered channel read".

### The gate

Four arm-A responses — two Mode C specs, two Mode A concepts — each rendered **twice by mutually blind
agents** into self-contained HTML, captured at 390 × 844 through one headless binary with identical font
availability, then handed to §42's judge as image pairs, both orders. Pre-registered: **≥ 6 of 8
`no-meaningful-difference`** means the renderer's share is small and phase 2 can proceed; **≥ 6 of 8
naming a winner** refutes item C as specified.

**The first run was voided and is reported, not replaced.** The render prompt said "write the file" and
did not forbid previewing; four of eight agents started `python3 -m http.server` to look at their own
work, two outlived their agents as orphans, and — the part that mattered — preview use **split within
pairs** on two of four documents. A process asymmetry I introduced sat inside the variable being
measured. The re-run forbade it explicitly and was verified per tool call: 0 server or preview attempts
in 20 calls. Rule 29 again, on process rather than corpus.

### P2, met on every judgement

| | |
|---|---|
| named a winner between two renderings of **one** document | **8 / 8** |
| `no-meaningful-difference` | **0 / 8** |
| `difference_kind` | **structural on all 8** |
| order-invariant | **4 / 4 documents** — `r1` won both orders every time |

Mean confidence 3.50. **Item C's phase 2 is refuted**: a rendered contrast between two skill versions
would measure the renderer, not the skill.

### But the reason is not the one the pre-registration guessed, and it is better

The pre-registration allowed that a P2 result would mean *the document underdetermines the screen*.
Hand-adjudication says something sharper. **Every structural difference the judges named is explicitly
stated in the source spec.** `checkout-d1` states the money column three times — *"right-aligned to the
single money column edge"*, *"the money column is the screen's spine — one right-aligned edge"* — and one
render abandoned it, running prices inline. `spec-package-tracking` states *"Between blocks 24dp.
Between rows inside a block 12dp"* and *"grouping is done with spacing, not with borders"*; the judges'
complaint is precisely that one render flattened that ladder. `g-fintech` states *"32 pt between
sections, 16 pt between blocks inside a section, 4 pt between a figure and its scope label"* and calls
the differential *"Gestalt proximity doing the work"*.

**The spec did not leave these open. It stated them, and a competent blind implementer did not obey
them.** That is a fact about the skill's output that no document-channel instrument in this series could
have produced, and it lands directly on a claim the rubric makes.

### The claim it lands on

`docs/design-quality-rubric.md` said, at band 4/5 and again in the `Production readiness` 3 → 4 cell,
that stated values and mappings mean *"two implementers produce the same screen"*. Four specs that state
them produced **8 of 8 structurally different judgements**. Both sites now say the implementers have the
same **decisions in front of them**, and the band-4 note records what stating does not buy. The
questions stay questions — the validator refused a first edit that turned the boundary cell into a
statement, which is rule 1's guard working.

### A measure that had to be rebuilt before it could be believed, again

A fidelity check — what share of each render's spacing values sit on the scale its spec states — first
returned **"the judged-worse render is more faithful, 4 of 4"**. It was wrong: the renders express
spacing through CSS custom properties, so a raw `px` regex saw 5 of 30 declarations. With variables
resolved (validated against declaration counts, 87–121%), the result is **2 of 4 each way**. The broken
version would have shipped a confident inversion of the truth. Fourth instance this session of rule 35.

What survives it is the more interesting half: **scale fidelity does not predict which render was
judged better.** It cannot, because every difference the judges named is a *relation* — between-block
space exceeding within-block space, money sharing one right edge, the accent holding one job — and a
render can draw every value from 4/8/16/32 while setting 24 between rows and 24 between sections.

### Rule 38

**A value on the stated scale is not the rule the scale exists to serve, and checking membership instead
of relation is the presence trap one level down.** §24 established that presence-of-statement is not
quality. This is the same failure at presence-of-value: 42–96% "on scale" across four renders,
predicting nothing about which screen a judge preferred, while the deciding differences were all
relational. Any future implementation check must measure the relation the rule encodes, not the
vocabulary it draws from.

Also from this run:
- **Gate before building, fourth time it has paid.** Twenty-four agents refuted a phase that would have
  cost a corpus, and returned a finding the corpus would not have produced.
- **The rendered channel is not a version comparator. It is a spec-implementability check** — the one
  thing this repo has never had an instrument for, and exactly what `Production readiness` claims to
  score. That is where item C should be re-opened, with the renderer as the subject rather than the
  nuisance.
- **A silent side effect is worse than a loud one.** The orphaned servers ran for minutes and nothing in
  the pipeline surfaced them; the repo's owner did, from outside. Any future run that spawns processes
  needs a mechanical sweep, not an instruction.

---

## 44. Пункт C, переоткрытый — «заявлено» и «выполнено» измерены порознь, и разрыв оказался структурным

§43 отказал пункту C в первоначальном виде и оставил вопрос, для которого в репозитории никогда не было
инструмента: **выполняет ли исполнитель те правила, которые спецификация взяла на себя труд
сформулировать?** `Production readiness` заявляет, что оценивает ровно это.

### Устройство

Четыре спеки и восемь реализаций из §43 — ничего не генерировалось заново. Правила извлекались по одному
агенту на спеку, **вслепую к реализациям**; все **87 цитат проверены на дословность механически, 0
расхождений**. Набор заморожен с SHA-256 до того, как его увидел хоть один проверяющий. Затем по одному
проверяющему на пару (спека × реализация), на входе HTML и PNG, на выходе вердикт по каждому правилу с
обязательным доказательством — измеренное значение, селектор, цвет, позиция.

**23% правил недостижимы статичным рендером** и исключены с причинами: состояния загрузки и ошибки,
движение, порядок фокуса, скринридер, крупный текст, тёмная тема. Почти четверть того, что спека
обязывает сделать, нельзя проверить, глядя на экран по умолчанию, — это результат, а не потеря.

### Фальсификатор, и почему ручная сверка изменила его цифру

В копию каждого r1 механически внедрено по три нарушения, истина зафиксирована заранее. Проверяющий
поймал **10 из 12**. Ручная сверка двух пропусков показала, что виноват не он: в `checkout` деньги
размечены классом `.money`, а правка красила `.value` и попала в строку адреса — **проверяющий сам
опознал инъекцию и объяснил, почему она не задевает денежную колонку**; в `g-fintech` класс `.sec`
оказался цветовым, элементов с ним ноль, и правка отступа не попала никуда. Действительных внедрений
было **10, поймано 10**. Обе цифры сообщаются: 10/12 по букве предрегистрации, 10/10 против внедрений,
которые сработали.

**Надёжность проверяющего измерена в том же прогоне** (правило 30): испорченные копии отличаются от r1
только точечным CSS, поэтому на правилах, которых внедрения не касались, вердикты должны совпадать.
Совпало **50 из 54 — 93%**, выше потолка ~84%, у которого стоят остальные инструменты серии.

### Результат

| | |
|---|---|
| **доля выполнения на чистых реализациях** | **81,1%** (107 выполнено, 25 нарушено), 95% ДИ **[74,4%; 87,7%]** |
| «не определить» | **0 из 132** — проверяющий ни разу не уклонился |
| **P2 (предсказано < 85%)** | **выполнено** |

**Примерно каждое пятое явно сформулированное правило исполнитель нарушает.**

### Разрыв структурен — и это главное

| форма правила | выполнено | нарушено |
|---|---|---|
| наличие («на экране есть X») | **14/14 = 100%** | **0%** |
| запрет («X не появляется») | 35/42 = 83,3% | 17% |
| значение («X равен 24dp») | 48/60 = 80,0% | 20% |
| **отношение («X больше Y», «выровнено по одному краю»)** | **10/16 = 62,5%** | **38%** |

Отношения нарушаются почти вдвое чаще значений (разница 17,5 п.п., точный тест Фишера **p = 0,187** —
ячейка в 16 наблюдений, направление, а не результат; недомощность P4 записана **до** данных). Но
крайние точки шкалы разговаривают сами: **назвать элемент — выполняется всегда, связать два элемента
отношением — не выполняется в трети случаев.**

**Десять правил из 66 нарушены обеими независимыми реализациями** — это не разброс исполнителя, а форма,
которая не переживает реализацию: интервалы зоны в `checkout`, минимальная высота строки, денежная роль,
шкала 8dp в `spec-package-tracking`, «никаких карточек и заливок» в `g-fintech`.

### P3: выполнение и качество — разные оси

Реализация, которую судьи §43 предпочли во всех четырёх парах и в обоих порядках, выполняет правила
**82%**; проигравшая — **80%**. Разницы нет. Соблюдение спеки не объясняет, какой экран сочли лучше, и
§43's вывод о том, что решают отношения, здесь подтверждается с другой стороны: обе реализации одинаково
плохо держат отношения, а расходятся в том, чего спека не диктует.

### Правило 39

**Форма правила предсказывает, переживёт ли оно реализацию: назвать — переживает, связать — нет.** 66
заявленных правил, независимый исполнитель: наличие 100%, запрет 83%, значение 80%, **отношение 62,5%**.
Правило 38 говорило, что принадлежность значения шкале — не то же, что правило, которому шкала служит;
правило 39 добавляет причину: **отношение и есть та форма, которую исполнитель теряет чаще всего**, а
именно отношения решали исход в §43. И это ортогонально качеству — 82% против 80% при счёте судей 4:0.

Ещё из этого прогона:
- **«Не определить» — ноль из 132.** Правило, сформулированное проверяемо, проверяется; неопределённость
  жила в отборе (23% исключённых), а не в вердиктах.
- **Ручная сверка снова изменила цифру** (правило 20): 10/12 превратились в 10/10, потому что два моих
  внедрения не сработали. Инструмент, который объясняет, почему инъекция не считается, — лучше того,
  который её «ловит».
- **Инструкция изменена не будет.** P4 незначим, а правило 15 требует мерить правку на той поверхности,
  куда она поедет. Направление записано, текст не тронут.
- **Закреплённые элементы не там, где их ждут**: `position:fixed` в headless-съёмке разрешается
  относительно полной высоты страницы, и внедрённый FAB не попал в кадр 390 × 844 (0 пикселей при
  попиксельной проверке), оставшись видимым только в исходнике.
