---
description: Initialize the full UX chain for this project — the vision (optional), then foundation (personas, JTBD, journeys, stories), flows, screens and scenarios derived from it
---

Initialize the UX chain, WHAT-IT-IS → WHY → HOW → WHAT-IT-DOES:

0. **Vision (offer, never assume).** If `docs/ux/vision.md` is missing, ask
   once whether the product's direction is settled. Settled → say so and go
   to 1. Not settled, or the answer is "we keep arguing about scope" →
   invoke the `vision` skill first: the anti-vision is what later stops a
   feature that every persona would happily use and the product should not
   have. **Never seed an empty `vision.md`** — a blank vision reads as a
   decided one, and every later check would pass over it.

1. **Foundation.** If `docs/ux/foundation.md` is missing or empty, invoke
   the `ux-foundation` skill in Init mode — interview for greenfield,
   reverse-engineering for an existing product. Get the layers approved.
   (Tiny project and the user explicitly wants to skip? Note it and go
   v1 mode — scenarios without Traces.)
2. **Flows.** Invoke the `ux-flows` skill: Design (greenfield — task
   analysis → mermaid flows → screen states per story) or Reverse
   (existing code — reconstruct actual flows with evidence, tag
   `inferred`).
3. **Scenarios.** Invoke the `ux-scenarios` skill in Init mode: cover
   every flow node and edge (happy path, error edges, alt branches) with
   use-case scenarios, `Traces:` filled with story + flow IDs.
4. Finish with the traceability check (Validate) and a status summary,
   then run `python3 docs/ux/lint.py` and report its counts. If a
   `vision.md` exists, confirm its alignment rule reached the project's
   instruction file — the linter warns when it did not.

5. If the product has user-facing text, say that `docs/brand/` is the layer
   that governs it and offer `/brand-init`. The chain decides what the
   product does; it does not decide how it speaks.

If `foundation.md`, `flows.md`, and `scenarios.md` already exist with
entries, do NOT reinitialize — say so and suggest `/ux` for the action menu
instead. If only some layers exist, initialize the missing ones and leave
the rest untouched.

Additional context from the user: $ARGUMENTS
