# Locales — one voice, several languages

A voice does not survive translation intact. Some of it is invariant, some of
it has to be decided again per language, and the difference has to be written
down or every locale quietly becomes its own brand.

## Contents

- [What travels and what does not](#what-travels-and-what-does-not)
- [Length](#length)
- [The primary locale is the source of meaning, not of form](#the-primary-locale-is-the-source-of-meaning-not-of-form)
- [Parity, declared rather than hidden](#parity-declared-rather-than-hidden)
- [Keywords are researched, never translated](#keywords-are-researched-never-translated)
- [What never translates](#what-never-translates)
- [Legal and regulatory differences](#legal-and-regulatory-differences)
- [Who decides](#who-decides)


File shape: [brand-contract.md](brand-contract.md). Locale files live at
`docs/brand/locales/<code>.md`.

## What travels and what does not

`voice.md` splits its own axes into two lists, and that split is the whole
model.

**Invariant** — the things that make the brand itself, expressed differently
but never abandoned: whether it hedges, whether it claims what it cannot
prove, whether it leads with the reader's problem, whether it names its
limits.

**Reconsidered per locale** — the things that are conventions rather than
character:

- **Address form.** German `Sie`/`du`, French `vous`/`tu`, Russian
  «вы»/«ты», Japanese politeness level. A single choice per locale, applied
  everywhere, recorded in the locale file. This one decision changes how the
  brand is perceived more than any word choice.
- **Humor.** Rarely transfers. Default to one step lower than the base and
  raise it only with evidence from someone who lives in the language.
- **Directness.** A register that reads as confident in one market reads as
  rude in another, and the reverse.
- **Idiom and wordplay.** Dead on arrival. Listed in `Dead idioms` with a
  replacement that does the same job — not a translation of the joke.

## Length

Every locale carries a `Length coefficient`. It multiplies each field limit
in `channels.md` when the linter checks that locale (`B040`, `B073`).

Rough starting values, to be replaced with measured ones as soon as real
strings exist: German 1.3, French 1.2, Spanish 1.2, Russian 1.15, Polish 1.2,
Japanese 0.6, Korean 0.7, Chinese 0.5.

The tightest surfaces break first: buttons, tab labels, store titles and
subtitles. A 30-character App Store title at 1.3 leaves 23 characters of
meaning — which is a design constraint on the English original, not a
translation problem discovered later.

## The primary locale is the source of meaning, not of form

The most common failure in localized products is a CTA translated word for
word: grammatically perfect, and nobody clicks it. `Get started` rendered
literally is often an instruction to begin an unspecified activity.

So the rule: translate the **job** the string does, then write the string
that does that job in the target language. `B072` flags strings that look
like literal renderings of the primary CTA.

Same for headlines, taglines and store captions. Same for anything short —
the shorter the string, the more its impact depends on idiom, and the worse
literal translation performs.

## Parity, declared rather than hidden

A locale does not have to be complete. It has to be honest about not being
complete.

`voice.md` sets `Locale parity threshold`. The linter computes coverage per
locale and warns below it (`B071`) with the percentage and the count of
lagging strings. A partial locale that declares itself is a known state; one
that does not is a surprise waiting for a user who does not speak the
fallback.

Fallback behaviour is a product decision that belongs in scenarios, not here
— but the copy layer's rule is that a fallback is visible, never silent.

## Keywords are researched, never translated

Search and store terms come from what people in that market actually type.
The translation of a high-volume English keyword is routinely a term with no
volume, while the term people do use is a different word entirely.

Each locale file records its own keyword list. This is also why a locale can
have a genuinely different page structure: if the market's questions differ,
the headings differ.

## What never translates

Recorded in `Never translated`: the product name, entity names, tier names,
and any term the dictionary in `terminology.md` marks as ours. A tier called
`Pro` stays `Pro` in every locale — translating tier names breaks support,
billing conversations and every screenshot ever taken.

## Legal and regulatory differences

Some locales require copy that others do not: an Impressum in Germany, VAT
inclusive pricing in the EU, specific consent wording, cooling-off periods.
These are recorded per locale as `Legal differences` and treated as required
strings, not optional ones — a missing legally required string is a defect
even when parity is otherwise complete.

## Who decides

A locale file is written with someone who lives in the language. Machine
translation drafts it; a person who reads that language every day decides
the address form, the humor level and the idiom replacements. Where nobody
is available, the honest move is to say the locale is unreviewed in the file
itself rather than to ship a confident guess.
