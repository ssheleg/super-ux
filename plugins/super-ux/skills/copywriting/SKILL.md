---
name: copywriting
description: Use when writing, rewriting or editing any text a user will read — interface strings, buttons, errors, empty states, landing and pricing pages, blog posts, changelogs, social posts, app store listings, ads, lifecycle email. Triggers - "write copy" / "напиши текст", "rewrite this" / "перепиши", "headline" / "заголовок", "CTA" / "кнопка", "post for X" / "пост для твиттера", "store listing" / "описание в сторе", "this sounds like AI" / "звучит как нейросеть", "microcopy" / "микрокопия", "build a landing page" / "сделай лендинг" (the copy for it; the visual layer is sheleg-design's). For defining the voice itself, see brand-voice.
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
| [landing-pages.md](references/landing-pages.md) | assembling a landing page: the offer, awareness, proof, the action |
| [channel-playbooks.md](references/channel-playbooks.md) | a social, blog, changelog, ads or email surface |
| [store-copy.md](references/store-copy.md) | App Store or Google Play |
| [seo-aeo-safety.md](references/seo-aeo-safety.md) | anything a crawler or answer engine reads |
| [ai-tells.md](references/ai-tells.md) | every mode that produces text: the pass runs by default |
| [localization.md](references/localization.md) | any locale that is not primary |
| [surface-registers.md](references/surface-registers.md) | the register for a surface |

## Modes

**The humanization pass runs by default, in every mode that produces text.**
It is not a mode you enter, it is the last step of Write, Edit and Adapt, under
the guards in [ai-tells.md](references/ai-tells.md) which are not optional. The
reason it is a default rather than an option: a draft nobody swept carries the
markers that file grades, and a reader registers them before they can name why.

`voice.md` records the state in two fields that answer different questions.
**`Humanization: on | off`** is whether the pass runs, and it defaults to `on`
when the field is absent. **`Humanization pass:`** names which implementation
runs, and absent it is `own`, the only one that reads this pack's registers and
canonical facts. Turning it off is a legitimate decision that outlives whoever
made it, so `off` carries a `Humanization declined:` line with the reason and
the date. `B064` checks all three states.

**Every delivery of copy states what happened**, in one line, before the copy
or immediately after it:

```
Humanization: on — own pass, 7 markers at 2 densities, 4 addressed, 11% changed
Humanization: off — declined 2026-08-30, wording fixed by counsel
```

The line is not decoration. A pass that runs invisibly is indistinguishable
from one that did not run, and the reader of the copy is usually not the person
who chose the setting.

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
6. **Run the humanization pass** under the Humanize guards below, then print
   the status line. On new text the change rate is measured against the draft
   you just wrote, so the 50% ceiling does not apply the way it does to an
   edit; report the rate regardless.

### Edit

The seven sweeps from `marketing-copy.md`, in order, looping back after each:
clarity, voice and tone, so-what, prove-it, specificity, emotion, zero risk.
Deliver sweep by sweep, prioritised by impact, not by reading order.

**The humanization pass runs last**, after the seven, and then the status line.
Last because the sweeps rewrite whole sentences and a humanization pass run
before them is measured against text that no longer exists; and because the
semantic-preservation checklist is cheapest to apply to a version nobody is
about to rewrite again.

### Adapt

One piece across several surfaces. Re-write per surface — never paste one
register into another. What survives adaptation is the claim and the proof;
what changes is length, structure, CTA policy and register.

State plainly what each version drops. A thread is not a page with line
breaks.

**The pass runs per surface, not once on the source.** Each version is
different text in a different register, and a marker density that is fine in a
blog post is not fine in a landing hero. One status line per surface.

### Humanize

The standalone mode, for auditing text that already exists without writing any:
an inherited page, a competitor's copy, a draft somebody else wrote. The same
guards govern the pass wherever it runs, and they are not optional:

- Above ~10 markers per 500 words, say so and rewrite from the argument — a
  patch produces the same patterns with better words.
- **Above a 50% change rate, do not ship.** Report the rate and ask. That is
  no longer an edit.
- Run the semantic-preservation checklist before output: numbers, dates and
  proper nouns intact; causal direction unchanged; no negation inverted;
  quotations untouched; the core claim the same.
- Text that already reads naturally is left alone. Editing what is fine to
  prove the pass ran is this mode's failure.
- **A marker count is not a verdict and never gates anything.** Say which markers
  are present at what density; never say a text was AI-written. The false
  positives fall hardest on people writing in a second language, and a writer is
  not a defect to be edited into fluency they did not ask for. `ai-tells.md`
  carries the measurement and what it binds.
- **Read `voice.md`'s two fields first.** `Humanization:` is whether the pass
  runs and defaults to `on`; `Humanization pass:` names which implementation,
  and absent it is `own`. Neither absence stops work: run the default, print the
  status line saying it was a default, and offer to record it once. A value naming
  a tool that is not installed falls back to `own` and says so — a missing optional
  tool must not stop copy being written.
- Other implementations exist and two are worth knowing —
  `npx sshlg-skills humanizers` lists what this machine has. Reach for one for an
  audit with no rewrite, for long-form prose, or when the writer has a sample of
  their own writing to match. Stay here for product copy: the brand pack's
  registers and canonical facts are the constraint, and a general-purpose
  humanizer does not read them.

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
- The humanization status line is printed, whichever state it reports.
- New interface strings are in `strings.md` with location and scenario.
- `python3 docs/brand/lint.py` exits 0 for the touched surfaces.
- Anything reported as missing — a term, a fact, a surface — is named
  explicitly, not worked around.
