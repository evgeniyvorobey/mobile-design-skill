# Proposal: quality ceiling and design diversity upgrade

Status: **in progress** — Commits 1–3 landed, Commits 4–6 pending.
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
| P0-7 | **Tablet MVU** — see §4. | `SKILL.md`, `skill/templates.md`, `docs/adaptive-layout.md`, `docs/quality-bars.md`, `docs/clarification-policy.md` |
| P0-8 | **No-fit escape hatch.** `Mode: outside the standard six — <what it is>` instead of rounding paywall/notification-frequency/whole-app-IA requests to the nearest template. | `SKILL.md`, `docs/workflow.md`, `docs/self-review.md` |
| P0-9 | **Auth-wall honesty.** State that Mobbin / Page Flows / UI Sources / Pttrns / Screenlane cannot be opened. Rewrite the self-review prompt that currently asks whether the model used them — it is a standing invitation to describe a screen it never saw. Add a guardrail marking version-bound rows as current-as-of-last-review. | `docs/inspiration-sources.md`, `docs/visual-benchmark-playbooks.md`, `docs/self-review.md`, `docs/guardrails.md` |

### P1 — structural, one release

| # | Change |
|---|--------|
| P1-1 | ✅ *landed in Commit 3* **Token-consequence schema for the art-direction catalog.** Convert the school/product list in place: base unit + ratio, type role split + pairing rule, colour-construction rule (neutral anchor + accent derivation + semantic roles held separate), radius/elevation/border posture, density posture, motion signature, iconography stance, "do not use for". Reconcile the motion bands first — `docs/design-quality.md` says 200–500 ms while `docs/quality-bars.md` caps navigation at 300–400 and tap feedback at 100–150, so the signature currently has no room. |
| P1-2 | **Craft substrate:** `docs/color-system.md` (platform semantic roles first, derived ramp only on user-supplied brand, any printed ratio labelled as computed); a layout section in quality bars (margins by class, baseline grid tying line-height boxes to spacing steps, columns/gutters, optical-alignment rules); motion by cited platform curves (M3 easing tokens, SwiftUI spring presets, Compose stiffness/dampingRatio) with distance/size rules and stagger caps; type-scale ratio by density anchored at body 17/16, tracking-at-size, role → iOS text style / M3 type role mapping. Broaden Mode E to "typography, spacing, and colour". |
| P1-3 | **Cross-file parity validator.** ✅ *landed in Commit 1* |
| P1-4 | **Rebuild the golden `Design quality calibration` blocks** to carry a named direction as tokens plus one owned asset with repeat locations, guardrail lines intact. Assert a `Signature move:` line naming a token and a repeat location, pairwise-distinct across files. Do **not** require literal hex/typeface values — that would model the invented brand specifics the skill forbids. |
| P1-5 | **Corpus diversity validator** over golden + example + case-study files: at most 60 % of `Quality target:` lines share a score (fails today at 32/33), and median pairwise 5-gram Jaccard of calibration-block bodies at most 0.15. First cross-response instrument in the repo. |
| P1-6 | **Fix the tautological CI step and the flat fixtures.** Rename the oracle step so it stops claiming to validate quality. Current rubric fixtures are 31–52 words with dimension spreads of 0,1,1,0,0 — a judge ignoring the median rule passes the whole pack. Add an adversarial fixture with spread ≥ 2 and assert `expected_score == floor(median(dimension_scores))` unless a cap is present. |
| P1-7 | **Shape assertions in the prose validator.** Replace bare-word matches (`\bover\b`) with bullet-count plus word-count-after-`because` assertions; replace the five-element generic-next-actions denylist with a positive test (each bullet contains a digit, a mid-sentence capitalized token, or a backticked identifier). Fix the examples, not the rules. |
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
| 5 | Honesty and scope: P0-8, P0-9. | pending |
| 6 | Corpus and CI: P1-5 (land it knowing it fails at 32/33, then rebuild goldens per P1-4 until it passes), P1-6, P1-7. | pending |

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
