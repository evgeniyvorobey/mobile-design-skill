# Patterns Catalog

This is a decision reference, not a tutorial. For every common mobile pattern, it answers:

- **Use when** — concrete criteria that make this the right choice.
- **Avoid when** — concrete criteria that make this the wrong choice.
- **Trade-offs** — what this choice buys and what it costs.
- **Variants / platform notes** — how iOS and Android differ in the default implementation.
- **Red flag** — what misuse looks like (used as a violation check in Mode D reviews).

When a pattern has close siblings (sheet vs modal vs full-screen; list vs grid; inline edit vs dedicated screen), the entry is structured as a **decision matrix** so the skill can pick, not enumerate.

Patterns here cross-reference:

- `docs/heuristics.md` for the laws driving each choice (Fitts, Hick, Jakob, Zeigarnik, etc.)
- `docs/context-defaults.md` for when context changes the default (older adults favor dedicated edit screens; power users favor inline)
- `docs/quality-bars.md` for numeric minimums every pattern must respect

---

## How to use this document

During generation (Mode A, C, F):

1. Identify the design problem (navigate between sections, reveal secondary info, collect an input, confirm an action, etc.).
2. Find the matching category below.
3. Use the decision matrix to pick a pattern, honoring the active context (`context-defaults.md`).
4. Cite the pattern choice with its reason in the `Pattern choices and why` block.
5. Name the losing alternative in `Alternatives considered`.

During review (Mode D):

1. Identify which pattern the design uses.
2. Check it against the **Use when / Avoid when** rules.
3. If the pattern is used outside its Use-when criteria, flag it with the red-flag reference.

When no pattern fits cleanly: prefer the simplest pattern that solves the task, and document the deviation in `Assumptions`. Do not invent novel patterns to impress; novelty breaks Jakob's Law.

---

## 1. Primary navigation

### Bottom navigation vs navigation drawer vs top tabs

| Criterion | Bottom nav | Nav drawer | Top tabs |
|-----------|------------|------------|----------|
| Number of primary destinations | 3–5 | 5+ (with hierarchy) | 2–4 |
| Reach (one-handed) | Best | Weakest (drawer icon top-left) | Weak on large phones |
| Discoverability | High — always visible | Low — hidden behind icon | High when at top of screen |
| Switching cost | One tap | Two taps (open + pick) | One tap |
| Platform fit iOS | Native (tab bar) | Non-native | Acceptable as segmented or under nav bar |
| Platform fit Android | Native (Material bottom nav) | Native (Material drawer) | Native (Material tabs) |

**Use bottom nav when** the app has 3–5 top-level destinations the user moves between frequently.
**Use nav drawer when** the hierarchy is deep (>5 primary areas) and frequency of switching is low.
**Use top tabs when** the user switches between related views of the same content (segments of one destination), not between destinations.

**Trade-off**: bottom nav consumes vertical space continuously; drawer gives screen real estate but adds a tap. Top tabs combine well with bottom nav (bottom nav switches destinations, top tabs switch views within a destination).

**Red flag**:
- Bottom nav with 6+ tabs.
- Drawer used to hide primary features because they "didn't fit" in bottom nav.
- Top tabs used for destination-level navigation instead of view-level.

**Heuristic**: Hick's Law, Jakob's Law, thumb zone.

---

### Tab order and labeling

| Use when | Avoid |
|----------|-------|
| Order by frequency (most-used first or in thumb-reach positions 2–4) | Ordering alphabetically |
| Icon + label for every tab | Icon-only (violates recognition over recall for all but universal icons like home, search, profile) |
| Labels under 12 characters | Labels that truncate on standard phone width |

**Red flag**: icon-only tab bar where a tab's meaning is not universally obvious.

---

### Back behavior

**iOS**: left-edge swipe + top-left chevron. Both must return to the previous meaningful screen and preserve the current screen's state until confirmed discard.

**Android**: system back button, gesture back (Android 10+), and in-app back affordance must all behave consistently. Predictive back (Android 13+) should be supported.

**Cross-platform rule**: unsaved changes must prompt or auto-save, never silently discard. Back from a detail view returns to the list with scroll position preserved.

**Red flag**:
- Back dismisses a modal but also exits the app if tapped again without warning.
- Back silently discards form entries.
- iOS swipe-back works but the chevron does different behavior.

**Heuristic**: Jakob's Law, interruption-resilience, peak-end rule.

---

## 2. Presentation overlays

### Modal vs sheet vs full-screen

| Criterion | Modal alert | Bottom sheet | Full-screen |
|-----------|-------------|--------------|-------------|
| Interrupts user | Yes — blocking | Partial — context behind is visible | Yes — replaces context |
| Task length | Single decision (<5 seconds) | Short task (a few fields, a picker) | Multi-step or extended input |
| Dismiss gesture | Explicit tap | Tap outside, swipe down, explicit close | Explicit close or complete |
| Platform-native | iOS alerts / Android dialogs | iOS sheets / Material bottom sheet | iOS sheet (full) / Android fragment |
| Context preservation | Interrupts | Preserves | Replaces |

