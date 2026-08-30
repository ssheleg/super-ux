## Vision alignment — hard rule (super-ux)

Before planning any new feature, capability or significant change, check it
against `docs/ux/vision.md` — specifically the **anti-vision** and the
**alignment test**.

**Aligned** → proceed, and say in one line which part of the vision it serves.

**Misaligned** → stop and say so before writing code:
1. Name the conflict — which layer it contradicts, quoting that layer.
2. Offer two paths: (a) reshape the feature to fit, with the specific change;
   (b) amend the vision, saying which layer changes and what that costs.
3. Wait for the decision. Do not pick one silently.

**Do NOT trigger for:** bug fixes, refactors, dependency work, tests,
documentation, or anything with no user-facing surface. A vision check on a
typo fix is how a team learns to skip the check that matters.
