---
description: Diagnose docs/ux against the current contract — mixed or stale contract versions, unmarked artifacts, files the tooling cannot find, audits with no base
argument-hint: "[path] [--fix] [--brief]"
---

Diagnose this project's UX chain against the contract it should be on:

```
python3 docs/ux/doctor.py $ARGUMENTS
```

If `docs/ux/doctor.py` is missing, copy it from the plugin's
`scripts/ux_doctor.py` (or run `/ux-rule`, which seeds both scripts).

`/ux-lint` checks a chain against itself — ids, links, orphans. It cannot see
that the whole base is written to a contract three versions old, because from
the inside such a chain is perfectly consistent. That is what this finds:
drift between the project and the contract, not within the project.

What it reports:

- **Mixed contract** — artifacts last touched by different versions and never
  reconciled. Seen in the wild with `foundation.md` on v2 and `screens.md` on
  v4 in the same project.
- **Behind / unmarked** — the effective version, and what each version since
  it introduced, so "upgrade" is a list rather than a feeling.
- **Misnamed** — a file the contract owns under another name (`ux-scenarios.md`
  instead of `scenarios.md`). The tooling looks for the contract name, finds
  nothing, and says so quietly.
- **Audits without a base** — reports produced against scenarios that are not
  there.
- **Optional and absent** — additive sections the project has not adopted.
  Not a problem; worth knowing.

`--fix` applies only what cannot be wrong: renaming a file the contract owns,
moving audit reports into `audits/`. Contract upgrades are content decisions —
run `/ux-update` for those, one layer at a time, and re-run the doctor after.

`--brief` prints one line per project, for sweeping several at once.
