# Self-review

This document defines the mandatory self-review pass every skill response must undergo before being returned.

Self-review is the single highest-impact lever for output quality. Without it, LLM responses drift toward plausible-sounding but shallow output — visible structure, weak substance. With it, most low-quality outputs are caught before the user ever sees them.

Self-review runs inside the workflow as **Step 9: Self-review against quality bar**, after the draft is complete and before it is returned.

---

## How to run self-review

Self-review has **two tiers, and only one of them blocks**.

1. Produce the full mode-specific draft using the template.
2. Answer the four **blocking-gate** questions below in writing. Any "yes" blocks the return until it is fixed.
3. Silently answer every prompt in the applicable improvement sections. A "no" there is work to do, not a reason to withhold the response: make the edits the input supports, then return.
4. Re-run the blocking gate after any fix that touched a state, a claim, an interaction, or the header.

**Why the tiers exist.** This pass previously required "a confident yes on every applicable prompt" across roughly forty questions, several of which cannot be answered yes by construction. That exit condition is unreachable, and it was measured returning "revise" on 9 of 9 drafts — good ones and deliberately defective ones alike. **A gate that never opens is not a strict gate but no gate**, because the only ways past it are an infinite loop and a silent override; the second is what happens, and it teaches that a mandatory step can be stepped over.

**What the gate blocks, and what it does not.** The gate carries only conditions that have **no legitimate version** — an invented fact, a missing required state, a broken accessibility hard rule, a dishonest header. A value that contradicts a bar is a different animal: sometimes the user's input requires the deviation, and sometimes the bar's scope does not reach the case at all (the 8 pt gap between *independent* tap targets does not govern adjacent rows of one list that carry the same consequence). That class is caught by the **contradicted-value cap** in `docs/design-quality-rubric.md`, which scores it down rather than blocking it — a gate that cannot tell a deviation from a scope argument blocks correct work.

Block on what is never right. Score down what is usually wrong.

---

## Blocking gate (answer in writing, before returning)

Four questions. Each has a definite answer, each is checkable against the draft rather than judged, and a good draft answers "no" to all four.

1. **Invented given.** Have I presented anything as supplied or established that the input did not supply — a brand value, a measured contrast ratio, a platform rule, a research finding, a usability result, or a compliance status?
2. **Missing required state.** Is any state the mode requires — default, loading, empty, error, and the detail-pane empty state at regular width — absent where it applies, while the surrounding prose reads as though coverage is complete?
3. **Accessibility hard rule.** Does the draft go below a touch-target minimum, carry a meaning by colour alone, leave a gesture without a non-gesture path, or put an action behind hover only?
4. **Contract and honesty of the header.** Is `Mode:`, `Platform scope:`, `Device class:`, `Assumptions:` or `Next actions:` missing, or did I round the request to the nearest template instead of using the no-fit branch?

None of the four can be argued away by a reason. If the answer is yes, the draft is not returnable as it stands.

Do not echo the self-review prompts in the response. Do not add a "self-review passed" footer. Self-review is internal quality control, not user-facing content.

Do not skip self-review to save tokens. A response that fails self-review is a regression; a response that passes is the floor, not the ceiling.

---

## Improvement prompts (run for every mode)

These never block a return. A "no" here is the next edit, and the draft goes out once the edits the input supports have been made.

**Values against bars belong here.** Walk the numbers, the pattern choices, the curves and the density against `docs/quality-bars.md`, `docs/patterns-catalog.md`, `docs/motion-system.md` and `docs/context-defaults.md`, and fix what the input lets you fix. What survives is scored, not blocked: see the contradicted-value cap in `docs/design-quality-rubric.md`. An author is measurably worse at this than a stranger is — 3 of 6 on their own arithmetic against a reviewer's 6 of 6 — because the draft already contains the argument that justified the value. Check the file, not the memory of deciding.

### Specificity
- Could this exact response have been written with **no** information about the user's product, domain, or audience? If yes, the response is too generic; rewrite with the provided context.
- Have I replaced every instance of vague language ("modern", "clean", "intuitive", "appropriate spacing", "good contrast") with a concrete claim?
- If I removed the `Mode:` and `Platform scope:` headers, would a reader still be able to tell which mode this is? If not, structure is weak.
- Is the `Mode:` header honest, or did I round the request to the nearest template? If the request is really paywall strategy, whole-app IA, notification policy, or design-system governance, use the no-fit branch instead of stretching a mode over it.
- Is every section I included carrying a decision the input supports? Any section I filled with a placeholder, a restatement of the request, or a generic caution should be cut and the omission named in one line under `Assumptions` — coverage is not quality.

