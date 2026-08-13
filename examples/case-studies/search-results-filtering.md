# Synthetic Case Study: Search Results Filtering

## Prompt

```text
Use the mobile-design-skill.

Design a mobile screen concept for search results and filtering in a rental marketplace.

Inputs:
- Platform: cross-platform
- User goal: narrow listings by price, availability, location, and amenities
- Audience: general consumers
- Constraints: many results, filters can create empty states, map and list may both be useful
```

## Weak response

```md
Mode: Generate mobile screen concept
Platform scope: Cross-platform
Assumptions:
- Users search for rentals.
- Filters are important.

Use a search bar at the top, a filter button, and a list of result cards. Add sort and a map toggle. Filters open in a modal with price, location, amenities, and availability. Show active filters as chips. Use infinite scroll for results.

Accessibility considerations: make filters tappable and labels clear.
Next actions: test with users and refine filters.
```

## Why this is weak

- Lists common pieces without deciding how users recover from over-filtering.
- Infinite scroll may hurt returnability and filter refinement.
- Map/list relationship, result counts, and active constraints are vague.
- Does not define loading, no results, partial results, or location permission behavior.
- Accessibility ignores filter state announcements and result count changes.

## Strong response

```md
Mode: Generate mobile screen concept
Platform scope: Cross-platform
Assumptions:
- Search results can be displayed as list, map, or a synced list-map state.
- Location permission is optional; typed location search must still work.
- Availability and price data can become stale.

## Screen goal
Help renters refine a large result set without losing context, over-filtering silently, or confusing map and list states.

## Primary user task
Find a manageable set of listings that match must-have constraints.

## Information hierarchy
1. Query/location and result count
2. Active must-have filters
3. Sort and map/list mode
4. Results with key comparison fields
5. Refinement and recovery options

## Recommended layout structure
- Sticky search summary: location/query, dates if relevant, and result count.
- Active filter chips: price, availability, amenities; each chip removable.
- Filter entry: one primary filter button with count of active filters.
- List/map switch: segmented or paired control; keep current filters visible in both modes.
- Result rows/cards: price, location area, availability, primary amenity flags, and saved state.

## Empty / loading / error states
- Loading: preserve active filters and show skeleton rows; announce that results are updating.
- No results: show which filters are restrictive and offer "remove last filter", "expand price", or "clear amenities".
- Partial results: label stale or unavailable sections; do not mix uncertain listings into normal results silently.
- Location denied: keep typed location search and explain what map features are unavailable.
- Network error: preserve query and filters; retry without clearing state.

## Alternatives considered
- Rejected: hidden filter-only modal with no active chips. It makes constraints hard to inspect.
- Rejected: infinite scroll as the only pagination model. Search refinement benefits from stable position and clear result counts.

## Platform-specific notes
- iOS: filter sheet can work if active chips remain visible after dismissal; preserve list scroll when opening details.
- Android: system back from filter sheet returns to results without losing unsaved edits unless user discards explicitly.

## Accessibility considerations
- Result count changes should be announced after filters apply.
- Filter chips need accessible remove actions with the filter value in the label.
- Map pins need list equivalents; do not make the map the only way to discover listings.
- Large text should keep price, location, and availability visible before secondary amenities.

## Design quality calibration
- Quality target: 3/5 - constraint transparency and recovery are handled well, but the screen is inert: with the logo removed it is interchangeable with any search-and-filter result list, and no owned asset was supplied or derived. Capped at 3/5 by the inert-screen test until one repeatable treatment exists; filter taxonomy, availability freshness, and map behavior still need confirming.
- The craft is in constraint transparency and recovery, not just richer cards.

## Next actions
- Confirm which filters are must-have versus preference and whether map bounds affect results.
- QA no results, location denied, stale availability, filter back behavior, screen reader announcements, and long locations.
```

## Why this is stronger

- Makes result count and active constraints central.
- Defines recovery from over-filtering.
- Treats map/list as linked states with accessibility alternatives.
- Preserves query and filters through errors.
- Avoids defaulting to infinite scroll when returnability matters.

## Regression checks

- Does the concept show active filters and result count together?
- Does it offer recovery from empty results?
- Does it preserve search state across errors and detail navigation?
- Does it avoid requiring location permission?
- Does it provide list equivalents for map information?
