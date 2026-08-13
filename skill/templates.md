# Output Templates

Use these templates as the response skeleton for each mode.

Templates are structure, not quality. Before returning any filled template, run the known-weakness preflight from `docs/weaknesses.md` and the 1-5 design-quality rubric from `docs/design-quality-rubric.md`; do not expose the preflight as a separate output section unless the user explicitly asks for failure-mode analysis.

---

## Clarification-only template

Use this only when `docs/clarification-policy.md` says missing information blocks a reliable artifact.

```md
Mode: [best inferred mode]
Platform scope: [known / unspecified / assumed]
Device class: [known / assumed phone / assumed adaptive]
Assumptions:
- [known fact or minimal assumption]
- [what cannot be safely assumed]

## Clarifying questions
1. [blocking question]
2. [blocking question if needed]
3. [blocking question if needed]

## Why this blocks
- [reason tied to task/platform/accessibility/safety/implementation]

## Fast path
- [smallest safe assumption for a provisional draft]

## Next actions
- [answer questions or confirm fast path]
- [share missing artifact/context if needed]
```

---

## Template A: Generate mobile screen concept

```md
Mode: Generate mobile screen concept
Platform scope: [iOS / Android / Cross-platform / Assumed]
Device class: [Phone / Tablet / Foldable / Adaptive]
Assumptions:
- [assumption 1]
- [assumption 2]

## Screen goal
[what the screen is for]

## Primary user task
[the main action the user needs to complete]

## Information hierarchy
1. [highest priority content/action]
2. [secondary content/action]
3. [supporting content/action]

## Recommended layout structure
- Header:
- Primary content area:
- Secondary content area:
- Persistent actions / navigation:
- Footer or bottom area if relevant:

## Suggested components
- [component] — [why]
- [component] — [why]

## Interaction notes
- [behavior]
- [behavior]

## Empty / loading / error states
- Empty:
- Loading:
- Error:

## Platform-specific notes
### iOS
- [only if relevant]

### Android
- [only if relevant]

## Accessibility considerations
- [consideration]
- [consideration]
- [consideration]

## Adaptive behavior
<!-- Include only when Device class is not Phone. Omit entirely for phone-only work. -->
- Breakpoint: [compact < 600dp / medium 600-839dp / expanded >= 840dp — name the ones this product supports]
- Canonical layout: [list-detail / supporting pane / feed] — [why this one]
- Navigation by width: [bottom bar at compact / rail at medium / sidebar at expanded]
- Collapse rule: [what the two-pane layout becomes at compact, and what back does in each state]
- Detail-pane empty state: [placeholder with an action / default selection]
- Multitasking: [Split View / Slide Over / Stage Manager / multi-window — what survives a resize]
- Input additions: [pointer / hardware keyboard / drag-and-drop / stylus] — touch minimums unchanged, every drag has a non-drag path

## Design quality calibration
- Direction: [thesis] (from: [catalog entry name / baseline]) — committed over the two in `Alternatives considered`
- Dimension read: [dimension] [n], [dimension] [n], ... (mark `n/v` where the evidence channel cannot carry the question). Median of the assessable = [n].
- Quality target: [derived]/5 — [below the top band: blocked from [next]/5 by [outlying dimension] until [named input or fix] | at the top band: nothing blocks 5/5 — [the resilience the bands record]]
- Attention path:
- Composition and spacing:
- Typography:
- Color and state:
- Interaction polish:
- Signature move: [owned asset as a token] repeated at [locations] — or: none, this screen is inert because [reason], and [what would change it]
- Production checks:

## Rationale for major choices
- [decision] because [reason]
- [decision] because [reason]

## Alternatives considered
- Direction rejected — [thesis] (from: [catalog entry name / baseline]): [base unit / ratio], [type role split], [colour rule], [composition move], [motion signature] — rejected because [mechanism tied to user goal, task, platform, accessibility, or implementation]
- Direction rejected — [thesis] (from: [catalog entry name / baseline]): [at least two token consequences] — rejected because [mechanism]

## Next actions
- [action]
- [action]
```

---

## Template B: Design mobile user flow

