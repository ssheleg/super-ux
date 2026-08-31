# Pipeline retrospective — super-ux

One file per project. Stage 0 of every run reads the standing instructions
below **in full** before its first question.

## Standing instructions

Hard cap: ten. Each carries the run stamp it was written at. Retire an entry
the moment any of its three triggers fires — it became a mechanical check,
the paths or commands it names are gone, or it has not fired in five run
stamps — and log the deletion as one line under *Retired*.

1. **(2026-08-05)** Before tagging any release, run
   `python3 test/release_preflight.py`. A clean tree and a green validator
   describe the repo, not the remote. *(Retire when a hook or CI runs it
   automatically.)* — **fired on v0.28.0, v0.29.0 and v0.30.0: passed all
   three, every push used `--atomic` as it prints. The failure it was written
   for has not recurred.** Checked against all three retirement triggers at
   the v0.30.0 run: still not automated, paths intact, fired within five
   stamps. Kept.

2. **(2026-08-05)** **Never read a gate's verdict through a pipe.** Run the
   gate alone, check `$?`, then print. `python3 test/validate.py | tail -2 &&
   git commit` commits on a red validator, because `tail` exits 0 and `&&`
   reads the pipeline's status, not the gate's. *(Retire when a hook enforces
   it, or after five stamps with no recurrence.)* — **fired on 2026-08-10:**
   `python3 docs/brand/lint.py … | tail -3; echo exit=$?` printed `exit=0`
   while nine errors scrolled past. Two stamps, two catches. Kept.

3. **(2026-08-10)** **A new check runs against the seeded template before it
   runs against anything else.** `CONTRIBUTING.md` requires a freshly seeded
   project to lint clean from the first second, and a check written against
   real content will not notice it broke that. The vision emptiness check
   errored on the pristine `templates/vision.md`, because `read()` strips the
   HTML comments the template is made of. *(Retire when the validator seeds a
   project and lints it, or after five stamps with no recurrence.)* — **fired
   on v0.33.0, one stamp after it was written:** B007 warned on every freshly
   seeded pack, because a seeded `voice.md` legitimately has no references
   yet. The fix was to gate the check on `Status` leaving `draft`, not to
   soften the promise. Two checks written, one caught. Kept, and the cold
   clock resets here.

4. **(2026-08-10)** **An artifact added to stop drift needs its own answer to
   "what would notice if this fell behind?"** A harness, a registry, a matrix,
   a checklist — each can drift, and "someone remembering" is not an answer.
   Where the artifact is a set, give its members ids first: a rule set that
   cannot be enumerated cannot have coverage computed over it. *(Retire when a
   coverage gate exists for every generated or hand-kept set in the repo, or
   after five stamps with no recurrence.)* — **fired on 2026-08-19 (SU-01), on
   the ratchet itself:** `test/floors.json` had held floors for
   `ux_lint_test.py` and `brand_lint_test.py` since v0.36.1 and `check_floor`
   was called for `validate.py` alone, so two of the three recorded floors were
   decoration and a deleted fixture would have dropped either count in silence.
   Both harnesses now read their own floor, watched refusing against a planted
   9999. Kept — the trigger it names is not met while `SU-03` shows a layer
   (`JTBD-NN`) whose ids no rule can even enumerate.
   **Fired again on 2026-08-19 (SU-02), on a set nobody had counted as a set:**
   the status enums existed twice — once in `scenario-format.md` and once in
   `ux_lint.py` — and had already drifted, the contract declaring five screen
   statuses against a matcher listing four, so a `blocked` screen read as having
   no status and `U021` stopped applying to it. Nothing could have noticed.
   `validate_status_enums_match_contract` is the answer, and it reads the linter's
   side with `ast` rather than restating it, so it does not become the third copy.

5. **(2026-08-14)** **A fixture that asserts a set of codes proves the code
   arrived, not which branch produced it.** Where two branches of one check emit
   the same code, deleting either leaves the suite green and the plant reports
   nothing. Both of this run's misses were this: an English fixture for the
   dash-before-conjunction branch stayed green when that branch was deleted,
   because the strict branch emitted `B062` by another path; and a fenced-block
   fixture stayed green when the fence stripper was deleted, because the
   inline-code stripper removed the same dash. **The fix is to write the fixture
   in the conditions where only the branch under test can fire** — Russian for
   the conjunction case, since strict is off there; a lone backtick inside the
   fence for the other, since that defeats the inline pass. *(Retire when the
   harness asserts which branch fired rather than which code arrived, or after
   five stamps with no recurrence.)*
   **Held on 2026-08-19 (SU-02) by design rather than by recurrence.** `U068` has
   two branches emitting one code — a code citation offered as an outcome signal,
   and an audit verdict offered as one — so it was built as three disjoint `if`s
   rather than an `elif` chain, and each fixture is written where only its own
   branch can fire: the citation cases leave nothing but paths, so the verdict
   guard is false there; the verdict case leaves prose, so the citation guard is.
   Both plants landed on exactly their own cases, four then one. What the plants
   also caught was the opposite failure — a check narrower than its message: the
   citation branch went CLEAN against `bin/super-ux.js:235-296`, the range form
   this pack's own chain writes, and again against two citations separated by a
   comma. Kept, and the cold clock resets here.

