---
name: vision
description: Use when a project needs the layer ABOVE personas and jobs - what the product IS, why it exists, and what it refuses to become. Writes docs/ux/vision.md in nine layers (essence, core idea, system behaviour, user role, principles, anti-vision, horizon, the one sentence, and the alignment test) and installs a vision-alignment rule into the project's own instruction file so later features get checked against it. Triggers - "vision" / "видение", "product vision" / "продуктовое видение", "what is this product about", "define product direction", "write a vision", new project with no direction, a feature that feels off-strategy.
license: MIT
---

# vision

The layer above `ux-foundation`. Foundation answers **who** uses the product and
**why**; vision answers **what the product is** and **what it refuses to
become**. Without it, "should we build this?" has no answer that outlives the
person who last had an opinion.

> **This skill produces two things, and the second is the point.**
> 1. `docs/ux/vision.md` — the document.
> 2. A **vision-alignment rule** in the project's own instruction file, so every
>    later feature gets checked against the vision instead of the vision being
>    written once and never read.
>
> A vision nothing reads is a document, not a constraint.

Fits the chain: **vision → foundation (personas, JTBD, journeys, stories) →
flows → scenarios → audit.** Each layer traces up to the one above it.

## Step 0 — read the project, not its README

Before writing a word:

1. `README.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `CHANGELOG.md`, everything in
   `docs/`.
2. Key source: entry points, main services, the schema, the routing table.
3. Marketing surfaces if they exist — landing, pricing, features.
4. `package.json` / `pyproject.toml` / `Cargo.toml` for what it actually depends on.
5. The live UI. What the product *does*, not what it says it does.
6. If `docs/ux/foundation.md` exists, read it — the vision must not contradict
   the personas and jobs already agreed.

**A vision written from the README alone describes the README.** The gap between
what a project says it is and what its code does is usually where the real
vision is hiding, and naming that gap out loud is often the most valuable thing
this skill does.

## Step 1 — the transformation

Answer internally before writing:

```
User BEFORE this product exists →  [chaos / complexity / pain]
User AFTER  this product exists →  [clarity / simplicity / power]
```

Everything below flows from this. If you cannot state it, you do not yet know
the product well enough to write its vision — go back to step 0.

## Step 2 — write `docs/ux/vision.md` in nine layers

Every layer is mandatory. Write in the project's documentation language.

**1. Essence.** One sentence. `[Product] is [type of system] that changes how
[user] [does X]`. No feature names, no UI, no technology. The test: *if the
product were rebuilt from scratch on a different stack, would this sentence
still be true?* If not, it names an implementation, not an essence.

**2. Core idea.** Not a problem statement — an observation about the world.

```
[X] is abundant.
[Y] is scarce.
→ this product bridges the gap.
```

One observation, not a list. "Information is abundant, clarity is scarce."

**3. What the system does.** Continuous behaviour, verbs not nouns:
*observes … understands … transforms … surfaces …*. No feature names. "Has a
dashboard" is not behaviour; "surfaces contradictions between sources" is.

**4. The user's role.** What the user becomes when using it. Not "the user
clicks" — the user *directs*, *judges*, *decides*. If the user's role is
indistinguishable from operating any other tool, the vision is not yet specific.

**5. Principles.** Three to five, each in the form *we do X, not Y*, where Y is
something a reasonable team would actually choose. A principle with no rejected
alternative is a slogan.

**6. Anti-vision.** What this product **refuses to become**, explicitly. This is
the layer teams skip and the only one that ever settles an argument. Name the
adjacent products it could drift into and say no to each.

**7. Horizon.** Where this goes in two to three years, as a direction, not a
roadmap. Roadmaps belong in the tracker and go stale in a quarter.

**8. The one sentence.** If someone remembers exactly one thing, this is it.

**9. The alignment test.** Three to five questions any proposed feature must
pass. These are what the rule in step 4 will actually run.

## Step 3 — validate before you ship it

Check every one, and fix rather than rationalize:

- [ ] Essence survives a total rewrite on different technology
- [ ] No layer names a feature, a screen, or a vendor
- [ ] The anti-vision names real alternatives, not strawmen
- [ ] Principles have a rejected side that someone might genuinely have picked
- [ ] Nothing contradicts `docs/ux/foundation.md` — and if something does, that
      is a finding to raise, not to quietly smooth over
- [ ] A stranger could use the alignment test to reject a plausible feature

## Step 4 — install the alignment rule

Write the rule into **the project's own instruction file**, the same one
`ux-rule` uses: `CLAUDE.md` for Claude Code, `AGENTS.md` for Codex and opencode,
`GEMINI.md` for Gemini. Detect which the project already has; create `CLAUDE.md`
only if none exists. **Never hardcode one agent's path** — a rule installed
where the running agent cannot see it is worse than no rule, because everyone
believes it is covered.

Idempotent: if the heading is already present, update the block in place rather
than appending a second copy.

```markdown
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
```

## Step 5 — point the README at it

One line under the project's overview linking `docs/ux/vision.md`. A vision
nobody can find from the front door is a vision nobody reads.

## Common mistakes

| Mistake | Why it breaks |
|---|---|
| Essence names the technology | it stops being true at the first rewrite |
| Principles with no rejected side | "we value quality" settles no argument |
| No anti-vision | the one layer that decides scope questions, missing |
| Horizon written as a roadmap | stale in a quarter, and then the whole document reads as stale |
| Vision contradicts `foundation.md` | two sources of truth, and teams follow whichever they read last |
| The rule installed at one agent's hardcoded path | invisible to the agent actually running; nobody notices, because absence looks identical to compliance |
| Written from the README | describes the README |