```md
Mode: Design mobile user flow
Platform scope: [iOS / Android / Cross-platform / Assumed]
Device class: [Phone / Tablet / Foldable / Adaptive]
Assumptions:
- [assumption 1]
- [assumption 2]

## Flow goal
[what the flow needs to accomplish]

## Entry points
- [entry point]
- [entry point]

## Ordered steps / screens
1. [screen/step]
2. [screen/step]
3. [screen/step]

## Decision points
- [condition] → [branch]
- [condition] → [branch]

## Back-navigation logic
- [rule]
- [rule]

## Failure and recovery paths
- [failure case] → [recovery]
- [failure case] → [recovery]

## Platform behavior notes
### iOS
- [note]

### Android
- [note]

## Accessibility and usability risks
- [risk]
- [risk]

## Simplification opportunities
- [opportunity]
- [opportunity]

## Next actions
- [action]
- [action]
```

---

## Template C: Create platform-aware UI spec

```md
Mode: Create platform-aware UI spec
Platform scope: [iOS / Android / Cross-platform / Assumed]
Device class: [Phone / Tablet / Foldable / Adaptive]
Assumptions:
- [assumption 1]
- [assumption 2]

## Screen or flow scope
[scope]

## Structural zones
- Top area:
- Main content area:
- Supporting area:
- Bottom actions / navigation:

## Components by section
### Section 1
- [component]
- [component]

### Section 2
- [component]
- [component]

## State definitions
- Default:
- Focused / active:
- Loading:
- Empty:
- Error:
- Success:
- Disabled if applicable:

## Behavior rules
- [rule]
- [rule]

## Content guidance
- [content principle]
- [content principle]

## Spacing and layout notes
- [note]
- [note]

## Typography rules
- [role] → [usage]
- [role] → [usage]

## Accessibility requirements
- [requirement]
- [requirement]
- [requirement]

## Adaptive behavior
<!-- Include only when Device class is not Phone. Omit entirely for phone-only work. -->
- Breakpoint: [compact < 600dp / medium 600-839dp / expanded >= 840dp — name the ones this product supports]
- Canonical layout: [list-detail / supporting pane / feed] — [why this one]
- Navigation by width: [bottom bar at compact / rail at medium / sidebar at expanded]
- Collapse rule: [what the two-pane layout becomes at compact, and what back does in each state]
- Detail-pane empty state: [placeholder with an action / default selection]
- Multitasking: [Split View / Slide Over / Stage Manager / multi-window — what survives a resize]
- Input additions: [pointer / hardware keyboard / drag-and-drop / stylus] — touch minimums unchanged, every drag has a non-drag path

## Design quality requirements
- Direction: [thesis] (from: [catalog entry name / baseline]) — committed over the two in `Alternatives considered`
- Dimension read: [dimension] [n], [dimension] [n], ... (mark `n/v` where the evidence channel cannot carry the question). Median of the assessable = [n].
- Quality target: [derived]/5 — [below the top band: blocked from [next]/5 by [outlying dimension] until [named input or fix] | at the top band: nothing blocks 5/5 — [the resilience the bands record]]
- Attention path:
- Composition and spacing:
- Typography:
- Color and state:
- Interaction polish:
- Signature move: [owned asset as a token] repeated at [locations] — or: none, this spec is inert because [reason], and [what would change it]
- Production checks:

## Platform-specific implementation notes
### iOS
- [note]

### Android
- [note]

## Key decision tradeoffs
- [decision] chosen over [alternative] because [reason]
- [decision] chosen over [alternative] because [reason]

## Next actions
- [action]
- [action]
```

---

## Template D: Review screen for usability/accessibility

