# Reading a funnel market before designing one

The method for the step that comes before `foundation.md` on a paid-acquisition
product: finding the funnels already running in your category, reading which of
them are working, and turning a pile of them into two lists you can design
against. Seven steps, `FR-01`..`FR-07`, each with an output that lands somewhere
in the chain. Practices: BP-116..123 design the surfaces, BP-124..129 the
web2app chain, BP-211..215 the wiring underneath.

**The premise, and the whole reason this is a method rather than a browse:** you
cannot see anyone's revenue. Not in an ad library, not in a review site, not
anywhere. A product can be making millions with nothing on its funnel that says
so. Every signal below is a proxy for spend, and spend is a proxy for return
made by someone whose judgement you cannot inspect. The output is a **shape to
start from**, never a template, and BP-001 is the discipline that keeps it that
way.

## Contents

- [FR-01 — Collect the funnels](#fr-01--collect-the-funnels)
- [FR-02 — Read the four signals that survive without revenue](#fr-02--read-the-four-signals-that-survive-without-revenue)
- [FR-03 — Record the same fields for every funnel](#fr-03--record-the-same-fields-for-every-funnel)
- [FR-04 — Turn the corpus into two lists](#fr-04--turn-the-corpus-into-two-lists)
- [FR-05 — Look one niche over](#fr-05--look-one-niche-over)
- [FR-06 — Stop before copying](#fr-06--stop-before-copying)
- [FR-07 — Land the findings where the chain reads them](#fr-07--land-the-findings-where-the-chain-reads-them)
- [The shape the corpus keeps producing](#the-shape-the-corpus-keeps-producing)
- [What this method cannot do](#what-this-method-cannot-do)

## FR-01 — Collect the funnels

A funnel is a public surface behind a public ad, so the collection problem is
solved by whoever is required to publish the ads.

| Where | What it gives you, and its catch |
|---|---|
| **Platform ad libraries** (Meta Ad Library, TikTok Creative Center) | The live funnel: open a competitor's ad, click through, and you are in it at step one. TikTok's is the more useful of the two because it filters by geography and industry and sorts by reach over the last 7 and 30 days, which is FR-02's second signal already computed. The catch is coverage: only the platforms with a disclosure obligation, only currently-running ads |
| **Review sites** (Trustpilot and its regional equivalents) | A traffic proxy nobody thinks to use. Reviews accumulate with volume, so sorting a category by review count ranks by rough traffic, and the "similar companies" block is a ready-made list of the niche. The catch is that it ranks by *accumulated* traffic, so it favours age over momentum. FR-02's third signal is the correction |
| **Your own recommender** | Click through several funnels in one category and the feed starts serving more of them. Cheap, and it finds the ads that are being *shown*, which no library ranks by. The catch is that it is a sample of one profile |
| **Paid ad-intelligence tools** | Volume and history, for money. Worth it when the corpus needs to be large enough to count frequencies rather than read examples |

**Output:** a list of live funnel URLs with the ad that led to each. Keep the ad,
because BP-116 is checked against it and cannot be checked without it.

**Who does the clicking, and where that stops.** The walk is mechanical until it
is not, so the method names the split rather than leaving it to whoever reads it.
A browser tool — `chrome-devtools` or `claude-in-chrome`, whichever the session
has — does the part that is mechanical: open the ad's destination, follow the
redirect chain, and capture four things per funnel, because they are the ones a
screenshot loses.

| Capture | Why it, and not a screenshot |
|---|---|
| the **final URL after redirects** | the ad points at a tracker; the funnel is what it lands on, and the two are rarely the same domain |
| **every step's URL**, in order | FR-03 records step counts, and a step you did not see is a step you cannot count |
| the **network requests on the paywall step** | which processor and which price ids — this is the one place the funnel states its own price without a human reading it |
| the **ad that led there** | the output line above; a capture without it fails BP-116's check |

**A human takes over at three points, and they are not incidental.** Consent
walls and cookie banners vary by geography and are the first thing an automated
walk gets stuck in. **Sign-in and paywall steps** are where the funnel gets
interesting and where a tool cannot proceed without real credentials or a real
card — do not automate past them, and do not create accounts to see further;
FR-06 is the rule that ends this method before it becomes competitor copying.
And **ad libraries rate-limit and detect automation**: Meta's in particular will
serve a challenge to a driven browser, so the library browsing itself is a human
step and only the click-through is automated.

So the split is: **the library is read by a person, the funnel is walked by a
tool, and the walk stops at the first wall that asks who you are.** Silence here
used to read as *nobody thought about it*, which is worse than either answer.

## FR-02 — Read the four signals that survive without revenue

None of these measures return. All four measure **investment**, which is a
decision made by someone with access to the numbers you do not have. That is the
strongest inference available and it is still an inference.

| Signal | Read | Why it carries information |
|---|---|---|
| **How long the ad has been running** | Libraries publish the launch date | Nobody keeps paying to run an ad at a loss for months. Longevity is the cheapest signal and the hardest to fake |
| **How many creatives are in rotation on one offer** | Count the variants pointing at the same funnel | Variant count is production spend, and production spend follows return. A dozen creatives on one offer is a team that has decided this funnel earns |
| **How fast reviews are growing** | The rate, never the count | Count is mostly age. Rate is current traffic, which is what you want and what the sort in FR-01 gets wrong |
| **Recurrence across independent players** | The same move in several unrelated funnels | Once is taste, three times is a pattern. This is the only one of the four that is about the *mechanic* rather than the advertiser |

**The shared failure mode:** a well-funded funnel that is losing money looks
identical to a profitable one on all four signals, for as long as the budget
lasts. Treat a single funnel's evidence as weak and the recurrence signal as the
only strong one.

**Output:** each funnel in the list marked kept or dropped, with which signals
it showed. A funnel kept on no signal is a funnel you liked the look of, and
that is worth writing down as such rather than laundering into evidence.

## FR-03 — Record the same fields for every funnel

The corpus is only comparable if every entry answers the same questions. Improvise
the fields per funnel and you end up with a folder of screenshots and no way to
count anything.

| Field | Note when recording | Practice it feeds |
|---|---|---|
| Quiz: number of steps, what each asks | Separate the questions that shape the offer from the ones that only build commitment | BP-002, BP-143 |
| What the offer repeats back | The exact words, not a summary of them | BP-010, BP-211 |
| Tier count, and which is highlighted | And what the highlight is made of: a badge, a size, a colour, a saving | BP-118, BP-022 |
| Price anchor unit | Per day, per week, per month, per year, and whether the billed amount appears beside it | BP-118 |
| Trial: length, and whether a card is required | These are two different products, not one field | BP-070 |
| Upsell: position and offer | Before checkout, after it, or on the success screen | BP-017, BP-028 |
| What the paywall claims, and what backs the claim | Note the claims with no proof separately: they are the cheapest thing to beat | BP-190 |
| How access arrives after payment | Which rung of the ladder, and whether you can tell from outside | BP-215 |

**Output:** one row per funnel, one column per field. This table is the corpus.

## FR-04 — Turn the corpus into two lists

Count frequencies across the table and split the result:

- **What almost everyone does** is the proven base. Start from it, because the
  cost of discovering it independently has already been paid by the category.
- **What almost nobody does** is open space, and the corpus **cannot tell you
  which kind**. An untried idea and an idea the category tried and abandoned look
  exactly the same from here. Before spending on one, look for the reason: a
  platform rule, a payment constraint, a support cost, an audience that punished
  it.

Summarizing a large corpus with a model is a reasonable use of one for the
frequency count, which is arithmetic. The judgement about *why* a gap exists is
not arithmetic and does not survive being delegated.

**Output:** two lists, and for every item on the second one, a sentence on which
kind of empty it is.

## FR-05 — Look one niche over

Mechanics transfer between categories that share a **buyer state**, not a topic.
A funnel selling a plan to someone anxious about a deadline works on the same
mechanics whether the deadline is a race, an exam or a visa. Categories that run
this shape hard, and are therefore worth reading even when they look unrelated to
yours: self-improvement and habit products, health and body scanners, astrology
and personality tests, language learning, personal finance.

The transfer that works is the mechanic with its mechanism attached. The transfer
that fails is the surface: the same three-tier layout in a category whose buyers
compare on one axis is a layout, not a strategy.

**Output:** the mechanics worth trying, each with the buyer state it depends on,
so the claim can be checked against your own foundation rather than assumed.

## FR-06 — Stop before copying

What you can see from outside is the structure and the prices. What you cannot
see is everything that made them work: which pricing test landed on that number,
which audience the copy was tuned against, what the retention behind that trial
length looks like, how much of the conversion is the funnel and how much is the
brand that ran the ad. A funnel copied whole inherits the visible half and none
of the reasons.

BP-001 states the discipline: name the mechanism before reusing the move, check
it against this product's value and audience, then test an adapted version.
Applied here, it means the corpus produces **candidates with mechanisms
attached**, and a candidate whose mechanism you cannot name did not survive the
step.

## FR-07 — Land the findings where the chain reads them

A market read that becomes its own document is a document nothing reads. Each
finding has a home that already exists:

| Finding | Home |
|---|---|
| Who the buyer is, what job they are hiring the product for | `docs/ux/foundation.md` — personas, JTBD |
| The funnel's step chain and its branches | `docs/ux/flows.md` |
| Each screen, its states and its elements | `docs/ux/screens.md` |
| The behaviour of every step, including the skipped-answer branch | `docs/ux/scenarios.md` |
| Which practices were considered and what was decided | The compliance table, `practice-selection.md` step 4 |
| Any figure quoted from a competitor | `docs/brand/facts.md`, with its source, or it is not quoted |

The corpus table itself is working material. Keep it if it is useful, and do not
promote it to a source of truth: it describes other people's products, and it is
stale the week after it is built.

## The shape the corpus keeps producing

Ad → landing → quiz → loading → offer → paywall → checkout → success. It recurs
because each step does one job the next one needs, which is also why it is a
starting point rather than a rule.

| Step | Its job | Where it is specified |
|---|---|---|
| Landing | Pick up the ad's exact promise and move the visitor into the quiz | BP-116, BP-117 |
| Quiz | Build commitment, and collect the few answers the offer repeats | BP-002, BP-143, BP-211 |
| Loading | A calculated pause that makes the result feel computed for this person | BP-005 |
| Offer | The answers come back as a plan, wording branched, price not | BP-010, BP-211 |
| Paywall | Tiers, what is included, the trial, the anchor unit | BP-118, BP-022, BP-070 |
| Checkout | The smallest identity that unblocks the purchase, total visible before the last step | BP-119, BP-120 |
| Success | Confirmation, and the handoff into the product | BP-125, BP-215 |

Every one of those steps is a screen in `screens.md` and a scenario in
`scenarios.md`, including the loading screen and including the branch where the
quiz answer is missing. A step that exists in the build and not in the record is
the drift the chain exists to prevent.

## What this method cannot do

Stated so the output is not read as more than it is.

- **It cannot rank funnels by profit.** Every signal is spend. A competitor
  burning a raise looks like a competitor with a working funnel.
- **It cannot see the tests behind a number.** A price is a result; the
  experiment that produced it is not published.
- **It cannot see anything behind the paywall.** Retention, refund rate, dunning
  recovery and support load are the numbers that decide whether the funnel was
  worth running, and none of them is visible from the funnel.
- **It goes stale.** Live ads rotate, prices move, and the corpus describes the
  week it was built. Date it.
- **It is not a substitute for the foundation.** A market read tells you what the
  category does. It does not tell you who your buyer is, and a funnel designed
  from the corpus alone is aimed at a competitor's audience.
