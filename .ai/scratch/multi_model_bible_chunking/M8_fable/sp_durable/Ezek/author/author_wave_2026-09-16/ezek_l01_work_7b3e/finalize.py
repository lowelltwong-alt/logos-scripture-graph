# -*- coding: utf-8 -*-
import json, hashlib

W = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l01_work_7b3e'
out = json.load(open(W + r'\_stage.json', encoding='utf-8'))

out["escalations"] = [
 {"row": "P01-001",
  "what": ("The boundary_rationale asserts that 'the transport-verb and \"he said to me\" sweeps that mark scene "
           "changes elsewhere in the book's visions do not begin until chapter 8'. That is FALSE against the pinned "
           "inventory v2: /vision_transport/verses_mt has 33 members and MT 3:12 and MT 3:14 are two of them "
           "(MEASURED by set membership over the pinned list). It is not merely wrong by a verse - it is wrong in "
           "exactly the place the campaign has fenced off, because MT 3:12 and MT 3:14 are both on the 13-verse "
           "/vision_transport/relation_to_the_strategy_closed_20/verses_the_predicate_adds list that brief section "
           "12 names as HELD and routed to the controlling agent."),
  "why_i_did_not_write_it": ("Brief section 12 forbids writing a transport-class membership claim for any of those "
                             "13 verses, and repairing this sentence would require asserting or denying membership "
                             "for MT 3:12 and MT 3:14. No worklist item covers the sentence, so there is nothing for "
                             "me to mark not-discharged; it needs the controlling agent's transport ruling first. I "
                             "also note the exemption I ruled for l01#00 keeps my edits out of this sentence "
                             "entirely, which is why no edit of mine touches it.")},
 {"row": "P01-005",
  "what": ("The same held question shadows this row: its boundary_rationale calls 3:12 'the return-transport' and "
           "3:14 'transit texture', and both verses are on the held 13. I read the field closely and judged that "
           "neither phrase is a CLASS-membership claim - they describe the narrated action, and the row's "
           "observed_substrate_signals list carries only hand.yhwh, no transport signal."),
  "why_i_did_not_write_it": ("I therefore left that wording byte-identical. My three A6 edits on this field add "
                             "quotation delimiters and web: references only; they do not touch, strengthen or weaken "
                             "any transport description. Flagged so the controlling agent can re-read it once the "
                             "transport ruling lands.")},
 {"row": "P01-008",
  "what": ("An in-span parashah mark is undisclosed. pmarks_Ezek.json records SAMEKH on Ezek.4.15 as well as on "
           "Ezek.4.12 and Ezek.4.14. The row's device_notes discloses the marks after MT 4:12 and MT 4:14 but not "
           "the one after MT 4:15; the row's refs cite 4:15 only for its K/Q. Ezek.4.15 therefore carries both a "
           "K/Q and a samekh, and only the K/Q is acknowledged."),
  "why_i_did_not_write_it": ("No worklist item covers it - my lane has no MARKS class - and the brief tells me not to "
                             "invent items. Recording it rather than letting silence read as 'nothing here'.")},
 {"row": "P01-008",
  "what": ("Two further in-span devices are undisclosed: MT 4:5 and MT 4:6 are both members of inventory v2's "
           "11-verse /year_word_but_not_a_dateline class (MEASURED). The row discloses 4:6 for its K/Q and its "
           "editorial note but neither verse as a year-word non-dateline."),
  "why_i_did_not_write_it": "No worklist item covers it; reported, not invented."},
 {"row": "P01-009",
  "what": ("The order for l01#73 says 'the four interior marks'. I found FIVE mark-carrying verses strictly inside "
           "the span (pe after 5:4; samekh after 5:6, 5:7, 5:9; pe after 5:10), which is also exactly the set the "
           "row's own device_notes already listed. My reading is that the order reserves 5:4 for its second clause "
           "(the 5:4/5:5 rival) and means the other four; I cannot verify that reading."),
  "why_i_did_not_write_it": ("I did not write 'four'. My rewrite states all five and names which three coincide with "
                             "a messenger-formula onset, so the discrepancy cannot hide inside the prose either "
                             "way. Flagged for the controlling agent to confirm the intended set.")},
]

