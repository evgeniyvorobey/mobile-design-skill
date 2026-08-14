# Visual Review Fixtures

This document indexes synthetic visual-review fixtures for `mobile-design-skill`.

The fixtures do not contain screenshots, real products, real brands, or copied UI. They are Figma-like text descriptions designed to test review discipline:

- critique concrete structure, hierarchy, states, and interaction behavior
- avoid unsupported visual claims when no image is provided
- avoid compliance, conversion, safety, or research claims without verification
- translate findings into specific fixes instead of vague taste feedback
- apply the 1-5 design-quality rubric with an appropriate confidence qualifier

Use these fixtures when evaluating Mode D: `Review screen for usability/accessibility`.

## Fixture Type

Each fixture is a description-only review case. Treat it as `D2: text description only`.

The skill may review:

- structure and ordering
- stated dimensions and density
- described typography roles
- named colors only as stated
- known component states
- stated constraints
- task, risk, and recovery gaps

The skill must not claim:

- exact spacing, balance, visual weight, or contrast beyond the provided specs
- accessibility compliance
- regulatory compliance
- usability test outcomes
- conversion, retention, or business impact
- real platform correctness unless tied to known platform guidance or framed as a recommendation

## Fixture Schema

Every fixture uses this structure:

- `Review setup` - platform and evidence scope
- `Screen description` - product context and user task
- `Frame specs` - device/frame assumptions and density notes
- `Visible hierarchy` - ordered visual/content priority as described
- `Components` - named UI elements and grouping
- `Typography` - stated text roles and size/weight signals
- `Color and state notes` - described color semantics and component states
- `Interaction states` - default, loading, error, disabled, success, or recovery behavior
- `Known constraints` - business, safety, platform, or implementation constraints
- `Expected critique` - issues the skill should identify
- `Prohibited critique` - claims the skill should not make from text-only evidence
- `Severity expectations` - expected priority tiering
- `Rubric score expectation` - expected current design-quality score and reason

## Coverage

| Fixture | File | Primary risk tested |
| --- | --- | --- |
| Fintech dashboard dense summary | `examples/visual-review-fixtures/fintech-dashboard-dense-summary.md` | Trust, financial clarity, density, color-only semantics |
| Health appointment booking | `examples/visual-review-fixtures/health-appointment-booking.md` | Safety escalation, appointment state clarity, evidence boundaries |
| Enterprise SaaS mobile table/card list | `examples/visual-review-fixtures/enterprise-saas-mobile-table-card-list.md` | Dense operational scanning, status semantics, bulk-action risk |
| Marketplace product detail/checkout edge | `examples/visual-review-fixtures/marketplace-product-detail-checkout-edge.md` | Price clarity, inventory volatility, checkout recovery |
| Social profile privacy/control | `examples/visual-review-fixtures/social-profile-privacy-control.md` | Privacy audience clarity, destructive controls, preview gap |
| Education quiz/results | `examples/visual-review-fixtures/education-quiz-results.md` | Feedback quality, color-only correctness, learner recovery |
| iPad team inbox stretched phone | `examples/visual-review-fixtures/ipad-team-inbox-stretched-phone.md` | Width-blind layout, bottom tabs at expanded width, unbounded measure, undefined detail-pane state |

## Pass Criteria For A Skill Review

A good review should:

- begin with `Mode: Review screen for usability/accessibility`
- state that the review is based on a text description, not a screenshot
- include at least one real strength
- separate high-risk issues from craft issues
- include `Unresolved assumptions` for visual details not provided
- recommend concrete fixes that can be implemented
- use severity consistently
- include a provisional current design-quality score when scoring is requested or expected

## Fail Criteria

Hard-fail a review if it:

- claims the design is compliant without verified evidence
- gives exact contrast or pixel-perfect judgments not included in the fixture
- says the design copies or resembles a real brand
- invents user testing, conversion impact, medical safety validation, or fraud reduction
- treats inspiration or aesthetics as evidence
- only says "make it cleaner" or "improve hierarchy" without specifying what changes
