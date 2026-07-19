---
description: Update the UX scenario base after a change to user-facing behavior (same-change rule), or validate a new feature idea against existing scenarios
argument-hint: [change or feature description]
---

Invoke the `ux-scenarios` skill.

If `$ARGUMENTS` describes a **new feature idea**, run the Validate workflow
first (which existing scenarios does it touch, contradict, or duplicate?),
then draft the new scenarios. If it describes a **change already made or in
progress**, run the Update workflow against it (use the current git diff
when no description is given).

Change / feature to process: $ARGUMENTS
