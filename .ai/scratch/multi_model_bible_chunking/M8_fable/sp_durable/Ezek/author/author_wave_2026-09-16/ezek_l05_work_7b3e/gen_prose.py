# -*- coding: utf-8 -*-
import json
LANE = r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
lane = json.load(open(LANE, encoding='utf-8'))
ROWS = {r['decision_id']: r for r in lane['your_rows']}
D = json.load(open('derived_strings.json', encoding='utf-8'))
PROBLEMS = []
EDITS = []

LDQ = "\u201c"   # left double curly quote
RDQ = "\u201d"   # right double curly quote


def rep(text, old, new, tag):
    n = text.count(old)
    if n != 1:
        PROBLEMS.append("%s: 'old' occurs %d times, need exactly 1 :: %r" % (tag, n, old[:80]))
        return text
    return text.replace(old, new, 1)


def slice_rep(text, a, b, new, tag):
    """Replace from the start of anchor a up to (not including) anchor b. Avoids retyping Hebrew."""
    if text.count(a) != 1 or text.count(b) != 1:
        PROBLEMS.append("%s: anchors not unique (a=%d b=%d)" % (tag, text.count(a), text.count(b)))
        return text
    i, j = text.index(a), text.index(b)
    if j <= i:
        PROBLEMS.append("%s: anchors out of order" % tag)
        return text
    return text[:i] + new + text[j:]


def add(row, field, value, items, sweep, why, tier, note=None):
    if value == ROWS[row][field]:
        PROBLEMS.append("%s/%s: value identical to expected_before (no-op edit)" % (row, field))
    e = {"row_id": row, "field": field, "op": "set",
         "expected_before": ROWS[row][field], "value": value,
         "worklist_item_ids": items, "sweep": sweep, "why": why, "tier": tier}
    if note:
        e["sweep_pooling_note"] = note
    EDITS.append(e)


# ---------------------------------------------------------------- P07-008 A6
t = ROWS["P07-008"]["boundary_rationale"]
t = rep(t, "to wail for the multitude of Egypt -- a different technical verb",
        "to " + LDQ + "wail for the multitude of Egypt" + RDQ + " (web:Ezek.32.18) -- a different technical verb",
        "P07-008/a6")
add("P07-008", "boundary_rationale", t, ["l05_i09"], "a6",
    "The 6-word run is the WEB's own wording at Ezek.32.18 (MEASURED: exactly 1 occurrence in WEB Ezekiel, in span), it is not a rendering of any A6-b counted device, so the delimiter and the in-field web reference are owed and installed.",
    "MEASURED: run located in the pinned WEB verse map by exact token match")

# ---------------------------------------------------------------- P08-002 BOSS_RETURN
t = ROWS["P08-002"]["boundary_rationale"]
t = rep(t,
        "which restates the people's complaint and YHWH's verdict (" + LDQ + "I will judge every one of you after his ways" + RDQ + " (web:Ezek.33.20)) verbatim against 33.17, marking the disputation's true end.",
        "which restates the people's complaint verbatim against 33.17 -- the four pointed words " + D['COMPLAINT'] +
        " stand byte-identical in both verses (oshb:Ezek.33.17, oshb:Ezek.33.20; WLC/OSHB, single witness) -- and then adds YHWH's verdict (" +
        LDQ + "I will judge every one of you after his ways" + RDQ + " (web:Ezek.33.20)), which stands at 33.20 only and has no counterpart anywhere in 33.17, marking the disputation's true end.",
        "P08-002/br-verbatim")
t = rep(t, "This is disclosed as a single-witness punctuation divergence;",
        "That absence is MEASURED from the pinned marks input, whose own resolved-anomaly record names this verse and types it as a real source fact rather than a parsing gap (pmarks_Ezek.json, arithmetic_anomalies_resolved.sof_pasuq_1272_for_1273_verses, keys verse/finding/status). This is disclosed as a single-witness punctuation divergence;",
        "P08-002/br-sofpasuq")
