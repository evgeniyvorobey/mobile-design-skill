# Context-aware Defaults

A generic mobile design is a mediocre mobile design. The right defaults for a banking app are wrong for a kids' game; the right defaults for power users are wrong for older adults.

This document defines the defaults the skill applies when it detects a specific context, so the output is tuned to that context from the first pass instead of needing to be corrected after the fact.

Use these defaults as starting points, not as rigid rules. When the user's stated constraint contradicts a default, the user's constraint wins — but the conflict must be surfaced, not silently resolved.

All numeric thresholds cross-reference `docs/quality-bars.md`, which defines the absolute minimums regardless of context. Context-defaults only adjust values **above** those floors; they never soften a bar.

---

## How to use this document

1. During Step 2 (Identify context) of the workflow, extract the context signals from the input.
2. Look up the defaults for each signal below.
3. When signals conflict (for example, "enterprise" + "older adults"), apply the stricter default.
4. State in `Assumptions` which context defaults were applied, so the user can correct the classification if wrong.

---

## Audience dimension

### Older adults (primary or significant portion)

Signals: "for older users", "60+", "retirement", "accessibility-sensitive for elderly", "large-text-dependent".

| Variable | Default |
|----------|---------|
| Body text size | 17pt iOS / 16sp Android minimum (bumped from 15/14) |
| Line-height | 1.5–1.6 (upper end of range) |
| Touch target | 48pt iOS / 52dp Android minimum (bumped from 44/48) |
| Touch gap | 12pt / 12dp minimum |
| Density | Sparse; one primary action per screen zone |
| Contrast | WCAG AAA target (7:1 body, 4.5:1 large) where feasible |
| Color reliance | Must always pair with text, icon, or pattern |
| Motion | Default to reduced; short durations (150–200ms); no parallax |
| Navigation depth | Shallow; avoid deep hierarchies requiring memory of where the user came from |
| Gestures | Every gesture has a tap equivalent; swipe-to-delete pairs with explicit delete button |
| Confirmation | Confirm destructive actions always; prefer explicit over undo |
| Error recovery | Verbose; state what happened AND how to fix, in plain language |
| Default text style | Avoid all-caps; avoid condensed fonts |

### Children (primary audience under 12)

Signals: "kids app", "children", "educational for young learners", COPPA references.

| Variable | Default |
|----------|---------|
| Touch target | 56pt iOS / 64dp Android minimum |
| Touch gap | 16pt / 16dp minimum |
| Reading level | Match target age; visual cues for pre-readers |
| Text-only CTAs | Avoid; pair text with icon always |
| Navigation | Very shallow; a single back affordance always visible |
| Destructive actions | Multi-step confirmation; avoid in primary flows |
| External links | Explicit parental gate if app is COPPA-scoped |
| Ads / IAP | Must be unambiguously outside the play surface and gated |
| Error tone | Friendly, non-blaming, reassuring |

### Power users / professional tools

Signals: "power users", "pro", "enterprise tool", "daily driver", "trading", "operations".

| Variable | Default |
|----------|---------|
| Density | Medium-to-dense; comparison tasks favored |
| Keyboard shortcuts | First-class where possible (iPad hardware keyboard, Android Bluetooth) |
| Batch operations | Default; not a power-user afterthought |
| Advanced filters | Visible by default, not hidden behind "more" |
| Undo window | Long (10–30s) or persistent action history |
| Confirmation | Minimized; trust the user, support undo instead |
| Animation | Fast (100–200ms); skippable; no flashy transitions |
| Onboarding | Skippable; "show me the app" must be one tap away |

### General consumer (default if no audience signal)

Signals: absent, or "mass market", "general users", "broad audience".

| Variable | Default |
|----------|---------|
| Body text | 15pt iOS / 14sp Android (`quality-bars.md` minimum) |
| Touch target | Platform minimum (44pt / 48dp) |
| Density | Medium; balanced between focus and information |
| Motion | Standard durations per `quality-bars.md` |
| Navigation | Standard bottom nav (3–5 destinations) |
| Onboarding | Light; one primary-value screen, then the app |
| Confirmation | For destructive or irreversible actions only; trust + undo elsewhere |

