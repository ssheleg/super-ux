# Test panel: <product>

Ten portraits the design-tester walks through the scenarios before and after a build
(task-pipeline `references/design-review.md`). A panel is a **test instrument**: it decides
what to test, never what to build. Each portrait says its basis: `evidence RE-NN` when the
research ledger supports it, `hypothesis` when it is a reasoned guess filling coverage.

Revision: <date> · confirmed by the operator: <yes/no> · foundation: `docs/ux/foundation.md`

Every portrait keeps these eight lines, in this form, so `design_gate.py panel` can read them.
The `retention` line opens with `local` or `tourist`, and the panel carries at least two of
each (see the note at the end).

## P-01 <short name>

- **basis**: evidence RE-01, RE-04 | hypothesis
- **situation**: <who, where, on what, under what pressure>
- **goals**: <the jobs they hire the product for, in their words>
- **features**: <the features they actually use, by name>
- **scenarios**: <two to four composite chains across features, by SCR- id: SCR-03 → SCR-07>
- **activation**: <steps to first value, and the step they are likely to drop at>
- **retention**: local | tourist: <trigger → action → reward → what brings them back, and what makes them leave>
- **needs**: <device and engine, locale, text size, accessibility, connection>

## P-02 <short name>

- **basis**: …
- **situation**: …
- **goals**: …
- **features**: …
- **scenarios**: …
- **activation**: …
- **retention**: …
- **needs**: …

<!-- … through P-10. Spread the ten across the foundation's personas, the activation stages
(new, activating, active, at risk, returning), and the needs that change a screen: small
phone, large text, keyboard only, a second locale, a slow connection.

Locals and tourists: at least two portraits are locals (high engagement, enter their data or
connect sources, arrived through a friend, build the product into their routine) and at least
two are tourists (low engagement, enter little, arrived through an ad or a discount, try many
services). Locals are who the product's lifetime value rests on; tourists are most of its churn.
Source: GP Bullhound, Consumer Subscription Software, October 2025, p. 71. -->
