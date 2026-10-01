#!/usr/bin/env python3
"""Language-zone guard for Jer (WARN-level heuristic + one Tier-0 symmetry arm).

Jer carries EXACTLY ONE Aramaic verse - MT 10:11 = WEB 10:11 (identity
numbering; Phase 0 byte-proven: 15 A-prefixed OSHB morph codes, all in that
verse; the other 21,961 codes are H-prefixed). It is a self-contained
Aramaic island inside the ch-10 idol polemic (10:10 and 10:12 are Hebrew).

Three arms:
 1. ARAMAIC LABEL OUTSIDE 10:11 (flag, review candidate): an "Aramaic" or
    "Syrian(-language)" label within 100 chars of a Jer ref OTHER than
    10:11 - no other verse of Jeremiah is in Aramaic. Aramaism /
    Aramaic-INFLUENCE discussion is legitimate (negative lookahead), and a
    field that ENGAGES the island (carries a 10:11 ref anywhere) is exempt
    - island discussion legitimately sits beside neighboring-verse refs.
 2. HEBREW LABEL ON 10:11 (flag, review candidate): a "Hebrew" grammar
    label within 60 chars of a 10:11 ref with no Aramaic word nearby -
    the island verse is NOT Hebrew.
 3. ISLAND DISCLOSURE SYMMETRY (flag; rows only): any ROW whose span covers
    WEB 10:11 must say "Aramaic" somewhere in the row - the island is a
    first-order literary fact of that stretch of text; shipping a row over
    it silently is a disclosure gap (the mark-symmetry principle applied
    to the language layer).
Usage: check_language_zones.py file1.json [more...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jer_lib import expand_ref_token

REFPAT = re.compile(r"Jer\.(\d+)\.(\d+)")
ARAMAIC = re.compile(r"\bAramaic\b(?!\s*(?:-influenced|influence|ism|izing|"
                     r"coloring|colouring|loan))|\bSyrian\b")
HEBREW_LABEL = re.compile(r"\bHebrew\b")
RANGE = re.compile(r"Jer\.\d+\.\d+(?:-(?:Jer\.)?\d+(?:\.\d+)?)?")


def iter_strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from iter_strings(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from iter_strings(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


def load_any(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    return json.loads(text)


def rows_of(data):
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if isinstance(data, dict):
        if "decisions" in data:
            return [r for r in data["decisions"] if isinstance(r, dict)]
        return [v for v in data.values() if isinstance(v, dict)]
    return []


def main() -> int:
    flags = []
    for f in sys.argv[1:]:
        data = load_any(Path(f))
        # arms 1 + 2: label checks over every string field
        for path, s in iter_strings(data):
            field_engages_island = any(
                (int(m.group(1)), int(m.group(2))) == (10, 11)
                for m in REFPAT.finditer(s))
            for m in REFPAT.finditer(s):
                c, v = int(m.group(1)), int(m.group(2))
                ctx = s[max(0, m.start() - 100):m.end() + 100]
                is_island = (c, v) == (10, 11)
                if ARAMAIC.search(ctx):
                    if not is_island and not field_engages_island:
                        flags.append({"file": Path(f).name, "path": path,
                                      "issue": "aramaic_label_outside_10_11",
                                      "note": ("review candidate - Jer's ONLY Aramaic "
                                               "verse is 10:11; discussing the island "
                                               "from a neighbor is legitimate, labeling "
                                               "another VERSE as Aramaic is not"),
                                      "ref": m.group(0), "context": ctx[:160]})
                elif is_island:
                    near = s[max(0, m.start() - 60):m.end() + 60]
                    if HEBREW_LABEL.search(near):
                        flags.append({"file": Path(f).name, "path": path,
                                      "issue": "hebrew_label_on_10_11",
                                      "note": ("review candidate - MT/WEB 10:11 is the "
                                               "book's single ARAMAIC verse (byte-proven "
                                               "from morph codes)"),
                                      "ref": m.group(0), "context": near[:160]})
        # arm 3: island disclosure symmetry (rows with spans only)
        for row in rows_of(data):
            span = row.get("span")
            if not isinstance(span, str):
                continue
            m = RANGE.search(span)
            if not m:
                continue
            pairs = expand_ref_token(m.group(0))
            if (10, 11) not in pairs:
                continue
            whole = json.dumps(row, ensure_ascii=False)
            if not re.search(r"\bAramaic\b", whole):
                flags.append({"file": Path(f).name,
                              "decision_id": row.get("decision_id", "?"),
                              "issue": "aramaic_island_undisclosed",
                              "note": ("row span covers WEB 10:11 - the single Aramaic "
                                       "verse - with no Aramaic disclosure anywhere in "
                                       "the row"),
                              "span": span})
    print(json.dumps({"flag_count": len(flags), "flags": flags,
                      "status": "GREEN" if not flags else "FLAGS"},
                     ensure_ascii=False, indent=1))
    return 1 if flags else 0


if __name__ == "__main__":
    raise SystemExit(main())
