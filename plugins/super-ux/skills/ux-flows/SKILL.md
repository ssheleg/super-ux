---
name: ux-flows
description: Use when designing or improving HOW users move through the product - task analysis, user flows (screens, branches, error paths), screen states, low-fi wireframes, Figma mockups, heuristic UX evaluation and redesign proposals. Maintains docs/ux/flows.md between foundation (stories) and scenarios. Triggers - "user flow", "юзер флоу", "флоу экранов", "поток пользователя", "task analysis", "улучши UX", "почини UX", "redesign flow", "wireframe", "вайрфрейм", "figma", "фигма", "нарисуй дизайн", "мокап".
---

# ux-flows — Design HOW Users Move

Turns user stories into user flows AND maintains the UI map: task analysis →
flow diagram (mermaid) → the screen registry `screens.md` (every screen and
state with Figma frame, wireframe, coverage, resources) → optional
wireframes/Figma mockups. Also the home of UX improvement: heuristic
evaluation of existing flows and traced redesign proposals.

**Two files owned:** `flows.md` (flows referencing screens by `SCR-ID`) and
`screens.md` (the canonical per-screen spec — the design map that ties UX,
UI, Figma, and code together). A screen used by several flows is described
once in `screens.md`.

**Contracts:** [scenario-format.md](../references/scenario-format.md)
(ux-contract v3, `flows.md` section) and
[ux-design-principles.md](../references/ux-design-principles.md) — read the
principles doc before designing; it is the thinking playbook (task-analysis
method, flow rules, PRN-01..16 heuristics, improvement procedure).
Proven tactics: [best-practices.md](../references/best-practices.md) by
stage tags.

**Position in the chain:** foundation (WHY) → **flows (HOW)** → scenarios
(WHAT). Stories in, flows out; `ux-scenarios` then covers every node and
edge with scenarios. If foundation is missing on a non-trivial product,
recommend `ux-foundation` first.