6. **(2026-08-30)** **A field, option or exemption added to a template or a
   contract is read by code in the same change, or it is not added.** Three
   occurrences now, and the third was found only because the second opened the
   file. `AT-06` listed a table-cell exemption `B062` never implemented.
   `Humanization pass:` lived in `templates/brand/voice.md` and nowhere else:
   not in `brand-contract.md`, not in this pack's own `voice.md`, read by no
   code, for releases. Both looked exactly like a working feature to anyone
   reading the artifact that declared them. `validate_brand_contract_fields`
   closes one direction only — a field the linter reads must be one the
   contract defines — and there is no arrow from a declared field to a reader.
   *(Retire when a gate enumerates template and contract fields and requires a
   reader for each, or after five stamps with no recurrence.)*

7. **(2026-08-31)** **Reproduce a board row before fixing it.** Plant the
   defect it describes and read what comes back. Two of the eleven rows closed
   on 2026-08-31 were false: `B-021` asked for a check that already existed and
   nearly shipped a duplicate, and `B-019` described a defect four probes could
   not reproduce. Both were caught by planting first and neither would have been
   caught by reading the row. A row is a claim about the repository at the
   moment it was written, and it ages like any other claim; priority makes a
   stale one actively expensive, because it is picked first. *(Retire when a
   gate can decide whether an open row is still true — which needs the row's
   own text to be executable — or after five stamps with no recurrence.)*

## Retired

*(nothing yet)*

## Run stamps

Newest last.

| Date | Task | Diverged? |
|---|---|---|
| 2026-08-05 | Tier-1 audit findings → BP-147..156, audit scope section, catalog validator; v0.27.0 → v0.27.1 | yes — see below |
| 2026-08-05 | Carry-over ledger closed → BP-157..179, PRN-17..21, three optional contract fields, prototype step, catalog index; v0.28.0 | no |
| 2026-08-05 | Contract doctor + the audit's four unclaimed findings; v0.29.0 | no |
| 2026-08-05 | Verbal identity layer, carry-over ledger to zero, code graph; v0.30.0 → v0.30.1 | yes — see below |
| 2026-08-05 | Verbal identity layer — brand-contract v1, brand-voice + copywriting, brand_lint.py, BP-182..205, PRN-22..24; v0.30.0 | yes — see below |
| 2026-08-10 | Structural audit of 0.31.0 → 22 findings closed, three composition gates, dogfood chain + brand pack; v0.32.0 | yes — see below |
| 2026-08-10 | Web surface in the contract, four routing rows, composite briefs, B007 + B026, ux_lint fixture harness; v0.33.0 | yes — see below |
| 2026-08-10 | B-010 + B-002 — UX linter codes U001..U054, 43 fixtures, coverage gate, run-instruction gate; v0.34.0 | yes — see below |
| 2026-08-12 | Reference sweep for flows in `ux-flows` (Refero, Mobbin, Lazyweb), gated on tools not config; v0.35.0 → v0.35.1 | yes — see below |
| 2026-08-14 | The rhetorical dash and the full-stopped title become `B062`/`B063`; markers get ids `AT-01..15`; doctrine prose swept; dogfood wired into CI; v0.39.0 | yes — see below |
| 2026-08-19 | SU-01 (manifesto M-17) — `U060..U065` give the requirement layer the observable it demands; the pack's own 15 scenarios cite their code; both harness floors become readable | no — single-row close; the one plant that missed is recorded in the ledger |
| 2026-08-19 | SU-02 (manifesto M-21) — `Product: unobserved / observed / contradicted` as a state no audit can promote; `U066..U070`; the field vocabulary settled on the long spelling; the live screens enum drift closed | no — single-row close; two plant misses recorded in the ledger |
| 2026-08-30 | Wave-2 family-audit close (SUX-01/06/07/08/11) — templates mirrored into the plugin and each seeding skill by `sync_references.py`, `validate_shipped_templates` + `validate_shipped_paths` gate the class, `/ux-audit` scope surface completed, three descriptions stop over-claiming; v0.50.0 | yes — standing instruction #4 fired on the floor itself: `floors.json` held 3667 against a pre-change suite of 4111, un-raised since SU-04; raised to the measured 4174. R-70 is a `never` (three homes of one enum, no comparator) filed as `B-030` rather than left off the ledger |
| 2026-08-30 | `B062` judges the dash's role rather than its glyph; the table-cell exemption `AT-06` promised gets implemented; `landing-pages.md` gives `copywriting` the assembly layer it lacked (`LP-01..LP-20`); humanization becomes a default with `B064` and a status in four places; `onboarding.md`, `internal-screens.md` and `product-frameworks.md` add `ON-`, `IS-` and `PF-`; one coverage gate over four id sets; v0.52.0 | yes — two divergences: a doctrine exemption sixteen days unimplemented (`B-031`), and the bytecode cache defeating a planted defect |
| 2026-08-31 | Board close-out — all eleven open rows closed with a mechanism and a watched plant each: `Kind: copy \| layout` in the string registry, `U076`/`U077`/`U078`, `B065`, `cited_entries_date`, three contract-parity gates, `test/evals/`, and a refreshed code graph with `validate_graph_claims` over what its labels assert; v0.52.0 | yes — two rows were not what the board said, and the refreshed graph asserted a number nobody computed |
| 2026-08-31 | Wave-3 family-audit close (SUX-02/04/05) — per-skill `compatibility:` front matter ×7 (yaml.safe_load-proven, plant caught), `$schema` in both manifests (the resolving spellings), and the eval suite executed: 28 blind trigger probes 14/14 on two models, 12/12 scenario lines, receipts and Method in `test/evals/RESULTS.md`; `B-033` filed for the missing YAML front-matter gate; v0.52.2 | yes — twice. (1) A concurrent session cut v0.52.1 from this working tree while this run's SUX-02/05 edits sat uncommitted in it: they shipped inside that release with no CHANGELOG line, and the guarded files it wrote (`CHANGELOG.md`, `package.json`, both manifests, `test/validate.py`) were written while THIS run held the only live lease (`SUX-W3`) — the fs lease is advisory for a session that never asks. The 0.52.2 entry documents the stowaways; the coordination miss is recorded here rather than smoothed over. (2) The eval run was killed mid-flight by an account spend limit and re-executed clean after reset — the first attempt produced zero result files, so nothing partial leaked into the recorded rows |

