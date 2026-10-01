# ezek_author_l06 deliverable builder. Private to this lane's work dir.
# expected_before values are taken PROGRAMMATICALLY from the lane file, never retyped.
import json, re, sys, io

LANE = r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_06_worklist.json"
BOOK = r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek"

d = json.load(open(LANE, encoding="utf-8"))
ROWS = {r["decision_id"]: r for r in d["your_rows"]}
ITEMS = d["your_worklist_items"]

# ---------- item ids: self-describing, index-anchored ----------
def item_id(i):
    it = ITEMS[i]
    if it["cls"] == "A4_CITATION":
        key = "cite=" + it["citation"]
    elif it["cls"] == "A6":
        key = "run=" + it["run"]
    else:
        key = it["cls"]
    return f"L06#{i}:{it['row_id']}:{it['cls']}:{key}"

# ---------- Hebrew snippets pulled from the pinned witness ----------
T = {}
for line in open(BOOK + r"\Ezek_oshb.txt", encoding="utf-8"):
    line = line.rstrip("\n")
    if not line.strip():
        continue
    k, _, v = line.partition("\t")
    T[k] = v

def skel(tok):
    return "".join(c for c in tok if "\u05d0" <= c <= "\u05ea")

def tok_by_skel(verse, sk, nth=0):
    hits = [t for t in T[verse].split() if skel(t) == sk]
    assert len(hits) > nth, (verse, sk, hits)
    return hits[nth]

HEB = {
    "vayomer_elai_4318": " ".join(T["Ezek.43.18"].split()[:2]),
    "vayolicheni_476":   tok_by_skel("Ezek.47.6", "ויולכני"),
    "vayeshiveni_476":   tok_by_skel("Ezek.47.6", "וישבני"),
    "nachal_close_475":  " ".join(T["Ezek.47.5"].split()[-4:]),
    "betzet_haish_473":  " ".join(T["Ezek.47.3"].split()[:2]),
    "vayaavireni_473":   tok_by_skel("Ezek.47.3", "ויעברני"),
}

EDITS = []
DISCHARGED = []

def prose_edit(row_id, field, pairs, items, sweep, why, tier, note=None):
    """pairs: list of (old_substring, new_substring); each old must occur exactly once."""
    cur = ROWS[row_id][field]
    new = cur
    for old, rep in pairs:
        n = new.count(old)
        assert n == 1, f"ANCHOR MISS {row_id}/{field}: {n} occurrences of {old[:70]!r}"
        new = new.replace(old, rep, 1)
    assert new != cur, f"NO-OP {row_id}/{field}"
    e = {
        "row_id": row_id, "field": field, "op": "set",
        "expected_before": cur, "value": new,
        "worklist_item_ids": [item_id(i) for i in items],
        "sweep": sweep, "why": why, "tier": tier,
    }
    if note:
        e["note"] = note
    EDITS.append(e)
    DISCHARGED.extend(item_id(i) for i in items)

def append_ref(row_id, entry, items, role_token, why, tier):
    cur = ROWS[row_id]["boundary_evidence_refs"]
    assert entry not in cur
    EDITS.append({
        "row_id": row_id, "field": "boundary_evidence_refs", "op": "append_ref",
        "expected_before": list(cur), "value": entry,
        "worklist_item_ids": [item_id(i) for i in items],
        "sweep": "a4", "role_token": role_token, "why": why, "tier": tier,
    })
    DISCHARGED.extend(item_id(i) for i in items)

def set_refs(row_id, new_list, items, why, tier, note=None):
    cur = ROWS[row_id]["boundary_evidence_refs"]
    assert new_list != cur
    e = {
        "row_id": row_id, "field": "boundary_evidence_refs", "op": "set",
        "expected_before": list(cur), "value": new_list,
        "worklist_item_ids": [item_id(i) for i in items],
        "sweep": "a4", "why": why, "tier": tier,
    }
    if note:
        e["note"] = note
    EDITS.append(e)
    DISCHARGED.extend(item_id(i) for i in items)

MEAS_WEB = "EXTRACTED: run verified word-for-word against tools/verse_map_web.json at the cited verse"
MEAS_PM  = "MEASURED: my script over pmarks_Ezek.json (marks/paseq/kq keys read directly; kq values are LISTS)"
MEAS_OSHB= "MEASURED: my script over Ezek_oshb.txt consonantal skeleton"
EXTR_INV = "EXTRACTED from ezek_device_inventory.v2.json by exact key"

# ===================== A6 / prose sweeps =====================

# ---- P10-002 (A6 idx 0)
prose_edit("P10-002", "boundary_rationale", [
    ("(oshb:Ezek.40.5) 'there was a wall on the outside of the house, all around', with",
     "(oshb:Ezek.40.5) \u201cthere was a wall on the outside of the house all around\u201d (web:Ezek.40.5), with"),
], [0], "a6",
 "The 12-word run is the WEB's own wording at 40:5; delimited and referenced. The row's comma after 'house' is not in the WEB and is dropped so the delimited text is verbatim.",
 MEAS_WEB)

# ---- P10-003 (A6 idx 5, 6)
prose_edit("P10-003", "boundary_rationale", [
    ("(oshb:Ezek.40.17) 'he brought me into the outer court', a genuine",
     "(oshb:Ezek.40.17) \u201che brought me into the outer court\u201d (web:Ezek.40.17), a genuine"),
    ("named gate ('the gate of the outer court that faces toward the north')",
     "named gate (\u201cthe gate of the outer court\u201d (web:Ezek.40.20) that faces toward the north)"),
], [5, 6], "a6",
 "idx5: verbatim WEB run at 40:17. idx6 judged a QUOTATION, not a coincidence: the 6-word run is the WEB's wording at the adjacent verse the row is describing, so the convention is owed; the row's own 'that faces toward the north' stays outside the delimiters because the WEB reads 'which'.",
 MEAS_WEB)

