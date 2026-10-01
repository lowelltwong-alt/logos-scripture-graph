#!/usr/bin/env python3
"""Phase-0 helper (orchestrator only): stage the BOOK-SPECIFIC members of the Ezek shared toolkit.

Sourcing was decided by measured code diffs, not by preference:
  - check_language_zones.py comes from Lam/tools. Lam is Hebrew throughout like Ezekiel, and its version is the
    compact Hebrew-only tool; Jeremiah's is built entirely around its Aramaic island at 10:11 and would be wrong here.
  - cap_sweep.py comes from Jer/tools. It is book-agnostic apart from one assertion pinning 52 chapters / 1364
    verses, which becomes 48 / 1273.
  (citation_sweep.py and check_marks.py are staged separately: they need Jeremiah's zone logic combined with
   Lamentations' no-special-letter wording, plus an Ezekiel puncta arm, and each change is tested.)

Every replacement is asserted to occur the expected number of times; a mismatch aborts before any file is written.
After writing, each output is compiled and scanned for stale source-book facts. This script NEVER touches ezek_lib.py,
TOOLKIT.md or _toolkit_selfcheck.py.
"""
import py_compile
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
DST = Path(__file__).resolve().parent
SP = DST.parent.parent
LAM = SP / "Lam" / "tools"
JER = SP / "Jer" / "tools"
OSHB_DIR = SP.parents[4] / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files"
PROTECTED = {"ezek_lib.py", "TOOLKIT.md", "_toolkit_selfcheck.py"}


def sub_exact(text, pattern, repl, expected, label, regex=False):
    if regex:
        new, n = re.subn(pattern, repl, text)
    else:
        n = text.count(pattern)
        new = text.replace(pattern, repl)
    if n != expected:
        raise SystemExit("ABORT %s: expected %d occurrence(s) of %r, found %d" % (label, expected, pattern[:60], n))
    return new


def morph_prefix_counts(book):
    raw = (OSHB_DIR / ("%s.xml" % book)).read_text(encoding="utf-8")
    return Counter(re.findall(r"<w\b[^>]*?\bmorph=\"([A-Z])", raw))


def stage_language_zones():
    # The docstring's morph counts are measured here, never typed. The method is calibrated first: it must reproduce
    # the Lam tool's own stated 1,564 / 0, or the Ezek number would be a different kind of count.
    lam = morph_prefix_counts("Lam")
    if (lam["H"], lam["A"]) != (1564, 0):
        raise SystemExit("ABORT calibration: this method gives Lam H=%d A=%d, not the Lam tool's 1,564 / 0" % (lam["H"], lam["A"]))
    ez = morph_prefix_counts("Ezek")
    if ez["A"] != 0:
        raise SystemExit("ABORT: Ezek.xml carries %d A-prefixed morph codes; the Hebrew-only model does not apply" % ez["A"])
    t = (LAM / "check_language_zones.py").read_text(encoding="utf-8-sig")
    t = sub_exact(t, r"\(1,564\s+H-prefixed, 0 A-prefixed\)", "(%s H-prefixed, 0 A-prefixed)" % format(ez["H"], ","),
                  1, "morph counts", regex=True)
    t = sub_exact(t, "no verse of Lamentations is in Aramaic", "no verse of Ezekiel is in Aramaic", 1, "prose")
    t = sub_exact(t, "aramaic_label_in_lam", "aramaic_label_in_ezek", 1, "issue id")
    t = sub_exact(t, "Lam is Hebrew throughout (0 A-prefixed morph codes); no verse is Aramaic",
                  "Ezek is Hebrew throughout (0 A-prefixed morph codes); no verse is Aramaic", 1, "flag note")
    t = re.sub(r"\bLam\b", "Ezek", t)
    t = t.replace("LAM", "EZEK")
    return "check_language_zones.py", t


def stage_cap_sweep():
    t = (JER / "cap_sweep.py").read_text(encoding="utf-8-sig")
    t = sub_exact(t, "assert len(LAST_VERSE) == 52 and sum(LAST_VERSE.values()) == 1364",
                  "assert len(LAST_VERSE) == 48 and sum(LAST_VERSE.values()) == 1273", 1, "book totals")
    t = t.replace("jer_lib", "ezek_lib").replace("Jer_", "Ezek_").replace("_Jer", "_Ezek")
    t = re.sub(r"\bJer\b", "Ezek", t)
    t = re.sub(r"\bJER\b", "EZEK", t)
    t = re.sub(r"\bjer\b", "ezek", t)
    return "cap_sweep.py", t


STALE = re.compile(r"\b1364\b|\b52\b|8:23|\bWEB 9:|\bMT 9:|10:11|Aramaic island|Jeremiah|\b1,564\b|Lamentations|\b154\b")


def main():
    staged = [stage_language_zones(), stage_cap_sweep()]
    for name, text in staged:
        assert name not in PROTECTED
        out = DST / name
        if out.exists() and out.read_text(encoding="utf-8") != text:
            raise SystemExit("ABORT: %s already exists with different content; nothing overwritten" % name)
    for name, text in staged:
        (DST / name).write_text(text, encoding="utf-8", newline="\n")
        py_compile.compile(str(DST / name), doraise=True)
        stale = [(i, l.strip()[:100]) for i, l in enumerate(text.splitlines(), 1) if STALE.search(l)]
        print("%-26s written | compile ok | stale-fact lines: %d" % (name, len(stale)))
        for i, l in stale:
            print("      %d: %s" % (i, l))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
