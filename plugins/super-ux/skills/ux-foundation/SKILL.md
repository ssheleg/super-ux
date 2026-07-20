---
name: ux-foundation
description: Use when defining or revising WHO the users are and WHY they use the product - personas, Jobs to Be Done, customer journey maps, user stories with acceptance criteria. Maintains docs/ux/foundation.md, the WHY layer that UX scenarios trace to. Triggers - "jtbd", "customer journey", "user story", "персоны", "джобы", "карта пути", "юзер стори", new product discovery, "who is this for".
---

# ux-foundation — The WHY Layer

Interfaces fail when built without knowing WHO uses them and WHY. This skill
maintains `docs/ux/foundation.md`: **Personas → Jobs to Be Done → Customer
journeys → User stories.** Scenarios (`ux-scenarios` skill) are built on top
and trace to these IDs — the full chain gives every scenario its context.

**Format contract:** [scenario-format.md](../references/scenario-format.md)
(ux-contract v2). Never deviate from ID schemes or field names.

## Quality bars (non-negotiable)

- **Personas** are grounded in data or observation, recognizable by a real
  user — not invented archetypes with stock-photo traits.
- **JTBD** statements name a situation, motivation, and outcome — never a
  feature ("When I land a new client, I want to start a clean workspace, so
  I can bill them separately" — not "I want a projects dropdown"). Capture
  the four forces: push, pull, anxiety, habit.
- **Journeys** cover the end-to-end experience (before, during, after the
  product), one row per stage: action, touchpoint, emotion (1–5), pain,
  opportunity. Score opportunities Frequency × Severity × Solvability. When
  filling opportunities, consult
  [best-practices.md](../references/best-practices.md) by stage tags for
  proven mechanisms.
- **Stories** pass INVEST; acceptance criteria are Given/When/Then and
  observable. A story that can't be verified is not done being written.
- Evidence beats opinion: repeated pain across users, observable
  workarounds, measurable cost. One stakeholder's idea is an assumption, not
  a fact — mark assumptions (desirability / viability / feasibility /
  usability) and flag the risky-untested ones.

## Choosing a workflow

| Situation | Workflow |
|---|---|
| No `foundation.md`, new product | Init (interview) |
| No `foundation.md`, existing product/scenarios | Init (reverse) |
| Understanding of users changed | Update |
| Consistency questioned; before building on top | Validate |

If `docs/ux/` is missing, create it; seed `foundation.md` from the plugin's
`templates/foundation.md`.

## Init (interview) — greenfield

One question at a time; user's answers are the data:

1. Who will use this? (→ personas; probe until each is concrete enough to
   recognize)
2. Per persona: what situation triggers them to reach for the product? What
   are they really trying to get done? What outcome tells them it worked?
   (→ JTBD + forces)
3. Walk their path end-to-end, before/during/after: where do they start,
   what do they touch, where does it hurt today? (→ journeys, emotion + pain
   per stage)
4. Derive user stories from journey pains and job outcomes; write
   acceptance criteria; prioritize must/should/could against the job's
   success metric.
5. Present layer by layer for approval; mark unvalidated guesses as
   assumptions with a risk note.

## Init (reverse) — existing product

1. Inventory what exists: scenarios.md (if any), screens/routes, onboarding,
   settings, analytics/support artifacts when available.
2. Reverse-engineer: what jobs does the current UI implicitly serve? Which
   personas does it assume? Draft JTBD/journeys/stories from evidence, tag
   confidence (observed vs inferred).
3. Flag the gaps loudly: features serving no discernible job (candidates to
   cut), jobs with no support (opportunities), journey stages with pain and
   no coverage.
4. Present for validation; inferred entries stay marked until the user
   confirms them.

## Update

Given new knowledge (user feedback, analytics, pivot, new segment):

1. Locate affected entries by ID; update statements, stages, stories.
2. Dropped directions: mark stories `dropped`, keep entries — never delete.
3. Cascade check: which scenarios trace to the changed IDs? List them and
   hand the list to `ux-scenarios` (Update) in the same session.

## Validate

1. **Integrity:** IDs sequential/unique; every story traces to a job; every
   journey belongs to a persona × job; statuses legal.
2. **Quality:** JTBD statements are situation/motivation/outcome (no
   features); stories INVEST; acceptance criteria observable; journeys have
   all layers filled.
3. **Coverage:** every persona has ≥1 job; every job has ≥1 journey and ≥1
   story; every must/should story has ≥1 scenario in scenarios.md (or is
   explicitly awaiting one).
4. Report as a checklist with per-item fixes; apply approved fixes.

## Definition of done

- Layers consistent, IDs stable, assumptions marked as such.
- The user approved new/changed entries.
- Cascading scenario updates identified and handed to `ux-scenarios` — the
  chain never silently drifts.