out["verification_evidence"] = [
 ("DIGESTS: all 11 pinned inputs matched their launch-table digests before I read them (sha256sum). "
  "web_mt_offset_map.json had no pinned digest and was measured: b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887."),
 ("EXPECTED_BEFORE: every expected_before was copied programmatically out of lane_01_worklist.json, never retyped. "
  "assemble.py re-compares each one against the lane-file bytes: identical for all 62 non-rebased edits. The one "
  "rebased edit (P01-001 boundary_evidence_refs, a6) was checked to equal the original list plus that row's single "
  "a4 append, in order."),
 ("A6 RUN EXISTENCE - MEASURED by a6_locate2.py over tools/verse_map_web.json: all 34 runs located at every verse "
  "their item names, and every item's declared words value equals its token count (asserted, no exception). My "
  "FIRST locator returned 0 hits for items 58, 59, 60; the cause was MY tokenizer folding WEB's nested left single "
  "quote into the following word, not any absence in the source. Recording the false negative because a boolean "
  "'not found' would have been indistinguishable from 'the claim is false'."),
 ("A6 SURGERY SAFETY - build_a6.py asserts each old substring occurs EXACTLY ONCE in the field before replacing it; "
  "all 27 installs passed. 12 set-edits result, one per (row, field)."),
 ("A6 PARAPHRASE CHECK - gloss_diff.py compared each single-quoted gloss to its WEB verse. Three glosses were NOT "
  "WEB runs: l01#09 ('and you, son of man, hear' vs WEB 'But you, son of man, hear'), l01#10 ('a hand stretched out "
  "to me' vs WEB 'a hand was stretched out to me'), l01#15 ('go, get you to the house of Israel' vs WEB 'go to the "
  "house of Israel'). I corrected the first two to the WEB's wording before delimiting and ruled the third exempt; "
  "delimiting a paraphrase as web: would have manufactured a false quotation. One further finding: WEB Ezek.3.7 "
  "carries a footnote marker between 'obstinate' and 'and', which the quotation omits as editorial apparatus."),
 ("ROTATION RULE - build_all.py asserts every one of the 48 annotations is <= 6 words and that any token used 4 or "
  "more times has at least 4 distinct formulations. Result: all 48 formulations are distinct "
  "(WARRANT-close 11/11, DISCLOSURE-mark 10/10, ANCHOR 9/9, WARRANT-rival 8/8, WARRANT-onset 5/5, "
  "DISCLOSURE-device 4/4, WARRANT-absence-over-range 1/1)."),
 ("7-GRAM GATE - my three new grounds texts produce 248, 168 and 180 new 7-grams with ZERO collisions against the "
  "original prose of all ten of my rows and ZERO collisions against each other. I deliberately varied wordings that "
  "would otherwise have repeated across the two rivals ('a mark alone never satisfies limb (b)' vs 'a parashah mark "
  "cannot meet that limb by itself'; 'disclosed for the alternative it corroborates' vs 'recorded as corroboration "
  "of the rival'). No annotation can form a 7-gram, being 6 words or fewer."),
 ("MARK DIRECTION - verified against pmarks_Ezek.json's own marks_note, not against any primary packet: a mark is "
  "recorded ON the verse it FOLLOWS. Every DISCLOSURE-mark token I installed was then checked against the marks "
  "dict: Ezek.3.3 PE, Ezek.3.21 SAMEKH, Ezek.4.12 SAMEKH, Ezek.4.14 SAMEKH, Ezek.4.17 PE, Ezek.5.4 PE, "
  "Ezek.5.6 SAMEKH, Ezek.5.9 SAMEKH, Ezek.5.10 PE, Ezek.5.17 PE. All ten confirmed."),
 ("K/Q SHAPE - pmarks kq is a dict verse -> LIST of concatenated ketiv+qere strings. I read it as a list and it "
  "reproduces every K/Q claim my rows make: Ezek.1.8 ketiv w-yd-w / qere w-ydy, Ezek.3.15, Ezek.4.6, Ezek.4.15, "
  "Ezek.6.3. All five K/Q verses of chs 1-6 are disclosed by my rows, and all three notes_other verses "
  "(1:11, 3:20, 4:6) are disclosed."),
 ("ITEM l01#24, the one WARRANT-absence-over-range - the claim VERIFIES. Ezek.3.10 and Ezek.3.11 are in none of the "
  "any-form word-event set, the 7-verse hand-of-YHWH list or the 14-verse dateline list. Tier: the 49/7/14 figures "
  "are EXTRACTED from ezek_device_inventory.v2.json; the non-membership of the two verses is MEASURED by my "
  "set-membership script over those pinned lists. As a by-product the script reproduced the brief's own arithmetic "
  "independently: vayehi_any(41) union hayah_any(7) = 48 exactly, and 48 + MT 1:3 = 49."),
 ("GROUNDS P01-008 - MEASURED. (i) pmarks records SAMEKH after Ezek.4.3. (ii) MT 4:3 ends "
  "'...oth hi l-beth yisrael', the sign colophon, verse-final; WEB Ezek.4.3 ends 'This shall be a sign to the house "
  "of Israel.' (iii) Ezek.4.3 is absent from both the 81-verse utterance list and the 64-verse recognition family, "
  "so CUT-RULE limb (b) is unmet; the addressee is unchanged (2ms imperatives both sides), so limb (a) is unmet. "
  "(iv) The reworded test: consonantal-skeleton test shows the TITLED form we-attah ben adam at Ezek.4.1 and "
  "Ezek.5.1, and bare we-attah without the title at Ezek.4.3, Ezek.4.4 AND Ezek.4.9 - three interior stages, where "
  "the old text named only two and omitted 4:3, the very verse the mark follows. (v) Far face is empty of formulae: "
  "across all 46 inventory verse-lists, ch 4's only members are son_of_man_address at 4:1 and 4:16 and "
  "year_word_but_not_a_dateline at 4:5 and 4:6. (vi) EXTRACTED: strategy section 7 line 373 holds exactly this "
  "division, '4:1-3, 4:4-8, 4:9-17'."),
 ("GROUNDS P01-009 - MEASURED, and the false ground is false three times over, not once. For each of the five "
  "interior marks I tested whether the following verse opens on a messenger formula: pe after 5:4 -> Ezek.5.5 in the "
  "122-verse messenger class, formula verse-initial; samekh after 5:6 -> Ezek.5.7 in the class, verse-initial behind "
  "lakhen; samekh after 5:7 -> Ezek.5.8 in the class, verse-initial behind lakhen; samekh after 5:9 -> Ezek.5.10 NOT "
  "in the class; pe after 5:10 -> Ezek.5.11 NOT in the class, opening on the oath with the utterance signature "
  "(5:11 is the only utterance-list verse in chs 1-6). So 'none coincides with a formula onset' was false for three "
  "of the five. The replacement ground is CUT-RULE and it holds: none of 5:4, 5:6, 5:7, 5:9, 5:10 appears in the "
  "utterance list or the recognition family, so no near face ends on a close-role formula. Addressee test at the "
  "A16 rival: 5:4 is 2ms to the prophet, 5:5 carries no second person at all, the 2mp shift arriving at 5:7 and the "
  "2fs at 5:8 - so limb (a) fails too. EXTRACTED: strategy section 7 line 373 holds '5:1-4' against 'the "
  "interpretation 5:5-17'."),
 ("NUMBERING FACE - MEASURED from web_mt_offset_map.json: rule.identity_outside_the_zone = true, and its "
  "tier0_disclosure confines the dual-writing duty to WEB 20:45-49, WEB ch 21 and MT ch 21, 'and only there'. My "
  "span is Ezek.1.1-Ezek.6.10, wholly outside the zone, so no reference of mine owes dual writing and none is "
  "written. I crossed no face by arithmetic."),
 ("COUNTS I DID NOT WRITE BUT PRESERVED - the fields I rewrote for A6 carry pre-existing figures that are not my "
  "items. I sourced them rather than assume: the 23-verse we-attah ben adam family in P01-008 is strategy line 121 "
  "(a named sweep, no verse list, so REPORTED and not an A12 class under A12-b; inventory v2 carries no such list, "
  "so under C2-amended it is not unsourced); the 12-verse rebellious-house figure and 'six in chapters 2-3' in "
  "P01-007 are strategy lines 124 and 270 (REPORTED). P01-001's 49-versus-48 word-event distinction and P01-006's "
  "'39 strict / 48 family' both reproduce against inventory v2 (MEASURED): MT 3:16 and MT 6:1 are the only chs 1-6 "
  "members of the strict 39, and MT 1:3 is in none of the three lists, which is exactly why it sits in the 49 and "
  "not the 48. The 7-verse hand-of-YHWH claims in P01-001, P01-005 and P01-007 reproduce: 1:3, 3:14, 3:22 are the "
  "chs 1-6 members, and 3:14 is additionally in the 2-verse conjunction-form sub-list, matching the row's pointed "
  "quotation. I changed none of these figures."),
]