**Money moments are first-class flows:** when the foundation declares a
Monetization section, design dedicated flows for each money moment —
paywall (first-session placement, BP-069), upgrade-at-limit (the gated
action's limit branch is a flow edge to the offer, BP-074), trial start/end,
cancel + winback, rating prompt after success moments (BP-076). Each money
flow uses its checklist row from
[practice-selection.md](../references/practice-selection.md) step 3.

## Choosing a workflow

| Situation | Workflow |
|---|---|
| Stories exist, flows don't (or new feature) | Design |
| Existing product, flows unknown | Reverse |
| Flows exist, behavior changing | Update |
| Existing UX feels wrong / improvement requested | Improve |

## Design (forward)

Per story (or tight cluster):

1. **Task analysis** (principles doc, method section): goal in the user's
   words → minimal user-visible micro-steps → cut/merge/default-away every
   step that doesn't serve the job → mark the first-value step and pull it
   as early as possible.
2. **Draw the flow** (mermaid, node conventions from the contract): every
   decision an explicit branch; every error edge lands on recovery; all
   entry points enumerated; happy path ≤5 steps or justified.
3. **Register screens in `screens.md`:** each screen the flow touches gets
   (or updates) its `SCR-NN` entry — states (loading/empty/error/success)
   with per-state behavior, elements with one primary action, coverage,
   scenarios, resources; the flow's Screens-traversed table just lists the
   SCR-IDs and states it uses. Fill the Design system block once (Figma
   library, token/component/asset locations).
4. **Optional wireframes** (`docs/ux/wireframes/FLW-NN.md`): ASCII blocks —
   hierarchy and primary action, not pixels. Storyboard only when usage
   context drives design.
   **Figma mockups** (default on — see
   [figma-integration.md](../references/figma-integration.md)): if Design
   tooling has Figma enabled, build a frame per screen-state applying the
   visual-craft practices (BP-079..090) as hard constraints, and write the
   frame deep-link into every screen row's `Figma` column. If Figma is
   chosen but the MCP isn't connected, recommend connecting it and continue
   text-only (flows/wireframes stay the source of truth, sync later). Ask
   the Figma yes/no question once at the start and record it in the
   foundation.
5. **Practice pass** (mandatory, per
   [practice-selection.md](../references/practice-selection.md)): build the
   product profile from the foundation, pull the mandatory sets + this
   artifact's checklist row, give every pulled practice a verdict
   (applied / adapted / rejected+reason / deferred+trigger) in a compliance
   table attached to the flow entry. No silent skips; applied practices
   must be visible in the flow/scenario artifacts.
6. Present for approval (flow + compliance table); hand off to
   `ux-scenarios` to cover nodes/edges.

## Reverse (backwards mode)

1. Inventory routes/screens/navigation from the code; trace real
   transitions including error handling.
2. Reconstruct flows as they ARE (not as they should be), tag `inferred`;
   attach `file:line` evidence per node. Build `screens.md` from the
   inventory: one `SCR-NN` per real screen, its actual states, `Coverage`
   pointing at the code; if Figma exists, link existing frames, else leave
   frames empty and flag as a design gap.
3. Derive/match stories with `ux-foundation`; mismatches between actual
   flows and jobs are findings, not silent fixes.
4. Present; confirmed flows lose the `inferred` tag.

## Update (same-change rule)

Any interface change → in the SAME change: update the affected flow
nodes/edges (when navigation changed) AND the affected `screens.md` entries
(elements, states, coverage — always, whenever a screen changes), AND — when
Figma is enabled — the Figma frame(s) plus their links in `screens.md`
(never leave a stale/broken link). Superseded flows/screens kept with a
note. Cascade to `ux-scenarios` (which scenarios now miss coverage?). Leaving
`screens.md` or a Figma frame behind is exactly the drift this system
prevents.

## Improve (heuristic evaluation → redesign)

Follow the improvement procedure in the principles doc, strictly:

1. Prerequisite: flows exist (run Reverse first if not).
2. Walk every flow against PRN-01..16 + journey pains; record violations
   `[PRN-NN] node — what breaks — severity (4..1)`.
3. Redesign proposals: trace to a pain/job/story; cite `PRN-NN`/`BP-NNN`;
   show flow before → after (two mermaid diagrams); state the expected
   observable effect. No untraced "make it nicer" changes. When Figma is
   enabled, produce before → after frames beside the diagrams
   ([figma-integration.md](../references/figma-integration.md)).
4. Approved proposals land in THREE places, same session: flow Updates
   (+ scenario cascade) AND a concrete UX plan
   (`docs/ux/plans/YYYY-MM-DD-<scope>.md`, contract format): target
   interface per screen + CREATE/MODIFY/DELETE table, every row traced,
   prioritized Frequency × Severity × Solvability.
5. Offer autonomous execution of the plan: task-pipeline plugin
   (`/task-pipeline` on the plan file) if installed, else superpowers
   writing-plans → subagent-driven execution.

## The build gate (state this to the user plainly)

Interface code does not get written until this workflow is done: the chain
(foundation → flows → scenarios) is designed and approved, and — when Figma
is enabled (default) — the UI is mocked up in Figma with every screen linked
to its frame. When a user jumps straight to "build the screen", say so and
run the workflow first; that ordering is the whole point of super-ux.

## Definition of done

- Every flow traced to stories; every node states-complete; no dead-end
  error edges; entry points enumerated.
- Every screen the flows touch exists in `screens.md` with states,
  elements, coverage, scenarios, resources; no orphan screens either way.
- Scenarios cover every node and edge (checked with `ux-scenarios`).
- When Figma enabled: every screen state has a frame link in `screens.md`;
  visual-craft practices applied on the frames; Design system block filled;
  foundation Design tooling records the choice + file.
- Only after all of the above does UI implementation start.
- Improvements: every proposal traced and cited; nothing applied without
  approval.
