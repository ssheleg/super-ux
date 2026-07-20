# Changelog

All notable changes to this project are documented in this file. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions
follow [SemVer](https://semver.org/spec/v2.0.0.html).

## [0.7.0] - 2026-07-20

### Added

- **Best-practices catalog** (`skills/references/best-practices.md`) — a
  living, tag-indexed catalog (48 entries seeded from "48 Laws of
  Subscription App Success", Botsi 2025): each practice has an ID (BP-NNN),
  own-words summary, mechanism, applicability, and tags (stage / mechanism /
  domain / effect) so agents can select what fits the product. Growable per
  in-file rules.
- Integration: `ux-scenarios` consults the catalog when drafting (practices
  applied only when they serve a traced job); `ux-foundation` uses it for
  journey opportunities; `ux-audit` gains an optional practices pass
  (suggestion findings `[BP-NNN]`, never blockers); `/ux` menu gains a
  "Best-practices review" action.

## [0.6.0] - 2026-07-20

### Added

- **ux-foundation skill** — the WHY layer: personas, Jobs to Be Done (with
  forces and success metrics), customer journey maps (stage / action /
  touchpoint / emotion / pain / opportunity), user stories (INVEST,
  Given/When/Then acceptance criteria). New file contract
  `docs/ux/foundation.md`, template, `/ux-foundation` command, Cursor rule.
- **ux-contract v2** — scenarios gain a `Traces:` field (story/job/journey
  stage) and traceability rules: every must/should story covered, every
  scenario serves a story or job; orphans are findings.
- **Full-context audits** — `ux-audit` loads traced acceptance criteria as
  checks and judges whether the implementation serves the job, not just
  renders elements; new `coverage` scope audits the chain itself; fix plans
  prioritized by Frequency × Severity × Solvability.
- **`/ux` action menu** — single entry point now reports status across all
  three layers and offers the applicable actions (init/update foundation,
  build scenarios, validate chain, audit, coverage audit, plan fixes) with
  one recommended default.

## [0.5.0] - 2026-07-19

### Changed

- Installer menu is now a real multi-select: arrow keys / j k to move, space
  or number to toggle, `a` selects all three targets at once, enter installs
  the whole selection in one run (own questions asked up front, the external
  skills-CLI picker runs last). Non-TTY stdin gets a text fallback
  (`1,3` / `all` / `q`). Zero dependencies (stdlib raw-mode).

## [0.4.0] - 2026-07-19

### Added

- Interactive installer menu: bare `npx super-ux` now offers (1) skills for
  any of 70+ agents via the `skills` CLI picker, (2) Cursor rules into a
  project, (3) the Claude Code plugin user-globally (runs the `claude plugin`
  CLI when available). Flag paths (`--cursor [dir] [--force]`) unchanged.

### Fixed

- Prompt handling with piped stdin (persistent line buffer instead of
  sequential `rl.question`, which dropped pre-buffered answers).

## [0.3.0] - 2026-07-19

### Added

- npx installer: `npx github:ssheleg/super-ux --cursor [project-dir]`
  (`bin/super-ux.js`, cross-platform Node CLI, no dependencies) — same
  behavior as `install.sh`, plus `package.json` for npm/npx distribution.
- Validator now checks `package.json` (name, bin shebang, files whitelist)
  and includes its version in the version-sync check.

## [0.2.0] - 2026-07-19

### Added

- `/ux` — one-command entry point: inspects the project, installs the hard
  rule and seeds/initializes the scenario base if anything is missing,
  otherwise prints a status report and suggests exactly one next action.
  Idempotent; `/ux-init`, `/ux-update`, `/ux-audit`, `/ux-rule` remain as
  direct controls.

## [0.1.0] - 2026-07-19

### Added

- Claude Code plugin `super-ux`: skills `ux-scenarios` (maintain the scenario
  base) and `ux-audit` (scenario audit loop); commands `/ux-init`,
  `/ux-update`, `/ux-audit`, `/ux-rule`.
- Scenario format contract v1
  (`plugins/super-ux/skills/references/scenario-format.md`).
- Cursor rules: `cursor/rules/super-ux.mdc` (always-on hard rule),
  `ux-scenarios.mdc`, `ux-audit.mdc`.
- Templates: scenario base skeleton, audit report skeleton, CLAUDE.md hard
  rule snippet.
- `install.sh --cursor <project-dir>` installer for Cursor projects.
- Repo validator (`test/validate.py`) and GitHub Actions CI.
