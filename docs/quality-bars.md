# Quality Bars

This document defines concrete numeric thresholds the skill must meet. Principles in `docs/principles.md` describe intent; this file describes measurable minimums.

Every bar is marked **floor** or **default** where the distinction has ever been disputed. A **floor** is a value nothing may sit under, whatever component it is; a **default** is what to use unless a platform component or a stated context legitimately differs. Reading a default as a floor flags correct work — measured at three of six correct decisions wrongly flagged before these annotations existed — and reading a floor as a default ships a defect.

Use these values as defaults in every mode output. When deviating from a bar, state the reason explicitly — and note that stating it keeps the artifact honest without making the value right: the contradicted-value cap in `docs/design-quality-rubric.md` still applies unless the user's own input requires the deviation.

Bars are drawn from Apple Human Interface Guidelines, Material Design 3, WCAG 2.2, W3C mobile guidance, and established typography research. Where guidance differs between iOS and Android, both thresholds are listed.

---

## Typography

### Minimum sizes (body and reading content)

| Role | Minimum | Preferred | Notes |
|------|---------|-----------|-------|
| Body text | 15pt (iOS) / 14sp (Android) | 16–17pt / 16sp | Smaller only for dense reference UI with explicit audience consent |
| Labels (form fields, metadata) | 12pt / 12sp | 13–14pt / 14sp | Below 12 is a readability failure for most users |
| Caption / helper | 11pt / 11sp | 12pt / 12sp | Never the only indicator of critical information |
| Button / action text | 15pt / 14sp | 17pt / 16sp | Large enough to read mid-task without leaning in |
| Screen title | 22pt / 20sp | 28–34pt / 24sp | Anchored by platform title conventions |

### Line-height ratios

| Context | Ratio (multiplier of font size) |
|---------|---------------------------------|
| Body reading text | 1.4 – 1.6 |
| Dense list rows | 1.2 – 1.35 |
| Headings | 1.1 – 1.25 |
| Multi-line labels | 1.3 – 1.45 |

### Line length

- Optimal for reading: 45–75 characters per line (measure at default text size).
- On phone-width screens this naturally lands around 40–60 characters; do not artificially widen.

### Type scale

- Minimum ratio between adjacent roles: **1.125× (major second)**.
- Preferred ratio between display and body: **at least 1.5×**.
- Use role-based tokens (Display, Title, Body, Caption), not ad-hoc sizes.

**Anchor the scale at body, then pick the ratio by density.** Body is 17 pt (iOS) / 16 sp (Android); every other role is derived from it rather than chosen independently.

| Density | Ratio | Fits |
|---------|-------|------|
| Dense | 1.125 | operational lists, tables, dashboards, anything compared row to row |
| Default | 1.2 | general consumer product |
| Spacious | 1.25 | reading, marketing, onboarding, low-information screens |

Round every derived size to a whole point; a scale that emits 21.25 pt has not been applied.

### Role to platform text style

A type role that names no platform style ships as a hardcoded size and stops scaling. Map every role.

| Role | iOS Dynamic Type style | Material 3 type role |
|------|------------------------|----------------------|
| Display | Large Title | `displaySmall` / `headlineLarge` |
| Title | Title 1 – Title 3 | `titleLarge` / `headlineSmall` |
| Section heading | Headline | `titleMedium` |
| Body | Body | `bodyLarge` |
| Secondary body | Callout / Subheadline | `bodyMedium` |
| Label | Footnote | `labelLarge` / `labelMedium` |
| Caption | Caption 1 – Caption 2 | `labelSmall` / `bodySmall` |

Custom faces still map to these styles: take the platform style's scaling behaviour and substitute the face, rather than fixing a point size.

### Tracking at size

Tracking compensates optically for size; it is not a style choice made once for the whole scale.

| Size | Tracking |
|------|----------|
| Display, ≥ 28 pt | negative, −0.5 % to −1.5 % of size |
| Body and UI text, 15–17 pt | 0 — the face's default |
| Labels and captions, ≤ 12 pt | positive, +0.5 % to +2 % |
| All-caps at any size | positive, +5 % to +10 % |

The platform system faces already carry per-style tracking: on iOS the Dynamic Type styles supply it, and Material 3 assigns a `letterSpacing` per type role. **A custom face must supply its own tracking table** — inheriting the system face's values with a different face is a defect. When the design keeps the platform face, say so explicitly rather than leaving tracking unstated.

### Dynamic Type / font scale

- iOS: every text role must respond to Dynamic Type (Larger Text setting up to XXXL / Accessibility sizes).
- Android: every text role must scale with the system font-scale setting up to 200%.
- Layout must not clip, overlap, or hide critical content at maximum scaling.

---

## Touch targets

### Minimum sizes