**Prune, 2026-08-31 (v0.52.0, board close-out).** All five checked against the three retirement
triggers; nothing retired, nothing added, so the list stands at five against a
cap of ten. **#3 fired and passed:** before the widened dash check was written,
`templates/brand/*.md` and `docs/brand/*.md` were both measured for the newly
banned spelling and both returned zero, so a freshly seeded project still lints
clean from the first second; the seeded `docs/brand/lint.py` was re-copied from
its source and run, and `validate_seeded_scripts` compared the bytes. **#4 fired
twice and shaped the work rather than commenting on it:** the twenty playbook
rules were given ids and `validate_landing_coverage` before the prose was
accepted as finished, and the citations to `docs/research/landings/` got a gate
instead of a `never` row in the ledger, which is the trade this instruction
exists to force. **#5 fired hardest** and decided the shape of every new
fixture, recorded in this run's entry. **#2 held:** all five gates were run
alone and their own exit codes read, printed beside each verdict, and no
pipeline stood between a gate and its status; it is four stamps since it last
caught anything, one short of its cold trigger, so it is kept and watched.
**#1 fires at the tag** in this same run. **One added (#6)**, from the third
occurrence of a declared-but-unread field, so the list stands at six against a
cap of ten. The bytecode finding is deliberately **not** added: it became a
mechanical check in the same change, which is retirement trigger one, and a
standing instruction that is already a gate is the list filling with things
nobody needs to remember. **Re-checked at the close-out:** #1 fires at the tag,
#2 held across roughly forty gate runs with every exit code read alone, #3 fired
again on `U076` — which went silent on the very template it was written for until
placeholders stopped counting as content — #4 shaped four of the eleven closures,
and #5 decided the isolation pair for `Kind`. **One added (#7)**, so the list
stands at seven against a cap of ten.

