# Ezekiel book strategy (M8_fable, m8-mesh-r3) — fable-authored, Phase 1 candidate

- attempt_id `ezek_strategy_a1`, execution_id `ezek_strategy_a1#e1`. Candidate-only, NON-AUTHORIZING
  research on the OW-6b HARD-BOOK TRACK: Fable is the controlling agent, peer and spot coverage are
  raised, the flagged regions (§7) get no sampling shortcut, and a second independent Fable review of
  the flagged regions runs before the close.
- Substrate: WEB (T421 canonical USFM) + OSHB/WLC (T430 lane), staged and Phase-0 verified at
  sp_durable/Ezek/ (book facts, numbering crosswalk, parashah/paseq/K/Q/note inventories and the
  formula spine are CONSUMED here, not re-derived). Every count below that is not from a staged
  inventory names the sweep that produced it (consonantal-skeleton regex over the staged MT extract,
  NFD-stripped `[֑-ׇ]`, verses-containing-the-form).
- Status: no theology, no canon/authorship/redaction positions (the "school of Ezekiel", a
  Palestinian versus Babylonian setting, and the relation of chs 40-48 to the Priestly legislation are
  never argued or assumed), no preferred readings. Interpretive alternatives are uncertainty under the
  schema, not errors.

## §1 Objective and shape

