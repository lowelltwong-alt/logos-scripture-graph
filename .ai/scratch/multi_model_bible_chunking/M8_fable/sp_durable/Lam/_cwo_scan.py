#!/usr/bin/env python3
"""Deterministic corpus-wide-order scanner (E-18 execution parity), Lamentations. The boss ledger
(reviews/boss_lam_b1.json corpus_wide_orders, 13 entries) is the controlling text; this tool carries each
order to execution as its OWN sweep over the given corpus: the EXACT arms (CWO-1, CWO-2, CWO-4, CWO-6,
CWO-10) return candidate rows with byte evidence and are re-run after the wave (each must return 0
candidates); the HEURISTIC arms (CWO-3, 5, 7, 8, 9, 11, 12, 13) return per-row screen evidence over the
whole 26-row scope (the author reads and disposes; the screen over-collects by design). Digits are the
tool's COUNTS. Usage: _cwo_scan.py rows_vN.jsonl [--json out.json]"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE / "tools"
sys.path.insert(0, str(TOOLS))
import lam_lib  # noqa: E402

SPAN = re.compile(r"^Lam\.(\d+)\.(\d+)-Lam\.(\d+)\.(\d+)$")
PROSE4 = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")
PROSE3 = ("boundary_rationale", "strongest_rejected_alternative", "device_notes")
SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Zא-ת\"'(])")
# CWO-1 AS NARROWED BY BOSS RULING B3-1 (2026-09-07). The issued order (boss_lam_b1.json, unedited) banned the bare
# tokens samekh and pe as mark-layer names. In this book both are ALSO Hebrew letter names, and the acrostic letters are
# a tier-1 byte fact while the marks are tier-3 single-witness; banning the letter name because it collides with a mark
# name is itself the letter/mark conflation the hazard catalog forbids. The boss narrowed the scope: the homonyms are
# letter names when and only when they stand under acrostic.* without mark wording. R2 additionally CLOSES a hole in the
# issued list (closure.pe would have passed it), so the narrowed rule is stricter in one respect and looser in another.
CWO1_LABEL = "CWO-1 as narrowed by B3-1 (2026-09-07)"
CWO1_MARK_ALWAYS = {"parashah", "parashot", "parashiyot", "petuchah", "setumah", "mark", "marks", "marked", "marker", "markers"}
CWO1_HOMONYM = {"pe", "samekh"}
CWO1_MARK_CONTEXT = {"close", "closes", "closed", "closing", "closure", "end", "ends", "ending", "poem", "section",
                     "sections", "break", "division", "open", "opens", "opening", "layer", "inventory", "seg", "segs",
                     "segment", "type"}
CWO1_TRANSLIT = {"samech": "samekh", "samek": "samekh", "peh": "pe", "fe": "pe", "feh": "pe",
                 "parasha": "parashah", "parsha": "parashah", "parshah": "parashah",
                 "petucha": "petuchah", "petuhah": "petuchah", "setuma": "setumah"}


def cwo1_verdict(key):
    """Return (rejected: bool, rule: str|None) for one observed_substrate_signals key under CWO-1/B3-1."""
    kl = key.lower()
    prefix = kl.split(".", 1)[0]
    toks = {CWO1_TRANSLIT.get(t, t) for t in re.split(r"[._]", kl) if t}
    if toks & CWO1_MARK_ALWAYS:
        return True, "R1 mark-layer token under any prefix"
    if (toks & CWO1_HOMONYM) and prefix != "acrostic":
        return True, "R2 letter/mark homonym outside the acrostic namespace"
    if (toks & CWO1_HOMONYM) and (toks & CWO1_MARK_CONTEXT):
        return True, "R3 letter/mark homonym paired with mark wording"
    return False, None


CWO1_VECTORS = {
    "acrostic.triplet_nun_samekh_pe_partial": False, "acrostic.triplet_pe_partial_ayin_tsade": False,
    "acrostic.letter_boundary": False, "acrostic.triplet_alef_bet_gimel": False, "closure.wrath_inclusio": False,
    "closure.imprecatory_close": False, "hymn.eternal_throne": False, "acrostic.samekh_stanza": False,
    "acrostic.pe_before_ayin_order": False, "acrostic.triplet_pe_onset": False, "closure.unresolved_close": False,
    "closure.poem_end_pe": True, "hymn.pe_close": True, "divine_title.samekh": True, "acrostic.pe_close": True,
    "acrostic.samekh_mark": True, "acrostic.triplet_samekh_setumah": True, "closure.pe": True,
    "acrostic.triplet_pe_partial_closing": True, "acrostic.pe_section": True, "parashah.pe": True,
    "closure.samech_close": True, "acrostic.triplet_samech_setuma": True, "acrostic.peh_closed": True,
    "voice.marks": True, "closure.pe_mark": True, "acrostic.samekh_layer": True, "closure.PE_close": True,
    "acrostic.triplet_pos16_partial_entry_mark": True,
}
_bad = [k for k, want in CWO1_VECTORS.items() if cwo1_verdict(k)[0] != want]
assert not _bad, f"CWO-1/B3-1 predicate fails the boss's test vectors: {_bad}"
# CWO-2 universals (boss list) + the digit/unit test (boss list; singular admitted)
UNIV = re.compile(r"\b(only|never|first|last|sole|solely|unique|alone|each|every|densest|nowhere|no other|no further|whole-book|entire|throughout|always)\b", re.I)
UNIV_EXEMPT = re.compile(r"\b(first|second|third)[- ](person|plural|singular)\b", re.I)   # a grammatical person label is not an exclusivity word
DIGIT_UNIT = re.compile(r"\b\d+\s+(?:[A-Za-z-]+\s+){0,2}(verses?|occurrences?|tokens?|marks?|segments?|notes?|sites?|hits?)\b", re.I)
# CWO-6 literal phrases (boss list); "this unit" exempt
CWO6 = ["the following span", "the previous span", "the preceding span", "the next span", "the group before", "the group after",
        "the span before", "the span after", "that row", "this row", "cross-part", "the neighbouring unit", "the neighboring unit",
        "the adjacent unit", "held for the following", "argued in the previous", "left behind", "the unit before", "the unit after"]
# CWO-10 disclosure test
KQ_DISC = re.compile(r"(ketiv|kethib|qere|q[eə]r[eê]|K/Q|K-Q|kq)", re.I)
KQ_BOTH = re.compile(r"(both notes|two notes|2 notes|doubled|second note|two variant|2 variant|both variant)", re.I)
# CWO-4 named two-token formulas (English name -> skeleton form)
FORMULAS = [(re.compile(r"daughter[- ]of[- ]zion|bat[- ]?(?:tsiyon|zion|ṣiyyon|siyyon)", re.I), "בת ציון", "daughter-of-Zion"),
            (re.compile(r"daughter[- ]of[- ]jerusalem|bat[- ]?(?:yerushala[iy]?m)", re.I), "בת ירושלם", "daughter-of-Jerusalem"),
            (re.compile(r"daughter[- ]of[- ]judah|bat[- ]?yehudah", re.I), "בת יהודה", "daughter-of-Judah"),
            (re.compile(r"daughter[- ]of[- ]edom|bat[- ]?edom", re.I), "בת אדום", "daughter-of-Edom"),
            (re.compile(r"daughter[- ]of[- ]my[- ]people|bat[- ]?ammi", re.I), "בת עמי", "daughter-of-my-people")]
# CWO-5 screen
MARK_TERM = re.compile(r"\b(parashah|setumah|petuchah|samekh|pe[- ]mark|closed paragraph|open paragraph|paragraph mark|mark layer|SAMEKH|PE)\b")
DRIVER = re.compile(r"\b(argues?|argued|marks|carries|carried|establish(?:es|ed)?|licens(?:es|ed)|warrants?|warranted|justif(?:ies|ied)|is why|drives?|grounds?|anchors?|decides?|fixes|sets the seam|argues for keeping)\b", re.I)
# CWO-7 form-class labels
FORM = re.compile(r"\b(first[- ]person|second[- ]person|third[- ]person|masculine|feminine|singular|plural|imperative|jussive|cohortative|participle|perfect|prefix[- ]conjugation|suffix[- ]conjugation|suffix class|object suffix|independent pronoun|[123](?:ms|fs|cs|mp|fp|cp)\b|imperfect|infinitive|vocative)", re.I)
OSHB_REF = re.compile(r"oshb:Lam\.(\d+)\.(\d+)")
REF = re.compile(r"\bLam\.(\d+)\.(\d+)\b")


def load(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def span_range(r):
    m = SPAN.match(r["span"]); return (int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))


def main():
    rows_path = Path(sys.argv[1]).resolve()
    rows = load(rows_path)
    vm = json.load(open(TOOLS / "verse_map_oshb.json", encoding="utf-8-sig"))
    pm = json.load(open(HERE / "pmarks_Lam.json", encoding="utf-8-sig"))
    kq = {k: int(v) for k, v in pm["kq"].items()}
    order = []   # book-linear verse list
    for ch in sorted(lam_lib.LAST_VERSE):
        for v in range(1, lam_lib.LAST_VERSE[ch] + 1):
            order.append((ch, v))
    lin = {cv: i for i, cv in enumerate(order)}
    skel_text = {cv: lam_lib.skeleton(vm[f"Lam.{cv[0]}.{cv[1]}"]["text"]) for cv in order}
    assert len(order) == 154, len(order)

    def sweep_skel(sk):
        return [cv for cv in order if sk and sk in skel_text[cv]]

    def edges(r):
        s, e = span_range(r); i, j = lin[s], lin[e]
        return (order[i - 1] if i > 0 else None), (order[j + 1] if j + 1 < len(order) else None), s, e

    def fields_all(r):
        for k, v in r.items():
            if isinstance(v, str):
                yield k, v
            elif isinstance(v, list):
                yield k, " | ".join(str(x) for x in v)

    out = {"corpus": str(rows_path), "rows": len(rows), "orders": {}}
    # ---- CWO-1 (exact): parashah-mark-layer tokens in oss keys
    c1 = []
    for r in rows:
        for k in r["observed_substrate_signals"]:
            rejected, rule = cwo1_verdict(k)
            if rejected:
                c1.append({"row": r["decision_id"], "key": k, "rule": rule})
    out["orders"]["CWO-1"] = {"arm": "exact (oss key token rules R1-R3)", "predicate": CWO1_LABEL, "candidates": c1,
                              "vectors_selftested": len(CWO1_VECTORS)}
    # ---- CWO-2 (exact): universals without a same-sentence digit+unit citation
    c2 = []
    QUOTED = re.compile("\u201c[^\u201d]*\u201d")   # SCANNER CORRECTIONS 2026-09-07: a verbatim run inside one closed curly pair
    for r in rows:
        for f in PROSE4:
            # the order governs the ROW'S OWN claims; words inside a verbatim quotation belong to the translation, and
            # E-15 requires that quotation to stay verbatim. Quoted runs are stripped from the WHOLE FIELD before the
            # sentence split, because a quotation regularly spans a sentence boundary and a per-sentence strip would
            # miss its second half.
            field_unquoted = QUOTED.sub(" ", r.get(f, ""))
            for s in SENT.split(field_unquoted):
                s2 = UNIV_EXEMPT.sub("", s)
                if UNIV.search(s2) and not DIGIT_UNIT.search(s):
                    c2.append({"row": r["decision_id"], "field": f, "words": sorted({m.group(1).lower() for m in UNIV.finditer(s2)}), "sentence": s.strip()[:400]})
    out["orders"]["CWO-2"] = {"arm": "exact (sentence-level universal without digit+unit)", "candidates": c2,
                              "sentences_flagged": len(c2), "rows_flagged": len({c["row"] for c in c2})}
    # ---- CWO-4 (exact): spliced forms / named formulas hitting the verse just outside either seam, undisclosed in device_notes
    c4, c4_all = [], []
    for r in rows:
        prev, nxt, s, e = edges(r)
        dn = r.get("device_notes", "")
        probes = []
        for f in PROSE3:
            txt = r.get(f, "")
            for m in lam_lib.HEB_RUN.finditer(txt):
                sk = lam_lib.skeleton(m.group(0)).strip()
                if len(sk.replace(" ", "")) < 3:
                    continue
                after = txt[m.end():m.end() + 60]; mm = OSHB_REF.search(after)
                probes.append({"kind": "splice", "field": f, "form": m.group(0), "skeleton": sk, "cited": (f"Lam.{mm.group(1)}.{mm.group(2)}" if mm else None)})
            for rx, sk, name in FORMULAS:
                if rx.search(txt):
                    probes.append({"kind": "formula", "field": f, "form": name, "skeleton": sk, "cited": None})
        seen = set()
        for p in probes:
            key = (p["kind"], p["skeleton"])
            if key in seen:
                continue
            seen.add(key)
            hits = sweep_skel(p["skeleton"])
            adj = [cv for cv in (prev, nxt) if cv and cv in hits]
            if not adj:
                continue
            inside = [cv for cv in hits if s <= cv <= e]
            for cv in adj:
                out_ref = f"Lam.{cv[0]}.{cv[1]}"
                in_refs = [f"Lam.{a}.{b}" for a, b in inside]
                disclosed_out = out_ref in dn
                # SCANNER CORRECTIONS 2026-09-07: "name BOTH the in-span verse and the out-of-span verse" presupposes
                # the form occurs in-span; where every occurrence lies outside, the satisfiable requirement is that the
                # disclosure be anchored to a verse of the span itself
                if in_refs:
                    disclosed_in = any(x in dn for x in in_refs)
                else:
                    disclosed_in = any(f"Lam.{a}.{b}" in dn for a, b in order[lin[s]:lin[e] + 1])
                allprose = " ".join(r.get(f, "") for f in PROSE4)
                rec = {"row": r["decision_id"], "span": r["span"], "kind": p["kind"], "field": p["field"], "form": p["form"], "skeleton": p["skeleton"],
                       "hits_book_wide": len(hits), "in_span_hits": in_refs, "adjacent_out_of_span": out_ref, "cited_ref": p["cited"],
                       "device_notes_names_out_of_span": disclosed_out, "device_notes_names_in_span": disclosed_in,
                       "row_prose_names_out_of_span_anywhere": out_ref in allprose, "row_prose_names_an_in_span_hit_anywhere": any(x in allprose for x in in_refs)}
                c4_all.append(rec)
                if not (disclosed_out and disclosed_in):
                    c4.append(rec)
    out["orders"]["CWO-4"] = {"arm": "exact (splice/formula sweep vs seam edges; device_notes names the out-of-span verse and an in-span verse - the carrying verse where one exists, otherwise a verse of the span)", "candidates": c4, "adjacencies_total": len(c4_all), "all": c4_all}
    # ---- CWO-6 (exact): positional / neighbouring-unit phrases
    c6 = []
    for r in rows:
        for f, txt in fields_all(r):
            low = txt.lower()
            for ph in CWO6:
                for m in re.finditer(re.escape(ph), low):
                    c6.append({"row": r["decision_id"], "field": f, "phrase": ph, "context": txt[max(0, m.start() - 50):m.end() + 50]})
    out["orders"]["CWO-6"] = {"arm": "exact (literal phrase scan over every field)", "candidates": c6}
    # ---- CWO-10 (exact): oshb: splices at K/Q verses without the disclosure in the same field
    c10, c10_all = [], []
    for r in rows:
        for f in PROSE3:
            txt = r.get(f, "")
            # a SPLICE is a pointed Hebrew run with an oshb: ref attached (the ref that follows it); a bare citation is not a splice
            spliced = {}
            for m in lam_lib.HEB_RUN.finditer(txt):
                mm = OSHB_REF.search(txt[m.end():m.end() + 60])
                if mm:
                    spliced.setdefault(f"Lam.{mm.group(1)}.{mm.group(2)}", []).append(m.group(0))
            for ref, forms in sorted(spliced.items()):
                if ref not in kq:
                    continue
                disc = bool(KQ_DISC.search(txt)); both = bool(KQ_BOTH.search(txt)) if kq[ref] > 1 else True
                rec = {"row": r["decision_id"], "field": f, "ref": ref, "kq_notes": kq[ref], "spliced_forms": forms, "disclosure_in_field": disc, "both_notes_named": both}
                c10_all.append(rec)
                if not (disc and both):
                    c10.append(rec)
    out["orders"]["CWO-10"] = {"arm": "exact (pointed Hebrew runs with an attached oshb: ref x the K/Q inventory; same-field disclosure test; a bare citation without a spliced run is not a splice)", "candidates": c10, "kq_splices_total": len(c10_all), "all": c10_all}
    # ---- heuristic arms: per-row screen evidence over the whole scope
    h3, h5, h7, h8, h9, h11, h12, h13 = [], [], [], [], [], [], [], []
    for r in rows:
        rid = r["decision_id"]; s, e = span_range(r); nverses = lin[e] - lin[s] + 1
        cites = []
        for f in PROSE4:
            for sent in SENT.split(r.get(f, "")):
                if re.search(r"\d", sent) and re.search(r"sweep|verses?|occurrences?|tokens?|marks?|segments?|notes?|sites?|hits?", sent, re.I):
                    cites.append({"field": f, "sentence": sent.strip()[:300]})
        h3.append({"row": rid, "digit_bearing_citations": len(cites), "citations": cites})
        hits5 = []
        for f in ("boundary_rationale", "strongest_rejected_alternative"):
            for sent in SENT.split(r.get(f, "")):
                if MARK_TERM.search(sent) and DRIVER.search(sent):
                    hits5.append({"field": f, "sentence": sent.strip()[:300]})
        h5.append({"row": rid, "mark_plus_driver_sentences": len(hits5), "hits": hits5})
        labels = []
        for f in PROSE4:
            for m in FORM.finditer(r.get(f, "")):
                labels.append({"field": f, "label": m.group(0), "context": r[f][max(0, m.start() - 40):m.end() + 40]})
        h7.append({"row": rid, "form_class_labels": len(labels), "labels": labels})
        h8.append({"row": rid, "unit_type": r["unit_type"], "literature_type_guess": r.get("literature_type_guess", "")[:200], "span": r["span"], "span_verses": nverses,
                   "device_notes_mentions_unit_type": r["unit_type"].replace("_", " ") in r.get("device_notes", "").replace("_", " ")})
        h9.append({"row": rid, "span": r["span"], "keys": list(r["observed_substrate_signals"])})
        sra = r.get("strongest_rejected_alternative", "")
        h11.append({"row": rid, "span": r["span"], "refs_in_sra": sorted({f"Lam.{m.group(1)}.{m.group(2)}" for m in REF.finditer(sra)}), "sra_head": sra[:200]})
        h12.append({"row": rid, "span": r["span"], "confidence": r["confidence"], "frontier_flag_considered": r["frontier_flag_considered"],
                    "whole_poem": (s[1] == 1 and e[1] == lam_lib.LAST_VERSE[e[0]] and s[0] == e[0]), "screen": ("high confidence: name a tier-1 signal at BOTH seams or lower" if r["confidence"] == "high" else "check both seams; lower where a seam rests on continuity / tier-3-only / held-open")})
        runs = []
        for f in ("boundary_rationale", "device_notes"):
            for m in lam_lib.HEB_RUN.finditer(r.get(f, "")):
                runs.append({"field": f, "form": m.group(0), "context": r[f][max(0, m.start() - 60):m.end() + 80]})
        h13.append({"row": rid, "hebrew_splices": len(runs), "runs": runs})
    out["orders"]["CWO-3"] = {"arm": "heuristic (every digit-bearing sweep citation re-derived; author reads form classes off the bytes)", "candidates": h3}
    out["orders"]["CWO-5"] = {"arm": "heuristic (mark term + driver verb co-occurrence screen; author reads the governing relation)", "candidates": h5, "screen_hits_rows": len([x for x in h5 if x["mark_plus_driver_sentences"]])}
    out["orders"]["CWO-7"] = {"arm": "heuristic (form-class labels re-derived from the pointed bytes)", "candidates": h7}
    out["orders"]["CWO-8"] = {"arm": "heuristic (unit_type carried by the row's own bytes or one deviation sentence with true arithmetic)", "candidates": h8}
    out["orders"]["CWO-9"] = {"arm": "heuristic (every oss key has a byte object at a verse inside the span)", "candidates": h9}
    out["orders"]["CWO-11"] = {"arm": "heuristic (rejected alternative resolves to a contiguous range and is argued FOR the alternative)", "candidates": h11}
    out["orders"]["CWO-12"] = {"arm": "heuristic (high confidence only with a tier-1 signal at BOTH seams; whole-poem cap separate and hard)", "candidates": h12, "high_rows": [x["row"] for x in h12 if x["confidence"] == "high"]}
    out["orders"]["CWO-13"] = {"arm": "heuristic (gloss extent = splice extent)", "candidates": h13}
    summary = {}
    for k in ("CWO-1", "CWO-2", "CWO-4", "CWO-6", "CWO-10"):
        summary[k] = {"arm": "exact", "candidate_items": len(out["orders"][k]["candidates"]), "rows": len({c["row"] for c in out["orders"][k]["candidates"]})}
    for k in ("CWO-3", "CWO-5", "CWO-7", "CWO-8", "CWO-9", "CWO-11", "CWO-12", "CWO-13"):
        summary[k] = {"arm": "heuristic", "scope_rows": len(out["orders"][k]["candidates"]),
                      "screen_hit_rows": (out["orders"][k].get("screen_hits_rows") if k == "CWO-5" else (len(out["orders"][k]["high_rows"]) if k == "CWO-12" else None))}
    out["summary"] = summary
    # B3-1 history rule: every CWO-1 report carries the narrowed-predicate label, so a reader comparing scans
    # across the wave knows which predicate produced which digit. Both digits live in
    # cwo/cwo1_predicate_label.v1.json; reporting only the narrowed one would imply the order was satisfied
    # as issued, and it was not - it was narrowed by a recorded ruling.
    out["cwo1_predicate_label"] = CWO1_LABEL
    out["cwo1_predicate_note"] = ("CWO-1 digits here are computed under the NARROWED predicate; the issued "
                                  "token list returns a different digit. Both are stated in "
                                  "cwo/cwo1_predicate_label.v1.json.")
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
