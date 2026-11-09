# UX Scenarios

<!-- Managed with super-ux (ux-contract v5). Update in the same change as any user-facing behavior change. -->

## Index

| ID | Title | Feature | Persona | Traces | Status | Last audit |
|----|-------|---------|---------|--------|--------|------------|
| SCN-001 | Cancel a subscription | billing | P-01 | ST-001 | implemented | none |
| SCN-002 | An agent cancels a subscription | billing | P-01 | ST-001, CAP-01 | draft | none |

## Personas

Defined in foundation.md.

## billing

### SCN-001: Cancel a subscription
- **Persona:** P-01
- **Feature:** billing
- **Traces:** ST-001, FLW-01, CAP-01 (JTBD-01, JRN-01/#1)
- **Channel:** human
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

### SCN-002: An agent cancels a subscription
- **Persona:** P-01
- **Feature:** billing
- **Traces:** ST-001, CAP-01 (JTBD-01)
- **Channel:** agent
- **Entry point:** A-01 holds the owner's billing grant
- **Preconditions:** one active plan
- **Steps:**
  1. A-01 -> billing_subscription_cancel (plan, idempotency key) -> the plan returns with status cancelled
  2. A-01 repeats the call with the same key -> the same result, and no second effect
- **Expected result:** the plan is cancelled once and `subscription.cancelled` is emitted
- **Errors & recovery:** the grant lacks billing:write -> a typed refusal naming the missing scope
- **Status:** draft
- **Coverage:** none yet
- **Product:** unobserved
