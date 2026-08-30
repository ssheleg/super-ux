Contract: brand-contract v1
Locale: <de>
Primary: <no>
Address form: <Sie>
Length coefficient: <1.30>
Humor: <-1 from base>
Never translated: <product name, entity names, tier names>
Keywords: <own research — see below>
Reviewed by: <name of someone who reads this language daily, or `unreviewed`>

# Locale delta

Copy this file to `locales/<code>.md`, one per declared locale. The invariant
half of the voice does not appear here — it is in `voice.md` and holds in
every language. This file carries only what is decided again.

## Address form

<The single choice, applied everywhere. This decision changes how the brand
is perceived more than any word choice, so it is made once and recorded, not
per string.>

## Dead idioms

Idiom and wordplay from the primary locale that does not survive. The
replacement does the same **job**; it is not a translation of the joke.

| Primary | Replacement | Job it does |
|---|---|---|
| <"ship it"> | <"raus damit"> | <permission to stop polishing> |

## Keywords

Researched in this market, never translated from the primary. The
translation of a high-volume English term is routinely a term with no volume,
while the term people actually type is a different word.

| Term | Volume | Where it is used |
|---|---|---|
| <…> | <…> | <…> |

## Legal differences

Required copy this locale has and others do not. Treated as required strings:
a missing one is a defect even when parity is otherwise complete.

| Requirement | Text or reference |
|---|---|
| <Impressum> | <…> |
| <VAT-inclusive pricing> | <…> |

## Length notes

Surfaces where the coefficient bites hardest in this locale — usually
buttons, tab labels, store title and subtitle. Recorded here so the
constraint reaches the primary-locale original, where it can still be
designed around.

| Surface | Primary limit | Effective limit | Note |
|---|---|---|---|
| <App Store title> | <30> | <23> | <…> |

## Parity

Computed by the linter against `strings.md`; not maintained by hand. Below
the threshold in `voice.md` it warns (`B071`) with the percentage. A partial
locale that declares itself is a known state; one that does not is a surprise
for a user who does not speak the fallback.
