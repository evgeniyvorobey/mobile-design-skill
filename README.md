<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo-light.svg" alt="Mobile Design Skill" width="640">
  </picture>
</p>

<p align="center">
  <img alt="version" src="https://img.shields.io/badge/version-1.36.0-blue">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-green">
</p>

# Mobile App Design Skill

A production-ready reusable AI skill that helps generate, review, structure, and justify mobile UI/UX design decisions for iOS, Android, and cross-platform products.

Works as a Claude Code skill (native slash invocation), as a Codex / OpenAI skill, and as a system prompt for direct Claude API or any LLM integration.

Current version: **1.36.0** — see [`CHANGELOG.md`](CHANGELOG.md) and [`docs/versioning.md`](docs/versioning.md).

---

## Table of contents

- [Quickstart](#quickstart)
- [What this skill does](#what-this-skill-does)
- [Install](#install)
  - [Claude Code — terminal (recommended)](#claude-code--terminal-recommended)
  - [Claude Code — manual](#claude-code--manual)
  - [Codex / OpenAI](#codex--openai)
  - [Claude API (Python)](#claude-api-python)
  - [Claude API (TypeScript)](#claude-api-typescript)
  - [Cursor and other IDEs](#cursor-and-other-ides)
- [Usage](#usage)
- [Supported modes](#supported-modes)
- [Architecture](#architecture)
- [Updating](#updating)
- [Uninstalling](#uninstalling)
- [Customization](#customization)
- [Versioning](#versioning)
- [Contributing](#contributing)
- [License](#license)

---

## Quickstart

One-liner terminal install for Claude Code:

```bash
git clone https://github.com/evgeniyvorobey/mobile-design-skill.git ~/mobile-design-skill
cd ~/mobile-design-skill
./scripts/install.sh
```

Then open Claude Code and invoke:

```text
/mobile-design-skill review this Android settings screen for usability and accessibility
```

That's it. The rest of this README covers other integration paths and what the skill actually does.

---

## What this skill does

This skill enforces a practical framework for mobile design decisions. It is built for product work, not decorative advice.

It is structured around:

- **Six primary modes** — every request is classified into exactly one: screen concept, user flow, platform-aware UI spec, usability/accessibility review, typography/spacing system, or handoff rationale.
- **Clarification policy** — asks only blocking questions, otherwise proceeds with minimal labeled assumptions.
- **Judged mode** — `/mobile-design-skill --judge` drafts, runs an independent rubric judge pass when the host supports subagents, revises if needed, and returns a compact score summary.
- **Guardrails** — no invented platform rules, no fabricated research findings, no aesthetic-only advice without usability reasoning.
- **Quality bars** — concrete numeric thresholds (touch 44pt iOS / 48dp Android, WCAG 2.2 AA contrast, line-height 1.4–1.6, motion 200–300ms).
- **Design quality calibration** — visual hierarchy, composition, density, typography craft, color semantics, motion/feedback, brand expression, and production-readiness checks.
- **Design quality rubric** — 1–5 scoring derived from the assessable dimensions for generated artifacts, and a current → projected score in reviews.
- **Rubric eval pack** — score-calibrated fixtures for `1/5` through `5/5` plus a before/after upgrade example.
- **LLM-as-judge runner** — LLM-agnostic JSONL runner with an external-agent command adapter for semantic rubric calibration.
- **Visual benchmark playbooks** — source-specific checklists for Mobbin, Page Flows, Apple Design Awards, and Awwwards that keep inspiration separate from evidence.
- **Golden examples** — compact taste and domain calibration examples for premium UI, enterprise SaaS, fintech, health, onboarding, settings, checkout, and tablet list-detail.
- **Synthetic case studies** — 12 bad-to-good calibration cases that show weak vs strong mobile design responses without real products or screenshots.
- **Visual review fixtures** — Figma-like text descriptions with expected critique and prohibited overclaims for Mode D review calibration.
- **Benchmark report format** — a compact structure for turning 3-5 references into borrow / do-not-copy / token-component-state guidance.
- **Domain packs** — mini-playbooks for fintech, health, SaaS, marketplace, social, and education.
- **Rendered-output QA workflow** — optional post-implementation QA guidance for checking mobile viewports, overlap, clipping, tap-target risk, contrast hints, and state behavior when a rendered artifact exists.
- **Known weakness prevention** — internal failure-mode preflight for generic output, first-idea bias, evidence overreach, platform flattening, happy-path-only design, and weak handoff.
- **Context-aware defaults** — adjusts output for audience (older adults, children, power users), domain (finance, health, government, enterprise, social), platform, and use-context (one-handed, outdoor, in-vehicle, emergency).
- **Heuristic grounding** — decisions cite Fitts, Hick, Jakob, Zeigarnik, Gestalt, Nielsen rather than being presented as preference.
- **Pattern catalog** — decision matrices for navigation, overlays, lists, pickers, feedback surfaces, forms, search, and authentication. No inventing novel patterns where established ones fit.
- **Inspiration layer** — Mobbin, Page Flows, UI Sources, Pttrns, Screenlane, Apple Design Awards, Awwwards, Behance, Dribbble, Pinterest, and Figma Community are available for visual inspiration and benchmarking, but kept separate from UX/accessibility evidence.
- **Mandatory self-review** — the skill runs a silent quality pass before returning any response.

See [`docs/`](docs) for the full framework.

---

## Install

### Claude Code — terminal (recommended)

**Prerequisites**: git, bash, Claude Code installed.

Clone this repository to a stable location and run the install script:

```bash
git clone https://github.com/evgeniyvorobey/mobile-design-skill.git ~/mobile-design-skill
cd ~/mobile-design-skill
./scripts/install.sh
```

This creates a symlink from `~/.claude/skills/mobile-design-skill` to the cloned repo, making the skill available globally in every Claude Code session.

**Alternatives**:

```bash
# Install only inside the current project (not global)
./scripts/install.sh --scope project

# Install inside a specific project
./scripts/install.sh --scope project --project-path /absolute/path/to/project

# Use a self-contained copy instead of a symlink (for filesystems without symlink support)
./scripts/install.sh --method copy

# Check where the skill is installed
./scripts/install.sh --status

# Remove the install
./scripts/install.sh --uninstall
./scripts/install.sh --uninstall --scope project
```

**Verify**:

```bash
./scripts/install.sh --status
```

Output should show `symlink -> /path/to/mobile-design-skill/.claude/skills/mobile-design-skill` for your chosen scope.

Open Claude Code and try:

```text
/mobile-design-skill
```

---

### Claude Code — manual

If you prefer to bypass the install script:

```bash
# Global install (any Claude Code session)
mkdir -p ~/.claude/skills
ln -s /absolute/path/to/mobile-design-skill/.claude/skills/mobile-design-skill \
      ~/.claude/skills/mobile-design-skill

# Or project-local install (only for one project)
mkdir -p /path/to/project/.claude/skills
ln -s /absolute/path/to/mobile-design-skill/.claude/skills/mobile-design-skill \
      /path/to/project/.claude/skills/mobile-design-skill
```

The symlink must point to the `.claude/skills/mobile-design-skill` subdirectory of the cloned repo, not to the repo root.

If you cannot use symlinks, run `./scripts/install.sh --method copy`, which builds a self-contained copy with paths rewritten to stay within the installed directory.

---

### Codex / OpenAI

This repository ships a Codex-compatible entrypoint at [`SKILL.md`](SKILL.md) and UI metadata at [`agents/openai.yaml`](agents/openai.yaml).

**Option A — attach as system prompt**:

```bash
# Read the canonical skill prompt
cat ~/mobile-design-skill/SKILL.md
```

Paste the contents as the system prompt for your Codex session, or inject it via the API:

```python
from openai import OpenAI

with open("SKILL.md") as f:
    system_prompt = f.read()

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Design a payment screen for an iOS banking app."}
    ],
)
print(response.choices[0].message.content)
```

**Option B — register as a managed skill**:

If your Codex setup supports skill registries, register:

- **name**: `mobile-design-skill`
- **entrypoint**: `SKILL.md`
- **metadata**: `skill/metadata.yaml`
- **UI descriptor**: `agents/openai.yaml`

Keep these files loaded alongside the active prompt for full skill behavior:

- `skill/modes.md`
- `skill/templates.md`
- `docs/workflow.md`
- `docs/clarification-policy.md`
- `docs/judged-mode.md`
- `docs/principles.md`
- `docs/guardrails.md`
- `docs/sources.md`
- `docs/quality-bars.md`
- `docs/motion-system.md`
- `docs/context-defaults.md`
- `docs/heuristics.md`
- `docs/patterns-catalog.md`
- `docs/adaptive-layout.md`
- `docs/design-quality.md`
- `docs/design-quality-rubric.md`
- `docs/golden-examples.md`
- `docs/synthetic-case-studies.md`
- `docs/domain-packs/index.md`
- `docs/weaknesses.md`
- `docs/inspiration-sources.md`
- `docs/visual-benchmark-playbooks.md`
- `docs/benchmark-report-format.md`
- `docs/visual-review-fixtures.md`
- `docs/rendered-output-qa.md`
- `docs/self-review.md`

---

### Claude API (Python)

Direct Claude API integration using the `anthropic` SDK:

```bash
pip install anthropic
git clone https://github.com/evgeniyvorobey/mobile-design-skill.git
```

```python
import anthropic
from pathlib import Path

SKILL_ROOT = Path("mobile-design-skill")
system_prompt = (SKILL_ROOT / "SKILL.md").read_text()

# Optionally inline the expanded reference set for deeper behavior:
for ref in ["skill/modes.md", "skill/templates.md", "docs/workflow.md",
            "docs/clarification-policy.md", "docs/judged-mode.md",
            "docs/principles.md", "docs/guardrails.md",
            "docs/sources.md", "docs/quality-bars.md", "docs/motion-system.md",
            "docs/context-defaults.md", "docs/heuristics.md",
            "docs/patterns-catalog.md", "docs/adaptive-layout.md",
            "docs/design-quality.md",
            "docs/design-quality-rubric.md", "docs/golden-examples.md",
            "docs/synthetic-case-studies.md", "docs/domain-packs/index.md",
            "docs/weaknesses.md", "docs/inspiration-sources.md",
            "docs/visual-benchmark-playbooks.md", "docs/benchmark-report-format.md",
            "docs/visual-review-fixtures.md", "docs/rendered-output-qa.md",
            "docs/self-review.md"]:
    system_prompt += f"\n\n# {ref}\n\n" + (SKILL_ROOT / ref).read_text()

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4000,
    system=system_prompt,
    messages=[{
        "role": "user",
        "content": "Create a platform-aware UI spec for a medication refill screen. "
                   "Audience: older adults. Cross-platform. Accessibility-sensitive."
    }],
)
print(response.content[0].text)
```

For production, use prompt caching on the system prompt (it rarely changes):

```python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4000,
    system=[{
        "type": "text",
        "text": system_prompt,
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{"role": "user", "content": "..."}],
)
```

---

### Claude API (TypeScript)

```bash
npm install @anthropic-ai/sdk
git clone https://github.com/evgeniyvorobey/mobile-design-skill.git
```

```ts
import Anthropic from "@anthropic-ai/sdk";
import { readFileSync } from "node:fs";
import { join } from "node:path";

const SKILL_ROOT = "./mobile-design-skill";
const read = (p: string) => readFileSync(join(SKILL_ROOT, p), "utf8");

let systemPrompt = read("SKILL.md");
for (const ref of [
  "skill/modes.md",
  "skill/templates.md",
  "docs/workflow.md",
  "docs/clarification-policy.md",
  "docs/judged-mode.md",
  "docs/principles.md",
  "docs/guardrails.md",
  "docs/sources.md",
  "docs/quality-bars.md",
  "docs/context-defaults.md",
  "docs/heuristics.md",
  "docs/patterns-catalog.md",
  "docs/adaptive-layout.md",
  "docs/design-quality.md",
  "docs/design-quality-rubric.md",
  "docs/golden-examples.md",
  "docs/synthetic-case-studies.md",
  "docs/domain-packs/index.md",
  "docs/weaknesses.md",
  "docs/inspiration-sources.md",
  "docs/visual-benchmark-playbooks.md",
  "docs/benchmark-report-format.md",
  "docs/visual-review-fixtures.md",
  "docs/rendered-output-qa.md",
  "docs/self-review.md",
]) {
  systemPrompt += `\n\n# ${ref}\n\n` + read(ref);
}

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 4000,
  system: [{ type: "text", text: systemPrompt, cache_control: { type: "ephemeral" } }],
  messages: [{
    role: "user",
    content: "Review this Android settings screen for usability and accessibility.",
  }],
});

console.log(response.content[0].type === "text" ? response.content[0].text : "");
```

---

### Cursor and other IDEs

Any editor that supports a system prompt, rules file, or AI-instruction attachment can use this skill.

**Cursor** — save `SKILL.md` as a rule:

```bash
mkdir -p ~/your-project/.cursor/rules
cp mobile-design-skill/SKILL.md ~/your-project/.cursor/rules/mobile-design-skill.mdc
```

**Continue.dev** — add to your `~/.continue/config.json` context:

```json
{
  "contextProviders": [
    {
      "name": "file",
      "params": { "path": "/path/to/mobile-design-skill/SKILL.md" }
    }
  ]
}
```

**Generic** — paste the contents of `SKILL.md` as the system prompt or "custom instructions" of any AI tool you use.

---

## Usage

Invocation patterns once installed:

### In Claude Code

```text
/mobile-design-skill                                    # the skill will ask for a task
/mobile-design-skill --judge create a fitness tracker dashboard, cross-platform
/mobile-design-skill generate a home screen for a fitness app, iOS, general audience
/mobile-design-skill review my checkout form, Android, older users, description only
/mobile-design-skill design a user flow for password reset with email verification
/mobile-design-skill create a UI spec for a medication refill screen, cross-platform
/mobile-design-skill create a typography system for a finance app
/mobile-design-skill prepare a handoff rationale for the attached checkout redesign
```

### In Codex / API

Prepend `Use the mobile-design-skill.` to your user message, then describe the task:

```text
Use the mobile-design-skill.

Create a platform-aware UI spec for a medication refill screen in a cross-platform
healthcare app.

Audience: older adults
Primary goal: request refill quickly and safely
Constraints: accessibility-sensitive, high trust, existing design system, dense medical content
```

### Minimal context is fine

If the task description is short, the skill will state its assumptions, narrow the scope, and surface the information it needs next. See [`examples/anti-patterns.md`](examples/anti-patterns.md) for how it handles underspecified input.

If missing information would materially change the recommendation, the skill asks up to three blocking clarifying questions and offers a fast path when a provisional draft is still useful. See [`docs/clarification-policy.md`](docs/clarification-policy.md) and [`examples/clarification-policy.md`](examples/clarification-policy.md).

### Judged mode

Use `--judge` when you want a second rubric pass in the same interactive session:

```text
/mobile-design-skill --judge create a platform-aware UI spec for a fitness tracker app, cross-platform
```

The skill drafts privately, asks an independent judge agent when the host supports subagents, revises any dimension the judge leaves short of a question the input can answer, and returns the final answer with a compact `Judge summary`. See [`docs/judged-mode.md`](docs/judged-mode.md).

---

## Supported modes

Every request is classified into exactly one primary mode:

| # | Mode | Use when |
|---|------|----------|
| 1 | **Generate mobile screen concept** | You need a first-pass concept with structure, hierarchy, components, and states. |
| 2 | **Design mobile user flow** | You need ordered steps, decision points, back-navigation logic, and recovery paths. |
| 3 | **Create platform-aware UI spec** | You need an implementation-ready structure with states, behaviors, spacing, typography. |
| 4 | **Review screen for usability/accessibility** | You have a screen and need critique with severity-tiered issues and fixes. Sub-cases D1–D4 handle visual vs description-only vs problem-statement vs context-change reviews. |
| 5 | **Create typography and spacing system** | You need type roles, size hierarchy, line-height, spacing scale, density rules, touch implications. |
| 6 | **Prepare design rationale / handoff** | You need a rationale and handoff package with decisions, tradeoffs, validation plan. |

Full mode definitions, required/optional inputs, validation checklists, and fallback behavior: [`skill/modes.md`](skill/modes.md).

Output skeletons per mode: [`skill/templates.md`](skill/templates.md).

---

## Architecture

```text
mobile-design-skill/
├── SKILL.md                              Canonical entrypoint (Codex + Claude API)
├── README.md                             This file
├── CHANGELOG.md                          Release history (semver)
├── LICENSE                               MIT
├── .claude/
│   ├── agents/
│   │   └── mobile-design-judge.md        Companion Claude Code agent for /mobile-design-skill --judge
│   └── skills/
│       └── mobile-design-skill/
│           ├── SKILL.md                  Claude Code wrapper for /mobile-design-skill
│           └── logo.svg                  Skill wrapper icon
├── agents/
│   └── openai.yaml                       Codex UI metadata
├── assets/
│   ├── logo-light.svg                    Project logo — light theme variant
│   └── logo-dark.svg                     Project logo — dark theme variant
├── .github/
│   └── workflows/
│       ├── validate.yml                  CI: structure + link validation
│       └── release-validate.yml          Manual release validation
├── scripts/
│   ├── install.sh                        Install script (symlink or copy)
│   ├── bump_version.py                   Version bumper (synchronizes all version references)
│   ├── validate_repo.py                  Repository structure, docs hygiene, link, and example-response validator
│   ├── validate_release.py               Release validation and version/tag sanity checks
│   ├── verify_install.py                 Installs into a throwaway dir and checks every reference resolves
│   ├── rubric_judge_oracle_agent.py      Deterministic stdin/stdout agent for judge-command CI self-tests
│   ├── paired_eval_oracle_agent.py       Deterministic stand-in judge that proves the paired-eval adapter
│   ├── generation_oracle_agent.py        Deterministic stand-in generator that proves the generation-eval adapter
│   ├── run_paired_eval.py                Forced-choice paired comparison of two arms, with a mandatory null-pair control
│   ├── run_generation_eval.py            Scores what the skill generates against the committed-example contract
│   ├── run_diversity_eval.py             Decision-vector spread across generated responses — measures sameness
│   └── run_rubric_judge.py               Provider-agnostic LLM-as-judge runner and external-agent adapter
├── skill/
│   ├── modes.md                          Per-mode inputs, outputs, validation, fallback
│   ├── templates.md                      Output skeletons for each mode
│   ├── usage.md                          Usage guide
│   └── metadata.yaml                     Machine-readable skill metadata
├── docs/
│   ├── workflow.md                       11-step internal workflow
│   ├── clarification-policy.md           Ask-vs-assume rules for underspecified input
│   ├── judged-mode.md                    /mobile-design-skill --judge orchestration rules
│   ├── principles.md                     11 design principles
│   ├── guardrails.md                     Hard constraints (do not invent, do not claim compliance, etc.)
│   ├── sources.md                        Source hierarchy (Apple HIG, Material 3, WCAG, ISO, GOV.UK)
│   ├── quality-bars.md                   Concrete numeric thresholds
│   ├── motion-system.md                  Named platform curves and springs, duration scaling, stagger caps
│   ├── design-quality.md                 Visual hierarchy, composition, density, and craft calibration
│   ├── design-quality-rubric.md          1-5 design quality scoring and improvement ladder
│   ├── paired-comparison.md              Which of two designs is better: the instrument the rubric's boundary questions cannot be
│   ├── golden-examples.md                Golden example index and calibration guide
│   ├── synthetic-case-studies.md         Synthetic bad-to-good case-study index
│   ├── visual-review-fixtures.md         Text-only visual review fixture index
│   ├── benchmark-report-format.md        3-5 reference benchmark report template
│   ├── rendered-output-qa.md             Optional post-implementation rendered QA workflow
│   ├── weaknesses.md                     Known failure modes and prevention checks
│   ├── context-defaults.md               Audience / domain / platform / use-context defaults
│   ├── domain-packs/
│   │   ├── index.md                      Domain pack index
│   │   ├── fintech.md                    Fintech mobile design playbook
│   │   ├── health.md                     Health mobile design playbook
│   │   ├── saas.md                       Enterprise SaaS mobile design playbook
│   │   ├── marketplace.md                Marketplace mobile design playbook
│   │   ├── social.md                     Social mobile design playbook
│   │   └── education.md                  Education mobile design playbook
│   ├── heuristics.md                     Fitts, Hick, Jakob, Zeigarnik, Nielsen, Gestalt — with mobile applications
│   ├── patterns-catalog.md               Mobile pattern decision matrices
│   ├── adaptive-layout.md                Tablet, foldable, and adaptive layout: width classes and canonical layouts
│   ├── inspiration-sources.md            Non-authoritative inspiration and reference layer
│   ├── visual-benchmark-playbooks.md     Mobbin, Page Flows, Apple Design Awards, Awwwards benchmark playbooks
│   ├── llm-judge-runner.md               JSONL contract for semantic rubric judge runs
│   ├── release-automation.md             Release validation workflow and local command
│   ├── self-review.md                    Mandatory pre-response quality pass
│   ├── evals.md                          Structural + content + fail-condition evaluation criteria
│   ├── versioning.md                     Semver policy
│   ├── commands.md                       Invocation reference
│   └── github-publishing.md              Publishing kit
└── examples/
    ├── generate-screen.md                Worked example for Mode 1
    ├── clarification-policy.md           Ask-vs-assume examples for blocking and non-blocking gaps
    ├── design-flow.md                    Worked example for Mode 2
    ├── ui-spec.md                        Worked example for Mode 3
    ├── review-screen.md                  Worked example for Mode 4
    ├── typography-spacing.md             Worked example for Mode 5
    ├── rationale-handoff.md              Worked example for Mode 6
    ├── rubric-before-after.md            2/5 → 4/5 rubric upgrade example
    ├── anti-patterns.md                  Bad/Good pairs — how the skill should behave under ambiguous input
    ├── benchmark-report.md               Synthetic benchmark report example
    ├── case-studies/                     Synthetic bad-to-good calibration cases
    │   ├── fintech-account-overview.md
    │   ├── health-medication-refill.md
    │   ├── saas-approval-queue.md
    │   ├── marketplace-checkout-substitution.md
    │   ├── social-privacy-settings.md
    │   ├── education-lesson-progress.md
    │   ├── onboarding-permissions.md
    │   ├── settings-consent-destructive-action.md
    │   ├── search-results-filtering.md
    │   ├── empty-error-state-recovery.md
    │   ├── typography-spacing-system.md
    │   └── rationale-handoff.md
    ├── golden/                           Compact taste/domain calibration examples
    │   ├── premium-ui.md                 Premium UI calibration
    │   ├── enterprise-saas.md            Enterprise SaaS calibration
    │   ├── fintech.md                    Fintech calibration
    │   ├── health.md                     Health calibration
    │   ├── onboarding.md                 Onboarding calibration
    │   ├── settings.md                   Settings calibration
    │   ├── checkout.md                   Checkout calibration
    │   └── tablet-list-detail.md         Tablet list-detail calibration
    ├── visual-review-fixtures/           Figma-like text review fixtures
    │   ├── fintech-dashboard-dense-summary.md
    │   ├── health-appointment-booking.md
    │   ├── enterprise-saas-mobile-table-card-list.md
    │   ├── marketplace-product-detail-checkout-edge.md
    │   ├── social-profile-privacy-control.md
    │   ├── education-quiz-results.md
    │   └── ipad-team-inbox-stretched-phone.md
    ├── rendered-output-qa/
    │   ├── report-schema.json            Optional rendered QA report schema
    │   └── sample-report.json            Example rendered QA report
    └── evals/
        ├── rubric-score-1.json                       Rubric fixture: broken or misleading
        ├── rubric-score-2.json                       Rubric fixture: structurally weak
        ├── rubric-score-2-adversarial.json           Rubric fixture: complete template, weak specification
        ├── rubric-score-3.json                       Rubric fixture: acceptable baseline
        ├── rubric-score-3-contradicted-value.json    Rubric fixture: baseline clamped by a contradicted value
        ├── rubric-score-3-visual-rules-state-gap.json  Rubric fixture: visual rules stated, states missing
        ├── rubric-score-4.json                       Rubric fixture: strong and shippable
        ├── rubric-score-5.json                       Rubric fixture: excellent and resilient
        ├── generation-prompts.json                   Prompt pack for the generation eval
        ├── diversity-fixtures.json                   Uniform/varied corpora the diversity self-test must separate
        └── paired-comparison-fixtures.json           Separating, null, and broken-control arms for the paired eval
```

---

## Updating

The skill is a git repository. Updates are pulled like any other repo:

```bash
cd ~/mobile-design-skill
git pull
```

If the install uses the default symlink method, the new version is active immediately — no reinstall needed.

If the install uses `--method copy`, re-run the install script to sync the copy:

```bash
./scripts/install.sh --method copy
# or for a project-local install
./scripts/install.sh --method copy --scope project --project-path /path/to/project
```

Check your installed version:

```bash
python3 scripts/bump_version.py --show
```

Compare to the latest release on [GitHub](https://github.com/evgeniyvorobey/mobile-design-skill/releases).

---

## Uninstalling

```bash
# Global uninstall
./scripts/install.sh --uninstall

# Project-local uninstall
./scripts/install.sh --uninstall --scope project --project-path /path/to/project

# Manual removal
rm ~/.claude/skills/mobile-design-skill
```

Then you can delete the cloned repo if no longer needed:

```bash
rm -rf ~/mobile-design-skill
```

---

## Customization

Fork the repository, edit the files that govern skill behavior, and run the install script against your fork. Files most commonly customized:

- [`docs/context-defaults.md`](docs/context-defaults.md) — add domain-specific defaults for your product
- [`docs/clarification-policy.md`](docs/clarification-policy.md) — tune when the skill asks questions vs proceeds with assumptions
- [`docs/judged-mode.md`](docs/judged-mode.md) — tune `/mobile-design-skill --judge` orchestration and fallback behavior
- [`docs/quality-bars.md`](docs/quality-bars.md) — tighten numeric thresholds for your design system
- [`docs/design-quality.md`](docs/design-quality.md) — tune design-quality calibration for hierarchy, rhythm, visual craft, and production readiness
- [`docs/design-quality-rubric.md`](docs/design-quality-rubric.md) — tune 1-5 design-quality scoring, caps, and improvement ladder
- [`docs/paired-comparison.md`](docs/paired-comparison.md) — compare two arms of output; the pre/post instrument for an instruction-text change
- [`docs/golden-examples.md`](docs/golden-examples.md) — tune compact taste and domain calibration examples
- [`docs/synthetic-case-studies.md`](docs/synthetic-case-studies.md) — tune synthetic bad-to-good calibration cases
- [`docs/domain-packs/index.md`](docs/domain-packs/index.md) — tune domain-specific mobile playbooks
- [`docs/benchmark-report-format.md`](docs/benchmark-report-format.md) — tune benchmark report structure for 3-5 references
- [`docs/visual-review-fixtures.md`](docs/visual-review-fixtures.md) — tune text-only review calibration fixtures
- [`docs/rendered-output-qa.md`](docs/rendered-output-qa.md) — tune optional post-implementation QA workflow
- [`docs/weaknesses.md`](docs/weaknesses.md) — tune known weakness patterns and prevention checks for recurring output regressions
- [`docs/llm-judge-runner.md`](docs/llm-judge-runner.md) — tune semantic judge runner contract and pass criteria
- [`docs/patterns-catalog.md`](docs/patterns-catalog.md) — add patterns unique to your product area
- [`docs/adaptive-layout.md`](docs/adaptive-layout.md) — tune width classes, canonical layouts, and the device-class signal list
- [`docs/inspiration-sources.md`](docs/inspiration-sources.md) — tune visual inspiration, production reference, and moodboard sources
- [`docs/visual-benchmark-playbooks.md`](docs/visual-benchmark-playbooks.md) — tune source-specific benchmark checklists
- [`skill/templates.md`](skill/templates.md) — adjust output structure for your team's handoff format
- [`docs/guardrails.md`](docs/guardrails.md) — add organization-specific constraints

After editing:

```bash
python3 scripts/validate_repo.py             # check structure, docs hygiene, links, and example outputs
python3 scripts/validate_release.py          # run deterministic release checks
python3 scripts/bump_version.py minor        # bump version
# write the CHANGELOG entry, then rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`
git commit -am "customize for <product>"
```

---

## Versioning

This project uses [Semantic Versioning 2.0.0](https://semver.org/) with policy adapted for a prompt-and-documentation skill. See [`docs/versioning.md`](docs/versioning.md) for the full bump rules.

| Bump | Reason |
|------|--------|
| MAJOR | Breaking contract change (mode removed, output format changes, SKILL.md schema breaks) |
| MINOR | Additive enhancement (new guardrail, new document, new sub-case, new quality bar) |
| PATCH | Non-behavioral fix (typo, link repair, script fix, docs polish) |

Version is stored in `skill/metadata.yaml` (canonical), mirrored into `SKILL.md` frontmatters and the README badge. Use `scripts/bump_version.py` to keep them in sync.

---

## Contributing

Contributions are welcome via pull request. Before submitting:

1. Run `python3 scripts/validate_repo.py` — must print `[OK] Repository structure, documentation hygiene, relative links, and example responses are valid.`
2. Run `python3 scripts/validate_release.py` before tagging a release.
3. If you added a new document under `docs/`, add it to `REQUIRED_FILES` in `scripts/validate_repo.py` and to the skill's SKILL.md reference list when it affects runtime behavior.
4. If you changed the mode set or output contract, bump MAJOR.
5. If you added a new capability, bump MINOR and fill in the CHANGELOG.
6. If you only touched docs or scripts, bump PATCH.
7. Keep PRs focused — one logical change per PR.

---

## Source hierarchy

The skill uses this source priority for any claim or recommendation:

1. Official platform guidance and standards — **Apple Human Interface Guidelines**, **Material Design 3**, **Android Navigation guidance**
2. Accessibility and usability standards — **WCAG 2.2**, **W3C Mobile**, **ISO 9241-210**, **ISO 9241-11**
3. Public-sector and enterprise-grade design systems — **GOV.UK Design System**, **NHS Design System**, **Fluent 2**
4. Established research and case-study sources
5. Workflow and tooling references — **Figma Variables**, platform implementation guides

Full list with canonical URLs: [`docs/sources.md`](docs/sources.md).

### Source provenance

The canonical URL appendix in [`docs/sources.md`](docs/sources.md) was consolidated from an external curation document used during repository preparation:

- `Design thinking.pdf` (`Curated Learning Map for Mobile UI/UX Design Using US and European Sources`)

The PDF itself is not bundled; the normalized public URLs and grouped source map are preserved in the repo.

### Screenshots

Screenshots are intentionally not bundled. The repository uses worked examples instead — each of the six modes has a corresponding file in [`examples/`](examples). These double as regression targets.

---

## License

MIT — see [`LICENSE`](LICENSE).
