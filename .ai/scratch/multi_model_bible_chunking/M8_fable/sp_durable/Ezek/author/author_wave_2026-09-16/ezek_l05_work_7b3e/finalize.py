# -*- coding: utf-8 -*-
import json, collections, hashlib
WORK = r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l05_work_7b3e"
B = r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek"
LANEP = r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
d = json.load(open('edits_all.json', encoding='utf-8'))
rep = json.load(open('assemble_report.json', encoding='utf-8'))
EDITS = d['edits']

# rotation-rule accounting over EVERY entry I install, including the ones that
# ride inside a combined 'set' of a refs list (otherwise the tally undercounts).
import re as _re
TOKENS = ("WARRANT-onset", "WARRANT-close", "WARRANT-rival", "WARRANT-absence-over-range",
          "DISCLOSURE-kq", "DISCLOSURE-mark", "DISCLOSURE-paseq", "DISCLOSURE-note",
          "DISCLOSURE-device", "QUOTE", "ANCHOR")
rot = collections.defaultdict(list)
installed = []
for e in EDITS:
    cands = []
    if e['op'] == 'append_ref':
        cands = [e['value']]
    elif e['op'] == 'set' and e['field'] == 'boundary_evidence_refs':
        cands = [x for x in e['value'] if _re.search(r"\[(%s)\] " % "|".join(TOKENS), x)]
    for v in cands:
        m = _re.search(r"\[(%s)\] (.*)$" % "|".join(TOKENS), v)
        assert m, v
        rot[m.group(1)].append(m.group(2))
        installed.append(v)
rotation = {k: {"instances": len(v), "distinct_formulations": len(set(v)),
                "max_words": max(len(x.split()) for x in v), "formulations": sorted(set(v))}
            for k, v in sorted(rot.items())}
rotation["_total_entries_installed_with_a_role_token"] = len(installed)
assert len(installed) == 38, len(installed)
for v in installed:
    tail = _re.search(r"\] (.*)$", v).group(1)
    assert len(tail.split()) <= 6, v

SOURCES = [
 {"path": B + r"\AUTHOR_WAVE_BRIEF.v1.md",
  "sha256": "ccb7026f908345d3f9800671e621cd8fbdedc3429d41c22dc244b03e0474bd79",
  "read": "in full, before writing anything; digest verified against the launch table"},
 {"path": LANEP,
  "sha256": "3d4badba3a319e481903daad25f2aab713b00e11102f664a53547f6424a58e05",
  "read": "in full: all 24 rows (every prose field, refs list, confidence, unit_type, signals) and all 83 worklist items, read through structured extracts of the file rather than by eye"},
 {"path": B + r"\Ezek_oshb.txt",
  "sha256": "337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e",
  "read": "1273 verses parsed; measured the accent structure of 33:20, 33:29, 36:23, 36:32, 36:38 and 32:32, the 33:17 vs 33:20 word-level overlap, the 33:10/33:12 addressee pair, 33:11's utterance-formula position, and the vayyamod run over 40:5-41:5"},
 {"path": B + r"\pmarks_Ezek.json",
  "sha256": "25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315",
  "read": "marks for every verse I cite a mark at; kq at 31:5, 32:31, 32:32, 33:13, 33:16, 33:20, 35:9, 35:12, 36:13, 36:14, 36:15, 37:16, 37:19, 37:22, 39:25; paseq at 33:11, 39:17, 40:1; arithmetic_anomalies_resolved in full. A kq entry is a LIST of K-Q pair strings, one or two members, which is how I read it"},
 {"path": B + r"\tools\verse_map_web.json",
  "sha256": "bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98",
  "read": "all 1273 clean texts loaded; every A6 run located by exact token match book-wide; the mt back-reference of all 60 verses I cite checked for face identity"},
 {"path": B + r"\ezek_device_inventory.v2.json",
  "sha256": "356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f",
  "read": "formulae.recognition_formula_2mp.verses_mt, to test P09-001's 21-verse claim; top-level key list. v2 read, not v1"},
 {"path": B + r"\web_mt_offset_map.json",
  "sha256": "b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887",
  "read": "in full (DIGEST MEASURED HERE, the launch table said 'measure and report'): identity outside the zone, the five zone pairs, totals 1273/1273, verdict GREEN"},
 {"path": B + r"\verse_inventory.json",
  "sha256": "7314690191ec380b25578ca33d4745f4e60196b9f0e1dda4a1bcc9286c19cf54",
  "read": "digest verified only; numbering_face WEB is taken from the brief, not re-derived"},
 {"path": B + r"\book_strategy_Ezek.md",
  "sha256": "4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3",
  "read": "digest verified; NOT opened. Every rule I applied (CUT-RULE, CONF-CAL, the over-split guard, A6-b, MARKS-3D, D11) is quoted in the brief, which governs; I did not need the strategy text and did not read it"},
 {"path": B + r"\ezek_device_inventory.json",
  "sha256": "0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142",
  "read": "digest verified; NOT opened. It is SUPERSEDED for counts and no figure in my output comes from it"},
 {"path": B + r"\tools\verse_map_oshb.json",
  "sha256": "408b7ee74564aef902c5fc539d6577f7708fa9aa839c993ce6281d86dc3a7901",
  "read": "digest verified; NOT opened. No citation of mine falls in the ch 20/21 zone, so no MT-keyed crosswalk lookup was needed"},
]

