---
description: Recalibrate the brand pack after positioning, personas, pricing or naming changed — propagate the change through terminology, strings and every locale in the same edit
---

Run the `brand-voice` skill in **Update** mode.

1. Name what changed — positioning, a persona, a price, a tier name, a new
   surface, a fact past its review date.
2. Apply the edits where they belong. A renamed entity propagates to
   `terminology.md`, `strings.md` and every `locales/<code>.md` **in the same
   change** — a rename that lands in one file and not the others is how two
   spellings start.
3. Changed files drop to `Status: draft` until re-approved.
4. Re-stamp `Last calibrated`.
5. Run `python3 docs/brand/lint.py` and report what moved.

If the foundation changed rather than the copy, say so: the pack derives from
it, and a positioning change may deserve a different pack rather than a
patched one.

Additional context from the user: $ARGUMENTS
