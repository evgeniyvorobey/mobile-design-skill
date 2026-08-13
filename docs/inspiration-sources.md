# Inspiration Sources

This document defines the skill's inspiration and reference layer.

The goal is to improve visual range, product awareness, and pattern benchmarking without weakening the evidence hierarchy. Inspiration sources can help answer "what could this feel like?" or "how do strong products approach this surface?" They must not be used as proof for usability, accessibility, platform behavior, or compliance.

For source-specific benchmark guidance, use [`visual-benchmark-playbooks.md`](visual-benchmark-playbooks.md).

---

## Core rule

Use inspiration sources only after the design decision is already grounded in:

1. official platform guidance and standards
2. accessibility and usability standards
3. maintained design systems and production pattern references
4. context, task, and implementation constraints

Inspiration can shape visual direction, comparison examples, and exploration breadth. It cannot justify a recommendation by itself.

Bad:
- "Use this pattern because it is popular on Dribbble."
- "This is accessible because similar layouts appear on Behance."
- "Awwwards sites use this motion, so it is appropriate for checkout."

Better:
- "The interaction pattern is justified by the task and platform conventions. For visual tone, Mobbin and Apple Design Award winners can be used as reference sets."
- "Use Dribbble or Behance to explore visual language only after the flow, hierarchy, and accessibility requirements are stable."

---

## Source tiers

### Tier 1: Production UI and flow references

Use first when the user asks for mobile product references, real app examples, or pattern benchmarking.

| Source | Best for | Use carefully because |
|--------|----------|----------------------|
| Mobbin | Real mobile and web app screens, flows, product UI patterns | It shows what exists, not what is automatically right for the user's context |
| Page Flows | End-to-end user flows, onboarding, checkout, upgrade, search, account flows | It is strongest for journey comparison, not visual polish alone |
| UI Sources | Interaction videos and app journeys from production apps | Availability and coverage vary by product category |
| Pttrns | Mobile pattern browsing and app screen references | Some patterns may be old; verify current platform fit |
| Screenlane | Mobile and web UI screen inspiration | Treat as screen reference, not validation evidence |

### The skill cannot read these sources

Mobbin, Page Flows, UI Sources and Pttrns sit behind sign-in or paid subscriptions, and a skill run has no session for any of them. Even in a host with web access, a fetch returns a landing page, not the screens. Screenlane is more open but still not something the skill has browsed.

Therefore:

- Name them as a **lookup for the user to perform**, never as something already consulted.
- Do not describe what a specific product's screen on one of these sites looks like. That is a description of a screen nobody in this conversation has seen.
- Do not attribute a pattern to "what Mobbin shows" or "current examples on Page Flows".
- If the user pastes a screenshot, a flow description, or their own notes from one of these, that becomes real evidence and is reviewable as normal D1 input.

The same applies to award galleries and portfolio sites: naming them as places to look is useful; narrating their current contents is fabrication.

### Tier 2: Platform and award references

Use when the user asks for high-quality craft, platform-native excellence, or polished interaction direction.

| Source | Best for | Use carefully because |
|--------|----------|----------------------|
| Apple Design Awards | iOS craft, interaction quality, accessibility/inclusivity inspiration, platform-native polish | Award winners are exceptional references, not templates to copy |
| Material Design blog / case studies | Android and Material-aligned product craft, system adoption, expressive UI | Case-study context may not match the user's product constraints |
| Awwwards | Web craft, typography, visual experimentation, motion, editorial interaction | Often web-first and visually expressive; not a mobile usability baseline |

### Tier 3: Visual portfolio and moodboard references

Use when the user asks for visual exploration, brand direction, moodboards, or creative range.

| Source | Best for | Use carefully because |
|--------|----------|----------------------|
| Behance | Case studies, branding, presentation craft, visual systems | Work may be conceptual or polished for portfolio storytelling |
| Dribbble | Visual treatments, components, micro-interactions, style exploration | Many shots are isolated and may ignore real states, accessibility, and edge cases |
| Pinterest | Moodboards, visual themes, broad aesthetic discovery | Weak for product logic, interaction behavior, and implementation detail |
| Figma Community | UI kits, design systems, templates, interaction patterns | Quality varies; do not assume accessibility or platform correctness |

---

## Reasoning and point-of-view sources (derivation layer)

