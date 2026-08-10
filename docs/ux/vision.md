# super-ux — Vision

<!-- Managed with super-ux (ux-contract v4). The layer above the chain: what
the product IS and refuses to become. Owned by the `vision` skill. -->

**Status:** approved
**Last reviewed:** 2026-08-10

## 1. Essence

super-ux is a design system for coding agents that makes user behaviour a
versioned artifact, so an interface is decided before it is written and
stays decided after the conversation that produced it is gone.

Rebuild it on a different agent, a different language, a different editor:
the sentence holds. It names no command, no file format and no vendor.

## 2. Core idea

Code-generating capacity is abundant. **Agreement about what the product
should do is scarce**, and it evaporates between prompts — so a coding agent
re-derives intent from the diff and quietly rewrites what was already
approved.

super-ux bridges that gap by giving intent a home the agent must read and
must update.

## 3. What the system does

Interrogates a product for who uses it and why. Derives the paths they take
and the screens those paths need. Records every step, state and error as
prose a machine can check. Traces each layer to the one above so an orphan
is visible. Compares the running code against that record and reports the
gaps with evidence. Refuses to let a change to behaviour land without a
change to the record.

## 4. The user's role

The user **decides and approves**; they do not draw and they do not
specify. They answer questions about their users in their own words, judge
what comes back, and say yes. The vocabulary of the system — layers, skills,
contract versions — is never theirs to learn; `/ux` carries it.

## 5. Principles

- **We make drift checkable, not forbidden.** A rule an agent can violate
  silently is a preference. Every rule here has a linter, a validator or an
  audit behind it — we do not add a rule we cannot fail on.
- **We derive claims, we do not store them.** A count in a document is read
  from the artifact it counts. Stored numbers agree with themselves while
  disagreeing with the world, and nothing reveals it.
- **We name defects with `file:line`, not with adjectives.** An audit finding
  that cannot be opened is an opinion, and opinions do not survive review.
- **We recommend companions, we never require them.** sheleg-design and
  task-pipeline are offered once with their install; the chain works without
  either. A dependency dressed as a recommendation is still a dependency.
- **We degrade rather than block.** No Figma, no foundation, no brand pack —
  the chain says what is missing and continues in a named degraded mode. A
  tool that stops on absence gets removed instead of fixed.

## 6. Anti-vision

super-ux **refuses to become**:

- **A design tool.** We do not render, we do not own a canvas, we do not
  compete with Figma. We describe screens; something else draws them.
- **A design system or component library.** No components, no tokens, no
  palettes ship here. The style pack is sheleg-design's job, recorded in
  `screens.md` by reference.
- **A project tracker.** No tickets, no sprints, no assignees, no status
  workflow beyond what the contract needs. Roadmaps go stale in a quarter
  and take the document's credibility with them.
- **A general "AI docs" generator.** We do not write READMEs, ADRs or API
  docs. One question — what should the interface do — answered completely.
- **A hosted service.** Everything is files in the user's repository, read
  by whatever agent they already run. The moment there is a server, the
  artifact stops being theirs.
- **A framework you build inside.** super-ux never appears in the shipped
  product's dependencies. It is scaffolding for the decision, not for the
  code.

## 7. Horizon

The chain becomes something other tools read, not just this one: a design
record portable enough that an audit, a test generator and a design tool can
each key off the same IDs. The direction is *fewer things super-ux does
itself, more things it makes checkable for others.*

## 8. The one sentence

An interface an agent builds without a written model of user behaviour is a
guess, and super-ux is where that model lives.

## 9. The alignment test

1. Does it make some existing drift **checkable** — by a linter, a
   validator, or an audit with `file:line` evidence? A feature that only
   adds prose fails.
2. Does it stay inside "what should the interface do", or does it start
   answering how it looks, how it is scheduled, or how it is built?
3. Would it still make sense if the user switched agents tomorrow? Anything
   that only works in one harness belongs in that harness.
4. Does it degrade when its input is missing, rather than blocking?
5. Is the number it reports **derived** from an artifact, or stored and
   maintained by hand?
