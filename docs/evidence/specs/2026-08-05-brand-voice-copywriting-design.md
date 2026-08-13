# Design — the verbal identity layer: `brand-voice` + `copywriting`

Date: 2026-08-05
Status: approved (design), pending implementation plan
Target release: super-ux v0.30.0

## 1. The problem

super-ux decides **what the interface must be** and, through the
`sheleg-design` companion, **how it looks**. Nothing in the system decides
**how it speaks**. The consequences are already visible in real projects:

- The same action is named two different things on two screens, and no
  linter can see it — the chain is internally consistent either way. This is
  the verbal twin of the contract drift `ux_doctor` was built to catch.
- Marketing surfaces (landing, blog, social, store listings) are written in
  whatever register the session happened to produce, so a product reads like
  three different companies.
- Public copy quotes numbers that exist nowhere as a checkable fact.
- Copy written for search engines drifts into over-optimization — stuffing,
  filler openers, unearned superlatives — which now costs visibility instead
  of buying it.

A survey of ~40 copy/brand/SEO skills installed on this machine found no
skill that (a) derives voice from an existing product model, (b) checks
string consistency across a whole interface, (c) anchors copy to `file:line`,
or (d) separates one product voice from per-surface register as a contract.
The closest prior art — `prowl-brand` — does all of this in prose for a
single product, with no portable contract.

## 2. Decisions locked

These were decided in brainstorming and are not open in the plan:

| # | Decision |
|---|---|
| D1 | **Full vertical stack.** The skill owns UI copy, marketing copy, blog, social, email, store listings, ads, and SEO/AEO. No dependency on `marketing-skills`, `notfair`, or `seo-aeo-audit`. |
| D2 | **Artifact root is `docs/brand/`**, multiple files, not `docs/ux/`. Brand is wider than UX; each file loads on demand. |
| D3 | **Voice pack library + per-project calibration.** Six shipped archetypes; the pack is a starting position, `voice.md` is the truth. |
| D4 | **`brand_lint.py` + a hard rule in the project's `CLAUDE.md`.** Errors block, like the scenario-first rule. Taste stays in the audit. |
| D5 | **Multi-locale from day one.** `locales/<code>.md`, parity reporting, length coefficients. |
| D6 | **Topology B**: two new skills split by verb (`brand-voice` defines, `copywriting` produces), plus a new `copy` scope inside the existing `ux-audit`. |
| D7 | **All skill content, references, templates, linter messages, spec, and plan are written in English**, like the rest of super-ux. |

## 3. Scope

**In scope.** The `docs/brand/` contract; the `brand-voice` skill (init,
calibrate, update, validate); the `copywriting` skill (write, edit, adapt,
humanize) across product and marketing surfaces; six voice packs; the
surface/channel register model; locale handling; `brand_lint.py`; the
`copy` audit scope; catalog additions; templates; installer, cursor rule,
doctor, validator, and README wiring; release v0.30.0.

**Out of scope.** Translation itself (this is not an i18n runtime, and
`strings.md` is not a message catalog). Visual identity — unchanged,
`sheleg-design` keeps it. Paid-media buying strategy, budget, and targeting;
only ad *copy* is in scope. Analytics instrumentation; `Telemetry` on
scenarios already covers it. Rewriting the existing four UX skills beyond the
integration points named in §11.

## 4. Architecture and ownership

```
foundation.md  (WHY: personas, JTBD, journeys, stories)
     |
     +--> docs/brand/       VOICE — who speaks, how, in whose words, on what proof
     |         |
     |         +--> interface strings   <-> scenarios.md / screens.md
     |         +--> marketing surfaces  (landing, blog, social, store, ads, email)
     |
     +--> flows.md -> screens.md -> scenarios.md  (WHAT)
```

**The dependency is one-way.** The brand pack derives from the foundation;
the foundation never changes because a tone was appealing. With no
`foundation.md`, `brand-voice` runs degraded (reverse from code + interview),
stamps `Derived-from: inferred`, and recommends building the WHY layer first.

| Question | Owner |
|---|---|
| Who the user is, what job the product is hired for | `ux-foundation` |
| Which screens and states exist, what an element does | `ux-flows` / `ux-scenarios` |
| What voice the product speaks in; which words are ours and which are banned; which numbers it may quote | **`brand-voice`** |
| Register on a given surface (landing vs tooltip vs Reddit) | **`brand-voice`** (`channels.md`) |
| The actual text: a button label, a headline, a thread, a store description | **`copywriting`** |
| Palette, type, motion | `sheleg-design` (companion, unchanged) |
| Whether shipped text matches the pack | `brand_lint.py` + `ux-audit` scope `copy` |

