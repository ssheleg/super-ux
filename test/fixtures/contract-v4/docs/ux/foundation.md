# UX Foundation

<!-- Managed with super-ux (ux-contract v4). The WHY layer. -->

## Personas

### P-01: Team owner
Runs a five-person team and pays for its tools.

## Jobs to Be Done

### JTBD-01: Stop paying for unused tools
- **Statement:** When a tool goes unused, I want to cancel it, so I can stop paying for it.
- **Personas:** P-01
- **Type:** functional
- **Forces:** push: waste; pull: one list; anxiety: losing data; habit: a monthly review
- **Success metric:** unused subscriptions are cancelled within a week of going idle

## Customer journeys

### JRN-01: Team owner, stop paying (JTBD-01)
- **Owner:** unknown
| # | Stage | User action | Touchpoint | Emotion (1-5) | Pain | Opportunity |
|---|-------|------------|------------|---------------|------|-------------|
| 1 | Review | opens the list | app | 3 | bills are scattered | one list |

## Design tooling
- **Figma:** disabled

## User stories

### ST-001: Cancel a subscription
- **Story:** As P-01, I want to cancel a subscription, so that I stop paying for it.
- **Traces:** JTBD-01, JRN-01/#1
- **Acceptance criteria:**
  - Given an active plan, when I cancel it, then billing stops and the list shows it cancelled.
- **Priority:** must
- **Status:** validated
