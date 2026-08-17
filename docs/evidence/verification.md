# Verification ledger — super-ux

One row per shipped requirement, and the answer to a single question: **has
anyone watched this check fail?** A green from a check nobody has seen go red
against a planted defect is not evidence — it is an untested assertion with a
tick beside it.

`Watched` values: `planted` (a defect was introduced and the check caught it,
in this run), `observed` (it caught a real defect at some point), `never`.

## 2026-08-14 — web funnel mechanics, v0.40.0

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-27 | BP-211 states the personalization boundary: named state keys, a mandatory default, and product and price identical across every branch | The entry, its tags, and `bp_index --check` agreeing with the catalog | **observed** — the gap it closes was measured before it was written: BP-010 and BP-029 both say to branch and neither says where the branch stops |
| R-28 | BP-212 states the stand-up order, BP-213 the three decisions on a stored answer, BP-214 that legal text is sourced, BP-215 the access ladder and its token rule | Each entry; `validate_stated_numbers` recomputes the 215 the README quotes | **observed** — `B030` refused `215` in the README until `facts.md` was recomputed |
| R-29 | `[GDPR]` Art. 13 fixes the notice at the moment data is obtained, and Art. 17 gives erasure without undue delay | Both articles fetched from the regulation text rather than recalled, before either practice was written | **observed** — the timing claim in BP-213 is the article's, not a paraphrase |
| R-30 | Every `## Contents` anchor in a reference resolves to a heading in that file | `validate_reference_contents`, 150 checks over 21 files; plant: `## FR-04 — Turn the corpus into two lists` renamed **and the copies re-synced**, so only this branch could fire | **planted** — one failure, exactly the renamed anchor |
| R-31 | The plant is keyed to the branch, not to the code arriving | With `for anchor in re.findall(...)` replaced by `for anchor in []`, the same planted rename exits 0 and the count drops 3500 → 3354 | **planted** — standing instruction #5 applied to this run's own check; the deletion is caught by the floor, not by the fixture |
| R-32 | `FR-01..NN` in prose equals the highest FR id in `funnel-research.md` | The range check, in the form `PRN-01..NN` already had; plant: an `FR-08` step appended | **planted** — three carriers went red (README, `practice-selection.md`, `system-map.md`); the two SKILL.md files cite ids individually and correctly did not fire |
| R-33 | `funnel-research.md` reaches `ux-foundation` and `ux-flows` byte-identically, and reaches no other skill | `sync_references.py` then `validate_shipped_references`; both skills moved 10 → 11 contracts, `ux-scenarios` stayed at 10 | **observed** |
| R-34 | The five practices are reachable by the selection protocol rather than only present in the catalog | Two Step-2 rows and four Step-3 rows in `practice-selection.md` | never — the protocol is doctrine an agent reads, and `validate.py` can confirm only that the rows exist. The same limit `R-14` records for the reference sweep |

## 2026-08-14 — the rhetorical dash and the full-stopped title, v0.39.0

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-16 | `B062` errors on a dash before a coordinating conjunction | Fixture "a dash introduces a conjunction, where strict is off"; plant: `conj = DASH_CONJ_RE.search(...)` → `conj = None` | **planted** |
| R-17 | `B062` errors on paired dashes bracketing an aside | Fixture "a pair of dashes brackets an aside, where strict is off"; plant: `if bare >= 2:` → `if False:` | **planted** |
| R-18 | `B062` errors on every non-range dash where the locale has no grammatical one | Fixture "a lone dash where the locale has no grammatical dash"; plant: `if strict and bare > 0:` → `if False:` | **planted** |
| R-19 | The Russian copula, direct speech and numeric ranges are never findings | Three negative fixtures; plants: `COPULA_LOCALES = ()` with a never-matching `CYRILLIC_RE`, and a never-matching `DASH_RANGE_RE` | **planted** |
| R-20 | A dash inside a fenced block is code, not prose | Fixture "a dash inside a fenced block is code, not prose"; plant: the fence `re.sub` replaced by `pass` | **planted**, see the note below |
| R-21 | `B063` errors on a title or heading ending in a full stop, and spares `?`, `…` and abbreviations | Two positive fixtures, one negative; plant: `return not ABBREVIATION_RE.search(text)` → `return True` | **planted** |
| R-22 | Every marker carries an id, so coverage over the set is computable | The `AT-01`..`AT-15` table in `ai-tells.md`, each row naming its checker | never, nothing counts ids against the prose yet; filed as B-016 |
| R-23 | The rule reaches a project through the Brand voice hard rule, in all three carriers | `validate_hard_rule_copies` went red on the template edit before the carrier was re-copied, and green after | **observed**, it caught this run's own divergence |
| R-24 | This project's own chain and brand pack are gated in CI | Two new workflow steps. `docs/brand/lint.py` was red on `B030` before this run and nothing reported it | **observed**, the absence is the defect it was added for |
| R-25 | `B005` dates `foundation.md` by its commit, not by its mtime, and CI checks out full history so the commit is there to read | Fixture `git_date_beats_mtime`; plant: the `git log` branch of `content_date` replaced by `pass`, falling back to mtime | **planted**, and **observed** first: it turned CI red on the run that added the dogfood step |
| R-26 | A seeded script that has fallen behind its source fails the gate | `validate_seeded_scripts` gains byte equality; plant: two lines appended to `docs/brand/lint.py` | **planted**, and **observed** first: `docs/brand/lint.py` was 227 lines behind `brand_lint.py` for the whole of this run's dogfood |