# ---- P10-004 (A6 idx 9, 10)
prose_edit("P10-004", "boundary_rationale", [
    ("(oshb:Ezek.40.21) 'was like the measure of the first gate', a phrase",
     "(oshb:Ezek.40.21) \u201cthe measure of the first gate\u201d (web:Ezek.40.21), a phrase"),
    ("(oshb:Ezek.40.24) 'he led me toward the south', moving",
     "(oshb:Ezek.40.24) \u201che led me toward the south\u201d (web:Ezek.40.24), moving"),
], [9, 10], "a6",
 "Both runs are verbatim WEB at the cited verses. 'was like' is the row's gloss of the Hebrew already quoted beside it and is dropped so the delimited text is exactly the run.",
 MEAS_WEB)

# ---- P10-016 (A6 idx 12)
prose_edit("P10-016", "boundary_rationale", [
    ("(oshb:Ezek.40.28) 'he brought me to the inner court by the south gate', a location change",
     "(oshb:Ezek.40.28) \u201che brought me to the inner court by the south gate\u201d (web:Ezek.40.28), a location change"),
], [12], "a6",
 "11-word run verbatim in the WEB at 40:28; delimited and referenced.",
 MEAS_WEB)

# ---- P10-005 (A6 idx 16, 17)
prose_edit("P10-005", "boundary_rationale", [
    ("'and a chamber, with its door, was by the posts of the gates' with a bare vav",
     "'and a chamber, \u201cwith its door was by the posts\u201d (web:Ezek.40.38) of the gates' with a bare vav"),
    ("(oshb:Ezek.40.47) 'the altar was before the house', a summary notice",
     "(oshb:Ezek.40.47) \u201cthe altar was before the house\u201d (web:Ezek.40.47), a summary notice"),
], [16, 17], "a6",
 "idx16: only the 7-word stretch is WEB wording (the WEB reads 'A room ... at the gates'), so the delimiters enclose exactly that run and the row's own rendering stays outside; the row's comma after 'door' is not in the WEB and is dropped. idx17: verbatim WEB at 40:47.",
 MEAS_WEB)

# ---- P10-006 (A6 idx 21, 22, 24; idx 23 judged NOT a quotation, no edit)
prose_edit("P10-006", "boundary_rationale", [
    ("(oshb:Ezek.40.48) 'he brought me to the porch of the house', marking entry",
     "(oshb:Ezek.40.48) \u201che brought me to the porch of the house\u201d (web:Ezek.40.48), marking entry"),
    ("(oshb:Ezek.41.1) 'he brought me to the nave... and measured', disclosed here",
     "(oshb:Ezek.41.1) \u201che brought me to the nave and measured\u201d (web:Ezek.41.1), disclosed here"),
    ("(oshb:Ezek.41.4) 'he said to me, this is the most holy place', a genuine speak-formula close",
     "(oshb:Ezek.41.4) \u201che said to me, this is the most holy place\u201d (web:Ezek.41.4), a genuine speak-formula close"),
], [21, 22, 24], "a6",
 "Three verbatim WEB runs delimited and referenced. At 41:1 the row's internal ellipsis is removed because the WEB's words run continuously. 41:4's run carries the content clause as well as the speak-formula, so A6-b does not exempt it.",
 MEAS_WEB)

# ---- P10-007 (A6 idx 27)
prose_edit("P10-007", "boundary_rationale", [
    ("(oshb:Ezek.41.5) 'he measured the wall of the house', introducing",
     "(oshb:Ezek.41.5) \u201che measured the wall of the house\u201d (web:Ezek.41.5), introducing"),
], [27], "a6", "7-word run verbatim in the WEB at 41:5.", MEAS_WEB)

# ---- P10-008 (A6 idx 33, 34, 35)
prose_edit("P10-008", "boundary_rationale", [
    ("(oshb:Ezek.41.12) 'the building that was before the separate place, at the side toward the sea (west)', confirmed",
     "(oshb:Ezek.41.12) \u201cthe building that was before the separate place at the side toward the west\u201d (web:Ezek.41.12), confirmed"),
    ("(oshb:Ezek.41.22) 'he spoke to me, this is the table that is before YHWH' (the 'spoke to me' root, distinct from the 'said to me' form at 41:4)",
     "(oshb:Ezek.41.22) \u201cto me, this is the table that is before\u201d (web:Ezek.41.22) YHWH, opened by the 'spoke to me' root, distinct from the 'said to me' form at 41:4"),
    ("(oshb:Ezek.41.26) 'and the side rooms of the house, and the thresholds' immediately before",
     "(oshb:Ezek.41.26) 'and \u201cthe side rooms of the\u201d (web:Ezek.41.26) house, and the thresholds' immediately before"),
], [33, 34, 35], "a6",
 "idx33: the run is extended by one word to the WEB's own 'west' so the delimited text is a complete verbatim clause; the row's comma and its '(west)' gloss go. idx34: the shared run begins at 'to me' -- the WEB renders BOTH 41:4 and 41:22 with 'said', so 'he spoke' is the row's rendering of the Hebrew root and stays outside the delimiters. idx35: the 5-word run diverges at temple/house, so only the run is delimited; the same run also stands at WEB 40:10.",
 MEAS_WEB)

# ---- P10-010 (A6 idx 43, 44, 46 in rationale; 47 in rejected-alt; idx 45 judged NOT a quotation)
prose_edit("P10-010", "boundary_rationale", [
    ("(oshb:Ezek.42.1) 'he brought me out into the outer court ... then he brought me into the room' -- the strongest onset",
     "(oshb:Ezek.42.1) \u201che brought me out into the outer court\u201d (web:Ezek.42.1) ... \u201cthen he brought me into the room\u201d (web:Ezek.42.1) -- the strongest onset"),
    ("where the priests eat the most holy things and must change garments",
     "where the priests \u201ceat the most holy things\u201d (web:Ezek.42.13) and must change garments"),
], [43, 44, 46], "a6",
 "Three verbatim WEB runs at 42:1 (twice) and 42:13, each delimited with its own in-field reference. The same 42:1 run also stands at WEB 46:21; the in-field reference names the verse this row is glossing.",
 MEAS_WEB)

