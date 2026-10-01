import json, hashlib, os
W = r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l06_work_7c3f"
stage = json.load(open(os.path.join(W, "edits_stage.json"), encoding="utf-8"))
EDITS = stage["edits"]
NOT_D = stage["not_discharged"]
JUDGE = stage["judgement_no_edit"]
DISCH = [x for x in stage["discharged"] if x not in NOT_D]   # 91 lives in NOT_discharged only

rows_touched = sorted({e["row_id"] for e in EDITS})

SOURCES = [
 {"path": r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\ezek_author_l06_LAUNCH.md",
  "sha256": "not listed in the launch table; read as my own launch message", "read": "in full, first"},
 {"path": r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\AUTHOR_WAVE_BRIEF.v1.md",
  "sha256": "ccb7026f908345d3f9800671e621cd8fbdedc3429d41c22dc244b03e0474bd79",
  "read": "in full, all 12 sections, digest verified before reading"},
 {"path": r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_06_worklist.json",
  "sha256": "59c7c5231630a1d288278f85ee25357b2201f619532b99b014908ae6dac343a6",
  "read": "in full: all 26 rows' bytes and all 98 worklist items, each item's every key enumerated"},
 {"path": r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\Ezek_oshb.txt",
  "sha256": "337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e",
  "read": "1273 verse lines loaded; scripted skeleton sweeps for the measure verb, guided-motion tokens, the prostration and Chebar families, son-of-man variants and puncta; Hebrew quoted into my edits was SLICED from these bytes, never retyped"},
 {"path": r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\pmarks_Ezek.json",
  "sha256": "25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315",
  "read": "marks, paseq, kq and notes_other for chs 39-48 enumerated by key. kq values handled as LISTS of K-Q pair strings, which is what they are"},
 {"path": r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\book_strategy_Ezek.md",
  "sha256": "4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3",
  "read": "599 lines; targeted reads of the device sweeps (lines 100-159), source-metadata law (236-254), the parent architecture and P8 hard seams (256-277), the region notes (430-444) and the self-check arms (522-599)"},
 {"path": r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\ezek_device_inventory.v2.json",
  "sha256": "356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f",
  "read": "v2 only, as section 12 directs: vision_transport in full including relation_to_the_strategy_closed_20, the formula blocks, calendar_dates_not_datelines, year_word_but_not_a_dateline, dated_oracles, masoretic_disclosure_objects"},
 {"path": r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\verse_inventory.json",
  "sha256": "7314690191ec380b25578ca33d4745f4e60196b9f0e1dda4a1bcc9286c19cf54",
  "read": "digest verified only; not relied on, because the inventory v2 states the WEB/MT divergence directly"},
 {"path": r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\web_mt_offset_map.json",
  "sha256": "b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887",
  "read": "MEASURED and reported, as the launch table asked (no digest was pinned for it). Not otherwise needed: my lane is chs 40-48, where the pinned inputs state MT/WEB identity, so no face crossing arises and no dual writing is owed"},
 {"path": r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\tools\verse_map_web.json",
  "sha256": "bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98",
  "read": "1273 keyed verses; every one of the 42 A6 runs checked word-for-word against the cited verse, plus a 5-gram index of the whole book used to prove my new prose introduces no fresh undelimited quotation"},
 {"path": r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\tools\verse_map_oshb.json",
  "sha256": "408b7ee74564aef902c5fc539d6577f7708fa9aa839c993ce6281d86dc3a7901",
  "read": "digest verified; not read further, because Ezek_oshb.txt carries the same witness and my lane never crosses faces"},
]

