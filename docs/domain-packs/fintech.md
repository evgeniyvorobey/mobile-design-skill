# Fintech Mobile Domain Pack

Use this pack for mobile experiences involving money, payments, balances, budgets, identity, cards, investing, crypto, subscriptions, rewards, loans, or financial decision support.

This pack provides recommendations, not legal, compliance, investment, or security proof. Confirm regulated requirements with qualified product, legal, compliance, and security owners.

## When To Use

- Banking, wallet, card, payment, remittance, or budgeting apps.
- Investing, trading, portfolio, market-data, crypto, or retirement features.
- Subscription management, bill pay, taxes, payroll, lending, credit, or rewards flows.
- Any screen where incorrect wording, stale data, or accidental action could affect money.

## Primary User Jobs

- Understand current financial position without misreading pending or unavailable funds.
- Move money with confidence: send, pay, transfer, deposit, withdraw, or exchange.
- Detect risk: fraud, suspicious activity, subscription drift, unusual fees, or failed payments.
- Compare options without hidden costs, misleading emphasis, or advice laundering.
- Recover from declined, delayed, blocked, duplicate, or partially completed transactions.
- Manage trust settings: cards, limits, alerts, authentication, devices, beneficiaries, privacy.

## Trust And Safety Risks

- Stale balances or prices presented as current.
- Ambiguous money movement, especially irreversible transfers or exchange-rate changes.
- Hidden fees, spread, tax assumptions, subscription renewal terms, or cut-off times.
- Advice-like language that exceeds the product's authority or regulatory posture.
- Phishing-prone authentication, overbroad permissions, or insecure copy patterns.
- False reassurance from biometric login, encryption badges, or generic "bank-level" claims.
- Alert fatigue that causes users to ignore meaningful account-risk signals.

## Common Mobile Surfaces

- Account overview with balance, pending activity, alerts, and next best actions.
- Transaction detail with status, merchant, category, amount, fee, date, and dispute path.
- Transfer/payment composer with recipient, amount, source, timing, fees, and confirmation.
- Card management with freeze, limits, PIN, travel, tokenized wallet, and replacement states.
- Portfolio/watchlist with holdings, performance, risk labels, price timestamp, and chart.
- KYC/identity flow with document capture, review status, retry, and support escalation.
- Security center with trusted devices, passkeys/biometrics, alerts, recovery, and privacy.

## Hierarchy Guidance

- Put the user's actionable financial state first, not promotional modules.
- Pair every primary number with context: currency, account, status, timestamp, and scope.
- Separate settled, pending, available, projected, and estimated values visually and textually.
- Use confirmation screens for consequential actions; show final amount, recipient, fees, timing, and reversibility.
- De-emphasize upsell inside high-risk tasks such as payments, disputes, fraud, or recovery.
- Make risk language plain and specific: what happened, what it means, what the user can do.
- For charts, expose the primary insight in text; do not make color or line shape the only explanation.

## State And Recovery Requirements

- Empty: no accounts, no transactions, no cards, no linked bank, no portfolio holdings.
- Loading: skeletons must avoid implying a real balance before data arrives.
- Stale: show last updated time and a refresh path when data freshness matters.
- Pending: clearly distinguish authorized, processing, scheduled, posted, failed, reversed, or disputed.
- Blocked: explain compliance/security review without exposing sensitive detection logic.
- Error: preserve entered details, prevent duplicate submission, and explain retry safety.
- Offline: allow read-only cached views only when clearly labeled and safe.
- Recovery: include support, dispute, cancel, edit, retry, and receipt paths where applicable.

## Accessibility Notes

- Meet WCAG contrast targets and avoid red/green-only status coding.
- Support Dynamic Type/font scaling without clipping currency values or CTA labels.
- Provide text alternatives for charts, spark lines, balance deltas, and trend badges.
- Use clear labels for masked account numbers, amounts, dates, and destructive actions.
- Keep tap targets large enough for repeated numeric entry and one-handed review.
- Avoid time-boxed confirmations unless required; provide accessible countdown semantics if used.

## Platform Notes

- Prefer platform authentication APIs for biometrics/passkeys; do not present biometrics as a standalone security guarantee.
- Use native number pads and currency formatting, but preserve locale-specific separators and currency codes.
- Respect iOS and Android notification controls for security, transaction, and marketing alerts.
- On Android, account for predictive back and edge-to-edge layouts in payment confirmation flows.
- On iOS, preserve expected navigation hierarchy and avoid hiding system affordances during high-risk review.

## Evidence And Compliance Boundaries

- Benchmarks can inspire layout or sequencing, but cannot prove accessibility, security, compliance, or conversion.
- Do not claim a financial recommendation is suitable without the product's validated advisory framework.
- Do not infer KYC, AML, tax, lending, or securities obligations from generic design knowledge.
- Privacy labels and data-safety declarations are disclosure surfaces, not proof of good data practice.
- Security UI should align with security engineering decisions; design copy must not overpromise.

## Design-Quality Traps

- Premium styling that hides fees, timestamps, or risk states.
- Green growth visuals that imply performance certainty.
- Confirmation screens that look like receipts before an action completes.
- Empty states that push funding or trading before the user understands risk.
- Generic "secure and encrypted" badges without concrete user control or explanation.
- Dense dashboards that make the user hunt for failed, pending, or suspicious activity.

## Handoff Checks

- Define currency, precision, rounding, negative values, and locale formatting.
- Specify balance freshness, data-source labels, and pending/available semantics.
- List every transaction status and the copy/action available in each state.
- Include duplicate-submit prevention and idempotency expectations for payments.
- Provide chart accessibility text and non-color status tokens.
- Document permission, notification, security, and privacy surfaces separately from marketing.
- Flag legal/compliance/security review items rather than resolving them in design copy.

## Source Anchors

- Apple HIG, Apple accessibility, Android mobile UI guidance, W3C WCAG 2.2.
- Apple privacy information, Google Play Data safety, NIST digital identity guidance.
- Use these as grounding references; they do not replace product-specific compliance review.

