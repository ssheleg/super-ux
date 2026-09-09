#!/usr/bin/env python3
"""FIX-UX-04.01 — one skill, two incompatible ownership rules for strings.md
(sherlock audit, UX-04).

The finding: "This skill never writes to docs/brand/" was absolute, while
Write step 5 and the DoD require adding/updating strings.md, which lives in
docs/brand/.

The fix under test (copywriting/SKILL.md):
* ownership is by FILE, not directory — brand-voice owns
  voice/terms/facts/channels/locale (never written here); copywriting owns
  strings.md (Status: proposed) and the product text;
* writing a strings.md row needs no extra approval for its location; a
  coordinated run claims the file; voice/facts stay untouched;
* the file-ownership rule run as behaviour.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DOC = os.path.join(ROOT, "plugins", "super-ux", "skills", "copywriting", "SKILL.md")

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


def t_ownership_by_file():
    d = flat()
    assert "Ownership is by FILE, not by directory." in d
    assert "the directory is not the owner — the file is" in d
    assert "This skill never writes to `docs/brand/`." not in d, \
        "the absolute directory rule survived"


def t_brand_voice_owns_sources():
    d = flat()
    for src in ("`voice.md`", "terminology dictionary", "`facts.md`",
                "channel playbooks", "locale policy"):
        assert src in d, f"brand-voice source {src} not named"
    assert "this skill **never writes those**" in d


def t_copywriting_owns_strings():
    d = flat()
    assert "This skill DOES own **`strings.md`**" in d
    assert "needs no extra approval\n for its LOCATION".replace("\n ", " ") in d \
        or "needs no extra approval for its LOCATION" in d
    assert "a coordinated run claims the file before editing" in d
    assert "voice and facts stay untouched" in d


# ---- the file-ownership rule as behaviour


BRAND_VOICE_FILES = {"docs/brand/voice.md", "docs/brand/terminology.md",
                     "docs/brand/facts.md", "docs/brand/channels.md",
                     "docs/brand/locale.md"}
COPYWRITING_FILES = {"docs/brand/strings.md"}


def may_write(skill, path):
    if skill == "copywriting":
        return path in COPYWRITING_FILES or not path.startswith("docs/brand/")
    if skill == "brand-voice":
        return path in BRAND_VOICE_FILES
    return False


def t_one_error_string_updates_source_and_row():
    # editing one error string touches its source (the product file) and its
    # strings.md row — both allowed for copywriting in one pass
    assert may_write("copywriting", "src/components/Toast.tsx")
    assert may_write("copywriting", "docs/brand/strings.md")
    # voice/facts are NOT written by copywriting
    assert not may_write("copywriting", "docs/brand/voice.md")
    assert not may_write("copywriting", "docs/brand/facts.md")


def t_no_directory_veto():
    # strings.md is under docs/brand/ but that does not veto the write
    assert may_write("copywriting", "docs/brand/strings.md"), \
        "the directory location vetoed a legitimate strings.md write"


def main():
    case("ownership is by file, not directory; the absolute rule is gone",
         t_ownership_by_file)
    case("brand-voice owns voice/terms/facts/channels/locale", t_brand_voice_owns_sources)
    case("copywriting owns strings.md + product text, no location approval",
         t_copywriting_owns_strings)
    case("fixture: one error-string edit updates source + row; voice/facts untouched",
         t_one_error_string_updates_source_and_row)
    case("fixture: docs/brand/ location does not veto the strings.md write",
         t_no_directory_veto)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