The tiers above are a *retrieval* layer — places to see what exists. These are a *derivation* layer: they teach why strong products made a decision, so you can reason about your own context. They go beyond Apple/Google. The same rule applies — never proof of usability, accessibility, platform correctness, or compliance.

### Production-reasoning sources (the "why", not the look)

| Source | Teaches | Do NOT use for |
|--------|---------|----------------|
| Airbnb Design (DLS, "Building a Visual Language") | Deriving a system from named principles; cross-platform componentization | Proof your tokens are accessible or platform-correct |
| The Linear Method | Opinionated defaults that reduce user decisions; scoping and quality-bar mindset | Usability/accessibility evidence |
| Stripe design/engineering writing | Reasoning behind developer experience and accessible color-system construction | A blanket "Stripe does X so X is correct" |
| Figma blog; Intercom product principles; Spotify Design | Process, design-system governance, decision frameworks | Platform-behavior or compliance proof |
| Shopify Polaris | Stated reasoning behind dense/admin patterns | Assuming Polaris reasoning transfers to your platform |
| Smashing Magazine; A List Apart | Technique deep-dives and durable craft principles | Authoritative standards (defer to WCAG/HIG/Material) |

### How step 5.5 samples this catalog

`SKILL.md` step 5.5 draws **two of its three candidate directions from the two catalogs below** — one compositional school, one point-of-view product. This is the mechanism that stops the option set collapsing to the model's modal answer for a surface: a free-generated candidate set is unimodal, a sampled one is not.

The selection rule, restated here because this is the file the step loads:

1. Discard entries whose `Do NOT use for` line disqualifies them for the domain, audience, and use context at hand.
2. From the survivors, pick the entry whose token consequences differ **most** from the conventional baseline — not the first that fits.
3. Carry the entry's name into the output as `from:` provenance.

**Asset classes**, for the divergence rule on the committed direction's owned asset: colour, geometry/shape, type treatment, motion signature, layout structure, illustration/mascot. Three answers reaching for a layout-structure meter under three names is one retrieved asset, not three owned ones.

### Editorial / typographic / compositional schools (range beyond platform defaults)

These are the direction vocabulary for step 5.5 in `SKILL.md`. Each entry carries **token consequences**, because a direction that exists only as a school name produces three drafts that differ in adjectives and not in output.

**These token sets are this skill's translation into mobile product terms, not a historical claim about the school.** They are directional defaults: a starting point to differentiate three candidate directions, always overridden by a design system the user supplied, and always re-checked against the evidence hierarchy (contrast, text scaling, touch targets, platform fit) before anything ships.

#### Swiss / International Typographic Style
- **Teaches**: grid, hierarchy, and whitespace as compositional logic
- **Base unit / ratio**: 8 / 1.25 (major third)
- **Type role split**: one grotesque across every role; character comes from size and weight contrast, never a second face
- **Colour rule**: one neutral ramp plus a single accent; semantic roles defined separately so the accent can change without moving state meaning
- **Shape posture**: radius 0–4, borders over shadows, elevation 0–1
- **Density**: comfortable-to-dense — alignment carries grouping well enough that dividers can be deleted
- **Composition move**: strict modular grid with one deliberately asymmetric content column
- **Motion signature**: screen-level transition at 300 ms, standard curve, moving position rather than scale
- **Icon stance**: geometric, single stroke weight
- **Do NOT use for**: accessibility or interaction proof; emotionally warm consumer onboarding; screens that must reassure rather than be precise

#### Müller-Brockmann, *Grid Systems*
- **Teaches**: modular grids richer than the 4/8 pt platform grid
- **Base unit / ratio**: 8 / 1.2 (minor third)
- **Type role split**: 2–3 roles maximum; tighter tracking at display sizes only
- **Colour rule**: near-monochrome plus one signal colour reserved exclusively for state
- **Shape posture**: radius 0, elevation 0 — whitespace and rule lines carry structure
- **Density**: dense and modular
- **Composition move**: a 4- or 6-column modular grid where content spans unequal column counts
- **Motion signature**: minimal — a 150 ms cross-fade, nothing else
- **Icon stance**: labels over glyphs; icons only where a label cannot fit
- **Do NOT use for**: a guarantee of usability; task-critical mobile flows needing strong affordance cues; low-vision contexts where rule lines would be doing contrast's job

