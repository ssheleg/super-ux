# Research evidence — the ledger that keeps provenance

**Load this when:** synthesizing user research into the foundation (personas,
JTBD, journeys), importing interview / survey / analytics findings, or writing
any number into a UX document. Synthesis without this contract produces the
failure it exists to prevent: a confident foundation nobody can trace back to a
person who said it.

## Contents

- [The four classes](#the-four-classes)
- [The row](#the-row)
- [Contradictions are findings](#contradictions-are-findings)
- [A number travels with its anchors](#a-number-travels-with-its-anchors)
- [Single source is a flag, not a fact](#single-source-is-a-flag-not-a-fact)
- [No data stays a hypothesis](#no-data-stays-a-hypothesis)
- [Promotion is append-only](#promotion-is-append-only)

## The four classes

Every ledger entry carries exactly one `class`, and the classes never blend:

| class | what it is | what its `source` must name |
|---|---|---|
| `observation` | something that happened, seen first-hand | who and when: `P07, interview 2026-08-14` |
| `citation` | an external source's claim | the address and the date read: `https://… (read 2026-08-14)` |
| `inference` | a conclusion derived from other entries | the entries it derives from: `derived-from: RE-0001, RE-0004` |
| `hypothesis` | a belief nothing yet supports | what would confirm it: `confirm-by: …` |

The blend is the defect. "Users hate the paywall" written as an observation when
one participant sighed at it is an inference wearing an observation's authority;
a citation restated without its address is a rumour; an inference whose inputs
are not named cannot be re-derived when one input falls.

## The row

The machine-checkable shape, one entry per row, ids `RE-NNNN`:

```
- id: RE-0007
  class: observation
  statement: "P07 abandoned checkout at the currency step"
  source: P07, moderated session 2026-08-14
  contradicts: RE-0004        # optional — and RE-0004 stays in the ledger
  single-source: true         # required on any inference resting on one input
  number: 12% | unit: of sessions | entity: checkout currency step |
          population: DE cohort, n=41 | date: 2026-08
```

`number` and its four anchors (`unit`, `entity`, `population`, `date`) appear
**together or not at all** — see below. Fields the class does not require are
omitted, never left empty.

## Contradictions are findings

Two participants disagreeing is a segmentation signal, not noise. When entries
conflict:

- **both stay in the ledger** — deleting or averaging destroys the one thing
  the disagreement was telling you;
- each names the other in `contradicts:`, so a reader arriving at either one
  is pointed at the tension rather than shielded from it;
- the synthesis that uses one of them says why it chose, in an `inference`
  row that `derived-from:`s both.

## A number travels with its anchors

A bare number is not evidence. "Conversion is 12%" answers nothing until it
says **12% of what** (`unit`), **where** (`entity` — which funnel, which step),
**for whom** (`population` — cohort and n), and **when** (`date`). A ledger row
carrying `number` without all four anchors is invalid — the row is rejected,
not padded. A number quoted from outside carries them from its source or drops
to `hypothesis` until they are found.

## Single source is a flag, not a fact

An `inference` resting on one participant or one citation carries
`single-source: true`, visibly. It may inform a draft; it may not be promoted
into a foundation document (persona trait, JTBD force, journey stage) until a
second **independent** entry supports it — independent meaning a different
participant or a different publisher, not the same interview quoted twice.

## No data stays a hypothesis

There is **no quota of evidence**. A synthesis that "needs" support it does not
have writes the `hypothesis` row, names `confirm-by:` (the observation or
citation that would settle it), and moves on. Inventing an `observation` to
fill a gap — or citing a source that says something adjacent — is the one
corruption this ledger cannot recover from, because every later inference
inherits it.

## Promotion is append-only

A `hypothesis` becomes supported by **adding** the observation or citation rows
that support it and an `inference` that names them — never by editing the
hypothesis row's `class` in place. The ledger's history is how a reviewer
audits the synthesis; a class rewritten in place erases the fact that the team
once believed something without evidence, which is exactly the fact worth
keeping.
