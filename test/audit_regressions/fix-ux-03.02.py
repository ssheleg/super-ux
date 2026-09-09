#!/usr/bin/env python3
"""FIX-UX-03.02 — B060 semantic safety: advisory, never a count-driven gate
(sherlock audit, UX-03, code side).

The finding (with FIX-UX-03.01 the doctrine): brand_lint escalated B060 to an
ERROR at three S1 markers, so marker-rich but correct copy BLOCKED the run —
a marker count treated as proof of authorship.

The fix under test (brand_lint.py):
* B060 severity is always WARN — no escalation by count;
* marker-rich correct text does not block (the linter exits 0 on warnings);
* the check never rewrites, so a number, a negation and a causal statement are
  preserved verbatim (semantic-preservation no-ops).

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

_spec = importlib.util.spec_from_file_location("brand_lint", SCRIPT)
BL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(BL)

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def findings_for(body):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        brand = root / "docs" / "brand"
        brand.mkdir(parents=True)
        doc = root / "content" / "a.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text(f"---\nsurface: landing hero\ntitle: T\n---\n\n{body}\n", encoding="utf-8")
        return BL.check_ai_tells(brand, {"marketing": ["content/*.md"]})


# many S1 markers in one page
MARKER_RICH = ("It is important to note that teams delve into this. In conclusion, "
               "it is worth noting the result. Moreover, it is worth noting again.")


def t_b060_is_always_a_warning():
    b060 = [f for f in findings_for(MARKER_RICH) if f.code == "B060"]
    assert b060, "the marker-rich text produced no B060 at all — the check went silent"
    for f in b060:
        assert f.severity == BL.SEVERITY_WARN, \
            f"B060 escalated to {f.severity} by count — it must stay advisory"


def t_no_count_escalation():
    # source-level: the escalation branch is gone
    src = open(SCRIPT, encoding="utf-8").read()
    assert 'severity = SEVERITY_ERROR if len(hits) >= 3' not in src, \
        "the count-driven ERROR escalation survived"
    assert '"B060", SEVERITY_WARN' in src, "B060 is not pinned to WARN"


def t_marker_rich_text_does_not_block():
    # the linter exits 1 only on an ERROR (or --strict). A warnings-only page
    # must exit 0 — marker-rich correct copy is not blocked.
    findings = findings_for(MARKER_RICH)
    errors = [f for f in findings if f.severity == BL.SEVERITY_ERROR]
    assert not errors, f"marker-rich copy produced blocking errors: {[f.code for f in errors]}"


def t_check_never_rewrites_semantics():
    # the check reports; it does not mutate the copy. A number, a negation and a
    # causal claim survive verbatim (semantic preservation).
    samples = [
        "Revenue did NOT fall; it rose 12 percent because retention improved.",
        "It is important to note we shipped 3 releases, not 4.",
        "In conclusion, the outage was caused by a config change, not a deploy.",
    ]
    for body in samples:
        before = body
        findings_for(body)   # running the check must not touch the source string
        assert body == before, "the check mutated the copy — it must only report"
        # and it never errors on these
        errs = [f for f in findings_for(body) if f.severity == BL.SEVERITY_ERROR]
        assert not errs, f"a correct causal/negation/number sentence was blocked: {body!r}"


def main():
    case("B060 is always a warning, never escalated by count", t_b060_is_always_a_warning)
    case("the count-driven ERROR escalation is gone from the source", t_no_count_escalation)
    case("marker-rich correct text does not block the run", t_marker_rich_text_does_not_block)
    case("the check reports, never rewrites — numbers/negations/causality preserved",
         t_check_never_rewrites_semantics)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
