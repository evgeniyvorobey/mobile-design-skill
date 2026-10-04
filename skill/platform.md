# Platform facts

Checked against Apple's and Google's documentation between 2026-10-02 and 2026-10-04. These are the facts that changed recently or are often remembered a version behind. For the versions named here, this file wins over memory. For anything not listed, use what you know and name the OS version when the answer depends on it.

## iOS and iPadOS 26 and 27

- **Liquid Glass.** System bars and controls float above content and size themselves. Use the system components and do not pin bar heights in a spec: 44 pt and 49 pt are UIKit values from before iOS 26.
- **iPhone tab bar.** It sits at the bottom, floats, and can minimise as the person scrolls. Pin a custom bottom control to the safe area, not to a bar height.
- **iPad navigation.** The system tab bar sits near the top and can convert to a sidebar. Consider the tab bar first and a sidebar when the destinations have hierarchy. iPadOS has no navigation rail.
- **iPad windows.** Since iPadOS 26 app windows resize freely, and from iPadOS 27 `UIRequiresFullScreen` no longer opts an app out (TN3192). An iPad app has to work at any width, including compact.
- **iPhone Duo**, Apple's foldable iPhone (HIG page "Designing for iPhone Duo", added 2026-09-09). Do not design per pose. A compact-width layout for the outer display and a regular-width layout for the inner display are the basis for every pose. Keep function and state identical across the two displays and show one more level of hierarchy inside where it fits: a split view expands inside and collapses to one pane outside. Keep layouts clear of the outer camera, the inner camera when it is active, and the fold when the device is half open. Bars move to the side on the outer display and on the inner display in landscape. The page gives no point values for poses, so do not pin any.
- **Bottom edge.** Keep custom controls and custom gestures out of the bottom safe-area inset, where the home indicator's system swipes win.
- **Back swipe.** Since iOS 26 a pushed screen also goes back on a horizontal swipe that starts anywhere in its content, not only at the leading edge (`UINavigationController.interactiveContentPopGestureRecognizer`). Keeping a custom horizontal drag (a dial, a carousel, a swiped row) away from the edge does not avoid the conflict: say which gesture wins.
- **Before a permission alert.** A custom screen shown before a system permission alert has one button, titled like "Continue" or "Next", and that button opens the alert. It has no second action and no way to close, cancel or skip the alert, unless a legal consent needs one (HIG, Privacy). An alternative to granting, such as search in place of location, belongs on the screen before it or after the person has answered the alert.
- **Approximate location.** With Precise Location off, the position is usually within 1 to 20 km of the real one and updates at most a few times an hour (`kCLLocationAccuracyReduced`). It finds the city, not the street: do not centre a street-level map on it or rank "nearest" from it.
- **Login.** An app that offers a third-party or social login also offers an equivalent that limits data to name and email, lets the person keep their email private, and does not track for advertising without consent (App Review Guideline 4.8, revised January 2024). Sign in with Apple meets it and is no longer the only way.
- **Type.** Map every text role to a Dynamic Type style. A custom face takes the style's scaling and supplies its own tracking.

## Android 16 and Material 3 Expressive

- **Android 16 (API 36)** has been required for Play updates since 2026-08-31.
- **Edge-to-edge** has no opt-out. Handle the system bar insets.
- **Large screens.** On a display whose smallest width is at least 600 dp, the system ignores orientation, resizability and aspect-ratio restrictions (games are exempt), and Android 17 removes the developer opt-out.
- **Predictive back.** For an app targeting API 36 the animations are on by default, `onBackPressed` is not called and `KEYCODE_BACK` is not dispatched. Intercept Back with the back callbacks (`OnBackPressedCallback`, or `BackHandler` and `PredictiveBackHandler` in Compose), including for an unsaved-changes prompt.
- **Approximate location.** Since Android 12 a person can grant approximate location only, whatever the app asks for. It is accurate to about 3 km², where precise is usually within about 50 m (`ACCESS_COARSE_LOCATION`, `ACCESS_FINE_LOCATION`). Design the approximate case: it does not find a street or the nearest stop.
- **Windows.** Desktop windowing joins split-screen and freeform windows. Any of them can hand the app a compact width at any moment.
- **Navigation (Material 3 Expressive, May 2025).** The navigation drawer is deprecated in favour of the expanded navigation rail (220 to 360 dp). The collapsed rail is 96 dp. The navigation bar is 64 dp. Top app bars are 64 dp small, 112 dp medium and 152 dp large.
- **FAB (Material 3 Expressive).** 56 dp, medium 80 dp, large 96 dp. The 40 dp small FAB survives only as a baseline variant and is no longer recommended. Extended FAB: small 56 dp, medium 80 dp, large 96 dp.
- **Motion (Material 3 Expressive).** Components animate with spring tokens under one theme-level scheme: expressive, the recommended default, which overshoots, or standard, with minimal bounce, for utilitarian products. Each scheme has spatial tokens (position, size, rotation, corners) and effects tokens (colour and opacity, which never overshoot), each at fast, default and slow, for example `md.sys.motion.spring.fast.spatial`. In Compose: `MotionScheme.expressive()` and `MotionScheme.standard()`, read from `MaterialTheme.motionScheme`. Transitions between screens have not moved to springs and are still specified with easing and duration tokens.
- **Foldables.** Tabletop is half-opened with a horizontal hinge, book is half-opened with a vertical hinge. Keep content and controls off a hinge that separates or occludes the display (`FoldingFeature.isSeparating`, `occlusionType`). Treat a posture change like a width change: state survives it.

## Width, on both platforms

| Width class | Window width | Layout | Android navigation | iPadOS navigation |
|---|---|---|---|---|
| Compact | under 600 dp, or a compact size class | one pane | navigation bar | tab bar at the bottom |
| Medium | 600 to 839 dp | one pane, or two if the detail pane keeps at least 320 dp | navigation rail, 96 dp | system tab bar near the top |
| Expanded | 840 to 1199 dp | two panes | expanded navigation rail, 220 to 360 dp | the same tab bar, or a sidebar |
| Large | 1200 to 1599 dp | two panes | expanded navigation rail | tab bar or sidebar |
| Extra-large | 1600 dp and wider | two panes, or three | expanded navigation rail | tab bar or sidebar |

- Large and extra-large are Android's newer width classes (Jetpack WindowManager 1.5.0, and opt-in in Compose `material3-adaptive` 1.2.0: `currentWindowAdaptiveInfo(supportLargeAndXLargeWidth = true)`). Height classes: compact under 480 dp, medium 480 to 899 dp, expanded 900 dp and taller.
- Material 3 recommends two panes through large and suggests a third only at extra-large. A third pane in a narrower window is a deliberate choice: show the arithmetic that every pane keeps its minimum width.
- Slide Over and a narrow Split View return an iPad to compact width while the app is running, so the compact layout is never optional on a tablet.
- Choose from the established large-screen layouts before inventing one: list-detail, supporting pane, feed.
- A width change keeps scroll position, selection, text being typed and open sheets.
- A detail pane has its own empty state. Back is defined both with two panes and after they collapse into one.
- Touch minimums do not shrink for a pointer. Hover adds and is never the only path. Every drag has a path that is not a drag.
- Wider windows get more columns or wider margins, never longer lines: a reading column stays at 45 to 75 characters, about 640 to 720 pt.
