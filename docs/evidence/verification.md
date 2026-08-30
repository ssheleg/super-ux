# Verification ledger — super-ux

One row per shipped requirement, and the answer to a single question: **has
anyone watched this check fail?** A green from a check nobody has seen go red
against a planted defect is not evidence — it is an untested assertion with a
tick beside it.

`Watched` values: `planted` (a defect was introduced and the check caught it,
in this run), `observed` (it caught a real defect at some point), `never`.

## 2026-08-31 — the board goes to zero, v0.52.0

Eleven rows, each closed with a mechanism and at least one watched plant. The
plant transcripts live on the board rows themselves rather than being copied
here; this section records what shipped and what could not be watched.

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-84 | `strings.md` gains `Kind: copy \| layout`; `layout` is registered and exempt from the language rules; `B065` refuses an out-of-enum kind (`B-029`) | The isolation pair: one row, one banned word, differing only in `Kind` — `layout` silent, `copy` emits `B010`. Plants: the skip removed → the layout fixture red; `STRING_KINDS` widened → the fixture **and** the contract-parity gate. `docs/brand/lint.py` moved from a permanent warning to `brand pack is clean` | **planted** |
| R-85 | A `Coverage:` citation may name its subject; `U078` resolves it (`B-028`) | Plant on the drift the row describes: `338-399` → `223-284` gave `U078 … as covering \`selectInteractive (found at line 338)\``, while `U071` stayed silent on the same edit. Three fixtures: outside the span, inside it, and the old form with no subject | **planted**, and **observed** — the drift was live for a release |
| R-86 | `B005` dates the cited entries, not the file (`B-023`) | Measured on this repository: whole file 2026-08-20, `P-01,P-02` 2026-08-10, `JTBD-01..03` 2026-08-20, an unknown id falling back with `exact=False`. The message names which question it answered | **observed** — the false positive it removes was recorded on SU-02 |
| R-87 | `U076` names a vision that is still the seeded template (`B-005`) | Three states walked: the pristine seed warns, one written section silences it, this pack's own written vision is silent. The placeholder pass was found by watching the check **not** fire on the document it was written for | **planted** |
| R-88 | `VISION_RULE_TEXT` in the seeded linter, `U077` in target projects, `validate_vision_rule_embed` over the third copy (`B-001`) | Plants on both: a rule softened by hand in a target `CLAUDE.md` → `U077`; the embed edited → `ux_lint.py's VISION_RULE_TEXT differs from templates/vision-rule.md` | **planted** |
| R-89 | `validate_audit_scope_enum` over four homes (`B-030`) | Plants in both directions, each with its own message: the scope dropped from step 1, and dropped from the `argument-hint` | **planted** |
| R-90 | `AT-06-E1..E4`, and the arrow from a named exemption to a negative fixture (`B-031`) | Plants both ways: a fixture losing its id, and an exemption renumbered | **planted** |
| R-91 | `test/evals/` — four cases, a runner, and `validate_eval_cases` over their shape (`B-032`) | Plant: `**The humanization pass runs last**` reworded in the skill → `EV-03: the anchor … no longer appears`. The runner refuses to report a pass when the `claude` CLI is absent, verified by running it | **planted** for the shape. **never** for the behaviour, which is the whole point of the row: what an agent does with an instruction is read by a person, not by CI |
| R-92 | The reverse routing arrow in `validate_bp_index` (`B-021`) | Plant: `BP-999` in a routing row → `the row sends a profile at nothing`. The forward arrow this row asked for was already present, proved by planting a well-formed `BP-242`, and the duplicate written here was deleted rather than shipped | **planted** |
| R-93 | The report prints each distinct failure once and names duplicate emissions (`B-019`) | Four probes found no duplicate: both hard rules, each from both sides. Plant: `HARD_RULES` doubled → `note: 1 duplicate emission(s); a check is firing twice for one defect` | **planted** |
| R-94 | The code graph refreshed, and `validate_graph_claims` over what its labels assert (`B-022`) | The refresh ran unattended and is recorded on the board row. Plant: a node relabelled `99 practices` → refused. The gate is narrowed to `label`/`norm_label`, and that narrowing was forced by a false positive it produced first — a node quoting `181 practices against a catalog of 206`, which is history and true | **planted**, and the false positive is why the narrowing is there |

**Rows at `never`: 1 in this section** (R-91, the behaviour half), and it is the
row's own subject rather than an omission: an eval that runs an agent cannot be
a required check without making the gate paid and flaky.

## 2026-08-30 — humanization stops being a mode, and the assembly layer arrives, v0.52.0