add("P08-002", "boundary_rationale", t, ["l05_i15"], "grounds",
    "Boss work order, carried: the verbatim scope is corrected to the complaint alone (MEASURED: the longest identical contiguous pointed run between MT 33:17 and 33:20 is those four words, and none of the verdict clause's four tokens occurs in 33:17), and the sof-pasuq sentence keeps its MEASURED tier with the pmarks key cited, per the order's instruction to strike the tier cure.",
    "MEASURED over Ezek_oshb.txt and pmarks_Ezek.json at their pinned digests")

t = ("The rival onset is the 'and you, son of man' (ve'attah) at Ezek.33.12, and CUT-RULE limb (a) does license it: "
     "the addressee changes from " + D['ADDR3310'] + " at 33.10 to " + D['ADDR3312'] + " at 33.12 "
     "(oshb:Ezek.33.10, oshb:Ezek.33.12; WLC/OSHB, single witness). It is held against on the over-split guard: cutting there "
     "would leave 33:10-11 as a two-verse row that is not a complete word-event unit, and 33:11's own close-shaped cluster cannot "
     "supply the missing onset -- its utterance formula stands mid-verse, at word 4 of that verse's 25, with independent imperatives "
     "running on after it, so CUT-RULE limb (b) is not met there, and a mark alone never satisfies that limb however strong the pe looks. "
     "The disputation therefore runs on as one 'you say ... but I say' unit across 33:10-20, which is the near face on both of this row's seams.")
add("P08-002", "strongest_rejected_alternative", t, ["l05_i15"], "grounds",
    "Boss work order, carried: LF's correction names the 33:12 ve'attah as the rival onset with the over-split guard as the holding ground. Both are MEASURED here -- the addressee change and the mid-verse position of 33:11's utterance formula -- so the weighing states what each face carries, that CUT-RULE licenses the rival, and the stated ground for holding.",
    "MEASURED over Ezek_oshb.txt at its pinned digest")

t = ROWS["P08-002"]["device_notes"]
t = rep(t,
        "held at medium_low rather than split, because an oath or messenger sub-onset counts as a row seam only when a refrain-grade close immediately precedes it, and none precedes 33.11's oath+utterance.",
        "held at medium_low rather than split: the licensed rival onset is the ve'attah at 33.12, licensed by an addressee change under CUT-RULE limb (a), and the ground for holding against it is the over-split guard, since a cut there would leave 33:10-11, under three verses and not a complete word-event unit.",
        "P08-002/dn-ground")
t = rep(t, "Paseq (count-only, single-witness): Ezek.33.11 carries 2 occurrences;",
        "K/Q, A2 disclosure (single-witness): oshb:Ezek.33.13 carries one note, ketiv " + D['K3313'] + " / qere " + D['Q3313'] +
        ", and oshb:Ezek.33.16 carries one note, ketiv " + D['K3316'] + " / qere " + D['Q3316'] +
        "; each ketiv stands unpointed in the running text of this witness, each of the two notes carries two morpheme separators in the K/Q layer which are dropped from the forms as given here, and no boundary is argued from either Qere. MEASURED from pmarks_Ezek.json, kq, where the entry at each of these two verses is a list of K-Q pair strings with one member. "
        "Paseq (count-only, single-witness): Ezek.33.11 carries 2 occurrences;",
        "P08-002/dn-kq")
add("P08-002", "device_notes", t, ["l05_i15"], "disclosures",
    "Boss work order, carried: the A2 disclosure of the K/Q at 33:13 and 33:16 is added (it was absent from every field of this row), and the medium_low holding ground is brought into line with the corrected rejected-alternative so the two fields do not state different grounds.",
    "MEASURED from pmarks_Ezek.json and Ezek_oshb.txt at their pinned digests")

# ---------------------------------------------------------------- P08-007 A6
t = ROWS["P08-007"]["boundary_rationale"]
t = rep(t, "carrying the 'behold, I am against you' verdict-onset device.",
        "carrying the " + LDQ + "Behold, I am against you" + RDQ + " (web:Ezek.35.3) verdict-onset device.",
        "P08-007/a6-behold")
