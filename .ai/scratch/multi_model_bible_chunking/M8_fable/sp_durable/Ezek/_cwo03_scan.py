#!/usr/bin/env python3
"""CWO-EZ-03 (ruling CWO-EZ-03): the section 2d.6 and mid-unit-refrain re-examination, as a deterministic REPORT. It changes no
row.

Predicate (the order): every row longer than 16 verses whose unit_type is not lament_qinah, temple_measurement or
land_allotment. For each, three tests over the row's MT verses:
  (a) messenger formulae inside the row. Whether the addressee changes is NOT machine-decidable, so these are reported
      for the author wave, never judged here;
  (b) a refrain-grade VERSE-FINAL close followed immediately by a messenger formula or a listed sub-onset;
  (c) any refrain-grade verse-final close inside the row, marked as a cut candidate when both resulting parts are >= 3
      verses.
The order: where (a) or (b) holds, or (c) holds with both parts >= 3, the author wave cuts at the last qualifying close;
otherwise the row holds with the cap disclosure at <= medium_low.

Refrain-grade families (rulings S5 and CWO-EZ-03): strict recognition 28 and the 2ms form 5 (inventory), 2mp 21, the
Adonai form 5, 2fp 2, the wide family 64, the utterance formula 81 (inventory), and 'I YHWH have spoken' 14 (inventory).
Families the inventory does not carry are derived here by consonantal regex, and their verse counts are ASSERTED
against the rulings' digits. A drifted sweep aborts; it never reports. The listed sub-onset 'and you, son of man' is
derived the same way and asserted at 23.
The controlling agent already applied the test to 7:5-27, 30:1-19, 34:1-31 and ch 38; those rows are reported as
'ruled'. It expects 4:1-17, 5:1-17, 20:1-26, 23:1-21, 31:1-18 and 44:15-31 to hold, and any row whose scan disagrees is
flagged for the controlling agent rather than cut.

Usage: _cwo03_scan.py --rows repair/rows_v2_swept_r3.jsonl
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
RULED = {"Ezek.7.5-Ezek.7.27", "Ezek.30.1-Ezek.30.19", "Ezek.34.1-Ezek.34.31", "Ezek.38.1-Ezek.38.9",
         "Ezek.38.10-Ezek.38.13", "Ezek.38.14-Ezek.38.16", "Ezek.38.17-Ezek.38.23"}
EXPECTED_TO_HOLD = {"Ezek.4.1-Ezek.4.17", "Ezek.5.1-Ezek.5.17", "Ezek.20.1-Ezek.20.26", "Ezek.23.1-Ezek.23.21",
                    "Ezek.31.1-Ezek.31.18", "Ezek.44.15-Ezek.44.31"}
TAIL_OK = r"(?:\s+ועשיתי\S*)?\s*$"


def sk(text):
    """Consonants and single spaces only, so sof pasuq, paseq and any other non-letter never hides a verse-final close."""
    return re.sub(r"\s+", " ", re.sub(r"[^א-ת ]", " ", skeleton(text))).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    a = ap.parse_args()
    rows_p = EZ / a.rows
    oshb = {k: sk(v) for k, v in (l.split("\t", 1) for l in (EZ / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines() if "\t" in l)}
    inv = json.loads((EZ / "ezek_device_inventory.json").read_text(encoding="utf-8"))["formulae"]
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
    messenger = set(inv["thus_says_the_lord_yhwh"]["verses_mt"])
    refrain_members = (set(inv["recognition_formula"]["verses_mt"]) | set(inv["recognition_formula_2ms"]["verses_mt"])
                       | fam["wide_64"] | fam["2mp_21"] | fam["adonai_5"] | fam["2fp_2"]
                       | set(inv["utterance_of_the_lord_yhwh"]["verses_mt"]) | set(inv["i_am_yhwh_spoken"]["verses_mt"]))
    final_pat = re.compile(r"(?:כי אני (?:אדני )?יהוה|נאם אדני יהוה|אני יהוה דברתי)" + TAIL_OK)

    def verse_final_close(key):
        return key in refrain_members and bool(final_pat.search(oshb.get(key, "")))

    rows = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    report = []
    for r in rows:
        m = re.match(r"Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)", r["span"])
        c1, v1, c2, v2 = map(int, m.groups())
        web = []
        cc, vv = c1, v1
        while (cc, vv) <= (c2, v2):
            web.append((cc, vv))
            cc, vv = (cc, vv + 1) if vv < LAST_VERSE[cc] else (cc + 1, 1)
        if len(web) <= 16 or r.get("unit_type") in EXCLUDED_TYPES:
            continue
        mt = ["Ezek.%d.%d" % web_to_mt(*w) for w in web]
        a_hits = [k for k in mt[1:] if k in messenger]
        b_hits, c_hits = [], []
        for i, k in enumerate(mt[:-1]):
            if not verse_final_close(k):
                continue
            nxt = mt[i + 1]
            head, tail = i + 1, len(mt) - (i + 1)
            c_hits.append({"close": k, "parts": [head, tail], "both_parts_ge_3": head >= 3 and tail >= 3})
            if nxt in messenger or nxt in fam["sub_onset_and_you_son_of_man_23"]:
                b_hits.append({"close": k, "next": nxt, "next_is": "messenger" if nxt in messenger else "sub_onset"})
        qualifies = bool(b_hits) or any(h["both_parts_ge_3"] for h in c_hits)
        # The rulings say no row beyond the ruled ones qualifies, so a qualifying row is a disagreement with the
        # controlling agent, routed to it; the author wave does not cut on the scan alone.
        status = ("ruled by the controlling agent" if r["span"] in RULED else
                  "QUALIFIES, contradicting the controlling agent's expectation - route to it, do not cut" if qualifies else
                  "holds under (b)/(c); (a) messenger formulae inside - author wave judges any addressee change" if a_hits else
                  "holds as expected" if r["span"] in EXPECTED_TO_HOLD else
                  "holds: cap disclosure at <= medium_low")
        report.append({"row": r["decision_id"], "span": r["span"], "verses": len(web), "unit_type": r.get("unit_type"),
                       "a_messenger_formulae_inside": a_hits, "b_close_then_onset": b_hits, "c_verse_final_closes": c_hits,
                       "qualifies_under_b_or_c": qualifies, "status": status})
    out = {"schema": "m8_cwo03_scan.v1", "cwo": "CWO-EZ-03", "book": "Ezek",
           "ordered_by": "ezek_controlling_rulings_a1#e2", "rows_file": {"path": a.rows, "sha256": hashlib.sha256(rows_p.read_bytes()).hexdigest()},
           "families_asserted": got, "rows_scanned": len(report), "rows": report,
           "limit": "a deterministic scan; test (a) reports messenger formulae but cannot judge an addressee change"}
    op = EZ / "repair" / "cwo03_scan_report.json"
    op.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({"rows_scanned": len(report), "families_asserted": got,
                      "by_status": {s: [x["span"] for x in report if x["status"] == s] for s in sorted({x["status"] for x in report})}},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
