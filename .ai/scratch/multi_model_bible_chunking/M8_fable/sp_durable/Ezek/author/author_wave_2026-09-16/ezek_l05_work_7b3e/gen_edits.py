# -*- coding: utf-8 -*-
import json
LANE = r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_aw\lanes\lane_05_worklist.json"
lane = json.load(open(LANE, encoding='utf-8'))
ROWS = {r['decision_id']: r for r in lane['your_rows']}
D = json.load(open('derived_strings.json', encoding='utf-8'))
EDITS = []
PROBLEMS = []

TIER_A4 = ("MEASURED over the pinned witness and marks input for every mark, K/Q and accent fact named; "
           "the citation's unmirrored status is EXTRACTED from the ruled worklist item")


def E(row, field, op, value, items, sweep, why, tier, role=None, note=None):
    r = ROWS[row]
    e = {"row_id": row, "field": field, "op": op,
         "expected_before": r[field],
         "value": value, "worklist_item_ids": items, "sweep": sweep,
         "why": why, "tier": tier}
    if role:
        e["role_token"] = role
    if note:
        e["sweep_pooling_note"] = note
    EDITS.append(e)


# ============ 1. CONFIDENCE ============
CONF = [("P07-008", "medium_low", "l05_i08", "low"),
        ("P08-003", "medium", "l05_i16", "medium_low"),
        ("P08-012", "medium", "l05_i39", "high"),
        ("P08-013", "medium", "l05_i43", "high"),
        ("P09-009", "medium", "l05_i68", "medium_low"),
        ("P09-011", "medium", "l05_i75", "high")]
for row, newv, iid, expect in CONF:
    assert ROWS[row]["confidence"] == expect, (row, ROWS[row]["confidence"])
    assert newv in ("high", "medium", "medium_low", "low")
    E(row, "confidence", "set_confidence", newv, [iid], "confidence",
      "Applied as ruled; the grade is on the four-value scale and is not chosen here. Current value %r -> %r." % (expect, newv),
      "EXTRACTED from the ruling carried in the worklist item")

