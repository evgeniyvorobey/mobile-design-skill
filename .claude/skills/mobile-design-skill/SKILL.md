---
name: mobile-design-skill
description: Generate, review, and structure mobile UI/UX decisions for iOS, Android, and cross-platform products. Use when you want to invoke the mobile design workflow directly in Claude Code with /mobile-design-skill.
argument-hint: "[--judge] [task / screen / flow]"
disable-model-invocation: true
version: 1.36.0
---

# Mobile Design Skill

Use the repository's canonical mobile design skill for this request.

When invoked:

1. Read `${CLAUDE_SKILL_DIR}/../../../SKILL.md` first. That file is the canonical skill entrypoint and contains the core workflow.
2. Read supporting files only as needed. This list mirrors the canonical `SKILL.md` reference
   list in the same order; `scripts/validate_repo.py` fails if the two drift apart.
   - `${CLAUDE_SKILL_DIR}/../../../skill/modes.md`
   - `${CLAUDE_SKILL_DIR}/../../../skill/templates.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/workflow.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/clarification-policy.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/judged-mode.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/principles.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/guardrails.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/sources.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/quality-bars.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/motion-system.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/design-quality.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/design-quality-rubric.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/golden-examples.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/synthetic-case-studies.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/domain-packs/index.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/weaknesses.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/evals.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/llm-judge-runner.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/paired-comparison.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/context-defaults.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/heuristics.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/patterns-catalog.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/adaptive-layout.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/inspiration-sources.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/visual-benchmark-playbooks.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/benchmark-report-format.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/visual-review-fixtures.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/rendered-output-qa.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/self-review.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/commands.md`
3. If `$ARGUMENTS` begins with `--judge`, strip that flag from the design task and apply `${CLAUDE_SKILL_DIR}/../../../docs/judged-mode.md`. Prefer the companion `mobile-design-judge` agent for the independent judge pass when available.
4. Apply the workflow to the current request.

Invocation payload:

$ARGUMENTS

If no arguments were passed after `/mobile-design-skill`, use the most recent user request from the conversation as the task input.

Return the result as a normal skill response, following the structure defined by the canonical skill.
