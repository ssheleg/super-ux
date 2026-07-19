## UX scenarios — hard rule (super-ux)

- `docs/ux/scenarios.md` is the source of truth for all user-facing behavior.
- Any change that touches user-facing behavior MUST update
  `docs/ux/scenarios.md` in the same change (add/adjust scenarios, statuses,
  coverage).
- Any new feature or project STARTS with scenarios: draft them, validate
  against existing scenarios (conflicts, overlaps, gaps), get them approved —
  only then design and build UI.
- Use the `ux-scenarios` skill to maintain the base and `ux-audit` to verify
  the codebase against it.
