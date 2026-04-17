# Quality Bars

This document defines concrete numeric thresholds the skill must meet. Principles in `docs/principles.md` describe intent; this file describes measurable minimums.

Use these values as defaults in every mode output. When deviating from a bar, state the reason explicitly.

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

### Dynamic Type / font scale

- iOS: every text role must respond to Dynamic Type (Larger Text setting up to XXXL / Accessibility sizes).
- Android: every text role must scale with the system font-scale setting up to 200%.
- Layout must not clip, overlap, or hide critical content at maximum scaling.

---

## Touch targets

### Minimum sizes

| Platform | Minimum | Preferred |
|----------|---------|-----------|
| iOS | 44 × 44 pt | 48 × 48 pt |
| Android | 48 × 48 dp | 56 × 56 dp |

### Spacing between targets

- Minimum gap between independent tap targets: **8 pt / 8 dp**.
- Preferred gap: **12 pt / 12 dp** when the targets have similar visual weight.

### Tap area vs visual size

- Visual size may be smaller than the tap area as long as the hit region meets the minimum.
- Never reduce the hit region below the minimum to match a smaller visual.

### Thumb reach

- On phones, assume right- and left-handed one-handed use.
- Primary actions belong in the thumb-reachable lower half of the screen when feasible.
- Avoid placing destructive actions adjacent to primary actions without a gap or a visual break.

---

## Color and contrast (WCAG 2.2 AA)

| Element | Minimum contrast ratio |
|---------|------------------------|
| Body text (under 18pt or under 14pt bold) | 4.5:1 |
| Large text (≥18pt regular or ≥14pt bold) | 3:1 |
| UI components and meaningful graphics | 3:1 |
| Focus indicators | 3:1 against adjacent colors |
| Disabled elements | No minimum, but must be visually distinct |

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
