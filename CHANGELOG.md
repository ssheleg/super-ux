# Changelog

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