**Hard boundary:** `copywriting` never writes to `docs/brand/`. When a needed
term is absent from the dictionary or a number is absent from the facts file,
it stops and says so. A missing fact is reported, never invented to close a
gap.

## 5. Artifact contract — `docs/brand/`

Contract marker `Contract: brand-contract v1` in the header of every file,
same shape as `ux-contract`, so `ux_doctor.py` can detect drift.

| File | Holds |
|---|---|
| `voice.md` | identity: pack, five axes as IS / IS NOT, narrative, locale-transfer rules, trace to foundation |
| `terminology.md` | our term -> banned generic word; entity and tier names; banned list; glossary |
| `facts.md` | canonical numbers, proof, quotes, disclaimers, legal lines — the only source of any figure in public copy |
| `channels.md` | one record per surface: register deltas, format, limits, bans, CTA policy, proof policy |
| `strings.md` | interface string registry: key -> text -> `file:line` -> scenario -> status |
| `locales/<code>.md` | per-locale delta: address form, humor, length coefficient, keywords, what never translates |
| `README.md` | project-side map of the above (seeded) |
| `lint.py` | project copy of `brand_lint.py` (seeded by the installer) |

### 5.1 `voice.md`

```markdown
Contract: brand-contract v1
Voice pack: operator-brief          # one of the six, or `custom`
Locales: en (primary), ru, de
Locale parity threshold: 80%
Derived-from: PER-01, PER-03, JTBD-02
Status: draft | validated
Last calibrated: 2026-08-05

## Axes
| Axis       | The product IS | The product IS NOT |
| Confidence | ...            | ...                |
| Register   | ...            | ...                |
| Distance   | ...            | ...                |
| Humor      | ...            | ...                |
| Density    | ...            | ...                |

## Narrative
Hero:    <the user, in which role>
Enemy:   <what stands in the way — a state of the world, not a competitor>
Product role: <guide | weapon | instrument>
Promise: <one line, checkable against a fact in facts.md>

## Invariant in every language
- <e.g. never hedges>

## Reconsidered per locale
- <e.g. address form, humor level>
```

`Status` follows the same lifecycle as scenarios: `draft` until the user has
seen and approved it, then `validated`. Any edit drops it back to `draft`.

### 5.2 `terminology.md`

```markdown
Contract: brand-contract v1

## Product terms — always
| Our term | Never write | Applies to |

## Entity and tier names — exact spelling
| Name | Wrong forms seen |

## Banned
| Word or phrase | Why | Use instead |

## Glossary
| Term | Meaning |
```

The banned table seeds from three sources at init: buzzwords and weak verbs
(utilize, leverage, seamless, robust, cutting-edge), hedging chains, and the
AI-marker vocabulary in `ai-tells.md`. The calibration pass adds
product-specific bans.

### 5.3 `facts.md`

```markdown
Contract: brand-contract v1

| Fact | Value | Source | Checked | Review by | Public |
|------|-------|--------|---------|-----------|--------|
```

`Public: no` marks internal figures that must never appear in copy. A fact
past `Review by` is a lint warning; a fact with no `Source` is a lint
warning. A number in public copy with no matching row is a lint **error**.

### 5.4 `channels.md`

One record per surface:

```markdown
### <surface>
Register:   deltas from the base voice (e.g. "humor -2, distance -1, density +1")
Format:     length, structure, required elements
Limits:     characters / fields — platform physics
Forbidden:  physics: <what the platform penalises> | brand: <what we don't do>
CTA:        policy
Proof:      which proof types belong here
Locales:    where this surface behaves differently
```

**Register moves the axes; it never crosses the invariants** listed in
`voice.md`. A Reddit post may be longer, CTA-free, and self-deprecating — but
a brand that does not hedge does not hedge there either.

**Platform physics and brand choice are different fields, deliberately.**
"A link in the tweet body suppresses reach" and "our brand does not post
links" are different claims; merging them makes it impossible six months
later to tell an algorithm constraint from a decision.

Surfaces shipped in the template:

*Product:* primary action · empty state · error · loading · success/toast ·
onboarding · paywall and upgrade · destructive confirm · billing and receipts ·
settings and legal · transactional email and push · docs and help.

