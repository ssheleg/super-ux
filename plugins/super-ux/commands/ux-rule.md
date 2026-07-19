---
description: Install the scenario-first hard rule into this project's CLAUDE.md and create the docs/ux/ skeleton
---

Install the super-ux hard rule into this project. Idempotent — safe to run
twice.

1. If the project's `CLAUDE.md` (create it if absent) does not already
   contain the heading `## UX scenarios — hard rule (super-ux)`, append this
   block verbatim:

   ```markdown
   ## UX scenarios — hard rule (super-ux)

   - `docs/ux/scenarios.md` is the source of truth for all user-facing behavior.
   - Any change that touches user-facing behavior MUST update
     `docs/ux/scenarios.md` in the same change (add/adjust scenarios, statuses,
     coverage).
   - Any new feature or project STARTS with scenarios: draft them, validate
     against existing scenarios (conflicts, overlaps, gaps), get them approved —
     only then design and build UI.
   - Use the `ux-scenarios` skill to maintain the base and `ux-audit` to verify
     the codebase against it.
   ```

   If the heading is already present, leave CLAUDE.md untouched and say so.

2. If `docs/ux/scenarios.md` does not exist, create `docs/ux/` and seed
   `scenarios.md` from the plugin's `templates/scenarios.md`. Never
   overwrite an existing scenario base.

3. Report what was installed and suggest `/ux-init` next if the base is
   still empty.
