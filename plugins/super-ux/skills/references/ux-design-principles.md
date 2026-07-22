# UX Design Principles — How the Agent Thinks

The reasoning playbook for designing new UX and improving existing UX. The
`ux-foundation`, `ux-flows`, `ux-scenarios`, and `ux-audit` skills apply it;
audits cite its principle IDs. This is the "taste" layer — formats live in
[scenario-format.md](scenario-format.md), proven tactics in
[best-practices.md](best-practices.md).

## The pipeline (any product)

```
1. RESEARCH      personas, JTBD, journeys        -> foundation.md   (WHY)
2. DEFINE        user stories + acceptance       -> foundation.md   (WHAT FOR)
3. STRUCTURE     task analysis -> user flows     -> flows.md        (HOW)
4. SPECIFY       scenarios: action -> response,  -> scenarios.md    (WHAT EXACTLY)
                 alt & error paths (use cases)
5. VISUALIZE     wireframes / storyboards        -> optional, per flow
6. BUILD UI      only now
7. VERIFY        audits -> prioritized fix plans -> audits/
```

**Forward mode** (new product/feature): run 1→7 in order. Never design a
screen before its flow exists; never draw a flow for a story that traces to
no job.

**Backwards mode** (existing product): fill the same artifacts in reverse —
inventory the UI → reconstruct flows from code → derive scenarios → infer
stories/jobs → then judge the existing UX against what the chain SHOULD be.
Every reverse-engineered entry is tagged `inferred` until a human confirms.
The gaps between "is" and "should" become the improvement backlog.

## Task analysis (method for step 3)

1. Take one user story. Name the goal as the user states it.
2. Decompose into the minimal sequence of user-visible micro-steps needed to
   reach the goal — what the user does, not what the system does.
3. For each step ask: does this step serve the job? Can the system do it for
   the user (default, prefill, inference)? Can two steps collapse into one?
   Steps that survive get a flow node; steps that don't get cut.
4. Mark the step where the user first receives real value — the flow must
   reach it as early as possible (aha is engineered, not hoped for).

## Flow design rules (method for step 3, continued)

- One flow = one user goal (one story or a tight story cluster).
- Every decision point is an explicit branch — no implicit "the user
  figures it out".
- Every error edge lands somewhere recoverable: retry, edit, help, back.
  Dead ends are defects by definition.
- Enumerate ALL entry points (deep link, tab, push, empty state CTA…) —
  flows entered mid-way must still work.
- Count steps on the happy path; challenge every step above five.
- Every screen node declares its states: loading / empty / error / success.

## Screen & interaction rules (method for steps 4–6)

- Every user action gets visible feedback within the same screen.
- Destructive actions: confirmation AND undo where feasible; undo beats
  confirmation when both are possible.
- Primary action per screen: exactly one, visually dominant.
- Forms: validate inline at the field, preserve input on error, label errors
  with what to DO, not what went wrong internally.
- Empty states sell the next action, never just state emptiness.

## Heuristics checklist (PRN-01..PRN-10, after Nielsen)

Used by design reviews and the audit's heuristic pass. Each has an audit
question; violations get the principle ID as evidence.

| ID | Principle | Audit question |
|----|-----------|----------------|
| PRN-01 | Visibility of system status | Does the user always know what's happening (loading, saving, progress)? |
| PRN-02 | Match the real world | Are labels the user's words (from JTBD/interviews), not internal jargon? |
| PRN-03 | User control & freedom | Can the user undo, cancel, go back at every step? |
| PRN-04 | Consistency & standards | Same action = same word = same place everywhere? Platform conventions kept? |
| PRN-05 | Error prevention | Are errors prevented (constraints, defaults, confirmation) rather than reported? |
| PRN-06 | Recognition over recall | Is everything needed for a decision visible on screen, not memorized? |
| PRN-07 | Flexibility & efficiency | Do frequent users get shortcuts (recents, defaults, bulk) without hurting novices? |
| PRN-08 | Minimalist design | Does every element on the screen serve the current job? |
| PRN-09 | Error recovery | Do error messages say what happened + how to recover, in plain language? |
| PRN-10 | Help in context | Is help available where confusion happens, not in a distant manual? |

## Cognitive principles (PRN-11..PRN-16)

| ID | Principle | Rule of thumb |
|----|-----------|---------------|
| PRN-11 | Progressive disclosure | Show the minimum first; reveal complexity on demand. |
| PRN-12 | Smart defaults | Every choice ships with the best-guess default; "Suggest for me" at decision-heavy steps. |
| PRN-13 | Hick's law | Fewer options = faster decisions; group or stage large option sets. |
| PRN-14 | Jakob's law | Users spend most time in OTHER apps — deviate from familiar patterns only when the job demands it. |
| PRN-15 | Fitts's law | Primary targets big and close; dangerous targets far from frequent ones. |
| PRN-16 | Peak–end rule | Polish the emotional peaks and the ending: first value, errors, completion, offboarding. |

## Improving existing UX (heuristic evaluation procedure)

1. Prerequisite: backwards-mode chain exists (flows + scenarios at least
   `inferred`). You cannot judge UX without knowing the intended jobs.
2. Walk every flow against PRN-01..PRN-16 and the journey's pain points.
   Record violations: `[PRN-NN] screen/flow-node — what breaks — severity`.
3. Severity (NN/g scale → audit mapping): 4 catastrophic / 3 major →
   `critical`/`major`; 2 minor → `minor`; 1 cosmetic → note only.
4. Every redesign proposal must: trace to a pain/job/story; cite the
   principle or practice (`PRN-NN` / `BP-NNN`) it applies; show the flow
   before → after (two mermaid diagrams); state the expected observable
   effect. "Make it prettier" is not a proposal.
5. Prioritize Frequency × Severity × Solvability; feed the top of the list
   into the project's planning workflow.

## Wireframes & storyboards (optional artifacts)

- **Wireframe** = low-fi structure check BEFORE UI: ASCII/markdown blocks
  per screen showing hierarchy, primary action, and states — not pixels.
  Store under `docs/ux/wireframes/<FLW-ID>.md`, linked from the flow.
  Validate: does the layout match the flow node's declared elements and
  states? Is the primary action unmistakable?
- **Storyboard** = 3–6 captioned frames of the usage context (where/when/
  with what in hand). Use when context drives design (mobile on the go,
  shared devices, stress situations); skip otherwise.

## Anti-patterns (stop signals)

- Designing screens before flows, or flows before stories.
- A flow node with no error edge ("nothing can fail" must be stated and
  justified in the scenario, not assumed).
- Copying a competitor mechanic without naming its mechanism (BP-001).
- Redesign proposals without a traced pain or principle.
- Optimizing a step that shouldn't exist (task analysis first).
- Treating the paywall/conversion moment as exempt from honesty rules —
  dark patterns create churn and refunds, not LTV.
