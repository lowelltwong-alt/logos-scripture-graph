"""Post-FIXUP-3 CWO coverage report: every hit of the sweep on the applied rows, hand-classed.
usage: make_post3_report.py SWEEP_FX3.json SWEEP_FX2.json ROW_OUT.json"""
import hashlib, json, sys, datetime
from pathlib import Path
SP = Path(__file__).resolve().parents[3]
R = SP / "1Cor/review"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
sw, swb, row_out = [json.load(open(x, encoding="utf-8")) if i < 2 else x for i, x in enumerate(sys.argv[1:4])]
ROWS = SP / "1Cor/fixup/draft_rows_fixup3_applied.jsonl"
SCRIPT = R / "cwo_sweep_1cor.py"
OUT = R / "cwo_1cor_post_fixup3_report.v1.json"
S3 = R / "1cor_fixup2_review_S3.json"
MAP = {"disclosure_only": "compliant", "location_only": "compliant_location", "informs_compliant": "compliant", "support_use": "false_positive"}
C05 = {("W1-005", None, "Robinson"): "location", ("W1-010", None, "The step begins"): "location", ("W1-010", None, "at 3:16"): "false_positive",
       ("W1-011", None, "An RP pilcrow"): "location", ("W1-013", None, "At 4:6"): "false_positive", ("W3-006", None, "The row closes"): "false_positive",
       ("W3-008", None, "Across the seam"): "false_positive", ("W4-001", 0, "rp:1Cor.11.2"): "false_positive", ("W6-001", 5, "rp:1Cor.15.12"): "false_positive",
       ("W6-009", 6, "rp:1Cor.16.13"): "false_positive", ("W6-010", 4, "rp:1Cor.16.15"): "false_positive"}
C06 = {("W2-008", "1Cor.7.9"): "false_positive", ("W6-004", "1Cor.15.35"): "false_positive"}
k = lambda x: (x["row"], x["field"], x.get("index"), x.get("text"))
old04 = {k(x) for x in swb["CWO04"]["list"]}
l04 = []
for x in sw["CWO04"]["list"]:
    y = dict(x, **{"class": MAP[x["auto_class"]], "bytes_since_S3": "unchanged" if k(x) in old04 else "new"})
    if k(x) not in old04 and x["row"] != "W6-006":
        raise SystemExit("REFUSED: unread new CWO-04 hit " + x["row"])
    if x["auto_class"] == "support_use":
        if x["row"] != "W6-013" or k(x) not in old04:
            raise SystemExit("REFUSED: open support_use " + x["row"])
        y["basis"] = "The PD2 word 'marks' has a quotation of 16:21 as subject; the pilcrow is placed at 16:21 in the same unit, because the SPLIT does not break after a closing quotation mark. Unit byte-identical to the one S3 classed, so S3-05's false positive stands."
    if x["row"] == "W6-006" and k(x) not in old04:
        y["basis"] = "New unit from R4 wording: the mark is placed at 15:50 and 'decides nothing' is the disclosure."
    l04.append(y)
l05 = []
for x in sw["CWO05"]["list"]:
    c = [v for (r, i, s), v in C05.items() if r == x["row"] and i == x.get("index") and x["text"].startswith(s)]
    if len(c) != 1:
        raise SystemExit("REFUSED: unclassed CWO-05 hit " + x["row"])
    y = dict(x, **{"class": c[0]})
    if x["row"] == "W1-011":
        y["basis"] = "Re-classed on the new bytes as GATE-E4 condition 7 orders: 'stands' places each mark at a verse; 'opening' qualifies a verse; 'begins' has a prohibition as subject. No mark is subject or agent of a PD3 verb."
    l05.append(y)
l06 = []
for x in sw["CWO06"]["list"]:
    l06.append(dict(x, **{"class": C06[(x["row"], x["verse"])]}))
if [x for x in l05 if x["class"] == "true"] or sw["CWO07"]["unlisted"] or sw["CWO02"]["fail"] or sw["A"]["hits"]:
    raise SystemExit("REFUSED: open hit")
b_same = sorted(json.dumps(x, sort_keys=True) for x in sw["B"]["list"]) == sorted(json.dumps(x, sort_keys=True) for x in swb["B"]["list"])
from collections import Counter
hc = {"CWO04": dict(Counter(x["class"] for x in l04)), "CWO05": dict(Counter(x["class"] for x in l05)), "CWO06": dict(Counter(x["class"] for x in l06))}
rep = {"schema": "m8_cwo_coverage_report.v1", "book": "1Cor",
       "rows_file": {"path": "sp_durable/1Cor/fixup/draft_rows_fixup3_applied.jsonl", "sha256": sha(ROWS)},
       "sweep_script": {"path": "sp_durable/1Cor/review/cwo_sweep_1cor.py", "sha256": sha(SCRIPT)},
       "rulings_file": {"path": "sp_durable/1Cor/review/1cor_controlling_agent_rulings_E4.v1.json", "sha256": sha(R / "1cor_controlling_agent_rulings_E4.v1.json")},
       "S3_classes": {"path": "sp_durable/1Cor/review/1cor_fixup2_review_S3.json", "field": "cwo.CWO-1COR-04.my_classes", "sha256": sha(S3)},
       "A": {"hits": sw["A"]["hits"]}, "B": {"hits": sw["B"]["hits"], "list": sw["B"]["list"], "identical_to_FIXUP2_hits": b_same},
       "CWO02": sw["CWO02"], "CWO04": {"hits": len(l04), "by_class": sw["CWO04"]["by_class"], "list": l04},
       "CWO05": {"hits": len(l05), "list": l05}, "CWO06": {"hits": len(l06), "list": l06}, "CWO07": {k2: v for k2, v in sw["CWO07"].items()},
       "hand_classes": hc,
       "note": "Hand classes are the orchestrator's on the applied bytes: 48 CWO-1COR-04 units and 10 CWO-1COR-05 units are byte-identical to units already classed, and carry those classes; W6-006 (CWO-04) and W1-011 (CWO-05) are new units read here. These are unreviewed until S5 re-derives them. W3-006's class is carried as recorded although the remedy's location wording may fit it better; neither class is true, so no order follows."}
OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
row = {"schema": "m8_attempt_receipt.v1", "book": "1Cor", "parent_agent_id": "orchestrator", "record_kind": "cwo_coverage_report",
       "ordered_by": "cor_controlling_rulings_r4_a1#e1 GATE-E4 s2_conditions 5 to 8",
       "report": {"path": "sp_durable/1Cor/review/cwo_1cor_post_fixup3_report.v1.json", "sha256": sha(OUT)},
       "sweep_script": rep["sweep_script"], "rows_file": rep["rows_file"],
       "summary": {"A": sw["A"]["hits"], "B": sw["B"]["hits"], "cwo02_fail": sw["CWO02"]["fail"], "cwo04": sw["CWO04"]["by_class"], "cwo04_open": 0,
                   "cwo05_hits": len(l05), "cwo05": hc["CWO05"], "cwo06_hits": len(l06), "cwo06": hc["CWO06"], "cwo07_unlisted": sw["CWO07"]["unlisted"]},
       "outcome": "Every hit on the FIXUP-3 applied rows classed; 0 open true, 0 open support_use, 0 count_excess, 0 unlisted verses.",
       "effect": "None on the gate: S5 tests the conditions.",
       "recorded_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
Path(row_out).write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"report": sha(OUT), "hc": hc, "b_same": b_same, "cwo07": sw["CWO07"]["unlisted"]}))
