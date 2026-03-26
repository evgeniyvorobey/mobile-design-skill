# GitHub Publishing Kit

This document contains ready-to-use GitHub metadata and launch copy for `mobile-design-skill`.

Use it when creating the repository, filling the GitHub "About" section, and preparing the first public release.

---

## Recommended repository description

Use this as the primary GitHub repository description:

`Reusable AI skill for Claude Code / Codex that generates, reviews, and structures mobile UI/UX decisions for iOS, Android, and cross-platform products.`

Shorter variant:

`Reusable Claude Code / Codex skill for practical mobile UI/UX design and review.`

---

## Suggested topics

Recommended GitHub topics:

- `ai-skill`
- `codex`
- `claude-code`
- `prompt-engineering`
- `mobile-ui`
- `mobile-ux`
- `ios-design`
- `android-design`
- `cross-platform`
- `accessibility`
- `design-system`
- `ux-review`
- `ui-spec`
- `product-design`
- `design-ops`

If you want a tighter list, keep this core set:

- `ai-skill`
- `codex`
- `claude-code`
- `mobile-ui`
- `mobile-ux`
- `ios-design`
- `android-design`
- `accessibility`
- `design-system`

---

## Release title

Recommended first public release title:

`v1.1.0 — GitHub-ready release`

Alternative:

`v1.1.0 — Public packaging release`

---

## Release notes

Recommended release text:

```md
## Mobile App Design Skill

`mobile-design-skill` is a reusable AI skill for Claude Code / Codex focused on practical mobile product design work.

It helps generate, review, structure, and justify mobile UI/UX decisions for:

- iOS
- Android
- cross-platform products

### What it supports

- mobile screen concepts
- user flows
- platform-aware UI specs
- usability and accessibility reviews
- typography and spacing systems
- design rationale and handoff

### What is included in this release

- canonical `SKILL.md` entrypoint for Codex
- Codex UI metadata in `agents/openai.yaml`
- expanded prompt pack in `skill/`
- supporting documentation in `docs/`
- worked examples in `examples/`
- repository validation script and GitHub Actions workflow

### Quality bar

This skill is designed to prioritize:

- usability over decoration
- accessibility by default
- platform-aware guidance
- implementation-friendly output
- clearly labeled assumptions
- durable source hierarchy over trend-driven advice

### Notes

- Screenshots are not included in this repository.
- Worked examples are provided instead to show the expected structure and output quality.
- The source appendix in `docs/sources.md` was consolidated from an external curated research/reference document used during repository preparation.
```

---

## Recommended README intro for GitHub visitors

If you want a slightly sharper opener for the top of the README or social preview text, use:

```md
Reusable AI skill for Claude Code / Codex that helps product teams generate, review, and hand off mobile UI/UX decisions for iOS, Android, and cross-platform apps.
```

Alternative:

```md
Practical mobile UI/UX skill for Claude Code / Codex with structured outputs for flows, screen concepts, UI specs, accessibility reviews, and handoff.
```

---

## Positioning notes

Recommended positioning for public publishing:

- Present it as a reusable skill, not a generic prompt dump.
- Emphasize mobile product design, accessibility, and platform conventions.
- Be explicit that Claude Code supports `/mobile-design-skill` through the bundled `.claude/skills/` wrapper.
- Describe Codex support as standard skill compatibility, not guaranteed slash-command compatibility, unless OpenAI documents a slash entrypoint for the target Codex surface.
- Use worked examples as the substitute for screenshots.
- Keep the value proposition operational: structured outputs, strong guardrails, and implementation usefulness.

Avoid over-positioning it as:

- visual inspiration
- generic design thinking advice
- aesthetic trend guidance
- screenshot-driven portfolio material
