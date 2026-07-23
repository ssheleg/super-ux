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
   - Any change that touches user-facing behavior or interface MUST update,
     in the same change: `docs/ux/scenarios.md`; affected flows; the
     affected screens in `docs/ux/screens.md` (the UI map — states,
     elements, coverage); and, when Figma is enabled, the Figma frame(s)
     plus their links in `screens.md`. A screen whose code diverges from its
     record, or a stale Figma link, is drift — the exact thing this system
     prevents.
   - Any new feature or project STARTS with the chain: which job does it
     serve, which journey stage, which story — then flows and scenarios,
     validated against the existing base, approved.
   - Do NOT write interface code until the UX workflow is done first: the
     foundation → flows → scenarios chain is designed and approved, and —
     when Figma is enabled (default) — the UI is mocked up in Figma with
     every screen linked to its frame. Building UI before this is the exact
     mistake super-ux exists to prevent.
   - After any UX change and before calling the work done, run the linter
     `python3 docs/ux/lint.py` — it must pass (wire it into CI/pre-commit).
   - Use `/ux` as the entry point; skills: `ux-foundation`, `ux-flows`
     (flows + Figma mockups), `ux-scenarios` for maintenance, `ux-audit`
     for evidence-backed verification.
   ```

   If the heading is already present but the block text differs from the
   above, replace the block with this version (it supersedes older ones).

2. If `docs/ux/scenarios.md` does not exist, create `docs/ux/` (including
   `audits/`) and seed `scenarios.md`, `foundation.md`, `flows.md`,
   `screens.md`, and `README.md` from the plugin's `templates/`. Never
   overwrite existing files.

3. Copy the linter to `docs/ux/lint.py` from the plugin's
   `scripts/ux_lint.py` (refresh it even if present — it's code, not user
   content). Suggest wiring `python3 docs/ux/lint.py` into the project's CI
   or pre-commit.

4. Report what was installed and suggest `/ux` next if the base is still
   empty.
