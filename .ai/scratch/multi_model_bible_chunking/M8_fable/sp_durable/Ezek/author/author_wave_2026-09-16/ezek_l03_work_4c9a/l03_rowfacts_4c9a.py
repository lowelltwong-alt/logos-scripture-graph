#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Compact per-row Masoretic fact table for lane ezek_author_l03.
Every cell is MEASURED from pmarks_Ezek.json at its pinned digest, by exact key.
Reports what was FOUND (PRESENT / ABSENT_FROM_KEYSET), never a bare boolean.
"""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
D = r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek"
pm = json.load(open(D + r"\pmarks_Ezek.json", encoding='utf-8'))
MARKS, KQ, NOTES = pm['marks'], pm['kq'], pm['notes_other']
PASEQ = pm['paseq']

# (row, mt_first, mt_last, web_first, web_last)  MT chapter is the same int in all rows here
ROWS = [
 ("P03-004", 16, 20, 23, 16, 20, 23),
 ("P03-005", 16, 24, 34, 16, 24, 34),
 ("P03-007", 16, 44, 50, 16, 44, 50),
 ("P03-008", 16, 51, 58, 16, 51, 58),
 ("P03-010", 17, 1, 10, 17, 1, 10),
 ("P03-011", 17, 11, 18, 17, 11, 18),
 ("P03-012", 17, 19, 21, 17, 19, 21),
 ("P03-013", 17, 22, 24, 17, 22, 24),
 ("P03-014", 18, 1, 4, 18, 1, 4),
 ("P03-015", 18, 5, 9, 18, 5, 9),
 ("P03-016", 18, 10, 20, 18, 10, 20),
 ("P03-017", 18, 21, 23, 18, 21, 23),
 ("P03-018", 18, 24, 26, 18, 24, 26),
 ("P03-019", 18, 27, 32, 18, 27, 32),
 ("P03-020", 19, 1, 14, 19, 1, 14),
 ("P04-001", 20, 1, 26, 20, 1, 26),
 ("P04-002", 20, 27, 29, 20, 27, 29),
 ("P04-003", 20, 30, 38, 20, 30, 38),
 ("P04-005", 21, 1, 5, 20, 45, 49),     # MT 21:1-5 = WEB 20:45-49
 ("P04-006", 21, 6, 10, 21, 1, 5),
 ("P04-007", 21, 11, 12, 21, 6, 7),
 ("P04-008", 21, 13, 22, 21, 8, 17),
 ("P04-009", 21, 23, 29, 21, 18, 24),
 ("P04-010", 21, 30, 32, 21, 25, 27),
 ("P04-011", 21, 33, 37, 21, 28, 32),
 ("P05-001", 22, 1, 16, 22, 1, 16),
 ("P05-002", 22, 17, 22, 22, 17, 22),
 ("P05-003", 22, 23, 31, 22, 23, 31),
]
VPC = {16: 63, 17: 24, 18: 32, 19: 14, 20: 44, 21: 37, 22: 31, 23: 49}  # MT, from inventory v2

def key(c, v):
    return f"Ezek.{c}.{v}"

def prev_mt(c, v):
    if v > 1:
        return key(c, v - 1)
    return key(c - 1, VPC[c - 1])

def next_mt(c, v):
    if v < VPC[c]:
        return key(c, v + 1)
    return key(c + 1, 1)

def cell(k):
    out = []
    out.append("mark=" + (",".join(MARKS[k]) if k in MARKS else "-"))
    if k in KQ:
        out.append(f"kq={len(KQ[k])}note(s)")
    n = sum(1 for x in PASEQ if x == k)
    if n:
        out.append(f"paseq={n}")
    if k in NOTES:
        out.append(f"note={len(NOTES[k])}")
    return k + " [" + " ".join(out) + "]"

for (rid, c, f, l, wc, wf, wl) in ROWS:
    print("=" * 78)
    print(f"{rid}  MT Ezek.{c}.{f}-{l}   WEB Ezek.{wc}.{wf}-{wl}")
    print("  BEHIND onset seam : " + cell(prev_mt(c, f)))
    print("  ONSET verse       : " + cell(key(c, f)))
    interior = [cell(key(c, v)) for v in range(f + 1, l)]
    hot = [s for s in interior if "[mark=-" not in s or "kq=" in s or "paseq=" in s or "note=" in s]
    print(f"  INTERIOR ({max(0,l-f-1)} verses) non-empty cells:")
    for s in hot:
        print("      " + s)
    print("  CLOSE verse       : " + cell(key(c, l)))
    print("  BEYOND close seam : " + cell(next_mt(c, l)))
