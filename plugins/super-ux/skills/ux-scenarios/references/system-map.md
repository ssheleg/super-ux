# super-ux System Map

The whole system on one page. Every skill points here so an agent entering
from any trigger sees where it is and what else exists. Read this first when
unsure.

## Contents

- [The pipeline](#the-pipeline)
- [Files in a target project (`docs/ux/`)](#files-in-a-target-project-docsux)
- [The reference shelves: this map names them, and links none](#the-reference-shelves-this-map-names-them-and-links-none)
- [Skills & the one entry point](#skills--the-one-entry-point)
- [The four rules that keep agents in sync](#the-four-rules-that-keep-agents-in-sync)
- [Companions (recommended, never forced)](#companions-recommended-never-forced)
- [When entering mid-project](#when-entering-mid-project)


## The pipeline

```
Vision  →  Personas ─ JTBD ─ Journeys ─ Stories  →  Flows  →  Screens  →  Scenarios  →  Audits  →  Plans
(what the          (WHY, foundation.md)              (HOW,      (UI map,    (what it       (evidence)  (action)
 product IS                                          flows.md)  screens.md)  DOES,
 and refuses                                                                 scenarios.md)
 to become,
 vision.md)
```

Each layer traces to the one above. Build forward for new work; fill
backward (tagged `inferred`) for an existing product. UI code comes only
after this chain is designed and approved (and, with Figma on, mocked up).

**Two layers answer a question shaped like "what", and confusing them is the
one mistake this map exists to prevent.** `vision.md` answers *what the
product is*: its essence, its principles, and what it refuses to become.
`scenarios.md` answers *what it does*: every step, state and error. A
feature can be perfectly scenario'd and still violate the anti-vision, which
is why the alignment check runs before the chain, not inside it.

## Files in a target project (`docs/ux/`)

| File | Layer | Owner skill | Holds |
|------|-------|-------------|-------|
| `vision.md` | what it IS | `vision` | essence, core idea, system behaviour, the user's role, principles, anti-vision, horizon, the one sentence, the alignment test |
| `foundation.md` | WHY | `ux-foundation` | personas, JTBD, journeys, user stories, monetization, Figma on/off + file URL |
| `flows.md` | HOW | `ux-flows` | task analysis + user-flow diagrams, referencing screens by `SCR-ID` |
| `screens.md` | UI map | `ux-flows` | the design system block + every screen and state with Figma frame, wireframe, coverage, scenarios, resources |
| `scenarios.md` | WHAT | `ux-scenarios` | use-case scenarios (source of truth for behavior) |
| `audits/…` | evidence | `ux-audit` | one report per audit run |
| `plans/…` | action | `ux-audit`/`ux-flows` | target-interface + CREATE/MODIFY/DELETE plan |
| `wireframes/…` | optional | `ux-flows` | low-fi ASCII wireframes / storyboards |
| `README.md`, `lint.py`, `doctor.py` | meta | seeded | this map (project copy), the drift linter, the contract doctor |

Beside the chain, one more root: **`docs/brand/`**, the verbal identity
(`brand-contract v1`, named here and not linked; the shelf note below says
why):

| File | Owner skill | Holds |
|------|-------------|-------|
| `voice.md` | `brand-voice` | pack, five axes, narrative, invariants, locales |
| `terminology.md` | `brand-voice` | our words, banned words, entity and tier names |
| `facts.md` | `brand-voice` | canonical numbers, the only source of a figure |
| `channels.md` | `brand-voice` | one record per surface: register, limits, bans |
| `strings.md` | `brand-voice` | interface string registry → `file:line` → scenario |
| `locales/<code>.md` | `brand-voice` | per-locale delta |
| `lint.py` | seeded | `brand_lint.py`, 40 deterministic checks (B001..B073) |

It is a separate root because the brand also governs surfaces that are not
UX: a store listing, an ad, a post. The pack derives from `foundation.md` and
never the reverse. `copywriting` writes from it and never to it.

## The reference shelves: this map names them, and links none

**Every link in a skill is a shipping instruction.** `test/sync_references.py`
copies the transitive closure of a skill's links into that skill, so that the
contracts arrive intact on Cursor, Codex and every other agent that ships one
directory. Because *every skill points at this map*, a link from here is a
link from all of them at once: one pointer to `brand-contract.md` once put all
nine brand contracts inside every UX skill, 352K of App Store guidance riding
along in `ux-foundation`. So the rule here is absolute: **this map names a
contract, it never links one.** Each skill links exactly what it reads, and
carries exactly that.

*The chain shelf.* `scenario-format.md` is the format contract. Design
reasoning: `ux-design-principles.md` (PRN-01..24). Practices:
`best-practices.md`, selected via `practice-selection.md` and previewed
through `best-practices-index.md`; control choice:
`component-guidelines.md`. Figma workflow: `figma-integration.md`; file
structure and naming: `figma-structure.md`. Visual identity (style pack via
the **sheleg-design** companion): `visual-identity.md`. On a paid-acquisition
product, the step before the foundation is reading the funnels already running
in the category: `funnel-research.md` (FR-01..FR-07), carried by `ux-foundation`
and `ux-flows`.

*The brand shelf,* reached through `brand-contract.md`. `voice-packs.md` is
the library the voice is chosen from (six archetypes, each declaring its own
failure mode) and `surface-registers.md` is the model the layer runs on (one
voice, deltas per surface). Craft: `ui-copy.md`, `marketing-copy.md`,
`landing-pages.md`, `channel-playbooks.md`, `store-copy.md`. Guards: `seo-aeo-safety.md`,
`ai-tells.md`, `localization.md`.

## Skills & the one entry point

- **`/ux`** is the only command a user needs. It asks the task in plain words,
  routes to the right workflow, reports status. Users never pick skills.
  Everything below is reachable from it; a skill `/ux` cannot route to is a
  skill nobody runs.
- `vision` is the layer above the chain: what the product is and what it
  refuses to become. Also installs the **vision-alignment rule**, which
  checks a proposed feature against the anti-vision before the chain starts.
- `ux-foundation` · `ux-flows` · `ux-scenarios` build and maintain the layers.
- `ux-audit` verifies code against the chain (depths quick/standard/deep;
  scope `copy` judges text against the brand pack).
- `brand-voice` · `copywriting` define the voice, then write in it.
- Direct commands: `/vision` `/ux-init` `/ux-foundation` `/ux-flows`
  `/ux-update` `/ux-audit` `/ux-rule` `/ux-lint` `/ux-doctor`; `/brand`
  `/brand-init` `/brand-update` `/brand-lint` `/copy`.

## The four rules that keep agents in sync

1. **Chain-first.** New feature/project starts with the chain (which job →
   flow → screen → scenario), validated and approved, before any UI code.
2. **Same-change.** Any interface/behavior change updates the affected
   layers in the SAME change: scenarios always; flows when navigation
   changes; `screens.md` whenever a screen changes; and, with Figma on, the
   Figma frame plus its link.
3. **No drift.** Code diverging from a screen's `screens.md` record, a
   stale/broken Figma link, an orphan, or a broken trace is a finding, not
   an acceptable state. The linter makes this checkable.
4. **Run the linter.** After any UX change and before calling work done,
   run `python3 docs/ux/lint.py` (or `/ux-lint`). It must pass; wire it into
   the project's CI/pre-commit so drift can't merge.

## Companions (recommended, never forced)

- **sheleg-design** carries the visual identity: one locked style pack (palette,
  type, texture, motion tokens, bans) + ready token CSS, plus the motion
  methodology for cinematic scroll-driven pages. Used at VISUALIZE/BUILD,
  recorded once in `screens.md` → Design system. The protocol lives in
  `visual-identity.md`, carried by the skills that draw.
- **task-pipeline** implements a finished UX plan end-to-end (spec → plan →
  subagent build → tests → deploy → docs). Offered after audits and Improve
  passes.

Both are offers, not dependencies: one recommendation with its one-time
install, then the user's answer stands.

## When entering mid-project

Run `/ux` (or `python3 docs/ux/lint.py`) first: it reports which layers
exist, what's stale, and the one recommended next action. Reconstruct
nothing by hand.