**Use modal alert when** the user must make one critical decision before continuing (destructive confirmation, auth required, critical error).

**Use bottom sheet when** the task is short, complementary to the underlying screen, and the user may want to reference the context behind (picker, share options, comment input, quick edit).

**Use full-screen when** the task is multi-step, requires focus, or involves a different mental mode (compose, checkout, onboarding, immersive picker).

**Trade-off**: modals stop the user; sheets ride alongside; full-screen replaces the mental model. Overuse of modals causes decision fatigue and encourages dismiss-by-reflex.

**Red flag**:
- Modal used for an optional or informational message (use toast or inline banner).
- Bottom sheet used for a multi-step wizard (upgrade to full-screen).
- Full-screen used for a single field input (downgrade to sheet or inline).

**Heuristic**: Hick's Law, user control and freedom (Nielsen #3).

---

### Bottom sheet sub-pattern (static vs draggable vs modal)

| Variant | Use when |
|---------|----------|
| Static / peek | Persistent secondary content (map controls, now-playing mini-player) |
| Draggable with snap points | Variable disclosure (expand for more detail, collapse to peek) |
| Modal bottom sheet | Blocking choice or input tied to a triggering action |

**Red flag**: draggable sheet with unclear snap points that cause accidental full-expand during scroll.

---

### Popover / tooltip

**Use when** a small piece of context-tied information needs to appear next to its trigger without replacing the screen (iPad hints, menu from a button, inline help).

**Avoid when** the content is scrollable or multi-step — upgrade to a sheet.

**Platform**: popovers are native on iPad; on iPhone, popovers collapse into full-width sheets or modal menus. Android typically uses popup menus or bottom sheets rather than popovers.

**Red flag**: popover used on a narrow phone where it collapses into a sheet anyway — skip the popover abstraction.

---

### Action sheet

**Use when** a single action needs to offer 2–7 mutually exclusive options (share destination, sort order, media picker source).

**Avoid when** the options need explanations longer than a label, or when only two options exist (use inline or a simple dialog).

**iOS**: `UIActionSheet` / `UIAlertController` with `.actionSheet`, anchored to bottom on phone.
**Android**: Material modal bottom sheet with list items, or popup menu for short single-choice.

**Red flag**: action sheet with a single destructive action and no non-destructive alternative (collapse into a confirm dialog).

---

## 3. Content display

### List vs grid

| Criterion | List | Grid |
|-----------|------|------|
| Primary content channel | Text | Visual |
| Information per item | Multiple fields, variable length | Image + 1–2 labels |
| Scannability | Top-to-bottom reading | Eye-sweep across rows |
| Density | Medium | High |
| Common domains | Messaging, finance, settings, task lists | Media, shopping, galleries, people |

**Use list when** the item's meaning is text-primary (title, timestamp, subtitle, metadata).

**Use grid when** the item is image-primary and text is a caption.

**Hybrid**: many apps use list for primary content and grid for sub-sections (list of conversations, grid of attachments within one).

**Red flag**:
- Grid used for text-primary content, causing each cell to feel crowded.
- List used for media library where thumbnails are the point.

**Heuristic**: Gestalt (similarity, common region), Miller's Law.

---

### Card vs row

| Criterion | Card | Row |
|-----------|------|-----|
| Visual weight | High — elevated or bordered | Low — just spacing and dividers |
| Content density | Rich (image + title + body + actions) | Compact (label + value) |
| Tap affordance | Entire card is often tappable | Whole row or specific controls |
| Use count per screen | 2–6 before the screen feels busy | 10+ is fine |

**Use cards when** each item is self-contained and invites consideration (product, event, person).

**Use rows when** the list is scannable and each item is an item in a sequence (messages, transactions, settings).

**Red flag**: card UI for a 50-item list, causing excess scroll and low density when scanning is the task.

---

### Pagination: infinite scroll vs paged vs load more

| Criterion | Infinite scroll | Paged | Load more |
|-----------|-----------------|-------|-----------|
| Browsing behavior | Casual, open-ended | Targeted, specific page recall | Middle ground |
| Goal clarity | "Show me what's out there" | "Find a specific item" | Either |
| Footer accessibility | Hard — footer recedes | Easy — always reachable | Easy — button at bottom |
| Returnability (come back to same spot) | Hard | Easy | Medium |
| Analytics friction | Hard to define "end" | Easy to define session | Easy |

**Use infinite scroll when** the content is exploratory and the user is not trying to reach a specific item (feeds, discovery).

**Use paged when** users search for specific items, bookmark results, or need page recall (reference apps, admin consoles, printable lists).

**Use load-more when** you want some of both — user stays in control and the footer remains reachable.

**Red flag**:
- Infinite scroll on search results where the user needs to filter later.
- Paged UI on a feed where the user will never think in terms of pages.

