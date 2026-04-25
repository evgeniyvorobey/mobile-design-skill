# Social Mobile Domain Pack

Use this pack for mobile experiences involving feeds, communities, messaging, creator networks, comments, profiles, reactions, groups, sharing, discovery, live content, or user-generated content.

This pack provides recommendations, not proof of safety, moderation effectiveness, community health, legal compliance, or engagement quality.

## When To Use

- Any product with user-generated content visible to other users.
- Feeds, posts, comments, replies, direct messages, groups, communities, or live rooms.
- Creator tools, media publishing, collaboration, sharing, following, reputation, or notifications.
- Social layers inside another domain, such as marketplace messaging or education discussion.

## Primary User Jobs

- Discover relevant people, content, groups, or conversations without losing control.
- Publish or respond with the right audience, privacy, and edit/delete options.
- Manage identity, profile, visibility, notifications, and relationship boundaries.
- Stay safe from harassment, spam, impersonation, scams, and unwanted contact.
- Report, block, mute, hide, restrict, or leave without friction.
- Understand moderation outcomes and recover from mistakes where appropriate.

## Trust And Safety Risks

- UGC without reporting, blocking, moderation, or clear terms.
- Anonymous or high-velocity interactions that amplify harassment or abuse.
- Privacy leakage through audience defaults, read receipts, location, contacts, or media metadata.
- Notification loops that create pressure, shame, or compulsive checking.
- Creator monetization or ranking that incentivizes unsafe content.
- Age, identity, consent, and sensitive-content boundaries not represented in the UI.
- Moderation copy that overpromises speed, fairness, or guaranteed outcome.

## Common Mobile Surfaces

- Home/feed with ranking controls, freshness, following/discover separation, and content warnings.
- Composer with audience, media, alt text, draft, privacy, tagging, and preview.
- Profile with identity, bio, links, followers, privacy, report/block, and verification context.
- Comments/replies with threading, moderation affordances, and collapsed sensitive content.
- Messaging with requests, blocking, reporting, media permissions, safety notices, and deletion states.
- Notifications with priority, grouping, quiet controls, and safety-relevant alerts.
- Moderation center with reports, appeals, hidden content, muted words, and community rules.

## Hierarchy Guidance

- Put audience and privacy context near publishing actions.
- Keep report, block, mute, and hide reachable from content, profile, and message context.
- Separate user-controlled feeds from algorithmic discovery when possible.
- Make content warnings specific without sensationalizing the content.
- Expose relationship state clearly: following, friend, member, blocked, muted, restricted, requested.
- Show moderation status in user language: submitted, under review, action taken, no action, appealed.
- Avoid making engagement metrics more prominent than safety controls in vulnerable contexts.

## State And Recovery Requirements

- Empty: no posts, no followers, no messages, no communities, no notifications.
- Loading: avoid content jumps that cause accidental taps or missed controls.
- Hidden/removed: explain visibility and available appeal/edit actions.
- Reported: acknowledge report, set expectations, and provide immediate block/mute options.
- Blocked/muted: show reversible state and impact without escalating conflict.
- Permission: camera/photos/contacts/microphone/location must have clear purpose and denial path.
- Offline: preserve drafts and clearly mark unsent messages or pending uploads.
- Recovery: edit, delete, undo send where supported, restore draft, appeal, leave group, change audience.

## Accessibility Notes

- Support alt text and captions for media-first experiences.
- Do not rely only on color, animation, or haptics for reactions, warnings, or relationship states.
- Ensure compose, media picker, mentions, hashtags, comments, and moderation menus are screen-reader navigable.
- Avoid motion-heavy infinite feeds without reduce-motion behavior.
- Keep tap targets generous around destructive and safety actions.
- Make notification and privacy settings searchable and understandable.

## Platform Notes

- Follow Apple App Review and Google Play UGC requirements for reporting, blocking, moderation, and contact information.
- Use native share sheets, media permissions, notification settings, and content privacy affordances where possible.
- Respect iOS and Android expectations for deep links, back behavior, media upload progress, and notification channels.
- Avoid custom gestures as the only way to access safety or privacy controls.
- Design lock-screen notification previews for privacy-sensitive message and community contexts.

## Evidence And Compliance Boundaries

- Do not claim a social design is safe because it has report/block buttons.
- Do not infer age assurance, child safety, DSA, privacy, or regional moderation obligations without expert review.
- Do not claim ranking, engagement, or retention impact from benchmark examples.
- App-store UGC guidance is a minimum policy anchor, not a complete trust/safety program.
- This pack is not compliance proof; privacy, child-safety, moderation, and regional obligations need qualified review.
- Content moderation operations, escalation SLAs, and appeal rules need product-policy ownership.

## Design-Quality Traps

- Engagement-first feed hierarchy that buries safety and privacy controls.
- Audience ambiguity at the moment of posting.
- Reporting flows that feel like forms for the company instead of protection for the user.
- Notifications that mix safety, social pressure, and marketing in one channel.
- Profile verification visuals that imply trust beyond what is verified.
- Infinite scroll with no recovery, grounding, or control over ranking.

## Handoff Checks

- Define UGC surfaces, audience models, visibility states, and default privacy settings.
- Specify report, block, mute, restrict, hide, delete, appeal, and moderation-status flows.
- Include media permissions, alt text, captions, content warnings, and sensitive-content handling.
- Document notification categories, quiet modes, lock-screen privacy, and escalation paths.
- Map identity, verification, impersonation, spam, abuse, and age-related review items.
- Flag policy, legal, privacy, security, and trust/safety operations review requirements.

## Source Anchors

- Apple App Store Review Guidelines for user-generated content.
- Google Play User Generated Content policy.
- Apple HIG, Android mobile UI guidance, W3C WCAG 2.2, W3C mobile accessibility.
- Use these as grounding references; moderation safety requires product-specific policy and operations.
