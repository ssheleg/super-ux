# super-ux — Scenario-Driven UI Development for AI Agents (Design Spec)

- **Date:** 2026-07-19
- **Status:** Approved (variant A: full plugin marketplace repo)
- **Repo:** `ssheleg/super-ux` (public, MIT)
- **Language:** All agent-facing content in English. Scenario files generated in
  target projects follow the target project's language.

## 1. Problem

AI agents generate poor interfaces because they build UI without a model of
user behavior. Screens get created feature-by-feature; error states, empty
states, and cross-feature flows are invented ad hoc or skipped entirely.

**Fix:** make a versioned base of UX scenarios the source of truth for all
user-facing behavior. Scenarios are written and validated *before* UI is
built, kept up to date on every change, and used as the checklist for
recurring scenario audits of the codebase.

## 2. Deliverable

One public GitHub repo `ssheleg/super-ux` containing:

1. A **Claude Code plugin** `super-ux` (installable via
   `/plugin marketplace add ssheleg/super-ux`) with two skills and four
   commands.
2. **Cursor rules** (`.mdc`) implementing the same methodology for Cursor.
3. **Templates** for the scenario base, audit report, and the CLAUDE.md rule
   snippet.
4. **Validation**: `test/validate.py` + GitHub Actions CI.

## 3. Repo layout (locked)

```
super-ux/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── super-ux/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/
│       │   ├── ux-init.md
│       │   ├── ux-update.md
│       │   ├── ux-audit.md
│       │   └── ux-rule.md
│       └── skills/
│           ├── ux-scenarios/
│           │   └── SKILL.md
│           ├── ux-audit/
│           │   └── SKILL.md
│           └── references/
│               └── scenario-format.md
├── cursor/
│   └── rules/
│       ├── super-ux.mdc          # alwaysApply: the hard rule
│       ├── ux-scenarios.mdc      # agent-requested: format + maintenance
│       └── ux-audit.mdc          # agent-requested: audit methodology
├── templates/
│   ├── scenarios.md              # scenario base skeleton
│   ├── audit-report.md           # audit report skeleton
│   └── claude-rule.md            # CLAUDE.md rule snippet
├── test/
│   └── validate.py
├── .github/
│   └── workflows/
│       └── validate.yml
├── docs/
│   └── superpowers/
│       ├── specs/
│       └── plans/
├── install.sh
├── README.md
├── CHANGELOG.md
└── LICENSE
```

## 4. Target-project contract (locked)

The plugin operates on a *target project* and maintains:

```
docs/ux/
├── scenarios.md              # the scenario base (source of truth)
└── audits/
    └── YYYY-MM-DD[-scope].md # audit results, one file per run
```

### 4.1 `docs/ux/scenarios.md` format

Managed markdown file. Structure:

1. **Header comment** — `<!-- Managed with super-ux (scenario-format v1).
   Update in the same change as any user-facing behavior change. -->`
2. **Index table** — one row per scenario:
   `| ID | Title | Feature | Persona | Status | Last audit |`
3. **Personas section** — named personas (`new-user`, `returning-user`, …)
   with 1–3 sentences each.
4. **Scenarios** grouped by feature, each entry:

```markdown
### SCN-001: First-run onboarding — happy path
- **Persona:** new-user
- **Feature:** onboarding
- **Entry point:** first launch, no saved state
- **Preconditions:** none
- **Steps:**
  1. User opens the app for the first time …
- **Expected result:** user lands on the main screen with project created
- **UI elements:** [every button, field, link, dialog the user interacts with]
- **States covered:** loading | empty | error | success (list which apply)
- **Errors & recovery:** what the user sees on each failure and how they recover
- **Status:** draft | validated | implemented | retired
- **Coverage:** src/onboarding/Wizard.tsx:12 (or `none yet`)
```

**Rules (locked):**

- IDs are `SCN-NNN`, sequential, **never reused**. Retired scenarios keep
  their entry with `Status: retired` — never deleted.
- Status lifecycle: `draft` → `validated` (human approved) → `implemented`
  (coverage confirmed by audit) → `retired`.
- Coverage completeness checklist per feature: happy path, every error path,
  empty state, loading state, destructive-action confirmation, and the
  returning-user variant where behavior differs.
- Full-product checklist: first-run onboarding, every core feature flow,
  settings, multi-entity flows (e.g. adding a second project), account/data
  lifecycle where applicable.

### 4.2 Audit report format (`docs/ux/audits/YYYY-MM-DD[-scope].md`)

```markdown
# UX Audit — YYYY-MM-DD
- **Scope:** all | feature:<name> | SCN-001..SCN-020
- **Method:** static code trace [+ live run]
- **Base version:** git SHA of scenarios.md at audit time

## Summary
- Totals: PASS n / PARTIAL n / FAIL n / BLOCKED n
- Top issues: …
- Recommended next actions (prioritized): …

## Batch 1: <feature> (SCN-001..SCN-005)
### SCN-001 — PASS|PARTIAL|FAIL|BLOCKED
- **Evidence:** file:line, file:line …
- **Findings:**
  - [AUD-YYYY-MM-DD-01] (critical|major|minor) description → suggested fix

## Findings register
| # | Scenario | Severity | Finding | Suggested fix |
```

**Verdicts (locked):** `PASS` (all elements/states present and wired),
`PARTIAL` (flow exists, gaps found), `FAIL` (flow missing or broken),
`BLOCKED` (cannot verify — say why; never guess).

After a run, the auditor updates the `Last audit` column in `scenarios.md`
(e.g. `2026-07-19 PASS`) and flips `validated` → `implemented` where coverage
is confirmed.

