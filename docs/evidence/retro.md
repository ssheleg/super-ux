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
   after five stamps with no recurrence.)*

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