t = rep(t, "('they have been laid desolate')",
        "(" + LDQ + "They have been laid desolate." + RDQ + " (web:Ezek.35.12))",
        "P08-007/a6-desolate")
add("P08-007", "boundary_rationale", t, ["l05_i27", "l05_i30"], "a6",
    "Both runs are the WEB's own wording at an IN-SPAN verse (MEASURED: 'behold i am against you' at web:Ezek.35.3, 1 of 9 book-wide occurrences; 'they have been laid desolate' at web:Ezek.35.12, its only occurrence). Neither is a rendering of an A6-b counted device -- the heneni-against verdict device is not on A6-b's closed list -- so the convention is owed. The AUTHOR_JUDGEMENT question on the first run is answered NOT COINCIDENTAL: the in-span verse the sentence is about is itself one of the occurrences, so the correct in-field reference is web:Ezek.35.3, not the out-of-span verses the item listed.",
    "MEASURED over tools/verse_map_web.json at its pinned digest")

L = list(ROWS["P08-007"]["boundary_evidence_refs"])
L[3] = rep(L[3], "messenger formula + 'behold, I am against you' verdict device",
           "messenger formula + the verdict device, rendered at web:Ezek.35.3 as " + LDQ + "Behold, I am against you" + RDQ,
           "P08-007/refs3")
L[10] = rep(L[10], "K/Q on the verb rendered 'they have been laid desolate'",
            "K/Q on the verb, which web:Ezek.35.12 renders " + LDQ + "They have been laid desolate." + RDQ,
            "P08-007/refs10")
add("P08-007", "boundary_evidence_refs", L, ["l05_i31", "l05_i32"], "a6",
    "The same two runs appear inside existing refs entries, which are the fields the items name. Emitted as one 'set' of the complete final list because two entries change and the rule is one edit per (row, field); no entry is re-tokenised and no entry is added or removed. The reference is placed before the quotation in each entry so that the entry and the prose field do not share a 7-gram.",
    "MEASURED over tools/verse_map_web.json at its pinned digest")

# ---------------------------------------------------------------- P08-010 A6
L = list(ROWS["P08-010"]["boundary_evidence_refs"])
L[1] = rep(L[1], "addressee pivots from Seir to the mountains of Israel))",
           "addressee pivots from Seir to " + LDQ + "the mountains of Israel" + RDQ + " (web:Ezek.36.1)))", "P08-010/refs1")
add("P08-010", "boundary_evidence_refs", L, ["l05_i35"], "a6",
    "The run reproduces WEB Ezek.36.1 exactly (MEASURED: its only occurrence in WEB Ezekiel, in span) and the entry is itself about Ezek.36.1, so an in-field reference is available and makes the wording checkable. The leading 'to' is the entry's own, so the run is not purely an addressee title and I did not take the A6-b exemption; installing is the safe direction.",
    "MEASURED over tools/verse_map_web.json at its pinned digest")

# ---------------------------------------------------------------- P08-011 BOSS_RETURN
t = ROWS["P08-011"]["boundary_rationale"]
t = rep(t, "All four are split from the K/Q note layer with morpheme separators stripped.",
        "Of those four notes, morpheme separators are present in the K/Q layer -- and therefore stripped in the forms as rendered here -- "
        "only for the SECOND 36:13 note (%d separators) and the FIRST 36:14 note (%d); the first 36:13 note and the second 36:14 note carry "
        "none in the layer at all, so nothing was stripped from either of them. MEASURED by counting the '/' morpheme separators in each member of "
        "pmarks_Ezek.json, kq, whose entry at each of these verses is a two-member list of K-Q pair strings: 36:13 measures [%d, %d] and 36:14 measures [%d, %d]."
        % (D['SEP3613'][1], D['SEP3614'][0], D['SEP3613'][0], D['SEP3613'][1], D['SEP3614'][0], D['SEP3614'][1]),
        "P08-011/kq-sep")
