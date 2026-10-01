#!/usr/bin/env python3
"""Report-only control for a known hazard: a book-token transform rewrites history along with identifiers.

When a toolkit file is adapted by replacing the source book's tokens, prose such as "NEW for Jer" or "carried to Jer"
can come out naming the new book, which is false provenance. A stale-fact grep cannot see it, because the rewritten
line names the right book. Daniel port (T2): this script aligns every Dan toolkit file with its source in SRC_TOOLS,
the predecessor book it was ported from, and reports, per file:

  - source lines that carry a predecessor book token (identifier or prose),
  - how many of those the Dan copy changed, and how many it kept verbatim,
  - every Dan line that still names the predecessor, so a reviewer can confirm each is true history,
  - every Dan line pairing a Dan token with a lineage word, which is the signature of rewritten history.

It gates nothing and classifies nothing; each listed line needs a reader. It never writes a file.

Pairing. The source is the file of the same name; failing that, the file whose name the adapter's own filename token
transform gives (a Dan token in the name becomes the predecessor's, as _test_zone_tools_dan.py came from
_test_zone_tools_ezek.py under the T1 spec's RENAME). The rename map lived only in a lane's scratch spec, so it is
derived here instead of read. A file listed in AUTHORED was written for Daniel, not ported, and is reported under
authored_not_ported, never aligned. Every other Dan file with no source is reported under unpaired, so a missed
pairing is visible instead of silent.
Usage: _audit_book_token_transform.py [--lines]
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
BOOK_TOOLS = Path(__file__).resolve().parent
SRC_TOOLS = BOOK_TOOLS.parent.parent / "Ezek" / "tools"   # the predecessor: Dan/tools was ported from it
SRC_TOKEN = re.compile(r"\bEzek\b|\bEZEK\b|ezek_lib|\bezek\b|Ezekiel")
DAN_TOKEN = re.compile(r"\bDan\b|\bDAN\b|dan_lib|\bdan\b|Daniel")
LINEAGE = re.compile(r"\b(?:NEW for|carried (?:to|from|over)|lineage|v\d+ run|finding|patch|lesson|upgrade[sd]?|"
                     r"introduced|inherited|ported|as of|since|first (?:seen|found|caught)|regression)\b", re.I)
SKIP = {"dan_lib.py", "ezek_lib.py", Path(__file__).name}
AUTHORED = {"_toolkit_selfcheck.py": "written for Daniel's artifacts (E-61 item 2); Ezekiel's is a different file"}


def source_for(name: str) -> tuple[Path | None, str]:
    """The predecessor file a Dan tool was ported from, and how it was paired."""
    if (SRC_TOOLS / name).exists():
        return SRC_TOOLS / name, "name"
    renamed = name.replace("_dan.", "_ezek.").replace("_dan_", "_ezek_")
    if renamed != name and (SRC_TOOLS / renamed).exists():
        return SRC_TOOLS / renamed, "filename_token"
    return None, ""


def main() -> int:
    show = "--lines" in sys.argv
    report, totals = [], {"files": 0, "src_token_lines": 0, "changed": 0, "kept_verbatim": 0,
                          "dan_lines_naming_src": 0, "dan_token_with_lineage_word": 0}
    unpaired, authored = [], []
    for ez in sorted(BOOK_TOOLS.glob("*.py")):
        if ez.name in SKIP:
            continue
        if ez.name in AUTHORED:
            authored.append({"file": ez.name, "reason": AUTHORED[ez.name]})
            continue
        src, paired_by = source_for(ez.name)
        if src is None:
            unpaired.append(ez.name)
            continue
        a = src.read_text(encoding="utf-8-sig").splitlines()
        b = ez.read_text(encoding="utf-8-sig").splitlines()
        kept = changed = 0
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            for line in a[i1:i2]:
                if SRC_TOKEN.search(line):
                    if op == "equal":
                        kept += 1
                    else:
                        changed += 1
        naming_src = [(n, l.strip()) for n, l in enumerate(b, 1) if SRC_TOKEN.search(l)]
        lineage = [(n, l.strip()) for n, l in enumerate(b, 1) if DAN_TOKEN.search(l) and LINEAGE.search(l)]
        row = {"file": ez.name, "source": src.name, "paired_by": paired_by,
               "src_token_lines": kept + changed, "changed": changed, "kept_verbatim": kept,
               "dan_lines_naming_src": len(naming_src), "dan_token_with_lineage_word": len(lineage)}
        if show:
            row["naming_src"] = ["%d: %s" % (n, l[:150]) for n, l in naming_src]
            row["lineage_signature"] = ["%d: %s" % (n, l[:150]) for n, l in lineage]
        report.append(row)
        totals["files"] += 1
        for k in ("src_token_lines", "changed", "kept_verbatim", "dan_lines_naming_src", "dan_token_with_lineage_word"):
            totals[k] += row[k]
    print(json.dumps({"totals": totals, "per_file": report, "unpaired": unpaired, "authored_not_ported": authored,
                      "limit": "report only - a listed line is a candidate for review, not a verdict"},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
