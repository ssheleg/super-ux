#!/usr/bin/env python3
"""FIX-UX-14.01 — BP-212 no longer declares local payment testing impossible
(sherlock audit, UX-14).

The finding: BP-212 required a real public address before wiring a payment
provider, explaining it as the post-payment path being untestable locally — but
Stripe documents `stripe listen --forward-to localhost:4242/webhook` with no
registered URL. The error is a universal gate, not the genuine need for a
public HTTPS endpoint in PRODUCTION.

The fix under test (references/best-practices.md, BP-212):
* three environments separated — local sandbox (webhook forwarding / emulator)
  tests the wiring; production delivery needs a public HTTPS endpoint +
  signature verification;
* the "untestable on a laptop" claim is gone;
* production readiness is a separate provider-capability check, not a universal
  UX gate;
* the environment rule run as behaviour.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DOC = os.path.join(ROOT, "plugins", "super-ux", "skills", "references",
                   "best-practices.md")

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


def t_three_environments():
    d = flat()
    assert "separate the THREE environments" in d
    assert "stripe listen --forward-to localhost:4242/webhook" in d
    assert "no registered URL\n  needed".replace("\n  ", " ") in d or "no registered URL needed" in d


def t_untestable_claim_gone():
    d = flat()
    assert "untestable while the funnel exists only on a laptop" not in d, \
        "the untestable-on-a-laptop claim survived"
    assert 'IS testable on\n  a laptop with the provider\'s CLI'.replace("\n  ", " ") in d \
        or "IS testable on a laptop with the provider's CLI" in d
    assert '"untestable until it has a public\n  address" is false'.replace("\n  ", " ") in d \
        or '"untestable until it has a public address" is false' in d


def t_production_is_separate_check():
    d = flat()
    assert "PRODUCTION delivery needs a real public HTTPS endpoint with\n  signature verification".replace("\n  ", " ") in d \
        or "PRODUCTION delivery needs a real public HTTPS endpoint with signature verification" in d
    assert "a provider-capability question, not a universal UX gate that blocks local work" in d


# ---- the environment rule as behaviour


def can_test(env, has_public_https, has_cli_forwarding):
    """Which payment work each environment supports."""
    if env == "local":
        return has_cli_forwarding          # local wiring/tests need only forwarding
    if env in ("staging", "production"):
        return has_public_https            # delivery needs a public HTTPS endpoint
    return False


def t_local_needs_only_forwarding():
    assert can_test("local", has_public_https=False, has_cli_forwarding=True) is True, \
        "local payment testing was blocked without a public URL — the finding"
    assert can_test("local", has_public_https=False, has_cli_forwarding=False) is False


def t_production_needs_https():
    assert can_test("production", has_public_https=True, has_cli_forwarding=False) is True
    assert can_test("production", has_public_https=False, has_cli_forwarding=True) is False, \
        "production delivery passed without a public HTTPS endpoint"


def main():
    case("BP-212 separates the three environments with the Stripe CLI example",
         t_three_environments)
    case("the untestable-on-a-laptop claim is gone", t_untestable_claim_gone)
    case("production readiness is a separate provider-capability check",
         t_production_is_separate_check)
    case("fixture: local payment testing needs only forwarding",
         t_local_needs_only_forwarding)
    case("fixture: production delivery needs a public HTTPS endpoint",
         t_production_needs_https)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
