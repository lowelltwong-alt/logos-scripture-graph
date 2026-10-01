#!/usr/bin/env python3
"""CWO-EZ-02 (rulings R2 C2 and CWO-EZ-02): Hebrew-quote binding and curly-quote stripping, as its own sweep.

The order, verbatim in substance: every Hebrew run in boundary_rationale, strongest_rejected_alternative, device_notes and
strong_or_hebrew_tags_used gets an adjacent oshb: ref in the same field where exactly one nearby cited ref collates
byte-true; curly quotes around Hebrew are stripped (Hebrew is spliced bare). Runs that collate to no nearby ref, or to a
Qere, are listed for the author wave with row, field and best candidate.

Deterministic reading, stated so a reviewer can test it:
  - a run needs binding exactly when citation_sweep's own binding would fail: it has 3 or more letters, and no oshb: ref
    among its three nearest refs in the field collates at the tier the tool requires (byte for pointed runs), counting
    the tool's Qere tier;
  - "nearby cited ref", stage 1: the verses of refs written in the SAME field (web:/oshb:/bare Ezek.C.V, MT C:V, and
    bare C:V read as WEB numbering), crosswalked to MT keys. Stage 2, only when stage 1 has no byte hit: the refs
    anywhere in the row, the row's span, and the verse on either side of it. At the first stage that has any byte hit,
    EXACTLY ONE verse must hold the run byte-true, or the run is routed with its candidates;
  - only POINTED runs are bound; the order says byte-true, and an unpointed run cannot be byte-true. Unpointed runs are
    routed with their skeleton candidates;
  - a run byte-true only in a Qere note is routed, never bound (the order);
  - the inserted ref sits immediately after the run: ' (oshb:Ezek.C.V)', or inside the numbering zone the dual
    ' (web:Ezek.W.X = oshb:Ezek.21.Y)' that §8 requires in every field;
  - curly double quotes whose content is Hebrew-dominant are removed in every prose field, keeping the content.

Usage: _cwo02_hebrew_binding.py --in repair/rows_s2_cwo04.jsonl --out repair/rows_s3_cwo02.jsonl
"""
import argparse
import json
import re
import sys

from _sweep_common import EZ, load_rows, summary, write_sweep

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(EZ / "tools"))
from ezek_lib import LAST_VERSE, collate_hebrew, kq_split, mt_to_web, web_to_mt  # noqa: E402

FIELDS = ("boundary_rationale", "strongest_rejected_alternative", "device_notes")
TAGS = "strong_or_hebrew_tags_used"
PROSE_SKIP = {"decision_id", "writer_decision_id", "span", "book", "writer_part", "parent_collection", "confidence",
              "unit_type", "model_id", "writer_attempt_id", "review_status", "boundary_evidence_refs"}
HEB_RUN = re.compile(r"[֑-״]{2,}(?:[ ־][֑-״]+)*")
POINTED = re.compile(r"[ְ-ּׁׂ֑-֯]")
OSHB_REF = re.compile(r"oshb:Ezek\.(\d+)\.(\d+)")
KQ_WORD = re.compile(r"\b(?:ketiv|qere|K/Q)\b", re.I)
REF_ANY = re.compile(r"(?:(oshb|web):)?Ezek\.(\d+)\.(\d+)(?:-(?:Ezek\.)?(\d+)(?:\.(\d+))?)?|\b(MT\s+)?(\d{1,2}):(\d{1,2})\b")
CURLY = re.compile(r"“([^”]*)”")
MARK_WORD = re.compile(r"\b(petuchah|setumah)\b|\b(pe|samekh)\b(?!\w)", re.I)
DOTTED = re.compile(r"(?<![\w.:])(\d{1,2})\.(\d{1,2})(?![\d.])")
SENT_END = re.compile(r"(?<!\d)[.;](?!\d)|\n")


def sentence_of(text, start, end):
    """The sentence holding [start, end): bounded by a period or semicolon that is not inside a dotted number."""
    lo = max([m.end() for m in SENT_END.finditer(text, 0, start)] or [0])
    nxt = SENT_END.search(text, end)
    return text[lo:nxt.start() if nxt else len(text)]


def named_verses(sentence):
    """MT keys of every verse a sentence names: witness refs, bare Ezek.C.V, C:V, and the writers' dotted C.V form."""
    keys = set(refs_in(sentence))
    for m in DOTTED.finditer(sentence):
        k = web_to_mt(int(m.group(1)), int(m.group(2)))
        if k:
            keys.add(k)
    return keys


def mt_key(kind, c, v):
    if kind == "oshb" or kind == "MT":
        return (c, v)
    return web_to_mt(c, v)


