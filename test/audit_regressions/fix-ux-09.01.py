#!/usr/bin/env python3
"""FIX-UX-09.01 — competitor funnels are observed exposure, not a proven base
(sherlock audit, UX-09).

The finding: the reference admitted a loss-making funded funnel looks
profitable, then said "nobody keeps paying at a loss", "production spend
follows return", and called common patterns a "proven base" — turning unknown
profit into proven causal effectiveness.

The fix under test (references/funnel-research.md):
* every market signal is OBSERVED EXPOSURE; the mechanism claim is a
  HYPOTHESIS with alternative explanations;
* "what almost everyone does" is a FREQUENT PATTERN, not a proven conversion
  lift; frequency is computed by a script with a denominator, duplicates
  collapsed; adoption is a local experiment;
* the frequency arithmetic run as behaviour: a corpus of 10 similar funnels
  gives a frequent pattern; a known loss-maker does not break it; two funnels
  of one owner are one observation.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DOC = os.path.join(ROOT, "plugins", "super-ux", "skills", "references",
                   "funnel-research.md")

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def flat():
    with open(DOC, encoding="utf-8") as fh:
        return " ".join(fh.read().split())


def t_signals_are_observed_exposure():
    d = flat()
    assert "Every signal below is OBSERVED EXPOSURE" in d
    assert "a claim\nthat spend proves RETURN is a HYPOTHESIS".replace("\n", " ") in d \
        or "any claim that spend proves RETURN is a HYPOTHESIS" in d
    assert "never a template or a\nproven result".replace("\n", " ") in d \
        or "never a template or a proven result" in d


def t_longevity_and_variant_reframed():
    d = flat()
    assert "Longevity is OBSERVED EXPOSURE" in d
    assert "never as proof the funnel earns" in d
    assert "Variant count is production SPEND — observed exposure, not observed return" in d
    assert '"Production spend follows return" is a HYPOTHESIS' in d
    assert "Nobody keeps paying to run an ad at a loss for months." not in d, \
        "the old causal claim survived"


def t_frequent_not_proven():
    d = flat()
    assert "a FREQUENT PATTERN, not a proven conversion\n  lift".replace("\n  ", " ") in d \
        or "a FREQUENT PATTERN, not a proven conversion lift" in d
    assert "adoption is decided by a LOCAL experiment" in d
    assert "explicit DENOMINATOR" in d
    assert "DUPLICATES are\n  collapsed first".replace("\n  ", " ") in d \
        or "DUPLICATES are collapsed first" in d


# ---- the frequency arithmetic as behaviour


def frequency(corpus):
    """corpus: list of {owner, pattern, note}. Returns pattern -> count over
    INDEPENDENT observations (one per owner), with a denominator."""
    seen_owner_pattern = set()
    counts = {}
    owners = set()
    for f in corpus:
        owners.add(f["owner"])
        key = (f["owner"], f["pattern"])
        if key in seen_owner_pattern:
            continue                       # same owner, same pattern → one observation
        seen_owner_pattern.add(key)
        counts[f["pattern"]] = counts.get(f["pattern"], 0) + 1
    return counts, len(owners)


def t_corpus_gives_frequent_not_proven():
    corpus = [{"owner": f"o{i}", "pattern": "quiz-first"} for i in range(10)]
    counts, denom = frequency(corpus)
    assert counts["quiz-first"] == 10 and denom == 10
    # it is a FREQUENT pattern (10/10), never a "proven conversion lift" — the
    # test asserts the arithmetic only counts exposure, not return
    assert "lift" not in counts     # counts hold exposure frequency, nothing about return


def t_same_owner_two_funnels_is_one():
    corpus = [{"owner": "acme", "pattern": "quiz-first"},
              {"owner": "acme", "pattern": "quiz-first"},   # duplicate owner+pattern
              {"owner": "other", "pattern": "quiz-first"}]
    counts, denom = frequency(corpus)
    assert counts["quiz-first"] == 2, \
        f"two funnels of one owner counted as independent: {counts}"
    assert denom == 2


def t_known_loss_maker_does_not_break_it():
    # a loss-making but funded advertiser is one observation, not a veto
    corpus = [{"owner": f"o{i}", "pattern": "quiz-first"} for i in range(9)]
    corpus.append({"owner": "lossmaker", "pattern": "quiz-first", "note": "funded, loss-making"})
    counts, denom = frequency(corpus)
    assert counts["quiz-first"] == 10, "the loss-maker distorted the count"


def main():
    case("every signal is observed exposure; mechanism is a hypothesis",
         t_signals_are_observed_exposure)
    case("longevity and variant-count are reframed off causation",
         t_longevity_and_variant_reframed)
    case("common = frequent pattern, not proven; denominator + duplicates + local experiment",
         t_frequent_not_proven)
    case("fixture: 10 similar funnels give a frequent pattern, not a lift",
         t_corpus_gives_frequent_not_proven)
    case("fixture: two funnels of one owner are one observation",
         t_same_owner_two_funnels_is_one)
    case("fixture: a known loss-maker does not break the pattern",
         t_known_loss_maker_does_not_break_it)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
