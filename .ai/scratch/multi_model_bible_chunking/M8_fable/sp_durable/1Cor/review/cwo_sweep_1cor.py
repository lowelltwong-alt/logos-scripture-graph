"""CWO-1COR-01 and CWO-1COR-02 sweep (1Cor controlling rulings cor_controlling_rulings_r1_a1#e1), predicates verbatim
from the installed rulings. TF-3 (cor_controlling_rulings_r2_a1#e1) adds CWO-1COR-04 as an addition, its predicate
verbatim from the installed E2 rulings; A, B and CWO02 are unchanged. CWO04 auto classes are proposals: every hit is
classed by hand in the coverage report. TF-4 (cor_controlling_rulings_r3_a1#e1) adds CWO-1COR-05 as an addition,
its predicate verbatim from the installed E3 rulings; A, B, CWO02 and CWO04 are unchanged. Known leakage (E2 ruling): a crediting verb more than one sentence from the
mark, or a paraphrase in neither PD2 nor VERB (e.g. a pilcrow said to decide or drive a cut), is not caught. Reads ROWS.jsonl and the installed ngram7.prose (import, read-only); writes --out only. TF-5 (cor_controlling_rulings_r4_a1#e1) adds CWO-1COR-06 and CWO-1COR-07 as additions, from the E4 reference; these two also read 1Cor_rp.txt, 1Cor_sbl.txt and pmarks_1Cor.json, read-only.
usage: cwo_sweep.py ROWS.jsonl --out FILE.json
"""
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
SP = Path("C:/wt/logos-t423-m8-fable/.ai/scratch/multi_model_bible_chunking/M8_fable/sp_durable")
sys.path.insert(0, str(SP / "1Cor" / "tools"))
from ngram7 import prose  # noqa: E402

rows_p = Path(sys.argv[1])
out_p = Path(sys.argv[sys.argv.index("--out") + 1])
A1, A2 = re.compile(r"^\s*web:"), re.compile(r"(?i)WEB paragraph|paragraph start|DISCLOSURE-mark")
B1 = re.compile(r"(?i)pilcrow|WEB paragraph|paragraph start|chapter division")
B2 = re.compile(r"(?i)corroborat|agree|join|inform|favour|support|lean|confirm")
SPLIT = re.compile(r"(?<=[.;])\s+")
GREEK = re.compile("[\u0370-\u03FF\u1F00-\u1FFF]")
L1, L2 = "Robinson-Pierpont Byzantine Textform (Unlicense)", "SBLGNT (CC BY 4.0)"
# CWO-1COR-04 (TF-3): W, P, DIS, PD2 and VERB verbatim from the E2 corpus_wide_orders predicate.
W4 = re.compile(r"(?i)\bWEB\b[^.;]{0,40}?\bparagraph(?: starts?)?|\bparagraph starts?\b|\bchapter (?:division|break)s?\b")
P4 = re.compile(r"(?i)pilcrow|\bparagraph marks?\b")
DIS4 = re.compile(r"(?i)not weighed|formatting|decides? nothing|does not decide|do not decide|never drives?|neither drives? nor corroborates?|excluded|not (?:drive|corroborate)|without deciding|informs? and does not decide")
PD2 = re.compile(r"(?i)corroborat|agree|\bjoin|confirm|support|favou?r|\blean|points? to|(?<!paragraph )(?<!-)\bmark(?:s|ed|ing)?\b|\bsignal|establish|determin")
VERB4 = re.compile(r"(?i)\b(?:falls?|stands?|sits?|opens?|starts?|breaks?|coincides?|points?|agrees?|marks?|as well|likewise|too|same|also)\b")
# CWO-1COR-05 (TF-4): PD3 verbatim from the E3 corpus_wide_orders predicate; bare 'close' is deliberately not in it.
PD3 = re.compile(r"(?i)\b(?:opens?|opened|opening|closes|closed|decides?|decided|decisive|drives?|drove|driven|driving|begins?|began|begun)\b")
S1_01_ROWS = {"W5-001", "W5-002", "W5-003", "W5-010", "W5-011", "W5-012", "W5-013", "W5-014",
              "W6-002", "W6-003", "W6-008", "W6-011", "W6-012"}


def cwo04_units(r):
    for f in ("boundary_rationale", "strongest_rejected_alternative", "device_notes"):
        v = r.get(f)
        if isinstance(v, str):
            for s in SPLIT.split(v):
                yield f, None, s
    for f in ("observed_substrate_signals", "boundary_evidence_refs"):
        for i, x in enumerate(r.get(f) or []):
            yield f, i, (x if isinstance(x, str) else json.dumps(x, ensure_ascii=False))