---

## Domain dimension

### Finance / payments / banking

Signals: "banking app", "wallet", "investing", "insurance", "payments", "billing".

| Variable | Default |
|----------|---------|
| Trust surface | Explicit: visible account status, last sync time, session info |
| Numeric alignment | Tabular (monospaced or right-aligned) for amounts |
| Decimals | Consistent precision; currency symbol placement per locale |
| Destructive language | "Cancel" near money fields must disambiguate (account vs form cancel) |
| Confirmation | Always for transfers, withdrawals, account changes; show amount + recipient + source |
| Biometric re-auth | For sensitive views (account details, transfers) and after inactivity |
| Empty states | Informative; explain why balance is zero, not a generic illustration |
| Error handling | Never silent; financial errors must be visible even in background tasks |
| Density | Medium-high; comparison across accounts is a common task |

### Health / medical

Signals: "health app", "medical", "clinical", "medication", "patient", "fitness tracking".

| Variable | Default |
|----------|---------|
| Data-entry tolerance | Low; validate aggressively, surface format before submit |
| Units | Always labeled (mg, mmHg, kg, bpm); support locale variants |
| Critical alerts | Never suppressed by notification settings; separate channel |
| Privacy surface | Explicit; what is shared, with whom, retention periods |
| Destructive actions | Multi-step; history of changes visible |
| Medication flows | Never allow silent skip; confirm dose; clear timing |
| Accessibility | AAA contrast for critical readings; large-text-tolerant |
| Emergency affordance | If relevant, persistent access to emergency contact or instructions |

### Social / community

Signals: "social", "community", "chat", "forum", "dating", "sharing", "feed".

| Variable | Default |
|----------|---------|
| Authoring surface | Persistent, reachable in thumb zone |
| Moderation / reporting | Always reachable from content; not buried 3 levels deep |
| Block / mute | First-class; not hidden in settings |
| Privacy controls | Granular and visible; default toward less sharing |
| Real-time indicators | Clear online/offline state; distinguish typing from idle |
| Notification density | User-tunable; channels per interaction type |
| Content warnings | Available for sensitive topics; respect OS-level preferences |

### E-commerce / retail

Signals: "shopping", "store", "marketplace", "checkout", "cart".

| Variable | Default |
|----------|---------|
| Price visibility | Always; no hidden totals until checkout |
| Cart persistence | Across sessions and devices if signed in |
| Guest checkout | Available unless impossible (subscription, KYC) |
| Payment options | Apple Pay / Google Pay shown above manual card on mobile |
| Address entry | Autocomplete (platform contacts + address API) |
| Shipping | Visible before final confirm, not surprise at the end |
| Returns policy | Reachable from product and order pages |
| Out-of-stock | Surface early; don't let user fill a cart with unavailable items |

### Enterprise / B2B

Signals: "enterprise", "internal tool", "admin panel on mobile", "B2B", "operations".

| Variable | Default |
|----------|---------|
| Density | Medium-to-dense; users are trained and expect information |
| SSO | First-class; email-and-password is the fallback |
| Roles and permissions | Visible; what the user can and cannot do must be discoverable |
| Audit trail | Accessible for actions with organizational impact |
| Bulk actions | Supported on lists; multi-select is standard |
| Tablet parity | Consider landscape and split-screen layouts |
| Offline | Partial-offline support for field use; sync on reconnect |

### Government / public service

Signals: "gov", "public service", "tax", "benefits", "voting", "civic".

| Variable | Default |
|----------|---------|
| Reading level | Plain language; target grade 8 or lower |
| Language support | Multilingual by default; localized error messages |
| Accessibility | AAA where feasible; must be operable on older devices |
| Jargon | Avoid; government terminology must be translated to plain language |
| Trust cues | Official seals, .gov domains, clear "this is the official app" framing |
| Form fields | Label everything; no placeholder-only labeling; example format shown |
| Save and resume | Mandatory for long forms |
| Accountability | Contact information and help path visible from every screen |

### Productivity / utility

Signals: "note-taking", "tasks", "calendar", "email", "writing", "reader".

