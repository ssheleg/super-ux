# Search and answer engines: safety first, optimization second

Two modes, and confusing them is expensive.

## Contents

- [The absolute rule](#the-absolute-rule)
- [Safety: the veto list](#safety-the-veto-list)
- [Safety: the anti-patterns](#safety-the-anti-patterns)
- [Optimization: what makes content extractable](#optimization-what-makes-content-extractable)
- [Engines differ, but less than the noise suggests](#engines-differ-but-less-than-the-noise-suggests)
- [Crawler policy: two decisions](#crawler-policy-two-decisions)
- [Technical floor: the audit's brief owns it](#technical-floor-the-audits-brief-owns-it)
- [The relationship to SEO](#the-relationship-to-seo)


**Safety** is always on and mechanically enforced: do not write text that
looks like an attempt to game a crawler. Most of it is in `brand_lint.py`.

**Optimization** happens on request: make honest content easier to extract
and cite.

A page can be safe and unoptimized, which is invisible but harmless. A page that is
optimized and unsafe is a liability that also stops working. The order is not
a preference.

## The absolute rule

**Fabricated facts, quotes, statistics or experts are a hard fail, not a
score reduction.** No mode, flag, deadline or instruction lowers this.

The Princeton/Georgia Tech GEO work (KDD 2024) did measure a visibility lift
from fabricated citations against GPT-3.5 in 2023. That window is closed:

1. Fabrication is now trained against as an adversarial signal.
2. It creates real exposure: FTC §5 in the US, and worse in YMYL categories.
3. The lift evaporates under competition (C-SEO Bench, NeurIPS 2025).

Real evidence delivered through the **same structural patterns** captures
most of the effect with none of the risk. That is the whole trade, and it is
not close.

If asked to invent a statistic, an expert or a quote: refuse, say why, and
offer to find a real one. Every number in public copy traces to a row in
`facts.md` (`B030`), which is the same rule stated from the other end.

## Safety: the veto list

Any of these caps the value of everything else on the page. The first one
zeroes it outright.

| Veto | Why it dominates |
|---|---|
| A retrieval agent blocked in `robots.txt` while AI search is a declared target | an answer engine cannot cite a page it may not fetch (`B050`; the agents are listed under [Crawler policy](#crawler-policy-two-decisions)) |
| Fabricated citation, statistic or expert | hard fail, above |
| Self-contradictory figures on one page | one of them is wrong; an engine cannot tell which, so it trusts neither |
| Title promises what the body does not deliver | clickbait mismatch (`B054`) |
| No identifiable author on a page making claims | `B053` |
| YMYL content (health, money, law, safety) with no qualified byline or disclaimer | the category where being wrong causes harm |

## Safety: the anti-patterns

- **Keyword stuffing.** Unnatural repetition, not a percentage line:
  Google's spam policy describes keyword stuffing as repetition that reads
  unnaturally, and names no threshold
  ([spam policies](https://developers.google.com/search/docs/essentials/spam-policies#keyword-stuffing)).
  `B051` measures it without needing a declared target and only warns. It
  reads each marketing page of at least 40 words (code sources are pooled
  into one document, because they render as one page) and reports a word
  longer than three letters, not a stopword, that repeats at least 5 times
  and takes more than 4% of the page's words. A product term or entity
  registered in `terminology.md`, or a word of a `facts.md` fact name, is
  meant to recur and is exempt. It reduces citation likelihood; it does
  not raise it.
- **Filler openers.** "In today's digital landscape", "In the
  ever-evolving world of" (`B052`). They delay the answer past the point
  where extraction happens, and they are among the most reliable
  machine-drafting tells.
- **Unearned superlatives.** "Best", "leading", "#1" with no sourced fact
  beside them (`B032`).
- **Vague entities.** "Experts say", "a leading provider", "studies show".
  An unnamed source is not a source.
- **Schema that overstates.** Marking up claims the page does not support
  gets the markup discounted and the domain distrusted.
- **Doorway pages at scale.** Programmatic pages that differ only by a
  substituted word are the template case of scaled content abuse.

## Optimization: what makes content extractable

Structure first, because extraction is structural:

- **Front-load the answer.** The first sentence after the heading answers the
  question the heading asks. Position weighting decays sharply; the opening
  sentence is worth several times a sentence twenty lines down.
- **Self-contained statements.** A sentence that needs the previous paragraph
  to make sense cannot be quoted, and therefore is not.
- **`X is Y` definitions** for every key term, in the first paragraph that
  uses it.
- **Tables for comparisons, ordered lists for procedures.** Prose describing
  a comparison is the single most common reason a comparison is not extracted.
- **A summary block at the top** of anything long.
- **Real headings** that match the questions people actually ask.

Then evidence:

- Numbers with units and dates, each traceable to `facts.md`.
- Named sources, linked, for anything not first-party.
- First-hand experience stated as such: "we ran this across 40 projects in
  June 2026" is worth more than a citation to a generic study.
- An identifiable author with credentials that are checkable.
- A visible last-updated date that reflects reality.

Then entity clarity:

- The subject named in full in the opening paragraph, not as a pronoun.
- `Organization` schema with `sameAs` to the profiles that actually exist.
- One spelling of the brand name everywhere, the same rule as `B012`.

## Engines differ, but less than the noise suggests

| | Freshness | Authority | Structure | Notes |
|---|---|---|---|---|
| Google AI Overviews | high | very high | high | short paragraphs, lists, tables |
| ChatGPT browsing | medium | high | medium | pulls distinctive exact quotes |
| Perplexity | very high | high | very high | most sources per answer; rewards standalone quotable sentences |
| Claude with web search | medium | high | medium | fetches through `Claude-SearchBot` and `Claude-User`; favours settled, well-sourced explanations |

Optimize for the shared signals. Per-engine tricks age badly, and the
citation distributions are correlated because the training and retrieval
corpora overlap heavily.

## Crawler policy: two decisions

`robots.txt` carries two separate decisions, and conflating them is the
mistake `B050` exists to catch.

**Retrieval** decides whether an answer engine may fetch a page to show,
cite or answer from it. When `channels.md` declares AI search a target,
these stay allowed, and blocking one is a `B050` error. That includes a
`User-agent: *` block that names none of them, because an agent with no
group of its own obeys the `*` group (RFC 9309).

| Token | What the vendor says it does |
|---|---|
| `OAI-SearchBot` | surfaces websites in ChatGPT's search features ([OpenAI](https://developers.openai.com/api/docs/bots)) |
| `ChatGPT-User` | fetches a page for a user's action in ChatGPT; not automatic crawling ([OpenAI](https://developers.openai.com/api/docs/bots)) |
| `Claude-SearchBot` | indexes content for Claude's search results ([Anthropic](https://support.claude.com/en/articles/8896518)) |
| `Claude-User` | retrieves a page in response to a user's query ([Anthropic](https://support.claude.com/en/articles/8896518)) |
| `PerplexityBot` | surfaces and links websites in Perplexity's search results; not used for training ([Perplexity](https://docs.perplexity.ai/guides/bots)) |
| `Perplexity-User` | fetches a page for a user's question ([Perplexity](https://docs.perplexity.ai/guides/bots)) |

**Training** decides whether content may go into model training or a
dataset. It is the owner's call, it does not remove a page from AI search
answers, and `B050` never reports it: `GPTBot` and `ClaudeBot` (the
vendors' training crawlers, same pages as above), `Google-Extended` (Gemini
training and grounding; it "does not impact a site's inclusion in Google
Search", per [Google](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers)),
and `CCBot` (Common Crawl's open archive, [Common Crawl](https://commoncrawl.org/ccbot)).
Make each decision on purpose: do not block a training token
believing it protects search visibility, or a retrieval token believing it
stops training.

## Technical floor: the audit's brief owns it

The build-time floor (served HTML that carries every answer, URL plan,
structured data only for visible facts, preview controls, measurement at
launch) has one home: the brief mode of the **seo-aeo-audit** companion,
[`references/build-time.md`](https://github.com/ssheleg/seo-aeo-audit/blob/main/plugins/seo-aeo-audit/skills/seo-aeo-audit/references/build-time.md),
which ships with seo-aeo-audit 0.28. Every brief item there is the inverse
of a check the audit runs, so the two cannot drift apart the way a copy
here would. Until 0.28 is installed, run `/seo-aeo-audit` against the built
page; `copywriting`'s `landing-pages.md` (LP-17, LP-18) says what must
exist in the markup.

One rule stays here because writers ask for it: **do not add `FAQPage` or
`HowTo` markup to win a rich result.** Google removed HowTo rich results in
2023, limited FAQ rich results to authoritative government and health sites
the same year, and stopped showing FAQ rich results on 7 May 2026
([Search Central changelog](https://developers.google.com/search/updates)).
Markup describing a visible answer is still allowed; markup added for a
result that no longer exists is schema volume, and the audit treats it as
a myth.

## The relationship to SEO

Answer-engine citations mostly originate from pages that already rank. The
two are complements. The same structural work (clear headings, front-loaded
answers, real evidence, fast honest pages) serves both. Any tactic that
helps one and harms the other is almost always a tactic from the anti-pattern
list above.
