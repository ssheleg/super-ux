---
name: ux-scenarios
description: Use when creating or updating UX scenarios, starting ANY new feature or project, making ANY change to user-facing behavior, or onboarding an existing codebase into scenario-driven development. Maintains docs/ux/scenarios.md as the source of truth for all user-facing behavior. Triggers - "ux scenarios", "сценарии использования", "новая фича", new feature/project planning, UI changes.
---

# ux-scenarios — Maintain the Scenario Base

AI-generated interfaces go bad when UI is built without a model of user
behavior. This skill keeps one: `docs/ux/scenarios.md` in the target project
is the source of truth for everything the user can do, see, and hit — every
feature, every button, every state, every error, every result.

**Format contract:** [scenario-format.md](../references/scenario-format.md)
(ux-contract v2). Read it before writing or editing scenarios. Never deviate
from its field names, ID rules, statuses, or checklists.

**The WHY layer:** when `docs/ux/foundation.md` exists (personas, JTBD,
journeys, user stories — maintained by the `ux-foundation` skill), scenarios
are derived FROM it: draft scenarios per user story and journey stage, fill
the `Traces:` field, and enforce the traceability rules (every must/should
story covered; every scenario serves a story or job — a scenario serving
nothing is a candidate for deletion, not implementation). If the foundation
is missing on a non-trivial product, recommend running `ux-foundation`
first; proceed in v1 mode (no Traces) only for tiny projects or on explicit
user choice.

## The hard rule

1. Scenarios come BEFORE interface. A new feature or project starts with
   drafting scenarios and validating them against the existing base —
   conflicts, overlaps, gaps — and getting them approved. Only then design
   and build UI.
2. Any change touching user-facing behavior updates `docs/ux/scenarios.md`
   in the SAME change. New behavior with no scenario is a blocker, not a
   warning.

## Choosing a workflow

| Situation | Workflow |
|---|---|
| No `docs/ux/scenarios.md`, little or no code | Init (greenfield) |
| No `docs/ux/scenarios.md`, existing product code | Init (existing code) |
| Base exists; behavior is being added/changed | Update |
| Base exists; consistency questioned, or a new feature idea arrives | Validate |

Announce which workflow you are running. If `docs/ux/` is missing, create it
(seed `scenarios.md` from the plugin's `templates/scenarios.md`).

## Init (greenfield)

Scenarios are designed here, not reverse-engineered.

1. Interview the user, one question at a time: who are the personas? what
   job does each hire the product for? what are the core features? what must
   never happen to the user?
2. Draft personas, then scenarios feature by feature. For every feature,
   satisfy the per-feature completeness checklist (happy path, every error
   path, empty state, visible loading, destructive-action confirmation,
   returning-user variant) and the per-product checklist (first-run
   onboarding through multi-entity flows) from the format contract.
3. All entries start as `Status: draft`, `Coverage: none yet`.
4. Present the base to the user section by section for approval. Approved
   scenarios move to `validated`.
5. Only after validation may UI design/implementation begin — pointed at
   these scenarios.

## Init (existing code)

The base must cover *everything that exists*, then expose the gaps.

1. Inventory sweep of the codebase (dispatch parallel Explore/general
   subagents for large codebases, one area each): routes and screens;
   interactive elements (buttons, forms, dialogs, menus); state branches
   (loading / empty / error / success); error paths and what the user sees;
   onboarding and first-run logic; settings; multi-entity flows.
2. Draft scenarios from the inventory, feature by feature, filling
   `Coverage:` with the `file:line` evidence found during the sweep.
3. Flag both gap directions explicitly in your report to the user:
   - code behavior with no scenario (was invented ad hoc — now captured);
   - checklist items with no code (e.g. no empty state exists at all) —
     record these as `draft` scenarios with `Coverage: none yet`.
4. Present for validation as in greenfield step 4.

## Update

Given a change (a diff, a feature description, a bug fix):

1. Identify affected scenarios by feature and UI elements. Search the base —
   don't trust memory.
2. Apply edits: adjust steps/elements/errors of existing scenarios; add new
   scenarios for new behavior; retire scenarios that are no longer true
   (`Status: retired` + one-line reason — never delete).
3. Changed scenarios drop back to `draft` until re-approved; keep the Index
   table in sync.
4. If the change introduced user-facing behavior that fits NO scenario even
   after this pass, stop and say so — that behavior needs a scenario decision
   before it ships.

## Validate

Consistency pass over the base (also run before approving any new feature
idea):

1. **Integrity:** IDs sequential and unique; Index matches entries; every
   referenced persona defined; statuses legal.
2. **Coverage:** every feature meets the per-feature checklist; the product
   meets the per-product checklist. List what's missing.
3. **Traceability** (when foundation.md exists): every must/should story has
   ≥1 scenario; every scenario traces to ≥1 story or job; every journey
   stage with a product touchpoint has ≥1 scenario. Orphans in either
   direction are findings.
4. **Conflicts:** scenarios that contradict each other (same entry point,
   incompatible outcomes; same element, different behavior). For a new
   feature idea: validate against the foundation first (which job does it
   serve? which journey stage?), then against existing scenarios — propose
   reconciliation before any UI work. An idea serving no job is challenged,
   not silently accepted.
5. Report findings as a checklist with per-item fixes; apply approved fixes.

## Definition of done

- Index, personas, and entries in sync; format contract honored.
- The user has seen and approved new/changed scenarios (`validated`).
- Gaps and conflicts reported honestly — never silently dropped.