out["unresolved_uncertainty"] = [
 ("ITEM IDS. The 84 items carry no id field. I minted l01#NN from the 0-based index in your_worklist_items and "
  "supplied item_identification so every id can be rebound to its (row, class, field, citation-or-run) tuple. If "
  "the orchestrator's mechanical check keys on a different id scheme, remap through that block, not through my "
  "index."),
 ("SCHEMA ADDITIONS. I added two top-level keys the brief's skeleton does not list - item_id_scheme with "
  "item_identification, and items_discharged_without_edit. The second exists because 7 discharged items are A6-b "
  "EXEMPT rulings that correctly produce NO edit, and the launch says items_discharged is checked against my edits "
  "mechanically. Rather than hide 7 items in either list I put them in items_discharged (the schema says 'every "
  "worklist item id you addressed') AND itemised them separately with their rulings, so the reconciliation is "
  "explicit: 84 = 77 with an edit + 7 exempt by ruling. All required keys are present and unrenamed."),
 ("ONE REBASED EXPECTED_BEFORE - the single real mechanism hazard in this lane. P01-001 needs both an A4 append and "
  "an A6 repair of an EXISTING refs entry (the 1:8 K/Q gloss), and both target boundary_evidence_refs in different "
  "sweeps. I followed the documented order in brief section 10 - A4 installs at step 4, A6 delimiting at step 5 - so "
  "the a6 set-edit's expected_before is the ORIGINAL list plus that row's one a4 entry, and its value is the "
  "repaired list plus the same entry. If the orchestrator pools these two sweeps in the other order, or applies the "
  "a6 edit without the a4 append, that expected_before will not match and the batch will be refused. The fallback "
  "form is in the limit field. This is the only edit in the lane whose expected_before is not the raw lane-file "
  "value, and it is the only place two sweeps touch one field."),
 ("l01#24 MAY BE REDUNDANT, and I installed it anyway. Under DEF-A4-ARGUED clause 3 a range is mirrored when an "
  "entry covers either endpoint, so the single-verse entries I install for Ezek.3.10 (l01#23) and Ezek.3.11 "
  "(l01#22) already mirror the range Ezek.3.10-Ezek.3.11. The same holds for l01#43 (range Ezek.4.1-Ezek.4.17) "
  "against l01#41 (Ezek.4.1) in P01-007. Both were ordered as separate items and each carries a distinct claim that "
  "deserves its own token, so I installed all of them rather than silently dropping any; flagging the overlap "
  "instead of resolving it."),
 ("WORKLIST METADATA ODDITY - repeats_in_row is 0 on 14 A4 items whose citation is demonstrably present in the "
  "named field (for example l01#14 raw '3:4', l01#23 raw '3:10', l01#25 raw '3:12', l01#31 raw '3:16'). The bare "
  "C:V forms appear to count differently from the witness-prefixed ones. It did not change any token I chose - I "
  "read every verse's role off the row's prose - but the field should not be trusted as an occurrence count."),
 ("l01#01's field is 'refs', which is not one of the field names in the deliverable schema. I mapped it to "
  "boundary_evidence_refs, which is where the run actually lives (inside the Ezek.1.8 K/Q entry)."),
 ("A6-b JUDGEMENT BOUNDARY. I ruled INSTALL rather than EXEMPT on three items where the argument could go either "
  "way - l01#09 ('you, son of man, hear': the title plus an imperative, so not 'nothing but' a title rendering), "
  "l01#18 ('moreover he said to me': 'he said to me' is a strategy sweep at line 108 but has NO verse list in "
  "inventory v2, so under A12-b it is not an inventory class and is not one of A6-b's five named counted-device "
  "families), and l01#29 / l01#40 ('at the end of seven days': neither a device rendering nor an addressee title). "
  "I chose the install side deliberately: exempting on a class that is not a counted device is the failure "
  "direction that fails closed toward 'not a defect'."),
 ("MT 33:20's sof pasuq is UNAVAILABLE at verse granularity per brief section 12. It is outside my span, no row of "
  "mine is scored on it, and I neither resolved nor asserted it."),
 ("INTRA-VERSE MARK POSITION is UNAVAILABLE from the pinned inputs, as pmarks's own paseq_note states (the extract "
  "drops segs) and as strategy line 239 states for the pe at MT 3:16. I opened both files; neither carries it. I "
  "made no intra-verse position claim, and the rows' existing disclaimers to that effect are left standing."),
]