```md
Mode: Review screen for usability/accessibility
Platform scope: [iOS / Android / Cross-platform / Assumed]
Device class: [Phone / Tablet / Foldable / Adaptive]
Sub-case: [D1 visual provided / D2 description only / D3 problem statement / D4 context change]
Assumptions:
- [assumption 1]
- [assumption 2]

## Quick summary
[one-paragraph assessment; for D3, lead with diagnosis hypothesis]

## Strengths
- [strength]
- [strength]

## Findings
> Each finding is one causal chain, ordered by severity. High-severity (3–4) findings use all fields. Low/cosmetic (0–2) may compress to Observation → Change → Severity. Never split an issue from its fix.

### F1 — [short title]
- Lens: [Usability / Accessibility / Hierarchy & readability / Design quality / Navigation & interaction]
- Observation: [what is there now — evidence-bound; for D2, structure & behavior only, no visual assertions]
- Violated principle: [named — e.g. Nielsen #5 Error prevention · Hick's Law · Cognitive load (extraneous) · Gestalt proximity · Wroblewski form-design]
- User consequence: [the mechanism by which it hurts the user — not a restatement of the observation]
- Change: [the specific edit]
- Predicted effect: [directional + confidence — "should reduce mis-submits; confidence M (D2 text-only)". Never a fabricated %]
- Severity: [0–4, Nielsen] — [frequency × impact × persistence, one line]
- Moves: [dimension] [n]→[n] — the boundary question the fix answers; + "lifts cap: …" if applicable

### F2 — [short title]  (full form, repeat F1's fields)
- Lens:
- Observation:
- Violated principle:
- User consequence:
- Change:
- Predicted effect:
- Severity:
- Moves:

### F3 — [short title]  (compressed form for a cosmetic/severity-0–2 finding)
- Observation: [what is there now]
- Change: [the specific edit]
- Severity: [0–2, Nielsen] — [one-line reason]

## Design quality score (current → projected)
- Current: [1-5]/5 — the median of the assessable `Now` bands in the table below; [evidence-based reason; "provisional" for D2/D3]
- Projected: [1-5]/5 — the median of the assessable projected dimensions once the listed fixes land; conditional: requires F[..] AND [assumptions]. State a flat number, not "up to". [D2/D3: provisional — visual dimensions stay unassessable.]
- Ceiling note: with a visual pass confirming [x], the ceiling is [1-5]/5 (capped at 4/5 unless resilience is named). Visual dimensions are never projected upward from a text-only review.
- Primary lever(s): [the one or two findings that move the score most]

| Dimension | Now | Projected | Gated by (cap / ladder rung) | Confidence |
|-----------|-----|-----------|------------------------------|------------|
| Attention path & hierarchy | [n] | [n] | [cap / rung / —] | [verifiable / provisional / not-from-text] |
| Composition & spacing | [n] | [n] | | |
| Typography craft | [n] | [n] | | |
| Color, state & contrast | [n] | [n] | | |
| Density & rhythm | [n] | [n] | | |
| Interaction polish & motion | [n] | [n] | | |
| Context & brand fit | [n] | [n] | | |
| Production readiness | [n] | [n] | | |
| Distinctiveness & owned assets | [n] | [n] | | |
- Both overall numbers = the median of the assessable (non-`n/v`) bands in the matching column, lowered if a critical task dimension stays weak. Neither is the sum of per-dimension gains, and neither is raised by a dimension the input cannot verify. A higher number reachable only after a visual pass belongs in `Ceiling note`, not here.
- A band is `n/v` only when the evidence channel cannot carry the question — not when the input is merely thin. See the two-axis rule in `docs/design-quality-rubric.md`: routing thin evidence to `n/v` removes the weakest dimension from the median.

## Severity index
> A rollup for triage (0 = not a problem, omitted). Each finding already carries its severity inline.
- 4 (catastrophe): [F..]
- 3 (major): [F..]
- 2 (minor): [F..]
- 1 (cosmetic): [F..]

## Bold move (optional — omit unless the trigger is met)
> Use only when ALL hold: the screen is already competent (current ≥3/5) but inert (loses no major points yet has no point of view); there is no unresolved severity-3 or severity-4 finding (fix those first); and there is a concrete UX upside. Allowed in D1/D3; D2 = structure/flow only; D4 = only if the new context unlocks it. This is NOT a fix and NOT required to ship. At most one (two only if genuinely distinct). If unsure, omit.

- The move: [one buildable sentence — a component/layout/flow/interaction change, not an adjective]
- Deviates from: [the product assumption / current direction / brand rule / platform convention it contradicts]
- Job served (JTBD): [the job + one desired-outcome statement: minimize/increase [metric] of [object] when [context]]
- UX upside: [concrete, checkable benefit — tie to a named heuristic or quality bar]
- Risk / cost: [learnability, discoverability, accessibility exposure, or dev cost if this is wrong]
- De-risk / validate: [the cheap test before committing + kill criterion + the contrast/large-text/reduced-motion checks it must still pass]
- Score impact: safe fixes alone → [X]/5; this move targets [Y]/5; it does NOT raise the score until validated.
- Conviction: [Speculative / Worth a spike / High-confidence]

## Platform-convention mismatches
- [mismatch]
- [mismatch]

## Unresolved assumptions
- [unknown]
- [unknown]

## Next actions
- [action]
- [action]
```