prose_edit("P10-010", "strongest_rejected_alternative", [
    ("the north-side description ('like the appearance of the rooms which were toward the north') rather than opening",
     "the north-side description, \u201clike the appearance of the rooms which were toward the north\u201d (web:Ezek.42.11), rather than opening"),
], [47], "a6", "11-word run verbatim in the WEB at 42:11.", MEAS_WEB)

# ---- P10-011 (A6 idx 50, 51, 52)
prose_edit("P10-011", "boundary_rationale", [
    ("(oshb:Ezek.42.15) 'when he had finished' ... 'measuring the inner house', paired with",
     "(oshb:Ezek.42.15) \u201cwhen he had finished measuring the inner house\u201d (web:Ezek.42.15), paired with"),
    ("(oshb:Ezek.42.20) 'to make a separation between the holy and the common' -- a genuine thematic close",
     "(oshb:Ezek.42.20) \u201cto make a separation between that which was holy and that which was common\u201d (web:Ezek.42.20) -- a genuine thematic close"),
], [50, 51, 52], "a6",
 "idx50: the WEB's words run continuously at 42:15, so the row's internal ellipsis goes. idx51+idx52 together: the WEB at 42:20 reads 'between that which was holy and that which was common'. The row's compressed 'the holy and the common' is NOT the WEB's wording at the verse it glosses -- that is why the 5-word run matched 22:26 and 44:23 instead. Restoring the verse's own wording inside the delimiters discharges the install and dissolves the out-of-span collocation.",
 MEAS_WEB)

# ---- P10-012 (A6 idx 58, 59 rationale; 60 rejected-alt; 61 refs -- refs folded into one set edit)
prose_edit("P10-012", "boundary_rationale", [
    ("and 'I fell on my face' (one of five)",
     "\u201cand I fell on my face\u201d (web:Ezek.43.3) (one of five)"),
    ("(oshb:Ezek.43.9) 'then I will dwell among them forever' immediately before",
     "(oshb:Ezek.43.9) \u201cthen I will dwell among them forever\u201d (web:Ezek.43.9) immediately before"),
], [58, 59], "a6",
 "Both runs verbatim in the WEB. The 43:3 run includes its leading 'and', which is the WEB's own word there.",
 MEAS_WEB)

prose_edit("P10-012", "strongest_rejected_alternative", [
    ("43:6's 'I heard one speaking to me out of the house' continues",
     "43:6's \u201cI heard one speaking to me out of the house\u201d (web:Ezek.43.6) continues"),
], [60], "a6", "10-word run verbatim in the WEB at 43:6.", MEAS_WEB)

# ---- P10-013 (A6 idx 64, 65 rationale; 66 refs)
prose_edit("P10-013", "boundary_rationale", [
    ("(oshb:Ezek.43.12) 'this is the law of the house ... behold, this is the law of the house', repeating",
     "(oshb:Ezek.43.12) \u201cthis is the law of the house\u201d (web:Ezek.43.12) ... \u201cbehold, this is the law of the house\u201d (web:Ezek.43.12), repeating"),
], [64, 65], "a6",
 "Both halves of the doubled inclusio are verbatim WEB at 43:12; each is delimited separately with its own reference, matching the two worklist runs.",
 MEAS_WEB)

# ---- P10-014 (A6 idx 68)
prose_edit("P10-014", "boundary_rationale", [
    ("(oshb:Ezek.43.13) 'and these are the measurements of the altar', functioning",
     "(oshb:Ezek.43.13), the vav-initial \u201cthese are the measurements of the altar\u201d (web:Ezek.43.13), functioning"),
], [68], "a6",
 "7-word run verbatim in the WEB at 43:13; the row's leading 'and' renders the Hebrew vav and is described rather than quoted, since the WEB does not carry it.",
 MEAS_WEB)

# ---- P10-015 (A6 idx 72 + measured precision fix at 43:18)
_p1015 = ROWS["P10-015"]["boundary_rationale"]
_a, _b = "Onset side: 43:18 opens with ", " (oshb:Ezek.43.18)"
_i, _j = _p1015.index(_a), _p1015.index(_b)
_heb_4318_in_row = _p1015[_i + len(_a):_j]          # the row's own Hebrew bytes, not retyped
_old_4318 = _a + _heb_4318_in_row + _b
_new_4318 = ("Onset side: 43:18 opens on a said-to-me verse, " + HEB["vayomer_elai_4318"]
             + ", and then carries " + _heb_4318_in_row + _b)
prose_edit("P10-015", "boundary_rationale", [
    (_old_4318, _new_4318),
    ("(oshb:Ezek.43.27) 'then I will accept you, says the Lord YHWH', this time genuinely row-final",
     "(oshb:Ezek.43.27) \u201cthen I will accept you, says the Lord Yahweh\u201d (web:Ezek.43.27), this time genuinely row-final"),
], [72], "a6",
 "idx72: 8-word run verbatim in the WEB at 43:27 (the WEB spells the divine name Yahweh, so the delimited text carries the WEB's own spelling). The 43:18 clause is a MEASURED precision fix, not an ordered item: the verse does not begin with the messenger formula -- it begins with the said-to-me formula, and the son-of-man plus messenger material follows. Re-emitting the old wording would have asserted a byte-false claim.",
 MEAS_OSHB,
 note="carries an unordered but MEASURED precision correction; declared in changes_made_or_no_change")

# ---- P11-001 (A6 idx 75 rationale; MARKS_3D idx 76 device_notes)
prose_edit("P11-001", "boundary_rationale", [
    ("closes with the prostration formula 'I fell on my face,' matching",
     "closes with the prostration formula \u201cI fell on my face\u201d (web:Ezek.44.4), matching"),
], [75], "a6",
 "Judged a QUOTATION and the convention installed. The 5-word run is verbatim in the WEB at this row's own verse 44:4, so the in-field reference is anchored there rather than at the out-of-span cross-references. A6-b is NOT applied: its exemption names the messenger, utterance, recognition, word-event and hand-of-YHWH renderings and addressee titles, and the prostration formula is not among them, so the duty stands even though the row names the device. The cross-reference list (1.28, 3.23, 11.13, 43.3) was checked and is exactly the rest of the pinned 5-verse class.",
 MEAS_WEB)

