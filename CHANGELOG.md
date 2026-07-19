# Changelog

All notable changes to this project are documented in this file. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions
follow [SemVer](https://semver.org/spec/v2.0.0.html).

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
