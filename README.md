# super-ux

[![npm](https://img.shields.io/npm/v/super-ux)](https://www.npmjs.com/package/super-ux)
[![CI](https://github.com/ssheleg/super-ux/actions/workflows/validate.yml/badge.svg)](https://github.com/ssheleg/super-ux/actions/workflows/validate.yml)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Scenario-driven UI development for AI agents (Claude Code + Cursor).

AI agents generate poor interfaces because they build UI without a model of
user behavior: screens appear feature by feature, while error states, empty
states, and cross-feature flows get invented ad hoc or skipped. **super-ux**
fixes the process, not the symptom — a versioned base of UX scenarios becomes
the source of truth for all user-facing behavior. Scenarios are written and
validated *before* UI is built, updated in the same change as any behavior
change, and used as the checklist for recurring, evidence-backed audits of
the codebase.

```mermaid
flowchart LR
    W[Personas + JTBD\n+ journeys + stories] --> B[Derive scenarios\nwith Traces]
    A[Feature idea] --> V{Which job? Which stage?\nValidate vs base}
    W --> V
    V -->|approved| D[Design & build UI]
    D --> E[Update scenarios\nin the same change]
    E --> F[/ux-audit: code vs scenarios\nwith story acceptance criteria/]
    B --> F
    F --> G[Report + findings]
    G --> H[Prioritized fix plan\nFreq × Severity × Solvability] --> D
```

## What's inside

| Piece | Purpose |
|---|---|
| skill `ux-foundation` | The WHY layer (`docs/ux/foundation.md`): personas, Jobs to Be Done with forces, customer journey maps, user stories with Given/When/Then acceptance criteria |
| skill `ux-flows` | The HOW layer + UI map: `docs/ux/flows.md` (task analysis, mermaid user flows referencing screens) and `docs/ux/screens.md` — the design map: every screen and state with its **Figma frame link**, wireframe, code coverage, scenarios, and resources, kept in sync on every interface change (default-on Figma mockups apply the visual-craft practices); heuristic UX evaluation and traced redesign proposals |
| skill `ux-scenarios` | Maintain `docs/ux/scenarios.md`: use-case scenarios (action → system response, alt paths) covering every flow node/edge, `Traces:` to stories and flows, validated for conflicts, coverage, and traceability |
| skill `ux-audit` | Batched audit loop with full context: code vs every scenario + its story's acceptance criteria; verdicts PASS/PARTIAL/FAIL/BLOCKED with `file:line` evidence; `coverage` scope audits the chain itself |
| `/ux` | **The one command**: sets up whatever is missing, then status across all layers + a menu of applicable actions with one recommended default. Idempotent |
| `docs/ux/lint.py` + `/ux-lint` | Deterministic linter: missing Figma frames, unresolved SCR/story traces, orphans, built screens without coverage, index desync, ID gaps, broken links — run after changes and in CI so drift can't merge |
| [system-map.md](plugins/super-ux/skills/references/system-map.md) | The whole system on one page — pipeline, files, skills, and the four sync rules; every skill points here |
| `/ux-foundation` `/ux-flows` `/ux-init` `/ux-update` `/ux-audit` `/ux-rule` `/ux-lint` | Direct controls; `/ux-rule` installs the hard rule into the project's CLAUDE.md |
| [ux-design-principles.md](plugins/super-ux/skills/references/ux-design-principles.md) | How the agent thinks: the design pipeline (forward + backwards), task analysis, flow rules, heuristics PRN-01..16, improvement procedure, anti-patterns |
| `cursor/rules/*.mdc` | The same methodology for Cursor (always-on hard rule + three agent-requested rules) |
| `templates/` | Skeletons for the foundation, scenario base, audit report, and the CLAUDE.md rule snippet |
| [component-guidelines.md](plugins/super-ux/skills/references/component-guidelines.md) | When to use which control (radios/select/switch, sheet/alert, modal/disclosure, combobox, nav bar/rail, FAB, dates, toasts) + platform rules — from Apple HIG, Material 3, W3C ARIA APG, GOV.UK (BP-101..115) |
| [best-practices.md](plugins/super-ux/skills/references/best-practices.md) | Living, tag-indexed catalog of 115 proven UX/growth practices — subscription-app laws, mobile/web/voice interface guidance (HIG 2025, M3 Expressive, NN/g, Baymard, WCAG 2.2), monetization economics (RevenueCat/PLG 2025 benchmarks, ASO, freemium boundaries, web2app), visual craft (typography, color, spacing, microcopy), Figma file structure (BP-091..100); selected deterministically via [practice-selection.md](plugins/super-ux/skills/references/practice-selection.md) |
| [figma-integration.md](plugins/super-ux/skills/references/figma-integration.md) · [figma-structure.md](plugins/super-ux/skills/references/figma-structure.md) | Optional Figma surface (default-on): when/how to mock up, and how to structure the file so frames named `SCR-NN/<Screen>/<state>` map 1:1 to `screens.md` — deterministic lookup, checkable drift |

The format all of them share is locked in
[scenario-format.md](plugins/super-ux/skills/references/scenario-format.md):
scenario entries with stable `SCN-NNN` IDs, personas, per-feature and
per-product completeness checklists, the `draft → validated → implemented`
lifecycle, audit verdicts and severities.

## The hard rule

- `docs/ux/scenarios.md` is the source of truth for all user-facing
  behavior; foundation (WHY) and flows (HOW) are the layers it traces to.
- Any change touching user-facing behavior or interface updates **in the
  same change**: scenarios, affected flows, the affected screens in
  `docs/ux/screens.md` (the UI map — states, elements, coverage), and (Figma
  on) the Figma frames plus their links. Code that diverges from a screen's
  record, or a stale Figma link, is drift the audit flags.
- Any new feature or project **starts** with the chain: which job, which
  journey stage, which story — then flows and scenarios, validated and
  approved.
- **Do not write interface code until the UX workflow is done first** — the
  foundation → flows → scenarios chain designed and approved, and (when
  Figma is enabled, the default) the UI mocked up in Figma with every screen
  linked to its frame. Building UI before this is the mistake super-ux
  exists to prevent.

## Install

### Claude Code

```
/plugin marketplace add ssheleg/super-ux
/plugin install super-ux@super-ux
```

Then in your project: `/ux`. That's it — it installs the hard rule, seeds
`docs/ux/`, builds the scenario base if empty, and on every later run just
reports status and the next action.

### Any agent via the skills CLI (70+ agents)

```sh
npx skills add ssheleg/super-ux            # both skills, current project
npx skills add ssheleg/super-ux -g         # user-global
npx skills add ssheleg/super-ux --skill ux-audit   # one skill
```

[vercel-labs/skills](https://github.com/vercel-labs/skills) discovers the
skills through this repo's marketplace manifest and installs them for Claude
Code, Cursor, Codex, OpenCode and others. Note: this installs the skills
only — the `/ux` commands and the Cursor always-on hard rule come with the
methods below.

### Interactive (pick agent + scope)

```sh
npx super-ux
```

Multi-select menu (space to toggle, `a` = everything at once, enter to
install): skills for any of 70+ agents (delegates to the `skills` CLI picker
— choose agents and global/project there), Cursor rules into a project, and
the Claude Code plugin user-globally — any combination in one run.

### Cursor

```sh
npx super-ux --cursor /path/to/your/project
```

(also works: `npx github:ssheleg/super-ux --cursor <dir>` straight from the
repo, or clone and run `./install.sh --cursor <dir>` — same behavior.) Copies the
rules into `.cursor/rules/` and seeds `docs/ux/`. An existing scenario base
is never overwritten; re-run with `--force` to update rules after a new
release.

### Updating everything

Global channels (run after each release, then restart the Claude Code
session so the plugin reloads):

```sh
claude plugin marketplace update super-ux && \
claude plugin update super-ux@super-ux && \
npx --yes skills update ux-audit ux-flows ux-foundation ux-scenarios --global --yes
```

Cursor rules + the seeded `docs/ux/lint.py` are per-project (Cursor has no
global rules dir) — refresh each project you use:

```sh
npx super-ux@latest --cursor /path/to/your/project --force
```

`--force` overwrites the rule files and the linter; your scenario base
(`docs/ux/scenarios.md`) and the rest of `docs/ux/` are never touched.
Check the published version any time with `npm view super-ux version`.

## For the user: one command, plain words

You don't need to know the layers or skills. Run `/ux` and say what you
want in your own words — "стартуем новый продукт", "добавить фичу", "UX
неудобный, улучши", "проверь что всё работает", "что чинить в первую
очередь". The agent asks at most one clarifying question, picks the right
workflow itself, and only shows you human decisions (approve scenarios,
pick a plan). Everything below this line is internals for the agent.

## Typical cycle

1. `/ux` — first run sets everything up: foundation first (greenfield:
   interview about personas, jobs, journeys; existing code:
   reverse-engineer them), then scenarios derived from the stories with
   full traceability.
2. Work normally; every user-facing change updates the base in the same
   change (the always-on rule catches it; `/ux-update` for manual control).
   New feature ideas are validated against the chain first: which job,
   which journey stage, which story.
3. `/ux` any time — status across layers + action menu; `/ux-audit` —
   batched verification of code vs scenarios (with acceptance criteria);
   `/ux-audit coverage` — chain gaps. Reports land in
   `docs/ux/audits/YYYY-MM-DD.md`.
4. Findings become a concrete UX plan (`docs/ux/plans/…`): target interface
   per screen + traced CREATE/MODIFY/DELETE change table, prioritized by
   Frequency × Severity × Solvability — offered for autonomous execution
   via task-pipeline (or your planning workflow); build; repeat.

## Development

`python3 test/validate.py` checks repo consistency (manifests, versions,
front-matter, templates, links); CI runs it on every push and PR. Versioning
is semver; bump `marketplace.json` + `plugin.json` + `CHANGELOG.md` together
— the validator enforces the sync.

## По-русски (коротко)

Проблема: агенты генерируют плохие интерфейсы, потому что строят UI без
модели поведения пользователя. super-ux строит цепочку: **персоны → JTBD →
карта пути → user stories → UX-сценарии → аудиты → планы фиксов**.
Foundation (`docs/ux/foundation.md`) отвечает на «зачем», сценарии
(`docs/ux/scenarios.md`) — источник правды поведения, трассируются к
stories. Всё пишется и валидируется **до** интерфейса, обновляется тем же
изменением, что и поведение. Аудиты (`/ux-audit`) проверяют код против
сценариев вместе с acceptance criteria, вердикты PASS/PARTIAL/FAIL/BLOCKED
с доказательствами `file:line`; `/ux-audit coverage` ищет дыры в самой
цепочке. Установка: в
Claude Code — `/plugin marketplace add ssheleg/super-ux`, в Cursor —
`npx super-ux --cursor <проект>`. Дальше одна команда — `/ux`: сама ставит
правило и базу, а при повторных запусках показывает статус и следующий шаг.

## License

MIT © ssheleg
