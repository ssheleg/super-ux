#!/usr/bin/env python3
"""FIX-UX-01.02 — B030 scoped validation: provenance link + unit + precision +
date type, not a coincidence of digits (sherlock audit, UX-01, code side).

The finding: check_facts resolved a public figure by matching its bare digits
against a set of known numbers — so one row `supported integrations = 500`
licensed `500 million paying customers`; a year-form token was excluded
unconditionally, so `2026 integrations` was waved through; precision was
ignored, so `$3.10` sourced `$3.1`.

The fix under test (brand_lint.py):
* a figure resolves against a SIGNATURE (digits, unit, scale, precision), so
  three counterexamples — a scale mismatch, a precision mismatch, and a
  year-form figure with no row — no longer PASS;
* a legitimate known claim still passes;
* a year is NOT excluded automatically: `2026 integrations` is checked,
  `Apple HIG 2025` / `in 2026` / `2020—2024` stay dates;
* subject/population confirmation is explicitly left to the semantic review.

Runs the real check_facts end-to-end on a temp pack, and the signature helpers
directly. Standard library only.
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


def codes_for(facts_rows, copy_body):
    """Run the REAL check_facts over a temp pack and return the B030/B031 codes."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        brand = root / "docs" / "brand"
        brand.mkdir(parents=True)
        header = (MARKER + "\n\n| Fact | Value | Source | Checked | Review by | Public |\n"
                  "|---|---|---|---|---|---|\n")
        (brand / "facts.md").write_text(header + facts_rows, encoding="utf-8")
        doc = root / "content" / "a.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text(f"---\nsurface: landing hero\ntitle: T\n---\n\n{copy_body}\n",
                       encoding="utf-8")
        findings = BL.check_facts(brand, {"marketing": ["content/*.md"]})
        return {f.code for f in findings}


ROW_INTEGRATIONS = "| integrations | 500+ | registry | 2026-08-01 | 2099-01-01 | yes |\n"
ROW_COST = "| run cost | $3.10 | billing | 2026-08-01 | 2099-01-01 | yes |\n"


# ---------------- the three counterexamples must NOT pass


def t_scale_mismatch_blocks():
    codes = codes_for(ROW_INTEGRATIONS, "We serve 500 million paying customers.")
    assert "B030" in codes, "500 (integrations) licensed 500 MILLION customers — the finding"


def t_precision_mismatch_blocks():
    codes = codes_for(ROW_COST, "Median run cost is $3.1.")
    assert "B030" in codes, "$3.10 sourced $3.1 — precision was ignored"


def t_year_form_figure_blocks():
    codes = codes_for(ROW_INTEGRATIONS, "Now spanning 2026 integrations.")
    assert "B030" in codes, "a year-form figure (2026 integrations) was auto-excluded"


# ---------------- a legitimate known claim passes; real dates stay dates


def t_legit_known_claim_passes():
    codes = codes_for(ROW_INTEGRATIONS, "Reaches 500+ agents across the catalog.")
    assert "B030" not in codes, "a claim matching link+unit+scale+precision was blocked"


def t_real_years_stay_dates():
    for copy in ("Guidance from Apple HIG 2025 and Material 3.",
                 "Shipping since 2019.",
                 "The window runs 2020—2024 without a gap."):
        codes = codes_for(ROW_INTEGRATIONS, copy)
        assert "B030" not in codes, f"a genuine date was read as a figure: {copy!r}"


# ---------------- the signature model, unit-level


def t_signatures_separate_the_axes():
    assert BL._signature("500", "million") != BL._signature("500"), "scale is not in the signature"
    assert BL._signature("$3.10") != BL._signature("$3.1"), "precision is not in the signature"
    assert BL._signature("42%") != BL._signature("42"), "unit is not in the signature"
    assert BL._signature("500", "") in BL._row_signatures("500+"), \
        "a bound marker no longer sources the bare figure"
    # subject/population is NOT in the signature — that is the semantic review's job
    src = " ".join(open(SCRIPT, encoding="utf-8").read().split())
    assert "semantic review" in src, "the doc no longer defers subject match to the semantic review"


def main():
    case("a scale mismatch (500 vs 500 million) is blocked", t_scale_mismatch_blocks)
    case("a precision mismatch ($3.10 vs $3.1) is blocked", t_precision_mismatch_blocks)
    case("a year-form figure with no row is blocked", t_year_form_figure_blocks)
    case("a legitimate known claim passes", t_legit_known_claim_passes)
    case("genuine dates are not read as figures", t_real_years_stay_dates)
    case("the signature separates digits/unit/scale/precision; subject stays semantic",
         t_signatures_separate_the_axes)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
