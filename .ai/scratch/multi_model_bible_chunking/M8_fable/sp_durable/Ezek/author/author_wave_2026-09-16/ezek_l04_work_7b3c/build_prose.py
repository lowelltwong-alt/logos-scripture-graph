# -*- coding: utf-8 -*-
import json, io
LANE = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_04_worklist.json'
lane = json.load(open(LANE, encoding='utf-8'))
ROWS = {r['decision_id']: r for r in lane['your_rows']}
LQ, RQ = '\u201c', '\u201d'
PROSE = []


def rep(row, field, pairs, items, why, tier, prefix='', suffix=''):
    cur = ROWS[row][field]
    new = cur
    for old, repl in pairs:
        if isinstance(old, tuple):
            # ASCII-delimited span: slice the exact bytes out of the row rather than retype them
            start, end = old
            assert cur.count(start) == 1, 'SPAN START %r x%d in %s.%s' % (start, cur.count(start), row, field)
            i = cur.index(start)
            j = cur.index(end, i) + len(end)
            old = cur[i:j]
        n = new.count(old)
        assert n == 1, 'ANCHOR COUNT %d for %s.%s: %r' % (n, row, field, old[:70])
        r = repl(old) if callable(repl) else repl
        new = new.replace(old, r, 1)
    new = prefix + new + suffix
    assert new != cur, 'NO CHANGE %s.%s' % (row, field)
    PROSE.append(dict(row_id=row, field=field, op='set', expected_before=cur, value=new,
                      worklist_item_ids=items, why=why, tier=tier))


# ---------------- MARKS-3D sweep ----------------
rep('P05-004', 'device_notes', [], ['P05-004/MARKS_3D/22:31'],
    "pmarks_Ezek.json records ['PE'] on Ezek.22.31, and marks are recorded on the verse they follow, so the mark stands behind this row's onset at 22:31/23:1. The audit called it a closed-section mark; the same file's marks_note defines PE as petuchah (OPEN), so existence and direction reproduce and the section class is corrected.",
    'MEASURED (pmarks_Ezek.json) for the mark, its verse and its class',
    suffix=" Onset-seam mark, disclosed in the three-direction form: MEASURED from pmarks_Ezek.json, MT 22:31 is followed by a PE (petuchah, OPEN section, single-witness), recorded on the verse it follows, so it stands behind this row's ONSET seam at 22:31/23:1. The interior direction carries the samekh after MT 23:10 and the close direction the samekh after MT 23:21, both disclosed above, so all three directions are now on the record. CLASS CORRECTION, recorded rather than silently absorbed: the audit that raised this named it the closed-section mark on MT 22:31; pmarks_Ezek.json records PE, and that file's marks_note defines SAMEKH as setumah (closed section) and PE as petuchah (open section), so the mark's existence and its onset-seam direction reproduce exactly while its section class does not. Under the precedence rule the mark is weak corroboration and carries nothing on its own; this onset rests on the strict word-event formula at 23:1.")

rep('P05-008', 'device_notes', [], ['P05-008/MARKS_3D/24:14'],
    "pmarks_Ezek.json records ['PE'] on Ezek.24.14, i.e. behind this row's onset at 24:14/24:15. Same class correction as at 22:31: the audit called it closed-section; the file records PE (petuchah, open), and the neighbouring row P05-007 already calls it a pe, agreeing with the file.",
    'MEASURED (pmarks_Ezek.json) for the mark, its verse and its class',
    suffix=" Onset-seam mark, disclosed in the three-direction form: MEASURED from pmarks_Ezek.json, MT 24:14 is followed by a PE (petuchah, OPEN section, single-witness), recorded on the verse it follows, so it stands behind this row's ONSET seam at 24:14/24:15. The interior direction carries a single-witness samekh after MT 24:24 (disclosed here) and the close direction the samekh after MT 24:27 (disclosed above), completing the three directions. CLASS CORRECTION, recorded not absorbed: the audit named this the closed-section mark on MT 24:14; pmarks_Ezek.json records PE, and its marks_note defines SAMEKH as setumah (closed) and PE as petuchah (open), so the mark and its direction reproduce while the section class is corrected. Under the precedence rule the PE is weak corroboration; this onset rests on the full-form strict word-event formula at 24:15.")