prose_edit("P11-001", "device_notes", [
    ("No parashah mark falls between the double samekh recorded after Ezek.43.27 and the pe recorded after Ezek.44.14; this row's own span carries no parashah corroboration on either side, and that absence is disclosed, not treated as evidence for or against the seam.",
     "Parashah in three directions, MEASURED from pmarks_Ezek.json, where a mark is recorded ON the verse it FOLLOWS. Onset seam: corroboration IS present -- two consecutive samekh marks follow Ezek.43.27, the verse immediately before this row's first verse, and this row's own rationale argues from them. Interior, Ezek.44.1-Ezek.44.3: no mark. Close seam: no mark follows Ezek.44.4; the next mark in the book is the pe following Ezek.44.14. The earlier clause, that the span carried no parashah corroboration on either side, was false against that measurement and is corrected here; each mark is single-witness and corroborates only, never deciding a seam alone."),
], [76], "marks",
 "The false clause is fixed and replaced by the three-direction disclosure the sweep requires. MEASURED: pmarks_Ezek.json carries marks['Ezek.43.27'] = ['SAMEKH','SAMEKH'] and marks['Ezek.44.14'] = ['PE'], with no key for 44:1, 44:2, 44:3 or 44:4. The doubled mark at 43:27 is the book's only doubled parashah occurrence (184 occurrences on 183 verses).",
 MEAS_PM)

# ---- P11-007 (A6 idx 81)
prose_edit("P11-007", "boundary_rationale", [
    ("itself carrying the construction glossed 'the (day of the) new moon' -- disclosed",
     "itself carrying \u201cthe day of the new moon\u201d (web:Ezek.46.1) -- disclosed"),
], [81], "a6",
 "6-word run verbatim in the WEB at 46:1 (and again at 46:6, which the row names); the row's parenthesised gloss is replaced by the WEB's own wording so the delimited text is verbatim.",
 MEAS_WEB)

# ---- P11-009 (A6 idx 86, 87, 88)
prose_edit("P11-009", "boundary_rationale", [
    ("at Ezek.46.19 ('he brought me through the entry ... into the holy rooms for the priests') reopens",
     "at Ezek.46.19 (\u201che brought me through the entry\u201d (web:Ezek.46.19) ... \u201cinto the holy rooms for the priests\u201d (web:Ezek.46.19)) reopens"),
    ("a further transport ('he brought me out into the outer court', 21)",
     "a further transport (\u201che brought me out into the outer court\u201d (web:Ezek.46.21), 21)"),
], [86, 87, 88], "a6",
 "Three verbatim WEB runs at 46:19 (twice) and 46:21. The 46:21 entry delimits a quotation only; it makes no transport-class membership claim, MT 46:21 being one of the thirteen verses whose membership is routed.",
 MEAS_WEB)

# ---- P11-010 (A6 idx 90 rationale; GROUNDS idx 91 rejected-alt)
prose_edit("P11-010", "boundary_rationale", [
    ("at Ezek.47.1 ('he brought me back to the door of the temple') continues",
     "at Ezek.47.1 (\u201che brought me back to the door of the temple\u201d (web:Ezek.47.1)) continues"),
], [90], "a6",
 "10-word run verbatim in the WEB at 47:1, which is itself in the strategy's closed 20-verse transport list, so the surrounding description is unaffected by the routed question.",
 MEAS_WEB)

A16 = (
    "Splitting at 47.5/47.6 to isolate the measuring circuit (47.3-5) as its own temple_measurement row. "
    "Weighed under A9/A16 and held on stated grounds. The rival's near face, Ezek.47.6, IS licensed: the verse "
    "is both a said-to-me verse and a guided-motion verse (" + HEB["vayolicheni_476"] + ", " + HEB["vayeshiveni_476"] + "), "
    "and it stands in the strategy's closed 20-verse transport list, so a seam there would not be device-free. "
    "Its far face, Ezek.47.5, carries the fourth measure-verb occurrence and a content close (" + HEB["nachal_close_475"] + "), "
    "with no close-role formula and no parashah mark, so the rival is one-faced rather than two-faced. "
    "The row holds against it on three stated grounds: Ezek.47.6's question looks BACK at the measuring just reported and its "
    "motion returns the prophet to the bank inside one scene rather than opening a new one; the strategy treats 47:1-12 as a "
    "single region and names 47:6 inside it as interior texture; and the only further signal at 47:6 is the WEB's mid-verse "
    "paragraph, which is tier-4 and never corroborates a seam. "
    "The earlier ground -- that no fresh transport or messenger formula opens 47.3 and none closes 47.5 -- is replaced because it "
    "understated the witness: MEASURED over Ezek_oshb.txt, Ezek.47.3 does not BEGIN with a guided-motion verb (it opens "
    + HEB["betzet_haish_473"] + ") but does carry " + HEB["vayaavireni_473"] + " later in the verse, and Ezek.47.4 carries that same "
    "form twice. Whether those tokens are members of the row-operative transport class is the question routed to the controlling "
    "agent, so no membership claim is made here in either direction. The measuring sequence therefore remains texture inside the "
    "single river vision running 47.1-12, disclosed as a one-sentence category deviation rather than split into a separate row."
)
prose_edit("P11-010", "strongest_rejected_alternative", [
    (ROWS["P11-010"]["strongest_rejected_alternative"], A16),
], [91], "grounds",
 "Executes the one duty the order names explicitly -- the A16 weighing of the 47:6 rival -- and replaces the ground that "
 "understated the bytes at 47:3/47:4, without asserting or denying transport-class membership for either verse. The seam is not moved.",
 "MEASURED for the byte facts (my scripts over Ezek_oshb.txt and pmarks_Ezek.json); EXTRACTED for the strategy's closed-20 membership of 47:6 and its 47:1-12 region; the order's own scope is REPORTED and is not fully enumerated in any input this lane may read",
 note="PARTIAL: the order reads 'all five repairs' and no input available to this lane enumerates the five. See items_NOT_discharged and escalations.")

