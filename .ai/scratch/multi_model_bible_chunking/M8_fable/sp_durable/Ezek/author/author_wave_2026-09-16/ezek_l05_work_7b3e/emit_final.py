# -*- coding: utf-8 -*-
import json, hashlib, os
LANEP = r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
lane = json.load(open(LANEP, encoding='utf-8'))
ROWS = {r['decision_id']: r for r in lane['your_rows']}
dv = json.load(open('ezek_author_l05_deliverable.json', encoding='utf-8'))

# ---- last-gate re-validation of the file as it now stands on disk ----
gate = []
for e in dv['edits']:
    if e['expected_before'] != ROWS[e['row_id']][e['field']]:
        gate.append("expected_before drift at %s/%s" % (e['row_id'], e['field']))
ids = set(dv['items_discharged']) | set(x['item'] for x in dv['items_NOT_discharged'])
if len(ids) != 83 or set(dv['items_discharged']) & set(x['item'] for x in dv['items_NOT_discharged']):
    gate.append("item accounting broken")
for k in ("lane", "attempt_id", "execution_id", "sources", "edits", "items_discharged",
          "items_NOT_discharged", "escalations", "changes_made_or_no_change",
          "verification_evidence", "unresolved_uncertainty", "e19_selfreport", "limit"):
    if k not in dv:
        gate.append("missing required key: " + k)
for e in dv['edits']:
    if e['field'] in ("span", "osis_start", "osis_end", "decision_id",
                      "writer_attempt_id", "writer_decision_id", "writer_part", "model_id", "book"):
        gate.append("SEAM/IDENTITY FIELD TOUCHED: " + e['field'])
assert not gate, gate


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


dsha = sha('ezek_author_l05_deliverable.json')
fm = dict(dv)
fm["output_files"] = {
    "work_directory": r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l05_work_7b3e",
    "ezek_author_l05_deliverable.json": {"sha256": dsha, "bytes": os.path.getsize('ezek_author_l05_deliverable.json')},
    "ezek_author_l05_final_message.json": {
        "sha256": "reported in the returned message, not embeddable here: a file cannot contain its own digest",
        "note": "this file is the deliverable plus this output_files block; its digest is taken after this write and is reported in the lane's returned JSON"
    },
    "final_gate": "re-validated against the lane file at this write: 63/63 expected_before byte-exact, 83/83 items accounted in exactly one list, 0 seam or writer-identity fields touched"
}
json.dump(fm, open('ezek_author_l05_final_message.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
fsha = sha('ezek_author_l05_final_message.json')
print("DELIVERABLE sha256 :", dsha)
print("DELIVERABLE bytes  :", os.path.getsize('ezek_author_l05_deliverable.json'))
print("FINAL_MESSAGE sha256:", fsha)
print("FINAL_MESSAGE bytes :", os.path.getsize('ezek_author_l05_final_message.json'))
json.dump({"deliverable_sha256": dsha, "final_message_sha256": fsha},
          open('DIGESTS.json', 'w', encoding='utf-8'), indent=1)