VERIF = [
 "A6 run existence: all 42 ordered runs were located BOTH in the row field named by the item AND in tools/verse_map_web.json at the cited verse. EXTRACTED, by script, matching on a lowercased alphanumeric token sequence. None was missing; none had to be refused for non-existence.",
 "A6 verbatim-ness, the thing the run check does NOT establish: five of the ordered runs sat inside row glosses that are NOT the WEB's wording. 40:5 and 40:38 carried a comma the WEB has not; 41:1 and 42:15 were split by an ellipsis the WEB has not; 41:12 stopped one word short of the WEB's 'west'. In each case the delimited text now carries the verse's own words and the row's gloss stays outside the delimiters.",
 "A6-b judgements, five items, recorded as findings rather than as yes/no. idx6 (web:Ezek.40.20, 'the gate of the outer court'): a QUOTATION -- the WEB's wording at the very verse the row is describing; convention installed. idx75 (web:Ezek.44.4, 'I fell on my face'): a QUOTATION; A6-b NOT applied because its exempt list names the messenger, utterance, recognition, word-event and hand-of-YHWH renderings and addressee titles, and the prostration formula is none of those, so the duty stands even though the row does name the device. idx52 ('the holy and the common', web:Ezek.22.26/44.23): NOT a quotation of either -- see the next entry, it is the row mis-rendering its own verse. idx23 ('between the porch and the', web:Ezek.8.16): NOT a quotation -- the words are the author's running prose ('no formula or refrain close intervenes between the porch and the nave'); the collocation with 8:16 ('between the porch and the altar') is accidental. idx45 ('he said to me these are the', web:Ezek.46.24): NOT a quotation -- the run only exists by straddling the row's own quotation boundary, 'he said to me': these are the holy chambers, and the 'he said to me' part is the WEB's fixed rendering of a device the row names, which A6-b does gloss. Note the cause precisely: because normalisation strips punctuation, this collocation cannot be removed by any punctuation change, which is why it is a judgement and not a repair.",
 "idx52 root cause, MEASURED against tools/verse_map_web.json: the WEB at Ezek.42.20 reads 'to make a separation between that which was holy and that which was common'. The row had compressed this to 'the holy and the common', which is not the WEB's wording at 42:20 but IS the WEB's wording at 22:26 and 44:23 -- which is exactly why the audit flagged an out-of-span match. Restoring the verse's own words inside the delimiters discharges the install and dissolves the collocation at once.",
 "MARKS_3D at P11-001, MEASURED from pmarks_Ezek.json with the stated convention that a mark is recorded ON the verse it follows: marks['Ezek.43.27'] == ['SAMEKH','SAMEKH']; marks['Ezek.44.14'] == ['PE']; there is NO key for Ezek.44.1, 44.2, 44.3 or 44.4. So the flagged clause was false in the precise way the order said: the onset seam DOES carry corroboration, and the row's own rationale already argued from it. Three directions now recorded separately: onset corroborated, interior 44:1-44:3 empty, close seam empty until the pe after 44:14. The doubled samekh is the book's only doubled parashah occurrence (184 occurrences on 183 verses, per masoretic_disclosure_objects), and it is not added to the verse total.",
 "Paseq, MEASURED per verse from pmarks_Ezek.json for every row in the lane. All eight pre-existing paseq claims in my rows REPRODUCE exactly: P10-002 five occurrences over four verses (40:5, 40:6, 40:14, 40:16 x2); P10-003 one at 40:17; P10-004 one at 40:25; P10-016 four over four (40:29, 40:30, 40:33, 40:36); P10-005 two (40:43, 40:47); P10-007 six over six with 41:9 alone empty; P10-008 five over four (41:12, 41:16 x2, 41:17, 41:19); P10-010 three over two (42:10, 42:13 x2); P10-011 two (42:15, 42:20); P10-012 one at 43:8; P10-013 one at 43:12; P10-014 none in 43:13-17; P10-015 none in 43:18-27.",
 "K/Q, MEASURED from pmarks_Ezek.json, kq values read as LISTS. The 'twenty-three doubled-note K/Q verses' figure that P10-004 and P10-016 both rely on REPRODUCES: exactly 23 verses in the book carry two or more K-Q notes (14 of them carry exactly two). P10-004's four named verses (40:21, 40:22, 40:24, 40:26) and P10-016's six (40:29, 40:31, 40:33, 40:34, 40:36, 40:37) are all in that set, and the per-verse note counts the refs entries state (tripled, quadrupled, doubled) match the list lengths verse for verse.",
 "Measure-verb count in P10-002, MEASURED by script over the Ezek_oshb.txt skeleton: the claim 'the first of six occurrences of the measuring verb inside this row (40:5, 6, 8, 9, 11, 13)' reproduces exactly -- vayamad stands at 40:5, 40:6, 40:8, 40:9, 40:11, 40:13 and nowhere else in 40:5-40:16. 40:10's two tokens are the NOUN 'measure' and are correctly excluded. The '18-verse vayamad run 40:5-41:5' in the same row matches the strategy's own figure at line 113.",
 "Puncta, MEASURED by counting U+05C4 in the verse bytes: Ezek.41.20 carries 5 and Ezek.46.22 carries 7, totalling the 12 that masoretic_disclosure_objects records, with zero U+05C5. P10-008's five and P11-009's seven are both right, and both rows carry the single-witness disclosure the strategy's puncta arm requires.",
 "Unmarked-stretch figure in P10-012, MEASURED: ch 39 has 29 verses, so 39:29 is its last verse. From the verse after the pe at 39:29 through 43:8 is 49+26+20+8 = 103 verses carrying no mark, ended by the samekh following 43:9. The row's '103-verse unmarked stretch' therefore reproduces; the figure is the run of unmarked verses, not the distance to 43:9, which is 104.",
 "Formula-class figures my rows lean on, EXTRACTED from ezek_device_inventory.v2.json by exact key and cross-checked against the strategy: son-of-man 93 verses (40:4, 43:7, 43:10, 43:18, 44:5, 47:6 in my stretch); long messenger formula 122 verses (43:18, 44:6, 44:9, 45:9, 45:18, 46:1, 46:16, 47:13); long utterance 81 verses (43:19, 43:27, 44:12, 44:15, 44:27, 45:9, 45:15, 47:23, 48:29). Every messenger and utterance claim in my rows sits on a verse in those lists. The 'next messenger formula is not until 46.16' claim in P11-007 is confirmed by the same list.",
 "'And you, son of man' at P10-013, MEASURED: the form with the leading vav stands in exactly 23 verses, matching the strategy's 23; the vav-less form at 43:10 is UNIQUE in the book (one verse). So the row's description -- a near-form disclosed as distinct from the 23-verse sweep rather than counted against it -- is exactly right.",
 "Chebar and prostration figures at P10-012, both checked because the refs entry I had to edit carries them. Chebar: the strategy names 8 verses and my sweep finds the kbr token in exactly those 8 (1:1, 1:3, 3:15, 3:23, 10:15, 10:20, 10:22, 43:3; two of them spell it with the prefixed b-). Prostration: the strategy names 5 verses (1:28, 3:23, 11:13, 43:3, 44:4) and my sweep finds the exact form in exactly those 5. P11-001's cross-reference list is that same class minus its own verse. Both figures stand.",
 "Prostration, the thing I found that nobody asked about: a SIXTH verse, MT 9:8, carries the lengthened form of the same verb with the same 'on my face' phrase, and the WEB renders 9:8 'I fell on my face' too. The strategy's 5-verse class excludes it and ezek_device_inventory.v2.json carries no prostration class at all. I did not touch the figure -- it is sourced, it reproduces on the exact form, and no item ordered it -- but the class boundary is narrower than its gloss suggests. Routed in escalations.",
 "'He said to me', the discrepancy I nearly mis-reported. My first sweep of the bare adjacent pair returned 35 verses against the strategy's 36, which looks like a defect. It is not: admitting an intervening divine name adds MT 23:36 and the figure becomes exactly 36. Reported here as a predicate-scope difference, not as a mismatch, because the difference is in my predicate and not in the pinned input. No row of mine cites the figure.",
 "Chodesh, calendar and year-word claims, EXTRACTED from the inventory: calendar_dates_not_datelines is exactly 45:18, 45:20, 45:21, 45:25, and chodesh_verses_correctly_excluded contains 45:17, 46:1, 46:3, 46:6 and 47:12 -- so every homograph disclosure in P11-005, P11-007 and P11-010 is sourced, and 47:12 is indeed the last such verse in the book. year_word_but_not_a_dateline contains 46:13 and 46:17, so P11-007's and P11-008's year-word disclaimers are sourced. dated_oracles is 14 verses with 40:1 the highest, so P11-006's claim that no year-bearing dateline falls across 44:1-48:35 holds.",
 "Hard seams and regions, EXTRACTED from the strategy: P8's named hard seams are 42:20/43:1, 43:27/44:1, 46:18/46:19 and 47:12/47:13, and the p11 part row additionally names 47:1. Every 'hard seam' claim in P10-011, P11-008, P11-009, P11-010 and P11-011 lands on one of those. The strategy's named vision_report regions include 43:1-9, 44:1-4, 47:1-12 and the kitchen circuit 46:19-24, matching those rows' unit_type; its temple_law list matches P10-013, P10-015, P11-004 through P11-008; its land_allotment list matches P11-011 through P11-015 and P11-013; and it names 47:3-5 as temple_measurement, which is what P11-010 discloses as a category deviation.",
 "The A16 weighing at P11-010, each limb measured before it was written. Near face Ezek.47.6: a said-to-me verse AND a guided-motion verse carrying two 1cs-suffixed motion verbs, and it is one of the strategy's closed 20, so the rival is licensed and I say so rather than dismissing it. Far face Ezek.47.5: one measure-verb occurrence and a content close, no close-role formula, and pmarks has no mark key for it -- so the rival is one-faced, not two-faced. Grounds for holding: 47:6's question looks back at the measuring just reported; the strategy treats 47:1-12 as one region and names 47:6 inside it; and the only further signal there is the WEB's mid-verse paragraph, which the strategy's own E-23 rule makes tier-4 and never corroborating.",
 "The replaced ground at P11-010, stated as what I found rather than as agreement or disagreement. The old clause said no fresh transport or messenger formula opens 47:3 and none closes 47:5. Narrowly, on verse-initial position, that is TRUE: 47:3 opens with an infinitive-construct clause, not a motion verb. But 47:3 carries a 1cs-suffixed motion verb later in the same verse and 47:4 carries the same form twice, so the clause implied an absence the bytes do not support. Both verses are in the routed thirteen, so the replacement states the byte facts and makes no membership claim in either direction.",
 "Self-checks run over my own output, by script: (1) every one of the 78 edits' expected_before compared byte-for-byte against the value in the lane file -- all 78 identical, and each was taken programmatically from the parsed lane file rather than retyped; (2) every replacement anchor asserted to occur EXACTLY once in the field before substitution, which is how a bad anchor at P10-003 was caught and fixed rather than shipped; (3) one set edit per (row, field), verified none doubled; (4) a 5-gram index of the whole WEB run against my new prose with delimited quotations masked out -- ZERO new undelimited five-word WEB runs introduced, so this wave's A6 repairs create no fresh A6 defects; (5) the rotation rule checked per token type -- ANCHOR 9 entries/9 formulations, WARRANT-close 9/9, WARRANT-rival 9/9, WARRANT-onset 6/6, DISCLOSURE-mark 6/6, DISCLOSURE-paseq 11 entries/8 formulations, every free text at or under 6 words; (6) no edit touches span, osis_start, osis_end, decision_id or any writer-identity field, and no edit touches confidence, since this lane was handed no confidence item.",
 "Numbering, checked before writing single-face references: ezek_device_inventory.v2.json states MT/WEB identity in every chapter outside the ch 20/21 zone, and pmarks_Ezek.json states the same. My lane is Ezek.40.5-Ezek.48.35, wholly outside the zone, so dual writing is not owed here and no reference of mine crosses a face by arithmetic.",
]