| Variable | Default |
|----------|---------|
| Fast capture | One-tap entry from anywhere in the app |
| Keyboard shortcuts | Supported on iPad / Bluetooth keyboard |
| Search | Always in a predictable location; indexes user content |
| Sync transparency | Last sync time visible; conflict resolution surfaces |
| Offline-first | Reads and writes work offline; sync queued |
| Organization | Flat by default; hierarchy is opt-in, not forced |

### Entertainment / media

Signals: "streaming", "music", "video", "gaming", "reading".

| Variable | Default |
|----------|---------|
| Onboarding friction | Minimal; sign up is deferred, trial content is foregrounded |
| Playback controls | Platform-native; respect system media controls |
| Background behavior | Continue playback per platform rules (audio sessions / foreground services) |
| Cast / AirPlay | Supported where relevant |
| Discoverability | Browse + search + personalized; don't force just one |
| Download for offline | First-class for long-form content |

---

## Platform dimension

### iOS specifics (supplement to `docs/quality-bars.md`)

| Variable | Default |
|----------|---------|
| Navigation | Native UINavigationController patterns; large titles for top-level |
| Tab bar | 3–5 tabs; "More" for overflow |
| Sheet presentation | Bottom sheet or form sheet for secondary flows |
| Destructive actions | Red text in action sheets; confirm via system-style alert |
| Pull-to-refresh | Where list data is user-driven and cacheable |
| Haptics | Used for success, warning, error confirmations; not on every tap |
| Apple Pay | Above manual card entry for payment |
| Sign in with Apple | Required where other third-party sign-in is offered |
| Dark mode | Respect system setting; semantic colors, not hardcoded hex |
| Dynamic Type | Full support for accessibility sizes |

### Android specifics (supplement to `docs/quality-bars.md`)

| Variable | Default |
|----------|---------|
| Navigation | Bottom nav (3–5) or nav drawer depending on hierarchy |
| Back behavior | Predictable; system back and in-app back are consistent |
| Edge-to-edge | Support insets properly; don't hide content behind system bars |
| Material version | Material 3 by default unless product has a strong custom language |
| FAB | For a single primary action on content-heavy screens |
| Destructive actions | Confirm via Material dialog; red text for destructive item |
| Pull-to-refresh | Standard for list data |
| Predictive back | Support the gesture (Android 13+) |
| Themed icons | Provide monochrome adaptive icon asset |
| Dark theme | Respect system; use Material tonal colors |

Version-bound rows above (Material version, predictive back, themed icons) are current as of this skill's last review, not permanent facts. Name the OS level or design-system version a default assumes when it materially affects the recommendation. See guardrail 16.

### Cross-platform

| Variable | Default |
|----------|---------|
| Shared structure | Shared first; split only where conventions materially differ |
| Navigation paradigm | Choose one (tab bar / bottom nav / drawer) and apply consistently |
| Platform idioms | Respected where differences matter (back, sheets, haptics, system dialogs) |
| Component library | Use a library that handles platform divergence (or implement both paths explicitly) |
| Typography | Platform default system font unless brand dictates otherwise |

### Tablet

Signals: "iPad", "iPadOS", "tablet", "Android tablet", "Chromebook", "large screen", "Split View", "Slide Over", "Stage Manager", "multi-window", "keyboard case", "Apple Pencil", "stylus", or a use context implying a mounted or two-handed device (kiosk, point of sale, clinician or bedside, field technician, warehouse, classroom, studio, control room).

| Variable | Default |
|----------|---------|
| Width classes | Compact < 600 dp / medium 600–839 dp / expanded ≥ 840 dp — design against the class, never the device model |
| Layout | List-detail once the window clears ~700 pt (list 320–400 pt, detail ≥ 320 pt); one pane below that |
| Primary navigation | Bottom bar at compact / navigation rail 80 dp at medium / sidebar 240–360 dp at expanded |
| Screen margin | 16 pt compact / 24 pt medium / 24–32 pt expanded |
| Reading column | 640–720 pt maximum; extra width becomes margins or columns, never longer lines |
| Grid columns | 2 compact / 4–6 medium / 6–8 expanded |
| Touch target | Phone minimums still apply — 44 pt / 48 dp; a pointer is not a licence to shrink |
| Detail pane at rest | Never blank: the restored selection, or a named placeholder carrying the pane's primary action |
| Multitasking | Split View, Slide Over, Stage Manager (iPadOS) / multi-window (Android); resize without state loss |
| Keyboard | Hardware keyboard first-class if a typing-heavy app; focus always visible |
| Landscape | Design for both orientations if the app is content-consumption |