ESC = [
 {"id": "ESC-1", "row": "P08-007",
  "what": "Two measurably FALSE separator claims stand in this row's boundary_rationale, in the same defect class that the P08-011 boss work order corrects. The row says of the 35:9 note and again of the 35:12 note that it is 'split from the K/Q note layer with its separators stripped'. MEASURED from pmarks_Ezek.json kq: the entry at Ezek.35.9 is a one-member list whose member carries ZERO '/' morpheme separators, and the entry at Ezek.35.12 likewise carries ZERO. Nothing was stripped from either, because neither note has any separator in the layer.",
  "why_i_did_not_write_it": "No worklist item of mine orders it, and rewriting a row's prose outside my orders is how lanes diverge. I edited this same field for l05_i27 and l05_i30 and deliberately left the adjacent separator clause untouched. PROPOSED CORRECTION, for the controlling agent to order in one step: replace 'split from the K/Q note layer with its separators stripped' at each of the two places with 'rendered as the read form from the K/Q note layer, which carries no morpheme separator at this verse'. The same wording would also be worth checking at every other row that carries the phrase."},
 {"id": "ESC-2", "row": "P08-002",
  "what": "A direct conflict between two of my controlling instructions about MT 33:20's sof pasuq. Brief section 12 says it 'is UNAVAILABLE at verse granularity and no row is scored on it. Do not resolve it, do not assert it either way.' My BOSS_RETURN item l05_i15 orders the opposite handling: strike the sof-pasuq tier cure, because 'the row's claim is MEASURED via pmarks arithmetic_anomalies_resolved and may cite it'. WHAT I FOUND, independently of the boss's C1: pmarks_Ezek.json arithmetic_anomalies_resolved.sof_pasuq_1272_for_1273_verses has keys verse/finding/status, its verse value is exactly 'Ezek.33.20', its finding states the verse carries no x-sof-pasuq seg and that the OSHB editors wrote an untyped note in its place, and its status calls this 'a real source fact, not a parsing gap'. The fact is therefore MEASURABLE at verse granularity, and section 12's sentence does not reproduce against the pinned input.",
  "why_i_did_not_write_it": "I DID write the item's order, because it is the later, row-specific ruling, it arrives with a C1 reproduction, and it is the one that agrees with the pinned bytes; per the brief's own closing rule, if a figure or gloss disagrees with the pinned input, the input wins and I say so. What I did NOT do is resolve the sof pasuq either way: my edit only records what the pinned input says about its absence, which is what the row already said, and cites the key. Section 12's sentence should be corrected or the conflict ruled, because the next author agent will hit it too."},
 {"id": "ESC-3", "row": "P08-014 (and bearing on P08-013)",
  "what": "A seam-licensing question I will not touch. MEASURED from Ezek_oshb.txt: at MT 36:32 the utterance formula stands at words 5-7 of a 14-word verse, an INDEPENDENT clause (yivvada lakhem) follows it before the etnachta, and independent imperatives (boshu ve-hikkalmu) fill the b-half. Under the #e14 Q2 refinement that is the WEAK mid-verse shape, not a verse-final close. P08-014's onset is argued from that close, and its own onset device is a messenger formula at 36:33 with no addressee change from 36:32 (both address the 2mp 'you'/house of Israel), so on my reading neither CUT-RULE limb (a) nor limb (b) is satisfied at that seam.",
  "why_i_did_not_write_it": "This is a seam and a confidence question, and I do not move a seam or raise or lower a grade unasked. I wrote the ordered A4 install at 36:32 with WARRANT-onset, because the token records where the ROW's rationale rests, and pointed the edit's 'why' at this escalation. P08-014 has no CONFIDENCE item in my lane, so its medium stands untouched."},
 {"id": "ESC-4", "row": "P08-002",
  "what": "A confidence implication I did not act on. After the ordered correction, this row's rejected-alternative weighs a rival onset that CUT-RULE limb (a) DOES license (the 33:12 addressee change, MEASURED) and holds against it on a stated ground (the over-split guard). CONF-CAL's second limb makes 'a two-faced rival held on stated grounds' MEDIUM. The row stands at medium_low and no CONFIDENCE item in my lane touches it.",
  "why_i_did_not_write_it": "CONF-CAL is explicit that no row's confidence is raised unasked, and confidence is a grade ruled for me, not chosen by me. Raised so the controlling agent can decide whether the corrected weighing now carries the row to MEDIUM."},
 {"id": "ESC-5", "row": "P08-013, P09-002, P10-001",
  "what": "A sweep-pooling exception in three edits. On each of these three fields an A6 item and an A4 item (or an A6 item and a grounds item) both land, and the one-edit-per-(row, field) rule leaves no way to split them: a later 'set' cannot be split out from an earlier append_ref, because after the a4 sweep lands the list no longer matches the 'set' expected_before and the harness refuses the whole a6 batch. So each is emitted as ONE edit carrying both items, with a sweep_pooling_note naming the borrowed item.",
  "why_i_did_not_write_it": "I did write them, as single combined edits; what I am escalating is the sweep-parity accounting. Under E-18 the a6 sweep's ordered count will include l05_i47, l05_i60 and l05_i80, which have no a6-labelled edit of their own. If the orchestrator would rather have the A6 halves dropped and re-ordered as their own sweep, each is a self-contained substring change and is trivially separable at its end."},
 {"id": "ESC-6", "row": "P09-002",
  "what": "A residual incompleteness left inside the boss work order's scope boundary. The FALSE statement about 37:16 ('both the same word ... read <first form>') lived in device_notes and is corrected. Refs entry index 2 still reads 'ketiv <K> / qere <first form> and a second instance in the same verse', which is literally true but silent about the second note's differing pointing.",
  "why_i_did_not_write_it": "The order names 'the 37:16 disclosure', which is the device_notes sentence, and editing the refs entry too would have created a fourth combined-sweep edit on a field that already takes the l05_i61 A4 append. This row is in the spot wave's FULL-COVERAGE set under C3 regardless, so flagging is the cheaper route than a sweep exception."},
]

