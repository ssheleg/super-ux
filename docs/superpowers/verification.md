# Verification ledger — super-ux

One row per shipped requirement, and the answer to a single question: **has
anyone watched this check fail?** A green from a check nobody has seen go red
against a planted defect is not evidence — it is an untested assertion with a
tick beside it.

`Watched` values: `planted` (a defect was introduced and the check caught it,
in this run), `observed` (it caught a real defect at some point), `never`.

## 2026-08-10 — audit findings, v0.32.0

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-01 | The system map names contracts and links none, so no skill inherits a shelf it does not read | `python3 test/sync_references.py` output: ux-flows/foundation/scenarios 19 → 10 contracts, brand-voice 19 → 10, vision 1 | observed |
| R-02 | `vision` reaches the map, the linter, the doctor, a template, a Cursor rule and `/ux` | `validate_skill_parity` asks for each of the seven skills by name in five places | planted — deleted `cursor/rules/vision.mdc`, deleted `copywriting` from `commands/ux.md`, removed a skill from `plugin.json` |
| R-03 | `vision.md` is checked, not trusted: nine sections, a non-empty anti-vision once approved, an installed alignment rule | `python3 docs/ux/lint.py` | planted — renamed `## 6. Anti-vision`, emptied it under `approved`, removed the rule from `CLAUDE.md`, removed the instruction file entirely |
| R-04 | Both hard rules have exactly one source | `validate_hard_rule_copies`, now driven by the `HARD_RULES` pair list | planted — edited one line of the vision rule inside `vision/SKILL.md` |
| R-05 | Every script an instruction names is seeded by some command | `validate_seeded_scripts` | planted — removed the `brand_lint.py → docs/brand/lint.py` clause from `/brand-init` |
| R-06 | Every count in prose equals the artifact it counts | `validate_stated_numbers` | planted — 206→181 practices, 33→31 checks, PRN-01..24→..16, "seven skills"→"four", "seven agent-requested rules"→"four" |
| R-07 | All fifteen commands and all nine templates are required | `validate_commands`, `validate_templates` | planted — removed `commands/copy.md` |
| R-08 | The seeded project passes both linters from the first second | `node bin/super-ux.js --cursor <tmp>` then both linters, exit 0 | observed |
| R-09 | super-ux's own chain and pack exist and pass | `python3 docs/ux/lint.py`, `python3 docs/ux/doctor.py`, `python3 docs/brand/lint.py` — all exit 0 | observed |
| R-10 | B030 reads figures, not identifiers, standards or years | `python3 test/brand_lint_test.py` — four fixtures added | planted — `BP-079..090`, `NIST SP 800-63B`, `Apple HIG 2025` must not fire; `Used by 4200 teams` must |
| R-11 | The literal extractor respects quote pairing and template interpolation | brand pack over `bin/super-ux.js`: 598 warnings → 0 | observed |
| R-12 | B024 allows declared proper nouns, acronyms, sentence boundaries and escape sequences | `python3 test/brand_lint_test.py` (42 checks) plus the real CLI | observed |
| R-13 | The installer speaks one language, offers the routing block from both doors, and its help matches what it writes | `node --check`, end-to-end install, `docs/ux/scenarios.md` SCN-006, SCN-012, SCN-014 | observed |

**Rows at `never`: 0.**

Every `planted` row above names the exact defect that was introduced and
reverted. The plant/revert transcript is the evidence; a row that says
`planted` without naming what was planted is the failure this file exists to
prevent.