---

## Template E: Create typography and spacing system

```md
Mode: Create typography and spacing system
Platform scope: [iOS / Android / Cross-platform / Assumed]
Device class: [Phone / Tablet / Foldable / Adaptive]
Assumptions:
- [assumption 1]
- [assumption 2]

## Type roles
- Display:
- Screen title:
- Section title:
- Body:
- Secondary body:
- Label:
- Caption / helper:
- Button / action label:

## Size hierarchy
- [role] → [size guidance]
- [role] → [size guidance]

## Weight usage
- [weight] for [purpose]
- [weight] for [purpose]

## Line-height guidance
- [guidance]
- [guidance]

## Spacing scale
- 4
- 8
- 12
- 16
- 24
- 32
- 40

## Density rules
- [rule]
- [rule]

## Visual rhythm rules
- Direction: [thesis] (from: [catalog entry name / baseline]) — committed over the two in `Alternatives considered`
- Dimension read: [dimension] [n], [dimension] [n], ... (mark `n/v` where the evidence channel cannot carry the question). Median of the assessable = [n].
- Quality target: [derived]/5 — [below the top band: blocked from [next]/5 by [outlying dimension] until [named input or fix] | at the top band: nothing blocks 5/5 — [the resilience the bands record]]
- [rule]
- [rule]

## Touch-target implications
- [implication]
- [implication]

## Accessibility considerations
- [consideration]
- [consideration]

## Usage examples
- App bar:
- List row:
- Form:
- Detail screen:
- Bottom action area:

## Next actions
- [action]
- [action]
```

---

## Template F: Prepare design rationale / handoff

```md
Mode: Prepare design rationale / handoff
Platform scope: [iOS / Android / Cross-platform / Assumed]
Device class: [Phone / Tablet / Foldable / Adaptive]
Assumptions:
- [assumption 1]
- [assumption 2]

## Design objective
[objective]

## Target users and context
[users and context]

## Key design decisions
- [decision] — alternative considered: [alternative] — chosen because [reason tied to user goal, task, platform, accessibility, or implementation]
- [decision] — alternative considered: [alternative] — chosen because [reason]

## Pattern choices and why
- [pattern] over [alternative pattern] because [reason]
- [pattern] over [alternative pattern] because [reason]

## Design quality rationale
- Direction: [thesis] (from: [catalog entry name / baseline]) — committed over the two in `Alternatives considered`
- Dimension read: [dimension] [n], [dimension] [n], ... (mark `n/v` where the evidence channel cannot carry the question). Median of the assessable = [n].
- Quality target: [derived]/5 — [below the top band: blocked from [next]/5 by [outlying dimension] until [named input or fix] | at the top band: nothing blocks 5/5 — [the resilience the bands record]]
- Signature move: [owned asset as a token] repeated at [locations] — or: none, this design is inert because [reason], and [what would change it]
- [quality decision] — [mechanism: size/spacing/alignment/color/density/motion/token] — [why it fits context]
- [quality decision] — [mechanism] — [why]

## Platform alignment
### iOS
- [alignment note]

### Android
- [alignment note]

## Accessibility and usability considerations
- [consideration]
- [consideration]

## States and edge cases
- [state]
- [state]

## Implementation notes
- [note]
- [note]

## Open questions
- [question]
- [question]

## Validation plan / recommended testing focus
- [test focus]
- [test focus]

## Next actions
- [action]
- [action]
```
