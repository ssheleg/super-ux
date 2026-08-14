# Machine-drafting markers: detect, fix, and know when to stop

Text drafted by a model has measurable habits. This file names them, grades
them, and bounds the repair, because an unbounded "make it sound human" pass
destroys meaning while improving rhythm.

## Contents

- [Severity](#severity)
- [Naturalness grade, applied to the result](#naturalness-grade-applied-to-the-result)
- [The markers](#the-markers)
- [The dash rule in full](#the-dash-rule-in-full)
- [Density threshold](#density-threshold)
- [The change-rate guard](#the-change-rate-guard)
- [Semantic-preservation check, mandatory before output](#semantic-preservation-check-mandatory-before-output)
- [What "human" is not](#what-human-is-not)


Used by the `Humanize` mode of `copywriting` and by `B060`, `B062` and `B063`
in `brand_lint.py`. Voice, once the generic is gone, comes from
[voice-packs.md](voice-packs.md) via the project's `voice.md`.

Every marker carries an id. A rule set that cannot be enumerated cannot have
coverage computed over it, and three of these are now mechanical checks whose
ids are how the linter and the doctrine stay pointed at the same thing.

## Severity

| Grade | Meaning |
|---|---|
| **S1** | decisive on its own, so one instance reads as machine-drafted |
| **S2** | one or two are fine; three or more is a signal |
| **S3** | weak alone, decisive when stacked with others |

`B060` warns at any S1 or three S2, and errors at three S1.

## Naturalness grade, applied to the result

After the rewrite, not the input:

- **A**: no S1, at most two S2. Reads as written by a person.
- **B**: one or two S1, or three to five S2. Natural with minor traces.
- **C**: three or more S1, or six or more S2. Traces are obvious; another
  pass is warranted.
- **D**: violations across several categories, or the change-rate guard
  fired.

## The markers

| id | Marker | Grade | Checked by |
|---|---|---|---|
| AT-01 | Vocabulary | S1 | `B060` |
| AT-02 | Hedging chains | S1 | `B060` |
| AT-03 | Uniform sentence length | S1 | judgement |
| AT-04 | Identical paragraph shape | S1 | judgement |
| AT-05 | Vagueness where a fact belongs | S1 | `B030` from the other side |
| AT-06 | The rhetorical dash | S1 | `B062` |
| AT-07 | A title that ends in a full stop | S1 | `B026`, `B063` |
| AT-08 | The rule-of-three habit | S2 | judgement |
| AT-09 | False balance | S2 | judgement |
| AT-10 | The summary conclusion | S2 | judgement |
| AT-11 | "Not just X, but Y" | S2 | judgement |
| AT-12 | The bold reflex | S2 | judgement |
| AT-13 | The colon hook | S2 | judgement |
| AT-14 | Symmetrical headings | S3 | judgement |
| AT-15 | Over-signposting | S3 | judgement |

### AT-01. Vocabulary, S1

`delve`, `landscape` (figurative), `crucial`, `vital`, `pivotal`,
`leverage` (as a verb), `robust`, `comprehensive`, `holistic`, `foster`,
`facilitate`, `navigate` (figurative), `seamless`, `tapestry`, `realm`,
`testament to`, `underscores`, `it's worth noting`.

Never simply delete: replace with the thing the word was standing in for.
`robust` becomes the number. `facilitate` becomes `help`. `crucial` becomes
the consequence, stated, so the importance is self-evident.

### AT-02. Hedging chains, S1

"It is important to note that", "It is worth mentioning that", "One might
argue that", "In many cases", "It goes without saying", "Needless to say".

These exist because the drafting process is uncertain and hedges by default.
A person hedges when they are actually uncertain, which is much less often.

### AT-03. Uniform sentence length, S1

Every sentence 18 to 22 words. The most reliable tell and the least noticed,
because no individual sentence is wrong.

The fix is rhythm, not vocabulary: break long sentences, let a short one land
after a long one, use a fragment where it serves emphasis, and let one
sentence run when the thought genuinely needs the room.

### AT-04. Identical paragraph shape, S1

Statement, explanation, example, bridge, every paragraph, forever. Real
writing varies: a one-sentence paragraph, a question answered immediately, a
short list dropped into prose, an aside, a correction.

### AT-05. Vagueness where a fact belongs, S1

"Many companies", "studies show", "significantly improved", "leading
brands", "a lot of". Each is a place where a specific claim was avoided
because a specific claim can be checked.

Replace with the real figure from `facts.md`, or say plainly that you do not
have one. Honest absence beats confident vagueness, and it is also the
`B030` rule from the other side.

### AT-06. The rhetorical dash, S1

A dash standing in for a full stop, a comma or a colon. See
[the dash rule in full](#the-dash-rule-in-full), because the distinction
between the rhetorical dash and the grammatical one is the whole rule, and
deleting dashes without it produces worse text than leaving them alone.

### AT-07. A title that ends in a full stop, S1

A heading, a label, a button, a menu item, a page title, a store title, a
subject line: each is a name, not a statement, so it takes no terminal
punctuation. A question mark is fine where the title genuinely asks. An
ellipsis is fine where the control genuinely opens something further.

The full stop is different. It is the single most reliable sign that prose
was generated into a slot meant for a name, and a reader registers it as
stiffness before they can say why. `B026` catches it in the string registry,
`B063` in marketing documents.

Exceptions the checks already allow, because they are not the defect: a title
that is several sentences (a different problem), an ellipsis, and a trailing
abbreviation such as `etc.` or `Node.js` that carries its own period.

### AT-08. The rule-of-three habit, S2

Three adjectives, three examples, three-item lists, everywhere. Three is a
good number sometimes; it is not a good number always.

### AT-09. False balance, S2

"While X has advantages, Y also has merits" as a way of avoiding a position.
If the piece has a view, state it.

### AT-10. The summary conclusion, S2

"In conclusion, we explored X, Y and Z. By implementing these strategies…"
A restatement of the introduction. A real ending either adds something or
stops.

### AT-11. "Not just X, but Y", S2

Also "it's not about X, it's about Y", and in Russian «не просто X, а Y».
The construction is legitimate and common in real writing. The tell is the
reflex: it appears whenever the draft needs to sound insightful and has no
new fact to offer, so the sentence pivots on a contrast the reader was never
holding.

The test is whether anyone actually believed X. If nobody did, the sentence
is refuting a position it invented, and the fix is to delete the first half
and keep Y.

### AT-12. The bold reflex, S2

Every second phrase bolded, so the emphasis marks nothing. Bold is a claim
that this is the part to read first; four claims per paragraph is no claim.

The fix is a budget rather than a ban. One bolded span per paragraph at most,
and only where a reader skimming the page would need exactly that phrase.
Lists of bolded lead-ins are the one place density is fine, because there the
bold is structure and not emphasis.

### AT-13. The colon hook, S2

"Here's the thing:", "The result?", "But here's what most people miss:",
«И вот в чём дело:». A fragment that promises a revelation, then delivers an
ordinary sentence. It is the written form of a pause for effect, and it works
about once per piece.

Related and worse: the one-line paragraph used as a drumbeat, three or four
of them in a row, each landing a supposed insight. That rhythm is the most
recognisable shape of generated marketing prose in 2026.

### AT-14. Symmetrical headings, S3

Every heading the same grammatical shape and roughly the same length.

### AT-15. Over-signposting, S3

"First, let's look at…", "Now that we've covered…", "Let's dive into…".
Structure the reader can see does not need narrating.

## The dash rule in full

The em dash is banned where it is **rhetorical** and kept where it is
**grammatical**. That distinction is the rule. A pass that strips every dash
produces ungrammatical Russian, and a pass that keeps them all produces the
tone this file exists to remove.

**Rhetorical, and out.** The dash is doing a job that punctuation already has
a mark for:

| Written | Standing in for | Fix |
|---|---|---|
| "It works — and it works fast" | a comma | "It works, and it works fast" |
| "One thing matters — speed" | a colon | "One thing matters: speed" |
| "He left — it was too late" | a full stop | "He left. It was too late" |
| "The result — which nobody predicted — was…" | brackets or commas | "The result, which nobody predicted, was…" |

**Grammatical, and kept.** The language requires the mark, and removing it is
an error rather than a style choice:

- The Russian and Ukrainian copula, where the verb is absent by rule:
  «Москва — столица». English has no equivalent, which is why a global ban
  reads as reasonable in English and breaks Russian on the first line.
- Numeric and page ranges: «2020—2024», «с. 15—20».
- Direct speech in the Russian convention: «— Привет, — сказал он».
- A dash alone in a table cell, standing for "no value". It is a glyph doing
  the job of an empty string, not punctuation joining two clauses.

**Choosing the replacement is the work, and it is not mechanical.** The full
stop, the comma and the colon carry three different relationships between the
halves of the sentence. A comma joins, a colon promises that the second half
explains the first, a full stop says they are separate thoughts. Substituting
the wrong one damages the text more than the dash did, so the replacement is
chosen from the meaning, never by find-and-replace.

Where the two halves genuinely need no relationship stated, the strongest fix
is usually the full stop, because a dash is most often reached for to avoid
committing to one.

**What the linter proves and what it cannot.** `B062` errors on the patterns
that can be established without parsing grammar: a dash followed by a
coordinating conjunction, which is always a comma's job, and paired dashes
bracketing an aside inside one sentence. In a locale with no grammatical
dash, it errors on every dash that is not a range or direct speech, which is
the rule stated above. In a locale that has one, it cannot separate the
copula from the rhetorical remainder without a parser, so it reports the
density and leaves the judgement here. A check that claimed to know the
difference would be asserting what it has not measured.

## Density threshold

Above roughly **ten markers per 500 words**, editing does not work. The
result of polishing a piece that is mostly patterns is the same patterns with
better words. Say so and rewrite from the argument instead. That judgement is
part of the job, not a failure of it.

## The change-rate guard

After rewriting, estimate the proportion of the text that actually changed,
counting meaning-bearing changes and not punctuation or spacing.

| Change rate | Action |
|---|---|
| under 30% | ship it |
| 30 to 50% | ship it, and say the rate out loud |
| **over 50%** | **do not ship.** Report the rate and ask. |

Above half, this is no longer an edit. It may be the right rewrite, but that
is a decision with an owner, and quietly replacing someone's text while
calling it a polish is how meaning gets lost without anyone noticing.

Dash removal is the case most likely to breach the guard while looking
harmless, because it touches many lines and each touch is small. Punctuation
alone does not count toward the rate; a clause reordered to lose its dash
does.

## Semantic-preservation check, mandatory before output

Every one of these, every time. A failure means fix and re-check, not note
and proceed.

- [ ] Every number, date, currency and proper noun preserved exactly
- [ ] Causal direction unchanged, so no "X because Y" turned into "Y because X"
- [ ] No negation inverted: can/cannot, will/will not, is/is not
- [ ] Direct quotations untouched, inside their quotation marks
- [ ] The core claim and the conclusion unchanged
- [ ] Register and formality consistent with `voice.md`, not drifted upward
- [ ] Every remaining factual claim still traceable to `facts.md`
- [ ] Every dash removal re-read in place, because the replacement mark
      changes the relationship between the two halves

## What "human" is not

Not typos. Not slang. Not deliberate roughness. The target is a person who
writes well: someone with a position, specific knowledge, and a reason to
have written this. Add friction only where a real writer would have it, such
as a correction mid-thought, an admission of uncertainty, or an aside that
shows they know more than the paragraph needed.

And a piece that already reads naturally gets left alone. Editing text that
is fine to prove the pass ran is the failure mode of this whole activity.
