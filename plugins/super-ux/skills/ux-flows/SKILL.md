---
name: ux-flows
description: Use when designing or improving HOW users move through the product - task analysis, user flows (screens, branches, error paths), screen states, low-fi wireframes, heuristic UX evaluation and redesign proposals. Maintains docs/ux/flows.md between foundation (stories) and scenarios. Triggers - "user flow", "юзер флоу", "флоу экранов", "поток пользователя", "task analysis", "улучши UX", "почини UX", "redesign flow", "wireframe", "вайрфрейм".
---

# ux-flows — Design HOW Users Move

Turns user stories into user flows: task analysis → flow diagram (mermaid) →
screen/state inventory → optional wireframes. Also the home of UX
improvement: heuristic evaluation of existing flows and traced redesign
proposals.

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
3. **Screens & states table:** each screen declares loading/empty/error/
   success and key elements; exactly one primary action per screen.
4. **Optional wireframes** (`docs/ux/wireframes/FLW-NN.md`): ASCII blocks —
   hierarchy and primary action, not pixels. Storyboard only when usage
   context drives design.
5. Check against PRN-01..16 and applicable `BP-NNN` practices before
   presenting; present for approval; hand off to `ux-scenarios` to cover
   nodes/edges.

## Reverse (backwards mode)

1. Inventory routes/screens/navigation from the code; trace real
   transitions including error handling.
2. Reconstruct flows as they ARE (not as they should be), tag `inferred`;
   attach `file:line` evidence per node.
3. Derive/match stories with `ux-foundation`; mismatches between actual
   flows and jobs are findings, not silent fixes.
4. Present; confirmed flows lose the `inferred` tag.

## Update

Behavior change → update affected flow nodes/edges + screens table in the
SAME change; superseded flows kept with a strikethrough note; cascade the
node/edge diff to `ux-scenarios` (which scenarios now miss coverage?).

## Improve (heuristic evaluation → redesign)

Follow the improvement procedure in the principles doc, strictly:

1. Prerequisite: flows exist (run Reverse first if not).
2. Walk every flow against PRN-01..16 + journey pains; record violations
   `[PRN-NN] node — what breaks — severity (4..1)`.
3. Redesign proposals: trace to a pain/job/story; cite `PRN-NN`/`BP-NNN`;
   show flow before → after (two mermaid diagrams); state the expected
   observable effect. No untraced "make it nicer" changes.
4. Prioritize Frequency × Severity × Solvability; approved proposals become
   flow Updates + scenario updates + a plan via the project's planning
   workflow.

## Definition of done

- Every flow traced to stories; every node states-complete; no dead-end
  error edges; entry points enumerated.
- Scenarios cover every node and edge (checked with `ux-scenarios`).
- Improvements: every proposal traced and cited; nothing applied without
  approval.