def refs_in(text):
    keys = []
    for m in REF_ANY.finditer(text):
        if m.group(2):
            kind, c, v = m.group(1) or "web", int(m.group(2)), int(m.group(3))
            ends = []
            if m.group(4):
                ec, ev = (c, int(m.group(4))) if not m.group(5) else (int(m.group(4)), int(m.group(5)))
                if (ec, ev) >= (c, v) and ec - c <= 3:
                    cc, vv = c, v
                    while (cc, vv) <= (ec, ev) and cc in LAST_VERSE:
                        ends.append((cc, vv))
                        cc, vv = (cc, vv + 1) if vv < LAST_VERSE[cc] else (cc + 1, 1)
            for cv in (ends or [(c, v)]):
                k = mt_key(kind, *cv)
                if k:
                    keys.append(k)
        else:
            k = mt_key("MT" if m.group(6) else "web", int(m.group(7)), int(m.group(8)))
            if k:
                keys.append(k)
    return keys


def span_keys(span):
    m = re.match(r"Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)", span)
    c, v, ec, ev = map(int, m.groups())
    prev = (c, v - 1) if v > 1 else (c - 1, LAST_VERSE.get(c - 1, 0))
    nxt = (ec, ev + 1) if ev < LAST_VERSE[ec] else (ec + 1, 1)
    out, cc, vv = [], c, v
    while (cc, vv) <= (ec, ev):
        out.append((cc, vv))
        cc, vv = (cc, vv + 1) if vv < LAST_VERSE[cc] else (cc + 1, 1)
    keys = [web_to_mt(*x) for x in [prev] + out + [nxt] if x[0] in LAST_VERSE and 1 <= x[1] <= LAST_VERSE[x[0]]]
    return [k for k in keys if k]


