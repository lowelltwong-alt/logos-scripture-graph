#!/usr/bin/env python3
"""CWO-EZ-10 (ezek_controlling_rulings_a1#e3): the CWO-EZ-03 long-row scan re-run over the APPLIED rows with test (c)
NARROWED. It is a deterministic REPORT and changes no row.

Predicate: every row longer than 16 verses whose unit_type is not lament_qinah, temple_measurement or land_allotment.

Tests over the row's MT verses:
  (a) UNCHANGED - messenger formulae inside the row, reported (an addressee change is not machine-decidable);
  (b) UNCHANGED - a refrain-grade verse-final close followed immediately by a messenger formula or a listed sub-onset;
  (c) NARROWED - a refrain-grade verse-final close inside the row whose two resulting parts are both >= 3 verses.
      Recognition-family closes and 'I YHWH have spoken' qualify as before. A verse-final UTTERANCE formula qualifies only
      when at least one of these holds:
        - it is stacked with a recognition-family close or 'I YHWH have spoken' in the same verse;
        - a Masoretic mark (pe or samekh) follows the verse;
        - the next verse carries an onset device: word-event (any of the 49 forms), dateline, messenger formula,
          'and you, son of man', set-your-face, hand-of-YHWH, a transport verb, 'he said to me', or 'therefore'.
      An utterance formula signing an OATH ('as I live' in the same verse) is never a (c) close.
The report lists every excluded close with its reason. A row that qualifies under (b) or narrowed (c) and is not already
ruled is routed to the controlling agent, never cut by the scan.

Families are derived by consonantal regex and their counts are ASSERTED against the rulings' digits (wide 64, 2mp 21,
Adonai 5, 2fp 2, sub-onset 23). The 49 word-event forms are the inventory's 41 + 7 lists plus MT 1:3. A drifted count
aborts the scan before anything is reported.

Usage: _cwo10_scan.py --rows <applied rows file> --out <report path>
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
sys.path.insert(0, str(EZ / "tools"))
from ezek_lib import LAST_VERSE, skeleton, web_to_mt  # noqa: E402

EXCLUDED_TYPES = {"lament_qinah", "temple_measurement", "land_allotment"}
# rows the controlling agent has ruled on as spans (G2, G8, G9, G10, C3-1, C3-2, C3-3)
RULED = {"Ezek.7.10-Ezek.7.27": "G2", "Ezek.38.1-Ezek.38.23": "G10", "Ezek.20.1-Ezek.20.26": "C3-1 (hold)",
         "Ezek.44.15-Ezek.44.31": "C3-2 (hold)", "Ezek.5.1-Ezek.5.17": "C3-3 (hold)", "Ezek.31.1-Ezek.31.18": "C3-3 (hold)",
         "Ezek.7.5-Ezek.7.27": "G2 (pre-wave span)", "Ezek.30.1-Ezek.30.19": "G8 (pre-wave span)",
         "Ezek.34.1-Ezek.34.31": "G9 (pre-wave span)"}
TAIL_OK = r"(?:\s+ועשיתי\S*)?\s*$"
TRANSPORT = re.compile(r"(?:^|\s)(?:ויביאני|ויוליכני|וישבני|ויוציאני|ויעבירני|ותשאני|ותשא אתי)(?:\s|$)")


def sk(text):
    return re.sub(r"\s+", " ", re.sub(r"[^א-ת ]", " ", skeleton(text))).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows_p = Path(a.rows) if Path(a.rows).is_absolute() else EZ / a.rows
    out_p = Path(a.out) if Path(a.out).is_absolute() else EZ / a.out
    oshb = {k: sk(v) for k, v in (l.split("\t", 1) for l in (EZ / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines() if "\t" in l)}
    inv = json.loads((EZ / "ezek_device_inventory.json").read_text(encoding="utf-8"))
    f = inv["formulae"]
    marks = json.loads((EZ / "pmarks_Ezek.json").read_text(encoding="utf-8"))["marks"]
    fam = {
        "wide_64": {k for k, t in oshb.items() if re.search(r"(?:^|\s)\S*ידע\S*\s(?:\S+\s){0,8}?כי אני יהוה", t)},
        "2mp_21": {k for k, t in oshb.items() if re.search(r"(?:^|\s)וידעתם כי אני יהוה", t)},
        "adonai_5": {k for k, t in oshb.items() if re.search(r"(?:^|\s)כי אני אדני יהוה", t)},
        "2fp_2": {k for k, t in oshb.items() if re.search(r"(?:^|\s)וידעתן כי אני יהוה", t)},
        "sub_onset_and_you_son_of_man_23": {k for k, t in oshb.items() if re.search(r"(?:^|\s)ואתה בן אדם", t)},
    }
    want = {"wide_64": 64, "2mp_21": 21, "adonai_5": 5, "2fp_2": 2, "sub_onset_and_you_son_of_man_23": 23}
    got = {k: len(v) for k, v in fam.items()}
    if got != want:
        raise SystemExit("ABORT: derived family counts %s do not reproduce the rulings' digits %s" % (got, want))
    word_event_49 = set(f["word_event_vayehi_any"]["verses_mt"]) | set(f["word_event_hayah_any"]["verses_mt"]) | {"Ezek.1.3"}
    if len(word_event_49) != 49:
        raise SystemExit("ABORT: the any-form word-event set has %d verses, not 49" % len(word_event_49))
    messenger = set(f["thus_says_the_lord_yhwh"]["verses_mt"])
    recog = (set(f["recognition_formula"]["verses_mt"]) | set(f["recognition_formula_2ms"]["verses_mt"])
             | fam["wide_64"] | fam["2mp_21"] | fam["adonai_5"] | fam["2fp_2"])
    spoken = set(f["i_am_yhwh_spoken"]["verses_mt"])
    utterance = set(f["utterance_of_the_lord_yhwh"]["verses_mt"])
    onset_sets = {"word-event": word_event_49, "dateline": set(inv["dated_oracles"]["verses_mt"]), "messenger formula": messenger,
                  "and you, son of man": fam["sub_onset_and_you_son_of_man_23"],
                  "set your face": set(f["set_your_face"]["verses_mt"]), "hand of YHWH": set(f["hand_of_yhwh_upon_me"]["verses_mt"])}
    recog_final = re.compile(r"כי אני (?:אדני )?יהוה" + TAIL_OK)
    spoken_final = re.compile(r"אני יהוה דברתי" + TAIL_OK)
    utter_final = re.compile(r"נאם אדני יהוה" + TAIL_OK)

    def next_onset(key):
        t = oshb.get(key, "")
        hits = [name for name, s in onset_sets.items() if key in s]
        if TRANSPORT.search(t):
            hits.append("transport verb")
        if re.search(r"(?:^|\s)ויאמר אלי(?:\s|$)", t):
            hits.append("he said to me")
        if re.search(r"(?:^|\s)לכן(?:\s|$)", t):
            hits.append("therefore")
        return hits

    rows = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    report = []
    for r in rows:
        c1, v1, c2, v2 = map(int, re.match(r"Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)", r["span"]).groups())
        web, cc, vv = [], c1, v1
        while (cc, vv) <= (c2, v2):
            web.append((cc, vv))
            cc, vv = (cc, vv + 1) if vv < LAST_VERSE[cc] else (cc + 1, 1)
        if len(web) <= 16 or r.get("unit_type") in EXCLUDED_TYPES:
            continue
        mt = ["Ezek.%d.%d" % web_to_mt(*w) for w in web]
        a_hits = [k for k in mt[1:] if k in messenger]
        b_hits, c_hits, excluded = [], [], []
        for i, k in enumerate(mt[:-1]):
            t, nxt = oshb.get(k, ""), mt[i + 1]
            head, tail = i + 1, len(mt) - (i + 1)
            kind = ("recognition" if k in recog and recog_final.search(t) else
                    "i_yhwh_have_spoken" if k in spoken and spoken_final.search(t) else
                    "utterance" if k in utterance and utter_final.search(t) else None)
            if kind is None:
                continue
            if kind == "utterance":
                if re.search(r"(?:^|\s)חי אני(?:\s|$)", t):
                    excluded.append({"close": k, "reason": "signs an oath ('as I live' in the same verse)"})
                    continue
                licence = []
                if k in recog or k in spoken:
                    licence.append("stacked with a recognition-family or 'I YHWH have spoken' close")
                if marks.get(k):
                    licence.append("mark after the verse: %s" % "+".join(marks[k]))
                onset = next_onset(nxt)
                if onset:
                    licence.append("next verse %s carries: %s" % (nxt, ", ".join(onset)))
                if not licence:
                    excluded.append({"close": k, "reason": "bare utterance signature: no stacked close, no mark, no onset device at %s" % nxt})
                    continue
            else:
                licence = ["%s close (unchanged)" % kind]
            entry = {"close": k, "kind": kind, "licence": licence, "parts": [head, tail], "both_parts_ge_3": head >= 3 and tail >= 3}
            c_hits.append(entry)
            if nxt in messenger or nxt in fam["sub_onset_and_you_son_of_man_23"]:
                b_hits.append({"close": k, "next": nxt, "next_is": "messenger" if nxt in messenger else "sub_onset"})
        qualifies = bool(b_hits) or any(h["both_parts_ge_3"] for h in c_hits)
        ruled = RULED.get(r["span"])
        status = ("ruled (%s)" % ruled if ruled else
                  "QUALIFIES under (b)/narrowed (c) and is unruled - route to the controlling agent; the scan cuts nothing" if qualifies else
                  "holds under (b)/(c); (a) messenger formulae inside - addressee change not machine-decided" if a_hits else
                  "holds")
        report.append({"row": r["decision_id"], "span": r["span"], "verses": len(web), "unit_type": r.get("unit_type"),
                       "a_messenger_formulae_inside": a_hits, "b_close_then_onset": b_hits, "c_closes": c_hits,
                       "c_excluded": excluded, "qualifies": qualifies, "status": status})
    out = {"schema": "m8_cwo10_scan.v1", "cwo": "CWO-EZ-10", "book": "Ezek", "ordered_by": "ezek_controlling_rulings_a1#e3",
           "narrowed_predicate_label": "every row of the applied rows file longer than 16 verses whose unit_type is not lament_qinah, "
                                       "temple_measurement or land_allotment - the CWO-EZ-03 predicate re-evaluated on the new spans",
           "rows_file": {"path": str(rows_p), "sha256": hashlib.sha256(rows_p.read_bytes()).hexdigest()},
           "families_asserted": got, "word_event_forms": len(word_event_49), "rows_scanned": len(report), "rows": report,
           "routed_to_controlling_agent": [x["span"] for x in report if x["status"].startswith("QUALIFIES")],
           "limit": "a deterministic scan; test (a) reports messenger formulae but cannot judge an addressee change"}
    body = json.dumps(out, ensure_ascii=False, indent=1)
    if out_p.exists() and out_p.read_text(encoding="utf-8") != body:
        raise SystemExit("ABORT: %s exists with different content" % out_p)
    out_p.write_text(body, encoding="utf-8", newline="\n")
    print(json.dumps({"rows_scanned": len(report), "routed": out["routed_to_controlling_agent"],
                      "by_status": {s: [x["span"] for x in report if x["status"] == s] for s in sorted({x["status"] for x in report})},
                      "excluded_closes": sum(len(x["c_excluded"]) for x in report)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
