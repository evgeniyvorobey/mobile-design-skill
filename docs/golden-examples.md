# Golden Examples

These examples are regression targets for taste and design-quality calibration. They are intentionally compact: each one includes a prompt, a focused golden output, and notes about what should be rewarded or treated as a regression.

## Coverage

| Area | File | Calibration focus |
| --- | --- | --- |
| Premium UI | `examples/golden/premium-ui.md` | Premium as restraint, trust, imagery, and transparent decision support |
| Enterprise SaaS | `examples/golden/enterprise-saas.md` | Dense operational workflows, data freshness, permissions, and mistake prevention |
| Fintech | `examples/golden/fintech.md` | Trust-sensitive financial summaries, chart accessibility, and advice boundaries |
| Health | `examples/golden/health.md` | High-trust medical information, safe escalation, units, ranges, and clinician context |
| Onboarding | `examples/golden/onboarding.md` | Fast first value, contextual permission requests, and progress preservation |
| Settings | `examples/golden/settings.md` | Consent clarity, row semantics, destructive actions, and text-only review limits |
| Checkout | `examples/golden/checkout.md` | Fee transparency, volatile state recovery, substitutions, and final action confidence |
| Tablet list-detail | `examples/golden/tablet-list-detail.md` | Regular-width layout, navigation by width, detail-pane state, resize behaviour, and additive input |

## How To Use

- Use these as golden examples when judging whether a response has real design judgment rather than polished generic advice.
- Prefer answers that name concrete hierarchy, states, tradeoffs, accessibility implications, and production checks.
- Treat vague aesthetic language, invented visual observations, hidden high-risk states, and missing recovery paths as regressions.
