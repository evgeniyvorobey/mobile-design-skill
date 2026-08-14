# Golden Example: Tablet List-Detail

## Prompt

```text
Use the mobile-design-skill.

Create a platform-aware UI spec for the library screen of a saved-reading app on tablets.

Inputs:
- Platform: cross-platform, one design for iPadOS and Android tablets
- User goal: work through saved articles - pick one from the collection, read it, annotate it, and file it
- Audience: researchers and analysts who save all week and read in long sessions
- Constraints: the app also ships to phones, sync is frequent and sometimes offline, and articles vary from 200 to 8000 words
```

## Golden output

```md
Mode: Create platform-aware UI spec
Platform scope: Cross-platform — shared structure, split only at the named divergences
Device class: Tablet — regular width is the primary target, and Split View, Slide Over, Stage Manager and Android multi-window can return the app to compact width at any moment
Assumptions:
- Article body, source, saved date, read state, and offline availability are available per item.
- Collections are user-created and can be empty; sources are derived from the article's origin.
- Annotation is highlight-plus-note; there is no collaborative editing.
- Not specified: brand palette and typeface. Type roles and colour roles below are stated as tokens and required ratios, not as invented brand values.

## Screen or flow scope
The library screen: choose a collection, pick an article from it, read the article, annotate and file it — without leaving the screen. Search and settings are separate destinations.

## Structural zones
Expanded width (≥ 840 dp): three columns.
- **Sidebar**, 280 dp, permanently visible: All, Unread, Offline, then user collections, then sources.
- **List pane**, 360 dp: the articles in the selected collection.
- **Detail pane**, remaining width: the article, its body column measure-locked to 680 pt with the leftover width as margin.

Medium width (600–839 dp): two panes — navigation rail 80 dp + list — with the detail pushed over both. The sidebar's contents move into the rail's overflow, not into a hamburger.

Compact width (< 600 dp): one pane. Bottom bar with the sidebar's four fixed destinations; collections open as a pushed list; articles push over it.

**Canonical layout: list-detail.** The user returns to the collection after every article, so the list stays on screen where the width allows it. A supporting pane for annotations was ruled out: it would need a fourth column and the window does not have ~1200 dp to spare, so annotations are an anchored popover at regular width and a sheet at compact.

## Components by section
- Sidebar: section header, destination row (icon + label + count), collection row (source tint dot + name + count), collapse control.
- List pane: search field, sort control, article row.
- Article row: 3 pt leading tint edge, title (2 lines max), source name, read time, saved date, offline badge, unread dot.
- Detail pane: article header (title, source, tint rule, saved date), body, inline highlight, floating annotation popover, bottom reading-progress bar.
- Detail toolbar (in the pane, not the window): Archive, Move to collection, Share, Text size.
- Window toolbar: sync status and account only — nothing that acts on a single pane.

## State definitions
- **Default**: a collection selected, an article selected, body rendered.
- **Loading**: list pane shows 6 skeleton rows at the real row height; detail shows the header and a body skeleton, never a spinner over blank space.
- **Empty — no collections yet**: sidebar shows All/Unread/Offline plus a "New collection" row.
- **Empty — collection has no articles**: list pane states the collection name and offers "Add from Inbox".
- **Empty — nothing selected**: the detail pane shows the collection name, its article count, and the pane's primary action ("Open the newest" / "Add from Inbox"). Never a blank pane.
- **Offline**: rows without a downloaded body show an offline badge and open to a stub with a retry; the sync chip in the window toolbar reads "Offline — last synced HH:MM".
- **Error — sync failed**: non-blocking banner above the list, last-known articles stay readable, retry in the banner.
- **Conflict — annotation changed on another device**: the detail pane shows both versions inline with "Keep mine / Keep theirs"; nothing is discarded silently.

## Behavior rules
- The selection is the layout's state and survives every width change. Collapsing to compact turns the selected article into the top screen of the stack; expanding again restores both panes with the same selection and scroll offset.
- Back at compact width returns to the list, not to the sidebar; back at expanded width is not a navigation action — it moves focus, and the panes do not change.
- Opening an article does not mark it read; reaching 90 % of the body does. Auto-select is therefore safe to omit: the detail pane's empty state is a placeholder, because a mis-restored selection would move an article's read state.
- Resizing never loses scroll position, selection, in-progress annotation text, or an open popover — an open popover becomes a sheet at compact width rather than closing.
- Drag an article row onto a collection to file it. Drag is an accelerator only: "Move to collection" exists in the row's context menu, in the detail toolbar, and on `⌘M` / `Ctrl+M`. The drop target highlights before the drag starts.
- Hardware keyboard: `↑ ↓` move the list selection, `Return` opens, `E` archives, `⌘F` focuses search. Focus ring visible on every focusable element.

## Content guidance
- Row title is the article's own title, never truncated mid-word; two lines then ellipsis.
- Read time is stated in minutes from word count, not in words.
- Empty states name the collection and offer the action; no "Nothing here yet" without a next step.
- Sync copy states time, not adjectives: "Last synced 14:32", never "Recently synced".

## Spacing and layout notes
- 8-based scale: 8 / 16 / 24 / 32.
- Pane gutters 24 dp at expanded, 16 dp at medium; screen margin 16 dp compact / 24 dp medium / 24–32 dp expanded.
- Article row: 88 dp tall, 16 dp internal padding, 12 dp between title and metadata line.
- Body column capped at 680 pt; the width beyond it becomes margin, never line length.
- **Rule for panes this spec does not list**: a pane joins at 24 dp gutters and never renders below 320 dp — below that it collapses to a sheet or a pushed screen instead of compressing.

## Typography rules
- Roles: Display (article title in the detail header), Title (row title), Body (article body), Label (metadata), Caption (badges).
- Values: Body 17 pt / 1.5 line-height; Title 17 pt semibold / 1.3; Label 13 pt / 1.4; Caption 11 pt / 1.3; Display 28 pt / 1.2.
- Adjacent roles differ by at least 1.125×, or by weight where the size is shared (Body vs Title).
- Dynamic Type / font scale to 200 %: the row grows to 3 lines then truncates the metadata line first; the body column keeps its 45–75 character measure by narrowing, never by widening.
- **Rule for a role this spec does not list**: new content joins the nearest existing role; a new role exists only if it differs from both neighbours by ≥ 1.125× or by weight *and* appears in more than one zone.

## Accessibility requirements
- Touch targets 44 pt (iOS) / 48 dp (Android) at every width — the pointer on a keyboard case does not license a smaller row control.
- Every meaning carried by the source tint is also carried by the source name; the unread dot is paired with a bold title; the offline badge carries text, not only an icon.
- Contrast: body and label text ≥ 4.5:1 against the pane surface, tint edge and badges ≥ 3:1, in both light and dark; stated as token pairs, with dark values defined alongside.
- Screen reader: the three panes are three landmarks with names; changing the list selection announces the article title and does not steal focus from the detail pane.
- Every drag has a menu and keyboard equivalent (above); no action is drag-only.
- Reduced motion: pane transitions become cross-fades, the reading-progress bar stops animating.

## Adaptive behavior
| Width | Navigation | Panes | Overlays |
|-------|------------|-------|----------|
| Compact < 600 dp | Bottom bar, 4 destinations | 1 | Annotation as a bottom sheet |
| Medium 600–839 dp | Navigation rail, 80 dp | List, detail pushed over | Annotation as a bottom sheet |
| Expanded ≥ 840 dp | Sidebar 280 dp, collapsible to the rail | Sidebar + list + detail | Annotation as an anchored popover |

Multitasking: Slide Over and a narrow Split View hand the app compact width mid-session, so the compact layout is a first-class state, not a fallback. Stage Manager and external displays only widen it — the same three-column rule applies, with the body column still capped at 680 pt.

## Design quality requirements
- Quality target: 4/5 — the structure, the states, and the values are decided across the widths the spec declares, and four dimensions carry a rule for cases the spec does not list. Held below 5 by Colour, state and contrast and by Context and brand fit, both of which stop at stated pairs and a stated departure budget because the brand palette was not supplied, so neither can settle an unlisted case.
- Signature move: `color.source-tint` — one hue per source, carried as a 3 pt leading edge on the article row, the dot in the sidebar collection row, the rule under the detail header, and the search-result row. Always paired with the source name, so it is a second cue and never the only one.
- Density: the 88 dp row is the repeat unit; at the crowded end (a 3-line title at 200 % scale) the metadata line truncates first and the row grows rather than the type shrinking.
- Motion: pane-scoped changes 150–200 ms, overlay entry 250–350 ms, anything that changes which pane is on screen 200–300 ms, ease-out entering / ease-in exiting; reduced-motion fallback stated above.
- Hard bars vs negotiable: touch minimums, the contrast pairs, and the 680 pt measure cap are hard bars; tint hues, corner radii, and the 88 dp row height are negotiable against the design system.

## Platform-specific implementation notes
- **iPadOS**: three-column split view; the sidebar is the primary column and collapses to the rail behaviour on width change. Annotation popover anchors to the highlight. Keyboard shortcuts appear in the command-key HUD.
- **Android tablet**: Material 3 adaptive list-detail; navigation rail at medium, standard navigation drawer at expanded. Annotation uses a menu or bottom sheet — a popover is not a Material surface. Predictive back applies at compact width only, where back is a navigation action.
- Component and API names above are library-version-bound; check them against the versions in the project before implementation.

## Key decision tradeoffs
- **Three columns over two.** Costs the detail pane 280 dp of width; buys collection switching without a trip back. Acceptable because the body column is capped at 680 pt anyway, so the sidebar consumes margin, not measure.
- **Placeholder over auto-select in the detail pane.** Costs one tap on launch; buys not moving an article's read state on the user's behalf.
- **Annotations as popover/sheet over a fourth pane.** Costs simultaneity while annotating; buys a detail pane that stays readable below 1200 dp.
- **Sidebar collapsible to the rail.** Costs a control most users will never touch; buys the full width for a long reading session without changing the destination set.

## Next actions
- Confirm the brand palette so the tint hues and the contrast pairs can carry values instead of ratios.
- Verify the 680 pt measure and the 88 dp row at 200 % font scale on the narrowest medium window the product supports.
- Test a resize from expanded to Slide Over mid-annotation and confirm the popover becomes a sheet with the text intact.
```

## Design-quality notes

- Reward the width-conditional decisions: a breakpoint tied to a stated layout change, navigation that changes container without changing the destination set, and a compact state treated as first-class because multitasking produces it at runtime.
- Reward the detail pane having decided content rather than a decided existence — the empty state names what it shows and why auto-select was rejected.
- Reward every large-screen accelerator carrying its non-drag, keyboard, and screen-reader path.
- Penalize a phone layout centred at tablet width, a bottom tab bar at expanded width, a body column that grows with the window, and any pane whose behaviour at compact width is unstated.
- The 4/5 label is derived, not asserted: colour and brand fit are the two weakest dimensions here because the prompt supplied no palette, and a reader who disagrees should re-derive rather than adopt the number.
