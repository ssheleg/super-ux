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
so. Every signal below is OBSERVED EXPOSURE — a proxy for spend — and any claim
that spend proves RETURN is a HYPOTHESIS with alternative explanations (a
funded launch burning runway, a vanity spend, a strategic loss-leader), not a
measurement. The output is a **shape to start from**, never a template or a
proven result, and BP-001 is the discipline that keeps it that way.

## Contents

- [FR-01 — Collect the funnels](#fr-01--collect-the-funnels)
- [FR-02 — Read the four signals that survive without revenue](#fr-02--read-the-four-signals-that-survive-without-revenue)
- [FR-03 — Record the same fields for every funnel](#fr-03--record-the-same-fields-for-every-funnel)
- [FR-04 — Turn the corpus into two lists](#fr-04--turn-the-corpus-into-two-lists)
- [FR-05 — Look one niche over](#fr-05--look-one-niche-over)
- [FR-06 — Stop before copying](#fr-06--stop-before-copying)
- [FR-07 — Land the findings where the chain reads them](#fr-07--land-the-findings-where-the-chain-reads-them)
- [The shape the corpus keeps producing](#the-shape-the-corpus-keeps-producing)
- [Your own numbers: subscription economics and cohorts](#your-own-numbers-subscription-economics-and-cohorts)
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
A browser tool does the part that is mechanical — WebKit first
([browser-engine.md](browser-engine.md)): Playwright's `webkit`, which logs the
redirect chain and the network requests, or Safari through `safaridriver`; a
Chrome tool (`chrome-devtools`, `claude-in-chrome`) only as a stated fallback
when the session has no WebKit route: open the ad's destination, follow the
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
| **How long the ad has been running** | Libraries publish the launch date | Longevity is OBSERVED EXPOSURE — a well-funded advertiser can run a loss-making ad for months, so read it as "someone is spending here", the cheapest and hardest-to-fake signal of THAT, never as proof the funnel earns |
| **How many creatives are in rotation on one offer** | Count the variants pointing at the same funnel | Variant count is production SPEND — observed exposure, not observed return. "Production spend follows return" is a HYPOTHESIS with alternatives (a funded launch, a vanity bet, a mandate); a dozen creatives says a team is spending here, not that the funnel earns |
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

- **What almost everyone does** is a FREQUENT PATTERN, not a proven conversion
  lift. Frequency across a corpus is observed exposure repeated; it is a shape
  worth starting from because the category has already spent to discover it —
  but "frequent" is not "proven", and adoption is decided by a LOCAL experiment
  on your own funnel, never asserted from the count. The frequency is computed
  by a script over the corpus with an explicit DENOMINATOR, and DUPLICATES are
  collapsed first: two funnels owned by the SAME company are one observation,
  not two, and a single known loss-making-but-funded advertiser does not move
  the pattern.
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
| Loading | Only where REAL asynchronous work exists: show the actual operation, never delay a ready result. A product that wants a narrative pause names it honestly — no claim of personal analysis that is not happening — and measures its cost | BP-005 |
| Offer | The answers come back as a plan, wording branched, price not | BP-010, BP-211 |
| Paywall | Tiers, what is included, the trial, the anchor unit | BP-118, BP-022, BP-070 |
| Checkout | The smallest identity that unblocks the purchase, total visible before the last step | BP-119, BP-120 |
| Success | Confirmation, and the handoff into the product | BP-125, BP-215 |

Every one of those steps is a screen in `screens.md` and a scenario in
`scenarios.md`, including the loading screen — where one legitimately exists —
and including the branch where the quiz answer is missing; that branch shows
its honest empty state, never a staged personalization over answers nobody
gave. An instant local result renders without a timer. A step that exists in
the build and not in the record is the drift the chain exists to prevent.

## Your own numbers: subscription economics and cohorts

Everything above reads other people's funnels, and the last section below says
what that cannot see: retention, renewals and payback sit behind the paywall.
Once your own funnel runs, those are the numbers that decide whether it was
worth running. This section names them, the band an investor reads each one
against, and the two cuts that keep an average from lying. The source is GP
Bullhound's *Consumer Subscription Software* (October 2025), cited by page as
`[GPB25 p. N]`; the practice catalog (`best-practices.md`) carries the
screen-level decisions from the same report, BP-242..245.

**Read the bands as investor expectations, not laws.** They come from an
advisory firm's view of what separates good subscription businesses from great
ones, the report itself notes that the organic share depends heavily on
company size [GPB25 p. 65], and your own trend overrules them the moment you have one.

### The unit economics, and the band each is read against

| Metric | How it is computed | Weak | Strong |
|---|---|---|---|
| LTV/CAC | lifetime value divided by acquisition cost | under 3x | 6x [GPB25 p. 65] |
| CAC payback | CAC ÷ (ARPU × gross margin), in months [GPB25 p. 67] | | under 3 months, "critical to counter the high churn of initial users" [GPB25 p. 66] |
| First-period annual retention | the share of a sign-up cohort still paying after its first pay period, typically month 3, 6 or 12 [GPB25 p. 66] | under 30% | over 60% [GPB25 p. 65] |
| Annual cohort renewal | the share of each annual cohort that renews | | exceptional businesses "renew 60%+ of each annual cohort and 40% of Year 2" [GPB25 p. 66] |
| Free-to-paid conversion | users who start free and become paying, over users who started free | under 2% | 10%+ [GPB25 p. 65] |
| Organic share of acquisition | users from organic channels over all new users | under 20% | over 50% [GPB25 p. 65]; "50%+ ... is generally considered great" [GPB25 p. 66] |

The formulas the report uses [GPB25 p. 67]: **LTV** = ARPU × gross margin ÷
churn rate (equivalently, the average customer's lifetime in months or years ×
ARPU × gross margin [GPB25 p. 66]); **CAC** = sales and marketing spend ÷ new
customers, counting users from free and paid channels alike; **gross churn** =
customers lost in the period ÷ customers at its start; **net churn** = (customers
lost minus customers gained, including reactivated ones) ÷ customers at its start.

**Why first-period retention is the gate.** Subscription products typically lose
between 20% and 70% of first-time sign-ups after the first pay or trial period
[GPB25 p. 66]. Retention after that period is the evidence that users found the
value, and it is why CAC payback has to be short: a cohort that loses most of
itself at the first renewal must have paid back before it.

**Output:** each metric measured on your own cohorts, dated, with the band
beside it. A metric under its weak bound is the first problem to work on,
whatever the funnel looks like. A figure you publish goes through
`docs/brand/facts.md` like any other.

### Four cohort states, and two kinds of user

**Four states.** Track retention separately for **new**, **current**,
**reactivated** and **resurrected** users, the cohort model one large freemium
platform adopted from earlier consumer-app practice and runs beside free-to-trial,
trial-to-paid, renewal and ARPU as one full-funnel view [GPB25 p. 39]. The
report names the states without defining their windows. Write yours down
before the first chart: new (first active period), current (active now and in
the previous period), reactivated (back after a short gap) and resurrected
(back after a long one), each gap a fixed number of days. A blended retention
curve hides which of the four moved.

**Locals and tourists.** The LTV formula assumes every user churns at the same
even rate and ignores upsells and re-subscriptions, so it discounts the
**locals** who stay for life and overweights the high churn of the **tourists**
[GPB25 p. 71]. The report's two profiles:

| | Tourists | Locals |
|---|---|---|
| Engagement | low | high |
| Data | do not enter data | connect data sources |
| How they arrived | through an ad | through a friend |
| Behaviour | try many services, sign up through discounts | build the service into their life |

How to use the split [GPB25 p. 71]:

1. **Divide users by engagement**, using signals the product already records:
   comments, photos, shares, posting, connected data sources, logins, and
   automatic renewals from the app stores. Write the rule down, so the split is
   recomputable.
2. **Compute LTV per cohort**, estimating the lifetime value of the locals
   separately, rather than one average over both.
3. **Optimise acquisition for locals.** Judge a channel by the long-term usage
   of the users it brings, not only by its sign-ups and its return on ad spend
   (ROAS), because a channel that buys tourists cheaply can win on ROAS and lose
   on renewals.
4. **Report the average LTV** where CAC payback needs it, with the locals'
   value beside it.

The design side of the same split: the test panel (`ux-foundation`, *The test
panel*) carries at least two locals and two tourists among its ten portraits,
so a design review walks both the user the product is built around and the one
most of the churn comes from.

**Output:** the four-state retention table and the local/tourist rule, both
dated, and LTV stated per cohort.

## What this method cannot do

Stated so the output is not read as more than it is.

- **It cannot rank funnels by profit.** Every signal is spend. A competitor
  burning a raise looks like a competitor with a working funnel.
- **It cannot see the tests behind a number.** A price is a result; the
  experiment that produced it is not published.
- **It cannot see anything behind the paywall.** Retention, refund rate, dunning
  recovery and support load are the numbers that decide whether the funnel was
  worth running, and none of them is visible from the funnel: your own are read
  as *Your own numbers* describes.
- **It goes stale.** Live ads rotate, prices move, and the corpus describes the
  week it was built. Date it.
- **It is not a substitute for the foundation.** A market read tells you what the
  category does. It does not tell you who your buyer is, and a funnel designed
  from the corpus alone is aimed at a competitor's audience.