add("P08-011", "boundary_rationale", t, ["l05_i36"], "disclosures",
    "Boss work order, carried: OL's finding reproduces independently here. I counted the '/' separators per member and found 36:13 = [0, 2] and 36:14 = [4, 0], so 'separators stripped' is true only of the second 36:13 note and the first 36:14 note, exactly as the order states. A1 is untouched: no labelled, slash-free Qere form is challenged.",
    "MEASURED from pmarks_Ezek.json at its pinned digest; independently reproduces the boss's C1 figures")

# ---------------------------------------------------------------- P08-012 WORDING
t = ROWS["P08-012"]["strongest_rejected_alternative"]
t = rep(t, "36.23's utterance formula is a full refrain-grade close",
        "36.23's recognition-plus-utterance material runs from the major disjunctive through to the verse's last word, its formula tokens "
        "standing mid-verse with only a dependent temporal infinitive (" + D['TAIL3623'] + ", oshb:Ezek.36.23; WLC/OSHB, single witness) after them, "
        "which under #e14 Q2 grades as an ordinary licensed near-face signal and not the weak mid-verse shape",
        "P08-012/wording")
add("P08-012", "strongest_rejected_alternative", t, ["l05_i40"], "grounds",
    "#e14 Q2's wording order, applied to a description true to the bytes. MEASURED: the etnachta falls on be-tokham (word 9), the b-half carries the knowing clause then the utterance formula, and the three words that follow to the final word are a preposition-plus-infinitive-construct, i.e. a dependent completion. Worded differently from the P08-013 order so no 7-gram is shared between the two rows.",
    "MEASURED over Ezek_oshb.txt at its pinned digest")

# ---------------------------------------------------------------- P08-013 WORDING
t = ROWS["P08-013"]["strongest_rejected_alternative"]
t = rep(t, "36.23 is a full refrain-grade close",
        "at 36.23 the knowing clause and the utterance signature together fill the second half of that verse, the formula words sitting inside it "
        "rather than at its end, and what follows them as far as the final word is a dependent temporal infinitive and not an independent clause "
        "(oshb:Ezek.36.23) -- which #e14 Q2 treats as a licensed close of the ordinary kind rather than the weak mid-verse case,",
        "P08-013/wording")
add("P08-013", "strongest_rejected_alternative", t, ["l05_i44"], "grounds",
    "#e14 Q2's wording order on the second of the two rows that carried the phrase. Same MEASURED fact, deliberately different formulation, because the ruling's own sentence used verbatim on both rows would create a shared 9-word string and trip the ngram7 gate. The confidence does not move: #e14 HELD it at MEDIUM and the separate CONFIDENCE item carries that.",
    "MEASURED over Ezek_oshb.txt at its pinned digest")

# ---------------------------------------------------------------- P08-013 A6 prose
t = ROWS["P08-013"]["boundary_rationale"]
t = rep(t, "(\u2018I don't do this for your sake ... let it be known to you, be ashamed\u2019)",
        "(" + LDQ + "I don't do this for your sake" + RDQ + " and " + LDQ + "Let it be known to you. Be ashamed" + RDQ + ", both web:Ezek.36.32)",
        "P08-013/a6-prose")
add("P08-013", "boundary_rationale", t, ["l05_i45", "l05_i46"], "a6",
    "Two runs in one parenthetical, both the WEB's own wording at Ezek.36.32 (MEASURED: 'i don't do this for your sake' at web:Ezek.36.22 and web:Ezek.36.32, the in-span one being 36:32; 'let it be known to you be ashamed' only at web:Ezek.36.32). Neither is an A6-b counted device. The elision in the original single-quoted gloss is removed so each delimited run is an exact quotation.",
    "MEASURED over tools/verse_map_web.json at its pinned digest")

# ---------------------------------------------------------------- P08-013 refs: A6 + A4 combined
L = list(ROWS["P08-013"]["boundary_evidence_refs"])
L[2] = rep(L[2], "('you will be my people' device)",
           "(" + LDQ + "You will be my people" + RDQ + " (web:Ezek.36.28) device)", "P08-013/refs2")
