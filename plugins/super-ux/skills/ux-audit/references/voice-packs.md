# Voice packs — the archetype library

Six packs. A pack is a **starting position**, not the answer: `brand-voice`
picks one from the foundation, then calibrates it against the product until
`docs/brand/voice.md` is the truth and the pack name survives only as
provenance. Field names come from [brand-contract.md](brand-contract.md);
register deltas are applied per surface as described in
[surface-registers.md](surface-registers.md).

Picking one is not a taste question. Read `foundation.md` first: who the
persona is, what job the product is hired for, and — the deciding input —
**what the user loses when the product fails**. A voice that is charming when
the stakes are a playlist is intolerable when the stakes are payroll.

## The pack contract

Every pack carries all nine fields. A seventh pack is authored against this
list, not improvised.

| Field | Holds |
|---|---|
| `Use for` | product categories this voice fits |
| `Not for` | where it actively misfires — the honest half |
| `Axes` | the five fixed axes filled as IS / IS NOT |
| `Narrative template` | hero, enemy, product role, promise |
| `Lexicon` | favoured verbs, sentence shapes, length |
| `Pack bans` | what this voice never does, regardless of surface |
| `Register deltas` | how it shifts on the surfaces that stress it most |
| `Ready lines` | six to ten samples — how it sounds, not what to copy |
| `Failure mode` | the degenerate form it collapses into when overdone |

### Why `Failure mode` is mandatory

Every voice has an overshoot, and the overshoot always sounds *more* like the
pack, not less — which is why nobody catches it from inside. Naming it up
front turns "this feels like too much" into a checkable finding: the `copy`
audit scope looks for exactly the degeneration the pack declared. A pack
without it is an instruction to overshoot with no brake.

---

## operator-brief

**Use for:** infrastructure, security, observability, developer tooling,
competitive intelligence, anything where the user is accountable for an
outcome and measured on it.

**Not for:** consumer wellness, education for beginners, bereavement or
health contexts, or any product whose users did not choose to be there. The
register assumes competence and reads as contempt when that assumption is
wrong.

**Axes**

| Axis | IS | IS NOT |
|---|---|---|
| Confidence | declarative, takes a position | "we think this could help" |
| Register | terse, operational, verb-first | corporate marketing speak |
| Distance | one professional to another | vendor addressing an account |
| Humor | dry, rare, earned by accuracy | quirky, punning, emoji-led |
| Density | every sentence carries weight | filler, throat-clearing, restatement |

**Narrative template**

- Hero: the operator who owns the outcome and is measured on it
- Enemy: guesswork that costs money before anyone notices
- Product role: instrument
- Promise: you stop guessing, and you can show the work

**Lexicon.** Command verbs — run, deploy, trace, verify, cut, ship. Short
declaratives; a comma is a hint the sentence should be two. Numbers before
adjectives. No adverbs: "it fails fast" beats "it fails very quickly."
Sentence length 6–14 words in body copy.

**Pack bans.** Adverbs · hedges ("maybe", "could", "we believe") · passive
voice · feature dumps · generic CTAs ("Get started", "Learn more") · any
sentence that would sit unchanged on a competitor's page.

**Register deltas.** Error: humor −2, distance −1 — state what happened, what
was preserved, what to do. Onboarding: density −1, the terseness that reads
as confident to an expert reads as withholding to a newcomer. Reddit:
distance −1, humor +1, drop the CTA entirely. Docs: humor −2, density −1.

**Ready lines**

- Stop guessing. Start measuring.
- The market already ran your experiment and paid for it.
- Every wrong angle is budget you donated.
- Not a dashboard. A decision.
- It costs less than one failed test.
- You do not manage tools. You command outcomes.

**Failure mode.** Military-jargon parody: verbs escalate to *strike*,
*hunt*, *dominate* until the copy is about the voice instead of the user's
problem. The tell is a sentence that would need a glossary before it needs a
fact. Also: terseness applied where the user is new, which reads as
gatekeeping.

---

## calm-expert

**Use for:** fintech, health, compliance, legal, insurance, enterprise B2B —
anywhere a mistake is expensive and the reader is already anxious.

**Not for:** products competing on delight or novelty, or launches that need
to be talked about. This voice is trusted and rarely shared.

**Axes**

| Axis | IS | IS NOT |
|---|---|---|
| Confidence | quiet authority, states its limits | bravado, superlatives |
| Register | plain professional | either legalese or chat |
| Distance | advisor to client | buddy, or institution to subject |
| Humor | almost none, never about the stakes | levity to lighten a hard moment |
| Density | complete over compact | dense to the point of ambiguity |

**Narrative template**

- Hero: the person who will be held responsible for the decision
- Enemy: irreversible mistakes made from incomplete information
- Product role: guide
- Promise: you will understand what you are agreeing to before you agree

