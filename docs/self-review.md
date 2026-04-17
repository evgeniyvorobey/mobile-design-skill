# Self-review

This document defines the mandatory self-review pass every skill response must undergo before being returned.

Self-review is the single highest-impact lever for output quality. Without it, LLM responses drift toward plausible-sounding but shallow output — visible structure, weak substance. With it, most low-quality outputs are caught before the user ever sees them.

Self-review runs inside the workflow as **Step 9: Self-review against quality bar**, after the draft is complete and before it is returned.

---

## How to run self-review

1. Produce the full mode-specific draft using the template.
2. Silently answer every prompt in the relevant section below.
3. If any answer is "no" or "not sure", revise the draft.
4. Only return the response after every applicable prompt has a confident "yes".

Do not echo the self-review prompts in the response. Do not add a "self-review passed" footer. Self-review is internal quality control, not user-facing content.

Do not skip self-review to save tokens. A response that fails self-review is a regression; a response that passes is the floor, not the ceiling.

---

## Universal self-review prompts (run for every mode)

### Specificity
- Could this exact response have been written with **no** information about the user's product, domain, or audience? If yes, the response is too generic; rewrite with the provided context.
- Have I replaced every instance of vague language ("modern", "clean", "intuitive", "appropriate spacing", "good contrast") with a concrete claim?
- If I removed the `Mode:` and `Platform scope:` headers, would a reader still be able to tell which mode this is? If not, structure is weak.

### Substance
- Does every recommendation have a reason tied to user goal, task, accessibility, readability, or implementation — not aesthetic preference?
- For each major design decision, have I named at least one alternative and said why it was rejected? If not, the decision was not actually made.
- Are there any sentences that could be deleted without losing information? Delete them.

### Honesty
- Have I claimed any platform behavior, research finding, or accessibility compliance that I cannot source or that was not provided?
- Have I made a visual claim (contrast, spacing value, typography treatment) when only a text description was provided? If yes, move it to `Unresolved assumptions`.
- Have I echoed a user-provided compliance claim (for example, "WCAG AA") as fact? If yes, add the "cannot independently verify" qualifier.

### Context fit
- Have I applied the relevant defaults from `docs/context-defaults.md` (audience, domain, platform, use-context)?
- When context signals conflicted, did I resolve them using the documented precedence (safety/accessibility > regulated domain > use-context > audience > platform) and surface the resolution in `Assumptions`?
- Did I apply a generic default where a context-specific one would have been more appropriate?

### Heuristic grounding
- For each major decision, can I name the heuristic that justifies it (Fitts, Hick, Miller, Jakob, Zeigarnik, peak-end, goal-gradient, Nielsen, Gestalt)?
- If I cited a heuristic, is the citation doing work, or is it decorative? Remove decorative citations.
- Did I miss a red flag from `docs/heuristics.md` that applies to this screen or flow?

### Pattern selection
- Did I pick each pattern (navigation, overlay, list/grid, picker, feedback surface) using the decision matrix in `docs/patterns-catalog.md`, or did I default to my first instinct?
- Did I cite the losing alternative for every pattern-level choice?
- Am I inventing a novel pattern where an established one fits? If yes, revert to the established pattern unless the input truly has no fit.
- For Mode D reviews: did I check every pattern the design uses against the matching entry's red flags?

### Completeness
- Are all three edge states addressed (empty, loading, error) where the mode requires them?
- Does the `Next actions` section contain specific, testable actions — not "test it", "iterate", "validate"?
- For cross-platform outputs, have I split iOS and Android where conventions actually differ, and shared the structure where they align?

### Readability of the response itself
- Can a designer skim this response in under 2 minutes and extract the 3 most important decisions?
- Are sections ordered by decision priority, not template default?
- Is the response too long? If so, the structure is hiding thin content; cut and strengthen.

---

## Mode-specific self-review prompts

### Mode A: Generate mobile screen concept
- Is the primary user task singular and obvious, or did I list three parallel tasks?
- Is the information hierarchy ordered by what the user needs to decide or do first, not by visual prominence?
- Are the suggested components buildable on the named platform (native components or a common UI kit)?
- Have I addressed what happens when the screen has zero data, partial data, stale data, and full data?
- Did I commit to one layout rather than describing three possible layouts without choosing?

### Mode B: Design mobile user flow
- Does the flow run end-to-end from a concrete entry point to a success state?
- Is back-navigation defined for every step, not just the last one?
- Have I defined recovery for at least network failure, user abandonment, and input validation?
- Does any step assume desktop conventions (hover, right-click, keyboard-first entry)?
- Are any steps invented business rules? If yes, are they labeled as assumptions?

### Mode C: Create platform-aware UI spec
- Can an engineer begin implementation without asking clarifying structural questions?
- Are states defined beyond "default" — at minimum default, loading, empty, error?
- Are spacing and typography values concrete (tokens, pixels, dp), not relative ("more", "tighter")?
- For cross-platform: are iOS and Android sections meaningfully different, or did I duplicate shared content to look thorough?
- Does the spec reference a design system (named or assumed), or does it invent component names without grounding?

### Mode D: Review screen for usability/accessibility
- Did I classify the sub-case (D1 visual / D2 description only / D3 problem statement / D4 context change) at the top?
- For D2 (description only): did I avoid asserting visual properties (contrast, spacing values, visual weight)?
- Did I find at least one genuine strength? A review with only negatives is biased, not thorough.
- Does every severity-High issue have a concrete recommended fix, not a restatement of the issue?
- Is severity assigned based on user impact, not on how much it bothers me visually?

### Mode E: Create typography and spacing system
- Are type roles named (Display, Title, Body, etc.), not just a list of sizes?
- Does the scale support Dynamic Type on iOS and font-scale on Android, or did I ignore scaling?
- Is the spacing scale systematic (4- or 8-based, or explicit token names)?
- Did I state minimum touch targets (44pt iOS / 48dp Android)?
- If multilingual was requested, did I address script-specific adjustments (CJK, Arabic, Devanagari)?

### Mode F: Prepare design rationale / handoff
- Does every "Key design decision" have an alternative that was considered and rejected, with reason?
- Is the rationale connected to the specific design in question, or does it read like a generic essay?
- Does the validation plan specify what to test and how (method, metric, acceptance), not just "test with users"?
- Are open questions genuinely open (blocking or undecided), not filler?

---

## When self-review finds a problem

If self-review fails on any prompt:

1. Do not patch the surface. Address the root cause.
2. If the draft cannot be fixed with light edits, rewrite the affected section from scratch.
3. Re-run self-review after the fix.

If self-review cannot pass because the input is underspecified:

1. Reduce the scope of the response to what the input supports.
2. Move unsupported claims to `Unresolved assumptions`.
3. Strengthen `Next actions` to pull the missing information from the user.

Do not return a response that fails self-review with a disclaimer. Fix it or narrow it.

---

## Integration with other quality mechanisms

Self-review complements, but does not replace:

- **Guardrails** (`docs/guardrails.md`): hard rules that must never be violated.
- **Evals** (`docs/evals.md`): external scoring criteria for regression tests.
- **Mode validation checklists** (`skill/modes.md`): structural contracts per mode.
- **Quality bars** (`docs/quality-bars.md`): concrete thresholds self-review checks against.

The flow is: draft → self-review (internal) → response returned → evals (external, automated or manual).

---

## Maintenance

When a new failure mode is observed in the field, add a corresponding self-review prompt here. The goal is that every regression caught in eval should trigger a new self-review prompt to prevent recurrence.

Keep prompts answerable in one pass — yes/no or short-answer. Self-review must be fast to run, or it will be skipped.
