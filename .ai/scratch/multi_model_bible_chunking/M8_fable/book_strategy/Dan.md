# Daniel book strategy (Phase 0, Lane S)

Attempt `dan_strategy_a1`, execution `dan_strategy_a1#e3`. Written by claude-opus-5-5 in the controlling-agent role as a
recorded `grader_fallback` (OW-25). That is a recorded downgrade from Fable, not an equivalence. This is a planning
record. It writes no rows and settles no grade or class question: those go to Fable at the campaign's end (OW-28).
Tiers follow OW-18: MEASURED names the script in this lane's OUT; EXTRACTED names the pinned file read.
Ezekiel's strategy was used as a model of form only; no figure of Ezekiel's appears here as Daniel's (E-65).

This is the reconciled version. The orchestrator applied check lane C1's and C2's exact corrections to candidate `.a1`
(which stays unchanged under `strategy_candidate/`) and ruled on their four judgements, on claude-opus-5-5 as a
recorded `grader_fallback` (OW-25). Each change is listed in "What changed from a1" at the end, with the lane item it
executes.

## §1 Objective and shape

Objective: give every Daniel writer, checker and reviewer one plan: 10 parents, 6 writer parts, a closed
unit_type vocabulary, a device matrix, numbering and language rules, a marker policy, the expected low-confidence
regions, hygiene rules, self-checks and a lens count of 3.

Two macro-structures cross in Daniel. Both were measured against the bytes.

Shape adopted: the GENRE frame for tiling. Court tales run 1:1-`web:Dan.6.28`=`oshb:Dan.6.29` (parents PA-PF, 196 verses) and dated vision
reports run 7:1-12:13 (parents PG-PJ, 161 verses) [MEASURED gen_strategy.py over verse_inventory.json]. The language
runs are carried as a crossing overlay on every row (§3). They are never a tiling.

Evidence for the genre frame:
- Person. The tales narrate Daniel in the third person: 48 WEB verses in 1:1-`web:Dan.6.28`=`oshb:Dan.6.29` name "Daniel", and none has
  "I, Daniel". Daniel names himself in the first person only in 7:1-12:13, in 9 verses (7:15, 7:28, 8:1, 8:15, 8:27, 9:2, 10:2, 10:7, 12:5); the string "I, Daniel" is in 5 of them, and the rest read "As for me, Daniel", "even to me, Daniel" or "I, even I Daniel" [MEASURED check lane C1 c1_measure.py]. The
  device inventory agrees: i_daniel_aram (7:15, 7:28) plus i_daniel_heb (seven verses, 8:1 to 12:5) [EXTRACTED]. The
  one first-person voice in the tales is the king's (i_nebuchadnezzar_aram at `web:Dan.4.4`=`oshb:Dan.4.1`, `web:Dan.4.34`=`oshb:Dan.4.31`, `web:Dan.4.37`=`oshb:Dan.4.34`).
- Chronology. 5:30 narrates Belshazzar's death, `web:Dan.5.31`=`oshb:Dan.6.1` brings in Darius and `web:Dan.6.28`=`oshb:Dan.6.29` reaches Cyrus. 7:1 then dates a
  vision to "the first year of Belshazzar", and the datelines 8:1, 9:1 and 10:1 run a second regnal sequence to Cyrus
  [EXTRACTED datelines; WEB slices, s09_probe.py]. A restart of the regnal sequence is the text's own signal of a new
  series [INFERRED].
- Closure. WEB names Cyrus only at 1:21, `web:Dan.6.28`=`oshb:Dan.6.29` and 10:1 [MEASURED s10_probe2.py]. The first two are the closing
  verses of the first and last tales: "even to the first year of King Cyrus" and "in the reign of Cyrus the Persian".
  Reading them as a bracket around the tales is INFERRED.

Evidence against the genre frame:
- Chapter 7 is Aramaic and shares the tales' formula stock [EXTRACTED; distribution MEASURED s10_probe2.py]:
  - behold_aram: six of its nine verses are in chapter 7, the rest in chapters 2 and 4;
  - i_was_seeing_aram: eight of 12 verses are in chapter 7, the rest in chapters 2 and 4;
  - most_high_aram: four of 13 verses are in chapter 7;
  - everlasting_dominion_aram pairs `web:Dan.4.34`=`oshb:Dan.4.31` with 7:14, and everlasting_kingdom_aram pairs `web:Dan.4.3`=`oshb:Dan.3.33` with 7:27.
- Dream-vision reporting is not confined to 7:1-12:13. The dream reports of chapters 2 and 4 use the same Aramaic
  vocabulary: visions_of_my_head_aram at 2:28, `web:Dan.4.5`=`oshb:Dan.4.2`, `web:Dan.4.10`=`oshb:Dan.4.7` and `web:Dan.4.13`=`oshb:Dan.4.10`, then 7:1 and 7:15.

Rival tested: the LANGUAGE shape. Its runs are Hebrew 1:1 to 2:4 word 4, Aramaic 2:4 word 5 to 7:28, and Hebrew
8:1-12:13 [EXTRACTED dan_language_zones.json].
- For it: the runs are measured (157 Hebrew, 199 Aramaic, 1 mixed verse). The Aramaic run is lexically
  cohesive (above). The return to Hebrew at 8:1 word 1 falls on a dateline.
- Against it: its first boundary falls inside a verse. MT 2:4 switches after word 4, and word 4 is the word "Aramaic"
  itself (OSHB/WLC אֲרָמִ֑ית; WEB "in the Syrian language") [MEASURED s10_probe2.py]. The switch sits inside the
  Chaldeans' reply, in the middle of the tale that opens at the 2:1 dateline and closes at the 2:49 promotion. No row
  boundary may fall inside a verse, so this shape cannot tile. At the one point where it would cut, it would sever
  2:1-2:3 from the tale they open.

Verdict:
- The genre frame tiles and the language runs are an overlay.
- Both shapes agree on 7:28/8:1: the closing formula at 7:28 ("Here is the end of the matter") and the dateline at 8:1.
  That seam is a parent seam under either shape.
- Chapter 7 is the hinge. It belongs to the vision series by its dateline and its first-person report, and to the
  Aramaic run by its language. Writer part W4 holds PG and PH so that one reviewer has both sides of the return to
  Hebrew.
- A third candidate was not tested in this lane: the concentric reading of chapters 2 to 7 known from the scholarly
  literature [ASSUMED, from model knowledge; UNAVAILABLE here]. It would move no parent seam. Its units are the tales
  and the chapter 7 vision, which this plan already holds as whole parents (PB-PG) [INFERRED].