# ---------------- GROUNDS sweep ----------------
rep('P05-005', 'boundary_rationale', [], ['P05-005/GROUNDS/23:35-samekh'],
    "Ordered disclosure. pmarks_Ezek.json records ['SAMEKH'] on Ezek.23.35; recorded on the verse it follows, that places it on this row's CLOSE seam at 23:35/23:36, where the row previously disclosed only the 23:21, 23:27, 23:31 and 23:34 marks.",
    'MEASURED (pmarks_Ezek.json) for the mark; MEASURED (Ezek_oshb.txt) for the 23:34 verse-final utterance formula',
    suffix=" CLOSE-SEAM MARK, disclosed as ordered: MEASURED from pmarks_Ezek.json, MT 23:35 is followed by a SAMEKH (setumah, closed section, single-witness). Because a mark is recorded on the verse it follows, this one stands on THIS row's close seam at 23:35/23:36 - not behind the onset and not mid-unit - so the close is corroborated on its near face by the mark and on its far face by the addressee-count shift at 23:36. Under the precedence rule the samekh is weak corroboration and decides nothing alone. One further measured fact is put on the record here without being acted on, because it bears on the rejected alternative rather than on this disclosure: MT 23:34 ends verse-finally on the utterance formula (oshb:Ezek.23.34), which means the messenger formula opening MT 23:35 satisfies CUT-RULE limb (b), so the 23:34/23:35 rival is a licensed, two-faced rival and not one defeated by addressee continuity alone. The seam is NOT moved here; the row stands at medium, which is exactly CONF-CAL's second limb for a licensed rival held on stated grounds, and the point is escalated for the controlling agent.")

rep('P05-007', 'strongest_rejected_alternative', [], ['P05-007/GROUNDS/A9-24:8-24:9'],
    'A9 order: name and weigh the 24:8 PE and the 24:9 messenger formula. Both measured. CUT-RULE licenses neither limb at 24:9, so the rival is mark-only and, per CONF-CAL, weighed but never fatal.',
    'MEASURED (pmarks_Ezek.json) for the PE; MEASURED (Ezek_oshb.txt) for the 24:9 messenger formula, the 24:8 verse-final words and the 24:6 addressee',
    suffix=" (3) Cutting at 24:8/24:9 - the alternative the Masoretic paragraph layer proposes, named and weighed here as A9 requires. What the rival's near face carries: MEASURED from Ezek_oshb.txt, MT 24:9 opens on the long-form messenger formula after a therefore-particle (oshb:Ezek.24.9). What its far face carries: MEASURED from pmarks_Ezek.json, MT 24:8 is followed by a PE (petuchah, open section, single-witness) - and nothing else, because MEASURED from Ezek_oshb.txt MT 24:8 ends on a purpose infinitive (oshb:Ezek.24.8), with no utterance, recognition or I-YHWH-have-spoken signature anywhere in that verse. Whether CUT-RULE licenses it: it does NOT. Limb (a) fails, because the addressee does not change - MT 24:6 already addresses the bloody city (oshb:Ezek.24.6) and MT 24:9 addresses that same city. Limb (b) fails, because the verse immediately before it does not END on a close-role formula, and a mark alone never satisfies limb (b). The stated ground on which this row holds: under the precedence rule the PE after MT 24:8 is weak corroboration and is disclosed FOR the alternative it corroborates, not for this row, and it is outranked by the licensed drivers this row does rest on - the fused dateline-plus-word-event onset at 24:1 and the stacked I-YHWH-have-spoken plus utterance close at 24:14. So the 24:8/24:9 cut is a mark-only, paragraph-grade rival: weighed, disclosed and held, and under CONF-CAL never fatal to this row's grade.")

