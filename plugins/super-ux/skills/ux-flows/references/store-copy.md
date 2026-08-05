# Store listings — App Store and Google Play

Field limits, indexing rules and craft for the two store surfaces. Field
values live in the project's `channels.md`; the limits below are what the
platforms enforce, and `B040` checks copy against them with the locale's
length coefficient applied.

*Platform limits checked 2026-08-05. Both stores change them; re-verify
before a listing rewrite rather than trusting this table.*

## Field limits

| Field | App Store | Google Play |
|---|---|---|
| Title | 30 | 50 |
| Subtitle | 30 | — |
| Short description | — | 80 |
| Keyword field | 100 | — |
| Promotional text | 170 | — |
| Full description | 4000 | 4000 |
| What's new | 4000 | 500 |

Two structural differences that change how each is written:

- **App Store has a hidden keyword field; Google Play indexes the
  description.** So the App Store description is written entirely for humans,
  while the Play description carries the terms as well — naturally, at the
  density prose tolerates.
- **App Store keyword changes need a submission; promotional text does not.**
  Promotional text is the only field that can be changed between releases,
  which makes it the place for anything time-bound.

## The iOS keyword field

100 characters, and most listings waste a third of them.

- **No space after commas.** `task,todo,planner` — each space is a character
  bought for nothing.
- **No plurals.** Both forms are matched from the singular; `reminders` costs
  a character for no reach.
- **Nothing already in the title or subtitle.** Those are indexed at higher
  weight; repeating them here spends the field twice.
- **No competitor brand names.** Not a style preference — it is grounds for
  rejection.
- **Singular concepts, comma-separated**, ordered by relevance. The field is
  a bag of terms, not a phrase.

These four rules are `B041`.

```
✗  task manager, todo list, productivity app, daily planner, reminder app
✓  task,todo,checklist,reminder,organize,daily,planner,schedule,deadline,goal
```

The first spends 69 characters on eight terms, several already in the title.
The second fits eleven distinct terms in 70.

## Title and subtitle

The title carries the brand plus the single strongest term. The subtitle
carries the benefit, in the user's words, with the secondary term.

```
✗  MyTasks
✗  MyTasks - The Best Task Management App For Busy Professionals
✓  MyTasks: Todo List & Planner
```

Neither field is a place for a sentence. Read them together — they appear
together everywhere in the store.

## Description

The first two or three lines are visible before "more". Almost nobody
expands. Write the opening as if it were the whole listing.

1. **Opening** — the user's problem, then what the app does about it, then
   one piece of proof. No throat-clearing, no company history.
2. **Benefits** — five short bullets, outcome-first. Not a feature dump.
3. **Proof** — rating, install count, a named award or press mention. Every
   figure traceable to `facts.md`.
4. **Close** — the next step and the reassurance that removes the hesitation
   (`no account needed`, `free to try`, `cancel anytime`).

Keyword density above the `B051` threshold reads as stuffing to the store's
own review as well as to `brand_lint.py`.

## Screenshot captions

The caption is read before the screenshot is understood, so it carries the
value, not the label.

```
✗  Task List Feature      (names the UI)
✗  Create Task Lists      (names the action)
✓  Never miss a deadline  (names the outcome)
```

First screenshot does the work of a headline; the rest tell a sequence. Five
to seven is the practical range.

## What's new

Play truncates at 500 characters, so the first line has to carry the release.
Write what changed for the user — the changelog rule from
[channel-playbooks.md](channel-playbooks.md) applies unchanged. "Bug fixes
and performance improvements" as the entire entry is a wasted surface that
users do read.

## Ratings and reviews

- The prompt goes after a success moment, never on launch and never during a
  failure. A prompt shown at the wrong moment converts a neutral user into a
  one-star.
- Respond to reviews in the product's voice, at the register of
  `settings and legal`: plain, specific, no defensiveness, no humor.
- A review naming a bug that is now fixed deserves a reply saying which
  version fixed it.

## Localization

Store listings are the surface where machine translation is most visible and
most damaging: the title and subtitle are short enough that a literal
translation reads as obviously foreign.

- Keyword research is redone per locale. Translated keywords are not
  keywords — see [localization.md](localization.md).
- Length coefficients bite hardest here, because these are the tightest
  fields in the product. A 30-character title at a 1.3 coefficient has 23
  characters of usable meaning.
- Screenshot captions are re-written, not translated.