## §2 Device matrix

Counts come from `dan_device_inventory.json` (MT face, converted by dan_lib) [EXTRACTED]. Distributions are MEASURED by
s10_probe2.py.

Tier-1 seam skeleton. These signals drive the parent seams.
- Datelines that open a unit: 1:1, 2:1, 7:1, 8:1, 9:1 and 10:1. These are six of the inventory's eight dateline
  entries. The other two do not open a unit: 9:2 resumes 9:1 ("in the first year of his reign"), and 11:1 stands inside
  the messenger's direct speech.
- Tale onsets without a dateline:
  - the subject-first royal clause at 3:1 and 5:1;
  - the epistolary prescript at `web:Dan.4.1`=`oshb:Dan.3.31` (to_all_peoples_nations_tongues_aram, peace_be_multiplied_aram);
  - the succession notice at `web:Dan.5.31`=`oshb:Dan.6.1`.
- Closures:
  - the regnal terminus at 1:21;
  - the promotion notices at 2:49 and 3:30;
  - the first-person praise at `web:Dan.4.37`=`oshb:Dan.4.34`;
  - "In that night" at 5:30;
  - the regnal summary at `web:Dan.6.28`=`oshb:Dan.6.29`;
  - "Here is the end of the matter" at 7:28;
  - the collapse notice at 8:27;
  - the end of the messenger's speech at 9:27;
  - the dismissal at 12:13.

Rulings on interaction (working rulings, binding on writers, open to Fable):
- D1. A refrain or doxology is close-side evidence: it belongs to the unit before it, and the edge after it is weighed
  from both sides (the inventory's rules: "a refrain CLOSES a unit"; "a seam is assessed from BOTH sides" [EXTRACTED
  dan_device_inventory.json]). It does not by itself fix the next edge. The candidates are:
  - 2:20-2:23 (blessed_aram, praise_aram);
  - `web:Dan.4.3`=`oshb:Dan.3.33`;
  - `web:Dan.4.34`-`web:Dan.4.35`=`oshb:Dan.4.31`-`oshb:Dan.4.32`;
  - `web:Dan.4.37`=`oshb:Dan.4.34`;
  - `web:Dan.6.25`-`web:Dan.6.27`=`oshb:Dan.6.26`-`oshb:Dan.6.28`;
  - 7:14 (everlasting_dominion_aram).
  A row does not join a closing doxology to a following verse that carries its own onset signal. Where the verse after
  a doxology resumes rather than opens, the writer weighs both sides and grades the edge honestly (§7 (o) and (p)).
- D2. Two datelines are texture, never tier-1: the resumptive dateline (9:2) and the dateline inside direct speech
  (11:1).
- D3. A language switch is never a boundary by itself (inventory rule; campaign rule 5). At 8:1 the dateline drives.
- D4. Weak connectives never open a unit alone. They are then_aram (43 verses), answered_and_said_aram
  (16 strict, 28 loose), because_of_this_aram and and_he_said_heb (17 verses).
- D5. "I was seeing" and "behold" (behold_aram, behold_heb) step scenes inside a vision or dream report. They do not open
  a parent. Inside an interpretation (7:19-7:22; 7:21 "I saw") vision vocabulary does not reopen the vision.
- D6. Two further signals are texture: a person shift, such as first person to third person in chapter 4 at `web:Dan.4.19`=`oshb:Dan.4.16`;
  and a time-interval clause, such as `web:Dan.4.29`=`oshb:Dan.4.26` "At the end of twelve months", the ten-day test in 1:12-1:15, or the day
  counts at 12:11-12:12.
- D7. A closing notice may stand as a one-verse row (summary_notice, §6). It is never merged forward into the next
  unit's onset.

Texture signals. These inform rows and never set parents:
- vayehi_heb (1:6, 1:16, 1:21, 8:2, 8:15);
- in_those_days_heb (10:2);
- at_that_time_heb (12:1);
- time_of_the_end_heb (8:17, 11:35, 11:40, 12:4, 12:9);
- fear_not_heb (10:12, 10:19);
- this_is_the_interpretation_aram (2:36, `web:Dan.4.24`=`oshb:Dan.4.21`, 5:26);
- the vision nouns: hazon (11 verses) and mareh (13 verses). The mareh count includes the "appearance"
  sense at 1:4 and 1:13 (phase0_defects).

Disclosure objects. These are never seams, except the calendar date at 10:4, whose status is left open (see the calendar onsets below, and §7(n)):
- the word-level switch in 2:4;
- the return to Hebrew at 8:1 word 1;
- the Greek insertion point at 3:23/3:24;
- the two numbering zones (§3);
- the single calendar date at 10:4.

Calendar onsets. This strategy states NO working rule on whether a calendar date may open a unit. No Daniel ruling
exists, and Ezekiel's ruling does not carry over. The inventory records one calendar date, 10:4 ("the twenty-fourth day
of the first month"), inside the unit dated at 10:1, and its CAL_NO_ONSET set is empty [EXTRACTED]. The plan records
`cal_no_onset` as rule null with no verses. The question is listed for Fable.

## §3 Numbering and language discipline

Numbering.
- The tiling face is WEB: `verse_inventory.json` declares numbering_face "WEB", 357 verses and 12 chapters
  [EXTRACTED; the validator re-sums].
- A plain C:V ref is on the WEB face. Outside the zones WEB and MT are identical.
- The zones [EXTRACTED web_mt_offset_map.json, verification GREEN; dan_lib.web_to_mt self-test GREEN, s07_selftest.py]:
  - `web:Dan.4.1`-`web:Dan.4.3`=`oshb:Dan.3.31`-`oshb:Dan.3.33`;
  - `web:Dan.4.4`-`web:Dan.4.37`=`oshb:Dan.4.1`-`oshb:Dan.4.34`;
  - `web:Dan.5.31`=`oshb:Dan.6.1`;
  - `web:Dan.6.1`-`web:Dan.6.28`=`oshb:Dan.6.2`-`oshb:Dan.6.29`.
- Every ref in a zone is written as a token pair on one line. The device inventory and the marks are on the MT face.
  Convert them only through web_mt_offset_map.json or dan_lib.mt_to_web, never by arithmetic from memory.
- Two parent seams sit at zone edges: 3:30/`web:Dan.4.1`=`oshb:Dan.3.31` and 5:30/`web:Dan.5.31`=`oshb:Dan.6.1`. The MT chapter lines place the prescript with
  chapter 3 and the succession notice with chapter 6. Chapter lines never drive or corroborate a seam (E-23), so both
  seams are argued from the text (§5, §7) and their rivals go to Fable.