rep('P07-001', 'strongest_rejected_alternative', [], ['P07-001/GROUNDS/29:7-29:8+29:1-16'],
    'The order requires this field to name both the 29:7/29:8 rival and the 29:1-16 tiling and to carry the A10 disclosure of the 29:7 mark. All three are measured below. The 29:7/29:8 rival turns out to be licensed and two-faced (the addressee shifts from masculine to feminine singular at 29:8), which is CONF-CAL MEDIUM and independently corroborates the ruled demotion from high to medium.',
    'MEASURED (Ezek_oshb.txt) for every clause and person shift cited; MEASURED (pmarks_Ezek.json) for the marks and for the absence of a mark at 29:6 and 29:9; EXTRACTED (book_strategy_Ezek.md line 408) for the 29:1-16 sketch',
    prefix='Three alternatives are weighed. (1) ',
    suffix=" Two further readings are weighed, as ordered. (2) Cutting at 29:7/29:8 - the alternative the paragraph layer proposes, carrying the ordered A10 mark disclosure. A10: MEASURED from pmarks_Ezek.json, MT 29:7 is followed by a SAMEKH (setumah, closed section, single-witness), recorded on the verse it follows, and MT 29:7 additionally carries one ketiv/qere pair, already disclosed in this row. What the rival's near face carries: MEASURED from Ezek_oshb.txt, MT 29:8 opens on the long-form messenger formula after a therefore-particle (oshb:Ezek.29.8), and with it a grammatical addressee shift - MT 29:7 addresses a masculine singular and MT 29:8 a feminine singular (oshb:Ezek.29.7, oshb:Ezek.29.8), that is, from Pharaoh to the land. Whether CUT-RULE licenses it: limb (a) IS satisfied on that addressee change, so this rival is licensed and two-faced and is not dismissed. Its far face is nevertheless thin: MT 29:7 ends with no close-role formula, so limb (b) would fail there and only the SAMEKH stands. The stated ground on which this row holds: the crocodile verdict's own refrain is the recognition formula at MT 29:9, and MT 29:10 restates the same charge as a fresh against-you cycle (oshb:Ezek.29.10); under the precedence rule the SAMEKH after MT 29:7 is weak corroboration and is disclosed FOR this rival, not for this row. A licensed two-faced rival held on stated grounds is CONF-CAL's MEDIUM limb, which is where this row's grade now sits. (3) Tiling MT 29:1-29:16 as ONE row - the reading the pinned strategy itself sketches, EXTRACTED from book_strategy_Ezek.md line 408 inside its flagged chs 25-32 region, which reads there as 29:1-16 with the mid-verse WEB paragraph at 29:9 and the forty-years turn at 29:13. What supports it: MEASURED from Ezek_oshb.txt, no dateline and no word-event formula stands anywhere between MT 29:1 and the next dateline at MT 29:17; MEASURED from pmarks_Ezek.json, the only marks inside that stretch follow MT 29:7 and MT 29:12, and NO mark stands on MT 29:9. And this row's own close is the weak shape under the #e14 Q2 refinement: MEASURED from Ezek_oshb.txt, the recognition formula in MT 29:9 ends at the etnachta and an INDEPENDENT causal clause with a finite verb fills the rest of the verse (oshb:Ezek.29.9) - unlike MT 29:6, whose words after its own recognition clause are a causal phrase built on an infinitive construct (oshb:Ezek.29.6), a dependent completion that grades as an ordinary licensed near-face signal rather than the weak mid-verse shape. The stated ground on which this row holds: MT 29:10 opens a fresh against-you verdict cycle restating the charge, so the collision is resolved at the verse boundary after 29:9. The seam is NOT moved here - that is the controlling agent's call and this wave does not make it - and the weakness of the 29:9 close together with the strategy's own 29:1-16 sketch are disclosed rather than argued away; they are why this row is graded medium and not high.")

