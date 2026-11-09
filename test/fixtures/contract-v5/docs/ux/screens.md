# UI Screen Registry

<!-- screens-format: 2 -->
<!-- Managed with super-ux (ux-contract v5). The UI map. -->

## Index

| ID | Screen | Used by | Figma | Status | Coverage |
|----|--------|---------|-------|--------|----------|
| SCR-01 | Subscriptions | FLW-01 | none | built | src/app.js:1-3 |

## Design system
- **Axes:** viewport: 375, 1280; theme: light; text: default; locale: en

## Web surfaces
- **Web surfaces:** no

## Screens

### SCR-01: Subscriptions
- **Used by:** FLW-01 (step 1)
- **Purpose:** see every plan and cancel one
- **Fronts:** CAP-01
- **Why human:** oversight (JTBD-01: the owner reviews what an agent cancelled)
- **States:**
  | State | Trigger | Behavior |
  |---|---|---|
  | default | open | the list, with a cancel action per plan |
  | error | cancel failed | inline error and retry |
- **Coverage:** `src/app.js:1-3 cancelSubscription`
- **Scenarios:** SCN-001
- **Status:** built