L.append("web:Ezek.36.25 [ANCHOR] cleansing material within the span")
add("P08-013", "boundary_evidence_refs", L, ["l05_i47", "l05_i48"], "a4",
    "COMBINED EDIT. One A6 refs fix (entry 2, the covenant-formula run, MEASURED at web:Ezek.36.28 as its only occurrence) and one A4 install (Ezek.36.25, ANCHOR, in-span cleansing content the boundary does not rest on) both land on this one field. The one-edit-per-(row, field) rule and the fact that a later 'set' would no longer match its expected_before after an earlier append make a single 'set' of the complete final list the only safe form.",
    "MEASURED over tools/verse_map_web.json; the A4 unmirrored status is EXTRACTED from the ruled item",
    "carries an a6 item (l05_i47) inside an a4-labelled edit; flagged in unresolved_uncertainty for the orchestrator's sweep-parity accounting")

# ---------------------------------------------------------------- P09-001 A6
t = ROWS["P09-001"]["device_notes"]
t = rep(t, "(\u2018Son of man, can these bones live?\u2019 web:Ezek.37.3, then the prophet's reply)",
        "(" + LDQ + "Son of man, can these bones live?" + RDQ + " (web:Ezek.37.3), then the prophet's reply)",
        "P09-001/a6")
add("P09-001", "device_notes", t, ["l05_i53"], "a6",
    "The run is the WEB's own wording at Ezek.37.3 (MEASURED: its only occurrence, in span). The in-field reference was already present; the delimiter is upgraded to the double curly quotes the convention specifies. 'Son of man' alone would be an A6-b addressee title, but a 7-word question is not, so the convention is owed.",
    "MEASURED over tools/verse_map_web.json at its pinned digest")

# ---------------------------------------------------------------- P09-002 BOSS_RETURN + A6
t = ROWS["P09-002"]["device_notes"]
t = slice_rep(t, "37.16 is a doubled ketiv/qere verse", ", and 37.19 carries one further note",
              "37.16 is a doubled ketiv/qere verse: two notes on one verse, each written " + D['K3716'] +
              " (oshb:Ezek.37.16, ketiv), and each read as the same consonantal word under different pointing -- the first note reads " +
              D['Q3716a'] + " and the second " + D['Q3716b'] +
              ", the two differing by exactly one codepoint, U+0591 HEBREW ACCENT ETNAHTA in the first against U+05BD HEBREW POINT METEG in the second"
              " (MEASURED by diffing the two members of the kq entry at this verse in pmarks_Ezek.json, codepoint by codepoint; WLC/OSHB, single witness)",
              "P09-002/kq-37-16")
add("P09-002", "device_notes", t, ["l05_i59"], "disclosures",
    "Boss work order, carried: OL's second finding reproduces independently here. I diffed the two members of the kq list at codepoint level and found them identical apart from U+0591 in member 0 against U+05BD in member 1, so the two Qere notes are the same word under different pointing and the old 'both the same word ... read <first form>' was false of the second note. A1 is untouched: neither labelled, slash-free Qere form is challenged.",
    "MEASURED from pmarks_Ezek.json at its pinned digest; independently reproduces the boss's C1 codepoint claim")

t = ROWS["P09-002"]["strongest_rejected_alternative"]
t = rep(t, "no samekh or pe mark falls anywhere inside 37.15-28",
        "under the MARKS-3D direction convention no samekh or pe falls in this row's INTERIOR, 37.15-37.27 (the only marks anywhere in range are the pe recorded on 37.14, behind the onset seam, and the samekh recorded on 37.28, at the close seam)",
        "P09-002/mark-scope")
t = rep(t, "(\u2018The sticks... will be in your hand before their eyes\u2019)",
        "(" + LDQ + "The sticks on which you write will be in your hand before their eyes." + RDQ + " (web:Ezek.37.20))",
        "P09-002/a6-3720")