Same release as the block below; both shipped in one tag. This half answers the
operator's two asks: humanization on by default and visible, and the structural
layer above the 241 tactical practices.

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-76 | **Humanization is a default, not a mode.** Write, Edit and Adapt each end in the sweep; `Humanize` survives as the standalone mode for auditing text nobody is writing. Position is load-bearing: last in Edit, because the seven sweeps rewrite whole sentences and a pass run before them is measured against text that no longer exists; per surface in Adapt, because a marker density fine in a blog post is not fine in a landing hero | Read against the skill's own modes: the sweep is a numbered step in `Write`, a named paragraph in `Edit` and `Adapt`, and the Definition of done requires the status line. Doctrine only, no gate: `B064` checks the recorded state, not that an agent obeyed the instruction, and that is said out loud rather than claimed | **never** — an instruction an agent follows, filed as `B-032` |
| R-77 | **Two fields for the two questions the old one conflated.** `Humanization: on \| off` is whether the pass runs (absent = `on`); `Humanization pass:` names the implementation (absent = `own`). Declared in `brand-contract.md`, seeded by `templates/brand/voice.md`, recorded in this pack's own `voice.md` | Observed before the change: `grep -rn "Humanization" ` found the field in `templates/brand/voice.md` and **nowhere else** — absent from `brand-contract.md`, absent from `docs/brand/voice.md`, and read by no code in `brand_lint.py`. `validate_brand_contract_fields` now holds the other direction: every `header_field` read must be a field the contract defines, so removing the declaration goes red | **planted**, via the enum-parity plant below, and **observed** — the field was inert for releases |
| R-78 | **`B064` refuses the three defective states**: absent field warns that the default applies unrecorded, an out-of-enum value errors, `off` with no `Humanization declined:` reason errors | Three plants, each reverted, each landing on its own fixture and nothing else: the absent branch re-coded to `B999` → `FAIL: no Humanization field, so the default applies unrecorded: expected ['B064'], got ['B999']`; the enum branch disabled → `FAIL: an out-of-enum Humanization value leaves the pass in neither state: expected ['B064'], got []`; the reason branch disabled → `FAIL: Humanization off with no recorded reason: expected ['B064'], got []`. Each fixture sits in the only state where its own branch can fire, per standing instruction #5. A fourth fixture proves `off` **with** a reason is silent | **planted** |
| R-79 | **The state is visible in four places**: `voice.md`, the status line every copy delivery prints, the `/ux` and `/brand` status blocks, and `B064` | `grep` over the four homes; the two commands carry it in both their inspect step and their status-report step, so a status table cannot omit what the inspect step collected. The status line is specified with both its forms written out in `copywriting/SKILL.md` | **never** for the printed line — it is an instruction, not a check; same `B-032` |
| R-80 | **The `Humanization` enum is inside the parity mechanism from the day it was written.** `DOC_ENUM_DECL_RE` generalised past its hardcoded `**Status**` so any document-level enum is compared, and `HUMANIZATION_MODES` is read out of `brand_lint.py` with `ast` rather than restated | Plant, reverted: `HUMANIZATION_MODES` changed to `("on", "off", "auto")` → `FAIL: voice.md Humanization: brand_lint.py matches ['auto', 'off', 'on'] and brand-contract.md declares ['off', 'on']`, exit 1. This is `SU-02`'s defect refused in advance rather than after it shipped | **planted** |
| R-81 | **`header_field` ends a value at an aligned comment.** Two spaces or more before a `#`; one space does not, so `Humanization declined: per ticket #431` keeps its reason | Observed: standing instruction #3 fired on the first run against a freshly seeded pack — `ERROR B064 voice.md:1: 'Humanization: on                    # on \| off; on is the default...' is not one of on \| off`, exit 2. After the fix the seeded pack returns `brand pack is clean`, exit 0. Two fixtures added, one for each side of the two-space discriminator | **planted**, and **observed** on the seed |
| R-82 | **Three references give the pack its assembly layer**: `onboarding.md` (`ON-01..ON-18`, ux-flows), `internal-screens.md` (`IS-01..IS-18`, ux-flows), `product-frameworks.md` (`PF-01..PF-12`, ux-foundation) | The gap was measured, not assumed: word-boundary `grep` over every skill for twelve named frameworks returned **zero** for Hook, Fogg, Kano, opportunity solution tree, AARRR, north star, time to value, value proposition canvas, forces of progress, switch interview, service blueprint and double diamond. `RICE` and `ICE` first appeared to be present at 30 and 94 files and were false positives inside `practice`, `notice` and `service`, which is why the second pass used `grep -w`. Shipping footprint enumerated after sync: each file reaches its own skill and no other | **planted**, through the coverage gate below |
| R-83 | **One coverage gate over four id sets.** `validate_doctrine_set_coverage` is parameterised over `LP`, `ON`, `IS`, `PF`; `check_id_set_coverage` and `check_reference_is_linked` are the shared halves | The four plants recorded for `LP` in the section below all run through the same code path now. Re-verified after the refactor against `ON`: the `### ON-09.` section deleted → `FAIL: onboarding.md: ON-09 has a table row and no ### ON-09. section`, exit 1, reverted | **planted** |

**Rows at `never`: 2 in this section** (R-76, R-79), both filed as `B-032`, and
both of the same kind: an instruction an agent reads rather than a check a gate
runs. Named rather than dressed up as coverage.

## 2026-08-30 — the dash rule stops checking the glyph, v0.52.0

Two blocks: a verified defect in `B062` found by reading a live page, and the
landing-page layer the pack did not have. Evidence base: three teardowns in
`docs/research/landings/`, read 2026-08-30.

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-72 | **`B062` judges the dash's role, not its codepoint.** `normalise_dash_spelling` reduces the em dash, the en dash and a hyphen with a space each side to one mark before the three existing branches judge it; the substitutions are length-preserving so the finding quotes the author's own characters | Watched failing first: the battery of 17 cases ran against the unmodified source at 12/17, the four glyph-escape cases silent. Plants against the fixed source, each reverted: the hyphen substitution deleted → `FAIL: a hyphen with a space each side is the same mark: expected ['B062'], got []` **and** `FAIL: a spaced hyphen introduces a conjunction, where strict is off`, exit 1; the alias substitution neutered → `FAIL: an en dash is the same mark`, exit 1. Fixtures written per standing instruction #5, in conditions where only the branch under test can fire: none carries an em dash, so deleting the normaliser leaves no dash for any branch to find. Origin measured in the wild: trycomp.ai, 20 rhetorical dashes, 0 em dashes | **planted**, and **observed** in the wild before it was written |
| R-73 | **A dash alone in a table cell is an empty string.** `TABLE_CELL_DASH_RE` blanks it before judgement, which is the allowance `AT-06` has listed among the grammatical exemptions since it was written and nothing implemented | Observed against the unmodified source: `\| landing \| — \|` in a strict locale returned a `B062` finding, so the doctrine and the code disagreed and only the doctrine said so. Plant against the fix, reverted: the table-cell substitution deleted → `FAIL: a dash alone in a table cell is an empty string, not punctuation: expected [], got ['B062']`, exit 1 | **planted**, and **observed** — the gap was live |
| R-74 | **`landing-pages.md` ships into `copywriting` and nowhere else, and its 20 ids are covered.** `validate_landing_coverage` checks rows against sections in both directions, duplicates, sequence gaps, an id the readiness check names that no section defines, and the `SKILL.md` link | Shipping footprint enumerated after sync: `find . -name landing-pages.md` returns the source and the `copywriting` copy only — `system-map.md` names the file in backticks and links it nowhere, which is why it did not travel into the four UX skills. Four plants, each reverted: `### LP-12.` deleted → `FAIL: LP-12 has a table row and no ### LP-12. section`, exit 1; `LP-07` renumbered to `LP-27` → `FAIL: the rule set is [1..20, 27] … a gap means a rule was deleted rather than retired`, exit 1; the readiness check repointed at `LP-44` → `FAIL: the readiness check names LP-44 and no section defines it`, exit 1; the `SKILL.md` row removed → `FAIL: copywriting/SKILL.md does not link references/landing-pages.md`, exit 1 | **planted** |
| R-75 | **A cited teardown resolves or the gate refuses.** The linter's own comment and the playbook cite `docs/research/landings/*.md`; nothing else watches those paths | Plant, reverted: `docs/research/landings/trycomp.md` moved aside → `FAIL: docs/research/landings/trycomp.md is cited and does not exist -- a claim that reads as sourced and is not`, exit 1. The gate also refuses when nothing cites the folder at all, so deleting the citations rather than the files does not satisfy it | **planted** |