Language.
- The runs [EXTRACTED dan_language_zones.json]: Hebrew 1:1 to 2:4 word 4; Aramaic 2:4 word 5 to 7:28; Hebrew
  8:1-12:13. That is 157 Hebrew verses, 199 Aramaic verses and one mixed verse.
- The mixed verse is 2:4: 12 words, with the switch after word 4 [EXTRACTED dan_lib MIXED_VERSES; MEASURED
  s10_probe2.py].
- Every row carries a language field taken from the zones file's verse_language: `H` (Hebrew), `A` (Aramaic) or `mixed`.
- A row that covers 2:4 carries "mixed" and states: "covers the 2:4 word-level switch (Hebrew words 1-4, Aramaic words
  5 onward)". No row boundary falls inside a verse, so 2:4 is never a seam.
- A quotation from 2:4 names its half: Hebrew (words 1-4) or Aramaic (words 5-12) [EXTRACTED dan_language_zones.json].
  A device count that covers 2:4 reports each half under its own language. The device inventory already does: each
  pattern is matched only on its own language's text, and MT 2:4 is split by word index [EXTRACTED
  dan_device_inventory.json method]. The only formula it finds in 2:4 is o_king_live_forever_aram, at words 5-7, in
  the Aramaic half [MEASURED orchestrator reconcile_dan_strategy.py]. The readiness file makes this the controlling
  agent's call; the orchestrator adopted it at reconciliation (check lane C2 DEF-5), and it is listed for Fable.
- Rows over 2:5-7:28 carry `A`. Their quotations are sliced from the OSHB/WLC Aramaic, and their morphology labels
  are Aramaic. Rows over 1:1-2:3 and 8:1-12:13 carry `H`.
- PB holds the switch; the PG/PH seam holds the return. Language never moves a seam.

## §4 Marker policy and cross-tradition scope

Parashah marks [MEASURED s06_marks.py over pmarks_Dan.json].
- There are 30 marks: 22 PE and 8 SAMEKH. Each is recorded after a verse, on the MT face.
- They are single-witness evidence. They inform and never decide. A writer cites PE or SAMEKH by name and never merges
  them as "a mark".
- A PE follows the close verse of every parent seam in this plan: 1:21, 2:49, 3:30, `web:Dan.4.37`=`oshb:Dan.4.34`, 5:30, `web:Dan.6.28`=`oshb:Dan.6.29`, 7:28, 8:27
  and 9:27. That agreement is reported as single-witness information. It is not the reason for any seam.
- Marks inside parents that writers weigh:
  - PE after 2:13, 2:16, 2:28 and 2:45, and SAMEKH after 2:24;
  - SAMEKH after 3:12, 3:18 and 3:25, and PE after 3:23;
  - PE after `web:Dan.4.28`=`oshb:Dan.4.25`;
  - SAMEKH after 5:7, and PE after 5:12 and 5:16;
  - SAMEKH after `web:Dan.6.5`=`oshb:Dan.6.6` and `web:Dan.6.10`=`oshb:Dan.6.11`;
  - PE after 7:14, 10:3 and 10:21;
  - SAMEKH after 12:2, and PE after 12:3 and 12:8.
- Silences:
  - no mark in 1:1-1:20;
  - none after `web:Dan.4.3`=`oshb:Dan.3.33` or `web:Dan.5.31`=`oshb:Dan.6.1`;
  - none at 8:14/8:15, 9:19/9:20 or 9:23/9:24;
  - none after any verse in 11:1-11:45;
  - none after 12:4.
- Other paratext is not boundary evidence. Paseq occurs in 40 verses and K/Q notes in 80 verses [MEASURED
  s06_marks.py]. A K/Q note enters a row only as a reading-form disclosure (method record, open question 3).
- The WEB's paragraphing (134 pilcrow lines in the clean extract [MEASURED s08_webfmt.py]), its poetry line
  breaks, its footnote sites, and all capitalization and punctuation never drive or corroborate a boundary (E-23).

Cross-tradition scope.
- The following is metadata, in prose only: the Old Greek, Theodotion, the Greek additions (the Prayer of Azariah and
  the Song of the Three, Susanna, Bel and the Dragon), the Qumran Daniel fragments, 4Q242, the Targum, the Peshitta and
  the Vulgate.
- None of it is in the staged witnesses. None of it is a refs entry, boundary evidence or counterevidence.
- The Greek text inserts its additions between 3:23 and 3:24. The hardness file marks its Greek numbering equivalence
  as recalled from memory [REPORTED hardness_batch_01.json].
- A PE follows MT 3:23. That coincidence is disclosed, and it is never cited as a reason tied to the Greek.
- A row boundary at 3:23/3:24, if a writer places one, rests on the Aramaic text alone. 3:24 opens with "Then", a weak
  connective (D4); 3:23 is the fall into the furnace.

## §5 Parent architecture, byte-anchored

Opening words are sliced by gen_strategy.py from Dan_web_clean.txt (WEB). Seam evidence is given from both sides.

