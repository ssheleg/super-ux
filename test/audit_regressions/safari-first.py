#!/usr/bin/env python3
"""A rendered screen is checked in WebKit (Safari) first (family release
2026-10-16, R15).

ux-audit's RUNTIME tier and its live pass open the product in a browser. The
engine order lives in one shared contract, `references/browser-engine.md`:
WebKit first, Chromium as a stated fallback, a Chromium-only check reported as
exactly that. ux-audit and funnel-research link it, and the copy ux-audit ships
is byte-identical to the source of truth. Mutations that drop each point are
refused, so the check is watched saying no. Text integrity only: no claim that
a model follows it.

Standard library only.
"""
import os
import re
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SKILLS = os.path.join(ROOT, "plugins", "super-ux", "skills")
CONTRACT = os.path.join(SKILLS, "references", "browser-engine.md")
LINK = "](references/browser-engine.md)"

checks = 0
failures = []


def case(name, fn):
    global checks
    try:
        fn()
        checks += 1
        print(f"  ok  {name}")
    except (AssertionError, IndexError, ValueError, OSError) as e:
        failures.append(f"{name}: {e!r}")
        print(f"FAIL  {name}: {e!r}")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def flat(text):
    return " ".join(text.split())


def engine_contract(text):
    body = flat(text)
    for needle in ("safaridriver", "Playwright", "`webkit`", "--browser webkit",
                   "npx playwright install webkit", "Safari Web Inspector",
                   "open -a Safari", "WebKit/Safari backend",
                   "stated fallback", "say which and why", "Chrome Dev",
                   "Lighthouse", "CDP trace", "chrome-devtools MCP",
                   "temporary profile", "close every process",
                   "checked only in Chromium"):
        assert needle in body, f"browser-engine.md no longer states {needle!r}"


def t_contract():
    engine_contract(read(CONTRACT))


def t_ux_audit_links_it_in_runtime_and_live_pass():
    skill = read(os.path.join(SKILLS, "ux-audit", "SKILL.md"))
    tiers = skill.split("**Three evidence tiers", 1)[1].split("4. **Check the batches", 1)[0]
    live = skill.split("## Live pass and visual drift", 1)[1].split("\n## ", 1)[0]
    assert LINK in tiers, "RUNTIME tier does not name the engine order"
    assert LINK in live, "live pass does not name the engine order"
    assert "WebKit" in flat(live)


def t_shipped_copy_is_identical():
    shipped = os.path.join(SKILLS, "ux-audit", "references", "browser-engine.md")
    assert read(shipped) == read(CONTRACT), "ux-audit's copy drifted; run test/sync_references.py"


def t_funnel_walk_is_webkit_first():
    text = flat(read(os.path.join(SKILLS, "references", "funnel-research.md")))
    para = text.split("**Who does the clicking, and where that stops.**", 1)[1]
    para = para.split("| Capture |", 1)[0]
    assert "browser-engine.md" in para
    assert para.index("webkit") < para.index("chrome-devtools"), \
        "the funnel walk still names a Chrome tool first"


def t_dropped_points_are_refused():
    text = read(CONTRACT)
    engine_contract(text)
    for token in ("safaridriver", "open -a Safari", "stated fallback",
                  "temporary profile", "close every process",
                  "checked only in Chromium", "Chrome Dev"):
        pattern = r"\s+".join(map(re.escape, token.split()))
        try:
            engine_contract(re.sub(pattern, "REMOVED", text))
        except AssertionError:
            continue
        raise AssertionError(f"dropping {token!r} was not refused")


case("references/browser-engine.md carries the WebKit-first order", t_contract)
case("ux-audit links it from the RUNTIME tier and the live pass",
     t_ux_audit_links_it_in_runtime_and_live_pass)
case("the copy ux-audit ships is byte-identical", t_shipped_copy_is_identical)
case("funnel-research walks the funnel in WebKit first", t_funnel_walk_is_webkit_first)
case("dropping any point is refused", t_dropped_points_are_refused)

if failures:
    print(f"\n{len(failures)} failure(s), {checks} passed")
    sys.exit(1)
print(f"\nall green ({checks} checks)")
