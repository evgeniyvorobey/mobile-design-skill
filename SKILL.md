---
name: mobile-design-skill
description: Use when designing, reviewing, specifying, or justifying mobile UI/UX for iOS, Android, or cross-platform products. Produces structured, platform-aware outputs for screens, flows, UI specs, typography systems, accessibility-aware reviews, and handoff rationale.
version: 2.2.0
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

## 2. Decide everything, and write it to build from

Make every decision the design needs: structure, behaviour, exact copy, sizes, colours as values, typefaces by name, and the product rules the request left open. Where the request is silent, choose what a good product would do and build on it.

- **Proposals are the work. Facts are not yours to invent.** The features, rules, copy and sample data you propose are design. Research results, usage numbers, measured values, platform rules and details of the user's existing product are facts: state only what you were given or are sure of.
- **Do not hand decisions back.** No "TBD", no placeholder, no open question standing where a decision should be. When something really needs the owner's yes or no, give your recommended answer and design to it. If the request can be read two ways, say in the first lines which reading you took.

Be thorough: the reader will build from your answer, so cover the states and the edge cases and leave no open questions. Around 3,000 words is fine for a screen, a flow, a spec or a system. A review is as long as the findings that matter.

Open with the job and the idea in a few sentences and the two or three decisions that set this design apart. Then show the thing before explaining it: a text mockup with real content for a screen, a step map for a flow, the decisions everything rests on for a spec or a system, the verdict in three lines for a review.

A type and spacing system gives the rules behind the numbers; typefaces named, with fallbacks; tokens for each context of use, mapped to platform text styles and covering the full range of content the product really sets, not only its two or three main styles; where each spacing step is used; a short recipe for each main screen area; and behaviour at the largest text sizes. On the tightest row the content comes before the system's own tokens: when a row does not fit at the narrowest width, tighten the gaps and the size of the figures before you truncate or abbreviate what the person reads.

A review says in one line what the material lets it judge (a description alone does not support findings on contrast, spacing or visual weight), gives its findings in order of impact, each as one chain (what happens, what it costs the person, the change, what improves), and shows the reworked screen as a before and after mockup. A request that is not a screen (pricing, notification strategy, information architecture) is answered as what it is. After the committed design you may add one bolder variant worth testing, in three or four sentences: what changes, what it risks, how to test it.

Leave out labels that classify the request and any preamble of process, any score or rating nobody asked for, where an idea came from and lists of rejected directions, any mention of this skill, its files or its checks, and boilerplate caveats. Answer in the language of the request.

## 3. Floors and facts

Check these once the design exists. They are floors, not sections to write: put into the answer only what is specific to this design.

- **States.** Every screen has its first use and empty state, loading, an error with a way forward, offline, and the extremes of real content. Every action that can fail says what is kept and how to retry. Every step of a flow says what Back does and what survives a call, a killed app or a rotation.
- **Accessibility.** Hit areas of at least 44 × 44 pt on iOS and 48 × 48 dp on Android. Text contrast of at least 4.5:1, and 3:1 for large text and for meaningful graphics; when you give colours, compute the ratio. Text scales through the accessibility sizes on iOS and to 200% on Android, with no fixed-height box around it. Do not lock a screen to portrait or to landscape unless the task cannot be done in the other orientation; a one-handed grip and accidental rotation are not such reasons, because the system's rotation lock already covers them. Where you do lock, say why. Never colour alone, and every gesture has a visible path that is not a gesture. Do not claim compliance; say what has to be tested on a device.
- **Platform.** Read `skill/platform.md` before you specify system bars, navigation, platform components and their sizes, back behaviour, a custom gesture, a permission request, location, or anything for tablets, foldables and resizable windows. It is dated. Both platforms changed in 2025 and 2026 (Liquid Glass, Material 3 Expressive, Android 16), and what you remember may be a version behind. Design for the platform and device the request names; if it names none, design for a phone and say which platform's units you used. Never state a platform rule you are not sure of for the OS version you name.

## 4. Keep it consistent

Contradictions are the most common defect of a long answer. Before writing, fix the facts that will repeat: the sample data (names, amounts, dates), the sizes and tokens, and the name of each thing. Write from that one set.

After writing, read the draft once for contradictions only, and fix what you find without reporting the pass: a number, name or label that differs between the mockup, the tables and the prose; a rule that one of your own examples or states breaks; an "always", "never", "only" or "every" that your own design, its states or its edge cases break; a figure that is arithmetic and was not computed.

## 5. Only on request

Load these only when the user asks for what they cover.

- Several visual directions, references, or a more distinctive look: `docs/inspiration-sources.md`
- A score or rating of a design: `docs/design-quality-rubric.md`
- An independent judge pass (`--judge`): `docs/judged-mode.md`
- A benchmark of references or competitors: `docs/benchmark-report-format.md` and `docs/visual-benchmark-playbooks.md`
- QA of a build, prototype or screenshot: `docs/rendered-output-qa.md`
- The long form of the thresholds, pattern decision tables and named motion curves: `docs/quality-bars.md`, `docs/patterns-catalog.md`, `docs/motion-system.md`