VER = [
 "All 11 pinned-input digests verified BEFORE reading. Nine matched the launch table exactly; web_mt_offset_map.json had no pinned value and I measured it as b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887 (2368 bytes).",
 "C1 REPRODUCTION 1 of 3 (P08-002): pmarks_Ezek.json arithmetic_anomalies_resolved.sof_pasuq_1272_for_1273_verses exists with sibling keys finding/status/verse and verse == 'Ezek.33.20'. REPRODUCES. I also checked kq['Ezek.33.20'] and found the key ABSENT, which is the correct expectation for a verse that is not a K/Q site, not a defect.",
 "C1 REPRODUCTION 2 of 3 (P08-011): '/' separator counts per kq member measure Ezek.36.13 = [0, 2] and Ezek.36.14 = [4, 0]. REPRODUCES the boss's expected figures exactly. Consequence I checked myself: 'separators stripped' is true only of the second 36:13 note and the first 36:14 note, which is what the order says.",
 "C1 REPRODUCTION 3 of 3 (P09-002): kq['Ezek.37.16'] has 2 members; a codepoint diff finds member 0 carrying U+0591 HEBREW ACCENT ETNAHTA absent from member 1, and member 1 carrying U+05BD HEBREW POINT METEG absent from member 0, and nothing else differing. REPRODUCES the expected 'exactly U+0591 against U+05BD'.",
 "WORDING order, byte basis MEASURED: at Ezek.36.23 the etnachta falls on the 9th word (be-tokham); the b-half runs knowing-clause, then utterance formula, then a three-word preposition-plus-infinitive-construct tail to the final word, which carries U+05BD. So the remainder after the formula tokens is a DEPENDENT completion and #e14 Q2 grades it an ordinary licensed close. The contrast case checks too: at Ezek.29.9 the recognition formula ends at the etnachta and an independent causal clause (ya'an amar ...) fills the b-half, which is the weak shape.",
 "VERBATIM SCOPE (P08-002) MEASURED: the longest identical contiguous pointed-word run between MT 33:17 and MT 33:20 is 4 words, the complaint lo yittakhen derekh adonai, byte-identical. None of the four tokens of the verdict clause (ish ki-drakhav eshpot etkhem) occurs anywhere in 33:17. The row's unscoped 'verbatim' was therefore true of the complaint and false of the verdict.",
 "CUT-RULE limb test (P08-002) MEASURED: 33:10 addresses beit yisra'el, 33:12 addresses benei ammekha - an addressee change, so limb (a) licenses the 33:12 ve'attah. At 33:11 the utterance formula stands at word 4 of 25 with independent imperatives after it, so limb (b) is NOT met there; and a mark alone never satisfies limb (b), however strong the pe on 33:11 looks.",
 "CUT-RULE limb test (P08-005) MEASURED: 33:29's recognition formula ends at the etnachta and the b-half is a dependent temporal infinitive, so it is verse-final in effect under #e14 Q2 and limb (b) licenses the 33:30 ve'attah. That is the ground for the WARRANT-onset token on the 33:29 entry.",
 "MARKS-3D, verified by me against pmarks and NOT from any primary packet: PE on 30.19, 32.16, 32.32, 33.11, 33.20, 33.22, 37.14, 39.29; SAMEKH on 30.21, 30.26, 31.18, 33.9, 33.24, 33.26, 33.29, 36.12, 36.15, 36.21, 36.32, 36.38, 37.10, 37.12, 37.28, 39.16; and NO mark on 30.20, 30.25, 31.1, 32.1, 32.17, 33.7, 33.23, 33.28, 34.1, 37.1-37.9, 37.11, 37.13, 38.3, 39.11, 39.12, 39.14, 39.17, 40.1-40.6. Every mark claim I tokened DISCLOSURE-mark reproduces; no row claim of mine failed.",
 "P09-001's rejected-alternative claim that 37.10 and 37.12 both carry a samekh REPRODUCES (both are SAMEKH). That is what makes the rival mark-only and, under CONF-CAL, weighable but never fatal.",
 "P09-002's claim 'no samekh or pe mark falls anywhere inside 37.15-28' is FALSE as literally worded and TRUE once scoped: a samekh IS recorded on 37.28, which is numerically inside 37:15-28 but is the CLOSE SEAM under the convention that a mark sits on the verse it follows. The interior 37.15-37.27 carries none. That is the wording-scope fix the order allows, and it is a scope defect, not a disclosure defect.",
 "A6 sweep MEASURED over the WEB verse map, every run located by exact token match across all 1273 verses: 31 A6/A6_UNION runs checked for book-wide occurrence count, in-span occurrence, presence at each declared reference, and presence in the row's own named field. All 31 results are recorded per item in the deliverable.",
 "ONE A6 run is NOT PRESENT IN THE ROW AT ALL: l05_i33's 'have heard all your insults' is absent from all four fields of P08-007. It does occur once in WEB Ezekiel, at web:Ezek.35.12, in span. Reported as a finding, not as agreement or disagreement.",
 "P10-001's existing claim of 'an eighteen-verse run of that verb across 40:5-41:5' REPRODUCES: stripping all combining marks, 18 of the 50 verses in 40:5-41:5 carry the consonant string ymd, one occurrence each (40:5, 6, 8, 9, 11, 13, 19, 23, 27, 28, 32, 47, 48 and 41:1-5). I did not restate the figure in any entry, since it is the row's own count, but it holds.",
 "P09-001's existing claim that the 37:14 close is 'part of a 21-verse 2mp family sweep' is SUPPORTED by the governing input: ezek_device_inventory.v2.json formulae.recognition_formula_2mp.verses_mt is a 21-member list and Ezek.37.14 is in it. Read from v2, which C2-amended makes authoritative for counts and list membership.",
 "FACE CHECK: all 60 verse references I cite were tested against each WEB entry's own mt back-reference and every one is identity (mt == web key). None falls in the ch 20/21 renumbering zone, so no dual-face writing is owed on any entry of mine. I did not cross faces by arithmetic anywhere; the one zone verse I encountered in passing, web:Ezek.21.3 = oshb:Ezek.21.8, appeared only in an item's context list and I did not cite it.",
 "MY OWN TWO DETECTOR BUGS, caught and corrected, reported because a silent false negative here is the exact failure this wave guards against. (1) My first A6 matcher kept ASCII apostrophes as word characters, so runs adjacent to a quote mark in the WEB text failed to match; it reported 'they have been laid desolate' as occurring ZERO times and web:Ezek.26.3 as not carrying 'behold, I am against you'. Both were WRONG. Re-tokenising every non a-z character to a space, the run IS at web:Ezek.35.12 and 26:3 DOES carry the other. Had I trusted the first pass I would have refused two executable orders. (2) My first vayyamod scan stripped only three combining marks and returned ZERO verses for a claimed eighteen-verse run; stripping all Mn characters returns 18. Neither bad result reached the deliverable.",
 "SELF-CHECKS run over the finished edit set: expected_before re-compared byte-for-byte against the lane file for all 63 edits (0 mismatches); one-edit-per-(row, field) enforced, with append_ref groups confirmed to share an identical expected_before; every one of the 83 item ids present in exactly one of items_discharged and items_NOT_discharged; every ROLE-token annotation at most 6 words with exactly one token per entry; and a 7-gram scan over all of my new text against itself and against the pre-edit bytes, which now shows ZERO new duplicate 7-grams (my first draft introduced 16 and I reworded until none remained).",
]

