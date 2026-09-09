#!/usr/bin/env python3
"""FIX-EV-01.02 — the outcome corpus for ux-flows (sherlock audit, parent
FIX-EV-01; depends on the family harness of FIX-EV-01.01).

The corpus (evals/cases/ux-flows.json) holds a positive (claim
provenance, UX-01/B030), a negative (routing), a no-op (unique text is not
spam, UX-02/B051), and two humanization cases (meaning preserved, and off
blocks nothing, UX-03/B060) — judged on ARTIFACTS through the family's
outcome-case contract, so ux-flows can no longer pass an eval by its name
being picked.

Standard library only.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CASES = os.path.join(ROOT, "evals", "cases", "ux-flows.json")
HARNESS = os.path.expanduser("~/DATA/sshlg-skills/test/outcome_harness.py")

failures = []
not_run = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def manifest():
    with open(CASES, encoding="utf-8") as fh:
        return json.load(fh)


def t_cases_are_structurally_valid():
    m = manifest()
    ids = [c["id"] for c in m["cases"]]
    assert len(ids) == len(set(ids)) and len(ids) >= 5
    for c in m["cases"]:
        assert c["schema_version"] == "outcome-case/1"
        assert c["skill"] == "ux-flows"
        assert c["environment"]["case_digest"] == \
            hashlib.sha256(c["prompt"]["text"].encode()).hexdigest(), \
            f"{c['id']}: case_digest does not pin the frozen prompt"
        assert c["checks"]["outcome"], f"{c['id']}: no outcome checks"


def t_positive_is_pattern_not_proof():
    c = next(x for x in manifest()["cases"] if "funnel-is-pattern" in x["id"])
    assert any((o.get("expect") or "") == "frequent pattern" for o in c["checks"]["outcome"]), \
        "the funnel case does not pin pattern-not-proof (UX-09)"


def t_negative_forbids_loading():
    neg = next(c for c in manifest()["cases"] if "negative" in c["id"])
    assert "ux-flows" in neg["checks"]["load_trace"]["expect_not_loaded"]


def t_loading_figma_and_payment():
    m = manifest()
    ld = next(c for c in m["cases"] if "no-fake-loading" in c["id"])
    assert any((o.get("expect") or "") == "no timer" for o in ld["checks"]["outcome"]), \
        "the loading case does not forbid fake loading theatre (UX-10)"
    fg = next(c for c in m["cases"] if "figma-fallback" in c["id"])
    assert "FIGMA_TOKEN" in fg["checks"]["tool"][0]["command"], \
        "the Figma case has no probe"
    assert any((o.get("expect") or "") == "deferred" for o in fg["checks"]["outcome"]), \
        "the Figma fallback does not reach a build state (UX-11)"
    pay = next(c for c in m["cases"] if "local-payment" in c["id"])
    assert any((o.get("expect") or "") == "Stripe CLI" for o in pay["checks"]["outcome"]), \
        "the payment case does not pin local testability (UX-14)"
    flat = " ".join(json.dumps(m, ensure_ascii=False).split())
    for needle in ("actual output oracle", "raw result", "with/without-skill",
                   "NOT_RUN", "grader convenience"):
        assert needle in flat, f"the manifest no longer records {needle!r}"


def t_family_harness_validates_each_case_where_present():
    if not os.path.isfile(HARNESS):
        not_run.append("family harness absent — case validation NOT_RUN (never PASS)")
        return
    for c in manifest()["cases"]:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(c, fh)
            path = fh.name
        try:
            r = subprocess.run([sys.executable, HARNESS, path],
                               capture_output=True, text=True, timeout=60)
            assert r.returncode == 0, f"{c['id']} rejected:\n{r.stdout}"
        finally:
            os.unlink(path)


def main():
    case("every case is structurally valid, none is name-picking",
         t_cases_are_structurally_valid)
    case("the positive funnel case is pattern, not proof",
         t_positive_is_pattern_not_proof)
    case("the negative case forbids the skill from loading", t_negative_forbids_loading)
    case("loading/figma/payment oracles are pinned", t_loading_figma_and_payment)
    case("the family harness validates each case (where present)",
         t_family_harness_validates_each_case_where_present)
    for n in not_run:
        print(f"  NOT_RUN  {n}")
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