# ---------------- A6 sweep and BOSS_RETURN ----------------
rep('P06-001', 'boundary_rationale',
    [('toward the children of Ammon', LQ + 'toward the children of Ammon' + RQ + ' (web:Ezek.25.2, WEB)')],
    ['P06-001/A6/toward-the-children-of-ammon'],
    "A6 install. MEASURED: the five-word run is the WEB rendering at Ezek.25.2 and at no other verse in the book (1 of 1273 scanned). A6-b does not reach it - the run names the addressee nation, which is neither one of A6-b's counted devices nor one of its inventoried addressee titles - so the delimiter and the in-field web reference are owed.",
    'MEASURED (tools/verse_map_web.json, whole-book scan) for the run and its single attachment')

rep('P06-005', 'boundary_rationale',
    [('("in the eleventh year, in the first of the month")', '(' + LQ + 'in the eleventh year, in the first of the month' + RQ + ', web:Ezek.26.1, WEB)')],
    ['P06-005/A6/in-the-eleventh-year'],
    "A6 install on the un-delimited gloss. MEASURED: the ten-word run is the WEB rendering at Ezek.26.1 and at no other verse (1 of 1273). The row's later full citation of WEB 26:1 was already compliant; this straight-quoted gloss was not. A dateline is a counted device in the inventory but is not in A6-b's exempt enumeration, so the convention is owed.",
    'MEASURED (tools/verse_map_web.json) for the run and its single attachment')

rep('P06-005', 'device_notes',
    [(('the "behold, I am against you"', 'verdict-onset idiom'),
      lambda old: 'the ' + LQ + 'Behold, I am against you' + RQ + ' (web:Ezek.26.3, WEB) verdict-onset idiom, '
                  + old[old.index('" (') + 3: old.index(' (oshb:Ezek.26.3))')] + ' (oshb:Ezek.26.3)')],
    ['P06-005/A6/behold-i-am-against-you'],
    'A6 install. MEASURED: the five-word run occurs in the WEB at ten verses book-wide (13:8, 13:20, 21:3, 26:3, 28:22, 29:3, 29:10, 35:3, 38:3, 39:1); the audit listed three of those. Only 26:3 is in this span and it is the verse the row asserts, so that is the reference installed. The ch 20/21 renumbering zone is deliberately not entered: web:Ezek.21.3 would require dual-face writing and is not this row\u2019s claim. Capitalisation follows the WEB.',
    'MEASURED (tools/verse_map_web.json, whole-book scan) for all ten attachments')

