# -*- coding: utf-8 -*-
import json, re, hashlib, collections
LANE = r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
lane = json.load(open(LANE, encoding='utf-8'))
ROWS = {r['decision_id']: r for r in lane['your_rows']}
ITEMS = lane['your_worklist_items']
A = json.load(open('edits_part_a.json', encoding='utf-8'))
B = json.load(open('edits_part_b.json', encoding='utf-8'))
EDITS = A['edits'] + B['edits']
FAIL = []
assert not A['problems'] and not B['problems'], (A['problems'], B['problems'])

# ---- check 1: expected_before is byte-exact against the lane file ----
for e in EDITS:
    cur = ROWS[e['row_id']][e['field']]
    if e['expected_before'] != cur:
        FAIL.append("expected_before mismatch at %s/%s" % (e['row_id'], e['field']))

# ---- check 2: one edit per (row, field), except append_ref which may repeat ----
bykey = collections.defaultdict(list)
for e in EDITS:
    bykey[(e['row_id'], e['field'])].append(e)
for k, v in bykey.items():
    ops = set(x['op'] for x in v)
    if len(v) > 1:
        if ops != {'append_ref'}:
            FAIL.append("multiple non-append edits on %s: ops=%s n=%d" % (k, ops, len(v)))
        else:
            eb = set(json.dumps(x['expected_before'], ensure_ascii=False) for x in v)
            if len(eb) != 1:
                FAIL.append("append_ref group on %s has differing expected_before" % (k,))

# ---- check 3: every worklist item is in exactly one of the two lists ----
NOT_DISCHARGED = [
 ("l05_i13", "EXEMPT_A6B + ALREADY_COMPLIANT", "P08-001",
  "No edit owed, and none made. The field already carries the convention for the quoted material: " + "\u201c" + "the children of your people" + "\u201d" + " (web:Ezek.33.2). The 6-word sweep run is that 5-word delimited quotation plus the row's own preceding 'to'. Independently, A6-b exempts it: brief section 3 names 'children of your people' as an addressee title, and the sentence names it as the addressee the unit returns to. MEASURED: the run occurs at web:Ezek.3.11 and web:Ezek.33.2, the in-span one being 33:2."),
 ("l05_i19", "EXEMPT_A6B", "P08-004",
  "A6-b exemption taken. The run is the WEB's fixed rendering of the recognition formula, a counted device, and the row names it ('the recognition formula at Ezek.33.29'). MEASURED: 22 occurrences in WEB Ezekiel, the in-span one being web:Ezek.33.29, which is exactly the verse the row names. No delimiter or reference is owed on a gloss of a census object."),
 ("l05_i23", "EXEMPT_A6B", "P08-005",
  "A6-b exemption taken. The row names the device twice and uses the gloss precisely to say the close does NOT match it ('does not match the standard <gloss> formula bytes', 'so as not to inflate any of the book's recognition-formula counts'). MEASURED: 57 occurrences in WEB Ezekiel and ZERO inside this row's span 33:30-33, so there is no in-span verse an in-field reference could point at; installing one would have asserted a quotation that is not there."),
 ("l05_i28", "EXEMPT_A6B", "P08-007",
  "A6-b exemption taken. The recognition formula is a counted device and the row names it at the point of use ('a 2ms recognition-formula variant'). MEASURED: 17 occurrences in WEB Ezekiel, two of them in span at web:Ezek.35.4 and web:Ezek.35.9. FINDING recorded rather than acted on: the row's SECOND use of this gloss sits at 35:12, and WEB 35:12 renders that verse differently ('You will know that I, Yahweh, have heard all your insults'), so the gloss there is the formula's standard rendering and not a quotation of 35:12 - legitimate under A6-b, but noted for the spot wave."),
 ("l05_i29", "EXEMPT_A6B", "P08-007",
  "A6-b exemption taken, same ground as l05_i28. This is the second of two identical items on the same run in the same field; the two correspond to the two occurrences of the gloss in the field (at 35:4 and at 35:12), and neither owes the convention."),
 ("l05_i33", "NOT_PRESENT_IN_ANY_FIELD", "P08-007",
  "Cannot be executed as written, and this is a finding, not an omission. The peer's hand-named run does NOT occur in any field of this row: MEASURED absent from boundary_rationale, strongest_rejected_alternative, device_notes, and every entry of boundary_evidence_refs. A6's duty attaches to a run that a field publishes, and there is nothing here to delimit. What I DID find: the run occurs exactly once in WEB Ezekiel, at web:Ezek.35.12, in span, inside the clause 'I, Yahweh, have heard all your insults'; the row quotes only the three words 'I have heard' out of that clause. If the controlling agent wants the longer clause published at this row, that is a new order rather than this one."),
 ("l05_i34", "EXEMPT_A6B + ALREADY_COMPLIANT", "P08-010",
  "No edit owed on this field, and none made. boundary_rationale already carries " + "\u201c" + "the mountains of Israel," + "\u201d" + " (web:Ezek.36.1); the 5-word run is that delimited quotation with the row's own 'to' in front of it. MEASURED: the run occurs once in WEB Ezekiel, at web:Ezek.36.1, in span. The companion item on the refs field, l05_i35, IS discharged with an edit."),
 ("l05_i41", "EXEMPT_A6B", "P08-012",
  "A6-b exemption taken, on two independent grounds. First, the run is the WEB's fixed rendering of the recognition family and the row names the device ('matching the recognition-family <gloss> pattern'). Second, MEASURED: in the field the words are NOT contiguous - the row writes 'know ... that I am Yahweh' with an ellipsis, so the 5-word run only exists after punctuation is stripped. There is no contiguous run in the field to delimit."),
 ("l05_i49", "ALREADY_COMPLIANT", "P08-013",
  "No edit owed, and none made. The peer's union run sits inside an already-compliant quotation in boundary_rationale: " + "\u201c" + "You will be my people, and I will be your God." + "\u201d" + " (web:Ezek.36.28) - double curly quotes plus the in-field web reference. MEASURED: the run occurs once in WEB Ezekiel, at web:Ezek.36.28, in span. The orchestrator's disclosure stands, that whether the peer named it AS an A6 run is an inference from its presence in the packet."),
 ("l05_i52", "EXEMPT_A6B", "P09-001",
  "A6-b exemption taken. The run is a rendering of a counted device and the row names it and its census ('the second-person plural recognition variant ..., part of a 21-verse 2mp family sweep'). VERIFIED against the governing input: ezek_device_inventory.v2.json, formulae.recognition_formula_2mp.verses_mt, is a 21-member list and Ezek.37.14 IS a member, so the row's sweep claim is supported by v2, which C2-amended makes authoritative for counts and list membership. MEASURED: the 7-word run occurs once in WEB Ezekiel, at web:Ezek.6.7, out of span; WEB 37:14 renders its own clause 'and you will know that I, Yahweh, have spoken it', so the parenthetical is a formula gloss and not a quotation of 37:14 - which is what A6-b licenses."),
 ("l05_i67", "ALREADY_COMPLIANT", "P09-008",
  "No edit owed, and none made. boundary_rationale already carries " + "\u201c" + "It will happen in that day" + "\u201d" + " (web:Ezek.39.11), the full convention. MEASURED: the run occurs at web:Ezek.38.10, web:Ezek.38.18 and web:Ezek.39.11, and the row already names all three of those locations."),
 ("l05_i71", "EXEMPT_A6B + ALREADY_COMPLIANT", "P09-010",
  "No edit owed, and none made. The field already carries " + "\u201c" + "the house of Israel" + "\u201d" + " (web:Ezek.39.22); the 5-word run is that delimited quotation plus the row's own 'to'. Independently, A6-b exempts it: 'house of Israel' is named in brief section 3 as an addressee title and the sentence names it as the recognition close's addressee. MEASURED: 16 occurrences in WEB Ezekiel and ZERO in this row's span, so the AUTHOR_JUDGEMENT on coincidence is answered - it is an addressee title, not a borrowed collocation."),
 ("l05_i74", "EXEMPT_A6B", "P09-010",
  "A6-b exemption taken. The run occurs undelimited inside refs entry 1, which itself names the device ('wide-family recognition close addressed to the house of Israel'), and 'house of Israel' is an A6-b addressee title. MEASURED: zero occurrences in span, so no in-field reference to an in-span verse exists; the entry already carries its own coordinate, oshb:Ezek.39.22."),
]
discharged = []
for e in EDITS:
    for i in e['worklist_item_ids']:
        if i not in discharged:
            discharged.append(i)
