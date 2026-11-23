# Test panel: <product>

Ten portraits the design-tester walks through the scenarios before and after a build
(task-pipeline `references/design-review.md`). A panel is a **test instrument**: it decides
what to test, never what to build. Each portrait says its basis: `evidence RE-NN` when the
research ledger supports it, `hypothesis` when it is a reasoned guess filling coverage.

Revision: <date> · confirmed by the operator: <yes/no> · foundation: `docs/ux/foundation.md`

Every portrait keeps these eight lines, in this form, so `design_gate.py panel` can read them.
The `retention` line opens with `local` or `tourist`, and the panel carries at least two of
each (see the note at the end). The `needs` line opens with the portrait's experience with
this kind of app: `novice`, `regular` or `expert`. The panel carries at least two novices and
one expert; at least one novice is skilled in the domain (a guitarist new to this metronome),
which is what tests "new, not stupid". When the product targets a tablet, at least one
portrait's `needs` names it.

**The novice** has not used an app like this; reads every label; does not guess hidden
gestures, long presses or icon-only controls; understands a plain explanation the first time.
A portrait never describes the novice as slow, confused or careless.

## P-01 <short name>

- **basis**: evidence RE-01, RE-04 | hypothesis
- **situation**: <who, where, on what, under what pressure>
- **goals**: <the jobs they hire the product for, in their words>
- **features**: <the features they actually use, by name>
- **scenarios**: <two to four composite chains across features, by SCR- id: SCR-03 → SCR-07>
- **activation**: <steps to first value, and the step they are likely to drop at>
- **retention**: local | tourist: <trigger → action → reward → what brings them back, and what makes them leave>
- **needs**: novice | regular | expert: <device and engine, locale, text size, accessibility, connection>

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

## Novice walk

The design-tester walks every screen in scope once per novice portrait, on the frames and
again on the build. It writes the novice's answers before it opens the screen's action map
(`screens.md`, `Actions:`), and every answer quotes the visible text or names the glyph that
led to it; an answer without visible evidence is a guess and counts as a fail.

| Test | Question | Pass when | Finding when it fails |
|---|---|---|---|
| 1.1 first ten seconds | What is this screen for? | the answer matches the verb and object of `Purpose` | `purpose` |
| 1.2 | What would you tap first? | the primary action, or the control of the scenario's first step | `first-tap` |
| 1.3 | For each control you see, what happens when you tap it? | every counted visible action predicted, with evidence | `label` |
| frame against map | (no question) | no control outside the map, none missing | `unmapped`, `missing` |
| budget | (no question) | five or fewer counted visible actions | `overload` |
| 2 find it | the goal in the scenario's words ("you want the click softer") | a visible action on the first tap; a hidden one with at most one wrong container | `findability` |
| 3.1, 3.2 state | Is something happening right now? How do you stop it? | the state named from text, the stop control found | `state-unclear` |
| 3.3 | You made a mistake a moment ago. How do you take it back? | an undo path found | `no-undo` |

A fail by either novice is a fail for the screen. The expert runs a counter-check: no
`often` action costs more taps than before the change, and every gesture accelerator still
works (finding `slower`). The panel is a model playing a person: before a flagship release,
repeat tests 1 and 3 with three to five real first-time users.
