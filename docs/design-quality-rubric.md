# Design Quality Rubric

This document turns design quality into a 1-5 scoring system. Use it to raise the quality of proposed designs, not only to critique existing ones.

**What the number records, measured.** Every boundary question here asks what an artifact *states*. Held against six designs and six twins made deliberately worse without changing a value, deleting a statement or breaking a bar, this scale returned the **identical band 12 paired scorings out of 12** — while showing 17% jitter on unchanged text, so it moves, just not with quality. **A band is not a verdict on which of two designs is better.** For that question use `docs/paired-comparison.md`, which separated the same twelve pairs 12 of 12. The two are complements: this scale says what an artifact has decided and where it sits; that one says which of two is the better screen.

The rubric complements:

- `docs/design-quality.md` for quality dimensions and mechanisms
- `docs/weaknesses.md` for recurring failure modes
- `docs/quality-bars.md` for numeric thresholds
- `docs/evals.md` for external response evaluation
- `docs/golden-examples.md` for compact taste and domain calibration examples
- `docs/synthetic-case-studies.md` for synthetic bad-to-good calibration cases
- `docs/domain-packs/index.md` for domain-specific risk and trust calibration
- `docs/visual-review-fixtures.md` for text-only review calibration
- `docs/rendered-output-qa.md` for optional QA when a rendered artifact exists
- `examples/evals/` for score-calibrated rubric fixtures
- `examples/rubric-before-after.md` for a weak-to-strong upgrade example
- `scripts/run_rubric_judge.py` and `docs/llm-judge-runner.md` for semantic judge calibration

---

## When to score

Score design quality when the response:

- proposes a screen concept
- creates a UI spec
- reviews a screen or screen description
- creates a typography and spacing system
- prepares a rationale or handoff

Mode B user flows normally do not need a visual quality score unless screen pacing, progress feedback, or transition quality materially affects the flow.

---

## Output rule

**The dimension read is the output; the score is a footnote to it.** Write the bands first, then take the median. A number written before the bands exist is retrieved, not derived.

For generated or specified design artifacts, the score is primarily internal:

- derive the score: bands per dimension, median of the assessable ones, then caps as a downward clamp
- if the derivation lands **at or below the midpoint** and the missing context is not blocking, revise the design and re-derive before returning
- if missing input prevents lifting a dimension past the boundary question it failed, state the limitation in `Assumptions` or `Unresolved assumptions`

For reviews, expose both a current and a projected score. Both are medians of the same dimension table — the current over the bands as found, the projected over the bands once the listed fixes land:

```md
- Current: [1-5]/5 — the median of the assessable dimensions as found; [short evidence-based reason; "provisional" for D2/D3 text-only]
- Projected: [1-5]/5 — the median of the assessable projected dimensions once the listed fixes land; conditional: requires those fixes AND the named assumptions to hold. State a flat number, not "up to". For D2/D3, provisional — visual dimensions stay unassessable (n/v) and are never projected upward.
- Ceiling note: with a visual pass confirming [x], the ceiling is [1-5]/5 (capped at 4/5 unless resilience is named).
```

Both numbers are derived the same way, and the current one is derived too: a review that states a current score without a band per dimension has asserted it. The projected score is the median of the assessable (non-`n/v`) projected dimensions, not the sum of per-dimension gains; a cap lifts only when the specific fix that meets its condition is present; a P0/Fail is never projected up to a number; and a higher figure reachable only after a visual pass belongs in `Ceiling note`, never in the projected number.

For generation, specs, typography systems, and handoff, expose the read and the target together:

```md
- Dimension read: [dimension] [n], [dimension] [n], ... (mark `n/v` where the evidence channel cannot carry the question). Median of the assessable = [n].
- Quality target: [derived]/5 — [either: blocked from [next]/5 by [dimension] until [named input or fix] | or, when nothing blocks the top band: nothing blocks 5/5 — [the resilience the bands record]]
```

Derive the bracketed values. Do not reuse the dimension named in any example you have read — if `Context & brand fit` is the blocker in three consecutive answers, it is being retrieved, not assessed.

**Name the blocker, at every level.** Below the top band, state which dimension holds the score there and whether the available input supports lifting it past the boundary question it failed. If it does, lift it and re-derive before returning. If it does not, say what input is missing. A score with no named blocker is a default, not a score — see `SKILL.md` on flagging defaults as such. When no dimension blocks the top band, say that instead of manufacturing a blocker to fill the slot.

Do not let the score replace the reasoning. The score is a compression of the critique, not the critique itself.

---

## 1-5 score levels

