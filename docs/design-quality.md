# Design Quality Calibration

This document defines the skill's design-quality layer: the part that turns a structurally correct mobile design into a clearer, more polished, more production-ready design proposal.

Use `docs/design-quality-rubric.md` when this qualitative calibration needs a 1-5 score, target level, cap, or improvement ladder.

Design quality is not decoration. For this skill, design quality means:

- the user's attention is guided in the right order
- hierarchy is visible without excessive explanation
- spacing, alignment, and grouping make relationships obvious
- typography supports scanning, reading, and confidence
- color communicates priority and state without becoming the only cue
- motion and feedback clarify what happened
- visual language supports brand and trust without overriding usability
- the result can be converted into tokens, components, and QA checks

---

## Research synthesis

The design-quality layer is grounded in the same source hierarchy as the rest of the skill.

Key takeaways:

- Apple HIG frames layout as a way to ground people in content, make important information easy to find, group related items, align components for scanning, and adapt to safe areas and font-size changes.
- Apple HIG frames typography as legibility plus hierarchy: type size, weight, color, and Dynamic Type behavior must preserve the relative hierarchy as text scales.
- Apple HIG frames color as communication: use it consistently, test light/dark/increased-contrast contexts, and never rely on color alone for meaning.
- Apple HIG frames motion as purposeful feedback, not ornament; motion should support status, instruction, and continuity while respecting reduced-motion needs.
- Material 3 and Android guidance frame design quality through color roles, type roles, adaptive layouts, component states, and a simplified type scale that maps display/headline/title/body/label roles to concrete sizes.
- GOV.UK and Fluent both emphasize that clarity, hierarchy, accessibility, and responsive behavior are ongoing design responsibilities, not final visual polish.
- NN/g visual-design principles are useful as critique lenses: scale, visual hierarchy, balance, contrast, and Gestalt grouping.
- Baymard research is a reminder that production quality comes from resolving accumulated medium-level UX issues, especially in dense mobile flows and commerce patterns.

---

## Quality dimensions

### 1. Attention path and hierarchy

A high-quality mobile proposal should identify the intended first glance, second glance, and action path.

Use:

- one primary focal point per screen zone
- 2-3 emphasis levels for most task screens
- size, weight, contrast, position, and spacing to communicate priority
- reading order that matches the platform and locale

Red flags:

- every card, label, or CTA has equal visual weight
- primary action depends only on copy to be noticed
- secondary controls appear before the user understands the main state
- hierarchy is described verbally but not backed by type, spacing, or position

### 2. Composition, spacing, and grouping

Composition should make relationships visible before the user reads every label.

Use:

- a 4- or 8-based spacing system
- tighter spacing inside a group than between groups
- consistent alignment edges for scannable content
- enough negative space around important decisions
- safe-area-aware placement for persistent controls

Red flags:

- decorative cards used where simple rows would scan better
- borders and backgrounds compensate for weak spacing
- section spacing and row spacing are too similar to reveal structure
- layouts depend on fixed heights that break with large text

### 3. Typography craft

Typography should make the screen easier to understand, not merely branded.

Use:

- role-based type tokens, not ad-hoc sizes
- concrete size and line-height guidance
- limited type styles per screen
- medium/semibold weights for emphasis before adding extra colors
- native/system fonts unless brand constraints require otherwise
- text scaling and truncation rules

Red flags:

- more than 4-5 type styles on a routine task screen
- small captions carrying critical information
- thin weights at small sizes
- all caps for routine labels or long text
- center-aligned body copy in dense or transactional screens

### 4. Color, contrast, and semantic meaning

Color should support hierarchy, brand, and state communication.

Use:

- semantic color roles for status and feedback
- neutral surfaces to create depth and grouping
- one primary accent role for the main action or active state
- contrast values that meet the relevant quality bar
- light, dark, and increased-contrast variants when custom colors are proposed
- non-color indicators for status and errors

Red flags:

- brand color used for both interactive and noninteractive elements
- success, warning, and error rely on color alone
- one-note palette where every surface is a tint of the same hue
- visual direction creates low contrast or weak focus states

### 5. Density and rhythm

Density is a product decision, not an aesthetic preference.

Use:

- sparse density for confidence, safety, older adults, onboarding, or high-stakes decisions
- medium density for general consumer tasks
- dense-but-structured layouts for comparison, enterprise, finance, and power-user workflows
- repeated spacing rhythms so users can predict where information starts and ends

