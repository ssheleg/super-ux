# Machine-drafting markers — detect, fix, and know when to stop

Text drafted by a model has measurable habits. This file names them, grades
them, and — more importantly — bounds the repair, because an unbounded
"make it sound human" pass destroys meaning while improving rhythm.

## Contents

- [Severity](#severity)
- [Naturalness grade — applied to the result](#naturalness-grade--applied-to-the-result)
- [The markers](#the-markers)
- [Density threshold](#density-threshold)
- [The change-rate guard](#the-change-rate-guard)
- [Semantic-preservation check — mandatory before output](#semantic-preservation-check--mandatory-before-output)
- [What "human" is not](#what-human-is-not)


Used by the `Humanize` mode of `copywriting` and by `B060` in
`brand_lint.py`. Voice, once the generic is gone, comes from
[voice-packs.md](voice-packs.md) via the project's `voice.md`.

## Severity

| Grade | Meaning |
|---|---|
| **S1** | decisive on its own — one instance reads as machine-drafted |
| **S2** | one or two are fine; three or more is a signal |
| **S3** | weak alone, decisive when stacked with others |

`B060` warns at any S1 or three S2, and errors at three S1.

## Naturalness grade — applied to the result

After the rewrite, not the input:

- **A** — no S1, at most two S2. Reads as written by a person.
- **B** — one or two S1, or three to five S2. Natural with minor traces.
- **C** — three or more S1, or six or more S2. Traces are obvious; another
  pass is warranted.
- **D** — violations across several categories, or the change-rate guard
  fired.

## The markers

### Vocabulary — S1

`delve`, `landscape` (figurative), `crucial`, `vital`, `pivotal`,
`leverage` (as a verb), `robust`, `comprehensive`, `holistic`, `foster`,
`facilitate`, `navigate` (figurative), `seamless`, `tapestry`, `realm`,
`testament to`, `underscores`, `it's worth noting`.

Never simply delete: replace with the thing the word was standing in for.
`robust` → the number. `facilitate` → `help`. `crucial` → state the
consequence and let it be self-evidently important.

### Hedging chains — S1

"It is important to note that", "It is worth mentioning that", "One might
argue that", "In many cases", "It goes without saying", "Needless to say".

These exist because the drafting process is uncertain and hedges by default.
A person hedges when they are actually uncertain, which is much less often.

### Uniform sentence length — S1

Every sentence 18–22 words. The most reliable tell and the least noticed,
because no individual sentence is wrong.

The fix is rhythm, not vocabulary: break long sentences, let a short one land
after a long one, use a fragment where it serves emphasis, and let one
sentence run when the thought genuinely needs the room.

### Identical paragraph shape — S1

Statement → explanation → example → bridge, every paragraph, forever. Real
writing varies: a one-sentence paragraph, a question answered immediately, a
short list dropped into prose, an aside, a correction.

### Vagueness where a fact belongs — S1

"Many companies", "studies show", "significantly improved", "leading
brands", "a lot of". Each is a place where a specific claim was avoided
because a specific claim can be checked.

Replace with the real figure from `facts.md`, or say plainly that you do not
have one. Honest absence beats confident vagueness, and it is also the
`B030` rule from the other side.

### The rule-of-three habit — S2

Three adjectives, three examples, three-item lists, everywhere. Three is a
good number sometimes; it is not a good number always.

### Em-dash reflex — S2

One or two in a piece is normal. One every other paragraph is a fingerprint.

### False balance — S2

"While X has advantages, Y also has merits" as a way of avoiding a position.
If the piece has a view, state it.

### The summary conclusion — S2

"In conclusion, we explored X, Y and Z. By implementing these strategies…"
A restatement of the introduction. A real ending either adds something or
stops.

### Symmetrical headings — S3

Every heading the same grammatical shape and roughly the same length.

### Over-signposting — S3

"First, let's look at…", "Now that we've covered…", "Let's dive into…".
Structure the reader can see does not need narrating.

## Density threshold

Above roughly **ten markers per 500 words**, editing does not work. The
result of polishing a piece that is mostly patterns is the same patterns with
better words. Say so and rewrite from the argument instead — that judgement
is part of the job, not a failure of it.

## The change-rate guard

After rewriting, estimate the proportion of the text that actually changed —
meaning-bearing changes, not punctuation and spacing.

| Change rate | Action |
|---|---|
| under 30% | ship it |
| 30–50% | ship it, and say the rate out loud |
| **over 50%** | **do not ship.** Report the rate and ask. |

Above half, this is no longer an edit. It may be the right rewrite, but that
is a decision with an owner, and quietly replacing someone's text while
calling it a polish is how meaning gets lost without anyone noticing.

## Semantic-preservation check — mandatory before output

Every one of these, every time. A failure means fix and re-check, not note
and proceed.

- [ ] Every number, date, currency and proper noun preserved exactly
- [ ] Causal direction unchanged — no "X because Y" turned into "Y because X"
- [ ] No negation inverted — can/cannot, will/will not, is/is not
- [ ] Direct quotations untouched, inside their quotation marks
- [ ] The core claim and the conclusion unchanged
- [ ] Register and formality consistent with `voice.md`, not drifted upward
- [ ] Every remaining factual claim still traceable to `facts.md`

## What "human" is not

Not typos. Not slang. Not deliberate roughness. The target is a person who
writes well: someone with a position, specific knowledge, and a reason to
have written this. Add friction only where a real writer would have it — a
correction mid-thought, an admission of uncertainty, an aside that shows they
know more than the paragraph needed.

And a piece that already reads naturally gets left alone. Editing text that
is fine to prove the pass ran is the failure mode of this whole activity.
