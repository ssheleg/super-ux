# Surface registers — one voice, many surfaces

A product has **one** voice and roughly two dozen surfaces. The mistake this
reference exists to prevent is solving that with two dozen voices — which is
how a product ends up reading like three different companies, and is the
verbal twin of the visual drift a style pack prevents.

Field names and the surface list come from
[brand-contract.md](brand-contract.md). The axes being shifted are the five
fixed axes in `voice.md`, filled by a pack from
[voice-packs.md](voice-packs.md).

## The model

A **register** is the voice with per-axis deltas applied. Nothing else
changes: the vocabulary in `terminology.md`, the numbers in `facts.md`, and
the invariants declared in `voice.md` hold on every surface.

```
voice.md            axes + invariants          (one per product)
   │
   └── channels.md  register = axes ± deltas   (one record per surface)
```

Deltas are written as signed steps on named axes: `humor -2, density +1`.
A step is a perceptible shift, not a percentage — three steps in either
direction is the practical range before the voice stops being recognisable.

## Rule 1 — a register moves the axes, never the invariants

`voice.md` lists what is invariant. A Reddit post may run long, drop the CTA,
and turn self-deprecating; if the brand does not hedge, it does not hedge
there either.

This is the rule that keeps per-surface freedom from becoming per-surface
improvisation. When a surface seems to need an invariant broken, the answer
is one of two things, and neither is breaking it quietly: the invariant was
wrong and `voice.md` changes for the whole product, or the surface is wrong
for this product and is not used. Both are decisions with an owner.

## Rule 2 — platform physics and brand choice are different fields

"A link in the post body suppresses reach" is a fact about an algorithm.
"We do not post links" is a decision someone made. Written on one line they
become indistinguishable within a quarter, and then nobody can tell which one
is safe to revisit when the platform changes its ranking.

So `Forbidden:` always carries both halves, and one of them may be `none`:

```
Forbidden:  physics: link in body suppresses reach; >2 hashtags penalised
            | brand: no engagement bait, no fake urgency
```

The linter enforces the physics half (`B042`, `B043`, `B040`) because it is
mechanical. The brand half is judged by the `copy` audit scope, because it is
a decision.

## Rule 3 — humor is forbidden where the user is losing something

On `error`, `destructive confirm`, `billing and receipts` and
`paywall and upgrade`, humor, exclamation marks and emoji are banned in every
pack — including `playful-consumer`. The user is losing data, access or money
at that moment, and levity reads as mockery of a loss the product caused.

This is `B061` and it blocks. It is not a register delta, because a delta is
negotiable and this is not.

---

## Product surfaces

The register notes below are defaults. A pack's own `Register deltas` field
overrides them where the two disagree, and the project's `channels.md`
overrides both.

### primary action

The button that carries the screen. Verb phrase naming the outcome, not the
mechanism: `Publish`, not `Submit`. One action keeps one name across the
whole flow — button `Publish`, toast `Published`, history entry `Published`.
Two names for one action is `B020` and it is the single most common copy
defect in a product built screen by screen.

### empty state

Teaches, never apologises. Three jobs in order: what belongs here, why it is
worth putting there, and the one action that starts it. An empty state that
only says "Nothing here yet" wastes the highest-attention moment a feature
gets.

Register: humor unchanged — this is where a warm pack earns its keep.

### error

Three facts, in this order: what happened, what was **not** affected, and the
one next step. The middle one is the one products skip and users need most —
"your draft was saved" turns a failure into an interruption.

Never blame the user, never say "unexpected", never show a code without a
sentence. Register: humor −3, density +1, distance −1.

### loading

If it is under 400ms, say nothing. If it is longer, say what is happening in
the product's own words. If it is longer than about ten seconds, say what the
user can do meanwhile, and never let the copy claim progress the system
cannot observe.

### success / toast

The past tense of the action's own verb, and nothing else. `Published.` A
toast is not a place for a sentence.

### onboarding

Density −1 from base for every pack. Terseness that reads as confident to an
expert reads as withholding to someone on their first screen. Name the
first-value moment in the user's terms and get there; explain the model only
where the next step is impossible without it.

### paywall and upgrade

Say what is being sold, what it costs, what happens at the end of the term,
and how to leave. Humor −3, absolute. A joke while asking for money reads as
a trick, and the read is not unfair.

### destructive confirm

Name the object, the consequence, and whether it is reversible. `Delete
project "Atlas" and its 340 files. This cannot be undone.` The confirming
verb matches the destructive verb — `Delete`, never `OK`. Humor −3.

### billing and receipts

Numbers, dates, and what happens next. Every figure traceable to `facts.md`
or to the account itself. Humor −3.

### settings and legal

Labels label, help text explains, examples demonstrate — one job per string.
Plain language applies to legal text too: a consent notice nobody understands
is not consent.

### transactional email and push

One purpose per message, named in the first line. Push has no room for a
register: state the fact and the object. A notification that says "Something
happened" is a notification that gets disabled.

### docs and help

Humor −2, density −1. Ground a term before leaning on it — see the grounding
model in [marketing-copy.md](marketing-copy.md). The reader is here because
something did not work; every sentence either moves them forward or is cut.

---

## Marketing surfaces

Per-platform mechanics — limits, what suppresses reach, what each surface
rewards — live in [channel-playbooks.md](channel-playbooks.md). This section
covers only the register.

### landing hero

The one surface where every pack drops density by a step: the reader has not
opted in yet. One claim, checkable, in the reader's own words. Confidence +1.

### landing body

Base register. One idea per section, each advancing a single argument.

### pricing

Density +1 and confidence +1 in every pack. Anxiety here is about choosing
wrong, not about the number: make the recommended plan obvious and say what
happens at the boundary between plans.

### blog

Distance −1, density −1. Long enough to ground its terms, and no longer.

### changelog

Distance −1, humor +1 where the pack allows. Users who read changelogs are
the ones who stayed; write to them as such. Every entry says what changed for
the reader, not which module was refactored.

### X

Density +1, distance −1. One idea per post; the first line decides whether
the rest is read.

### Reddit

Distance −2, humor +1, CTA dropped entirely. The register that works
elsewhere reads as marketing intrusion here. A post that would work unchanged
on the landing page should not be posted.

### LinkedIn

Distance −1, density −1. The platform rewards a specific claim with a
consequence; it punishes the abstract lesson.

### HN and Product Hunt

Confidence +1, humor −1, density +1. State what it is, what it does not do,
and what it costs, in the first three sentences. Anything that reads as
positioning gets answered as positioning.

### App Store and Google Play

Density +2 — the field limits leave no room for register at all. Craft rules
are in [store-copy.md](store-copy.md).

### ads

Density −1 in every pack. One claim and one action; an ad has no room to
ground a term, so any term needing grounding is the wrong term for an ad.

### lifecycle email

Distance +1. One purpose per email, named in the subject line, delivered in
the first sentence.
