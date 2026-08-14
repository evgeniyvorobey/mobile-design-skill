# Adaptive Layout (device class beyond the phone)

This document is the skill's tablet, foldable, and adaptive-layout layer. Load it from step 3 of the workflow whenever the resolved device class is anything other than phone-only.

Platform scope answers *which OS*. Device class answers *how much width the layout gets and what input is available*. They are independent axes: an iOS tablet and an Android tablet share more layout structure with each other than either shares with its own phone.

The rest of the skill still applies unchanged. Nothing here relaxes touch minimums, contrast, Dynamic Type, state coverage, or the pattern discipline in `patterns-catalog.md`.

This document holds the width classes, the canonical layouts, and the multitasking rules. The decision matrices that choose between their large-screen siblings — layout, detail-pane state, secondary content, navigation, overlays, action placement, columns, and cross-pane drag — are `docs/patterns-catalog.md` §15. The numbers are in `docs/quality-bars.md`.

---

## 1. Device class and its signals

| Device class | Meaning |
|--------------|---------|
| Phone | Compact width in both orientations. The skill's default when nothing indicates otherwise. |
| Tablet | Regular width available in at least one orientation; multitasking can return it to compact at any moment. |
| Foldable | Width changes at runtime as the device folds and unfolds; both states are primary. |
| Adaptive | One layout must serve every width because the product ships to all of them. |

Resolve to tablet, foldable, or adaptive when the request names any of:

- iPad, iPadOS, tablet, Android tablet, Chromebook, large screen, big screen
- Split View, Slide Over, Stage Manager, multi-window, multitasking, freeform
- foldable, Fold, flip, unfolded, hinge, dual-screen, posture
- landscape-primary, external display, desk mode, keyboard case, Apple Pencil, stylus
- a use context that implies a mounted or two-handed device: kiosk, point of sale, clinician or bedside, field technician, warehouse, classroom, studio, cockpit, control room

When the request names none of these, stay phone-first — but say so as a **reversible assumption** ("compact width only; a regular-width layout can be added on request"), never as a closed statement. Phone-first is a default, not a finding.

Device class does not enter the context-defaults precedence order. Precedence resolves conflicts between context dimensions (safety, domain, use-context, audience, platform); device class rarely conflicts with them. It is a trigger, not a rank.

---

## 2. Width classes

Design against width, not against a device name. A device name is unstable — an iPad in Slide Over is a compact-width surface, and a foldable is two devices.

| Class | Width | Typical | Layout consequence |
|-------|-------|---------|--------------------|
| Compact | < 600 dp / compact size class | phones; iPad in Slide Over or narrow Split View; unfolded-inner-display-off | One pane. Everything the phone layout already does. |
| Medium | 600–839 dp | small tablets, large phones in landscape, foldables unfolded, half-screen Split View | One pane with more generous margins, or a two-pane layout only if the detail pane stays ≥ 320 dp |
| Expanded | ≥ 840 dp | tablets in landscape, desktop-class windows | Two panes as the default; a third supporting pane above ~1200 dp |

The 600 / 840 dp breakpoints and the compact/medium/expanded naming are Android's official window size classes; Apple expresses the same distinction as compact vs regular size classes. Height classes exist too (compact < 480 dp), and matter mainly for sheets, keyboards, and full-screen media.

**Never map a layout to a device model.** Map it to a width class, then state what happens at each class the product supports.

---

## 3. Canonical layouts

Pick from the established set; do not invent a large-screen pattern where one of these fits.

| Layout | Use when | Avoid when | Collapse rule at compact |
|--------|----------|------------|--------------------------|
| List-detail | The user moves repeatedly between a collection and its items (mail, messages, files, patients, orders) | Items are consumed once and never compared | Becomes two screens with normal push navigation; the selected item must survive the collapse |
| Supporting pane | A secondary surface supports the primary task continuously (filters, tools, properties, a running total, live chat) | The secondary content is consulted rarely | Becomes a sheet or a tab; never silently disappears |
| Feed | Content is browsed rather than navigated (cards, media, dashboards) | The user needs a stable position while acting on one item | Reduces column count; item size stays constant |

