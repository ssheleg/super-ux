## 0.52.5 — the card the umbrella renders, and the half of the role that was copywriting's

The committed social preview is now the umbrella's own render, byte for byte
(`node test/site_test.js` → `PASS: site — 42 checks`). Nothing about this pack changed;
the string it is rendered from did.

**`super-ux`'s role cell said *"what the interface must do and how it sounds"*** in the
routing map — the block's first content and its highest-salience surface — while the
precedence table 362 lines below gave *"how it sounds"* to `copywriting`, and this pack's
own router text says the same split. A reader who stopped at the first table routed copy
work to `/ux`, on the one router pair the block works hardest elsewhere to separate. The
cell is now *"what the interface must do"*, which is exactly what the precedence table
already said.

The umbrella carries the fixture that keeps it: no member's role may contain another
router's answer, with one declared exemption. Watched refusing the old string —
`super-ux's role answers copywriting's question: "how it sounds"`.

Board: `B-131`.

# Changelog

## 0.52.4 — the registry card stopped being four releases stale

`SKILL-CARD.md` carries the fields Anthropic's Skills-for-enterprise guidance asks every
organisation to keep — *"written so somebody who did not build this can decide"*. It said
`0.48.3` while this package shipped `0.52.3`.

**Nothing read it, so it could only drift.** The version moves in `package.json`,
`plugin.json` and `marketplace.json` on every release; the card was in no list. Measured
2026-09-01 across the family: **four of nine cards were behind** — this one by four minor
releases, `agent-stack` by ten.

The check refuses a card whose `Version` row disagrees with `package.json`, and refuses a
card that states no version at all: one a reader cannot see go stale is worse than one
that lags visibly. Watched failing before it shipped. `repo validator checks`
4617 → **4619**, recomputed by the command the fact itself cites rather than by hand.

**And the same defect as the sibling, in the same kind of place.** `test/validate.py`
carried an invalid escape sequence — a lone backslash-pipe in a non-raw docstring — which
Python already warns about and future versions will reject. It sat in a paragraph
explaining that *"the escape-awareness is the whole check"*. Now raw, zero escape
warnings — as `agent-stack`'s was an hour earlier, from a paragraph explaining how to
escape a pipe.

## 0.52.3 — the front matter gets read by a parser, not by a regex

- **`validate_front_matter_is_yaml` parses all 30 shipped front-matter blocks with PyYAML**
  (`B-033`): 7 `SKILL.md`, 15 commands, 8 `.mdc` mirrors. `front_matter()` reads a block line
  by line and never asks what a YAML parser would, so a `: ` inside an unquoted scalar turns
  the whole block into an invalid mapping and ships anyway — green here, refused by every
  installer that parses YAML, and the hub copy freezes on the previous version. The family
  shipped exactly that twice in twelve days (`sheleg-design` 1.37.4 and 1.58.0, both
  `mapping values are not allowed here`), so the remedy is **ported from the sibling that
  paid for it** rather than reinvented.
- **The two guards are the ones that history says matter.** It fails **closed** when PyYAML
  is missing, because a guard that discloses and passes when its tool is absent is the hole
  the first fix left open; and it refuses an **empty walk**, because globs that all match
  nothing is a moved directory rather than a clean tree. Both watched: `yaml` blocked at
  import, and the three globs renamed.
- **`YAML_SELF_TEST` is a permanent plant, not a one-off.** This gate's whole claim is that
  it sees what `front_matter()` cannot; a parser that stopped refusing that shape would leave
  it green on a clean tree forever, so the shape is re-checked on every run.
- PyYAML installed in both workflows: `setup-python` puts a different interpreter on PATH
  than the runner's system one, which is where PyYAML is preinstalled.

## 0.52.2 — the evals stop being a promise, and 0.52.1's stowaways get their record

- **The eval suite has dated rows instead of a vacant table** (SUX-04, family audit
  2026-08-29). 28 blind trigger probes — one fresh subagent per query per model
  (`haiku`, `sonnet`), each shown only the query and the 28 installed family skill
  descriptions — scored 14/14 on both models (train 8/8, validation 6/6), with every
  raw answer recorded. Three scenario runs in fresh scratch workspaces scored 12/12
  expected-behavior lines, each re-verified by running the pack's own linters over
  the agents' outputs (s01 design chain: `ux_lint.py` 0 errors; s03 rewritten copy:
  `brand pack is clean`). `test/evals/RESULTS.md` carries the per-query receipts,
  the scenario evidence, and a Method section that states the limits — single
  repetition per query against a README that asks for three, model aliases rather
  than snapshot ids, and the one non-hermetic call the s02 audit itself disclosed.
- **Two changes shipped inside v0.52.1 without a line of record, and this is that
  line.** The 0.52.1 commit was cut by a concurrent session from this working tree
  while this run's edits sat uncommitted in it, so they rode along:
  **`compatibility:` front matter in all seven skills** (SUX-02) — per-skill rather
  than one blanket string: the five UX skills name python3 3.9+ (stdlib only) for
  the linter this pack seeds, `ux-flows` names its optional MCPs (Figma for
  mockups, Refero/Mobbin/Lazyweb for reference screens) and what happens when they
  are absent, `ux-audit` states which half of the Figma check survives without the
  MCP, and the two brand skills name `docs/brand/lint.py` — and **`$schema` in both
  manifests** (SUX-05), the two schemastore spellings that resolve (the family also
  carries a `claude-code-plugin.json` variant, which 404s and was not copied);
  `claude plugin validate --strict` passes on both. Every `compatibility` value is
  a one-line YAML plain scalar with no colon-space sequence, parsed with
  `yaml.safe_load` before it ever reached a commit — the family shipped that exact
  defect twice this week (sheleg-design 1.37.4 and 1.58.0), and a planted
  colon-space here was caught by the same `mapping values are not allowed here`.
  Budgets measured: 153–358 chars against the standard's 500; the pinned house
  auditor returns 0 GAP on all seven. The class — a repo gate that parses shipped
  front matter as YAML — is filed as `B-033` rather than claimed, because this
  run's check was manual.

## 0.52.1 — a ledger row that machine-read as something else

- **`B-029`'s board row carried an unescaped `|` inside a backticked span**
  (`` `Kind: copy \| layout` ``), and markdown splits a table row on the pipe before any
  inline parsing happens, so the code fence does not protect it. Every column after the
  break shifted by one and `Status` read as whatever landed in its place: a `resolved` row
  that a machine reads as something else, in one of the two files this pipeline treats as
  its record. Escaped.
- **Found by the family umbrella's validator on this repository's own v0.52.0 tag**, while
  bumping the pin — not by anything here. `validate_ledger_table_shape` now asks the same
  question of both ledgers, and it is escape-aware because the first version was not: it
  counted `\|` as a separator and reported fourteen broken rows in files that had one,
  which is a detector nobody would have kept. Watched on the exact defect, and its limit
  measured and written down — `backlog.md` carries its header twice, so the guard catches
  a header that vanished entirely while a partial loss falls to the ratchet, which moved
  4488 to 4475 on that plant.

## 0.52.0 — the dash rule stops checking the glyph, humanization stops being a mode, and the pack learns to assemble a product

- **`B062` judges the dash's role rather than its codepoint.** `DASH` was the single
  character `—`, so a find-and-replace swapping it for `–` or for a hyphen with a space
  each side cleared every finding and left the habit untouched. Measured in the wild on
  trycomp.ai, 2026-08-30: twenty rhetorical dashes on one page and not one em dash among
  them. `normalise_dash_spelling` now reduces every spelling to the canonical mark before
  the three existing branches judge it, so the conjunction rule, the paired-dash rule,
  the locale allowances and the range and direct-speech exemptions all apply unchanged to
  all three spellings. The substitutions are length-preserving by construction and the
  finding quotes the raw text, so a report shows the characters the author actually typed
  rather than a mark they never used.
- **A dash alone in a table cell is an empty string, and now the code agrees.** `AT-06`
  has listed the no-value cell dash among the grammatical exemptions since it was
  written, and nothing implemented it: in any strict locale `| landing | — |` was
  reported. `TABLE_CELL_DASH_RE` blanks it before judgement. The doctrine is corrected in
  the same change, because it opened "The em dash is banned where it is rhetorical" while
  the rule it states is about the mark's role.
- **`landing-pages.md`, a new reference in `copywriting`: how a landing page is
  assembled, not how its sentences are edited.** Twenty rules with ids `LP-01..LP-20`
  across five layers — the offer, awareness and the shape it demands, the proof ladder,
  the action and the risk beside it, and the page as a machine — each carrying a verbatim
  example from a page that shipped. It closes six gaps the pack had: no offer
  architecture, no awareness-to-structure map, no proof ladder, no CTA or risk mechanics,
  no answer for a category nobody searches for yet, and no readiness criterion. The file
  ends in a runnable readiness check and says which of its rules no command can decide.
- **`validate_landing_coverage` is the answer to "what would notice if this fell
  behind?"** Table rows against sections in both directions, duplicate ids, a gap in the
  sequence, an id the readiness check names that no section defines, and the
  `copywriting/SKILL.md` link without which the reference ships to nobody. Four defects
  planted, each caught by its own message and reverted. The validator grows 4174 → 4197
  checks, `brand_lint_test.py` 89 → 93, and `test/floors.json` ratchets with both.
- **The evidence is in the repository, not in a summary of it.** `docs/research/landings/`
  carries the three teardowns the rules were extracted from — crowdreply.io, trycomp.ai
  and zerorank.ai, read 2026-08-30 as raw markup, rendered text and in a browser. Three
  independent pages committed the same four defects, and those four are the ones stated
  as classes: answers absent from the markup, one action under several labels, numbers
  that disagree with themselves, and the strongest proof filed one click behind the claim
  it proves.

## 0.50.0 — the templates ship where the texts say they are

- **`templates/` now travels with everything that names it** (SUX-01, family audit
  2026-08-29). Six shipped texts pointed at "the plugin's `templates/`" while the
  marketplace ships `./plugins/super-ux` and the directory lived at the repo root only —
  verified absent from all 13 cached installed versions, so `/brand-init`, `/brand`,
  `/ux-rule` step 2 and the three seeding skills dead-ended at a path that resolves in
  the one place users never run from: this repository's own checkout. The repo root stays
  the single source (the hard rules and the installer CLI read it);
  `test/sync_references.py` now mirrors the full tree into `plugins/super-ux/templates/`
  and the named seeds into each seeding skill's own directory — a skill installed by the
  skills CLI has no plugin root to reach up to — and the three skill texts say "this
  skill's own `templates/…`" while the three command texts keep "the plugin's
  `templates/…`", which is now true.
- **The class is gated, not just the instance.** `validate_shipped_templates` refuses a
  copy that drifts from its source and a copy with no source, in both homes;
  `validate_shipped_paths` requires every backticked `templates/…` or `scripts/…` token
  in a shipped text to resolve inside what actually ships — the plugin root for commands,
  the skill's own directory for skill files. Six defects planted, each caught by its own
  branch with its own message, each reverted; the sync verified idempotent across three
  runs. The validator grows 4111 → 4174 checks and `test/floors.json` ratchets with it.
- **`/ux-audit` admits its whole scope surface** (SUX-06). `copy` and
  `benchmark:<competitor>` join the `argument-hint` and the step-1 enumeration — the body
  has treated both as legal scopes since they shipped, while the two places an agent
  reads first omitted them.
- **Trigger hygiene in three descriptions** (SUX-07, SUX-08, SUX-11). `ux-scenarios`
  defers the empty-project start up the chain — vision and ux-foundation own it — instead
  of claiming "ANY new feature or project" unqualified; `copywriting` narrows "build a
  landing page / сделай лендинг" to the copy for it, naming sheleg-design as the visual
  half; `ux-flows` drops the bare "figma"/"фигма" claim and delegates the visual system
  and Figma variables to sheleg-design, mirroring its own body. Every phrase the family
  umbrella routes on remains a literal substring of its description — verified with the
  umbrella's own `advertised_check.js` (43/43, and watched failing against a dropped
  «мокап»).
- **Humanization runs by default, in every mode that produces text.** It was a mode you
  had to know to ask for, so the common path produced unswept drafts, and the one field
  that touched the question -- `Humanization pass:` -- existed **only in the template**:
  absent from `brand-contract.md`, absent from this pack's own `voice.md`, and read by no
  code anywhere. Two fields now answer the two different questions the old one conflated.
  `Humanization: on | off` is whether the pass runs, defaulting to `on` when absent;
  `Humanization pass:` names which implementation, defaulting to `own`. Write, Edit and
  Adapt each end in the sweep, positioned where it cannot be wasted: after the seven
  sweeps in Edit, per surface in Adapt. `Humanize` survives as the standalone mode for
  auditing text nobody is writing.
- **The state is visible in four places, because a pass that runs invisibly is
  indistinguishable from one that did not.** `voice.md` records it, every delivery of copy
  prints a status line naming the pass and what it changed, `/ux` and `/brand` report it
  in their status blocks, and `B064` refuses the three states that are defects: an absent
  field warns that the default applies unrecorded, an out-of-enum value errors, and `off`
  with no `Humanization declined:` reason errors. The enum joins
  `validate_status_enums_match_contract` from the day it was written rather than after it
  drifted, which required generalising `DOC_ENUM_DECL_RE` past the hardcoded `**Status**`
  so the next document-level enum is compared too.
- **`header_field` stops swallowing an aligned comment.** Standing instruction #3 fired on
  the first enum field the templates seed with a literal value beside a comment: the
  freshly seeded pack errored because the whole line, `# on | off; on is the default`
  included, was the value. Two spaces or more before a `#` now ends the value; one space
  does not, so a `Humanization declined: per ticket #431` keeps its reason.
- **Three references give the pack the assembly layer above its 241 tactics.**
  `onboarding.md` (`ON-01..ON-18`, in `ux-flows`) orders the path to the first value and
  rests on that value being defined first. `internal-screens.md` (`IS-01..IS-18`, in
  `ux-flows`) covers the screens nobody A/B tests, where the four states are one design
  and a list is a working surface rather than a directory of links.
  `product-frameworks.md` (`PF-01..PF-12`, in `ux-foundation`) carries the named decision
  models the pack had **none** of -- measured: Hook, Fogg, Kano, opportunity solution
  tree, AARRR, north star, time to value, value proposition canvas, forces of progress,
  switch interview, service blueprint and double diamond all returned zero occurrences --
  each with the failure mode that makes it worth knowing rather than worth quoting.
- **One coverage gate over four id sets, not four copies of one.**
  `validate_landing_coverage` became `validate_doctrine_set_coverage`, parameterised over
  `LP`, `ON`, `IS` and `PF`: rows against sections both ways, duplicates, sequence gaps,
  an id the readiness check names that no section defines, and the `SKILL.md` link without
  which a reference ships to nobody. A fourth hand-written copy of one comparison is the
  drift the gate exists to refuse.
- **The board went to zero.** All eleven open rows closed with a mechanism and a watched
  plant each, not with a status change. `B-029` got the decision it asked for rather than a
  filter: `strings.md` gains `Kind: copy | layout`, so an aligned option table is registered
  and exempt from the rules that would be judging typesetting, and `docs/brand/lint.py` now
  prints `brand pack is clean` where it printed a permanent warning. `B-028`: a `Coverage:`
  citation may name its subject (`path:start-end symbolName`) and `U078` resolves it, catching
  the drift a range cannot report about itself. `B-023`: `B005` asks `git log -L` about the
  cited entries rather than the whole file, so a jobs edit stops warning about personas.
  `B-005`: `U076` says a vision is still the seeded template instead of passing until someone
  self-declares `approved`. `B-001`: the seeded linter carries `VISION_RULE_TEXT`, `U077` warns
  when a target project's installed rule differs, and `validate_vision_rule_embed` keeps that
  third copy honest. `B-030` and `B-031` get contract-parity gates; `B-032` gets `test/evals/`
  with four cases whose anchors must still resolve.
- **Two of the eleven turned out not to be what the board said.** `B-021` asked for a
  reachability arrow that had existed inside `validate_bp_index` since before the row was
  filed; a duplicate check was written, caught by planting `BP-242`, and deleted rather than
  shipped. What was genuinely missing ran the other way: a routing row pointing at a `BP-NNN`
  the catalog does not define, invisible because every check in that function starts from the
  catalog. `B-019` did not reproduce in four probes; it had been fixed by an uncredited
  refactor, and the class is now mechanical — the report prints each distinct message once and
  names any duplicate emission.
