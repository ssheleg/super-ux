# super-ux System Map

The whole system on one page. Every skill points here so an agent entering
from any trigger sees where it is and what else exists. Read this first when
unsure.

## The pipeline

```
Personas ─ JTBD ─ Journeys ─ Stories   →  Flows  →  Screens  →  Scenarios  →  Audits  →  Plans
        (WHY, foundation.md)              (HOW,      (UI map,    (WHAT,        (evidence)  (action)
                                          flows.md)  screens.md) scenarios.md)
```

Each layer traces to the one above. Build forward for new work; fill
backward (tagged `inferred`) for an existing product. UI code comes only
after this chain is designed and approved (and, with Figma on, mocked up).

## Files in a target project (`docs/ux/`)

| File | Layer | Owner skill | Holds |
|------|-------|-------------|-------|
| `foundation.md` | WHY | `ux-foundation` | personas, JTBD, journeys, user stories, monetization, Figma on/off + file URL |
| `flows.md` | HOW | `ux-flows` | task analysis + user-flow diagrams, referencing screens by `SCR-ID` |
| `screens.md` | UI map | `ux-flows` | the design system block + every screen and state with Figma frame, wireframe, coverage, scenarios, resources |
| `scenarios.md` | WHAT | `ux-scenarios` | use-case scenarios (source of truth for behavior) |
| `audits/…` | evidence | `ux-audit` | one report per audit run |
| `plans/…` | action | `ux-audit`/`ux-flows` | target-interface + CREATE/MODIFY/DELETE plan |
| `wireframes/…` | optional | `ux-flows` | low-fi ASCII wireframes / storyboards |
| `README.md`, `lint.py` | meta | seeded | this map (project copy) + the linter |

Beside the chain, one more root — **`docs/brand/`**, the verbal identity
(`brand-contract v1`, [brand-contract.md](brand-contract.md)):

| File | Owner skill | Holds |
|------|-------------|-------|
| `voice.md` | `brand-voice` | pack, five axes, narrative, invariants, locales |
| `terminology.md` | `brand-voice` | our words, banned words, entity and tier names |
| `facts.md` | `brand-voice` | canonical numbers — the only source of a figure |
| `channels.md` | `brand-voice` | one record per surface: register, limits, bans |
| `strings.md` | `brand-voice` | interface string registry → `file:line` → scenario |
| `locales/<code>.md` | `brand-voice` | per-locale delta |
| `lint.py` | seeded | `brand_lint.py`, 31 deterministic checks |

It is a separate root because the brand also governs surfaces that are not UX
— a store listing, an ad, a post. The pack derives from `foundation.md` and
never the reverse. `copywriting` writes from it and never to it.

Formats: [scenario-format.md](scenario-format.md). Design reasoning:
[ux-design-principles.md](ux-design-principles.md). Practices:
[best-practices.md](best-practices.md) selected via
[practice-selection.md](practice-selection.md); control choice:
[component-guidelines.md](component-guidelines.md). Figma workflow:
[figma-integration.md](figma-integration.md); Figma file structure &
naming: [figma-structure.md](figma-structure.md). Visual identity (style
pack via the **sheleg-design** companion):
[visual-identity.md](visual-identity.md).

## Skills & the one entry point

- **`/ux`** — the only command a user needs. Asks the task in plain words,
  routes to the right workflow, reports status. Users never pick skills.
- `ux-foundation` · `ux-flows` · `ux-scenarios` — build/maintain the layers.
- `ux-audit` — verify code against the chain (depths quick/standard/deep;
  scope `copy` judges text against the brand pack).
- `brand-voice` · `copywriting` — define the voice, then write in it.
- Direct commands: `/ux-init` `/ux-foundation` `/ux-flows` `/ux-update`
  `/ux-audit` `/ux-rule` `/ux-lint`; `/brand` `/brand-init` `/brand-update`
  `/brand-lint` `/copy`.

## The four rules that keep agents in sync

1. **Chain-first.** New feature/project starts with the chain (which job →
   flow → screen → scenario), validated and approved, before any UI code.
2. **Same-change.** Any interface/behavior change updates the affected
   layers in the SAME change: scenarios always; flows when navigation
   changes; `screens.md` whenever a screen changes; and — Figma on — the
   Figma frame plus its link.
3. **No drift.** Code diverging from a screen's `screens.md` record, a
   stale/broken Figma link, an orphan, or a broken trace is a finding, not
   an acceptable state. The linter makes this checkable.
4. **Run the linter.** After any UX change and before calling work done,
   run `python3 docs/ux/lint.py` (or `/ux-lint`). It must pass; wire it into
   the project's CI/pre-commit so drift can't merge.

## Companions (recommended, never forced)

- **sheleg-design** — the visual identity: one locked style pack (palette,
  type, texture, motion tokens, bans) + ready token CSS, plus the motion
  methodology for cinematic scroll-driven pages. Used at VISUALIZE/BUILD,
  recorded once in `screens.md` → Design system.
  [visual-identity.md](visual-identity.md).
- **task-pipeline** — implements a finished UX plan end-to-end (spec → plan →
  subagent build → tests → deploy → docs). Offered after audits and Improve
  passes.

Both are offers, not dependencies: one recommendation with its one-time
install, then the user's answer stands.

## When entering mid-project

Run `/ux` (or `python3 docs/ux/lint.py`) first: it reports which layers
exist, what's stale, and the one recommended next action — reconstruct
nothing by hand.
