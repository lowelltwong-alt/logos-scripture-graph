#!/usr/bin/env python3
"""Deterministic corpus-wide-order scanner (E-18 execution parity), Jeremiah. Each CWO executes as
its OWN sweep: this tool produces, per order, the candidate row list from the given corpus so the
CWO wave's orders are built from the tool's COUNT and the post-wave verification re-runs the same
scan. Candidates are triage inputs where the arm is heuristic (CWO-4/6/7 prose arms); CWO-1/3/5/9
arms are exact. Usage: _cwo_scan.py rows.jsonl [--json out.json]"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE / "tools"
SPAN = re.compile(r"^Jer\.(\d+)\.(\d+)-Jer\.(\d+)\.(\d+)$")
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes")
HEB = re.compile(r"[֐-׿]")
CWO4_SITES = ["5.19", "7.28", "8.4", "11.3", "13.12", "13.13", "14.17", "15.2", "16.11", "17.20", "19.11", "23.33",
              "25.27", "25.28", "25.30", "26.4", "38.26", "43.10"]   # MT = WEB at every site (none in the zone)


def load(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def span_range(r):
    m = SPAN.match(r["span"]); return (int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))


def covers(r, ch, v):
    s, e = span_range(r); return s <= (ch, v) <= e


def skel(s):
    return re.sub(r"[֑-ׇ]", "", s).replace("־", " ")


def main():
    rows_path = Path(sys.argv[1]).resolve()
    rows = load(rows_path)
    vm = json.load(open(TOOLS / "verse_map_oshb.json", encoding="utf-8"))
    sys.path.insert(0, str(TOOLS))
    import jer_lib  # one-zone injective crosswalk: WEB (ch, v) -> MT (ch, v)

    def verse_text(ch, v):
        """WEB (ch, v) -> the MT verse text via the crosswalk (zone-safe)."""
        mt = jer_lib.web_to_mt(ch, v)
        mch, mv = (mt if isinstance(mt, tuple) else (mt["ch"], mt["v"]))
        e = vm.get(f"Jer.{mch}.{mv}")
        return e if isinstance(e, str) else (e.get("text") or e.get("tokens") if isinstance(e, dict) else None)

    out = {"corpus": str(rows_path), "rows": len(rows), "orders": {}}
    # CWO-1: ngram7 gate over the corpus (the tool's own count)
    p = subprocess.run([sys.executable, str(TOOLS / "ngram7.py"), str(rows_path), "--gate", "10", "--full-ids"], capture_output=True, text=True, encoding="utf-8", cwd=str(TOOLS))
    try:
        ng = json.loads(p.stdout)
    except json.JSONDecodeError:
        ng = {"unparseable": p.stdout[-800:], "stderr": p.stderr[-400:]}
    out["orders"]["CWO-1"] = {"arm": "exact (ngram7 --gate 10)", "result": ng if isinstance(ng, dict) else {"raw": ng}}
    # CWO-2: plain armies-title key on rows whose span verses carry the full stack (Elohei Yisrael after tsevaot)
    cand = []
    for r in rows:
        keys = r["observed_substrate_signals"]
        if any(k in ("divine_title.yhwh_tsevaot", "speech_formula.koh_amar_yhwh_tsevaot", "speech_formula.koh_amar_yhwh_tsevaot_onset") for k in keys):
            s, e = span_range(r)
            full = []
            for (ch, v), _t in ((k2, 0) for k2 in []):
                pass
            vmw = json.load(open(TOOLS / "verse_map_web.json", encoding="utf-8"))
            for key in vmw:
                m = re.match(r"^Jer\.(\d+)\.(\d+)$", key)
                if not m: continue
                ch, v = int(m.group(1)), int(m.group(2))
                if not (s <= (ch, v) <= e): continue
                t = skel(verse_text(ch, v) or "")
                if "צבאות אלהי ישראל" in t:
                    full.append(f"web:Jer.{ch}.{v}")
            cand.append({"row": r["decision_id"], "keys": [k for k in keys if "tsevaot" in k], "full_stack_verses_in_span": full,
                         "candidate": bool(full)})
    out["orders"]["CWO-2"] = {"arm": "exact (key + span bytes)", "rows_with_plain_key": len(cand), "candidates": [c for c in cand if c["candidate"]], "all": cand}
    # CWO-3: word_event.discourse_imperative_onset re-filing
    c3 = [r["decision_id"] for r in rows if "word_event.discourse_imperative_onset" in r["observed_substrate_signals"]]
    out["orders"]["CWO-3"] = {"arm": "exact (key)", "candidates": c3}
    # CWO-4: delivery-construction form-class: rows covering a site whose oss/prose labels an imperative
    c4 = []
    for r in rows:
        sites = [st for st in CWO4_SITES if covers(r, *map(int, st.split(".")))]
        if not sites: continue
        keys = [k for k in r["observed_substrate_signals"] if "imperative" in k]
        prose_hits = [f for f in PROSE if re.search(r"imperativ", r.get(f, ""), re.I)]
        if keys or prose_hits:
            c4.append({"row": r["decision_id"], "sites_in_span": sites, "imperative_keys": keys, "prose_fields_mentioning_imperative": prose_hits})
    out["orders"]["CWO-4"] = {"arm": "heuristic (site + imperative label) -> author re-reads the form off the bytes", "candidates": c4}
    # CWO-5: closure-classed keys whose device is absent from the row's own closing verse (neum keys)
    c5 = []
    for r in rows:
        ck = [k for k in r["observed_substrate_signals"] if "closure" in k]
        if not ck: continue
        s, e = span_range(r)
        close_t = skel(verse_text(*e) or "")
        neum_keys = [k for k in ck if "neum" in k]
        if neum_keys and "נאם" not in close_t:
            c5.append({"row": r["decision_id"], "closing_verse": f"Jer.{e[0]}.{e[1]}", "keys": neum_keys, "neum_in_closing_verse": False})
    out["orders"]["CWO-5"] = {"arm": "exact for neum-classed closure keys (B4-6 bind-or-drop)", "candidates": c5,
                              "closure_key_rows_total": sum(1 for r in rows if any("closure" in k for k in r["observed_substrate_signals"]))}
    # CWO-6: p13 device_notes byte-tier labels attached to bare coordinates (no Hebrew run within 80 chars before the label)
    c6 = []
    for r in rows:
        if r.get("writer_part") != "p13": continue
        dn = r.get("device_notes", "")
        for m in re.finditer(r"byte[- ]tier", dn, re.I):
            window = dn[max(0, m.start() - 80):m.start()]
            if not HEB.search(window) and re.search(r"\b\d{1,2}:\d{1,2}\b|Jer\.\d+\.\d+", window):
                c6.append({"row": r["decision_id"], "context": dn[max(0, m.start() - 80):m.end() + 20]})
    out["orders"]["CWO-6"] = {"arm": "heuristic (p13 device_notes)", "candidates": c6}
    # CWO-7: OAN block date labels (chs 46-51), excluding 49:34
    c7 = []
    for r in rows:
        s, e = span_range(r)
        if not (46 <= s[0] <= 51): continue
        if s == (49, 34): continue
        hits = []
        for f in PROSE + ("literature_type_guess",):
            for m in re.finditer(r"\bdat(ed|es|e)\b", r.get(f, ""), re.I):
                hits.append((f, r[f][max(0, m.start() - 60):m.end() + 60]))
        if hits:
            c7.append({"row": r["decision_id"], "span": r["span"], "hits": hits[:4]})
    out["orders"]["CWO-7"] = {"arm": "heuristic (date language in the OAN block)", "candidates": c7}
    # CWO-8: absence-as-evidence in strongest_rejected_alternative (two named rows + corpus scan of the same class)
    c8 = []
    for r in rows:
        sra = r.get("strongest_rejected_alternative", "")
        if re.search(r"\b(absence|absent|no (interior |internal )?(parashah|setumah|petuchah|mark)|lacks? (a |an )?(parashah|setumah|petuchah|mark))\b", sra, re.I):
            c8.append({"row": r["decision_id"], "text": sra[:300]})
    out["orders"]["CWO-8"] = {"arm": "heuristic (mark-absence language as rival ground) - named rows P19-008 + P19-009 plus corpus scan", "candidates": c8}
    # CWO-9: bare in-zone coordinates in prose of rows touching WEB ch 9 / MT 8:23 / MT ch 9
    c9 = []
    for r in rows:
        s, e = span_range(r)
        if not (s <= (9, 26) and e >= (8, 18)): continue
        for f in PROSE:
            for m in re.finditer(r"(?<![\w:.])(8:2[3]|9:\d{1,2})(?!\d)", r.get(f, "")):
                pre = r[f][max(0, m.start() - 12):m.start()]
                if re.search(r"(MT|WEB|web:|oshb:)\s*$", pre): continue
                c9.append({"row": r["decision_id"], "field": f, "coord": m.group(0), "context": r[f][max(0, m.start() - 40):m.end() + 30]})
    out["orders"]["CWO-9"] = {"arm": "exact (bare in-zone coordinate without MT/WEB/web:/oshb: qualifier)", "candidates": c9}
    summary = {k: (len(v["candidates"]) if isinstance(v.get("candidates"), list) else "see result") for k, v in out["orders"].items()}
    out["summary"] = summary
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