- **The refreshed code graph asserted a number nobody computed.** `B-022`'s refresh ran
  unattended (1149 nodes, 1801 edges, built from `6348b641`), and 58 label fields said
  `82 tags, 206 practices` about a catalog of 241 and an index that states no counts at all —
  cached across refreshes, and read with the authority of a machine. Corrected, and gated by
  `validate_graph_claims`, narrowed to `label`/`norm_label` because a node summarising a past
  defect legitimately quotes an old number, and one of them does.
- **The bytecode cache could defeat a planted defect, which is this project's unit of
  evidence.** CPython invalidates on `(mtime, size)`, so swapping `"B064"` for `"B999"` --
  identical length -- and reverting inside the same second left a `.pyc` the interpreter
  considered current: the revert ran the plant and the transcript reported a defect no
  longer in the file. Observed live during this run's own plants. Both harnesses now set
  `sys.dont_write_bytecode`, verified by plant-then-revert-in-second going red then green
  with no cache clear.

## 0.49.1 — the skills handoff refuses the shadow it used to create

- **The skills-menu item now consults the target home before delegating.** `npx skills add`
  auto-detects Claude Code and writes a plain `~/.claude/skills/super-ux` copy even when
  claude-code is never picked, and on a machine where super-ux is installed as a Claude
  Code plugin that copy shadows the plugin and serves the version it was copied from
  forever. The handoff now reads `~/.claude/plugins/installed_plugins.json` — the record of
  what is actually installed, under any marketplace name — and refuses with **exit 3**, the
  remedy in the refusal (`claude plugin marketplace update super-ux`, `claude plugin update
  <spec from the JSON>`, and the family launcher), and `npx super-ux --force` as the named
  override. The `plugins/marketplaces/super-ux` directory is kept only as the fallback
  signal: it under-reports, because a directory-sourced marketplace has no dir there and
  plugin names differ from marketplace names. A missing or corrupt JSON reads as "no
  plugin" — fail open, never crash. Only the Claude Code channel is gated; `--cursor`
  installs into a project beside the plugin exactly as before. Canon:
  make-skill v0.25.0, `references/distribution.md` §3; reproduced live 2026-08-29 when a
  bare `npx @ssheleg/telegram-dev` shipped three shadows past this exact class of hole.
- **A successful run now ends by saying how the next version arrives** — `npx
  super-ux@latest` for this member, the family launcher for every channel at once. An
  installer that never mentions updates has still chosen an update model: never.
- **`test/installer_test.js`** runs both installers against throwaway HOMEs — the
  plugin-present refusal (exit 3, remedy, nothing delegated, nothing written), the
  differently-named marketplace spec in the remedy, `--force`, corrupt-JSON fail-open, a
  prefix collider (`super-ux-extra@x`), the marketplaces-dir fallback, the fresh HOME, and
  that `install.sh` never touches `~/.claude` at all. Wired into `npm test` and CI; watched
  failing against the pre-fix installer (7 of 10 cases red, the plugin-present case
  delegating with exit 0) before the fix was un-stashed.
- SCN-016 and SCN-017 record the refusal and the update line in `docs/ux/scenarios.md`;
  SCR-05 gains the `refused` state; the string registry carries the new copy and the
  `refused:` prefix joins the state vocabulary.

## 0.49.0 — the humanization pass names what it cannot prove

- **`ai-tells.md` now says these markers are not a verdict, and who they misjudge.** Every
  marker is more common in model output; none proves a machine wrote anything, and the
  failure is not symmetric. Independent audits found false-positive rates **above 60% on
  non-native English writers** (Liang et al., Stanford, *Patterns*, 2023). Three rules bind
  the rest of the file: never say a text was AI-written, only which markers appear at what
  density; never gate on a marker count; and a second-language writer is not a defect to be
  edited into fluency they did not ask for.
- **Other implementations are named, compared and pointed at** — `blader/humanizer` and
  `conorbronsdon/avoid-ai-writing`, with a table of what each does that this pack does not
  and the reverse. Reach outward for an audit that changes nothing (only one has a
  detect-only mode), for long-form prose, or when the writer has a sample of their own
  writing to match. Stay here for product copy: the brand pack's registers, terminology and
  canonical facts are the constraint, and a general-purpose humanizer does not read them.
  Two guards remain this pack's own — the 50% change-rate refusal and the mandatory
  semantic-preservation check — and neither external implementation carries an equivalent.
- **`voice.md` gains an optional `Humanization pass:` field**, and its absence is
  meaningful: it means nobody has been asked. `brand-voice` Init asks once and records the
  answer; `copywriting` reads it rather than asking again. A value naming a tool that is not
  installed falls back to `own` and says so — a missing optional tool must not stop copy
  being written.
- `npx sshlg-skills humanizers` lists what is installed on the machine.

## 0.48.4 — the channel that sends the installs, on npm too

- The `skills.sh` badge and the canonical `homepage` reached GitHub in the previous cycle and stopped
  there: npm serves the README and the metadata from the last **publish**, so the package
  page still showed a badge-less README and a homepage pointing at GitHub.
  This release carries both across.
- No behaviour changes. Cut because a change that lands on `main` and never publishes is a
  change the package's own readers cannot see.

## 0.48.3 — the shared seam is explicit

Both shared validators now state `diverges: none`, completing the umbrella
mechanism contract.

## 0.48.2 — shared guards identify their owner

The eval and social-preview validators now declare their umbrella-owned shared
mechanisms, so family drift is checked without pretending the copies diverge.

## 0.48.1 — the UX chain gets an installable public front door

A root skill card now states the boundary between behavior, copy, visuals and
integrations. Portable trigger and behavioral evals cover the scenario chain,
audit and brand path without pretending they have been run against a model. The
README opens with one install and one cancellation-flow request; CI adds the
pinned house audit, eval plant and social-preview check.

## 0.48.0 — 2026-08-22

**BP-235..241 — products with a long time-to-value.** Measured on
`babylovegrowth.ai`, the same category as BP-216..234's reference and the opposite answer to
almost every question: where that product is dense and instrumented, this one is patient.
Results arrive over months, most of a new account's numbers are zero on day one, and the
design's whole job is to make that read as *early* rather than as *broken*.

* **A disconnected source renders at the size its data would** (**BP-235**) — full card, one
  sentence naming what connecting buys, the button. The dashboard's shape then does not change
  when a source is added, and a new account reads as unfinished rather than empty.
* **Price the vanity metric in the currency the reader already has** (**BP-236**) — *80K
  potential reach · $641 to buy this visibility via Ads*. A figure whose scale a user cannot
  judge is a figure they discount.
* **If value takes months, put the months on the dashboard** (**BP-237**) — named phases with
  ranges, beside the empty numbers rather than in an onboarding email. On these products the
  first weeks look identical to failure, and the churn that follows is a reading error.
* **A composite score shows its parts in the same glance** (**BP-238**) — the ring tells a user
  their state, the decomposition names their next action.
* **The card that is working says so on itself** (**BP-239**) — the complement of BP-217:
  that one says do not blank a surface with a value, this one says where the progress signal
  goes instead.
* **A guarantee under the CTA is the other way to remove the risk** (**BP-240**) — BP-229's
  sibling. Two doors remove the *password*; a bounded guarantee removes the *bet*.
* **Two card levels, and the difference between them is the grouping** (**BP-241**) — different
  radii, one step of tint, and a flattening rule below tablet as part of the pattern rather than
  a fallback.

`practice-selection.md` gains three artifact rows: integration flow, long-time-to-value product,
and the dashboard row widened to reach the new set.

## 0.47.0 — 2026-08-21

**BP-216..227 — product dashboards.** The catalog had `Web apps, forms & performance` and
nothing about the screen a person opens every morning to decide what to do next. A dashboard
fails in ways neither a landing nor a report does: it goes stale without saying so, it encodes
state in a colour nobody can separate, and it blanks itself on every reload to prove it is
fetching. Twelve entries, every one measured on 2026-08-21 against a production surface
(`outrank.so/dashboard`, whose product half runs Semrush's Intergalactic), with the measurement
named in each `Why`.

The ones that change how a screen is built: the first block is *what to do next*, not what
happened (**BP-216**); a data surface **dates itself instead of blanking** (**BP-217**); a
number is a shape and is led like one — 32px at 32px leading (**BP-219**); a tint encodes the
**category**, never the state (**BP-220**); one 100% bar with a dot legend costs a text line
where a pie costs six (**BP-221**); a row **tints, it does not lift** (**BP-224**); an empty
cell **keeps its border**, because the grid's shape is the information (**BP-226**).

**BP-228..234 — the long SaaS landing, measured end to end.** A 20 806px production page, its
fourteen sections listed in order with the buyer question each one answers, and the finding that
the sequence is ordered by *when the question occurs* rather than by feature importance — the
mechanism precedes the capabilities because a buyer who does not believe the *how* does not read
the *what*. Section 12 repeats the hero **verbatim**, which is what lets a reader who scrolled
past it decide without scrolling back.

### Three old entries now say where they stop

This is the half that matters more than the new ids. A newer practice that quietly disagrees
with an older one leaves an auditor applying whichever they read first.

* **BP-117 — "one primary action per landing page"** is about *intent*, not button count, and it
  was regularly read as the second. **BP-229** states the difference: two buttons that begin the
  same job — an SSO door beside a credentialled one — are one action with two doors, and removing
  the ghost in BP-117's name raises friction in the name of a rule about focus. BP-117 now
  carries that pointer in its own entry.
* **BP-058 — "skeletons/progress for longer work"** now says it applies where there is **no
  previous value**. On a surface that has already drawn data, a skeleton on re-fetch destroys a
  reading the person could use, to signal a fetch they did not ask for.
* **BP-059 — "no info by color alone"** points at **BP-218**, which carries the CVD numbers that
  make it a measurement rather than a principle: two of the reference's own status hues separate
  by 6.9 under tritanopia.

Taxonomy gains `dashboard` and `data-density`. `practice-selection.md` gains six artifact rows —
long SaaS landing, dashboard home, KPI card, dense table, in-product upgrade prompt — because an
entry nothing routes to is an entry no skill can reach.

## 0.46.0 — 2026-08-20

**The check that decides whether a public number is real accepted any substring of the
others.** `B030` built its corpus as `" ".join(values)` and then asked whether the figure
was *in* that string with the spaces removed — so the eight facts became the character
sequence `7158215243770+`, and every substring of it was "sourced". Watched: appending
*"super-ux is used by 58 teams and ships 1582 checks."* to `README.md` — a declared public
surface — left `docs/brand/lint.py` printing `brand pack is clean`, exit 0. This is the one
check the brand hard rule exists to enforce. Values are normalised and compared one at a
time now, against a set.

Twelve more, each reproduced before it was fixed and each new guard watched failing:

- **`facts.md` had no duplicate-key rule**, and a second `| skills shipped | 99 |` row not
  only stood beside the first but widened the sourced corpus, making `99` quotable in
  public copy. `B033`.
- **"every row names a command that recomputes it" ran nothing.** Two rows named no
  command, and `repo validator checks` read 3500 against a measured 3539. Each `Source` is
  executed now; the self-referential row runs the validator as a count-neutral child, and
  the row that cannot be recomputed here is marked and **disclosed** rather than skipped.
- **`Coverage:` line ranges were never resolved** — `bin/super-ux.js:99000-99999` in a
  396-line file passed. `U071`/`U072`, and the fourteen live citations that had drifted are
  rewritten.
- **The job layer was invisible to every rule.** `ids()` required `### PREFIX-NN: <name>`
  and this repo's jobs carry no name, so two identical `JTBD-01` ids passed. Entries are
  matched by id now (`U073`, `U074`), and the three jobs carry the five fields the contract
  requires.
- **Nine `Status:` values sat on layers no enum covered**, and `voice.md` read `approved`
  where the contract declares `draft|validated` — it worked only because the linter
  compared `== "draft"`. Enums are declared per layer and parity-checked; the two layers
  that legitimately have no status say so (`U075`, `B034`).
- **The Cursor umbrella shipped a three-release-old system**: four workflows named of eight
  rules shipped, with `vision`, `brand-voice` and `copywriting` at zero mentions. It must
  name every shipped skill now.
- **The `AT-` marker set had ids and no gate**: deleting a whole section while leaving its
  table row kept the validator at `OK (3539 checks)`, exit 0. Covered both directions.
- **The board reused ids** — `B-011`–`B-013` in two tables with different content — and
  nothing read the board at all.
- **The hard rule had four payload homes and `HARD_RULES` paired two** (320/2102 words and
  chars against 349/2284 and 348/2204). Anchor parity now, derived from the template, with
  the one legitimate exemption as data.
- **The front-matter budget measured the wrong thing**: the whole block against 1024
  instead of `name` ≤ 64 and `description` ≤ 1024 separately. No live violation; both
  directions planted.
- **One pack, two opposite exit policies.** `brand_lint.py` returned 1 on warnings-only
  while `ux_lint.py` returned 0 unless `--strict`, so thirteen of thirty-seven codes turned
  `npm test` red while printing `0 error(s)`. `--strict` added, warnings non-blocking by
  default, and the three homes of that rule reworded in the same change.
- **The literal extractor could not cross a newline**, so `usage()` — the most-read UI
  surface the pack has — was invisible to the string registry. Sixteen findings came out of
  it on the first run.

Checks: `validate.py` 3539 → **3667**, `brand_lint_test.py` 77 → **89**, `ux_lint_test.py`
106 → **133**, with `test/floors.json` raised to the measured per-block delta.

Two findings came out of planting rather than reading: per-line template extraction
produced six mid-sentence fragments no registry row can hold, and a reworded README line
tripped the pack's own AI-tell check.


## 0.45.0 — 2026-08-19

**The requirement layer could not see a requirement with no observable.** The contract said
one was unfinished without it; nothing read for one. `ux_lint.py` never opened a scenario or
user-story body — no rule looked for `Expected result`, `Acceptance criteria` or a success
metric — while the layer *below* it, screens, had carried that check since U055/U056.

The dogfood is the argument: this pack's own 15 scenarios all read `Status: implemented`,
**none cited any code**, no test touched `bin/super-ux.js`, and `npm test` exited 0 over all
of it. A chain that demands the layers before code could not tell that its own chain closed
on nothing.

### U060–U065 — the requirement layer gets read

A scenario or story with no observable is refused; a scenario claiming `implemented` must
cite code that resolves. `U055/U056` and `U064/U065` now share one owner (`coverage_claim`),
so two layers cannot answer the same question differently. All 15 own scenarios now cite
implementing ranges in `bin/super-ux.js`, each read rather than recalled.

### `Product:` — a shipped scenario stops counting as a validated one

`unobserved | observed | contradicted`, distinct from `Status`, with **no floor and no
target**: absence means `unobserved`, and neither `unobserved` nor `contradicted` fails
anything. Outcome evidence often cannot exist yet, and saying so is not a defect.

Four things stop an audit promoting it: `U068` refuses everything an audit produces as an
outcome signal — a `file:line`, a PASS/FAIL verdict, a path into `docs/ux/audits/`; `U067`
refuses `observed` with no signal; `U066` refuses an out-of-enum value outright, because an
unrecognised value read as *no state* is how an enum drifts; and both homes of the
after-a-run step carry **The audit never writes `Product:`**, with a gate that fails if
either loses the sentence.

**All 15 own scenarios now read `unobserved`.** Before this they read as fifteen validated
bets, because `implemented` was the only state the chain had.

### Found while there

The screens status enum had **already** drifted: the contract declared five values and the
linter matched four, so a `blocked` screen read as having *no* status and `U021` silently
stopped applying. Fixed. Two further instances of the same class filed rather than hidden.

The long spelling (`**Expected result:**`) is canonical; the short forms are still read, and
`U069` warns rather than errors — failing a live project over a synonym is the false positive
that gets a whole family switched off.

## 0.44.0 — 2026-08-17

**Three lint codes for the two layers whose claims nothing could check.** `U055`, `U056` and
`U057`; the linter goes 43 → **54** fixtures, each code carrying the defect it must catch and
the shapes it must **not**.

### A `Coverage` claim is a claim about code (`U055`, `U056`) — closes #6

Measured in a real project: five screens carried `partial` in the index while their entries
named no file, and one said `none — no per-account memberships route exists` about a route a
task had built the day before. **Two fields of one record contradicted each other for a day,
and neither was checked against the other.**

- `U055` (warn) — a `Coverage` value other than `none` that names no file. A claim about code
  citing no code cannot be checked by a script *or* by a reader, who has nowhere to go to
  disagree.
- `U056` (error) — a cited path that does not exist. A stale citation is the same defect with
  the means to notice.

**The path pattern is deliberately narrow and that was the design decision, not a detail.** It
requires a slash **and** an extension, so `src/routes/x.tsx:12` matches while *"partial —
client/server split"* and *"the route is built"* do not. A wider pattern was tried first and
flagged three correct prose entries — the false positive that gets a rule switched off inside a
day, taking the real check with it.

### A flow's verdict must be measurable, not inherited (`U057`) — closes #7

The chain is foundation → flows → screens → scenarios, and audits in practice attach to the two
**ends**. Flows sit between and are the only layer with no artefact of their own: a flow is a
path across screens, so the cheap thing is to derive its verdict from theirs — and a derived
verdict presented as a measured one is how one project's `flows.md` carried **no code verdict
for 42 flows across three weeks**, its header delegating to an audit that had itself derived
them, and a later scenario walk refuting that audit on every clause without touching flows.

`U057` does not verdict a flow. It reports the flows for which **no verdict can be measured at
all** — the state that was invisible. A flow naming no screen stays `U010`'s subject, not this
one.

Run against this repository's own chain: clean.

## 0.43.0 — 2026-08-17

**`ux-flows` has told agents to sweep real products before inventing a flow since 0.35.0,
and no prompt could ask for it.** The body carries the rule — *"Real flows off the shelf,
before you invent one"*, with Refero read for structure and Mobbin looked at for whether it
reads — and `references/funnel-research.md` FR-01 collects live competitor funnels. The
`description` said flows, wireframes and task analysis, so `найди референсы дизайна`,
`подбери референсы` and `find reference screens` all reached no route at all.

The word is now advertised: the funnel clause reads *"read against reference screens from
products already in the category"*, which says the same thing in fewer characters and makes
`reference screens` / `референсы` routable.

**Why this skill and not the visual one.** `sheleg-design`'s own `DESIGN_SYNC_BRIDGE.md` §4
opens with *"A reference sweep answers what a good version of this screen contains —
sections, hierarchy, content order. It never answers what it looks like."* Structure is this
chain's ground, so the unqualified word lands here; the visual half (`visual reference` /
`визуальные референсы`) went to `sheleg-design` 1.40.0 in the same pass. A prompt naming both
— `нужны визуальные референсы` — now raises both routers, which is the wanted answer.

