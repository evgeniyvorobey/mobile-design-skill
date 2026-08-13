# Proposal: quality ceiling and design diversity upgrade

Status: **released as v1.17.0.** Commits 1–6 plus three acceptance-driven fix commits. Cross-run variance (acceptance criterion A3) is unresolved and carried to v1.18.0.
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
| P1-11 | **Resolve `skill/skill.md`.** 489 lines, on no load path, self-contradictory internally. Either delete it (porting the classifier hints and the "no vague advice" hard constraint into `SKILL.md`) or declare it a non-Claude-host entrypoint and bring it under the parity validator. Leaving three files that each claim to be the workflow is the condition that produced the drift in §2.1. **Owner decision required.** |

### P2 — long-horizon

| # | Change |
|---|--------|
| P2-1 | `scripts/run_generation_eval.py` reusing the proven `--judge-command` stdin/stdout contract and importing `MODE_REQUIREMENTS` unchanged; ~10 prompts × N runs. First validator that reads generated text. |
| P2-2 | `scripts/run_diversity_eval.py` — decision-vector extraction (pattern name, hierarchy sequence, component set, named alternative, emitted numbers, owned asset), cross-prompt uniqueness, rejected-alternative entropy, frame repetition. Drop within-prompt divergence from the first cut: no sampling-temperature contract exists, so a threshold is unjustifiable until baseline data exists. |
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
| 4 | Tablet MVU: P0-7 plus `docs/adaptive-layout.md`, the large-screen bars, `Device class:` in the six template headers and in `MODE_REQUIREMENTS`. New sources added to `docs/sources.md`. | pending |
| 5 | Honesty and scope: P0-8, P0-9. | ✅ landed |
| 6 | Corpus and CI: P1-5, P1-4, P1-6, P1-7. | ✅ landed |

Deferred to 1.18+: P1-2 (wants the direction step in production first, so the token fields are shaped by real
use), P1-8, P1-9, P1-10, and the whole P2 tier. P1-11 awaits an owner decision.

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
