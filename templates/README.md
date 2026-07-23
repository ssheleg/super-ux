# docs/ux — UX design system (super-ux)

This folder is the single source of truth for the product's UX. Keep it in
sync with the code on every interface change.

## The pipeline

```
Personas · JTBD · Journeys · Stories  →  Flows  →  Screens  →  Scenarios  →  Audits  →  Plans
         foundation.md                    flows.md  screens.md  scenarios.md   audits/    plans/
```

| File | Holds |
|------|-------|
| `foundation.md` | WHO & WHY: personas, jobs-to-be-done, journeys, user stories, monetization, Figma on/off |
| `flows.md` | HOW: user-flow diagrams (screens, branches, error paths), referencing screens by `SCR-ID` |
| `screens.md` | THE UI MAP: every screen and state with its Figma frame link, wireframe, code coverage, scenarios, resources |
| `scenarios.md` | WHAT EXACTLY: use-case scenarios — the source of truth for behavior |
| `audits/` | audit reports (code vs the chain) |
| `plans/` | UX plans (target interface + what to create/modify/delete) |
| `wireframes/` | optional low-fi wireframes / storyboards |
| `lint.py` | the integrity/drift linter |

## Rules

1. **Design before you build.** A new feature starts here (job → flow →
   screen → scenario), approved, before any UI code.
2. **Update in the same change.** Any interface change updates
   `scenarios.md`, affected flows, the affected screens in `screens.md`,
   and (Figma on) the Figma frame plus its link — together, not later.
3. **No drift.** Code that diverges from a screen's record, or a stale Figma
   link, is a bug to fix.
4. **Lint it.** Run `python3 docs/ux/lint.py` after changes and in CI.

Maintained with the super-ux plugin. In Claude Code, run `/ux`.
