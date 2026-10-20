---
description: Build or update personas, jobs, journeys and stories in docs/ux/foundation.md
argument-hint: "[what changed or what to explore]"
---

Invoke the `ux-foundation` skill.

Pick the workflow from state: no `docs/ux/foundation.md` → Init (interview
for greenfield, reverse for an existing product); exists and `$ARGUMENTS`
describes new knowledge → Update; exists and consistency is the question →
Validate.

After any change, run the cascade check: list scenarios tracing to changed
IDs and hand them to the `ux-scenarios` skill in the same session.

Context from the user: $ARGUMENTS