| id | span | verses | opening words (WEB, sliced) | seam evidence, both sides | zone dual |
|---|---|---|---|---|---|
| PA | 1:1-1:21 | 21 | "In the third year of the reign" | onset: dateline (Jehoiakim, third year), book start. close: regnal terminus "even to the first year of King Cyrus"; PE after 1:21 (single witness) | none (identity) |
| PB | 2:1-2:49 | 49 | "In the second year of the reign" | onset: dateline (Nebuchadnezzar, second year); prior side: 1:21 terminus. close: 2:49 promotion notice; PE after 2:49. Holds the 2:4 word-level switch (disclosure, never a seam) | none (identity) |
| PC | 3:1-3:30 | 30 | "Nebuchadnezzar the king made an image of" | onset: subject-first royal clause "Nebuchadnezzar the king made"; prior side: 2:49 promotion. close: 3:28-3:29 blessing and decree, 3:30 promotion; PE after 3:30. Holds the 3:23/3:24 Greek insertion point (disclosure) | none (identity) |
| PD | 4:1-4:37 | 37 | "Nebuchadnezzar the king," | onset: epistolary prescript (to_all_peoples_nations_tongues_aram, peace_be_multiplied_aram at `web:Dan.4.1`=`oshb:Dan.3.31`); `web:Dan.4.2`=`oshb:Dan.3.32` turns to what God worked "toward me"; prior side: 3:30 promotion, PE after 3:30, no mark after `web:Dan.4.3`=`oshb:Dan.3.33`. close: first-person praise `web:Dan.4.37`=`oshb:Dan.4.34`; doxology pair `web:Dan.4.3`=`oshb:Dan.3.33` and `web:Dan.4.34`=`oshb:Dan.4.31` (generation_to_generation_aram at both; everlasting_kingdom_aram at `web:Dan.4.3`=`oshb:Dan.3.33` answered by everlasting_dominion_aram at `web:Dan.4.34`=`oshb:Dan.4.31`); PE after `web:Dan.4.37`=`oshb:Dan.4.34` | `web:Dan.4.1`=`oshb:Dan.3.31`; `web:Dan.4.37`=`oshb:Dan.4.34` |
| PE | 5:1-5:30 | 30 | "Belshazzar the king made a great feast" | onset: subject-first royal clause "Belshazzar the king made a great feast"; prior side: `web:Dan.4.37`=`oshb:Dan.4.34` praise, PE after it. close: 5:30 "In that night" (in_that_night_aram) the king is slain, the fulfilment of 5:26-5:28; PE after 5:30 | none (identity) |
| PF | 5:31-6:28 | 29 | "Darius the Mede received the kingdom, being" | onset: succession notice "Darius the Mede received the kingdom" at `web:Dan.5.31`=`oshb:Dan.6.1`; the Darius of `web:Dan.6.1`=`oshb:Dan.6.2` onward depends on it; prior side: 5:30 death notice, PE after 5:30. close: decree and doxology `web:Dan.6.25`-`web:Dan.6.27`=`oshb:Dan.6.26`-`oshb:Dan.6.28`, regnal summary `web:Dan.6.28`=`oshb:Dan.6.29`; PE after `web:Dan.6.28`=`oshb:Dan.6.29` | `web:Dan.5.31`=`oshb:Dan.6.1`; `web:Dan.6.28`=`oshb:Dan.6.29` |
| PG | 7:1-7:28 | 28 | "In the first year of Belshazzar king" | onset: dateline (Belshazzar, first year): the regnal sequence restarts; prior side: `web:Dan.6.28`=`oshb:Dan.6.29` regnal summary, PE after it. close: 7:28 "Here is the end of the matter"; PE after 7:28 | none (identity) |
| PH | 8:1-8:27 | 27 | "In the third year of the reign" | onset: dateline (Belshazzar, third year), with the return to Hebrew at word 1; prior side: 7:28 closing formula. close: 8:27 Daniel faints, "I wondered at the vision"; PE after 8:27 | none (identity) |
| PI | 9:1-9:27 | 27 | "In the first year of Darius the" | onset: dateline (Darius son of Ahasuerus, first year), 9:2 resumptive; prior side: 8:27 close. close: 9:27 ends the speech of 9:22-9:27; PE after 9:27 | none (identity) |
| PJ | 10:1-12:13 | 79 | "In the third year of Cyrus king" | onset: dateline (Cyrus, third year) "a message was revealed"; prior side: 9:27 close, PE after it. close: 12:13 dismissal "go your way until the end", book end. Holds 11:1 (dateline in speech) and the 12:4 sealing command | none (identity) |

Arithmetic: 10 parents; the verse counts sum to 357 [MEASURED gen_strategy.py; re-summed by the validator].

Notes:
- PD, the prescript seam. The MT chapter line puts `web:Dan.4.1`-`web:Dan.4.3`=`oshb:Dan.3.31`-`oshb:Dan.3.33` with chapter 3. The text points forward:
  - `web:Dan.4.1`=`oshb:Dan.3.31` is a letter prescript: sender, addressees, greeting;
  - `web:Dan.4.2`=`oshb:Dan.3.32` announces what God worked "toward me", which is the king's own experience in the chapter that follows, not the
    furnace of chapter 3;
  - the doxology of `web:Dan.4.3`=`oshb:Dan.3.33` is answered by `web:Dan.4.34`=`oshb:Dan.4.31` (generation_to_generation_aram at both verses; everlasting_kingdom_aram at `web:Dan.4.3`=`oshb:Dan.3.33` is answered by everlasting_dominion_aram at `web:Dan.4.34`=`oshb:Dan.4.31`) [EXTRACTED dan_device_inventory.json].
  The rival: the prescript closes chapter 3 as a further royal proclamation, like the decree of 3:29 and the letter of
  `web:Dan.6.25`-`web:Dan.6.27`=`oshb:Dan.6.26`-`oshb:Dan.6.28`, which closes its own tale. Recorded for Fable.
- PF, the succession seam. `web:Dan.5.31`=`oshb:Dan.6.1` introduces "Darius the Mede". WEB has "the Mede" only at `web:Dan.5.31`=`oshb:Dan.6.1` and 11:1 [MEASURED
  s10_probe2.py]. Chapter 6 then says only "Darius", which reads as dependent on `web:Dan.5.31`=`oshb:Dan.6.1` [INFERRED]. The rival: `web:Dan.5.31`=`oshb:Dan.6.1`
  closes chapter 5 as the fulfilment of 5:28 (the kingdom "given to the Medes and Persians"). Recorded for Fable.