ESCAL = [
 {"row": "P11-006 (and the strategy itself)",
  "what": "book_strategy_Ezek.md contradicts itself about MT 45:18, which is this row's first verse. Section 2d.5 (lines 144-152) says the three festival dates 45:20, 45:21 and 45:25 are not datelines, that 'a row seam at 45:20, 45:21 or 45:25 is a hard error' -- 45:18 pointedly NOT in that list -- and that those dates 'sit inside the temple-law paragraph opened by the messenger formula at 45:18'. The region notes (line 440) likewise name only 45:20, 45:21 and 45:25 as verses that never open a row. But the section 10 self-check arm at line 582 reads 'Calendar-date arm: any row whose onset is MT 45:18, 45:20, 45:21 or 45:25 fails.' Read as written, that arm fails P11-006, whose span is Ezek.45.18-Ezek.45.25. Read as 'any row whose onset is ARGUED FROM the calendar date', P11-006 passes, and it passes cleanly, because it rests its onset on the messenger formula and discloses the date as not onset evidence.",
  "why_i_did_not_write_it": "C2-amended: where ONE input contradicts itself, report upward and score no row. Deciding it either way would either condemn a row whose reasoning the strategy's own section 2d.5 endorses, or silently pick the reading that suits the row. It also touches whether the span is legal, and a span is not mine to move. My single item for this row is an unrelated mark disclosure at 45:17, which I did install: it records only that a samekh follows that verse, MEASURED from pmarks, and it stands whichever way the contradiction is resolved."},
 {"row": "P11-010",
  "what": "The GROUNDS order reads, in full, 'all five repairs; A16 weigh the 47:6 rival'. The five repairs are not enumerated in my launch message, in the AUTHOR_WAVE_BRIEF, or in the lane file, and the item carries no field key. I executed the one duty named explicitly -- the A16 weighing -- and the one repair I could establish from the bytes, the clause that understated the guided-motion tokens at 47:3 and 47:4. I cannot certify five-for-five parity against an order I cannot read.",
  "why_i_did_not_write_it": "I did write an edit, and I have ALSO listed the item in items_NOT_discharged, deliberately and not as an oversight: claiming it discharged would assert a completeness I cannot evidence, and claiming nothing was done would hide a real repair. The controlling agent should either supply the enumeration for a second pass or confirm that the weighing plus the byte repair is the whole of it. Two further candidate repairs I found but did NOT make, because no item named them: this row discloses no paseq at all, though pmarks records three occurrences over two verses in its span (47:9 once, 47:12 twice); and it calls the four measurements of 47:3-5 'four successive measured wadings', where the fourth, at 47:5, is the channel that cannot be crossed rather than a wading."},
 {"row": "P10-005, P10-011, P11-009, P10-004, P10-006, P11-001, P10-015 (the routed thirteen inside my lane)",
  "what": "My lane is where the transport-class question bites. Eight of the thirteen routed verses fall in it: MT 40:24, 40:48, 42:15, 43:1, 44:1, 46:21, 47:3 and 47:4. I wrote NO membership claim for any of them. Where an item required a seam-facing entry at one -- WARRANT-close at 40:48 and at 43:1, WARRANT-rival at 44:1 and at the 44:1-44:4 range -- the free text describes what the verse does and names no class and no count, and each entry's tier line records that the class question is routed. Separately, and this is the part that needs a decision rather than my judgement: four of these rows carried PRE-EXISTING descriptions calling 40:24, 40:48, 42:15, 43:1, 44:1 and 46:21 'transport verbs' in fields my A6 items forced me to re-emit. I carried those clauses forward byte-unchanged, adding nothing, because #e12 A12 as recorded in the inventory permits a row to describe such a verse as guided motion by content while forbidding it to call the verse a member of the closed 20, and none of those clauses states a count or a list.",
  "why_i_did_not_write_it": "A membership claim at any of the thirteen is exactly what section 12 forbids until the controlling agent rules. Neutralising the pre-existing wording instead would have changed grounds I was not ordered to change; re-emitting it unchanged asserts only what #e12 A12 already allows. If the ruling goes the other way, those clauses are the exposure and this is the list of them."},
 {"row": "P11-009 (device_notes, a field I did not touch)",
  "what": "P11-009's device_notes says 'The book's transport-verb sweep (sweep: 20 verses) names only Ezek.46.19 for this chapter'. That sentence is true of the strategy's closed 20 and it labels its source, but it is a count-and-membership claim keyed to the very list whose authority for rows is routed, and MT 46:21 -- named in the same sentence -- is one of the thirteen. If v2 supersedes the closed 20 for rows, this sentence becomes a superseded figure written into a row.",
  "why_i_did_not_write_it": "No item of mine addresses that field, and I did not touch it. Flagged so the decision has the full exposure list rather than only the fields this wave happened to open."},
 {"row": "P11-008 (a field I did not touch)",
  "what": "P11-008's boundary_rationale licenses its messenger-formula onset at 46:16 like this: the topic is 'a distinct subject (inheritance, not the cultic calendar) from the cultic-calendar law before it (46.1-15), which is exactly the corroboration required before a messenger-formula seam is honored'. Under the governing CUT-RULE in section 1 of my brief, that is not one of the two limbs: limb (a) is that the ADDRESSEE changes, limb (b) that the previous verse ENDS on a verse-final close-role formula, and a mark alone never satisfies limb (b). MEASURED: 46:15 ends on 'a continual burnt offering' with no close-role formula, and the pe that follows it is a mark; the addressee does not change, only the subject. So the row's stated licensing ground appeals to a topic change, which the strategy's older section 2d.6 phrasing allows and the ruled CUT-RULE does not.",
  "why_i_did_not_write_it": "My two items for this row are A4 reference installs, which append to boundary_evidence_refs and do not open the rationale, so I never re-emitted the clause. Re-arguing an onset is a grounds change nobody ordered and could shade into a seam question, which is not delegated to this wave. Raised, not written."},
 {"row": "P11-004, P11-007, P10-016 (disclosure gaps found in passing)",
  "what": "MEASURED from pmarks_Ezek.json, three of my rows do not disclose K/Q or note-layer items their spans cover. P11-004 (45:1-45:8) discloses none, while kq has entries at Ezek.45.3 and Ezek.45.5. P11-007 (46:1-46:15) discloses none, while kq has entries at Ezek.46.9 and Ezek.46.15 and notes_other has an untyped note at Ezek.46.12. P10-016 (40:28-40:37) discloses its six K/Q verses but not the untyped ketiv/qere note at Ezek.40.31 in notes_other.",
  "why_i_did_not_write_it": "No worklist item of mine covers these, and A2/A3 disclosure is a separate sweep in the order of execution. Installing them unasked would put unordered content into two fields. Recorded so the gap is visible rather than absorbed."},
 {"row": "the pinned inputs, not a row",
  "what": "The prostration class is 5 verses in book_strategy_Ezek.md (1:28, 3:23, 11:13, 43:3, 44:4) and absent from ezek_device_inventory.v2.json altogether. MEASURED: a sixth verse, MT 9:8, carries the same verb in its lengthened form with the same 'on my face' phrase, and the WEB renders it 'I fell on my face' as well. So the 5 is the exact-form count, not the count of the phrase, and two of my rows (P10-012's 'one of five' and P11-001's four cross-references) inherit that scoping.",
  "why_i_did_not_write_it": "The figure is sourced in a pinned input, it reproduces against the exact form, no item ordered it, and C2-amended gives the inventory authority over counts only where the inventory HAS the class -- here it has none. Changing '5' on my own initiative would substitute my predicate for the pinned one. Reported for the inventory's next version, where the class deserves a stated predicate the way the transport class now has one."},
]

