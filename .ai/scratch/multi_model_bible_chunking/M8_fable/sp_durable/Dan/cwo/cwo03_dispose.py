"""CWO-DAN-03 hand-disposition aid (Daniel). Reads the sweep report (tf/applied/cwo_applied.json) and re-classifies every
hit with ZONE PRECEDENCE: any C.V whose numbers fall inside a numbering zone on either face (MT 3:31-33 / WEB 4:1-3,
MT 4:1-34 / WEB 4:4-37, MT 6:1 / WEB 5:31, MT 6:2-29 / WEB 6:1-28) is 'zone' even when it is part of a seam pair,
unless its context names another book. Verse-only matches (no chapter) are listed for reading against the row's range.
The sweep's own classifier checked seam_pair before zone, so zone tails of a pair were filed as seam_pair.
usage: cwo03_dispose.py REPORT OUT_JSON"""
import collections
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
OTHER = re.compile(r"Maccabees|Jeremiah|Ezekiel|Isaiah|Genesis|Revelation|Matthew|Mark|Luke|Ezra|Nehemiah|Chronicles|"
                   r"Kings|Psalm")


def in_zone(c, v):
    return (c == 3 and 31 <= v <= 33) or c == 4 or (c == 5 and v == 31) or (c == 6 and 1 <= v <= 29)


rep = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
hits = rep["orders"]["CWO-DAN-03"]["hits"]
out, verse_only = [], []
for h in hits:
    m, ctx = h["match"], h["context"]
    cv = re.fullmatch(r"(?:Dan(?:iel)?\s+)?(\d{1,2})[:.](\d{1,3})", m.strip(), re.I)
    chv = re.search(r"(?:chapter|ch\.?)\s*(\d+)\s*,?\s*(?:verse|verses|v\.|vv\.)\s*(\d+)", m, re.I)
    if OTHER.search(ctx) and not cv:
        cls = "other_book"
    elif cv or chv:
        c, v = (int(x) for x in (cv or chv).groups())
        if OTHER.search(ctx[max(0, ctx.find(m) - 30):ctx.find(m) + len(m)] if m in ctx else ctx):
            cls = "other_book"
        elif in_zone(c, v):
            cls = "zone"
        elif h["proposed"] == "seam_pair?":
            cls = "seam_pair"
        else:
            cls = "plain"
    else:
        cls = "verse_only_read"
        verse_only.append(h)
    out.append(dict(h, disposition=cls))
cnt = collections.Counter(x["disposition"] for x in out)
moved = collections.Counter((x["proposed"], x["disposition"]) for x in out if x["proposed"].rstrip("?") != x["disposition"])
Path(sys.argv[2]).write_bytes((json.dumps({"source_report_rows_sha256": rep["rows_sha256"], "counts": cnt,
                                           "reclassified": {"%s->%s" % k: n for k, n in moved.items()},
                                           "hits": out}, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
print(json.dumps({"counts": cnt, "reclassified": {"%s->%s" % k: n for k, n in moved.items()},
                  "zone_rows": sorted({x["row"] for x in out if x["disposition"] == "zone"})}))
for h in verse_only:
    print("VERSE_ONLY", h["row"], h["field"], h["match"], "|", h["context"][:100])
