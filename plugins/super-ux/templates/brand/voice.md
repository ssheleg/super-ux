Contract: brand-contract v1
Voice pack: <pack id from voice-packs.md, or `custom`>
Locales: <en (primary)>
Locale parity threshold: 80%
Derived-from: <P-NN, JTBD-NN from docs/ux/foundation.md — or `inferred`>
Status: draft
Last calibrated: <YYYY-MM-DD>
Humanization: on                    # on | off; on is the default, off needs a reason below
Humanization pass: <own | humanizer | avoid-ai-writing>   # optional; absent = own

# Voice

The pack was the starting position. This file is the truth.

## Axes

The five axes are fixed. A project sharpens the wording; it does not add or
remove an axis, because `channels.md` expresses every register as a delta
against exactly these five.

| Axis | The product IS | The product IS NOT |
|---|---|---|
| Confidence | <…> | <…> |
| Register | <…> | <…> |
| Distance | <…> | <…> |
| Humor | <…> | <…> |
| Density | <…> | <…> |

## Narrative

```
Hero:         <who the reader is, in the role this product meets them in>
Enemy:        <the state of the world that costs them — not a competitor>
Product role: <instrument | guide | weapon>
Promise:      <one line, checkable against a row in facts.md>
```

## Invariant in every language

What survives translation. Breaking one of these is a finding on any surface,
in any locale.

- <e.g. never hedges>
- <e.g. never claims a number that is not in facts.md>

## Reconsidered per locale

Conventions rather than character. Each is decided again in
`locales/<code>.md`.

- address form
- humor level
- idiom and wordplay
- <…>

## Failure mode

Copied from the pack, kept here so the audit can look for it by name.

<the degenerate form this voice collapses into when overdone>

## Voice references

<!-- Two fixed points. The refused one does most of the work: it is the only
half that can be checked against a draft out loud ("this is the thing we said
we would never sound like"). Required once Status leaves `draft`. -->
- **Admired:** <brand or product, and the ONE thing it does that you want>
- **Refused:** <brand or product, and the ONE thing it does that you refuse>