Red flags:

- making an information-heavy screen sparse enough to harm comparison
- making a high-stakes screen dense enough to create decision errors
- using whitespace as decoration rather than to clarify grouping
- shrinking text or hit areas to fit more content

### 6. Interaction polish and motion

Interaction polish should make state changes legible and trustworthy.

Use:

- immediate tap feedback
- visible loading, saving, and error states
- motion only when it clarifies continuity or status
- reduced-motion alternatives
- haptics or system feedback where platform-appropriate and not noisy

Red flags:

- animation used to make a weak hierarchy feel "premium"
- slow transitions in utility or power-user workflows
- no visible pressed, loading, disabled, or success state
- motion is the only way a state change is communicated

### 7. Brand expression and visual character

Brand expression is valuable when it supports recognition, trust, or emotional fit.

Use:

- brand moments in lower-risk surfaces such as onboarding, empty states, success states, and illustrations
- restrained brand expression in regulated or high-trust flows
- a clear distinction between product personality and interaction semantics
- inspiration sources only after the usability structure is grounded

Red flags:

- visual style fights platform conventions
- illustration duplicates the copy instead of adding meaning
- brand color weakens status semantics
- portfolio-style polish removes states, edge cases, or implementation constraints

### 8. Production readiness

A high-quality recommendation should be buildable and testable.

Use:

- token-ready sizes, spacing, colors, elevation/surface roles, and motion durations
- component/state mapping
- acceptance checks for text scaling, contrast, touch targets, and state coverage
- notes for platform divergence where it affects implementation

Red flags:

- "make it cleaner" with no measurable change
- "premium visual style" without tokens or constraints
- no dark-mode, large-text, or error-state implications
- component names that do not map to a native component, design-system component, or explicit assumption

---

## Distinctiveness levers

These operationalize "creative / distinctive / memorable / premium" as checkable levers — a count, a token, or a pass/fail question — so distinctiveness can be pushed without becoming aesthetic laundering. Each carries the guardrail that keeps it honest. The frameworks they rest on are non-authoritative creative-range references (see `docs/sources.md`): they inform visual direction, never usability or accessibility proof. In Mode D, these mainly feed the score (via the inert-screen test) and the `Bold move` block.

### The inert-screen test (the anti-forgettable gate)
- Ask: "If this screen lost its logo and brand color, would it still be distinguishable from a competitor's?"
- If no, the screen is inert: `Distinctiveness and owned assets` sits below band 4, and the inert cap in `docs/design-quality-rubric.md` clamps the artifact score with an upside note however well the other dimensions read.

### Onlyness check (Neumeier, *Zag*)
- Can the distinctive choice complete "This is the only [category] that [specific buildable move]…" without a taste word? If the blank fills only with "premium/modern/clean," it fails — that is polish, not a point of difference.

### Distinctive-asset audit (Sharp & Romaniuk, *Building Distinctive Brand Assets*)
- Count the screen's owned, name-independent assets (a color, shape, type treatment, motion signature, mascot). Forgettable = zero owned assets; distinctive = at least one that category competitors do not share.
- Guardrail: an asset must be repeated and consistent to count — this rewards bold use of an existing owned asset and rejects one-off invented decoration, which keeps the no-novelty stance intact.

### Delight-placement gate (Kano model)
- A signature/delight moment is justified only on an *attractive* (delighter) feature — never on a must-be (a missing required affordance) and never instead of a linear performance improvement.

### Norman level + cost check (Norman, *Emotional Design*)
- Tag a signature moment visceral / behavioral / reflective, and confirm it does not raise behavioral cost (extra tap, delayed feedback). A visceral flourish bought with behavioral debt fails.