**Lexicon.** Full sentences. Conditions stated before conclusions. "You can"
and "you cannot" rather than "it is possible to". Numbers with units and
dates. Limitations named in the same paragraph as the capability, never in a
footnote.

**Pack bans.** Urgency manufactured from nothing · countdowns · "limited
time" without a real limit · minimising risk language ("just", "simply",
"only takes a second") · claims without a dated source · humor on anything
the user could lose.

**Register deltas.** Error: density +1 — say what happened, what it did not
affect, and what happens next. Pricing: confidence +1, every number sourced.
Landing hero: density −1, this is the one surface where the voice may be
brief. Lifecycle email: distance +1.

**Ready lines**

- Know what you are signing before you sign it.
- Two things this does not do, before the five it does.
- Reviewed quarterly. Last reviewed 12 June 2026.
- If this is wrong, here is how you find out early.
- No surprises at renewal. The price you see is the price.
- We will tell you when this is not the right tool for you.

**Failure mode.** Corporate mush: caution multiplies into hedging, every
sentence acquires a qualifier, and the copy stops saying anything a reader
could act on. The tell is a paragraph that survives deletion with no loss.
Second form: limits stated so prominently the product sounds broken.

---

## peer-builder

**Use for:** developer tools, APIs, open source, infrastructure libraries,
anything whose buyer will read the source before the pricing page.

**Not for:** non-technical buyers, regulated purchases with a committee, or
any audience for whom "here is where it breaks" reads as an admission rather
than as respect.

**Axes**

| Axis | IS | IS NOT |
|---|---|---|
| Confidence | specific and falsifiable | vague and unarguable |
| Register | technical, unadorned | marketing prose about technology |
| Distance | equals who have both been on call | expert lecturing a student |
| Humor | wry, self-aware, in-group without excluding | memes as a substitute for content |
| Density | high, but every term grounded | jargon assumed rather than introduced |

**Narrative template**

- Hero: the engineer who will have to maintain this at 3am
- Enemy: tools that hide their failure modes until production
- Product role: instrument
- Promise: it does what the README says, and the README says what it does not

**Lexicon.** Concrete nouns. Real numbers with units. Trade-offs stated as
trade-offs. Code where prose would be longer. "Here is where it breaks" as a
section, not an apology. Terms grounded before use — see the grounding model
in [marketing-copy.md](marketing-copy.md).

**Pack bans.** Benchmarks without methodology · "blazingly fast" and its
family · claiming a category nobody uses · hiding limits in a FAQ · comparing
against a straw configuration of a competitor.

**Register deltas.** Landing hero: density −1 — the one place the audience
has not opted in yet. Error: humor −2. Changelog: distance −1, humor +1.
Docs: humor −1, density +1. Ads: density −2, an ad has no room to ground a
term.

**Ready lines**

- It does one thing. Here is the thing, and here is where it stops.
- Benchmarks, with the harness, on a machine you can rent.
- Breaking changes get a codemod, not a migration guide.
- Yes, it is slower than X for Y. Use X for Y.
- The whole API is nine functions.
- If you hit an edge we did not document, that is our bug.

**Failure mode.** Insider shorthand: the in-group signals compound until
newcomers cannot enter, and the humor lands only for people who already use
the product. The tell is a homepage that assumes the reader already knows
what the category is called. Second form: honesty performed rather than
practised — limits listed for credit while the real one stays buried.

---

## editorial-premium

**Use for:** brand-led products, design tools, media, hospitality, fashion,
anything sold on taste where the purchase is partly an identity statement.

**Not for:** utility products bought under time pressure, technical
evaluation, or any funnel where comprehension speed beats atmosphere.

**Axes**

| Axis | IS | IS NOT |
|---|---|---|
| Confidence | assured, unhurried | loud, insistent |
| Register | considered, literary restraint | flowery, ornamental |
| Distance | curator to an equal of taste | luxury brand to aspirant |
| Humor | dry, occasional, never broad | jokes, wordplay for its own sake |
| Density | spare — silence is a device | sparse because there is nothing to say |

**Narrative template**

- Hero: someone who notices the difference and is tired of not finding it
- Enemy: the default, chosen by nobody and accepted by everyone
- Product role: guide
- Promise: fewer, better, and you will not think about it again

**Lexicon.** Concrete sensory nouns over abstractions. One metaphor per
piece, carried rather than mixed. Rhythm matters: vary sentence length
deliberately, and let a short sentence land. White space is content.

**Pack bans.** Exclamation marks · stacked adjectives · "curated",
"bespoke", "elevated", "crafted" used as filler · superlatives · borrowed
prestige (name-dropping unrelated brands) · urgency of any kind.

