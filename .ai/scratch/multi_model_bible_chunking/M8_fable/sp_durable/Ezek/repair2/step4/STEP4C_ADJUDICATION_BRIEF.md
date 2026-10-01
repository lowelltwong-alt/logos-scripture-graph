# REPAIR-2 STEP 4c - ADJUDICATION OF TWO BLIND VOCABULARY LANES (Fable)

Attempt `ezek_repair2_step4c_adjudication_a1`, execution `ezek_repair2_step4c_adjudication_a1#e1`. You are the
controlling adjudicator (OW-13: Fable adjudicates). Two blind Opus lanes answered the same 103 owed items on 64 rows
of the clause 6 v2 installation; you produce ONE proposal the orchestrator applies.

## What you decide, recorded in adjudication.json

1. Per item (S4-nnn): DISCHARGED (with the entry you adopt), NO_DEFECT (with evidence) or STOP (with evidence).
2. SEAM PAIRS: where the lanes name different seam pairs for a rival, read the row's rejected alternative and the
   bytes and decide which cut the row actually weighs; where both name the same pair but different qualifiers, the
   rule decides (:near on the rival's candidate onset verse, :far on the verse behind it). A seam pair neither lane can
   support from the row is a STOP.
3. TOKENS: for a disputed token, apply the three decided cases - content a rationale rests on is a WARRANT; an
   inventoried device the boundary does not rest on is DISCLOSURE-device, never ANCHOR; a device the census does not
   record is never DISCLOSURE-device (ANCHOR, or WARRANT-absence / DISCLOSURE-absence for a true absence, with the
   census verified EMPTY at the verse).
4. ROUTED: anything beyond this step - to #e16, the second Fable review of the flagged regions, or step 5 - listed
   with its reason.

## Where the lanes diverge - stated as the orchestrator found it, not as a preference

The lanes' statuses disagree on 20 items; read both discharge files, not this summary, before deciding.

1. **FORWARD-MERGE RIVALS - a class question.** S4-009, 012, 014, 017, 019, 026, 027, 028, 029, 030, 031, 060, 070,
   074, 076, 077, 078, and the qualifier part of S4-085: a WARRANT-rival whose rejected alternative keeps the row's
   onset and extends the row forward, with the entry on the verse after the row's last verse. Lane A qualified them
   with the seam the merge would dissolve on :near and labels that convention INFERRED. Lane B stopped: it holds the
   clause's rival :near ("the candidate onset verse for a rival") gives no truthful face there, cites #e15's
   own_seam_faces and the ruling's one worked merge rival (17.10/17.11), and names three class options with the exact
   entry under each. Decide it here ONLY if clause 6 v2 and #e15 as written decide it. If deciding needs a meaning the
   clause does not give, it is a vocabulary ruling: route it to #e16 with both readings and every affected entry,
   leave those rivals unqualified, and record each item as STOP with the routing. That the member's phase flip then
   waits for #e16 is not a reason to decide either way - quality and completion are the objective, budget a limit.
2. **S4-090 (P02-018).** Lane A: NO_DEFECT - the row's own device_notes answers the implication. Lane B: STOP - the
   implication stands, and every repair re-tokenises a pre-wave descriptive entry, which clause 6 v2's retro-
   qualification clause bars; it needs an exception ruling. P02-018 is already on the #e16 confidence-calibration list.
3. **S4-091 (P05-008).** Lane A: NO_DEFECT - uneven not false, and the order names no re-gloss. Lane B: DISCHARGED -
   one device_notes phrase evened with the rejected-alternative field. Decide whether the item's order reaches that
   field; if it does not, the prose pass owns it.
4. **RE-FACES NO ITEM ORDERED.** Lane A moved seven entries from web: to oshb: under the face rule (15.2, 16.2, 16.8,
   24.9, 24.25, 29.6, 29.8); Lane B five (15.2, 16.2, 24.9, 24.25, 29.6). "Change only what an owed item names" and
   the face rule both bind; decide per entry, and say which rule governed.
5. **ZONE SEAM PAIRS** are written in WEB numbering by both lanes; the role_tokens member skips zone entries, so the
   offset-map form check is the only verification. Say so in what_i_could_not_verify if you adopt them.
6. **NOTED, NOT YOURS TO REPAIR HERE:** SRA prose in P01-009, P02-003 and P03-007 uses near/far in the older before/
   after sense (the prose pass owns it); the universals triage member stops reading an annotation once a qualifier is
   present, so triage counts can fall with no claim changing (a member defect, already routed).

## Rules for the proposal (the lanes' brief is pinned and binds you identically)

Change only what an owed item names; no grade, span, identity or signals changes; face qualifiers only on WARRANT-
onset/close/rival; MT-borne devices on the oshb: face and English quotations on the web: face; in the zone (MT 21:1-5
= WEB 20:45-49) every entry is written on BOTH faces; annotations one to six words (seven when a rival's first word is
its seam pair); DEF-A4-ARGUED mirroring kept; "single-witness" on any mark, paseq or puncta mention; never hand-type
Hebrew - SLICED from the witness or the live row; double curly quotes and a web: reference for five or more WEB words
(A6-b); C2-amended - unsourced means absent from BOTH pinned inputs; a mark is recorded on the verse it FOLLOWS; the
register rule - a row is a scholar-facing record; no 7-gram in more than a handful of rows, at least 4 distinct
formulations.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `32f33f05e8adb185027b278813537b8b466f58a7a82eabad186e5ad72dcf398e` | the live rows |
| `SP\Ezek\repair2\step4\step4c_slices.v1.json` | `dd25e38b14e22b1525803f9899f542dc9f55f8d28f41d337cab7374d7bf22d5b` | per row: span, prose, refs, owed items; clause 6 v2 verbatim |
| `SP\Ezek\repair2\step4\step4c_worklist.v1.json` | `40036cc483f451e10e650dedf9cbc87a1e732828cefbcdedb07c38f5b7fc7d12` | the worklist and the gate's scope |
| `SP\Ezek\repair2\step4\STEP4C_AUTHOR_BRIEF.md` | `c5c7cbb0cefd12dfcb38bfc916e03859db290e26344b729ed02bbb9dcf32b1ee` | the brief both lanes held: clause 6 v2 and one worked example per token |
| `SP\Ezek\author\repair2_step4c\lane_a\proposal.json` | `31c93d16eb927f42892883596ea84b69471388715cdb22f6fa48f70d25ac2960` | blind lane A - proposal |
| `SP\Ezek\author\repair2_step4c\lane_a\discharge.json` | `67e0055fe41cc8ea8f115812daf695cae0b1c6ea5960a1cc6975726ec2244569` | blind lane A - per-item discharge |
| `SP\Ezek\author\repair2_step4c\lane_b\proposal.json` | `a9c850340b0e1c189ad2d57d86e64237c084be22e866c7927e6a5798dfd81338` | blind lane B - proposal |
| `SP\Ezek\author\repair2_step4c\lane_b\discharge.json` | `0e0c63fdae86f99fafc05666521217c59de4704d1084852f863ba0a84ad2bdc7` | blind lane B - per-item discharge |
| `SP\Ezek\repair2\step4\check_candidate_v4.py` | `9ef213b6c3c24ca15c9abc449ca30d72471d650cd29d67f083c4984be6846883` | YOUR GATE (v4) |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` | imported by the gate |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` | imported by the gate |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` | imported by the gate |
| `SP\Ezek\tools\run_validator_suite.py` | `d7778f83eb0afff94a63dc7d8aad8ed7908b52bdaca4724b615f2fc30d35bf69` | run by the gate, with the hard role_tokens member |
| `SP\Ezek\tools\check_role_tokens.py` | `6fc5fb3ff5e35a99b0d132f42f842b99784bb0b5b86254c2f895732be1872d64` | verifies every face qualifier and seam pair |
| `SP\Ezek\tools\role_tokens_phase.json` | `1a70b7a300486f361c9a793cdeb6ebd473b85519ed0b2a14515f99f1f35f94aa` | the member's pinned phase |
| `SP\Ezek\tools\check_register.py` | `5106d1be66f3c7c860f98589b46ba52a5d5900cdb41251b54dd7021a7c06462d` | imported by the gate |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` | imported by the gate |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` | imported by the gate |
| `SP\Ezek\verse_inventory.json` | `7314690191ec380b25578ca33d4745f4e60196b9f0e1dda4a1bcc9286c19cf54` | per-chapter verse counts, WEB face |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, K/Q, paseq, notes (single witness) |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | the device census |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT map |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | the ruling whose clause 6 v2 is being installed |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `32f33f05e8adb185027b278813537b8b466f58a7a82eabad186e5ad72dcf398e` |
| `SP\Ezek\repair2\step4\step4c_slices.v1.json` | `dd25e38b14e22b1525803f9899f542dc9f55f8d28f41d337cab7374d7bf22d5b` |
| `SP\Ezek\repair2\step4\step4c_worklist.v1.json` | `40036cc483f451e10e650dedf9cbc87a1e732828cefbcdedb07c38f5b7fc7d12` |
| `SP\Ezek\repair2\step4\STEP4C_AUTHOR_BRIEF.md` | `c5c7cbb0cefd12dfcb38bfc916e03859db290e26344b729ed02bbb9dcf32b1ee` |
| `SP\Ezek\author\repair2_step4c\lane_a\proposal.json` | `31c93d16eb927f42892883596ea84b69471388715cdb22f6fa48f70d25ac2960` |
| `SP\Ezek\author\repair2_step4c\lane_a\discharge.json` | `67e0055fe41cc8ea8f115812daf695cae0b1c6ea5960a1cc6975726ec2244569` |
| `SP\Ezek\author\repair2_step4c\lane_b\proposal.json` | `a9c850340b0e1c189ad2d57d86e64237c084be22e866c7927e6a5798dfd81338` |
| `SP\Ezek\author\repair2_step4c\lane_b\discharge.json` | `0e0c63fdae86f99fafc05666521217c59de4704d1084852f863ba0a84ad2bdc7` |
| `SP\Ezek\repair2\step4\check_candidate_v4.py` | `9ef213b6c3c24ca15c9abc449ca30d72471d650cd29d67f083c4984be6846883` |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` |
| `SP\Ezek\tools\run_validator_suite.py` | `d7778f83eb0afff94a63dc7d8aad8ed7908b52bdaca4724b615f2fc30d35bf69` |
| `SP\Ezek\tools\check_role_tokens.py` | `6fc5fb3ff5e35a99b0d132f42f842b99784bb0b5b86254c2f895732be1872d64` |
| `SP\Ezek\tools\role_tokens_phase.json` | `1a70b7a300486f361c9a793cdeb6ebd473b85519ed0b2a14515f99f1f35f94aa` |
| `SP\Ezek\tools\check_register.py` | `5106d1be66f3c7c860f98589b46ba52a5d5900cdb41251b54dd7021a7c06462d` |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` |
| `SP\Ezek\verse_inventory.json` | `7314690191ec380b25578ca33d4745f4e60196b9f0e1dda4a1bcc9286c19cf54` |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` |

## The gate - clean verdict, and the completion measure driven to what the rows honestly allow

`python -B <SP>\Ezek\repair2\step4\check_candidate_v4.py C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step4c_adjudication\proposal.json --work C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step4c_adjudication\gate_work`

It checks form and introduced flags, runs the WHOLE pinned suite including the hard role_tokens member (which
verifies every face qualifier and seam pair and fails loud), and reports the warrants still unqualified on your
candidate. Every warrant left unqualified must be a recorded STOP.

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step4c_adjudication\proposal.json` - only changed fields; refs as FULL lists.
2. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step4c_adjudication\adjudication.json` - per item the decision; per disputed seam pair or token the reading taken and why;
   top-level `gate` with the completion measure, `routed`, `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. Escalate
rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts itself, a digest that
differs from the table.
