---
name: mobile-design-skill
description: Generate, review, and structure mobile UI/UX decisions for iOS, Android, and cross-platform products. Use when you want to invoke the mobile design workflow directly in Claude Code with /mobile-design-skill.
argument-hint: "[--judge] [task / screen / flow]"
disable-model-invocation: true
version: 2.0.0
---

# Mobile Design Skill

Use the repository's canonical mobile design skill for this request.

When invoked:

1. Read `${CLAUDE_SKILL_DIR}/../../../SKILL.md` first. That file is the canonical skill entrypoint and is the whole of the default behaviour.
2. The canonical file names its other files by repository-relative path. They resolve here:
   - Read when the canonical file says to, which is for almost every design request:
     - `${CLAUDE_SKILL_DIR}/../../../skill/platform.md`
   - Read only when the user asks for what the file covers (canonical section 6):
     - `${CLAUDE_SKILL_DIR}/../../../docs/inspiration-sources.md`
     - `${CLAUDE_SKILL_DIR}/../../../docs/design-quality-rubric.md`
     - `${CLAUDE_SKILL_DIR}/../../../docs/judged-mode.md`
     - `${CLAUDE_SKILL_DIR}/../../../docs/benchmark-report-format.md`
     - `${CLAUDE_SKILL_DIR}/../../../docs/visual-benchmark-playbooks.md`
     - `${CLAUDE_SKILL_DIR}/../../../docs/rendered-output-qa.md`
     - `${CLAUDE_SKILL_DIR}/../../../docs/quality-bars.md`
     - `${CLAUDE_SKILL_DIR}/../../../docs/patterns-catalog.md`
     - `${CLAUDE_SKILL_DIR}/../../../docs/motion-system.md`
3. If `$ARGUMENTS` begins with `--judge`, strip that flag from the design task and apply `${CLAUDE_SKILL_DIR}/../../../docs/judged-mode.md`. Prefer the companion `mobile-design-judge` agent for the independent judge pass when available.
4. Answer the request the way the canonical file describes.

Invocation payload:

$ARGUMENTS

If no arguments were passed after `/mobile-design-skill`, use the most recent user request from the conversation as the task input.
