"""CWO-1COR-06 reference implementation (cor_controlling_rulings_r4_a1#e1).
usage: cwo06_ref.py ROWS.jsonl OUT.json   (CWO-1COR-06 and CWO-1COR-07 reference; writes OUT.json only)"""
import json, re, sys, unicodedata
from collections import Counter

SIGNS = "\u2E00\u2E01\u2E02\u2E03\u2E04\u2E05\u2E06\u2E07\u2E08\u2E09\u2E0A\u2E0B\u2E0C\u2E0D"
GCH = "\u0370-\u03FF\u1F00-\u1FFF"
RUN = re.compile("[%s%s\u2019\u02BC][%s%s\u2019\u02BC\u00B7\u0387,;.\\s]*" % (GCH, SIGNS, GCH, SIGNS))
LOC = re.compile(r"(?<![\w:])rp:1Cor\.(\d+)\.(\d+)(?!-)")
SBLTOK = re.compile(r"(?<![\w:])sbl:1Cor\.(\d+)\.(\d+)(?:-1Cor\.(\d+)\.(\d+))?")
def load(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        l = l.rstrip("\n")
        m = re.match(r"^\ufeff?(1Cor\.\d+\.\d+)[\t ]+(.*)$", l)
        if m: d[m.group(1)] = m.group(2)
    return d
def sk(tok):
    t = unicodedata.normalize("NFD", tok).casefold().replace("\u03C2", "\u03C3")
    return "".join(c for c in t if ("\u03B1" <= c <= "\u03C9"))
def toks(s):
    return [x for x in (sk(w) for w in s.split()) if x]
def sbltoks(s):
    out, inside = [], False
    pend = False
    for w in s.split():
        flag = pend; pend = False
        if "\u2E00" in w or "\u2E01" in w: flag = True
        if "\u2E02" in w or "\u2E04" in w: inside = True
        if inside: flag = True
        if "\u2E03" in w or "\u2E05" in w: inside = False
        if "\u2E06" in w or "\u2E07" in w or "\u2E08" in w: flag = True; pend = True
        x = sk(w)
        if x: out.append((x, flag))
    return out
def find(hay, nd):
    for i in range(len(hay) - len(nd) + 1):
        if hay[i:i + len(nd)] == nd: return i
    return -1
SP = r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable"
RP, SBL = load(SP + r"\1Cor\1Cor_rp.txt"), load(SP + r"\1Cor\1Cor_sbl.txt")
pm = json.load(open(SP + r"\1Cor\pmarks_1Cor.json", encoding="utf-8"))
DIFF = set(pm["rp_sbl_differences"])
def units(r):
    for f in ("boundary_rationale", "strongest_rejected_alternative"):
        yield f, None, r.get(f) or ""
    for i, x in enumerate(r.get("boundary_evidence_refs") or []):
        yield "boundary_evidence_refs", i, x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)
def quotes(s):
    for m in LOC.finditer(s):
        v = "1Cor.%s.%s" % m.groups()
        a = s[m.end():]
        pre = re.match(r'^(\s*\[[^\]]*\])?\s*[("\u201C]?', a)
        q = RUN.match(a[pre.end():])
        if q and re.search("[%s]" % GCH, q.group(0)):
            yield v, q.group(0).strip(), "after"
        if m.start() >= 2 and s[m.start() - 2:m.start()] == " (":
            b = s[:m.start() - 2]
            k = len(b)
            while k > 0 and (re.match("[%s%s\u2019\u02BC\u00B7\u0387,;.\\s]" % (GCH, SIGNS), b[k - 1])): k -= 1
            q2 = b[k:].strip()
            if re.search("[%s]" % GCH, q2): yield v, q2, "before"
def covered(r, v):
    c, vs = v.split(".")[1:]; c, vs = int(c), int(vs)
    txt = json.dumps(r, ensure_ascii=False)
    exact, rng = False, False
    for m in SBLTOK.finditer(txt):
        a, b, e, f = m.groups()
        a, b = int(a), int(b)
        if e is None:
            if (a, b) == (c, vs): exact = True
        else:
            if (a, b) <= (c, vs) <= (int(e), int(f)): rng = True
    return exact, rng
SITES = pm["sbl_variant_sites"]
SPL = re.compile(r"(?<=[.;])\s+")
def pv(x): return tuple(int(y) for y in x.split(".")[1:])
def sweep06(rows):
    hits = []
    for r in rows:
        seen = set()
        for f, i, s in units(r):
            for v, q, side in quotes(s):
                if v not in DIFF: continue
                qt = toks(q); st = sbltoks(SBL.get(v, "")); st0 = [a for a, b in st]
                js = find(st0, qt)
                if js < 0: kind = "wording_absent_from_sbl"
                elif any(b for a, b in st[js:js + len(qt)]): kind = "on_sign"
                else: continue
                ex, rg = covered(r, v)
                key = (r["decision_id"], v, tuple(qt))
                if ex or key in seen: continue
                seen.add(key)
                hits.append({"row": r["decision_id"], "field": f, "index": i, "verse": v, "quote": q, "kind": kind, "range_token": rg})
    return hits
def sweep07(rows):
    out = []
    for r in rows:
        a, b = r["span"].split("-") if "-" in r["span"] else (r["span"], r["span"])
        a, b = pv(a), pv(b)
        strs = [r.get(f) or "" for f in ("boundary_rationale", "strongest_rejected_alternative", "device_notes")]
        us = [u for s in strs for u in SPL.split(s)]
        us += [x if isinstance(x, str) else json.dumps(x, ensure_ascii=False) for f in ("observed_substrate_signals", "boundary_evidence_refs") for x in (r.get(f) or [])]
        for k in SITES:
            c, v = pv(k)
            if a <= (c, v) <= b and not any(re.search(r"sbl:1Cor\.%d\.%d(?!\d)" % (c, v), u) or (re.search(r"(?<![\d:])%d:%d(?!\d)" % (c, v), u) and "SBL" in u) for u in us):
                out.append({"row": r["decision_id"], "verse": "%d:%d" % (c, v)})
    return out
if __name__ == "__main__":
    rows_p, out_p = sys.argv[1:3]
    rows = [json.loads(x) for x in open(rows_p, encoding="utf-8") if x.strip()]
    h6, h7 = sweep06(rows), sweep07(rows)
    res = {"rows": len(rows), "cwo06_hits": len(h6), "cwo06_rows": len({h["row"] for h in h6}), "cwo06_range_token": sum(h["range_token"] for h in h6),
           "cwo06_by_kind": dict(Counter(h["kind"] for h in h6)), "cwo07_unlisted": len(h7), "cwo07_rows": len({h["row"] for h in h7}), "cwo06": h6, "cwo07": h7}
    json.dump(res, open(out_p, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=0)
    print({k: v for k, v in res.items() if k not in ("cwo06", "cwo07")})