# ============ 2. A4 append_ref ============
A4 = [
 ("P07-005", "l05_i00", "web:Ezek.31.1 [WARRANT-close] next dateline bounds the close", "WARRANT-close",
  "The close is argued as standing immediately before the hard-seam dateline at 31:1, so the close rests on this verse."),
 ("P07-005", "l05_i01", "web:Ezek.30.19 [DISCLOSURE-mark] pe precedes this onset", "DISCLOSURE-mark",
  "device_notes asserts a pe after MT 30:19. MEASURED: pmarks marks[Ezek.30.19] == [PE]. A mark is corroboration, not a driver, so it is disclosed and not warranted."),
 ("P07-006", "l05_i02", "web:Ezek.32.1 [WARRANT-close] dateline at the far close face", "WARRANT-close",
  "The cedar allegory is closed immediately before 32:1's hard-seam dateline; the close rests there."),
 ("P07-006", "l05_i03", "web:Ezek.30.26 [DISCLOSURE-mark] samekh behind the onset seam", "DISCLOSURE-mark",
  "device_notes asserts a samekh after MT 30:26 corroborating the 31:1 onset. MEASURED: marks[Ezek.30.26] == [SAMEKH]."),
 ("P07-007", "l05_i04", "web:Ezek.32.17 [WARRANT-close] following dateline fixes this close", "WARRANT-close",
  "The qinah colophon close is argued against the hard-seam dateline that follows at 32:17."),
 ("P07-007", "l05_i05", "web:Ezek.32.8 [WARRANT-rival] rival seam weighed and held", "WARRANT-rival",
  "The rejected-alternative field weighs a split at 32:8/32:9; 32:8 carries the rival's near face, an utterance-formula close."),
 ("P07-007", "l05_i06", "web:Ezek.32.9 [WARRANT-rival] far face of that rival", "WARRANT-rival",
  "32:9 is the far face of that same weighed rival, the fresh 'I will also trouble' clause."),
 ("P07-007", "l05_i07", "web:Ezek.31.18 [DISCLOSURE-mark] witness records a mark here", "DISCLOSURE-mark",
  "device_notes asserts a samekh after MT 31:18 at this row's onset seam. MEASURED: marks[Ezek.31.18] == [SAMEKH]."),
 ("P07-008", "l05_i10", "web:Ezek.32.1-Ezek.32.16 [ANCHOR] preceding qinah unit, genre comparison", "ANCHOR",
  "A RANGE citation takes a RANGE entry. The row cites 32:1-16 to compare genre labels, not to argue this row's seam, so ANCHOR is the honest label and not a demotion."),
 ("P07-008", "l05_i11", "web:Ezek.32.19-Ezek.32.21 [ANCHOR] taunt section inside the span", "ANCHOR",
  "A RANGE citation takes a RANGE entry. The taunt is in-span content the boundary does not rest on."),
 ("P07-008", "l05_i12", "web:Ezek.32.16 [DISCLOSURE-mark] pe follows, corroborating this onset", "DISCLOSURE-mark",
  "device_notes asserts a pe after MT 32:16 at this row's own onset seam. MEASURED: marks[Ezek.32.16] == [PE]. Only one token is allowed per entry, so the qinah-colophon mention in the rejected-alternative field rides on this same entry."),
 ("P08-001", "l05_i14", "web:Ezek.33.7 [DISCLOSURE-device] son-of-man recurrence, non-cutting", "DISCLOSURE-device",
  "device_notes cites 33.7 for a second in-span son-of-man address the boundary does not rest on. MEASURED: marks[Ezek.33.7] is absent, so the entry implies no mark."),
 ("P08-003", "l05_i17", "web:Ezek.33.23 [WARRANT-close] fresh word-event past this close", "WARRANT-close",
  "The two-verse unit's close is argued against the fresh, formally distinct word-event opening at 33:23."),
 ("P08-003", "l05_i18", "web:Ezek.33.23-Ezek.33.29 [WARRANT-rival] merge rival weighed then refused", "WARRANT-rival",
  "A RANGE citation takes a RANGE entry. The rejected alternative is folding 33:21-22 into that following row, which is the rival weighed under A9/A16."),
 ("P08-004", "l05_i20", "web:Ezek.33.24 [DISCLOSURE-device] address follows the word-event onset", "DISCLOSURE-device",
  "The onset rests on 33:23's strict word-event; 33:24's son-of-man address follows as corroboration, so a WARRANT token would overstate. 33:24 also carries a MEASURED samekh already disclosed in device_notes."),
 ("P08-004", "l05_i21", "web:Ezek.33.26 [DISCLOSURE-mark] interior samekh, non-cutting texture", "DISCLOSURE-mark",
  "device_notes discloses the samekh after 33.26 as non-cutting. MEASURED: marks[Ezek.33.26] == [SAMEKH]."),
 ("P08-004", "l05_i22", "web:Ezek.33.28 [ANCHOR] cohesion phrase, texture only", "ANCHOR",
  "The row itself says the cohesion phrase at 33.28 is texture and not boundary evidence; ANCHOR records that. MEASURED: marks[Ezek.33.28] is absent. The row's 15-verse sweep figure is its own and is not restated here."),
 ("P08-005", "l05_i24", "web:Ezek.34.1 [WARRANT-close] hard seam opens immediately after", "WARRANT-close",
  "The close is argued against 34:1's fresh word-event hard seam on the far face."),
 ("P08-005", "l05_i25", "web:Ezek.33.23-Ezek.33.29 [WARRANT-rival] backward merge rival, rejected", "WARRANT-rival",
  "A RANGE citation takes a RANGE entry. The rejected alternative is reading 33:30-33 as the tail of that row."),
 ("P08-005", "l05_i26", "web:Ezek.33.29 [WARRANT-onset] verse-final close licenses this onset", "WARRANT-onset",
  "MEASURED from the pinned witness: 33:29's recognition formula ends at the etnachta on YHWH and the remainder of the verse is a dependent temporal infinitive, which #e14 Q2 grades verse-final in effect. CUT-RULE limb (b) is therefore met and the 33:30 ve'attah sub-onset rests on this close."),
 ("P08-011", "l05_i37", "web:Ezek.36.12 [WARRANT-onset] close and samekh behind onset", "WARRANT-onset",
  "LF's A4 install, carried under the boss work order. The onset is argued from the refrain-grade close plus samekh at 36:12. MEASURED: marks[Ezek.36.12] == [SAMEKH]."),
 ("P08-011", "l05_i38", "web:Ezek.36.1-Ezek.36.12 [WARRANT-rival] fold-back rival, addressee change refuses", "WARRANT-rival",
  "A RANGE citation takes a RANGE entry. The row weighs folding these three verses back into 36:1-12 and holds against it on the 2mp/2ms-to-2fs addressee change, CUT-RULE limb (a)."),
 ("P08-012", "l05_i42", "web:Ezek.36.20 [ANCHOR] profanation narrated here, interior content", "ANCHOR",
  "36:20 is cited for the third-person narration the 36:22 pivot draws on: interior content, not a seam claim. MEASURED: marks[Ezek.36.20] is absent."),
 ("P08-014", "l05_i50", "web:Ezek.36.32 [WARRANT-onset] onset rests on this close", "WARRANT-onset",
  "The row's prose does rest its onset on 36:32's close, and the token records where the rationale rests. SEE ESCALATION ESC-3: I measured 36:32's utterance formula as mid-verse with an independent clause following it, the #e14 Q2 weak shape; that bears on the licensing and is raised upward rather than written into the row."),
 ("P08-014", "l05_i51", "web:Ezek.37.1 [ANCHOR] seam context only, not argued", "ANCHOR",
  "The row says in terms that 37:1 is named only as the seam context and not as a claim; ANCHOR is the honest token for exactly that case."),
 ("P09-001", "l05_i54", "web:Ezek.37.2 [ANCHOR] scene interior, bones setting", "ANCHOR",
  "The tracked citation is 'verse 2' in boundary_rationale, an in-span scene statement. The separate paseq disclosure at 37.2 in device_notes rides on this entry, since only one token is allowed."),
 ("P09-001", "l05_i55", "web:Ezek.37.10 [WARRANT-rival] rival split point, mark-only", "WARRANT-rival",
  "The rejected alternative weighs a split at 37.10. MEASURED: marks[Ezek.37.10] == [SAMEKH], so the rival is mark-only, which CONF-CAL makes weighable but never fatal."),
 ("P09-001", "l05_i56", "web:Ezek.37.12 [WARRANT-rival] second rival point, also mark-only", "WARRANT-rival",
  "The same rejected alternative weighs 37.12. MEASURED: marks[Ezek.37.12] == [SAMEKH]; the row's claim that both points carry a samekh reproduces."),
 ("P09-001", "l05_i57", "web:Ezek.37.3 [QUOTE] A6 run anchored at this verse", "QUOTE",
  "After the A6 install on device_notes this field carries a delimited WEB quotation anchored at 37:3, which is what QUOTE labels. It is not a boundary claim, and the row's tier-4 formatting disclaimer stands."),
 ("P09-001", "l05_i58", "web:Ezek.36.38 [DISCLOSURE-mark] setumah recorded on this verse", "DISCLOSURE-mark",
  "device_notes asserts a samekh after MT 36:38 behind this row's onset. MEASURED: marks[Ezek.36.38] == [SAMEKH]."),
 ("P09-002", "l05_i61", "web:Ezek.37.22 [DISCLOSURE-kq] K/Q note inside this span", "DISCLOSURE-kq",
  "device_notes discloses a K/Q at 37.22 and argues no boundary from it. MEASURED: pmarks kq[Ezek.37.22] is a one-member list and the ketiv and qere forms the row prints reproduce from it."),
 ("P09-003", "l05_i62", "web:Ezek.38.3 [WARRANT-onset] messenger names the addressee here", "WARRANT-onset",
  "The onset argument is a three-verse cluster (38:1 word-event, 38:2 set-your-face, 38:3 messenger formula naming Gog), so the rationale does rest on 38:3 as part of it."),
 ("P09-008", "l05_i65", "web:Ezek.39.12 [DISCLOSURE-device] duration word, not a dateline", "DISCLOSURE-device",
  "device_notes cites 39.12's month-word as a stated duration and expressly not a dateline. Consistent with the ratified D11 table, which does not list it. No census count is asserted here."),
 ("P09-008", "l05_i66", "web:Ezek.39.14 [DISCLOSURE-device] second duration reading, no date", "DISCLOSURE-device",
  "The same device_notes sentence cites 39.14. The A6 quotation installed at 39:14 in that field rides on this entry; one token per entry, and the reading claim is what this citation anchors."),
 ("P09-009", "l05_i70", "web:Ezek.39.16 [DISCLOSURE-mark] single samekh corroborates the onset", "DISCLOSURE-mark",
  "device_notes asserts a samekh after MT 39:16 as onset corroboration. MEASURED: marks[Ezek.39.16] == [SAMEKH]."),
]
for row, iid, val, role, why in A4:
    E(row, "boundary_evidence_refs", "append_ref", val, [iid], "a4", why, TIER_A4, role)

# annotation length guard: at most 6 words after the ROLE token
for e in EDITS:
    if e["op"] == "append_ref":
        tail = e["value"].split("] ", 1)[1]
        if len(tail.split()) > 6:
            PROBLEMS.append("annotation over 6 words: " + e["value"])
        if e["value"].count("[") != 1:
            PROBLEMS.append("token count wrong: " + e["value"])

json.dump({"edits": EDITS, "problems": PROBLEMS},
          open('edits_part_a.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("part A edits:", len(EDITS))
print("problems:", PROBLEMS if PROBLEMS else "none")
