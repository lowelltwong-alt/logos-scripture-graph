#!/usr/bin/env python3
"""CWO-EZ-04 (rulings R3(i), P2, CWO-EZ-04): ketiv+qere concatenations split with ezek_lib.kq_split, and every Hebrew
defect located and classified, as its own sweep.

Every Hebrew run in every string of every row is examined, boundary_evidence_refs included, because CWO-EZ-01 moved
the p09/p11 splices there. A run byte-present in the verse text, or among the Qere readings, is fine. Otherwise it is
classed:
  b  a ketiv+qere CONCATENATION: the raw K+Q of one note, or K + space + Q, occurs in the string. REPLACED by the
     reading the sentence names: 'qere' nearby and no 'ketiv' keeps the Qere; 'ketiv' and no 'qere' keeps the ketiv;
     otherwise both are written, labelled 'ketiv <K> / Qere <Q>'. The Qere keeps its exact note bytes (accents kept,
     morpheme separators stripped), as CWO-EZ-04 requires. Nothing is guessed, and a sentence that names neither keeps
     both readings;
  n  an NFD-only variant of verse bytes: REPLACED with the verse's exact bytes. They are canonically equivalent, so the
     content is identical; this is the normalizer's own replacement (E-01);
  a  a pointed form whose consonants equal a Qere's but whose bytes differ (a Qere quoted without its exact note bytes):
     ROUTED to the author wave with the note's bytes;
  c  a pointed form in neither the verse text nor the note layer: ROUTED to the author wave.
The manifest lists every located defect with row, field, class, the candidate verse, and what happened. The output is
re-classified afterwards: no class b or n may remain.

Usage: _cwo04_kq_split.py --in repair/rows_s1_cwo01.jsonl --out repair/rows_s2_cwo04.jsonl
"""
import argparse
import json
import re
import sys

from _sweep_common import EZ, load_rows, summary, write_sweep

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(EZ / "tools"))
from ezek_lib import kq_split, nfd, skeleton  # noqa: E402
import normalize_hebrew_in_json as NZ  # noqa: E402

RUN = re.compile(r"[֑-״]+(?:[ ־][֑-״]+)*")
POINTS = re.compile(r"[֑-ׇ]")
QERE_W = re.compile(r"\bqere\b", re.I)
KETIV_W = re.compile(r"\bketi[bv]\b", re.I)
KQ_W = re.compile(r"\bK/Q\b")
QERE_RAW = [""]   # every Qere reading in its RAW note bytes, separators stripped; filled by build()