**Budget:** 893 → 940 characters, 30 free under the 970 working limit; the rewritten funnel
clause paid for most of the addition.

## 0.42.0 — 2026-08-17

**The pack has carried the growth vocabulary since long before it could be asked for it.**
Counted across `plugins/super-ux`: **448** mentions of funnels, **499** of onboarding, **493**
of paywalls, **196** of retention, **171** of activation, **100** of referral. `retention`,
`onboarding`, `paywall`, `winback`, `lifecycle`, `activation`, `virality` and `referral` are
first-class tags in the practice taxonomy. `references/funnel-research.md` is 190 lines of
method, `FR-01`..`FR-07`. And not one of those words appeared in any skill's `description`.

That mattered more than it looks, because **a description is a routing surface**. The
umbrella's prompt hook may only fire on words the skill itself advertises — the fixture that
enforces it does a literal substring check — so fifteen of fifteen realistic growth prompts
reached no route at all: `как повысить ретеншн пользователей`, `спроектируй воронку
активации`, `добавь пейволл после онбординга`, `improve user retention`, `reduce churn on the
trial`, `add a paywall screen`. Measured by `test/route_coverage.js` in the umbrella.

### Two descriptions, and which word goes where is not a preference

`funnel-research.md`'s own `FR-07` already says where each finding lands, so the split follows
it rather than convenience:

| Word | Skill | Why that one |
|---|---|---|
| funnel, onboarding, paywall, activation funnel | `ux-flows` | *"The funnel's step chain and its branches → `docs/ux/flows.md`"* — and this skill's body already names the chain (ad → landing → quiz → loading → offer → paywall → checkout → success) |
| user retention, churn | `ux-foundation` | *"Who the buyer is, what job they are hiring the product for → `foundation.md`"*; a journey covers before, **during and after**, which is where retention is won and churn starts |

Neither skill could carry the other's words honestly, which is why the route now fronts two
skills rather than one.

### The English half is phrases and the Russian half is bare words, and that was measured

A first pass advertised the bare `activation` and `retention`. The umbrella's matcher stems
them to `activat-` and `retent-`, and the probe caught the cost immediately: `activate the
virtualenv` and `activate the feature flag` routed to `/ux`, and so did `retention policy for
logs`. The English words became `activation funnel` and `user retention`; «активация» and
«ретеншн» stayed single words, because nobody here writes «активация» about a virtualenv.
After the change all three noise cases are silent and every growth prompt still routes.

**Budget:** `ux-flows` 592 → 884 characters, `ux-foundation` 401 → 619. Both inside the 970
working limit with room left, which was the point of not spending it on the bare words.

`python3 test/validate.py` → `OK (3500 checks)`; the full gate green.

## 0.41.5 — 2026-08-16

**`copywriting` now answers when somebody asks for a landing page.** The unqualified
`сделай лендинг` and `build a landing page` reached no route at all — a landing is the
canonical two-craft surface, and the ask for one arrived at neither craft.

Both phrases are advertised here and in `sheleg-design`, so they reach the two together,
which is what the family's composition order says a landing needs. Verb phrases rather than
the bare noun: with a bare `лендинг` trigger, `напиши текст для лендинга` picked up a
visual route it never asked for. With the phrase it stays copywriting alone, measured
before and after.

## 0.41.4 — 2026-08-16

**This gate can now see an invariant it breaks one repository away.** The family umbrella
routes work by matching a prompt against a table in `lib/triggers.js`, and every trigger
there must be a word this skill's own `description` advertises. Nothing here knew that
table existed. On 2026-08-16 `sheleg-design` 1.37.0 shipped green having dropped a phrase
that was still a live trigger, the umbrella found out minutes after the tag, and it cost a
patch release — because the member releases FIRST and the umbrella re-pins after.

`test/validate.py` now asks the umbrella's own checker (`test/advertised_check.js`), which
reads the module the hook itself calls. **No copy of the table lives here**, so there is
nothing to drift. With no umbrella above this checkout — a standalone clone, and CI — it
discloses rather than passing, because a check that cannot look must never read as one
that looked.

Watched refusing a real drop before shipping: every one of the seven members carrying
routed triggers had one of its own advertised phrases removed and every one of them failed
its own gate.

## 0.41.3 — 2026-08-16

**`facts.md` is a document, not only a facts table.** `facts()` took any
six-column row anywhere in the file, and a project that keeps a product ledger
there has one whose columns mean something else entirely:
`Product | App Store name | id | Released | Sold | Publisher today`. Its **Sold**
year landed in `Review`, so three completed sales produced "was due for review
on 2022" warnings, and the ledger's own header row became a fact called
`Product`. Four phantom rows in a registry of 43.

Scoped by header now — a table qualifies when its first column says `Fact`,
which is the only thing in a markdown table that declares what its columns
mean. A `tables()` helper groups rows per table beside the existing
`table_rows()`, which flattens every table in a file and is right for a caller
that wants every row.

Found on `sshlg.me` and fixed there first, in that project's copy of the linter,
where it would have been overwritten by the next sync — a plugin-owned file
edited in a downstream project serves that project until the day it silently
does not. Ported up with its fixture, which was watched failing.

### Three more changes landed in this version, from a concurrent session

They carry the same `0.41.3` in every manifest and sit inside the tag, so the
entry names them rather than leaving a release whose changelog describes a
quarter of it. Summarised from their own commit messages, not re-derived.

- **`B021` reads the built page** (`6fe309e`). The registry records what a
  reader sees, and the check looked for that string in component *source*, where
  an interpolated value never appears literally and an inline `<strong>` or `<a>`
  splits a sentence the registry stores whole. On `sshlg.me` that was five errors
  with no honest repair — hardcode the number and lose the guarantee it is
  derived, or delete the rows and lose the check. `rendered_text()` now reads
  `dist`, `build`, `out` or `_site`, first that exists, and a project that does
  not build keeps the byte-exact source comparison. The message says which of the
  two it checked. **This closes the last class `sshlg.me` had open**: that
  project went from five errors to zero.
- **The same fix, applied to the script this package actually ships**
  (`213ae1b`). It had gone into `docs/brand/lint.py`, the dogfood copy, while
  `plugins/super-ux/scripts/brand_lint.py` is what `package.json` ships and what
  `validate.py` reads as the authority — so it reached this repository's own
  linting and no installed project. The pair check was red the whole time and the
  commit went in without running it, which its author recorded rather than
  quietly fixed.
- **`guardedFiles` covers the linters** (`3e133ab`). The manifests, the evidence
  ledgers and `test/validate.py` were guarded; `docs/brand/lint.py` and
  `plugins/super-ux/scripts/brand_lint.py` were not, and that is exactly where two
  agents collided on 2026-08-16 and lost about twenty minutes. "A config that
  guards what is edited rarely and leaves what is edited hourly open describes a
  project nobody works on."

**The tag was placed on the tip rather than on the release commit**, by the run
that wrote the section above this one: `git tag` was given no target and took
`HEAD`, which by then carried three commits it had not seen. Left where it is —
a published tag is not moved — and the entry was widened to match it instead.
Both are recoveries from the same mistake, and only one of them is safe.

## 0.41.2 — 2026-08-16

> **Never released on its own.** There is no `v0.41.2` tag and no `0.41.2` on npm,
> so `npm install super-ux@0.41.2` and `git checkout v0.41.2` both fail. This section
> describes work that shipped inside a later version. The note is here because
> the section reads as a release (2026-08-17, umbrella `B-71`).

**A source file is not prose, and the prose rules were reading all of it.** On
`sshlg.me`, whose `Sources:` block points `marketing` at `src/data/*.ts`, that
produced 20 rhetorical-dash errors inside `//` comments and 7 keyword-stuffing
errors on `const`, `string`, `name` and `category`. Twenty-seven standing errors
that no edit to the copy could clear, sitting in a report meant to be read. The
failure is the same one 0.40.1 fixed from the other direction: a check nobody
can act on gets ignored, and then it is not a check.

For a file with a code suffix the body is now its **copy** — the string literals
`_looks_like_copy` already accepts, which is the definition `B022` sweeps with.
A comment is addressed to a maintainer and an identifier is not a word.

Three things this had to get right, and the first two were found by getting them
wrong:

- **Comments are stripped by a scanner, not a regex.** `"https://x"` contains
  `//`. The first attempt used a pattern and immediately reported a rhetorical
  dash inside a comment that quoted a phrase — in the very change meant to stop
  reading comments.
- **`${...}` is substituted, not dropped.** `CODE_FRAGMENT_RE` rejects any
  literal carrying an interpolation, so without this every interpolated string
  would fail `_looks_like_copy`. On the site that would have silently dropped the
  whole biography. It turns out interpolated copy was **not** covered before
  either: the fixture for it fails against 0.40.1, so this widens coverage rather
  than preserving it.
- **A literal with no space is skipped.** `"@/data/site"` counted as copy would
  put `data` into the density figures.

Ten fixtures, five end-to-end and five on the scanner directly. Four were watched
failing before the fix went in; the fifth end-to-end case is the boundary that
must not move — a rhetorical dash in a rendered string is still an error.

**And the same sentence has a second half: a source file is not a *document*
either.** `B051` measures keyword density, which is a property of the page a
reader meets. A project that keeps its copy in `src/data/*.ts` splits one page
across seven files, so measuring each file separately measures the split. On
`sshlg.me` that produced six errors — `co-founder` at 2.0% of
`track-record.ts`, `account` at 1.2% of `site.ts` — while the rendered page
carried **nothing above 1%** and those two words sat at 0.07% and 0.04%.

Code files are pooled into one document for that check; markdown sources are
not, because there one file really is one page. A pooled finding names the set
rather than a file, since no single file is the defect. The fixture that proves
it has a twin that must keep firing: a word genuinely dense across the whole
pool is still an error.

Measured on `sshlg.me`: **32 errors to 5**, and the five that remain are one
class — `B021` on registry rows whose text carries an interpolated count or an
inline link, which needs a linter that reads `dist/` rather than `src/`. One
real finding surfaced on the way: a rhetorical dash in live copy that had been
buried under twenty false ones.

## 0.41.1 — 2026-08-16

> **Never released on its own.** There is no `v0.41.1` tag and no `0.41.1` on npm,
> so `npm install super-ux@0.41.1` and `git checkout v0.41.1` both fail. This section
> describes work that shipped inside a later version. The note is here because
> the section reads as a release (2026-08-17, umbrella `B-71`).

**`B024` fined the writer for meeting a threshold this pack sets.** The
sentence-case check reads any capitalised word inside a sentence as Title Case,
and a contraction of the first person survived every exemption it had: `I'm` is
not upper-case, is in no entity table, and starts with a capital. So it fired.

That is not a cosmetic false positive. `formats.md` asks for **4 to 8
contractions per 1000 words** on a published surface and names their absence as
"the single loudest reason our prose reads as assembled" — and the first-person
contractions are the loudest ones available. The check and the threshold were
pulling in opposite directions, and the only repair available to a writer was to
delete the contraction the pack had just asked for. Found on `sshlg.me`, where
three registry rows tripped it on 2026-08-15 and none of them was miscased.

`I'm`, `I'll`, `I've` and `I'd` are now exempt, with either apostrophe. Nothing
else is: `We're` and `They'd` inside a sentence really are miscased, and the
capital is grammar only for the first person. Both halves are fixtures, so the
exemption cannot widen without a test saying so.

## 0.41.0 — 2026-08-16

### Added

- **`ux-audit` checks its batches against each other before the report reads as one
  answer.** The batches run independently — in a large scope, in parallel subagents that
  never see one another — and the summary then turns them into a single verdict. That is a
  convergence, and a convergence trusts its inputs because they arrived.

  Four things to look for: one root cause wearing several finding ids, which splits its own
  priority across three rows; two batches that contradict on one screen, PASS in one and
  FAIL in the other; a batch that returned nothing where its scenarios touch a screen
  another batch flagged, since an empty result and an unrun batch look identical in a
  summary; and a verdict whose evidence is weaker than its neighbour's, presented at equal
  weight.

  `Cross-batch: clean` is the answer most audits write, and writing it is the point. The
  scenario base already had the same mechanism one layer up — `ux-scenarios` step 4,
  *scenarios that contradict each other* — and this is it applied to the audit's own
  outputs rather than to its inputs.

## 0.40.0 — 2026-08-14

A 42-page practitioner guide on building web2app funnels was read against the
catalog, and most of what it teaches was already here: BP-001 on adapting rather
than copying, BP-005 on loading screens that sell, BP-010 and BP-029 on echoing
the stated goal, BP-116..123 on the surfaces, BP-124..129 on the web2app chain.
What was missing had one thing in common. **Every gap was something that fails
without changing what the funnel looks like.**

Five practices, `BP-211..215`, in a section named for that property:

- **BP-211 — personalize the wording, never the price.** The catalog said to
  branch the offer on the quiz answer and never said where the branch stops.
  Two rules: the product and its price are identical across every branch, and
  the branch has a default, because the person who skips the question currently
  meets an empty offer at the moment of highest intent.
- **BP-212 — publicly addressable before it takes money, instrumented before it
  takes traffic.** Both orderings are forced rather than tidy. A provider
  confirms a charge by calling a public address, so the whole post-payment path
  is untestable on a laptop; and traffic bought before instrumentation cannot be
  read afterwards, because the sessions are spent and the losing step was never
  recorded.
- **BP-213 — a collected answer carries three decisions no screen shows:** who
  may read the row, when the person was told, how they get it deleted. `[GDPR]`
  Art. 13 fixes the timing at *the moment the data is obtained*, which is why
  this is a design-time decision and not a launch-week chore, and Art. 17 is why
  a funnel with no deletion route has promised something it cannot do.