# ---- P11-011 (A6 idx 92)
prose_edit("P11-011", "boundary_rationale", [
    ("at Ezek.47.13 ('thus says the Lord GOD: this shall be the border...') opens",
     "at Ezek.47.13 (thus says the Lord GOD, then \u201cthis shall be the border\u201d (web:Ezek.47.13)) opens"),
], [92], "a6",
 "5-word run verbatim in the WEB at 47:13 (and again at 47:15). The messenger-formula words are left undelimited under A6-b: the row names the device and the WEB's rendering of it is a gloss of a census object, not a quotation.",
 MEAS_WEB)

# ---- P11-015 (A6 idx 95)
prose_edit("P11-015", "boundary_rationale", [
    ("on its own explicit resumption formula ('and the rest of the tribes'), a change",
     "on its own explicit resumption formula, the vav-initial \u201cthe rest of the tribes\u201d (web:Ezek.48.23), a change"),
], [95], "a6",
 "5-word run verbatim in the WEB at 48:23; the row's leading 'and' renders the Hebrew vav, which the WEB does not carry, so it is described rather than enclosed.",
 MEAS_WEB)

# ---- P11-013 (A6 idx 96)
prose_edit("P11-013", "boundary_rationale", [
    ("no formula device opens Ezek.48.30 ('these are the exits of the city...')",
     "no formula device opens Ezek.48.30 (\u201cthese are the exits of the city\u201d (web:Ezek.48.30))"),
], [96], "a6",
 "7-word run verbatim in the WEB at 48:30.",
 MEAS_WEB)

# ===================== A4 reference installs =====================
PAS = {
    1: "paseq present; count-only, position unsourceable",
    2: "one paseq stroke here, count-only",
    3: "disjunctive stroke counted, not located",
    4: "paseq tallied; intra-verse place unavailable",
    5: "two strokes on this verse",
    6: "no paseq on this verse",
    7: "stroke counted; no position claim",
    8: "single stroke, position not sourceable",
}
PASEQ_WHY = "MEASURED from pmarks_Ezek.json: the verse's paseq occurrence count, count-only; the extract drops the segs so no intra-verse position is claimed."
MARK_WHY  = "MEASURED from pmarks_Ezek.json, where a mark is recorded ON the verse it follows; disclosed as single-witness corroboration, never as the deciding ground."

