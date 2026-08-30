---
description: Single entry point for the verbal identity — status across voice, terminology, facts, channels, strings and locales, then a menu of applicable actions (init, calibrate, update, validate, write, audit)
---

Single entry point for the brand layer. The user is NOT expected to know the
files, fields or codes inside `docs/brand/` — routing is your job. Idempotent:
safe to run at any stage, any number of times.

## 0. Understand the task

If `$ARGUMENTS` states it, route and skip the question. Otherwise ask ONE
plain question — "What do you need the product's text to do?" — with examples
in everyday words (a new landing page, a post, the interface sounds
inconsistent, we need a tone of voice, check everything).

Never ask the user to choose between skills or files.

| User says (any language) | Route to |
|---|---|
| "we have no tone of voice", "define how we sound" / "нужен тон оф войс" | 1 (Init) |
| "write X", "post for X", "landing copy" / "напиши текст", "пост" | 5 (Write) |
| "the copy is inconsistent" / "текстовка везде разная" | 4 then 6 |
| "check everything" / "проверь всё" | 4 (lint) then 6 (audit) |
| "we changed pricing / renamed a tier" / "переименовали тариф" | 3 (Update) |
| "this sounds like AI" / "звучит как нейросеть" | 5, Humanize mode |
| "don't know" / "просто посмотри" | run 1–3 of Inspect, recommend from state |

## 1. Inspect state

- `docs/brand/` present? Which of the seven files exist.
- `voice.md`: pack, `Status`, `Last calibrated`, declared locales, and the
  `Humanization` state. An absent field is not silence: it means the pack
  default `on` applies and nobody chose it, which `B064` warns about. When
  the state is `off`, report the `Humanization declined:` reason beside it,
  because an opt-out nobody can see is one nobody can safely reverse.
- `facts.md`: rows, how many with no source or past `Review by`.
- `channels.md`: how many surfaces recorded, which of the product's surfaces
  are missing.
- `strings.md`: rows by status, how many `drifted` or `orphan`.
- `locales/`: declared versus present, parity where computable.
- **Run the linter** `python3 docs/brand/lint.py` and fold its errors and
  warnings into the status.
- Also read `docs/ux/foundation.md` if present — the pack derives from it,
  and a foundation newer than `Last calibrated` is worth saying out loud.

## 2. Repair silently

- `docs/brand/` missing → seed it from the plugin's `templates/brand/` and
  copy the linter, then continue.
- `Sources:` block empty → this is the first thing to fill; nothing else can
  be checked without it. Propose values from the repo layout.

## 3. Status report

One compact table: voice (pack, status, last calibrated, humanization), terminology
(terms, banned, entities), facts (rows, unsourced, overdue), channels
(surfaces recorded / surfaces the product has), strings (by status), locales
(declared, present, parity), linter (errors, warnings).

## 4. Action menu

Offer ONLY the applicable actions, numbered, each with a one-line why. Mark
exactly one "recommended".

1. **Define the voice** — `brand-voice` Init — no `docs/brand/`.
2. **Calibrate** — `brand-voice` Calibrate — pack chosen, product specifics
   thin.
3. **Update** — `brand-voice` Update — positioning, personas, prices or tier
   names changed.
4. **Check** — `python3 docs/brand/lint.py` — mechanical findings with
   `file:line`.
5. **Write or edit copy** — `copywriting` — a named surface.
6. **Audit** — `/ux-audit copy` — what the linter cannot prove: tone drift,
   unproven claims, narrative coherence, the pack's own failure mode.
7. **Nothing** — everything green; rerun after the next text change.

Recommend by state: no pack → 1; unsourced facts → 3; linter errors → 4;
user came with a surface → 5; validated and unaudited → 6.

Additional context from the user: $ARGUMENTS