NOT_DISCHARGED = [
 {"item": NOT_D[0],
  "why_not": "PARTIAL, and listed here rather than in items_discharged on purpose. The order is 'all five repairs; A16 weigh the 47:6 rival' and nothing available to this lane enumerates the five repairs; the item also names no field. I DID produce an edit for this item -- the A16 weighing of the 47:6 rival, written on measured limbs, plus the replacement of the one ground I could show understated the bytes at 47:3 and 47:4 -- and that edit lists this item id in its worklist_item_ids and carries a PARTIAL note. What I cannot do is certify that the repairs I made are the five the ruling ordered. Calling that discharged would be the exact failure this wave guards against; calling it untouched would hide real work. See escalations for the two further candidate repairs I found and deliberately did not make."},
]

UNRESOLVED = [
 "Token fit for the 41:9 absence entry. The row's claim is that 41:9 alone in its span carries no paseq. MEASURED and true. But the vocabulary's absence token, WARRANT-absence-over-range, is scoped to a range, and 41:9 is a single verse, so I used DISCLOSURE-paseq with free text that states the polarity ('no paseq on this verse'). The token names the right layer and the text carries the fact, but if the spot wave expects the absence token stretched to a one-verse range, this is the entry to re-token.",
 "Whether P11-006's span is legal at all, pending the MT 45:18 self-contradiction in escalations. My edit for that row records only a mark and does not depend on the answer.",
 "Whether the pre-existing 'transport verb' descriptions I carried forward unchanged at 40:24, 40:48, 42:15, 43:1, 44:1 and 46:21 survive the routed ruling. I added nothing to them and no count sits in any of them, but if v2 supersedes the closed 20 for rows, those clauses are where my lane is exposed.",
 "The scope of the P11-010 order, unresolved by construction: five repairs were ordered and I can evidence two.",
 "Two A6 items discharge to 'no convention owed' and therefore carry NO edit by design: L06#23 (web:Ezek.8.16) and L06#45 (web:Ezek.46.24). They are in items_discharged because a judgement was made and recorded, not because bytes changed. If the mechanical check pairs items_discharged against edits, those two will show as unpaired and this is the reason. The 46:24 one cannot be resolved by editing at all, since the collocation survives punctuation normalisation.",
 "DISCLOSURE-device has only one entry in my lane, so it necessarily carries one formulation rather than the rotation rule's four. Every token type with four or more entries meets the rule.",
 "Quotation case-folding: where an ordered run begins a WEB sentence and sits mid-sentence in the row, I kept the row's lowercase inside the delimiters (for example 'he led me toward the south' at 40:24, which the WEB capitalises). I treated sentence-initial case as a quoting convention rather than a content change, and I did NOT treat internal punctuation the same way -- commas and ellipses the WEB lacks were removed.",
]

