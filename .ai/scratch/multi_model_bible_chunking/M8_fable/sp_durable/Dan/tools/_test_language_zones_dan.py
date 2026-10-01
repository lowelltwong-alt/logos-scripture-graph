#!/usr/bin/env python3
"""Fixture test for Dan/tools/check_language_zones.py: every arm fires on its target and stays quiet on its
legitimate neighbor. The MT 2:4 words are read from Dan_oshb.txt, never typed. Exit 0 only if every case holds."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
GUARD = TOOLS / "check_language_zones.py"
V24 = dict(l.split("\t", 1) for l in (TOOLS.parent / "Dan_oshb.txt").read_text(encoding="utf-8").splitlines())["Dan.2.4"].split(" ")
HEB_HALF = " ".join(V24[1:3])      # words 2-3 (Hebrew half, 2:4a)
ARAM_HALF = " ".join(V24[5:8])     # words 6-8 (Aramaic half, 2:4b)

# (name, fixture rows, expected sorted issue list)
CASES = [
    ("hebrew row, no disclosure needed", [{"decision_id": "r1", "span": "Dan.1.1-Dan.1.21", "note": "court tale"}], []),
    ("island row undisclosed; covers 2:4 inside",
     [{"decision_id": "r2", "span": "Dan.2.1-Dan.2.13", "note": "the dream demand"}],
     ["aramaic_island_undisclosed", "mid_verse_switch_undisclosed"]),
    ("island row disclosing the switch", [{"decision_id": "r3", "span": "Dan.2.1-Dan.2.13",
                                           "note": "Aramaic begins at 2:4b"}], []),
    ("row ending at 2:4 without a half", [{"decision_id": "r4", "span": "Dan.2.1-Dan.2.4",
                                           "note": "Aramaic speech begins mid-verse"}],
     ["mid_verse_boundary_half_unstated"]),
    ("row ending at 2:4 with a half", [{"decision_id": "r5", "span": "Dan.2.1-Dan.2.4",
                                        "note": "ends after 2:4a; the Aramaic 2:4b opens the next row"}], []),
    ("row starting at 2:4 without a half", [{"decision_id": "r6", "span": "Dan.2.4-Dan.2.13",
                                             "note": "Aramaic"}], ["mid_verse_boundary_half_unstated"]),
    ("late island row undisclosed", [{"decision_id": "r7", "span": "Dan.7.15-Dan.7.28", "note": "vision"}],
     ["aramaic_island_undisclosed"]),
    ("Hebrew-zone row after the island", [{"decision_id": "r8", "span": "Dan.8.1-Dan.8.27", "note": "ram"}], []),
    ("WEB-only coordinate inside the island", [{"decision_id": "r9", "span": "Dan.4.35-Dan.4.37", "note": "x"}],
     ["aramaic_island_undisclosed"]),
    ("MT-space span inside the island", [{"decision_id": "r10", "span": "oshb:Dan.3.31-33", "note": "x"}],
     ["aramaic_island_undisclosed"]),
    ("Aramaic label on a Hebrew verse", [{"note": "Dan.9.4 opens an Aramaic prayer"}],
     ["aramaic_label_on_hebrew_verse"]),
    ("Syrian label on a Hebrew verse", [{"note": "Dan.1.4 in the Syrian tongue"}],
     ["aramaic_label_on_hebrew_verse"]),
    ("Aramaic-influence discussion is legitimate", [{"note": "Aramaic-influenced diction at Dan.9.4"}], []),
    ("field engaging the island is exempt", [{"note": "the Aramaic of Dan.7.28 ends; Dan.8.1 resumes"}], []),
    ("Dan.2.4a ref labeled Aramaic without engaging", [{"note": "Dan.2.4a is Aramaic"}], []),
    ("Hebrew label on an Aramaic verse", [{"note": "Dan.3.23 uses a Hebrew verb form"}],
     ["hebrew_label_on_aramaic_verse"]),
    ("Hebrew label on MT-only Aramaic coordinate", [{"note": "oshb:Dan.3.33 has a Hebrew idiom"}],
     ["hebrew_label_on_aramaic_verse"]),
    ("Hebrew Bible names the corpus", [{"note": "Dan.3.23 in the Hebrew Bible"}], []),
    ("Hebrew beside Aramaic is exempt", [{"note": "Dan.3.23, Hebrew and Aramaic compared"}], []),
    ("Hebrew label near a Hebrew-zone ref", [{"note": "Dan.7.28 closes; Dan.8.1 is Hebrew"}], []),
    ("Hebrew label on Dan.2.4b", [{"note": "Dan.2.4b is Hebrew"}], ["hebrew_label_on_aramaic_verse"]),
    ("bare 2:4 quote of the Aramaic half", [{"q": "Dan.2.4 " + ARAM_HALF}], ["mid_verse_quote_half_unstated"]),
    ("2:4b quote of the Aramaic half", [{"q": "Dan.2.4b " + ARAM_HALF + " (Aramaic)"}], []),
    ("2:4a stated for Aramaic-half words", [{"q": "Dan.2.4 (2:4a) " + ARAM_HALF}],
     ["mid_verse_quote_half_mismatch"]),
    ("bare 2:4 quote of the Hebrew half", [{"q": "Dan.2.4 " + HEB_HALF}], ["mid_verse_quote_half_unstated"]),
    ("quote spanning the switch, both halves stated", [{"q": "Dan.2.4 2:4a-2:4b " + V24[3] + " " + V24[4]}], []),
    ("bare 2:4 cite with no quotation", [{"note": "see Dan.2.4 for the switch"}], []),
]


def run(rows) -> tuple[int, list[str]]:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "fixture.json"
        p.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, str(GUARD), str(p)], capture_output=True, text=True, encoding="utf-8")
    out = json.loads(r.stdout)
    return r.returncode, sorted(f["issue"] for f in out["flags"])


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    failed = []
    for name, rows, want in CASES:
        code, got = run(rows)
        if got != sorted(want) or code != (1 if want else 0):
            failed.append({"case": name, "want": want, "got": got, "exit": code})
    print(json.dumps({"module": "_test_language_zones_dan", "cases": len(CASES), "passed": len(CASES) - len(failed),
                      "failed": failed, "verdict": "GREEN" if not failed else "RED"}, ensure_ascii=False, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