**Heuristic**: Zeigarnik effect (infinite scroll exploits it, sometimes harmfully), goal-gradient.

---

### Accordion / expand-collapse

**Use when** the user needs to survey many items' headings before drilling into one, and sections are independently useful (FAQ, categories in settings, hierarchical filters).

**Avoid when** users will expand many at once (use a grid or list instead), or when the hierarchy is shallow (just stack the content).

**Red flag**: accordion with only one section, or accordion that collapses on scroll, losing the user's reading position.

---

### Carousel

**Use when** the items are genuinely parallel (product images, onboarding screens, featured posts) and the user's default expectation is to see most of them.

**Avoid when** items are not parallel (users expect different things), or when the hidden items are more important than the visible one.

**Red flag**: carousel with 10+ items where only the first 2 are ever seen (telemetry shows this most of the time — reconsider).

---

## 4. Actions

### Primary action placement

| Placement | Use when |
|-----------|----------|
| Top-right of nav bar | iOS convention for "Save" / "Done" on forms |
| Bottom edge (floating or sticky) | Long forms; primary action is always reachable; thumb zone |
| Material FAB | A single primary action on a content-heavy screen |
| Inline at end of content | Short content fits above the fold |
| Top-right + sticky bottom | Long forms where both discoverability and reachability matter |

**Red flag**: primary action at the top-right of a scrollable form on phone — users have to scroll back up to submit.

**Heuristic**: Fitts' Law, thumb zone.

---

### Destructive action confirmation: confirm-dialog vs undo-snackbar

| Criterion | Confirm dialog | Undo pattern |
|-----------|---------------|--------------|
| Reversibility | Required because action is irreversible after confirm | Action executes, undo available for a window |
| Speed for power users | Slow (forces confirm every time) | Fast (execute + undo if wrong) |
| Risk of mistake | Low (extra step) | Medium (depends on undo window) |
| Data recoverability | Hard or impossible | Possible via undo |

**Use confirm dialog when** the action is truly irreversible (account deletion, financial transfer above a threshold, permanent data loss).

**Use undo snackbar when** the action is reversible within a short window (delete a message, archive, mark as read, bulk operations).

**Trade-off**: dialogs protect but frustrate; undo is fast but fails if the user doesn't notice or misses the window.

**Red flag**:
- Undo with a 2-second window (too short to notice).
- Confirm dialog on a trivial, reversible action.
- Undo that doesn't actually restore all the deleted state.

