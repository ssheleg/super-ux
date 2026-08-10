# Acceptance — web surface in the chain, and a router that speaks

**v0.33.0**, tag pushed atomically, CI green, npm serving `0.33.0`.
Run commit `7c66119`. Board: **8 open** (B-001..B-005, B-010..B-012),
verification ledger: **0 rows at `never`**, carry-over: **1 open**, below.

## The ladder walk, first

Each REQ walked bottom-up — decision → spec section → contract *and its failure
behaviour* → task → change → executed test → surface. Findings ordered by seam.

| Seam | What the walk found | Where it went |
|---|---|---|
| contract → gate | The `Web surface:` block would have shipped as prose with no check if the fixture harness had not been written first — `ux_lint.py` had no test file at all | Built `test/ux_lint_test.py`, wired into CI. Backfill for older checks → **B-010** |
| gate → seeded template | B007 fired on every freshly seeded pack: a new pack legitimately has no references yet | Gated on `Status` leaving `draft`. Standing instruction 3 caught it — one stamp after being written |
| doctrine → count | `README.md` and `system-map.md` said 33 checks against 35 emitted | Caught by `validate_stated_numbers` mid-run; both updated |
| code → contract | B007 and B026 had no row in `brand-contract.md` | Caught by `validate_brand_lint_coverage` mid-run; both rows added |
| release → family | super-ux's pin, and two others released by concurrent sessions, were behind; `seo-aeo-audit`'s submodule pointer was moved in the working tree with no parent commit recording it | `check_pins.py` found all three. Pins bumped, pointers committed |
| registry → pin | `sheleg-design` was briefly pinned ahead of npm: the tag existed, the registry still served the previous version | Pinning waited for the registry, not the tag — `update` installs from npm |
| article → doctrine | Of three sources read, most content was already covered or carried no source | Three items entered (B007's field, and two board rows); the unsourced numbers were rejected and the rejection recorded |

Two absences the walk surfaced became new REQ rows **before** the table below:
**R-14** (a fixture harness must exist before a check is trusted) and **R-15**
(a new check runs against the seeded template before anything else — promoted
from standing instruction to a shipped requirement of this run).

## Coverage

| REQ | Evidence | Watched |
|---|---|---|
| R-01 | `scenario-format.md` → screen entry + five rules; `validate.py` OK (3112 checks) | observed |
| R-02 | `check_web_surface` in `ux_lint.py`; fixture *no declaration at all warns* | planted — removed the declaration |
| R-03 | five fixtures, one per missing field, plus the `no`-with-a-block contradiction | planted — each field deleted in turn |
| R-04 | `node bin/super-ux.js --cursor <tmp>` then both linters, exit 0, zero warnings | observed |
| R-05 | `ux-flows/SKILL.md` step 5, beside Figma and the style pack | observed |
| R-06 | `ux-audit/SKILL.md` pass 2 — route, no-JS, entity, indexation, and the declaration contradiction | observed |
| R-07 | `commands/ux.md` §0, `system-map.md`, README; install commands verified against the registry (`@ssheleg/seo-aeo-audit` 0.14.0, scoped) | observed |
| R-08 | four rows in `commands/ux.md`; each names the action and the practice set behind it | observed |
| R-09 | step 0 decomposition rule | observed |
| R-10 | `validate.py` OK (3112 checks) | planted — the run went red on two counts and two missing contract rows |
| R-11 | `docs/ux/screens.md` → Web surfaces `no`, with the reason; `docs/brand/voice.md` → references | observed |
| R-12 | `ux_doctor.py` exit 0, marker unchanged at v4 | observed |
| R-13 | `release_preflight.py` OK; `git push --atomic`; run 31406816515 success; `npm view super-ux version` → `0.33.0`; GitHub release not draft | observed |
| R-14 | `test/ux_lint_test.py`, 14 checks, in `validate.yml` | planted — 10 of 14 red before the implementation |
| R-15 | B007 gated on `draft`; fresh install lints clean, zero warnings | planted — the ungated version warned on every seeded pack |

**Rows at `never`: 0.**

## Ledgers

- **Board:** B-007, B-008, B-009 closed. B-010, B-011, B-012 opened from this
  run. Eight open, priorities re-derived.
- **Carry-over, 1 open:** the npm name `task-pipeline` belongs to an unrelated
  package (`node-task`, 0.1.0); ours is `task-pipeline-skill` (1.38.0).
  super-ux never advises `npx task-pipeline`, so nothing here is wrong — the row
  exists so the next person to write an install line does not invent it. **Home:
  the task-pipeline repository**, not this one.
- **Repositories:** `super-ux` clean and pushed; `sshlg-skills` clean, pushed,
  `git submodule status` with no line starting `+`.
