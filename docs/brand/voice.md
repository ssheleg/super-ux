Contract: brand-contract v1
Voice pack: peer-builder
Locales: en (primary)
Locale parity threshold: 80%
Derived-from: P-01, P-02, JTBD-01, JTBD-02, JTBD-03
Status: validated
Last calibrated: 2026-08-20

# Voice

The pack was the starting position. This file is the truth.

`peer-builder` was chosen because every buyer of this product reads the
source before the README — it ships as text files in their repository, and
the first thing a sceptical user does is open `ux_lint.py`. The runner-up was
`calm-expert`: it would have suited the audit reports, and it loses because
its caution reads as hedging to someone deciding whether a linter is worth
wiring into CI. What the user loses when this product fails is *time and
trust in their own approved decisions* — high stakes, no room for charm.

## Axes

The five axes are fixed. A project sharpens the wording; it does not add or
remove an axis, because `channels.md` expresses every register as a delta
against exactly these five.

| Axis | The product IS | The product IS NOT |
|---|---|---|
| Confidence | specific and falsifiable — every claim has a file, a command or an id behind it | confident about things it has not checked |
| Register | technical and unadorned; the vocabulary of a design review | marketing prose about design |
| Distance | equals who have both watched an agent rewrite an approved screen | a methodology lecturing a practitioner |
| Humor | dry, structural, arising from the situation being absurd | jokes, exclamation marks, or personality applied to an error |
| Density | high, every term grounded on first use | jargon assumed, or a layer named without saying what it holds |

## Narrative

```
Hero:         the builder whose agent keeps rewriting what they already approved
Enemy:        intent that evaporates between prompts, so every session re-decides
Product role: instrument
Promise:      the interface is decided before it is written, and stays decided
```

## Invariant in every language

What survives translation. Breaking one of these is a finding on any surface,
in any locale.

- Never claims a number that has no row in `facts.md`.
- Never states a defect without the `file:line` that proves it.
- Never says a check passed when it was not run.
- Never presents a companion (sheleg-design, task-pipeline) as required.
- Never uses levity where the user can lose work — errors, overwrite
  warnings, anything touching an existing scenario base.
- Names the limit in the same breath as the capability, not in a FAQ.

## Reconsidered per locale

Conventions rather than character. Each is decided again in
`locales/<code>.md`.

- address form
- humor level
- idiom and wordplay
- the length coefficient for CLI output, which must not wrap at 80 columns

## Failure mode

Copied from the pack, kept here so the audit can look for it by name.

Insider shorthand: the in-group signals compound until a newcomer cannot
enter, and the tell is a page that assumes the reader already knows what
"the chain" or "the contract" is. Second form: honesty performed rather than
practised — limits listed for credit while the real one stays buried. For
this product the second form has a specific shape: publishing a linter's
check count as a badge while the count is stale.

## Voice references

Two fixed points, and the refused one does most of the work: it is the only
half that can be checked against a draft out loud.

- **Admired:** Stripe's API documentation — every claim arrives with something
  you can run, so trust is earned by the reader rather than asserted by the
  writer.
- **Refused:** the launch-post register that opens with "We're thrilled to
  announce" — a tone that treats the reader's attention as already won, and
  puts the writer's excitement where the reader's problem should be.