*Marketing:* landing hero · landing body · pricing · blog · changelog · X ·
Reddit · LinkedIn · HN / Product Hunt launch · App Store · Google Play · ads ·
lifecycle email.

**One non-negotiable rule across all packs:** humor, exclamation marks, and
emoji are forbidden on error, destructive confirm, and billing surfaces —
including in `playful-consumer`. The user is losing data or money at that
moment. This is enforced by the linter (`B061`), not left to taste.

### 5.5 `strings.md`

```markdown
Contract: brand-contract v1

| Key | Text (primary) | Location | Scenario | Status |
|-----|----------------|----------|----------|--------|
| action.project.publish | Publish | src/ui/ProjectBar.tsx:47 | SCN-014 | agreed |
```

Statuses: `agreed` · `proposed` · `drifted` · `orphan`.

**This is a decision registry, not a message catalog.** It does not replace
i18n keys and does not hold translations. It records which strings have been
reconciled with the pack, which scenario each serves, and where it lives. It
is what makes the check "one action, two names" possible at all; without it
that defect is only findable by reading the entire interface.

It is populated by an inventory sweep at init — the same method
`ux-scenarios` uses on an existing codebase — not by hand.

### 5.6 `locales/<code>.md`

```markdown
Contract: brand-contract v1
Locale: de
Primary: no
Address form:        Sie
Length coefficient:  1.30
Humor:               -1 from base
Never translated:    product name, entity names, tier names
Keywords:            own research, not translated from primary
Dead idioms:         <base-voice idiom> -> <replacement>
Legal differences:   Impressum, VAT-inclusive pricing
```

Two rules:

1. **The primary locale is the source of meaning, not of form.** A
   word-for-word CTA translation is a finding even when grammatically
   perfect.
2. **A locale need not be complete, but must declare that it lags.** The
   linter reports parity ("de: 68% of strings, 14 behind en") instead of
   letting an incomplete locale look finished.

## 6. Voice pack library

Six packs ship in `references/voice-packs.md`. Each conforms to a pack
contract so a seventh can be authored rather than improvised.

| Pack | For | Core |
|---|---|---|
| `operator-brief` | infrastructure, security, devtools, intelligence | short declaratives, command verbs, tension before solution, zero hedging |
| `calm-expert` | fintech, health, compliance, enterprise B2B | quiet authority, states its limits before anyone finds them, never manufactures urgency |
| `peer-builder` | dev tools, open source, APIs | peer to peer, technical honesty, "here is where it breaks" as part of the pitch |
| `editorial-premium` | brand-led, media, design products | rhythm over density, metaphor rationed, silence as a device |
| `plain-service` | government, utilities, mass-market services | GOV.UK school: no ornament, the short word over the precise long one, readable under stress |
| `playful-consumer` | consumer apps, habit, wellness, social | warmth and lightness; humor serves comprehension, never draws attention to itself |

Pack contract — required fields:

```
Name · Use for · Not for
Axes (all five, filled as IS / IS NOT)
Narrative template (hero / enemy / product role)
Lexicon (favoured verbs, typical structures, sentence length)
Pack bans (what it never does)
Register deltas per surface
Ready lines (6–10 samples — how it sounds, not what to copy)
Failure mode
```

`Failure mode` exists in no surveyed skill and the library is harmful without
it. Every voice has a degenerate form: `operator-brief` becomes military-jargon
parody, `playful-consumer` becomes cringe, `calm-expert` becomes corporate
mush, `editorial-premium` becomes beautiful emptiness. A pack must describe
its own overshoot, which makes it checkable in the audit instead of being a
matter of opinion.

**Selection.** `brand-voice` reads `foundation.md` (personas, JTBD, and what
the user loses when the product fails), scans existing copy and code, and —
where available — reviews and competitor copy. It proposes **one** pack with
reasoning plus one alternative. Then calibration: dictionary, canonical
facts, bans, ready lines. After calibration `Voice pack:` keeps the pack name
for provenance, but `voice.md` is the truth.

## 7. Skills and command surface

### `brand-voice` (new skill)

Modes, mirroring `ux-foundation`: **Init** (greenfield or existing code) ·
**Calibrate** · **Update** · **Validate**.

Invoked with no task, it reports status and proposes exactly one next action
— the pattern proven in `prowl-brand`. Status covers: is a pack recorded,
`voice.md` status, unresolved `TBD` facts, locale parity, open linter
findings.

### `copywriting` (new skill)

