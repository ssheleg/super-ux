---
description: Initialize the brand pack — read the foundation and existing copy, propose a voice pack with reasoning, seed docs/brand/, and sweep the interface into the string registry
---

Run the `brand-voice` skill in **Init** mode.

Order matters:

1. Read `docs/ux/foundation.md` — personas, jobs, and what the user loses
   when the product fails. No foundation → degraded mode, stamp
   `Derived-from: inferred`, say the WHY layer should be built, continue.
2. Read what the product already says: interface strings, landing copy,
   README, store listing, recent posts.
3. Propose **one** pack with reasoning plus one alternative, and say why the
   runner-up loses.
4. Seed `docs/brand/` from `templates/brand/` **and copy the linter** —
   `scripts/brand_lint.py` → `docs/brand/lint.py`, refreshed even if present
   (it is code, not user content). Fill the `Sources:` block first: nothing
   can be checked until the linter knows where the text is, and nothing can
   be checked at all if the linter was never installed.
5. Sweep the interface into `strings.md`, each row with `file:line` and the
   scenario it serves.
6. Everything starts `Status: draft`. Present for approval section by
   section.

Never invent a fact to fill a table. An unknown is reported.

Additional context from the user: $ARGUMENTS