This table is a **reading key for a derived number**, not a second test to score against. The number comes from the dimension bands below; these labels say what a given median means and which verdict word to use. Do not score an artifact by picking the row that sounds right.

| Score | Label | What this median means |
|-------|-------|------------------------|
| 1/5 | Broken or misleading | Most dimensions failed their first boundary question, or a hard limit fired: the design obscures the primary task, invents unsupported claims, violates hard guardrails, or creates serious accessibility/usability risk. |
| 2/5 | Structurally weak | Most dimensions name the thing without deciding it — a palette listed but no role, two components offered instead of one chosen — so users or implementers will have to guess. A cap can also land an artifact here whose bands sit higher. |
| 3/5 | Acceptable baseline | Most dimensions decide the default case but stop before the variations: the design can work, and the first non-default case raises a question the artifact does not answer. |
| 4/5 | Strong and shippable | Most dimensions state values across the variations the artifact's own scope declares — states, appearances, text sizes, platforms — so two implementers building only from this have the same decisions in front of them. Note what this band does **not** claim: stating a value is not the same as its surviving implementation. Two blind implementations of one such spec were judged structurally different in 8 of 8 judgements (proposal section 43). |
| 5/5 | Excellent and resilient | Most dimensions carry a rule that decides cases the artifact does not itself list, so the design extends without re-asking the designer. |

---

## Dimension scoring

Score each relevant dimension from 1-5 by walking four boundary questions. A boundary question has a yes/no answer against the artifact in front of you; it is not a description to match against.

**How to read the table.** Start at the left. **The band is the number of consecutive questions answered yes, plus one.** Fail the first question and the dimension is 1; answer the first two yes and the third no and it is 3; answer all four yes and it is 5. A later yes never rescues an earlier no — the boundary you fail is where the dimension sits, because a design that skipped a rung did skip it. This is deliberately not an average: averaging a dimension whose parts disagree is how a mixed reading becomes a middling number.

The four boundaries ask the same four things of every dimension, and it helps to hold the ladder in mind before the row:

| Boundary | What it separates |
|---|---|
| 1 → 2 | contradicted or absent → **named** |
| 2 → 3 | named → **decided for the default case** |
| 3 → 4 | decided → **stated with values across the variations the artifact's own scope declares** |
| 4 → 5 | stated → **a rule that settles the cases the artifact does not list** |

Two consequences worth stating outright. Band 3 is a decision test, not a completeness test: an artifact that decides which content takes which role has passed it even if it never prints a number, because deciding and specifying are different acts and only one of them is band 3. And band 5 always has the same shape — *does a stated rule decide a case the artifact does not itself list?* — because that is the one thing a longer draft cannot manufacture by writing more of what it already wrote. Enumerating the cases you thought of is band 4.

### The band-5 closure test

**Answering the `4 → 5` question by inspection does not work.** It was measured: 63 statements pulled from live output were handed to three readers who saw the statement and one unsettled case from its own product, and nothing else — no artifact, no dimension, no band. Statements scored 5 were judged to settle their case 11 times in 28; statements scored 4, nine times in 25. The boundary did not separate them, and 17 of the 28 band-5 statements were judged non-generative by two or more readers who never saw a score.

So band 5 is not awarded on the reading. It is awarded on a closure test you actually run:

> Take one ordinary case the artifact does not list. State what the statement returns for it. **If you cannot write the answer, the band is 4.**

The case has to be ordinary — one a competent team meets in the first month — not an edge case chosen to be survivable. And the answer has to be the answer, not a restatement of the rule.

Two constraints on the case, both of which cost a measurement to learn:

- **It must be an instance of the unlisted thing this dimension's question names** — a surface, a pair of competing signals, new content, a section, a content volume, an interaction class, a decision class, an unlisted value. A case drawn from a different band's question fails a statement that answered its own question correctly: in one run, three dimensions were graded against cases their `4 → 5` cell never asked about, and 17 of 18 readings came back underdetermined on mechanisms that worked.
- **The answer must not already be printed in the statement.** A case can be unlisted while its answer is listed — the statement then closes it by quotation rather than by derivation, which is a band-2 reading dressed as a band-5 one. If you can answer by pointing at a sentence, pick another case.
- **Fix every input the rule needs except the one under test.** A case that also leaves the rule's input open is testing two rules at once, and it reads as undecided when only the second one is missing. Pick something the artifact already places, and ask what the rule returns for it.

Four shapes fail this test almost every time. They are listed as diagnoses, not as a menu to satisfy:

- **A ratio or a floor with no anchor.** Adjacent-role ratios and a minimum step, with no absolute size and no mapping from content to role. A contrast floor with no colour. The scale is stated; nothing generates a value.
- **A budget with no behaviour.** A duration ceiling that never says what the interaction does — on a re-tap, an early release, a duplicate input.
- **A precedence ladder with no output.** *Safety over audience over platform*, with the terms never mapped to a visual consequence, so two contexts pulling opposite ways still have no tie-break.
- **A requirement with no threshold.** "Stale must be visually distinct" with no staleness threshold; "parity with the lock screen" with no list of what has parity.

Each of these reads like a rule and decides nothing. The common error underneath all four is **a closed-world statement presented as a generative one**: the enumeration is the rule, and outside the enumeration there is nothing.

These four were first read backwards, out of statements already judged hollow. They have since been tested forwards: statements written to three of them on purpose closed 2 of 18 unlisted cases against blind readers, where statements built on a mechanism that returns something closed 29 of 36. What passes is deliberately not listed here — that is the point at which a diagnosis becomes a form to fill in.

| Dimension | 1 → 2 | 2 → 3 | 3 → 4 | 4 → 5 |
|-----------|-------|-------|-------|-------|
| Attention path and hierarchy | Does anything carry visibly more weight than everything else? | Is the element carrying most weight the one the primary task needs first, with the order of first glance, second glance and action decided? | Is the mechanism producing that order stated — which of size, weight, position or colour does the work? | Does a stated rule decide the order when two signals compete in a case the artifact does not list? |
| Composition and spacing | Do the groups read as groups without borders, shadows or fill doing the work? | Is it decided which elements belong together and which are separated, with the separation between groups larger than within them? | Are the spacing values stated, and do they survive the content expanding? | Does a stated rule produce the spacing for a section the artifact does not list? |
| Typography craft | Are type roles named at all, rather than a size chosen per element? | Is it decided which content takes which role, and what distinguishes each role from its neighbour? | Does each role carry stated values, and is the behaviour named when text scales up? | Does a stated rule decide which role new content joins, and what a new role must satisfy to exist? |
| Color, state, and contrast | Is every meaning carried by colour also carried by a second cue? | Is each semantic role decided — which meaning it carries and where it is used — rather than a palette listed? | Are the foreground/background pairs stated, and what they become in dark or increased contrast? | Does a stated rule return the dark and increased-contrast values for a role the artifact does not list? |
| Density and rhythm | Can the primary task be completed without the density hiding it? | Is the repeat unit decided — what one row or card carries, and what separates it from the next? | Is the recurring interval stated as a value, and what the layout does at the crowded end of the content range? | Does a stated rule decide the density for a content volume the artifact does not list? |
| Interaction polish and motion | Does every action that can fail or take time produce feedback at all? | Are the feedback states decided per action rather than listed once for the screen? | Are duration, curve and the reduced-motion fallback stated for the transitions the artifact names? | Does a stated rule assign a curve and duration band to an interaction class the artifact does not list? |
| Context and brand fit | Does the visual language avoid contradicting the domain's trust expectations and the platform's conventions? | Are the conventions being followed named, and each departure named with its reason? | Is the departure budget stated — what brand may override, and what semantics it may never override? | Does a stated rule decide the treatment for a context-sensitive decision class the artifact does not list? |
| Production readiness | Is there enough here for an implementer to start a conversation? | Is each component decided — which one, in which states — rather than offered as a choice between two? | Are token names and the state-to-component mapping stated, so two implementers have the same decisions in front of them? | Does a stated test return hard-bar or negotiable for a value the handoff does not list? |
| Distinctiveness and owned assets | Is any owned asset present at all, or is the screen interchangeable once the logo is removed? | Is the asset a stated treatment rather than an adjective? | Is it a token whose repeat locations are named beyond this one screen, within the delight-placement and brand-expression budgets? | Does a stated rule decide where the asset applies and where it never does, on a surface the artifact does not list? |

**Each cell is one test, not a checklist.** Where a cell names two things, the second is the single declared variation that value has to survive — not a list of everything the dimension could cover. A boundary written as a four-way conjunction fails almost every real artifact and pins the whole scale one notch below it; that failure has already happened here once.

**Score the artifact the mode produces.** A screen concept and a UI spec are held to the same boundaries, but they reach them with different evidence: a concept decides and a spec specifies. Band 3 is where a good concept lives; band 4 is where a spec has to get to. Do not fail a concept for lacking a number its own output contract never asked for — and do not pass a spec that only decided.

### When the answer is `n/v`, and when it is a low band

These are two different findings and the corpus has historically confused them.