nd = [x[0] for x in NOT_DISCHARGED]
allids = ["l05_i%02d" % i for i in range(len(ITEMS))]
both = set(discharged) & set(nd)
missing = [i for i in allids if i not in discharged and i not in nd]
extra = [i for i in discharged + nd if i not in allids]
if both:
    FAIL.append("item in BOTH lists: %s" % sorted(both))
if missing:
    FAIL.append("SILENT DROP - item in neither list: %s" % missing)
if extra:
    FAIL.append("unknown item id: %s" % extra)

# ---- check 4: 7-gram duplication among my own new prose values ----
def toks(s):
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()
grams = collections.defaultdict(list)
for e in EDITS:
    if e['op'] != 'set':
        continue
    vals = e['value'] if isinstance(e['value'], list) else [e['value']]
    for v in vals:
        w = toks(v)
        for i in range(len(w) - 6):
            grams[" ".join(w[i:i + 7])].append(e['row_id'] + "/" + e['field'])
dups = {g: sorted(set(rs)) for g, rs in grams.items() if len(set(rs)) > 1}
# a 7-gram shared between two fields is only a concern if it is text I wrote;
# report all, then filter by whether it also appears in the pre-edit bytes.
pre = collections.defaultdict(set)
for rid, r in ROWS.items():
    for f in ('boundary_rationale', 'strongest_rejected_alternative', 'device_notes'):
        w = toks(r[f])
        for i in range(len(w) - 6):
            pre[" ".join(w[i:i + 7])].add(rid + "/" + f)
    for ent in r['boundary_evidence_refs']:
        w = toks(ent)
        for i in range(len(w) - 6):
            pre[" ".join(w[i:i + 7])].add(rid + "/boundary_evidence_refs")
new_dups = {g: rs for g, rs in dups.items() if g not in pre or len(pre[g]) < 2}

report = {
 "edit_count": len(EDITS),
 "rows_touched": sorted(set(e['row_id'] for e in EDITS)),
 "fields_touched": sorted(set(e['row_id'] + "/" + e['field'] for e in EDITS)),
 "items_discharged_n": len(discharged),
 "items_not_discharged_n": len(nd),
 "total_accounted": len(discharged) + len(nd),
 "item_total": len(ITEMS),
 "new_7gram_duplicates_introduced": new_dups,
 "preexisting_7gram_duplicates_left_alone": {g: rs for g, rs in dups.items() if g not in new_dups},
 "FAIL": FAIL,
}
json.dump(report, open('assemble_report.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump({"edits": EDITS, "discharged": discharged, "not_discharged": NOT_DISCHARGED},
          open('edits_all.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in report.items() if k != 'fields_touched'}, ensure_ascii=False, indent=1))