Tile all 1,273 WEB verses of Ezekiel (48 chapters; MT and WEB totals equal; ONE renumbering zone, §3)
into adversarially reviewed candidate chunk rows under the r3 HYBRID shape, sized to a
prose-dominant prophetic book (487 `|q` poetry lines in 12 of 48 chapters; 36 chapters carry none —
sweep of the WEB extract's ` |q` lines per chapter banner).

What Ezekiel IS, structurally, from the bytes: a first-person book (the prophet narrates; "he said to
me" ויאמר אלי opens 36 verses, sweep) built from **dated vision-and-oracle complexes**. Fourteen
verses carry a regnal/exilic YEAR formula — the thirteen in the staged inventory (MT 1:1, 1:2, 8:1,
20:1, 26:1, 29:1, 29:17, 30:20, 31:1, 32:1, 32:17, 33:21, 40:1) plus **MT 24:1**, which the inventory
omits (§2, §7, and the final record). Between the datelines the text is a chain of formula-framed
oracles: 49 verses carry the word-event formula in some form (39 in the strict contiguous form the
inventory counts, plus 10 in the dateline-bearing or interrupted forms, §2a), each unit typically
opened by the address "son of man" (93 verses) and closed by a recognition refrain or the utterance
signature. Four long prose visions (1:1-3:15; 8:1-11:25; 37:1-14; 40:1-48:35) are marked at onset by
the hand-of-YHWH idiom and internally by transport verbs ("he brought me", 20 verses, sweep) rather
than by oracle formulae. Poetry is confined to lament and oracle-against-nation texture (chs 18, 19,
21, 23, 24, 26-32).

A chunk row here is a **formula-bounded literary unit**: one oracle, one sign-act with its
interpretation, one lament, one vision scene or measurement circuit, one law paragraph, one allotment
list — bounded by the prophetic frame spine (§2) and never straddling a parent seam (§5). The
architecture of this strategy is the eight-parent, byte-anchored division in §5 with a hard-seam
layer (every dateline and vision onset) inside it.

Wave shape (r3 HYBRID, scaled): (1) whole-book writer wave over the 11 parent-aligned parts of §9,
gated by the Tier-0 validator suite (nfd HARD per E-01, cap_sweep HARD per E-02, E-15/E-16 arms, the
numbering-zone dual-ref arm, the Aramaic-label arm); (2) FULL dual-blind primaries (LF + OL) over ALL
rows in clusters of <=8; (3) r3-scoped peer round (challenged rows + a raised sample — no sampling
shortcut inside the §7 regions), boss rulings, consolidation emitting the explicit corpus_wide_orders
list (E-18); (4) author wave consuming peer remedies as work orders, validator re-run for mechanical
classes, a fresh full second-generation sweep with a checker distinct from the authors after every
repair wave (OW-2 item 4), every CWO as its OWN sweep (E-18 parity); (5) ONE book-level spot wave with
the dedicated lanes (cross-part seam, second-generation checklist E-17, the E-23 punctuation lane,
the B-8 LF-SUPPORT AUDIT LANE BY DEFAULT) plus the OW-6b second independent Fable review of §7; (6)
ONE postcheck and the hard-gated close under CAMPAIGN_CLOSE_GATE.v1.md items 5-6 and 8.

## §2 Device matrix (consume ezek_device_inventory.json; counts below are that file's unless a sweep is named)

### §2a The prophetic frame spine (tier-1: the seam skeleton) — literary_form_decision_matrix

| form | inventory verses | ROLE ruled here |
|---|---|---|
| word-event formula ויהי דבר יהוה אלי לאמר | 39 | **ONSET** of an oracle unit (default row onset) |
| "son of man" בן אדם | 93 | address; onset corroboration, never an onset alone (it recurs inside units: 8:5-17 ×6, 33:2-30 ×6) |
| messenger formula כה אמר אדני יהוה | 122 | opens a SPEECH inside a unit; a sub-onset only when the addressee changes or a close stands before it |
| utterance formula נאם אדני יהוה | 81 | **CLOSE** (oracle-final signature); mid-unit occurrences are paragraph-final, not row-final, unless a fresh onset follows |
| recognition formula וידעו כי אני יהוה | 28 | **CLOSE** — the refrain closes the unit BEFORE it (standing rule) |
| 2ms variant וידעת כי אני יהוה | 5 | **CLOSE** |
| "I YHWH have spoken" אני יהוה דברתי | 14 | emphatic **CLOSE** (often stacked with the utterance formula: 24:14, 26:14) |
| hand-of-YHWH יד יהוה / יד אדני יהוה | 7 | **ONSET** of a vision (1:3, 3:22, 8:1, 37:1, 40:1); at 3:14 it is transit texture, at 33:22 the mouth-opening event — neither opens a vision (§7) |
| "set your face" שים פניך | 9 | direction opener of a sign-act or oracle; onset corroboration, follows a word-event in 8 of 9 (13:17 follows "and you, son of man") |
| ORACLE DATELINES (year-bearing) | 13 (+1, below) | **ONSET of the first order**; every dateline is a HARD seam (rows never straddle) |

**Complementary sweeps (skeleton regex over the staged MT extract; not replacements for the
inventory, labelled so the digits stay separable):**

- `דבר יהוה אל` any form: **49 verses** = the 39 strict + 1:3 (הָיֹ֣ה הָיָ֣ה דְבַר יְ֠הוָה — infinitive
  absolute + perfect, third person, the superscription) + 12:8 (בַּבֹּ֥קֶר interrupts) + **24:1** (the date interrupts) + the seven
  dateline-bearing perfects at 26:1, 29:1, 29:17, 30:20, 31:1, 32:1, 32:17 (הָיָ֥ה דְבַר יְהוָ֖ה אֵלַ֥י
  לֵאמֹֽר after the date). Rule: every one of the 49 is a word-event ONSET for row purposes; the
  inventory's 39 is the strict-form subset and is cited as such.
- **MT 24:1 is a year-bearing dateline**: וַיְהִי֩ דְבַר יְהוָ֨ה אֵלַ֜י בַּשָּׁנָ֤ה הַתְּשִׁיעִית֙ בַּחֹ֣דֶשׁ הָעֲשִׂירִ֔י
  בֶּעָשׂ֥וֹר לַחֹ֖דֶשׁ לֵאמֹֽר — "in the ninth year, in the tenth month, on the tenth of the month". It
  satisfies the inventory's own gloss ("a date formula carrying a regnal/exilic YEAR") and is absent
  from both the `dated_oracles` list (13) and the `word_event_formula` list (39) because the year
  clause splits the contiguous pattern. This strategy treats MT 24:1 as a dateline-grade onset and
  hard seam; the inventory discrepancy is reported upward, not patched here (sweep: `שנה`, 19 verses,
  of which 14 are year-formulae and 5 are durations — 4:6, 26:10, 29:11, 29:12, 29:13).
- Recognition family, wider: `ידע…כי אני יהוה` in one verse, **64 verses**; of these the 2mp form
  וידעתם כי אני יהוה = **21 verses** (6:7, 6:13, 7:4, 7:9, 11:10, 11:12, 12:20, 13:14, 14:8, 15:7, 17:21,
  20:38, 20:42, 20:44, 22:22, 25:5, 35:9, 36:11, 37:6, 37:13, 37:14) is NOT in the inventory and is the
  dominant close in the Israel-addressed oracles of chs 6-22; the "nations shall know" and "house of
  Israel shall know" expansions (28:26, 34:30, 37:28, 39:7, 39:22, 39:28) are in the 64. Rule: any
  member of the 64 is refrain-grade close evidence; the inventory's 28+5 are cited as the strict
  forms.
- Short forms: נאם יהוה without אדני **4 verses** (13:6, 13:7, 16:58, 37:14); כה אמר יהוה without
  אדני **3 verses** (11:5, 21:8 MT, 30:6). Both count as their long-form roles.
- Oath חי אני **16 verses** (13 with the utterance signature attached) — an emphatic sub-onset of a
  verdict paragraph, never a row onset alone.
- הנני אליך/עליך "behold, I am against you" **14 verses** — verdict onset inside a unit (OAN-dense:
  26:3, 28:22, 29:3, 29:10, 30:22, 35:3, 38:3, 39:1).

### §2b Vision devices (tier-1 inside the four visions) — scene_participant_location_change
- Hand-of-YHWH onsets: 1:3 (וַתְּהִ֥י עָלָ֛יו שָׁ֖ם יַד יְהוָֽה), 3:22, 8:1 (וַתִּפֹּ֤ל עָלַי֙ שָׁ֔ם יַ֖ד אֲדֹנָ֥י
  יְהֹוִֽה — the אדני form, why the inventory matches the construct alone), 37:1, 40:1.
- Transport verbs "he brought me / led me out / set me down / the Spirit lifted me": **20 verses**
  (8:3, 8:7, 8:14, 8:16, 11:1, 11:24, 37:1, 40:1, 40:17, 40:28, 40:32, 40:35, 41:1, 42:1, 43:5, 44:4, 46:19,
  47:1, 47:2, 47:6; sweep) — the scene-change skeleton of chs 8-11 and 40-48; a row seam inside a
  vision sits ON a transport verse or a "he said to me" verse, never mid-scene.
- "He said to me" ויאמר אלי **36 verses** (sweep); "in visions of God" במראות אלהים **3 verses** (1:1,
  8:3, 40:2 — the three vision-transport frames); "the river Chebar" **8 verses** (1:1, 1:3, 3:15, 3:23,
  10:15, 10:20, 10:22, 43:3 — the inclusio device tying 10 and 43 back to 1); "I fell on my face" **5
  verses** (1:28, 3:23, 11:13, 43:3, 44:4); "the glory of YHWH" כבוד יהוה **9 verses** (1:28, 3:12, 3:23,
  10:4, 10:18, 11:23, 43:4, 43:5, 44:4 — the departure/return arc).
- Measurement: וימד "and he measured" **21 verses** (40:5-41:5 ×18, 47:3-5 ×3); the wider מדד/מדה
  family **40 verses** (sweep). This is the texture of the temple_measurement unit type (§6).

### §2c Genre labels the text itself supplies (tier-1 for unit_type)
- קינה "lament" **8 verses** (19:1, 19:14, 26:17, 27:2, 27:32, 28:12, 32:2, 32:16; sweep) — the
  qinah colophon at 19:14 קִ֥ינָה הִ֖יא וַתְּהִ֥י לְקִינָֽה and at 32:16 קִינָ֥ה הִיא֙ are CLOSES.
- משל "parable/proverb" **11 verses** (12:22, 12:23, 14:8, 16:44, 17:2, 18:2, 18:3, 19:11, 21:5 MT, 24:3,
  42:6 — the last is a homograph "taken away from", not the genre word); חידה **1 verse** (17:2).
- "And you, son of man" ואתה בן אדם **23 verses** (sweep) — the sub-onset that opens a new command
  WITHOUT a word-event (4:1, 5:1, 36:1, 39:1, 39:17 …); it is why 36:1 and 39:1 are chapter breaks
  that do not cut a word-event unit (§6).
- "Rebellious house" בית מרי / בית המרי **12 verses**, six of them in 2:5-3:27 and none in 4-11 — the
  commission's refrain; its last occurrence at 3:27 (כִּ֛י בֵּ֥ית מְרִ֖י הֵֽמָּה) is a refrain-grade CLOSE
  for parent P1 (§5).

### §2d Rulings on interaction
1. A refrain CLOSES a unit. When a recognition/utterance verse is immediately followed by a
   word-event or dateline verse, the seam falls between them and both sides are cited (e.g. 7:27 →
   8:1; 24:27 → 25:1; 32:32 → 33:1; 39:29 → 40:1).
2. **Dateline + word-event in one verse** (24:1, 26:1, 29:1, 29:17, 30:20, 31:1, 32:1, 32:17): one
   onset, cited as dateline-grade; the verse never splits.
3. **Dateline without a word-event** (1:1-2, 8:1, 20:1, 33:21, 40:1): the dateline opens a NARRATIVE
   frame (vision or scene); the first word-event after it (20:2; 33:23) opens the oracle INSIDE the
   frame and is a sub-onset, not a competing onset. 1:1-3 is one superscription (two datelines and a
   third-person word-event) and is never split across rows.
4. **Onset/close collision** (a close-formula verse that also carries onset material): 20:44 (2mp
   recognition + utterance, then MT 21:1 word-event) — no collision, the seam is at the verse boundary.
   Real collisions are the OAN verdict verses where הנני + messenger formula follow a recognition
   close inside one chapter (26:6 → 26:7; 28:23 → 28:24; 29:9 → 29:10 where the WEB even paragraphs
   mid-verse): the row seam sits at the verse boundary AFTER the close verse, and the mid-verse WEB
   paragraph at 29:9 is tier-4 and never cuts.
5. **The three festival-calendar dates at MT 45:20, 45:21, 45:25 are NOT datelines.** Bytes: 45:21
   בָּ֠רִאשׁוֹן בְּאַרְבָּעָ֨ה עָשָׂ֥ר יוֹם֙ לַחֹ֔דֶשׁ יִהְיֶ֥ה לָכֶ֖ם הַפָּ֑סַח (Passover, month and day, NO year);
   45:20 בְּשִׁבְעָ֣ה בַחֹ֔דֶשׁ; 45:25 בַּשְּׁבִיעִ֡י בַּחֲמִשָּׁה֩ עָשָׂ֨ר י֤וֹם לַחֹ֨דֶשׁ֙ בֶּחָ֔ג. They sit inside the
   temple-law paragraph opened by the messenger formula at 45:18 (which itself carries בָּֽרִאשׁוֹן֙
   בְּאֶחָ֣ד לַחֹ֔דֶשׁ, a calendar date, not an onset). None of the four opens anything; a row seam at
   45:20, 45:21 or 45:25 is a hard error. A day-formula sweep on the dateline phrasings
   (`בעשור לחדש|באחד לחדש|בחמשה לחדש|בשבעה לחדש|בשנים עשר לחדש|בחמשה עשר לחדש|בארבעה עשר`) hits 16
   verses: the fourteen year-bearing datelines plus 45:18 and 45:21 — the two calendar sites that
   share a dateline's day-phrasing without a year; 45:20 and 45:25 phrase the day differently.
6. Messenger formula clusters (36:2-7 ×6; 25:3-16 ×7; 13:3-20 ×5) mark paragraphs, not rows; a
   row is cut at a messenger formula only where the addressee changes (25:8 Moab after Ammon; 25:12
   Edom; 25:15 Philistia) or a refrain close stands immediately before it.

### §2e Texture and cohesion signals (staging; never row evidence alone)
Poetry `|q` lines per WEB chapter (sweep): 18 (43), 19 (46), 21 (55), 23 (10), 24 (38), 26 (8), 27
(68), 28 (75), 29 (14), 30 (55), 31 (27), 32 (48); zero elsewhere. WEB `[fn]` 38 sites (ch 45 alone
9). Divine-name texture: אדני יהוה dominates the frame (messenger 122 / utterance 81); the short forms
are rare (7 verses total, §2a). Repeated cross-unit refrains that argue continuity rather than a seam:
"my eye will not spare, I will not pity" **5 verses** (5:11, 7:4, 7:9, 8:18, 9:10); "my sanctuary"
מקדשי **18 verses**; "the mountains of Israel" **15 verses** (chs 6, 33-39 cluster). A byte-true device
straddling a proposed row seam (e.g. the ropes עבותים of 3:25 and 4:8 across the P1/P2 seam) is
disclosed as continuity evidence against the seam — the seam may still stand, but the disclosure is
mandatory.

### §2f Disclosure objects (MT-keyed inventories in pmarks_Ezek.json)
Parashah 113 samekh + 71 pe = 184 occurrences on 183 verses (MT 43:27 carries two consecutive samekh
segs — counted as two occurrences on one verse, never added to the verse count). **Chapters with ZERO
parashah marks: 10, 40, 41, 42** (tally over the marks list) — chs 40-42 (95 verses) carry no mark
at all, and the unmarked stretch from the pe at 39:29 to the samekh at 43:9 is 103 verses
(40:1-43:8); the temple-measurement rows are cut on
transport/measurement seams with no parashah corroboration available, and its absence is never
counterevidence. Paseq 136 segs / 121 verses, COUNT-ONLY (chs 40-42 carry 30, ch 48 carries 17).
K/Q 134 notes / 99 verses; the ch-16 cluster (11 verses / 17 notes — the archaic 2fs forms) and the
ch-40 cluster (14 verses / 35 notes — the gate-measurement nouns) are the two dense sites; 23
doubled-note verses per the toolkit. OSHB editorial notes 71 verses (37 are the ch-21 KJV-variance
layer). sof-pasuq 1,272 for 1,273 verses: MT 33:20 carries none (an untyped punctuation-divergence
note and then the pe) — disclosed by any row spanning it, never a boundary argument. **Puncta
extraordinaria: MT 41:20 and 46:22 only.** Absence proofs run for this strategy (code-point sweep of
the extract): U+05C4 upper dot present in exactly those two verses (5 and 7 marks: וְקִ֖יר הַׄהֵׄיׄכָֽׄלׄ;
מְׄהֻׄקְׄצָׄעֽׄוֹׄתׄ); U+05C5 lower dot 0; U+05C6 nun hafukha 0; U+05C0 paseq 0, U+05BE maqaf 0, U+05C3
sof-pasuq 0 (the last three confirm the extract drops those segs, exactly as the toolkit states — a
"no maqaf in the text" claim would be about the extract). NB the toolkit says the puncta live "in the
note layer, not in the verse bytes"; the staged extract in fact carries the dots AS combining marks
on the verse bytes at both sites, so a splice of either word carries U+05C4 and the row must disclose
it as single-witness (see the final record).

## §3 Numbering + language discipline

**NOT an identity book — one renumbering zone, a SHIFT not a gap (byte-proven three ways in
web_mt_offset_map.json; crosswalk injective, verdict GREEN):**

```
MT 21:1-5    =  WEB 20:45-49     (WEB ch 20 = 49 vv; MT ch 20 = 44)
MT 21:6-37   =  WEB 21:1-32      (WEB ch 21 = 32 vv; MT ch 21 = 37)
identity in every other chapter; totals equal at 1,273
```

Tier-0 ENFORCED: any structured ref touching WEB 20:45-49, WEB ch 21 or MT ch 21 carries an explicit
dual or numeric qualifier — `web:Ezek.20.45 = oshb:Ezek.21.1`, or `(MT 21:1)` after a `web:` ref — in
EVERY field where it appears, including device_notes prose. Bare coordinates are ambiguous exactly
there and only there. Convention: bare/`web:` refs and row spans = WEB; `oshb:`/pmarks/inventory refs
= MT. Convert with the offset map ALWAYS. This document itself follows the rule: unqualified refs
elsewhere are identity; inside the zone it writes both.

The zone is a seam site as well as a numbering site. Bytes: MT 21:1 (= WEB 20:45) is a word-event
onset וַיְהִ֥י דְבַר יְהוָ֖ה אֵלַ֥י לֵאמֹֽר; MT 21:5 (= WEB 20:49) closes with the prophet's complaint
הֲלֹ֛א מְמַשֵּׁ֥ל מְשָׁלִ֖ים הֽוּא and carries the pe; MT 21:6 (= WEB 21:1) is the next word-event. So WEB
20:45-49 = MT 21:1-5 is a complete five-verse unit (the forest-fire mashal) and WEB 21:1-5 = MT 21:6-10
its sword-interpretation (closing at MT 21:10 with וְיָֽדְעוּ֙ כָּל בָּשָׂ֔ר כִּ֚י אֲנִ֣י יְהוָ֔ה + samekh).
Expected row set in the zone, all dual-written: `web:Ezek.20.45-Ezek.20.49 = oshb:Ezek.21.1-Ezek.21.5`;
`web:Ezek.21.1-Ezek.21.5 = oshb:Ezek.21.6-Ezek.21.10`; `web:Ezek.21.6-Ezek.21.7 = oshb:Ezek.21.11-Ezek.21.12`
(sigh sign-act; utterance close + pe at MT 21:12); `web:Ezek.21.8-Ezek.21.17 = oshb:Ezek.21.13-Ezek.21.22`
(sword song; "I YHWH have spoken" at MT 21:22 + pe); `web:Ezek.21.18-Ezek.21.27 = oshb:Ezek.21.23-Ezek.21.32`
(two ways; pe at MT 21:28, 21:29, 21:32 — held, §7); `web:Ezek.21.28-Ezek.21.32 = oshb:Ezek.21.33-Ezek.21.37`
(Ammon; "I YHWH have spoken" at MT 21:37 + pe). The only K/Q in MT ch 21 is MT 21:28 (= WEB 21:23);
the only paseq in the five-verse shift is MT 21:3 (= WEB 20:47). Both are disclosed dual.

Arithmetic guard for writers: a span's verse count is computed from verse_inventory.json (WEB) and
cross-checked against the MT count via the map; inside the zone the two chapter numbers differ but
the count of any dual-written span is identical on both sides (injective map).

**Language: Hebrew throughout.** Morph prefixes are H only across 18,866 tokens; `aramaic_verses` is
empty. There is no Aramaic island (contrast oshb:Jer.10.11 — a different book; a bare "MT 10:11"
in this toolkit is Ezekiel's 10:11, a cherubim verse). Any Aramaic label on any Ezekiel verse, in
any field, is a hard error (the Aramaic-label validator arm flags it).

## §4 Marker policy + cross-tradition scope — source_metadata_evidence_only_check

Owner addendum weights bind: TEXT signals drive (dateline; word-event; hand-of-YHWH; transport verb;
"and you, son of man"; set-your-face; messenger formula with addressee change; recognition/utterance/
"I have spoken" closes; qinah/mashal labels; the muteness/mouth-opening arc 3:26 → 24:27 → 33:22).
Masoretic parashah marks are tier-3 single-witness EVIDENCE that informs and never decides: a pe or
samekh on the close verse of a proposed row is corroboration to disclose; a proposed seam with no
mark is not weakened; a mark with no formula (e.g. the samekh chain in 23:10-45, seven marks) is
disclosed and never cuts alone. PE is never conflated with SAMEKH. The mark is recorded on the verse
it follows; **intra-verse position is not carried by the inventory** — the pe recorded at MT 3:16
sits on the verse whose second clause is the book's first word-event formula, and whether the mark
follows the verse or falls inside it cannot be settled from the staged files (§7; XML by exact path
only). Chapter/verse divisions, WEB `¶` paragraphing, `|q` line breaks, `[fn]` sites, capitalization
and punctuation NEVER drive or corroborate a boundary (E-23); the WEB's mid-verse paragraphs (1:28,
3:3, 8:5, 8:8, 9:6, 9:7, 10:2, 11:24, 17:24, 29:9, 31:18, 37:3, 47:6, 47:15) are cited only in the E-23
lane as tier-4 texture.

Cross-tradition material is METADATA in prose only, never a `refs` entry, never boundary evidence,
never counterevidence: the Greek Ezekiel's shorter text and its differently ordered passage in ch 7,
the Greek witness (Papyrus 967) whose order in chs 36-39 differs from the MT, the Qumran Ezekiel
fragments and the Masada scroll, Targum/Peshitta/Vulgate. None of it is in the staged witnesses; a
row may name it in device_notes as context for a held question (36:23-38; 7:3-9) and may not use it
to move a seam. Intra-canon parallels (the watchman charge 3:16-21 // 33:1-9; the recognition
formula's Priestly kinship; Ezek 1 // 10 // 43) are tradition metadata; the Ezek 1/10/43 parallel
IS text-internal and is citable as the "river Chebar" inclusio (§2b) with its sweep digit.

## §5 Parent architecture (byte-anchored; R2) — eight parents, one hard-seam layer

Rule for a PARENT seam: (a) a dateline or hand-of-YHWH vision onset, or a word-event onset with an
addressee-class or genre-class shift, on the onset side; AND (b) a refrain-grade close, a genre
colophon, or a vision-return on the close side; AND (c) the tradition's five-block shape is tested
against, not assumed from, that evidence. Every dateline (14) and every vision onset is a HARD seam
inside its parent even where it is not a parent seam (rows never straddle a hard seam; parts may
subdivide a parent only at a hard seam). The traditional shape survives in modified form: the
"judgment on Judah" block splits into a sign-act/first-oracle complex, the temple vision, an undated
oracle collection and a dated collection; the "restoration" block begins at the addressee shift
(33:1), not at the fugitive's dateline (33:21).

| parent | span (WEB; identity except P5) | vv | onset evidence | close evidence | why the seam is here and not at the traditional alternative |
|---|---|---|---|---|---|
| **P1** inaugural vision and commission | Ezek.1.1-Ezek.3.27 | 65 | datelines 1:1-2; word-event 1:3 (perfect, 3rd person); hand-of-YHWH 1:3; vision "I saw" 1:4 | 3:27 refrain כִּ֛י בֵּ֥ית מְרִ֖י הֵֽמָּה (6th and last of the commission's six in 2:5-3:27; sweep 12 verses book-wide, none in 4-11); samekh after 3:27 | The competing seam 3:15/3:16 (seven-days close + word-event + pe) is a HARD seam inside P1; it does not become the parent seam because the muteness command 3:22-27 and the "ropes" of 3:25 are taken up at 4:8 — the commission's coda and the sign-acts are welded, and the refrain close at 3:27 is the last commission device. Held at §7. |
| **P2** sign-acts and the first judgment oracles | Ezek.4.1-Ezek.7.27 | 75 | 4:1 וְאַתָּ֤ה בֶן אָדָם֙ קַח לְךָ֣ לְבֵנָ֔ה (sign-act sub-onset; 23-verse family); unit type changes from narrative to commanded action | 7:27 וְיָדְע֖וּ כִּֽי אֲנִ֥י יְהוָֽה + pe; 8:1 is a dateline | Not merged with P1 because P2 has its own closes (5:13/5:15/5:17 "I YHWH have spoken" ×3, 6:14 and 7:27 recognition) and its own hard seams (word-events 6:1, 7:1). Not merged with P3 because 8:1 is a dateline + hand + transport. |
| **P3** the temple vision | Ezek.8.1-Ezek.11.25 | 76 | dateline 8:1 (sixth year); hand 8:1 (אדני form); transport 8:3 בְּמַרְא֣וֹת אֱלֹהִ֗ים | 11:24 return transport וַיַּ֨עַל֙ מֵֽעָלַ֔י הַמַּרְאֶ֖ה אֲשֶׁ֥ר רָאִֽיתִי + 11:25 report to the exiles; pe after 11:25 | One transported vision; the embedded word-event oracle 11:14-21 is a sub-unit (§7). 12:1 is a word-event with no vision frame — the class shifts from vision to oracle. |
| **P4** the undated oracle collection | Ezek.12.1-Ezek.19.14 | 215 | word-event 12:1 after the vision return | 19:14 qinah colophon קִ֥ינָה הִ֖יא וַתְּהִ֥י לְקִינָֽה + pe; 20:1 is a dateline | Thirteen word-event onsets (12:1, 12:8, 12:17, 12:21, 12:26, 13:1, 14:2, 14:12, 15:1, 16:1, 17:1, 17:11, 18:1) and the qinah onset 19:1 — all hard seams; no dateline and no class shift inside, so no parent seam inside. |
| **P5** the dated disputation-to-siege collection | Ezek.20.1-Ezek.24.27 (contains the zone: MT 20:1-24:27, same total) | 188 | dateline 20:1 (seventh year) + elders' scene; word-event 20:2 | 24:27 וְיָדְע֖וּ כִּֽי אֲנִ֥י יְהוָֽה + samekh; the mouth-opening promise that 33:22 fulfils | Hard seams inside: MT 21:1, 21:6, 21:13, 21:23 (all dual-written), 22:1, 22:17, 22:23, 23:1, **24:1 (dateline)**, 24:15. The 24:1 dateline is not a parent seam: no addressee-class shift (Jerusalem throughout) and ch 24 closes the muteness arc opened in P1. Held at §7. |
| **P6** oracles against the nations | Ezek.25.1-Ezek.32.32 | 197 | word-event 25:1; 25:2 בֶּן אָדָ֕ם שִׂ֥ים פָּנֶ֖יךָ אֶל בְּנֵ֣י עַמּ֑וֹן — the first foreign addressee (addressee-class shift); recognition + samekh at 24:27 behind it | 32:32 נְאֻ֖ם אֲדֹנָ֥י יְהוִֽה + pe; 33:1 word-event returns the addressee to "the children of your people" | Seven datelines inside (26:1, 29:1, 29:17, 30:20, 31:1, 32:1, 32:17) are hard seams but NOT parent seams: the collection is nation-ordered, not date-ordered — the year-27 date at 29:17 (וַיְהִ֗י בְּעֶשְׂרִ֤ים וָשֶׁ֨בַע֙ שָׁנָ֔ה, the latest date in the book) stands between year 10 (29:1) and year 11 (30:20), byte evidence that dates here serve the Egypt dossier, not the book's chronology. 28:24-26 (Israel gathered) is an embedded salvation coda inside P6, not a P7 onset. |
| **P7** restoration oracles and visions | Ezek.33.1-Ezek.39.29 | 197 | word-event 33:1 + addressee "children of your people"; the utterance/pe close at 32:32 behind it | 39:29 נְאֻ֖ם אֲדֹנָ֥י יְהוִֽה + pe; 40:1 is a dateline + hand + transport | Hard seams inside: 33:21 (dateline — the fugitive בָּא אֵלַ֨י הַפָּלִ֧יט מִירוּשָׁלִַ֛ם לֵאמֹ֖ר הֻכְּתָ֥ה הָעִֽיר; 33:22 hand + mouth opened), 33:23, 34:1, 35:1, 36:16, 37:1 (hand), 37:15, 38:1. The alternative parent seam at 33:20/33:21 (dateline; pe at 33:20; the no-sof-pasuq verse) is held at §7. |
| **P8** the temple vision and the land | Ezek.40.1-Ezek.48.35 | 260 | dateline 40:1 (year 25, "fourteenth year after the city was struck"); hand הָיְתָ֤ה עָלַי֙ יַד יְהוָ֔ה וַיָּבֵ֥א אֹתִ֖י שָֽׁמָּה; transport 40:2 בְּמַרְא֣וֹת אֱלֹהִ֔ים | end of book; 48:29 utterance + pe closes the allotment; 48:30-35 city-gate coda ending וְשֵׁם הָעִ֥יר מִיּ֖וֹם יְהוָ֥ה שָֽׁמָּה (no formula after — the book's last verse is its own close) | Hard seams inside: 42:20/43:1 (measuring finished 42:15 וְכִלָּ֗ה אֶת מִדּוֹת֙ הַבַּ֣יִת הַפְּנִימִ֔י; 42:20 לְהַבְדִּ֕יל בֵּ֥ין הַקֹּ֖דֶשׁ לְחֹֽל; 43:1 transport + glory), 43:27/44:1 (utterance close + the double samekh, the best-marked close in P8; 44:1 transport), 46:18/46:19 (law → transport), 47:12/47:13 (river → messenger formula on the border). |

Sums (deterministic, verse_inventory.json): 65 + 75 + 76 + 215 + 188 + 197 + 197 + 260 = **1,273**.
Rows never straddle a parent seam; `parent_collection` names the parent (P1…P8 with the labels
above). The thirteen dateline blocks of the inventory (plus 24:1's) are recorded as `dated_block`
metadata on every row (the block's opening dateline, dual-written where in the zone) so a reviewer
can test the chronology layer independently of the parent layer.

## §6 unit_type vocabulary + granularity (Q1 + Q3) — over_split_risk_check

**Closed 12-value vocabulary** (operative-category law: a per-bytes deviation is allowed with a
one-sentence disclosure in device_notes; no free text). Each value is anchored on a byte device:

1. `vision_report` — first-person vision narrative: hand/transport/"he said to me"/glory devices
   (1:1-28; 2:1-3:15 scenes; 3:22-27; 8:1-11:13, 11:22-25; 37:1-14; 43:1-9; 44:1-4; 47:1-12; the kitchen
   circuit 46:19-24).
2. `commission_narrative` — the prophet's office: sending, scroll, watchman charge, muteness
   (2:1-3:11 speeches; 3:16-21; 3:24-27; and 33:1-9 as the watchman recapitulation).
3. `sign_act` — a commanded symbolic action with its interpretation (4:1-17; 5:1-17; 12:1-16;
   12:17-20; `web:Ezek.21.6-Ezek.21.7 = oshb:Ezek.21.11-Ezek.21.12`; `web:Ezek.21.18-Ezek.21.23 = oshb:Ezek.21.23-Ezek.21.28`;
   24:15-27; 37:15-28). Device: imperative to the prophet + "sign" מופת/אות + "in their sight".
4. `judgment_oracle` — Israel/Jerusalem-addressed word-event unit with a verdict and a refrain close
   (6; 7; 11:1-13; 13; 14; 22:1-16, 22:17-22, 22:23-31; 24:1-14 carries the mashal label and goes to 7).
5. `oracle_against_nation` — foreign addressee via set-your-face or naming (25:1-7, 25:8-11,
   25:12-14, 25:15-17; 26:1-21 units; 28:1-10; 28:20-26; 29-31 units; 32:17-32; 35:1-36:15 as one
   two-sided unit; 38:1-39:24). Device: הנני אליך; recognition close in the nations' mouth.
6. `lament_qinah` — units the text labels קינה or נהה (19:1-14; 26:15-21 with the embedded qinah
   17-18; 27:1-36; 28:11-19; 32:1-16; 32:17-32 is a "wail" נהה — allowed here with disclosure, else 5).
7. `parable_allegory` — units the text labels משל/חידה or built as extended figure (15:1-8 vine;
   16:1-63 foundling; 17:1-10 eagles + 17:11-24 interpretation; 23:1-49 sisters; 24:1-14 cauldron;
   `web:Ezek.20.45-Ezek.20.49 = oshb:Ezek.21.1-Ezek.21.5` forest, labelled mashal at MT 21:5).
8. `disputation_oracle` — a quoted popular saying refuted (12:21-25; 12:26-28; 18:1-32; 20:1-44
   history disputation; 33:10-20; 33:23-29; 33:30-33; 11:14-21 blends with 9).
9. `salvation_oracle` — restoration promise as the unit's burden (11:14-21; 16:59-63 when cut off;
   28:24-26; 34:1-31; 36:16-38; 37:15-28 shares with 3; 39:25-29). Device: gather/return,
   ברית שלום (2 verses), עבדי דוד (3 verses), שם קדשי (8 verses).
10. `temple_measurement` — the guided measuring tour (40:5-42:20; 43:13-17 altar dimensions; 47:3-5
    inside the river vision). Device: וימד 21 verses; the ch-40 K/Q cluster.
11. `temple_law` — statute paragraphs (43:10-12 torah of the house; 43:18-27; 44:5-31; 45:1-8;
    45:9-17; 45:18-25; 46:1-15; 46:16-18). Device: messenger formula + jussive/2mp instruction; the
    three calendar dates live here and never open a row.
12. `land_allotment` — borders, tribal portions, city exits (47:13-23; 48:1-29; 48:30-35). Device:
    גבול (33 verses), שבט (16 verses), the "one portion" list refrain 48:1-7, 48:23-27.

**Granularity (Q3).** A row is ONE formula-bounded unit: from a hard or default onset (dateline;
word-event in any of the 49 forms; hand-of-YHWH; qinah/mashal command; "and you, son of man" when it
starts a new command; a transport verb or "he said to me" inside a vision; a messenger formula with
an addressee change) to the verse BEFORE the next such onset, with the refrain close inside the row.
Inside a long unit (16 = 63 vv; 20:1-44; 23 = 49 vv; 40 = 49 vv) the row is cut at internal seams
that are themselves formula-marked: a messenger formula with addressee change (16:35 "therefore,
prostitute, hear" + pe; 23:22 Oholibah verdict after the narrative; 16:59 the covenant turn), a
refrain close followed by a fresh "therefore" (20:27, 20:30, 20:39 in the history disputation), a
transport verb (40:17, 40:28, 40:32, 40:35, 40:48; 41:1; 42:1; 42:15), or a change of measured object
with וימד. Target density: 7-10 verses per row (projected ~130-170 rows), with the measured and
listed blocks (40-42, 45, 48) allowed up to 14-16 verses where no formula seam exists and a cut
would split a circuit or a list.

**Chapter divisions** cut where they coincide with a hard or default onset (most do: 6:1, 7:1, 8:1,
12:1, 13:1, 15:1, 16:1, 17:1, 18:1, 19:1, 20:1, 22:1, 23:1, 24:1, 25:1, 26:1, 27:1, 28:1, 29:1, 30:1,
31:1, 32:1, 33:1, 34:1, 35:1, 38:1, 40:1, 43:1, 44:1, 47:1 — and the WEB 20/21 division coincides with
MT 21:5 pe / MT 21:6 word-event). They do NOT cut where the unit continues: 2:1 → 3:1 (the scroll
scene runs 2:8-3:3 — cut at 2:1 "he said to me" if at all, not at 3:1 unless the row is sized there);
9:1, 10:1, 11:1 (vision scenes — cut on the transport/cry verse, which 9:1 and 11:1 are, 10:1 is not);
14:1 (the elders' scene 14:1 precedes the word-event 14:2 — the row opens at 14:1); 21:1 WEB (= MT
21:6, a word-event — cuts); 36:1 (וְאַתָּ֣ה בֶן אָדָ֔ם הִנָּבֵ֖א אֶל הָרֵ֣י יִשְׂרָאֵ֑ל — a sub-onset inside
the 35:1 word-event unit; a row seam here is allowed by the sub-onset but the two rows disclose the
shared word-event frame); 37:1 (hand — cuts); 39:1 (sub-onset inside 38:1's unit — same rule as
36:1); 41:1, 42:1, 46:1, 48:1 (measurement/law/allotment — cut only on transport, messenger formula
or list onset, which 41:1 ויביאני, 42:1 ויוצאני, 46:1 messenger formula and 48:1 "these are the
names" respectively are; 45:1 is a continuation "and when you divide the land" with NO formula — it
does not cut by chapter; the seam is at 44:31/45:1 only if the priests' portion 44:28-31 is argued as
the close, held at §7).

**Over-split guard (E-02 posture):** a row under 3 verses only when it is a complete word-event
unit (12:26-28 is 3; 33:21-22 is 2 and is held, §7); a qinah-labelled unit is never split; a
numbered/refrain list (27:12-24 trade list; 32:22-30 the nations in Sheol; 48:1-7 and 48:23-27
tribal portions; 40:20-37 the gate circuits) is never cut inside the list; a messenger formula is
never separated from the speech it opens; the superscription 1:1-3 is never its own row unless the
vision row would otherwise exceed the cap. Whole-chapter spans sit at medium_low/low with the cap
disclosure (cap_sweep HARD) — expected for chs 15 (8 vv), 19 (14), 27 (36, one qinah), 34 (31, one
word-event unit with internal messenger paragraphs; a cut at 34:17 "as for you, my flock" is the
disclosed alternative) and 38/39 units, and always disclosed.

## §7 Expected low-confidence regions — sidecar_specificity_plan

Hold at medium_low/low with bespoke rationale; never force. The OW-6b track gives these raised peer
and spot coverage and the second Fable review.

- **chs 1-3 (flagged).** 1:1-3 — two datelines in two systems ("thirtieth year" / "fifth year of
  Jehoiachin's exile") and a third-person word-event in a first-person book: one superscription row
  or the vision row's head. 1:28 samekh + 2:1 "he said to me": vision/commission seam. 3:12-15 the
  transport to Tel-abib as the vision's close versus the commission's close. **3:16** — the book's
  first word-event with a temporal onset וַיְהִ֕י מִקְצֵ֖ה שִׁבְעַ֣ת יָמִ֑ים and a pe whose intra-verse
  position the inventory cannot give (§4); the P1/P2 alternative at 3:15/3:16 versus 3:27/4:1 is the
  held parent question (§5). 3:22-27 — a hand-of-YHWH onset that opens a five-verse scene; whether it
  is its own row or the head of the sign-act series (the ropes 3:25 // 4:8).
- **chs 4-7.** Whether the four sign-acts (4:1-3, 4:4-8, 4:9-17, 5:1-4) are one row or two with the
  interpretation 5:5-17; the triple "I YHWH have spoken" at 5:13, 5:15, 5:17 (which one closes the
  row); 6:1-10 / 6:11-14 (pe at 6:10 and a fresh messenger formula at 6:11); 7:1-4 / 7:5-27 (pe at 7:4;
  the "end" poem is prose in the WEB — no `|q` lines in ch 7).
- **chs 8-11 (flagged; ONE vision).** Scene seams at 8:5, 8:7, 8:14, 8:16 (transport/"he said to
  me"), 9:1 (the cry), 10:1 (glory departs — no transport verb; a scene change argued from כבוד יהוה
  10:4/10:18), 11:1 (transport), 11:13 (Pelatiah's death and the prophet's cry — a narrative close),
  **11:14-21** a word-event oracle embedded inside the vision (own row, or held inside the 11:1-21
  scene), 11:22-25 the return. Whether ch 10's wheel description (10:9-17, echoing ch 1) is a row or
  texture.
- **ch 12 and the short disputations.** 12:1-16 sign-act with 12:8 as a morning re-onset (word-event
  with בבקר); 12:21-25 / 12:26-28 two three-to-five-verse units on the same proverb — one row with
  disclosure or two.
- **ch 16 (63 vv; 11 K/Q verses).** Internal cuts at 16:35 (pe; addressee "prostitute"), 16:44
  (mashal of the sisters), 16:59 (messenger + covenant turn); whether 16:59-63 is `salvation_oracle`
  or the allegory's close. 17: 17:1-10 / 17:11-21 / 17:22-24 as one, two or three rows. 18: poetry
  case-law (18:5-17 `|q`) versus prose disputation; the 18:21-32 turn. 19: one qinah row (never
  split; 19:10-14 the vine stanza is inside the colophon).
- **the ch 20/21 numbering zone (flagged; every ref dual).** 20:1-44 internal seams at 20:27, 20:30,
  20:39 (each "therefore … thus says" after a refrain) versus one long disputation row with the cap
  disclosure; the pe at MT 21:5 (= WEB 20:49); the two-ways sign-act
  `web:Ezek.21.18-Ezek.21.27 = oshb:Ezek.21.23-Ezek.21.32` with three pe marks (MT 21:28, 21:29, 21:32) and the prince oracle
  `web:Ezek.21.25-Ezek.21.27 = oshb:Ezek.21.30-Ezek.21.32` — one row or two; the Ammon sword unit
  `web:Ezek.21.28-Ezek.21.32 = oshb:Ezek.21.33-Ezek.21.37` — an OAN-form unit inside P5 (unit type 5
  with parent P5, disclosed).
- **chs 22-24.** 22's three word-event units; 23:36-49 (a second cycle "will you judge Oholah and
  Oholibah" without a word-event, opened by ויאמר יהוה אלי at 23:36 — own row or the allegory's
  close); **24:1 as a dateline the inventory omits** (§2a); 24:1-14 cauldron mashal + 24:15-27
  wife's death; 24:25-27 the mouth-opening promise as the P5 close.
- **chs 25-32 (flagged; onset and close collide).** 25: four short OAN (Ammon 2-7 with TWO
  recognition closes at 25:5 and 25:7; Moab 8-11; Edom 12-14; Philistia 15-17) — four rows of 3-6
  verses, or two, or one 17-verse row; 26: four messenger units (1-6, 7-14, 15-18 with the embedded
  qinah, 19-21) each with its own close — one row per unit is the default, held; 27: one 36-verse
  qinah (the trade list 12-24 in prose inside a poem); 28:1-10 / 28:11-19 / 28:20-23 / 28:24-26 — the
  Israel coda 28:24-26 (recognition ×3 at 28:22, 28:23, 28:26) as its own `salvation_oracle` row
  inside P6; 29:1-16 with the mid-verse WEB paragraph at 29:9 and the forty-years turn 29:13; 29:17-21
  the year-27 Nebuchadnezzar oracle; 30:1-19 undated with four messenger paragraphs (30:2, 30:10,
  30:13) inside; 30:20-26 (7 vv); 31 one cedar allegory under a dateline (unit type 5 or 7); 32:1-16
  qinah; 32:17-32 the Sheol roster (32:22-30 never cut inside).
- **ch 33 (the hinge).** 33:1-9 watchman recapitulation (type 2) / 33:10-20 disputation (pe at 33:11
  and 33:20; MT 33:20 has no sof-pasuq — disclosed, never argued); **33:21-22** — the fugitive
  dateline and the mouth-opening: two verses that fulfil 24:26-27; own row (under-size, disclosed) or
  the head of 33:23-29; whether the P6/P7 parent seam belongs at 32:32/33:1 (chosen) or at 33:20/33:21
  (dateline) is the held parent question of this region.
- **chs 34-37.** 34 as one unit with internal messenger paragraphs (34:7-10, 34:11-16, 34:17-19,
  34:20-31) — the cap disclosure or a cut at 34:17; **35:1-36:15** one word-event unit across the
  chapter break (Seir 35 / mountains of Israel 36:1-15, the "and you, son of man" sub-onset at 36:1;
  the seven messenger formulae in 36:2-7); 36:16-38 with the 36:33 and 36:37 messenger re-onsets and
  the recognition close 36:38 (the cross-tradition question on 36:23-38 is metadata only, §4); 37:1-14
  vision (recognition at 37:6, 37:13, 37:14 — which closes the row); 37:15-28 two-sticks sign-act
  with the salvation burden 37:21-28.
- **chs 38-39 (flagged; recapitulation-versus-sequence).** Gog: 38:1-9, 38:10-13, 38:14-16, 38:17-23,
  39:1-8, 39:9-10, 39:11-16, 39:17-20, 39:21-24, 39:25-29 — a paragraph chain with FIVE samekh marks in
  ch 38 and utterance closes at 38:18, 38:21, 39:5, 39:8, 39:10, 39:13, 39:20, 39:29; whether 39:1
  begins a second oracle (the "and you, son of man" sub-onset) or a recapitulation of 38:1-9; whether
  39:25-29 is the Gog unit's coda or the P7 close as `salvation_oracle`.
- **chs 40-48 (flagged; few formulae, no parashah marks in 40-42, the K/Q cluster on the
  measurements).** Where the measurement rows cut (gates 40:5-16, court 40:17-19, north/south gates
  40:20-27, inner gates 40:28-37, chambers and tables 40:38-47, porch 40:48-49; nave 41:1-4, side
  chambers 41:5-15, decoration 41:15-26; chambers 42:1-14; outer measure 42:15-20) — each cut sits on
  a transport or וימד verse and none has parashah corroboration; the 41:20 and 46:22 puncta verses
  (disclosed single-witness, and present as U+05C4 in the extract bytes); 43:1-12 glory return +
  torah of the house (43:10 "you, son of man" and 43:12's double זֹ֖את תּוֹרַ֣ת הַבָּ֑יִת inclusio);
  43:13-17 altar dimensions versus 43:18-27 altar ordinances (43:15 anomalous-form note); 44:1-3 the
  shut gate (3 vv; 44:3 anomalous-form note) — own row or the head of 44:4-31; 44:4-31 with the
  Levites/Zadokites contrast at 44:10/44:15 (utterance at 44:12, 44:15, 44:27; pe at 44:14, 44:31);
  **44:31/45:1** — no formula at 45:1 (וּבְהַפִּֽילְכֶ֨ם "and when you divide"); 45:9 messenger formula
  "enough, princes of Israel" as a law-paragraph onset; **45:18-25 the festival calendar: 45:20,
  45:21, 45:25 never open a row (§2d.5)**; 46:1-15 / 46:16-18 (two messenger formulae) / 46:19-24 the
  kitchens (transport — a `vision_report` island inside the law); 47:1-12 the river (47:6 "have you
  seen, son of man"); 47:13-23 borders; 48:1-29 portions (48:8-22 the holy portion inside the tribal
  list — never cut inside 48:1-7 or 48:23-27); 48:30-35 the gates and the name — the book's close
  without a formula.

E-02 binds: whole-chapter spans sit at medium_low/low + frontier flag + cap disclosure (cap_sweep is
HARD); in Ezekiel they are expected to be UNCOMMON but not rare (chs 15, 19, 27, 31, 34 and the
36:1-15 half-chapter are the candidates), each disclosed.

## §8 Register + hygiene (verbatim into every brief)

Row prose (all 22 fields) never contains: decision-ids, strategy-file/§ citations, erratum or
repair narration, positional row references (incl. "that row"), cross-part references,
file-order talk, review-actor names, tool filenames, session/wave talk, or staged-file
names/stems. The "(sweep: N verses)" convention is the one sanctioned citation shorthand.
Cross-row references are verse-anchored; self-reference ("this unit") is exempt. Curly double
quotes are for WEB text ONLY, with an inline web: ref in the SAME field; pointed Hebrew is
spliced programmatically from the staged MT verse map with its oshb: ref and tier named — never
hand-typed, never copied through the draft (E-01 nfd degradation is HARD at the writer gate).
Every ref that touches WEB 20:45-49, WEB ch 21 or MT ch 21 is written dual
(`web:Ezek.20.45 = oshb:Ezek.21.1`) or with a numeric qualifier, in EVERY field including prose;
a bare coordinate there is a Tier-0 failure. No Aramaic label anywhere: the book is Hebrew
throughout (18,866 H-prefixed tokens, 0 A). Every universal claim (only/never/first/last/each/
sole/densest/unique/nowhere/no-other …) carries an adjacent DIGIT-BEARING sweep citation naming
the swept OBJECT and UNIT; exclusivity claims are NEVER tier-dampened (E-16). Tier-label every
recurrence claim; "verbatim/byte-identical" only per collate truth with the tier named. Form-class
labels (imperative, jussive, participle, gender, person, perfect/wayyiqtol) are byte-checkable
claims — same discipline as digits; the staged extract has NO morphology layer and NO maqaf, paseq
or sof-pasuq (a claim about their absence is a claim about the extract, not the source). Paseq is
COUNT-ONLY from the inventory; an intra-verse paseq position is unsourceable. Parashah marks are
disclosed in prose ("pe follows MT 24:27, single witness") and never as an oss key; intra-verse
parashah position is never asserted. K/Q verses are checked BEFORE slicing (the ch-16 and ch-40
clusters; the 23 doubled-note verses); a Qere never argues a boundary. Puncta extraordinaria are
disclosed only at MT 41:20 and 46:22, single witness; anywhere else is a fabrication; selah, large/
small letters, reversed nun are fabrication classes. A dateline is cited as "dateline" only at the
fourteen year-bearing verses (the inventory's thirteen plus MT 24:1, disclosed as such); the
calendar dates at MT 45:18, 45:20, 45:21, 45:25 are never called datelines and never open a unit.
Gloss extent = splice extent (E-08). Read back every splice in its sentence (E-04). Semantic-class
count discipline: name the swept object FIRST, then count; blended sweeps forbidden (the strict
word-event 39 and the any-form 49 are never mixed; the strict recognition 28 and the family 64 are
never mixed). Cross-seam cohesion: a byte-true device straddling the row's own seam argues
continuity against the row unless disclosed. Every row discloses the formula devices its span
carries by role (onset / sub-onset / close), its dated block, and — inside a vision — the transport
or "he said to me" verse it opens on. observed_substrate_signals uses the dotted signal-key taxonomy
(dateline.*, wordevent.*, address.son_of_man, messenger.*, utterance.*, recognition.{3mp,2ms,2mp,
nations,israel}, spoken.i_yhwh, hand.yhwh, face.set_toward, vision.{transport,glory,said_to_me},
signact.*, qinah.*, mashal.*, oath.as_i_live, against.behold_i_am, law.*, measure.*, allotment.*,
closure.* …); parashah.* keys BARRED from oss (disclosure in prose only); staged-file names/stems
barred in every field. Mandated recurring sentences ship with variation orders (4+ formulations) —
the CWO-1 lesson from Jeremiah binds from day one: no disclosure sentence template (the dual-ref
sentence, the K/Q sentence, the dated-block sentence, the "refrain closes" sentence) may converge
into a 7-gram shared by >=10 rows, and observed_substrate_signals key sequences are tokenized by
ngram7 too. Rows inside the same word-event unit (36:1; 39:1; the ch-16 and ch-40 cuts) disclose the
shared frame in each row with a verse anchor, never with a positional reference.

## §9 Writer part plan (tiling 1,273 EXACTLY, 11 parts, parent-aligned)

| part | span (WEB) | vv | parent(s) | boundary warrant at onset (both sides) |
|---|---|---|---|---|
| p01 | Ezek.1.1-Ezek.7.27 | 140 | P1+P2 | book start; datelines 1:1-2 + hand 1:3; internal parent seam 3:27/4:1 (refrain close + samekh / "and you, son of man") — rows never straddle it; hard seams 3:16, 3:22, 6:1, 7:1 |
| p02 | Ezek.8.1-Ezek.14.23 | 150 | P3 + P4(a) | dateline 8:1 + hand + transport; recognition + pe at 7:27 behind; internal parent seam 11:25/12:1 (vision return + pe / word-event); part end at 14:23 (utterance + pe; 15:1 word-event) |
| p03 | Ezek.15.1-Ezek.19.14 | 141 | P4(b) | word-event 15:1; utterance + pe at 14:23 behind; ends at the qinah colophon 19:14 + pe |
| p04 | Ezek.20.1-Ezek.21.32 (= MT 20:1-21:37) | 81 | P5(a) | dateline 20:1 + elders' scene; qinah colophon + pe at 19:14 behind; the WHOLE numbering zone sits inside this part (no part seam near it); ends at MT 21:37 "I YHWH have spoken" + pe (= WEB 21:32) |
| p05 | Ezek.22.1-Ezek.24.27 | 107 | P5(b) | word-event 22:1; "I YHWH have spoken" + pe at MT 21:37 (= WEB 21:32) behind; hard seams 22:17, 22:23, 23:1, 24:1 (dateline), 24:15; ends at the P5 close 24:27 |
| p06 | Ezek.25.1-Ezek.28.26 | 100 | P6(a) | word-event 25:1 + set-your-face 25:2 (first foreign addressee); recognition + samekh at 24:27 behind; ends at 28:26 (recognition, "YHWH their God" + samekh; 29:1 dateline) |
| p07 | Ezek.29.1-Ezek.32.32 | 97 | P6(b) | dateline 29:1 (Egypt dossier onset); recognition + samekh at 28:26 behind; six more datelines inside as hard seams; ends at the P6 close 32:32 |
| p08 | Ezek.33.1-Ezek.36.38 | 117 | P7(a) | word-event 33:1 + addressee shift; utterance + pe at 32:32 behind; hard seams 33:21 (dateline), 33:23, 34:1, 35:1, 36:16; ends at 36:38 recognition + samekh (37:1 hand) |
| p09 | Ezek.37.1-Ezek.39.29 | 80 | P7(b) | hand-of-YHWH 37:1 + transport; recognition + samekh at 36:38 behind; hard seams 37:15, 38:1; ends at the P7 close 39:29 |
| p10 | Ezek.40.1-Ezek.43.27 | 122 | P8(a) | dateline 40:1 + hand + transport; utterance + pe at 39:29 behind; hard seam 42:20/43:1; ends at 43:27 utterance + the double samekh |
| p11 | Ezek.44.1-Ezek.48.35 | 138 | P8(b) | transport 44:1 (the shut east gate); utterance + double samekh at 43:27 behind; hard seams 46:19, 47:1, 47:13; ends at the book's last verse |

Arithmetic (per-chapter WEB counts from verse_inventory.json, summed by a deterministic probe that
also asserted contiguity 1:1 → 48:35 with no gap and no overlap):
140 + 150 + 141 + 81 + 107 + 100 + 97 + 117 + 80 + 122 + 138 = **1,273**.
Per-part derivations: p01 = 28+10+27+17+17+14+27; p02 = 18+11+22+25+28+23+23; p03 = 8+63+24+32+14;
p04 = 49+32 (WEB; = MT 44+37); p05 = 31+49+27; p06 = 17+21+36+26; p07 = 21+26+18+32;
p08 = 33+31+15+38; p09 = 28+23+29; p10 = 49+26+20+27; p11 = 31+25+24+23+35.
Every part boundary is a parent seam or a hard seam (dateline, vision onset, or a word-event onset
with a refrain/pe close behind it); two parts DO span a parent seam and this is
deliberate — see the orchestrator disposition below; the numbering zone is interior
to p04 and every p04/p05 ref is written dual. Parts range 80-150 verses (mean 115.7), reviewable in
<=8-row clusters.

### ORCHESTRATOR DISPOSITION (added 2026-09-08, ezek_p0_repair_a1#e1)

Two rulings on this deliverable, recorded here rather than applied silently.

**1. Parts spanning a parent seam — ACCEPTED as designed; the contradicting sentence corrected.**

The §9 table is right and the summary sentence was wrong. `p01` (Ezek.1.1-7.27) spans the P1/P2 seam at
3:27/4:1, and `p02` (Ezek.8.1-14.23) spans the P3/P4 seam at 11:25/12:1. The table labels both internal
parent seams explicitly; the prose then claimed no part straddles one. The table is the truth and the
sentence is corrected above.

The design is accepted, against the brief's instruction that parts be parent-aligned, for three reasons:

- The binding law is that **ROWS** never straddle a parent seam, and §5 and §9 both carry it. A part is a
  work assignment; a row is a claim about the text. Only the second is a correctness boundary.
- Parent-aligned parts would run 65 verses (P1) against 260 (P8) — a four-fold imbalance that makes review
  depth uneven across the book, which is a real quality cost on a hard-track book.
- A part that contains a parent seam puts **both sides of that seam in one reviewer's hands**, which is what
  the standing "a seam is assessed from both sides" rule actively wants. Splitting the parts exactly at the
  parent seams would guarantee that no single reviewer ever weighs one.

Every writer whose part contains an internal parent seam is told so in their launch message, and the
rows-never-straddle rule binds them there as everywhere.

**2. The dateline discrepancy — RULED: 14, and the inventory was corrected, not the strategy.**

§2 flagged that `ezek_device_inventory.json` carried 13 datelines while the bytes show 14, named MT 24:1 as
the missing one, and **reported it upward rather than patching around it**. That was the correct action and
it is the reason the defect was found at all.

The orchestrator verified MT 24:1 from the bytes and ruled: **14 is the count.** The inventory's rule was
defective — it required a CARDINAL numeral stem, and 24:1 writes ordinals (`התשיעית`, `העשירי`, `בעשור`),
which share no substring with the cardinals. The same infixed date also hid 24:1 from the strict word-event
pattern, so one verse was invisible twice for two unrelated reasons. The rule is now structural: a year word
together with a month or day term, needing no numeral vocabulary. `ezek_device_inventory.json` and
`TOOLKIT.md` were repaired and re-verified (80/80 GREEN), and a distinct checker re-derived the claims from
the bytes. **This strategy's use of 14 stands unchanged and is now ratified.**

## §10 Strategy self-checks (T467 anchor summary) — how a reviewer tests this against the bytes

- literary_form_decision_matrix: §2a-§2d — re-run the skeleton sweeps named there against the
  staged MT extract; the digits must reproduce exactly (word-event any-form 49; recognition family
  64; 2mp 21; qinah 8; mashal 11; "and you, son of man" 23; transport 20; וימד 21; בית מרי 12; U+05C4
  in exactly 2 verses). The inventory's own counts are consumed, never re-derived — a mismatch
  between an inventory count and a sweep here is REPORTED (as the 13-versus-14 dateline count is),
  not silently resolved.
- Parent seams: §5 — for each of the seven internal seams, read the close verse and the onset verse
  in both witnesses and confirm the two-sided evidence named; confirm the traditional alternatives
  (3:16; 24:1; 33:21) are held in §7 rather than adopted.
- over_split_risk_check: §6 — the 12-value vocabulary is closed; the list-never-cut rule; the
  under-3-verse rule; the chapter-division rule with its named non-cutting chapters (10:1, 36:1,
  39:1, 45:1); the E-02 cap posture.
- source_metadata_evidence_only_check: §4 — parashah weights, the intra-verse-position bar, the E-23
  classes (the fourteen WEB mid-verse paragraphs are the E-23 lane's checklist), cross-tradition
  material in prose only.
- Numbering/language: §3 — the zone rows are listed dual; a validator arm flags any bare ref in
  WEB 20:45-49 / WEB 21 / MT 21 in any field; the Aramaic-label arm; the dual-span count identity.
- Calendar-date arm: any row whose onset is MT 45:18, 45:20, 45:21 or 45:25 fails.
- Puncta arm: any puncta claim outside MT 41:20 / 46:22 fails; a splice of either verse must carry
  the single-witness disclosure (and, because the extract carries U+05C4 in the bytes, the nfd
  arm must treat U+05C4 as a legitimate combining mark, not degradation).
- sidecar_specificity_plan: §7 — named held questions with spans; the OW-6b second Fable review
  covers exactly the flagged regions listed there.
- Part plan: §9 — recompute the eleven sums from verse_inventory.json; assert contiguity; assert
  each boundary is in the hard-seam set.
- Budget (Q5): the Isa/Jer per-verse actual recorded at Lamentations (~32k tokens/verse at full r3
  depth) scales to ~41M tokens for 1,273 verses BEFORE the OW-6b raised coverage; RECOMMEND
  authorization to be REQUESTED (not assumed) at ~40-50M ± 30% at full r3 depth, with the
  per-session soft cap and the pre-8M check-in left in force unless the owner waives them for this
  book explicitly; the no-waste bar and honest per-attempt reporting stand.
- Ratification items (R-pattern, owner-correctable): R1 the frame-spine onset/close ruling and the
  hard-seam layer (§2d, §5); R2 the eight-parent architecture with 33:1 (not 33:21) and 25:1 (no
  dateline) as parent seams and 24:1 as a hard seam only (§5); R3 the 12-value vocabulary and the
  dotted oss taxonomy (§6, §8); R4 the treatment of MT 24:1 as a dateline pending inventory
  correction (§2a); R5 the 11-part plan (§9).
