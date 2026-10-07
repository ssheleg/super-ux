# Outliers: what to study before writing a short video

Raw views are not evidence. 400,000 views on an account with two million
followers is a quiet Tuesday; the same 400,000 on an account with 4,000 is a
find worth repeating. This file is the method for telling the two apart, so
the hooks in [hooks.md](hooks.md) and the scripts in
[video-script.md](video-script.md) start from what beat its own account, not
from what was merely big.

*Method from `Jakeschincariol/instagram-agent-skill` (MIT,
[`skills/ig-viral/SKILL.md`](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-viral/SKILL.md)
and [`swipe.py`](https://github.com/Jakeschincariol/instagram-agent-skill/blob/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-viral/swipe.py)
at `d03c56b`), rewritten here; read 2026-10-07.*

## Contents

- [The multiple](#the-multiple)
- [The sample](#the-sample)
- [What to record per video](#what-to-record-per-video)
- [Worked example](#worked-example)
- [Reading the sample](#reading-the-sample)
- [Collecting without breaking anything](#collecting-without-breaking-anything)

## The multiple

**multiple = the video's views ÷ the account's median views**

- The median is taken over the account's recent videos (about its last
  twelve). With no median to hand, use the follower count and **say which
  base was used**, because the two give different multiples.
- **3× or more is a signal**: the video beat its own account, and something
  in it is repeatable.
- **Under 1.5× is noise**: an ordinary day for that account, which teaches
  nothing.
- Between the two, keep the row and do not build on it alone.
- On YouTube Shorts compare **engaged views** only: since 2025-03-31 a view
  counts from the first frame or a replay, so views either side of that date
  do not compare
  ([Tubefilter](https://www.tubefilter.com/2025/03/26/youtube-shorts-views-counting-stats/)).

## The sample

- **Six to twelve accounts within about 10× of your own size**, either way:
  about four direct competitors slightly ahead of you, about four adjacent
  accounts (another niche, the same audience; formats arrive there first),
  and two to four large accounts studied for format only, never for
  multiples.
- **Your own saved collection** counts: the fastest corpus there is, already
  filtered by your taste.
- **Twelve videos show nothing; forty across six accounts start to show
  something.** State the sample size and the confidence in words beside every
  conclusion.

## What to record per video

One row per video: account, followers, the account's median views, the
video's views, the multiple, the hook **verbatim** (the first spoken line,
errors included), the on-screen text, the length, the ask. The hook and the
views are the two columns a row cannot lack.

## Worked example

Your account: 5,000 followers, so the sample runs from 500 to 50,000.

| Video | Account | Followers | Median views | Views | Multiple | Reading |
|---|---|---|---|---|---|---|
| V1 | @kitchen-a | 8,000 | 2,000 | 9,400 | 4.7 | signal |
| V2 | @kitchen-a | 8,000 | 2,000 | 2,600 | 1.3 | noise |
| V3 | @budget-b | 31,000 | 12,000 | 41,000 | 3.4 | signal |
| V4 | @budget-b | 31,000 | 12,000 | 22,000 | 1.8 | between |
| V5 | @mealprep-c | 1,900 | 600 | 4,100 | 6.8 | signal |
| V6 | @celebrity-d | 2,000,000 | 380,000 | 400,000 | 1.1 | outside the sample |

- **V5 is the strongest find** at 6.8×, on the smallest account in the
  sample, with the fewest raw views but one.
- **V6 has the most views and teaches the least**: 1.1× is an ordinary day,
  and the account is 400× your size, so it would be studied for format only.
- **V1 and V2 are one account**: the same audience and the same face, so the
  difference between them (4.7× against 1.3×) is mostly the video. Compare
  their hooks first.
- Six rows from three accounts is far under forty: this is an illustration of
  the arithmetic, not a finding.

`test/validate.py` recomputes every multiple and every reading in this table
from its Views, Median views and Followers columns, so the example cannot
drift from the rule it illustrates.

## Reading the sample

1. Sort by multiple. Split into top and bottom thirds.
2. Classify each hook by formula ([hooks.md](hooks.md#twenty-six-formulas)),
   from the most specific formula to the least. Note which formulas are
   over-represented in the top third.
3. Compare the median hook length in words, top against bottom.
4. **Read the unclassified hooks by hand.** That is where a pattern the
   library does not have yet is hiding.
5. Rewrite the three strongest formulas as **your** version: your case, your
   number from `facts.md`. Copy the formula, never the video.

The same multiple works on your own account afterwards: rank your published
videos by multiple and by sends per reach, not by views
([channel-playbooks.md](channel-playbooks.md#short-video)). Views without
follows is a profile problem; no views is a hook problem.

## Collecting without breaking anything

- **Read, do not scrape.** A browser at a human pace, a dozen videos from
  each of ten accounts. No crawlers, no scraping services.
- **Never sign in as the user and never ask for a password.** The platform's
  terms govern automated access, and an account lost to a ban costs more
  than any sample.
- **Attribute every row** to the account it came from; a swipe file is a
  record of other people's work.
- A public fallback corpus is YouTube Shorts metadata and auto-captions,
  where the platform's terms allow it.
