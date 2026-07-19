---
description: One-command entry point — sets up super-ux in this project if anything is missing, otherwise reports scenario-base status and suggests the next action
---

Single entry point for super-ux. Detect the project state and act. Never ask
the user which mode they want — decide from the state. Idempotent: safe to
run any number of times.

## 1. Inspect state

- Hard rule installed? — project `CLAUDE.md` contains the heading
  `## UX scenarios — hard rule (super-ux)`.
- `docs/ux/scenarios.md` exists? `docs/ux/audits/` exists?
- If the base exists, parse its Index table: scenario count by status
  (draft / validated / implemented / retired), features covered, `Last
  audit` values.
- Latest report in `docs/ux/audits/` (date + Summary totals), if any.

## 2. Repair whatever is missing (in this order)

- Rule missing → install it exactly as `/ux-rule` does (append the block to
  CLAUDE.md, create it if absent).
- `docs/ux/` or `scenarios.md` missing → create the skeleton, seed
  `scenarios.md` from the plugin's `templates/scenarios.md`, create
  `docs/ux/audits/`.
- Base empty (no scenario entries) → invoke the `ux-scenarios` skill in Init
  mode right now (auto-detect greenfield vs existing code) and build the
  base in this same run.

Nothing missing → repair step is a no-op; say so in one line.

## 3. Status report (always, last)

Compact table: rule installed (yes/no→fixed), scenarios total and by status,
features covered, last audit (date + PASS/PARTIAL/FAIL/BLOCKED totals, or
"never"), open findings from the latest report.

## 4. Suggest exactly one next action

Pick the first that applies:

- Base was just initialized → "review and validate the draft scenarios".
- Drafts pending → "review drafts, then they move to validated".
- Validated scenarios never audited, or audit older than the last
  user-facing change → "run /ux-audit".
- Latest audit has FAIL/PARTIAL findings → "plan fixes from
  docs/ux/audits/<latest>".
- Everything green → "nothing to do; run /ux again after the next change".

Additional context from the user: $ARGUMENTS
