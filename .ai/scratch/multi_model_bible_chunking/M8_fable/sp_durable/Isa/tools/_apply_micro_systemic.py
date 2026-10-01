"""Deterministic micro-round systemic fixes over rows_v2.jsonl -> rows_v2m.jsonl.

Three classes, all mechanical, all logged per change:
  A. curly-quoted HEBREW runs -> straight quotes (curly is reserved for verbatim WEB
     English; a run containing Hebrew codepoints inside curly quotes is mis-quoted).
  B. staged-file-name register strike: 'verse_inventory.json' -> "the book's verse
     inventory" (the sanctioned phrasing).
  C. web:-prefixed refs in parashah-mark context -> oshb: (the layer is MT-keyed).
     CONSERVATIVE: only refs OUTSIDE both offset zones (identity mapping); zone-touching
     candidates are logged as residue for the micro authors, never auto-converted.
Run from SP/Isa.
"""
import json, re, sys, hashlib

sys.path.insert(0, "tools")
from isa_lib import web_to_mt  # noqa: E402

HEB = re.compile(r"[֐-׿]")
CURLY = re.compile(r"“([^“”]{1,300}?)”")
MARK_CTX = re.compile(r"SAMEKH|PE\b|setumah|petuchah|parashah|paseq", re.I)
WREF = re.compile(r"web:Isa\.(\d+)\.(\d+)")
PROSE = ["boundary_rationale", "device_notes", "strongest_rejected_alternative"]

def in_zone(ch, v):
    return ch == 9 or (ch == 63 and v == 19) or ch == 64

rows = [json.loads(l) for l in open("rows_v2.jsonl", encoding="utf-8")]
log = {"A_hebrew_unquoted": [], "B_staged_name": [], "C_reprefixed": [], "C_residue_zone": []}
for r in rows:
    rid = r["writer_decision_id"]
    for f in PROSE:
        t = r.get(f) or ""
        # A: curly-quoted Hebrew -> straight
        def fix_curly(m):
            inner = m.group(1)
            if HEB.search(inner):
                log["A_hebrew_unquoted"].append(f"{rid}.{f}")
                return '"' + inner + '"'
            return m.group(0)
        t2 = CURLY.sub(fix_curly, t)
        # B: staged file name
        if "verse_inventory.json" in t2:
            t2 = t2.replace("verse_inventory.json", "the book's verse inventory")
            log["B_staged_name"].append(f"{rid}.{f}")
        # C: web: refs in mark-context sentences (sentence-scoped)
        parts = re.split(r"(?<=[.;])\s+", t2)
        changed_sent = False
        for i, s in enumerate(parts):
            if MARK_CTX.search(s):
                def reref(m):
                    ch, v = int(m.group(1)), int(m.group(2))
                    if in_zone(ch, v):
                        log["C_residue_zone"].append(f"{rid}.{f}: {m.group(0)}")
                        return m.group(0)
                    mt = web_to_mt(ch, v)
                    mt_ch, mt_v = (mt if isinstance(mt, tuple) else (ch, v))
                    mt_ref = f"Isa.{mt_ch}.{mt_v}"
                    assert mt_ref == f"Isa.{ch}.{v}", (rid, m.group(0), mt_ref)
                    log["C_reprefixed"].append(f"{rid}.{f}: {m.group(0)}")
                    return "oshb:" + mt_ref
                ns = WREF.sub(reref, s)
                if ns != s:
                    parts[i] = ns
                    changed_sent = True
        if changed_sent:
            t2 = " ".join(parts)
        if t2 != t:
            r[f] = t2
with open("rows_v2m.jsonl", "w", encoding="utf-8", newline="\n") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
sha = hashlib.sha256(open("rows_v2m.jsonl", "rb").read()).hexdigest()[:16]
with open("_micro_systemic_log.json", "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=1)
print(json.dumps({"rows": len(rows), "out": "rows_v2m.jsonl", "sha16": sha,
                  "A_count": len(log["A_hebrew_unquoted"]), "B_count": len(log["B_staged_name"]),
                  "C_count": len(log["C_reprefixed"]), "C_residue": len(log["C_residue_zone"])}, indent=1))