**Heuristic**: user control and freedom (Nielsen #3), Peak-End rule (recoverable mistakes feel better).

---

### Bulk actions

**Use when** users regularly act on multiple items (delete many photos, archive many messages, assign many tasks).

**Entry**: long-press to enter selection mode, or a persistent "Select" affordance, or checkboxes revealed by swipe.

**Red flag**:
- Bulk selection mode with no "select all" / "select none".
- Bulk action bar that covers content the user needs to see while selecting.

---

### Swipe actions

**Use when** the item is a row in a list and the action is a short secondary verb (delete, archive, pin, flag).

**iOS**: swipe-to-delete is native; trailing swipe is destructive, leading swipe is non-destructive.
**Android**: swipe actions are present in Material but less ubiquitous; pair with a visible button where possible.

**Red flag**:
- Swipe is the only way to perform a common action — violates gesture-alternative principle.
- Swipe direction conflicts with horizontal scroll in the same area.

**Heuristic**: Jakob's Law (platform idioms), accessibility gesture alternatives.

---

## 5. Input

### Inline edit vs dedicated edit screen

| Criterion | Inline | Dedicated |
|-----------|--------|-----------|
| Field count | 1–3 | 3+ |
| Relationship between fields | Independent | Related / validated together |
| Audience | Power users, daily use | Occasional use, older adults |
| Reversibility | Easy (leaves read view) | Clear (explicit save/cancel) |
| Error handling surface | Inline field error | Summary + inline |

**Use inline edit when** the field is scalar, the user edits often, and the undo surface is immediate.

**Use dedicated screen when** multiple fields interact, validation is non-trivial, or the audience benefits from explicit save/cancel.

**Red flag**: inline edit for a 12-field profile — overwhelming and error-prone.

**Heuristic**: Tesler's Law (complexity goes somewhere — inline pushes it to screen real estate, dedicated pushes it to navigation cost).

---

### Picker: inline vs sheet vs modal

| Picker | Use when |
|--------|----------|
| Inline (segmented control, chips, radio) | 2–5 options; user benefits from seeing all at once |
| Sheet picker (wheel, list) | 5+ options; user benefits from scrolling/searching; underlying screen context is useful |
| Modal / dedicated picker screen | Complex selection (search, categories, multi-select) |

**Red flag**: wheel picker with 3 options (use segmented control).

---

### Segmented control vs dropdown vs tabs

| Criterion | Segmented | Dropdown | Tabs |
|-----------|-----------|----------|------|
| Options visible | All at once | One (chosen) | All at once |
| Options count | 2–4 | 5+ | 2–6 |
| Switching cost | One tap | Two taps (open + pick) | One tap |
| Persistence | Temporary filter on one screen | Temporary filter on one screen | Switches primary views within a destination |

**Use segmented when** 2–4 mutually exclusive states affect the current screen (filter by status, mode).

**Use dropdown when** 5+ options need compact access and the current value is the important thing to show.

**Use tabs when** the user is switching between sibling views, not filtering one view.

**Red flag**: dropdown used where segmented control would fit and reveal all options.

---

### Search: instant vs submit

| Variant | Use when |
|---------|----------|
| Instant (search-as-you-type) | Small dataset, fast index, results help the user refine query |
| Submit on enter / button | Expensive query, paginated results, user knows what they want |
| Scoped tabs within search | Heterogeneous results (people, photos, files) |

**Red flag**: instant search that triggers a network call per keystroke without debounce.

---

### Form field grouping

**Use when** a form has more than 5 fields: group by meaning (Personal, Contact, Payment) with visible headers and whitespace.

**Single flat form** is acceptable only for 5 or fewer fields.

**Red flag**: 15-field flat form with no grouping (see `examples/anti-patterns.md`).

**Heuristic**: Miller's Law, Gestalt (proximity, common region).

---

## 6. Feedback and status

### Toast vs snackbar vs banner vs alert

| Surface | Use when |
|---------|----------|
| Toast (brief, auto-dismiss) | Passive feedback, short, non-critical ("Saved") |
| Snackbar (with optional action, auto-dismiss) | Confirmable action result ("Deleted — Undo") |
| Banner (persistent until dismissed) | Sustained status that matters while on the screen (offline, degraded mode, limited-time) |
| Alert / dialog (blocking) | Critical, requires acknowledgement |

**Red flag**:
- Alert used for non-critical info (users learn to dismiss alerts reflexively, losing real signal).
- Toast used for critical info the user must act on.

**Heuristic**: visibility of system status (Nielsen #1), user control and freedom.

---

### Loading: spinner vs skeleton vs progress bar

| Variant | Use when |
|---------|----------|
| Spinner | Unknown duration, single atomic operation (save, submit) |
| Skeleton | Known layout, fetching data for a predictable shape (list, detail) |
| Progress bar | Known total, long duration (upload, multi-file sync) |
| Inline state (button) | Primary action in progress; keeps focus on action |

**Duration thresholds** (see `docs/quality-bars.md`):
- 0–100ms: no indicator needed
- 100ms–1s: inline state (button press, skeleton start)
- 1s–10s: explicit loading
- 10s+: progress with cancel or background

**Red flag**:
- Skeleton that flashes for 150ms (just add debounce so it never appears for fast loads).
- Spinner for a multi-file upload with no progress (upgrade to progress bar).

**Heuristic**: Doherty Threshold, visibility of system status.

---

### Optimistic updates

**Use when** the action is likely to succeed and the user benefits from immediate feedback (like, favorite, archive, send message).

**Avoid when** failure has high cost and the user cannot recover easily (payment, destructive irreversible action, medical dosing).

**Red flag**:
- Optimistic update with no rollback handling — user's state drifts from server state silently.
- Optimistic update for an operation that often fails (makes rollback the common case).

---

### Error communication

| Variant | Use when |
|---------|----------|
| Inline field error | Validation of a specific input |
| Form-level summary | Multiple fields failed; summary at top with jump-to |
| Banner at top | System-wide error (offline, server down) |
| Modal alert | Critical, action blocked, user must acknowledge |
| Empty error state (screen replacement) | Resource could not be loaded at all |

**Every error** must include: what happened, why, how to recover. Plain language. Not just "Something went wrong."

**Red flag**:
- Generic error toast with no detail.
- Error shown only in color, with no icon or text.

**Heuristic**: Nielsen #9 (help users recognize, diagnose, recover).

---

## 7. States

### Empty state

**Purpose**: communicate that the state is intentional (no data yet) vs failure (data should be there but isn't).

**Three types**:
- **First-use empty**: user hasn't done anything; onboarding-like, with a clear next action.
- **User-cleared empty**: user emptied the list (archived all messages); reassuring confirmation.
- **No-match empty**: filter or search returned nothing; suggest relaxation.

**Red flag**:
- Empty state with no action.
- Empty state that looks identical to a loading state.
- Empty state that shows a decorative illustration with no text or action.

---

### Skeleton design

- Use the exact layout of the real content, not a generic placeholder.
- No shimmer faster than ~1 pulse per second.
- No skeleton if the load completes under ~300ms (use debounce).

**Red flag**: skeleton that doesn't match the real layout, causing visual jolt when content arrives.

---

### Error state (screen-level)

- Explain what happened, in plain language.
- Offer a clear recovery action (Retry, Go back, Contact support).
- Preserve user-entered data; do not wipe forms on failure.

**Red flag**: error screen that says "An error occurred" with no retry and no preserved state.

---

## 8. Forms

### Single-screen long form vs multi-step wizard

| Criterion | Single screen | Multi-step |
|-----------|--------------|------------|
| Field count | Up to ~10 | 10+ |
| Logical grouping | Weak (flat list) or medium (1–3 sections) | Strong (5+ related sections) |
| Completion motivation | Goal is immediate, user sees end | Goal benefits from progress indicator |
| Error recovery | Easy — all fields visible | Harder — user must navigate steps |
| Abandonment | Medium | Higher if no save-and-resume |

**Use single screen when** the form is short, fields relate to each other, and the user completes in one session.

**Use multi-step when** the form is long, fields group naturally, and the user may abandon / resume.

**Red flag**:
- 20-field single screen with no grouping.
- 3-field wizard split into 3 steps for no reason.

**Heuristic**: Miller's Law, goal-gradient, Zeigarnik effect, peak-end.

---

### Validation timing

| Variant | Use when |
|---------|----------|
| On blur | Most fields — respects user typing without nagging |
| On submit | Cross-field validation, final check |
| As-you-type | Format enforcement (card number, phone, strong password indicator) |
| On focus change | Structured data that must be valid to continue (date, currency) |

**Red flag**: error appearing while the user is still typing their first character of a valid value.

---

### Save strategy

| Strategy | Use when |
|----------|----------|
| Explicit save + cancel | Dedicated edit screen; change confirmation matters |
| Auto-save (silent) | Continuous editing (notes, drafts); user's mental model is "it's saved" |
| Auto-save + explicit publish | Multi-stage (draft, preview, publish) |
| Save on field blur | Single-value edits; power-user surfaces |

**Red flag**:
- Explicit save on a note-taking app — users lose content when they navigate away.
- Auto-save with no visible confirmation (user unsure if saved).

---

### Required field marking

- Mark required fields **before** submission, not via error.
- Asterisk + "Required" label on first marked field as a legend; or explicit "(required)" per field.
- Do not rely on color alone.

**Red flag**: user submits a form and discovers, field by field, what was required.

---

## 9. Onboarding

### Walkthrough / intro screens

**Use when** the app has a genuinely non-obvious value proposition that needs a 3–4 slide intro.

**Avoid when** the app's value is obvious from the first screen (social apps, utilities, standard categories). A walkthrough adds friction without value.

**Red flag**: 8-screen walkthrough before the user can try anything.

---

### Coach marks / tooltips

**Use when** a novel interaction needs a one-time explanation (new gesture, non-standard control).

**Avoid when** the interaction is standard (Jakob's Law — users already know).

**Red flag**: coach mark covering a button the user is trying to tap.

---

### Just-in-time tips

**Use when** explanation is cheap and discovery is expensive. Surface tip next to the relevant control, the first time the user encounters it.

**Prefer** JIT over upfront walkthrough for most apps.

**Heuristic**: recognition over recall, goal-gradient.

---

### Empty state as onboarding

**Use when** the user's first view is legitimately empty and a single CTA (create, connect, import) is the obvious next step.

**Red flag**: empty state without a CTA.

---

## 10. Search UX

### Scope

| Variant | Use when |
|---------|----------|
| Global (searches everything in app) | User often doesn't know where their thing is |
| Scoped to current view | User knows they're in the right area |
| Tabbed search results | Heterogeneous content (people, photos, files) |

---

### Recent queries and suggestions

- Show recent queries when the field is focused, before the user types.
- Show suggestions (autocomplete, entity match, popular) as the user types.
- Let the user clear recent queries.

**Red flag**: search field that shows nothing until the user types 3+ characters — wastes the focus state.

---

### Search results layout

- List for text-heavy results.
- Grid for media-heavy results.
- Mixed with labeled sections for heterogeneous results.
- Sort and filter affordances visible but not in the way.

**Red flag**: search results with no sort/filter option when the default ranking is unhelpful.

---

## 11. Notifications and signals

### Notification types

| Type | Use when |
|------|----------|
| Push | User is not in the app; content is time- or identity-relevant |
| In-app banner | User is in the app; relevant event occurred elsewhere in the product |
| Badge | Asynchronous unread state; pulls user back |
| Inline (in-context) | Event relevant to the screen the user is on |

**Red flag**: push notification for content that is not actually important (erodes attention and opt-in).

---

### Notification grouping

- Group by conversation, sender, or topic rather than chronological.
- Allow per-group settings (mute, snooze, disable).
- Summarize bursts (3 messages from X) rather than 3 separate notifications.

---

## 12. Authentication

### Sign-in patterns

| Variant | Use when |
|---------|----------|
| Email + password | Default fallback; required for some account types |
| Magic link | Low-stakes; eliminates password management |
| Social (Apple, Google, Facebook) | Reduces friction; Sign-in with Apple is required on iOS when other third-party sign-ins exist |
| Phone + OTP | Phone-first audiences; SMS-gated accounts |
| Biometric (Face/Touch ID) | Re-auth on a signed-in device; never the only auth factor |

**Red flag**:
- Email+password as the only option on an iOS app with third-party sign-in (missing Sign-in with Apple).
- OTP form that doesn't auto-fill from SMS (iOS autofill / Android SMS Retriever).

---

### Session and re-auth

- Re-auth for sensitive operations (payments above threshold, account changes, export).
- Re-auth via biometrics is preferred over re-typing password on mobile.
- Surface session state (signed in as X, last sync, device list).

---

## 13. Accessibility patterns

### Accessible action labels

- Every interactive element has an accessibility label describing the action ("Delete message"), not the appearance ("Trash icon").
- Dynamic labels update when state changes ("Like" → "Unlike" when liked).

### Focus management

- When a sheet or modal appears, focus moves into it; on dismiss, focus returns to the trigger.
- Focus order follows visual reading order.

### Gesture alternatives

- Every swipe, long-press, and drag has a button or menu alternative.
- Custom gestures have onboarding or visible hints.

**Red flag**: swipe-only delete on a messaging app (missed by screen readers and motor-impaired users).

---

## 14. Platform-divergence patterns

When cross-platform output is required, share structure first and split only where conventions differ. Common divergences:

| Pattern | iOS | Android |
|---------|-----|---------|
| Primary action on a form | Top-right nav bar ("Save", "Done") | Bottom sheet action or top-bar action button |
| Destructive confirmation | Action sheet with red destructive action | Material dialog with red text destructive button |
| Navigation back | Top-left chevron + edge swipe | System back button + predictive back |
| Tab bar | Bottom, 3–5 items, native tab bar | Bottom nav (Material) with 3–5 destinations |
| Date picker | Wheel picker in sheet | Material date picker (calendar or input) |
| Share | UIActivityViewController (native share sheet) | Android share sheet (system) |
| Haptics | System haptic feedback taxonomy | Material haptic patterns |
| Large-screen primary navigation | Sidebar at regular width; collapses to rail-equivalent behaviour | Navigation rail 600–839 dp; standard navigation drawer ≥ 840 dp |
| Two-pane container | Split view, two- or three-column | Material 3 adaptive list-detail / supporting-pane scaffold |
| Contextual overlay at regular width | Popover anchored to its source | Menu or dialog — a popover is not a Material surface |
| Multitasking surface | Split View, Slide Over, Stage Manager | Split-screen and freeform multi-window |
| Keyboard shortcut discovery | Command-key HUD | Keyboard shortcuts helper |

Component and API names in the large-screen rows are library- and OS-version-bound. Name the version a recommendation assumes when it materially changes the answer (guardrail 16).

**Rule**: when sharing structure, use platform-neutral nouns in the spec and split the implementation notes per platform.

---

## 15. Large-screen and adaptive patterns

Every entry above was written for one pane at compact width. This section chooses between their large-screen siblings. `docs/adaptive-layout.md` holds the width classes, the canonical layouts, and the multitasking rules; `docs/quality-bars.md` holds the numbers. This section is the choosing.

Width, not the device, drives every matrix here — compact < 600 dp, medium 600–839 dp, expanded ≥ 840 dp — and a tablet in Slide Over is a compact surface. So every choice below has to answer two questions: what it is at regular width, and what it becomes when the width drops.

### List-detail vs stacked navigation vs feed

| Criterion | List-detail (two panes) | Stacked navigation (one pane) | Feed / grid |
|-----------|-------------------------|-------------------------------|-------------|
| User's movement | Back and forth between a collection and its items | One-way drill in, then out | Browse; no stable selection |
| Selection | Is the layout's state; survives resize | Ends when the screen is popped | None |
| Comparison across items | Supported — the list stays on screen | Not supported | Visual only |
| Width to be worth it | ~700 pt total (list 320–400 pt + detail ≥ 320 pt) | Any | Any |
| At compact width | Two screens, push navigation; the selection survives the collapse | Already this | Fewer columns, item size constant |

**Use list-detail when** the user returns to the collection repeatedly — mail, messages, patients, orders, files, tickets.
**Use stacked navigation when** an item is opened once, acted on, and left; a two-pane layout then keeps a list on screen that nobody looks at.
**Use a feed when** the content is browsed rather than navigated and no item needs to stay selected.

**Trade-off**: list-detail buys context and comparison and costs the detail pane its full width — at medium width that is the difference between a readable detail and a compressed one. Stacked navigation buys the whole width for one thing and costs a return trip per item.

**Rule**: pick the canonical layout from the user's movement between collection and item, not from the width available. Width then decides whether that layout is shown as panes or as screens.

**Red flag**:
- Two panes at medium width leaving the detail under 320 pt.
- List-detail on a flow that is entered once (checkout, onboarding, a wizard).
- A layout named for a device ("the iPad layout") instead of for a width class.

**Heuristic**: recognition over recall, Jakob's Law, Hick's Law.

---

### Detail-pane empty state: placeholder vs default selection vs restore

| Criterion | Named placeholder with an action | Auto-select the first item | Restore the last selection |
|-----------|----------------------------------|----------------------------|----------------------------|
| First launch with data | Works | Works | Nothing to restore — falls back to the placeholder |
| First launch with no data | Works — carries the empty-collection action | Nothing to select | Nothing to restore |
| Cost of opening an item | None | Real when opening marks read, logs a view, locks a record, or starts a download | None if the item still exists |
| What the user learns | What this pane is for | Nothing; it looks like a chosen item | Where they left off |

**Use a placeholder when** opening an item has any side effect, or the collection can be empty.
**Use auto-select when** opening is free of side effects and the first item is the one the user almost always wants (a settings pane, a single-account view).
**Use restore when** the session is long and interrupted — the tablet locks between rooms, the app is resumed after Split View.

**Rule**: the detail pane is never blank. Restore the last selection when it still exists; otherwise show a named placeholder carrying the pane's primary action. Auto-select only when opening an item has no side effect.

**Red flag**:
- An empty grey rectangle at launch.
- Auto-select in a mail-like or clinical app, where selecting marks the item read or records access.
- An empty state that says only "Select an item" and offers nothing to do.

---

### Secondary content at width: supporting pane vs sheet vs tab vs popover

| Criterion | Supporting pane / inspector | Sheet | Tab or segment | Popover |
|-----------|-----------------------------|-------|----------------|---------|
| Consulted | Continuously while the primary task runs | Once per task, then dismissed | When the user switches to it | Once, near its trigger |
| Edits while the primary pane stays visible | Yes | No — it covers the context | No | Rarely |
| Width it needs | A third pane above ~1200 pt; below that it is the second pane or a sheet | None | None | None |
| At compact width | Becomes a sheet or a tab — never silently disappears | Already this | Already this | Full-width sheet |

**Use a supporting pane when** the user changes something in it and watches the effect in the primary pane — filters over a queue, properties over a canvas, a running total over a cart, live chat beside a document.
**Use a sheet when** the content is consulted and dismissed, or when it is a task of its own.
**Use a tab when** the secondary content is a different view of the same object rather than a control over it.

**Trade-off**: an inspector buys simultaneity and costs the primary pane 280–360 pt permanently. Below ~1200 pt that cost usually outweighs it.

**Rule**: an inspector earns its width only if the user changes something in it *while looking at* the primary pane. Consulted-then-dismissed content is a sheet at every width.

**Red flag**:
- A third pane at 1024 pt that squeezes both other panes.
- A supporting pane that vanishes at compact width with no replacement surface.
- An inspector holding a form the user submits once — that is a sheet.

---

### Primary navigation by width: bottom bar vs navigation rail vs sidebar

| Width | Primary navigation | Destinations | Why |
|-------|--------------------|--------------|-----|
| Compact (< 600 dp) | Bottom bar / bottom navigation | 3–5 | Thumb reach; the phone rule, unchanged |
| Medium (600–839 dp) | Navigation rail, 80 dp, leading edge | 3–7 | Leading edge is closer to the holding hand than the bottom of a 10-inch screen, and the vertical space is free |
| Expanded (≥ 840 dp) | Sidebar / permanent drawer, 240–360 dp | 5+, grouped and hierarchical | Width is available; labels and grouping fit; the destination is visible without a tap |

**Use a rail when** the width is medium or the sidebar's labels would cost the content more width than they are worth.
**Use a sidebar when** the width is expanded and the destination set has hierarchy (folders, projects, saved filters) — a rail cannot express grouping.
**Keep the bottom bar when** the app is at compact width, including a tablet in Slide Over or a narrow Split View.

**Trade-off**: the sidebar takes 240–360 pt from the content permanently; make it collapsible to a rail when the primary task is reading or editing at full width. A rail costs 80 dp and holds no hierarchy.

**Rule**: navigation changes container with width, never destination set. The same destinations appear at every width, so a user who resizes mid-session never loses a section. Never map navigation to a device model.

**Red flag**:
- A bottom bar at expanded width — the single most common large-screen defect. The controls sit as far from the eye as the layout allows and the width above them goes unused.
- Five bottom tabs centred as a group in the middle of a 1366 pt bar.
- A hamburger drawer at expanded width, hiding destinations that would fit permanently.
- A rail with more than about seven items, or icon-only rail items whose meaning is not obvious.

**Heuristic**: Fitts's Law, Hick's Law, Jakob's Law.

---

### Overlays by size class: popover vs sheet vs inline panel vs dialog

| Surface | At regular width | At compact width | Use when |
|---------|------------------|------------------|----------|
| Popover, anchored to its source | Native on iPad; arrow points at the trigger | Becomes a full-width sheet | Short, source-anchored choice or detail; roughly 2–7 options |
| Sheet | Centred or edge-attached; does not cover the whole window | Full-width bottom sheet | A short task with its own inputs |
| Inline panel inside a pane | Replaces the pane's content, keeps the other panes | Becomes a pushed screen | The task belongs to one pane and is longer than a popover |
| Modal dialog | Blocks the window | Blocks the screen | One critical decision, destructive or auth |

**Rule**: name both ends. "Use a popover" is half a decision — state where it anchors at regular width and what it becomes at compact width, because multitasking will produce both within one session.

**Trade-off**: a popover keeps the context and costs a small target for its content; a full-window modal at 1366 pt makes a two-line question feel like a page.

**Red flag**:
- An overlay named for one width only.
- A modal dialog stretched across the whole window for a single confirmation at expanded width.
- A popover carrying a scrollable multi-step task — that is an inline panel or a sheet.

---

### Action placement: pane toolbar vs window toolbar vs bottom bar vs inline

| Criterion | Toolbar in the pane | Window / top toolbar | Bottom action bar | Inline in the row or card |
|-----------|---------------------|----------------------|-------------------|---------------------------|
| What the action acts on | That pane's content | The whole window or document | The current screen | One item |
| Ambiguity at two panes | None — scope is where it sits | High if it acts on only one pane | High | None |
| Reach at expanded width | Near the content it changes | Top edge; a deliberate trip | Far from both hands and eyes at 1366 pt | At the item |
| At compact width | Becomes the screen's nav-bar action | Unchanged | Unchanged | Unchanged |

**Use a pane toolbar when** the action changes what one pane shows or contains — sort, filter, add to this list, compose in this detail.
**Use the window toolbar when** the action is document- or window-scoped — share, export, close, switch mode.
**Use a bottom action bar when** one screen-wide commit action repeats constantly under time pressure (send the order, take the payment) and the layout is a single pane.
**Use inline actions when** the action belongs to one item and the item is visible.

**Rule**: an action lives in the toolbar of the pane whose content it changes. When two panes are visible, a toolbar at the window level says "this acts on everything" — if it does not, it is in the wrong place.

**Red flag**:
- An "Add" button in the window toolbar when there are two panes and it only adds to one of them.
- A phone's bottom action bar carried unchanged to a two-pane layout, so the action is 700 pt from the pane it affects.
- The same action offered in two toolbars at different scopes.

**Heuristic**: Fitts's Law, Gestalt (proximity and common region).

---

### Columns and reading measure at width

| Content | Compact | Medium | Expanded |
|---------|---------|--------|----------|
| Card or media grid | 2 columns | 4–6 | 6–8 |
| Body text | Full width minus margins | ≤ 640–720 pt | ≤ 640–720 pt; the leftover width goes to margins, navigation, or a different pane |
| Data rows | One row set | One row set, wider margins | One row set plus a supporting pane, or two panes |

**Rule**: extra width becomes more columns or wider margins — never a longer line. The 45–75 character measure holds at every width.

A centred single column is *not* automatically a stretched phone: it is a legitimate reading layout when the measure is locked deliberately and the leftover width carries something — navigation, an inspector, or a stated margin. It is a stretched phone when the leftover width does nothing and the phone's own layout was simply centred in it.

**Red flag**:
- One text column stretched past ~720 pt.
- A grid that keeps two columns at 1366 pt, so each card is 600 pt wide.
- A phone layout centred at tablet width with empty background on both sides and no other change.

---

### Cross-pane drag vs explicit move

| Criterion | Drag between panes | Explicit move / assign command | Cut and paste |
|-----------|--------------------|--------------------------------|---------------|
| Discoverability | Low — nothing on screen says it is possible | High — named in a menu | Medium |
| Precision cost | Real: a long drag across 1366 pt with a moving target | None | None |
| Keyboard and screen-reader path | None by itself | Yes | Yes |
| Speed for a practiced user | Highest | Medium | Medium |

**Rule**: drag is an accelerator, never the only path. Every cross-pane or cross-app drag has a menu, button, or keyboard equivalent, and the drop target is visibly a drop target before the drag starts.

**Red flag**:
- Reassigning, filing, or reordering that can only be done by dragging.
- A drop target that only appears once the drag is already in flight.
- Drag as the answer to "how does this work on tablet" with no compact-width equivalent.

**Heuristic**: recognition over recall; gesture alternatives (see §13).

---

## Maintenance

- Add a pattern here only after it has solved a real design problem in the field or surfaced as a common question.
- Do not inflate the catalog with rarely used patterns. A leaner catalog is more useful than a complete one.
- When a pattern's sibling entry creates real decision pain, promote it to a decision matrix like the ones above.
- Review the platform-divergence table when HIG or Material 3 publish material updates.
- Every entry must pay for itself by improving at least one real output. If an entry is never cited in responses, prune it.
