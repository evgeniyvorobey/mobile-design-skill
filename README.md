<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo-light.svg" alt="Mobile Design Skill" width="640">
  </picture>
</p>

<p align="center">
  <img alt="version" src="https://img.shields.io/badge/version-2.1.0-blue">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-green">
</p>

# Mobile App Design Skill

A short set of instructions for mobile UI/UX design work on iOS, Android, and cross-platform products: screen concepts, flows, UI specs, reviews, type and spacing systems, rationale and handoff.

Works as a Claude Code skill (native slash invocation), as a Codex / OpenAI skill, and as a system prompt for direct Claude API or any LLM integration.

**What it is measured to do.** Against the same model (Opus 5.5), judged blind in both orders, every arm generated in one batch. The record is in [`docs/proposals/skill-vs-baseline.md`](docs/proposals/skill-vs-baseline.md).

- **Against no skill, on sixteen briefs nobody had read** (2026-10-04, effort `xhigh`): all 16 pairs to the skill. No medium or high error in the skill's sixteen answers against 2 with no skill, and 7 errors of any severity against 10. The skill's answers are 2.9 times as long (3,700 words against 1,300) and take 3.3 times as long, 11.7 minutes against 3.6. A comparison across that much length is not controlled for depth; the next one is.
- **Against no skill plus one sentence asking for a thorough, decided answer, on the same briefs, at about equal length**: 14 pairs to the skill, none to the sentence, 2 tied (both reviews). No medium or high error against 5, and 7 errors of any severity against 30. The skill takes 1.9 times as long as the sentence, 11.7 minutes against 6.2.
- **A caveat on the error count.** Three of the skill's seven low errors are the same defect, a screen locked to portrait, and other auditors rated that defect medium in each of the other two arms. Rated alike everywhere, the count against no skill would be 3 against 2 or 0 against 1.
- **What this does not cover.** One draw per brief. Judges, auditors and the writers of the briefs are the same model family as the skill's author. Effort `xhigh` only: at `max` the previous text (2.0.0) tied the same one-sentence request, 3 / 2 / 3 on eight briefs, and this text has not been run there. Nothing is measured on a weaker model.

Earlier results, and the time figure corrected in 2.0.1, are in [`CHANGELOG.md`](CHANGELOG.md).