**Register deltas.** Error: density +1, humor −2 — atmosphere is not an
excuse for vagueness when something failed. Pricing: density +1, be plain
about money. Onboarding: density +1. App Store: density +2, the field limits
leave no room for atmosphere.

**Ready lines**

- Made once, properly.
- The version you stop replacing.
- Everything it does not do was also a decision.
- Quiet by design.
- It will outlast the trend that made you look.
- Nothing here is new. All of it is right.

**Failure mode.** Beautiful emptiness: the rhythm survives, the content
leaves. The tell is a page a reader finishes without learning what the
product does, or a line that reads well and cannot be checked. Second form:
restraint used to avoid saying the price.

---

## plain-service

**Use for:** government, healthcare access, utilities, banking basics,
logistics, anything with a legally or practically captive audience and a wide
range of reading ability.

**Not for:** differentiation-led products in crowded markets. This voice
cannot make anyone want something; it makes things possible.

**Axes**

| Axis | IS | IS NOT |
|---|---|---|
| Confidence | direct instruction | authoritarian, or apologetic |
| Register | plainest available word | simplified to the point of vagueness |
| Distance | service to a person who needs it done | institution addressing a case number |
| Humor | none | warmth mistaken for jokes |
| Density | one idea per sentence | terse to the point of ambiguity |

**Narrative template**

- Hero: someone who needs this done and did not choose to be here
- Enemy: process that costs time, money or dignity to navigate
- Product role: instrument
- Promise: you will know what to do next, at every step

**Lexicon.** Short word over precise long one. Active voice, present tense.
Second person. Numerals for numbers. One instruction per sentence. Say
"you must" and "you can" rather than "it is required that". Read at the
level of a stressed person on a phone, not a calm person at a desk.

**Pack bans.** Metaphor · idiom (it fails first in translation and for
non-native readers) · abbreviations without expansion · nested conditionals ·
cheerfulness about a difficult process · any word that a reader might have to
look up.

**Register deltas.** Error: density +1 — name what happened, what it did not
affect, and the next step. Landing hero: unchanged, this voice does not
perform anywhere. Legal: density +1, plainness applies to legal text too.
Marketing surfaces generally: this pack barely moves, which is the point.

**Ready lines**

- You do not need an account to check this.
- This takes about 4 minutes.
- If you do not have your number, you can still continue.
- We saved what you entered. Nothing was lost.
- You will get an email within 2 working days.
- If this is wrong, call 0800 000 000. A person will answer.

**Failure mode.** Flatness that reads as indifference: correct, complete and
cold, so a person in difficulty feels processed. The tell is an error message
that explains everything and acknowledges nothing. Second form:
simplification that removes the information the reader actually needed.

---

## playful-consumer

**Use for:** consumer apps, habit and wellness, social, learning, creative
tools — products used voluntarily, often daily, where warmth earns retention.

**Not for:** anything holding money, health records or irreversible actions
as its core object. Also poor for enterprise buyers, who read levity as
immaturity in a vendor.

**Axes**

| Axis | IS | IS NOT |
|---|---|---|
| Confidence | warm and sure | needy, over-eager |
| Register | conversational, contractions | slang chasing a demographic |
| Distance | a friend who knows the thing | brand performing friendship |
| Humor | light, in service of clarity | jokes that delay the point |
| Density | light, generous with white space | padded with personality |

**Narrative template**

- Hero: someone trying to build something small and good into their life
- Enemy: the friction that makes them quit in week two
- Product role: guide
- Promise: it stays easy on the day you do not feel like it

**Lexicon.** Contractions. Second person. Verbs over nouns. Specifics over
enthusiasm: "three days in a row" beats "amazing progress". Humor arrives in
one clause and leaves; it never occupies a whole sentence on its own.

**Pack bans.** Shaming a lapse · fake streak anxiety · exclamation marks
stacked more than one per screen · humor on error, billing, destructive
confirm or paywall · pretending a limit is a feature · emoji standing in for
a word the copy should have written.

**Register deltas.** Error: humor −3, density +1 — the ban is absolute here.
Billing and paywall: humor −3, distance +1; a joke while asking for money
reads as a trick. Empty state: humor unchanged, this is the surface the pack
is best at. Ads: density −1.

**Ready lines**

- Day one is the hard one. This is day one.
- Missed yesterday? It still counts. Keep going.
- Two taps, then it is out of your head.
- Nothing here is going anywhere.
- You can undo this. You can always undo this.
- Start with one. One is a real number.

**Failure mode.** Cringe: personality applied where the user wanted an
answer, until the product sounds like it is entertaining itself. The tell is
copy that is funny on the first read and obstructive on the fortieth —
microcopy is read hundreds of times, and a joke has a half-life. Second
form: warmth used to soften a refusal the product should state plainly.