**Rows at `never`: 0 in this section.**

The playbook itself makes a claim no gate can check, and it is stated in the
file rather than left implied: three pages is enough to notice a repeated
defect and not enough to generalise, so the repeats are named as repeats and
the single-page observations stay attributed to their one page.

## 2026-08-30 — the templates ship where the texts say they are, v0.50.0

Wave-2 close of the 2026-08-29 family audit's SUX-01/06/07/08/11 (SUX-03 was
cancelled by operator decision — no renames anywhere; SUX-02/05 are wave 3,
SUX-04 is evals day, SUX-09/10 closed in wave 0).

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-68 | **Every template a shipped text seeds from travels with what ships.** `sync_references.py` mirrors `templates/` (source of truth, unchanged) into `plugins/super-ux/templates/` and the named seeds into each seeding skill's own directory — brand-voice gets `templates/brand/` (7 files), ux-scenarios and ux-foundation their single seed; `validate_shipped_templates` refuses drift and strays in both homes | Observed at v0.49.1: all six seeding texts pointed at a path absent from every installed channel — `find` over the 13 cached plugin versions returned no `templates/` (family audit SUX-01) — while `validate.py` printed `OK (4111 checks)`, because every gate resolved paths against the repo root. Plants against the new gate, each reverted: plugin copy drifted → `FAIL: … has drifted from templates/scenarios.md`, exit 1; stray `extra.md` → `FAIL: … a copy with no source is a fork`, exit 1; plugin copy deleted → `FAIL: … missing from the shipped plugin`, exit 1; skill copy drifted → `FAIL: brand-voice/templates/brand/voice.md has drifted`, exit 1. Sync verified idempotent: three consecutive runs, `0 file(s) written/removed` on the second and third | **planted**, and **observed** — the dead path was live in every shipped channel |
| R-69 | **The class is gated, not the instance:** `validate_shipped_paths` requires every backticked `templates/…`/`scripts/…` token in a shipped text to resolve inside what ships — plugin root for commands, the skill's own directory for skill files, the same rule `validate_shipped_references` enforces for contracts | Plants, each reverted: the ux-scenarios seed deleted from the skill dir → `FAIL: … names \`templates/scenarios.md\`, which does not resolve inside what ships — skill 'ux-scenarios' ships its own directory and nothing else`, exit 1; a command repointed at `templates/missing-dir/` → `FAIL: … the plugin ships plugins/super-ux/ and nothing above it`, exit 1. All 11 live tokens enumerated and resolving; the `plugins/super-ux/scripts/bp_index.py` developer notes inside contracts are outside the pattern by anchor, verified by the same enumeration | **planted** |
| R-70 | **`/ux-audit` names its whole scope surface**: `copy` and `benchmark:<competitor>` in the `argument-hint` and in the step-1 enumeration, and the single-pass list carries both | Read against the body's own scope sections (`## Copy scope (\`copy\`)`, `## Benchmark scope (\`benchmark:<competitor>\`)`), which treated both as legal since they shipped. No gate compares the three homes of this enum; that class is filed as `B-030` rather than claimed covered | **never** — a text alignment with no gate, said out loud; the gate is board row `B-030` |
| R-71 | **Three descriptions stop over-claiming and every routed trigger survives**: ux-scenarios defers the empty-project start to vision/ux-foundation in the trigger itself; copywriting narrows the landing-page phrase to the copy, naming sheleg-design; ux-flows drops bare "figma"/"фигма" and delegates the visual system and Figma variables to sheleg-design | Budgets measured after the edits: 486 / 634 / 983 of 1024, `check_description_canon` green. The umbrella's own checker run directly (`node ../sshlg-skills/test/advertised_check.js --member super-ux --root .`): `ok: super-ux advertises all 43 routed trigger(s) across 3 skill(s)`, exit 0 — and watched failing against a planted drop of «мокап»: exit 1, `the family's routing hook fires on 1 word(s) super-ux no longer advertises`, reverted | **planted**, and the B-54 class checker did the watching |

**Rows at `never`: 1 in this section** (R-70), filed as `B-030`.

## 2026-08-20 — the checks that were measuring the wrong thing, SU-04

Thirteen defects, all measured in this tree at `cc4c3eb` (the v0.45.0 tree) and
every one of them reproduced before it was touched. **Observed at** below names
the tree the plant was run against; where a plant is a branch mutation, it names
the guard that was disabled.

The class they share is not "a missing check". Eleven of the thirteen were checks
that ran, passed, and measured something adjacent to what they claimed: a
substring instead of a value, a path instead of a citation, a front-matter block
instead of two fields, a colon instead of an id, three prefixes instead of eight
layers. A gate that measures the wrong quantity is indistinguishable from a gate
that holds, which is why every row here carries the exit code of the run that
saw it fail.

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-51 | **`B030` compares a public figure against each fact's `Value`, exactly.** `_fact_figures()` normalises one value at a time (whitespace out, a bound marker like `500+` stripped, plus whatever `NUMBER_RE` reads inside it) and the corpus is a `set`, not a string | Observed at `cc4c3eb`: appending *"super-ux is used by 58 teams and ships 1582 checks."* to `README.md` left `python3 docs/brand/lint.py` printing `brand pack is clean`, **exit 0** — because `known` was `" ".join(values).replace(" ", "")` = `7158215243770+` and `1582` is a substring of it. Against the fix: `ERROR B030 README.md:0 … 1582 … no row in facts.md`, and `215`, a real row, still passes. Four fixtures in `brand_lint_test.py` (a substring of one value, a figure spanning two adjacent values, each value on its own, a `500+` bound). Branch plant: the original expression restored verbatim → `FAIL: a figure spanning two adjacent values is not sourced either: expected ['B030'], got []`, exit 1 | **planted**, and **observed** — the invented number was live in the tree for the length of one command |
| R-52 | **`B033` refuses two rows under one `Fact` name.** `facts()` appended every row with no uniqueness test at all | Observed at `cc4c3eb`: a second `\| skills shipped \| 99 \| … \|` row left the pack clean **and** put `99` into the sourced corpus, so the duplicate did not merely go unreported, it licensed a figure nobody had agreed. Against the fix: `ERROR B033 facts.md:0 … has 2 rows`, and `995` in copy is still refused. Three fixtures (duplicate, duplicate differing only in case, distinct names). Branch plant `if count > 1:` → `if False:` → exit 1 | **planted** |
| R-53 | **Every row in `facts.md` is what its own `Source` command returns.** `validate_facts_recompute` runs each one; the self-referential row runs `python3 test/validate.py` as a child under `SUPER_UX_FACTS_RECOMPUTE_CHILD=1`, which skips the recomputation and **not** the counting, so parent and child print the same total; the one row an external registry owns is marked `not recomputable here:` and **disclosed** (`unlooked: …`), never counted as a pass | Observed at `cc4c3eb`: the file had claimed "every row below names a command that recomputes it" for four releases and nothing ran one — two rows named no command at all, and `repo validator checks` read **3500 against a measured 3539**. The stale row is `Public: no`, so no `B030` could ever have pointed at it. Plants: a `Source` stripped of its backticked command → `FAIL … names no runnable command in its Source`, exit 1; `skills shipped` set to 8 → `FAIL … records '8' and its own Source command returns '7'`, exit 1; the `not recomputable here:` marker removed → `FAIL … names no runnable command`, exit 1 | **planted**, and **observed** — one live row was wrong by 39 |
| R-54 | **A `Coverage:` citation resolves its line range, not just its path.** `coverage_claim` returns a third answer, and `U071`/`U072` refuse a span the file does not have (out of bounds, single line past EOF, and a range that ends before it starts) | Observed at `cc4c3eb`: `bin/super-ux.js:99000-99999` on `SCR-01` in a **396-line** file left `python3 docs/ux/lint.py` printing `OK — docs/ux is consistent`, exit 0. Against the fix: `ERROR: [U071] … the file resolves and those lines do not`, exit 1. Seven fixtures across both layers. Branch plant `if first < 1 or last < first or last > total:` → `if False:` → exit 1, exactly four cases red | **planted**, and **observed** — the live drift underneath is R-55's other half |
| R-55 | **The seven pre-shift coverage ranges in `screens.md` name the code they claim.** 14 citations rewritten (7 entries + 7 index rows), each verified against `bin/super-ux.js` and against `scenarios.md`, which already had the same functions right | Observed at `cc4c3eb`: `screens.md:49` cited `bin/super-ux.js:223-284` while `selectInteractive` occupied **235-296**, and `scenarios.md:52` cited 235-296 — two layers of one chain disagreeing in writing with nothing comparing them. All seven were shifted by the same edit: `selectFallback` 286-294 → 298-306, the cursor-dir prompt 322-326 → 334-338, `installCursor` 51-135 → 54-147, `installSkillsCli` 143-147 → 155-159, `installClaudePlugin` 149-166 → 161-178, `usage` 27-44 → 27-47. **The bounds check cannot catch this class** — 284 is inside a 396-line file — so it is recorded as a limitation, not as a gate | **observed** — found by resolving every citation by hand, and it stays findable only that way until a citation names its symbol (board row) |
| R-56 | **The job layer is visible to every rule.** `_entry_header_re` matches an entry by its **id**, not by the colon after it; `U073` then refuses a header with no name, and `U074` asks a job for `Statement`, `Personas`, `Type`, `Forces`, `Success metric` | Observed at `cc4c3eb`: this repo's three jobs are `### JTBD-01` with no name, so `ids()` and `entry_blocks()` matched **zero** of them — two identical `### JTBD-01` headers passed the whole gate, exit 0, and the missing `Success metric` on all three could not be reported because the layer could not be seen. Against the fix, the duplicate gives `ERROR: [U001] foundation.md/jobs: duplicate id JTBD-01 (2 entries)`, exit 1. Twelve fixtures — the header check covers every entry layer, not only the foundation ones, because the invisibility was never specific to jobs. Branch plants: the colon restored in the matcher → exit 1, four cases; `if colon and title:` → `if True:` → exit 1, three cases; the field loop disabled → exit 1, two cases | **planted**, and **observed** — three live jobs and one live duplicate-id blind spot |
| R-57 | **This repo's three jobs meet the contract.** Each carries a name, all five fields, and a `Success metric` that is a user outcome rather than a feature | `python3 docs/ux/lint.py` → exit 0 with `U073`/`U074` live. The statements and forces are the operator's original wording, restructured into the contract's fields; the metrics are new and are stated as things that stop happening to a person, which is what the contract asks for | **observed** |
| R-58 | **A `Status` the contract does not declare is refused on every layer that carries one.** `P` and `JTBD` get the enum they were already using (`proposed \| confirmed \| retired`); `vision.md` gets its document-level enum; `FLW` and `JRN` are declared to have **none**, and `U075` refuses one there; `B034` does the same for `voice.md` | Observed at `cc4c3eb`: **nine** live `Status:` values sat outside every enum — `confirmed` on four flows (`flows.md:29,55,75,101`) and on two personas and three jobs (`foundation.md:19,25,35,42,49`) — because `ENUM_DECL_RE` accepted `SCN\|ST\|SCR` only. Same class in the brand pack: `voice.md:6` read `approved` where `brand-contract.md` declares `draft \| validated`, and it worked only because every read asks `== "draft"`. Against the fix: four `U075` errors on the flows, exit 1. Fixes: the four flow statuses removed with the reason recorded in `flows.md`, `voice.md` moved to `validated` per the contract's own lifecycle sentence. Eleven fixtures (eight in `ux_lint_test.py`, three in `brand_lint_test.py`). Branch plants: the `U075` guard inverted → exit 1, three cases; `B034` disabled → exit 1; `"P"` dropped from `STATUS_ENUMS` → `FAIL: P Status: … one side moved alone` | **planted**, and **observed** — nine live values, and the parity check that was passing over all of them |
| R-59 | **The enum parity check reaches every layer, in three declaration forms.** `ENUM_DECL_RE` now spans `SCN\|ST\|SCR\|P\|JTBD`; `DOC_ENUM_DECL_RE` reads the document-level layers out of **both** contracts; the statusless pair is read from the contract's own sentence, and declaring an enum for either of them fails | Plants from both directions: `"P"` removed from the linter's table → `FAIL`, exit 1; `copywriting` removed from a rule → two guards fire at once. `VOICE_STATUSES` is read out of `brand_lint.py` with `ast`, so the brand layer is inside the mechanism instead of beside it | **planted** |
| R-60 | **The Cursor umbrella routes to everything the pack ships,** and `validate_skill_parity` asks for each skill by name in it | Observed at `cc4c3eb`: `cursor/rules/super-ux.mdc:29-41` named four workflows against **eight** `.mdc` files shipped, and `grep -c` returned **0** for `vision`, `brand-voice` and `copywriting` — three rule files nothing routed to, for three releases, on the one channel where a rule that is never named is a rule that is never loaded. Against the fix, removing `copywriting` from the umbrella gives two failures at once: `does not name \`copywriting\`` from the reachability check and `its 'UX scenarios — hard rule' copy does not name \`copywriting\`` from the anchor check, exit 1 | **planted**, and **observed** |
| R-61 | **Every live copy of a hard rule names everything its source names.** `HARD_RULE_HOMES` lists the copies `HARD_RULES` cannot pair byte for byte, the anchors are **derived** from the template section (backticked tokens plus space-free bolded ones), and an exemption is data with its reason beside it | Observed at `cc4c3eb`: the `UX scenarios` rule has four payload homes and `HARD_RULES` pairs two. Measured — `templates/claude-rule.md` 320 words / 2102 chars, `CLAUDE.md:68` 349 / 2284, `cursor/rules/super-ux.mdc:6` 348 / 2204. Byte equality is the wrong test for the two that are not the carrier: `CLAUDE.md` diverges by choice and its wording is the better one. Plant: `docs/ux/flows.md` deleted from `CLAUDE.md`'s copy → `FAIL: CLAUDE.md: its 'UX scenarios — hard rule (super-ux)' copy does not name \`docs/ux/flows.md\``, exit 1. The one exemption is `/ux` on the Cursor copy, because Cursor has no slash commands | **planted** |
| R-62 | **The `AT-` marker set has a coverage gate, in both directions.** `validate_ai_tell_coverage` matches table rows against `### AT-NN.` sections and refuses a gap in the sequence | Observed at `cc4c3eb`: deleting the whole `### AT-15.` section while leaving its row at `:66` — with the two mirrored copies re-synced, so nothing else could take the credit — kept `python3 test/validate.py` at **`OK (3539 checks)`, exit 0**. Against the check: `FAIL: ai-tells.md: AT-15 has a table row and no \`### AT-15.\` section`, exit 1. The other direction planted too: the row deleted, the section left → `FAIL: … has a section and no table row`, exit 1 | **planted** |
| R-63 | **The board's ids are unique, and a `B-` id the ledger cites resolves to one row.** `validate_board_ids` reads the first cell of every row in either table | Observed at `cc4c3eb`: `B-011`, `B-012` and `B-013` each appeared in **both** tables with different content — `FAIL: … B-011 appears 2 times`, three of them, exit 1 — and nothing read the board at all. The three open rows were renumbered to `B-025`..`B-027` (the board's own `B-016` had specified that direction; the Closed rows are cited by `CHANGELOG.md:690,720`, a dated record this repository does not rewrite), each keeping a pointer to its old id. `R-22` cited `B-016` for the `AT-` gap where the board files it as `B-017`; fixed and the row closed. Plants: `B-023` renamed to `B-024` → exit 1; this row's `Filed as B-017` pointed at an id the board does not carry → `FAIL: … cites B-0xx, which is not a row on the board`, exit 1 (the plant used a three-digit id that does not exist; it is not written here, because a document that names a dead id is the thing this guard refuses) | **planted**, and **observed** — three live collisions and one live miscitation |
| R-64 | **The front-matter budgets are the two the standard sets:** `name` ≤ 64 and `description` ≤ 1024, each measured on its own field | Observed at `cc4c3eb`: `test/validate.py:66-73` compared the length of the **whole front-matter block** to 1024, so a long name could push a legal description over an imaginary line and a `description` of exactly 1024 passed a limit it was at rather than under. No skill was over either real budget — measured, the widest are `name` 13 and `description` 940 — which is why nothing ever said so. Plants both ways: a description padded to 1452 → `FAIL … \`description\` is 1452 chars, the Agent Skills limit is 1024`, exit 1; a 67-character `name` (with its directory renamed to match, or `name != dirname` answers first) → `FAIL … \`name\` is 67 chars`, exit 1 | **planted** |
| R-65 | **One pack, one meaning for a warning.** `brand_lint.py` takes `--strict`; without it, warnings report and pass, which is the policy `ux_lint.py` has always had | Observed at `cc4c3eb`: `brand_lint.py:1558` returned `1` whenever any finding existed, so 13 of the 39 codes turned `npm test` red while printing `0 error(s), 1 warning(s)`, and `ux_lint.py:716` returned 0 for the same input. Against the fix: `python3 docs/brand/lint.py` → **exit 0** over one live warning, `--strict` → **exit 1**. Reworded in the same change: `README.md`, `commands/brand-lint.md`, `cursor/rules/brand-voice.mdc`, `cursor/rules/copywriting.mdc`, and the brand-linter bullet in all three homes of the hard rule | **planted** |
| R-66 | **The literal extractor crosses a newline.** `TEMPLATE_RE` reads a template literal and `code_literals` yields it a **paragraph** at a time, which is the unit a reader sees; `B021` gains a wrap-tolerant fallback so a wrapped block can be registered at all | Observed at `cc4c3eb`: `LITERAL_RE` used `[^\n]`, so `usage()` at `bin/super-ux.js:27-47` — the most-read UI surface the pack has — was invisible to the registry for as long as the code existed, and `strings.md` recorded it as needing "a per-language extractor". It needed a second pattern. Against the fix, the first run reported 16 lines from inside `usage()`, the top one being `warn B022 bin/super-ux.js:0: "super-ux installer" is in the code with no registry row`. Per line it also produced six mid-sentence fragments no registry row could hold, so the unit is a paragraph; `super-ux installer` is now registered as `help.title`. Two fixtures. Branch plants: the template loop emptied → `FAIL: a string inside a multi-line template literal is swept: expected ['B022'], got []`, exit 1; the `B021` fallback removed → exit 1 | **planted**, and **observed** |
| R-67 | **The code graph's staleness is recorded, not repaired.** `graphify-out` is 11 commits behind and `funnel-research.md` still produces no nodes | Not verified and deliberately not attempted: `graphify . --update` needs semantic extraction for the changed docs, no LLM key is present in this environment, and `--code-only` would answer fewer questions than the stale graph while looking current. The staleness lives in `GRAPH_REPORT.md`'s own header and in board row `B-022`, whose measurement is refreshed to this commit. A graph is believed where a document is argued with, which is why this row says `never` out loud rather than being left off the ledger | **never** — the honest value, and the row exists so the gap is countable |

