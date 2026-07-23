---
description: Audit the codebase against scenarios and flows in batches (with full JTBD/story context); depths quick/standard/deep add heuristic, practice, and coverage passes
argument-hint: [all | feature:<name> | SCN-010..SCN-020 | coverage | practices | heuristics] [quick|deep]
---

Invoke the `ux-audit` skill.

Scope + depth: $ARGUMENTS (defaults: all, standard). Depth `deep` runs all
five passes (scenarios, flow conformance, heuristics PRN, practices per the
selection protocol, chain coverage); single-pass scopes run just that pass.
