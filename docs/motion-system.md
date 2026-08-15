# Motion System (curves, springs, and scaling)

`docs/quality-bars.md` owns the **durations** and the 400 ms ceiling. This document answers the three questions that file does not: **which curve**, **which spring**, and **how a duration changes with travel distance and item count**.

Load it from step 5.5 when committing a motion signature, and from step 9 when checking motion against the bars. Nothing here raises a duration band; a curve is a shape, not a licence for a longer animation.

Every token name and numeric constant below is **library- and OS-version-bound** (guardrail 16). Name the version a recommendation assumes when it materially changes the answer, and verify a token exists in the version the project ships before stating it does.

---

## 1. Two ways to specify motion

| | Tween (duration + easing curve) | Spring (physics) |
|---|---|---|
| Specified by | a duration and a curve | stiffness and damping, or duration and bounce |
| Deterministic end time | yes | approximately |
| Interruptible mid-flight | badly — restarts or jumps | naturally — velocity carries |
| Use for | state changes, fades, timed reveals, progress | anything the user drags, throws, or can interrupt; position changes that should feel physical |

**Rule**: if the user's finger can be on it, use a spring. If it runs on its own to a known end, use a tween with a named curve.

---

## 2. Named curves — Material 3

| Token | cubic-bezier | Use for |
|-------|--------------|---------|
| `standard` | (0.2, 0, 0, 1) | the default for elements that begin and end on screen |
| `standard decelerate` | (0, 0, 0, 1) | elements entering the screen |
| `standard accelerate` | (0.3, 0, 1, 1) | elements leaving the screen |
| `emphasized decelerate` | (0.05, 0.7, 0.1, 1) | an entering element that should read as the subject of the transition |
| `emphasized accelerate` | (0.3, 0, 0.8, 0.15) | that subject leaving |
| `emphasized` | not a single cubic-bezier | M3 specifies it as a two-segment curve; use the platform token rather than approximating it with one bezier |

Legacy Material easing, still the default in much shipped code: `FastOutSlowIn` = (0.4, 0, 0.2, 1), exposed in Compose as `FastOutSlowInEasing`.

**M3 duration tokens** run `short1` 50 ms, `short2` 100, `short3` 150, `short4` 200, `medium1` 250, `medium2` 300, `medium3` 350, `medium4` 400 — the same ladder as the bands in `docs/quality-bars.md`. The `long*` and `extraLong*` tokens sit above this skill's 400 ms ceiling and are not used for the interactions it covers.

---

## 3. Named curves and springs — Apple platforms

Apple's idiom is springs, not cubic-beziers. Matching an iOS transition to an M3 bezier is a cross-platform smell: share the *intent* and split the implementation.

| API | Parameters | Notes |
|-----|------------|-------|
| `Animation.easeOut(duration:)` / `.easeIn` / `.easeInOut` | duration | the tween path; use when the end time must be known |
| `Animation.timingCurve(_:_:_:_:duration:)` | four control points | when a design system supplies a bezier |
| `.smooth`, `.snappy`, `.bouncy` (iOS 17+) | none | preset springs: no bounce, slight bounce, pronounced bounce |
| `Animation.spring(duration:bounce:)` (iOS 17+) | duration, bounce 0–1 | `bounce: 0` is `.smooth`, ~0.15 is `.snappy`, ~0.3 is `.bouncy` |
| `Animation.spring(response:dampingFraction:blendDuration:)` | response, damping | the pre-iOS 17 form, still common |
| `UISpringTimingParameters(dampingRatio:)` with `UIViewPropertyAnimator` | damping ratio | UIKit |

**The spring presets default above this skill's ceiling** — their perceptual duration is half a second. Pass an explicit duration from the band the interaction belongs to rather than taking the default.

---

## 4. Springs — Jetpack Compose

| Constant | Value | Reads as |
|----------|-------|----------|
| `Spring.DampingRatioNoBouncy` | 1.0 | settles without overshoot |
| `Spring.DampingRatioLowBouncy` | 0.75 | a hint of overshoot |
| `Spring.DampingRatioMediumBouncy` | 0.5 | visible bounce |
| `Spring.DampingRatioHighBouncy` | 0.2 | playful; rarely right for utility UI |
| `Spring.StiffnessHigh` | 10000 | fast, tight |
| `Spring.StiffnessMedium` | 1500 | the default |
| `Spring.StiffnessMediumLow` | 600 | slower settle |
| `Spring.StiffnessLow` | 200 | slow, expressive |

`spring(dampingRatio = …, stiffness = …)` for physical motion; `tween(durationMillis = …, easing = …)` for timed motion.

**Damping is where character lives.** A brand adjective picks the damping ratio and the curve; it never picks a longer duration.

---

## 5. Duration scales with distance and size

A single duration for every transition makes short moves feel sluggish and long moves feel rushed.

- **Within the band its interaction belongs to** (`docs/quality-bars.md`), take the **low end for short travel and small elements**, the **high end for long travel and large elements**.
- Practical split for phone-width screens: travel under ~100 pt takes the low end; travel across most of the screen takes the top of the band; a full-screen push takes the navigation band.
- **A larger element needs longer than a smaller one over the same distance** — a full-width sheet and a chip do not share a duration.
- The band is a hard boundary. Scaling happens inside it, never past it.

---

## 6. Stagger

| Rule | Value |
|------|-------|
| Delay between adjacent items | 20–40 ms |
| Total stagger budget for one group | ≤ 200 ms |
| Items actually staggered | the first 5–7; the remainder arrive together |

Stagger is `delay × count`, so an uncapped list turns a 200 ms reveal into a two-second one at item fifty. Cap the count, not just the delay.

**Never stagger content the user is waiting on.** A staggered list of search results delays the answer to make the arrival look nice.

---

## 7. Reduced motion

| Motion | Replacement when reduced motion is on |
|--------|----------------------------------------|
| Slide, push, parallax | cross-fade, or an instant change |
| Zoom or scale transition | cross-fade at constant scale |
| Spring with bounce | the same move with no overshoot, or a cross-fade |
| Autoplaying or looping motion | paused, with a control to play |

Read the setting rather than assuming: `UIAccessibility.isReduceMotionEnabled` / SwiftUI `@Environment(\.accessibilityReduceMotion)` on Apple platforms, and the system animator duration scale on Android. Motion is never the only carrier of a state change (WCAG 2.3.3, and the state-coverage bar).

---

## 8. What this document does not change

- Durations, bands, and the 400 ms ceiling stay in `docs/quality-bars.md`.
- Tap feedback stays at 100–150 ms regardless of the signature.
- One signature transition per product, repeated in named places.
- Every named curve ships with its reduced-motion fallback stated.

---

## 9. Sources

- [Material 3: Easing and duration](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs)
- [Material 3: Transitions](https://m3.material.io/styles/motion/transitions/transition-patterns)
- [Apple HIG: Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- [SwiftUI: Animation](https://developer.apple.com/documentation/swiftui/animation)
- [Jetpack Compose: Animation](https://developer.android.com/develop/ui/compose/animation/introduction)
- [WCAG 2.2: Animation from Interactions (2.3.3)](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
