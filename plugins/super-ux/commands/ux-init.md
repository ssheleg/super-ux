---
description: Initialize the full UX chain for this project — foundation (personas, JTBD, journeys, stories), then scenarios derived from it
---

Initialize the UX chain, WHY before WHAT:

1. **Foundation.** If `docs/ux/foundation.md` is missing or empty, invoke
   the `ux-foundation` skill in Init mode — interview for greenfield,
   reverse-engineering for an existing product. Get the layers approved.
   (Tiny project and the user explicitly wants to skip? Note it and go
   v1 mode — scenarios without Traces.)
2. **Scenarios.** Invoke the `ux-scenarios` skill in Init mode: derive
   scenarios from the stories and journey stages (greenfield) or run the
   inventory sweep and trace everything found back to the foundation
   (existing code), filling `Traces:`.
3. Finish with the traceability check (Validate) and a status summary.

If both files already exist and are non-empty, do NOT reinitialize — say so
and suggest `/ux` for the action menu instead.

Additional context from the user: $ARGUMENTS