### 4.3 The hard rule (CLAUDE.md snippet, `templates/claude-rule.md`)

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

## 5. Skills

### 5.1 `ux-scenarios` — maintain the scenario base

Front-matter description triggers on: creating or updating UX scenarios,
starting a new feature/project, any UI change, "ux scenarios", onboarding a
codebase into the methodology.

Four workflows (mode auto-detected, overridable):

- **Init (greenfield):** no code yet → interview the user (personas, jobs,
  features), draft the full scenario base first. UI comes after validation.
- **Init (existing code):** inventory sweep of the codebase — routes/screens,
  components, buttons, dialogs, error paths, empty/loading states — draft
  scenarios covering *everything found*, flag gaps (states that exist in code
  but have no scenario, and vice versa), present for validation.
- **Update:** given a change (diff or description), update affected
  scenarios in the same change; new user-facing behavior without a scenario
  is a blocker, not a warning.
- **Validate:** consistency pass — duplicate/conflicting scenarios, personas
  drift, features without error/empty coverage, index/table sync, ID
  integrity. New feature ideas are checked against existing scenarios for
  conflicts before any UI work.

The skill reads `references/scenario-format.md` for the format contract and
uses `templates/scenarios.md` when creating the file.

### 5.2 `ux-audit` — scenario audit loop

Triggers on: "ux audit", verifying UI against scenarios, pre-release UX
checks, "прогони по сценариям".

Loop (locked):

1. Read `docs/ux/scenarios.md`; determine scope (all / feature / ID range).
2. Group scenarios into batches by feature (~5–8 per batch).
3. Per batch — may dispatch parallel subagents, one batch per agent: for each
   scenario trace the code: entry point exists? every step reachable? every
   listed UI element present? loading/empty/error/success states handled?
   errors honest (no silent swallowing)? Record verdict + `file:line`
   evidence. No evidence → `BLOCKED`, never a guess.
4. Write the report to `docs/ux/audits/` (format §4.2), appending batch by
   batch.
5. Final summary with totals, top issues, prioritized recommendations.
6. Update `Last audit` column + statuses in `scenarios.md`.
7. Offer handoff: turn FAIL/PARTIAL findings into a plan via the project's
   planning workflow (superpowers writing-plans / task-pipeline) — offer,
   don't auto-run.

Optional dynamic pass (documented, off by default): if the project has a
runnable dev server and browser tooling is available, replay top scenarios
live and attach observed evidence.

## 6. Commands (thin wrappers)

| Command | Behavior |
|---|---|
| `/ux-init` | Invoke `ux-scenarios`, init mode (auto-detect greenfield vs existing code) |
| `/ux-update` | Invoke `ux-scenarios`, update mode, `$ARGUMENTS` = change description |
| `/ux-audit` | Invoke `ux-audit`, `$ARGUMENTS` = scope (default: all) |
| `/ux-rule` | Install `templates/claude-rule.md` into the project's CLAUDE.md (idempotent), create `docs/ux/` skeleton if missing |

## 7. Cursor rules (`cursor/rules/*.mdc`)

- `super-ux.mdc` — `alwaysApply: true`; the hard rule (§4.3) + pointer to the
  scenario file and formats.
- `ux-scenarios.mdc` — `alwaysApply: false` + description; format contract +
  the four maintenance workflows (condensed from §5.1).
- `ux-audit.mdc` — `alwaysApply: false` + description; audit loop (condensed
  from §5.2).

Installed by copying into the target project's `.cursor/rules/` via
`install.sh --cursor <project-dir>` (also copies `templates/` usage docs).

## 8. install.sh

- `./install.sh --cursor <project-dir>` — copy `cursor/rules/*.mdc` into
  `<project-dir>/.cursor/rules/`, create `docs/ux/` from templates if absent.
  Refuses to overwrite existing rule files unless `--force`.
- No flags → print usage, including the Claude Code path
  (`/plugin marketplace add ssheleg/super-ux` → `/plugin install
  super-ux@super-ux`).
- POSIX sh, `set -eu`, clear errors on missing target dir.

## 9. Validation & CI

`test/validate.py` (stdlib only, exit non-zero on failure):

1. `marketplace.json` / `plugin.json` parse; required fields present;
   versions match each other and the latest CHANGELOG entry.
2. Every `skills/*/SKILL.md` has YAML front-matter with `name` (matches dir)
   and `description`.
3. Every `commands/*.md` has front-matter with `description`.
4. Every `cursor/rules/*.mdc` has front-matter with `alwaysApply` and (unless
   alwaysApply) `description`.
5. Templates referenced by skills/commands exist.
6. Relative markdown links inside the repo resolve.

`.github/workflows/validate.yml` runs it on push + PR (ubuntu, python3).

## 10. README

English, with a short Russian section at the end. Sections: problem → the
methodology (scenario-first, one diagram in mermaid), install (Claude Code /
Cursor), commands, the hard rule, target-project file contract, updating,
contributing, license.

## 11. Versioning

Semver, starting `0.1.0`. `CHANGELOG.md` (keep-a-changelog style). Versions in
`marketplace.json` + `plugin.json` bumped together; `validate.py` enforces
sync.

## 12. Non-goals / future

- Dynamic (live browser) audit as a first-class stage — documented as
  optional only in v0.1.
- A dedicated `ux-auditor` agent definition (`agents/`) for batch runs.
- VS Code / Copilot rule variants.
- Scenario coverage metrics dashboard.

## 13. Human steps (single block)

1. `gh auth login -h github.com` (current token is invalid — 401).
2. Confirm repo creation: `gh repo create ssheleg/super-ux --public` + push
   (agent runs these once auth works; they are prepared in the plan).