| Platform | Minimum | Preferred | |
|----------|---------|-----------|---|
| iOS | 44 × 44 pt | 48 × 48 pt | minimum is a **floor**, preferred is a **default** |
| Android | 48 × 48 dp | 56 × 56 dp | minimum is a **floor**, preferred is a **default** |

**The minimum governs the hit region, not the drawn control.** A 24 pt glyph inside a 44 pt target passes; a 44 pt-looking control with a 32 pt hit region does not. Platform components are frequently drawn under the minimum — a segmented control is 32 pt tall on iOS — and that is not a violation when the hit region is padded out to the floor.

**So state the hit region whenever the drawn size is below the minimum.** A spec that says "segmented control, 32 pt" and stops has not made a hit region reviewable, and it will be read as a violation — correctly, because nothing in it says otherwise. One clause fixes that: "32 pt drawn, 44 pt hit region".

### Spacing between targets

- Minimum gap between separately-consequenced adjacent controls: **8 pt / 8 dp**. **Floor.**
- Preferred gap: **12 pt / 12 dp** when the targets have similar visual weight. **Default.**

**What this bar is for, and what it does not govern.** It protects against a mis-tap that costs the user something different from what they intended — two buttons side by side, a destructive action beside a benign one, a small control near another small control. It does **not** govern the seams inside one repeating structure whose cells each meet the size floor: contiguous list rows, calendar cells, segmented-control segments, and bottom-navigation destinations ship edge to edge on both platforms, and requiring 8 pt between them would contradict HIG and Material 3 rather than follow them.

Two questions decide it. Do the neighbours carry **different consequences**, and is either one **at or under the size floor**? A yes to either means the gap bar applies. A repeating row of same-consequence cells, each above the floor, is within scope with no gap at all.

Adjacency of a destructive action to a primary one is a separate rule and is never waived by this one — see `Thumb reach` below.

### Thumb reach

- On phones, assume right- and left-handed one-handed use.
- Primary actions belong in the thumb-reachable lower half of the screen when feasible.
- Avoid placing destructive actions adjacent to primary actions without a gap or a visual break.

---

## Color and contrast (WCAG 2.2 AA)

| Element | Minimum contrast ratio | |
|---------|------------------------|---|
| Body text (under 18pt or under 14pt bold) | 4.5:1 | **floor** |
| Large text (≥18pt regular or ≥14pt bold) | 3:1 | **floor** |
| UI components and meaningful graphics | 3:1 | **floor** |
| Focus indicators | 3:1 against adjacent colors | **floor** |
| Disabled elements | No minimum, but must be visually distinct | — |

### Non-color indicators

- Color must never be the only channel for meaning.
- Every colored status (error, success, warning) must also carry a text label, icon, shape, or pattern.
- Red-green combinations require extra non-color reinforcement (color-blindness incidence ~8% in men).

---

## Motion

### Durations

| Interaction | Duration |
|-------------|----------|
| State change on tap (button press) | 100–150 ms |
| Small element movement (chip, badge) | 150–200 ms |
| Screen-level transition | 200–300 ms |
| Modal / sheet entry | 250–350 ms |
| Full-screen navigation | 300–400 ms |

### Easing

- Entering elements: ease-out (decelerate).
- Exiting elements: ease-in (accelerate).
- Elements entering and exiting together: ease-in-out (standard curve).
- Avoid linear motion for user-initiated interactions; it feels mechanical.

**Name the curve, not the adjective.** "Ease-out" is a family, not a value: state the platform token or its control points — an M3 easing token, a `cubic-bezier`, a SwiftUI spring preset, or Compose `dampingRatio`/`stiffness`. The tables are in `docs/motion-system.md`, which also carries how a duration scales with travel distance and element size, and the stagger caps. Durations stay here.

### Signature transition

A product may designate **one** recurring transition as its motion signature — the mechanism behind "motion personality" in `docs/design-quality.md`.

- It takes the top of its own band from the table above (300 ms for a screen-level transition, 350 ms for a sheet, 400 ms for full-screen navigation). It never borrows a band above itself, and 400 ms is the ceiling for any signature.
- It never applies to tap feedback, which stays at 100–150 ms. Feedback that waits on a signature is a defect, not a personality.
- One signature per product, repeated in named places. A second one is decoration.
- It ships with a reduced-motion fallback like every other transition.

The bands in this table are the authority. A brand adjective selects *which* interaction carries the signature and *which* easing curve it uses — never a longer duration. Name that curve as a platform token or its control points from `docs/motion-system.md`.

### Reduced motion

- Respect the OS "Reduce motion" setting on iOS and "Remove animations" on Android.
- Replace parallax, zoom, and slide transitions with a cross-fade when reduced motion is on.
- Do not rely on animation to convey state; state must be readable statically.