Modes: **Write** (a surface named in `channels.md`) · **Edit** (seven-sweep
pass: clarity, voice and tone, so-what, prove-it, specificity, emotion, zero
risk) · **Adapt** (repurpose one piece across channels without flattening it
to one register) · **Humanize** (AI-marker removal under the guards in §9).

First action in every mode is to read the brand pack. No pack -> hand off to
`brand-voice`; never improvise a voice.

### Commands

| Command | Does |
|---|---|
| `/brand` | single entry: inspect -> silent repair -> status -> menu with one recommended action |
| `/brand-init` | initialize the pack |
| `/brand-update` | recalibrate after foundation or positioning changes |
| `/brand-lint` | run `python3 docs/brand/lint.py` |
| `/copy` | write or edit copy for a surface |

## 8. `brand_lint.py`

Ships at `plugins/super-ux/scripts/brand_lint.py`, installed into projects as
`docs/brand/lint.py`. Stdlib-only, matching `ux_lint.py` and `ux_doctor.py`.
Read-only by default; `--fix` applies only the mechanical subset. Flags
`--brief` and `--json` follow the doctor's precedent.

**Design rule:** the linter checks only what a machine can prove. Everything
evaluative goes to the audit. This is the same split that already exists
between `lint.py` and `ux-audit`.

### 8.1 Scan surface

The linter cannot guess where a project keeps its text, so `docs/brand/README.md`
carries a `Sources:` block that names it. Nothing outside these paths is
scanned, and a missing block is `B006` (error) — the linter refuses to report
a clean run over a surface it never read.

```markdown
Sources:
  ui:        src/**/*.{ts,tsx,js,jsx,vue,svelte}   # interface strings
  marketing: content/**/*.{md,mdx}                  # landing, blog, pricing
  store:     store/{ios,android}/*.md               # listing fields
  robots:    public/robots.txt
  locales:   src/locales/*.json                     # optional; enables parity
```

`ui` and `marketing` classify a finding as an interface string or as public
copy — several checks apply to only one of the two. A project may declare any
subset; checks whose source is absent are skipped and counted as skipped in
the summary, never silently passed.

### 8.2 Checks

| Code | Severity | Check |
|---|---|---|
| B001 | error | `docs/brand/` present but no contract marker, or unknown version |
| B002 | error | mixed contract versions across brand files |
| B003 | warn | `voice.md` is `draft` while `strings.md` treats it as validated |
| B004 | error | `Derived-from:` references a persona/JTBD id absent from `foundation.md` |
| B005 | warn | foundation personas changed after `Last calibrated` |
| B006 | error | `docs/brand/README.md` has no `Sources:` block, so there is nothing to scan |
| B010 | error | banned word from `terminology.md` in an interface string or public copy |
| B011 | error | generic word used where the dictionary mandates a product term |
| B012 | error | entity or tier name spelled inconsistently |
| B020 | error | one action, two names (same scenario/action, two string values) |
| B021 | error | string in code diverged from the registry |
| B022 | warn | interface string in code with no registry entry |
| B023 | error | registry entry pointing at a `file:line` that no longer exists |
| B024 | error | declared casing violated (e.g. sentence case) |
| B025 | warn | button label is not a verb phrase ("OK", "Submit") — BP-089 |
| B030 | error | number, percentage, or currency in public copy absent from `facts.md` |
| B031 | warn | fact with no source, or past its `Review by` date |
| B032 | error | superlative with no adjacent fact reference |
| B040 | error | field over the channel limit, locale length coefficient applied |
| B041 | error | iOS keyword-field violation (space after comma, plural duplicate, word already in title) |
| B042 | error | link in post body where the channel forbids it |
| B043 | warn | more hashtags than the channel allows |
| B050 | error | robots.txt blocks GPTBot / ClaudeBot / PerplexityBot / Google-Extended while `channels.md` declares AI search a target |
| B051 | error | in a `marketing` document, any single non-stopword token exceeds 1% of the document's word count — measured without needing a declared target keyword |
| B052 | error | filler opener ("In today's digital landscape", "In the ever-evolving world of") |
| B053 | warn | no author or byline where the channel requires E-E-A-T |
| B054 | warn | title promises what the body does not deliver |
| B060 | warn / error | AI-marker density in `marketing` documents: S1/S2/S3 scoring with an A–D naturalness grade; warning at any S1 or 3+ S2, error at 3+ S1 |
| B061 | error | humor, exclamation mark, or emoji on error, destructive confirm, or billing surfaces |
| B070 | error | declared locale with no `locales/<code>.md` |
| B071 | warn | locale parity below `Locale parity threshold` in `voice.md`, reported as a percentage; requires a `locales` source |
| B072 | warn | locale string looks like a word-for-word translation of the primary CTA |
| B073 | error | field overflow under the locale's length coefficient |

