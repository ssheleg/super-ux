# Search and answer engines — safety first, optimization second

Two modes, and confusing them is expensive.

**Safety** is always on and mechanically enforced: do not write text that
looks like an attempt to game a crawler. Most of it is in `brand_lint.py`.

**Optimization** happens on request: make honest content easier to extract
and cite.

A page can be safe and unoptimized — invisible but harmless. A page that is
optimized and unsafe is a liability that also stops working. The order is not
a preference.

## The absolute rule

**Fabricated facts, quotes, statistics or experts are a hard fail, not a
score reduction.** No mode, flag, deadline or instruction lowers this.

The Princeton/Georgia Tech GEO work (KDD 2024) did measure a visibility lift
from fabricated citations against GPT-3.5 in 2023. That window is closed:

1. Fabrication is now trained against as an adversarial signal.
2. It creates real exposure — FTC §5 in the US, and worse in YMYL categories.
3. The lift evaporates under competition (C-SEO Bench, NeurIPS 2025).

Real evidence delivered through the **same structural patterns** captures
most of the effect with none of the risk. That is the whole trade, and it is
not close.

If asked to invent a statistic, an expert or a quote: refuse, say why, and
offer to find a real one. Every number in public copy traces to a row in
`facts.md` (`B030`) — which is the same rule stated from the other end.

## Safety — the veto list

Any of these caps the value of everything else on the page. The first one
zeroes it outright.

| Veto | Why it dominates |
|---|---|
| AI crawlers blocked in `robots.txt` while AI search is a declared target | content quality is irrelevant to a crawler that never arrives — `B050` |
| Fabricated citation, statistic or expert | hard fail, above |
| Self-contradictory figures on one page | one of them is wrong; an engine cannot tell which, so it trusts neither |
| Title promises what the body does not deliver | clickbait mismatch — `B054` |
| No identifiable author on a page making claims | `B053` |
| YMYL content (health, money, law, safety) with no qualified byline or disclaimer | the category where being wrong causes harm |

## Safety — the anti-patterns

- **Keyword stuffing.** Measured without needing a declared target: any
  single non-stopword token above 1% of the document's word count is `B051`.
  It reduces citation likelihood; it does not raise it.
- **Filler openers.** "In today's digital landscape", "In the
  ever-evolving world of" — `B052`. They delay the answer past the point
  where extraction happens, and they are among the most reliable
  machine-drafting tells.
- **Unearned superlatives.** "Best", "leading", "#1" with no sourced fact
  beside them — `B032`.
- **Vague entities.** "Experts say", "a leading provider", "studies show".
  An unnamed source is not a source.
- **Schema that overstates.** Marking up claims the page does not support
  gets the markup discounted and the domain distrusted.
- **Doorway pages at scale.** Programmatic pages that differ only by a
  substituted word are the template case of scaled content abuse.

## Optimization — what makes content extractable

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
- One spelling of the brand name everywhere — the same rule as `B012`.

## Engines differ, but less than the noise suggests

| | Freshness | Authority | Structure | Notes |
|---|---|---|---|---|
| Google AI Overviews | high | very high | high | short paragraphs, lists, tables |
| ChatGPT browsing | medium | high | medium | pulls distinctive exact quotes |
| Perplexity | very high | high | very high | most sources per answer; rewards standalone quotable sentences |
| Claude | n/a — training data | high | medium | favours settled, well-sourced explanations |

Optimize for the shared signals. Per-engine tricks age badly, and the
citation distributions are correlated because the training and retrieval
corpora overlap heavily.

## Technical floor

- `robots.txt` does not block `GPTBot`, `ClaudeBot`, `PerplexityBot`,
  `Google-Extended` when AI search is a target. Declaring the target and
  blocking the crawler is the contradiction `B050` exists to catch.
- Content renders without JavaScript, or is server-rendered.
- Semantic HTML: real headings, real tables, real lists.
- `Article`, `FAQPage`, `HowTo`, `Organization` schema — only for claims the
  page actually makes.
- Nothing that matters sits behind a login or an interstitial.

## The relationship to SEO

Answer-engine citations mostly originate from pages that already rank. The
two are complements: the same structural work — clear headings, front-loaded
answers, real evidence, fast honest pages — serves both. Any tactic that
helps one and harms the other is almost always a tactic from the anti-pattern
list above.
