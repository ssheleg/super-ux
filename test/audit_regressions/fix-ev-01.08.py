#!/usr/bin/env python3
"""FIX-EV-01.02 — the outcome corpus for vision (sherlock audit, parent
FIX-EV-01; depends on the family harness of FIX-EV-01.01).

The corpus (evals/cases/vision.json) holds a positive (claim
provenance, UX-01/B030), a negative (routing), a no-op (unique text is not
spam, UX-02/B051), and two humanization cases (meaning preserved, and off
blocks nothing, UX-03/B060) — judged on ARTIFACTS through the family's
outcome-case contract, so vision can no longer pass an eval by its name
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
CASES = os.path.join(ROOT, "evals", "cases", "vision.json")
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
        assert c["skill"] == "vision"
        assert c["environment"]["case_digest"] == \
            hashlib.sha256(c["prompt"]["text"].encode()).hexdigest(), \
            f"{c['id']}: case_digest does not pin the frozen prompt"
        assert c["checks"]["outcome"], f"{c['id']}: no outcome checks"


def t_positive_has_anti_vision():
    c = next(x for x in manifest()["cases"] if "nine-sections" in x["id"])
    assert any((o.get("expect") or "") == "anti-vision" for o in c["checks"]["outcome"]), \
        "the positive case does not require the anti-vision section (UX-07)"


def t_negative_forbids_loading():
    neg = next(c for c in manifest()["cases"] if "negative" in c["id"])
    assert "vision" in neg["checks"]["load_trace"]["expect_not_loaded"]


def t_titles_host_and_missing():
    m = manifest()
    ru = next(c for c in m["cases"] if "russian-titles" in c["id"])
    assert any((o.get("expect") or "") == "essence" for o in ru["checks"]["outcome"]), \
        "the russian-titles case does not pin identity-by-ID (UX-07)"
    host = next(c for c in m["cases"] if "host-file" in c["id"])
    assert any((o.get("expect") or "") == "AGENTS.md" for o in host["checks"]["outcome"]), \
        "the host-file case does not pick the host's own instruction file (UX-06)"
    miss = next(c for c in m["cases"] if "missing-anti-vision" in c["id"])
    assert any((o.get("expect") or "") == "missing" for o in miss["checks"]["outcome"]), \
        "the missing-anti-vision case does not fail it (UX-07)"
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
    case("the positive case requires the anti-vision section",
         t_positive_has_anti_vision)
    case("the negative case forbids the skill from loading", t_negative_forbids_loading)
    case("titles/host-file/missing-section oracles are pinned",
         t_titles_host_and_missing)
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
