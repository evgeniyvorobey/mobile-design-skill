# Mobile App Design Skill

![version](https://img.shields.io/badge/version-1.4.0-blue) ![license](https://img.shields.io/badge/license-MIT-green)

A production-ready reusable AI skill for Claude Code / Codex that helps users generate, review, structure, and justify mobile UI/UX design decisions for iOS, Android, and cross-platform products.

Current version: **1.4.0** — see [`CHANGELOG.md`](CHANGELOG.md) for details and [`docs/versioning.md`](docs/versioning.md) for the versioning policy.

- canonical Codex entrypoint: [`SKILL.md`](SKILL.md)
- Codex UI metadata: [`agents/openai.yaml`](agents/openai.yaml)
- extended prompt/reference set: [`skill/`](skill) and [`docs/`](docs)
- output previews instead of screenshots: [`examples/`](examples)

This skill is built for practical product work, not decorative nonsense. It treats mobile design as a combination of:

- usability
- navigation predictability
- readability and typography
- accessibility
- hierarchy and interaction clarity
- platform-aware behavior
- implementation-ready structure

It supports six primary modes:

1. Generate mobile screen concept
2. Design mobile user flow
3. Create platform-aware UI spec
4. Review screen for usability/accessibility
5. Create typography and spacing system
6. Prepare design rationale / handoff

---

## What this skill is for

Use this skill when you need help with:

- mobile screen concepts
- information hierarchy
- component recommendations
- layout guidance
- user flows and navigation
- platform-specific behavior notes
- typography and spacing systems
- accessibility-aware critique
- handoff-ready rationale and implementation notes

It is designed to prefer durable official guidance over trend-driven aesthetic advice.

---

## Design philosophy

This skill enforces the following principles:

- Mobile UI design is not only visual styling. It includes usability, navigation, readability, accessibility, hierarchy, and interaction predictability.
- Accessibility is a built-in design requirement, not a final compliance pass.
- Typography is part of usability and interaction quality.
- Platform conventions matter. iOS and Android should not be blended when platform-specific behavior is relevant.
- Strong design output must be explainable through user goals, context, platform norms, and evidence-backed principles.
- Recommendations should prefer durable official guidance over trend-driven aesthetic advice.
- Outputs should be practical, structured, and implementation-friendly.

---

## Source hierarchy

The skill uses this source priority:

1. Official platform guidance and standards
2. Accessibility and usability standards
3. Public-sector and enterprise-grade design systems
4. Established research and case-study sources
5. Workflow and tooling references

Primary source families built into the skill:

- Apple Human Interface Guidelines
- Material Design 3
- Android Navigation guidance
- WCAG 2.2
- W3C guidance for applying WCAG to mobile apps
- ISO 9241-210
- ISO 9241-11
- GOV.UK Design System patterns
- NHS Design System typography
- Fluent 2 typography/accessibility
- Figma Variables guidance
- case-study based learning and system thinking

See [`docs/sources.md`](docs/sources.md) for the full hierarchy.

---

## Source provenance

The canonical source appendix in [`docs/sources.md`](docs/sources.md) was consolidated from an external curation document used during repository preparation:

- `Design thinking.pdf` (`Curated Learning Map for Mobile UI/UX Design Using US and European Sources`)

The PDF itself is not bundled in this repository, but the normalized public URLs and grouped source map are now preserved in the repo.

---

## Screenshots

Screenshots are intentionally not included in this repository.

To show the expected quality and structure of outputs, the repository uses worked examples instead:

- [`examples/generate-screen.md`](examples/generate-screen.md)
- [`examples/design-flow.md`](examples/design-flow.md)
- [`examples/ui-spec.md`](examples/ui-spec.md)
- [`examples/review-screen.md`](examples/review-screen.md)
- [`examples/typography-spacing.md`](examples/typography-spacing.md)
- [`examples/rationale-handoff.md`](examples/rationale-handoff.md)
- [`examples/anti-patterns.md`](examples/anti-patterns.md) — calibration examples showing how the skill should behave when input is ambiguous or invites a hallucination

---

## Repository structure

```text
mobile-design-skill/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
├── .claude/
│   └── skills/
│       └── mobile-design-skill/
│           └── SKILL.md
├── agents/
│   └── openai.yaml
├── .github/
│   └── workflows/
│       └── validate.yml
├── scripts/
│   └── validate_repo.py
├── skill/
│   ├── skill.md
│   ├── metadata.yaml
│   ├── modes.md
│   ├── templates.md
│   └── usage.md
├── docs/
│   ├── commands.md
│   ├── context-defaults.md
│   ├── evals.md
│   ├── github-publishing.md
│   ├── guardrails.md
│   ├── heuristics.md
│   ├── principles.md
│   ├── quality-bars.md
│   ├── self-review.md
│   ├── sources.md
│   ├── versioning.md
│   └── workflow.md
└── examples/
    ├── anti-patterns.md
    ├── generate-screen.md
    ├── design-flow.md
    ├── ui-spec.md
    ├── review-screen.md
    ├── typography-spacing.md
    └── rationale-handoff.md
```

---

## Installation / setup

No package installation is required.

Copy this repository into your prompts, skills, or internal AI-skills directory, then load the skill entrypoint:

- primary skill entrypoint for Codex: `SKILL.md`
- Codex UI metadata: `agents/openai.yaml`
- extended prompt source: `skill/skill.md`
- legacy metadata: `skill/metadata.yaml`

Suggested repository name:

`mobile-design-skill`

---

## How to use in Claude Code

### Option 1: Native slash invocation

This repository now includes a Claude Code project skill at:

- `.claude/skills/mobile-design-skill/SKILL.md`

When the repository is opened as a Claude Code project, you can invoke it directly with:

```text
/mobile-design-skill
```

Or pass a task inline:

```text
/mobile-design-skill review this Android settings screen for usability and accessibility
```

### Option 2: Manual skill loading
Provide the contents of `SKILL.md` as the primary skill prompt.

If you want the expanded prompt pack available during use, keep these references alongside it:

- `skill/modes.md`
- `skill/templates.md`
- `docs/sources.md`
- `docs/workflow.md`

### Option 2: Skill registry pattern
If your Claude Code setup supports skill registries, register:

- name: `mobile-design-skill`
- entrypoint: `SKILL.md`
- metadata: `skill/metadata.yaml`

### Typical invocation
```text
Use the mobile-design-skill.

Create a platform-aware UI spec for a medication refill screen in a cross-platform healthcare app.
Audience: older adults
Primary goal: request refill quickly and safely
Constraints: accessibility-sensitive, high trust, existing design system, dense medical content
```

---

## How to use in Codex

Attach or inject `SKILL.md` as the governing instruction for the assistant instance handling product design tasks.

Recommended pattern:

1. Load `SKILL.md` as the active design skill prompt
2. Keep `skill/modes.md`, `skill/templates.md`, and `docs/sources.md` available as supporting references
3. Use `examples/` for regression checks and prompt QA

Example:
```text
Use the mobile-design-skill.
Task: review a settings screen for usability and accessibility.
Platform: Android
Screen description: ...
Constraints: enterprise, high density, one-handed use
```

---

## Input the skill accepts

The skill is designed to accept any combination of:

- app idea
- feature description
- user goal
- target audience
- platform: iOS / Android / cross-platform
- screen type
- current wireframe or screen description
- flow description
- constraints such as brand, accessibility, enterprise context, content density, or time pressure

If information is missing, the skill makes only minimal clearly labeled assumptions.

---

## Output behavior

The skill always:

- classifies the request into exactly one primary mode
- determines platform scope
- checks whether enough information exists
- labels assumptions clearly
- includes usability and accessibility considerations by default
- includes platform-aware notes whenever platform choice matters
- prefers operational guidance over theory dumps
- distinguishes facts from recommendations
- ends with practical next actions

---

## Hard constraints enforced

The skill must not:

- invent official platform rules
- invent research findings or usability test results
- claim accessibility compliance unless explicitly verified
- give purely aesthetic advice without usability reasoning
- ignore typography, spacing, navigation, or touch behavior
- output vague advice like “make it cleaner” without concrete interpretation
- collapse iOS and Android guidance into one answer when conventions differ
- overcomplicate with unnecessary theory when the user needs a design artifact
- invent components, flows, or states unless they are explicitly framed as assumptions

---

## Files to start with

- Start here: [`SKILL.md`](SKILL.md)
- Claude Code slash wrapper: [`.claude/skills/mobile-design-skill/SKILL.md`](.claude/skills/mobile-design-skill/SKILL.md)
- Codex UI metadata: [`agents/openai.yaml`](agents/openai.yaml)
- Expanded prompt source: [`skill/skill.md`](skill/skill.md)
- Mode definitions: [`skill/modes.md`](skill/modes.md)
- Output templates: [`skill/templates.md`](skill/templates.md)
- Usage guide: [`skill/usage.md`](skill/usage.md)
- Command reference: [`docs/commands.md`](docs/commands.md)
- GitHub publishing kit: [`docs/github-publishing.md`](docs/github-publishing.md)
- Source hierarchy: [`docs/sources.md`](docs/sources.md)
- Guardrails: [`docs/guardrails.md`](docs/guardrails.md)
- Evaluation criteria: [`docs/evals.md`](docs/evals.md)
- Quality bars (numeric thresholds): [`docs/quality-bars.md`](docs/quality-bars.md)
- Context-aware defaults (audience × domain × platform × use-context): [`docs/context-defaults.md`](docs/context-defaults.md)
- Heuristics catalog (Fitts, Hick, Jakob, Nielsen, Gestalt with mobile applications): [`docs/heuristics.md`](docs/heuristics.md)
- Self-review pass: [`docs/self-review.md`](docs/self-review.md)
- Versioning policy: [`docs/versioning.md`](docs/versioning.md)
- Anti-patterns: [`examples/anti-patterns.md`](examples/anti-patterns.md)

---

## Worked examples

Each mode includes a full example prompt and example output:

- [`examples/generate-screen.md`](examples/generate-screen.md)
- [`examples/design-flow.md`](examples/design-flow.md)
- [`examples/ui-spec.md`](examples/ui-spec.md)
- [`examples/review-screen.md`](examples/review-screen.md)
- [`examples/typography-spacing.md`](examples/typography-spacing.md)
- [`examples/rationale-handoff.md`](examples/rationale-handoff.md)

---

## Maintenance

When updating this skill:

1. update `CHANGELOG.md`
2. keep `SKILL.md`, `skill/skill.md`, and `agents/openai.yaml` aligned
3. keep source priority aligned with `docs/sources.md`
4. preserve the six-mode classification model
5. keep platform-aware distinctions intact
6. do not relax the evidence and accessibility guardrails just because somebody wants prettier nonsense faster
7. run `python3 scripts/validate_repo.py` before publishing changes

---

## License

See [`LICENSE`](LICENSE).