A4 = [
 # row, entry, items, token, why, tier
 ("P10-002","oshb:Ezek.40.4 [WARRANT-onset] charge-speech close precedes onset",[1],"WARRANT-onset",
  "The onset's far face at 40:4 carries the man's charge speech, a close-role signal the row's onset argument rests on; MT 40:4 is also a son-of-man verse in the pinned 93-verse list.",EXTR_INV),
 ("P10-002","oshb:Ezek.40.17 [WARRANT-close] transport verb opens the court",[2],"WARRANT-close",
  "The row's close rests on the far face at 40:17, which is in the strategy's closed 20-verse transport list, so no routed membership question arises.",EXTR_INV),
 ("P10-002","oshb:Ezek.40.7 [WARRANT-rival] mid-gate cut weighed, rejected",[3],"WARRANT-rival",
  "40:7 is the rival mid-gate seam the rejected-alternative field weighs.","EXTRACTED from the row's own strongest_rejected_alternative"),
 ("P10-002","oshb:Ezek.40.14 [DISCLOSURE-paseq] "+PAS[1],[4],"DISCLOSURE-paseq",PASEQ_WHY,MEAS_PM),

 ("P10-003","oshb:Ezek.40.20 [WARRANT-close] far face pivots to named gate",[7],"WARRANT-close",
  "The row's close rests on the far face at 40:20, where the survey pivots from the court as a whole to a named gate.","EXTRACTED from the row's own boundary_rationale, verified against Ezek_oshb.txt"),
 ("P10-003","oshb:Ezek.40.20-Ezek.40.27 [WARRANT-rival] merged eleven-verse rival weighed",[8],"WARRANT-rival",
  "One RANGE entry for the range citation, not one per interior verse: the rejected alternative is the merged 40:17-27 row.","EXTRACTED from the row's own strongest_rejected_alternative"),

 ("P10-004","oshb:Ezek.40.28 [WARRANT-close] court change on the far face",[11],"WARRANT-close",
  "The row's close rests on the far face at 40:28, which is in the strategy's closed 20-verse transport list.",EXTR_INV),

 ("P10-016","oshb:Ezek.40.20-Ezek.40.27 [ANCHOR] neighbour row named, not argued",[13],"ANCHOR",
  "The range is cited only to name the adjacent outer-court row; the boundary does not rest on it. ANCHOR also keeps this entry clear of any transport-class claim about MT 40:24.","EXTRACTED from the row's own boundary_rationale"),
 ("P10-016","oshb:Ezek.40.38 [ANCHOR] far face lacks a device",[14],"ANCHOR",
  "The row cites 40:38 for what it LACKS -- the close is conceded to be weaker on that side -- so no WARRANT token is honest here.","EXTRACTED from the row's own boundary_rationale, verified against Ezek_oshb.txt"),
 ("P10-016","oshb:Ezek.40.30 [DISCLOSURE-paseq] "+PAS[2],[15],"DISCLOSURE-paseq",PASEQ_WHY,MEAS_PM),

 ("P10-005","oshb:Ezek.40.37 [ANCHOR] prior gate close; not warrant",[18],"ANCHOR",
  "The row states in terms that this onset 'carries no formula evidence of its own' and rests on content, so 40:37 locates the seam without warranting it.","EXTRACTED from the row's own boundary_rationale"),
 ("P10-005","oshb:Ezek.40.48 [WARRANT-close] guide leads inward; scene changes",[19],"WARRANT-close",
  "The close rests on the far face at 40:48, described by what the bytes do there. MT 40:48 is one of the thirteen verses whose transport-class membership is routed, so this entry makes no membership or count claim.","MEASURED from Ezek_oshb.txt for the verb at 40:48; the class question is REPORTED as routed"),
 ("P10-005","oshb:Ezek.40.43 [DISCLOSURE-paseq] "+PAS[3],[20],"DISCLOSURE-paseq",PASEQ_WHY,MEAS_PM),

 ("P10-006","oshb:Ezek.41.5 [WARRANT-close] measuring verb opens new object",[25],"WARRANT-close",
  "The close rests on the far face at 41:5, where a fresh measure verb turns to the house wall.",MEAS_OSHB),
 ("P10-006","oshb:Ezek.40.49 [WARRANT-rival] porch-only rival weighed, rejected",[26],"WARRANT-rival",
  "40:49 is the close of the two-verse porch-only rival the rejected-alternative field weighs.","EXTRACTED from the row's own strongest_rejected_alternative"),

 ("P10-007","oshb:Ezek.41.4 [WARRANT-onset] speak-formula close behind this onset",[28],"WARRANT-onset",
  "Unlike P10-005's onset, this row does not disclaim far-face evidence: 41:4 carries a said-to-me close that makes the onset seam two-faced, and the rationale argues from it.",MEAS_OSHB),
 ("P10-007","oshb:Ezek.41.6 [DISCLOSURE-paseq] "+PAS[7],[29],"DISCLOSURE-paseq",PASEQ_WHY,MEAS_PM),
 ("P10-007","oshb:Ezek.41.7 [DISCLOSURE-paseq] "+PAS[4],[30],"DISCLOSURE-paseq",PASEQ_WHY,MEAS_PM),
 ("P10-007","oshb:Ezek.41.10 [DISCLOSURE-paseq] "+PAS[8],[31],"DISCLOSURE-paseq",PASEQ_WHY,MEAS_PM),
 ("P10-007","oshb:Ezek.41.9 [DISCLOSURE-paseq] "+PAS[6],[32],"DISCLOSURE-paseq",
  "The row's paseq claim is that 41:9 alone in the span carries none. MEASURED: pmarks_Ezek.json has no paseq entry for Ezek.41.9 while it has one for each of 41:5, 41:6, 41:7, 41:8, 41:10 and 41:11. The token names the layer and the free text carries the polarity, since the absence token in the vocabulary is scoped to a range.",MEAS_PM),

 ("P10-008","oshb:Ezek.42.1 [WARRANT-close] double motion opens outer court",[36],"WARRANT-close",
  "The close rests on the far face at 42:1, which is in the strategy's closed 20-verse transport list.",EXTR_INV),
 ("P10-008","oshb:Ezek.41.16-Ezek.41.19 [ANCHOR] gallery material, no boundary claim",[37],"ANCHOR",
  "One RANGE entry: the row lists the gallery structure as in-span content, not as boundary evidence.","EXTRACTED from the row's own boundary_rationale"),
 ("P10-008","oshb:Ezek.41.21 [WARRANT-rival] rival onset weighed, content only",[38],"WARRANT-rival",
  "The same verse-set is cited twice in this row and takes ONE entry. The stronger of the two mentions is the rejected alternative's internal division at 41:21, weighed and held.","EXTRACTED from both of the row's own fields"),
 ("P10-008","oshb:Ezek.41.23-Ezek.41.25 [ANCHOR] door description, boundary rests elsewhere",[39],"ANCHOR",
  "One RANGE entry for in-span content the boundary does not rest on.","EXTRACTED from the row's own boundary_rationale"),
 ("P10-008","oshb:Ezek.41.16 [DISCLOSURE-paseq] "+PAS[5],[40],"DISCLOSURE-paseq",
  "MEASURED from pmarks_Ezek.json: Ezek.41.16 carries TWO paseq occurrences, count-only; position unsourceable from the extract.",MEAS_PM),
 ("P10-008","oshb:Ezek.41.17 [DISCLOSURE-paseq] "+PAS[1],[41],"DISCLOSURE-paseq",PASEQ_WHY,MEAS_PM),
 ("P10-008","oshb:Ezek.41.19 [DISCLOSURE-paseq] "+PAS[2],[42],"DISCLOSURE-paseq",PASEQ_WHY,MEAS_PM),

 ("P10-010","oshb:Ezek.42.10-Ezek.42.12 [WARRANT-rival] south-side rival weighed, held",[48],"WARRANT-rival",
  "One RANGE entry. The same range is cited twice in the row and the weighed rival is the stronger reading.","EXTRACTED from both of the row's own fields"),
 ("P10-010","oshb:Ezek.42.10 [DISCLOSURE-paseq] "+PAS[7],[49],"DISCLOSURE-paseq",PASEQ_WHY,MEAS_PM),

 ("P10-011","oshb:Ezek.42.17 [ANCHOR] north reading; boundary rests elsewhere",[53],"ANCHOR",
  "One of the four cardinal measurements the row lists as in-span content; MEASURED order is east 42:16, north 42:17, south 42:18, west 42:19.",MEAS_OSHB),
 ("P10-011","oshb:Ezek.42.18 [ANCHOR] south cardinal listed, not argued",[54],"ANCHOR",
  "In-span cardinal measurement, not boundary evidence.",MEAS_OSHB),
 ("P10-011","oshb:Ezek.42.19 [ANCHOR] west side measured, no warrant",[55],"ANCHOR",
  "In-span cardinal measurement, not boundary evidence.",MEAS_OSHB),
 ("P10-011","oshb:Ezek.43.1 [WARRANT-close] far face: guide leads, glory returns",[56],"WARRANT-close",
  "The close rests on the far face at 43:1. MT 43:1 is one of the thirteen verses whose transport-class membership is routed, so the entry describes what the verse does and claims no membership or count.","MEASURED from Ezek_oshb.txt for the verb at 43:1; the class question is REPORTED as routed"),
 ("P10-011","oshb:Ezek.43.1-Ezek.43.9 [WARRANT-rival] rival extension weighed against close",[57],"WARRANT-rival",
  "One RANGE entry for the rival that would extend this row through the glory's return.","EXTRACTED from the row's own strongest_rejected_alternative"),

 ("P10-014","oshb:Ezek.43.12 [WARRANT-onset] inclusio closes; onset follows it",[69],"WARRANT-onset",
  "The onset's far face at 43:12 carries the doubled torah-of-the-house inclusio, a close device the row argues from.",MEAS_OSHB),
 ("P10-014","oshb:Ezek.43.18 [WARRANT-close] messenger formula opens far side",[70],"WARRANT-close",
  "The close rests on the far face at 43:18. MEASURED: 43:18 carries the long messenger formula (one of the pinned 122 verses) and also opens on a said-to-me formula.",EXTR_INV),
 ("P10-014","oshb:Ezek.43.18-Ezek.43.27 [WARRANT-rival] merged ordinance rival weighed",[71],"WARRANT-rival",
  "One RANGE entry for the merge-with-the-ordinances rival.","EXTRACTED from the row's own strongest_rejected_alternative"),

 ("P10-015","oshb:Ezek.44.1 [WARRANT-rival] rival continuation across this verse",[73],"WARRANT-rival",
  "44:1 is the rival's onset verse. MT 44:1 is one of the thirteen verses whose transport-class membership is routed; no membership or count claim is made.","EXTRACTED from the row's own strongest_rejected_alternative; the class question is REPORTED as routed"),
 ("P10-015","oshb:Ezek.44.1-Ezek.44.4 [WARRANT-rival] shut-gate block rival weighed",[74],"WARRANT-rival",
  "A distinct verse-set from the single 44:1 citation, so under DEF-A4-ARGUED clause 2 it is a separate citation and takes its own RANGE entry.","EXTRACTED from the row's own strongest_rejected_alternative"),

 ("P11-001","oshb:Ezek.43.27 [WARRANT-onset] far face: utterance close, doubled mark",[77],"WARRANT-onset",
  "MEASURED: 43:27 carries the long utterance formula (one of the pinned 81 verses) and is followed by two consecutive samekh marks, the book's only doubled parashah occurrence. The onset argument rests on that far face; the marks corroborate.",MEAS_PM),

 ("P11-004","oshb:Ezek.44.31 [DISCLOSURE-mark] pe follows this verse",[78],"DISCLOSURE-mark",MARK_WHY,MEAS_PM),
 ("P11-005","oshb:Ezek.45.8 [DISCLOSURE-mark] closed-section mark behind onset",[79],"DISCLOSURE-mark",MARK_WHY,MEAS_PM),
 ("P11-006","oshb:Ezek.45.17 [DISCLOSURE-mark] setumah after this verse",[80],"DISCLOSURE-mark",
  MARK_WHY+" This entry records only the mark and is independent of the strategy's self-contradiction about MT 45:18 raised in escalations.",MEAS_PM),
 ("P11-007","oshb:Ezek.46.6 [DISCLOSURE-device] chodesh homograph, not a dateline",[82],"DISCLOSURE-device",
  "EXTRACTED: ezek_device_inventory.v2.json lists Ezek.46.6 in calendar_dates_not_datelines.chodesh_verses_correctly_excluded, so the construction is an in-span device the boundary does not rest on.",EXTR_INV),
 ("P11-007","oshb:Ezek.45.25 [DISCLOSURE-mark] mark corroborates; no seam decided",[83],"DISCLOSURE-mark",MARK_WHY,MEAS_PM),
 ("P11-008","oshb:Ezek.46.15 [DISCLOSURE-mark] open-section mark stands here",[84],"DISCLOSURE-mark",MARK_WHY,MEAS_PM),
 ("P11-008","oshb:Ezek.46.19 [WARRANT-close] transport reopens the vision scene",[85],"WARRANT-close",
  "The close rests on the far face at 46:19, which is in the strategy's closed 20-verse transport list, and the strategy names 46:18/46:19 a hard seam.",EXTR_INV),
 ("P11-009","oshb:Ezek.46.18 [ANCHOR] structural mention, boundary rests elsewhere",[89],"ANCHOR",
  "46:18 is cited to locate the hard seam behind the onset; the onset itself rests on 46:19, so no WARRANT token belongs on 46:18.","EXTRACTED from the row's own boundary_rationale"),
 ("P11-011","oshb:Ezek.47.12 [DISCLOSURE-mark] paragraph mark follows, weak corroboration",[93],"DISCLOSURE-mark",MARK_WHY,MEAS_PM),
 ("P11-012","oshb:Ezek.47.23 [WARRANT-onset] utterance plus mark close behind",[94],"WARRANT-onset",
  "MEASURED: 47:23 carries the long utterance formula and is followed by a samekh, the doubled close signal the row's onset argument rests on.",MEAS_PM),
 ("P11-013","oshb:Ezek.48.29 [WARRANT-onset] far face closes the allotment",[97],"WARRANT-onset",
  "MEASURED: 48:29 carries the long utterance formula and is followed by a pe; the row's onset argument rests on that close.",MEAS_PM),
]
for row, entry, items, tok, why, tier in A4:
    append_ref(row, entry, items, tok, why, tier)