out["changes_made_or_no_change"] = (
 "63 edits across all 10 rows, discharging 77 of 84 items; the other 7 are A6-b EXEMPT rulings that correctly "
 "produce no edit. By sweep: 3 grounds, 48 a4, 12 a6. NO SEAM MOVED - no edit touches span, osis_start, osis_end, "
 "decision_id, any writer-identity field, or confidence (my worklist contains no confidence item, and no row's "
 "confidence is raised unasked). "
 "GROUNDS (3 field edits, 2 items): P01-008's strongest_rejected_alternative now names and weighs the 4:3 samekh "
 "and the verse-final sign colophon under A9 and rewords the test, which had omitted 4:3 - the very verse the mark "
 "follows - from the bare we-attah list; P01-009's device_notes retracts a false ground ('none coincides with a "
 "formula onset') and states what is actually there, three of five interior marks standing immediately before a "
 "verse-initial messenger formula, with CUT-RULE supplied as the correct ground; P01-009's "
 "strongest_rejected_alternative adds the A16 weighing of the 5:4/5:5 rival, naming the PE and the formula, testing "
 "both CUT-RULE limbs and holding the seam on stated grounds. Both rivals are ones strategy section 7 already holds. "
 "A4 (48 append_ref edits): one entry per citation, ranges as range entries, each carrying exactly one of the "
 "eleven ROLE tokens - WARRANT-close 11, DISCLOSURE-mark 10, ANCHOR 9, WARRANT-rival 8, WARRANT-onset 5, "
 "DISCLOSURE-device 4, WARRANT-absence-over-range 1 - with all 48 annotations distinct and 6 words or fewer. No "
 "existing entry was re-tokenised. "
 "A6 (12 set edits, 27 items): the convention installed as double curly quotes plus an in-field web: reference; two "
 "glosses were corrected to the WEB's exact wording first, because delimiting a paraphrase as web: would have "
 "manufactured a false quotation. "
 "NO CHANGE, deliberately: P01-001's transport-sweep sentence and P01-005's transport wording, both escalated "
 "untouched because they turn on the HELD 13-verse transport question; and every pre-existing census figure in the "
 "fields I rewrote, which I sourced but did not alter."
)

