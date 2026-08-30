# Brand Contract (v1): Voice, Terminology, Facts, Channels, Strings, Locales

This is THE contract for `docs/brand/` in a target project. The `brand-voice`
and `copywriting` skills, the `copy` scope of `ux-audit`, `brand_lint.py` and
the Cursor rules all follow it. Do not deviate from file names, field names,
statuses or surface names, because tooling keys off them. The reasoning behind the
model lives in [surface-registers.md](surface-registers.md); the pack library
it selects from is [voice-packs.md](voice-packs.md).

## Contents

- [Files in the target project](#files-in-the-target-project)
- [The marker](#the-marker)
- [Where the voice comes from](#where-the-voice-comes-from)
- [`voice.md`](#voicemd)
- [`terminology.md`](#terminologymd)
- [`facts.md`](#factsmd)
- [`channels.md`](#channelsmd)
- [`strings.md`](#stringsmd)
- [`locales/<code>.md`](#localescodemd)
- [`README.md` and the `Sources:` block](#readmemd-and-the-sources-block)
- [The three rules that hold the layer together](#the-three-rules-that-hold-the-layer-together)
- [The check codes](#the-check-codes)
- [Versioning](#versioning)


`docs/ux/` answers **what the product does**. `docs/brand/` answers **how it
speaks**. They are separate roots on purpose: the brand pack also governs
surfaces that are not UX at all: a blog post, a store listing, an ad.

## Files in the target project

```
docs/brand/
├── voice.md              # identity: pack, axes, narrative, locale transfer
├── terminology.md        # our words, banned words, entity and tier names
├── facts.md              # canonical numbers and proof, the only source
├── channels.md           # one record per surface: register, limits, bans
├── strings.md            # interface string registry -> file:line -> scenario
├── locales/
│   └── <code>.md         # per-locale delta (en.md, ru.md, de.md, …)
├── README.md             # this map, project-side, plus the Sources: block
└── lint.py               # the brand linter, seeded by the installer
```

## The marker

The **first line** of every file under `docs/brand/`, including
`locales/<code>.md`, is exactly:

```
Contract: brand-contract v1
```

`brand_lint.py` reports a missing marker as `B001` and disagreeing markers
across files as `B002`. `ux_doctor.py` reads the same line to tell a base
written to an old contract from one written to the current one. A base three
versions behind is internally consistent, which is precisely why a linter
cannot see it.

## Where the voice comes from

The pack is **derived from** `docs/ux/foundation.md`: personas, jobs, and
what the user stands to lose when the product fails. The dependency runs one
way. A persona does not change because a tone was appealing.

`voice.md` records the trace in `Derived-from:`. When no foundation exists,
`brand-voice` still works, stamps `Derived-from: inferred`, and says plainly
that the WHY layer should be built.

---

## `voice.md`

```markdown
Contract: brand-contract v1
Voice pack: operator-brief
Locales: en (primary), ru, de
Locale parity threshold: 80%
Derived-from: P-01, P-03, JTBD-02
Status: validated
Humanization: on
Humanization pass: own
Last calibrated: 2026-08-05

## Axes

| Axis | The product IS | The product IS NOT |
|---|---|---|
| Confidence | states its position | "we think this could help" |
| Register | terse, operational | corporate marketing speak |
| Distance | peer to peer | vendor to account |
| Humor | dry, rare, earned | quirky, emoji-led |
| Density | every sentence carries weight | filler, throat-clearing |

## Narrative

Hero: the operator who owns the outcome
Enemy: guesswork that costs money before anyone notices
Product role: instrument
Promise: you stop guessing within one run

## Invariant in every language

- never hedges
- never claims a number that is not in facts.md

## Reconsidered per locale

- address form
- humor level
- idioms and wordplay
```

**Header fields.** `Voice pack` is a pack id from
[voice-packs.md](voice-packs.md) or `custom`. `Locales` lists every locale,
marking exactly one `(primary)`. `Locale parity threshold` is the percentage
below which `B071` warns. `Derived-from` lists `P-` / `JTBD-` ids from
`foundation.md`, or the single word `inferred`. `Last calibrated` is an ISO date.

**A header value ends where an aligned comment begins.** Two spaces or more
before a `#` starts a comment and the value stops there, which is how the
seeded templates annotate a field. One space does not, because a reason may
legitimately read `per ticket #431` and truncating it would leave no reason
at all.

**`Humanization` and `Humanization pass` answer two different questions**, and
conflating them is why the second one existed for releases while nothing read
it. `Humanization` is **whether the pass runs at all**; `Humanization pass`
names **which implementation** runs, and absent it is `own`, the only one that
reads this pack's registers and canonical facts.

`Humanization` defaults to `on`, and it is a default rather than a preference:
every mode that produces text runs the sweep, because a draft nobody swept
carries the markers `ai-tells.md` grades and a reader registers them before
they can say why. An absent field is `B064` at warning level, since the default
is the safe state. `off` is legitimate and it is a decision that outlives the
person who made it, so it requires a `Humanization declined:` line carrying the
reason and the date; without one it is `B064` at error level. The value is
what every status this pack prints reports, so a project can always see which
state it is in without reading a file.

**The `Status` enum, in one home:**

- `voice.md` **Status** — `draft | validated`
- `voice.md` **Humanization** — `on | off`

`validate_status_enums_match_contract` reads that line and compares it against
`VOICE_STATUSES` in `brand_lint.py`, so neither side can move alone. It is here
because the two had already disagreed and it worked by accident: this pack's own
`voice.md` said `Status: approved` for two releases, and every read in the linter
asked `== "draft"` or `!= "draft"` — so `approved` behaved like `validated` and
would have read as **not** validated the first time any check tested for the
value. An out-of-enum status is `B034`.

**Status lifecycle.** Same as a scenario: `draft` until the operator has seen
and approved it, then `validated`. `approved` is not a third state; it is what
the operator does, and `validated` is what the file then says. Any edit drops it
back to `draft`.

**The five axes are fixed**: `Confidence`, `Register`, `Distance`, `Humor`,
`Density`. A pack fills them; a project may sharpen the wording but may not
add or remove an axis, because `channels.md` expresses register as deltas
against exactly these five.

---

## `terminology.md`

```markdown
Contract: brand-contract v1

## Product terms: always

| Our term | Never write | Applies to |
|---|---|---|
| Run | Execution, Job | what the product performs |

## Entity and tier names: exact spelling

| Name | Wrong forms seen |
|---|---|
| Pro | PRO, Pro plan, pro |

## Banned

| Word or phrase | Why | Use instead |
|---|---|---|
| leverage | filler verb | use |
| seamless | claims what it cannot show | describe the step that disappeared |

## Glossary

| Term | Meaning |
|---|---|
```

The **Banned** table seeds from three places at init: weak verbs and
buzzwords, hedging chains, and the marker vocabulary in
[ai-tells.md](ai-tells.md). Calibration adds what is specific to the product.

`brand_lint.py` reads the first column of **Product terms** and **Banned**
for `B010` and `B011`, and the **Entity and tier names** table for `B012`.

---

## `facts.md`

```markdown
Contract: brand-contract v1

| Fact | Value | Source | Checked | Review by | Public |
|---|---|---|---|---|---|
| tools in the catalog | 448 | api/catalog.json | 2026-08-05 | 2026-11-05 | yes |
| median run cost | $3.10 | internal billing export | 2026-07-30 | 2026-10-30 | no |
```

**This is the only source of any figure in public copy.** A number in a
public surface with no row here is `B030` and blocks. `Public: no` marks
internal figures that must never be quoted. A row with no `Source`, or past
its `Review by`, is `B031` and warns.

A missing fact is reported, never invented to close a gap.

---

## `channels.md`

One record per surface, in this shape:

```markdown
### landing hero

Register:   confidence +1, density +1, humor -1
Format:     one headline under 60 characters, one subhead, one CTA
Limits:     title 60, meta description 160
Forbidden:  physics: none | brand: superlatives without a facts.md row
CTA:        one primary, verb plus outcome
Proof:      one number, sourced
Locales:    de headline budget 60 * 1.30
```

**Register** is expressed as deltas against the five axes in `voice.md`.
**Forbidden** always carries both halves, `physics:` and `brand:`, even when
one is `none`; see the second rule below.

### Surfaces

Product: `primary action` · `empty state` · `error` · `loading` ·
`success/toast` · `onboarding` · `paywall and upgrade` ·
`destructive confirm` · `billing and receipts` · `settings and legal` ·
`transactional email and push` · `docs and help`.

Marketing: `landing hero` · `landing body` · `pricing` · `blog` ·
`changelog` · `X` · `Reddit` · `LinkedIn` · `HN and Product Hunt` ·
`App Store` · `Google Play` · `ads` · `lifecycle email`.

A project may omit a surface it does not have. It may not rename one: the
linter and the audit both address surfaces by these names.

---

## `strings.md`

```markdown
Contract: brand-contract v1

| Key | Text (primary) | Location | Scenario | Status |
|---|---|---|---|---|
| action.project.publish | Publish | src/ui/ProjectBar.tsx:47 | SCN-014 | agreed |
```

Statuses: `agreed` · `proposed` · `drifted` · `orphan`.

**This is a decision registry, not a message catalog.** It does not replace
i18n keys and holds no translations. It records which strings have been
reconciled with the pack, which scenario each serves, and where it lives.
It is what makes `B020`, one action under two names, checkable at all; without
it that defect is only findable by reading the whole interface.

`Key` is dot-separated and stable. Two rows sharing a `Key` with different
`Text` is `B020`. A `Location` that no longer resolves is `B023`.

The registry is populated by an inventory sweep at init, not by hand.

---

## `locales/<code>.md`

```markdown
Contract: brand-contract v1
Locale: de
Primary: no
Address form: Sie
Length coefficient: 1.30
Humor: -1 from base
Never translated: product name, entity names, tier names
Keywords: own research, not translated from primary
Dead idioms: "ship it" -> "raus damit"
Legal differences: Impressum, VAT-inclusive pricing
```

`Length coefficient` multiplies every field limit in `channels.md` when the
linter checks that locale (`B040`, `B073`).

Two rules:

1. **The primary locale is the source of meaning, not of form.** A
   word-for-word CTA translation is a finding (`B072`) even when the grammar
   is perfect.
2. **A locale need not be complete, but must declare that it lags.** Parity
   below `Locale parity threshold` warns (`B071`) with the percentage, rather
   than letting an unfinished locale look finished.

---

## `README.md` and the `Sources:` block

The project-side map, and the one thing the linter cannot infer: where this
project keeps its text.

```markdown
Contract: brand-contract v1

Sources:
  ui:        src/**/*.{ts,tsx,js,jsx,vue,svelte}
  marketing: content/**/*.{md,mdx}
  store:     store/{ios,android}/*.md
  robots:    public/robots.txt
  locales:   src/locales/*.json
```

Nothing outside these paths is scanned. A missing block is `B006` and blocks:
the linter refuses to report a clean run over a surface it never read. Any
subset may be declared; checks whose source is absent are counted as skipped
in the summary, never silently passed.

`ui` and `marketing` also classify a finding, because several checks apply to only
one of the two.

---

## The three rules that hold the layer together

1. **Register moves the axes; it never crosses the invariants.** A Reddit
   post may run long, drop the CTA and turn self-deprecating. If the brand
   does not hedge, it does not hedge there either. The invariants are listed
   in `voice.md`; everything else is negotiable per surface.

2. **Platform physics and brand choice are separate fields.** "A link in the
   post body suppresses reach" and "we do not post links" are different
   claims. Merged into one line, nobody can tell six months later which was
   an algorithm and which was a decision, so `Forbidden:` always carries
   both halves.

3. **Humor is forbidden on `error`, `destructive confirm`,
   `billing and receipts` and `paywall and upgrade`**, in every pack,
   including `playful-consumer`. The user is losing data, access or money at
   that moment; a joke reads as mockery. Enforced as `B061`, not left to
   taste.

---

## The check codes

`brand_lint.py` emits these and nothing else. The contract owns the meanings;
the linter owns the detection. A code the linter can emit that is absent here
is a validator failure, because its meaning would otherwise live only in the
source of the thing doing the checking.

Severity is fixed per code: **E** blocks, **W** reports.

| Code | | Fires when |
|---|---|---|
| B001 | E | a file under `docs/brand/` has no contract marker |
| B002 | E | markers disagree across the pack |
| B003 | W | `voice.md` is `draft` while `strings.md` holds agreed rows |
| B004 | E | `Derived-from` cites an id absent from `foundation.md` |
| B005 | W | `foundation.md` changed after `Last calibrated` |
| B006 | E | `README.md` has no `Sources:` block, so nothing to scan |
| B007 | W | `## Voice references` names no admired or no refused brand, once the voice leaves `draft` |
| B010 | E | a banned word appears in a registered string |
| B011 | E | a generic word used where a product term exists |
| B012 | E | an entity or tier name spelled inconsistently |
| B020 | E | one action carries two different names |
| B021 | E | a registered string diverged from the code |
| B022 | W | a code string has no registry row |
| B023 | E | a registry row points at a location that does not exist |
| B024 | E | declared casing violated |
| B025 | W | a button label names no outcome |
| B026 | W | a label, button, menu item or title ends in a full stop |
| B030 | E | a figure in public copy has no row in `facts.md` |
| B031 | W | a fact has no source, or is past its `Review by` |
| B032 | E | a superlative with no fact beside it |
| B033 | E | two rows in `facts.md` under one `Fact` name — a figure cited by that name is ambiguous, and the duplicate also widened the sourced set |
| B034 | E | `voice.md` carries a `Status` the contract does not declare — every read here asks whether it is `draft`, so an unrecognised value behaves like `validated` today and reads as not-validated the moment a check tests for the value |
| B040 | E | a field exceeds its surface limit |
| B041 | E | an iOS keyword-field rule broken |
| B042 | E | a link in a body where the surface's physics forbid it |
| B043 | W | more hashtags than the surface tolerates |
| B050 | E | AI search declared a target while a crawler is blocked |
| B051 | E | a token exceeds 1% of a marketing document |
| B052 | E | a filler opener |
| B053 | W | no named author where the surface needs one |
| B054 | W | the title promises more than the body delivers |
| B060 | W/E | machine-drafting markers; error at three S1 |
| B061 | E | humor where the user is losing something |
| B062 | E | AT-06, a rhetorical dash standing in for a full stop, comma or colon |
| B063 | W | AT-07, a document title or heading ends in a full stop |
| B064 | W/E | the humanization pass: absent field warns that the default `on` applies unrecorded; an out-of-enum value errors; `off` with no `Humanization declined:` reason errors |
| B070 | E | a declared locale has no locale file |
| B071 | W | locale parity below the declared threshold |
| B072 | W | a locale row left identical to the primary |
| B073 | E | a field overflows under the locale's coefficient |

---

## Versioning

The version in the marker moves when a field is renamed or removed, or when a
new required field appears. Adding an **optional** field does not move it,
the same rule the UX contract follows. `ux_doctor.py` reports what each
version introduced, so a project can see what it is missing without reading
the diff.