Two rules that break more tablet layouts than anything else:

- **The detail pane needs its own empty state.** A two-pane layout at first launch has nothing selected. Define what fills it — a placeholder with an action, or a default selection — and say which.
- **Back must stay predictable across the collapse.** When two panes become two screens, the back stack changes shape. Define what back does in both states.

---

## 4. Navigation by width

| Width | Primary navigation |
|-------|--------------------|
| Compact | Bottom tab bar (iOS) / bottom navigation (Android), as on phones |
| Medium | Navigation rail — 80 dp wide, leading edge |
| Expanded | Standard navigation drawer / sidebar, ~240–360 dp, permanently visible |

Bottom navigation at expanded width is the single most common tablet failure: the controls sit as far from the user's hands and eyes as the layout allows, and the horizontal space above them goes unused. Moving to a rail or sidebar is not novelty — these are canonical HIG and Material 3 patterns, so the no-novelty rule points toward them, not away.

Sheets and popovers also diverge: a popover is native on iPad at regular width and collapses to a full-width sheet at compact width. State which surface is used at which width rather than naming one and hoping.

---

## 5. Multitasking and posture

A tablet layout is never guaranteed the full screen.

- **iPadOS**: Split View, Slide Over, and Stage Manager can hand the app any width at any time, including compact. Slide Over in particular returns a regular-width app to compact width mid-session.
- **Android**: split-screen and freeform multi-window do the same; foldables add posture changes as the device folds.
- **Resize without state loss** is the hard requirement. Scroll position, selection, in-progress input, and open sheets survive a width change, or the layout is broken regardless of how it looks at rest.
- Configuration changes are frequent, not exceptional. Design for the transition, not only for the two end states.

---

## 6. Input is additive, never assumed

Larger screens usually gain input methods. They never lose touch.

- **Touch minimums still apply**: 44 pt (iOS) / 48 dp (Android). A pointer being more precise is not a reason to shrink a target — the same build runs under a finger.
- **Pointer**: add hover states where they clarify affordance; never make hover the only way to discover an action.
- **Hardware keyboard**: on a typing-heavy tablet app, treat shortcuts and tab-order as first-class; ensure focus is always visible.
- **Drag and drop**: available across panes and across apps; always provide a non-drag path to the same outcome.
- **Stylus**: precision input, not a required input.

---

## 7. What does not change

State this explicitly in output so a tablet layout is not read as an accessibility exemption:

- contrast ratios, non-color cues, and focus visibility
- Dynamic Type and font-scale behaviour up to 200 %
- state coverage — default, loading, empty, error — now including the detail pane's empty state
- reading measure: 45–75 characters per line. Wider screens get **more columns or wider margins, not longer lines**.

---

## 8. Common failures

- **Stretched phone**: the phone layout at tablet width, with one column of content centred in a sea of margin and every row's line length past 90 characters.
- **Bottom navigation at 1366 pt**: see §4.
- **Two-pane with no empty state**: the detail pane shows a blank rectangle at launch.
- **Break on rotation or resize**: state is lost when Split View opens.
- **Density smuggling**: touch targets shrunk because "it's a tablet, there's a keyboard".
- **Tablet claimed, never specified**: "supports iPad" with no breakpoint, no canonical layout named, and no navigation change.

---

## 9. Evidence limits

- Do not claim a layout is correct at a width you were not told the product supports. Ask, or state the supported set as an assumption.
- Do not assert how a specific device model behaves under multitasking; reason about width classes instead.
- Naming a canonical layout is a design recommendation, not a compliance statement. Large-screen app-quality guidance is a checklist to design against, not proof the design passes it.

---

## 10. Sources

- [Apple HIG: Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
- [Apple HIG: Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking)
- [Apple HIG: Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)
- [Material 3: Applying layout](https://m3.material.io/foundations/layout/applying-layout/window-size-classes)
- [Material 3: Canonical layouts](https://m3.material.io/foundations/layout/canonical-layouts/overview)
- [Android: Support different screen sizes / window size classes](https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes)
- [Android: Large screen app quality guidelines](https://developer.android.com/docs/quality-guidelines/large-screen-app-quality)
