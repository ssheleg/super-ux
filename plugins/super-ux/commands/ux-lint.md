---
description: Lint docs/ux for integrity and drift — missing Figma frames, unresolved SCR/story traces, orphans, built screens without coverage, index desync, broken links
argument-hint: [--strict]
---

Run the super-ux linter against this project's `docs/ux/`:

```
python3 docs/ux/lint.py $ARGUMENTS
```

If `docs/ux/lint.py` is missing, run `/ux-rule` first to seed it (or copy it
from the plugin's `scripts/ux_lint.py`).

Read the output and FIX what it reports — errors are drift/broken structure
that must not merge; warnings are gaps to close. Re-run until clean. Run
this after any UX change and before calling the work done; recommend wiring
it into the project's CI or pre-commit so drift can't merge silently.
