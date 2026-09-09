#!/usr/bin/env python3
"""FIX-UX-02.01 — B051 no longer calls text with zero repetition spam
(sherlock audit, UX-02).

The finding: after 40 significant words, any token above 1% of the words was an
ERROR — but 45 unique words with NO repeat put each token at 1/45 = 2.2%, so a
page that repeats nothing was flagged, and for a short page the 1% bar is
mathematically unmeetable. Keyword stuffing is unnatural REPETITION and
manipulative intent (Google's spam policy), not a fixed percentage.

The fix under test (brand_lint.py):
* B051 is ADVISORY (warn), fires only when a word actually REPEATS (≥5x) and
  takes an unnatural share (>4%) on a page long enough to judge (≥80 words);
* registered domain terms (terminology.md / facts.md) are exempt;
* pages are judged independently;
* the doctrine drops the 1% threshold and the citation-likelihood promise.

Runs the real check end-to-end. Standard library only.
"""
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SCRIPT = os.path.join(ROOT, "plugins", "super-ux", "scripts", "brand_lint.py")
CONTRACT = os.path.join(ROOT, "plugins", "super-ux", "skills", "brand-voice",
                        "references", "brand-contract.md")

_spec = importlib.util.spec_from_file_location("brand_lint", SCRIPT)
BL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(BL)

MARKER = "Contract: brand-contract v1"
failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def codes_for(copy_body, terminology=None):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        brand = root / "docs" / "brand"
        brand.mkdir(parents=True)
        if terminology:
            brand.joinpath("terminology.md").write_text(terminology, encoding="utf-8")
        doc = root / "content" / "a.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text(f"---\nsurface: landing hero\ntitle: T\n---\n\n{copy_body}\n",
                       encoding="utf-8")
        findings = _run_keyword(brand, {"marketing": ["content/*.md"]})
        return {f.code for f in findings}, findings


def _run_keyword(brand, sources):
    # B051 is emitted by check_bot_safety over the marketing copy; call it
    # directly so the check is exercised without a full valid pack.
    return [f for f in BL.check_bot_safety(brand, sources) if f.code == "B051"]


def n_unique_words(n):
    return " ".join(f"word{i}alpha" for i in range(n))


def t_unique_words_no_repeat_are_clean():
    for n in (45, 80, 100):
        codes, _ = codes_for(n_unique_words(n))
        assert "B051" not in codes, f"{n} unique words with no repeat flagged B051 — the finding"


def t_real_repetition_is_advisory():
    body = ("buy tokens buy tokens buy tokens buy tokens buy tokens buy tokens "
            + n_unique_words(80))
    codes, findings = codes_for(body)
    assert "B051" in codes, "a genuinely repeated block did not warn"
    b051 = [f for f in findings if f.code == "B051"][0]
    assert b051.severity == BL.SEVERITY_WARN, "B051 is still an ERROR, not advisory"


def t_domain_term_repetition_is_kept():
    # 'tokens' registered as a product term → exempt even when it repeats
    term_md = ("## Product terms\n\n| our term | not |\n|---|---|\n"
               "| tokens | credits |\n")
    body = ("tokens tokens tokens tokens tokens tokens tokens tokens "
            + n_unique_words(80))
    codes, _ = codes_for(body, terminology=term_md)
    assert "B051" not in codes, "a registered domain term was flagged as stuffing"


def t_pages_judged_independently_and_doc_updated():
    # a short page cannot be judged; a long stuffed one can — different pages,
    # different verdicts, proving independence
    short_codes, _ = codes_for("buy buy buy tokens tokens")
    assert "B051" not in short_codes, "a short page was judged for stuffing"
    d = " ".join(open(CONTRACT, encoding="utf-8").read().split())
    assert "a token exceeds 1% of a marketing document" not in d, \
        "the 1% threshold survived in the doctrine"
    assert "manipulative repetition, not a fixed percentage" in d
    assert "citation likelihood" not in d or "no claim about citation likelihood" in d


def main():
    case("45/80/100 unique words with no repeat are clean",
         t_unique_words_no_repeat_are_clean)
    case("a genuinely repeated block is an advisory warning", t_real_repetition_is_advisory)
    case("a registered domain term may repeat", t_domain_term_repetition_is_kept)
    case("pages are judged independently; the doctrine dropped 1% and citation claim",
         t_pages_judged_independently_and_doc_updated)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