- PJ is one parent, from 10:1 to 12:13. It has one dateline, and 12:5 ("Then I, Daniel, looked, and behold") steps a
  scene inside the same vision (D5), by a river INFERRED to be the river of 10:4 (the MT nouns differ: nahar at 10:4, ye'or at 12:5) [MEASURED check lane C1 c1_measure.py for the nouns]. 11:1 and 12:4/12:5 are row-level questions (§7).

## §6 unit_type vocabulary and granularity

Closed vocabulary. A row takes exactly one type, and the writer names its evidence.
- `narrative`: narrated action, third person in the tales and first person framing in the visions.
- `dialogue`: an exchange of speeches between parties, for example the king and the Chaldeans in 2:1-2:13.
- `royal_proclamation`: a decree or encyclical, for example 3:29, `web:Dan.4.1`-`web:Dan.4.3`=`oshb:Dan.3.31`-`oshb:Dan.3.33` and `web:Dan.6.25`-`web:Dan.6.27`=`oshb:Dan.6.26`-`oshb:Dan.6.28`.
- `doxology_or_prayer`: praise, blessing, confession or petition, for example 2:20-2:23, `web:Dan.4.34`-`web:Dan.4.35`=`oshb:Dan.4.31`-`oshb:Dan.4.32` and 9:4-9:19.
- `dream_or_vision_report`: the report of what was seen, for example 2:31-2:35, `web:Dan.4.10`-`web:Dan.4.17`=`oshb:Dan.4.7`-`oshb:Dan.4.14`, 7:2-7:14 and 8:2-8:12.
- `interpretation`: the reading of a dream, a writing or a vision, for example 2:36-2:45, `web:Dan.4.24`-`web:Dan.4.26`=`oshb:Dan.4.21`-`oshb:Dan.4.23`, 5:25-5:28 and
  7:17-7:27.
- `heavenly_discourse`: revelation spoken by a heavenly figure, for example 9:22-9:27 and the messenger's speech inside
  PJ (10:1-12:13).
- `summary_notice`: a closing notice or regnal summary, for example 1:21, 2:49, 3:30, `web:Dan.6.28`=`oshb:Dan.6.29` and 7:28.

The example spans are illustrations of the types. They are not rows.

Granularity.
- The target row is 2 to 9 verses.
- A one-verse row is allowed only for a summary_notice or a zone or mixed-verse disclosure that the writer justifies.
- A row above 9 verses is allowed only when the unit is a single speech act with no internal tier-2 signal, and the
  writer states that. The prayer of 9:4-9:19 is the likely case.

Over-split guard:
- (a) No row boundary rests on a weak connective alone (D4).
- (b) In 11:2-12:4 no boundary rests on a historical identification of the kings. The turns between "the king of the
  south" and "the king of the north" are texture. Boundaries follow discourse signals only (time_of_the_end_heb at
  11:35 and 11:40; at_that_time_heb at 12:1). Inside 11:2-11:34 writers also weigh the text's own succession formula:
  וְעָמַ֧ד עַל כַּנּ֛וֹ (OSHB/WLC) opens 11:20 and 11:21, and 11:7 opens with וְעָמַ֛ד and carries כַּנּ֑וֹ [MEASURED
  orchestrator reconcile_dan_strategy.py]. It is a text signal like the others, weighed from both sides and kept apart
  from any identification of the kings. No PE or SAMEKH mark stands in chapter 11 [MEASURED orchestrator
  reconcile_dan_strategy.py].
- (c) No cut inside 9:24-9:27 without text signals from both sides. This lane's sweep found none: there is no mark
  inside 9:24-9:27, and the only PE is after 9:27.
- (d) A dream or vision report and its interpretation always sit in one parent, by construction. At row level they part
  only where the text marks the turn (the list is not exhaustive: chapter 4 turns at `web:Dan.4.18`=`oshb:Dan.4.15`/`web:Dan.4.19`=`oshb:Dan.4.16` and at `web:Dan.4.24`=`oshb:Dan.4.21`, §7(f)): 2:36 ("This is the dream; and we will tell its interpretation"), 7:15-7:16 and
  8:15.

Under-split guard: a row may not hold a closing doxology or notice together with the next scene's onset (D1, D7).
Where the verse after a doxology resumes rather than opens (§7 (o) and (p)), no onset follows, and the edge is weighed
from both sides.

## §7 Expected low-confidence regions

Each region names the evidence to weigh, the rival readings and the grade this lane expects. Expected grades are
INFERRED.
- (a) The switch at 2:4 (target 1). It is a disclosure object, not a seam (§3). The row covering 2:4 is "mixed". The
  row seam near it (2:3/2:4 or 2:4/2:5) rests on the dialogue's turns, never on the switch. Expected: medium_low for the
  row edge.
- (b) The dream and its reading in 2:31-2:45 (hardness boundary risk). 2:36 marks the turn inside Daniel's speech.
  Splitting the report from its reading across rows is allowed only at 2:35/2:36. Expected: medium.
- (c) The Greek insertion point at 3:23/3:24 (target 2). This is the PE-and-Greek coincidence of §4. The Aramaic
  narrative runs straight through, from the fall into the furnace to the king's astonishment. Expected: medium_low if a
  row edge is placed there.
- (d) The prescript `web:Dan.4.1`-`web:Dan.4.3`=`oshb:Dan.3.31`-`oshb:Dan.3.33` (target 3, first zone). This is a parent seam. The rival is in §5. Expected: medium_low
  for the rows at the seam; the class question goes to Fable.
- (e) The succession notice `web:Dan.5.31`=`oshb:Dan.6.1` (target 3, second zone). This is a parent seam. The rival is in §5. Expected:
  medium_low for the row at `web:Dan.5.31`=`oshb:Dan.6.1`.
- (f) The first-person encyclical frame of chapter 4 around the third-person centre (target 4).
  - The frame is `web:Dan.4.1`-`web:Dan.4.3`=`oshb:Dan.3.31`-`oshb:Dan.3.33` and `web:Dan.4.34`-`web:Dan.4.37`=`oshb:Dan.4.31`-`oshb:Dan.4.34`; the third-person narration is `web:Dan.4.19`-`web:Dan.4.33`=`oshb:Dan.4.16`-`oshb:Dan.4.30`.
  - The person shift at `web:Dan.4.19`=`oshb:Dan.4.16` is texture (D6), and the frame's inclusio is EXTRACTED from dan_device_inventory.json (the formula pairs above).
  - Rows are weighed at `web:Dan.4.18`=`oshb:Dan.4.15`/`web:Dan.4.19`=`oshb:Dan.4.16`, at `web:Dan.4.28`=`oshb:Dan.4.25`/`web:Dan.4.29`=`oshb:Dan.4.26` (PE after `web:Dan.4.28`=`oshb:Dan.4.25`; the "twelve months" clause) and at
    `web:Dan.4.33`=`oshb:Dan.4.30`/`web:Dan.4.34`=`oshb:Dan.4.31`.
  - Expected: medium_low at `web:Dan.4.19`=`oshb:Dan.4.16` and `web:Dan.4.29`=`oshb:Dan.4.26`.
- (g) The seam between vision and interpretation in chapter 7, 7:1-7:14 against 7:15-7:28 (target 5; hardness boundary
  risk).
  - From the close side: 7:14's everlasting dominion closes the vision (D1), and a PE follows 7:14.
  - From the onset side: 7:15 "As for me, Daniel" (i_daniel_aram) and "the visions of my head".
  - Inside the interpretation, 7:19-7:22 re-narrate the vision (D5).
  - Expected: medium for 7:14/7:15 and medium_low inside 7:19-7:22.
- (h) The seam between vision and interpretation in chapter 8, at 8:14/8:15 (found by this lane). 8:15 has vayehi_heb
  and "I, even I Daniel", and there is no mark. Expected: medium.