#### Vignelli, *The Vignelli Canon*
- **Teaches**: typographic restraint; principle over novelty
- **Base unit / ratio**: 8 / 1.25
- **Type role split**: one family, three roles, few sizes — restraint is the expression
- **Colour rule**: neutral plus exactly one saturated accent, never two; semantic colours stay outside the brand palette
- **Shape posture**: radius 0, no shadows
- **Density**: comfortable, generous margins
- **Composition move**: a repeated fixed header band at a constant type size across every screen
- **Motion signature**: none beyond state feedback at 100–150 ms
- **Icon stance**: single weight, no decorative glyphs
- **Do NOT use for**: platform or accessibility proof; products needing playfulness, gamification, or multi-brand theming

#### Brutalist / editorial web craft
- **Teaches**: expressive composition and editorial pacing for low-risk surfaces
- **Base unit / ratio**: 4 / 1.333 (perfect fourth) — the smaller base allows deliberately uneven rhythm
- **Type role split**: a personality display face confined to headlines and hero; body and UI on the readable system face
- **Colour rule**: high-contrast unblended pairs; semantic colours added separately rather than borrowed from the expressive palette
- **Shape posture**: radius 0, visible borders, elevation 0
- **Density**: irregular by intent — uneven vertical rhythm is the point
- **Composition move**: one full-bleed type block that breaks the grid, once per screen
- **Motion signature**: abrupt, 150 ms, minimal easing softening, with a reduced-motion fallback to instant
- **Icon stance**: heavy stroke, or none at all
- **Do NOT use for**: mobile usability or task-critical flows; regulated domains; any screen whose hierarchy must stay unambiguous under stress

### Point-of-view products (study the PRINCIPLE, never copy the surface)

The principle is what transfers; the token consequence is what makes it show up in the output. Take one principle as the forced input in the generative method below, or as the thesis of a candidate direction in step 5.5.

| Product | The one transferable principle | Token consequence when you take it |
|---------|-------------------------------|-------------------------------------|
| Linear | Opinionated defaults reduce decision cost | Remove one control per screen and ship its most common value as the default; density tightens one step because fewer options need room |
| Arc / The Browser Company | The "novelty tax": weigh novelty against learnability | Budget exactly one unfamiliar interaction per flow, and pair it with a conventional path to the same outcome |
| Things / Cultured Code | Craft as subtraction | Cap type roles at 3 and elevation levels at 2; spacing, not borders or cards, carries every grouping |
| Teenage Engineering | Constraints as a creative feature | Fix the palette at 2 colours plus neutrals, or the grid at one column count, and let the constraint become the recognizable asset |
| Superhuman | Perceived speed as a design material | Optimistic UI plus skeletons at the 200 ms threshold; the signature transition goes to the *fastest* band, not the showiest |
| Duolingo | Motivation mechanics on named psychology (with an ethics caveat) | One progress token (streak, ring, bar) repeated in at least three surfaces; never gate a required task behind it |
| Monzo / Revolut / Robinhood | Personality inside a trust constraint | Personality lives in the accent and in empty/success states only; money, status, and destructive actions stay on neutral semantic colour |
| Headspace / Calm | Pace and calm as design materials | Raise the base unit to 8 and the section gap to 32; motion signature at the slow end of its band; one focal element per screen |
| Spotify Wrapped | Data storytelling over data visualization | One number per screen at display size, its context as a caption below — replacing a chart, not annotating one |

---

## Canonical URLs

### Production UI and flows