# ---- the two refs SET edits (an ordered A6 install inside an existing entry + appends on the same field)
cur = list(ROWS["P10-012"]["boundary_evidence_refs"])
i_chebar = next(i for i, e in enumerate(cur) if e.startswith("oshb:Ezek.43.3"))
old_e = cur[i_chebar]
new_e = old_e.replace('"I fell on my face"', "\u201cI fell on my face\u201d (web:Ezek.43.3)")
assert new_e != old_e
new_list = list(cur)
new_list[i_chebar] = new_e
new_list.append("oshb:Ezek.43.6 [WARRANT-rival] rival cut weighed, scene continues")
new_list.append("oshb:Ezek.43.8 [DISCLOSURE-paseq] " + PAS[4])
set_refs("P10-012", new_list, [61, 62, 63],
 "One edit for this field because an ordered A6 install falls inside an existing entry while two A4 entries must be added. "
 "idx61: the 5-word run is verbatim WEB at 43:3, so it takes the delimiter and an in-field web reference. idx62: WARRANT-rival at 43:6, the rejected cut. "
 "idx63: DISCLOSURE-paseq at 43:8, MEASURED from pmarks. The two figures already in that entry were checked and both reproduce: "
 "the strategy's Chebar class is 8 verses and my sweep finds kbr in exactly 8, and the prostration class is 5 verses and my sweep finds the exact form in exactly those 5.",
 "EXTRACTED for the quotation run; MEASURED for the paseq and for both re-checked figures",
 note="existing entries are not re-tokenised in this wave; the two appended entries carry tokens and the modified entry keeps its original wording apart from the ordered delimiter")