Current version: **2.1.0** — see [`CHANGELOG.md`](CHANGELOG.md) and [`docs/versioning.md`](docs/versioning.md).

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
- [What you can ask for](#what-you-can-ask-for)
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

The entrypoint is [`SKILL.md`](SKILL.md), about 70 lines, plus one page of dated platform facts. It prescribes no output format. It changes how the model answers in five ways:

- **Job first.** Before any layout: who opens this, at what moment, to get which one to three things done. Then six tests that the primary job is finished on the screen and not only reported: act where it is shown, show the answer and not its inputs, design the peak moment, follow the fork, design the whole product and not its outline, give each use its own treatment.
- **Decide everything.** Structure, behaviour, exact copy, sizes, colours as values, typefaces by name, and the product rules the request left open. No placeholders and no decisions handed back as open questions. Proposals are the work; facts (research results, platform rules, compliance, your existing product) are never invented.
- **Thorough, to build from.** The answer covers the states and the edge cases and leaves no open questions, around three thousand words for a screen, a flow, a spec or a system. It opens with the two or three decisions that set the design apart and a mockup with real content. No mode labels, no scores nobody asked for, no account of process.
- **Floors and facts, checked after the design exists.** States and failure paths, accessibility minimums, and platform facts from [`skill/platform.md`](skill/platform.md): Liquid Glass, Material 3 Expressive, Android 16, width classes, foldables, the iOS 26 back swipe, the screen before a permission alert, the accuracy of approximate location, each with the date it was checked.
- **One read for contradictions before sending.** A number that differs between the mockup and the table, a rule its own example breaks, an "always" or a "never" that the design itself breaks. This is the most common defect of a long design answer, and where the measured difference in errors comes from.

Loaded only when you ask for it: several visual directions drawn from a catalogue of schools and products, a 1-5 design-quality score with its rubric, an independent judge pass (`--judge`), benchmark reports, and QA of a built screen. Behind those sits a reference library (pattern decision tables, numeric bars, heuristics, domain playbooks, calibration examples) that nothing loads by default.

What changed from 1.x: the six modes, the output contract, the mandatory three directions, the self-scores and the long mandatory self-review are gone from the default answer. They made answers thinner and longer than the model's own.

What changed from 2.0: the lists of what each kind of request needs, most of the lists of floors, the rule sizing the answer to the request and the rule for asking questions are gone, and the text is 1,570 words where it was 2,367. Set against 2.0.0 directly on sixteen working briefs, the shorter text took 11 pairs to 2 with 3 tied, at the same cost.

See [`docs/`](docs) for the reference library and [`docs/evals.md`](docs/evals.md) for how the skill is evaluated.

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

This creates `~/.claude/skills/mobile-design-skill` holding a generated wrapper whose references are absolute paths into the cloned repo, so the skill is available globally in every Claude Code session and `git pull` updates its content. (It is deliberately not a symlink to the repo's wrapper: Claude Code passes the skill its unresolved directory and resolves `..` textually, so a symlinked wrapper's relative references point outside the repo and nothing loads.)

**Alternatives**:

```bash
# Install only inside one project (not global): pass the project explicitly...
./scripts/install.sh --scope project --project-path /absolute/path/to/project

# ...or run the script from inside that project
cd /absolute/path/to/project && ~/mobile-design-skill/scripts/install.sh --scope project

# Use a self-contained copy instead of a live install (for filesystems without symlink support)
./scripts/install.sh --method copy

# Check where the skill is installed
./scripts/install.sh --status

# Remove the install
./scripts/install.sh --uninstall
./scripts/install.sh --uninstall --scope project --project-path /absolute/path/to/project
```

`install.sh` refuses any target that is the clone itself or inside it, and `--uninstall` only removes what the script created.

**Verify**:

```bash
./scripts/install.sh --status
```

Output should show `link install from /path/to/mobile-design-skill` for your chosen scope.

Open Claude Code and try:

```text
/mobile-design-skill
```

---

### Claude Code — manual

If you prefer to bypass the install script:

```bash
# Global install (any Claude Code session): a real directory, with the wrapper's
# `${CLAUDE_SKILL_DIR}/../../../` prefix replaced by the clone's absolute path
REPO=/absolute/path/to/mobile-design-skill
mkdir -p ~/.claude/skills/mobile-design-skill
sed -e "s|\${CLAUDE_SKILL_DIR}/\.\./\.\./\.\./|$REPO/|g" \
    "$REPO/.claude/skills/mobile-design-skill/SKILL.md" > ~/.claude/skills/mobile-design-skill/SKILL.md
```

Do not symlink the wrapper directory: the host resolves `${CLAUDE_SKILL_DIR}/../../../` textually from the symlink's own location, so every reference misses the repo.

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

Keep one more file loaded alongside the active prompt: `skill/platform.md`, the dated platform facts `SKILL.md` tells the model to read. Everything under `docs/` is loaded only when a user asks for what it covers; `SKILL.md` section 5 lists those files.

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

# SKILL.md tells the model to read skill/platform.md for platform facts; with no
# file access, inline it. Nothing else is needed for an ordinary request.
system_prompt += "\n\n# skill/platform.md\n\n" + (SKILL_ROOT / "skill/platform.md").read_text()

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
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
    model="claude-opus-5-5",
    max_tokens=16000,
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

// SKILL.md tells the model to read skill/platform.md for platform facts; with no
// file access, inline it. Nothing else is needed for an ordinary request.
const systemPrompt = read("SKILL.md") + "\n\n# skill/platform.md\n\n" + read("skill/platform.md");

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-5-5",
  max_tokens: 16000,
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

If the task description is short, the skill does not ask a questionnaire. It decides what a good product would do and designs to that. Where something needs your yes or no, it gives its recommended answer and designs to it, and if the request can be read two ways it says in the first lines which reading it took.

The answer is thorough by default, around three thousand words for a screen, a flow, a spec or a system. Say so when you want something shorter.

### Judged mode

Use `--judge` when you want a second rubric pass in the same interactive session:

```text
/mobile-design-skill --judge create a platform-aware UI spec for a fitness tracker app, cross-platform
```

The skill drafts privately, asks an independent judge agent when the host supports subagents, revises any dimension the judge leaves short of a question the input can answer, and returns the final answer with a compact `Judge summary`. See [`docs/judged-mode.md`](docs/judged-mode.md).

---

## What you can ask for

The skill no longer classifies a request into a mode or prints a mode label. These are the kinds of work it is written for, and what each answer leads with.

| Ask for | The answer leads with |
|---|---|
| **A screen concept** | The screen's job, the two or three decisions that set it apart, and a text mockup with real content |
| **A user flow** | The map of steps and branches, then each step with its copy, Back behaviour and recovery |
| **A UI spec** | The decisions it rests on, wireframes, components with sizes and behaviour, a state table, tokens, acceptance checks |
| **A review** | What the material lets it judge, what already works, findings in order of impact as cause and fix, a before and after mockup |
| **A type and spacing system** | The rules behind the numbers, named typefaces, tokens per context of use mapped to platform text styles |
| **Rationale and handoff** | What changed and why, proposed behaviour where the design is silent, anatomy, states, data, QA checklist |

Anything else (paywall architecture, notification strategy, information architecture, a teardown) is answered as what it is.

On request only, and loaded only then: several visual directions or references ([`docs/inspiration-sources.md`](docs/inspiration-sources.md)), a 1-5 score ([`docs/design-quality-rubric.md`](docs/design-quality-rubric.md)), an independent judge pass ([`docs/judged-mode.md`](docs/judged-mode.md)), a benchmark of references ([`docs/benchmark-report-format.md`](docs/benchmark-report-format.md)), and QA of a built screen ([`docs/rendered-output-qa.md`](docs/rendered-output-qa.md)).

---

## Architecture

```text
mobile-design-skill/
├── SKILL.md                              Canonical entrypoint: the whole default behaviour, about 70 lines
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
│   ├── install.sh                        Install script (live link or copy)
│   ├── bump_version.py                   Version bumper (synchronizes all version references)
│   ├── validate_repo.py                  Repository structure, docs hygiene and link validator
│   ├── validate_release.py               Release validation and version/tag sanity checks
│   ├── verify_install.py                 Installs into a throwaway dir and checks every reference resolves
│   ├── rubric_judge_oracle_agent.py      Deterministic stdin/stdout agent for judge-command CI self-tests
│   ├── paired_eval_oracle_agent.py       Deterministic stand-in judge that proves the paired-eval adapter
│   ├── run_paired_eval.py                Forced-choice paired comparison of two arms, with a mandatory null-pair control
│   ├── run_baseline_gate.py              Release gate: the skill against the same model with no skill
│   └── run_rubric_judge.py               Provider-agnostic LLM-as-judge runner and external-agent adapter
├── skill/
│   ├── platform.md                       Dated platform facts, the one file SKILL.md has the model read
│   └── metadata.yaml                     Machine-readable skill metadata
├── docs/
│   ├── judged-mode.md                    /mobile-design-skill --judge orchestration rules (on request)
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
│   ├── evals.md                          What the repository evaluates, and with which instrument
│   ├── versioning.md                     Semver policy
│   ├── commands.md                       Invocation reference
│   └── github-publishing.md              Publishing kit
└── examples/
    ├── rubric-before-after.md            2/5 → 4/5 rubric upgrade example
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
        ├── generation-prompts.json                   Ten ordinary requests: the second half of the gate's extended set
        ├── paired-comparison-fixtures.json           Separating, null, and broken-control arms for the paired eval
        ├── baseline-gate-briefs.json                 Brief sets for the release gate (skill versus no skill)
        ├── baseline-gate-heldout.json                Sixteen held-out briefs for the release gate, opened on 2026-10-04
        └── baseline-gate-heldout-2026-10-03.json     The eight held-out briefs opened on 2026-10-03
```

---

## Updating

The skill is a git repository. Updates are pulled like any other repo:

```bash
cd ~/mobile-design-skill
git pull
```

If the install uses the default link method, the new content is active immediately. Re-run `./scripts/install.sh` only when the pull changed `.claude/skills/mobile-design-skill/SKILL.md` or the judge agent, or after moving the clone.

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
rm -r ~/.claude/skills/mobile-design-skill
```

Then you can delete the cloned repo if no longer needed:

```bash
rm -rf ~/mobile-design-skill
```

---

## Customization

Fork the repository, edit, and run the install script against your fork.

What the model reads for an ordinary request, and therefore what changes its answers:

- [`SKILL.md`](SKILL.md): the whole default behaviour. Add your product's rules here, in as few words as you can
- [`skill/platform.md`](skill/platform.md): dated platform facts. Add the facts of your own design system or minimum OS versions

What it reads only on request:

- [`docs/inspiration-sources.md`](docs/inspiration-sources.md) and [`docs/visual-benchmark-playbooks.md`](docs/visual-benchmark-playbooks.md): visual directions, references and benchmark checklists
- [`docs/design-quality-rubric.md`](docs/design-quality-rubric.md) and [`docs/judged-mode.md`](docs/judged-mode.md): the 1-5 score and the `--judge` pass
- [`docs/benchmark-report-format.md`](docs/benchmark-report-format.md) and [`docs/rendered-output-qa.md`](docs/rendered-output-qa.md): benchmark reports and QA of a built screen
- [`docs/quality-bars.md`](docs/quality-bars.md), [`docs/patterns-catalog.md`](docs/patterns-catalog.md) and [`docs/motion-system.md`](docs/motion-system.md): the long form of the thresholds, pattern decision tables and named motion curves

The reference library behind those, which nothing loads by default: [`docs/adaptive-layout.md`](docs/adaptive-layout.md), [`docs/context-defaults.md`](docs/context-defaults.md), [`docs/design-quality.md`](docs/design-quality.md), [`docs/golden-examples.md`](docs/golden-examples.md), [`docs/synthetic-case-studies.md`](docs/synthetic-case-studies.md), [`docs/domain-packs/index.md`](docs/domain-packs/index.md), [`docs/visual-review-fixtures.md`](docs/visual-review-fixtures.md), [`docs/weaknesses.md`](docs/weaknesses.md), [`docs/guardrails.md`](docs/guardrails.md), [`docs/llm-judge-runner.md`](docs/llm-judge-runner.md).

A change to `SKILL.md` or `skill/platform.md` changes what the skill produces. Judge it with the release gate in [`docs/paired-comparison.md`](docs/paired-comparison.md), not with the validators below: they check that files and links are in order and say nothing about whether an answer is good.

After editing:

```bash
python3 scripts/validate_repo.py             # check structure, docs hygiene and links
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
| MAJOR | Breaking contract change (what the default answer contains, the invocation syntax, the SKILL.md schema) |
| MINOR | Additive enhancement (new guardrail, new document, new sub-case, new quality bar) |
| PATCH | Non-behavioral fix (typo, link repair, script fix, docs polish) |

Version is stored in `skill/metadata.yaml` (canonical), mirrored into `SKILL.md` frontmatters and the README badge. Use `scripts/bump_version.py` to keep them in sync.

---

## Contributing

Contributions are welcome via pull request. Before submitting:

1. Run `python3 scripts/validate_repo.py` — must print `[OK] Repository structure, documentation hygiene and relative links are valid.`
2. Run `python3 scripts/validate_release.py` before tagging a release.
3. If you added a new document under `docs/`, add it to `REQUIRED_FILES` in `scripts/validate_repo.py`, and either offer it on request in `SKILL.md` section 5 or list it in `SKILL_ENTRYPOINT_DOC_EXCLUSIONS` with the reason the model does not load it.
4. If you changed what the model reads at runtime (`SKILL.md`, `skill/platform.md`, or a document `SKILL.md` points to), run the release gate and record its result in the CHANGELOG entry.
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

Screenshots are intentionally not bundled. [`examples/`](examples) holds calibration material for the rubric and the judge, not sample answers: the 1.x worked examples followed an output format the skill no longer has, and were removed with it.

---

## License

MIT — see [`LICENSE`](LICENSE).
