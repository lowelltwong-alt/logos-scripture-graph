import json, sys
from pathlib import Path
SP = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad") / "SP" / "Lam"
inv = json.loads((SP / "verse_inventory.json").read_text(encoding="utf-8"))
last = {int(c): n for c, n in inv["chapters"].items()}
parts = [{"part": "p01", "span": "Lam.1.1-Lam.2.22", "verses": 44, "frames": ["F1 Lam.1.1-Lam.1.22", "F2 Lam.2.1-Lam.2.22"], "onset_warrant": "book start; eikhah + alef line 1:1; internal poem seam at 2:1 (rows never straddle it)"},
         {"part": "p02", "span": "Lam.3.1-Lam.3.66", "verses": 66, "frames": ["F3 Lam.3.1-Lam.3.66"], "onset_warrant": "ani ha-gever + alef triplet 3:1; PE close at 2:22 behind"},
         {"part": "p03", "span": "Lam.4.1-Lam.5.22", "verses": 44, "frames": ["F4 Lam.4.1-Lam.4.22", "F5 Lam.5.1-Lam.5.22"], "onset_warrant": "eikhah + alef line 4:1; internal poem seam at 5:1 (zekhor YHWH; rows never straddle it)"}]
def count(span):
    a, b = span.split("-"); _, c1, v1 = a.split("."); _, c2, v2 = b.split("."); c1, v1, c2, v2 = map(int, (c1, v1, c2, v2))
    assert 1 <= v1 <= last[c1] and 1 <= v2 <= last[c2], span
    n = 0
    for c in range(c1, c2 + 1):
        lo = v1 if c == c1 else 1; hi = v2 if c == c2 else last[c]; n += hi - lo + 1
    return n
tot = 0
for p in parts:
    n = count(p["span"]); assert n == p["verses"], (p["part"], n); tot += n
assert tot == sum(last.values()) == 154, tot
# contiguity
ends = [p["span"].split("-")[1] for p in parts]; starts = [p["span"].split("-")[0] for p in parts]
assert starts[0] == "Lam.1.1" and ends[-1] == "Lam.5.22"
for i in range(1, len(parts)):
    _, ce, ve = ends[i - 1].split("."); _, cs, vs = starts[i].split(".")
    assert (int(cs), int(vs)) == ((int(ce), int(ve) + 1) if int(ve) < last[int(ce)] else (int(ce) + 1, 1)), (ends[i - 1], starts[i])
doc = {"schema": "m8_writer_parts.v1", "book": "Lam", "total_verses": 154, "parts_count": 3, "writer_parts": parts, "probe": "PASS (sums 154 exactly; contiguous; range ends exist)"}
(SP / "writer_parts.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"parts": [(p["part"], p["span"], p["verses"]) for p in parts], "sum": tot, "probe": "PASS"}))