deliverable = {
 "lane": "ezek_author_l06",
 "attempt_id": "ezek_author_l06_a1",
 "execution_id": "ezek_author_l06_a1#e1",
 "sources": SOURCES,
 "edits": EDITS,
 "items_discharged": DISCH,
 "items_NOT_discharged": NOT_DISCHARGED,
 "escalations": ESCAL,
 "changes_made_or_no_change": (
   "78 edits across all 26 of my rows, discharging 97 of 98 worklist items outright and one partially. "
   "Exact composition, because this wave exists to catch loose reporting: 51 append_ref edits plus 27 set edits, of which 2 set edits are on "
   "boundary_evidence_refs and 25 are prose. The 54 A4 citations land as 51 appends plus 3 entries inside the two refs set edits (43:6 and 43:8 at P10-012, 43:9 at P10-013). "
   "The 42 A6 items land as 38 inside the 23 prose edits whose sweep is a6, 2 inside those same refs set edits (the ordered delimiter at P10-012's 43:3 entry and at P10-013's 43:12 entry), "
   "and 2 that discharge to 'no convention owed' with no edit. The MARKS_3D item is 1 device_notes edit at P11-001 and the GROUNDS item is 1 "
   "strongest_rejected_alternative edit at P11-010. No confidence edit, because this lane was handed no confidence item, "
   "and no row's confidence is raised unasked. P11-004, P11-005, P11-006, P11-008 and P11-012 receive reference installs only, so their prose is untouched. "
   "NO SEAM IS MOVED and no edit touches span, osis_start, osis_end, decision_id or any writer-identity field. "
   "Two rows receive a set edit on boundary_evidence_refs rather than appends, because at P10-012 and P10-013 an ordered A6 install falls INSIDE an existing entry "
   "while A4 entries must also be added to the same field; existing entries are not re-tokenised, only the ordered delimiter is installed. "
   "THREE THINGS IN THIS DELIVERABLE ARE NOT PLAIN ORDERED WORK AND ARE FLAGGED HERE SO NOBODY HAS TO FIND THEM: "
   "(1) P10-015's boundary_rationale carries an unordered MEASURED precision correction -- the row said 43:18 opens with the son-of-man plus messenger formula, "
   "while the verse opens with the said-to-me formula and carries that material after it. I fixed it because re-emitting a field means asserting it, "
   "and knowingly re-asserting a byte-false clause is the OW-18 breach. "
   "(2) P11-010's strongest_rejected_alternative is a PARTIAL discharge, recorded in items_NOT_discharged. "
   "(3) Two A6 judgement items discharge to 'no convention owed' and so carry no edit at all: L06#23 and L06#45. "
   "Five ordered runs also had their delimited text corrected to the verse's own wording, because the row's gloss was not the WEB's -- that is the install done properly, not an extra change."
 ),
 "verification_evidence": VERIF,
 "unresolved_uncertainty": UNRESOLVED,
 "e19_selfreport": (
   "Exact paths only. No listing, no glob, no recursive search, no directory test. Eleven files opened, all by the exact path given in my launch message "
   "or in the brief, each digest verified BEFORE reading: the AUTHOR_WAVE_BRIEF and lane file matched the launch table, and so did Ezek_oshb.txt, pmarks_Ezek.json, "
   "book_strategy_Ezek.md, ezek_device_inventory.v2.json, verse_inventory.json, tools/verse_map_web.json and tools/verse_map_oshb.json. "
   "web_mt_offset_map.json had no pinned digest and I measured and report it: b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887. "
   "I did NOT open ezek_device_inventory.json (v1): section 12 says v2 governs counts and membership, and I had no claim needing the superseded figures. "
   "I read no other lane's rows or output, no reviews directory, no peer packet, no fix-up order, no cure claim, no transcript, and no ruling beyond what my brief quotes. "
   "I wrote nothing under C:\\wt\\logos-t423-m8-fable. All my writing is in one uniquely-named private subdirectory, scratchpad\\ezek_l06_work_7c3f: "
   "two scripts, four verification transcripts, one staged edit file and the two output files. No git, no receipts, no registry, no validator run, no row mutation. "
   "Per E-29 the deliverable was written at my first stage and rewritten at every stage, and both digests below are taken AFTER the final write."
 ),
 "limit": (
   "What this lane does NOT establish. (a) No count in my prose is a hand tally: every figure I asserted or re-asserted came from a named script over a pinned file, "
   "and where a figure was sourced to a pinned input rather than measured by me I say EXTRACTED, not MEASURED. (b) Intra-verse paseq position is UNAVAILABLE, not omitted: "
   "pmarks_Ezek.json states the extract drops the segs, so every paseq entry I installed is count-only and says so. (c) The XML seg totals behind pmarks are REPORTED by that "
   "toolkit and are not verifiable from the extract; I did not open the XML, which is outside my exact-path set. (d) MT 33:20's sof pasuq I neither resolved nor asserted; "
   "it is outside my span. (e) I did not re-adjudicate any seam, span, unit_type, confidence level, or any citation's mirroring status beyond what the worklist ruled. "
   "(f) I could not verify the enumeration behind P11-010's 'all five repairs'. (g) I cannot see whether another lane's edits collide with mine; the harness pools by sweep "
   "and my expected_before values pin the pre-mutation state, so a collision will surface as a refusal rather than as a silent overwrite."
 ),
}

p_del = os.path.join(W, "ezek_author_l06_deliverable.json")
json.dump(deliverable, open(p_del, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

final = dict(deliverable)
final["final_message"] = True
final["rows_touched"] = rows_touched
final["counts"] = {
 "rows_in_lane": 26, "rows_touched": len(rows_touched),
 "worklist_items": 98, "items_discharged": len(DISCH), "items_not_discharged": len(NOT_DISCHARGED),
 "edits_total": len(EDITS),
 "edits_by_op": {"append_ref": sum(1 for e in EDITS if e["op"] == "append_ref"),
                 "set": sum(1 for e in EDITS if e["op"] == "set")},
 "edits_by_sweep": {s: sum(1 for e in EDITS if e["sweep"] == s) for s in sorted({e["sweep"] for e in EDITS})},
 "judgement_items_with_no_edit": JUDGE,
}
p_fin = os.path.join(W, "ezek_author_l06_final_message.json")
json.dump(final, open(p_fin, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for p in (p_del, p_fin):
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    print(os.path.basename(p), h, os.path.getsize(p), "bytes")
print("rows_touched", len(rows_touched), rows_touched)
print("counts", json.dumps(final["counts"], ensure_ascii=False))
