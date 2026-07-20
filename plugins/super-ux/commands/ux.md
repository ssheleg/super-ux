---
description: Single entry point for all UX work — status across foundation/scenarios/audits, then a menu of applicable actions (init, update, validate, audit, plan fixes)
---

Single entry point for super-ux. Never ask which mode — inspect first, then
present a status and a menu of applicable actions. Idempotent: safe to run
any number of times, at any project stage.

## 1. Inspect state

- Hard rule in project `CLAUDE.md`? (heading `## UX scenarios — hard rule (super-ux)`)
- `docs/ux/foundation.md`? If yes: counts of personas / JTBD / journeys /
  stories by status.
- `docs/ux/scenarios.md`? If yes: scenario counts by status, features,
  `Traces` filled or not, `Last audit` values.
- Latest report in `docs/ux/audits/` (date, totals, open findings).

## 2. Repair silently (no menu needed for these)

- Rule missing → install it (as `/ux-rule`).
- `docs/ux/` missing → create skeleton (seed `scenarios.md` and, for
  non-trivial products, `foundation.md` from the plugin templates).

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
3. **Build/extend scenarios** — `ux-scenarios` Init or Update — when
   scenarios missing, or stories lack scenario coverage.
4. **Validate the chain** — `ux-scenarios` Validate (+ `ux-foundation`
   Validate) — before building a new feature, or when traceability is
   doubtful.
5. **Audit code vs scenarios** — `ux-audit` (all / feature:X) — when
   validated scenarios were never audited, or code changed since the last
   audit.
6. **Coverage audit** — `ux-audit` scope `coverage` — orphan
   stories/scenarios, journey gaps.
7. **Plan fixes** — turn the latest audit's FAIL/PARTIAL findings into a
   prioritized work plan (Frequency × Severity × Solvability) via the
   project's planning workflow.
8. **Nothing** — everything green; rerun `/ux` after the next change.

Recommend exactly one action as the default (mark it "recommended"), based
on the state: no foundation → 1; foundation but no scenarios → 3; drafts
pending → validate/review; never audited or stale → 5; open findings → 7.

Additional context from the user: $ARGUMENTS