- (i) The prayer 9:4-9:19 against the seventy weeks 9:20-9:27 (target 6; hardness boundary risks).
  - 9:4 opens with the prayer formula (great_and_awesome_god_heb), and 9:19 ends in petition.
  - 9:20-9:21 are "while I was speaking" clauses that bind the answer to the prayer, so the seam is syntactically soft.
    There is no mark at 9:19/9:20 or 9:23/9:24.
  - The divine name yhwh_name_heb occurs at 9:20 as well as inside the prayer.
  - 9:24-9:27 is not cut internally without both-side evidence (§6(c)).
  - Expected: medium_low for 9:19/9:20 and 9:23/9:24.
- (j) The dateline inside speech at 11:1 (device item 2).
  - One side: a PE follows 10:21, which informs a break 10:21/11:1.
  - The other side: 11:2 "Now I will show you the truth" fulfils 10:21's "I will tell you that which is inscribed in the
    writing of truth" and opens the survey.
  - The working answer: 11:1 closes the messenger's preamble (10:20-11:1).
  - Expected: medium_low. Listed for Fable.
- (k) The continuous survey 11:2-12:4 (target 7; hardness boundary risk). The over-split guard §6(b) applies,
  including the succession formula at 11:7, 11:20 and 11:21 (check lane C2 DEF-3). 11:20 and 11:21 both open with it,
  so whether 11:20 stands as its own row (a one-verse row needs the §6 justification) or joins a neighbour is weighed
  there. No PE or SAMEKH mark stands in chapter 11, so every interior edge rests on the text alone. Expected:
  medium_low for interior row edges wherever no discourse signal falls. Listed for Fable.
- (l) The epilogue and its numbers, 12:5-12:13 (target 8).
  - 12:4 closes with the sealing command. 12:5 steps the scene (D5).
  - A PE follows 12:8.
  - The day counts at 12:11 and 12:12 are texture (D6). The beatitude at 12:12 (ashre_heb) does not open a row.
  - Expected: medium_low at 12:10/12:11 and at 12:4/12:5.
