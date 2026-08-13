# Example: Design mobile user flow

## Example prompt

```text
Use the mobile-design-skill.

Design the mobile user flow for onboarding a new user into a personal budgeting app.

Inputs:
- Platform: iOS
- User goal: connect one bank account and see the first spending summary
- Audience: first-time users, low patience
- Constraints: wants a fast first-run experience, accessibility should be built in
```

## Example output

```md
Mode: Design mobile user flow
Platform scope: iOS
Device class: Phone (compact width only; a regular-width layout can be added on request)
Assumptions:
- Users can browse marketing content before sign-up but must authenticate before connecting an account.
- Account connection uses a secure third-party provider.
- The product allows skipping secondary personalization until after first value is delivered.

## Flow goal
Get the user from first launch to first meaningful spending summary with minimum friction.

## Entry points
- First app launch after install
- Return from app store or marketing email deep link into onboarding

## Ordered steps / screens
1. Welcome / value framing
   - short explanation of what the app helps with
   - primary CTA: Get started
2. Account creation or sign-in
   - email or social sign-in options if supported
3. Consent and privacy explanation
   - why account access is needed
4. Connect bank account
   - institution search
   - secure connection handoff
5. Connection result
   - success, partial success, or retry
6. Initial summary setup
   - loading and categorization progress
7. First spending summary
   - key insight, recent transactions, next recommended action

## Decision points
- Existing user vs new user → sign-in or create account
- User consents to bank connection vs exits flow
- Bank connection succeeds vs fails vs requires later retry
- Data import completes quickly vs requires background processing

## Back-navigation logic
- Users can back out of welcome and auth steps without losing state.
- If the user exits during bank connection, preserve progress and provide a clear resume path.
- Avoid sending users backward from the first summary into the connection flow unless they explicitly edit account setup.

## Failure and recovery paths
- Failed sign-up → inline correction without full reset
- Bank connection failure → retry, choose another bank, or continue with limited manual mode if supported
- Data import delay → show progress state with reassurance and optional notification path
- Permission hesitation → provide concise explanation instead of a dead-end warning screen

## Platform behavior notes
### iOS
- Keep transitions linear and calm; onboarding should feel guided rather than nested or visually noisy.
- Avoid overloading the first-run experience with too many parallel decisions.

### Android
- Not primary platform here, so no Android-specific flow guidance included beyond avoiding cross-platform divergence if later expanded.

## Accessibility and usability risks
- Too much financial explanation before action could delay first value.
- Third-party connection handoff may create orientation loss when returning.
- Loading states can feel broken if progress language is vague.
- Users with larger text settings may struggle if summary cards are too dense too early.

## Simplification opportunities
- Defer budget category customization until after first summary.
- Merge welcome and privacy framing if legal language can be summarized clearly.
- Offer one primary setup goal: connect one account first, not all financial accounts at once.

## Next actions
- Confirm whether manual account entry exists as a fallback path.
- Prototype the connection-return moment carefully because that is the likeliest trust drop.
- Test whether users understand what they get immediately after account connection.
```