rep('P06-009', 'boundary_rationale',
    [(('"take up a lamentation', 'over Tyre"'), LQ + 'take up a lamentation over Tyre' + RQ + ' (web:Ezek.27.2, WEB)'),
     ('because a qinah-labelled unit is never split \u2014',
      'because a qinah-labelled unit is never split \u2014 a rule the pinned strategy states in its over-split guard at book_strategy_Ezek.md \u00a76, line 351, and restates for this region in \u00a77 as one 36-verse qinah, so the claim is sourced and is not an invented universal \u2014'),
     ('("you have become a terror, and will be no more")',
      '(the WEB renders it ' + LQ + 'You have come to a terrible end, and you will be no more.' + RQ + ', web:Ezek.27.36, WEB)'),
     ('and no formula marks any internal point in the chapter.',
      'and no formula licenses an internal seam. That last claim is CORRECTED here rather than repeated: its earlier absolute form, that no formula marks any internal point in the chapter, is FALSE, because MEASURED from Ezek_oshb.txt the long-form messenger formula does stand inside MT 27:3 (oshb:Ezek.27.3). It licenses nothing - it sits mid-verse inside the commissioned speech frame, and under CUT-RULE neither limb is met, since the addressee does not change (Tyre throughout) and MT 27:2 does not END on a close-role formula. MEASURED over the same file, that is the chapter\u2019s ONLY internal messenger formula, and the word-event formula occurs only at the onset, MT 27:1.')],
    ['P06-009/BOSS_RETURN', 'P06-009/A6/take-up-a-lamentation-over-tyre', 'P06-009/A6/you-have-become-a-terror'],
    "Four orders land in this field. (i) The boss's 27:3 correction, reproduced independently from the witness and scoped so the row's conclusion survives on a true premise. (ii) The never-split sentence is kept and sourced to the over-split guard, whose location I reproduced myself: line 351 falls inside \u00a76, since \u00a76 opens at line 285 and \u00a77 at line 360, so the order's \u00a76 attribution is correct. (iii) A6 install for the qinah command. (iv) The you-have-become-a-terror run is NOT this chapter's wording at all: MEASURED, it is the WEB rendering of Ezek.28.19 and of no other verse book-wide, while WEB 27:36 reads that Tyre has come to a terrible end. The row attributed 28:19's English to ch 27's own colophon, so the repair quotes the row's actual close verse, delimited and referenced, and leaves the 28:19 parallel to be argued where it is in span.",
    'MEASURED (Ezek_oshb.txt) for 27:3, 27:1 and the absence elsewhere; EXTRACTED (book_strategy_Ezek.md lines 351, 285, 360, 405-406); MEASURED (tools/verse_map_web.json) for both WEB renderings')

rep('P06-009', 'strongest_rejected_alternative',
    [('and a qinah-labelled unit is never split, regardless of length;',
      'and a qinah-labelled unit is never split, regardless of length \u2014 a rule the pinned strategy states at book_strategy_Ezek.md \u00a76, line 351, so it is sourced and not an invented universal;')],
    ['P06-009/BOSS_RETURN'],
    "The boss struck four peer findings that read this sentence as an unsourced universal; they are false positives, so the sentence stays and gains its source. I also re-verified this field's own negative claim instead of assuming it.",
    'EXTRACTED (book_strategy_Ezek.md line 351) for the rule; MEASURED (pmarks_Ezek.json, Ezek_oshb.txt) for the four rival points',
    suffix=" Verification of that negative, recorded rather than asserted: MEASURED from pmarks_Ezek.json, no parashah mark stands on MT 27:11, 27:12, 27:25 or 27:26 - the chapter's only mark is the samekh after MT 27:36 - and MEASURED from Ezek_oshb.txt neither the messenger formula (chapter-internal only at MT 27:3) nor the word-event formula (only at MT 27:1) falls at any of those four points, so the claim holds exactly as written.")

rep('P06-009', 'device_notes',
    [('36 verses, well beyond even the extended 14-16 verse cap allowed for measured/listed blocks;',
      "36 verses (MEASURED over Ezek_oshb.txt) against the strategy's 7-10 verses-per-row target, which is the benchmark that governs this row; the 14-16 verse allowance is NOT available here and the earlier disclosure against it is CORRECTED, because the pinned strategy grants that allowance only to the measured-and-listed blocks it names by chapter and this chapter is not among them;")],
    ['P06-009/BOSS_RETURN'],
    'The A7 benchmark correction the boss ordered. EXTRACTED from book_strategy_Ezek.md lines 330-331: the target is 7-10 verses per row and the 14-16 allowance is restricted to the named measured-and-listed blocks, which do not include ch 27. Disclosing 36 verses against an allowance this row cannot claim understated the deviation. The 36 is my own count of the chapter in the pinned witness, not a copied figure.',
    'MEASURED (Ezek_oshb.txt, ch 27 verse count = 36); EXTRACTED (book_strategy_Ezek.md lines 330-331) for the target and the allowance scope')