---

## Spacing

### Scale

- Use a 4-based or 8-based scale, not ad-hoc values.
- Canonical steps: 4, 8, 12, 16, 24, 32, 40, 48, 64.
- Rem-style alternative: 0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4 (× base).

### Minimums

| Gap | Minimum |
|-----|---------|
| Between adjacent tap targets | 8 pt / 8 dp |
| Between form fields | 12–16 pt / 12–16 dp |
| Between content and screen edge | 16 pt / 16 dp (phone) |
| Between sections | 24 pt / 24 dp |
| Between a label and its field | 4–8 pt / 4–8 dp |

### Baseline grid

The spacing scale and the type scale have to land on the same grid, or every screen needs manual nudging.

- **4 pt baseline grid** for type; **8 pt layout grid** for blocks and components. Every spacing step above is a multiple of 4.
- **Round every line-height box to a multiple of 4.** Body at 17 pt with a 1.5 ratio computes to 25.5 pt; ship 24 or 28, not 25.5. The rounded box, not the raw multiplication, is what the spacing steps stack against.
- A text block's spacing is measured **between line-height boxes**, not between glyphs. A 16 pt gap under a heading whose box already carries 6 pt of internal leading reads as 22.
- When a value cannot land on the grid — an icon's optical centre, a platform component's fixed height — say so where it happens instead of bending the whole scale around it.

### Columns and gutters

| Width | Columns | Margin | Gutter |
|-------|---------|--------|--------|
| Compact (phone) | 4 | 16 pt | 16 pt |
| Medium | 8 | 24 pt | 24 pt |
| Expanded | 12 | 24–32 pt | 24 pt |

A phone layout that never mentions columns is usually fine — one column and a margin is a legitimate grid. State the columns when the screen puts two or more things side by side, because that is where the gutter has to be decided rather than eyeballed.

### Optical alignment

Geometric alignment and optical alignment disagree, and the eye follows the second one.

- **Centre a triangle or a circle optically, not by bounding box.** A play glyph inside a round button sits ~1–2 % of the button's width right of geometric centre.
- **Align text to cap height or baseline**, not to the line-height box, when it sits next to an icon or an avatar.
- **Round shapes overshoot**: a circle needs ~2 % more diameter than a square to read as the same size, and the same applies to a pill next to a rectangle.
- **Hang punctuation** — quotes and bullets sit outside the text edge so the letters, not the marks, form the column edge.
- Optical corrections are stated as values in the spec ("nudge 1 pt right"), never left to implementation taste.

### Density reasoning

- Dense layouts are appropriate for comparison, scanning, and reference tasks.
- Sparse layouts are appropriate for focus, confidence, and low cognitive load.
- Density is a function of task, not aesthetic; see anti-pattern 4 in `examples/anti-patterns.md`.

---

## Forms and input

### Labels

- Every input must have a persistent visible label (not placeholder-only).
- Placeholder text is a hint, not a label.
- Required fields must be marked before submission, not discovered via validation error.

### Error handling

- Errors must appear inline, adjacent to the offending field.
- Error text must include what went wrong AND how to fix it.
- Errors must not rely on color alone (see non-color indicators above).
- Validation should be on blur or on submission attempt, not on every keystroke, unless format requires it (card number, phone).

### Keyboard and input types

- Use the most specific keyboard (`email`, `number`, `tel`, `url`, `decimal`) for the field's data.
- Enable autofill, autocomplete, and password manager integration where applicable.
- Never block paste into password or code fields.

### Completion affordance

- For forms longer than one screen, provide a persistent or sticky primary action.
- The primary action text must describe what it does ("Create account", "Save changes"), not just "Submit" or "OK".

---

## States

### Required states per mode

Every screen or spec covering interactive content must address:

- **Default**: normal data present
- **Empty**: no data yet; includes onboarding empty state if applicable
- **Loading**: initial load, refresh, and background fetch
- **Error**: network, validation, or server error
- **Offline**: degraded functionality when applicable

### Loading behavior thresholds

| Wait time | Minimum UI response |
|-----------|---------------------|
| 0–100 ms | Immediate, no special indicator needed |
| 100 ms – 1 s | Inline feedback (button state, skeleton shimmer) |
| 1 s – 10 s | Explicit loading indicator with context |
| 10 s+ | Progress indication with ability to cancel or background |

### Skeleton vs spinner

- Skeleton: prefer when the layout is known in advance (list, card, detail).
- Spinner: prefer when the outcome is unknown or the operation is atomic (save, submit).
- Skeletons should not animate flashily; shimmer is fine, pulsing quickly is not.

---

## Navigation

### Back behavior

