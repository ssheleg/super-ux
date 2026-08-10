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
   - Any change that touches user-facing behavior or interface MUST update, in
     the same change: `docs/ux/scenarios.md`; affected flows; the affected
     screens in `docs/ux/screens.md` (the UI map — states, elements,
     coverage); and, when Figma is enabled, the Figma frame(s) plus their
     links in `screens.md`. A screen whose code diverges from its record, or a
     stale Figma link, is drift — the exact thing this system prevents.
   - Any new feature or project STARTS with the chain: which job does it
     serve, which journey stage, which story — then flows and scenarios,
     validated against the existing base, approved.
   - **Do NOT write interface code until the UX workflow is done first:** the
     foundation → flows → screens → scenarios chain is designed and approved,
     and — when Figma is enabled (default) — the UI is mocked up in Figma with
     every screen linked to its frame. Building UI before this is the exact
     mistake super-ux exists to prevent.
   - Visual identity is ONE locked style pack, recorded in `docs/ux/screens.md`
     → Design system and obeyed by every Figma frame and every built screen —
     picked with the **sheleg-design** companion skill when the project has no
     design system of its own (recommended, not required). Inventing a palette,
     type pairing, or motion per screen is visual drift.
   - After any UX change and before calling the work done, run the linter
     `python3 docs/ux/lint.py` — it must pass (errors are drift/broken
     structure; wire it into CI/pre-commit).
   - Use `/ux` as the entry point; skills: `vision` (what the product is and
     refuses to become), `ux-foundation`, `ux-flows` (flows + Figma mockups),
     `ux-scenarios` for maintenance, `ux-audit` for evidence-backed
     verification, `brand-voice` and `copywriting` for everything the user
     reads. Full map: the plugin's system-map reference.

   ## Brand voice — hard rule (super-ux)

   - `docs/brand/` is the source of truth for how the product speaks:
     `voice.md` (axes, narrative, invariants), `terminology.md` (our words and
     the banned ones), `facts.md` (the only source of any public figure),
     `channels.md` (one record per surface), `strings.md` (the interface string
     registry), `locales/<code>.md`.
   - Any change to public-facing text — an interface string, a landing page, a
     post, a store listing, an ad, an email — updates `docs/brand/` in the SAME
     change. A new string with no registry row is drift, not a detail.
   - **Never quote a number that has no row in `facts.md`,** and never invent a
     fact, statistic, quote or expert to fill a gap. Report the gap instead.
   - **One action keeps one name** across button, confirmation, toast, history,
     notification and accessible name. Search `strings.md` before naming one.
   - **No humor, exclamation marks or emoji** on error, destructive confirm,
     billing or paywall surfaces — in any voice.
   - Run `python3 docs/brand/lint.py` after any text change and before calling
     work done. It must exit clean; wire it into CI or pre-commit alongside the
     UX linter so copy drift cannot merge.
   ```

   If the heading is already present but the block text differs from the
   above, replace the block with this version (it supersedes older ones).

2. If `docs/ux/scenarios.md` does not exist, create `docs/ux/` (including
   `audits/` and `plans/`) and seed `scenarios.md`, `foundation.md`,
   `flows.md`, `screens.md`, and `README.md` from the plugin's `templates/`.
   Never overwrite existing files.

3. Copy **both** scripts from the plugin's `scripts/`, refreshing them even
   if present — they are code, not user content:
   `ux_lint.py` → `docs/ux/lint.py` and `ux_doctor.py` → `docs/ux/doctor.py`.
   Suggest wiring `python3 docs/ux/lint.py` into the project's CI or
   pre-commit. **The rule installed in step 1 tells the reader to run
   `python3 docs/brand/lint.py` as well** — that file is seeded by
   `/brand-init` together with `docs/brand/` itself. If `docs/brand/` does
   not exist yet, say so in the closing report and offer `/brand-init`,
   rather than leaving a rule that points at a missing file.

4. Report what was installed and suggest `/ux` next if the base is still
   empty.
