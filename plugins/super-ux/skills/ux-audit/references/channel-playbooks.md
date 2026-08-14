# Channel playbooks: the physics of each surface

One playbook per marketing surface. Everything here is **platform physics**:
what the surface rewards, what it suppresses, what it limits. The register,
meaning how the voice shifts, lives in
[surface-registers.md](surface-registers.md), and the two are kept apart on
purpose, because merged they become indistinguishable within a quarter and
nobody can tell which half is safe to revisit when a platform changes.

## Contents

- [X](#x)
- [Reddit](#reddit)
- [LinkedIn](#linkedin)
- [HN and Product Hunt](#hn-and-product-hunt)
- [Blog](#blog)
- [Changelog](#changelog)
- [Ads](#ads)
- [Lifecycle email](#lifecycle-email)


Store listings have their own file: [store-copy.md](store-copy.md).

Anything a crawler or answer engine reads also passes
[seo-aeo-safety.md](seo-aeo-safety.md).

> **Physics decays.** Every ranking behaviour below carries the date it was
> last checked. A rule older than its review date is a hypothesis, not a
> constraint, so re-verify before treating it as one. Recording the date is
> what makes that possible; a rule with no date cannot be audited, only
> believed.

## X

*Physics checked 2026-08-05.*

- A link in the post body suppresses reach. Put it in the first reply.
  Enforced as `B042` when `channels.md` declares it.
- More than two hashtags is penalised. Zero is usually right.
- Replies received are weighted far above likes. Content that ends in a real
  question outperforms content that ends in a claim.
- Bookmarks weigh heavily: tactical, save-worthy posts (a list, a framework,
  a checklist) accumulate reach for days.
- Threads: 5–12 posts. Each one has to stand alone, because a weak post mid-thread
  costs the whole thread. The first line decides everything; if it does not
  stop the scroll, nothing after it is read.
- Editing within the first half hour resets distribution.

## Reddit

*Physics checked 2026-08-05.*

- The register that works everywhere else reads as intrusion here. A post
  that would work unchanged on the landing page should not be posted.
- Subreddit rules outrank every guideline in this file. Read them, and the
  last month of the sub, before writing.
- Self-promotion ratios are enforced socially and by moderators. Disclose the
  affiliation in the post, not in a reply after someone asks.
- No CTA. The link, if any, goes in a comment, and only if someone asks.
- Titles are not headlines: a headline sells, a Reddit title states. The
  title that performs is the one that could have been asked by a member.
- Being wrong in public and correcting it earns more than being right
  smoothly. Comments are the content.

## LinkedIn

*Physics checked 2026-08-05.*

- The first two lines appear before the fold; everything else is behind
  "…more". The break is the hook.
- External links in the body suppress reach; first comment is the
  convention.
- A specific claim with a consequence outperforms the abstract lesson. Named
  numbers, named outcomes, named mistakes.
- Documents (carousels) hold attention longer than text at the same length.
- Dwell time and comments dominate. Posts that invite a professional
  disagreement do well; posts that invite agreement do not.

## HN and Product Hunt

*Physics checked 2026-08-05.*

- State what it is, what it does not do, and what it costs, in the first
  three sentences. Anything read as positioning gets answered as positioning,
  and that thread is unrecoverable.
- The title carries no adjectives. `Show HN: <what it does>` is the whole
  shape.
- The founder answering questions in the thread is the content. Absence
  reads as a drive-by.
- Known limitations posted by the team land better than the same limitations
  discovered by a commenter.
- Never argue with a downvote, never edit away a criticism, never seed
  comments.

## Blog

- Ranking and citation mechanics: [seo-aeo-safety.md](seo-aeo-safety.md).
- Ground terms in order; the grounding model is in
  [marketing-copy.md](marketing-copy.md).
- Length follows the argument. A post padded to a word count is visible as
  padding, and padding is one of the strongest machine-drafting tells.
- One canonical claim per post. A post arguing two things ranks for neither.
- Date it, and update the date only when the content actually changed.

## Changelog

- Every entry says what changed for the reader. "Refactored the scheduler" is
  a commit message; "Recurring jobs no longer drift by up to 90 seconds" is a
  changelog entry.
- Breaking changes lead, with the migration path in the same entry.
- Group by user-visible area, never by internal module.
- Readers of changelogs are the users who stayed. Write to them as such.

## Ads

- One claim, one action. An ad has no room to ground a term, so a term
  needing grounding is the wrong term for an ad.
- The landing page headline matches the ad. A mismatch is the fastest bounce
  there is, and it is also the cheapest fix.
- Field limits are enforced by `B040` against the values in `channels.md`,
  multiplied by the locale's length coefficient.
- Claims in ads carry the same `facts.md` requirement as everywhere else, and
  the platform's own review will check some of them.

## Lifecycle email

- One purpose per email, named in the subject and delivered in the first
  sentence. An email with two asks gets neither.
- The subject is a promise; the first line pays it. Curiosity-gap subjects
  raise opens once and unsubscribes permanently.
- Transactional and marketing are different surfaces with different consent.
  Never smuggle marketing into a receipt.
- Every email states why the person is receiving it and how to stop, in
  plain words rather than legal ones.
- Preheader text is copy, not overflow. Left unwritten, the client shows the
  first sentence of the body, which is rarely what you would have chosen.