def ref_text(k):
    c, v = k
    if c == 21:
        w = mt_to_web(c, v)
        return "web:Ezek.%d.%d = oshb:Ezek.%d.%d" % (w[0], w[1], c, v)
    return "oshb:Ezek.%d.%d" % (c, v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--supersedes", help="an earlier output of this sweep that this run replaces as the chain input")
    a = ap.parse_args()
    in_p, out_p = EZ / a.inp, EZ / a.out
    oshb = dict(l.split("\t", 1) for l in (EZ / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines() if "\t" in l)
    pm = json.loads((EZ / "pmarks_Ezek.json").read_text(encoding="utf-8"))
    qere_by_key = {}
    for ref, ns in pm["kq"].items():
        c, v = int(ref.split(".")[1]), int(ref.split(".")[2])
        qere_by_key[(c, v)] = " | ".join(kq_split(n, oshb.get(ref, ""))[1].replace("/", "") for n in ns)

    def verse(k):
        return oshb.get("Ezek.%d.%d" % k, "")

    def tool_binds(field, run, pos):
        """citation_sweep's own binding test for this run: True if it already passes."""
        refs = list(OSHB_REF.finditer(field))
        if not refs:
            return False
        end = pos + len(run)
        cands = sorted(refs, key=lambda mm: (not (0 <= mm.start() - end <= 40),
                                             min(abs(mm.start() - pos), abs(mm.start() - end))))[:3]
        pointed = bool(POINTED.search(run))
        for near in cands:
            k = (int(near.group(1)), int(near.group(2)))
            tier = collate_hebrew(run, verse(k))
            if (tier == "byte") if pointed else tier != "none":
                return True
            q = qere_by_key.get(k, "")
            qt = collate_hebrew(run, q) if q.strip(" |") else "none"
            if ((qt == "byte") if pointed else qt != "none") and KQ_WORD.search(field[max(0, pos - 160):end + 160]):
                return True
        return False

    rows_in = load_rows(in_p)
    rows_out, changes, routed = [], [], []
    for r in rows_in:
        nr = json.loads(json.dumps(r, ensure_ascii=False))
        did = nr["decision_id"]
        # 1. curly quotes around Hebrew-dominant content, every prose string
        for k, v in list(nr.items()):
            if k in PROSE_SKIP:
                continue
            vals = v if isinstance(v, list) else [v]
            new_vals = []
            for i, s in enumerate(vals):
                if not isinstance(s, str):
                    new_vals.append(s)
                    continue

                def strip(m):
                    inner = m.group(1)
                    if len(re.findall(r"[א-ת]", inner)) > len(re.findall(r"[A-Za-z]", inner)):
                        return inner
                    return m.group(0)
                ns = CURLY.sub(strip, s)
                if ns != s:
                    changes.append({"row": did, "field": k if not isinstance(v, list) else "%s[%d]" % (k, i),
                                    "class": "curly_quotes_around_hebrew_removed", "count": s.count("“") - ns.count("“")})
                new_vals.append(ns)
            nr[k] = new_vals if isinstance(v, list) else new_vals[0]
        # 2. binding
        row_keys = []
        for k, v in nr.items():
            if k in ("decision_id", "writer_decision_id", "span"):
                continue
            for s in (v if isinstance(v, list) else [v]):
                if isinstance(s, str):
                    row_keys.extend(refs_in(s))
        stage2 = list(dict.fromkeys(row_keys + span_keys(nr["span"])))
        targets = [(f, None) for f in FIELDS] + [(TAGS, i) for i in range(len(nr.get(TAGS) or []))]
        for f, idx in targets:
            field = nr.get(f) if idx is None else nr[TAGS][idx]
            if not isinstance(field, str):
                continue
            path = f if idx is None else "%s[%d]" % (f, idx)
            for m in reversed(list(HEB_RUN.finditer(field))):
                run = m.group(0)
                if len(re.sub(r"[^א-ת]", "", run)) < 3 or tool_binds(field, run, m.start()):
                    continue
                pointed = bool(POINTED.search(run))
                stage1 = list(dict.fromkeys(refs_in(field)))
                chosen, stage_used, hits = None, None, []
                for stage, cands in (("same_field", stage1), ("row_and_span", stage2)):
                    hits = [k for k in cands if collate_hebrew(run, verse(k)) == "byte"] if pointed else []
                    if hits:
                        stage_used = stage
                        break
                if pointed and len(hits) == 1:
                    chosen = hits[0]
                # r2 GUARDS. The first run bound a Qere reading, and a quote whose own sentence named another verse, to
                # whichever verse happened to hold the same bytes (for example, a MT 37:22 Qere bound to 37:27), and it
                # moved the nearest ref of neighbouring pe/samekh and ketiv/qere claims. A binding must agree with what
                # the prose itself says, or it is routed.
                all_cands = list(dict.fromkeys(stage1 + stage2))
                qhits = [k for k in all_cands if qere_by_key.get(k) and collate_hebrew(run, qere_by_key[k]) != "none"]
                named = named_verses(sentence_of(field, m.start(), m.end()))
                window = field[max(0, m.start() - 120):m.end() + 120]
                guard = None
                if chosen is not None:
                    if qhits:
                        guard = "collates to a Qere (routed by the order even where another verse holds the same bytes)"
                    elif named and chosen not in named:
                        guard = "its sentence names other verses (%s)" % ", ".join("%d:%d" % k for k in sorted(named))
                    elif not named and (MARK_WORD.search(window) or KQ_WORD.search(window)):
                        guard = "an inserted ref would become the nearest ref of a pe/samekh or ketiv/qere claim"
                if guard:
                    routed.append({"row": did, "field": path, "run": run, "why": guard,
                                   "candidates": ["Ezek.%d.%d" % k for k in (qhits or hits or [chosen])]})
                    continue
                if chosen is None:
                    best = hits or [k for k in stage2 if collate_hebrew(run, verse(k)) != "none"][:3]
                    routed.append({"row": did, "field": path, "run": run,
                                   "why": ("unpointed run (byte-true binding impossible)" if not pointed else
                                           "collates to a Qere" if qhits else
                                           "several verses hold it byte-true" if len(hits) > 1 else "no nearby verse holds it"),
                                   "candidates": ["Ezek.%d.%d" % k for k in (qhits or best)]})
                    continue
                ins = " (%s)" % ref_text(chosen)
                field = field[:m.end()] + ins + field[m.end():]
                changes.append({"row": did, "field": path, "class": "oshb_ref_bound", "run": run, "inserted": ins.strip(),
                                "stage": stage_used})
            if idx is None:
                nr[f] = field
            else:
                nr[TAGS][idx] = field
        rows_out.append(nr)
    m = write_sweep("CWO-EZ-02", in_p, out_p, rows_in, rows_out, changes, {
        **({"supersedes": {"path": a.supersedes, "why": (
            "the first run bound by unique byte hit alone. It attached Qere readings, and quotes whose own sentence named "
            "another verse, to a coincidental verse match (e.g. a MT 37:22 Qere to 37:27), and it moved the nearest ref "
            "of neighbouring pe/samekh and ketiv/qere claims: mark_symmetry rose from 144 to 157 flags. This run adds three "
            "guards (Qere routed, sentence-named verse must agree, no binding inside a claim window without a named "
            "verse). The first run is kept as history.")}} if a.supersedes else {}),
        "guards": ["collates to a Qere -> routed", "sentence names other verses -> routed",
                   "no named verse and a pe/samekh or ketiv/qere word within 120 characters -> routed"],
        "predicate": "Hebrew runs failing citation_sweep's binding in the four named fields; curly quotes around Hebrew in every prose field",
        "counts": {"refs_bound": sum(1 for c in changes if c["class"] == "oshb_ref_bound"),
                   "curly_quote_pairs_removed": sum(c.get("count", 0) for c in changes if c["class"] == "curly_quotes_around_hebrew_removed"),
                   "routed": len(routed)},
        "routed_to_author_wave_unbound_hebrew": routed,
    })
    print(json.dumps(summary(m) | {"counts": m["counts"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
