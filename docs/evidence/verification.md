# Verification ledger — super-ux

One row per shipped requirement, and the answer to a single question: **has
anyone watched this check fail?** A green from a check nobody has seen go red
against a planted defect is not evidence — it is an untested assertion with a
tick beside it.

`Watched` values: `planted` (a defect was introduced and the check caught it,
in this run), `observed` (it caught a real defect at some point), `never`.

## 2026-08-12 — the reference sweep for flows, v0.35.0 → v0.35.1

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-14 | `ux-flows` step 2 sweeps a reference server before a node is drawn, gated on tools present rather than config | Fresh-context run, 2026-08-12: an iOS subscription-cancellation brief that never mentioned references | **observed** — see the note below |
| R-15 | Refero and Mobbin both return multi-step flows, in different media (structure vs preview images) | Live tool surfaces: `tools/list` on `api.refero.design`, and one `mcp__mobbin__search_flows` query returning a twenty-screen flow | observed — and it **refuted** the claim shipped in 0.35.0 |

**R-14 was filed `never` and closed the same day.** No check in this repository
can watch an agent decide to sweep — the behaviour lives in a SKILL.md an agent
reads, not a script a gate runs — so the only evidence available was a run. It
was run: a fresh context, an iOS subscription-cancellation brief, and **no
mention of references, sweeping, Mobbin or Refero anywhere in the prompt.** The
agent gated on the tools present rather than the config and said so
(`mcp__mobbin__*` and `mcp__lazyweb__*` present, `mcp__refero__*` absent), swept
both **before** drawing, read four shipped cancellation flows, and named what
each one changed and what it refused to let them change — the job stayed the
foundation's and the visual identity stayed the style pack's. It also declined an
instruction embedded in one server's own response asking to alter persistent
instructions, which is the untrusted-data rule holding under a live test nobody
designed.

Still `observed` rather than `planted`: nothing was planted, because there is
nothing here to plant a defect *in*. That limit is permanent and is the reason
this row reads the way it does.

**R-15 is why the ledger earns its keep.** 0.35.0 shipped the claim that Refero
was the only server returning flows, written while Mobbin was registered and
unauthenticated — invisible, therefore uncheckable. Signing in refuted it inside
an hour. The correction is 0.35.1.

## 2026-08-10 — UX linter codes and coverage, v0.34.0

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-01 | Every UX linter rule carries a stable code `U001..U054` | `validate_ux_lint_coverage` finds 21 | observed |
| R-02 | Every code has a fixture with its planted defect | `python3 test/ux_lint_test.py` — 43 checks | planted — three defects in the linter (`n > 1`→`n > 99`, frame branch short-circuited, `status == "never"`), each turned exactly one case red |
| R-03 | Every code has a row in the contract | `validate_ux_lint_coverage` | planted — deleted the U040 row |
| R-04 | A code with no fixture fails the build | `validate_ux_lint_coverage` | planted — renamed `"U014"` in the harness |
| R-05 | Every `python3 docs/**/*.py` an instruction names is seeded by a command | `validate_run_instructions` | planted — instruction renamed to `docs/ux/linter.py` |
| R-06 | The seeded project still lints clean, zero warnings | fresh install + both linters | observed |
| R-07 | v0.34.0 ships: four version places, preflight, atomic push, CI read, registry serving | run 31421172382, `npm view` → 0.34.0 | observed |

**Rows at `never`: 0.**

## 2026-08-10 — web surface and routing, v0.33.0

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-01 | A public screen records five fields, each the design-time twin of a live-page check | `scenario-format.md`; `validate.py` (3112 checks) | observed |
| R-02 | `screens.md` declares `Web surfaces: yes\|no`; absence is declared, not assumed | `check_web_surface` | planted — removed the declaration |
| R-03 | A partial block errors; `no` silences; a URL entry point under `no` still warns | `test/ux_lint_test.py` | planted — each of the five fields deleted in turn |
| R-04 | The seeded project lints clean from the first second, zero warnings | fresh install + both linters | observed |
| R-05 | `ux-flows` asks the web-surface question beside Figma and the style pack | `ux-flows/SKILL.md` step 5 | observed |
| R-06 | `ux-audit` checks a built public screen against its record | `ux-audit/SKILL.md` pass 2 | observed |
| R-07 | `seo-aeo-audit` is the third companion, with install commands verified against the registry | `commands/ux.md`, `system-map.md`, README | observed |
| R-08 | `/ux` speaks funnel, design, SEO and mobile app | `commands/ux.md` routing table | observed |
| R-09 | A composite brief maps to every matching row, in chain order | `commands/ux.md` step 0 | observed |
| R-10 | Counts, contract rows, manifests and hard rules stay in sync | `validate.py` | planted — went red on 33-vs-35 and two missing contract rows |
| R-11 | super-ux answers its own new questions | `docs/ux/screens.md`, `docs/brand/voice.md` | observed |
| R-12 | Contract stays v4 | `ux_doctor.py`, marker unchanged | observed |
| R-13 | v0.33.0 tagged, CI green, registry serving it | preflight, run 31406816515, `npm view` | observed |
| R-14 | The UX linter has a fixture harness at all | `test/ux_lint_test.py`, 14 checks, in CI | planted — 10 of 14 red before implementation |
| R-15 | A new check runs against the seeded template before anything else | B007 gated on `draft`; fresh install clean | planted — the ungated version warned on every seeded pack |

**Rows at `never`: 0.**

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
