# Judged Mode

Judged mode is an optional orchestration layer for higher-confidence design output.

It is triggered by:

```text
/mobile-design-skill --judge [task]
```

or by an equivalent explicit instruction such as:

```text
Use the mobile-design-skill with judge mode.
```

The flag means: produce the design artifact, run an independent rubric judge pass in the same session when the host supports subagents, revise if needed, then return the final answer with a compact judge summary.

---

## Core rule

`--judge` must not require the user to run `scripts/run_rubric_judge.py` manually.

The runner remains useful for CI, fixtures, and external command validation. Judged mode is the interactive user-facing workflow.

---

## Workflow

1. Strip the `--judge` flag from the task before mode classification.
2. Run the normal mobile-design-skill workflow and draft the response privately.
3. Build a judge packet containing:
   - selected mode
   - platform scope
   - user prompt
   - assumptions
   - draft response
   - relevant rubric dimensions from `docs/design-quality-rubric.md`
   - relevant fail conditions from `docs/evals.md` and `docs/weaknesses.md`
4. If the host environment supports a separate agent, subagent, or parallel reviewer, send the packet to that judge agent. In Claude Code, prefer the companion `mobile-design-judge` custom agent when available.
5. The judge agent must only score and critique. It must not rewrite the design.
6. If the judge's read leaves a dimension short of a boundary question the available input can answer, revise the draft, re-check the affected dimensions, and re-derive the score. Do not revise toward a number.
7. Return the final response, not the rough draft.
8. Add a compact `Judge summary` section at the end.

---

## Judge agent prompt contract

The judge agent should receive only the minimum packet needed to score the draft.

Use this instruction:

```text
You are an independent mobile design-quality judge.

Score each of the nine rubric dimensions by walking its four boundary questions:
the band is the number of consecutive questions answered yes, plus one.
The score is the median of the assessable bands, then clamped by caps.
Mark a dimension n/v only when the evidence channel cannot carry the question;
thin content inside the right channel is a low band, not n/v.
Before allowing any band 5, run the closure test: take one ordinary case the draft
does not list and state what its own statement returns for it. If you cannot write
the answer, the band is 4, however well the statement reads.
Do not rewrite the draft.
Return only:
- dimension read (all nine bands, with the median)
- score
- verdict
- weakest dimensions, each with the boundary question the draft failed
- hard limits or caps
- top revision suggestions
```

The judge pass is LLM-agnostic. It may run in Claude Code, Codex, another hosted model, a local model, or a company gateway. The skill only depends on the judge returning a concise rubric result.

---

## Fallback behavior

If a separate judge agent is not available in the host environment:

- do not ask the user to run a script manually
- run the normal internal rubric self-review
- label the final `Judge summary` as `Single-agent fallback`
- keep the response useful instead of blocking

This fallback is less independent than a real subagent pass, but it preserves the `/mobile-design-skill --judge` user experience.

---

## Final response addition

When judged mode is active, append:

```md
## Judge summary
- Mode: independent judge | single-agent fallback
- Dimension read: [dimension] [n], ... — median of the assessable = [n]
- Score: [1-5]/5
- Verdict: [short phrase]
- Weakest dimensions: [dimension] — [the boundary question it failed]
- Revisions applied: [1-3 concrete changes, or "None"]
```

Keep this section compact. Do not expose hidden chain-of-thought or raw judge transcripts.

---

## When not to judge

If the request is a clarification-only response because blocking information is missing, do not run a judge pass. Ask the blocking questions first. The next substantive answer can use judged mode after the missing input is resolved.
