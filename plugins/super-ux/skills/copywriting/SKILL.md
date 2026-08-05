---
name: copywriting
description: Use when writing, rewriting or editing any text a user will read — interface strings, buttons, errors, empty states, landing and pricing pages, blog posts, changelogs, social posts, app store listings, ads, lifecycle email. Triggers - "write copy" / "напиши текст", "rewrite this" / "перепиши", "headline" / "заголовок", "CTA" / "кнопка", "post for X" / "пост для твиттера", "store listing" / "описание в сторе", "this sounds like AI" / "звучит как нейросеть", "microcopy" / "микрокопия". For defining the voice itself, see brand-voice.
license: MIT
---

# copywriting — write it in the product's own voice

> Part of **super-ux** — see [system-map.md](references/system-map.md).
> After changes, run `python3 docs/brand/lint.py`.

**First action, every time: read the brand pack.** `docs/brand/voice.md`,
`terminology.md`, and the `channels.md` record for the surface being written.

**No pack? Stop and hand off to `brand-voice`.** Do not improvise a voice.
Guessing it and being wrong costs more than the pause, and a product whose
copy was invented surface by surface is exactly the drift this layer exists
to remove.

**This skill never writes to `docs/brand/`.** A term that is missing from the
dictionary, or a number with no row in `facts.md`, is **reported** — never
invented to finish the sentence. Adding it is `brand-voice`'s decision.

## References

| Read | When |
|---|---|
| [ui-copy.md](references/ui-copy.md) | any string inside the product |
| [marketing-copy.md](references/marketing-copy.md) | pages, long form, the seven sweeps, grounding |
| [channel-playbooks.md](references/channel-playbooks.md) | a social, blog, changelog, ads or email surface |
| [store-copy.md](references/store-copy.md) | App Store or Google Play |
| [seo-aeo-safety.md](references/seo-aeo-safety.md) | anything a crawler or answer engine reads |
| [ai-tells.md](references/ai-tells.md) | Humanize mode, or a draft that reads machine-made |
| [localization.md](references/localization.md) | any locale that is not primary |
| [surface-registers.md](references/surface-registers.md) | the register for a surface |

## Modes

### Write

1. Name the surface. It must exist in `channels.md`; if it does not, that is
   a `brand-voice` decision, not an improvisation here.
2. Apply the register: the axes from `voice.md`, plus that surface's deltas.
   **Deltas move axes; they never cross the invariants.**
3. Write. Every claim traces to `facts.md`. Every product term comes from
   `terminology.md`.
4. Deliver the copy first, then the reasoning. For headlines and CTAs give
   two or three options with what each trades away.
5. For interface strings, add or update the `strings.md` row — key,
   `file:line`, scenario, `Status: proposed`.

### Edit

The seven sweeps from `marketing-copy.md`, in order, looping back after each:
clarity, voice and tone, so-what, prove-it, specificity, emotion, zero risk.
Deliver sweep by sweep, prioritised by impact, not by reading order.

### Adapt

One piece across several surfaces. Re-write per surface — never paste one
register into another. What survives adaptation is the claim and the proof;
what changes is length, structure, CTA policy and register.

State plainly what each version drops. A thread is not a page with line
breaks.

### Humanize

Under the guards in `ai-tells.md`, which are not optional:

- Above ~10 markers per 500 words, say so and rewrite from the argument — a
  patch produces the same patterns with better words.
- **Above a 50% change rate, do not ship.** Report the rate and ask. That is
  no longer an edit.
- Run the semantic-preservation checklist before output: numbers, dates and
  proper nouns intact; causal direction unchanged; no negation inverted;
  quotations untouched; the core claim the same.
- Text that already reads naturally is left alone. Editing what is fine to
  prove the pass ran is this mode's failure.

## Non-negotiables

- **No fabricated facts, statistics, quotes or experts.** Not for a deadline,
  not for a benchmark, not because a placeholder would look better. Refuse,
  say why, offer to find a real one.
- **No humor on `error`, `destructive confirm`, `billing and receipts` or
  `paywall and upgrade`** — in any pack. The user is losing something there.
- **One action, one name.** Before naming an action, search `strings.md` for
  it. A second name for an existing action is a defect, not a synonym.
- **Never quote a number that is not in `facts.md`.**

## Definition of done

- Every string or section traces to a surface record and a voice.
- New interface strings are in `strings.md` with location and scenario.
- `python3 docs/brand/lint.py` exits 0 for the touched surfaces.
- Anything reported as missing — a term, a fact, a surface — is named
  explicitly, not worked around.