**Rows at `never`: 1** (R-67, the code graph).

The one finding this run did not close, and why it is written down instead:
`U071`/`U072` resolve whether a citation's lines **exist**, which catches
`99000-99999` in a 396-line file and cannot catch `223-284` in the same file when
the function has moved to 235-296. Bounds are all a range can prove about itself.
Naming the symbol beside the range would make it checkable; that is a contract
change, and it is filed rather than improvised.

## 2026-08-19 — delivery proof stops counting as outcome proof, SU-02 (M-21)

Manifesto M-21: *a change can be implementation-verified and product-unvalidated.
Some outcome evidence cannot exist until after release, so `unobserved` is a
legitimate product state. Pretending delivery proof is outcome proof is not.* The
pack had one state per scenario and an audit wrote it: `ux-audit/SKILL.md:211-212`
flipped `validated` → `implemented` on a PASS, so the chain recorded that the code
does what the scenario said and had **no way at all** to record whether the
scenario was the right thing to build. Measured before the change:

```
git grep -l unobserved fe2189e | wc -l    -> 0
```

Zero files. The state that M-21 calls legitimate did not exist in the vocabulary.

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-42 | `Product: unobserved \| observed \| contradicted` on a scenario and on a story, a state distinct from `Status`, **with no floor and no target** — absence means `unobserved`, `unobserved` fails nothing, and `contradicted` fails nothing either | `PRODUCT_STATES`/`PRODUCT_LAYERS` in `ux_lint.py`; fixtures "U066 silent when the field is absent — absence IS unobserved, and no floor asks" and "U066 clean on `contradicted`, which is information and not a failing gate"; the contract's own section states both non-gates in prose | **observed** — 15 of this pack's 15 scenarios are `implemented` with resolving coverage and `unobserved` on the product axis, and `npm test` exits 0 over that, which is the whole claim |
| R-43 | `U066` refuses a product value outside the enum, and a declared-but-empty field with it — an unrecognised value never reads as *no state* | Three fixtures (out-of-enum on a scenario, empty field, out-of-enum on a story) against four clean twins; plant **in the real chain**: `SCN-001` → `**Product:** verified` gave `ERROR: [U066]`, exit 1; branch plant `if state not in PRODUCT_STATES:` → `if False:` | **planted** — exactly the three U066 cases red, every twin green |
| R-44 | `U067` refuses an outcome claim that names no observation | Two fixtures (`observed`, `contradicted`) against two twins on `unobserved`; plant in the real chain: `**Product:** observed` alone gave `ERROR: [U067]`, exit 1; branch plant `if not stated(signal):` → `if False:` | **planted** — exactly the two U067 cases |
| R-45 | `U068` refuses **delivery proof handed in as an outcome signal**: a `file:line` — line ranges included — an audit verdict, and a path into `docs/ux/audits/` with any amount of prose around it. That is everything an audit produces, and none of it is a user | Six fixtures (citation, citation with a range, two citations, a story doing it, a verdict, the report linked inside a sentence) against two twins (an observation that cites code beside it; the word "passed" in prose). Plants in the real chain: `**Product:** observed — the 2026-08-10 audit came back PASS` → `ERROR: [U068]`, exit 1; `**Product:** observed — \`bin/super-ux.js:235-296\`` → `ERROR: [U068]`, exit 1. Branch plants: the citation guard → `if False:` (exactly four cases), the audit-evidence guard → `if False:` (exactly two); and **pattern-keyed** plants inside `AUDIT_EVIDENCE` — deleting the verdict regex reds exactly the verdict case, deleting the report-path regex reds exactly the report case | **planted** — and the first attempt at the citation plant went CLEAN, see the note below |
| R-46 | No audit can promote the product state, in doctrine as well as in code | `ux-audit/SKILL.md` step 7 is now "the delivery state, and only that" and carries **The audit never writes `Product:`.**; the contract's *After a run* carries the same words; `validate_audit_leaves_product_alone` checks both homes. Plant: the sentence replaced with "Flip `unobserved` -> `observed` where the audit PASSed" → `FAIL`, exit 1, naming the file and the missing words | **planted** |
| R-47 | The long field spelling is canonical, and `U069` says so without touching the question `U060`/`U061` ask | `FIELD_ALIASES` in `ux_lint.py`; two fixtures and two canonical twins; SU-01's four spelling fixtures still pass unchanged. Plant in the real chain: one `**Expected result:**` back to `**Expected:**` → `warn: [U069]`, exit 0 — a warning, deliberately, because an error would fail every project already writing the short form. Branch plant `if alias in body:` → `if False:` | **planted**, and **observed** first — it fired on 22 of 22 live entries the first time it ran (15 scenarios, 7 stories) |
| R-48 | `U070` refuses a `Status:` outside its layer's enum for all three layers that declare one | Three fixtures (scenario, story, screen) against three twins, one of them `blocked`; plant in the real chain: one story back to `**Status:** implemented` → `ERROR: [U070]`, exit 1; branch plant `if status is None or status in allowed:` → `if True:` | **planted**, and **observed** first — it fired on all 7 stories, which had carried the scenario layer's `implemented` since the chain was written |
| R-49 | The contract and the linter hold ONE copy of every enum and fail together | `validate_status_enums_match_contract` parses the contract's declaration list and reads `STATUS_ENUMS`/`PRODUCT_STATES`/`PRODUCT_LAYERS` out of the linter with `ast` — nothing restated. Plants from **both** directions: dropping `"blocked"` from the linter → `FAIL: SCR Status: … one side moved alone`, exit 1; adding `inconclusive` to the contract → `FAIL: SCN Product: …`, exit 1 | **planted**, and **observed** — the drift was live and had never been reported: the contract declared five screen statuses and the matcher listed four, so a `blocked` screen read as having **no** status and `U021` stopped applying to it |
| R-50 | This pack's own chain records the product state honestly | `docs/ux/scenarios.md`: 15 renames to `**Expected result:**`, 15 `**Product:** unobserved`. `docs/ux/foundation.md`: 7 renames to `**Acceptance criteria:**`, 7 statuses `implemented` → `delivered`, 7 `**Product:** unobserved`. `python3 docs/ux/lint.py` → exit 0, and `--strict` → exit 0 as well | **observed** — the answer is `unobserved` for all 15 scenarios and all 7 stories, and that is the correct answer, not a gap |

