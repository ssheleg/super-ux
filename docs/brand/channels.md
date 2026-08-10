Contract: brand-contract v1

# Channels

One record per surface. `Register` is deltas against the five axes in
`voice.md` — a register moves the axes, never the invariants.

`Forbidden` always carries both halves, even when one is `none`. Platform
physics and brand choice written on one line become indistinguishable within
a quarter, and then nobody can tell which is safe to revisit when the
platform changes.

super-ux has two surfaces and no more: a terminal and a README. The store,
ads, email and social records are deleted rather than left empty — a
surface described but never shipped is a register nobody maintains, and the
audit would judge copy that does not exist.

---

## Product surfaces

### primary action

```
Register:   humor -3, density +1
Format:     imperative naming the outcome; the menu label is the action
Limits:     78 characters — the line must not wrap in an 80-column terminal
Forbidden:  physics: no colour as the only signal, no cursor-relative layout in non-TTY | brand: "Submit", "OK", bare nouns
CTA:        this surface is the CTA
Proof:      none
Locales:    the length coefficient applies to the 78-character limit
```

### error

```
Register:   humor -3, density +1, distance -1
Format:     `error: ` then what happened, in the user's terms, then what was not touched
Limits:     78 characters
Forbidden:  physics: none | brand: humor, "unexpected", blame, bare codes, exclamation marks
CTA:        the recovery, on the same screen — `(use --force to overwrite)`
Proof:      none
Locales:    the `error: ` prefix is not translated; it is the vocabulary
```

An error here can cost the user a scenario base they wrote by hand. This is
the surface where the no-levity invariant is not a style preference.

### empty state

```
Register:   humor -2, density -1
Format:     name the empty thing and the one action that fills it
Limits:     78 characters
Forbidden:  physics: none | brand: apology, "oops", pretending a choice was a mistake
CTA:        the action that would fill it, or none when the state is valid
Proof:      none
Locales:    none
```

`Nothing selected.` is the whole of this surface. Choosing nothing is a
choice, and the copy must not read as a failure to choose.

### destructive confirm

```
Register:   humor -3, density +1
Format:     name what would be lost, by path, before naming the flag that would do it
Limits:     78 characters
Forbidden:  physics: none | brand: humor, emoji, "just", minimising the loss
CTA:        the explicit flag — never a bare yes/no
Proof:      none
Locales:    none
```

There is no interactive destructive confirm: `--force` is the confirmation,
and `keep:` proves what was never at risk. If one is ever added, this record
is the contract it obeys.

---

## Marketing surfaces

### landing hero

```
Register:   density -1
Format:     the failure the reader recognises, then the mechanism, then the limit
Limits:     title 60, subtitle 160
Forbidden:  physics: none | brand: benchmark claims without a harness, "blazingly fast", claiming a category nobody uses, hiding limits in a FAQ
CTA:        one install command, copyable
Proof:      one figure, sourced in facts.md
Locales:    en only
```

The README is this surface and also the npm package page. Its reader has
not opted in yet: it is the one place density drops, and the only place the
`peer-builder` failure mode — assuming the reader already knows what "the
chain" is — actually costs something.

### changelog

```
Register:   distance -1, humor +1, density +1
Format:     what changed, why it was wrong before, what a reader must do
Limits:     none
Forbidden:  physics: none | brand: "various improvements", a fix with no symptom, a version with no date
CTA:        the upgrade command when action is required
Proof:      the finding or the audit that produced the change
Locales:    en only
```

Written for developers, which is why `CHANGELOG.md` is not a `Sources:`
target: it documents the repository, not the product.
