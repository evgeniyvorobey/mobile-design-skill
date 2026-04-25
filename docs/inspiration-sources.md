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

Do not use this layer by default for every response. Most screen specs, reviews, and handoff notes should stay focused on the user's task unless inspiration is explicitly useful.

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

## Review checklist

Before returning an inspiration-backed response, confirm:

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
