---
description: Design, reverse-engineer, update, or improve user flows — task analysis, mermaid flow diagrams, screen states, wireframes, Figma mockups, heuristic UX evaluation
argument-hint: '[story/feature to design | "improve" | what changed]'
---

Invoke the `ux-flows` skill.

If this is design/improve work and the foundation has no Figma choice
recorded, ask once whether to mock up in Figma (default yes); when enabled,
mirror each screen into a Figma frame applying the visual-craft practices
and link every screen row to its frame.

Settle the visual identity before drawing anything: read `screens.md` →
Design system → `Style pack`, and when it's empty pick one with the
**sheleg-design** companion skill (offer its one-time install if missing —
recommend, don't force) and record the pack + its token file. Frames and
built screens use that pack's tokens instead of a per-screen palette.

Pick the workflow from state and `$ARGUMENTS`: stories exist but flows
don't → Design; existing product without flows.md → Reverse; `$ARGUMENTS`
says improve/fix/redesign → Improve (heuristic evaluation PRN-01..24 →
traced before/after proposals); otherwise → Update.

After flow changes, cascade to `ux-scenarios`: every new/changed node and
edge needs scenario coverage in the same session.

Context from the user: $ARGUMENTS
