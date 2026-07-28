---
description: Initialize the full UX chain for this project — foundation (personas, JTBD, journeys, stories), then scenarios derived from it
---

Initialize the UX chain, WHY → HOW → WHAT:

1. **Foundation.** If `docs/ux/foundation.md` is missing or empty, invoke
   the `ux-foundation` skill in Init mode — interview for greenfield,
   reverse-engineering for an existing product. Get the layers approved.
   (Tiny project and the user explicitly wants to skip? Note it and go
   v1 mode — scenarios without Traces.)
2. **Flows.** Invoke the `ux-flows` skill: Design (greenfield — task
   analysis → mermaid flows → screen states per story) or Reverse
   (existing code — reconstruct actual flows with evidence, tag
   `inferred`).
3. **Scenarios.** Invoke the `ux-scenarios` skill in Init mode: cover
   every flow node and edge (happy path, error edges, alt branches) with
   use-case scenarios, `Traces:` filled with story + flow IDs.
4. Finish with the traceability check (Validate) and a status summary.

If `foundation.md`, `flows.md`, and `scenarios.md` already exist with
entries, do NOT reinitialize — say so and suggest `/ux` for the action menu
instead. If only some layers exist, initialize the missing ones and leave
the rest untouched.

Additional context from the user: $ARGUMENTS