- (m) The terminus at 1:21 and the unmarked 1:1-1:20 (device item 1). The item asks whether a regnal year named as an end point is a dateline; this plan counts 1:21 as a closure, not a dateline (§2 closures; the inventory's eight datelines exclude it), and asks Fable to confirm. No mark stands inside the chapter. Rows rest on
  the text alone (vayehi_heb at 1:6 and 1:16). Expected: medium.
- (n) The calendar date at 10:4 (device item 3).
  - It stands after the 10:1 dateline and the mourning of 10:2-10:3, and a PE follows 10:3.
  - No rule is stated (§2).
  - Expected: medium_low for 10:3/10:4.
- (o) The edge after the praise of 2:20-2:23 (check lane C2 DEF-1; D1 weighs it).
  - Close side: the praise 2:20-2:23 (D1). No mark follows 2:23 [MEASURED orchestrator reconcile_dan_strategy.py].
  - Onset side: 2:24 opens with כָּל קֳבֵ֣ל דְּנָ֗ה (OSHB/WLC), because_of_this_aram, a weak connective (D4); WEB
    "Therefore Daniel went in to Arioch," (WEB). A SAMEKH follows 2:24, one witness. 2:25 opens "Then Arioch brought
    in Daniel" (WEB) [MEASURED orchestrator reconcile_dan_strategy.py].
  - Rivals: an edge at 2:23/2:24 against one at 2:24/2:25. Expected: medium_low. Listed for Fable.
- (p) The edge after the praise of `web:Dan.4.34`-`web:Dan.4.35`=`oshb:Dan.4.31`-`oshb:Dan.4.32` (check lane C2 DEF-1;
  D1 weighs it).
  - `web:Dan.4.36`=`oshb:Dan.4.33` repeats "my understanding returned to me" (WEB) from `web:Dan.4.34`=`oshb:Dan.4.31`
    [MEASURED orchestrator reconcile_dan_strategy.py], so it resumes the account the praise interrupts [INFERRED].
  - No mark follows `web:Dan.4.35`=`oshb:Dan.4.32` or `web:Dan.4.36`=`oshb:Dan.4.33`; a PE follows
    `web:Dan.4.37`=`oshb:Dan.4.34` [MEASURED orchestrator reconcile_dan_strategy.py].
  - Rivals: an edge at `web:Dan.4.35`=`oshb:Dan.4.32`/`web:Dan.4.36`=`oshb:Dan.4.33` against none inside
    `web:Dan.4.34`-`web:Dan.4.37`=`oshb:Dan.4.31`-`oshb:Dan.4.34`. Expected: medium_low. Listed for Fable.

Divided readings. Each is reported neutrally, with the attribution given in the hardness file or as general knowledge
[REPORTED; not adjudicated]. None moves a seam, and the strategy takes no position on any of them.
- Canon. The book is placed among the Writings in the Jewish canon and among the Prophets in Christian Old Testaments.
  Catholic and Orthodox canons include the Greek additions; Protestant canons do not.
- Date and authorship. A sixth-century setting and authorship is held in traditional Jewish and Christian reading. A
  second-century (Maccabean) date for the final form is held in critical scholarship.
- 9:24-9:27. The readings are messianic (traditional Christian), dispensational (a gap before the last week) and
  Antiochene (critical scholarship).
- 7:13. The one like a son of man is read as an individual (messianic readings) or as a corporate figure (the holy ones
  of 7:18 and 7:27).
- The fourth kingdom. It is read as Rome (traditional Jewish and Christian) or as Greece (critical scholarship).
- 8:14. The evenings and mornings are the basis of the Seventh-day Adventist sanctuary doctrine.
- 12:2. The verse is used as a proof text for resurrection, as the hardness file reports; the file links it to John 5:28-29 [REPORTED hardness_batch_01.json]. Which traditions use it this way is not measured here.
- 3:25. WEB reads "a son of the gods"; KJV reads "the Son of God", which some Christian readings take
  christologically.
- The abomination. The abomination of 9:27, 11:31 and 12:11 is identified in divided ways. The hardness file links the phrase to 1 Maccabees 1:54 and to Matthew 24:15 and Mark 13:14 [REPORTED hardness_batch_01.json]. This strategy takes no position among these readings.

## §8 Register and hygiene

Copy this section verbatim into every writer brief.
1. Register: a planning and segmentation record for scholars. It is plain and exact, with no homiletics and no
   adjudication of a divided reading. Where a divided reading bears on a row, report it neutrally and attribute it.
2. Evidence: the text's own signals drive a boundary. Parashah marks are single-witness evidence and never decide, and
   PE and SAMEKH are never merged. Chapter and verse divisions, WEB paragraphs, line breaks, footnote sites,
   capitalization and punctuation never drive or corroborate a boundary.
3. Numbering: a plain C:V ref is on the WEB face. A ref inside a zone is written as a `web:Dan.` token with its
   `oshb:Dan.` dual on the same line. Convert only through web_mt_offset_map.json or dan_lib.
4. Language: every row carries `H`, `A` or `mixed` (verse_language) from dan_language_zones.json. A row covering 2:4 says so. No row
   boundary falls inside a verse.
5. Cross-tradition: Greek, Qumran, Targum, Peshitta and Vulgate material is prose metadata only. It is never a refs
   entry and never evidence. The Greek insertion point at 3:23/3:24 is never a reason for a seam.
6. Quotations are short and sliced by script, and they carry their attribution (OSHB/WLC; WEB). Never retype a
   quotation.
7. Provenance: every count and claim carries its tier (MEASURED with its script, EXTRACTED with its file, REPORTED,
   INFERRED, ASSUMED, UNAVAILABLE). Never write a stronger word than the evidence. No figure from another book passes
   as Daniel's.
8. Grades: grade honestly. A row whose seam has one-sided evidence, or evidence only from a mark, is low or medium_low
   and goes to Fable's end review. Never round up a grade.
9. Seams: rows never straddle a parent seam. The parents are 1:1-1:21, 2:1-2:49, 3:1-3:30, `web:Dan.4.1`-`web:Dan.4.37`=`oshb:Dan.3.31`-`oshb:Dan.4.34`, 5:1-5:30, `web:Dan.5.31`-`web:Dan.6.28`=`oshb:Dan.6.1`-`oshb:Dan.6.29`, 7:1-7:28, 8:1-8:27, 9:1-9:27 and 10:1-12:13. A refrain or doxology is close-side evidence for the unit before it; it does not by itself fix the next edge. Assess every seam from both sides, and read
   the verse on either side of the part as read-only context.

## §9 Writer part plan

| id | span | verses | parents | internal parent seams | zone dual |
|---|---|---|---|---|---|
| W1 | 1:1-2:49 | 70 | PA, PB | internal parent seam 1:21/2:1 | none (identity) |
| W2 | 3:1-4:37 | 67 | PC, PD | internal parent seam 3:30/4:1 (`web:Dan.4.1`=`oshb:Dan.3.31`) | `web:Dan.4.37`=`oshb:Dan.4.34` |
| W3 | 5:1-6:28 | 59 | PE, PF | internal parent seam 5:30/5:31 (`web:Dan.5.31`=`oshb:Dan.6.1`) | `web:Dan.6.28`=`oshb:Dan.6.29` |
| W4 | 7:1-8:27 | 55 | PG, PH | internal parent seam 7:28/8:1 | none (identity) |
| W5 | 9:1-9:27 | 27 | PI | none | none (identity) |
| W6 | 10:1-12:13 | 79 | PJ | none | none (identity) |

Arithmetic: 6 parts; the verse counts sum to 357 [MEASURED gen_strategy.py; re-summed by the validator].

Why six parts, and why these:
- Review depth, not verse count, is balanced. The count of hard items per part is:
  - W1: target 1, device item 1 and the dream-reading risk;
  - W2: targets 2, 3 and 4, device item 4 (the twelve months) and the 3:25 reading;
  - W3: target 3 (second zone);
  - W4: target 5, the 7:13, fourth-kingdom and 8:14 readings, and region (h);
  - W5: target 6, the seventy weeks and two boundary risks, in 27 verses;
  - W6: targets 7 and 8, device items 2, 3 and 4, and the 12:2 and abomination readings.
- W6 is the longest part. Its 79 verses are one parent. The survey inside it is a continuous discourse whose main
  risk is over-splitting, so its depth per verse is lower. Dividing it would need a parent seam that the text does not
  give from both sides: 11:1 is a held question.
- Every internal parent seam is one where a rival reading or a crossing structure sits: 1:21/2:1 (device item 1), the
  two zone seams, and 7:28/8:1 (the return to Hebrew and the genre hinge). Each is placed in one reviewer's hands.
- Every part boundary falls on a parent seam with a dateline or a royal-clause onset: 2:49/3:1, `web:Dan.4.37`=`oshb:Dan.4.34`/5:1,
  `web:Dan.6.28`=`oshb:Dan.6.29`/7:1, 8:27/9:1 and 9:27/10:1. So no part boundary pre-decides a row.
- The macro seam `web:Dan.6.28`=`oshb:Dan.6.29`/7:1 is a part boundary. W3's writer reads 7:1-7:2, and W4's writer reads `web:Dan.6.25`-`web:Dan.6.28`=`oshb:Dan.6.26`-`oshb:Dan.6.29`, as
  read-only context.

## §10 Self-checks

A reviewer tests this record against the bytes as follows:
1. Run `_validate_strategy_dan.py` on this file and the plan (tiling, sums, spans, duals, the plan's mt_dual fields, headings, lens, coverage).
2. Re-slice the opening words in §5 from Dan_web_clean.txt, and confirm each seam's close verse from both sides.
3. Recompute every zone pair with dan_lib.web_to_mt, and grep each line that has a `web:Dan.` zone token for its
   `oshb:Dan.` dual.
4. Check every mark cited in §4 against pmarks_Dan.json, converted to WEB, with PE and SAMEKH kept apart.
5. Re-derive the §2 counts and distributions from dan_device_inventory.json (s10_probe2.py is in this lane's OUT).
6. Confirm the language field of each row from dan_language_zones.json, and confirm that no row boundary is inside
   2:4.
7. Confirm that no boundary cites the Greek insertion point, a chapter line, WEB paragraphing or a divided reading.
8. Confirm that every number of two or more digits here, other than a ref, is a Daniel measurement with its source or
   is labelled as lineage (report.json numbers_audit).

## §11 Lens record (OW-19)

- Count: 3.
- Reason: Daniel is an owner-named HARD book, 15 of 15 in the hardness file and severe on all five axes, and the readiness file indicates a third lens. Two blind lanes are the OW-19 floor. The third lane assesses each hard seam from the OSHB/WLC Hebrew and Aramaic bytes (the formula signals, the 2:4 word-level switch and the MT numbering zones), so its evidence access differs from lanes that start from the WEB face.
- Third lens kind: `ORIGINAL_LANGUAGE_OR_VERSIONAL`, from the readiness file's list.
- Caveat: every lane runs on claude-opus-5-5 (OW-25). The third lens is therefore decorrelated by evidence kind only,
  not by model family. Agreement among all three lanes is one family's voice, and a 2-1 split is not a majority.
  Whether this satisfies OW-19 is listed for Fable.
- Model downgrade (device inventory item 5): the inventory was built and self-checked on claude-opus-5-5 as grader_fallback (OW-25), and this strategy was written on the same model in Fable's role. Its parents, lens decision and working rulings D1-D7 go to Fable's end review as a recorded downgrade, the first non-Opus check [EXTRACTED dan_device_inventory.json for_fable_end_review].

## Provenance and limits

- Tiers are as marked. MEASURED items name scripts in this lane's OUT: s06_marks.py, s07_selftest.py, s08_webfmt.py,
  s09_probe.py, s10_probe2.py, s11_probe3.py and gen_strategy.py. EXTRACTED items name the pinned file.
- Items added at reconciliation name their source: "check lane C1 c1_measure.py" or "orchestrator
  reconcile_dan_strategy.py" (the orchestrator's script, which asserts every figure and slices every quotation it
  writes from the bytes).
- Quotations are sliced from Dan_web_clean.txt (WEB) and Dan_oshb.txt (OSHB/WLC).
- The structural readings (the brackets, the dependencies, the expected grades) are INFERRED. The divided readings are
  REPORTED and are not adjudicated.
- This lane did not read any cross-tradition witness. It did not test the concentric reading. It did not re-run the
  device inventory's census.
- It is a single-model plan written in Fable's role under a recorded downgrade (OW-25). Its seams are working
  architecture for Fable's end review, not rulings.

## What changed from a1

Sections and line numbers are as the check lanes named them in `.a1`. Lane C1's items are D1-D10; lane C2's are DEF-1
to DEF-8.

- R1 — §5 (PD row, line 208): The doxology pair WEB 4:3 / WEB 4:34 is attributed to everlasting_kingdom_aram and
  generation_to_generation_aram; the lane's exact correction applied. Executes: C1 D1.
- R2 — §5 (PD evidence, line 223): The same misattribution as D1, at its second site; the lane's exact correction
  applied. Executes: C1 D2.
- R3 — plan for_fable_end_review (zone seam 3:30/4:1 evidence): The same misattribution as D1, in the plan's evidence
  string; the lane's exact correction applied. Executes: C1 D3.
- R4 — §7 (f), line 285: 'MEASURED by the formula pairs above' names no script (OW-18); the lane's exact correction
  applied, and the same fix carried to plan scrutiny_targets[3].disposition, which the lane did not name. Executes: C1
  D4.
- R5 — §11: Device-inventory for_fable_end_review item 5 ('model downgrade') is assigned by the plan to §11, but §11
  does not dispose it; the lane's exact correction applied. Executes: C1 D5.
- R6 — §1 (person evidence, line 23): The md says the quoted string "I, Daniel" occurs in 9 verses; the lane's exact
  correction applied. Executes: C1 D6.
- R7 — §5 table, PD opening words (line 208): The PD opening words "Nebuchadnezzar the king, to all the peoples," are
  not a byte slice of Dan_web_clean.txt; the lane's exact correction applied. Executes: C1 D7.
- R8 — §5 (PJ, lines 229-230): 'at the same river' has no tier and is stronger than the bytes; the lane's exact
  correction applied. Executes: C1 D8.
- R9 — plan parents PD, PF and parts W2, W3; four plan strings; _validate_strategy_dan.py: The offset map's tier0
  disclosure says any structured ref touching WEB 4:1-37, WEB 5:31 or WEB ch 6 MUST carry an explicit dual. The
  orchestrator ruled options (b) and (c): every zone-touching span in the plan now carries an mt_dual field, which the
  validator requires and checks against tools/verse_map_web.json (cross-checked with web_mt_offset_map.json); MT duals
  added to scrutiny_targets[3].disposition and for_fable_end_review[1].evidence, [2].question and [3].evidence;
  scrutiny_targets[3].target is the readiness file's verbatim string and is left as it is. Executes: C1 D9
  (judgement).
- R10 — §7 (m), line 317: Device item 1 (MT 1:21 regnal terminus) asks whether a regnal year named as an end point is
  a dateline; the lane's exact correction applied. Executes: C1 D10.
- R11 — §2 D1; §6 under-split guard; §8 item 9; §7 (o) and (p); plan for_fable_end_review[9]: D1 is 'binding on
  writers' and lists embedded doxologies as closing their units. The orchestrator ruled option (a): D1 is a weighing
  rule, where a doxology is close-side evidence and the next edge is weighed from both sides; the rival edges after
  the praise of 2:20-2:23 and after the chapter-4 praise are named, expected medium_low, and listed for Fable.
  Executes: C2 DEF-1 (judgement).
- R12 — §6 over-split guard (d): The guard lists the report/interpretation turns as 2:36, 7:15-16 and 8:15, and the
  list reads as exhaustive; the lane's exact correction applied. Executes: C2 DEF-2.
- R13 — §6 over-split guard (b); §7 (k); plan for_fable_end_review[10]: Three rules collide over 11:2-11:35, a span of
  34 verses. The orchestrator ruled option (a): the succession formula is named as a discourse signal inside
  11:2-11:34, kept apart from identifying the kings; no mark stands in chapter 11. Executes: C2 DEF-3 (judgement).
- R14 — §2 disclosure objects against the calendar-onset statement: §2 puts 'the single calendar date at 10:4' under
  'Disclosure objects. These are never seams'; the lane's exact correction applied. Executes: C2 DEF-4.
- R15 — §3; plan for_fable_end_review[11]: readiness v2 names three questions to settle 'BEFORE mass review': which
  half of 2:4 a quotation came from, whether a boundary may fall at the language switch, and how a device census
  reports the mixed verse. The orchestrator ruled options (a) and (b): a quotation from 2:4 names its half, and a
  device count reports each half under its own language, as the device inventory already does; the readiness file
  names this the controlling agent's call, so it is listed for Fable. Executes: C2 DEF-5 (judgement).
- R16 — §7 divided readings (12:2): The 12:2 reading is reported in the passive, with no attribution and no source;
  the lane's exact correction applied. Executes: C2 DEF-6.
- R17 — §7 divided readings (the abomination): 'identified in divided ways' names neither the readings nor their
  sources; the lane's exact correction applied. Executes: C2 DEF-7.
- R18 — §8 item 9 (register: a dangling reference): §8 is copied verbatim into every writer brief, but item 9 points
  to '(§5)', which is outside §8; the lane's exact correction applied. Executes: C2 DEF-8.
- R19 — header; §10 item 1; provenance; plan for_fable_end_review[12]: the reconciliation is disclosed; its four
  rulings were made by the orchestrator on claude-opus-5-5 as grader_fallback (OW-25) and are listed for Fable to
  re-rule. Executes: the reconciliation record (no lane item).
