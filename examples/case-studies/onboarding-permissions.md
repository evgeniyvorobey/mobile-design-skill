# Synthetic Case Study: Onboarding Permissions

## Prompt

```text
Use the mobile-design-skill.

Design a mobile onboarding flow for a fitness tracker that needs notifications, motion/activity access, and optional location for outdoor workouts.

Inputs:
- Platform: iOS and Android
- User goal: start tracking a first workout quickly
- Audience: general consumers
- Constraints: avoid permission fatigue, explain privacy, app should still work if optional permissions are denied
```

## Weak response

```md
Mode: Design mobile user flow
Platform scope: iOS and Android
Assumptions:
- The app needs permissions.
- Users want quick onboarding.

Show three onboarding slides explaining benefits, then ask for notifications, motion, and location permissions. If the user declines, show a message saying they can enable permissions in settings. End with a start workout button. Use friendly illustrations and a progress indicator.

Accessibility and usability risks: keep text short and buttons large.
Next actions: test onboarding and adjust copy.
```

## Why this is weak

- Requests all permissions before the user understands the first workout task.
- Treats optional and required permissions as equivalent.
- Does not define degraded functionality when permission is denied.
- Optimizes permission acceptance without a privacy or trust guardrail.
- Platform differences around permission prompts and settings recovery are not addressed.

## Strong response

```md
Mode: Design mobile user flow
Platform scope: iOS and Android
Assumptions:
- A basic manual workout can start without optional location.
- Motion/activity access improves automatic tracking but may not be required for manual tracking.
- Notification permission is useful for reminders and workout completion, not required for first value.

## Flow goal
Get the user to a first useful workout quickly while asking for each permission at the moment its value is understandable.

## Entry points
- First app launch
- "Start first workout" from welcome screen
- Later permission recovery from workout setup or settings

## Ordered steps/screens
1. Welcome: value proposition and "Start workout setup"; secondary "Explore app".
2. Workout type: indoor, outdoor, or manual. This determines whether location is relevant.
3. Motion/activity rationale: explain automatic tracking benefit before native prompt if supported.
4. Workout setup: duration/goal optional; start manual workout remains available.
5. Outdoor route step: ask location only if user chose outdoor route tracking.
6. Notification step after first setup or after workout save: ask for reminders/completion alerts with skip.
7. Ready state: start workout, with visible permission status and recovery links.

## Decision points
- If motion is denied, allow manual workout and show "automatic detection unavailable".
- If location is denied, allow outdoor workout without route map if product supports it.
- If notifications are denied, reminders are off; workout tracking still works.
- If platform prompt has already been denied permanently, route to settings with instructions.

## Back-navigation logic
- Back from permission rationale returns to workout setup without losing selected workout type.
- Back after native prompt returns to the next app step with updated status.
- Leaving onboarding should not reset permission decisions.

## Failure and recovery paths
- Native prompt unavailable/previously denied: show status and settings link.
- Permission denied: explain the effect in one sentence and keep the primary task available where safe.
- Permission restricted by device policy: show non-blaming message and support link.

## Platform behavior notes
- iOS: use a pre-permission rationale screen, then native prompt; if denied, future recovery goes through Settings.
- Android: permissions may be requested at runtime and can vary by OS version; keep rationale tied to the specific feature being used.

## Accessibility and usability risks
- Avoid permission walls for optional features.
- Buttons should offer a clear non-punitive skip path.
- Permission status needs text labels, not icon-only checks.
- Rationale copy should be short and concrete: what is collected, why, and what still works if denied.

## Simplification opportunities
- First launch can skip a multi-slide carousel and move straight to workout setup.
- Notifications can be deferred until the user creates a reminder or saves the first workout.

## Next actions
- Confirm which permissions are truly required for each workout type and OS version.
- QA denied, restricted, previously denied, optional skip, settings recovery, and first-workout completion.
```

## Why this is stronger

- Quality target: 4/5 - strong once the permission taxonomy, manual fallback, and platform copy constraints are confirmed.
- Makes permission requests contextual instead of front-loaded.
- Defines graceful degradation for denied optional permissions.
- Splits iOS and Android behavior where it matters.
- Keeps first value accessible without dark patterns.
- Gives concrete recovery and QA states.

## Regression checks

- Does the flow avoid asking all permissions at launch?
- Does it distinguish required from optional permissions?
- Does it define what still works after denial?
- Does it give platform-specific recovery paths?
- Does it preserve selected workout setup across prompts and back navigation?
