---
description: Write the product vision (docs/ux/vision.md) and install the alignment rule into this project's instruction file
argument-hint: "[optional: what the product is, in one line]"
---

Run the `vision` skill for this project.

It sits above `ux-foundation`: foundation answers who uses the product and why,
vision answers what the product is and what it refuses to become.

1. Read the project properly first — README, architecture, roadmap, key source,
   the live UI, and `docs/ux/foundation.md` if it exists. Not the README alone.
2. Write `docs/ux/vision.md` in the nine layers, the anti-vision included —
   it is the layer teams skip and the only one that settles arguments.
3. Validate against the checklist; a contradiction with `foundation.md` is a
   finding to raise, not to smooth over.
4. Install the vision-alignment rule into the project's OWN instruction file
   (`CLAUDE.md` / `AGENTS.md` / `GEMINI.md` — whichever it already uses).
   Idempotent. Never hardcode one agent's path.
5. Link it from the README.

$ARGUMENTS