**Prune, 2026-08-14.** All four checked against the three retirement triggers.
**#2 fired hardest and fired on this run's own hands:** the first plant harness
read `python3 test/brand_lint_test.py 2>&1 | head -4; echo "exit=$?"`, printed
`exit=0`, and a `FAIL:` line scrolled past inside it. Three stamps, three
catches. **#3 fired** and passed: the new checks were run against a freshly
seeded `templates/brand/` pack before anything else, and it linted clean. **#4
fired twice** — the `AT-` ids were given precisely so coverage could be computed
and nothing computes it (`B-017`), and the dogfood linters turned out never to
have been in CI, which is why `docs/brand/lint.py` sat red on `B030` with a
three-count-stale `facts.md` and nothing said so. **#1 did not fire**; no tag
was cut in this run, and it is one stamp old on that count. Nothing retired,
**one added (#5)**, so the list stands at five against a cap of ten.

---

## 2026-08-31 — the board was not a description of the code

**Symptom.** Closing eleven rows meant reading eleven claims about this
repository, and two of them were false. `B-021` asked for a check that every
practice in the catalog is reachable from the selection protocol; that check
had existed inside `validate_bp_index` since before the row was written, and
the row had sat open at priority 18 — the joint highest on the board — for
seventeen days. `B-019` described a duplicate `FAIL:` line that four probes
could not reproduce: both hard rules, each from both sides of its pair, one
line per defect and a count that matched. It had been fixed by a refactor
nobody credited.

**Surfaced at** stage 5, and only because the work started by planting a defect
rather than by reading the code. `BP-242` went into the catalog and **two**
messages came back, one of them from a check this run was in the middle of
writing. **Owned by** stage 10 of the runs that fixed both: a fix that closes a
board row and does not strike it off leaves the board describing a repository
that no longer exists.

**Root cause.** The board is written by hand and read by hand. Every other set
in this repository has a gate asking whether it still matches the thing it is
about -- `AT-` ids against fixtures, `BP-` ids against the index and the
protocol, contract enums against the matchers, cited teardowns against the
files. The board has `validate_board_ids`, which asks whether the ids referenced
from the ledger exist. Nothing asks whether an open row is still true, and
nothing could: "is this defect still present" is the row's own text, in prose,
and only a person can read it.

**What that cost, beyond the duplicate.** A false open row is worse than a
missing one, because it is priced. `B-021` sat at `3×2×3 = 18` and would have
been picked first by anyone deriving priorities from the board, sending them at
work already done. The board's own header says a row with no evidence column is
a wish; the sharper rule this run found is that a row with evidence can still
be stale, because evidence ages.

**Fix, by grade.** *Practice, not mechanism, and said plainly:* both rows were
closed by **reproducing them first** — planting the defect each described and
reading what came back — rather than by writing the fix they asked for. That
found the duplicate before it shipped. *Mechanism where one was possible:* the
reverse arrow neither row had noticed, which is a routing row pointing at a
practice the catalog does not define, and a report that can no longer disagree
with its own count. *Class:* standing instruction #7.

**The second finding, from the same discipline.** `B-022`'s graph refresh
worked, and the refreshed graph then asserted `82 tags, 206 practices` in 58
label fields, about a catalog of 241 and an index that states no counts at all.
A model wrote that number and the cache preserved it across three refreshes. It
is exactly what this file has recorded before in the abstract — a wrong document
gets argued with, a wrong graph gets believed — and this is the first time it
was measured. `validate_graph_claims` now compares what the labels assert
against the files they are about, and its first run produced a false positive
that improved it: a node quoting `181 practices against a catalog of 206`, which
is a true sentence about a past defect. The gate is narrowed to `label` and
`norm_label`, where the graph speaks in its own voice.

**The check that catches it next time.** For the graph, `validate_graph_claims`.
For a stale board row, nothing mechanical, and standing instruction #7 says so
rather than pretending otherwise.

## 2026-08-30 — the evidence could be cached

**Symptom.** A planted defect is this project's unit of evidence: the ledger's
`planted` rows all mean "a defect was introduced and the check caught it", and
the transcript is the proof. During this run's `B064` plants, the revert did not
take. The source had zero occurrences of `B999`, `cmp` against the backup said
the file was identical, and `python3 test/brand_lint_test.py` still reported
`expected ['B064'], got ['B999']`.

**Surfaced at** stage 5, from a restored gate that stayed red for no reason the
file could explain. **Owned by** every run that has ever planted a defect in a
Python module, which is most of them.

**Root cause.** CPython invalidates cached bytecode on `(source mtime, source
size)`. The plant replaced `"B064"` with `"B999"`, which is byte-identical in
length, and the revert happened inside the same second. Both components of the
key matched, so the interpreter loaded the planted `.pyc` for a file that no
longer contained the plant. The failure is silent by construction: nothing in
the output distinguishes a stale cache from a live defect, and the natural next
move is to go looking for the defect in the source, where it is not.

**Why it matters more here than elsewhere.** The direction it failed in this
time was harmless: a revert that kept reporting a defect is loud and gets
investigated. The opposite direction is the dangerous one, and it is equally
reachable. Plant a defect, watch the *cached* clean build pass, and record
"the check did not catch it" — or worse, plant, get a real red, revert, and
have the cache serve the clean version so a genuinely broken revert looks
green. Either way the ledger fills with sentences that are false and look
exactly like the true ones.

**Fix, by grade.** *Mechanism:* both fixture harnesses set
`sys.dont_write_bytecode` before importing anything from the plugin's scripts,
with the measurement in a comment beside it. Verified by repeating the exact
sequence that failed: plant, red; revert in the same second, green, with no
cache cleared. *Scope, stated because it bounds the fix:* `test/validate.py`
needs no guard, because it never imports the modules it inspects — it reads
them as text and parses literals with `ast`, so there is no bytecode to stale.

**The check that catches it next time.** The guard itself, and it is a real
retirement trigger rather than a promise: standing instruction #6 covers the
class this belongs to only partially, so what protects this specific failure is
two lines of code that cannot be forgotten because they are not a habit.

## 2026-08-30 — the check knew the character and not the job

**Symptom.** `B062` is the mechanism behind `AT-06`, the rhetorical dash. Its
whole implementation rested on `DASH = "—"`, one codepoint, so a draft could be
cleared of every finding by exchanging that character for an en dash or for a
hyphen with a space each side. The habit the rule exists to catch survives all
three spellings unchanged. This was not hypothetical when it was found: a live
page read the same day carried twenty rhetorical dashes and not one em dash
among them, every one written as a spaced hyphen, and our own linter would have
called it clean.

**Surfaced at** stage 0, from reading three competitors' landing pages for an
unrelated reason. **Owned by** stage 5 of the run that introduced the code in
v0.39.0, which wrote seven planted defects against the branches and none
against the premise. Every one of those plants exercised *what the check does
with a dash*; none asked *what the check thinks a dash is*.

**Root cause.** The doctrine and the code agreed, and both were wrong in the
same place. `ai-tells.md` opened its own rule with "The em dash is banned where
it is rhetorical", naming a glyph in a paragraph whose next sentence says the
distinction is about the job the mark is doing. A fixture set derived from that
sentence inherits its blind spot, and the seven plants of v0.39.0 could not
have found this one, because a plant proves a branch and the defect was in the
constant every branch read.

**The second defect, found only because the first opened the file.** The same
doctrine lists a dash alone in a table cell among the grammatical exemptions,
"a glyph doing the job of an empty string". Nothing implemented it. In any
strict locale `| landing | — |` was reported, and had been for sixteen days.
`B-017` closed the arrow from a named marker to a check; there is no arrow from
a named **exemption** to a negative fixture, and that is now `B-031`.

**Fix, by grade.** *Mechanism:* `normalise_dash_spelling` reduces every
spelling to one mark before any branch judges it, so the conjunction rule, the
paired-dash rule, the locale allowances and the range and speech exemptions
apply to all three without being restated three times. The substitutions are
length-preserving by construction, which is what lets the finding quote the
author's own characters: a report quoting a mark the writer never typed sends
them grepping for it, and that is the failure mode this file recorded in
v0.39.0 under a different name. *Mechanism:* `TABLE_CELL_DASH_RE`.
*Doctrine:* the rule now says role rather than glyph, and says so in the
opening sentence where the error was. *Class:* `B-031`.

**What made the fixtures honest.** Standing instruction #5 says a fixture must
be written where only the branch under test can fire, and it decided the shape
of all four new ones: none carries an em dash, so deleting the normaliser
leaves no dash for any branch to find and the fixture goes red rather than
green by another path. The conjunction case is written in Russian, where strict
is off, so it proves the normalised spelling reaches that branch instead of
being caught by strict on the way past. Three plants, and each landed on
exactly its own cases.

**The check that catches it next time.** For the spellings, `B062` itself, now
watched failing on all three. For the exemption class, `B-031`. For the
premise-versus-branch distinction that both defects share, nothing yet, and
saying so is more useful than inventing a gate this run did not build.

## 2026-08-14 — the doctrine had the habit it was written to name

**Symptom.** `ai-tells.md` had carried "Em-dash reflex" since the verbal
identity layer shipped, graded S2, worded *"one or two in a piece is normal"*.
The file making that observation contained 28 em dashes in 163 lines. The
eleven references around it carried 158 between them. Meanwhile `S1_MARKERS` in
`brand_lint.py` held twelve string literals and no dash among them, so the
marker the doctrine named was the one thing the linter could not see.

**Surfaced at** stage 0, from the operator's own reading of the pack rather
than from any check. **Owned by** stage 5 of the run that introduced the marker
in v0.30.0: a marker was written into a reference and no check was written
beside it, which is the same shape as the four codes the 2026-08-10 audit found
emitting with no fixture.

**Root cause.** Doctrine and enforcement were added in different steps, and
nothing asks whether a named marker is checked. `validate_brand_lint_coverage`
runs the question in one direction (every emitted code needs a fixture and a
contract row) and there is no arrow the other way, from the prose to the code.
That gap is now `B-017`, filed against this run's own `AT-` ids so the same
thing cannot be said about them.

**Fix, by grade.** *Mechanism:* `B062` and `B063`, with seven planted defects
and a locale-aware allowance so the rule does not ban correct Russian.
*Mechanism:* the dogfood linters entered CI, which is what would have caught the
adjacent defect this run found by accident — `docs/brand/lint.py` had been
failing on `B030` with a `facts.md` three counts stale, and nothing reported it
because nothing ran it. *Doctrine:* every marker now carries an id.
*Housekeeping:* 144 of the 158 dashes are gone from the shelf.

**The check that catches it next time.** For the dash, `B062`. For the class,
`B-017`. For the meta-failure — a repository that installs a "wire the linter
into CI" rule into other projects while not obeying it itself — the two new
workflow steps, which fail on this project's own pack exactly as the hard rule
has always demanded of everyone else's.

**The dogfood it added measured the wrong file for most of the run.**
`docs/brand/lint.py` is a **copy** of `brand_lint.py`, seeded by `/brand-init`,
and it was 227 lines behind. So the pack was linted twice with two different
answers to what "the linter" means: the source, which had `B062` and `B063` and
drove every fix; and the copy, which had neither and still reported clean. Both
said clean, and only one had been asked the new questions.

`validate_seeded_scripts` could not see it, because it verified that *a command
instructs the copy*, not that the copy is current. It now compares bytes, and a
planted two-line append turns it red. This is standing instruction #4 again on a
third artifact: a copy that nobody notices falling behind is not a copy, it is a
fork with a misleading name.

**A correction this run made out loud.** Mid-run it claimed the Brand voice hard
rule had no drift gate, on the evidence that `HARD_RULES` names only the UX
scenarios and vision headings. That was wrong: the check compares the **whole
template file** against one embedded block, and the heading only selects the
block, so the Brand section was covered all along. The gate proved it by going
red on the template edit before the carrier was re-copied. What is genuinely
ungated is the third copy, in this repository's own `CLAUDE.md`, filed as
`B-018`.

## 2026-08-12 — a comparison whose third term was invisible

**Symptom.** 0.35.0 added a reference sweep to `ux-flows` step 2 and said Refero
was the server that returns flows "rather than loose screens". Mobbin returns
them too. 0.35.1 corrected it the same hour, alongside the identical correction
in `sheleg-design`.

**Root cause.** The sentence compared three servers and one of them could not be
inspected: Mobbin was registered and unauthenticated, so its tool surface was
invisible. The claim was written in the same voice as the two halves that had
been checked, sitting between them. The rule that forbids it — *gate on the tools
present in the session, not on the config* — was in the paragraph directly above,
written for the reader of the skill and never turned on its author.

**Why no gate held it.** None can. `validate.py` reads files; it cannot open an
MCP server and ask what it exposes, and a check that tried would fail for every
reader who has not signed in. This repository's ledger now carries that limit
explicitly: R-14 is `never`, and says why.

**What replaced it is better than what was wrong.** Both servers return flows, in
different media — Refero as structure (goal, action, system response per step),
Mobbin as preview images per step. So the instruction is now *read one to draw
the diagram, look at the other to check it*, which is actionable in a way "only
one has flows" never was.

**Carried across.** The companion repository widened its standing instruction from
*a pack needs a reachable reference* to *any claim about something outside the
session's reach*. The same rule applies here and is why R-15 was recorded as
`observed` against a live query rather than against a tool description.

---

## 2026-08-10 — the harness had the defect it was built to fix

**Symptom.** v0.33.0 shipped `test/ux_lint_test.py` with fourteen cases
covering **one** of the linter's twenty-one rules. It was filed as B-010 and
called a backfill. It is not a backfill — a partial harness reports green, and
green from a partial harness is indistinguishable from green from a complete
one. The linter it tests is the older and more central of the two; the brand
linter had carried a fixture per code since v0.30.0, four releases earlier, and
nobody had noticed the asymmetry because both were green.

**Surfaced at** stage 0 of the next run, reading its own board.

**Owned by** the previous run — this one. The harness was built without the
gate that keeps a harness honest, which is the same omission one level up from
the one it was built to close.

**Root cause.** An artifact added to stop drift is itself an artifact that can
drift, and the question *what makes this fall out of date, and what would
notice?* was never asked of the new file. Its answer would have been "someone
remembering", which is the answer that means there is no answer.

The mechanical obstacle underneath: the linter's rules were **prose**. A rule
set that cannot be enumerated cannot have coverage computed over it, so no gate
was possible until the rules had ids.

**Fix, by grade.**

- *Mechanical (taken):* codes `U001..U054` in every message; a fixture per
  code, 43 checks; `validate_ux_lint_coverage` requiring a fixture **and** a
  contract row per code. It went red on all twenty-one on its first run, which
  is what a coverage gate should do the day it is added.
- *Structural (taken):* `validate_run_instructions` closes B-002 from the
  inverse direction — for each path an instruction names, is it seeded? The
  existing gate asked only the forward question, and a rename breaks the other
  one.
- *Method (taken, and the part worth keeping):* the fixtures were confirmed to
  bite by planting defects **in the linter**, not in the input — a comparison
  weakened, a branch short-circuited, a condition keyed to an impossible value.
  Each turned exactly one case red. Fixtures passing proves the codes fire; only
  this proves the fixtures would notice if they stopped.

**The check that catches it next time:** `validate_ux_lint_coverage` for this
class, and the standing instruction below for the general one.

---

## 2026-08-10 — the index inherited the vocabulary of the people who wrote it

**Symptom.** A composite request — *feature, design, UX/UI, marketing funnel,
landing, web, app* — was walked through `/ux` as an agent reads it. Eight items:
**eight had an owner, three had a word.** `commands/ux.md` matched zero rows for
funnel, monetization, design-as-a-task, SEO, or mobile app, while
`practice-selection.md` routed `BP-116..123` off the purchase surface and
`BP-049..054` off `Platform: mobile-*`, and `ux-flows` named `sheleg-design`
twice. Separately, `scenario-format.md` mentioned indexability, robots,
crawlers and schema **zero times**, so the layer that designs landings had no
field for the rule that governs them.

**Surfaced at** stage 0, by a routing test the operator asked for. Every gate
was green, including the three composition gates added eight hours earlier.

**Owned by** the routing table and the contract — not by any skill. Each skill
was complete about its own subject.

**Root cause.** Two of the same family, one layer apart.

The routing table is the artifact built **for people who do not know the
internals**, and it is written **by** the people who do. Every row someone adds
is a row they personally needed; the concepts they already reach by another
name never become rows. Nothing errors — an unmatched request falls into the
catch-all and gets a confident answer to a question nobody asked.

The contract had the same shape at the layer below: `screens.md` recorded
Purpose, States, Elements, Figma and Coverage — everything a *screen* is — and
nothing about the screen being a *URL a machine reads*, because that reader was
never at the table when the fields were chosen.

**Fix, by grade.**

- *Mechanical (taken):* the `Web surface:` block, five fields, each read off
  `seo-aeo-audit`'s own O1–O5 checks so the record and the audit share one
  vocabulary; `check_web_surface` with fourteen fixtures; four routing rows;
  a decomposition rule for composite briefs; B007 and B026 with fixtures.
- *Structural (taken):* `test/ux_lint_test.py` exists at all. The brand linter
  has had a fixture per code since 0.30.0 and the older, more central linter
  had none — a gap nobody had asked about because both were green.
- *Documentation (taken):* the backfill for the pre-existing UX checks is
  **B-010**, named on the board rather than implied by the harness's existence.

**What the new checks did on their first run:** B026 found `Nothing selected.`
in this project's own installer, and B007 found a voice with no brand it refuses
to sound like. Both defects were in the tree the audit had just called clean.

**The check that catches it next time:** none of these. A router's coverage of
*the words a user brings* is not derivable from the repository — it needs a real
composite request in the user's own phrasing, walked through, with two columns:
capability, and the word for it. That is a scheduled exercise, not a gate, and
saying so is the honest half of this entry.

---

## 2026-08-10 — a green suite that had never been asked a question about composition

**Symptom.** `python3 test/validate.py` reported `OK (3427 checks)` on
v0.31.0 while the README advertised 181 practices against a catalog of 206
and 31 lint checks against a linter emitting 33; the heuristic range appeared
as `PRN-01..10`, `..16`, `..21` and `..24` in six files; `/ux` — documented
as "the only command a user needs" — named three of seven skills; and
`vision`, shipped the same day, reached neither the system map, the linter,
the doctor, a template, a Cursor rule nor the router. Evidence: the audit's
35-check re-verification script, all failing before this run and all passing
after.

**Surfaced at** stage 0, by an audit the operator asked for. Nothing in the
pipeline would have surfaced it: every stage was green.

**Owned by** the validator. Not by the people who wrote the drifting files —
each edit was locally correct, and no single file looked wrong.

**Root cause.** 3427 checks verified **shape** — front-matter fields, version
agreement across manifests, byte-identity of the shipped reference copies,
link resolution, one fixture per lint code. Not one of them verified
**composition**: whether a number in prose equals the artifact it counts,
whether a skill that exists is reachable, whether a script an instruction
names is installed by anything. Shape is what a single file can be wrong
about. Composition is what only the set can be wrong about, and absence has
one side — so it has to be asked for by name.

The second half of the cause is subtler and is why the drift was invisible
rather than merely unnoticed: **the checks that did exist made the suite feel
exhaustive.** 3427 is a number that stops people looking.

**Fix, by grade.**

- *Mechanical checks (taken):* `validate_stated_numbers` recomputes every
  count written in prose from the artifact it counts.
  `validate_skill_parity` asks for each skill by name in five places.
  `validate_seeded_scripts` proves every script an instruction names is
  copied there by some command. `validate_hard_rule_copies` is now driven by
  a pair list rather than one hardcoded pair. Each was verified against a
  planted defect before being trusted — the plant/revert transcript is in
  `docs/superpowers/verification.md`, and every row there is `planted` or
  `observed`, none `never`.
- *Structural (taken):* `references/system-map.md` names contracts and links
  none. Every link in a skill is a shipping instruction, and because every
  skill links the map, a link from the map is a link from all of them.
- *Documentation (taken):* `CONTRIBUTING.md` gains an "Invariants the
  validator asks for by name" section, so the next contributor meets the
  rules before tripping them.
- *Dogfood (taken):* super-ux now runs its own chain and its own pack. Six
  further defects surfaced within an hour of writing the scenarios, four of
  them in the shipped `brand_lint.py`. That is the real fix: the audit found
  the drift once, the dogfood finds it continuously.

**The check that catches it next time:** the three composition gates. The
older one — the suite's own count — is what to stop trusting.

### A note that expires

Writing a check and running it once against real content is not a test: the
pristine template is a different input, and `CONTRIBUTING.md` promises it
lints clean. Now standing instruction #3. **This note expires 2026-08-24**
(two runs) if #3 has held.

---

## 2026-08-05 — a tag published a tree four releases old

**Symptom.** `git push origin main --follow-tags` was rejected for `main`
(non-fast-forward) but pushed `v0.27.0` anyway. CI accepted the tag, and a
public GitHub release v0.27.0 was built from a tree that predated
0.26.2–0.26.5 — missing the MIT declarations, the `/ux-audit` front-matter
fix, `displayName`, and the npm-publish workflow. Evidence:
`git merge-base --is-ancestor origin/main v0.27.0` → false;
`gh release list` showed v0.27.0 as Latest.

**Surfaced at** stage 8 (release), on the push itself.

**Owned by** stage 0. The harvest recorded "clean, everything pushed" as a
fact about the repository and that fact was never re-verified across the
whole run. Six commits landed on the remote in between.

**Root cause,** two parts that only fail together:

1. Freshness was treated as durable. Every local signal available at tag
   time — clean tree, green validator, four manifests agreeing on the
   number — describes the repo and says nothing about the remote.
2. `git push --follow-tags` is not atomic. A rejected branch ref does not
   roll back the tag that travelled with it, so the repository ends in a
   state where the tag is public and the branch is not. Neither half looks
   wrong on its own.

**What saved it from being worse:** the broken tree predated the workflow
that publishes to npm, so it could not publish itself. npm stayed on 0.26.5
until the corrected 0.27.1. That was luck, not design.

**Fix, by grade.**

- *Mechanical check (taken):* `test/release_preflight.py` — fetches, refuses
  when `HEAD` does not contain `origin/main`, re-checks the four-way version
  sync, and prints the `--atomic` push line. Verified against the incident
  tree in an isolated worktree: it names the exact four missing releases.
- *Documentation (taken):* the release steps in `CONTRIBUTING.md` now run the
  preflight and push branch and tag together with `--atomic`. The same edit
  removed a stale step — `npm publish` had been described as a human 2FA step
  since before CI gained `PUBLISH_NPMJS`.
- *Standing instruction (taken, #1 above):* run the preflight before tagging,
  until something runs it automatically.

**The check that catches it next time:** the preflight's ancestor test. It is
the only one of the four that needs the network, which is exactly why the
failure was invisible without it.

### A second, smaller divergence

Verifying the preflight, I tested it by checking out an old commit *over the
working tree* (`git checkout <sha> -- .`), which silently reverted an
unrelated fix in `cursor/rules/ux-audit.mdc`. Caught immediately by
`git status`, restored, and re-tested in a throwaway `git worktree` instead.
No standing instruction: the lesson is specific enough to be a note, and
notes expire. **Expires 2026-08-19** (two runs): verify destructive-looking
things in a worktree, never over the tree you are working in.

---

## 2026-08-05 — a red gate was committed through, twice removed

**Symptom.** `sshlg-skills` v0.19.0 was tagged and pushed while its own
validator was reporting two failures: the `skills/super-ux` submodule still
pointed at the 0.26.5 commit, and the README table still printed 0.26.5. The
tag is public and superseded by v0.19.1. Evidence: the validator's two lines
appear in the same command output as the successful push.

**Surfaced at** stage 8 (release), one command after it was caused.

**Owned by** stage 8. The gate ran, said no, and was not heard.

**Root cause.** The command was
`python3 test/validate.py 2>&1 | tail -2 && git add -A && git commit …`.
`tail` exits 0 whatever it reads, and `&&` tests the *pipeline's* status, not
the gate's — so a red validator became a green-looking prefix. The output was
even printed; it scrolled past above a successful push line, which is the
worst possible presentation: visible, and structurally ignored.

**Second finding, older and quieter.** The pin the release exists to move had
been stale at 0.26.5 for **four** releases — 0.27, 0.28 and 0.29 all shipped
without touching it, so `npx sshlg-skills list` reported and `update`
installed a version nobody was publishing. `CONTRIBUTING.md` warns about
exactly this in prose. Nothing checks it, which is why prose was not enough.

**Fix, by grade.**

- *Standing instruction (taken, #2 above):* never read a gate's verdict
  through a pipe. Run it alone, check the exit code, then print.
- *Mechanical check (taken):* `sshlg-skills` `test/check_pins.py`, gated in
  CI, released as v0.20.0. It verifies ownership before reporting drift — a
  name that exists is not a name that belongs to us, and `task-pipeline` on
  npm is someone else's 0.1.0. On its first run it found `sheleg-design`
  pinned at 1.3.4 against a published 1.7.0, so the check paid for itself
  before it was merged. C-06 closed.
- *Documentation (taken):* the stale manual `npm publish` step in
  `CONTRIBUTING.md` was replaced this run — every repo in the family has
  published from CI on a `v*` tag since that text was written.

**The check that catches it next time:** the standing instruction, until the
registry comparison exists. Both halves of this run's release were verified
after the fact with `npx sshlg-skills@latest list`, which is the assertion the
pipeline should have made before the tag rather than after it.

---

## 2026-08-05 — a repeat audit found what a green suite could not

**Symptom.** A second audit pass, run with the axis rotated from the REQ table
to the code graph, found four defects in a layer that had passed 3338
validator checks, 34 linter fixtures and a full stage-10 acceptance:

1. `templates/brand/voice.md` shipped `PER-NN` where the UX contract numbers
   personas `P-NN`. `B004` traces `Derived-from` against `foundation.md`, so a
   project following our own template earned a **false blocking error**. It
   went out in v0.30.0.
2. `B005`, `B054`, `B060`, `B072` shipped with no fixture, while the suite was
   green and the fixture count looked right.
3. Eighteen of 33 check codes were documented only in `brand_lint.py`'s source,
   in a repo whose canon is *one owner per fact*.
4. `system-map.md` — the document whose stated job is telling an agent what
   else exists — named the brand artifacts but not the pack library or the
   register model, the two things an agent would otherwise improvise.

**Surfaced at** the repeat audit. **Owned by** stage 10: the first acceptance
compared the REQ table against the plan, which finds what was named and lost.
None of these four were on any list.

**Root cause.** The horizontal pass is structurally unable to see them. A
comparison needs two sides; an absence has one. A green suite cannot report a
check it was never asked to run, and the fixture *count* looking right is
exactly what hid the four missing ones.

**Fix, by grade.**

- *Mechanical (taken):* `validate_brand_lint_coverage` — every code the linter
  can emit must have a fixture **and** a contract row. Findings 2 and 3 became
  a gate rather than two ledger entries.
- *Mechanical (taken):* `check_changelog_headings` in `sshlg-skills` — a
  version documented twice would ship the previous release's notes, because
  the workflow reads the first section and stops. super-ux has guarded this
  since its own duplicate; the launcher had not, and a two-session collision
  on v0.21.2 walked straight through.
- *Content (taken):* the contract now owns all 33 codes with severities; the
  system map names the brand shelf without linking it, because linking would
  make every skill carry ten files it will not read.

**The check that catches it next time:** the coverage gate. It is the only one
of the four fixes that would have failed the build on the original commit.

**What this run confirms about the graph.** C-03 was closed by building it, and
it earned its place on the first pass by finding defect 1 — which four
gates, a full acceptance and a human read had all passed over.