The numbers here are the large-screen bars from `docs/quality-bars.md`, repeated for lookup at the point of decision; that file stays authoritative. The reasoning behind them is in `docs/adaptive-layout.md`, and the pattern choices they feed are in `docs/patterns-catalog.md` §15.

---

## Use-context dimension

### One-handed use (default for phones)

| Variable | Default |
|----------|---------|
| Primary actions | Thumb-reachable lower half of the screen |
| Navigation | Bottom nav over top nav; iOS lower sheet handle over top bar |
| Destructive actions | Not adjacent to primary; placed to prevent fat-finger tap |
| Reachability | Respect platform reachability modes (iOS, Android one-handed modes) |

### Outdoor / bright-light use

Signals: "outdoor", "delivery app", "field tool", "rideshare driver".

| Variable | Default |
|----------|---------|
| Contrast | Bump one tier above WCAG minimum |
| Typography | Heavier weights for glanceability |
| Color | Avoid pastels and low-saturation pairs |
| Dark mode | Not default; outdoor readability typically favors light mode |

### In-vehicle / driving

Signals: "car", "driving", "navigation primary use", CarPlay / Android Auto.

| Variable | Default |
|----------|---------|
| Surface | CarPlay / Android Auto canvas only; mobile UI is the passenger view |
| Interaction | Voice-first; minimal taps |
| Confirmation | No destructive actions while in drive mode |
| Information density | Very sparse; one decision per glance |
| Animation | Minimal; no distracting motion |

### Emergency / high-stakes moment

Signals: "emergency", "SOS", "crisis", critical operational alerts.

| Variable | Default |
|----------|---------|
| Decisions per screen | One |
| Contrast | Maximum available |
| Touch target | Largest practical |
| Animation | None; instant state changes |
| Friction | Zero for the critical path; confirmation only for destructive |
| Text | Short, imperative ("Call now", "Confirm safe") |

### At-desk / stable use

Signals: "office use", "desk", "workstation", professional long-session use.

| Variable | Default |
|----------|---------|
| Session length | Design for extended use; reduce eye strain |
| Density | Medium-to-dense acceptable |
| Motion | Standard; users tolerate richer animation |
| Notifications | Less interruptive; rely on user checking the app |

---

## Resolving conflicts across dimensions

When multiple context signals apply, use this precedence:

1. **Safety and accessibility constraints** always dominate. An accessibility-sensitive audience overrides density preferences from a domain default.
2. **Regulated domain constraints** (finance, health, government) override stylistic defaults from other dimensions.
3. **Use-context constraints** (driving, outdoor, emergency) override audience and domain defaults when the usage moment is active.
4. **Audience constraints** override domain defaults on ergonomic values (touch, type, gesture).
5. **Platform defaults** fill in anything the other dimensions did not specify.

When precedence is unclear, state the conflict in `Assumptions` and resolve toward the more conservative option. The user can relax if needed; the reverse is harder.

---

## When to deviate

Deviate from a default when:

- The user has provided an explicit constraint that contradicts it (honor the user, note the deviation).
- Research, telemetry, or evidence in the input suggests the default is wrong for this specific product.
- A regulated requirement mandates something stricter or different.

Do not deviate when:

- The deviation is aesthetic.
- The deviation would soften a `quality-bars.md` minimum.
- The deviation removes accessibility or safety behavior.

Every deviation must be stated in the response, tied to a specific reason, not assumed.

---

## Maintenance

- When a new context pattern is observed in the field, add a row here with defaults.
- When platform guidance publishes a material update (HIG, Material 3), review the platform section.
- Audit defaults against `docs/quality-bars.md` minimums quarterly; any row that softens a bar is a bug.
- Do not inflate this document with speculative scenarios. Add a context only when a real request benefits from tuning.
