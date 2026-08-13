# Marketing copy: pages, posts and long form

Craft for the marketing surfaces in [brand-contract.md](brand-contract.md).
Register per surface: [surface-registers.md](surface-registers.md). Platform
mechanics: [channel-playbooks.md](channel-playbooks.md). Anything a search
engine or answer engine will read also passes
[seo-aeo-safety.md](seo-aeo-safety.md).

## Contents

- [Before writing](#before-writing)
- [Page structure](#page-structure)
- [The seven sweeps](#the-seven-sweeps)
- [Word-level defaults](#word-level-defaults)
- [Long form: grounding](#long-form-grounding)
- [Comparison and competitor pages](#comparison-and-competitor-pages)
- [Blog and changelog](#blog-and-changelog)


Marketing copy is read once, by someone who did not ask for it, who is
deciding whether to keep reading. Every rule below follows from that.

## Before writing

Four inputs, and none of them are optional:

- **The one action** this surface is asking for.
- **The reader**, from `foundation.md`: which persona, which job, which
  stage of the journey.
- **Their words**, from the customer-language section of the foundation and
  from `terminology.md`. Copy that names the problem in the reader's words
  outperforms copy that names it in the company's, and the gap is not close.
- **The proof**, from `facts.md`. A claim with no row there does not get
  written. It gets reported as a missing fact.

## Page structure

Above the fold: one headline, one subhead, one primary action.

| Section | Job |
|---|---|
| Headline | the single most important claim, checkable |
| Subhead | the specificity the headline could not carry |
| Primary CTA | verb plus outcome |
| Social proof | credibility, attributed |
| Problem | show you understand the situation |
| Solution | three to five outcomes, not features |
| How it works | reduce perceived complexity to three or four steps |
| Objections | comparison, FAQ, guarantee |
| Final CTA | recap, repeat, remove the risk |

**One idea per section.** A section that advances two arguments advances
neither; split it or cut one.

Headline shapes that survive contact: *outcome without the pain*
("Ship on Friday without the Friday deploy"), *category for an audience*
("The CI for teams that deploy hourly"), *never again* ("Never chase a flaky
test twice"), *the reader's own question*. Pick by what the traffic already
knows, not by preference.

### Page types

- **Homepage.** Several audiences without becoming generic. Lead with the
  broadest true claim, then split the paths.
- **Landing page.** One message, one action, argument complete on the page.
  The headline matches the ad or link that brought the reader; a mismatch is
  the fastest bounce there is.
- **Pricing.** The anxiety is choosing wrong, not the number. Make the
  recommended plan obvious, say what happens at the boundary between plans,
  and state what happens at renewal.
- **Feature.** Feature to benefit to outcome, then a way to try it.
- **About.** Why the product exists, connected to what the reader gets. It
  still carries an action.
- **Comparison.** See the honesty rule below.

## The seven sweeps

An editing pass, run in order. After each sweep, re-check the sweeps before
it: a fix in one dimension routinely breaks an earlier one.

1. **Clarity.** Can a stranger parse every sentence once? Jargon, ambiguous
   pronouns, sentences carrying two ideas, points buried behind
   qualifications.
2. **Voice and tone.** Consistent with `voice.md` and the surface's register?
   Read it aloud; drift is audible before it is visible.
3. **So what.** For every claim, ask it literally. A feature with no
   "which means…" bridge is a fact the reader has to convert themselves, and
   they will not.
4. **Prove it.** Every claim carries evidence or gets softened. Numbers trace
   to `facts.md`. Superlatives without an adjacent sourced fact are `B032`.
5. **Specificity.** "Save time" → "cut reporting from four hours to fifteen
   minutes". Anything that cannot be made specific is usually filler, and
   deleting it costs nothing.
6. **Emotion.** Does the before-state feel real? Pain named but not felt does
   not move anyone. Emotion serves the argument; when it replaces the
   argument, that is manipulation and it is out of bounds.
7. **Zero risk.** At the CTA: what is the reader afraid of, and does the page
   answer it? Trial terms, cancellation, what happens to their data, what
   happens next after the click.

## Word-level defaults

Cut: very, really, extremely, just, actually, basically, in order to.
Replace: utilize → use · leverage → use · facilitate → help · implement →
set up · robust → the specific number · seamless → name the step that
disappeared · innovative → say what is different.

Active voice. One idea per sentence. Vary sentence length deliberately:
uniform length is the most audible tell of machine drafting, and the fix is
rhythm, not vocabulary (see [ai-tells.md](ai-tells.md)).

No rhetorical dash and no full stop after a title. Both are `AT-06` and
`AT-07`, both are checked by `B062` and `B063`, and the replacement is
chosen from the meaning rather than by find-and-replace.

## Long form: grounding

A concept must be **grounded** before a later passage can lean on it. It is
grounded one of two ways: the reader walked in with it (a **prerequisite**),
or an earlier passage established it (**introduced**). A passage that reaches
for an ungrounded concept loses the reader, and the loss is silent.

The unit is the concept, not the word: a paragraph can lean on an idea the
reader lacks with no jargon in sight.

The lever is what you make a prerequisite versus what you ground inside the
piece. Demand too much up front and you shut out the readers you wanted;
ground too much inside and the opening drowns in definitions. Decide it
before the first paragraph, write it down, and when a section turns out to
need something ungrounded, the fix is a grounding passage before it or a
promotion to prerequisite, never proceeding and hoping.

Keep a running list of what is grounded. It is also the outline.

## Comparison and competitor pages

The one place copy is most tempted to lie, and where it is checked hardest.

- Compare against the competitor's **current, real** configuration, not a
  straw one. Date the comparison and say when it was checked.
- Name at least one thing they do better. A comparison with no such line is
  read as an advertisement and discounted entirely. The concession is what
  makes the rest credible.
- Never quote a competitor's number that is not published by them.
- Where they are simply different rather than worse, say different.

## Blog and changelog

A blog post earns its place by carrying something the reader cannot get from
the six posts already ranking: original data, first-hand experience, or a
sharper frame. Restating the consensus in better prose is not a post.

Open with the point, not with context about the industry. Ground terms in
order. End where the argument ends.

A changelog entry says what changed **for the reader**. "Refactored the
scheduler" is a commit message; "Recurring jobs no longer drift by up to
90 seconds" is a changelog entry.