`--fix` subset — changes that cannot be wrong: casing normalisation (B024),
iOS keyword-field cleanup (B041), registry re-pointing after a file move
(B023 where the string is unchanged and found at exactly one new location).
Everything else is reported for a human.

Exit codes: `0` clean, `1` warnings only, `2` errors present.

**Hard rule.** The project `CLAUDE.md` gains a `## Brand voice — hard rule
(super-ux)` section, in the same shape as the existing scenario-first rule:
public-facing text changes update `docs/brand/` in the same change, and
`python3 docs/brand/lint.py` must exit clean before work is called done.

## 9. SEO/AEO: safety versus optimization

Two modes, deliberately separated:

**Safety** — always on, enforced by the linter. Stuffing, filler,
clickbait mismatch, blocked crawlers, unearned superlatives, missing byline.
This is what makes a site read as honest rather than as an attempt to game a
crawler.

**Optimization** — on request, in `copywriting`. Front-loading the answer in
the first 150 words, evidence density, tables instead of prose for
comparisons, schema, entity clarity, per-engine differences (Perplexity
weights freshness, AI Overviews weight E-E-A-T, Claude relies on training
data rather than live browsing).

**One absolute prohibition, above every setting: fabricated facts, quotes,
statistics, or experts are a hard fail, not a score reduction.** The Princeton
GEO work (KDD 2024) did show a lift from fabrication against GPT-3.5 in 2023;
it is now trained on as an adversarial signal, creates FTC §5 exposure, and
the lift evaporates under competition (C-SEO Bench, NeurIPS 2025). Real
evidence delivered through the same structural pattern captures 80–90% of the
effect with none of the risk. If a user explicitly asks for fabricated
figures, refuse and explain.

### Humanization guards

Borrowed from the `humanizer` methodology, which is the only surveyed skill
that treats de-AI-ing as measurable engineering:

- **Severity scale** S1 / S2 / S3 per marker, and an A–D naturalness grade on
  the *result*, not the input.
- **Change-rate guard:** if a rewrite alters more than 50% of the text, do not
  ship it — report the rate and ask, because the meaning has probably moved.
- **Mandatory semantic-preservation self-check** before output: numbers,
  dates, and proper nouns intact; causal direction not reversed; negations not
  inverted; direct quotes untouched; the core claim unchanged.
- **Density threshold** from `content-humanizer`: above ~10 markers per 500
  words, a patch is futile — say so and rewrite rather than polish.

## 10. `ux-audit` scope `copy`

A new single-pass scope, not a new skill. It judges what the linter cannot
prove, with `file:line` evidence and the same verdict vocabulary as every
other audit pass:

- tone drift from the recorded pack;
- the "could this sit on any other SaaS page" test;
- so-what failures (features with no benefit bridge);
- claims with no proof nearby;
- narrative coherence (hero, enemy, promise) across surfaces;
- **pack failure-mode detection** — the voice overshooting into its own
  degenerate form;
- register mismatch against `channels.md`.

Findings feed the existing fix-plan flow (`docs/ux/plans/`) unchanged.

## 11. Integration points

| Touchpoint | Change |
|---|---|
| `/ux` status | new brand-layer row: pack present, `voice.md` status, locale parity, open brand-lint findings |
| `ux_doctor.py` | learns the `brand-contract` marker so brand drift is visible to the doctor, not just the linter |
| `ux-scenarios` | scenario contract gains an optional `Strings:` field listing registry keys — same shape as the optional `Telemetry`, `Kill criteria`, and `Verdict` fields added in v0.28–0.29 |
| `references/system-map.md` | the brand layer added to the pipeline diagram and the file table |
| `templates/` | new `brand/` subdirectory: `voice.md`, `terminology.md`, `facts.md`, `channels.md`, `strings.md`, `locale.md`, `README.md` |
| `bin/super-ux.js` | seeds `docs/brand/` and copies `brand_lint.py`; asset paths stay literal strings so `test/validate.py` can regex them |
| `package.json` `files` | `plugins/super-ux/scripts/brand_lint.py` added |
| `cursor/rules` | brand rule added alongside the UX rules |
| `templates/claude-rule.md` | the brand hard rule appended |
| `README.md` | new skills, commands, and the brand layer documented |