- Back navigation must preserve user-entered data unless the user explicitly discards.
- Android hardware back and iOS edge-swipe must behave consistently with in-app back affordances.
- Unsaved changes must prompt or auto-save; silent loss is a failure.

### Tab bar vs drawer vs bottom nav

- Phone apps: bottom navigation with 3–5 primary destinations is the default.
- Above 5 destinations: reconsider the information architecture; add "More" rather than a 6th tab.
- Navigation drawers on phone should only be used when bottom nav cannot fit the information architecture, not as a hiding place for features.

### Deep links and resumption

- Each screen must be reachable via a coherent deep link or resumption path.
- App relaunch should restore the last meaningful state for interrupted flows.

---

## Accessibility specifics

### Labels and semantics

- Every interactive element must have an accessible label (iOS: accessibilityLabel; Android: contentDescription).
- Labels describe the action ("Delete item"), not the appearance ("Trash icon").
- Group related elements with accessibility containers where appropriate.

### Focus order

- Focus must follow visual reading order (top-left to bottom-right, top-to-bottom).
- Modals and sheets must trap focus until dismissed.
- After dismissing a modal, focus returns to the trigger element.

### Announcements

- State changes that are not visually obvious must announce to assistive technology (for example, new items loaded, error raised, form submitted).
- Avoid announcing every keystroke or every scroll position.

### Gesture alternatives

- Every gesture (swipe, drag, long-press) must have a button or menu alternative.
- Custom gestures must be discoverable through onboarding, hints, or a help affordance.

---

## Platform-specific anchors

### iOS

- Navigation bar height: 44pt (compact), 96pt (large title).
- Tab bar height: 49pt (standard), 83pt (with safe area on home-bar devices).
- Safe area insets must be respected at the top (notch, Dynamic Island) and bottom (home indicator).
- Minimum 44pt between the home indicator and the nearest interactive element.

### Android

- App bar height: 56dp (standard), 64dp (medium), 152dp (large).
- Bottom navigation: 80dp total height.
- Edge-to-edge content must handle the system bars correctly with `WindowInsets`.
- FAB size: 56dp standard, 40dp mini, 96dp extended minimum width.

---

## Large-screen and adaptive bars

Apply these whenever the resolved device class is anything other than phone-only. Full guidance lives in `docs/adaptive-layout.md`; these are the numbers.

### Width classes

| Class | Width | Panes |
|-------|-------|-------|
| Compact | < 600 dp (iOS: compact size class) | 1 |
| Medium | 600–839 dp | 1, or 2 if the detail pane stays ≥ 320 dp |
| Expanded | ≥ 840 dp | 2, plus a supporting pane above ~1200 dp |

The 600 / 840 dp values are Android's official window size class breakpoints. iPadOS Slide Over and narrow Split View return a tablet to **compact** width at runtime, so a compact layout is never optional on tablet.

### Pane and column sizes

| Element | Size |
|---------|------|
| Reading column (body text) | 640–720 pt maximum — the 45–75 character bar, expressed as width |
| List pane in a list-detail layout | 320–400 pt |
| Navigation rail (medium width) | 80 dp |
| Sidebar / standard drawer (expanded width) | 240–360 dp |
| Screen margin | 16 pt compact / 24 pt medium / 24–32 pt expanded |
| Grid columns | 2 compact / 4–6 medium / 6–8 expanded |

Wider screens get **more columns or wider margins, never longer lines**. A single column stretched to 1000 pt fails the line-length bar at every text size.

### Input and touch

- Touch minimums are unchanged at every width: 44 pt (iOS) / 48 dp (Android). A pointer being more precise is never a reason to shrink a target.
- Hover states are additive; hover is never the only path to an action.
- Every drag-and-drop affordance has a non-drag equivalent.

### Resize

- Scroll position, selection, in-progress input, and open sheets survive a width change. Multitasking resize is frequent, not exceptional.
- Both the two-pane state and its collapsed state define back-navigation behaviour.
- The detail pane has its own empty state; a blank pane at launch is a defect.

---

## How to apply these bars

1. When generating a design (Mode A, C, E), use these values as defaults unless the user has provided stronger constraints.
2. When reviewing a design (Mode D), compare observed values against these bars; flag any deviation without a stated reason as an issue.
3. When writing a rationale or spec (Mode C, F), cite the specific bar a decision respects or deviates from.
4. When self-reviewing (Step 9 in the workflow), confirm at least that touch targets, contrast, line-heights, and state coverage are addressed against these bars.

---

## Maintenance

- Bars are reviewed when a referenced standard (HIG, Material 3, WCAG) publishes a material change.
- Deviations between iOS and Android are tracked as two rows, not averaged.
- Do not soften a bar for stylistic reasons. If a real product constraint requires softening, document it in the product's own design system rather than here.
