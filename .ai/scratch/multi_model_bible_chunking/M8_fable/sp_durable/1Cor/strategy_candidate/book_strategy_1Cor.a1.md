# Book strategy: 1 Corinthians (WEB face)

Lane `cor_strategy_a1`, execution `cor_strategy_a1#e1`. Model `claude-opus-5-5`; grader role: controlling agent, grader_fallback (OW-25). Face WEB; 1 Corinthians numbering is identity throughout, so every WEB ref is the RP ref and the SBLGNT ref (MEASURED at staging, web_greek_offset_map.json: identity_throughout true, zones empty). All 18 pinned inputs matched their digests before any reading (MEASURED, verify_inputs.py). Every count below carries its OW-18 tier. Every number is a 1 Corinthians measurement or labelled lineage (E-65). Greek is quoted from RP and English from WEB, both sliced by script (gen_strategy.py, ledger in quote_ledger.json). Nothing here is typed from memory.

Tier key: MEASURED (script named), EXTRACTED (copied from a pinned record), TRANSCRIBED, REPORTED (asserted by a pinned record, not re-measured here), INFERRED, ASSUMED, UNAVAILABLE.

## §1 Shape adopted and rivals

**Adopted shape: an argument-structure tiling, with the topic headings as tier-1 onsets and the epistolary frame as bracketing parents.** Thirteen parents, six writer parts. The parents follow the letter's argumentative units:

- an opening frame;
- the divisions section;
- the reported-conduct units;
- the two halves of the marriage answers;
- the idol-food argument;
- the two worship-assembly units;
- the spiritual-gifts argument;
- the resurrection argument;
- the business of the last chapter;
- a closing frame.

Evidence for, in tier order:
- Topic headings. The formula peri de opens a topic at six verses in both witnesses: 7:1, 7:25, 8:1, 12:1, 16:1 and 16:12 (MEASURED, device inventory peri_de_topic_marker rp 6 / sbl 6). Five of them sit on parent seams adopted here. The sixth, 16:12, sits inside the travel-and-commendation business and is a row onset only.
- Frame formulae. They bracket the body in both witnesses: prescript 1:1, address 1:2, greeting 1:3, thanksgiving 1:4; then third-person greetings 16:19 and 16:20, the autograph 16:21, and the grace benediction 16:23 (MEASURED, device inventory frame family; FRAME_edges opening_before 1:10, closing_from 16:19).
- Closing devices. Units whose front seam carries no heading are still closed on the back side by a text device:
  - the calling refrain at 7:24, "μενέτω παρὰ θεῷ.";
  - the imitation command at 11:1, which echoes 10:33 ("καθὼς κἀγὼ" ... "καθὼς κἀγὼ χριστοῦ."; MEASURED, gen_strategy.py: the phrase occurs at 10:33 and 11:1 only);
  - the order maxim at 14:40;
  - the hoste-plus-vocative exhortation at 15:58 ("Ὥστε, ἀδελφοί μου ἀγαπητοί,"; MEASURED, gen_strategy.py: a verse-initial hoste with the vocative occurs at 11:33, 14:39 and 15:58 only).
- Units whose front carries no heading open with other formulae:
  - 1:10, the appeal formula "Παρακαλῶ δὲ ὑμᾶς, ἀδελφοί,";
  - 5:1, the report formula "Ὅλως ἀκούεται", asyndetic;
  - 6:1, an asyndetic question;
  - 11:2, the praise formula "Ἐπαινῶ δὲ ὑμᾶς, ἀδελφοί,";
  - 11:17, the negated praise "Τοῦτο δὲ παραγγέλλων οὐκ ἐπαινῶ,";
  - 15:1, the disclosure formula "Γνωρίζω δὲ ὑμῖν, ἀδελφοί,".

Rivals tested:

1. **Rival A, topical two-block** (reported matters, then the matters of the Corinthians' letter from 7:1).
   - For: 7:1 names the letter, "Περὶ δὲ ὧν ἐγράψατέ μοι,". The headings are the strongest formula family in the book.
   - Against: the headings cannot tile the book. 11:2-11:34 and 15:1-15:58 carry no peri de: they open with the praise and disclosure formulae. 7:25 and 16:12 fall inside topics. 8:4 resumes with a bare peri, "Περὶ τῆς βρώσεως οὖν", inside the 8:1 topic (MEASURED, device inventory peri_sentence_start_bare 8:4).
   - Retained as tier-1 onsets; rejected as the tiling.
2. **Rival C, frame-only** (prescript, thanksgiving, one body, closing).
   - For: the frame formulae are measured in both witnesses.
   - Against: a single body parent of more than four hundred verses gives review no handle and hides every seam.
   - Retained as the two frame parents.
3. **Rival D, chapter-level parents** (separate parents at 2:1, 3:1, 9:1, 10:1, 13:1 and 14:1).
   - For: several of these verses carry a vocative or a disclosure formula; 10:1 has "Οὐ θέλω δὲ ὑμᾶς ἀγνοεῖν, ἀδελφοί,".
   - Against, for 12-14: the scorer's boundary-risk record says 1:10-4:21, 8:1-11:1 and 12:1-14:40 are each one argument and that a parent seam at 9:1 or 10:1 severs the idol-food argument (REPORTED, hardness_batch_03). For 12-14 the text gives a measured bracket: the imperative zeloute stands at 12:31 and 14:1 and again at 14:39 (MEASURED, gen_strategy.py), framing chapter 13 as an inset.
   - Against, for 8:1-11:1: the 11:1 echo of 10:33 closes 10:31-11:1, so 8:1-11:1 ends as one unit.
   - Rejected; these verses become row-onset candidates (§5, §7).
4. **Rival E, one parent for 5:1-6:20.**
   - For: the topic porneia returns at 6:12-6:20 (INFERRED from the WEB sense, not measured).
   - Against: 6:1 opens asyndetically on a new topic, lawsuits. The "do you not know" question binds 6:1-6:20: six of its ten hits fall in chapter 6, at 6:2, 6:3, 6:9, 6:15, 6:16 and 6:19 (MEASURED, device inventory ouk_oidate_hoti). That gives chapter 6 its own cohesion.
   - Rejected. The 5:13/6:1 seam is graded B in §7.
5. **Rival F, one parent for 11:2-11:34.**
   - For: both units concern the assembly; the verb synerchesthai appears at 11:17, 11:18, 11:20, 11:33 and 11:34 (MEASURED, gen_strategy.py; also at 7:5 and 14:26).
   - Against: the praise / negated-praise pair, ἐπαινῶ at 11:2 and οὐκ ἐπαινῶ at 11:17 (MEASURED, device inventory epaino 11:2, 11:17, 11:22), gives a tier-1 onset at 11:17. The appeal to the churches' custom at 11:16 closes the head-covering unit.
   - Rejected. Two parents.

## §2 Device matrix

Tier-1 skeleton. These devices open or close parents; each is measured in both witnesses unless noted.

| device | verses (RP; SBL differences noted) | role here |
|---|---|---|
| peri de topic heading | 7:1, 7:25, 8:1, 12:1, 16:1, 16:12 | onset; parent seam except 16:12 (row onset) |
| frame opening (prescript, address, greeting, thanksgiving) | 1:1, 1:2, 1:3, 1:4 | brackets P01 1:1-1:9 |
| frame closing (greetings, autograph, benediction, love closing) | 16:19, 16:20, 16:21, 16:23, 16:24 | brackets P13 16:19-16:24 |
| appeal formula parakalo hymas | 1:10, 4:16, 16:15 | onset at 1:10 (parent); 4:16 and 16:15 row-level |
| report formula | 5:1 | onset (parent), with asyndeton |
| praise / negated praise | 11:2, 11:17, 11:22 | onsets at 11:2 and 11:17 (parents); 11:22 closes the abuse report |
| disclosure formulae (ou thelo agnoein; gnorizo hymin; thelo de hymas eidenai) | 10:1, 12:1; 12:3, 15:1; 11:3 | onset at 12:1 (with peri de) and 15:1 (parent); 10:1, 12:3 and 11:3 row-level |
| tradition vocabulary (paredoka, parelabon, parelabete, paradoseis) | 11:2, 11:23, 15:1, 15:3 | marks tradition blocks; never splits a tradition from its application |
| closing refrains | 7:24 (meneto also at 7:11, 7:20); 11:1; 14:40; 15:58 | close a unit (back side of a seam) |

Rulings:

- **D1, headings.** A peri de verse is a row's first verse. It is a parent seam where the back side also closes: at 7:1, 7:25, 8:1, 12:1 and 16:1. At 16:12 the topic Apollos sits inside the travel-and-commendation business and is a row onset only. The device inventory's sentence_start flag rests on edition punctuation, so the onset rests on the formula and never on the punctuation. The bare peri at 8:4 is resumptive: it is a row-onset candidate, never a parent seam.
- **D2, disclosure formulae open units but do not by themselves make parent seams.** 10:1 lies inside the idol-food argument, and a parent seam there is the scorer's named severing risk (REPORTED). 12:3 is a consequence (Dio) inside 12:1-12:3. 11:3 continues the 11:2 opening. 15:1 is a parent seam because the back side closes at 14:40 and the front adds tradition vocabulary.
- **D3, refrains close.** A refrain or a hoste-plus-vocative exhortation is the last verse of its unit. Measured closers: 7:24, 11:1, 14:40, 15:58. 11:33 and 14:39 carry the same hoste-plus-vocative pattern. They close their rows, and the parent continues to 11:34 and 14:40.
- **D4, the vocative adelphoi never sets a boundary alone.** It occurs at 22 RP verses and 21 SBL verses (MEASURED, device inventory adelphoi). It corroborates only beside another tier-1 signal. Nominative and accusative uses carry no boundary weight.
- **D5, a slogan and its response stay in one row.** The paired sites are 6:12 and 10:23; 6:13 carries a further slogan with response. Extent is governed by convention C3 (§10).
- **D6, a tradition and its application stay in one row.** These are 11:23-11:26 with 11:27-11:34, and 15:3-15:7 with 15:8-15:11. No row seam may fall at 11:26/11:27 or at 15:7/15:8 (REPORTED boundary risk, adopted as a ruling).
- **D7, thanksgiving verbs outside the frame are texture.** The eucharisto hits at 1:14, 10:30 and 14:18, and the amen at 14:16, are not frame and not onsets (MEASURED, device inventory eucharisto; SBL lacks the phrase with the article at 1:14).
- **D8, frame edges.** The opening frame ends at 1:9 and the body opens at the appeal at 1:10. The closing frame opens at 16:19 with the third-person greetings. The rival edge 16:13 is a run of imperatives followed by the 16:15 appeal; it is recorded in §7 G and sent to Fable.
- **D9, question openers step an argument.** These are ti oun at 10:19, 14:15 and 14:26 (SBL adds 3:5), and ti gar at 5:12, 7:16 and 10:29 (RP only at 10:29) (MEASURED, device inventory). They are row-onset candidates at most. 14:26, "Τί οὖν ἐστίν, ἀδελφοί;", is the strongest because it opens the assembly-order instructions.

Texture (never a boundary by itself):
- "do you not know" (ten hits);
- citation formulae: gegraptai at nine verses, and legei;
- me genoito at 6:15;
- idou at 15:51;
- charis to theo at 15:57;
- touto de phemi / lego at 7:6, 7:29 and 15:50 (MEASURED, gen_strategy.py);
- the addressee series at 7:8, 7:10 and 7:12: "Λέγω δὲ τοῖς ἀγάμοις", "Τοῖς δὲ γεγαμηκόσιν παραγγέλλω,", "Τοῖς δὲ λοιποῖς ἐγὼ λέγω," (MEASURED, gen_strategy.py; a further verse-initial tois de stands at 1:24).

Disclosure objects (reported in the rows that hold them, never reasons for a seam):
- the 14:33b-36 block and the transposition reported for some witnesses (§4);
- maranatha at 16:22 (§3);
- the ten witness-disagreement verses on formula hits (§3);
- the four pilcrow-only verses 1:18, 7:8, 14:34 and 15:50 (MEASURED, s03_probe.py marks);
- the SBL variant sites at text-critical cruxes 2:1, 11:24, 13:3, 14:34-14:35 and 15:51 (§3).

Calendar onsets: **none.** 1 Corinthians has no month-plus-day date (MEASURED, device inventory year_word 0, month_word 0). The calendar references at 5:7 (pascha), 16:2 (first of the week) and 16:8 (Pentecost) are metadata in their rows and open no row by themselves. The choice is recorded in cal_no_onset and listed for Fable.

## §3 Numbering, witness and language discipline

Numbering:
- Spans are written C:V-C:V with an ASCII hyphen on the WEB face.
- 1 Corinthians has no numbering zone, so no dual span and no MT-face token is ever written.
- Inline tokens, when used, are web:, rp: or sbl: followed by a real verse, for example web:1Cor.16.22 and rp:1Cor.16.22.

Witnesses:
- Greek is quoted from RP, sliced by script; SBL is quoted only to disclose a differing reading on which a row's argument rests.
- The two staged witnesses differ at 218 of 437 verses (MEASURED, cor_lib docstring and pmarks rp_sbl_differences). SBL carries 419 variant signs over 220 verses (MEASURED, device inventory totals).
- A quote that crosses an SBL sign reaches only the skeleton tier (EXTRACTED, cor_lib docstring). A row resting on such wording names both readings.

Witness disagreements on formula hits. The ten verses are 1:14, 3:5, 6:2, 6:16, 10:1, 10:23, 10:29, 11:2, 14:39 and 16:24 (EXTRACTED, device inventory item 3). The cases most likely to touch a row's argument:
- 10:23: RP "Πάντα μοι ἔξεστιν,"; SBL "⸀Πάντα ἔξεστιν·", without the pronoun. The slogan's identity with 6:12 is exact in RP and partial in SBL.
- 16:24: RP ends "Ἀμήν."; SBL lacks it.
- 10:1: the wider thelo de hymas formula is RP-only there.
- 11:2: adelphoi is RP-only.
- 14:39: SBL adds mou.

Disclosed readings at the named cruxes (MEASURED, s03_probe.py verse):
- 2:1: SBL marks a variant site at "⸀μαρτύριον". The content of the variant is UNAVAILABLE in the staged inputs.
- 11:24: RP has "Λάβετε, φάγετε·" and "κλώμενον·". SBL has neither, reading "ὑπὲρ ⸀ὑμῶν·".
- 13:3: RP "καυθήσωμαι,"; SBL "⸀καυθήσομαι,".
- 15:51: RP "πάντες μὲν οὐ"; SBL "⸀πάντες οὐ".
- 9:1: RP "Οὐκ εἰμὶ ἀπόστολος; Οὐκ εἰμὶ ἐλεύθερος;"; SBL "Οὐκ εἰμὶ ⸂ἐλεύθερος; οὐκ εἰμὶ ἀπόστολος⸃;". The question order is inverted. The WEB follows the SBL order, and a row quoting the WEB here must disclose it.

Maranatha (16:22):
- RP reads "Μαρὰν ἀθά."; SBL reads "⸂Μαράνα θά⸃." (MEASURED). The word division differs, and SBL marks the site.
- WEB translates the phrase, "Come, Lord!", and carries a footnote marker at 16:22.
- Rows quote the RP form in Greek script with the SBL division disclosed, never restore any other script, and do not let the phrase open a row.
- It is classed provisionally as a language-switch object inside the closing frame. The class goes to Fable (device item 5).

Language:
- Hebrew characters in the staged witnesses: 0 (MEASURED, device inventory totals).
- No language-switch rows exist other than the maranatha object.

Attribution lines (EXTRACTED, device inventory) travel with every quotation:
- Greek witnesses: Robinson-Pierpont Byzantine Textform (Unlicense), primary; SBLGNT (CC BY 4.0), secondary; their attribution terms travel with any quotation.
- World English Bible (WEB); its attribution terms travel with any quotation.

## §4 Marker policy and cross-tradition scope

There are three mark types. They are never conflated.

1. **RP pilcrows**: 35 verses, recorded at the paragraph's first verse (MEASURED, s03_probe.py marks). 31 of them are also WEB paragraph starts. Four are pilcrow-only: 1:18, 7:8, 14:34 and 15:50. A pilcrow is single-witness evidence: it informs and never decides. Five of the twelve adopted parent seams carry one: 1:10, 7:25, 11:2, 11:17 and 16:19. The frame-internal row onset 1:4 also carries one. Seven parent seams carry none: 5:1, 6:1, 7:1, 8:1, 12:1, 15:1 and 16:1 (MEASURED, s03_probe.py seams). Those seams stand on the text's own signals alone.
2. **WEB paragraph starts**: 87, plus a mid-verse break at 9:12. **WEB footnote sites**: 16 markers over 13 verses (MEASURED, s03_probe.py marks). WEB paragraphs, chapter and verse divisions, footnote sites, capitalisation and punctuation never drive or corroborate a boundary (E-23). WEB quotation marks are punctuation and fall under the same exclusion (convention C3).
3. **SBL signs**: these mark a variant site only. They say nothing about a boundary.

The 14:33b-36 block (MEASURED, s03_probe.py verse). Both staged witnesses carry the sentences on women's silence at 14:34-14:35, between 14:33 and 14:36. Neither staged witness carries them after 14:40.
- RP marks a pilcrow at 14:34.
- SBL marks variant sites at 14:34 and 14:35, and at 14:40 ("πάντα ⸀δὲ").
- SBL carries a parenthesis that opens in 14:32 and closes in 14:33 ("εἰρήνης),"), the only parenthesis verses in SBL (MEASURED, gen_strategy.py). This is edition punctuation, and it never drives.
- RP reads "Αἱ γυναῖκες ὑμῶν" where SBL reads "Αἱ ⸀γυναῖκες", without the possessive.
- Both editions end a sentence at the end of 14:33, after "ὡς ἐν πάσαις ταῖς ἐκκλησίαις τῶν ἁγίων.". That is edition punctuation and informs only.
- The Western order, with 14:34-14:35 after 14:40, is REPORTED by the brief and the readiness record (crux 14:34-35). It is a disclosure object: it is reported in the row's prose as metadata, attributed, and is never a reason for or against a seam.

Cross-tradition scope: the following appear only as metadata in prose, attributed, and never move a seam or a row:
- the SBLGNT apparatus;
- other editions;
- the ancient versions;
- reception.

## §5 Parent table

Opening words are sliced from WEB by gen_strategy.py. The front-seam evidence names the text signal on each side, and the RP words either side of the seam are sliced by the same script. The last column counts RP pilcrows, SBL sign verses and RP-SBL differing verses inside the parent (MEASURED, gen_strategy.py; the column totals are 35 / 220 / 218).

| id | span | verses | opening words (WEB, sliced) | front seam, before \| after (RP sliced) | RP pilcrows / SBL sign verses / RP-SBL differing verses inside |
|---|---|---|---|---|---|
| P01 | 1:1-1:9 | 9 | Paul, called to be an apostle of Jesus ... | book start \| prescript 1:1 (frame formula, both witnesses). (book start) \| Παῦλος κλητὸς ἀπόστολος Ἰησοῦ | 1 / 3 / 2 |
| P02 | 1:10-4:21 | 82 | Now I beg you, brothers, through the name ... | 1:9 closing affirmation of the thanksgiving \| 1:10 appeal formula with vocative; RP pilcrow informs. 1:9 ...τοῦ κυρίου ἡμῶν. \| 1:10 Παρακαλῶ δὲ ὑμᾶς, ἀδελφοί,... | 9 / 34 / 39 |
| P03 | 5:1-5:13 | 13 | It is actually reported that there is sexual ... | 4:21 closing question of the visit threat 4:18-4:21 \| 5:1 report formula, asyndeton, new topic; no RP pilcrow. 4:21 ...πνεύματί τε πρᾳότητος; \| 5:1 Ὅλως ἀκούεται ἐν ὑμῖν... | 1 / 9 / 9 |
| P04 | 6:1-6:20 | 20 | Dare any of you, having a matter against ... | 5:13 closing citation-imperative \| 6:1 asyndetic question, new topic; no RP pilcrow. 5:13 ...ἐξ ὑμῶν αὐτῶν. \| 6:1 Τολμᾷ τις ὑμῶν, πρᾶγμα... | 1 / 9 / 9 |
| P05 | 7:1-7:24 | 24 | Now concerning the things about which you wrote ... | 6:20 closing imperative (glorify God) \| 7:1 peri de heading naming the Corinthians' letter. 6:20 ...ἐστιν τοῦ θεοῦ. \| 7:1 Περὶ δὲ ὧν ἐγράψατέ... | 1 / 13 / 14 |
| P06 | 7:25-7:40 | 16 | Now concerning virgins, I have no commandment from ... | 7:24 calling refrain closes 7:17-7:24 \| 7:25 peri de heading; RP pilcrow informs. 7:24 ...μενέτω παρὰ θεῷ. \| 7:25 Περὶ δὲ τῶν παρθένων... | 1 / 11 / 10 |
| P07 | 8:1-11:1 | 74 | Now concerning things sacrificed to idols: We know ... | 7:40 closing first-person opinion \| 8:1 peri de heading. 7:40 ...πνεῦμα θεοῦ ἔχειν. \| 8:1 Περὶ δὲ τῶν εἰδωλοθύτων,... | 2 / 43 / 48 |
| P08 | 11:2-11:16 | 15 | Now I praise you, brothers, that you remember ... | 11:1 imitation command echoing 10:33 closes 10:31-11:1 \| 11:2 praise formula plus tradition vocabulary; RP pilcrow informs. 11:1 ...καθὼς κἀγὼ χριστοῦ. \| 11:2 Ἐπαινῶ δὲ ὑμᾶς, ἀδελφοί,... | 1 / 7 / 6 |
| P09 | 11:17-11:34 | 18 | But in giving you this command I don't ... | 11:16 appeal to the churches' custom closes \| 11:17 negated praise formula; RP pilcrow informs. 11:16 ...ἐκκλησίαι τοῦ θεοῦ. \| 11:17 Τοῦτο δὲ παραγγέλλων οὐκ... | 1 / 12 / 11 |
| P10 | 12:1-14:40 | 84 | Now concerning spiritual things, brothers, I don't want ... | 11:34 closing deferral to the visit \| 12:1 peri de heading plus disclosure formula. 11:34 ...ἂν ἔλθω, διατάξομαι. \| 12:1 Περὶ δὲ τῶν πνευματικῶν,... | 7 / 41 / 36 |
| P11 | 15:1-15:58 | 58 | Now I declare to you, brothers, the Good ... | 14:40 order maxim closes \| 15:1 disclosure formula plus tradition vocabulary; no RP pilcrow. 14:40 ...κατὰ τάξιν γινέσθω. \| 15:1 Γνωρίζω δὲ ὑμῖν, ἀδελφοί,... | 5 / 25 / 24 |
| P12 | 16:1-16:18 | 18 | Now concerning the collection for the saints: as ... | 15:58 closing hoste-vocative exhortation \| 16:1 peri de heading. 15:58 ...κενὸς ἐν κυρίῳ. \| 16:1 Περὶ δὲ τῆς λογίας... | 3 / 9 / 6 |
| P13 | 16:19-16:24 | 6 | The assemblies of Asia greet you. Aquila and ... | 16:18 commendation close \| 16:19 third-person greeting formula; RP pilcrow informs. 16:18 ...οὖν τοὺς τοιούτους. \| 16:19 Ἀσπάζονται ὑμᾶς αἱ ἐκκλησίαι... | 2 / 4 / 4 |

Each back seam is the next parent's front seam, so every seam is assessed from both sides in the row that names it.

Row-onset candidates inside each parent. These are candidates only; a writer adopts one only where the text's own signal holds on both faces:
- P01: 1:4 (thanksgiving formula).
- P02: 1:17 or 1:18 (§7 I), 1:26, 2:1, 2:6, 3:1, 3:5, 3:10, 3:16, 3:18, 4:1, 4:6, 4:14.
- P03: 5:6, 5:9.
- P04: 6:9, 6:12 (the slogan pair holds 6:12-6:13 in one row).
- P05: 7:8, 7:10, 7:12, 7:17.
- P06: 7:32, 7:36, 7:39.
- P07: 8:4, 8:7, 9:1, 9:3, 9:15, 9:19, 9:24, 10:1, 10:14, 10:23, 10:31.
- P08: 11:3 is not an onset (D2). The writer tests one interior seam on the text alone.
- P09: 11:23, with the gar link back to 11:22 disclosed. No seam at 11:26/11:27.
- P10: 12:4, 12:12, 12:27, 13:1, 13:4, 13:8, 14:1, 14:6, 14:13, 14:20, 14:26, 14:34, 14:37.
- P11: 15:12, 15:20, 15:29, 15:35, 15:42, 15:50 or 15:51, 15:58. No seam at 15:7/15:8.
- P12: 16:5, 16:10, 16:12, 16:13, 16:15.
- P13: 16:21, 16:23.

## §6 unit_type vocabulary, granularity and over-split risk

Vocabulary. Each row carries exactly one type:
- `frame_prescript`
- `frame_thanksgiving`
- `frame_closing`
- `appeal`
- `report_response`
- `topic_response` (a peri de row)
- `argument_step`
- `objection_reply` (an imagined questioner, e.g. 15:35 "Ἀλλ’ ἐρεῖ τις,")
- `example` (an illustrative case: the apostle's own conduct in chapter 9, Israel in 10:1-10:13)
- `inset` (chapter 13)
- `tradition_with_application`
- `slogan_with_response`
- `exhortation`
- `travel_and_commendation`

The type names never adjudicate a reading. Chapter 9 is typed `example`, not "digression", because whether it digresses is itself a divided reading.

Granularity: one row per complete argumentative move. A row opens only where the text's own signal holds on both faces (§5 candidates). It never opens at a pilcrow alone, a WEB paragraph start, or a chapter division.

Over-split risk, with each measured temptation:
- the vocative adelphoi (22 RP verses);
- "do you not know" (ten);
- verse-initial hoste (12 RP verses: 1:7, 3:7, 3:21, 4:5, 5:8, 7:38, 10:12, 11:27, 11:33, 14:22, 14:39, 15:58; MEASURED, gen_strategy.py).

Most of these hoste verses conclude inside a move. 11:27 lies inside the tradition-with-application block (D6).

Under-split risk: a row that keeps a whole parent such as P10 12:1-14:40 or P11 15:1-15:58 together hides the 14:33b-36 disclosure and the 15:50/15:51 question. Those rows must stand alone (§7).

## §7 Low-confidence regions

Grades: **A**, a tier-1 text signal on both faces; **B**, a tier-1 signal on one face with the other face inferred from sense or a weaker device; **C**, contested, so the row discloses the rival reading. The grades are expectations for the review lanes (INFERRED).

**A. 8:1-11:1 idol-food argument with the ch 9 digression** (scrutiny target 1).
- One parent, P07 8:1-11:1 (grade A).
- Rows may open at 9:1, "Οὐκ εἰμὶ ἀπόστολος; Οὐκ εἰμὶ ἐλεύθερος;" (asyndetic questions, SBL order inverted), and at 10:1, "Οὐ θέλω δὲ ὑμᾶς ἀγνοεῖν, ἀδελφοί,". Each such row states that it lies inside the idol-food argument (grades B).
- 10:14 combines Dioper with the vocative "my beloved"; RP carries a pilcrow there (B).
- 10:23 repeats the slogan (D5) (B).
- 10:31-11:1 closes the argument, and 11:1 belongs with it by the echo of 10:33. The chapter division at 11:1 and the WEB paragraph start at 11:1 never drive (11:1/11:2, A).
- Divided readings: none are recorded by the scorer for this region. Rows report the ch 9 function neutrally (§6).

**B. 12:1-14:40 with ch 13 inset and 14:33b-36 text-critical block** (scrutiny target 2).
- One parent, P10 12:1-14:40 (A).
- 12:31 holds two clauses: "Ζηλοῦτε δὲ" ..., then "Καὶ ἔτι καθ’ ὑπερβολὴν ὁδὸν ὑμῖν δείκνυμι.". The first clause matches 14:1 "Διώκετε τὴν ἀγάπην· ζηλοῦτε δὲ"; the second points forward. Rows are verse-granular, so 12:31 goes with chapter 12, and the row discloses that 12:31b introduces chapter 13 (C).
- Chapter 13 is an `inset` row or rows (13:1, 13:4, 13:8; 13:13 closes) (B).
- 14:33/14:34: the asyndetic new subject at 14:34 is a text signal; the RP pilcrow informs (C). The row 14:34-14:36 (or a row through 14:40, if a writer finds no signal at 14:36/14:37) carries three disclosures:
  - the 14:33b attachment;
  - the SBL variant sites;
  - the transposition (§4).
  The rhetorical question at 14:36, "Ἢ ἀφ’ ὑμῶν ὁ", attaches backward (INFERRED).
- 14:36/14:37: 14:37 opens a conditional "if anyone thinks"; RP pilcrow (B).
- Divided readings (REPORTED, hardness_batch_03): cessationist and continuationist readings of 12-14; readings of "the perfect" at 13:8-13:12; 14:34-14:35 in debates over ordination. Rows name each reading and its holders without preferring one.

**C. 11:2-16 headship unit and 11:17-34 Supper tradition** (scrutiny target 3).
- Two parents, P08 11:2-11:16 and P09 11:17-11:34. The seam 11:16/11:17 is graded A: the churches' custom closes, and the negated praise opens.
- 11:22/11:23: the tradition opens "Ἐγὼ γὰρ παρέλαβον ἀπὸ τοῦ κυρίου", but its gar ties it to 11:22 (B). A single row 11:17-11:34 is acceptable.
- 11:26/11:27 is never a row seam (D6).
- The 11:24 witness difference is disclosed (§3).
- Divided readings (REPORTED): kephale and head coverings, read differently across traditions; the Eucharist at 11:23-11:34, read in Catholic, Orthodox, Lutheran, Reformed and memorialist ways. Each reading is named and attributed, none is preferred, and none moves a seam.

**D. 15:1-58 creed 15:3-7, sequence 15:20-28, mystery 15:50-58** (scrutiny target 4).
- One parent, P11 15:1-15:58 (A).
- The creed "Παρέδωκα γὰρ ὑμῖν ἐν πρώτοις," and the apostle's appended witness 15:8-15:11 stay in one row 15:1-15:11 (D6) (A).
- 15:12 is a conditional; RP pilcrow (B).
- 15:20 opens "But now", nyni de; RP pilcrow (B). The sequence 15:20-15:28 holds; the 15:23 "each in his own order" is interior.
- 15:29 opens Epei; RP pilcrow (B).
- 15:35, "Ἀλλ’ ἐρεῖ τις,", is an objection opener; RP pilcrow (B).
- 15:50 against 15:51: "Τοῦτο δέ φημι, ἀδελφοί," against "Ἰδού, μυστήριον ὑμῖν λέγω·". 15:50 is pilcrow-only, and touto de phemi opens at 7:29 as well. The working answer opens a row at 15:50, and the row discloses the backward reading (C).
- 15:57 "thanks be to God" and 15:58 close (A).
- Divided reading (REPORTED): baptism for the dead at 15:29, read differently by Latter-day Saint and mainstream traditions. Named, attributed, not adjudicated.

**E. slogan quotations 6:12-20, 7:1, 8:1-8, 10:23** (scrutiny target 5).
- The extent convention is C3 (§10).
- MEASURED (s03_probe.py quotes): 35 WEB verses carry double quotes. The WEB places slogan quotes at 6:12, 6:13, 6:18 and 10:23, and none at 7:1, 8:1, 8:4 or 8:8. This WEB punctuation is excluded from every extent decision.
- Text signals for extent:
  - the repeated wording: "Πάντα μοι ἔξεστιν," at 6:12 and 10:23 in RP;
  - the adversative that begins the response, "ἀλλ’ οὐ πάντα συμφέρει·";
  - at 6:13, "Τὰ βρώματα τῇ κοιλίᾳ,", the response begins with a contrasting clause.
- At 7:1 ("it is good for a man..."), 8:1 ("οἴδαμεν ὅτι"), 8:4 and 8:8, whether a slogan is quoted, and how far, is contested.
- Rows keep the candidate slogan and its response together and disclose "slogan extent contested" with the candidate extents.
- Expected grade per slogan row: B, with disclosure mandatory.
- Divided readings (REPORTED): ethics debates over 6:9-6:11. Named and attributed only.

**F. ch 7 topical sub-seams 7:1, 7:8, 7:10, 7:12, 7:25, 7:36** (scrutiny target 6).
- Two parents, P05 7:1-7:24 and P06 7:25-7:40.
- 7:1 is the heading (A).
- 7:8, "Λέγω δὲ τοῖς ἀγάμοις", is pilcrow-only and opens the addressee series (B).
- 7:10 "to the married" and 7:12 "to the rest" continue that series (B each). The 7:10-7:11 command cites the Lord, and 7:12 marks "I, not the Lord". The two rows stay distinct.
- 7:17-7:24 is closed by the calling refrain (7:20, 7:24). 7:24/7:25 is graded A.
- 7:36 opens a conditional case (B).
- Divided reading (REPORTED): divorce and the Pauline privilege at 7:10-7:16. Named and attributed only.

**G. 16:1-24 collection, travel, greetings, maranatha** (scrutiny target 7).
- Two parents, P12 16:1-16:18 and P13 16:19-16:24.
- 15:58/16:1 is graded A.
- 16:12, "Περὶ δὲ Ἀπολλὼ τοῦ ἀδελφοῦ,", is a row onset, not a parent seam (B).
- The closing edge is contested: 16:19 is adopted on the greeting formula. 16:13 begins imperatives, and 16:15 is an appeal followed by a commendation. 16:18/16:19 is graded B and goes to Fable.
- 16:21, the autograph "Ὁ ἀσπασμὸς τῇ ἐμῇ χειρὶ Παύλου.", is a row onset inside P13.
- 16:22, curse and maranatha, is disclosed per §3.
- 16:23 is the benediction. 16:24 is the love closing; RP adds the amen.

**H. Boundary risks in the hardness entry, each disposed:**
- 1:10-4:21 as one section: one parent, P02.
- 8:1-11:1 with ch 9 embedded: one parent, P07; no parent seam at 9:1 or 10:1.
- 12-14 with 13 inset: one parent, P10.
- 15 as one argument: one parent, P11.
- Slogan-refutation pairs: D5 and C3.
- Tradition-plus-application blocks: D6.

**I. My own finds:**
- I1. 1:17/1:18. 1:17, "for Christ did not send me to baptize", hinges the divisions report to the word of the cross. 1:18 is pilcrow-only and no WEB start. Choose one row seam, at 1:17 or 1:18, and disclose the hinge (C).
- I2. 4:14-4:21. A paternal admonition with Timothy's sending (4:17) and the threatened visit (4:18-4:21). It closes P02; a writer may make it one row. It is not a parent of its own, because nothing opens at 4:14 except the RP pilcrow and a self-referential "I write these things" (B).
- I3. 5:13/6:1. The citation-imperative close and the asyndetic new topic (B). The vice lists of 5:10-5:11 and 6:9-6:10 tie the parents in sense (INFERRED). The row at 6:9-6:11 discloses the link.
- I4. 9:1 wording. The question order is inverted between the witnesses (§3). Any WEB quotation discloses it.
- I5. 14:39-14:40. 14:39 repeats zeloute and the hoste-vocative closer. 14:40 closes the parent with the order maxim, and SBL adds de at 14:40, a variant site.
- I6. Divided readings outside the targets (REPORTED): purgatory and 3:10-3:15; discipline at 5:1-5:13. Named and attributed only.

## §8 Register and hygiene (copy verbatim into every writer brief)

1. Spans are written C:V-C:V with an ASCII hyphen on the WEB face. WEB, RP and SBLGNT numbering are identical in 1 Corinthians. Never write a dual span, an oshb: token or an mt: token.
2. Quote Greek only from Robinson-Pierpont, sliced by script from the staged file. Quote SBLGNT only to disclose a differing reading on which the row's argument rests. Never type Greek by hand. Never restore any other script for maranatha.
3. Quote English only from the WEB, sliced by script.
4. WEB paragraphs, chapter and verse divisions, footnote sites, capitalisation, punctuation and quotation marks never drive or corroborate a boundary.
5. An RP pilcrow informs and never decides. An SBL sign marks a variant site and nothing else. Never conflate the three mark types.
6. Rows never straddle a parent seam.
7. A slogan and its response stay in one row. A tradition and its application stay in one row.
8. Where a slogan's extent is contested, say so and give the candidate extents.
9. A divided reading is reported neutrally: name the reading and its holders, attribute it, never prefer one, and never let it move a seam.
10. Cross-tradition material is metadata in prose only. This covers the Western order of 14:34-14:35, the apparatus, other editions, the ancient versions and reception.
11. Every count and claim carries its tier: MEASURED (name the script), EXTRACTED, TRANSCRIBED, REPORTED, INFERRED, ASSUMED or UNAVAILABLE. Every number is a 1 Corinthians measurement or labelled lineage.
12. Disclose on the row:
    - the SBL reading where the argument rests on differing wording;
    - the 14:33b attachment and the transposition on the row holding 14:33-14:36;
    - the backward reading on the row opening at 15:50;
    - the hinge on the row opening at 1:17 or 1:18.
13. Write descriptively and in the third person, in plain prose, with no devotional or polemical voice and no claim beyond the text and the named evidence.
14. Carry both attribution lines (§3) with any quotation.
15. Row prose must not reproduce an unquoted witness run (convention C2).

## §9 Writer part table

| id | span | verses | parents | internal parent seams |
|---|---|---|---|---|
| W1 | 1:1-4:21 | 91 | P01, P02 | internal parent seam 1:9/1:10 |
| W2 | 5:1-7:40 | 73 | P03, P04, P05, P06 | internal parent seam 5:13/6:1; internal parent seam 6:20/7:1; internal parent seam 7:24/7:25 |
| W3 | 8:1-11:1 | 74 | P07 | none |
| W4 | 11:2-11:34 | 33 | P08, P09 | internal parent seam 11:16/11:17 |
| W5 | 12:1-14:40 | 84 | P10 | none |
| W6 | 15:1-16:24 | 82 | P11, P12, P13 | internal parent seam 15:58/16:1; internal parent seam 16:18/16:19 |

Why six parts:
- Each part is a union of whole parents, so no writer receives half an argument.
- The parts balance review depth against the concentration of scrutiny targets:
  - W1 holds the frame and the divisions argument.
  - W2 holds the reported-conduct parents and both halves of chapter 7 (targets 5 and 6).
  - W3 holds the idol-food argument alone (target 1).
  - W4 holds the two worship-assembly parents (target 3). It is the smallest part, but it holds the densest divided readings: headship and the Supper.
  - W5 holds 12-14 alone (target 2).
  - W6 holds the resurrection argument, the business of chapter 16 and the closing frame (targets 4 and 7).
- Rivals considered:
  - Five parts, merging W4 into W3: rejected, because that part would hold two scrutiny targets and the heaviest reception load.
  - Seven parts, splitting W6 at 16:1: rejected, because P12 and P13 are short and depend on the 16:13/16:19 frame question, which one writer should see whole.

## §10 Self-checks and conventions

Self-checks run or required:
1. The validator _validate_strategy_1cor.py returns GREEN on this file and the plan (run by this lane; the result is in report.json).
2. Parents and parts each re-sum to 437 verses from verse_inventory.json (MEASURED by gen_strategy.py and independently by the validator).
3. The parent-table counts sum to 35 pilcrows, 220 sign verses and 218 differing verses (MEASURED, gen_strategy.py). That equals the book totals, so no verse is double-counted.
4. Every parent seam names a text signal on at least one face. No seam rests on a WEB mark, a chapter division or an SBL sign (by construction of §5; checked by reading).
5. Every opening-word cell and every Greek or English quotation in this file was sliced by script. The ledger is in quote_ledger.json.

Conventions as testable patterns. Each needs the check named, installed before writers run:

- **C1, mark direction.** In the 1 Corinthians pmarks, rp_paragraph_starts and web_paragraph_starts record a mark at the paragraph's FIRST verse. That is the opposite direction from the method record's Hebrew convention, where a mark is recorded on the verse it follows.
  - Check: assert that 1Cor.1.10 is in rp_paragraph_starts and 1Cor.1.9 is not, and that every consumer reads the list as onsets.
- **C2, Greek-witness unquoted-run predicate** (stated here as the first book with a Greek witness, per the method record). Per witness, RP and SBL separately:
  - Tokenisation: Unicode NFD; drop combining marks; casefold; final sigma folded; SBL sign characters, elision marks and punctuation removed; split on whitespace.
  - Run length: a run of 4 or more consecutive tokens.
  - Fields scanned: every free-prose field of a row (title, summary, rationale, disclosure notes). Fields that carry a script-sliced quotation with its witness tag are excluded.
  - Witness verses compared: the verses of the row's span, plus one verse on each side.
  - Violation: a run in a scanned field that matches a contiguous run of the witness text of those verses.
  - Calibration: RP has 5514 distinct 4-token runs, of which 72 recur in more than one verse (MEASURED, gen_strategy.py). Hence the comparison is limited to the span and its neighbours, so that formulaic recurrences elsewhere do not fire.
  - The run length 4 and the neighbour width 1 are ASSUMED parameters, sent to Fable.
  - Whether a tool implements this is not settled here.
- **C3, slogan extent.** A slogan's extent is decided only by Greek text signals in RP:
  - verbatim repetition across sites;
  - the adversative or contrasting clause that begins the response;
  - a change of person;
  with SBL disclosed where its wording differs (10:23). WEB quotation marks never count.
  - Check: no row seam at 6:12/6:13, 6:13/6:14, 10:23/10:24, 7:1/7:2, 8:1/8:2, 8:4/8:5 or 8:8/8:9.
  - Check: every row holding 7:1, 8:1, 8:4 or 8:8 carries a "slogan extent contested" disclosure.
- **C4, heading onsets.** Each verse in TOPIC_MARKER_PAIRS (7:1, 7:25, 8:1, 12:1, 16:1, 16:12) is the first verse of a row.
  - Check: set inclusion against the row starts.
- **C5, SBL difference disclosure.** A row whose argument quotes RP wording at a verse in rp_sbl_differences, where the quoted words fall on or across an SBL sign, carries an SBL disclosure.
  - Check: for each sliced RP quote, test sign overlap and require an sbl: token or an "SBL reads" note in the same row.
- **C6, frame typing.** The rows of P01 1:1-1:9 carry frame_prescript or frame_thanksgiving, and the rows of P13 16:19-16:24 carry frame_closing. No other row carries a frame type.
  - Check: type by span.
- **C7, tradition and slogan integrity.** No row seam at 11:26/11:27 or 15:7/15:8.
  - Check: row-start exclusion list.
- **C8, maranatha.** The row holding 16:22 contains the RP form and the SBL division.
  - Check: string presence of both slices in that row.
- **C9, 14:33b-36 disclosure.** The row or rows holding 14:33-14:36 carry the attachment, SBL-site and transposition disclosures. No seam rationale cites the transposition.
  - Check: required phrases present, and a forbidden reference in seam rationale.

## §11 Lens record

Lens count: **3** (OW-19).
- Two blind lanes are the floor.
- The third is the RECEPTION_TRADITION kind, one of the three decorrelating kinds the readiness record lists. The others are CROSS_BOOK and ORIGINAL_LANGUAGE_OR_VERSIONAL; that mapping is INFERRED by the readiness record.

Why reception: two of the three severe axes, ecclesial contestedness and connections, bear on row prose. A neutrality breach in the densest divided-reading rows is the costliest defect class here:
- 11:2-11:34;
- 12:1-14:40;
- the 14:33-14:36 block.
The reception lens checks those rows against convention C3, §8 items nine and ten and the §4 cross-tradition scope.

Rejected alternatives:
- CROSS_BOOK, the citation and Jesus-tradition links (7:10-7:11, 9:14, 11:23-11:25), which bear on extents.
- ORIGINAL_LANGUAGE_OR_VERSIONAL, the witness-split cruxes.
Both are carried as checks instead: D6, C5 and §3.

Model downgrade (device item 8): every role runs on claude-opus-5-5 under OW-25 grader_fallback. Model-family decorrelation is UNAVAILABLE (EXTRACTED, grader_models.v1.json). The third lens is decorrelated by kind only. A 2-1 split among same-family lanes is not a majority, and Fable's end review rules on any such split.

## Provenance and limits

- Inputs: the 18 pinned files named in the brief, opened by exact path and digest-verified (inputs_verified.json).
- Scripts, all in OUT and read-only on pinned files:
  - verify_inputs.py
  - s01_inventory.py
  - s02_devices.py
  - s03_probe.py
  - gen_strategy.py
- No listing, glob or recursive search was run (E-19). No git, receipt or registry action was taken.
- Not checked:
  - the SBLGNT apparatus contents (not staged; the variant readings at 2:1 and elsewhere are UNAVAILABLE);
  - any reception claim beyond the scorer's list (REPORTED, not re-verified);
  - the sense-level links marked INFERRED (the vice-list tie 5:10-5:11 / 6:9-6:10, the freedom vocabulary between chapters 8 and 9, the backward attachment of 14:36);
  - whether a tool for C2 exists.
- The WEB text was measured as staged. The scorer's note that the WEB is a Majority Text rendering is REPORTED and was not tested. The 9:1 order shows the WEB departing from RP at least once (MEASURED).
- The grades in §7 are expectations (INFERRED), not review outcomes.