add("P09-002", "strongest_rejected_alternative", t, ["l05_i59", "l05_i60"], "grounds",
    "COMBINED EDIT on one field. Boss work order, carried: the mark claim gets the wording-scope fix the peer's ruling allows -- MEASURED, the only marks anywhere in 37.14-37.29 are pe on 37.14 and samekh on 37.28, and on the convention that a mark sits on the verse it FOLLOWS the 37.28 samekh is the close seam, not the interior, so 'anywhere inside 37.15-28' was loose rather than a disclosure defect. The 8-word A6 run at 37:20 the order also directs is installed in the same field, with the original elision restored so the quotation is exact.",
    "MEASURED from pmarks_Ezek.json and tools/verse_map_web.json at their pinned digests",
    "carries an a6 item (l05_i60) inside a grounds-labelled edit, because both land on this one field")

# ---------------------------------------------------------------- P09-007 A6
t = ROWS["P09-007"]["boundary_rationale"]
t = rep(t, "the near-verbatim \u2018behold, I am against you, Gog\u2019 verdict",
        "the near-verbatim " + LDQ + "Behold, I am against you, Gog" + RDQ + " (web:Ezek.39.1, identically web:Ezek.38.3) verdict",
        "P09-007/a6")
add("P09-007", "boundary_rationale", t, ["l05_i63"], "a6",
    "MEASURED: the 6-word run occurs at exactly two verses in WEB Ezekiel, web:Ezek.39.1 (in span, this row's own onset) and web:Ezek.38.3 (the source of the repetition the sentence names). Both are given, so the near-verbatim claim itself is checkable. Not an A6-b counted device.",
    "MEASURED over tools/verse_map_web.json at its pinned digest")

# ---------------------------------------------------------------- P09-008 A6
t = ROWS["P09-008"]["device_notes"]
t = rep(t, "then a further search after the end of seven months)",
        "then a further search " + LDQ + "after the end of seven months" + RDQ + " (web:Ezek.39.14))",
        "P09-008/a6")
add("P09-008", "device_notes", t, ["l05_i64"], "a6",
    "MEASURED: the run is the WEB's own wording at Ezek.39.14, its only occurrence in WEB Ezekiel and in span. It stood undelimited in the field. Not an A6-b counted device.",
    "MEASURED over tools/verse_map_web.json at its pinned digest")

# ---------------------------------------------------------------- P09-009 A6
t = ROWS["P09-009"]["boundary_rationale"]
t = rep(t, "(\u2018I will set my glory among the nations\u2019)",
        "(" + LDQ + "I will set my glory among the nations" + RDQ + " (web:Ezek.39.21))",
        "P09-009/a6")
add("P09-009", "boundary_rationale", t, ["l05_i69"], "a6",
    "AUTHOR_JUDGEMENT answered NOT COINCIDENTAL. MEASURED: the 8-word run occurs once in WEB Ezekiel, at web:Ezek.39.21, and that is precisely the far-side verse the sentence quotes when weighing the close seam. An out-of-span quotation is still a quotation and owes the convention; the reference makes the far-side weighing checkable.",
    "MEASURED over tools/verse_map_web.json at its pinned digest")

# ---------------------------------------------------------------- P09-010 A6
t = ROWS["P09-010"]["device_notes"]
t = slice_rep(t, "The clause ", " recurs almost verbatim at 39.29",
              "The clause " + LDQ + "I hid my face from them" + RDQ +
              " (web:Ezek.39.24, and again at web:Ezek.39.23), in this witness " + D['HID3924'] + " (oshb:Ezek.39.24),",
              "P09-010/a6-hid")
t = rep(t, "(\u2018I won't hide my face from them any more\u2019)",
        "(" + LDQ + "I won't hide my face from them any more" + RDQ + " (web:Ezek.39.29))",
        "P09-010/a6-nothide")
add("P09-010", "device_notes", t, ["l05_i72", "l05_i73"], "a6",
    "Two runs in one field. MEASURED: 'i hid my face from them' occurs at web:Ezek.39.23 and web:Ezek.39.24, both in span, and the second occurrence is disclosed here because the row's own point is that the clause recurs; \"i won't hide my face from them any more\" occurs once, at web:Ezek.39.29, out of span. The second item's AUTHOR_JUDGEMENT is answered NOT COINCIDENTAL: 39:29 is the very verse the sentence says the clause recurs at, negated.",
    "MEASURED over tools/verse_map_web.json at its pinned digest")

