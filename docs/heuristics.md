# Heuristics Catalog

This document maps established usability and cognitive heuristics to concrete mobile design decisions. Each entry has:

- **What**: the heuristic in one sentence.
- **Mobile application**: specific decisions it drives on phones and tablets.
- **Red flag**: what a design violation looks like, so the skill can catch it in Mode D reviews and prevent it in generation modes.
- **Source**: where the heuristic comes from.

Heuristics are rules of thumb, not laws. Apply them with context in mind (`docs/context-defaults.md`), not as rigid checklists. When two heuristics conflict, the design decision must name both and say which one wins and why.

---

## Interaction laws

### Fitts' Law

**What**: The time to acquire a target is a function of the distance to it and the size of it — larger and closer targets are faster and more accurate.

**Mobile application**:
- Primary actions belong in the thumb-reachable lower half of the phone screen.
- Frequently used controls should be larger than occasional controls.
- Touch targets near the screen edges (especially in corners) are slower and easier to miss; keep critical actions away from edges unless the edge is itself the affordance (home indicator, edge-back gesture).
- Two targets adjacent to each other with different consequences (one primary, one destructive) must have visual and spatial separation; a small target next to a large one increases misses.

**Red flag**:
- Primary action placed at the top of a content-heavy screen on phone.
- Destructive action adjacent to primary with no gap.
- Small icon button as the only way to trigger a high-frequency action.

**Source**: Fitts (1954). Applied extensively in Apple HIG and Material 3 target sizing guidance. Cross-reference `docs/quality-bars.md` touch targets.

---

### Hick's Law

**What**: The time to make a decision grows with the logarithm of the number of choices.

**Mobile application**:
- Bottom navigation: 3–5 destinations, not 6+. The sixth destination should trigger an IA reconsideration, not a "More" tab as a graveyard.
- Filter and sort menus: group options; hide advanced behind a reveal, show top 3–5 by frequency.
- Onboarding: one decision per screen, not a wall of toggles.
- Empty-state CTAs: one primary option, optional secondary.
- Long lists of options (country picker, language picker): provide search, don't rely on scrolling.

**Red flag**:
- Filter screen with 12 equally weighted checkbox options.
- Onboarding screen with three competing primary CTAs.
- Navigation with more than 5 primary destinations and no hierarchy.

**Source**: Hick (1952), Hyman (1953). Related: cognitive load reduction.

---

### Miller's Law (7 ± 2)

**What**: Short-term working memory holds roughly 4–9 chunks of information.

**Mobile application**:
- Long forms: chunk into sections of 5–7 fields.
- Lists on a single screen: 7–9 items before scrolling is reasonable; beyond that, hierarchy or search helps.
- Multi-step flows: 3–7 steps; beyond that, split or reconsider.
- Summary screens: surface 3–5 key metrics before the rest.

**Red flag**:
- A form with 15 fields in a flat stack with no sections.
- A settings screen listing 20 toggles with no grouping.

**Source**: Miller (1956). Later refinements (Cowan) argue the real limit is closer to 4 chunks; design conservatively.

---

### Jakob's Law

**What**: Users spend most of their time on other apps, so they expect yours to work the way those other apps work.