rep('P06-010', 'boundary_rationale',
    [('stacking "for I have spoken it" (the i_am_yhwh_spoken family)',
      'stacking ' + LQ + 'for I have spoken it' + RQ + ' (web:Ezek.28.10, WEB), the i_am_yhwh_spoken family in its name-less member,')],
    ['P06-010/A6/for-i-have-spoken-it'],
    "A6 install, plus one precision the install would otherwise carry past. MEASURED: the run occurs in the WEB at exactly Ezek.23.34, 26.5, 28.10 and 39.5 - verse for verse the v2 inventory's name-less sub-family of i_am_yhwh_spoken (4 verses), not the 14 name-bearing members. So the reference is web:Ezek.28.10 and the family label is qualified, which stops a reader folding 28:10 into the 14-list. A6-b's exempt enumeration is messenger, utterance, recognition, word-event and hand-of-YHWH; I-have-spoken is not in it, so the convention is owed.",
    'MEASURED (tools/verse_map_web.json, whole-book scan); EXTRACTED (ezek_device_inventory.v2.json, formulae.i_am_yhwh_spoken) for the sub-family membership')

rep('P06-011', 'boundary_rationale',
    [(('"son of man, take up a lamentation', 'over the king of Tyre"'),
      LQ + 'Son of man, take up a lamentation over the king of Tyre' + RQ + ' (web:Ezek.28.12, WEB)'),
     ('the close pattern ("you have become a terror, and will exist no more") mirrors 27:36\'s terminal clause exactly',
      'the close pattern ' + LQ + 'You have become a terror, and you will exist no more.' + RQ + " (web:Ezek.28.19, WEB) mirrors MT 27:36's terminal clause in the CONSONANTAL Hebrew and not in the translation - MEASURED from Ezek_oshb.txt, the two verses end consonant for consonant on the same four words and differ only in the Masoretic pointing, feminine singular at MT 27:36 against masculine singular at MT 28:19, while the WEB renders MT 27:36 quite differently as " + LQ + 'You have come to a terrible end, and you will be no more.' + RQ + ' (web:Ezek.27.36, WEB); the earlier claim of an exact mirror held only of the Hebrew and is scoped here')],
    ['P06-011/A6/son-of-man-take-up-a-lamentation', 'P06-011/A6/you-have-become-a-terror'],
    "Two A6 installs, and one claim narrowed to what the bytes support. MEASURED: each run is the WEB rendering at exactly one verse book-wide (28:12 and 28:19), both in this row's span. The row's mirrors-27:36-exactly claim was true of the consonantal Hebrew and false of the WEB, which renders the two verses with different English; the sentence now says which witness the mirror holds in and discloses the pointing difference. web:Ezek.27.36 is a far-side reference under DEF-A4-ARGUED clause 4, outside the window [28:10, 28:20]: recorded, never a defect.",
    'MEASURED (tools/verse_map_web.json) for both runs; MEASURED (Ezek_oshb.txt) for the consonantal identity and the pointing difference')

rep('P06-011', 'literature_type_guess',
    [('qinah over the king of Tyre', 'qinah ' + LQ + 'over the king of Tyre' + RQ + ' (web:Ezek.28.12, WEB)')],
    ['P06-011/A6/over-the-king-of-tyre'],
    'A6 install, executed as ruled even though the field is a genre label rather than argued prose. MEASURED: the five-word run is the WEB rendering at Ezek.28.12 only, in span. A6-b does not reach it (not a counted device, not an inventoried addressee title), so on the rule as written the delimiter and reference are owed even here. The reservation is recorded in unresolved_uncertainty rather than used to decline the order.',
    'MEASURED (tools/verse_map_web.json, whole-book scan)')

io.open('prose_edits.json', 'w', encoding='utf-8').write(json.dumps(PROSE, ensure_ascii=False, indent=1))
print('OK %d prose edits built' % len(PROSE))
for e in PROSE:
    print('  %-8s %-32s items=%s' % (e['row_id'], e['field'], e['worklist_item_ids']))