UNRES = [
 "ITEM ID CONVENTION IS MINE, not the worklist's. The 83 items in your_worklist_items carry no id field of any kind. I minted 'l05_iNN' from each item's 0-based index in that array, in file order, and every id in this deliverable resolves that way (l05_i00 .. l05_i82). If your harness expects a different key, the mapping is mechanical and the per-edit row/field/citation triples identify each item independently.",
 "PREFIX CHOICE for new refs entries: I used 'web:' throughout, following the brief's three worked examples of entry shape and verse_inventory.json's WEB numbering face, even though most existing entries in these rows carry 'oshb:'. It is safe here only because I measured mt == web identity for all 60 refs. If the wave wants new entries in the witness face instead, the substitution is mechanical.",
 "THREE COMBINED EDITS borrow an item across sweeps (see ESC-5): P08-013/boundary_evidence_refs and P10-001/boundary_evidence_refs are labelled a4 but each carries one a6 item, and P09-002/strongest_rejected_alternative is labelled grounds but carries one a6 item. The sweep labels are my judgement, not an order.",
 "A6-b ASYMMETRY I chose deliberately and am disclosing: where a 5-word run is an addressee title plus the row's own preposition AND the quotation was already delimited with an in-field reference, I took the exemption and made no edit (l05_i13, l05_i34, l05_i71, l05_i74). Where the run reproduced a WEB verse exactly, was NOT already delimited, and the entry's own verse was available to reference, I installed rather than exempted (l05_i35, 'the mountains of Israel'). Whether 'the mountains of Israel' is an A6-b addressee title in the same sense as 'house of Israel' is genuinely arguable; I resolved it toward installing, because an unnecessary reference is checkable while a missed one is silent.",
 "P08-007's second use of the recognition gloss sits at 35:12, and WEB 35:12 renders that verse differently ('You will know that I, Yahweh, have heard all your insults'). Under A6-b a device gloss need not match the verse it stands next to, so I left it and took the exemption; but a reader could take the single-quoted gloss there as a quotation of 35:12, and the spot wave should look at it.",
 "P09-002 refs entry 2 remains silent on the second 37:16 Qere form (ESC-6).",
 "I did not open book_strategy_Ezek.md or either device inventory beyond the one v2 key named above. Every rule I applied is quoted verbatim in the brief, which governs, so this is a deliberate scope limit rather than an unavailability; if any of my rule applications needs to be checked against the strategy text itself, that check has not been done by me.",
 "The transport-class question is untouched. P10-001's prose already carries transport claims at MT 40:2 and 40:3, two of the thirteen verses brief section 12 routes to the controlling agent. None of my six P10-001 items requires a membership claim, I added none, and I altered none of the existing wording about them.",
]