- [Mobbin](https://mobbin.com/)
- [Page Flows](https://pageflows.com/)
- [UI Sources](https://uisources.com/)
- [Pttrns](https://www.pttrns.com/)
- [Screenlane](https://screenlane.com/)

### Platform and awards

- [Apple Design Awards](https://developer.apple.com/design/awards/)
- [Material Design blog and case studies](https://m3.material.io/blog)
- [Awwwards](https://www.awwwards.com/)

### Visual portfolios and moodboards

- [Behance](https://www.behance.net/)
- [Dribbble](https://dribbble.com/)
- [Pinterest](https://www.pinterest.com/)
- [Figma Community](https://www.figma.com/community)

---

## When to use inspiration

Use this layer when the request includes signals such as:

- "give me references"
- "visual inspiration"
- "make it feel premium"
- "modern app examples"
- "best-in-class examples"
- "benchmark competitors"
- "moodboard"
- "visual direction"
- "explore a few styles"

`SKILL.md` mirrors this exact list at its inspiration gate. If a signal is added here it must be added there too — a gate narrower than this list silently disables the layer for the requests that need it most.

Step 5.5 loads this document for direction vocabulary regardless of these signals. The signals govern the *reference and benchmark* layer: whether to name production examples, run the generative method in full, or return an `Inspiration references` section.

Do not turn every response into a reference hunt. Most screen specs, reviews, and handoff notes should stay focused on the user's task unless inspiration is explicitly useful.

---

## How to present inspiration in outputs

When inspiration is useful, keep it separate from UX rationale:

```md
## Inspiration references
- Production pattern references: Mobbin, Page Flows, UI Sources
- Visual direction references: Behance, Dribbble, Awwwards
- Use these for: visual range, comparable surfaces, interaction examples
- Do not use these for: accessibility proof, platform requirements, compliance claims
```

Do not overfit the user's design to a gallery trend. Use references to widen options, then choose using the skill's normal workflow: task clarity, context, platform conventions, accessibility, quality bars, pattern matrices, and implementation constraints.

Use [`benchmark-report-format.md`](benchmark-report-format.md) when the task needs a structured 3-5 reference comparison. It keeps benchmark observations separate from proof and translates references into tokens, components, states, and QA checks.

---

## Generative direction method

When the user wants a fresh direction (not just references), derive one instead of retrieving a gallery. Run this only AFTER the design is grounded in the evidence hierarchy; it widens options, it does not replace grounding.

This is the long form of step 5.5 in `SKILL.md`. That step is mandatory for every generated artifact and names three directions; this method is what you run when the request explicitly asks for a fresh direction, references, or exploration and three is not enough breadth.

1. Reframe the job (JTBD): "When [situation], I want to [motivation], so I can [outcome]."
2. Open the question (How Might We): 2–3 HMW questions from the job.
3. Diverge fast (Crazy Eights): 8 distinct directions in one timeboxed pass to beat first-idea bias.
4. Inject a forced input (de Bono Random Entry / "Po"): a random word, a point-of-view product's principle, or a compositional school — plus one deliberate provocation.
5. Transform a baseline (SCAMPER): Substitute, Combine, Adapt, Modify, Put-to-other-use, Eliminate, Reverse.
6. Cross-industry analogy: borrow a *mechanism* from a non-competitor domain, never its surface.
7. Converge on 2–3 directions, each named as a short thesis (not a moodboard).
8. Translate to mechanism (mandatory): use the same token fields as step 5.5 — base unit and scale ratio, type role split, colour-construction rule, one composition move, motion signature with its band and reduced-motion fallback — plus a density choice with a reason and state coverage.
9. Re-check against the evidence hierarchy (contrast, text scaling, touch targets, navigation recovery, platform fit).

A direction is not "done" until it exists as tokens, components, and states — never as adjectives.

---

## Reference → transferable mechanism

A reference is never reproduced; it is decomposed into the mechanism it implies.

- airy feel → a spacing ratio (baseline grid + line-height), not a screenshot
- "premium" density → an explicit density choice with a reason, validated against touch-target and readability minimums
- a reference's motion → a motion intent (orientation/feedback) + timing + reduced-motion fallback
- a striking layout → one composition move (e.g. an asymmetric grid), expressed as columns/zones

Benchmark to learn, not to copy: NN/g "Competitive Usability Evaluations" ("you want to beat the competition, not copy them") and "7 Steps to Benchmark Your Product's UX" (a benchmark is a metric to measure against, not a design to replicate).

---

## Review checklist

Before returning an inspiration-backed response, confirm:

- Does each direction differ from the others in at least two token fields, rather than in adjectives?
- Are the token values presented as directional defaults, not as brand facts the user supplied?
- Does the motion signature take its duration from the band in `docs/quality-bars.md` rather than from a brand adjective?

- Is the recommendation grounded in task, platform, accessibility, and implementation reasoning before inspiration is mentioned?
- Are production references separated from portfolio/moodboard references?
- Are inspiration sources framed as examples, not proof?
- Is the user warned when a reference category is likely to be visually attractive but weak for production UX?
- Are official platform and accessibility sources still higher priority?

If any answer is "no", revise the response before returning it.

---

## Maintenance

- Review these sources quarterly and remove dead or low-signal references.
- Add a new source only if it improves a real output mode.
- Prefer production app references over concept galleries when the user is making product decisions.
- Keep portfolio/moodboard sources available, but clearly labeled as visual exploration.
