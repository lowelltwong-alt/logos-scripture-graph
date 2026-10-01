# REPAIR-2 STEP 3 - MEASURED-FALSE CLAIMS ANYWHERE. Author brief (two blind lanes)

You are ONE OF TWO BLIND LANES. The other lane has this brief and these slices; you will not see its work and it will
not see yours. A Fable adjudicator reconciles the two. Your independence is the value of your pass.

## What this step is

#e15 ruled that "the repair scope extends to every claim a reviewer MEASURED false, wherever it sits and whichever
wave last touched the field ... the close gate cannot pass a row carrying a measured-false byte claim." The slices
carry 73 owed items on 43 rows from seven sources: #e15's measured-false list (each fact distinct-checked
and reproduced), undischarged orders, stale census figures, bare-decimal verse anchors, an author lane's escalations,
obligations the step-2 adjudication carried forward, and two Hebrew runs the citation sweep cannot collate.

Every item has a STATUS measured on the current rows: PRESENT means the claim or entry still stands; READER means
the order names nothing a string test can find, so you read the row and decide. A READER item where you find no
defect is recorded as NO_DEFECT with your evidence - never skipped.

## The rules that decide what you may write

- **An order is authority for exactly what it names and nothing adjacent.** A false only-ground is a STOP, never a
  substitution: if removing a false sentence leaves a grade or a boundary without its ground, record a STOP with the
  evidence instead of inventing a new ground.
