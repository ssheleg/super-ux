#!/usr/bin/env python3
"""FIX-UX-01.01 — claim provenance: a claim binds to a row, not to digits
(sherlock audit, UX-01).

The finding, reproduced live: all public figures were pooled into one set with
no subject, unit, denominator or claim→fact reference — the single fact
"supported integrations = 500" licensed "We serve 500 million paying
customers" (check_facts returned []). Bare numbers under 100 were never
extracted and any 19xx/20xx token was declared a year, so "99 languages" and
"2026 integrations" escaped entirely.

The fix under test (doc leaf — the schema and the narrowed promise):
* brand-contract.md binds claim-id → fact-id with subject, unit, population,
  date and declared transformations; a numeric coincidence is not proof; an
  unresolved claim prints UNVERIFIED, never a silent pass;
* B030's promise is narrowed to token-level verification, subject match named
  as the semantic audit's job, and the extractor's blind spots stated;
* the binding rules are RUN as behaviour on the audit's own example.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DOC = os.path.join(ROOT, "plugins", "super-ux", "skills", "brand-voice",
                   "references", "brand-contract.md")

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def doc():
    with open(DOC, encoding="utf-8") as fh:
        return " ".join(fh.read().split())


def t_schema_is_stated():
    d = doc()
    for needle in ("A claim binds to a row, not to digits",
                   "A numeric coincidence is not proof",
                   "500 million paying customers",
                   "must match the row's subject",
                   "inside the row's `Checked`→`Review by` window",
                   "only those the row declares",
                   "unresolved and prints as UNVERIFIED",
                   "a reader's, not a regex's"):
        assert needle in d, f"brand-contract.md no longer states {needle!r}"


def t_b030_promise_is_narrowed():
    d = doc()
    assert "a figure in public copy has no row in `facts.md` |" not in d, \
        "B030 still promises full figure verification — the over-promise itself"
    assert "a KNOWN numeric token in public copy has no row in `facts.md`" in d
    assert "prints UNVERIFIED, never a silent pass" in d


def t_blind_spots_are_stated_not_papered():
    d = doc()
    assert "bare numbers under 100" in d, "the <100 extraction gap is hidden"
    assert '"2026 integrations" is a figure, not a year' in d, \
        "year tokens are still unconditionally excluded"


# ---------------- the binding, run as behaviour


ROWS = [{"fact": "supported integrations", "value": "500", "subject": "integrations",
         "unit": "count", "population": "catalog", "transformations": ["round down"]}]


def resolve(claim, rows):
    """The doc's rule: every axis must match; digits alone resolve nothing."""
    for r in rows:
        if (claim.get("fact") == r["fact"] and claim.get("subject") == r["subject"]
                and claim.get("unit") == r["unit"]
                and claim.get("population") == r["population"]
                and claim.get("transformation", "none") in r["transformations"] + ["none"]):
            return "resolved"
    return "UNVERIFIED"


def t_coincidence_resolves_nothing():
    million_customers = {"fact": "supported integrations", "value": "500",
                         "subject": "customers", "unit": "millions", "population": "paying"}
    assert resolve(million_customers, ROWS) == "UNVERIFIED", \
        "500 integrations licensed 500 million paying customers — the finding itself"
    honest = {"fact": "supported integrations", "value": "500",
              "subject": "integrations", "unit": "count", "population": "catalog"}
    assert resolve(honest, ROWS) == "resolved"


def t_unknown_claim_stays_unresolved():
    unknown = {"fact": "customers served", "value": "500", "subject": "customers",
               "unit": "millions", "population": "paying"}
    assert resolve(unknown, ROWS) == "UNVERIFIED", "an unknown claim silently passed"
    undeclared = {"fact": "supported integrations", "value": "1000",
                  "subject": "integrations", "unit": "count", "population": "catalog",
                  "transformation": "double it"}
    assert resolve(undeclared, ROWS) == "UNVERIFIED", \
        "an undeclared transformation resolved — a new fact needs its own row"


def main():
    case("the claim provenance schema is stated", t_schema_is_stated)
    case("B030's promise is narrowed to the token level", t_b030_promise_is_narrowed)
    case("the extractor's blind spots are stated, not papered over",
         t_blind_spots_are_stated_not_papered)
    case("a numeric coincidence resolves nothing", t_coincidence_resolves_nothing)
    case("an unknown claim (and an undeclared transformation) stays UNVERIFIED",
         t_unknown_claim_stays_unresolved)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