# ---------------------------------------------------------------- P09-011 A6
t = ROWS["P09-011"]["strongest_rejected_alternative"]
t = rep(t, "mercy on the whole house of Israel,",
        LDQ + "mercy on the whole house of Israel" + RDQ + " (web:Ezek.39.25),",
        "P09-011/a6")
add("P09-011", "strongest_rejected_alternative", t, ["l05_i76"], "a6",
    "MEASURED: the 7-word run is the WEB's own wording at Ezek.39.25, its only occurrence and in span, and it stood undelimited inside a list of the row's salvation vocabulary. 'house of Israel' alone would be an A6-b addressee title, but this run is not that, so the convention is owed.",
    "MEASURED over tools/verse_map_web.json at its pinned digest")

# ---------------------------------------------------------------- P10-001 A6 prose
t = ROWS["P10-001"]["boundary_rationale"]
t = rep(t, "('after the city was struck')",
        "(" + LDQ + "after the city was struck" + RDQ + " (web:Ezek.40.1))", "P10-001/a6-struck")
t = rep(t, "'in the visions of God' (one of only three such headers in the book)",
        LDQ + "In the visions of God" + RDQ + " (web:Ezek.40.2; one of only three such headers in the book)",
        "P10-001/a6-visions")
t = rep(t, "'declare all that you see to the house of Israel'",
        LDQ + "Declare all that you see to the house of Israel." + RDQ + " (web:Ezek.40.4)",
        "P10-001/a6-declare")
add("P10-001", "boundary_rationale", t, ["l05_i77", "l05_i78", "l05_i79"], "a6",
    "Three runs in one field, each the WEB's own wording at an in-span verse (MEASURED: 'after the city was struck' once, at web:Ezek.40.1; 'in the visions of god' twice, at web:Ezek.8.3 and the in-span web:Ezek.40.2; 'declare all that you see to the house of israel' once, at web:Ezek.40.4). None is an A6-b counted device. No transport-class membership claim is added or altered, since MT 40:2 and 40:3 are among the thirteen verses brief section 12 routes to the controlling agent.",
    "MEASURED over tools/verse_map_web.json at its pinned digest")

# ---------------------------------------------------------------- P10-001 refs: A6 + A4 combined
L = list(ROWS["P10-001"]["boundary_evidence_refs"])
L[1] = rep(L[1], "transport pair; \"in the visions of God\", one of 3 book-wide",
           "transport pair; the header web:Ezek.40.2 renders " + LDQ + "In the visions of God" + RDQ + ", one of 3 book-wide",
           "P10-001/refs1")
L.append("web:Ezek.40.5 [WARRANT-close] measuring verb starts past close")
L.append("web:Ezek.40.5-Ezek.41.5 [ANCHOR] measuring-verb run beyond this row")
add("P10-001", "boundary_evidence_refs", L, ["l05_i80", "l05_i81", "l05_i82"], "a4",
    "COMBINED EDIT. One A6 refs fix (entry 1: straight double quotes replaced by the convention's curly pair plus the in-field reference) and two A4 installs land on this one field: web:Ezek.40.5 as WARRANT-close, because the close is argued against the measuring verb that starts at 40:5, and the RANGE citation 40:5-41:5 as a RANGE entry tokened ANCHOR, because it describes the following material rather than this row's seam. A single 'set' of the complete final list is the only safe form, for the same reason as at P08-013.",
    "MEASURED over tools/verse_map_web.json; the A4 unmirrored status is EXTRACTED from the ruled items",
    "carries an a6 item (l05_i80) inside an a4-labelled edit; flagged in unresolved_uncertainty for sweep-parity accounting")

json.dump({"edits": EDITS, "problems": PROBLEMS},
          open('edits_part_b.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("part B edits:", len(EDITS))
print("PROBLEMS:", PROBLEMS if PROBLEMS else "none")