- **Reproduce before you write.** A fact the slice carries as MEASURED (a distinct check) may be written. A fact a
  reviewer REPORTED (for example lane 02's wheel-vocabulary counts) must be reproduced by you from the witness by
  exact path first; if it does not reproduce, it is a STOP.
- **No grade, span or identity changes.** Grades are not yours in this step.
- **Refs may be reworded or removed only where an owed item names the entry.** A new or changed entry uses the
  vocabulary pinned today: `<face>:Ezek.C.V[-Ezek.C.V] [TOKEN] annotation`, one ROLE token from
  check_refs_mirror.ROLE_VOCABULARY (DEF-A4-ARGUED: every argued citation is mirrored by an entry with a ROLE token),
  NO face qualifier (step 4 installs those), an annotation of one to six words. An MT-borne device (mark, K/Q, paseq,
  note, device) sits on the oshb: face; a quotation on the web: face.
- **The zone:** MT 21:1-5 = WEB 20:45-49 and MT 21:6-37 = WEB 21:1-32. Any entry touching it is written on BOTH faces,
  `web:... = oshb:...`, mapped by the offset map and never by arithmetic.
- **observed_substrate_signals** may change only on a row whose owed item names it (P03-019, P09-010).
- **Marks:** a mark is recorded on the verse it FOLLOWS. Any entry or sentence that mentions a mark, paseq or puncta
  carries the literal disclosure "single-witness".
- **Hebrew:** never hand-type Hebrew. Every run is SLICED from `Ezek_oshb.txt` or from the live row by exact bytes; a
  labelled Qere form collates against its K/Q note.
- **English:** five or more WEB words are a quotation - double curly quotes and an in-field web: reference; the A6-b
  exemption covers a formula rendering only when the row names the device.
- **Categorical claims:** C2-amended - a claim that something is unsourced must be absent from BOTH pinned inputs; the
  census governs counts and membership.
- **Register rule:** row prose is a scholar-facing record - no rule identifiers, ruling numbers, file or tool names,
  digests, review or wave talk, or repair narration. State the fact about the text.
- **Rotation:** vary your wording; no 7-gram in more than a handful of rows, at least 4 distinct formulations for
  repeated kinds of statement.
- **Bare decimals (Q11 items):** if the dotted pair is an argued anchor, rewrite it as an explicit `oshb:Ezek.C.V` or
  `web:Ezek.C.V` and mirror it; if it is not argued (a range description, a count), leave it and say why.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `9abd545f4854c45610fb66a4b047d668596ed5fb492b348e76216dc220d13614` | the live rows after REPAIR-2 step 2 |
| `SP\Ezek\repair2\step3\step3_slices.v1.json` | `a76d278556039dee8534b07309fe1d2636e820453645f773f7886a39d6d5a188` | per row: live fields and every owed item, with its measured fact where one exists |
| `SP\Ezek\repair2\step3\step3_worklist.v1.json` | `6abae9b262f07cf99b797e534237629bf3d1c9dd92ca15b8681c6661d99b3494` | the worklist the slices come from, and the gate's scope |
| `SP\Ezek\repair2\step3\distinct_checks_q10.v1.json` | `9db639c824625ee585f01e2581bf8c1743ac12f0133693409f5c307299f275e1` | the 13 distinct checks (all reproduce) |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` | YOUR GATE - per-row checks plus the WHOLE pinned suite on your candidate |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` | imported by the gate |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` | imported by the gate |
| `SP\Ezek\tools\run_validator_suite.py` | `4c0caa08a2999089bcec23aee6e1a47963e4395fc86d75c1f8139c35775a78cb` | run by the gate |
| `SP\Ezek\tools\check_register.py` | `5106d1be66f3c7c860f98589b46ba52a5d5900cdb41251b54dd7021a7c06462d` | imported by the gate |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` | imported by the gate; ROLE_VOCABULARY is the vocabulary in force |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` | imported by the gate; web_to_mt and load_verse_maps |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse (WEB): read the 'clean' field |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) - slice Hebrew from here |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | section marks, K/Q notes, paseq, other notes (single witness) |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | the device census |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT numbering map |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | the ruling behind the Q10 items |
| `SP\Ezek\a4_extraction_gap.v1.json` | `1bfa3505960e6f1886455786c9738a64b607f3e4c6e92ee569cb645e708fa916` | the source of the bare-decimal items |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `9abd545f4854c45610fb66a4b047d668596ed5fb492b348e76216dc220d13614` |
| `SP\Ezek\repair2\step3\step3_slices.v1.json` | `a76d278556039dee8534b07309fe1d2636e820453645f773f7886a39d6d5a188` |
| `SP\Ezek\repair2\step3\step3_worklist.v1.json` | `6abae9b262f07cf99b797e534237629bf3d1c9dd92ca15b8681c6661d99b3494` |
| `SP\Ezek\repair2\step3\distinct_checks_q10.v1.json` | `9db639c824625ee585f01e2581bf8c1743ac12f0133693409f5c307299f275e1` |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` |
| `SP\Ezek\tools\run_validator_suite.py` | `4c0caa08a2999089bcec23aee6e1a47963e4395fc86d75c1f8139c35775a78cb` |
| `SP\Ezek\tools\check_register.py` | `5106d1be66f3c7c860f98589b46ba52a5d5900cdb41251b54dd7021a7c06462d` |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` |
| `SP\Ezek\a4_extraction_gap.v1.json` | `1bfa3505960e6f1886455786c9738a64b607f3e4c6e92ee569cb645e708fa916` |

## Your gate - run it until ALL_CLEAN

`python -B <SP>\Ezek\repair2\step3\check_candidate_v3.py <your dir>\proposal.json --work <your dir>\gate_work`

It checks each proposed row (scope from the worklist, entry form, register, mirroring) AND runs the whole pinned
suite on your candidate rows against the live rows: no hard member may gain a flag. Running the suite THROUGH THIS
GATE is permitted; run no validator any other way. Its selftest runs first and refuses a verdict if an arm cannot fire.
It is a floor: it cannot tell you a sentence is true.

## Outputs - write early and rewrite at every stage (E-29); digest after your final write

1. `proposal.json` - `{"<row>": {"<field>": <full new value>}}`, only fields you change; refs and signals as FULL values.
2. `discharge.json` - per item id (S3-nnn): `status` DISCHARGED | NO_DEFECT | STOP, `what_i_wrote` (the sentence or
   entry) or `evidence` (for NO_DEFECT and STOP), `facts_reproduced` (each with tier), plus top-level `gate` (final
   ALL_CLEAN summary), `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory. Never modify the corpus or any pinned file. Never run git, write a receipt or touch
a registry. Escalate rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts
itself, a digest that differs from the table.
