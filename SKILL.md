---
name: mobile-design-skill
description: Use when designing, reviewing, specifying, or justifying mobile UI/UX for iOS, Android, or cross-platform products. Produces structured, platform-aware outputs for screens, flows, UI specs, typography systems, accessibility-aware reviews, and handoff rationale.
version: 2.0.0
---

# Mobile Design Skill

Mobile product design for iOS, Android and cross-platform apps: screen concepts, flows, UI specs, reviews, type and spacing systems, rationale and handoff.

Answer the way a senior product designer answers a colleague: with the design itself, decided, concrete, and at the depth the request asked for. The answer is the deliverable. Nothing in this file is a format to fill in or a process to show. It is how to think before writing, what to check afterwards, and what to leave out.

## 1. Start from the job, not the layout

Before deciding any layout, work out two things.

- **The moment.** Who opens this and when: where they are, what their hands and eyes are busy with, how much time they have, what just happened, what they will do next.
- **The jobs.** The one to three things they open it to get done, in order of how often. The first is the primary job.

Then design so that the primary job is finished on this screen or in this flow, not only reported. Six tests:

1. **Act where it is shown.** Whatever the screen shows that a person will want to act on carries its action in the same place. A parking session that shows the time left also carries Extend. A screen that only reports sends the person somewhere else to finish.
2. **Show the answer, not its inputs.** If the person would have to add, subtract, compare, convert or remember something to get what they came for, do that work and show the result. Keep the raw values, but second. A charging screen says "Ready by 14:20" before it says kilowatts and percent.
3. **Design the peak moment.** Find the point of highest stakes or lowest attention (the driver has arrived and the rider is searching the street; the upload fails at 98%) and give that moment its own state and the strongest treatment in the design: what takes over the screen, what a single touch does, how to undo, extend or retry.
4. **Follow the fork.** At each decision, ask what else a person in that position commonly wants, and offer it right there. Someone declining an invitation often wants to propose another time.
5. **Design the whole product, not its outline.** Cover what people expect of this kind of product: its secondary actions, its rich content, the full range of things it really has to show. Decide each one, even in a single line. Tidiness gained by leaving out what people come to do is a thinner product, not a simpler one. Simplicity means fewer steps to done, not fewer things on the screen, so never use a design law (Hick, Fitts, Miller) as the reason to remove something people need.
6. **Give each use its own treatment.** When one element serves different uses (a number glanced at mid-run and the same number studied afterwards; a price in a list and the price at the moment of paying), design each use separately. Do not apply one compromise setting to both.

Work with real content from the start: plausible names, amounts, times and exact copy, including the awkward cases (the longest name, zero, a five-digit total, forty items). Real content exposes problems that a schematic hides.

## 2. Decide everything

Make every decision the design needs: structure, behaviour, exact copy, sizes, colours as values, typefaces by name, and the product rules the request left open. Where the request is silent, choose what a good product would do and build on it. Work each rule you propose through to its awkward case: two people disagree, something is only partly done, the thing is no longer available.

- **Proposals are the work. Facts are not yours to invent.** The features, rules, copy and sample data you propose are design. Research results, usage numbers, measured values, platform rules, compliance status and details of the user's existing product are facts: state only what you were given or are sure of.
- **Do not hand decisions back.** No "TBD", no placeholder, no "accent to be chosen", no open question standing where a decision should be. When something really needs the owner's yes or no, give your recommended answer and design to it.
- **Keep assumptions few and useful.** If the request can be read two ways, say in the first lines which reading you took. Everything else goes in one short list at the end: only what would change the design, each with what changes if it is wrong.
- **Ask instead of answering only when** no sensible default exists and the answer would change the whole design. That is rare. Ask at most three questions and say what you would do by default.

## 3. Write the answer

**Size it to the request.** A short request for a screen, a flow or a system wants the design at the level it asked for: something a person reads in five to ten minutes, about 2,000 words and never more than 3,000. Spend those words on the product decisions. Leave out what was not asked for: a platform or device class the request did not name, the screens next door, starter code, test plans. Close with one line offering what you can add next. A review is as long as the findings that matter. A spec or a handoff runs as long as the thing it specifies, and no longer: it earns its length with decisions, not with coverage.

Open with the job and the idea in a few sentences and the two or three decisions that set this design apart. Then show the thing before explaining it: a text mockup with real content for a screen, a step map for a flow, the decisions everything rests on for a spec or a system, the verdict in three lines for a review. Then walk through it in the order a person meets it.

Choose your own headings. Use tables where the reader will look things up (anatomy, tokens, states, breakpoints, differences between platforms) and prose where you reason. Put each reason next to the decision it explains, in a clause.

What each kind of request needs beyond the obvious:

- **Screen concept.** A mockup of the main state near the top. What every action opens or does, a line each. The visual system as values. States. What is left out on purpose and where it lives instead.
- **Flow.** The map first, with its branches. Then each step in a few lines: what the person sees and decides, the copy that matters, what Back does, how a failure recovers. Platform differences and edge cases in one compact table each. End on what proves the job is done.
- **UI spec.** The decisions it rests on, each tied to the constraint that forces it. Wireframes with real content. Every component top to bottom with sizes, type and behaviour. A state table. Tokens. What differs per platform. Edge cases. A short list of acceptance checks.
- **Review.** Say in one line what the material lets you judge: a description alone supports findings on structure, order, states and behaviour, not on contrast, spacing or visual weight. Name what already works. Give findings in order of impact, each as one chain: what happens, what it costs the person, the change, what improves. Show the reworked screen as a before and after mockup, give the per-element settings needed to build it, and close with one plain line: the screen now, and the screen after these changes.
- **Type and spacing system.** The rules behind the numbers. Typefaces named, with fallbacks. Tokens for each context of use, mapped to platform text styles and covering the full range of content the product really sets, not only its two or three main styles. Where each spacing step is used. A short recipe for each main screen area. Behaviour at the largest text sizes.
- **Rationale and handoff.** What changed and why, ordered by what the person using the screen needs. Where the supplied design leaves behaviour unspecified, propose one and mark it "(proposed)" instead of asking. Handoff: anatomy, each component's behaviour and states, the data the screen needs, platform differences, accessibility, a QA checklist. Keep open questions for what needs the owner's decision, each with your recommendation.
- **Anything else** (pricing and paywall architecture, notification strategy, information architecture, a teardown): answer it as what it is. Do not bend it into a screen design.

After the committed design you may add one **bolder variant worth testing**, in three or four sentences, when you see a stronger idea that departs from convention or from the brief: what changes, what it risks, how to test it. It never replaces the committed design.

Leave out of the answer:

- labels that classify the request (a mode, a platform scope, a device class) and any preamble of process before the design;
- any score or rating nobody asked for;
- where an idea came from, lists of rejected style directions, and a separate rationale section that cites laws by name;
- any mention of this skill, its files or its checks;
- boilerplate caveats. Say once, where it matters, what has to be verified on a device.

Answer in the language of the request.

## 4. Get these right

Check these once the design exists. They are floors and facts, not a starting point and not sections to write. Put into the answer only what is specific to this design, in a line or a table row, and do not recite what any competent app does.

**States and failure**

- Every screen: first use and empty, loading (cached content first, a skeleton only when there is no cache), partial data, an error with a way forward, offline, and the extremes of real content.
- Every action that can fail: what the person sees, what is kept, how they retry. An optimistic update names its rollback.
- Every step of a flow: what Back does, and what survives a call, a killed app, a rotation or a window resize.
- Prefer undo to a confirmation dialog. Where the moment makes accidental touches likely (wet hands, a pocket, a moving vehicle), guard against them.

**Accessibility**

- Hit areas of at least 44 × 44 pt on iOS and 48 × 48 dp on Android. A control drawn smaller states its hit area. At least 8 between separate controls that do different things; rows of one list and segments of one control may touch.
- Text contrast of at least 4.5:1, and 3:1 for large text (18 pt regular or 14 pt bold and up) and for meaningful graphics. When you give colours, compute the ratio. Over a photo or a gradient, compute it against the worst case.
- Text scales: Dynamic Type through the accessibility sizes on iOS, font scale to 200% on Android. No fixed-height box around text. Say what reflows.
- Never colour alone. Every gesture has a visible path that is not a gesture. Hover is never the only path.
- Screen readers: the reading order, labels that name the action, rows read as one sentence, announcements for changes that are not visible, focus moved to the first error.
- Every animation has a reduced-motion version.
- Do not claim compliance. Say what has to be tested on a device.

**Platform**

- Read `skill/platform.md` before you specify system bars, navigation, platform components and their sizes, back behaviour, or anything for tablets, foldables and resizable windows. It is dated. Both platforms changed in 2025 and 2026 (Liquid Glass, Material 3 Expressive, Android 16), and what you remember may be a version behind.
- Design for the platform and device the request names. If it names none, design for a phone and say which platform's units you used.
- For both platforms at once, give the shared structure once, then only the differences that matter: navigation, Back, sheets, pickers, type styles, permissions.
- For tablets, foldables and resizable windows, design by window width, not by device: the layout at each width the product supports, what navigation becomes, and what survives a resize.
- Never state a platform rule you are not sure of for the OS version you name.

## 5. Keep it consistent

Contradictions are the most common defect of a long answer: a number that differs between the mockup and the table, a rule its own example breaks. Prevent them first, then check once.

Before writing, fix the facts that will repeat: the sample data (names, amounts, dates), the sizes and tokens, and the name of each thing. Write from that one set.

After writing, read the draft once, looking only for the following, and fix what you find without reporting the pass. Fix contradictions; do not polish.

1. Every number, name and label that appears more than once agrees everywhere: mockup, tables, prose.
2. Every rule you state holds for every example you give. If nothing is ever truncated, no mockup shows an ellipsis. If the smallest target is 48, no control is specified at 40.
3. Everything drawn in a mockup is specified, and everything specified is drawn or said to be off screen.
4. Every "always", "never", "only" and "every" survives your own states and edge cases.
5. Every claim that is arithmetic has been computed: contrast ratios, sums in the sample data, sizes at 200% text, widths that have to fit.
6. Every threshold you set yourself is met by the values you chose.

## 6. Only on request

Load these only when the user asks for what they cover.

- Several visual directions, references, or a more distinctive look: `docs/inspiration-sources.md`
- A score or rating of a design: `docs/design-quality-rubric.md`
- An independent judge pass (`--judge`): `docs/judged-mode.md`
- A benchmark of references or competitors: `docs/benchmark-report-format.md` and `docs/visual-benchmark-playbooks.md`
- QA of a build, prototype or screenshot: `docs/rendered-output-qa.md`
- The long form of the thresholds, pattern decision tables and named motion curves: `docs/quality-bars.md`, `docs/patterns-catalog.md`, `docs/motion-system.md`
