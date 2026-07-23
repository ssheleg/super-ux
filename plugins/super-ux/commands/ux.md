---
description: Single entry point for all UX work — status across foundation/scenarios/audits, then a menu of applicable actions (init, update, validate, audit, plan fixes)
---

Single entry point for super-ux. The user is NOT expected to know the
skills, layers, or commands inside this plugin — routing is your job.
Idempotent: safe to run any number of times, at any project stage.

## 0. Understand the task (before anything technical)

If `$ARGUMENTS` already states the task, map it via the routing table and
skip the question. Otherwise ask ONE plain question — "What do you want to
get done with the product's UX?" — with a few examples in everyday words
(new product, new feature, "the UX feels bad", "check that everything
works", "make a fix plan"). Never ask the user to choose between skills or
layers — that vocabulary is internal.

**If the task involves designing or improving the interface** (routes 1, 3,
4), and the foundation's Design tooling section hasn't recorded a Figma
choice yet, ask one more plain question: "Design the interface visually in
Figma as we go, or text-only? (Figma is the default.)" Record the answer in
`foundation.md` → Design tooling. If Figma is chosen and the Figma MCP isn't
connected, recommend connecting it and proceed text-only until it is (see
figma-integration reference).

Routing table (user's words → action from the menu below):

| User says (any language) | Route to |
|---|---|
| new product / стартуем проект / "с нуля" | 1 then 3 then 5 (full chain init) |
| new feature / новая фича / "хочу добавить X" | 6 (validate idea vs chain) then 3/5 for the new parts |
| "UX плохой", "неудобно", improve/redesign | 4 (Improve) |
| "проверь что всё работает", audit, "прогони по сценариям" | 7 |
| "чего не хватает", gaps, coverage | 8 |
| "как лучше по практикам", best practices | 9 |
| "что чинить в первую очередь", план | 10 |
| don't know / "просто посмотри" | run 1–3 of Inspect, recommend from state |

## 1. Inspect state

- Hard rule in project `CLAUDE.md`? (heading `## UX scenarios — hard rule (super-ux)`)
- `docs/ux/foundation.md`? If yes: counts of personas / JTBD / journeys /
  stories by status.
- `docs/ux/flows.md`? If yes: flow count, `inferred` vs confirmed, stories
  without flows.
- `docs/ux/screens.md`? If yes: screen count by status
  (designed/built/drifted), screens missing Figma frames (when Figma on),
  screens missing coverage.
- `docs/ux/scenarios.md`? If yes: scenario counts by status, features,
  `Traces` filled or not, `Last audit` values.
- Latest report in `docs/ux/audits/` (date, totals, open findings).
- **Run the linter** `python3 docs/ux/lint.py` and fold its errors/warnings
  into the status — it is the fastest, deterministic read of what's stale,
  drifted, or missing (lost Figma frames, broken traces, orphans).

## 2. Repair silently (no menu needed for these)

- Rule missing → install it (as `/ux-rule`).
- `docs/ux/` missing → create skeleton (seed `scenarios.md`,
  `foundation.md`, `flows.md`, `screens.md`, `README.md`; copy `lint.py`;
  `audits/` dir) — as `/ux-rule` does.

## 3. Status report

Compact table across all three layers: foundation (present? entry counts,
assumptions unvalidated), scenarios (total/by status, traced %, features),
audits (last run, PASS/PARTIAL/FAIL/BLOCKED totals, open findings).

## 4. Action menu

Offer ONLY the applicable actions, numbered, with a one-line why; let the
user pick (multiple allowed). Full catalog:

1. **Build the WHY layer** — `ux-foundation` Init (interview or reverse) —
   when foundation is missing/empty.
2. **Update foundation** — `ux-foundation` Update — when user knowledge
   changed.
3. **Design user flows** — `ux-flows` Design/Reverse — when stories exist
   without flows, or an existing product has no flows.md.
4. **Improve existing UX** — `ux-flows` Improve — heuristic evaluation
   (PRN-01..16) of current flows → traced before/after redesign proposals.
5. **Build/extend scenarios** — `ux-scenarios` Init or Update — when
   scenarios missing, or flows/stories lack scenario coverage.
6. **Validate the chain** — `ux-scenarios` Validate (+ `ux-foundation`
   Validate) — before building a new feature, or when traceability is
   doubtful.
7. **Audit code vs scenarios & flows** — `ux-audit` (all / feature:X;
   depth `deep` adds heuristic + practice + coverage passes) — when
   validated scenarios were never audited, or code changed since the last
   audit; recommend `deep` before releases and after big UX changes.
8. **Coverage audit** — `ux-audit` scope `coverage` — orphan
   stories/flows/scenarios, journey gaps.
9. **Best-practices / heuristics review** — `ux-audit` scope `practices` or
   `heuristics`: tagged catalog (`BP-NNN`) and principles (`PRN-NN`)
   suggestions.
10. **Plan fixes** — produce `docs/ux/plans/YYYY-MM-DD-<scope>.md` from the
    latest audit/Improve results: target interface per screen +
    CREATE/MODIFY/DELETE change table, every row traced, prioritized
    Frequency × Severity × Solvability. Then say what the user has in hand
    (plan, audit report, `docs/ux/` chain, Figma) and recommend — don't
    force — implementing it autonomously by best practices with the ssheleg
    **task-pipeline** plugin: installed → `/task-pipeline <plan file>`; not
    installed (optional one-time) → `/plugin marketplace add
    ssheleg/task-pipeline` + `/plugin install task-pipeline@task-pipeline`;
    or superpowers writing-plans / by hand — user's call.
11. **Nothing** — everything green; rerun `/ux` after the next change.

Recommend exactly one action as the default (mark it "recommended"), based
on the state: no foundation → 1; stories without flows → 3; flows without
scenarios → 5; drafts pending → validate/review; never audited or stale →
7; open findings → 10; user said "UX плохой/improve" → 4.

Additional context from the user: $ARGUMENTS
