# UX Scenarios

<!-- Managed with super-ux (ux-contract v4). Update in the same change as any user-facing behavior change. -->

## Index

| ID | Title | Feature | Persona | Traces | Status | Last audit |
|----|-------|---------|---------|--------|--------|------------|
| SCN-001 | Cancel a subscription | billing | P-01 | ST-001 | implemented | none |

## Personas

Defined in foundation.md.

## billing

### SCN-001: Cancel a subscription
- **Persona:** P-01
- **Feature:** billing
- **Traces:** ST-001, FLW-01 (JTBD-01, JRN-01/#1)
- **Entry point:** the subscriptions list
- **Preconditions:** one active plan
- **Steps:**
  1. User taps Cancel on a plan -> system asks to confirm
  2. User confirms -> system cancels the plan and marks it cancelled
- **Expected result:** the plan shows as cancelled and billing stops
- **UI elements:** cancel button, confirm dialog
- **States covered:** success, error
- **Errors & recovery:** cancel fails -> inline error with retry, the plan stays active
- **Status:** implemented
- **Coverage:** `src/app.js:1-3 cancelSubscription`
- **Product:** unobserved