def cwo04_row(r):
    """CWO-1COR-04 hits of one row: W (support_use / disclosure_only / location_only), P (support_use /
    informs_compliant) and, in the S1-01/S1-01b rows, one count_excess hit per P mention after the first
    observed_substrate_signals P item."""
    rid, free_used, out = r["decision_id"], False, []
    for f, i, s in cwo04_units(r):
        hit = lambda pred, c: {"row": rid, "field": f, "index": i, "predicate": pred, "auto_class": c, "text": s}  # noqa: E731
        if W4.search(s):
            if DIS4.search(s):
                out.append(hit("W", "disclosure_only"))
            elif f == "observed_substrate_signals" and not VERB4.search(W4.sub(" ", s)):
                out.append(hit("W", "location_only"))
            else:
                out.append(hit("W", "support_use"))
        if P4.search(s):
            if PD2.search(s):
                out.append(hit("P", "support_use"))
            elif DIS4.search(s):
                out.append(hit("P", "informs_compliant"))
            if rid in S1_01_ROWS:
                n = len(P4.findall(s))
                if f == "observed_substrate_signals" and not free_used:
                    free_used, n = True, n - 1
                out += [hit("CNT", "count_excess") for _ in range(n)]
    return out


def cwo05_row(r):
    """CWO-1COR-05 hits of one row, over the CWO-1COR-04 units: P4 matches, PD2 does not, and PD3 matches the unit after
    every DIS4 match is replaced by a single space. Hits are unclassed: each is classed by hand in the coverage report."""
    return [{"row": r["decision_id"], "field": f, "index": i, "text": s} for f, i, s in cwo04_units(r)
            if P4.search(s) and not PD2.search(s) and PD3.search(DIS4.sub(" ", s))]


# CWO-1COR-06 and CWO-1COR-07 (TF-5): copied from the E4 reference cwo06_ref.py, sha f8dce30c; only its path constant changed.
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
RP, SBL = load(SP / "1Cor" / "1Cor_rp.txt"), load(SP / "1Cor" / "1Cor_sbl.txt")
pm = json.load(open(SP / "1Cor" / "pmarks_1Cor.json", encoding="utf-8"))
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

rows = [json.loads(x) for x in rows_p.read_text(encoding="utf-8").splitlines() if x.strip()]
a_hits, b_hits, c_fail = [], [], []
for r in rows:
    rid = r["decision_id"]
    for i, ref in enumerate(r.get("boundary_evidence_refs") or []):
        s = ref if isinstance(ref, str) else json.dumps(ref, ensure_ascii=False)
        if A1.search(s) and A2.search(s):
            a_hits.append({"row": rid, "field": "boundary_evidence_refs", "index": i, "ref": s})
    for f in ("boundary_rationale", "strongest_rejected_alternative", "device_notes"):
        v = r.get(f)
        if not isinstance(v, str):
            continue
        for sent in SPLIT.split(v):
            if B1.search(sent) and B2.search(sent):
                b_hits.append({"row": rid, "field": f, "sentence": sent})
    p = prose(r)
    if GREEK.search(p) and not (L1 in p and L2 in p):
        c_fail.append({"row": rid, "has_L1": L1 in p, "has_L2": L2 in p})
part = lambda h: h["row"].split("-")[0]  # noqa: E731
d_hits = [h for r in rows for h in cwo04_row(r)]
e_hits = [h for r in rows for h in cwo05_row(r)]
h6, h7 = sweep06(rows), sweep07(rows)
res = {"rows_file": str(rows_p), "rows_scanned": len(rows),
       "A": {"hits": len(a_hits), "rows": len({h["row"] for h in a_hits}), "by_part": dict(Counter(map(part, a_hits))),
             "list": a_hits},
       "B": {"hits": len(b_hits), "rows": len({h["row"] for h in b_hits}), "by_part": dict(Counter(map(part, b_hits))),
             "list": b_hits},
       "CWO02": {"fail": len(c_fail), "of": len(rows), "list": c_fail},
       "CWO04": {"hits": len(d_hits), "rows": len({h["row"] for h in d_hits}),
                 "by_class": dict(Counter(h["auto_class"] for h in d_hits)),
                 "support_or_excess_by_part": dict(Counter(part(h) for h in d_hits
                                                           if h["auto_class"] in ("support_use", "count_excess"))),
                 "list": d_hits},
       "CWO05": {"hits": len(e_hits), "rows": len({h["row"] for h in e_hits}), "list": e_hits},
       "CWO06": {"hits": len(h6), "rows": len({h["row"] for h in h6}), "range_token": sum(h["range_token"] for h in h6),
                 "by_kind": dict(Counter(h["kind"] for h in h6)), "list": h6},
       "CWO07": {"unlisted": len(h7), "rows": len({h["row"] for h in h7}), "list": h7}}
out_p.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({k: (v if k in ("rows_scanned",) else {kk: vv for kk, vv in v.items() if kk != "list"})
                  for k, v in res.items() if k != "rows_file"}, ensure_ascii=False))
