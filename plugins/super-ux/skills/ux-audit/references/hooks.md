# Hooks: the first three seconds of a short video or a video ad

A hook is three things that land at once: the **first frame**, the
**on-screen text** and the **first spoken line**. This file is how to write
them, a library to start from, and the filter `B044` runs over the spoken
line. The script around the hook is [video-script.md](video-script.md); the
platform physics are in [channel-playbooks.md](channel-playbooks.md#short-video).

*Sources read 2026-10-07. Every row names its source; a rule without one is
marked as practice.*

## Contents

- [The mechanics](#the-mechanics)
- [The triple](#the-triple)
- [Taxonomy](#taxonomy)
- [Twenty-six formulas](#twenty-six-formulas)
- [Forty templates](#forty-templates)
- [The filter, B044](#the-filter-b044)
- [Testing hooks](#testing-hooks)
- [Mistakes](#mistakes)
- [Provenance](#provenance)

## The mechanics

| # | Rule | Source |
|---|---|---|
| H1 | **Frame 0 already means something**: movement, a face, the product working, a contrast. Never a logo, a black frame or a greeting | [TikTok creative best practices](https://ads.tiktok.com/help/article/creative-best-practices?lang=en): "Introduce your content proposition in the first 3 seconds"; [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| H2 | **On-screen text by about 0.5 s**: 5–10 words, large, high contrast, inside the safe zone, naming the audience or the topic | [inro](https://www.inro.social/blog/instagram-reels-3-second-hook-leads); [r/NewTubers](https://www.reddit.com/r/NewTubers/comments/1uf54tv/) (practitioner) |
| H3 | **It works muted**: the first three seconds are understood from text and picture alone | [AdStellar on Meta Reels guidance](https://www.adstellar.ai/blog/vertical-video-ad-best-practices) |
| H4 | **Frame, text and line say the same thing**. Two hooks about two things split the attention they were meant to win | [Kallaway, "context lean"](https://youtubesummary.com/summary/LmXpbP7dD48) |
| H5 | **Never open on a testimonial**; earn the attention first | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| H6 | **The hook belongs to the product**. Bait unrelated to the offer buys the wrong viewers and angry comments | [Barry Hott via Alex Cooper](https://alexcooper.beehiiv.com/p/7-facebook-advertising-lessons-i-learned-from-barry-hott): "hook relevance, not just hook rate" |
| H7 | **The body pays the promise**, before the middle of the video. A paid-off hook keeps the viewers it bought | [`ig-reel/hooks.json`](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-reel/hooks.json); [r/NewTubers](https://www.reddit.com/r/NewTubers/comments/1uf54tv/) |
| H8 | **The topic is clear at once**, because platforms now match videos to stated interests | [TechCrunch on "Your Algorithm"](https://techcrunch.com/2025/12/10/instagrams-new-your-algorithm-tool-gives-you-more-control-over-the-reels-you-see) |
| H9 | **Small text and fast cuts with text are unreadable on a phone** | [r/SideProject](https://www.reddit.com/r/SideProject/comments/1wf474o/) (practitioner) |

"Viewers decide in 1.7 seconds" is a 2016 figure about time spent per item in
a mobile feed, not about Reels and not about deciding to stay. Use it as a
metaphor or not at all.

## The triple

Write every hook as three cells, one row per variant:

| Frame 0 (what the eye meets) | On-screen text (≤ 10 words) | First spoken line |
|---|---|---|
| the bank app, scrolled to a forgotten charge | `$400 A MONTH, GONE` | "You lose $400 a month to one subscription you forgot." |

- The on-screen text and the spoken line are **two different sentences about
  one thing**: the text is read in about a second, the line is heard in about
  two. The source this file draws on caps the text at six words; ten is the
  outer bound `B044` enforces.
- A number is said out loud. "A lot" is not a number, and every figure in
  either cell needs its `facts.md` row (`B030` reads the `hook` and
  `on-screen` fields).
- In the document, the triple is front matter: `hook:` (and `hook-2:`,
  `hook-3:` for variants), `on-screen:` (`on-screen-2:` …), with frame 0
  described in the shot list ([video-script.md](video-script.md#shot-list-and-storyboard)).

## Taxonomy

**By channel of perception:** visual (motion, transformation, an odd object),
text (overlay), verbal (the first line), sound (a doorbell, a notification, a
hard stop in the music), or a combination.

**By mechanism:** Motion's library names 33 tactics and maps each to a stage
of awareness: Aspirational, Authority, Belief, Bold Claim, CTA First,
Challenge, Confession, Contrast, Contrarian, Curiosity, Demographic Callout,
Direct Address, Directive, Exclusivity, Explainer, FOMO, How To, If Then,
Listicle, Myth Busting, Offer Only, Price Anchor, Question, Reasons Why,
Relatability, Reverse Psychology, Risk Reversal, Shocking Statement, Social
Proof, Statistic, Storytelling, Urgency, Warning
([Motion hook tactics](https://motionapp.com/library/hooks/tactics/)). Its 2026
benchmark ranks promotional tactics highest by hit rate, inside a window that
overlaps Black Friday, so the promotional lead is inflated
([Motion, top hook tactics](https://motionapp.com/library/research/creative-benchmarks-2026/top-hook-tactics)).

**By structure, for the spoken line (Kallaway):** a *context lean* (one or two
sentences that set the topic and tilt the viewer), a *scroll-stop
interjection* (one sentence turning on "but"), and a *contrarian snapback*
(the unexpected path inside the same topic)
([summary](https://youtubesummary.com/summary/LmXpbP7dD48)).

**A hook is about them; the story is yours.** Specific beats general: "if you
quietly unbutton your jeans at dinner" lands where "if you feel bloated" does
not ([r/SocialMediaMarketing](https://www.reddit.com/r/SocialMediaMarketing/comments/1njfv8a/), practitioner).

## Twenty-six formulas

The set and its names come from `Jakeschincariol/instagram-agent-skill`
(MIT, [`skills/ig-reel/hooks.json`](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-reel/hooks.json)
at `d03c56b`, 2026-09-13). The names are kept so the two can be compared;
every shape, example and trap below is rewritten in this file's own words.
Write formulas HF-01 to HF-26 in the shape shown, then fill the triple.

| id | Formula | Shape | Example (ours) | Best for | Trap |
|---|---|---|---|---|---|
| HF-01 | Cost Confession | the exact sum one mistake cost you | "One unsigned change order cost me $9,000." | fast trust: viewers stay when the author looks bad | a cost that is not money ("it cost me my peace") |
| HF-02 | Negative Command | stop a common habit, do this instead | "Stop batching emails at 9 a.m. Answer twice a day, at fixed times." | saves and arguments | forbidding something nobody does |
| HF-03 | Nobody Tells You | the inconvenient truth about the thing they want | "Nobody tells you your first ten videos are practice." | new audiences; the person saying the awkward thing aloud | a "secret" everyone already says |
| HF-04 | The Replacement | this cheap thing replaced that expensive one | "A $15 timer replaced the coach I paid $300 a month." | tool demos and reviews: the price gap does the work | overstating it; if it replaced half the job, say half |
| HF-05 | Time Collapse | it used to take this long, now this | "Invoices took me a whole evening. Now they take ten minutes." | any process where the win is speed | an unbelievable ratio |
| HF-06 | The Receipt | I did X for N days, here are the real numbers | "I cooked from one list for 30 days. Here is the grocery bill." | experiments shown with the real dashboard on screen | no screen recording: numbers without a screen are a claim |
| HF-07 | Wrong Way, Right Way | you do X wrong and it is not your fault, here is the fix | "You are salting pasta water wrong, and the box told you to." | teaching; "not your fault" removes the insult | dropping the "not your fault" |
| HF-08 | Insider Leak | N years inside, here is what we never said aloud | "Eight years pricing hotel rooms. Here is what the rate calendar hides." | authority without a credentials slide; only if the years are real | promising a secret, delivering a brochure |
| HF-09 | The Steal | take this artifact, it took me this long | "Take this three-line refund email. It took me four years of chargebacks." | saves and sends, the two signals that move reach most | the artifact is not on screen, so there is nothing to screenshot |
| HF-10 | If This, Then Watch | if you are in this exact situation, the next N seconds fix it | "If your plants die every August, the next 30 seconds fix it." | hard filtering: fewer viewers, the right ones | a situation too broad ("if you want to grow") |
| HF-11 | Numbered With A Favourite | N things, number k is the one nobody uses | "Four oven settings. Number three is the one nobody touches." | mid-video retention: the favourite keeps them past item three | N above seven |
| HF-12 | The Objection | the objection word for word, then the version that still works | "'I don't have time to meal prep.' Fine. Here is the ten-minute version." | selling to people who already said no once | an invented objection; take it verbatim from a comment or DM |
| HF-13 | Before And After, On Screen | then, now, and the one lever | "This was my desk in May. This is it now. I moved one shelf." | anything visual: the cut between two frames is the hook | three levers instead of one |
| HF-14 | The Callout | this exact group, here is what you have been avoiding | "Freelance translators under $0.10 a word: this is the rate card you skip." | narrowing to the audience that converts; raises sends | a group too large ("entrepreneurs") |
| HF-15 | The Flop Record | my first N attempts got nothing, here is what changed on N+1 | "My first 40 loaves were bricks. Loaf 41 rose. One thing changed." | beginners, the bulk of any audience; many comments | the change sounds like luck |
| HF-16 | The Verbatim Question | a question you are asked every week, in the asker's words | "'How do you stay consistent without hating it?' I get this every week." | search: platforms match the phrasing people type | a tidied-up question |
| HF-17 | Head To Head | A against B, I ran both, it was not close | "Paper planner versus app. I used both for 90 days and it was not close." | comments: people arrive with an opinion | refusing to name the winner |
| HF-18 | Cold Open Demo | start mid-action: watch what this does | "Watch what happens when I paste last year's budget into this." | screen recordings and anything with a visible result | the result arrives after ten seconds |
| HF-19 | The Deadline | X changes on a date, do Y before it | "Your free storage tier changes on the 1st. Export these two folders first." | real urgency: platform changes, seasonal windows | an invented deadline, which devalues every later one |
| HF-20 | Permission | you do not need the thing everyone says you need | "You do not need a home gym. You need one pull-up bar and a door." | relief; high saves | removing a barrier and putting nothing in its place |
| HF-21 | Mid-Sentence Start | open in the middle of the story's turn | "…and that is when the landlord asked for the keys back. Two days after signing." | stories: the viewer feels late and stays | no back-story by second eight |
| HF-22 | Contrarian Flip | a well-known saying, reversed | "Practice does not make perfect." | comments: the viewer argues with themselves | reversing a saying nobody uses |
| HF-23 | The Statistic | N% of a group do something surprising | "{N}% of {group} never {surprising act}." with the figure from `facts.md` | sends: a number people repeat at dinner | a statistic with no source |
| HF-24 | The Reveal | this is the new X | "This is the new pocket printer, and it fixes the one thing I hated." | physical and visual products: the object is the hook | showing the thing without saying what it changes |
| HF-25 | Someone Else's Result | one person got this result in this time | "One baker sold out a market stall in her first month. Here is her sign." | proof before you have your own number; third person is fine when true | no name and no link make it a rumour |
| HF-26 | The Superlative | the fastest, biggest or only way to X is Y | "The fastest way to learn a recipe is to cook it badly twice." | a one-claim video with no story; the most common shape, the easiest to ruin | a soft answer ("consistency") |

**Matching a hook someone else wrote** to a formula is how
[research-outliers.md](research-outliers.md) turns a swipe file into a pattern:
classify from the most specific formula to the least, and read the hooks that
match none by hand, because that is where a formula this table lacks hides.

## Forty templates

Collected in this family's short-video research of 2026-10-07. `[X]` is the slot.
Each row names the source of its mechanism; where the row is a practitioner's
anecdote it says so.

| id | Template | Example | Mechanism | Source |
|---|---|---|---|---|
| HT-01 | [Result] in [surprisingly short time] | "Three years of back training in 30 seconds" | timeframe tension | [r/SocialMediaMarketing](https://www.reddit.com/r/SocialMediaMarketing/comments/1njfv8a/) (practitioner) |
| HT-02 | How I [result] without [expected sacrifice] | "How I got to B2 Spanish without an app" | how-to, result first | [Motion tactics: How To](https://motionapp.com/library/hooks/tactics/) |
| HT-03 | The finished result as frame 0, then "here is how" | the finished cake on screen: "Fifteen minutes, here is how" | visual result first | [Motion visual formats: Demo](https://motionapp.com/library/research/creative-benchmarks-2026/top-visual-formats) |
| HT-04 | Before and after in the first two seconds | split screen | before & after | [Motion visual formats](https://motionapp.com/library/research/creative-benchmarks-2026/top-visual-formats) |
| HT-05 | The figure as proof | "We spent [sourced sum] to learn one thing about AI ads" | statistic | [Motion tactics: Statistic](https://motionapp.com/library/hooks/tactics/) |
| HT-06 | A screenshot as evidence | opens on the client's message or the dashboard | social proof without a testimonial | [Motion tactics: Social Proof](https://motionapp.com/library/hooks/tactics/) |
| HT-07 | You are doing [X] wrong | "You brew coffee wrong, and it is not the beans" | curiosity gap | [inro](https://www.inro.social/blog/instagram-reels-3-second-hook-leads) |
| HT-08 | Nobody talks about [X] | "Nobody mentions what the free tier deletes" | insider | [`hooks.json`, Nobody Tells You](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-reel/hooks.json) |
| HT-09 | I am not supposed to tell you this, but | "A recruiter friend told me what they actually read" | insider secret | [r/SocialMediaMarketing](https://www.reddit.com/r/SocialMediaMarketing/comments/1npf3sz/) (practitioner) |
| HT-10 | Context, then "but", then the turn | "The stadium screen is huge. But the screen is the least impressive part." | context lean, interjection, snapback | [Kallaway](https://youtubesummary.com/summary/LmXpbP7dD48) |
| HT-11 | An unfinished action | someone starts something risky; the result is at the end | curiosity, payoff deferred | [Motion tactics: Curiosity](https://motionapp.com/library/hooks/tactics/) |
| HT-12 | I tested [X] for [time], here is what happened | "I used only the bus for a month" | experiment | [`hooks.json`, The Receipt](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-reel/hooks.json) |
| HT-13 | A question the viewer cannot answer | "Why are aeroplane windows round?" | question | [Motion tactics: Question](https://motionapp.com/library/hooks/tactics/) |
| HT-14 | Stop [popular advice] | "Stop posting every day" | contrarian | [r/NewTubers](https://www.reddit.com/r/NewTubers/comments/1tzjhv0/) (practitioner) |
| HT-15 | [Common belief] is a myth | "Eight glasses a day is a myth" | myth busting | [Motion tactics: Myth Busting](https://motionapp.com/library/hooks/tactics/) |
| HT-16 | Before you [act], watch this | "Before you buy a robot vacuum, watch this" | warning | [Motion tactics: Warning](https://motionapp.com/library/hooks/tactics/) |
| HT-17 | The worst advice I got about [X] | "The worst advice I got about rent" | contrarian story | [Motion tactics: Contrarian](https://motionapp.com/library/hooks/tactics/) |
| HT-18 | Do not buy this if [you enjoy the problem] | "Do not buy this if you like an hour of ironing" | reverse psychology | [Motion tactics: Reverse Psychology](https://motionapp.com/library/hooks/tactics/) |
| HT-19 | [Group], this is for you | "Renters, this one is for you" | demographic callout | [inro](https://www.inro.social/blog/instagram-reels-3-second-hook-leads) |
| HT-20 | If you [hyper-specific situation], this is for you | "If you reheat the same coffee three times" | specificity | [r/SocialMediaMarketing](https://www.reddit.com/r/SocialMediaMarketing/comments/1njfv8a/) (practitioner) |
| HT-21 | POV: [the moment] | "POV: you finally stop overpaying at festivals" | point of view as advice | [r/SocialMediaMarketing](https://www.reddit.com/r/SocialMediaMarketing/comments/1njfv8a/) (practitioner) |
| HT-22 | The older I get, the more I realise | "The older I get, the less I buy" | story time | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-23 | A confession | "I ran this channel wrong for three years" | confession | [Motion, top hook tactics](https://motionapp.com/library/research/creative-benchmarks-2026/top-hook-tactics) |
| HT-24 | The anti-hook | "A long, boring video that will save you money" | anti-hook | [r/SocialMediaMarketing](https://www.reddit.com/r/SocialMediaMarketing/comments/1npf3sz/) (practitioner) |
| HT-25 | Three reasons why [X] | "Three reasons everyone should start running" | listicle | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-26 | [N] things I would do if I started again | "Five things I would do if I opened the café again" | listicle | [Motion tactics: Listicle](https://motionapp.com/library/hooks/tactics/) |
| HT-27 | The number one mistake [audience] make | "The first mistake new landlords make" | warning | [Motion tactics: Warning](https://motionapp.com/library/hooks/tactics/) |
| HT-28 | "Wait, what is this?" | the creator finds the product somewhere unexpected | pattern interrupt | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-29 | Self-skit | one person plays two characters | pattern interrupt | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-30 | Spin the bottle | a bottle spins among options and stops on the product | pattern interrupt | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-31 | Mission: find the perfect [X] | a magnifier effect searches the frame | pattern interrupt | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-32 | Everything in moderation, except | "…except coffee", the product snatched by the edit | pattern interrupt | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-33 | Animated text as the frame | one huge line or a handwritten note | text-led stopper | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-34 | The instant outfit change | a clap or a swipe changes the look | transformation | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-35 | The chat | "[Brand] entered the chat" | familiar interface | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-36 | The doorbell | the bell rings, the parcel is here | sound hook | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-37 | Car chat | a conversation in the car | native setting | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-38 | Swiping the variants | a hand flicks through options and lands on one | choice | [Savannah Sanchez via Motion](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/) |
| HT-39 | Offer first | frame 0 is the offer, the price or "new" | offer only | [Motion visual formats: Offer-First Banner](https://motionapp.com/library/research/creative-benchmarks-2026/top-visual-formats) |
| HT-40 | Price anchor | "It costs what one coffee a week does" | price anchor | [Motion tactics: Price Anchor](https://motionapp.com/library/hooks/tactics/) |

For organic posts, "send this to the friend who…" is not a hook but a line
the script carries, aimed at the sends signal
([channel-playbooks.md](channel-playbooks.md#short-video)).

## The filter, B044

`brand_lint.py` scores every `hook` field (and `hook-2`, `hook-3` …) on five
checks, each 0–100:

| Check | Full marks when | Low when |
|---|---|---|
| LENGTH | 5–12 words, 60 characters or fewer (about two seconds spoken) | under 5 or over 12 words, or two lines of on-screen text |
| SPECIFICITY | a figure, a name or a spoken number | nothing checkable |
| STAKES | two or more words that put something on the line (lose, wrong, never, cost, instead…), or a price | nothing at stake |
| FRONTLOAD | the payload word sits in the first four | a weak opener (so, hey, today, "in this…") or the payload is late |
| ADDRESS | it speaks to "you" | third person, nobody in the room |

**Score = 0.6 × mean + 0.4 × minimum − 15 per dealbreaker**, clamped to
0–100: the weakest property caps the hook, because one bad property is enough
for the thumb to keep moving. STRONG is 70 or more with no check under 55 and
no dealbreaker; WEAK is under 50. `B044` warns on WEAK, on any dealbreaker,
and on on-screen text over ten words.

**Five dealbreakers:** opening with "stop scrolling" or "don't scroll"; a
video preamble ("in this video", "I'll show you how"); a greeting first; a
hashtag in the hook; an emoji in the hook.

**It is a filter, not a predictor.** On its author's corpus of 74 real
short-form hooks the method separates written-to-be-bad hooks from real ones
well, **AUC 0.83**, and separates a creator's hits from the same creator's
misses barely at all, **AUC 0.56**, where 0.50 is a coin. Use it to throw out
the weak, never to choose between two decent hooks: that is decided by the
face, the edit, the sound and who the platform shows it to, and the retention
graph is the judge. The corpus and its measurement script are not published,
so the two figures are the author's and cannot be reproduced here
([`hookscore.py`](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-reel/hookscore.py),
docstring).

**The vocabulary is English.** A hook in Cyrillic or another non-Latin script
is not scored; only the hashtag and emoji dealbreakers, which do not depend on
the language, apply to it. A Russian hook is judged by reading it aloud and
by the mechanics above, not by a number calibrated on English.

## Testing hooks

- **Ads, a modular matrix:** one body, three to five hooks (frame, text and
  line changed together), ranked by how wide a gap each opens
  ([r/PPC](https://www.reddit.com/r/PPC/comments/1sc1mg7/), practitioner;
  [Segwise](https://segwise.ai/blog/creative-brief-template-performance-creative)).
- **After Meta's Andromeda retrieval engine, hooks alone are not enough:**
  test different concepts (persona × desire × awareness), not one concept
  with new first seconds
  ([r/FacebookAds](https://www.reddit.com/r/FacebookAds/comments/1ng8ves/), practitioner;
  [Meta Engineering](https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/)
  on what Andromeda is). Meta has not confirmed that near-identical ads are
  merged into one; varying at least two dimensions is cheap insurance either way.
- **Write the formula beside every number.** Hook rate is 3-second views ÷
  impressions; hold rate is 15-second plays ÷ 3-second plays in Motion's
  definition and ThruPlays ÷ impressions in others'
  ([Motion metrics](https://motionapp.com/blog/key-creative-performance-metrics)).
- **Organic:** a Trial Reel on non-followers; one video with different hooks
  on different platforms, the winner re-uploaded a week later
  ([r/DigitalMarketing](https://www.reddit.com/r/DigitalMarketing/comments/1otb0l7/), practitioner).
- **Against your own median**, of the last five to ten, never two videos
  ([channel-playbooks.md](channel-playbooks.md#short-video)).

## Mistakes

1. A logo, an intro or "hi everyone" in the first two seconds (H1).
2. Bait unrelated to the product (H6).
3. Optimising hook rate instead of the right viewer: a winning ad can have a
   low hook rate if it attracts the right audience
   ([Barry Hott](https://alexcooper.beehiiv.com/p/7-facebook-advertising-lessons-i-learned-from-barry-hott)).
4. A slow warm-up "so it is not cringe" (H1).
5. Text and line about different things (H4).
6. Small or fast text (H9).
7. "Testing a hook" by changing the background colour.
8. A testimonial with no hook (H5).
9. A promise the body does not pay (H7).
10. A claim nobody can source. No `facts.md` row, no claim, and an ad is the
    worst place to make one.

## Provenance

| What | From | Licence | How used |
|---|---|---|---|
| The 26 formula names, the five checks, the arithmetic, the dealbreakers, the AUC figures | [`Jakeschincariol/instagram-agent-skill`](https://github.com/Jakeschincariol/instagram-agent-skill) @ `d03c56bb598be770c60b201f94237e5d1a4268a6` | MIT, © 2026 Jake Schincariol | names kept for comparison; shapes, examples, traps and the linter's vocabulary rewritten, no text reproduced |
| Mechanics H1–H9, the 40 templates, testing and mistakes | the sources named in each row, read 2026-10-07 | per source | paraphrased with attribution |