- **BP-214 — the legal text is sourced, never generated.** A policy is a
  statement about your own processing, so generated prose is a fabricated claim
  about it: BP-194's failure with a regulator for a reader.
- **BP-215 — access after payment is a ladder, and the link carries a token
  rather than a person.** Each rung above the first adds a service that fails
  independently of the funnel, so the rung below stays reachable; and a URL is a
  bearer credential, so what is encoded in it is readable by everyone it is
  forwarded to.

**BP-118 gained the unit web funnels actually anchor on.** It stopped at the
monthly equivalent of an annual plan. The per-day figure is the same mechanism
one step further, and it ships beside the billed amount rather than instead of
it, because a price the buyer is never charged is the shape a dark pattern takes
here.

**`funnel-research.md` is new**, and it is a method rather than a practice:
`FR-01..FR-07`, from finding the funnels running in a category to landing each
finding in the chain. It leads with the constraint that makes it a method at
all — you cannot see anyone's revenue, so every signal is spend, and spend is
somebody else's judgement you cannot inspect. Its last section names the step
chain a corpus keeps producing and the practice specifying each step; its final
section is what the method **cannot** do. Carried by `ux-foundation` and
`ux-flows`, and by neither of the other five, because a link in a skill is a
shipping instruction.

**Two new gates, because a numbered set with nothing counting it is a promise.**

- `validate_reference_contents` — every `## Contents` anchor in a reference
  resolves to a heading in that file. The Contents list is the one part of the
  shelf that goes stale by somebody else's edit: rename a heading and the entry
  above it still looks right. 150 checks over 21 files, and it recorded the
  slug rule it needed to get right, because a checker that collapses the double
  hyphen an em dash leaves behind reports 22 failures on a clean shelf.
- The `FR-01..NN` range check, in the form `PRN-01..NN` already had, so a step
  added without updating its carriers goes red in all three of them.

Both were watched failing against planted defects, each isolated so only the
branch under test could fire it. Disarming the anchor loop drops the count from
3500 to 3354, which the floor ratchet refuses on its own.

`docs/brand/facts.md` was recomputed rather than edited: `B030` went red on
`215` in the README before this run had touched the table, which is the sequence
the check exists for.

## 0.39.0 — 2026-08-14

The em-dash reflex has been in `ai-tells.md` since the verbal identity layer
shipped, graded S2 and worded "one or two in a piece is normal". The linter
never looked for it: `S1_MARKERS` held twelve string literals, none of them a
dash. A title ending in a full stop was caught only inside the string
registry, by `B026`, so every heading and page title outside it went
unchecked. Both are now checks.

**The rule is a distinction, not a ban.** A dash standing in for a full stop,
a comma or a colon is out. A dash the language requires stays, because a
global ban makes Russian ungrammatical on its first line: the copula
(«Москва — столица»), numeric ranges and direct speech are orthography.

- **`B062`** errors on what can be established without parsing grammar: a
  dash before a coordinating conjunction, which is always a comma's job and
  which a copula dash never takes, and paired dashes bracketing an aside
  inside one sentence. In a locale with no grammatical dash it errors on
  every dash that is not a range. Where a locale has one, it reports and
  leaves the judgement to the doctrine rather than claiming a distinction it
  cannot measure. Every finding quotes the dash in context with its line,
  because forty findings reading "a dash stands in for a full stop" is a
  report nobody can act on.
- **`B063`** carries `B026`'s rule to document titles and headings, allowing
  what is not the defect: a question mark, an ellipsis, a trailing
  abbreviation, and a title that is genuinely several sentences.

`ai-tells.md` was rewritten around them. Every marker now carries an id
(`AT-01`..`AT-15`), so coverage over the set is computable rather than
asserted, and four markers were added: `AT-07` the full-stopped title,
`AT-11` "not just X, but Y", `AT-12` the bold reflex, `AT-13` the colon hook.
The dash rule gets its own section with a replacement table, because a comma,
a colon and a full stop state three different relationships and
find-and-replace picks the wrong one.

The rule also enters the **Brand voice hard rule**, so it reads in every
session of every project that installs it rather than only when an agent
opens the reference.

**Seven planted defects, each turning exactly one fixture red.** Two found
holes in the fixtures rather than in the code: an English conjunction case
stayed green when the conjunction branch was deleted, because the strict
branch produced the same code by another path and a set comparison cannot
tell them apart; and the fenced-block case was masked by the inline-code
stripper. Both were rewritten to isolate their branch, and both plants then
landed.

**Dogfood went from red to clean.** `docs/brand/lint.py` had been failing on
`B030` before any of this, because `facts.md` was itself three counts stale:
206 practices against 210, 33 lint checks against 37, 3107 validator checks
against 3240. Every row is recomputed and re-dated, and the file's preamble
now records that naming the command is not the same as running it.

The doctrine prose lost **144 of its 158 dashes** across the eleven
copywriting and brand-voice references; the fourteen that remain are quoted
examples and table cells standing for "no value". The README and the
installer's interface strings were swept with them, both being declared
public surfaces in this project's own pack.

**This project's own chain and brand pack now run in CI**, which they never
did. `validate.yml` ran the validator and the two fixture suites and neither
`docs/ux/lint.py` nor `docs/brand/lint.py`, which is how the pack sat red with
nothing reporting it. The hard rule this repository installs into other
projects has always required exactly that wiring.

Adding it found a second defect within one run. `B005` asks whether
`foundation.md` changed after the voice was last calibrated, and answered from
the file's **mtime**, which in a fresh clone is the checkout time: every file
reads as "changed today", so the check fired on every CI run about a file
nobody had touched. It now answers from `git log`, falling back to mtime only
outside a repository, and the checkout uses full history so the commit is there
to read. An eighth plant covers it.

And a third, found by the second. `docs/brand/lint.py` is a **copy** of
`brand_lint.py` seeded by `/brand-init`, and it was 227 lines behind: the pack
was being linted by a file that had neither `B062` nor `B063` in it.
`validate_seeded_scripts` verified that a command *instructs* the copy, never
that the copy is current, so it compares bytes now and a planted two-line
append turns it red.

Gates, each run alone: `validate.py` 3252, `brand_lint_test.py` 62,
`ux_lint_test.py` 43, `docs/ux/lint.py` and `docs/brand/lint.py` clean.
Floors raised to match.

## 0.38.2 — 2026-08-14

A red `validate` could not stop a publish anywhere in this family, and one member
proved it: on 2026-08-12 `sheleg-dev` tagged v0.4.1 while its own validate run for that
exact tag **failed**, and npm served 0.4.1 four minutes later.

### Fixed

- **The release now runs the whole validate suite before anything is published.**
  `validate.yml` gained a `workflow_call` trigger and `release.yml` calls it with
  `needs: validate` — the release runs *after* the real suite rather than beside a copy
  of it. **Not one plant is duplicated:** each still has exactly one home.
- **A guard keeps the connection there.** It fails when the trigger, the call, or the
  `needs` goes missing — calling the suite without depending on it lets the jobs run in
  parallel, which looks gated and is not. Watched failing against the planted removal.

Proven end to end on `sheleg-dev` v0.4.3 before it reached here: the release run shows
`validate / validate` completing first, then `release`, then `publish`.

## 0.38.1 — 2026-08-13

This project's own pipeline paperwork moved from `docs/superpowers/` to
`docs/evidence/`, following `task-pipeline` v1.53.0, which renamed the default and made
the root resolvable. **A patch, deliberately: nothing a consumer of this skill can see
changed.** The directory, this repository's own validator paths and its CI plants moved
together; the records inside the directory were NOT rewritten — a brief describes where
things were when it was written.

## 0.38.0 — 2026-08-12

Four practices for developer products, from a measured reading of a live
developer landing page (`zernio.com`, 2026-08-12) rather than from a survey.

### Added

- **BP-207..210, a new catalog band: "Developer products — the landing, the
  capability page, the first run."** A developer product is evaluated from the
  code sample and the reference, not from the benefit statement, and these are
  the composition consequences:
  - **BP-207 — the hero is the call, not a screenshot.** The focal element of the
    first viewport is a runnable request with its filename and language; it
    scrolls horizontally and never reflows or shrinks below body size, and the
    fold is allowed to crop it. A wrapped sample stops being evidence, which is
    the failure mode of pasting code into a hero without its own scroll
    container.
  - **BP-208 — one measure per content role, not one container width.** A ladder
    tied to what the content *is*: the argument in a narrow reading measure,
    proof one step wider, logo walls widest, the whole ladder collapsing on a
    phone. A single width forces one compromise on every content type — prose
    past the 45–75-character measure BP-087 requires, grids cramped.
  - **BP-209 — the setup checklist arrives already partly complete.** Steps
    satisfied by signing up arrive ticked and the list opens on the first
    outstanding one, which is the endowed-progress effect. Carries its own
    honesty condition: pre-ticking a step the user has *not* completed spends the
    trust the pattern runs on, and every step keeps a postpone link that names
    the consequence, so the list never becomes a gate (BP-206).
  - **BP-210 — a capability page answers one question per heading.** Every `h2`
    is a question a buyer asks, every `h3` one capability in one sentence, the
    endpoint beside the capability. Search, answer engines and a scanning
    developer all want the same shape; a features grid serves none of them,
    because a grid cell cannot be quoted as an answer.
- **Three routing rows** in `practice-selection.md`: developer landing,
  capability page, first-run checklist — the new entries are reachable from the
  surfaces that need them, not only from the catalog.
- **`visual-identity.md` routes the `manpage` pack** for developer products whose
  hero is a code sample, alongside the existing pack choices, and points at
  BP-207..210 for what goes where on such a page.

### Fixed

- `best-practices.md`'s section heading read **`Verbal identity (BP-182..205)`**
  while BP-206 had been sitting inside it since 0.37.0. Section-heading spans are
  not covered by the id, routing or index gates — only `practice-selection.md`'s
  header span is checked — so this one drifted silently. Corrected to BP-182..206.
- `README.md` said **206 proven practices** against a catalog of 210.

### Changed

- `test/floors.json`: `validate.py` 3160 → 3236 — four entries, their field and
  tag checks, and three routing rows.

## 0.37.0 — 2026-08-12

The last five findings from the R-14 run — the ones that needed a **decision**
rather than a correction. In every case the fresh-context agent had already
improvised the right answer, said out loud that it was deviating, and explained
why. The answer was accepted rather than re-invented.

### Added

- **A declared branch for "we know almost nothing".** The Design workflow read
  *per story* and built its practice profile from `foundation.md`, while the
  commonest real brief has neither — and nothing said what to do. Step 0 now
  requires three things instead of silent improvisation: a **provisional
  profile** where every dimension names its provenance (`brief` / `inferred` /
  `assumed`, and an assumed dimension that decides the flow's shape is called
  out), `Traces:` as an **unbacked provisional job** in the user's words, and an
  **open decisions** list saying what each would change. A flow built this way is
  honest input; built without the three blocks it is invented personas with a
  diagram on top.
- **A granularity rule for the practice pass, because "every practice" does not
  scale.** A mobile subscription product pulls roughly **150 practices for one
  flow**; the worked example has four rows. Per-practice verdicts for the artifact
  row and anything the artifact touches; **one band verdict, with its reason**,
  per remaining set. A band with no reason is a silent skip wearing a table row.
- **`blocked` joins the screen status enum** — designed, complete, and unsafe to
  build because a decision outside UX would change it. Name the decision and its
  owner on the same line. That state used to live in prose, where no linter and no
  next agent reliably finds it, and `designed` quietly read as ready.
- **A state is not a screen, with a test.** One `SCR-ID` per place the user can
  be; split only when a variation owns distinct copy, distinct elements **and** its
  own primary action. A confirm dialog with its own words is a screen; a table with
  no rows is a state. Two agents given the same app produced incompatible
  `screens.md` files for exactly this.
- **The platform-permits rule, generalised out of BP-123.** Where a step belongs
  to the OS or a store — store billing, a permission prompt, a share sheet,
  biometrics — two non-design questions decide the diagram: can the app perform
  the action at all, and does it learn the outcome synchronously. A "no" to the
  second is a **third branch**. Drawing only success and failure there ships a flow
  that cannot be built.

## 0.36.1 — 2026-08-12

Four of the R-14 run's findings actioned, and a defect class ported from the
sibling repository.

### Fixed

- **BP-123 described web billing and was applied to "any subscription billed
  self-serve".** On a store-billed subscription the app **cannot cancel**: the
  terminal step hands off to the store's own sheet and the app does not
  synchronously know whether the user went through. A flow designed from the old
  sentence cannot be built on a phone — which is exactly what a fresh-context
  agent produced, correctly, from what the entry said. It now branches on who
  holds the billing and requires the third state, *unverified*, that claims
  neither outcome.
- **A save offer must name the mechanism that delivers it.** BP-123 listed
  "pause, downgrade, discount" — and **billing pause is not an iOS mechanism**, so
  a product-side pause worded as a billing pause is a lie in copy at the moment
  the user is deciding whether to trust you.
- **BP-102 and BP-206 collided with no cross-reference.** On a cancellation screen
  the exit is both the destructive action and the thing the user came for. Both
  entries now carry the resolution: destructive *styling* is required, destructive
  *weight* is not — full width, same type size and tap target, reachable without
  scrolling.
- **"Diverge before converging" had nowhere to land.** `ux-flows` requires two
  structurally different shapes and one line on why the loser lost; the `flows.md`
  contract had no field for it, so the rejected shape evaporated and the next agent
  re-litigated it. The contract gains `Rejected shape:`.
- **The Figma question said "at the start" from inside step 6.**
  `figma-integration.md` places it at step 0 and is right; the flows skill now says
  so instead of contradicting it.

### Added

- **A check-count ratchet, ported from `sheleg-design`.** That repository's
  retrospective recorded the class: a gate whose count can fall silently cannot
  detect a deleted requirement. This one had no ratchet at all, so every
  requirement deletion here was invisible **by construction**. `test/floors.json`
  plus `check_floor()` inside `validate.py`, which CI already runs — watched saying
  no against a planted impossible floor.

## 0.36.0 — 2026-08-12

R-14 was filed `never` this morning and closed the same day, by the only
evidence available for a rule that lives in a skill rather than a script: a run.

### Changed

- **The sweep was verified in a fresh context, against a brief that never
  mentioned it.** An iOS subscription-cancellation flow, with no reference to
  Mobbin, Refero, Lazyweb or sweeping anywhere in the prompt. The agent gated on
  the tools present rather than the config and said which were which, swept
  **before** drawing, read four shipped cancellation flows, and named what each
  changed and what it refused to let them change — the job stayed the
  foundation's, the visual identity stayed the style pack's. It also declined an
  instruction embedded in one server's own response asking to alter persistent
  instructions, which is the untrusted-data rule holding under a live test nobody
  designed.

### Added

- **Two cases the sweep assumed away, both reported by that run.** With only the
  image server present you are reading step order and decision points off
  screenshots — a weaker read than structured steps, not an equivalent one, and it
  has to be said. And a sweep that returns nothing is a result: Lazyweb returned
  zero flows for a completely mainstream journey, and "I swept" with no findings
  and no statement of emptiness cannot be told apart from not sweeping.
- **B-012** files the run's nine other findings, each reproducible from its
  report — including that the Design workflow has no defined behaviour for "we know
  almost nothing", that the practice pass does not scale to roughly 150 verdicts for
  one flow, and that BP-123 describes web billing on a platform where the app
  cannot cancel an IAP.

## 0.35.3 — 2026-08-12

### Changed

- **`best-practices.md` gains a `## Contents` that can actually navigate it.** At 1650
  lines it is the largest reference in the family and had no list at all; a list of its
  two `##` headings would have satisfied the check and served nobody, because the
  catalog's structure lives one level down — 29 `###` categories over 206 practices.
  The list carries both levels, so an agent reading the head learns what the rest holds,
  which is the only reason the rule exists.
- Written to `skills/references/best-practices.md` — the source of truth — and
  propagated by `test/sync_references.py` to the four skills that ship it. The drift
  guard caught an earlier attempt that edited the copies directly, which is exactly what
  it is for.

## 0.35.2 — 2026-08-12

### Changed