deliverable = {
 "lane": "ezek_author_l05",
 "attempt_id": "ezek_author_l05_a1",
 "execution_id": "ezek_author_l05_a1#e1",
 "stage": "FINAL",
 "item_id_convention": "l05_iNN, where NN is the 0-based index of the item in your_worklist_items as delivered (the items carry no id field of their own). Range l05_i00 .. l05_i82.",
 "pinned_digests_confirmed": {
   "rows_file_sha256_at_read": "25cdba568d98ec60aa719606be7b273e6a7c7256c55b79a3c579ada3c21d0ecc",
   "worklist_sha256_at_read": "059c294e82a7a73097c0bf9e52016d400907c032358f1ecb09a76f9bda1af3ad",
   "note": "both copied from the lane file's own fields; the rows file itself was not opened, and nothing under C:\\wt\\logos-t423-m8-fable was written"
 },
 "sources": SOURCES,
 "edits": EDITS,
 "edit_summary": {
   "total": len(EDITS),
   "by_sweep": dict(collections.Counter(e['sweep'] for e in EDITS)),
   "by_op": dict(collections.Counter(e['op'] for e in EDITS)),
   "rows_touched": rep['rows_touched'],
   "seams_moved": 0,
   "fields_touched": rep['fields_touched'],
 },
 "role_token_rotation": rotation,
 "items_discharged": d['discharged'],
 "items_NOT_discharged": [{"item": a, "disposition": b, "row": c, "why_not": e} for a, b, c, e in d['not_discharged']],
 "escalations": ESC,
 "changes_made_or_no_change": (
   "CHANGES MADE. 63 edits across all 24 rows, 0 seams moved, no span/osis/decision_id/writer field touched. "
   "6 confidence moves applied as ruled (P07-008 low->medium_low; P08-003 medium_low->medium; P08-012 high->medium; "
   "P08-013 high->medium; P09-009 medium_low->medium; P09-011 high->medium), all inside the four-value scale. "
   "35 A4 refs entries installed as append_ref, one per citation, with a RANGE entry for each of the 6 range citations and exactly one of the eleven ROLE tokens on each. "
   "2 WORDING orders applied, replacing 'a full refrain-grade close' at P08-012 and P08-013 with descriptions true to the measured bytes of 36:23, differently formulated on the two rows so no 7-gram is shared; neither confidence moved on account of the wording, and both rows' MEDIUM comes from their own ruled CONFIDENCE items. "
   "3 BOSS_RETURN work orders carried in full, each after independently reproducing its C1 from the pinned input: P08-002 (A2 K/Q disclosure at 33:13 and 33:16 added, verbatim scope corrected, the 33:12 ve'attah installed as the licensed rival onset with the over-split guard as the stated holding ground, the sof-pasuq sentence kept MEASURED with its pmarks key cited and no tier cure applied, and the device_notes holding ground brought into line so the two fields no longer state different grounds); P08-011 (the 'separators stripped' claim rescoped to the two notes that actually carry separators, with the measured counts); P09-002 (the 37:16 disclosure reworded to two Qere notes of the same word under different pointing with the one-codepoint difference named, and the mark claim rescoped to the row's interior). "
   "20 A6 dispositions written and 11 answered as no-edit: 18 quotation conventions installed, 2 out-of-span AUTHOR_JUDGEMENT questions answered NOT COINCIDENTAL with evidence, 6 A6-b exemptions taken with the device naming quoted, 4 fields found already compliant, and 1 order reported unexecutable because the run is not in the row."
 ),
 "verification_evidence": VER,
 "unresolved_uncertainty": UNRES,
 "e19_selfreport": (
   "Exact-path law kept for every pinned input and every lane file: each was opened by the exact path given in the launch brief, and no glob, no recursive search and no directory walk was run anywhere under C:\\wt\\logos-t423-m8-fable or the lane directory. "
   "Two disclosures rather than a clean claim. (1) In the digest-verification pass I wrapped each of the nine pinned paths in a file-existence test before hashing it; that is a test, and although every path was an exact path from the brief and no directory was tested for, a stricter reading of 'a directory is never tested for' would have had me hash unconditionally and report the error. (2) I listed my OWN private scratch subdirectory once, immediately after writing the stage-0 stub, and ran line counts and text searches over my own intermediate files. No listing touched a shared or pinned location. "
   "Lane blindness kept: I read no other lane's rows or output, nothing in reviews/, no peer packet, no fix-up order, no cure claim, no transcript, and no ruling beyond what the brief quotes. The only cross-lane facts in this deliverable are the ones my three BOSS_RETURN items carry in their own text."
 ),
 "limit": (
   "What this lane does NOT establish. (1) I judged mirroring nowhere: which citations were unmirrored is EXTRACTED from the ruled worklist, not re-derived, so a missing item is invisible to me. (2) I did not re-verify the rows' pre-existing census figures except the four I name in verification_evidence (the 18-verse measuring run, the 21-verse 2mp membership of 37:14, the 14 year-bearing datelines against the ratified D11 table, and the 184 mark occurrences against marks_tally); every other sweep count in these rows is the original writer's and travels unchecked. (3) A6 run detection is mine and is only as good as its tokenisation - it ignores case, punctuation and apostrophes, so it can over-match a run that the WEB punctuates across a sentence break, and it will not see a run the boss's sweep did not name and no peer named. (4) Three rows carry substantive questions I measured but was not authorised to settle: P08-007's false separator claims, P08-014's onset licensing at the 36:32 weak-shape close, and P08-002's confidence under the corrected weighing. All three are in escalations; none is written into a row. (5) I read the strategy file's digest but not its text, so no rule application here has been checked against the strategy itself."
 ),
}

json.dump(deliverable, open('ezek_author_l05_deliverable.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print("deliverable written; edits", len(EDITS))
print("by_sweep", deliverable['edit_summary']['by_sweep'])
print("by_op", deliverable['edit_summary']['by_op'])
print("rotation:", {k: (v['instances'], v['distinct_formulations'], v['max_words'])
                    for k, v in rotation.items() if isinstance(v, dict)})
print("role-tokened entries installed:", rotation["_total_entries_installed_with_a_role_token"])
print("discharged", len(d['discharged']), "not_discharged", len(d['not_discharged']))