**Rows at `never`: 0.**

**The citation plant went clean on its first attempt, and that miss is the
reason `U068` works.** `**Product:** observed — \`bin/super-ux.js:235-296\`` — the
exact shape this pack's own chain writes — passed. `CITED_PATH` stops at the
first line number by design (it resolves a path; the range is `B-004`'s open
work), so subtracting what it matched left `-296` behind, and `stated()` read
that as prose. A second miss followed the fix: two citations separated by a
comma left `, ` behind, and `stated()` reads a lone comma as content too. `U068`
now subtracts `CITED_SPAN`, which carries the range, and strips punctuation
before judging the residue — with two fixtures pinning both misses. Standing
instruction #4 from the other side: the plant is what tells you the check is
narrower than its message.

**Standing instruction #5 was designed in rather than learned again.** `U068` has
two branches emitting one code, which is exactly the shape that leaves a suite
green when a branch is deleted. Each fixture is written where only its own branch
can fire — the citation cases leave nothing but paths, so the verdict guard is
false there; the verdict case leaves prose, so the citation guard is false — and
the guards are three disjoint `if`s rather than an `elif` chain for the same
reason. Both branch plants land on exactly their own cases: four, then one.

**What the honest outcome was on the pack's own chain.** All 15 scenarios are
`implemented`, all 15 cite code that resolves (SU-01), and all 15 are
`unobserved`. Nothing about this pack has been measured against a user: there is
no telemetry in the installer, no funnel behind it, and no signal that could move
the field. Recording `unobserved` fifteen times is the deliverable — before this
change the same chain read as fifteen validated bets, because `implemented` was
the only state it had. The seven stories are `delivered` and `unobserved` on the
same grounds.