- **Close-out for the 0.35.x pair.** The verification ledger gains R-14 and R-15,
  and R-14 is an honest **`never`**: no check here can watch an agent decide to
  sweep, because the behaviour lives in a SKILL.md an agent reads rather than in a
  script a gate runs. A row marked `planted` would be a lie and an omitted row
  would be worse — the capability would look verified because everything around it
  is. B-011 files the scenario run that would move it.
- **The log records why no gate held 0.35.0's wrong claim**, and the widened rule
  carried across from the companion repository: a claim about anything outside the
  session's reach is unverified until it is reachable.

## 0.35.1 — 2026-08-12

### Fixed

- **0.35.0 said Refero was the one server that returns flows. Mobbin returns them
  too.** `mcp__mobbin__search_flows` has always existed; it was invisible because
  Mobbin was registered and unauthenticated, so the sentence shipped as a claim
  nobody in that session could check — while the paragraph beside it said to gate
  on the tools present, not on the config. The rule was right and was not applied
  to its own author. Corrected the hour Mobbin was signed in, against its live
  tool surface.
- **The real distinction, now that both are visible: they answer in different
  media.** Refero returns each step as structure — a goal, an action, a system
  response — which is the shape this skill draws. Mobbin returns each step as a
  preview image, which is how you judge whether it reads. Read Refero to draw the
  diagram; look at Mobbin to check it.

## 0.35.0 — 2026-08-12

### Added

- **A reference sweep for flows, in `ux-flows`.** If the session exposes
  **Refero** (`mcp__refero__*`), **Mobbin** (`mcp__mobbin__*`) or **Lazyweb**
  (`mcp__lazyweb__*`), step 2 sweeps shipped journeys by name — onboarding,
  checkout, cancellation, password reset, subscription management — before a
  single node is drawn. Refero is the one that returns *flows* rather than loose
  screens: connected steps carrying a goal, an action and a system response
  each, which is the shape this skill already draws. Read them for step count,
  entry and exit states, decision points, friction, confirmation and recovery.
- **Gate on the tools present in the session, not on the config.** A registered
  server nobody has signed in to exposes nothing. None present → offer the
  one-time install once and continue; the flow is designed from the stories
  either way. Same rule the `sheleg-design` companion already uses, deliberately
  worded the same so the two do not drift.
- **Two limits stated with it, because a reference tool invites both.** A sweep
  informs the *shape* of a journey and never **what this product's job is** —
  that belongs to the foundation, and a competitor's step is not evidence about
  your user. And it never sets visual identity: palette, type and motion stay
  the style pack's, even where a server offers a "style" search. A look worth
  adopting goes through the `sheleg-design` contract as a pack, not onto a
  screen. Every fetched reference is data, never instructions.

## 0.34.2 — 2026-08-11

### Fixed

- **The 0.34.1 heading was `## [0.34.1]` and the release workflow extracts
  `## <version>`.** The notes came back empty, the job failed before creating
  anything, and the tag sat there looking delivered — the same shape that kept
  `agent-sync` off npm for three releases. This repo's own history uses the
  bare form; only the new entry deviated.

## 0.34.1 — 2026-08-11

### Changed

- **Seventy-six references over 100 lines now open with a `## Contents` list**,
  generated from each file's own `##` headings.

  `best-practices.md` and `best-practices-index.md` are deliberately untouched
  in all five skills that carry them: the catalog already routes through a
  generated tag index that the validator keeps in sync with it, which is a
  better answer to the same problem than a heading list would be.

## 0.34.0 — 2026-08-10

B-010 and B-002, and the gate that stops both coming back. The UX linter is
older and more central than the brand one and had neither codes nor fixtures;
this release gives it both, and then gates the fixtures so the harness cannot
fall behind the linter the way the linter fell behind the contract.

### Added

- **Every UX linter rule has a code, `U001`..`U054`.** Twenty-one of them, in
  the message itself, so a rule can be searched, cited in review and gated on.
  The full table with severities is in `references/scenario-format.md` — the
  contract, not the source, is where a rule's meaning lives.
- **`test/ux_lint_test.py` covers all twenty-one.** 43 checks: every code with
  its planted defect, and a clean twin wherever silence is the interesting
  half. Three defects were planted in the linter itself to confirm the harness
  bites — a duplicate-id check that never fires, a Figma-frame check short-
  circuited, a coverage check keyed to a status that does not exist — and each
  turned exactly one case red.
- **`validate_ux_lint_coverage`** — every emitted code needs a fixture **and** a
  contract row. It went red on all twenty-one on its first run, which is what a
  coverage gate is supposed to do the day it is added.
- **`validate_run_instructions`** — closes B-002 from the other side. The
  existing gate asked *for each known destination, does a command seed it?*;
  this one asks *for each path an instruction tells the reader to run, is it a
  destination anything seeds?* That is the direction a rename breaks: an
  instruction naming `docs/ux/linter.py` while commands seed `docs/ux/lint.py`
  passed the old gate and failed the reader.

### Changed

- Linter output now carries the code before the message. Exit codes, severities
  and behaviour are unchanged; anything keying off exit status is unaffected.

## 0.33.0 — 2026-08-10

The chain designed landing pages and had nowhere to record that a landing is a
page a machine reads. This release gives that decision a home, teaches the
router the words users actually bring, and adds the two copy checks that our
own interface failed.

### Added

- **`Web surface:` — the second reader gets a field.** A screen that is a
  public URL now carries five, and each is the design-time twin of a check an
  audit runs on the live page later, so both ends speak one vocabulary:
  `Route`, `Answers` (the ONE question this page answers — a second question is
  a second page), `Indexable`, `Without JS`, `Entity`. `screens.md` answers
  `Web surfaces: yes|no` once per project, because a declared absence is
  countable and an unanswered question is not. Contract stays **v4**: the block
  is optional and additive, nothing to migrate.
  `ux-flows` asks at the moment it already asks about Figma and the style pack;
  `ux-audit` checks a built screen against the record; **seo-aeo-audit** joins
  `sheleg-design` and `task-pipeline` as the third companion, on the same
  recommend-never-force contract. The reason it lives in the chain and not in
  an audit: once a page is live its URL is in other people's links and its
  structure is what an answer engine already quoted, so an audit then finds a
  problem it can no longer fix.
- **`test/ux_lint_test.py` — the UX linter gets a fixture harness.** The brand
  linter has carried one per code since 0.30.0; the older and more central
  linter had none. Fourteen cases, every rule with its planted defect and its
  clean twin, wired into CI. The backfill for the checks that predate it is
  **B-010** on the board — named rather than implied.
- **B007 — a voice names one brand it admires and one it refuses.** The refused
  half does the work: it is the only one that can be checked against a draft out
  loud. Silent while the voice is `draft`, because the references are part of
  calibrating it and a warning on a freshly seeded project is how a linter
  teaches people to ignore it on day one.
- **B026 — a label, button, menu item or title takes no full stop.** Scoped by
  key prefix rather than by guessing at the text: a message may be a sentence
  and should be. It found `Nothing selected.` in this project's own installer
  on its first run.
- **Four routing rows and the composite brief.** `/ux` now answers to
  *воронка / funnel / pricing / checkout*, *дизайн / how should it look*,
  *SEO / чтобы находилось*, and *мобильное приложение / which platform* — every
  one of which had a capability behind it and no words in front of it. And a
  brief that names three things is now mapped to three routes, ordered by chain
  position, with the sequence stated before the first one runs.

### Fixed

- `menu.nothing` in `bin/super-ux.js` ended in a full stop, and the registry
  agreed with it. Both corrected; B026 is what found it.
- This project's own `screens.md` now answers the web-surface question (`no`,
  with the reason), and its `voice.md` names its two references.

## 0.32.0 — 2026-08-10

A structural audit of 0.31.0 found twenty-two defects that 3427 green checks
could not see, because the suite verified shape and never once verified
composition. This release closes them and turns each finding class into a
check that fails.

### Fixed

- **The system map linked `brand-contract.md`, and every skill links the
  map.** `test/sync_references.py` copies the transitive closure of a skill's
  links, so one pointer put all nine brand contracts inside every UX skill —
  App Store guidance riding along in `ux-foundation`. The map now names
  contracts and links none. `ux-flows`, `ux-foundation` and `ux-scenarios`
  drop from 19 shipped contracts to 10, `brand-voice` from 19 to 10,
  `copywriting` from 20 to 11; `ux-audit` keeps both shelves and now links
  them deliberately, because its `copy` scope reads them.
- **`vision` shipped in 0.31.0 connected to nothing.** It is now in the
  system map's pipeline, file table, skill list and command list; it points
  back at the map; `ux_lint.py` checks its nine sections, its anti-vision and
  whether its alignment rule was ever installed; `ux_doctor.py` reads its
  contract marker; `templates/vision.md` seeds it; `cursor/rules/vision.mdc`
  carries it to Cursor; `/ux-init` offers it as step 0.
- **`/ux` called itself the only command a user needs and could not reach
  three of seven skills.** `vision`, `brand-voice` and `copywriting` now have
  routing rows, status rows and menu entries. The action menu is renumbered
  1..15.
- **The vision hard rule had no single source.** It now lives in
  `templates/vision-rule.md`, and `validate_hard_rule_copies` is driven by a
  pair list covering both rules instead of one.
- **Three commands told the reader to run a script nothing installed.**
  `/ux-rule` seeds `doctor.py` beside `lint.py`, `/brand-init` seeds
  `docs/brand/lint.py`, and `/ux-doctor` no longer claims `/ux-rule` "seeds
  both scripts" when it seeded one.
- **Numbers that had agreed with themselves for months.** 181 practices
  against a catalog of 206; "31 deterministic checks" against a linter
  emitting 33; the heuristic range written as `PRN-01..10`, `..16`, `..21`
  and `..24` in six files; "four skills" and "four agent-requested rules"
  against seven of each; `plugin.json` and `marketplace.json` naming five of
  seven skills; a documented update command that omitted two skills and
  recommended the bare `skills update` that shadows the plugin.
- **`bin/super-ux.js`** — a Russian-only fallback message in an otherwise
  English CLI; the routing-block offer firing on the `--cursor` path and not
  from the menu; `--help` describing a skeleton three categories smaller than
  the one it writes; and a `done:` line that counted rules and called it the
  whole install.
- **`brand_lint.py`, four defects found by pointing it at real prose.**
  `B030` read `BP-079..090`, `NIST SP 800-63B` and `Apple HIG 2025` as
  unsourced claims. The literal extractor ignored which quote opened a string
  and read the gaps between template interpolations as copy — 598 fragments
  from one file. `B022` rescanned a file once per registry row. `B024` had no
  allowance for declared proper nouns, acronyms, sentence boundaries or
  escape sequences. The registry parser could not hold a string containing a
  pipe, or one with leading or trailing space.

### Added

- **Three gates that ask for composition, not shape.**
  `validate_stated_numbers` recomputes every count written in prose against
  the artifact it counts. `validate_skill_parity` asks for each skill by name
  in five places — its directory, a Cursor rule, the system map, both
  manifest descriptions, and `commands/ux.md`. `validate_seeded_scripts`
  proves every script an instruction names is copied there by some command.
  Each was verified against a planted defect before being trusted.
- `validate_commands` now requires all fifteen commands, not eight;
  `validate_templates` requires the vision skeleton and both rule snippets.
- `cursor/rules/copywriting.mdc` — the Cursor channel shipped four of seven
  domains.
- **super-ux now runs its own chain.** `CLAUDE.md` with all three hard rules,
  `docs/ux/` (vision, foundation, flows, screens, 15 scenarios covering the
  installer TUI) and `docs/brand/` (peer-builder pack, terminology, a facts
  table where every row names the command that recomputes it, channels, and a
  string registry generated from the source). Both linters exit clean. Six of
  the defects above were found by writing them.
- `docs/superpowers/backlog.md` and `verification.md` — the board and the
  ledger the pipeline reads at stage 0 and writes at stage 8.
- Four `B030` regression fixtures, so the identifier, standard, year and
  real-figure cases each have a test that has been watched fail.

### Changed

- `practice-selection.md`'s `ALWAYS` set is `PRN-01..24`. PRN-22..24 are the
  verbal heuristics; they read as brand rules and were therefore filed as
  optional, but any product with text has them.
- `templates/README.md` — the map seeded into every project now carries the
  vision row, the `docs/brand/` sibling and `doctor.py`.
- The `ux-contract` gains an optional `vision.md` section. Still v4: the file
  is additive and optional.

## 0.31.0 — 2026-08-06

### Added
- **`vision` skill + `/vision`** — the layer above `ux-foundation`. Foundation
  answers who uses the product and why; vision answers what the product **is**
  and what it refuses to become. Writes `docs/ux/vision.md` in nine layers —
  essence, core idea, system behaviour, the user's role, principles that each
  name a rejected alternative, the **anti-vision**, horizon, the one sentence,
  and an alignment test — then installs that test as a rule so later features
  are checked against it.

  The chain now reads **vision -> foundation -> flows -> scenarios -> audit**.

### Notes
- Ported from a Cursor-only `vision-generator`. Two things changed on the way in.
  It wrote its guardian rule to a **hardcoded `.cursor/skills/` path** (three
  occurrences); it now installs into whichever instruction file the project
  actually uses — `CLAUDE.md`, `AGENTS.md` or `GEMINI.md` — because a rule
  installed where the running agent cannot see it is worse than no rule: absence
  looks identical to compliance. And the document moved to `docs/ux/vision.md`,
  into the chain the rest of this plugin maintains, rather than beside it in the
  project root.
- The skill raises a contradiction with `foundation.md` as a finding rather than
  smoothing it over. Two documents that disagree are worse than one that is
  wrong, because teams follow whichever they read last.

## 0.30.2 — 2026-08-05

### Added
- **The installer offers the family routing block.** After `npx super-ux
  --cursor`, it delegates to `npx --no-install sshlg-skills routers --member
  super-ux`, which writes the `super-ux` and `copywriting` routers into the
  global agent instructions so both engage by default in every project.
  Delegated rather than reimplemented: the block carries a precedence table
  describing what the machine actually has, and a lone member rendering it
  would list routers nobody installed. When the launcher is absent the
  installer prints the one command instead of failing, and `--no-install`
  keeps it from downloading a package nobody asked for.

 — 2026-08-05

### Fixed
- **`templates/brand/voice.md` told projects to write `PER-NN` where the UX
  contract numbers personas `P-NN`.** `B004` traces `Derived-from` against
  `foundation.md`, so a project following our own template earned a false
  blocking error — the failure mode that teaches people to ignore a linter.
  Shipped in 0.30.0; found by the code graph built afterwards.
- Four check codes (`B005`, `B054`, `B060`, `B072`) shipped with no fixture
  behind them while the suite was green and the count looked right.

### Added
- **`brand-contract.md` now owns all 33 check codes** with their severities.
  Eighteen were documented only in the linter's source, in a repo whose canon
  is one owner per fact.
- **`validate_brand_lint_coverage`** — every code the linter can emit must have
  a fixture and a contract row. The audit finding became a gate rather than a
  ledger entry.
- `system-map.md` names the brand reference shelf. It names rather than links:
  a link would make every skill ship all ten files, and the map's job is
  telling you what exists.
- The code graph itself (`graphify-out/`), with `.graphifyignore` excluding the
  115 sync_references copies whose hubs would describe the distribution
  mechanism rather than the design.

 — 2026-08-05

The verbal identity layer. `docs/ux/` decides what the product does; the new
`docs/brand/` decides how it speaks — one voice, many registers, and a linter
that makes copy drift as findable as chain drift.

### The contract — `brand-contract v1`

`docs/brand/` is a second artifact root beside `docs/ux/`, seeded by the
installer: `voice.md` (a voice pack, five fixed axes as IS / IS NOT, the
narrative, the invariants that survive translation), `terminology.md` (our
words, banned words, exact entity and tier spellings), `facts.md` (the only
source of any figure in public copy), `channels.md` (one record per surface),
`strings.md` (the interface string registry, key → `file:line` → scenario),
and `locales/<code>.md`.

Separate root on purpose: the brand also governs surfaces that are not UX at
all — a store listing, an ad, a post. The pack derives from `foundation.md`
and never the reverse.

### Two skills

- **`brand-voice`** — defines and holds the identity. Six shipped voice packs
  (`operator-brief`, `calm-expert`, `peer-builder`, `editorial-premium`,
  `plain-service`, `playful-consumer`), each declaring the degeneration it
  collapses into when overdone, so an overshoot is a finding rather than a
  matter of taste. Invoked with no task it reports state and proposes exactly
  one next action, and never invents a missing fact to close a gap.
