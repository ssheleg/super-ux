# Interactive flow prototypes — the bounded scenario graph

Part of **super-ux** — see [system-map.md](system-map.md). This is the
contract for the GRAPH under an interactive flow preview: the machine-checkable
model a clickable prototype walks. The prototype itself (the clickable
artifact, its scenario selector and reset) and the coverage receipt are
separate deliverables built ON this graph — this file owns only the graph and
its validation rules. The executable half is `test/flow_graph.py` in the
super-ux repository: `validate_graph()` implements every IFP rule below, and
`test/audit_regressions/ctx-03.01.py` watches each one refuse its defect.

## Why bounded

A prototype that improvises screens on click proves nothing about the flows it
claims to preview. The graph is **declared first, walked second**: every screen
and every transition is written down before anything is clickable, so "what
the preview can do" and "what the flows say" are the same document, and the
difference between declared and actually-walked is measurable later instead of
being invisible.

## The graph

One JSON object per flow preview:

```json
{
  "flow": "FL-checkout",
  "entry": "SCR-01",
  "screens": [{"id": "SCR-01", "title": "Cart"}],
  "external": [{"id": "external:stripe-checkout", "mock": "explicit"}],
  "transitions": [
    {"id": "TR-01", "origin": "SCR-01", "action": "Pay",
     "result": "external:stripe-checkout", "kind": "happy"}
  ],
  "scenarios": [{"id": "SCN-001", "kind": "happy", "path": ["TR-01"]}]
}
```

IDs follow [scenario-format.md](scenario-format.md): screens are `SCR-NN`,
scenarios `SCN-NNN`; transitions are `TR-NN`, sequential, never reused.

## The rules — `IFP-01 … IFP-06`

- **IFP-01 — a transition is origin/action/result, all three.** An edge
  missing any of them is not a smaller edge, it is an unanswerable question
  ("what happens when…?") shipped as data. Refused.
- **IFP-02 — origin and result resolve.** Every `origin` names a declared
  screen; every `result` names a declared screen or a declared `external:*`
  destination. A transition into a screen nobody declared is the prototype
  inventing product behaviour.
- **IFP-03 — no dangling state.** Every screen is reachable from `entry` by
  declared transitions, and every non-terminal screen has at least one way
  out. A screen you can reach but never leave — or declare but never reach —
  is a dead end the preview would hide behind whichever path the demo
  happens to click.
- **IFP-04 — the seven kinds are the coverage axes.** Each transition and
  each scenario carries a `kind` from `happy | error | recovery | back |
  cancel | returning | external`. A kind with no coverage is DECLARED absent
  (`"absent": ["returning"]` with a reason), never silently missing — the
  coverage matrix reads this field, it does not infer it.
- **IFP-05 — an external destination is an explicit mock.** Anything the
  preview cannot actually run (payment, OAuth, email) is `external:*` with
  `"mock": "explicit"` — a screenshot standing in for a working step is
  declared as standing in, so a functional-looking preview cannot claim a
  functional integration.
- **IFP-06 — a preview raises no status.** The graph carries NO `status`,
  `implemented` or product-state field, and the validator refuses one that
  does: walking a prototype changes `scenario-format.md` statuses exactly
  as much as reading it does — not at all. Status lives in
  `docs/ux/scenarios.md` and moves only by its own rules.

## The clickable half — the fixture pattern

The reference implementation is `test/fixtures/interactive-flow/index.html`
in the super-ux repository: one local page, the graph embedded as JSON, a
generic runner that renders ONLY what is declared — scenario selector, reset,
deep link (`#SCR-…`/`#SCN-…`), per-transition buttons derived from the graph.
A step the preview cannot actually run renders as a screen that `simulates`
its declared `external:*` destination, inside the labelled SIMULATION box —
clicking it proves a browser can click, never that money moves. No network
primitive, no external script, no SDK.

The coverage matrix, the walkthrough probes and the handoff receipt are in
[prototype-walkthrough.md](prototype-walkthrough.md).

## What this file does not own

The clickable artifact (selector, reset, labelled simulations), the
declared-vs-walked comparison and the coverage/handoff receipt are the two
deliverables built on this graph — see the ux-flows skill for routing. A
small exact-copy edit to an existing product does not require creating any
of this; the graph is for flows being DESIGNED, not a toll on every change.