out["e19_selfreport"] = (
 "E-19 exact paths only, and I believe I held it. Every read was by exact path: my launch brief, the "
 "AUTHOR_WAVE_BRIEF, my lane file, and the nine inputs in the launch table. No directory listing, no glob, no "
 "recursive search, no directory existence test. The two greps I ran were CONTENT searches inside two named files "
 "already on my read list (book_strategy_Ezek.md, ezek_device_inventory.v2.json) to source figures the rows assert, "
 "not path discovery. I read no other lane's rows or output, nothing under reviews/, no peer packet, no fix-up "
 "order, no cure claim, no transcript, and no ruling beyond those quoted in my brief. I wrote only inside one "
 "uniquely-named private scratch subdirectory, ezek_l01_work_7b3e, created for this attempt and never used a bare "
 "filename at scratch root; all eight helper scripts and both outputs are inside it. Nothing was written under "
 "C:\\wt\\logos-t423-m8-fable - the repository was read-only to me. No git, no receipts, no registry, no validator "
 "run, no row mutation. E-29: I wrote a deliverable at stage 0 before reading the inputs and rewrote it at each "
 "stage; the digests below were taken AFTER the final write of both files."
)

out["limit"] = (
 "Four limits, stated rather than papered over. (1) I judged A6-b at the row for 12 AUTHOR_JUDGEMENT items and "
 "those judgements are mine, not measurements - 7 exempt, 5 installed; the run existence behind each is MEASURED, "
 "the duty is judgement. (2) I did not re-derive the 23-verse we-attah family, the 12-verse rebellious-house sweep "
 "or the ordinal positions 'third/fifth/sixth of six'; those are strategy sweep figures with no verse list, they "
 "are not my items, I preserved them byte-identically and labelled them REPORTED rather than quietly promoting "
 "them. The ordinals in particular are NOT sourced to a verse list in either pinned input - I could not check them "
 "and I did not touch them. (3) The one rebased expected_before on P01-001. Its FALLBACK, if your sweeps do not run "
 "A4 before A6: apply the a6 set-edit with expected_before = the raw lane-file boundary_evidence_refs list and "
 "value = that same list with entry index 3 rewritten to 'oshb:Ezek.1.8 (K/Q, checked before quoting: ketiv "
 "widw / qere wydy, [double-curly]the hands of a man[double-curly] (web:Ezek.1.8))' - i.e. drop the trailing a4 "
 "entry from both sides of that one edit. The Hebrew in that entry is unchanged from the lane file either way; "
 "only the delimiter and the added web: reference differ. (4) I could not act on three real defects I found because "
 "no worklist item covers them - the undisclosed samekh after MT 4:15, the undisclosed year-word non-datelines at "
 "MT 4:5 and 4:6, and P01-001's transport-sweep sentence. They are in escalations, not silently absorbed."
)

json.dump(out, open(W + r'\ezek_author_l01_deliverable.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('deliverable written: %d edits, %d discharged, %d not discharged, %d escalations'
      % (len(out['edits']), len(out['items_discharged']), len(out['items_NOT_discharged']),
         len(out['escalations'])))
print('keys:', list(out.keys()))