def build():
    src, verses, skel_src = NZ.build_index()
    oshb = dict(l.split("\t", 1) for l in (EZ / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines() if "\t" in l)
    pm = json.loads((EZ / "pmarks_Ezek.json").read_text(encoding="utf-8"))
    notes = []
    for ref, ns in pm["kq"].items():
        for n in ns:
            k, q, method = kq_split(n, oshb.get(ref, ""))
            if method == "UNANCHORED":
                continue
            # kq_split works on nfd(note), but 66 of the 134 stored notes keep a non-canonical mark order, and writers
            # pasted THOSE bytes. The split falls on a base letter, and canonical reordering never moves a mark across
            # a base letter, so the same character offset splits the RAW note; asserted per note, never assumed.
            cut = len(k)
            k_raw, q_raw = n[:cut], n[cut:]
            assert nfd(k_raw) == k and nfd(q_raw) == q, "raw split does not reproduce kq_split at %s" % ref
            notes.append((ref, k_raw.replace("/", ""), q_raw.replace("/", ""), method))
    QERE_RAW[0] = " | ".join(q for _r, _k, q, _m in notes if q)
    return src, verses, skel_src, notes


def classify_string(s, src, verses, skel_src, notes):
    """Return [(class, start, end, run_or_hybrid, info)] for one string, without changing it."""
    out = []
    for ref, k, q, method in notes:
        if not k or not q:
            continue
        for hyb in (k + q, k + " " + q):
            pos = s.find(hyb)
            while pos != -1:
                out.append(("b", pos, pos + len(hyb), hyb, {"verse": ref, "ketiv": k, "qere": q, "split": method}))
                pos = s.find(hyb, pos + 1)
    covered = [(st, en) for _, st, en, _, _ in out]
    for m in RUN.finditer(s):
        run = m.group(0)
        if len(run.strip()) < 2 or any(st <= m.start() < en or st < m.end() <= en for st, en in covered):
            continue
        if run in src or run in NZ.KQ["qere"] or run in QERE_RAW[0]:
            continue
        if not POINTS.search(run):
            continue  # unpointed mentions are the normalizer's 'mention' class, not defects
        hit = NZ.find_source_bytes(run, src, verses)
        if hit is not None:
            out.append(("n", m.start(), m.end(), run, {"exact_bytes": hit}))
            continue
        sk = skeleton(run).replace(" ", "")
        qmatch = next(((ref, q) for ref, _k, q, _m in notes if q and skeleton(q).replace(" ", "") == sk), None)
        if qmatch:
            out.append(("a", m.start(), m.end(), run, {"verse": qmatch[0], "qere_note_bytes": qmatch[1]}))
        else:
            out.append(("c", m.start(), m.end(), run, {}))
    return sorted(out, key=lambda e: e[1])


def repair_string(s, events):
    """Apply class b and n replacements right-to-left; return (new_string, applied)."""
    applied = []
    for cls, st, en, old, info in sorted(events, key=lambda e: -e[1]):
        if cls == "b":
            window = s[max(0, st - 160):en + 160]
            has_q = bool(QERE_W.search(window))
            has_k = bool(KETIV_W.search(window))
            if KQ_W.search(window):
                has_q = has_k = True
            if has_q and not has_k:
                new, rule = info["qere"], "sentence names the Qere"
            elif has_k and not has_q:
                new, rule = info["ketiv"], "sentence names the ketiv"
            else:
                new, rule = "ketiv %s / Qere %s" % (info["ketiv"], info["qere"]), "sentence names both or neither: both kept, labelled"
            s = s[:st] + new + s[en:]
            applied.append({"class": "b", "old": old, "new": new, "rule": rule, "verse": info["verse"]})
        elif cls == "n":
            s = s[:st] + info["exact_bytes"] + s[en:]
            applied.append({"class": "n", "old": old, "new": info["exact_bytes"], "rule": "NFD-equivalent re-splice"})
    return s, applied


def walk(value, path, fn):
    if isinstance(value, str):
        return fn(value, path)
    if isinstance(value, list):
        return [walk(v, "%s[%d]" % (path, i), fn) for i, v in enumerate(value)]
    if isinstance(value, dict):
        return {k: walk(v, "%s.%s" % (path, k) if path else k, fn) for k, v in value.items()}
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--supersedes", help="an earlier output of this sweep that this run replaces as the chain input")
    a = ap.parse_args()
    in_p, out_p = EZ / a.inp, EZ / a.out
    src, verses, skel_src, notes = build()
    rows_in = load_rows(in_p)
    rows_out, changes, located, routed = [], [], [], []
    for r in rows_in:
        did = r["decision_id"]

        def fn(s, path):
            ev = classify_string(s, src, verses, skel_src, notes)
            for cls, st, en, old, info in ev:
                located.append({"row": did, "field": path, "class": cls, "run": old, **{k: v for k, v in info.items() if k != "exact_bytes"}})
                if cls in ("a", "c"):
                    routed.append({"row": did, "field": path, "class": cls, "run": old, **info})
            new, applied = repair_string(s, ev)
            for ap_ in applied:
                changes.append({"row": did, "field": path, **ap_})
            return new

        nr = {k: (walk(v, k, fn) if k not in ("decision_id", "span", "book", "writer_part", "parent_collection") else v)
              for k, v in r.items()}
        rows_out.append(nr)
    residual = []
    for r in rows_out:
        walk({k: v for k, v in r.items()}, "", lambda s, p: residual.extend(
            e for e in classify_string(s, src, verses, skel_src, notes) if e[0] in ("b", "n")) or s)
    extra_super = {}
    if a.supersedes:
        extra_super = {"supersedes": {"path": a.supersedes, "why": (
            "the first run matched concatenations and wrote readings in kq_split's NFD form; 66 of the 134 stored notes "
            "keep a non-canonical mark order and writers pasted those raw bytes, so 7 concatenations were missed and "
            "misclassed as 'neither layer'. This run matches and writes the RAW note bytes (separators stripped), "
            "which is what 'quote the Qere with its note bytes exactly' requires. The first run is kept as history.")}}
    m = write_sweep("CWO-EZ-04", in_p, out_p, rows_in, rows_out, changes, {
        **extra_super,
        "reading_bytes": "raw note bytes, separators stripped (never the NFD form)",
        "predicate": "every Hebrew run in every string field, boundary_evidence_refs included",
        "located_defects_by_class": {c: sum(1 for x in located if x["class"] == c) for c in ("a", "b", "c", "n")},
        "located_defects": located,
        "assert_no_b_or_n_remain_in_output": not residual,
        "routed_to_author_wave_hebrew_defects": routed,
    })
    print(json.dumps(summary(m) | {"located_defects_by_class": m["located_defects_by_class"],
                                   "assert_no_b_or_n_remain_in_output": m["assert_no_b_or_n_remain_in_output"]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