## 12. New references

Authored in `plugins/super-ux/skills/references/`, distributed to skills by
the existing `test/sync_references.py`:

`brand-contract.md` · `voice-packs.md` · `surface-registers.md` ·
`ui-copy.md` · `marketing-copy.md` · `channel-playbooks.md` ·
`seo-aeo-safety.md` · `ai-tells.md` · `localization.md` · `store-copy.md`

`marketing-copy.md` carries the seven-sweep editing pass and the *grounding*
model for long form (a concept must be grounded before a later block leans on
it; the lever is what is made a prerequisite versus introduced in the text).
`store-copy.md` carries per-platform field limits and the iOS keyword-field
rules.

## 13. Catalog additions

- Practices start at **`BP-182`** (`BP-181` is the current maximum).
- Exactly three new principles, `PRN-22` through `PRN-24` (`PRN-21` is the
  current maximum): **PRN-22** one voice, many registers — a register may move
  the axes but never cross an invariant; **PRN-23** every claim is checkable —
  a number in public copy exists as a sourced fact or is not written;
  **PRN-24** the interface never jokes about the user's loss — humor is
  forbidden where data, money, or access is at stake.
- New tags: `brand-voice` `copy` `narrative` `terminology` `channel-physics`
  `seo` `aeo` `aso`. **The existing `voice` tag is reserved for voice
  interfaces (VUI) and must not be reused**; `i18n` already exists and is
  reused rather than duplicated.
- Six clusters, **at least four practices each, 24 minimum** in one contiguous
  run from `BP-182`: voice and consistency · product microcopy (extending
  BP-089) · conversion copy · bot safety · channel physics · localization.
- Every new practice carries `Source:` and `Checked:` with a date. Given D1
  (no dependency on the upstream marketing skills), this is the mechanism
  that keeps divergence from `marketing-skills` and `notfair` a visible fact
  in the catalog rather than silent staleness.
- `bp_index.py` is re-run; the validator's index-freshness check covers the
  new entries.

## 14. Testing

**TDD throughout:** failing test, minimal implementation, green, commit.

`brand_lint.py` unit tests — one fixture directory per check code, each
asserting the code fires on the violation and stays silent on the clean
variant, plus `--fix` idempotence tests for the three fixable codes and exit
code assertions (0/1/2).

`test/validate.py` extensions:

- every `templates/brand/*.md` carries the contract marker;
- references are in sync across skills (existing check, new files included);
- the npm payload includes `brand_lint.py` (literal-path regex — the reason
  installer paths must not be built in a loop);
- the practices index is fresh;
- every practice at or above `BP-182` has non-empty `Source:` and `Checked:`;
- no new practice uses the `voice` tag.

## 15. Release

v0.30.0 through the standard cycle: version bump across `package.json` and
both plugin manifests, CHANGELOG entry, README, wiki, atomic tag and push, CI
validate and release, npm publish. Then the standing rule — refresh local
installs with `npx --yes sshlg-skills@latest update`, and remind about the
Claude Code restart, since skills load at session start.

## 16. External dependencies

None. `brand_lint.py` is stdlib-only, matching `ux_lint.py` and
`ux_doctor.py`; the installer is existing Node with no new packages. There is
no external library, SDK, or API whose contract needs verification against
current documentation, so no Context7 lookup applies to this design.

## 17. Risks and non-goals

- **Registry adoption cost.** On a large existing product the inventory sweep
  will produce hundreds of `B022` warnings. Mitigation: `B022` is a warning,
  not an error, so the hard rule does not block an unadopted project on day
  one; only strings the team has agreed become blocking.
- **Over-blocking on legacy projects.** Same mitigation shape as the UX hard
  rule: the rule is installed by the user's action, not silently.
- **Voice-pack overfitting.** Mitigated by the mandatory `Failure mode` field
  and the audit pass that checks for it.
- **Upstream divergence** (accepted consequence of D1) — mitigated by the
  `Source:` / `Checked:` fields, not eliminated.
- **Not a translation system.** `strings.md` is a decision registry; anything
  resembling a message catalog belongs in the project's own i18n layer.

## 18. Human steps

None on the autonomous path. The release itself may require unblocking
outward-facing commands (`git push`, `npm publish`) under the harness safety
rules; if so, that is a single request at release time, not a per-step
prompt.
