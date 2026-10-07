# Channel playbooks: the physics of each surface

One playbook per marketing surface. Everything here is **platform physics**:
what the surface rewards, what it suppresses, what it limits. The register,
meaning how the voice shifts, lives in
[surface-registers.md](surface-registers.md), and the two are kept apart on
purpose, because merged they become indistinguishable within a quarter and
nobody can tell which half is safe to revisit when a platform changes.

## Contents

- [X](#x)
- [Instagram](#instagram)
- [Short video](#short-video)
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

*Physics checked 2026-10-07 against the open-source ranker
[`xai-org/x-algorithm@e62790c`](https://github.com/xai-org/x-algorithm/blob/e62790c99484b51424c2eccc488ed4e7517e8778/home-mixer/params/param.rs),
`home-mixer/params/param.rs` lines 314–426, commit of 2026-10-06.*

The ranker scores a post as the sum of `weight × P(action)` over the actions
it predicts for one viewer. The weights multiply **predicted probabilities,
not counts**: the source says so beside the table, so "one report cancels 468
likes" is a misreading. Only actions on posts served in the Home timeline
count; a visit by direct link does not.

| Action | Weight | | Action | Weight |
|---|---|---|---|---|
| share via copy link | 20 | | like | 0.5 |
| reply | 5 | | open link | 0.2 |
| reply from a mutual follow | +15 boost | | mute author | −58.8 |
| quote | 5 | | not interested | −47.52 |
| share via DM | 5 | | block author | −31.2 |
| follow author | 4 | | report | −234 |
| share | 2 | | repost | 1 |

- **Write the post someone forwards.** Copying the link (20) and sending it in
  a DM (5) outweigh a like (0.5) by an order of magnitude or more: a figure, a
  checklist, a quotable line.
- **Write the post someone answers.** Replies and quotes weigh 5 each, ten
  times a like, and a reply from someone who follows the author back adds 15
  (A/B-tested from 2026-07-10, at 15 since 2026-07-24, per
  `docs/BIDIRECTIONAL_BOOST_CHANGE.md` in the same repository). Content that
  ends in a real question outperforms content that ends in a claim.
- **The post sells the account.** Follow author weighs 4.
- **Irritation is expensive.** Mute −58.8, not interested −47.52, block
  −31.2, report −234: bait that earns clicks and annoys loses on balance.
- **The window is 48 hours.** The candidate filter drops posts older than
  that from For You (README, filter table, same commit).
- **Unverified in the published ranker, kept as practice:** a link in the
  body suppressing reach. `open link` carries +0.2 and no penalty appears in
  the weights; a rule can still live in configuration or visibility filters
  this repository does not publish, so "not in the code" is not "refuted".
  Put the link in the first reply when `channels.md` declares it; `B042`
  enforces that declaration.
- **Removed 2026-10-07, not found in the ranker:** "bookmarks weigh heavily"
  (bookmarks exist as counts and model features, with no weight in the scorer)
  and "more than two hashtags is penalised" (no hashtag term in the value
  model). Absence from code is not proof of absence from the product; neither
  claim is a constraint until a source shows it.
- Threads: 5–12 posts. Each one has to stand alone, because a weak post mid-thread
  costs the whole thread. The first line decides everything; if it does not
  stop the scroll, nothing after it is read. *(Practice, checked 2026-08-05.)*
- Editing within the first half hour resets distribution. *(Practice, checked
  2026-08-05; not verified in the ranker.)*

## Instagram

*Physics checked 2026-10-07.* The caption under a post or a reel. The reel's
script is the [short video](#short-video) surface and
[video-script.md](video-script.md).

- **The feed shows about 125 characters before "… more".** The first line
  either fits that window or is cut mid-thought, and a tag or a mention spent
  there is a hook not written. The number is the window measured by
  `Jakeschincariol/instagram-agent-skill`
  ([`caption.py`](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-caption/caption.py),
  `TRUNCATE = 125`), not an Instagram specification; declare it as `fold 125`
  and `B045` checks it.
- **Five hashtags at most, since 2025-12-18.** The @creators account:
  "Using fewer (up to 5) more targeted hashtags … can improve both your
  content's performance"
  ([Keywords Everywhere, retelling](https://keywordseverywhere.com/news/instagram-algorithm-updates/)).
  Hashtags are navigation, not reach
  ([Planoly on Mosseri](https://planoly.com/blog/debunking-common-instagram-myths)).
  Declare `max 5 hashtags`; `B043` checks it.
- **Links in a caption do not click.** The link goes in the bio, a DM or a
  story; declare `link in body` and `B042` checks it
  ([`ig-caption/SKILL.md`](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-caption/SKILL.md)).
- **One ask.** Two asks split a reader's single action; declare `one ask` and
  `B046` counts them ([`ig-caption/SKILL.md`](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-caption/SKILL.md)).
- **Search reads the caption.** Write the phrase a person would type, in a
  sentence, rather than as a hashtag ([`ig-caption/SKILL.md`](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-caption/SKILL.md)).
- **Sends per reach is the signal for people who do not follow you yet.**
  Mosseri, 2025-01-22: "The top three signals … are watch time, likes and
  sends"; likes matter slightly more for followers, sends for non-followers
  ([Social Media Today](https://www.socialmediatoday.com/news/instagram-shares-algorithm-insights-2025/738034/)).
  Comments are not in the three.

## Short video

*Physics checked 2026-10-07.* Instagram Reels, YouTube Shorts and TikTok: the
spoken script, the on-screen text and the first frame. Writing the script is
[video-script.md](video-script.md); the hook is [hooks.md](hooks.md); what to
study first is [research-outliers.md](research-outliers.md).

**What each platform has said it rewards**

- **Instagram: watch time, likes and sends**, and sends weigh most for
  non-followers. Build in a reason to forward the reel to one named person
  ([Social Media Today, 2025-01-22](https://www.socialmediatoday.com/news/instagram-shares-algorithm-insights-2025/738034/)).
- **Instagram: Skip Rate replaced View Rate in Reels insights** (2025-08): the
  share of viewers who left in the first three seconds, beside a retention
  chart ([Social Samosa](https://www.socialsamosa.com/news-2/instagram-retention-chart-skip-rate-new-performance-metrics-reels-9730992)).
- **YouTube Shorts: a view counts from the start or a replay** since
  2025-03-31; the old metric is "engaged views". Compare engaged views only,
  never views across that date
  ([Tubefilter](https://www.tubefilter.com/2025/03/26/youtube-shorts-views-counting-stats/)).
- **TikTok publishes no weights.** It names interactions, video information
  and device settings ([TikTok Newsroom](https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you/)).
  "Completion must exceed 70%" and similar figures circulate without a primary
  source; use the account's own data instead.

**Originality**

- **Instagram, 2026-04-30:** accounts that mostly repost others' content
  without material edits lose recommendation eligibility in every format, over
  a rolling 30-day window; the author's own contribution has to be the focus
  ([Digital Music News](https://www.digitalmusicnews.com/2026/05/01/instagram-debuts-more-original-content-protections-for-creators/)).
- **Instagram: another platform's watermark reduces distribution; your own
  logo does not** ([Tubefilter, 2021](https://tubefilter.com/2021/02/10/instagram-reels-with-tiktok-watermark-less-discoverable/);
  [Social Media Today](https://www.socialmediatoday.com/news/instagram-clarifies-that-including-your-own-logo-on-a-reel-is-ok/730852/)).
- **YouTube, 2025-07-15: "inauthentic content"** replaces "repetitious":
  mass-produced, near-identical uploads such as slideshows with the same
  narration. AI is allowed when the work is original and disclosed
  ([Plagiarism Today](https://www.plagiarismtoday.com/2025/07/08/youtube-targets-inauthentic-content/)).

**AI labelling**

- **TikTok, 2025-11-19:** realistic AI-generated content must be labelled;
  C2PA metadata and invisible watermarks are read on upload
  ([TikTok Newsroom](https://newsroom.tiktok.com/more-ways-to-spot-shape-and-understand-ai-content?lang=en)).
  Never strip Content Credentials to avoid a label; it does not remove the
  duty to disclose.
- **Instagram, 2026-08-31:** a fully synthetic persona carries the
  "AI-generated profile" label or loses reach; AI used as a tool needs none
  ([AlternativeTo, retelling](https://alternativeto.net/news/2026/9/instagram-adds-new-ai-generated-profile-label-and-will-demote-users-who-do-not-comply/)).
- **EU AI Act, Article 50, from 2026-08-02:** a deepfake (realistic image,
  audio or video of real people, places or events) is disclosed by whoever
  publishes it ([SRD Rechtsanwälte](https://www.srd-rechtsanwaelte.de/en/blog/deepfake-labelling-under-the-ai-act-what-the-new-eu-guidance-clarifies)).
- **A fictional customer saying "it changed my results" is a fake
  testimonial**, AI or not. Voice real reviews, disclosed
  ([r/AI_UGC_Marketing](https://www.reddit.com/r/AI_UGC_Marketing/comments/1t348ja/),
  practitioner). The legal reading belongs to counsel; the copy rule is that
  no `facts.md` row means no claim.

**Frame, length, pace**

- **Safe zone, 1080×1920:** keep text out of the top ~14%, the bottom ~35%
  and ~6% each side on Reels ads
  ([AdStellar](https://www.adstellar.ai/blog/vertical-video-ad-best-practices));
  for organic reels nothing above y=230, nothing below y=1440, right 230 px
  clear ([`ig-reel/SKILL.md`](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-reel/SKILL.md)).
  TikTok: everything important inside the UI safe zone, 9:16, 720p or more
  ([TikTok creative best practices](https://ads.tiktok.com/help/article/creative-best-practices?lang=en)).
- **Length follows density, not a target.** Reels run to 20 minutes
  ([inro, retelling](https://www.inro.social/blog/instagram-reels-can-now-be-20-minutes-long-new-time-limit-explained-2025))
  and Shorts to 3 minutes since 2024-10-15
  ([PPC Land](https://ppc.land/youtube-expands-shorts-duration-to-3-minutes/));
  a 15–45 second reel is the working range the source above writes for. Short
  enough to be replayed is a strategy: on very short Shorts an average
  percentage viewed above 100% means replays
  ([r/NewTubers](https://www.reddit.com/r/NewTubers/comments/1uf54tv/), practitioner).
- **Change the picture every one to three seconds**; cut dead air longer than
  about half a second, not breathing
  ([TikTok creative best practices](https://ads.tiktok.com/help/article/creative-best-practices?lang=en)
  recommends transitions and text overlays; the interval is practice).
- **The loop:** the last line runs grammatically into the first, or the last
  frame matches the first, so a replay starts without a seam
  ([`ig-reel/beats.py`](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-reel/beats.py)
  flags a reel whose last beat repeats no word of the first).
- **The first three seconds work with the sound off:** on-screen text and the
  picture carry the hook
  ([AdStellar](https://www.adstellar.ai/blog/vertical-video-ad-best-practices)).

**Testing**

- **Trial Reels** show a reel to non-followers only and report after 24 hours;
  publish to the profile or archive it
  ([TechCrunch, 2024-12-10](https://techcrunch.com/2024/12/10/instagram-rolls-out-trial-reels-that-arent-shown-to-a-creators-followers)).
  Re-uploading the same video with a new caption is read as a duplicate by
  practitioners; change the footage
  ([r/InstagramMarketing](https://www.reddit.com/r/InstagramMarketing/comments/1orzr0x/), anecdote).
- **Do not post look-alike reels in a batch:** they compete for the same
  starting sample
  ([r/InstagramMarketing](https://www.reddit.com/r/InstagramMarketing/comments/1wlok7b/), anecdote).
- **Judge a reel against the median of your own last ten, never against a
  universal benchmark**, and never conclude from two
  ([r/NewTubers](https://www.reddit.com/r/NewTubers/comments/1wmal4p/): up to
  30× between two uploads of one channel in a week).

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
- A video ad is a script: the modular hook, body and call to action, the ten
  structures and the hook matrix are in [video-script.md](video-script.md)
  and [hooks.md](hooks.md).

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