### Brand-expression budget (Kholmatova, *Design Systems*)
- Budget perceptual (expressive) deviation: about one signature perceptual move per screen, two per flow. Functional patterns (where the control is, what the gesture does) are out of budget and stay conventional (Jakob's Law).

### Motion-personality tokens (Val Head, *Designing Interface Animation*)
- Express motion character as values, not adjectives: exactly one recurring signature transition, a named easing curve tied to a brand adjective — named from the tables in `docs/motion-system.md`, not described as "ease-out" — and a duration taken from the band its interaction belongs to in `docs/quality-bars.md` (see `Signature transition` there). The brand adjective chooses *which* interaction carries the signature and *which* curve it uses — never a longer duration. 400 ms is the ceiling, tap feedback stays at 100–150 ms regardless, and every signature ships a reduced-motion fallback.

### Type-personality split (Lupton, *Thinking with Type*)
- Confine a distinctive/personality typeface to display roles (headlines, hero); keep body and UI text on a readable face. Character bleeding into running text fails.

---

## Design quality calibration section

When the mode produces or packages a design artifact, include a concise quality calibration section.

Use this structure:

```md
## Design quality calibration
- Quality target: [derived]/5 — median of the assessable dimensions {[dimension]: [n], ...}; [outlying dimension] sits at [n]; blocked from [next]/5 by [that dimension] until [named input or fix]
- Attention path:
- Composition and spacing:
- Typography:
- Color and state:
- Interaction polish:
- Signature move:
- Production checks:
```

The `Quality target` line always names the dimension holding the score back and what would lift it. A bare number is a default, not a score.

`Signature move` names the one owned asset or justified signature moment the screen carries, as a token plus where it repeats — or states plainly that the screen is inert and what it would take to change that. It is the field that answers the inert-screen test below; leaving it as an adjective fails.

For short responses, compress it:

```md
## Design quality calibration
- Quality target: [1-5]/5 — [short reason]; blocked from [next level] by [dimension] until [input or fix]
- Prioritize [first thing] visually through [size/position/contrast].
- Use [spacing/type/color rule] to make [relationship/state] clear.
- Signature move: [owned asset as a token] repeated at [locations] — or: none, this screen is inert because [reason].
- Validate [large text/dark mode/state/touch target] before handoff.
```

Do not add this section as a decorative lecture. It should contain decisions the designer or engineer can apply.

---

## Mode guidance

### Mode A: Screen concept

Use design quality calibration to describe the visual hierarchy, density, and visual language of the proposed screen.

### Mode B: User flow

Use design quality calibration only when screen-to-screen pacing, progress feedback, or transition polish materially affects the flow.

### Mode C: UI spec

Use design quality calibration as concrete implementation requirements: token values, type roles, color/state rules, layout rhythm, and QA checks.

### Mode D: Review

Assess visual design quality only to the extent supported by the input. If no visual is provided, review structure and mark visual quality as unverifiable.

### Mode E: Typography and spacing system

Use design quality calibration to define rhythm, density presets, role limits, and large-text behavior.

### Mode F: Rationale / handoff

Use design quality calibration to explain why the final direction feels appropriate for the product context and how engineering should preserve it.

---

## Calibration checklist

Before returning a design proposal, ask:

- Can the primary action or state be identified in the first glance?
- Are there no more than 2-3 competing emphasis levels in the main screen area?
- Do spacing values reveal grouping before borders or cards are needed?
- Are type roles concrete and limited enough to implement consistently?
- Does color communicate state and hierarchy without being the only cue?
- Does density match the user's task and context?
- Are motion and feedback purposeful, fast enough, and optional when needed?
- Can this be translated into tokens, components, and QA acceptance checks?
- Inert-screen test: with the logo and brand color removed, is this screen still distinguishable from a competitor's? If not, it is inert — record `Distinctiveness and owned assets` below band 4 and let the inert cap clamp the score with an upside note.

If the answer is "no" or "not sure", revise the recommendation before returning it.

---

## Source references

- [Apple Human Interface Guidelines: Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
- [Apple Human Interface Guidelines: Typography](https://developer.apple.com/design/human-interface-guidelines/typography)
- [Apple Human Interface Guidelines: Color](https://developer.apple.com/design/human-interface-guidelines/color)
- [Apple Human Interface Guidelines: Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- [Material 3 in Compose / Android Developers](https://developer.android.com/develop/ui/compose/designsystems/material3)
- [Fluent 2: Layout](https://fluent2.microsoft.design/layout)
- [Fluent 2: Typography](https://fluent2.microsoft.design/typography)
- [Fluent 2: Color](https://fluent2.microsoft.design/color)
- [GOV.UK Design Principles](https://www.gov.uk/guidance/government-design-principles)
- [GOV.UK Design System: Accessibility](https://design-system.service.gov.uk/accessibility/)
- [Baymard: Mobile E-Commerce UX](https://baymard.com/research/mcommerce-usability)
- [NN/g: 5 Visual-design Principles in UX](https://media.nngroup.com/media/articles/attachments/Principles_Visual_Design-Letter.pdf)
