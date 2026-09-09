#!/usr/bin/env python3
"""XD-12.01 — component reuse and the token's role are fixed before a kit
migration (sherlock audit, XD-12).

The fix under test (references/component-guidelines.md):
* the inventory marks reuse/modify/create with a reason and scenario ids;
* token names prove the paint, not the component — the mandatory contract is
  DOM/API: roles, native props, focus, keyboard, disabled;
* a single-use item is not extracted for the count; creation carries a
  reason, never a ritual permission;
* the adapter checklist is change-specific and kit fixes stay separate
  (DS-01/VD-05);
* the rules run as behaviour.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DOC = os.path.join(ROOT, "plugins", "super-ux", "skills", "references",
                   "component-guidelines.md")

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


def t_dispositions_with_reasons():
    d = flat()
    assert "**reuse / modify / create**, each with its reason and the scenario ids" in d
    assert "a disposition nobody can explain is a migration nobody can review" in d


def t_tokens_are_not_an_api():
    d = flat()
    assert "Token names are not an API." in d
    for part in ("roles", "native props", "focus", "keyboard", "disabled"):
        assert part in d, f"the {part} half of the contract is missing"
    assert "identical token names and different `disabled` semantics are two components" in d


def t_no_ritual_extraction_or_creation():
    d = flat()
    assert "A single-use item is not extracted for the count." in d
    assert "raising the component number is not a reason" in d
    assert "Creation carries a reason, never a ritual permission." in d


def t_adapter_checklist_change_specific():
    d = flat()
    assert "The adapter checklist is change-specific" in d
    assert "stay separate implementation tasks" in d and "DS-01/VD-05" in d


# ---- behaviour


def compatible(a, b):
    """Token names prove paint; the API contract decides compatibility."""
    api = ("role", "native_props", "focus", "keyboard", "disabled")
    return all(a.get(k) == b.get(k) for k in api)


def review_inventory(items):
    problems = []
    for it in items:
        if it["disposition"] not in ("reuse", "modify", "create"):
            problems.append(f"{it['name']}: unknown disposition")
            continue
        if not it.get("reason") or not it.get("scenarios"):
            problems.append(f"{it['name']}: {it['disposition']} without reason/scenarios")
        if it["disposition"] == "create" and it.get("reason") == "we may create components":
            problems.append(f"{it['name']}: ritual permission is not a reason")
        if it.get("extracted") and it.get("consumers", 0) < 2 \
                and not it.get("named_upcoming_consumer"):
            problems.append(f"{it['name']}: extracted for the count")
    return problems


def t_same_tokens_different_api():
    a = {"tokens": ["--btn-bg", "--btn-fg"], "role": "button",
         "native_props": True, "focus": "ring", "keyboard": "space+enter",
         "disabled": "aria-disabled, focusable"}
    b = dict(a, disabled="disabled attr, unfocusable")
    assert a["tokens"] == b["tokens"]
    assert not compatible(a, b), \
        "identical token names proved Button compatibility — the finding"


def t_inventory_fixture():
    probs = review_inventory([
        {"name": "Button", "disposition": "reuse", "reason": "API matches SCN-004",
         "scenarios": ["SCN-004"]},
        {"name": "Chip", "disposition": "create",
         "reason": "we may create components", "scenarios": ["SCN-009"]},
        {"name": "StatCell", "disposition": "modify", "reason": "needs loading state",
         "scenarios": ["SCN-002"], "extracted": True, "consumers": 1},
    ])
    assert any("ritual permission" in p for p in probs), "the ritual creation passed"
    assert any("extracted for the count" in p for p in probs), \
        "the single-use extraction passed"
    assert not any("Button" in p for p in probs)


def main():
    case("dispositions carry reasons and scenario ids", t_dispositions_with_reasons)
    case("token names are not an API; the DOM/API contract is mandatory",
         t_tokens_are_not_an_api)
    case("no count-driven extraction, no ritual creation",
         t_no_ritual_extraction_or_creation)
    case("the adapter checklist is change-specific; kit fixes separate",
         t_adapter_checklist_change_specific)
    case("fixture: same tokens, different disabled semantics — incompatible",
         t_same_tokens_different_api)
    case("fixture: the inventory review flags ritual creation and count extraction",
         t_inventory_fixture)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
