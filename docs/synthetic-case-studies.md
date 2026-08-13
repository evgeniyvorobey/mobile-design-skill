# Synthetic Case Studies

This pack gives `mobile-design-skill` synthetic calibration examples for common mobile design tasks. The examples are intentionally not based on real products, proprietary workflows, copyrighted screenshots, or business metrics.

Use these files to compare a weak but plausible response against a stronger one, each carrying its own derived score. The goal is to train judgment: task specificity, state coverage, accessibility, platform awareness, alternatives, and handoff usefulness.

## Research Basis

The pack is grounded in the repository's own quality layers:

- `docs/design-quality-rubric.md`
- `docs/weaknesses.md`
- `docs/context-defaults.md`
- `docs/evals.md`
- `docs/golden-examples.md`

It also follows public source families already used by the skill:

- [Apple Human Interface Guidelines: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- [Android Developers: Accessibility in mobile design](https://developer.android.com/design/ui/mobile/guides/foundations/accessibility)
- [W3C WCAG2Mobile guidance](https://www.w3.org/TR/wcag2mobile-22/)

These sources inform the checks, but the case studies do not claim compliance or real-world validation.

## Coverage

| Area | File | Primary calibration focus |
| --- | --- | --- |
| Fintech account overview | `examples/case-studies/fintech-account-overview.md` | Trust, data freshness, privacy, numeric hierarchy |
| Health medication refill | `examples/case-studies/health-medication-refill.md` | Safety, eligibility, recovery, no medical overclaim |
| SaaS approval queue | `examples/case-studies/saas-approval-queue.md` | Dense enterprise decisions, audit trail, batch risk |
| Marketplace checkout/substitution | `examples/case-studies/marketplace-checkout-substitution.md` | Volatile inventory, consent, total changes |
| Social privacy settings | `examples/case-studies/social-privacy-settings.md` | Privacy clarity, audience preview, destructive settings |
| Education lesson progress | `examples/case-studies/education-lesson-progress.md` | Motivation without pressure, progress semantics, offline states |
| Onboarding permissions | `examples/case-studies/onboarding-permissions.md` | Contextual permission timing and denied-state recovery |
| Settings consent/destructive action | `examples/case-studies/settings-consent-destructive-action.md` | Consent semantics, deletion flow, reversibility boundaries |
| Search/results filtering | `examples/case-studies/search-results-filtering.md` | Query refinement, filter transparency, empty states |
| Empty/error state recovery | `examples/case-studies/empty-error-state-recovery.md` | Partial data, retry design, preserving user work |
| Typography/spacing system | `examples/case-studies/typography-spacing-system.md` | Token-ready roles, density rules, scaling behavior |
| Rationale/handoff | `examples/case-studies/rationale-handoff.md` | Decision rationale, implementation notes, validation plan |

## How To Use

- Read `Weak response` to understand the plausible regression.
- Read `Why this is weak` to identify which weakness pattern is present.
- Read `Strong response` as one worked answer with its own dimension read, not a universal template and not a score to aim at.
- Use `Regression checks` when reviewing future changes to the skill.

## Boundaries

- These case studies are synthetic fixtures, not product research.
- They must not be used to claim validated conversion, retention, medical, financial, accessibility, or compliance outcomes.
- They intentionally avoid screenshots and real brand references.
- Strong responses may contain assumptions, but those assumptions must be labeled and safe to revise.
