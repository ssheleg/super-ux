#!/usr/bin/env python3
"""XD-09.01 — the state-stress matrix (sherlock audit, XD-09).

The artifact under test (references/state-stress-matrix.md, linked from
ux-audit and synced into it):
* the row contract is scenario × state × action → expected VISIBLE result,
  plus a pressure dimension;
* four empties are four states (first-use / cleared / no-results /
  error-empty); an empty state does not require an illustration; an error is
  never dressed as empty;
* loading never simulates computation; drafts/retry/cancel/concurrent submit
  covered; financial actions stressed with fixtures only;
* content minimum/typical/maximum comes from the domain, synthetic is marked;
* evidence marking fixture/hypothesis/observed; a screenshot/trace attaches
  to exactly one row; a static source pass never promotes to implemented.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(ROOT, "plugins", "super-ux", "skills", "references",
                   "state-stress-matrix.md")
SYNCED = os.path.join(ROOT, "plugins", "super-ux", "skills", "ux-audit",
                      "references", "state-stress-matrix.md")
AUDIT = os.path.join(ROOT, "plugins", "super-ux", "skills", "ux-audit", "SKILL.md")

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def flat(path=SRC):
    with open(path, encoding="utf-8") as fh:
        return " ".join(fh.read().split())


def t_row_contract():
    d = flat()
    assert "scenario × state × action → expected visible result" in d
    assert '"the request succeeds" is a backend fact, not a visible result' in d
    for dim in ("content volume", "timing", "repetition", "interruption", "concurrency"):
        assert dim in d, f"pressure dimension {dim} missing"


def t_four_empties():
    d = flat()
    for st in ("**first-use**", "**cleared**", "**no-results**", "**error-empty**"):
        assert st in d, f"{st} missing"
    assert "No illustration is required" in d
    assert "NEVER dressed as empty" in d


def t_loading_and_actions():
    d = flat()
    assert "never simulates computation" in d
    for st in ("**drafts**", "**retry**", "**cancel**", "**concurrent submit**"):
        assert st in d, f"{st} missing"
    assert "no real charge, refund or transfer is ever triggered" in d


def t_content_volumes_from_domain():
    d = flat()
    assert "minimum" in d and "typical" in d and "maximum" in d
    assert "not from taste" in d
    assert "Synthetic content is marked synthetic" in d


def t_evidence_marking():
    d = flat()
    for m in ("**fixture**", "**hypothesis**", "**observed**"):
        assert m in d, f"{m} missing"
    assert "attaches to EXACTLY ONE row" in d
    assert "A static source pass never promotes a scenario to implemented." in d


def t_linked_and_synced():
    a = flat(AUDIT)
    assert "state-stress-matrix.md" in a, "ux-audit does not link the matrix"
    assert os.path.isfile(SYNCED), "the matrix did not sync into ux-audit"
    assert flat() == flat(SYNCED), "the synced copy drifted"


def main():
    case("the row contract names visible results and pressure dimensions",
         t_row_contract)
    case("four empties are four states; no mandatory illustration; error never empty",
         t_four_empties)
    case("loading honest; drafts/retry/cancel/concurrent covered; finance fixtures only",
         t_loading_and_actions)
    case("content volumes come from the domain; synthetic marked",
         t_content_volumes_from_domain)
    case("evidence marking + one-row attachment + no static promotion",
         t_evidence_marking)
    case("linked from ux-audit and synced", t_linked_and_synced)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
