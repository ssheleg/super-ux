---
description: Update the UX chain after a change to user-facing behavior (same-change rule), or validate a new feature idea against the foundation, flows, and scenarios
argument-hint: [change or feature description]
---

If `$ARGUMENTS` describes a **new feature idea**: validate it against the
chain first — which job does it serve, which journey stage, which story
(`ux-foundation` / `ux-scenarios` Validate; an idea serving no job is
challenged, not silently accepted) — then design/extend the affected flows
(`ux-flows`) and cover them with scenarios (`ux-scenarios`).

If it describes a **change already made or in progress**: run the
`ux-scenarios` Update workflow against it (use the current git diff when no
description is given), and cascade to `ux-flows` Update when the change
touches screens, branches, or error paths.

Change / feature to process: $ARGUMENTS