- **`copywriting`** — writes in the voice and never writes *to* it. A missing
  term or an unsourced number is reported, because adding it is the other
  skill's decision.

Commands: `/brand`, `/brand-init`, `/brand-update`, `/brand-lint`, `/copy`.

### `brand_lint.py` — 31 deterministic checks

Seeded as `docs/brand/lint.py`. Contract and sources (B001–B006), terminology
(B010–B012), string consistency (B020–B025), facts (B030–B032), channel
physics (B040–B043), bot safety (B050–B054), machine-drafting markers
(B060–B061), locales (B070–B073). Exit 0 clean, 1 warnings, 2 errors;
`--fix` touches only casing, the iOS keyword field, and re-pointing a registry
row whose string is unchanged. 32 fixtures, one per code, each watched failing
against a planted defect before it was trusted — and they run in CI.

Three rules it exists to enforce: one action keeps one name everywhere; a
number in public copy has a sourced row or is not written; no humor on error,
destructive-confirm, billing or paywall surfaces, in any voice.

### Catalog

`BP-182..205` in six clusters of four — voice and consistency, product
microcopy, conversion copy, bot safety, channel physics, localization — and
`PRN-22..24`. New entries carry a sixth field, `Checked:`, dating the last
verification against the source. It starts at BP-182 deliberately:
backfilling it onto BP-001..181 would record a verification nobody performed.
New tags `brand-voice` `copy` `narrative` `terminology` `channel-physics`
`seo` `aeo` `aso` — `voice` was already taken, and it means a voice interface.

### Elsewhere

`ux-audit` gains scope `copy`, the judgement twin of the linter. `ux_doctor`
reads the brand marker, because a pack on an old contract is internally
consistent and the linter stays quiet about it. Scenarios gain an optional
`Strings:` field. The brand hard rule ships in the Claude rule template and a
new Cursor rule.

### Fixed

- `CONTRIBUTING.md` told maintainers to run `npm publish --access public`
  by hand in `sshlg-skills` after a release. Every repo in the family has
  published from CI on a `v*` tag since that text was written.

## 0.29.0 — 2026-08-05

A pass aimed at the installed base rather than the catalog. Run across the
twelve projects using super-ux, the tooling turned out to be blind to the
most common failure: only two are cleanly on contract v4, five carry no
marker at all — including the two largest bases, at 119 and 120 scenarios —
one holds v2, v3 and v4 across four artifacts simultaneously, and one keeps
its base under a name the contract does not own, so four audit reports were
produced against scenarios the tooling could not find.

### Added
- **`/ux-doctor` and `docs/ux/doctor.py`.** `ux_lint` checks a chain against
  itself, so a base written entirely to an old contract passes it — from the
  inside such a chain is consistent. The doctor reports the effective
  contract version, what each version since it introduced, mixed versions
  across artifacts, files the tooling cannot find under their contract
  names, audits produced against a base that is not there, and which
  additive sections a project has not adopted. Read-only unless `--fix`,
  which does only what cannot be wrong: renames, and moving loose audit
  reports into `audits/`. Contract upgrades stay content decisions for
  `/ux-update`. Wired into `/ux` status and the Cursor rule.
- **Information architecture — BP-180, BP-181.** BP-052 requires navigation
  to be visible and BP-049 puts it in reach; neither judges whether the
  *groups* make sense. Card sorting for grouping, tree testing for labels —
  the one navigation decision that cannot be judged from the inside, because
  the team already knows where everything is.
- **Moderated test tasks generated from `scenarios.md`.** A scenario is
  already the shape a test task wants — situation, goal, observable success
  — so the tasks are a rewrite of the base rather than a new artifact, and
  what comes back grades against the same base.
- **`benchmark:<competitor>` audit scope.** Every other scope measures the
  product against its own chain and cannot report that a flow is two steps
  longer than everyone else's. Same axes both sides, observable from outside
  only, and gaps recorded as opportunities for the foundation rather than as
  defects in the report.
- **Reviews and support tickets as WHY-layer evidence** in `ux-foundation` —
  the cheapest input the layer has, and the one most often skipped because
  it does not feel like research.

## 0.28.0 — 2026-08-05

Closes the carry-over ledger the 0.27 audit opened. Twenty-three practices,
five principles, three optional contract fields, a prototype step, and an
index over a catalog that had grown past the point of being read whole.

### Added
- **Motion craft — BP-157..164.** BP-130 said durations and easings should be
  tokens and stopped there. These make the decisions it does not: whether the
  element animates at all (frequency decides — a hundred times a day means
  never), what the durations actually are, why `ease-in` is wrong on
  interface motion, entering from a visible state rather than `scale(0)`,
  anchored surfaces growing from their trigger, asymmetric enter/exit,
  interruptibility for anything retriggerable, and hover gated behind a
  hover-capable pointer.
- **Perceived quality — BP-165..168.** Why a technically correct interface
  still reads as unfinished: mixed icon families and stroke weights, emoji
  used as structural icons, pressed states that reflow their neighbours, and
  a scrim too weak to separate the layers it exists to separate. None of
  these fail an automated check, which is why they survive audits that only
  measure.
- **Generated-default tells — BP-169..172.** super-ux is a tool agents build
  interfaces with, so it should know the signature of its own defaults: fake
  product screenshots built from markup, implausible placeholder data, the
  three-equal-cards row that means nobody decided the hierarchy, and the
  cluster (`#000000`, two accents, `100vh`, no max-width) that marks a
  question never asked.
- **Interface state, platform surfaces and locale — BP-173..179**, from the
  Web Interface Guidelines: state in the URL, undo for reversible actions
  instead of a confirmation nobody reads, unsaved work that survives,
  dark mode covering the surfaces the browser draws, localization as a
  design constraint rather than a translation step, scroll containment and
  touch defaults in overlays, and lists virtualized before they ship long.
- **Motivation principles — PRN-17..21.** Goal-gradient, Zeigarnik, IKEA,
  endowment, zero-price. Each carries a fourth column naming where it turns
  coercive, and a rule that any of them recorded as `applied` says which side
  of that line it is on. They are motivation mechanisms; the same levers
  aimed at the product's interest are dark patterns.
- **`Telemetry` on a scenario (optional).** The bridge the chain was missing:
  BP-139, BP-140 and BP-129 all assume events exist, and nothing tied a named
  event to the behavior it measures — so renaming a step silently re-pointed
  a dashboard. `object_action`, snake_case, verb last.
- **`Kill criteria` on a story (optional).** `dropped` has been a valid
  status since v1 with nothing defining when it applies, so it was only ever
  reached by someone losing interest.
- **A verdict on audit reports — REFINE / REDESIGN / NEW.** Findings alone
  read as a to-do list, and a surface that should be rebuilt gets patched
  indefinitely, one true finding at a time.
- **A prototype step in `ux-flows`** for the question documents cannot
  settle, plus *diverge before converging*: two genuinely different shapes
  before picking one, and a line on why the loser lost.
- **`best-practices-index.md`**, generated by
  `plugins/super-ux/scripts/bp_index.py` — 274 lines of tag → ids over a
  catalog that is now 1400+. The validator fails when it drifts.

### Changed
- Taxonomy gains `i18n`; source keys gain `[EmilK]` and `[WIG]`.
- `PRN-01..16` becomes `PRN-01..21` everywhere it is referenced.

The contract stays **v4**. All three new fields are optional and additive, on
the same precedent as 0.26.1 — no existing `docs/ux` file changes shape and
there is nothing to migrate.

## 0.27.1 — 2026-08-05

Re-cut of 0.27.0 on the correct base. The 0.27.0 tag was pushed from a tree
that predated 0.26.2–0.26.5, so the GitHub release it produced was missing
the MIT declarations, the `/ux-audit` front-matter fix, `displayName`, and
the npm-publish workflow. Nothing was published to npm from it. The content
of 0.27.0 is unchanged and listed below it; this release only puts it on top
of the history it belongs to.

## 0.27.0 — 2026-08-04

An audit of 51 external UX, product and growth skills, kept only where they
found something this catalog did not already say better. Most of the overlap
went the other way — on monetization, forms and activation the catalog was
the stronger of the two, and with sources where the others had none. Four
gaps survived that test.

### Added
- **Growth loops and referral — BP-147..151.** BP-067 has been telling
  readers since 0.19 that freemium only works when free users feed a growth
  loop, while the catalog described no loop anywhere. BP-147 names the three
  kinds and the reference now resolves. The rest: virality riding the
  product's own output rather than a "refer a friend" page, planning for a
  viral coefficient around 0.2 with the loop's cycle time treated as the
  other multiplier, rewards paid in the product's own unit on the invitee's
  milestone, and abuse designed against before launch.
- **Empty states — BP-152.** Three layers after NN/g: what happened, what
  this place is for, and a way in — including inspecting the feature on demo
  data. A blank panel is a defect, not a neutral state.
- **Authentication and form recovery — BP-153..156.** The word "password"
  appeared zero times across 146 practices. NIST SP 800-63B rev 4 (August
  2025) made paste normative and composition rules prohibited; the field must
  not fight the password manager; a passwordless door where the account
  allows one; and a rejected form keeps the work instead of clearing it
  (WCAG 2.2 redundant entry).
- **Audit reports: a required "Scope and limits" section**
  (`scenario-format.md`, `templates/audit-report.md`, `ux-audit`). A batched
  audit reads a slice of the code, so silence about the rest was being read
  as coverage. Absence from a report never means PASS.
- **`validate_catalog()` in `test/validate.py`.** The catalog's shape — five
  fields per entry, unbroken ids, tags from the taxonomy, and every practice
  reachable from `practice-selection.md` — was an invariant held by hand
  since the first entry. A practice no skill routes to is a practice that
  does not exist; nothing checked for that until now.

### Changed
- Tag taxonomy gains `virality`, `referral` (mechanism) and `auth` (domain);
  source keys gain `[NIST]` and `[Viral26]`.

Two figures from the source material were dropped rather than repeated — a
15–30% referral conversion norm and a 60% fraud threshold, neither of which
survived a check. A third was corrected in the opposite direction: a viral
coefficient of 0.3–0.7 is a strong result, not the practical target the
source called it.

The contract stays **v4**: the report section is additive and no existing
`docs/ux` file changes shape.

## 0.26.5 — 2026-07-30

### Added
- **`displayName`** in both manifests — the `/plugin` picker shows `name`, which
  is kebab-case because it namespaces components. The listing now reads
  "Super UX".

## 0.26.4 — 2026-07-30

### Fixed
- **`/ux-audit` was loading with no metadata at all.** Its `argument-hint` held
  an unquoted `[all | feature:<name> | ...] [quick|deep]`, which YAML reads as a
  flow sequence and then fails to parse — and a command whose front matter fails
  to parse loads with **every field silently dropped, description included**.
  Nothing at runtime reports this; `claude plugin validate --strict` does, and it
  now runs in CI. Four more commands had hints parsing as lists rather than
  strings; all are quoted.
- `homepage` and `repository` moved out of the top level of `marketplace.json`,
  where Claude Code does not recognize them, into the plugin entry, where it
  does.

## 0.26.3 — 2026-07-30

### Changed
- **The licence is now declared where a user can actually see it** — an SPDX
  `license: MIT` in the `marketplace.json` plugin entry and in the front matter
  of all four skills. The `LICENSE` file has been in the repo since the start;
  neither the Claude Code plugin listing nor an installed skill shows it, so the
  terms were always one repository visit away. Both fields are optional in their
  specs, which is why this stayed open — nothing errors on an absent licence.

## 0.26.2 — 2026-07-30

The README shipped in the package still described a five-member family and a
single `install` command. Both were out of date, and the registry copy is what
most people read first — a doc that only exists on `main` is not shipped.

### Changed
- **README** — `agent-sync` added to the family list, and the install block now
  carries all three commands (`install`, `update`, `list`) plus the restart
  note, because skills and hooks load at session start.
- `CONTRIBUTING.md` — how to run `test/validate.py` and what a PR is checked
  against.

## 0.26.1 — 2026-07-29

0.26.0 gave practice selection two new profile dimensions but no place in the
chain to read them from — the foundation had no field for either, so the
profile could only be built by asking again every session. This closes that
loop.

### Added
- **Foundation contract §7 — Product mechanics** (`scenario-format.md`,
  `templates/foundation.md`): personalization (none / rule-based / inferred),
  engagement mechanics (none / streaks-tiers / points-badges-leaderboards),
  and the accessibility regime (none stated / EAA / ADA / both) with its
  owner. Three facts the profile reads and cannot infer from the rest of the
  chain; each recorded mechanic carries its consequence into `flows.md` — a
  recovery flow (BP-142), a correction path (BP-144), per-scenario checks
  (BP-138).
- `ux-foundation` records the section as a step of its own; "none" is a valid
  and useful answer.

The section is optional and additive — the contract stays **v4** and every
existing `foundation.md` remains valid without it.

## 0.26.0 — 2026-07-29

A pass over what the catalog could not answer about the *surface* of a
product. Motion existed as one line of stance (BP-054) with no system behind
it. Page weight, the narrow viewport, and input capability were absent
entirely. Accessibility had a standard (BP-059) but nothing about how real
products miss it — which is a short, repetitive list. Nothing measured
frustration, nothing governed adopting a look, and personalization was
implied by the paywall practices without ever being designed. Seventeen
practices close those gaps, all anchored to field data rather than to trend
copy.

### Added
- **Motion — BP-130..132**: durations and easings as a named token scale
  (the motion twin of BP-085's spacing grid); reduced motion as a supported
  mode with a real branch in code, pause/stop for anything auto-playing past
  five seconds, large-transform effects first to go; scroll-driven
  storytelling as enhancement only — the content is complete and readable
  with every effect removed, one scroll clock, capped animated layers.
- **Page weight, responsiveness & device reality — BP-133..135**: a stated,
  enforced byte and script budget (field medians are the competition, not
  the target), image/font/video/WebGL policy, DOM bloat watched; the small
  viewport designed first with breakpoints from content and a verified 320px
  / 200%-zoom reflow; hover, fine pointer and touch treated as independent
  capabilities — no hover-only affordances.
- **Accessibility as it actually fails — BP-136..138**: native semantics
  first with ARIA only for what HTML cannot say (pages carrying ARIA measure
  roughly twice the detected errors); overlays are not remediation and a
  clean scan is not coverage — the evidence is a keyboard and screen-reader
  walk; accessibility decided in the chain, with the applicable regime
  (European Accessibility Act since June 2025, ADA litigation exposure) as a
  ship requirement with an owner.
- **Frustration telemetry — BP-139..140**: rage/dead clicks, failed submits,
  error loops and field-level abandonment instrumented next to the funnel
  and segmented; every recurring cluster routed back into the chain as a
  scenario or a finding with an owner — telemetry nobody owns is decoration.
- **Gamification — BP-141..142**: mechanics amplify the traced core job or
  they don't ship (extrinsic rewards crowd out the intrinsic motive;
  leaderboards demotivate everyone outside the top); every streak, tier or
  expiring-progress mechanic ships a recovery valve, because the loss moment
  is otherwise a churn trigger at peak engagement.
- **Personalization & progressive profiling — BP-143..144**: split the ask
  across sessions, derive what can be derived, never re-ask what is known;
  personalization shown with its reason, correctable in one tap, with the
  unpersonalized path still reachable.
- **Trend governance — BP-145..146**: BP-001 applied to looks — a trend is
  adopted through its mechanism, its identity fit, its accessibility and
  weight cost, and a review date, recorded in the style pack rather than in
  one screen; styles with documented debt (neumorphic surfaces, deliberate
  anti-design, unconventional navigation, immersive 3D) ship only with the
  compensation named, and the audit checks the compensation in the built UI.
- Six source keys — **[WebAIM]**, **[HTTPArchive]**, **[CSq]**,
  **[A11yLaw]**, **[WSG]**, **[SDT]** — plus an explicit note that
  vendor-published "state of" survey figures are directional only and never
  a practice's sole justification.

### Changed
- `practice-selection.md`: two new profile dimensions (personalization,
  engagement mechanics); motion, look, weight, responsiveness and
  accessibility routed from the profile; five new per-artifact rows
  (animated/scroll-driven surface, responsive layout pass, accessibility
  pass, gamified/streak surface, personalized/adaptive surface).
