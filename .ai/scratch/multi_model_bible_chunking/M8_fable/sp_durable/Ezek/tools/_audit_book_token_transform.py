#!/usr/bin/env python3
"""Report-only control for a known hazard: a book-token transform rewrites history along with identifiers.

When a toolkit file is adapted by replacing the source book's tokens, prose such as "NEW for Jer" or "carried to Jer"
becomes "NEW for Ezek", which is false provenance. A stale-fact grep cannot see it, because the rewritten line names the
right book. This script aligns every Ezek toolkit file with the Jer file of the same name and reports, per file:

  - source lines that carry a Jer book token (identifier or prose),
  - how many of those the Ezek copy changed, and how many it kept verbatim,
  - every Ezek line that still names Jer or Jeremiah, so a reviewer can confirm each is true history,
  - every Ezek line pairing an Ezek token with a lineage word, which is the signature of rewritten history.

It gates nothing and classifies nothing; each listed line needs a reader. It never writes a file.
Usage: _audit_book_token_transform.py [--lines]
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ_TOOLS = Path(__file__).resolve().parent
JER_TOOLS = EZ_TOOLS.parent.parent / "Jer" / "tools"
JER_TOKEN = re.compile(r"\bJer\b|\bJER\b|jer_lib|\bjer\b|Jeremiah")
EZEK_TOKEN = re.compile(r"\bEzek\b|\bEZEK\b|ezek_lib|\bezek\b|Ezekiel")
LINEAGE = re.compile(r"\b(?:NEW for|carried (?:to|from|over)|lineage|v\d+ run|finding|patch|lesson|upgrade[sd]?|"
                     r"introduced|inherited|ported|as of|since|first (?:seen|found|caught)|regression)\b", re.I)
SKIP = {"ezek_lib.py", "jer_lib.py", Path(__file__).name}


def main() -> int:
    show = "--lines" in sys.argv
    report, totals = [], {"files": 0, "src_token_lines": 0, "changed": 0, "kept_verbatim": 0,
                          "ezek_lines_naming_jer": 0, "ezek_token_with_lineage_word": 0}
    for ez in sorted(EZ_TOOLS.glob("*.py")):
        src = JER_TOOLS / ez.name
        if ez.name in SKIP or not src.exists():
            continue
        a = src.read_text(encoding="utf-8-sig").splitlines()
        b = ez.read_text(encoding="utf-8-sig").splitlines()
        kept = changed = 0
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            for line in a[i1:i2]:
                if JER_TOKEN.search(line):
                    if op == "equal":
                        kept += 1
                    else:
                        changed += 1
        naming_jer = [(n, l.strip()) for n, l in enumerate(b, 1) if JER_TOKEN.search(l)]
        lineage = [(n, l.strip()) for n, l in enumerate(b, 1) if EZEK_TOKEN.search(l) and LINEAGE.search(l)]
        row = {"file": ez.name, "src_token_lines": kept + changed, "changed": changed, "kept_verbatim": kept,
               "ezek_lines_naming_jer": len(naming_jer), "ezek_token_with_lineage_word": len(lineage)}
        if show:
            row["naming_jer"] = ["%d: %s" % (n, l[:150]) for n, l in naming_jer]
            row["lineage_signature"] = ["%d: %s" % (n, l[:150]) for n, l in lineage]
        report.append(row)
        totals["files"] += 1
        for k in ("src_token_lines", "changed", "kept_verbatim", "ezek_lines_naming_jer", "ezek_token_with_lineage_word"):
            totals[k] += row[k]
    print(json.dumps({"totals": totals, "per_file": report,
                      "limit": "report only - a listed line is a candidate for review, not a verdict"},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
