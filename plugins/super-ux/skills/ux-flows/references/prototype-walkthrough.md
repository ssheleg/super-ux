# Prototype walkthrough — coverage, and the receipt that survives it

Part of **super-ux** — see [system-map.md](system-map.md). This is the third
piece of the interactive-flow deliverable: the graph is
[interactive-flow-prototypes.md](interactive-flow-prototypes.md), the
clickable page is its fixture pattern, and THIS file owns what a walkthrough
proves and how the proof is recorded. There is **no second flow store**: the
graph stays the single declaration, a walkthrough produces a WALKED log that
references it, and the two are never merged into one file that answers both
questions.

## The walkthrough — a goal, not a tour

A walkthrough is run against the **user's goal, stated without UI hints** —
"pay for what is in the cart", never "click Continue, then Pay": naming the
controls turns a behaviour test into a reading test. Every walkthrough
carries five probes beside the goal, because these are where prototypes rot
first:

1. **reset** — return to entry, state actually cleared;
2. **back** — the declared `back` edges, from every screen that has one;
3. **error** — at least one declared `error` path entered AND recovered;
4. **keyboard** — the goal completed with focus order alone, no pointer;
5. **async** — any step that simulates waiting shows its intermediate state.

## Coverage — three states, never two

Per transition, per scenario and per kind the matrix says `walked`,
`NOT_RUN`, or `declared absent` — **NOT_RUN is not a pass** and it is not
silence; it is the list of what the demo path skipped. A screenshot set with
an empty walked log is `NOT_RUN — screenshots alone are not a functional
pass`. A fired control that moved nothing is a **dead control and fails the
smoke by name**; so does a declared transition the smoke never reached. An
external step passes only as its declared explicit mock — simulated success
proves the browser can click, never that money moves.

## The receipt — pinned bytes, no status axis

The handoff receipt records the artifact's `sha256`, the coverage matrix and
the functional verdict — and **carries no status field**: a preview upgrades
neither `implemented` nor product evidence (IFP-06), and the receipt refuses
a graph or log that tries. Two gates stay separate entries in it: the
**production gate** (code against scenarios, `/ux-audit`) and the
**art-direction gate** (render critique, `sheleg-design`) — a green
walkthrough satisfies neither. The executable half is `test/flow_graph.py`
(`coverage`, `smoke`, `receipt`); the case corpus is
`test/interactive_flow_cases.json`.