### Clarification policy
- Did I apply `docs/clarification-policy.md` before deciding to ask questions or proceed?
- If I asked questions, are there three or fewer and are they genuinely blocking?
- If I proceeded with assumptions, are they minimal, labeled, and safe?
- Did I avoid asking cosmetic or preference questions before task, platform, safety, accessibility, or implementation blockers?
- If clarification blocks a reliable artifact, did I offer a fast path when a provisional draft would still be useful?

### Known weakness prevention
- Which weakness pattern from `docs/weaknesses.md` is most likely in this task, and did I actively prevent it?
- Does the draft resemble template completion without real decisions? If yes, add choices, rejected alternatives, and reasons.
- Did I avoid the common regression trio: generic output, first-idea bias, and happy-path-only design?
- If the task involves review or handoff, did I prevent visual overclaim and weak buildability?

### Substance
- Does every recommendation have a reason tied to user goal, task, accessibility, readability, or implementation — not aesthetic preference?
- For a recommendation that changes a design, did I state its intended effect, not just the change itself?
- For each major design decision, have I named at least one alternative and said why it was rejected? If not, the decision was not actually made.
- Are there any sentences that could be deleted without losing information? Delete them.

### Honesty
- Have I claimed any platform behavior, research finding, or accessibility compliance that I cannot source or that was not provided?
- Have I made a visual claim (contrast, spacing value, typography treatment) when only a text description was provided? If yes, move it to `Unresolved assumptions`.
- Have I echoed a user-provided compliance claim (for example, "WCAG AA") as fact? If yes, add the "cannot independently verify" qualifier.

### Device class
- Did I resolve device class as its own axis, or did I let "cross-platform" stand in for "phone"?
- If I defaulted to phone, did I state it as a reversible assumption rather than a closed statement?
- If the device class is not phone: did I map the layout to width classes rather than to a device model, name a canonical layout, change navigation with width, and say what survives a multitasking resize?
- Did I keep touch minimums unchanged at every width, and give every drag-and-drop a non-drag path?

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

### Design quality calibration
- If the response proposes, specifies, reviews, or rationalizes a design artifact, did I apply the relevant lenses from `docs/design-quality.md`?
- Did I apply the 1-5 rubric from `docs/design-quality-rubric.md`?
- For generated/specification outputs, does the number I printed equal the median of the dimension read I actually wrote — and for each dimension below the top band, did I answer the boundary question it failed or state the missing input?
- For Mode D reviews, did I expose both a current and a projected (conditional) design-quality score with a reason and evidence limits?
- For every dimension I put at band 5: did I run the closure test — take one ordinary case the artifact does not list, and state what my own statement returns for it? If I cannot write that answer, the band is 4, however well the statement reads.
- Did I define the intended attention path rather than only listing components?
- Did I translate visual quality into concrete mechanisms such as size, spacing, alignment, color role, density, motion, state treatment, or tokens?
- Did I avoid using "premium", "clean", "modern", "delightful", or "polished" as unexplained taste words?
- Did visual expression support task clarity and accessibility rather than hide missing states, weak hierarchy, or inaccessible interactions?
- Inert-screen test: if this screen lost its logo and brand color, would it still be distinguishable from a competitor's? If not, `Distinctiveness and owned assets` sits below band 4 and the inert cap applies — record it with an upside note rather than letting the median stand.

### Inspiration handling
- If I used inspiration sources, are they clearly separated from UX rationale, platform guidance, accessibility requirements, and compliance language?
- If I named a production reference (Mobbin, Page Flows, UI Sources, Pttrns, Screenlane), did I frame it as a lookup for the user to perform — rather than describing screens I have not seen? These sit behind sign-in or paid subscriptions; a skill run has no session for them.
- Did I state any platform default as timeless when it is version-bound (Material version, predictive back, themed icons, OS-gated behaviour)? Those are current as of this skill's last review, not permanent facts.
- Did I avoid presenting Behance, Dribbble, Pinterest, Awwwards, awards, or gallery examples as proof that a design is usable, accessible, or platform-correct?
- If the user did not ask for inspiration and it does not materially help, did I leave it out?

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
- Did I name three directions with different token consequences before drafting, or did I justify the first idea after the fact? Two directions that differ only in adjectives are one direction.
- Were D2 and D3 actually **drawn from the catalog** in `docs/inspiration-sources.md`, with their entry names recorded as `from:` provenance — or did I generate three candidates from instinct and cite the catalog afterwards?
- Would this same candidate set appear for any other product in this domain? If yes, the catalog was bypassed, not sampled.
- Is the committed direction's owned asset a different **asset class** from the nearest golden example's, or did I reach for the same class under a new name?
- Are the two entries under `Alternatives considered` structurally different from the chosen layout, or are they variants of the same structure wearing different labels?
- Does `Signature move` name an owned asset as a token with the places it repeats — or did I record honestly that the screen is inert and what would change that?

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
- Did the direction set precede the spec, and do the rejected directions in `Key decision tradeoffs` differ from the chosen one in at least two token fields?
- Does `Key decision tradeoffs` say what each contested choice gave up, or does it only restate what was chosen? A tradeoff with no cost named is a preference.

