# Capabilities

<!-- Managed with super-ux (ux-contract v5). What people and agents can do: one CAP-NN per effect set. -->

## Index

| ID | Capability | Actors | Gate | Status |
|----|------------|--------|------|--------|
| CAP-01 | Cancel a subscription | human, agent | none | specified |

## Capabilities

### CAP-01: Cancel a subscription
- **Traces:** ST-001
- **Actors:** human, agent
- **Agent excluded:** none
- **Roles:** owner, billing-admin
- **Gate:** none
- **Tools:** billing_subscription_cancel
- **Emits:** subscription.cancelled
- **Data:** payment
- **Automation:** none
- **Human surface:** SCR-01; Why human: oversight (JTBD-01: the owner reviews what an agent cancelled)
- **Since:** v1
- **Status:** specified
