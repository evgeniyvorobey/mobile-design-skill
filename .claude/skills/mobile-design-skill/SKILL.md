---
name: mobile-design-skill
description: Generate, review, and structure mobile UI/UX decisions for iOS, Android, and cross-platform products. Use when you want to invoke the mobile design workflow directly in Claude Code with /mobile-design-skill.
argument-hint: "[task / screen / flow]"
disable-model-invocation: true
version: 1.5.0
---

# Mobile Design Skill

Use the repository's canonical mobile design skill for this request.

When invoked:

1. Read `${CLAUDE_SKILL_DIR}/../../../SKILL.md` first. That file is the canonical skill entrypoint and contains the core workflow.
2. Read supporting files only as needed:
   - `${CLAUDE_SKILL_DIR}/../../../skill/modes.md`
   - `${CLAUDE_SKILL_DIR}/../../../skill/templates.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/workflow.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/sources.md`
   - `${CLAUDE_SKILL_DIR}/../../../docs/commands.md`
3. Apply the workflow to the current request.

Invocation payload:

$ARGUMENTS

If no arguments were passed after `/mobile-design-skill`, use the most recent user request from the conversation as the task input.

Return the result as a normal skill response, following the structure defined by the canonical skill.
