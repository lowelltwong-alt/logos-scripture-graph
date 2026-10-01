#!/usr/bin/env python3
"""#e17 tool order T-2: re-run #e16 O-64's six named WEB quotations against the fixture #e17 K5 fixed - verse_map_web.json
'text' with '[fn]' removed - BYTE for byte (no quote or case folding), and plan only the differences that survive.

Report, as the order asks, which field the member read before this order: check_web_quotes.py reads 'text' through
ezek_lib.norm_english, which already removes '[fn]' and FOLDS typographic quotes, apostrophes and dashes to ASCII (case is
kept). The member therefore cannot see an apostrophe difference; this re-run can. The member is unchanged by this order.

usage: python t2_quote_rerun.py   (writes t2/proposal.json and t2/report.json; applied by apply_proposal.py)
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
WEB = EZ / "tools" / "verse_map_web.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
web = json.loads(WEB.read_text(encoding="utf-8"))
rows = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
# (row, verse, field, element index or None, quoted run as written, the WEB bytes it must equal)
SITES = [("P01-013", "Ezek.7.4", "My eye will not spare"), ("P06-001", "Ezek.25.1", "Yahweh’s word came to me, saying,"),
         ("P10-005", "Ezek.40.47", "The altar was before the house"),
         ("P10-008", "Ezek.41.12", "The building that was before the separate place at the side toward the west"),
         ("P10-014", "Ezek.43.13", "These are the measurements of the altar"), ("P11-013", "Ezek.48.30", "These are the exits of the city")]
report, proposal = [], {}
for rid, ref, want in SITES:
    text = web[ref]["text"].replace("[fn]", "")
    fixture_ok = want in text
    r = rows[rid]
    found = []
    for f in ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "boundary_evidence_refs"):
        vals = r[f] if isinstance(r[f], list) else [r[f] or ""]
        for i, s in enumerate(vals):
            low = s.lower()
            k = low.find(want.lower()[:18].replace("’", "'")) if "’" not in s else low.find(want.lower()[:18])
            start = 0
            while True:
                j = low.find(want.lower()[:18], start)
                if j < 0:
                    break
                written = s[j:j + len(want)]
                found.append({"field": f, "index": i if isinstance(r[f], list) else None, "written": written,
                              "byte_equal_to_web": written == want or text.find(written) >= 0})
                start = j + 1
    report.append({"row": rid, "ref": ref, "web_run_in_fixture": fixture_ok, "occurrences": found})
# the four-word header quote on P10-014's refs is shorter than the run above; it is checked on its own
p = rows["P10-014"]["boundary_evidence_refs"]
hdr = [i for i, e in enumerate(p) if '"these are the measurements"' in e]
t43 = web["Ezek.43.13"]["text"].replace("[fn]", "")
if len(hdr) == 1 and "These are the measurements" in t43 and "these are the measurements" not in t43:
    new = list(p)
    new[hdr[0]] = new[hdr[0]].replace('"these are the measurements"', '"These are the measurements"')
    proposal["P10-014"] = {"boundary_evidence_refs": new}
    report.append({"row": "P10-014", "ref": "Ezek.43.13", "surviving_difference": "case: 'these' where the WEB bytes read 'These'",
                   "entry_index": hdr[0], "planned": True})
out = HERE / "t2"
out.mkdir(exist_ok=True)
(out / "proposal.json").write_text(json.dumps(proposal, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
(out / "report.json").write_text(json.dumps({"order": "#e17 T-2", "rows_sha256": sha(ROWS), "web_sha256": sha(WEB),
                                             "member_read_before": "'text' via ezek_lib.norm_english ([fn] removed; quotes, apostrophes and dashes folded; case kept)",
                                             "sites": report}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"planned_rows": sorted(proposal), "proposal_sha256": sha(out / "proposal.json"),
                  "sites_not_byte_equal": [(x["row"], o["field"], o["written"]) for x in report for o in x.get("occurrences", []) if not o["byte_equal_to_web"]]},
                 ensure_ascii=False, indent=1))
