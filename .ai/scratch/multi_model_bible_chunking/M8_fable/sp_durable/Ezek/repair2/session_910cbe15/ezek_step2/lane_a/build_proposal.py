#!/usr/bin/env python3
"""Lane A: build proposal.json from the live prose by EXACT-MATCH replacement.

Why this way: the Hebrew runs, the curly WEB quotes and the row voice must survive untouched. Retyping them
invites a transcription error that no gate in this step would catch. So every edit is anchored on a literal
substring of the live prose and asserted to occur exactly once; a drifted anchor is a hard failure, not a
silent no-op.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLICES = json.loads((HERE.parent / "step2_slices.v1.json").read_text(encoding="utf-8"))["slices"]

# ---------------------------------------------------------------- Hebrew lifted from the slices themselves
def _grab(rid, field, start_marker, end_marker):
    s = SLICES[rid]["live_prose"][field] if field != "refs" else "\n".join(SLICES[rid]["live_boundary_evidence_refs"])
    i = s.index(start_marker) + len(start_marker)
    j = s.index(end_marker, i)
    out = s[i:j].strip()
    assert out, (rid, field, start_marker)
    return out

# 39:24's own ending, from P09-010's pinned bytes for that verse (same verse, same witness).
HIDE_FACE_3924 = _grab("P09-010", "refs", "עָשִׂ֣יתִי אֹתָ֑ם", ")")
# 32:32's opening particle, from P07-008's own close bytes.
KI_3232 = _grab("P07-008", "device_notes", "close bytes (oshb:Ezek.32.32):", "נָתַ֥תִּי")
# 36:23's utterance signature, from P08-012's own bytes for that verse.
UTT_3623 = _grab("P08-012", "boundary_rationale", "כִּי אֲנִ֣י יְהוָ֗ה", "בְּהִקָּדְשִׁ֥י")
# The two addressee titles, lifted from P08-002's own live prose. MY MISTAKE, CORRECTED: the first pass typed
# these two runs by hand and corrupted both (a spurious he in the second word of the first title, the wrong
# accent on the first word of the second). Nothing in this step's gate reads Hebrew, so only extraction from
# the slice can be trusted here.
TITLE_ISRAEL = _grab("P08-002", "strongest_rejected_alternative", "changes from ", " at 33.10")
TITLE_PEOPLE = _grab("P08-002", "strongest_rejected_alternative", "at 33.10 to ", " at 33.12")

EDITS = {}


def E(rid, field, old, new):
    EDITS.setdefault(rid, []).append((field, old, new))


# ============================================================================== P08-002  (medium_low)
E("P08-002", "boundary_rationale",
  "immediately following the samekh-marked close at oshb:Ezek.33.9.",
  "immediately following the samekh-marked close at oshb:Ezek.33.9; that far face carries the mark and no "
  "formula, while the near face is this re-address to the people, after the watchman charge given to the "
  "prophet.")
E("P08-002", "boundary_rationale",
  " MT 33.20 carries NO sof-pasuq in this witness — it stands instead with an untyped OSHB editorial note, "
  "'We read punctuation in L differently from BHS,' immediately before the pe. That absence is MEASURED from "
  "the pinned marks input, whose own resolved-anomaly record names this verse and types it as a real source "
  "fact rather than a parsing gap (the section-mark record, "
  "arithmetic_anomalies_resolved.sof_pasuq_1272_for_1273_verses, keys verse/finding/status). This is disclosed "
  "as a single-witness punctuation divergence; no boundary is argued from the absent mark, only from the pe "
  "that follows and the topical restatement it closes.",
  " The section-mark witness records that this verse carries no sof pasuq; the editors' note stands in its "
  "place, 'We read punctuation in L differently from BHS,' immediately before the pe (single-witness). No "
  "boundary is argued from the absent mark, only from the pe that follows and the topical restatement it "
  "closes. The near face of that close is a verdict clause with no formula — the discourse close of the "
  "disputation — and a dateline opens the material past it; a close seam of that shape is what this row's "
  "medium_low records, whatever stands on its far face.")
E("P08-002", "strongest_rejected_alternative",
  SLICES["P08-002"]["live_prose"]["strongest_rejected_alternative"],
  "The rival onset is the 'and you, son of man' (ve'attah) at Ezek.33.12, which re-addresses the hearers as "
  "%s where 33.10 has %s "
  "(oshb:Ezek.33.10, oshb:Ezek.33.12; WLC/OSHB, single witness). That shift does not license a cut: the two "
  "titles name one audience inside one speech — the first stands at 33.10, 33.11 and 33.20, the second at "
  "33.2, 33.12 and 33.17 — and it is the second that opens the chapter's whole address. The rival's own "
  "close-shaped cluster cannot supply the missing onset either: 33:11's utterance formula stands mid-verse, at "
  "word 5 of that verse's 25 counted from one, with independent imperatives running on after it. The pe "
  "recorded on 33:11 is disclosed for the rival as a paragraph mark, not as an onset. Independently, a cut "
  "there would leave 33:10-11, two verses that are not a complete word-event unit, and that bar holds the span "
  "whatever shape the rival has. The disputation therefore runs on as one 'you say ... but I say' unit across "
  "33:10-20, which is the near face on both of this row's seams." % (TITLE_PEOPLE, TITLE_ISRAEL))
# device_notes edited in three anchored pieces, NOT rewritten, so the K/Q Hebrew is never retyped.
E("P08-002", "device_notes",
  "held at medium_low rather than split: the licensed rival onset is the ve'attah at 33.12, licensed by an "
  "addressee change under CUT-RULE limb (a), and the ground for holding against it is the bar on a row under "
  "three verses that is not a complete word-event unit, since a cut there would leave 33:10-11, under three "
  "verses and not a complete word-event unit.",
  "held at medium_low rather than split: the rival onset at 33.12 re-addresses the same audience under a "
  "second title and is not licensed, and a cut there would leave 33:10-11, under three verses and not a "
  "complete word-event unit.")
E("P08-002", "device_notes", "K/Q, A2 disclosure (single-witness):", "K/Q disclosure (single-witness):")
E("P08-002", "device_notes",
  "each of the two notes carries two morpheme separators in the K/Q layer which are dropped from the forms as "
  "given here, and no boundary is argued from either Qere. MEASURED from the section-mark record, kq, where "
  "the entry at each of these two verses is a list of K-Q pair strings with one member.",
  "each of the two notes carries two morpheme separators in the apparatus which are dropped from the forms as "
  "given here, and no boundary is argued from either Qere.")

# ============================================================================== P08-003  (medium)
E("P08-003", "boundary_rationale",
  "Onset: MT 33:20 is followed by a pe (single-witness), corroborating the onset at 33:21.",
  "Onset: MT 33:20 is followed by a pe (single-witness), corroborating the onset at 33:21, and that pe stands "
  "where the verse itself carries no sof pasuq. The onset's near face is the dateline, a licensed onset of its "
  "own; its far face carries that mark and no formula.")
E("P08-003", "boundary_rationale",
  "before Ezek.33.23 opens a fresh, formally distinct word-event oracle.",
  "before Ezek.33.23 opens a fresh, formally distinct word-event oracle; that close is two-faced, the "
  "hand-and-mouth-opening notice on its near face against the fresh word-event on its far face. A licensed "
  "near face at the onset with a mark-only far face behind it is the shape this row's medium records.")
E("P08-003", "device_notes",
  "Under-3-verse row, disclosed as a two-verse unit bounded by 33:21's dateline and the pe after 33:22, rather "
  "than by a tier-1 onset of its own.",
  "Under-3-verse row, disclosed as a two-verse unit bounded by 33:21's dateline — itself a tier-1 onset, "
  "one of the 14 in the book — and the pe after 33:22.")

# ============================================================================== P09-009  (medium)
E("P09-009", "device_notes",
  "Held below medium because, as at 39.1, the onset is a sub-onset sharing 38.1's word-event frame rather than "
  "an independent onset of its own class. Onset corroboration: one samekh stands after MT 39:16 in this "
  "witness, single witness.",
  "The onset is a sub-onset: it shares 38.1's governing word-event frame, but it turns the address from Gog to "
  "the birds and beasts, and that addressee change licenses it. Held at medium because the seam behind it "
  "carries a mark and no formula — one samekh stands after MT 39:16 in this witness, single witness.")

# ============================================================================== P09-011  (medium)
E("P09-011", "boundary_rationale",
  "Onset: a messenger formula reopens at oshb:Ezek.39.25",
  "Onset: the far face carries a samekh and no close-role formula — that verse ends %s "
  "(oshb:Ezek.39.24; WLC/OSHB, single witness) — and on the near face a messenger formula reopens at "
  "oshb:Ezek.39.25" % HIDE_FACE_3924)
E("P09-011", "boundary_rationale",
  "on the word ‘therefore,’ immediately turning from the exile retrospective to the restoration "
  "promise;",
  "on the word ‘therefore,’ immediately turning from the exile retrospective to the restoration "
  "promise — the addressee does not change across that turn, so it is a discourse turn and not a licensed "
  "sub-onset;")
E("P09-011", "boundary_rationale",
  "opens on a dateline plus hand-of-YHWH and transport at Ezek.40.1.",
  "opens on a dateline plus hand-of-YHWH and transport at Ezek.40.1. The close is therefore two-faced and top "
  "grade on both faces, while the onset stands on a mark behind and a discourse turn ahead: that is the shape "
  "this row's medium records.")

# ============================================================================== P07-008  (high)
E("P07-008", "boundary_rationale",
  "(year 12, month 12, day 15 -- a half-month after 32:1's date, perfect hayah word-event form)",
  "(year 12, day 15, with no month word in the verse, against the twelfth month named at 32:1; perfect hayah "
  "word-event form)")
E("P07-008", "boundary_rationale",
  "The genre call (oracle_against_nation vs. lament_qinah) is held, not resolved, at low confidence.",
  "The genre question is held, not resolved, and does not bear on the seam grade. Both seams stand two-faced "
  "and top grade: 32:16 ends on the utterance signature, verse-final, with a pe after it, and 32:32 likewise "
  "ends verse-final on that signature with a pe, against a fresh strict word-event opening past this close. "
  "Inside the row the utterance at 32:31 is paragraph-final, since 32:32 opens on %s (oshb:Ezek.32.32; "
  "WLC/OSHB, single witness) with no onset-class device after it, and 32:18's son-of-man address corroborates "
  "the onset rather than opening a unit of its own; no rival of a licensed class stands at either seam, and "
  "the row's sixteen-verse length is the extent of the Sheol roster itself." % KI_3232)
E("P07-008", "device_notes",
  "MT 32:16 carries a following pe, single witness, at this unit's own onset seam.",
  "MT 32:16 ends on the utterance signature, verse-final, and carries a following pe, single witness, at this "
  "unit's own onset seam.")

# ============================================================================== P08-012  (medium)
E("P08-012", "boundary_rationale",
  "the fourth and last such hard seam since Ezek.33.1 (after 33.1, 33.23, 34.1)",
  "the fifth such hard seam since Ezek.33.1 (33.1, 33.23, 34.1, 35.1, 36.16) and not the last — 37.15 and "
  "38.1 follow")
E("P08-012", "boundary_rationale",
  "a recognition-pattern clause addressed to the nations (matching the recognition-family ‘know ... that "
  "I am Yahweh’ pattern directly visible in the full verse above). This is disclosed as recognition-family "
  "texture rather than claimed as membership in a specific enumerated sweep beyond what these bytes themselves "
  "show.",
  "a recognition clause addressed to the nations, one of the 64 such verses book-wide and refrain-grade in "
  "class. Both that clause and the utterance signature stand mid-verse: the verse runs on after %s with a "
  "dependent temporal infinitive, and no mark is recorded on it. Its far face, 36.24, opens on no particle of "
  "any tracked class, belongs to no device class and carries no mark (oshb:Ezek.36.24); a close whose near "
  "face is refrain-grade in class but mid-verse in position, against an empty far face, is the shape this "
  "row's medium records." % UTT_3623)
E("P08-012", "strongest_rejected_alternative",
  "which under #e14 Q2 grades as an ordinary licensed near-face signal and not the weak mid-verse shape, and "
  "36.24's ‘for’ clause opens a fresh movement (the actual return and renewal) rather than continuing "
  "36.16-23's retrospective argument about the profaned name;",
  "which grades as an ordinary licensed near-face signal and not the weak mid-verse shape, and 36.24 opens the "
  "actual return and renewal rather than continuing 36.16-23's retrospective argument about the profaned name "
  "— no particle stands there in the Hebrew, and the English version's ‘For’ is translation "
  "wording that argues no boundary;")

# ============================================================================== P04-008  (medium)
E("P04-008", "boundary_rationale",
  "The poem's own refrains, sharpened and polished, the sword doubled and then tripled, run unbroken between "
  "the two without a competing onset.",
  "Both outer seams are two-faced and top grade: a pe stands in this witness immediately before the "
  "word-event onset verse (single witness), and the close formula carries a pe after it with a fresh "
  "word-event opening past that. The poem's own refrains, sharpened and polished, the sword doubled and then "
  "tripled, run between the two; the one interior seam that carries real evidence on both faces is weighed "
  "below and held as a paragraph, and that held rival is the granularity judgement this row's medium carries.")

# ============================================================================== P03-014  (medium_low)
E("P03-014", "boundary_rationale",
  "An oath formula recurs mid-verse at 18:3 ('as I live, declares the Lord YHWH'), weighed as texture inside "
  "the refutation rather than a row-final close, since the clause on the proverb's future use continues after "
  "it in the same verse.",
  "An oath formula opens 18:3 ('as I live, declares the Lord YHWH') in its first five words, with the clause on the proverb's future use running on "
  "after it in the same verse, so it stands as texture inside the refutation and not as a row-final close. The "
  "onset seam is two-faced and top grade — the strict word-event at 18:1 against the "
  "I-YHWH-have-spoken formula, verse-final, with a pe after it behind the seam (oshb:Ezek.17.24) — while "
  "the close is a case turn inside one word-event unit, carrying no formula device on either face, with the "
  "samekh recorded there corroborating the close and not deciding it: that is the shape this row's medium_low "
  "records.")

# ============================================================================== P03-015  (medium_low)
E("P03-015", "boundary_rationale",
  "a genuine verse-final refrain closing the first case before 18:10 opens with no formula of its own."
  if "a genuine verse-final refrain closing the first case before 18:10 opens with no formula of its own."
  in SLICES["P03-015"]["live_prose"]["boundary_rationale"] else
  "a genuine verse-final refrain closing the first case before the wicked son's case opens at 18:10 with no "
  "formula of its own.",
  "a genuine verse-final refrain closing the first case before the wicked son's case opens at 18:10 with no "
  "formula of its own. Both of this row's seams are case turns inside one word-event unit: at the onset the "
  "samekh recorded on 18:4 behind the seam corroborates and does not decide, with no formula device on either "
  "face, and at the close the verse-final utterance at 18:9 stands paragraph-final, since 18:10 brings no "
  "fresh onset and no mark falls at that seam. That is the shape this row's medium_low records.")
E("P03-015", "strongest_rejected_alternative",
  "unlike its mid-verse recurrences elsewhere in MT 18 (18:23, 18:30).",
  "unlike its mid-verse recurrences elsewhere in MT 18 (18:3, 18:23, 18:30, 18:32).")

# ============================================================================== P03-016  (medium_low)
E("P03-016", "boundary_rationale",
  "restates 18:4's thesis and closes the argument, matched by a samekh recorded on this same verse.",
  "restates 18:4's thesis and closes the argument, matched by a samekh recorded on this same verse. Behind the "
  "onset the preceding verse ends on the utterance formula, which stands paragraph-final there because 18:10 "
  "brings no fresh onset, and no mark falls at that seam; ahead of 18:20's samekh the next case turn opens "
  "with no formula of its own. Both seams are case turns inside one word-event unit, the close corroborated by "
  "a samekh that does not decide it and the onset carrying no mark at all: that is the shape this row's "
  "medium_low records.")

# ============================================================================== P03-017  (medium_low)
E("P03-017", "boundary_rationale",
  "the samekh mark closes the whole verse regardless of the formula's mid-verse position, and it is that mark, "
  "not formula-finality, that is used as the close evidence here.",
  "the samekh recorded on the verse corroborates that close and does not decide it. The seam itself is a case "
  "turn inside one word-event unit: the utterance formula inside 18:23 is mid-verse and so carries no "
  "close role, and the case past the seam opens with no formula device of its own; the onset seam behind, "
  "marked by the samekh after 18:20, is the same shape, a case turn with no formula on either face. That is "
  "what this row's medium_low records.")

# ============================================================================== P03-018  (medium_low)
E("P03-018", "boundary_rationale",
  "Israel's objection is quoted between the case and its restatement, at 18:25, inside this same span.",
  "Israel's objection is quoted between the case and its restatement, at 18:25, inside this same span. Both "
  "seams are case turns inside one word-event unit, each corroborated by a samekh that does not decide it "
  "— the one recorded after 18:23 behind the onset, the one on 18:26 at the close — and neither "
  "carries a seam-role formula on either face, 18:23's own utterance formula standing mid-verse there: that "
  "is the shape this row's medium_low records.")

# ============================================================================== P03-019  (medium_low)
E("P03-019", "boundary_rationale",
  "Israel's objection recurs at 18:29 in a form the OSHB editors flag with a single-witness note against BHS.",
  "Israel's objection recurs at 18:29, where a single-witness OSHB editorial note stands.")
E("P03-019", "boundary_rationale",
  "(oshb:Ezek.18.30) (“Therefore I will judge you, house of Israel, everyone according to his ways”, "
  "web:Ezek.18.30).",
  "(oshb:Ezek.18.30) (“Therefore I will judge you, house of Israel, everyone according to his ways”, "
  "web:Ezek.18.30); the formula embedded there is the utterance formula, and no messenger formula falls in "
  "this span.")
E("P03-019", "boundary_rationale",
  "not the formula's position, that anchor this close.",
  "not the formula's position, that anchor this close. The onset seam is a case turn inside one word-event "
  "unit, carrying no formula device on either face, with the samekh after 18:26 behind it corroborating and "
  "not deciding: that is the shape this row's medium_low records.")

# ============================================================================== P09-001  (medium)
E("P09-001", "boundary_rationale",
  "The unit runs as one uninterrupted scene:",
  "The unit is held as one scene, with the live rival inside it weighed below:")
E("P09-001", "boundary_rationale",
  "as a word to 'son of man' (address.son_of_man, oshb:Ezek.37.11",
  "as a word to 'son of man' (oshb:Ezek.37.11")
E("P09-001", "boundary_rationale",
  "so the close at 37.14 and the fresh onset at 37.15 corroborate each other from both directions.",
  "so the close at 37.14 and the fresh onset at 37.15 corroborate each other from both directions. Both faces "
  "of that close are top grade; the row is held at medium because a licensed rival stands inside the span, at "
  "the 37.10/37.11 seam.")
E("P09-001", "strongest_rejected_alternative",
  SLICES["P09-001"]["live_prose"]["strongest_rejected_alternative"],
  "A split inside the scene at the 37.10/37.11 seam, which is live and licensed rather than mark-only: a "
  "samekh stands on oshb:Ezek.37.10 behind it (tier-3 single-witness), and ahead of it oshb:Ezek.37.11 opens "
  "'he said to me' with the son-of-man address, a default onset inside a vision, while oshb:Ezek.37.12 carries "
  "a messenger formula and a second samekh continuing the same rival. Read that way 37.1-10 would be a "
  "complete scene — command, prophecy, result — and 37.11-14 its interpretation with its own "
  "recognition close. The span is nevertheless kept whole as one vision_report unit, the question of which "
  "recognition clause closes it held rather than decided here; the other 'he said to me' verses (37.3, 37.4, "
  "37.9) are dialogue turns that yield no scene-complete piece and are not live rivals, and 37.2's transport "
  "verb would leave a one-verse remainder.")
E("P09-001", "device_notes",
  "The witness also records a samekh after MT 36:38 (single witness), the paragraph mark behind this row's "
  "onset.",
  "The witness also records a samekh after MT 36:38 (single witness), the paragraph mark behind this row's "
  "onset. The second-person plural recognition variant stands inside the scene at 37.6 as well as at the "
  "close, disclosed here and arguing no boundary.")

# ============================================================================== P09-010  (low)
E("P09-010", "boundary_rationale",
  "the seam rests on the utterance-formula close standing at 39.20 behind it and on the topical turn",
  "the seam rests on the verse-final utterance formula standing at 39.20 behind it — no mark is recorded "
  "on that verse, and the formula stands there alone — and on the topical turn")
E("P09-010", "boundary_rationale",
  " and to 'the nations' at 39.23 -- both internal, paragraph-final rather than row-final.",
  ", internal and paragraph-final rather than row-final. The knowing-clause at 39.23 is addressed to the "
  "nations but carries no divine-name predicate and belongs to no tracked family; that family's "
  "nations-addressed member in this chapter stands outside this span.")
E("P09-010", "boundary_rationale",
  "39.25 then reopens with a fresh messenger formula, weighed from the far side of the seam.",
  "39.25 then reopens with a fresh messenger formula, weighed from the far side of the seam. The onset's own "
  "near face carries no device of any tracked class, which is what this row's low records.")

# ============================================================================== P02-008  (medium)
E("P02-008", "boundary_rationale",
  "A pe follows this very verse (single-witness), giving Masoretic corroboration to the onset.",
  "A pe follows this very verse (single-witness), falling inside the row between its first verse and the next "
  "— a mid-row mark disclosed and not cut, as the mark at 11:6 is. The onset rests instead on the "
  "transport itself, the two verbs that open it, a predicate-class member with two tokens and one "
  "of exactly two such transports in the book; behind it the far face carries no mark and no formula, and "
  "chapter 10 carries no parashah mark at all.")
E("P02-008", "boundary_rationale",
  "a pe follows this verse as well (single-witness), the strongest double-sided Masoretic corroboration in "
  "this vision.",
  "a pe follows this verse as well (single-witness), the close-side mark this row reads. Both near faces carry "
  "licensed evidence — the transport at the onset, the narrative close and its pe at the end — while "
  "the onset's far face is bare: that is the shape this row's medium records.")


def main():
    prop = {}
    for rid, edits in EDITS.items():
        live = SLICES[rid]["live_prose"]
        fields = {}
        for field, old, new in edits:
            cur = fields.get(field, live[field])
            n = cur.count(old)
            if n != 1:
                raise SystemExit("ANCHOR %s on %s/%s matched %d times" % (old[:60], rid, field, n))
            fields[field] = cur.replace(old, new)
        prop[rid] = fields
    for rid in SLICES:
        prop.setdefault(rid, {})
    (HERE / "proposal.json").write_text(json.dumps(prop, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"rows": len(prop),
                      "fields_per_row": {r: sorted(f) for r, f in prop.items()}}, indent=1))


if __name__ == "__main__":
    main()
