# Landing pages: assembling one, not editing one

[marketing-copy.md](marketing-copy.md) says how a page is written and edited.
This file says what it is made of, in what order, and how to tell before
shipping whether it holds. The two are different jobs: a page can survive
every one of the seven sweeps sentence by sentence and still fail, because
nothing in a sweep asks whether the argument is complete.

Everything below was extracted from teardowns of live pages rather than from
preference. Where a rule carries an example, the example is verbatim from a
page that shipped, with the site and the date it was read. Where three
independent pages made the same mistake, that is said, because a defect three
teams reached on their own is a defect the next team will reach too.

## Contents

- [Before the first line](#before-the-first-line)
- [The twenty](#the-twenty)
- [The offer](#the-offer)
- [Awareness, and the shape it demands](#awareness-and-the-shape-it-demands)
- [The proof ladder](#the-proof-ladder)
- [The action, and the risk beside it](#the-action-and-the-risk-beside-it)
- [The page as a machine](#the-page-as-a-machine)
- [The readiness check](#the-readiness-check)
- [Where the evidence came from](#where-the-evidence-came-from)

## Before the first line

The four inputs in `marketing-copy.md` still apply, and a landing page adds
one: **the traffic**. A page written without knowing what brought the reader
cannot open in the right place, and opening in the wrong place is the failure
no later section repairs.

Name these before writing, in one line each: the one action, the reader and
their job, the words they use, the proof from `facts.md`, and where they came
from. A page that cannot answer the fifth is a homepage, and it should be
built as one.

## The twenty

| id | Rule | Fails as |
|---|---|---|
| LP-01 | The headline names a change in the reader's world | a product description |
| LP-02 | The subhead carries the specificity the headline dropped | a headline nobody can parse |
| LP-03 | The enemy is named, conceded, then devalued with a verb | a comparison nobody believes |
| LP-04 | The promise escalates down the page | three restatements of one line |
| LP-05 | The mechanism is shown, not asserted | a claim with no reason to be true |
| LP-06 | The page opens where the traffic's awareness already is | an answer to a question nobody asked |
| LP-07 | A category nobody searches for borrows a known model | a manifesto about the future |
| LP-08 | The category's own vocabulary lives off the landing page | a page that only insiders can read |
| LP-09 | The strongest proof sits on the screen with the claim it proves | proof filed where only believers go |
| LP-10 | Every number is attributed or it is decoration | a page of unsourced percentages |
| LP-11 | One number keeps one value and one unit | a page arguing with itself |
| LP-12 | The product is shown with imperfect data | a screenshot nobody believes |
| LP-13 | One action keeps one label across the whole page | five names for one button |
| LP-14 | The first ask costs curiosity, not commitment | a signup wall above the fold |
| LP-15 | Each CTA carries the objection standing at that point | one reassurance copied three times |
| LP-16 | The warmest reader is not returned to the top | a demo that ends in nothing |
| LP-17 | Every answer the page gives exists in the markup | an FAQ that answers nothing |
| LP-18 | Appearance animation never holds the only copy of content | an empty screen that measures as shipped |
| LP-19 | One section advances one argument | a section that advances neither |
| LP-20 | The page states the price or states why it does not | a trust argument with a hole in it |

## The offer

### LP-01. The headline names a change in the reader's world

Not what the product is, and not what it does: what is different for the
reader afterwards. The test is substitution. If a competitor could put their
name on the sentence and it would still be true, it is a category label, not
a headline.

`Compliance that helps you close deals.` (trycomp.ai, 2026-08-30) survives
the test. The same page's `The AI-first compliance platform` does not, and
both are on one screen, which makes the pair the cheapest available lesson.

`Rank #1 in ChatGPT` (zerorank.ai, 2026-08-30) sells a position rather than
the tracker that measures it.

### LP-02. The subhead carries the specificity the headline dropped

The headline holds one idea, so everything that idea needs and cannot carry
goes immediately below it. Abbreviations, scope, integrations, constraints:
all of it belongs here rather than in the line above.

`SOC 2, ISO 27001, HIPAA, and GDPR - automated with 580+ integrations. We get
you audit-ready.` (trycomp.ai, 2026-08-30) is sixteen words holding four
standards and a number, under a headline of six words holding none.

### LP-03. The enemy is named, conceded, then devalued with a verb

A page that competes against nothing reads as a page about nothing. The
sequence matters: name what the reader is already using, concede that it
works, then say what it does not do. The concession is what makes the third
part credible, and a verb does the devaluing better than any adjective.

`Other tools show you where you're missing. CrowdReply gets you in.`
(crowdreply.io, 2026-08-30) is eleven words with no adjective in them.

`Most compliance platforms are black boxes - you trust them because you have
to.` (trycomp.ai, 2026-08-30) names the category rather than a company, which
is the form to use when the reader has not chosen a vendor yet.

### LP-04. The promise escalates down the page

The reader who reaches the last screen has spent attention and knows more
than the reader at the first. Repeating the opening claim to them wastes the
distance travelled. Raise it instead.

`Make [AI] Mention Your Brand` at the hero, `Become the brand AI recommends.`
in the body, `Your Brand Deserves to Be the Answer` at the close
(crowdreply.io, 2026-08-30): mention, then recommendation, then being the
answer itself.

### LP-05. The mechanism is shown, not asserted

A promise the reader cannot picture is a promise they discount. Between the
claim and the proof sits the question *how*, and three or four steps answer
it. Naming the step that is uncomfortable is stronger than smoothing it: a
reader who spots the euphemism stops believing the rest.

`We Post for You`, captioned `Posted through trusted community profiles on
your behalf.` (crowdreply.io, 2026-08-30). The product posts under the
customer's name, which is the part a reader would worry about, and it is
stated rather than dressed.

## Awareness, and the shape it demands

### LP-06. The page opens where the traffic's awareness already is

The same product needs a different first screen depending on what brought the
reader. This is the decision `marketing-copy.md` points at when it says to
pick by what the traffic already knows, and here is the map.

| The reader arrives | The first screen must | Opening with anything else |
|---|---|---|
| unaware of the problem | name the situation in their words | reads as an ad for nothing |
| aware of the problem, not of solutions | show that the problem is solvable | reads as a product they cannot place |
| comparing solutions | name the enemy and the difference | reads as a brochure |
| comparing vendors | show proof and price | reads as a stall |
| ready to buy | get out of the way | loses the sale it already had |

A page serving two of these rows serves neither. Split it, and let the link
that brought the reader decide which one they land on.

### LP-07. A category nobody searches for borrows a known model

Selling something the reader has no word for is not solved by explaining the
new word. It is solved by mounting the new thing on a model they already own,
so the first screen costs them no learning.

`Rank #1 in ChatGPT` (zerorank.ai, 2026-08-30) is search ranking, a concept
twenty years old, pointed at a surface two years old. The page carries no
sentence beginning *a new era* and no section explaining why the category
matters.

Two devices do the legitimising work in place of a manifesto. **Density of
number:** better than thirty figures across 1042 words, roughly one every
thirty-five. **Fear of falling behind rather than fear of ruin:**
`Reach customers before your competitors do.` repeated five times. The second
is deliberate, and worth copying: agreeing that you might be second is a much
smaller concession than agreeing that the world has changed.

### LP-08. The category's own vocabulary lives off the landing page

The terms an industry uses to name a young category are known to the people
already inside it, and those people are not the ones a landing page has to
convert. Put the jargon where the search for it happens.

`AEO` and `GEO` appear zero times on zerorank.ai's landing page, while
`/blog/aeo-vs-seo` and `/blog/geo-vs-aeo` both exist (2026-08-30). The
landing page is written for a reader who does not know the term; the blog
catches the reader who already types it.

## The proof ladder

Proof is not one thing, and the kinds are not interchangeable. Ordered by
what it costs a reader to disbelieve them:

1. **Something they can check themselves.** A link to the exact artefact, a
   live status page, a repository path.
2. **A named person at a named company**, with a role, saying something
   specific enough to be wrong.
3. **A number with a source and a period.**
4. **A logo.** Says a company exists nearby, and nothing about the result.
5. **An unattributed number.** Costs nothing to write, so it is read as
   costing nothing.

Every claim on the page should be met by the highest rung it can afford. A
page whose proof is entirely rungs four and five has decorated rather than
argued.

### LP-09. The strongest proof sits on the screen with the claim it proves

Proof filed on a second page reaches only the reader who already believes
enough to click. This is the most common single defect across the pages read
for this file, and all three committed it.

trycomp.ai's landing page carries no money figure while its `/case-studies`
holds `$400,000+ ARR unlocked`, `6 days To audit-ready` and `85 hours saved`,
which are the literal evidence for its own headline about closing deals.
crowdreply.io runs seven named case studies and then fills its testimonial
block with `Adrina W / App` and `Marcus A / eCom`. Both had the higher rung
already written and used the lower one where it mattered.

### LP-10. Every number is attributed or it is decoration

A percentage with no company, no period and no method is read as a design
element, because that is what it is. `+47%`, `75%`, `4%`, `2X`
(crowdreply.io, 2026-08-30) carry none of the three.

The reverse is cheap and works: `3x` above `mention growth`, then the quote,
then `Ervis Bregasi, CEO, ClickFlare` (zerorank.ai, 2026-08-30). The number
catches the eye, the quote explains it, the attribution settles it.

### LP-11. One number keeps one value and one unit

The same fact stated twice differently tells a reader that nobody checked,
and a reader who catches one stops trusting the rest. This is `facts.md`
doing its job: a figure with no row there has no single home, and a figure
with a row cannot drift.

`1k+ marketers` and `1000+ brands` on one page (zerorank.ai, 2026-08-30):
one number, two units, and they are not the same claim. `4.9/5` on screen
against `"ratingValue": "4.7", "reviewCount": "64"` in the same document's
JSON-LD (trycomp.ai, 2026-08-30): the page disagrees with its own machine
readable copy, which is the version an answer engine quotes.

### LP-12. The product is shown with imperfect data

A screenshot where every metric is complete reads as a mockup, because it is
one. Real numbers are uneven, and unevenness is what makes the picture
evidence rather than illustration.

`SOC 2 TYPE I - 92%`, `ISO 27001 - 35%` (trycomp.ai, 2026-08-30): nothing at
a hundred. zerorank.ai shows `10%` and `#8 Your rank` in its dashboard rather
than a leading position.

The same instinct applies to where a number lives. A figure inside a product
screenshot is read as a fact about the product; the identical figure in a
marketing tile is read as a claim about the company.

## The action, and the risk beside it

### LP-13. One action keeps one label across the whole page

This is the interface rule in `ui-copy.md` applied to a page, and it is
broken more often on landing pages than anywhere else, because sections get
written at different times by different people.

Measured: six labels for two actions on zerorank.ai (`Start Free Trial`,
`Start for Free`, `Start for free`, `Request Demo`, `Book a Demo`); five
labels for one action on crowdreply.io, all resolving to `/signup`; and
`Book Demo` against `Book a Demo` on trycomp.ai. Three independent pages,
three failures of the same rule, which is why it is checked mechanically in
[the readiness check](#the-readiness-check) rather than trusted to review.

### LP-14. The first ask costs curiosity, not commitment

The primary action above the fold sets a price in attention. An input field
the reader can fill without deciding anything costs less than a button that
commits them, and it earns the address the rest of the page needs.

`<input placeholder="your-website.com">` beside `Analyze` (zerorank.ai,
2026-08-30) asks the reader to be curious about their own site.
`Enter your work email` inline in the hero (trycomp.ai, 2026-08-30) asks for
one field, and the same single field appears in all seven of that page's
forms.

### LP-15. Each CTA carries the objection standing at that point

Microcopy under a button is not decoration and it is not one line reused. The
fear at the hero is not the fear after a demo, and answering the wrong one
wastes the space.

zerorank.ai runs three distinct pairs (2026-08-30): `Setup in 2 mins` with
`No credit card required` at the hero, which answers time and money;
`7-day free trial` with `Cancel anytime` after the demo video, which answers
duration and lock-in; `Secure and compliant` with `99.9% uptime` at the
footer, which answers the operational reader who got that far.

The counter-case is the same page type with none of it: on crowdreply.io,
`no credit card`, `guarantee` and `money-back` each occur zero times, and the
hero button carries no supporting line at all.

### LP-16. The warmest reader is not returned to the top

Someone who has just finished a demo video, a calculator or an interactive
tour is the most persuaded they will be. Ending that moment by handing them
the page again spends the persuasion.

zerorank.ai attaches a CTA to the end of its demo modal (2026-08-30), and
that CTA is the only place on the whole site where the trial length is
stated.

## The page as a machine

### LP-17. Every answer the page gives exists in the markup

An accordion whose answers are not in the document is not an FAQ. Nothing
reads it: not a reader with JavaScript disabled, not an answer engine, and on
one of the pages measured, not even a fully hydrated browser.

All three pages failed this, in two different directions. zerorank.ai: five
of six answers absent, and no `FAQPage` markup. crowdreply.io: seven of
eight absent, one `Organization` block and nothing else. trycomp.ai: a
complete `FAQPage` in JSON-LD and seven answers a human cannot reach, which
is the failure inverted. A machine is told and the reader is not.

Where an answer exists in two places, the two are one claim and they drift.
Write it once and render both from it.

### LP-18. Appearance animation never holds the only copy of content

Scroll-triggered reveals put content behind a condition. When the condition
does not fire, the content is not late: it is absent, and nothing on the page
says so.

Three of three pages had key content invisible at the moment of measurement
(2026-08-30). crowdreply.io: two of four scroll frames were an entirely empty
viewport, with 68 elements held at `opacity:0` and a single
`prefers-reduced-motion` rule against them. trycomp.ai: `opacity:0` written
inline into the server-rendered markup, so the hero arrived without its form
and without its trust seals. zerorank.ai: the main product screenshot
rendered as an empty rectangle while the file itself returned 200.

The rule this gives the visual layer is not about taste. Content is present
by default and animation is a modifier on something already there. A page
whose argument depends on a scroll event has no argument when the event does
not arrive.

### LP-19. One section advances one argument

The rule from `marketing-copy.md`, and the landing-page corollary: two
sections may cover the same capability if they address different readers.

`Everything You Need to Win in AI Search` and `Turn AI Visibility Into
Customer Growth` (zerorank.ai, 2026-08-30) describe one set of four features,
first as mechanism and then as outcome. That is not duplication, because the
reader who wants to know how it works and the reader who wants to know what
they get are two people.

### LP-20. The page states the price or states why it does not

Silence about price is read as an answer, and the answer it is read as is
*expensive, and you will have to talk to someone*. Either number or reason is
acceptable. Neither is not.

This matters most where the page's own argument is transparency.
trycomp.ai builds its case on `Most compliance platforms are black boxes -
you trust them because you have to.` and publishes no price on its landing
page or its pricing page, while its `/vanta-pricing` page criticises a
competitor for exactly that: `Pricing is not publicly listed and requires a
sales call` (2026-08-30). A page that breaks its own stated principle spends
the principle.

## The readiness check

Run against the built page, not the draft. Every line here is a command with
an exit code rather than an opinion, which is the standard the rest of this
pack holds itself to.

```sh
URL=https://example.com
curl -sL "$URL" -o /tmp/page.html

# LP-17. Every question has its answer in the markup.
#   Read both numbers. A question count above the answer count is the defect.
grep -c 'aria-expanded' /tmp/page.html
python3 - <<'PY'
import re, pathlib
html = pathlib.Path('/tmp/page.html').read_text(errors='ignore')
print('FAQPage in JSON-LD:', 'FAQPage' in html)
PY

# LP-13. One action, one label. Read the list: near-duplicates are the defect.
python3 - <<'PY'
import re, collections, pathlib
html = pathlib.Path('/tmp/page.html').read_text(errors='ignore')
labels = [re.sub(r'<[^>]+>', '', m).strip()
          for m in re.findall(r'<(?:a|button)\b[^>]*>(.*?)</(?:a|button)>', html, re.S)]
for text, n in collections.Counter(l for l in labels if 0 < len(l) < 40).most_common(30):
    print(f'{n:3}  {text}')
PY

# LP-18. The argument survives without JavaScript and without a scroll event.
#   A count near zero on a page that looks full is the defect.
python3 -c "import re,sys;h=open('/tmp/page.html',errors='ignore').read();\
t=re.sub(r'<(script|style)[^>]*>.*?</\1>','',h,flags=re.S);\
print('words without JS:', len(re.sub(r'<[^>]+>',' ',t).split()))"
grep -c 'opacity:\s*0' /tmp/page.html

# LP-11. One number, one value. Read the output: two spellings of one figure
#   is the defect, and it is the one a reader catches first.
grep -oE '[0-9][0-9,.]*(k|K|M|%|\+)?' /tmp/page.html | sort | uniq -c | sort -rn | head -20

# LP-20. The price is stated, or the reason is.
grep -icE '\$[0-9]|per month|/mo|pricing' /tmp/page.html
```

What no command can decide, and a person therefore must: LP-01 and LP-03,
because the substitution test needs a competitor's page beside yours; LP-06,
because only the traffic source says which row applies; and LP-09, because
whether the proof matches the claim is a reading, not a count.

## Where the evidence came from

Three teardowns of live pages, read on 2026-08-30: crowdreply.io,
trycomp.ai and zerorank.ai. Each was fetched as raw markup, as rendered text
and in a browser, and each section, headline, call to action and proof
element was recorded verbatim before any rule was written.

Two properties of that sample bound what it can support. All three sell to
technical or marketing buyers in or near the AI search category, so nothing
here is evidence about consumer pages. And three pages is enough to notice a
repeated defect, which is why the repeats are named as such and the
single-page observations are attributed to their one page rather than
generalised.

Where a later teardown contradicts a rule above, the rule changes and the new
evidence is cited beside the old. A playbook that only accumulates is a
playbook nobody has tested.
