# Example: Review screen for usability/accessibility

## Example prompt

```text
Use the mobile-design-skill.

Review this cross-platform mobile profile edit screen for usability and accessibility.

Screen description:
- title at top
- profile photo
- name, email, phone, birthday, address, company, job title all in one long form
- save button only at bottom
- placeholders are being used as labels
- required fields are not marked until submit
- errors appear only in red text
- there is a back arrow but unsaved changes behavior is unclear

Constraints:
- enterprise app
- high density
- many users are older
```

## Example output

```md
Mode: Review screen for usability/accessibility
Platform scope: Cross-platform
Assumptions:
- This is a phone-first screen.
- Email may be read-only in some account states, but that is not shown here.
- No section collapsing is currently implemented.

## Quick summary
The screen appears functionally complete but structurally overloaded. The main risks are weak form clarity, poor error prevention, insufficient labeling, and fragile completion behavior on a long mobile form. The design is likely to create avoidable errors and unnecessary scrolling, especially for older users or users with larger text settings.

## Strengths
- Common profile fields are present in one place.
- The top title and profile image create basic orientation.
- A single save action reduces ambiguity about how edits are finalized.

## Usability issues
- The form is too long without visible grouping, which increases scanning effort.
- Save action only at the bottom creates completion friction and scroll dependency.
- Required fields are discovered too late, which encourages preventable submission errors.
- Unsaved-changes handling is unclear, creating exit anxiety.

## Accessibility issues
- Placeholder-only labeling is weak for comprehension and assistive technology support.
- Error communication depends on red text, which is insufficient as the only cue.
- Large-text users may struggle if the long stacked form becomes visually undifferentiated.
- The screen likely needs better focus movement and error announcement behavior, though this cannot be verified from the description alone.

## Hierarchy and readability issues
- All fields appear to have near-equal visual priority.
- No sectional hierarchy means users must parse the entire form as one block.
- Dense profile fields such as address and company info should be grouped or progressively disclosed where appropriate.

## Navigation and interaction issues
- Back arrow behavior is unclear when changes are unsaved.
- Long-form completion likely feels fragile without a persistent save affordance or clear progress feedback.
- If keyboard behavior is not carefully managed, bottom controls may become hard to reach.

## Severity / priority
- High:
  - placeholder-only labels
  - late required-field feedback
  - unclear unsaved-changes handling
- Medium:
  - lack of grouping
  - bottom-only save action
  - error reliance on color
- Low:
  - visual hierarchy refinement after structural fixes

## Recommended fixes
- Replace placeholders with persistent field labels.
- Group fields into sections such as Personal, Contact, Work, and Address.
- Mark required fields before submission.
- Add inline validation and supporting helper text where needed.
- Use icon, text, and placement cues for errors rather than color alone.
- Add a sticky or persistently reachable save action for long forms if appropriate.
- Define explicit unsaved-changes behavior on back navigation.
- Consider reducing scope by moving low-frequency fields into a secondary “More details” section if business rules allow.

## Platform-convention mismatches
- Cross-platform caution: back behavior must remain predictable and should not silently discard edits.
- If the same screen is used on both iOS and Android, the save and exit patterns should still respect each platform’s navigation expectations rather than acting like a web form dropped into a phone.

## Unresolved assumptions
- Cannot verify field editability rules.
- Cannot verify keyboard handling.
- Cannot verify accessibility semantics or assistive technology announcements.
- Cannot verify text scaling resilience from the description alone.

## Next actions
- Restructure the form into grouped sections before polishing visuals.
- Define unsaved-changes behavior explicitly.
- Run a quick review with large text and error scenarios.
```