- **`n/v` — the evidence channel cannot carry the question.** Visual dimensions in a text-only D2/D3 review; Distinctiveness when no brand context was supplied and structure only was asked for. An unanswerable question is not a no.
- **A low band — the channel is right and the content is thin.** A spec that could have stated a contrast pair and did not is scored on what it stated. Absence inside the right channel is evidence, and routing it to `n/v` is an evasion that quietly removes the weakest dimension from the median.

Ask which one applies with: *would a fuller instance of this same evidence type have settled it?* If yes, the input was thin and the answer is a low band. If no — a screenshot can never state a token name — it is `n/v`.

### Reading a screen instead of a document

The questions ask what the artifact *states*. A screenshot or a screen description states things by showing them, so in Mode D read "is X stated" as "can X be determined from the evidence in front of you". A screenshot showing one contrast pair answers the default-appearance question yes and leaves the dark-appearance question `n/v`.

---

## Caps and hard limits

**A cap clamps the artifact score downward, after the median. It never changes a dimension band** — a band records what the artifact states, and a cap records a consequence of that. Applying a cap by lowering a band destroys the evidence the cap was derived from.

- Any P0 weakness from `docs/weaknesses.md` makes the response **Fail**, not a score.
- Any P1 weakness caps score at **2/5** until fixed.
- Missing empty/loading/error states where relevant caps generated concepts and UI specs at **3/5**.
- Unsupported accessibility compliance claims make the response **Fail**.
- Visual assertions from text-only review input cap Mode D score confidence; label the score as provisional or restrict it to structural quality.
- Aesthetic-only recommendations cap the design-quality score at **2/5** until translated into task, accessibility, or implementation mechanisms.
- Platform flattening in materially different iOS/Android behavior caps cross-platform outputs at **3/5**.
- **Contradicted value:** a stated value or pattern choice that contradicts a bar in `docs/quality-bars.md`, a Use-when / Avoid-when rule in `docs/patterns-catalog.md`, a curve semantic in `docs/motion-system.md`, or the resolved default in `docs/context-defaults.md` caps the artifact at **3/5**. Two or more such contradictions, or any one against a touch-target, contrast, or state-coverage bar, cap it at **2/5**. **A stated reason does not lift this cap** — an artifact that fails this way almost always carries one, and that is exactly what makes a wrong value read as a decided one. The only exit is a deviation the *user's input* requires, named together with the input that requires it. Every band in the table above records what the artifact **states**; this cap is the one place the derivation asks whether what it states is **right**, and it exists because a wrong value gets built while an absent one gets a question.
- **Inert screen:** when `Distinctiveness and owned assets` sits below band 4, the artifact caps at **3/5** with an upside note, not a quiet 4/5. The requirement is stated once, in that dimension's `3 → 4` boundary question, and nowhere else. The exit is the `3 → 4 (inert cap)` rung in the improvement ladder below, and only that rung: adding mechanisms, platform notes or QA checks does not lift it, because the cap is about having a point of view, not about having enough content.

---

## Final scoring method

1. Walk the four boundary questions for each relevant dimension, marking `n/v` where the evidence channel cannot carry them.
2. Write the dimension read. It is the output; steps 3-5 only compress it.
3. Take the median of the **assessable** bands. A dimension marked `n/v` is excluded entirely — it is neither counted as low nor projected upward. Excluding it changes the median, so state which dimensions were assessable when the count is not obvious. With an even number of assessable dimensions the median falls between two bands: report the lower one.
4. Lower the result if one dimension critical to the primary task sits below the median.
5. Apply the caps as a downward clamp. There is no matching raise step: a 5/5 is what a median of 5 gives, and the resilience that earns it is already recorded in the `4 → 5` questions the dimensions answered.

**Checking the caps means reading the artifact's emitted values against the bars they claim to respect** — the touch targets, the contrast ratios, the durations and curves, the spacing steps, the pattern choice, the density against the resolved context default. A cap nobody looked for is a cap that never fires, and the boundary questions above will not surface a wrong value on their own: they ask whether it is stated.

Do not average away a serious flaw. A beautiful 5/5 visual direction with 2/5 state handling is not a 4/5 design; it is a risky design with polish — step 4 exists to say so.

**Never adjust a band to move the median.** The band answers a question about the artifact; the median answers nothing on its own. If the number that falls out is uncomfortable, the fix is in the design, not in the read.

---

## Improvement ladder

**To lift a dimension, answer the boundary question it failed.** That is the whole ladder at dimension level — the question you could not answer yes to *is* the work, stated as a test rather than as advice. The `Moves:` notation in a Mode D finding names that movement (`[dimension] [n]→[n]`).

The rungs below are the **artifact-level** ladder, for the score the median produced:

- 1 → 2: remove misleading claims, fix hard guardrails, define the actual user task
- 2 → 3: decide what is only named — which content takes which role, which of two components, what each colour role means; qualify assumptions; remove aesthetic-only advice
- 3 → 4: put values on the decisions and state them across the variations the artifact's own scope declares — states, appearances, text sizes, platforms — plus the production checks that make it buildable
- 3 → 4 **when the inert cap applies**: bring `Distinctiveness and owned assets` to band 4 by answering its `3 → 4` question. Nothing else lifts this cap — more mechanism detail, more platform notes and more QA checks all leave it at 3/5. This rung and the inert cap above name one condition between them, and the requirement itself lives in the dimension table.
- 4 → 5: replace enumerations with rules that decide the cases the artifact does not list

**Derive the score; do not choose it.** If the derivation lands at 3/5, report 3/5 and name the boundary question that would lift the blocking dimension. If the bands support the top level, report 5/5 without inventing a blocker to look modest. A dimension read where every dimension carries the same band across every artifact is evidence the score is being asserted rather than computed.

But **a corpus where every artifact scores the same number is not**, and reading it that way chases the wrong cause. This scale returns the same band to a design and a deliberately worse version of it, so flatness across artifacts is what a faithful application produces. Output mode moves it further: band-5 closure runs at 63% for specs against 28% for concepts, so a same-mode corpus concentrates by construction. Diagnose a flat corpus by checking one artifact's derivation against its text, never by nudging bands apart to look computed.

---

## Self-review prompt

Before returning a design artifact, silently answer:

- Did I write the bands before the number, and does the number I printed equal the median of the bands I wrote?
- For each dimension, which boundary question did the artifact fail — and did I name it in the `Quality target` line rather than printing a bare number?
- Can I answer that question with the information already available? If yes, do it and re-derive. If not, did I state the missing input clearly?
- For every dimension I put at band 5: did I run the closure test — one ordinary unlisted case, and the answer the statement returns for it — or did I award it on how the statement reads?
- Did every dimension land on the same band? If so, what made them agree — or did I stop reading once the number looked right?
- Where I marked `n/v`, would a fuller instance of the same evidence type have settled it? If it would, that is a low band, not `n/v`.
- Does this screen carry one owned asset, expressed as a token with repeat locations — or did I record honestly that it is inert?
- Did I avoid using the score as a substitute for concrete design mechanisms?

If the derivation lands at or below the midpoint and can be improved without inventing facts, revise it and re-derive before returning. If the bands support the top level, report it rather than trimming to look modest.

---

## Eval calibration pack

The repository includes score-calibrated fixtures in `examples/evals/`:

- `rubric-score-1.json` — broken or misleading response
- `rubric-score-2.json` — structurally weak response
- `rubric-score-3.json` — acceptable baseline response
- `rubric-score-4.json` — strong and shippable response
- `rubric-score-5.json` — excellent and resilient response

Each fixture defines:

- prompt
- response excerpt
- expected score
- verdict
- cap or hard limit
- dimension scores
- failed dimensions
- improvement suggestions

Use these fixtures when tuning prompts, judging generated responses, or adding LLM-as-judge tests.

For human calibration, use `examples/rubric-before-after.md`. It shows the upgrade path from a 2/5 template-complete UI spec to a 4/5 shippable spec.

For taste and domain calibration, use `docs/golden-examples.md` and `examples/golden/`. These examples show compact worked patterns for premium UI, enterprise SaaS, fintech, health, onboarding, settings, checkout, and tablet list-detail, each with its own derived score rather than a shared one.

For broader synthetic calibration, use `docs/synthetic-case-studies.md` and `examples/case-studies/`. These cases show plausible weak responses, stronger responses, and regression checks across domains and modes. They are not real-world validation.

For domain-aware calibration, use `docs/domain-packs/index.md` and `docs/domain-packs/`. Domain packs raise quality by improving hierarchy, state coverage, trust language, and handoff checks for fintech, health, SaaS, marketplace, social, and education. They do not prove compliance or business impact.

For review calibration, use `docs/visual-review-fixtures.md` and `examples/visual-review-fixtures/` to test whether Mode D reviews avoid unsupported visual claims from text-only evidence.

For implemented UI, use `docs/rendered-output-qa.md` and `examples/rendered-output-qa/` as an optional post-design QA layer. Rendered overlap, clipping, overflow, or state failures can cap an otherwise strong written design until fixed.

For semantic runner calibration, use:

```bash
python3 scripts/run_rubric_judge.py --dry-run
```

See `docs/llm-judge-runner.md` for the provider-agnostic JSONL contract.

For live semantic calibration, use the runner's external-agent command path instead of storing provider keys in the repository.