**Two plants failed to land, and both were fixture defects rather than code
defects.** R-16's first fixture was written in English, where deleting the
conjunction branch still produced `B062` from the strict branch: same code,
different path, and a set comparison cannot tell them apart. Rewritten in
Russian, where strict is off and only the branch under test can emit. R-20's
first fixture used a plain fenced block, and the inline-code stripper happened
to pair the fence markers around the dash and remove it anyway; a lone backtick
inside the fence makes the fence pass load-bearing. Both plants landed after
the rewrite.

This is the class the 2026-08-10 audit found when `B005`, `B054`, `B060` and
`B072` were emitting with no fixture: a fixture can be green for a reason
nobody checked. The difference is that the plant found it here before the
release rather than an audit finding it four versions later.

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

## 2026-08-17 — the growth vocabulary becomes advertised, v0.42.0

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-01 | The pack carried the knowledge and advertised none of it | `grep -roicE` over `plugins/super-ux`: funnel 448, onboarding 499, paywall 493, retention 196, activation 171, referral 100; zero of those words in any `description:` before this release | observed |
| R-02 | The cost was a routing dead zone, not a documentation gap | the umbrella's `node test/route_coverage.js`: 15 of 15 growth prompts reached `[]` | observed |
| R-03 | Which word goes to which skill follows `FR-07`, not convenience | `references/funnel-research.md` FR-07 maps the step chain to `flows.md` and the buyer/after-the-session layer to `foundation.md`; `ux-flows` takes funnel/onboarding/paywall/activation funnel, `ux-foundation` takes user retention/churn | observed |
| R-04 | The bodies already backed both descriptions | `ux-flows` names funnels five times including the ad→landing→quiz→offer→paywall→checkout chain; `ux-foundation` line 31 defines a journey as before, during **and after** the product | observed |
| R-05 | Bare English stems were tried and measured, then narrowed | with bare `activation`/`retention` the umbrella matcher stemmed to `activat-`/`retent-` and routed `activate the virtualenv`, `activate the feature flag` and `retention policy for logs` to `/ux`; as `activation funnel` and `user retention` all three go silent and every growth prompt still routes | planted — the noise cases were driven through the real matcher before and after the narrowing |
| R-06 | The Russian half stays bare, deliberately | «активация» and «ретеншн» carry no second trade in this vocabulary; both still match their inflected forms («активацию», «ретеншн») through the umbrella's stemmer | observed |
| R-07 | Budget spent and budget left | `ux-flows` 592 → 884 chars, `ux-foundation` 401 → 619; the 970 working limit holds with 86 and 351 free | observed |
| R-08 | The gate is green | `python3 test/validate.py` → `OK (3500 checks)`; `npm test` exit 0 across all four suites | observed |
| R-09 | The advertised trigger list matches what is advertised | the `Triggers -` lists were corrected to `"activation funnel"` and `"user retention"` in the same edit that changed the prose, so the description does not advertise one word and list another | observed |

**Rows at `never`: 0.**

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
