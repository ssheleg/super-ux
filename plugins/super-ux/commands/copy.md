---
description: Write, edit, adapt or humanize copy for a named surface — interface strings, landing and pricing pages, blog, changelog, social posts, store listings, ads, lifecycle email — in the product's recorded voice
---

Run the `copywriting` skill.

**First action: read the brand pack** — `docs/brand/voice.md`,
`terminology.md`, and the `channels.md` record for the surface. No pack →
stop and route to `/brand-init`. Do not improvise a voice.

Pick the mode from what the user asked:

| They said | Mode |
|---|---|
| write, draft, need copy for X | **Write** |
| improve, tighten, review this | **Edit** — the seven sweeps, in order |
| turn this into a thread / post / listing | **Adapt** |
| sounds like AI, make it human | **Humanize** — under the ai-tells guards |

Then:

1. Name the surface, and check it exists in `channels.md`. A surface with no
   record is a `brand-voice` decision, not something to invent here.
2. Apply the register: axes from `voice.md` plus that surface's deltas.
   Deltas move axes; they never cross the invariants.
3. Deliver the copy first, the reasoning after. Two or three options for
   headlines and CTAs, each with what it trades away.
4. Interface strings get a `strings.md` row — key, `file:line`, scenario,
   `Status: proposed`.
5. Run `python3 docs/brand/lint.py` over what you touched.

**Report, never invent.** A term missing from the dictionary or a number with
no row in `facts.md` is named as missing. No fabricated statistics, quotes or
experts, under any framing.

Additional context from the user: $ARGUMENTS