**Mobile application**:
- Respect platform conventions over clever divergence (see `docs/guardrails.md` #6).
- For a new category (first banking app in a market), anchor to the closest neighboring category the user already knows.
- Novel interactions require explicit onboarding or an affordance; do not ship new gestures with no discovery path.
- Do not rename system concepts ("Account" → "My Realm") without a reason.

**Red flag**:
- A custom navigation pattern that replaces standard tabs with no onboarding.
- Back behavior that differs from platform expectation.
- Icons that look like system icons but do different things.

**Source**: Jakob Nielsen. Related: recognition over recall.

---

### Doherty Threshold

**What**: Systems that respond to a user in under ~400ms keep the user engaged; above ~1 second, the user's attention starts to drift.

**Mobile application**:
- Tap feedback: 100–150ms state change is the ceiling for "immediate".
- Screen transitions: 200–300ms; longer feels sluggish.
- Network-bound actions: show optimistic state and sync in the background where safe.
- Long operations (upload, sync): progress visibility and ability to cancel or background.

**Red flag**:
- Button with no visual state change on press.
- Network request with no loading indicator under 1s.
- 700ms "premium" transition on a simple screen change.

**Source**: Doherty & Thadani (1982). Cross-reference `docs/quality-bars.md` motion durations and loading thresholds.

---

### Tesler's Law (Conservation of Complexity)

**What**: Every system has an irreducible amount of complexity. The only question is who absorbs it: the user, the designer, or the engineer.

**Mobile application**:
- Smart defaults absorb complexity from the user at the cost of designer effort.
- Forms with auto-detected country codes, date formats, and currency absorb complexity from the user.
- Asking the user to "just configure it" pushes complexity onto the user.
- Hiding a setting does not remove complexity; it moves it to discoverability.

**Red flag**:
- A flow that asks the user questions the app could answer from context.
- Power-user features exposed on the happy path "so everyone can access them".

**Source**: Larry Tesler.

---

### Postel's Law (robustness principle)

**What**: Be conservative in what you send, liberal in what you accept.

**Mobile application**:
- Input validation: accept many formats (phone with/without country code, dates with slashes or dashes, credit card with/without spaces) and normalize internally.
- Do not reject valid-but-differently-formatted user input.
- Output formatting: consistent, predictable, locale-appropriate.

**Red flag**:
- Form field that rejects "+1 (555) 123-4567" because it expected "5551234567".
- Date input that only accepts "MM/DD/YYYY" with no placeholder showing format.

**Source**: Jon Postel (originally for network protocols).

---

## Cognitive heuristics

### Zeigarnik Effect

**What**: People remember incomplete or interrupted tasks better than completed ones.

**Mobile application**:
- Progress indicators in multi-step flows: show steps completed and steps remaining to exploit completion motivation.
- Incomplete profile or onboarding prompts: surface gently; the user is already motivated to close the loop.
- Do not abuse: badging everything as "incomplete" creates noise, not motivation.
- Resumable flows: when a user returns to an interrupted flow, pick up where they left off, do not restart.

**Red flag**:
- Multi-step flow with no progress indicator.
- Lost state on app backgrounding mid-flow.

**Source**: Bluma Zeigarnik (1927).

---

### Peak-End Rule

**What**: People judge an experience largely by how it felt at its peak (positive or negative) and at its end, not by the average.

**Mobile application**:
- Error recovery: a painful task that ends in success with a friendly resolution feels better than a smooth task that ends in silent failure.
- Success states: make them feel like a resolution, not a default screen.
- Checkout completion: confirmation matters more than the average speed of each step.
- Onboarding: the last step should land the user in the app's best moment, not in a settings screen.

**Red flag**:
- No success state after a multi-step task; just returning to the list.
- Error state that leaves the user stuck with no path forward.

**Source**: Kahneman et al.

---

### Goal-Gradient Effect

**What**: Motivation to complete a task increases as the user gets closer to the goal.

**Mobile application**:
- Progress bars in onboarding and checkout increase completion.
- "2 of 3" labeling, not just "Step 2".
- Near the end of a flow, remove optional distractions (upsells, tours).
- For long-term goals (savings, learning), show accumulated progress to exploit the gradient.

**Red flag**:
- A five-step flow with no indication of where the user is.
- Upsell interstitial inserted after step 4 of 5.

**Source**: Hull (1932). Related: completion bias.

---

### Serial Position Effect (primacy + recency)

**What**: Items at the beginning and end of a list are remembered better than items in the middle.

**Mobile application**:
- Navigation bar: place the two most important destinations first and last.
- Menu lists: critical actions at the top or bottom, not buried in the middle.
- Onboarding screens: the most important message goes first or last, not in the third screen of five.

**Red flag**:
- Critical action placed at position 3 of 5 in a menu.
- The most valuable destination buried in the middle of a nav bar.

**Source**: Ebbinghaus. Related: primacy / recency.

---

### Choice Overload (Paradox of Choice)

**What**: Too many options cause decision paralysis and reduce satisfaction with whatever is chosen.

**Mobile application**:
- Start with a curated set of options; let the user expand to "see all".
- Personalize early; show 5 relevant items before 500 possible.
- Defaults matter: a pre-selected "recommended" option is better than a blank choice.
- When the user must pick (for example, a plan), present 3 options, not 8.

**Red flag**:
- First-use screen that asks the user to pick from 20 categories with no guidance.
- Plan picker with 6 tiers and subtle differences.

**Source**: Iyengar & Lepper (2000).

---

### Recognition over Recall (Nielsen #6)

**What**: Recognizing something is easier than remembering it from memory.

**Mobile application**:
- Menus and lists of options are easier than free-text commands.
- Recent items, suggestions, and autocomplete reduce memory load.
- Labeled icons outperform icon-only controls for ambiguous meanings.
- Do not ask the user to remember a confirmation code from an email; let the email link in directly where possible.

**Red flag**:
- Icon-only navigation with non-obvious icons.
- Flow that requires the user to memorize a number from one screen and type it on the next.

**Source**: Nielsen's 10 heuristics.

---

### Aesthetic-Usability Effect

**What**: Users perceive aesthetically pleasing designs as more usable than less attractive ones, even when the underlying usability is the same.

**Mobile application**:
- Visual polish matters for first impressions and trust.
- Polish is **not a substitute** for usability; it only masks usability problems temporarily. Real usability failures will surface with continued use.
- The skill should never recommend aesthetic improvements as the primary fix for a usability problem (see `docs/guardrails.md` #4).

**Red flag**:
- A critique that says "make it prettier" as the fix for a navigation problem.
- Aesthetic polish that is used to justify skipping usability work.

**Source**: Kurosu & Kashimura (1995), Tractinsky (1997).

---

### Von Restorff Effect

**What**: An item that stands out from its neighbors is remembered better.

**Mobile application**:
- The primary action on a screen should visually dominate by contrast, not just position.
- Warning and error states should visually break the pattern, not blend in.
- Use sparingly: if everything stands out, nothing does.

**Red flag**:
- Primary CTA that looks like a secondary action.
- Error message styled to match body text.

**Source**: Hedwig von Restorff (1933).

---

### Cognitive Load Theory

**What**: Working memory is limited; extraneous load (clutter, decoration, redundant choices) competes with the task and is the load designers can most directly cut.

**Mobile application**:
- Reduce extraneous load before adding polish: one primary task per screen, progressive disclosure for the rest.
- Prefer recognition and smart defaults over inputs the app could infer.
- Treat dense decoration as a cost, not a feature.

**Red flag**:
- Over-decorated screens where ornament competes with the task. Name "extraneous load" as the violated principle for clutter findings.

**Source**: Sweller (1988).

---

## Nielsen's 10 Usability Heuristics (mobile adaptation)

Each of Nielsen's heuristics, adapted for mobile. Use during Mode D reviews and as a check during generation.

1. **Visibility of system status**: Users should always know what's happening. On mobile: show sync state, loading, offline, background-activity indicators. Do not let the user guess.
2. **Match between system and real world**: Language and concepts match the user's mental model, not internal system terminology. On mobile: plain language; no "record" where the user would say "item".
3. **User control and freedom**: Users should be able to leave unintended states easily. On mobile: clear back, cancel, and undo; escape hatches from modal flows.
4. **Consistency and standards**: Same things behave the same way everywhere. On mobile: platform conventions, in-app consistency, no surprise reinterpretations of standard UI.
5. **Error prevention**: Prevent errors before they happen. On mobile: smart defaults, format hints, disable invalid options, confirmation for destructive actions.
6. **Recognition rather than recall**: See above.
7. **Flexibility and efficiency of use**: Novice-friendly and power-user efficient. On mobile: gestures as accelerators; keyboard shortcuts on tablets; customizable defaults.
8. **Aesthetic and minimalist design**: Every visible element competes for attention. Remove the decorative; keep the functional.
9. **Help users recognize, diagnose, and recover from errors**: Errors in plain language, specific cause, and concrete fix. Never just "something went wrong".
10. **Help and documentation**: Help is discoverable, searchable, contextual. On mobile: inline help, not a separate manual.

**Source**: Nielsen Norman Group, https://www.nngroup.com/articles/ten-usability-heuristics/.

---

## Gestalt principles (grouping and perception)

### Proximity
Elements placed near each other are perceived as related. Use spacing, not borders, to group.

### Similarity
Elements that look alike are perceived as related. Consistent styling communicates consistent function.

### Closure
The mind completes partial shapes. Do not over-render; a suggested boundary is often enough.

### Continuity
The eye follows smooth lines and curves. Align elements along invisible baselines to guide scanning.

### Figure / ground
Foreground and background must be clearly separated. Ambiguity between the two creates cognitive load.

### Common region
Elements within a visible container are perceived as grouped even if similar elements exist outside.

**Mobile application**: spacing scale (`docs/quality-bars.md`) operationalizes proximity and closure; typographic hierarchy uses similarity; card layouts use common region.

**Red flag**:
- Form fields grouped by color instead of by spacing.
- Card visually blends into the background, making its boundary ambiguous.

**Source**: Max Wertheimer et al. (1923).

---

## Mobile-specific heuristics

### Thumb zone (Steven Hoober)

**What**: Studies of one-handed phone use show the thumb naturally reaches the bottom-center and bottom-side of the screen. Top corners are hardest.

**Mobile application**:
- Primary actions in the thumb zone.
- Frequent destinations in the thumb zone.
- Corners (especially top-right) for rare actions (settings), not primary.
- Note: on larger phones, even the bottom-center is a stretch for some users; support platform reachability modes.

**Red flag**:
- Primary "Save" button at the top-right of a content-heavy screen.

**Source**: Steven Hoober research on phone holding patterns.

---

### Interruption-resilience

**What**: Mobile use is interrupted (calls, notifications, context switches, backgrounding) more than any other medium.

**Mobile application**:
- Persist state across app backgrounding.
- Resume flows at the interrupted step, not the start.
- Auto-save user input frequently; never silently discard.
- Confirm destructive actions that cannot be undone after interruption.
- Avoid modal flows that lose context if the user must switch apps for information.

**Red flag**:
- Sign-up flow that resets if the user backgrounds the app to fetch a verification code from email.

**Source**: Mobile UX research; ISO 9241-210 context of use.

---

### One-screen-at-a-time constraint

**What**: Unlike desktop, mobile screens typically show one primary surface at a time.

**Mobile application**:
- Contextual information must be on the same screen, not assumed known from elsewhere.
- Summary before action: confirm details before destructive or expensive operations.
- Breadcrumbs and labeled navigation help orient the user when they cannot see the whole hierarchy.

**Red flag**:
- "Confirm delete" with no summary of what is being deleted.
- Step 4 of a flow that assumes the user remembers what was entered on step 1.

**Source**: Mobile IA practice; related to Miller's Law.

---

## Form and review principles

### Form design (Wroblewski)

**What**: Form usability comes from labeling, alignment, required-field marking, and error prevention — not styling.

**Mobile application**:
- Persistent visible labels (never placeholder-as-label); mark required fields before submit.
- Validate on blur with helper text; keep the primary action reachable on long forms.
- Distinguish primary from secondary actions; preserve entered data on error.

**Red flag**:
- Placeholder-only labels, required fields revealed only at submit, error signalled by color alone.

**Source**: Luke Wroblewski, *Web Form Design* (2008).

---

### Severity rating (Nielsen 0–4)

**What**: Rate each review finding 0–4 reasoned as frequency × impact × persistence (0 not a problem, 1 cosmetic, 2 minor, 3 major, 4 catastrophe).

**Mobile application**:
- Order findings by user impact, not by how much they bother you visually.
- A catastrophe (irreversible data loss, blocked task) is a 4 even if rare; a cosmetic nit is a 1 even if frequent.

**Severity crosswalk** — the skill uses three scales for different jobs. A single finding may reference more than one; this table keeps them consistent:

| Finding severity (Nielsen 0–4) | Coarse band | Weakness class (`docs/weaknesses.md`) | Effect on the 1–5 quality score (`docs/design-quality-rubric.md`) |
|---|---|---|---|
| 4 catastrophe (irreversible loss, blocked task) | High | P0/P1 | Fail or capped at 2/5 until fixed |
| 3 major | High | P1 | capped at 2/5 until fixed |
| 2 minor | Medium | P2 | lowers a dimension; rarely caps |
| 1 cosmetic | Low | P3 | lowers a dimension at most |
| 0 not a problem | — | — | none (omit from the Severity index) |

So "lifts cap: P1" on a severity-3/4 finding and the Nielsen number describe the same defect at different granularities — they are not separate problems.

**Source**: Nielsen, severity ratings for usability problems (NN/g, 1994); weakness classes and quality caps are this skill's own layers.

---

## How to apply heuristics

### During generation (Mode A, B, C, E, F)

When producing a design or spec, check each major decision against the heuristics above:

- Is the primary action placed per Fitts and thumb zone?
- Is choice bounded per Hick and chunked per Miller?
- Does the flow respect interruption-resilience?
- Is progress visible per Zeigarnik and goal-gradient?
- Are platform conventions respected per Jakob?
- Is extraneous cognitive load minimized (Cognitive Load Theory)?
- For forms, are labels, required marking, and error prevention handled (Wroblewski)?

Cite the relevant heuristic in the `Rationale for major choices` or `Pattern choices and why` block when it is the primary driver of a decision.

### During review (Mode D)

Use the Red Flag items above as a concrete violation checklist. Every red flag maps to a heuristic and should be cited in the review output with the heuristic name, not as a vague "this feels off".

For each finding, name the violated principle (including Cognitive Load Theory for clutter and Wroblewski for forms) and rate severity on the Nielsen 0–4 scale by user impact.

### Conflict resolution

When two heuristics suggest different solutions:

- State both.
- Pick one based on the user's context (`docs/context-defaults.md`).
- Explain the tradeoff in the output.

---

## Maintenance

- Add a heuristic here only when it has produced a real design decision in the field.
- Do not inflate the catalog with theoretical coverage. Each entry must pay for itself by improving specific outputs.
- Review the sources section in `docs/sources.md` when adding a heuristic; add the citation if missing.
