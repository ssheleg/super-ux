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

   - `docs/ux/scenarios.md` is the source of truth for all user-facing
     behavior; `docs/ux/foundation.md` (personas, JTBD, journeys, stories) and
     `docs/ux/flows.md` (user flows) are the WHY and HOW layers scenarios
     trace to.
   - Any change that touches user-facing behavior MUST update
     `docs/ux/scenarios.md` (and affected flows) in the same change.
   - Any new feature or project STARTS with the chain: which job does it
     serve, which journey stage, which story — then flows and scenarios,
     validated against the existing base, approved — only then design and
     build UI.
   - Use `/ux` as the entry point; skills: `ux-foundation`, `ux-flows`,
     `ux-scenarios` for maintenance, `ux-audit` for evidence-backed
     verification.
   ```

   If the heading is already present but the block text differs from the
   above, replace the block with this version (it supersedes older ones).

2. If `docs/ux/scenarios.md` does not exist, create `docs/ux/` (including
   `audits/`) and seed `scenarios.md`, `foundation.md`, and `flows.md` from
   the plugin's `templates/`. Never overwrite existing files.

3. Report what was installed and suggest `/ux` next if the base is still
   empty.
