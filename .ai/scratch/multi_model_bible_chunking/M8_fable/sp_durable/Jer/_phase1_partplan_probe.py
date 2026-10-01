#!/usr/bin/env python3
"""Phase-1 probe: verify part-plan seams + compute the 20-part verse sums from staged bytes."""
import json
import sys
from pathlib import Path

SP = Path(__file__).resolve().parent
sys.path.insert(0, str(SP / "tools"))
from jer_lib import load_verse_maps  # noqa: E402

inv = json.loads((SP / "verse_inventory.json").read_text(encoding="utf-8"))
dev = json.loads((SP / "jer_device_inventory.json").read_text(encoding="utf-8"))
web_map, _ = load_verse_maps()

web_counts = inv["web_chapter_verse_counts"] if "web_chapter_verse_counts" in inv else inv
print("INV_KEYS:", list(inv.keys())[:10])

# normalize: want {chapter:int -> count:int} for WEB
def get_counts(obj):
    for k in ("web_chapter_verse_counts", "web", "chapters_web"):
        if isinstance(obj, dict) and k in obj:
            return {int(c): int(n) for c, n in obj[k].items()}
    return None

wc = get_counts(inv)
if wc is None:  # derive from the verse map directly (authoritative anyway)
    wc = {}
    for ref in web_map:
        c = int(ref.split(".")[1])
        wc[c] = wc.get(c, 0) + 1
print("WEB_TOTAL:", sum(wc.values()), "CH8:", wc[8], "CH9:", wc[9], "CH4:", wc[4])

# word-event lists
we = dev.get("word_event_formulas", dev.get("word_event", {}))
print("WORD_EVENT_KEYS:", list(we.keys()) if isinstance(we, dict) else type(we))
vy = we.get("vayehi_debar_yhwh", {}) if isinstance(we, dict) else {}
print("VAYEHI:", vy)

# seam texts
for ref in ("Jer.4.5", "Jer.43.8", "Jer.11.1", "Jer.18.1", "Jer.21.1", "Jer.37.1"):
    print(ref, "::", web_map[ref]["clean"][:100] if "clean" in web_map[ref] else web_map[ref]["text"][:100])

# the ruled 20-part plan with the two straddle resolutions
def vv(a_ch, a_v, b_ch, b_v):
    n = 0
    for c in range(a_ch, b_ch + 1):
        lo = a_v if c == a_ch else 1
        hi = b_v if c == b_ch else wc[c]
        n += hi - lo + 1
    return n

parts = [
    ("p01", (1, 1, 4, 4), "F1+M1"), ("p02", (4, 5, 6, 30), "M1"),
    ("p03", (7, 1, 9, 26), "M2"), ("p04", (10, 1, 12, 17), "M2+M3"),
    ("p05", (13, 1, 15, 21), "M3"), ("p06", (16, 1, 18, 23), "M3+M4"),
    ("p07", (19, 1, 22, 30), "M4+M5"), ("p08", (23, 1, 24, 10), "M5"),
    ("p09", (25, 1, 26, 24), "M6"), ("p10", (27, 1, 29, 32), "M6"),
    ("p11", (30, 1, 31, 40), "M7"), ("p12", (32, 1, 33, 26), "M7"),
    ("p13", (34, 1, 36, 32), "N8"), ("p14", (37, 1, 39, 18), "N8"),
    ("p15", (40, 1, 43, 7), "N9"), ("p16", (43, 8, 45, 5), "N9"),
    ("p17", (46, 1, 48, 47), "M10"), ("p18", (49, 1, 50, 46), "M10"),
    ("p19", (51, 1, 51, 64), "M10"), ("p20", (52, 1, 52, 34), "N11"),
]
total = 0
for pid, (a, b, c, d), fr in parts:
    n = vv(a, b, c, d)
    total += n
    # range ends must exist
    assert f"Jer.{a}.{b}" in web_map and f"Jer.{c}.{d}" in web_map, (pid, "range end missing")
    print(f"{pid} Jer.{a}.{b}-Jer.{c}.{d} {fr} vv={n}")
print("TOTAL:", total)
assert total == 1364, total
print("PART_PLAN_ARITHMETIC: PASS")
