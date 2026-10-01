#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assembles ezek_author_l03_deliverable.json and ezek_author_l03_final_message.json."""
import json, re, sys, io, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OUT = (r"C:\Users\lowel\AppData\Local\Temp\claude"
       r"\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
       r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l03_work_4c9a")
LANE = (r"C:\Users\lowel\AppData\Local\Temp\claude"
        r"\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
        r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_03_worklist.json")
D = r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek"

EDITS = json.load(open(OUT + r"\_edits_stage.json", encoding='utf-8'))
lane = json.load(open(LANE, encoding='utf-8'))
ITEMS = lane['your_worklist_items']

def iid(n):
    it = ITEMS[n]
    disc = (it.get('citation') or it.get('run') or it.get('new_value')
            or it.get('action', '')[:40])
    return f"idx{n:02d}:{it['row_id']}:{it['cls']}:{disc}"

covered = sorted({int(re.match(r'idx(\d+):', i).group(1))
                  for e in EDITS for i in e['worklist_item_ids']})
missing = [n for n in range(len(ITEMS)) if n not in covered]
assert missing == [26], missing

SOURCES = [
 {"path": D + r"\AUTHOR_WAVE_BRIEF.v1.md",
  "sha256": "ccb7026f908345d3f9800671e621cd8fbdedc3429d41c22dc244b03e0474bd79",
  "read": "in full; digest verified before reading. CUT-RULE, CONF-CAL with the #e14 Q2 refinement, "
          "DEF-A4-ARGUED and the eleven ROLE tokens, A6-b, C2-amended, the A9/A16 weighing duty, "
          "the rotation rule, the ch 20/21 dual-writing rule, the OW-18 tiers, section 12 on v2."},
 {"path": LANE,
  "sha256": "ee1d77578c6e670022bb4dd0fce5efc14f3afc9ace8e72b0b56ac0c4a13e6bdb",
  "read": "in full; digest verified. All 28 rows' complete current bytes and all 79 worklist items. "
          "Every expected_before in this deliverable is copied from your_rows by script, never retyped."},
 {"path": D + r"\pmarks_Ezek.json",
  "sha256": "25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315",
  "read": "marks, paseq, kq and notes_other by exact key for every verse in and at the seams of my 28 "
          "rows. FOUND, and recorded because the brief names a reader who got this wrong: marks is a "
          "dict verse -> LIST of mark names; kq is a dict verse -> LIST of K-Q pair strings; paseq is "
          "a flat LIST repeated per occurrence; notes_other is a dict verse -> list of note dicts."},
 {"path": D + r"\ezek_device_inventory.v2.json",
  "sha256": "356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f",
  "read": "v2 only. Every list-membership claim I wrote was checked against this file's verses_mt "
          "lists: strict word-event 39, son-of-man 93, long messenger 122, messenger-variant census "
          "with MT 21:14, long utterance 81, short utterance 4, emphatic spoken 14, strict recognition "
          "28, recognition_formula_2s 5, 2mp 21, recognition_family_64 including its "
          "subject_intervening_members, and verses_per_chapter_mt for the seam arithmetic."},
 {"path": D + r"\ezek_device_inventory.json",
  "sha256": "0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142",
  "read": "NOT read. Superseded for counts and list membership; no figure in this deliverable comes "
          "from v1. Recorded as a deliberate non-read, not as an omission."},
 {"path": D + r"\book_strategy_Ezek.md",
  "sha256": "4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3",
  "read": "the heading index, then §7 in full (lines 360-449) and §8 in full (lines 451-495). §7 for "
          "the region direction CONF-CAL makes the tie-breaker; §8 for the register and hygiene rules "
          "that bind row prose, including the WEB-quotation marker, the programmatic-splice rule for "
          "pointed Hebrew, the dual-writing rule, the digit-bearing sweep rule for universal claims, "
          "and the bar on repair narration and positional row references."},
 {"path": D + r"\tools\verse_map_web.json",
  "sha256": "bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98",
  "read": "every WEB verse behind an A6 item, by exact key; each entry's `mt` back-reference used to "
          "verify every dual pair I wrote; and a full-book scan of all 1273 WEB verses to locate the "
          "runs. Entries carry text, para_before, continuation_paragraphs, poetry_lines and mt. "
          "Every WEB quotation I installed is spliced from here by word index, never hand-typed."},
 {"path": D + r"\tools\verse_map_oshb.json",
  "sha256": "408b7ee74564aef902c5fc539d6577f7708fa9aa839c993ce6281d86dc3a7901",
  "read": "the MT text of the seam and rival verses (MT 16:50, 16:51, 16:44-16:47, 17:18, 17:19, "
          "21:5, 21:6, 21:14, 21:17, 21:18, 21:19, 22:17, 22:18, 22:19) by exact key. The one pointed "
          "Hebrew string I introduced is spliced from here by word index."},
 {"path": D + r"\web_mt_offset_map.json",
  "sha256": "b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887",
  "read": "measured and reported, since the launch pinned no digest for it. Read for the two stated "
          "range identities (MT 21:1-5 = WEB 20:45-49; MT 21:6-37 = WEB 21:1-32), its identity-outside-"
          "the-zone rule and its Tier-0 disclosure clause. I applied the stated ranges and then "
          "verified every pair against the WEB map's own back-reference; no face was crossed by "
          "arithmetic."},
 {"path": D + r"\verse_inventory.json",
  "sha256": "7314690191ec380b25578ca33d4745f4e60196b9f0e1dda4a1bcc9286c19cf54",
  "read": "digest verified; not otherwise opened. The numbering_face it declares (WEB) is carried in "
          "the brief and in v2's numbering_face block, which I did read, so I had no need of it."},
 {"path": D + r"\Ezek_oshb.txt",
  "sha256": "337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e",
  "read": "digest verified; not opened. The verse-keyed MT map at its own pinned digest is what the "
          "tools read and is the form I needed. Declared so the non-read is visible."},
]

NOT_DISCHARGED = [
 {"item": iid(26),
  "why_not": "MEASURED, not assumed: I scanned every string field and every list element of P03-014 "
             "for this run's normalised word sequence and found 0 hits, so the run the peer named is "
             "absent from the row's prose and there is no text to delimit. The WEB does carry it at "
             "web:Ezek.18.2, which is inside the row's span, so the peer's sighting is sound; what is "
             "absent is any reproduction of it in this row. A6's duty attaches to a run the row's "
             "prose carries, so no install is owed and no edit exists to make. I did NOT manufacture "
             "the run in order to delimit it. Note the contrast with the two sibling union items, "
             "idx48 and idx53, which also scanned to 0 hits but for different reasons and ARE "
             "discharged: idx53 is the same run as idx48's sibling install in a different apostrophe "
             "spelling ('isn t' tokenises as two words against 'isn't' as one), and idx48's run does "
             "occur in the WEB verse the row already quotes, so extending that one install to the "
             "clause boundary covers it honestly."}
]

ESCALATIONS = [
 {"row": "P04-001",
  "what": "The rejected-alternative field states that oshb:Ezek.20.4 'carries no onset device of its "
          "own'. MEASURED against the pinned v2 inventory, MT 20:4 is a member of the 93-verse "
          "son_of_man_address class, which that file gives the role 'onset'. The denial is therefore "
          "false as written. The row's conclusion may still stand, because the son-of-man address "
          "alone is not one of the two limbs that license a sub-onset, but the stated ground is not.",
  "why_i_did_not_write_it": "No GROUNDS order exists for P04-001; its four items are reference "
          "installs. Rewriting an unordered grounds field would collide with whatever sweep owns it. "
          "I recorded the measured fact in the free text of the reference entry I was ordered to "
          "install and escalate the field itself. This is the same denial-shape defect the P04-008 "
          "order names, in a row with no order."},
 {"row": "P04-001",
  "what": "Two argued citations inside the A4 window look unmirrored and are in no worklist item. The "
          "rationale reads 'the recurring for-my-name's-sake clauses at oshb:Ezek.20.9, 20.14 and "
          "20.22'. Under DEF-A4-ARGUED clause 2 a comma/'and' list is one citation per member, and the "
          "window for this row is [Ezek.19.14, Ezek.20.27], so 20:14 and 20:22 are both in-window. The "
          "reference list carries entries for 20:1, 20:2, 20:26 and 20:27 only, so neither is mirrored. "
          "The likely cause is extraction: only the prefixed first member matches an Ezek.C.V token, "
          "while the two bare continuation members are written with dots rather than a colon.",
  "why_i_did_not_write_it": "The brief forbids inventing worklist items. I report the gap upward "
          "rather than installing entries no item ordered, and rather than staying silent, which is "
          "the failure direction the brief names."},
 {"row": "P03-007",
  "what": "The boundary_rationale calls the samekh close 'the cleanest mark-corroborated close "
          "available inside MT 16'. That is an exclusivity claim over a 63-verse chapter carrying no "
          "adjacent digit-bearing sweep citation naming the swept object and unit, which §8 requires "
          "and says is never tier-dampened.",
  "why_i_did_not_write_it": "My order for this row is a C4 rewrite of the rejected-alternative field "
          "plus the ruled confidence move. The exclusivity claim sits in a different field with no "
          "order on it; supplying a sweep figure would mean asserting a chapter-wide count no pinned "
          "input gives me."},
 {"row": "P05-001",
  "what": "Two observations, neither ordered. First, the boundary_rationale closes with 'Both sides of "
          "the next seam (22:16/22:17) are weighed at the following unit's onset (22:17)', a positional "
          "reference to another row, which §8 bars in row prose; the same field also refers to 'the "
          "prior unit'. Second, the reference list labels the 22:16 close "
          "'recognition_formula_2ms/2fs variant (5-list)'. The count is right - MT 22:16 is one of the "
          "5 verses in that class, MEASURED - but v2 relabels the class recognition_formula_2s "
          "precisely because the old key reads as a morphological claim the file withdraws, keeping "
          "2ms only as a census alias, and v2 measures MT 22:16's own pointing as feminine.",
  "why_i_did_not_write_it": "P05-001's six items are all reference installs; no field rewrite is "
          "ordered. The alias is explicitly retained by v2, so the label is not a defect on its face, "
          "which is exactly why it should be a decision rather than my silent edit."},
 {"row": "P04-011",
  "what": "A five-word WEB run that no worklist item names. The boundary_rationale contains the "
          "hyphenated device label 'the and-you-son-of-man-prophesy sub-onset', whose words reproduce "
          "the WEB's 'You, son of man, prophesy' at web:Ezek.21.28 = oshb:Ezek.21.33, an in-span verse. "
          "My own scan surfaces it; the sweep that produced my items evidently did not, which is "
          "consistent with a tokeniser that keeps a hyphenated compound whole while mine splits it. I "
          "judged it EXEMPT under A6-b: the run is nothing but the WEB's rendering of the ve'attah "
          "addressee-title-plus-command that the label names, and the row names the device as a "
          "sub-onset, so it is a gloss of a census object rather than a quotation.",
  "why_i_did_not_write_it": "I did not silently delimit it, because the judgement is mine and A6-b "
          "turns on it; the run is reported so the spot wave can test the judgement instead of "
          "discovering the run. Three sibling labels in my lane - P04-007's and P04-009's "
          "'and-you-son-of-man sub-onset' and P04-011's own earlier mention - fall to four words and "
          "under the threshold, so this is the single instance in 28 rows."},
]

DELIV = {
 "lane": "ezek_author_l03",
 "attempt_id": "ezek_author_l03_a1",
 "execution_id": "ezek_author_l03_a1#e1",
 "stage": "FINAL",
 "sources": SOURCES,
 "edits": EDITS,
 "items_discharged": [iid(n) for n in covered],
 "items_NOT_discharged": NOT_DISCHARGED,
 "escalations": ESCALATIONS,
 "changes_made_or_no_change":
   "71 edits across all 28 rows, discharging 78 of 79 worklist items; 1 item is not discharged, with "
   "a measured reason. By sweep: 4 confidence moves (P03-007 high->medium_low, P03-012 high->medium, "
   "P04-003 high->medium_low, P04-008 high->medium_low), all applied as ruled and none chosen; 5 "
   "grounds rewrites, one per GROUNDS item (P03-007 C4, P03-012 A16, P04-006 MARKS-3D, P04-008 "
   "A9/A16, P05-002 false ground), the P04-006 order additionally carrying one reference install so "
   "its own new prose citation is mirrored; 18 set edits carrying the 23 A6 items and 2 of the 3 "
   "A6_UNION items; 45 append_ref installs across 22 rows, 44 of them the A4 items, each "
   "one entry per citation, each range citation taking a single range entry, each carrying exactly "
   "one of the eleven ROLE tokens. NO SEAM WAS MOVED and no edit touches span, osis_start, osis_end, "
   "decision_id or any writer-identity field - a script asserts this over every edit. Four of the A6 "
   "items turned out to be not merely undelimited runs but hand glosses that reproduced a WEB verse "
   "OTHER than the one the row argues (P03-013's 'and I will do it', P03-017's 'turn from his way and "
   "live', P03-018's 'turns from his righteousness and', P04-011's 'against the children of Ammon'); "
   "in each case I quoted the row's own WEB verse exactly, or reworded the row's own label where no "
   "quotation of this span was available, rather than delimiting a run as though it came from a verse "
   "the row does not cite. P04-003 received its ruled confidence move and no prose change, because "
   "none was ordered.",
 "verification_evidence": [
  "All eight digests the launch pinned matched before reading, and the ninth file "
  "(web_mt_offset_map.json) was measured and reported at b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887.",
  "expected_before is not retyped anywhere. A script copies each value out of the lane file's "
  "your_rows and then asserts, after all edits are built, that every edit's expected_before still "
  "equals that live value byte for byte. Every prose change is an exact-fragment substitution that "
  "the script requires to match EXACTLY ONCE, so a mis-transcribed fragment fails the build instead "
  "of shipping. Apostrophes in match fragments are given as a character class covering straight and "
  "both curly forms, so no edit can fail on quote-style alone.",
  "Every append_ref shares one expected_before with its siblings on the same row - 45 appends "
  "across 22 rows. The script asserts that every append_ref on a row carries the identical list, "
  "that appends only ever target "
  "boundary_evidence_refs, and that no row has both a set and appends on that field. P03-013 is the "
  "one row with a set on the reference list and it carries no A4 item.",
  "One edit per (row, field) for every non-append op, asserted by the script. P03-017 carries three "
  "A6 items in one field and P03-020 four; each is ONE set edit whose value is the complete final "
  "text, with every item id listed.",
  "Marks, MEASURED by exact key from the pinned marks layer, with the layer's own direction "
  "convention (a mark is recorded ON the verse it FOLLOWS) applied and never inverted: SAMEKH on MT "
  "16:50, 16:58, 16:63, 17:8, 17:18, 17:21, 18:4, 18:20, 18:23, 18:26, 20:1, 20:26, 21:10, 21:30 "
  "and 22:18 (15 verses); PE on MT 16:35, 17:10, 17:24, 18:32, 19:9, 19:14, 20:44, 21:5, 21:12, "
  "21:18, 21:22, 21:28, 21:29, 21:32, 21:37, 22:16, 22:22 and 22:31 (18 verses). No mark at all on "
  "MT 16:23, 18:9, 20:29 or 20:38, which bears on three of my rows, whose close is argued at a "
  "verse the paragraph layer does not mark.",
  "The P05-002 false ground, stated as a finding rather than a verdict. The field denied that any "
  "formula device stands at the rival seam. What I FOUND: the samekh is recorded on MT 22:18, so the "
  "seam it corroborates is 22:18/22:19, one verse later than the field places it; MT 22:18 is a "
  "member of the 93-verse son_of_man_address class; MT 22:19 is a member of the 122-verse "
  "thus_says_the_lord_yhwh class. So the rival has evidence on BOTH faces and had to be weighed, not "
  "denied. It is still unlicensed, because MT 22:18's closing clause is the silver-dross statement "
  "and not a close-role formula, so the second limb is unmet, and the brief states that a mark alone "
  "never satisfies it. The row's high grade is untouched and stays consistent with CONF-CAL, which "
  "makes a paragraph-grade rival never fatal.",
  "The P04-008 denial, stated as a finding. The field held the unit together on the ground that the "
  "address at MT 21:19 'brings no fresh word-event or messenger formula with it'. What I FOUND: MT "
  "21:18 is a member of the 81-verse utterance class AND its last two tokens are that signature, so "
  "it ends VERSE-FINAL on a close-role formula and the second limb IS met at that seam - the denial "
  "tests the wrong thing. The ground that actually holds is the brief's own clause: a renewed command "
  "to the same addressee after a verse-final utterance signature is a paragraph, not an onset. "
  "Separately, the field claimed a WEB paragraph mark at web:Ezek.21.12; MEASURED on the staged WEB "
  "map that verse opens no paragraph and carries no continuation paragraph, so that claim does not "
  "reproduce and the rewrite states what is there.",
  "The P04-008 class blend. The field described web:Ezek.21.9 = oshb:Ezek.21.14 as a repetition of "
  "the same son-of-man address. MEASURED against v2, MT 21:14 is in the son-of-man class AND in the "
  "messenger_formula_variant_census under short_form_adonai_alone, where v2 records it as the fourth "
  "short-form VERSE and the THIRD distinct SHAPE. The rewrite names both and keeps the two classes "
  "apart, per the bar on blended sweeps.",
  "The P04-006 MARKS-3D direction, MEASURED: PE is recorded on MT 21:5, so the mark follows MT 21:5 "
  "and falls at the MT 21:5 / MT 21:6 seam, which is this row's ONSET seam - an onset-direction "
  "disclosure, not an interior or close one. Written dual as web:Ezek.20.49 = oshb:Ezek.21.5, and the "
  "same citation installed in the reference list so the new prose citation is mirrored rather than "
  "left as a fresh unmirrored one.",
  "Ketiv/Qere read as the LIST it is, which the brief names as a trap that already cost this session "
  "twice. FOUND at my seam and interior verses, as counts of K-Q pair strings in the list keyed to "
  "each verse: MT 16:20 one, 16:22 one, 16:25 one, 16:31 two, 16:43 two, 16:47 one, 16:51 two, 16:53 "
  "three, 16:59 one, 17:21 one, 18:20 one, 18:21 one, 18:24 one, 18:28 one, 21:28 one, 22:18 one. I "
  "installed a DISCLOSURE-kq entry only for MT 16:47, which is the one my worklist names.",
  "Paseq read as the flat occurrence LIST it is, count-only. FOUND 15 verses in my lane's range, "
  "one occurrence each, so no verse repeats: MT 16:43, "
  "16:52, 17:3, 17:9, 17:24, 18:20, 20:1, 20:30, 20:32, 20:39, 21:3, 21:20, 21:24, 21:27, 22:11. No "
  "intra-verse position is asserted anywhere in my edits, and each DISCLOSURE-paseq free text says so "
  "in a different formulation.",
  "Every dual pair I wrote is verified, not computed. The script extracts each 'web:X = oshb:Y' pair "
  "from every value it emits and checks Y against the WEB map's own mt back-reference for X; a "
  "mismatch is a build failure. All 17 distinct pairs my output emits passed, including both range "
  "endpoints of web:Ezek.21.9-Ezek.21.11 = oshb:Ezek.21.14-Ezek.21.16.",
  "No hand-typed WEB text and no hand-typed pointed Hebrew. Every quotation I installed is spliced "
  "by word index out of the staged verse maps at their pinned digests, and the splice helper flags a "
  "footnote marker if one falls inside a span - which is why the web:Ezek.20.29 install stops at the "
  "clause boundary before the marker rather than quoting it or silently dropping it.",
  "A6 runs located mechanically, not by eye. For all 26 A6 and A6_UNION items I scanned every string "
  "field and list element of the row for the run's normalised word sequence and recorded WHERE it was "
  "found: 23 items hit exactly one field, one item hit two fields (P03-013, prose and a reference "
  "entry, which is why that row has two edits), and three hit none. I then re-derived each far-side "
  "run's WEB locations myself over all 1273 verses: 'and I will do it' at exactly web:Ezek.24.14 and "
  "web:Ezek.36.36; 'turns from his righteousness and' at exactly web:Ezek.3.20 and web:Ezek.33.18; "
  "'against the children of Ammon' at exactly web:Ezek.25.10. These agree with the figures the "
  "worklist handed me; the agreement is recorded and does NOT upgrade anything, since corroboration "
  "never lifts a tier.",
  "A residual-run self-check over every new prose value: after building, the script re-scans each "
  "emitted value for any run of five or more consecutive words matching any WEB verse that is NOT "
  "inside curly double quotes. Exactly one survives across all 71 edits, the hyphenated device label "
  "in P04-011, and it is escalated with my A6-b judgement rather than left to be found.",
  "Rotation, MEASURED over my own output: WARRANT-rival 15 uses / 15 distinct formulations, "
  "DISCLOSURE-mark 7/7, ANCHOR 6/6, DISCLOSURE-paseq 5/5, DISCLOSURE-device 5/5, WARRANT-close 5/5, "
  "WARRANT-onset 1/1, DISCLOSURE-kq 1/1. Every free text is at most 6 words, asserted by the script, "
  "so no 7-gram can arise from an annotation.",
  "A 7-gram self-duplication scan inside every new prose value. What survives is only the mandated "
  "dual-reference token itself (two repeats in P04-005, both pre-existing in the row before my edit, "
  "and two in P04-008's retained text). I removed the three duplicate dual refs my own drafts had "
  "introduced. The dual-writing rule requires the pair verbatim at every reference, so a repeated "
  "coordinate string is a mandated form rather than a converging sentence template.",
  "The confidence scale was checked before applying: all four ruled values (medium_low, medium, "
  "medium_low, medium_low) are on the corpus's four-value scale, and the script refuses anything off "
  "it, so no medium_high could pass. No row's confidence was raised: three of the four are lowerings "
  "from high and the fourth (P03-012) is high -> medium.",
  "The two lowerings I could not derive from seam evidence alone were reconciled before being "
  "applied, not merely obeyed. P04-003's and P04-008's seams each carry a licensed near-face signal "
  "and a real far-face signal, which CONF-CAL's own limbs would grade higher. §7 names the ch 20/21 "
  "numbering zone as an expected low-confidence region and directs medium_low/low there, and names "
  "the 20:30 seam explicitly; CONF-CAL makes §7's direction the tie-breaker where it names the "
  "region. So the ruled grades are explicable and I applied them. P03-007's medium_low and "
  "P03-012's medium are likewise consistent with §7 naming the 16:44 cut and the "
  "17:1-10 / 17:11-21 / 17:22-24 tripartition as held questions.",
  "A4 mirroring checked before installing, so no entry duplicates cover already present. P03-012's "
  "A16 rewrite names the range 17:11-21; under DEF-A4-ARGUED clause 3 a range is mirrored when an "
  "entry covers either endpoint, and the row's existing oshb:Ezek.17.21 entry does, so I installed "
  "NO entry for it rather than over-installing. Conversely the P04-006 disclosure the order requires "
  "puts a new citation at the onset seam, so there I did install one.",
  "No transport-class membership claim appears anywhere in my output. None of the 13 verses whose "
  "membership is routed to the controlling agent falls inside Ezek 16-22, so no row of mine needed "
  "one, and I invented no items for the held peer findings.",
  "Existing reference entries were not re-tokenised. The eleven-token vocabulary is applied to my "
  "installs only. The one existing entry I altered is P03-013's, and the change is the removal of an "
  "English WEB run under an A6 order, not the addition of a role token."
 ],
 "unresolved_uncertainty": [
  "P03-012's weighing turns on a limb reading I could not settle from the pinned inputs. I found the "
  "second limb unmet at MT 17:18/17:19, because MT 17:18 ends on a content clause and not a "
  "close-role formula, and I found no addressee replacement for the 'rebellious house' named at MT "
  "17:12, so I wrote the merge as a LIVE rival held on stated grounds - which is what the ruled "
  "medium records. If the controlling agent reads the turn from third-person narration to "
  "first-person oath speech as an addressee change, the first limb would be met, the row's onset "
  "would be a licensed sub-onset, and the weighing would need to say so. I did not decide that.",
  "The same question, in the same shape, at P05-002. I wrote that the indicted party does not change "
  "across MT 22:18/22:19, because the house of Israel named at 22:18 is the party gathered at 22:19. "
  "If the first limb is instead read on the grammatical person of the speech - a singular command to "
  "the prophet at 22:18 against plural address in the quoted speech at 22:19 - the rival would be "
  "licensed, the weighing would change, and the row's untouched high grade would deserve a second "
  "look. That grade was not in my worklist and I did not change it.",
  "P04-011's literature_type_guess. I removed a five-word run that reproduced web:Ezek.25.10, a "
  "verse outside this row's span, by rewording the row's own label rather than by delimiting a "
  "quotation of a verse the row does not argue. That is a judgement about which of two true things "
  "to write; a reviewer who prefers the far-side citation would install it instead. I state the "
  "choice rather than hide it.",
  "The A4 role token for oshb:Ezek.20.26 in P04-002 and for oshb:Ezek.18.4 in P03-015 sits on a real "
  "boundary between two honest tokens. Both verses carry a closed-section mark on the far face of a "
  "seam the row's onset is argued from. I used DISCLOSURE-mark where the citation's assertion is "
  "purely about the mark (P04-002) and WARRANT-onset where the field argues the onset FROM the far "
  "face (P03-015). If the spot wave wants one rule for both, this is where it diverges.",
  "Whether P04-003 should have carried a prose change as well as its confidence move is not "
  "something I can see. Its single item is the grade; its prose reads as a two-faced HIGH while §7 "
  "directs the region low. I applied the grade and left the prose, because an unordered rewrite is "
  "the collision risk the sweep order exists to prevent."
 ],
 "e19_selfreport":
   "Exact paths only; no directory listing, no glob, no recursive search, and no directory tested for "
   "existence at any point. Files opened, all by exact absolute path, all digest-verified first: the "
   "AUTHOR_WAVE_BRIEF, my lane file, pmarks_Ezek.json, ezek_device_inventory.v2.json, "
   "book_strategy_Ezek.md (heading index then two exact line ranges), tools/verse_map_web.json, "
   "tools/verse_map_oshb.json, web_mt_offset_map.json. Digest-verified and deliberately NOT opened, "
   "declared so the non-read is visible rather than silent: Ezek_oshb.txt, verse_inventory.json, and "
   "ezek_device_inventory.json (v1, superseded for counts). I read no other lane's rows or output, no "
   "reviews directory, no peer packet, no fix-up order, no transcript, and no ruling beyond what my "
   "brief quotes. Nothing was written anywhere under C:\\wt\\logos-t423-m8-fable; all four of my files "
   "live in one uniquely-named private subdirectory, ezek_l03_work_4c9a, and no bare filename was "
   "reused at scratch root. No git, no receipts, no registry, no validator run, no row mutation. The "
   "deliverable was written at my first stage and rewritten at each of S1, S2 and FINAL, and both "
   "output digests are taken after the final write.",
 "limit":
   "Five things this lane does not settle. (1) The two limb-reading questions above, at P03-012 and "
   "P05-002, are genuinely undecided by the pinned inputs and are the load-bearing uncertainty in two "
   "of my five grounds rewrites. (2) I could not repair the four unordered defects I escalate - the "
   "false denial at P04-001, the two unmirrored comma-list citations in the same row, the unswept "
   "exclusivity claim at P03-007, and the positional references at P05-001 - because no order covers "
   "those fields and inventing items is barred; if the intent was that an author fixes what it finds, "
   "that intent did not reach me through the worklist. (3) My A6-b judgement on P04-011's hyphenated "
   "device label is a judgement, not a measurement, and my tokeniser disagreeing with the sweep's on "
   "hyphens means there may be sibling cases in other lanes that neither sweep nor author has seen. "
   "(4) Every figure I cite for a device class is EXTRACTED from v2's verses_mt lists by membership "
   "test, not re-derived from the consonantal bytes; I measured membership, not the counts "
   "themselves, and I have labelled them accordingly. (5) I ran no validator and no ngram7 gate; my "
   "duplicate and residual-run checks are my own scripts over my own output, which is weaker than the "
   "gate and is not a substitute for it."
}

DP = OUT + r"\ezek_author_l03_deliverable.json"
FP = OUT + r"\ezek_author_l03_final_message.json"

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 16), b''):
            h.update(blk)
    return h.hexdigest()

# FINAL write of the deliverable
json.dump(DELIV, open(DP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
d_sha = sha(DP)

# the final message is the same JSON plus the digest block
FINAL = dict(DELIV)
FINAL["output_digests"] = {
 "ezek_author_l03_deliverable.json": {
   "path": DP, "sha256": d_sha,
   "tier": "MEASURED after the deliverable's FINAL write, by streaming sha256 over the file bytes"},
 "ezek_author_l03_final_message.json": {
   "path": FP,
   "sha256": "reported in the returned message, not embedded here: a file cannot carry its own "
             "digest. It is measured after this file's final write and is the value returned to the "
             "orchestrator.",
   "tier": "MEASURED after this file's final write; carried in the returned message"}
}
json.dump(FINAL, open(FP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
f_sha = sha(FP)

print("edits", len(EDITS),
      "| discharged", len(DELIV['items_discharged']),
      "| not_discharged", len(DELIV['items_NOT_discharged']),
      "| escalations", len(DELIV['escalations']))
print("deliverable   sha256:", d_sha)
print("final_message sha256:", f_sha)
