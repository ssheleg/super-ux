---
description: Update the UX chain after a change to user-facing behavior (same-change rule), or validate a new feature idea against the foundation, flows, and scenarios
argument-hint: "[change or feature description]"
---

If `$ARGUMENTS` describes a **new feature idea**: validate it against the
chain first — which job does it serve, which journey stage, which story
(`ux-foundation` / `ux-scenarios` Validate; an idea serving no job is
challenged, not silently accepted) — then design/extend the affected flows
(`ux-flows`) and cover them with scenarios (`ux-scenarios`).

If it describes a **change already made or in progress**: run the
`ux-scenarios` Update workflow against it (use the current git diff when no
description is given), and cascade to `ux-flows` Update when the change
touches screens, branches, or error paths — updating `screens.md` (states,
elements, coverage) and, when Figma is enabled, the Figma frame(s) and their
links, all in the same change. Leaving `screens.md` or a frame stale is
drift.

**Format migration, offered once per project:** if `docs/ux/screens.md` has
no `<!-- screens-format: 2 -->` line (`docs/ux/doctor.py` reports it), offer
to bring it to format 2 in this change: add one
`- **Axes:** viewport: …; theme: …; text: …; locale: …` line to the Design
system block, give every screen a state list, run `python3 docs/ux/lint.py`
until no U079/U080/U081 warning is left, then add the marker under the title.
Until then those findings are warnings; after it, they fail the lint. Declined
→ leave the file on format 1 and do not ask again.

Change / feature to process: $ARGUMENTS