### Mode D: Review screen for usability/accessibility
- Did I classify the sub-case (D1 visual / D2 description only / D3 problem statement / D4 context change) at the top?
- For D2 (description only): did I avoid asserting visual properties (contrast, spacing values, visual weight)?
- Did I find at least one genuine strength? A review with only negatives is biased, not thorough.
- Is each finding a single causal chain (observation → violated principle → user consequence → change → predicted effect), with no issue split from its fix and no orphaned fix?
- Does every finding name the violated principle, and does every predicted effect name a user outcome (directional + confidence), not a restatement of the change?
- Is severity rated 0–4 (Nielsen = frequency × impact × persistence) and based on user impact, not on how much it bothers me visually?
- Did I expose both a current and a projected score, the projected number being the flat median of the assessable (non-`n/v`) projected dimensions — not the sum of per-dimension gains, and never "up to" — with the projection conditional, capped at 4/5 unless resilience is named, any higher post-visual-pass figure confined to a `Ceiling note`, and the whole block labeled provisional for D2/D3?
- If a Bold move is present: is its trigger met, all fields complete, and kept separate from required fixes — and did I withhold any UX-strengthening move only because it contradicts the product (if so, move it here)?

### Mode E: Create typography and spacing system
- Are type roles named (Display, Title, Body, etc.), not just a list of sizes?
- Does the scale support Dynamic Type on iOS and font-scale on Android, or did I ignore scaling?
- Is the spacing scale systematic (4- or 8-based, or explicit token names)?
- Did I choose the base unit and scale ratio as a direction decision with a stated reason, or did I emit the default 4/8/12/16/24/32/40 ladder by reflex?
- Did I state minimum touch targets (44pt iOS / 48dp Android)?
- If multilingual was requested, did I address script-specific adjustments (CJK, Arabic, Devanagari)?

### Mode F: Prepare design rationale / handoff
- Does every "Key design decision" have an alternative that was considered and rejected, with reason?
- Is the rationale connected to the specific design in question, or does it read like a generic essay?
- Does the validation plan specify what to test and how (method, metric, acceptance), not just "test with users"?
- Are open questions genuinely open (blocking or undecided), not filler?

---

## When self-review finds a problem

If the **blocking gate** answers yes:

1. Fix it before returning anything. There is no disclaimer that substitutes.
2. Address the root cause, not the surface.
3. Re-run the gate after the fix.

If an **improvement prompt** answers no:

1. Do not patch the surface. Address the root cause.
2. If the draft cannot be fixed with light edits, rewrite the affected section from scratch.
3. Make the edits the input supports, then return the response. An improvement prompt that stays "no" because the input cannot support better is recorded in `Assumptions`, not used to withhold the answer.

If self-review cannot pass because the input is underspecified:

1. Reduce the scope of the response to what the input supports.
2. Move unsupported claims to `Unresolved assumptions`.
3. Strengthen `Next actions` to pull the missing information from the user.

Do not return a response that fails the blocking gate with a disclaimer. Fix it or narrow it.

---

## Integration with other quality mechanisms

Self-review complements, but does not replace:

- **Guardrails** (`docs/guardrails.md`): hard rules that must never be violated.
- **Evals** (`docs/evals.md`): external scoring criteria for regression tests.
- **Mode validation checklists** (`skill/modes.md`): structural contracts per mode.
- **Quality bars** (`docs/quality-bars.md`): concrete thresholds self-review checks against.
- **Known weaknesses** (`docs/weaknesses.md`): recurring failure modes and prevention checks.

The flow is: draft → self-review (internal) → response returned → evals (external, automated or manual).

---

## Maintenance

When a new failure mode is observed in the field, add a corresponding self-review prompt here. The goal is that every regression caught in eval should trigger a new self-review prompt to prevent recurrence.

Keep prompts answerable in one pass — yes/no or short-answer. Self-review must be fast to run, or it will be skipped.

New prompts join the **improvement** tier by default. A prompt joins the blocking gate only when a good draft answers it cleanly, the answer is checkable against the draft rather than judged, and the condition has no legitimate version. Every prompt added to the gate that fails one of those three costs the gate its ability to discriminate, which is the only thing it is for.