cur = list(ROWS["P10-013"]["boundary_evidence_refs"])
i_incl = next(i for i, e in enumerate(cur) if e.startswith("oshb:Ezek.43.12"))
old_e = cur[i_incl]
new_e = old_e.replace("'this is the law of the house'", "\u201cthis is the law of the house\u201d (web:Ezek.43.12)")
assert new_e != old_e
new_list = list(cur)
new_list[i_incl] = new_e
new_list.append("oshb:Ezek.43.9 [DISCLOSURE-mark] samekh follows; corroboration only")
set_refs("P10-013", new_list, [66, 67],
 "One edit for this field: idx66's A6 install falls inside an existing entry and idx67 adds one. The 7-word run is verbatim WEB at 43:12; "
 "the appended entry records the samekh following 43:9, MEASURED from pmarks, as corroboration behind the onset.",
 "EXTRACTED for the quotation run; MEASURED for the mark",
 note="existing entries are not re-tokenised; only the ordered delimiter is installed in the modified entry")

# ---- judgement-only discharges (no edit by design)
JUDGE_NO_EDIT = [23, 45]
DISCHARGED.extend(item_id(i) for i in JUDGE_NO_EDIT)

# ===================== self-checks =====================
# 1. every worklist item accounted for exactly once
NOT_DISCHARGED_IDS = [item_id(91)]
acct = {}
for x in DISCHARGED:
    acct[x] = acct.get(x, 0) + 1
dupes = {k: v for k, v in acct.items() if v > 1}
all_ids = [item_id(i) for i in range(len(ITEMS))]
missing = [x for x in all_ids if x not in acct and x not in NOT_DISCHARGED_IDS]
extra = [x for x in acct if x not in all_ids]
# 91 is claimed in an edit AND listed NOT discharged -> declared, not silent
print("ITEMS", len(ITEMS), "| discharged", len(acct), "| not_discharged", len(NOT_DISCHARGED_IDS))
print("dupes:", dupes)
print("missing:", missing)
print("extra:", extra)
print("edits:", len(EDITS))
per_field = {}
for e in EDITS:
    if e["op"] == "set":
        k = (e["row_id"], e["field"])
        per_field[k] = per_field.get(k, 0) + 1
print("rows with >1 set edit on one field:", {k: v for k, v in per_field.items() if v > 1})

# 2. expected_before byte-identity against the lane file
for e in EDITS:
    cur = ROWS[e["row_id"]][e["field"]]
    assert e["expected_before"] == cur, ("EXPECTED_BEFORE DRIFT", e["row_id"], e["field"])
print("expected_before byte-identity: all", len(EDITS), "edits verified against the lane file")

# 3. A6 self-check: any NEW >=5-word run matching the WEB that is left outside curly quotes
web = json.load(open(BOOK + r"\tools\verse_map_web.json", encoding="utf-8"))
def words(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).split()
WEBGRAMS = {}
for k, v in web.items():
    w = words(v["text"].replace("[fn]", ""))
    for i in range(len(w) - 4):
        WEBGRAMS.setdefault(" ".join(w[i:i + 5]), set()).add(k)
def strip_quoted(s):
    return re.sub(r"\u201c[^\u201d]*\u201d", " QUOTED ", s)
newflags = []
for e in EDITS:
    if e["op"] != "set" or e["field"] == "boundary_evidence_refs":
        continue
    before_out = strip_quoted(e["expected_before"])
    after_out = strip_quoted(e["value"])
    b = set(" ".join(words(before_out)[i:i+5]) for i in range(max(0, len(words(before_out)) - 4)))
    a = set(" ".join(words(after_out)[i:i+5]) for i in range(max(0, len(words(after_out)) - 4)))
    for g in sorted(a - b):
        if g in WEBGRAMS:
            newflags.append((e["row_id"], e["field"], g, sorted(WEBGRAMS[g])[:4]))
print("NEW undelimited 5-word WEB runs introduced by my prose:", len(newflags))
for f in newflags:
    print("   ", f)

# 4. rotation rule: free-text formulations per token type, and the 6-word cap
from collections import defaultdict
forms = defaultdict(set)
toolong = []
for e in EDITS:
    if e["op"] != "append_ref":
        continue
    m = re.match(r"^(\S+) \[([A-Za-z-]+)\] (.+)$", e["value"])
    assert m, e["value"]
    tok, free = m.group(2), m.group(3)
    forms[tok].add(free)
    if len(free.split()) > 6:
        toolong.append((e["value"], len(free.split())))
for tok in sorted(forms):
    n_entries = sum(1 for e in EDITS if e["op"] == "append_ref" and f"[{tok}]" in e["value"])
    print(f"   {tok}: {n_entries} entries, {len(forms[tok])} distinct formulations")
print("free-text over 6 words:", toolong)

json.dump({"edits": EDITS, "discharged": sorted(acct), "not_discharged": NOT_DISCHARGED_IDS,
           "judgement_no_edit": [item_id(i) for i in JUDGE_NO_EDIT]},
          open("edits_stage.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote edits_stage.json")