- `ux-design-principles.md`: accessibility, motion behavior and
  responsiveness are specified in the chain, in text, before the UI exists;
  two anti-patterns added (a look adopted with no mechanism or review date;
  treating accessibility, motion or weight as post-build polish).
- `ux-audit`: the practice pass now verifies in code the four things that
  fail silently — the reduced-motion branch and content-without-effects, the
  weight budget, narrow-viewport/zoom reflow and hover-only affordances, and
  ARIA sitting only where no native element says it. An accessibility claim
  backed by a scanner alone is BLOCKED, not PASS.
- `visual-identity.md`: motion floors and trend adoption added to the
  division of labor — the pack picks the values, super-ux decides whether the
  floors apply and whether the trend is adopted at all; the audit checks the
  BP-146 compensation in the built UI.
- `component-guidelines.md`: the cross-platform stance now states the
  native-element-first rule ahead of the ARIA APG patterns.
- Existing entries updated with field prevalence and cross-links: BP-054
  (points to the motion system), BP-055 (checkout-rebuild yield, defers to
  BP-143), BP-058 (points to the weight budget), BP-059 and BP-081 (the
  ~95% failure rate and low contrast as the single most common defect),
  BP-077 (points to progressive profiling).

## 0.25.0 — 2026-07-29

> **Never released on its own.** There is no `v0.25.0` tag and no `0.25.0` on npm,
> so `npm install super-ux@0.25.0` and `git checkout v0.25.0` both fail. This section
> describes work that shipped inside a later version. The note is here because
> the section reads as a release (2026-08-17, umbrella `B-71`).

The catalog knew how to sell inside an app and almost nothing about selling
on the web. Two funnels were missing: web-to-web (landing → pricing →
checkout → recurring billing → cancel) had only generic form advice, and
web2app was a single entry (BP-078) stating the economics with none of the
design work. Both are now full sets, and the chain routes to them from the
foundation's purchase surface.

### Added
- **Web funnels — BP-116..123** (`best-practices.md`): one promise from ad to
  landing to first product screen; one page, one job, with proof beside each
  CTA rather than in a bottom section most visitors never reach; pricing page
  as three tiers with one visibly recommended and annual framed in absolute
  money; signup asking the smallest identity that unblocks value (card only
  when the trial is deliberately opt-out); total price — currency, tax, fees —
  shown before the last step, wallets above the card form; abandonment as a
  designed branch with surviving state and a resume link, not a leak; dunning
  as a UX surface (pre-expiry notice, one-tap in-product card update, retries
  that end in a real message); cancel self-serve and honest with exactly one
  save offer.
- **Web-to-app funnels — BP-124..129**: the web funnel replaces onboarding,
  not just the paywall; the paid handoff is a first-class scenario with its
  failure branches (wrong account, mail never arrived, purchase not yet
  propagated, second device, refunded) — a paying user must never meet a
  paywall; context carried across the store gap by deferred deep link with a
  deliberately designed magic-link fallback; storefront rules as a per-region
  variable re-checked each ship (US external links after the April 2025
  ruling, entitlement elsewhere, EU its own regime, IAP as fallback); the tax,
  SCA, refund and invoice duties the store used to absorb; and one funnel
  measured web session → purchase → install → activation, not stopping at the
  sale.
- Two source keys — **[CRO26]** (Baymard checkout research, ChartMogul/Paddle
  trial and failed-payment data, landing/pricing-page A/B aggregations) and
  **[W2A26]** (RevenueCat/Adapty/Superwall funnel benchmarks, Apple/Google
  storefront policy after the 2025 US anti-steering ruling) — with an explicit
  note that their figures are industry aggregates the product's own numbers
  overrule.
- Tag taxonomy: `billing`, `cancel` (stage), `landing-page`, `web2app`
  (domain).

### Changed
- **`practice-selection.md` routes to the new sets.** New profile dimension
  **Purchase surface** (none / IAP / web checkout / web2app); Step-2 mandatory
  sets for web-direct money products (BP-116..123), for any off-store purchase
  (BP-127, BP-128) and for web2app (BP-124..126, BP-129); Step-3 checklists
  for landing/campaign page, web pricing page, abandonment recovery, dunning,
  and the web2app funnel + paid handoff, with the existing forms/checkout and
  cancel rows extended.
- **The foundation now declares where the money is taken.** `Purchase surface`
  added to the Monetization section (`scenario-format.md`,
  `templates/foundation.md`, `ux-foundation` skill and Cursor rule); money
  moments now name checkout, failed payment and cancel; when the surface is
  web or web2app, the web funnel and the paid handoff are flows of this
  product, held to the same rigor as in-app screens (`ux-flows`,
  `ux-scenarios` completeness checklists and Cursor rule).
- Plugin/marketplace descriptions de-numbered again — a practice count had
  crept back in and gone stale; they now say "a tag-indexed best-practices
  catalog". README says 129 and names the two new areas.

## 0.24.0 — 2026-07-29

Checked what the plugin claims about Figma against the official Figma MCP's
actual tools and their contracts. Several instructions would have failed.

### Fixed
- **The MCP gates its own tools behind guidance skills, and super-ux ignored
  two of the three gates.** `use_figma` requires `/figma-use` first,
  `create_new_file` requires `/figma-create-new-file`, `get_design_context`
  requires `/figma-design-to-code` — skipping them is the server's documented
  cause of hard-to-debug failures. Only the first was mentioned, and only in
  one step of the design loop; the preflight told the agent to call
  `create_new_file` and Improve mode to call `get_design_context` with no gate
  at all. All three are now stated where the call is made, with the
  `skill://figma/<name>/SKILL.md` fallback for setups without the slash
  commands.
- **"Create a Figma file" was an unrunnable instruction.** `create_new_file`
  needs a plan key (from `whoami`, asking the user when there are several
  teams/orgs) and an `editorType`; neither was mentioned.
- `generate_figma_design` was listed as a plain alternative for mockups. It is
  narrower than that — the server's own guidance reserves it for capturing a
  *web app* page pixel-perfect the first time, run beside `use_figma`; for
  non-web and from-scratch design, `use_figma` only. Stated as such, and as
  "where the setup exposes it", since not every install has it.

### Added
- **A tool map in `figma-integration.md`** — need → tool, for the whole
  surface the chain actually touches: writes (`use_figma`), structure reads
  (`get_metadata`), implementation reads (`get_design_context`), screenshots,
  variables (`get_variable_defs`), libraries, assets
  (`download_assets` / `upload_assets`), Code Connect, and FigJam. Explicitly
  a map, not a contract: a missing tool degrades to what is there, and the
  agent never invents a call. Plus how `node-id` and `fileKey` come out of the
  links `screens.md` already stores.
- **Drift checks that use the cheap tool.** Frame existence and naming are
  verified with `get_metadata` (ids, names, types, sizes — no full design
  context needed), in both directions: a listed state without a frame, and a
  frame whose `SCR-ID`/state is in no `screens.md` row.
- **Token parity is now checkable, not assumed.** `get_variable_defs` reads
  what a frame actually references, so "built on the style pack's tokens"
  becomes a verdict with evidence — a frame full of raw hexes is the
  design-side twin of hard-coded colors in code.

## 0.23.2 — 2026-07-28

Open-source hygiene pass — the repo is public, so the files a first-time
contributor looks for now exist.

### Added
- `SECURITY.md` — what the skill and its installer actually run (two `claude`
  calls, explicit argv, no network from the linter), what they write, and private
  reporting.
- `CODE_OF_CONDUCT.md` and a pull-request template that asks for the command
  output rather than a "tests pass" claim.
- README now points at the security policy and the code of conduct alongside
  contributing.

## 0.23.1 — 2026-07-28

### Changed
- Consistent American spelling across every agent-facing file (`labour` →
  `labor`, `honour` → `honor`, `neighbouring` → `neighboring`) — the docs
  were mixing both, which reads as sloppy in a repo whose whole pitch is that
  small inconsistencies compound.
- Reflowed three paragraphs left ragged by the previous pass's mechanical
  edits (`figma-integration.md` intro, the `ux-flows` build gate), and the
  build gate now names the style pack alongside the chain and the Figma
  mockups.

## 0.23.0 — 2026-07-28

Production pass over the public repo: every file read again, the remaining
contradictions fixed, and the front door rewritten for people who have never
seen this project.

### Fixed
- **The hard rule described a three-layer chain.** The most-copied text in the
  project — the rule installed into every `CLAUDE.md`, the always-on Cursor
  rule, the README, `/ux-rule`, the `ux-flows` build gate — said
  "foundation → flows → scenarios" while `screens.md` has been a first-class
  layer with its own same-change rule since 0.16.0. All five copies now say
  foundation → flows → **screens** → scenarios.
- **`ux-foundation` didn't know about a section it owns.** The contract gives
  `foundation.md` a Design tooling block (Figma on/off + file URL), but
  neither the skill nor its Cursor rule ever mentioned it, so the field was
  only ever filled by whoever happened to read the template. Both now cover it
  — and state that everything else visual (design system, style pack, frame
  links) belongs to `screens.md`.
- The README's mermaid diagram used `\n` for line breaks, which GitHub renders
  literally; it is `<br/>` now — and the diagram shows the current chain
  (foundation → flows → screens → scenarios → build → audit → plan) instead of
  the pre-flows one.
- `/ux`'s own description advertised "foundation/scenarios/audits"; menu item 3
  said "design user flows" without mentioning that it also registers screens.
  Inspect now also reports unexecuted plans in `docs/ux/plans/`.
- `ux-flows` Design had visual identity, wireframes, and Figma crammed into one
  numbered step; identity is now its own step, before anything gets drawn.

### Added
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — repo layout (including *why* the
  contracts are duplicated per skill), the edit → sync → validate loop, the
  conventions, how to test a change from a packed tarball rather than the
  working tree, and the release checklist.
- Issue templates for bug reports and ideas, both asking for the thing that
  actually resolves a report: the file that says otherwise, and the check that
  would fail.
- Validator check: the plugin description in `marketplace.json` must equal the
  one in `plugin.json` — the ecosystem requires both copies, so the duplication
  gets a check instead of trust.
- `package.json` gains a `bugs` URL; `.gitignore` covers `npm pack` tarballs.

### Changed
- **README restructured for a first-time reader**: what goes wrong and what
  super-ux does about it, the chain diagram, what you get, quick start per
  channel, the hard rule, the typical cycle, companions, then the internals
  (skills, commands, and a second table for the contracts). Value first,
  reference last.
- Manifest descriptions rewritten to describe the current system — the whole
  chain, the four skills, the linter, and the style pack — instead of the
  0.17-era feature list.
- The historical `docs/superpowers/` spec and plan carry a banner marking them
  as v0.1.0 provenance, with pointers to the live contract; they described two
  skills and four commands and are not maintained.

## 0.22.0 — 2026-07-28

### Added
- **The visual layer has an owner: the `sheleg-design` companion.** super-ux
  decided what every screen must contain and which craft floors it had to
  clear, then left the actual look to be invented frame by frame — the visual
  half of the drift this system exists to prevent. New reference
  [`visual-identity.md`](plugins/super-ux/skills/references/visual-identity.md)
  makes one **style pack** the identity for the whole product: picked with the
  sheleg-design skill (`workbench` for product UI, dashboards and tools;
  `instrument-console`; `editorial-luxury`; or a new pack authored on its
  contract), recorded once, obeyed everywhere. A cinematic scroll-driven
  landing also takes that skill's motion methodology.
- **`Style pack` field** in `screens.md` → Design system (contract + template).
  One owner per fact: the pack is named there and referenced from everywhere
  else, with its token file location beside it.
- **Wired into every design entry point** — `ux-flows` Design (before a frame
  is drawn, not after), `/ux` step 0 beside the Figma question, `/ux-flows`,
  the Figma design loop (pack tokens become the Figma variable collections),
  the Cursor `ux-flows` rule, the hard rule in `templates/claude-rule.md` and
  `/ux-rule`, and the seeded `docs/ux/README.md`.
- **Audited like any other record.** When a `Style pack` is recorded, the deep
  audit's practice pass checks the built UI honors it — tokens referenced
  instead of raw values, the pack's bans respected, dark mode from its twin;
  a screen ignoring the recorded pack is `drifted`. No pack and an improvised
  visual layer → the companion is suggested once, as an opportunity finding.
- Validator guard: the hard rule embedded in `/ux-rule` must be byte-identical
  to `templates/claude-rule.md`. They had already drifted apart in wording —
  two copies of a rule is the exact failure the plugin preaches against.

### Changed
- Recommendation, not dependency, in both directions: one offer with its
  one-time install, then the user's answer stands and the chain continues on
  platform defaults. A project that already has a design system records that
  instead — two identities are worse than any one.
- Conflict rule stated where both sides live (`practice-selection.md`,
  `ux-design-principles.md`): the style pack owns identity and wins on look;
  BP-079..090 are floors (contrast, tap targets, line length, spacing rhythm)
  and win on safety. The conflict and its resolution go in the compliance
  table.
- README gains a Companions table (sheleg-design at VISUALIZE/BUILD,
  task-pipeline after a plan) and the hard rule gains its style-pack bullet.

## 0.21.0 — 2026-07-28

Full-repo consistency pass: every file read, every contradiction between the
contract, the skills, the Cursor rules, the templates, and the tooling fixed.

### Fixed
- **`npx super-ux --cursor` crashed for every npm user.** `package.json`
  `files[]` never shipped `plugins/super-ux/scripts/ux_lint.py`, so the CLI
  installed the rules and templates and then died with an ENOENT stack trace
  while copying the linter (reproduced against a packed 0.20.0 tarball). The
  script is now in `files[]`, and a missing linter degrades to a warning with
  a download link instead of a crash.
- **The linter mis-read story priorities.** `ST-NNN` bodies were scanned with
  a fixed 600-character window, so a neighboring story's `**Priority:**`
  line leaked into the previous story and produced false "must/should story
  has no scenario" warnings. The scan now stops at the next heading.