**The commit itself turned a second gate red, and the re-stamp is recorded
rather than quiet.** `docs/brand/lint.py` was clean before the commit and exited 1
after it: `B005` compares `Last calibrated` in `voice.md` against the *content
date* of `foundation.md`, and `content_date` reads git, so the sweep's own commit
moved the date. The calibration was then actually performed rather than assumed —
`voice.md` declares `Derived-from: P-01, P-02, JTBD-01..03`, and the diff shows
every hunk at line 99 or lower against a `## User stories` heading at line 93,
with **zero** changed lines mentioning `P-0`, `JTBD-` or `JRN-`:

```
git diff -U0 HEAD~1 -- docs/ux/foundation.md | grep "^@@"          -> all >= 99
git diff HEAD~1 -- docs/ux/foundation.md | grep -cE "P-0|JTBD-|JRN-" -> 0
```

Nothing the voice derives from moved, so `Last calibrated` is stamped
`2026-08-19` on that reading and not on the calendar. The granularity defect it
exposed is filed as `B-023`: `B004` checks the `Derived-from` **entities** and
`B005` checks the **file**, so any edit anywhere raises a warning about a trace
that is intact — and a warning whose only remedy is a re-stamp is one people
learn to re-stamp past.

**One more instance of the row's own class, filed rather than fixed.** Looking for
`Status` enums to put in the table turned up a third: `brand-contract.md:117`
declares `draft | validated` and `docs/brand/voice.md:6` says `approved`.
`brand_lint.py` only ever compares against `draft` (lines 189, 238), so the value
behaves like `validated` today and would read as **not** validated the moment a
check tests for the value instead. Filed as `B-024` and not fixed here, because
choosing between adding `approved` to the contract and moving the pack to
`validated` is a decision about the brand pack, not a rename SU-02 gets to make.

