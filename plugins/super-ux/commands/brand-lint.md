---
description: Run the brand linter over docs/brand/ and the declared sources — contract, terminology, string consistency, facts, channel limits, bot safety, AI markers and locales
---

Run the deterministic half of the brand check:

```bash
python3 docs/brand/lint.py
```

Exit codes: `0` clean or warnings only, `1` warnings under `--strict`, `2` any error. One pack, one policy: this linter returned `1` on warnings alone until 2026-08-20, while `docs/ux/lint.py` needed `--strict` for the same thing — so 13 of the 39 codes failed a build while reporting no error.

Useful flags: `--fix` applies only the three changes that cannot be wrong
(casing, the iOS keyword field, re-pointing a registry row whose string is
unchanged and matches exactly one new location); `--brief` prints one line,
for sweeping several projects; `--json` for pipelines.

Report findings grouped by code, most severe first, each with its
`file:line`. For every error, give the fix in one sentence.

**What this cannot answer.** The linter proves the mechanical half. Tone
drift, whether a claim lands, narrative coherence, and whether the voice has
overshot into the failure mode its pack declared are judged by
`/ux-audit copy`. If the linter is clean, say that clean means *checkable*,
not *good* — and offer the audit.

If there is no `docs/brand/`, do not lint an absence: route to `/brand-init`.

Additional context from the user: $ARGUMENTS