- **The UX-plan example rendered broken.** The `` ```markdown `` block in the
  contract contained a nested three-backtick fence, which closed the outer
  block early and inverted the rest of the section; it is a four-backtick
  fence now.
- Duplicate `refs(flows, "SCR")` computation in the linter collapsed into one.
- `release.yml` referenced a `pipeline.example.json` path that does not exist
  in this repo and installed `jsonschema` the stdlib-only validator never
  used.

### Changed
- **One owner per fact:** `**Design system:**` is gone from `foundation.md` →
  Design tooling (it contradicted `screens.md`, `figma-integration.md`, and
  the templates). Foundation records the Figma on/off choice and the file
  URL; `screens.md` → Design system records the library, tokens, components,
  and assets. `figma-structure.md` and `system-map.md` say the same thing.
- Cursor rules resynced with ux-contract v4: `ux-flows` documented a stale
  `Screens & states` table (it is `Screens traversed` + the `screens.md`
  entry shape); `ux-scenarios` was missing the `Alt paths` field and the
  monetization entries of the per-product checklist; `ux-audit` said "git SHA
  of scenarios.md" (the contract says `docs/ux`) and never mentioned
  flow/screen conformance or the `coverage` scope; `super-ux` told Cursor
  users to run `/ux-lint`, a Claude-Code-only command.
- `/ux` reports every layer (it said "all three"); `/ux-init` is incremental —
  existing layers are left untouched and only the missing ones initialized,
  instead of talking about "both files" from a two-file era; README no longer
  says the skills CLI installs "both skills".
- `docs/ux/plans/` is created by the installers, `/ux-rule`, and `/ux`
  alongside `audits/` — the contract has required the directory since v4.
- `install.sh --help` described seeding one file; it seeds the whole skeleton
  plus the linter. README's Development section documents the four-way
  version sync and the `sync_references.py` step.

### Added
- Validator check: every asset `bin/super-ux.js` copies must be covered by
  `package.json` `files[]`, parsed from the CLI source rather than a
  hand-kept list — the packaging regression above cannot come back silently.
- `templates/flows.md` carries the contract's `Wireframe` field.

## 0.20.0 — 2026-07-28

### Changed
- Skill descriptions restructured English-first: every Russian trigger now sits
  beside its English equivalent (`"user flow" / "юзер флоу"`) instead of forming
  a Russian-only tail, and the `/ux` routing table follows the same pairing.
- README is English-only: the Russian section is gone, replaced by a plain
  statement of what the skill gives you and an author/links block.

### Added
- Validator enforces the three description canon rules on every skill —
  `Use when` opening, Russian trigger aliases present, front-matter under 1024
  characters. Twelve new checks; all four skills pass.

## 0.19.0 — 2026-07-25

Review pass — the contracts were not reaching non-Claude agents.

- **FIX (distribution): shared contracts now ship with every skill.** The skills
  CLI copies only a skill's OWN directory, so the sibling `skills/references/`
  reached Claude Code plugins but arrived **dangling on Cursor / Codex / OpenCode /
  OpenClaw / …** — `~/.agents/skills/ux-audit/` held nothing but `SKILL.md` while
  its SKILL.md called `scenario-format.md` a contract to "never deviate" from.
  Each skill now carries its own `references/` (the transitive closure of what it
  links) and links them `references/…`. `skills/references/` stays the source of
  truth; `test/sync_references.py` re-syncs; the validator fails on drift, on a
  missing shipped contract, on any `../references/` link, and on dangling links
  inside the copies.
- Cursor always-on rule gains the `screens.md` and linter bullets it was missing
  (it was two canon versions behind the Claude rule).
- `ux-scenarios.mdc` contract stamp corrected `scenario-format v1` → `ux-contract v4`.
- `system-map.md` lists `/ux-init`; README fixes "both skills" → "all four",
  "three agent-requested rules" → "four", and the release note now names
  `package.json` in the version-sync set (the validator has always enforced it).

All notable changes to this project are documented in this file. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions
follow [SemVer](https://semver.org/spec/v2.0.0.html).

## [0.18.0] - 2026-07-23

### Changed

- **Closing handoff to task-pipeline (recommended, not forced).** When an
  audit or Improve pass produces a UX plan, super-ux now states what the
  user has in hand (the plan, audit report, the `docs/ux/` chain, Figma
  frames) and recommends implementing it end-to-end by best practices with
  the ssheleg **task-pipeline** plugin — including the one-time install
  (`/plugin marketplace add ssheleg/task-pipeline` → `/plugin install
  task-pipeline@task-pipeline` → `/task-pipeline <plan file>`) — while making
  clear the user owns how they finish (superpowers writing-plans or by hand
  are equally fine). Wired into the UX-plan contract (`scenario-format.md`),
  `ux-audit`, `ux-flows`, `/ux` menu, the audit-report template, and the
  Cursor audit rule.

## [0.17.1] - 2026-07-23

### Fixed

- Manifest descriptions no longer hardcode a practice count ("100" was
  already stale at 115) — they now say "a tag-indexed best-practices
  catalog + PRN heuristics + component guidelines", so the catalog can grow
  without a description bump.

## [0.17.0] - 2026-07-23

### Added

- **Component & control guidelines** (`references/component-guidelines.md`)
  + 15 practices (BP-101..115) from verified design systems (Apple HIG,
  Material Design 3, W3C ARIA Authoring Practices Guide, GOV.UK Design
  System): a "which control for the job" decision table (radios vs
  checkboxes vs select, switch vs checkbox, action sheet vs alert, modal vs
  disclosure, combobox, bottom nav vs rail, FAB budget, dates, toasts) plus
  platform rules (one-primary/never-destructive-primary, focus-trap+ESC+
  return for modals, APG combobox roles/keys, every-control-ships-all-states)
  and the "use the platform component of record" stance. Taxonomy gains a
  Components group; practice-selection routes every graphical UI to
  BP-101..115; wired into `ux-flows` screen registration, the principles
  doc, and the system map.

## [0.16.2] - 2026-07-23

### Fixed

- Marketplace/plugin descriptions now reflect the full system (flows, the
  screens.md UI map with Figma frames, the linter, the practice catalog) —
  they had lagged at the foundation/scenarios/audit-only wording.

## [0.16.1] - 2026-07-23

### Fixed

- Consistency pass across all docs: unified every contract stamp to
  `ux-contract v4` (were mixed v2/v3/v4); added the `screens.md` MAP step
  and Figma mockups to the pipeline in `ux-design-principles.md` (8 steps,
  aligned with the v4 chain); `practice-selection.md` now spans the full
  catalog (BP-001..100) and routes Figma-enabled products to BP-091..100;
  README reflects 100 practices and links the Figma references. No
  behavioral change — documentation coherence only.

## [0.16.0] - 2026-07-23

### Added

- **Figma file-structure guide** (`references/figma-structure.md`) + 10
  practices (BP-091..BP-100) from verified sources (Figma Best Practices,
  Figma Learn, Design Systems Collective's 2025/26 Variables playbook,
  zeroheight): cover+index pages, one page per flow, **frames named
  `SCR-NN/<Screen>/<state>` to match `screens.md` exactly** (deterministic
  lookup, checkable drift), purpose-based code-matched naming, variables as
  three-tier tokens (primitive → semantic → component) with modes,
  variants-for-states vs components-for-objects, auto layout everywhere,
  build-on-the-library, layer hygiene, one-convention-plus-an-owner
  governance. Taxonomy gains `figma`/`design-system`/`handoff`/
  `maintainability`. Wired into `figma-integration.md`, the `ux-flows`
  design loop, and the system map.

## [0.15.0] - 2026-07-23

### Added

- **Deterministic linter** (`plugins/super-ux/scripts/ux_lint.py`, seeded
  into projects as `docs/ux/lint.py`, run via `/ux-lint` or
  `python3 docs/ux/lint.py`) — turns the prose rules into a check that
  fails: missing Figma frames per screen state (when Figma enabled),
  flows referencing non-existent `SCR-IDs`, unresolved scenario traces,
  must/should stories without scenarios, `built` screens without coverage,
  index↔entry desync, duplicate/gapped IDs, orphan screens, broken relative
  links. Stdlib-only, tolerant parsing (strips HTML comments so template
  examples never false-positive), exit codes 0/1/2, `--strict`. Wired into
  the hard rule, `/ux` inspect, and every skill's "run the linter after
  changes" pointer; recommended for CI/pre-commit.
- **System map** (`references/system-map.md`) — the whole pipeline, files,
  skills, and the four sync rules (chain-first, same-change, no-drift,
  run-the-linter) on one page; every SKILL.md opens with a pointer to it so
  an agent entering from any trigger sees the whole system. A project-facing
  copy (`templates/README.md` → `docs/ux/README.md`) is seeded too.
- Installers (`install.sh`, `bin/super-ux.js`), `/ux-rule`, and `/ux`
  repair now seed `docs/ux/README.md` and refresh `docs/ux/lint.py`. The
  plugin validator compiles the linter.

## [0.14.0] - 2026-07-23

### Added

- **UI Screen Registry** (`docs/ux/screens.md`, ux-contract v4) — the
  canonical design map: one entry per screen with a stable `SCR-NN` id,
  every state (loading/empty/error/success) carrying its own Figma frame
  link, plus wireframe, code coverage, scenarios touching it, related
  UX/UI resources (components, tokens, assets, data deps), and a Status
  (designed → built → drifted → retired). A Design system block records the
  Figma library and where tokens/components/assets live in code. Flows now
  reference screens by `SCR-ID` instead of duplicating specs, so a screen
  used by many flows is described once.
- **Same-change update rule extended to the UI**: any interface change must
  update `screens.md` (and, when Figma is enabled, the Figma frame plus its
  link) in the same change; code diverging from a screen's record or a
  stale/broken Figma link is a `drifted` finding. Wired into the hard rule
  (template, /ux-rule, super-ux.mdc, README), `ux-flows` Update, and
  `/ux-update`.
- **Audit drift + coverage** now check code vs the screen registry (states
  rendered, elements present, coverage accurate → `drifted`), Figma-link
  presence per state, and registry orphans (screens unused by flows, flows
  referencing missing SCR-IDs).
- `ux-flows` owns and maintains `screens.md`; templates, installers
  (`install.sh`, `bin/super-ux.js`), `/ux` skeleton, and `/ux-rule` seed it.

## [0.13.0] - 2026-07-23

### Added

- **Figma design integration** (`references/figma-integration.md`), an
  opt-in surface enabled by default: the agent asks once at the start of
  design whether to mock up in Figma; if yes and the Figma MCP isn't
  connected it recommends connecting it (never blocks — degrades to
  markdown + wireframes and syncs later); records the Figma file in
  `foundation.md` → Design tooling before drawing; during `ux-flows` Design
  mirrors every screen-state into a Figma frame applying the visual-craft
  practices (BP-079..090) as hard constraints; **every screen row carries
  its Figma frame deep-link** (flows.md Screens & states gains a Figma
  column) — a screen without a frame link is an incomplete-design finding.
- **Explicit build gate** in the hard rule (templates/claude-rule,
  /ux-rule, super-ux.mdc, README, ux-flows DoD): do NOT write interface
  code until the UX workflow is done — chain designed and approved, and
  (Figma on) the UI mocked up with every screen linked. Stated plainly to
  the user, who is not expected to know the internals.
- Foundation gains a Design tooling section; `/ux` step 0 asks the Figma
  question for design tasks; `/ux-flows` and the Cursor flow rule updated.

## [0.12.1] - 2026-07-23

### Fixed

- Consistency audit across all documents: `templates/scenarios.md` and
  `templates/audit-report.md` brought up to ux-contract v3 (Traces column,
  action→response steps, Alt paths; Depth/passes header, Context line,
  Practice compliance section); hard-rule text unified across
  `templates/claude-rule.md` and `/ux-rule` (chain wording, all four
  skills, `/ux` entry point; `/ux-rule` now replaces outdated rule blocks);
  `/ux-update` routes feature ideas through the full chain and cascades to
  flows; Cursor `ux-scenarios` rule Index gains Traces; README practice
  count corrected to 90 and hard-rule section aligned; installers
  (`install.sh`, `bin/super-ux.js`, `/ux` repair, `/ux-rule`) now seed all
  three templates (scenarios, foundation, flows), never overwriting.

## [0.12.0] - 2026-07-23

### Added

- **Visual craft in the catalog** (BP-079..BP-090): body-text baseline
  (16px / 1.5 line height / 45–75 CPL, target ~66 — Baymard, USWDS, Dyson &
  Haselgrove research chain), single type system (≤2 faces, 1.3–1.6×
  heading scale), contrast floors with softened extremes (WCAG 4.5:1, no
  harsh #000-on-#FFF), 60-30-10 palette with one scarce accent, semantic
  colors as a contract (never repurposed, never color-only), dark mode as a
  designed palette (gray surfaces, desaturated accents, tonal elevation),
  4/8pt spacing grid with proximity-as-grouping, whitespace-as-hierarchy,
  single-grid alignment, tabular figures for data, microcopy rules (verbs,
  sentence case, stable action names), decoration subtraction. New tag
  group "Visual craft".
- Selection protocol: "any graphical UI" mandatory set (BP-079..090) +
  artifact rows for screen build/polish, reading surfaces, data tables.

## [0.11.0] - 2026-07-23

### Added

- **Practice Selection Protocol** (`references/practice-selection.md`) —
  the deterministic bridge between the catalogs (BP-001..078, PRN-01..16)
  and the design/audit functions: product profile (platform, money model,
  distribution, acquisition, forms, analytics) → mandatory consideration
  sets → per-artifact checklists (onboarding, paywall, upgrade-at-limit,
  trial, winback, rating prompt, forms, navigation, permissions,
  lifecycle, voice/chat, empty states, store listing, experiments) →
  compliance table with verdicts applied/adapted/rejected(reason)/
  deferred(trigger)/missing. No silent skips; no cargo-culting
  (consideration is mandatory, adoption only when a traced job is served);
  user-owned rejections recorded and not re-litigated.
- **Design function**: `ux-flows` Design gains a mandatory Practice pass —
  compliance table attached to every flow entry before approval.
- **Audit depth levels**: `quick` (scenarios), `standard` (+ flow
  conformance, default), `deep` (+ heuristic pass, practice pass via the
  protocol, chain coverage) — five ordered passes; report format gains
  Depth and a Practice compliance section.

## [0.10.0] - 2026-07-23

### Added

- **Monetization economics in the catalog** (BP-067..BP-078, sourced from
  RevenueCat State of Subscription Apps 2025, OpenView/ProductLed 2025
  benchmarks, converged ASO 2025 guidance): model choice with data (hard
  paywall ~5× freemium download-to-paid; hybrid beats subscription-only),
  first-session paywall placement (>80% of trials start day 0), trial
  design levers (opt-out ~31% vs opt-in ~9%; 17–32-day trials ~46% only
  with engagement), the 14-day conversion window, activation before
  monetization pressure, visible value-metric freemium boundaries,
  upgrade-at-limit triggers, store listing as onboarding screen zero
  (screenshots move conversion 20–35%), the 4.0+ rating loop,
  ad→listing→onboarding coherence, web-to-app funnels.
- **Monetization as a foundation layer**: `foundation.md` gains a
  Monetization section (model + reason, value metric, free boundary, money
  moments, acquisition coherence); money moments become first-class flows
  (paywall, upgrade-at-limit, trial start/end, cancel/winback, rating
  prompt); per-product scenario checklist extended accordingly;
  `ux-foundation` interview asks how the product earns.

## [0.9.0] - 2026-07-23

### Added

- **Catalog expansion from verified sources** (BP-049..BP-066, 18 entries):
  mobile interfaces (thumb-zone placement, platform tap-target sizes with
  the WCAG 2.2 24px floor, gesture affordances, visible navigation, current
  platform design languages — Apple HIG/Liquid Glass 2025, Material 3
  Expressive — motion-as-feedback); web apps & forms (Baymard-backed field
  minimization, guest-first flows, address automation, INP ≤200ms feedback
  budgets, WCAG 2.2 AA baseline); voice & conversational (tiered
  confirmations, echo-what-was-heard error recovery, barge-in, deviation
  tolerance, multimodal pairing, short latency-cued turns, honest AI
  limits). Tag taxonomy extended: voice, ai-chat, web, android, forms,
  checkout, navigation, accessibility, performance, feedback,
  error-recovery.
- **Plain-language routing in `/ux`**: the user never needs to know skills
  or layers — step 0 asks one everyday-words question (or reads
  `$ARGUMENTS`) and maps intent to the right workflow via a routing table;
  README gains a "one command, plain words" section.

## [0.8.0] - 2026-07-23

### Added

- **ux-flows skill** — the HOW layer (`docs/ux/flows.md`): task analysis →
  mermaid user flows (screens, explicit branches, recoverable error edges,
  all entry points) → screen/state tables → optional ASCII wireframes and
  storyboards. Workflows: Design (forward), Reverse (backwards mode for
  existing products, `inferred` tags with file:line evidence), Update,
  Improve (heuristic evaluation → traced before/after redesign proposals).
- **ux-design-principles.md** — the agent's thinking playbook: the 7-step
  pipeline (research → define → structure → specify → visualize → build →
  verify) with forward and backwards modes, task-analysis method, flow and
  screen rules, heuristics PRN-01..10 (after Nielsen) and cognitive
  principles PRN-11..16 with audit questions, the improvement procedure,
  wireframe/storyboard conventions, anti-patterns.
- **ux-contract v3** — scenarios become use cases: steps as `user action ->
  system response`, new `Alt paths` field, `Traces` includes `FLW-NN`;
  traceability now covers flows (every node and edge needs a scenario).
- `ux-audit`: verifies code against flow diagrams (nodes reachable, edges
  wired, states present); new `heuristics` scope (`[PRN-NN]` findings).
- `/ux-flows` command; `/ux` menu grows to 11 actions including "Improve
  existing UX"; `/ux-init` now chains foundation → flows → scenarios.
- **UX plans** (`docs/ux/plans/YYYY-MM-DD-<scope>.md`) — the actionable
  output of audits and Improve passes: target interface per affected screen
  (elements, one primary action, states, behavior notes) + a
  CREATE/MODIFY/DELETE change table where every row traces to
  scenario/flow/finding/principle IDs, prioritized by Frequency × Severity
  × Solvability, with a Definition of Done and an autonomous-execution
  handoff (task-pipeline plugin if installed, else superpowers
  writing-plans). Plans are written to be executable without the
  originating conversation.

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
