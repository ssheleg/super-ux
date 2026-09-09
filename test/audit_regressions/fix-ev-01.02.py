#!/usr/bin/env python3
"""FIX-EV-01.02 — the outcome corpus for brand-voice (sherlock audit, parent
FIX-EV-01; depends on the family harness of FIX-EV-01.01).

The corpus (evals/cases/brand-voice.json) holds a positive (claim
provenance, UX-01/B030), a negative (routing), a no-op (unique text is not
spam, UX-02/B051), and two humanization cases (meaning preserved, and off
blocks nothing, UX-03/B060) — judged on ARTIFACTS through the family's
outcome-case contract, so brand-voice can no longer pass an eval by its name
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
CASES = os.path.join(ROOT, "evals", "cases", "brand-voice.json")
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
        assert c["skill"] == "brand-voice"
        assert c["environment"]["case_digest"] == \
            hashlib.sha256(c["prompt"]["text"].encode()).hexdigest(), \
            f"{c['id']}: case_digest does not pin the frozen prompt"
        assert c["checks"]["outcome"], f"{c['id']}: no outcome checks"


def t_positive_flags_the_unsupported_claim():
    c = next(x for x in manifest()["cases"] if "claim-provenance" in x["id"])
    assert any(o.get("expect") == "unresolved" for o in c["checks"]["outcome"]), \
        "the provenance case does not pin the unsupported-claim flag"


def t_negative_forbids_loading():
    neg = next(c for c in manifest()["cases"] if "negative" in c["id"])
    assert "brand-voice" in neg["checks"]["load_trace"]["expect_not_loaded"]


def t_noop_pins_zero_spam():
    c = next(x for x in manifest()["cases"] if "no-repetition" in x["id"])
    assert any("findings: 0" in (o.get("expect") or "") for o in c["checks"]["outcome"]), \
        "unique text is not pinned to zero spam findings"


def t_humanization_preserves_and_off_blocks_nothing():
    m = manifest()
    keep = next(c for c in m["cases"] if "preserves-meaning" in c["id"])
    assert any((o.get("expect") or "") == "never" for o in keep["checks"]["outcome"]), \
        "the negation-preservation oracle is missing"
    off = next(c for c in m["cases"] if "off-blocks-nothing" in c["id"])
    assert any("no rewrite" in (o.get("expect") or "") for o in off["checks"]["outcome"]), \
        "the humanization-off case does not pin the no-rewrite outcome"
    flat = " ".join(json.dumps(m, ensure_ascii=False).split())
    for needle in ("actual output oracle", "raw result", "with/without-skill",
                   "grader convenience"):
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
    case("the positive case flags the unsupported claim (B030)",
         t_positive_flags_the_unsupported_claim)
    case("the negative case forbids the skill from loading", t_negative_forbids_loading)
    case("the no-op case pins zero spam findings (B051)", t_noop_pins_zero_spam)
    case("humanization preserves meaning and off blocks nothing (B060)",
         t_humanization_preserves_and_off_blocks_nothing)
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