**Where the boundary with `SU-03` was drawn.** M-21 asks that the hypothesis, its
success signal and its evidence state stay explicit. SU-02 owns **the evidence
state** — the field, its enum, and the refusals that keep an audit out of it —
and, where a state claims evidence, the signal on that line. It does **not** touch
the `JTBD-NN` layer: the three jobs still carry no `Success metric` and their
headers still lack the `: <name>` that would make them visible to `ids()` and
`entry_blocks()`, which is SU-03 exactly as filed. The line is that SU-02 makes a
missing outcome *sayable* at the layers the linter can already read, and SU-03
makes the layer above them readable at all. Doing SU-03's half here would have
meant changing `ids()` under a row that had not asked for it.

## 2026-08-19 — the requirement layer gets its observable, SU-01 (M-17)

Manifesto M-17: *a requirement with no observable is unfinished, because you
cannot connect it to the evidence graph later without inventing the test after
seeing the implementation.* The layer that defines the requirement had the rule
in prose and no mechanism: before this change `plugins/super-ux/scripts/ux_lint.py`
contained the strings `Expected` and `Acceptance criteria` **zero** times
(`git show a8640b1:plugins/super-ux/scripts/ux_lint.py | grep -c "Expected\|Acceptance
criteria"` → 0) and never read a scenario or
story body. The screens layer one level below had had exactly this check since
`U055`/`U056`.

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-35 | `U060` refuses a scenario past `draft` that states no observable result, and treats a `<placeholder>` as no answer | Fixtures "U060 an implemented scenario that states no observable" and "U060 a placeholder standing in for an observable", against four negative twins (long spelling, short spelling, `draft`, `retired`); plant: `if not stated(field_body(body, SCENARIO_OBSERVABLE)):` → `if False:` | **planted** — exactly the two U060 cases red, every twin still green |
| R-36 | `U061` refuses a story past `proposed` that states no acceptance criteria, including a label with nothing under it | Fixtures "U061 a story that states no acceptance criteria" and "U061 an acceptance field with nothing under it"; plant: `if not stated(criteria):` → `if False:` | **planted** — exactly the two U061 cases; see the note below, the first attempt at this plant did not land |
| R-37 | `U062` warns when acceptance criteria name no outcome, and accepts the `Given …, then …` compression this pack writes | Fixture "U062 acceptance criteria that state no observable outcome" plus its negative twin; plant: `elif not re.search(r"\bthen\b", …)` → `elif False:` | **planted** — one case |
| R-38 | `U063` warns when a scenario claims `implemented` and names no code | Fixture "U063 an implemented scenario naming no code" plus two twins; plant: `if status == "implemented" and (not cov or …)` → `if False:` | **planted**, and **observed** first — it fired on 15 of this pack's own 15 scenarios the first time it ran |
| R-39 | `U064`/`U065` hold a scenario's `Coverage` to the same standard as a screen's: name a file, and the file resolves | Fixtures for both, with `none`-and-no-file twins; plants: `if unfalsifiable:` → `if False:` (one case), `for rel in missing:` → `for rel in []:` (one case), and `missing = []` inside `coverage_claim` — which turns **U056 and U065** red together, which is the evidence that the two layers share one owner rather than two copies | **planted** |
| R-40 | This pack's own 15 scenarios cite the implementing code they were measured against, and the citations are re-resolved by the gate | `python3 docs/ux/lint.py` → exit 0, `OK — docs/ux is consistent`; plants **in the real chain**: `SCN-001` coverage → `bin/gone.js:1` gave `ERROR: [U065] … which does not exist`, exit 1; deleting `SCN-001`'s `**Expected:**` gave `ERROR: [U060]`, exit 1; a prose claim `full — the list is built` gave `warn: [U064]`, exit 0 as a warning should | **observed** then **planted** — the file was 15 for 15 unfalsifiable before this row, and `npm test` exited 0 over it |
| R-41 | Every floor recorded in `test/floors.json` is read by the script it names | `check_floor` wired into `ux_lint_test.py` and `brand_lint_test.py`; plant: each floor set to 9999 in turn → exit 1, naming the script and the count it ran | **planted**, and **observed** first — the floors for both harnesses had been recorded since v0.36.1 and read by nothing, so a deleted fixture would have dropped the count in silence. Standing instruction #4 on the ratchet itself |

