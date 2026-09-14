# UX Design Principles — How the Agent Thinks

The reasoning playbook for designing new UX and improving existing UX. The
`ux-foundation`, `ux-flows`, `ux-scenarios`, and `ux-audit` skills apply it;
audits cite its principle IDs. This is the "taste" layer — formats live in
[scenario-format.md](scenario-format.md), proven tactics in
[best-practices.md](best-practices.md).

## Contents

- [The pipeline (any product)](#the-pipeline-any-product)
- [Task analysis (method for step 3)](#task-analysis-method-for-step-3)
- [Flow design rules (method for step 3, continued)](#flow-design-rules-method-for-step-3-continued)
- [Screen & interaction rules (method for steps 4–7)](#screen--interaction-rules-method-for-steps-47)
- [Heuristics checklist (Nielsen's ten: PRN-01 – PRN-10)](#heuristics-checklist-nielsens-ten-prn-01--prn-10)
- [Cognitive principles (PRN-11..PRN-16)](#cognitive-principles-prn-11prn-16)
- [Motivation principles (PRN-17..PRN-21)](#motivation-principles-prn-17prn-21)
- [Voice principles (PRN-22..PRN-24)](#voice-principles-prn-22prn-24)
- [Improving existing UX (heuristic evaluation procedure)](#improving-existing-ux-heuristic-evaluation-procedure)
- [Wireframes & storyboards (optional artifacts)](#wireframes--storyboards-optional-artifacts)
- [Anti-patterns (stop signals)](#anti-patterns-stop-signals)


## The pipeline (any product)

```
1. RESEARCH      personas, JTBD, journeys        -> foundation.md   (WHY)
2. DEFINE        user stories + acceptance       -> foundation.md   (WHAT FOR)
3. STRUCTURE     task analysis -> user flows     -> flows.md        (HOW)
4. MAP           screens + states registry       -> screens.md      (UI MAP)
5. SPECIFY       scenarios: action -> response,  -> scenarios.md    (WHAT EXACTLY)
                 alt & error paths (use cases)
6. VISUALIZE     style pack first, then wireframes  -> optional, per screen
                 / storyboards / Figma mockups
                 (frames named SCR-NN/<Screen>/<state>)
7. BUILD UI      only now
8. VERIFY        audits -> prioritized fix plans -> audits/, plans/
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

## Screen & interaction rules (method for steps 4–7)

- Every user action gets visible feedback within the same screen.
- Destructive actions: confirmation AND undo where feasible; undo beats
  confirmation when both are possible.
- Primary action per screen: exactly one, visually dominant.
- Pick the right control for the job (radios vs checkboxes vs select,
  sheet vs alert, modal vs disclosure, nav bar vs rail) and use the
  platform's standard component — see
  [component-guidelines.md](component-guidelines.md) (BP-101..115).
- Forms: validate inline at the field, preserve input on error, label errors
  with what to DO, not what went wrong internally.
- Empty states sell the next action, never just state emptiness.
- Accessibility is decided here, in text, not after the UI exists: each
  scenario states its keyboard path, focus order, what gets announced, and
  the contrast pairs it depends on (BP-136..138). Retrofitting is the
  expensive way to reach the same place.
- Motion is specified like any other behavior — what it communicates, from a
  token scale, and what happens under reduced motion (BP-130..132). An
  effect with no reduced-motion branch is unfinished, not polished.
- Responsiveness starts narrow: the small viewport is the majority case, and
  breakpoints follow the content, not device names (BP-134, BP-135).
- Visual craft at build time — type system, contrast floors, palette
  discipline, spacing grid, alignment, microcopy — follows BP-079..090 in
  the best-practices catalog; the audit's heuristic and practice passes
  check them per the selection protocol. Those are floors, not an identity:
  the concrete palette/type/motion come from one locked style pack recorded
  in `screens.md`, picked with the **sheleg-design** companion when it's
  available — see [visual-identity.md](visual-identity.md). Inventing a look
  per screen is visual drift.

## Heuristics checklist (Nielsen's ten: PRN-01 – PRN-10)

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

## Motivation principles (PRN-17..PRN-21)

These describe why a user keeps going. Each is a **motivation** mechanism,
and every one of them has a coercive twin — the same lever aimed at the
product's interest instead of the user's. The line is the honesty stance
below: a mechanism that only works while the user misunderstands the
situation is a dark pattern wearing a principle's name. Applied honestly
they make a real goal easier to reach; applied otherwise they manufacture a
goal the user never had.

| ID | Principle | Rule of thumb | Where it turns coercive |
|----|-----------|---------------|--------------------------|
| PRN-17 | Goal-gradient | Effort rises as a visible goal nears — show real remaining distance (checklist progress, "2 of 5 left"). | Progress toward a goal the product invented, or a bar that never quite fills. |
| PRN-18 | Zeigarnik effect | An unfinished task stays in mind — an incomplete-setup marker works because the task is genuinely open. | Manufactured incompleteness: badges for things the user already finished or never started. |
| PRN-19 | IKEA effect | People value what they helped build — personalization in onboarding raises attachment, not just relevance. | Busywork disguised as setup, so leaving feels like discarding one's own effort. |
| PRN-20 | Endowment | Holding something raises its felt value — the honest use is a full-featured trial (a reverse trial, BP-070) that shows the real product. | Granting then removing capability to create loss the user did not choose. |
| PRN-21 | Zero-price effect | Free is disproportionately attractive — it is why a free tier drives reach (BP-147). | "Free" that is not: undisclosed cost, card required to see the price. |

Rule: any of PRN-17..21 recorded as `applied` in a compliance table names
which side of that fourth column it is on, and what the user gets from it.

## Voice principles (PRN-22..PRN-24)

These describe how a product **sounds**, and they sit beside the interaction
principles rather than under them: a product can satisfy every heuristic
above and still read like three different companies. Each has the same shape
as the rest — a mechanism, and the failure it prevents.

| ID | Principle | What it means | Violated when |
|---|---|---|---|
| PRN-22 | One voice, many registers | The voice is fixed and per-surface tone is a delta on named axes; invariants hold everywhere, including in every locale (BP-183, BP-202). | A surface quietly breaks an invariant because it "needs a different tone" — improvisation dressed as adaptation. |
| PRN-23 | Every claim is checkable | A number, a superlative or a citation exists as a sourced, dated fact, or it is not written (BP-190, BP-194). | Unsourced figures, fabricated quotes or experts, superlatives with nothing beside them. |
| PRN-24 | Never joke about the user's loss | Where data, money or access is at stake, the copy carries no levity — in any voice, including the playful one (BP-187). | A cheerful error, an emoji on a failed payment, a pun on a destructive confirmation. |

Rule: PRN-22..24 recorded as `applied` in a compliance table name the surface
and the pack they were judged against, since a voice judged with no recorded
pack is judged against taste.


## Improving existing UX (heuristic evaluation procedure)

1. Prerequisite: backwards-mode chain exists (flows + scenarios at least
   `inferred`). You cannot judge UX without knowing the intended jobs.
2. Walk every flow against PRN-01..PRN-24 and the journey's pain points.
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
- Adopting a look because it is current — a trend with no named mechanism,
  no owner, and no review date is debt on arrival (BP-145, BP-146).
- Treating accessibility, motion behavior, or page weight as a post-build
  polish pass rather than part of the spec.
- Redesign proposals without a traced pain or principle.
- Optimizing a step that shouldn't exist (task analysis first).
- Treating the paywall/conversion moment as exempt from honesty rules —
  dark patterns create churn and refunds, not LTV.
