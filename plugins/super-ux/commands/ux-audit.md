---
description: Audit the codebase against the UX scenario base in batches (with full JTBD/story context), or audit chain coverage; evidence-backed report to docs/ux/audits/
argument-hint: [all | feature:<name> | SCN-010..SCN-020 | coverage]
---

Invoke the `ux-audit` skill.

Scope: $ARGUMENTS (default: all). Scope `coverage` audits the
foundation↔scenarios chain (orphans, journey gaps) instead of the code.
