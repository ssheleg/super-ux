---
description: Initialize the UX scenario base (docs/ux/scenarios.md) for this project — interview-first for greenfield, inventory sweep for existing code
---

Invoke the `ux-scenarios` skill in Init mode.

Auto-detect the variant: if the project has little or no product code, run
**Init (greenfield)** — interview the user and design the scenario base
before any UI exists. If there is an existing product codebase, run **Init
(existing code)** — inventory sweep, then draft scenarios covering
everything found and flag both gap directions.

If `docs/ux/scenarios.md` already exists, do NOT reinitialize — say so and
suggest `/ux-update` or the Validate workflow instead.

Additional context from the user: $ARGUMENTS
