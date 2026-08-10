# docs/ux — UX design system (super-ux)

This folder is the single source of truth for the product's UX. Keep it in
sync with the code on every interface change.

## The pipeline

```
Vision  →  Personas · JTBD · Journeys · Stories  →  Flows  →  Screens  →  Scenarios  →  Audits  →  Plans
vision.md           foundation.md                  flows.md  screens.md  scenarios.md   audits/    plans/
```

| File | Holds |
|------|-------|
| `vision.md` | WHAT IT IS: essence, core idea, principles, the anti-vision, the alignment test. Optional layer; when present, new features are checked against it before anything is designed |
| `foundation.md` | WHO & WHY: personas, jobs-to-be-done, journeys, user stories, monetization, Figma on/off + file URL |
| `flows.md` | HOW: user-flow diagrams (screens, branches, error paths), referencing screens by `SCR-ID` |
| `screens.md` | THE UI MAP: every screen and state with its Figma frame link, wireframe, code coverage, scenarios, resources |
| `scenarios.md` | WHAT IT DOES: use-case scenarios — the source of truth for behavior |
| `audits/` | audit reports (code vs the chain) |
| `plans/` | UX plans (target interface + what to create/modify/delete) |
| `wireframes/` | optional low-fi wireframes / storyboards |
| `lint.py` | the integrity/drift linter |
| `doctor.py` | the contract doctor — mixed or stale contract versions across the artifacts |

**Two files answer a question shaped like "what".** `vision.md` says what
the product **is**; `scenarios.md` says what it **does**. A feature can
satisfy every scenario and still violate the anti-vision.

## Its sibling: `docs/brand/`

`docs/ux/` decides what the product does. **`docs/brand/`** decides how it
speaks — `voice.md`, `terminology.md`, `facts.md`, `channels.md`,
`strings.md`, `locales/<code>.md`, and its own `lint.py`. It is a separate
root because the brand also governs surfaces that are not UX: a store
listing, an ad, a post. Seed it with `/brand-init`.

## Rules

1. **Design before you build.** A new feature starts here (job → flow →
   screen → scenario), approved, before any UI code. With `vision.md`
   present, it is checked against the anti-vision first.
2. **Update in the same change.** Any interface change updates
   `scenarios.md`, affected flows, the affected screens in `screens.md`,
   and (Figma on) the Figma frame plus its link — together, not later.
   Any change to public text updates `docs/brand/` the same way.
3. **No drift.** Code that diverges from a screen's record, or a stale Figma
   link, is a bug to fix. The same goes for the look: one style pack is
   recorded in `screens.md` → Design system (pick it with the
   **sheleg-design** skill) and every screen obeys it.
4. **Lint it.** Run `python3 docs/ux/lint.py` after changes and in CI —
   plus `python3 docs/brand/lint.py` after any text change.

Maintained with the super-ux plugin. In Claude Code, run `/ux`.