**Rows at `never`: 0.**

**The U061 plant did not land on its first attempt, and the miss was worth
more than the plant.** Disabling the `U061` branch left `criteria` as `None` on
the way into the `U062` `elif`, so `re.search(…, None)` raised `TypeError` and
the harness died with a traceback instead of two clean red cases — exit 1 for
the wrong reason, which is indistinguishable from a pass if only the exit code
is read. The state is unreachable in the shipped code (`stated(None)` is always
false, so the `elif` is never taken), but this file's own linter promises that
malformed markdown is *reported, never raised*. `field_body(...) or ""` closes
the crash path, and only then did the plant land as two red cases. Standing
instruction #5, arrived at from the other direction: writing the fixture where
only one branch can fire also means the branch must be *disableable* without
taking the file down.

**What the honest outcome was on the pack's own chain.** All 15 scenarios
already carried an observable — spelled `**Expected:**`, the short form — so
`U060` fired on none of them, and all 7 stories carry Given/When/Then criteria,
so `U061` and `U062` fired on none. What was missing was the other half of
M-17, the path from the observable to the evidence: 15 of 15 claimed
`Status: implemented` and named no code. All 15 now cite the implementing
ranges in `bin/super-ux.js` (and, for `SCN-011`, the two templates that decide
the outcome), each verified by reading the file rather than by recall. **No
scenario was marked covered that is not**, and no rule was weakened to get
there: the tolerance for the short field spelling is a decision about the
question `U060` asks, filed as `SU-02` so the field vocabulary gets its own
code rather than being absorbed into this one.

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
| R-22 | Every marker carries an id, so coverage over the set is computable | The `AT-01`..`AT-15` table in `ai-tells.md`, each row naming its checker | **verified 2026-08-20** — `validate_ai_tell_coverage` counts rows against sections in both directions and refuses a gap in the sequence. Watched: deleting the whole `### AT-15.` section with its row left in place kept `test/validate.py` at `OK (3539 checks)`, exit 0; against the check it is `FAIL ... AT-15 has a table row and no ### AT-15. section`, exit 1. Filed as B-017 — this row said B-016, which is the id-reuse row (B-020) |
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

## 2026-08-17 (second) — reference sweeps become askable, v0.43.0

| REQ | What ships | Verified by | Watched |
|---|---|---|---|
| R-01 | The capability predates the routing by eight releases | `ux-flows/SKILL.md` carries *"Real flows off the shelf, before you invent one"* with the Refero/Mobbin distinction, and `references/funnel-research.md` FR-01 collects live competitor funnels; neither word was in any `description` | observed |
| R-02 | The cost was a routing dead zone | before, through the umbrella's matcher: `найди референсы дизайна`, `подбери референсы`, `find reference screens` → `[]`; after → `["super-ux"]` | observed |
| R-03 | The split is the other pack's own rule, not a preference | `sheleg-design/DESIGN_SYNC_BRIDGE.md` §4: *"A reference sweep answers what a good version of this screen contains — sections, hierarchy, content order. It never answers what it looks like."* Structure lands here; the visual half went to `sheleg-design` 1.40.0 | observed |
| R-04 | Both routers rise when a prompt names both halves | `нужны визуальные референсы` → `["super-ux","sheleg-design"]` | observed |
| R-05 | The addition paid for itself in characters | the funnel clause was rewritten rather than extended: 893 → 940, leaving 30 free under the 970 working limit | observed |
| R-06 | The gate is green | `python3 test/validate.py` → `OK (3500 checks)`; `npm test` exit 0 across all four suites | observed |

**Rows at `never`: 0.**

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
