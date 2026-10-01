# REPAIR-2 STEP 3 - ADJUDICATION OF TWO BLIND AUTHOR LANES (Fable)

Attempt `ezek_repair2_step3_adjudication_a1`, execution `ezek_repair2_step3_adjudication_a1#e1`. You are the
controlling adjudicator for this step (OW-13: Fable adjudicates). Two blind Opus lanes answered the same 73 owed items
on 43 rows from the same slices. You see both, and you produce ONE proposal the orchestrator applies.

## The gate changed after the lanes ran - and why that matters for their STOPs

Both lanes ran gate v3, which had two defects the lanes found. (1) It refused edits to fields no item named, yet marked
a row unclean for register flags anywhere in it, so P02-003, P08-013 and P09-002 - which carry pre-existing flags in
untouched fields - could never be clean: lane A stopped eight items on it (S3-001, S3-065, S3-066, S3-067..S3-071) and
lane B left the rows out, putting their candidate text in its discharge record. (2) It treated the worklist's
field lists as binding, and four claims sit in a field the list did not name (lane A: S3-009, S3-010, S3-014, S3-016).
Your gate is v3.1: it judges only the flags a proposal INTRODUCES, and it scopes by row. So those twelve STOPs are not
evidence that the items cannot be done - DECIDE THEM ON THE MERITS, using both lanes' would-write text.

Lane A's two other escalations stand on their own: two quotation items name a verse outside their row (S3-024 names
41:26 on P10-005; S3-025 names 40:38 on P01-002) - read what the row actually quotes and decide; and two items touch a
grade's ground (S3-010, S3-029) - a removal that would leave a grade without its ground is a STOP, and a HIGH row's
register rewrites belong to step 5.

## What you decide, item by item, recorded in adjudication.json

1. For every item (S3-nnn): DISCHARGED (with the sentence or entry you adopt), NO_DEFECT (with evidence), or STOP
   (with evidence). Where the lanes agree on status and substance, say so; where they differ, decide on the bytes and
   say which reading you took and why.
2. A lane's claim that a fact reproduces is not proof: re-read the witness, the marks record, the census or the WEB
   verse map by exact path for every fact the adopted text asserts and the slice does not already carry as MEASURED.
   A false only-ground is a STOP, never a substitution.
3. Items routed beyond step 3 - to #e16, to the second Fable review of the flagged regions, or to step 4 - are listed
   under `routed`, each with its reason.

## Rules for what the proposal may say (identical to the lanes' brief, which is pinned)

- No grade, span or identity changes. Refs may be reworded or removed only where an owed item names the entry; a new or
  changed entry uses the vocabulary pinned today (one ROLE token, NO face qualifier - step 4 installs those, a one-to-
  six-word annotation, MT-borne devices on the oshb: face, quotations on the web: face, DEF-A4-ARGUED mirroring). In
  the zone (MT 21:1-5 = WEB 20:45-49) every entry is written on BOTH faces.
- observed_substrate_signals change only on P03-019 and P09-010, as their items name.
- A mark is recorded on the verse it FOLLOWS; any mention of a mark, paseq or puncta carries "single-witness".
- Never hand-type Hebrew: SLICED from the witness or the live row. Five or more WEB words take double curly quotes and
  a web: reference (A6-b exempts a formula rendering only where the row names the device). C2-amended: a claim that
  something is unsourced must be absent from BOTH pinned inputs.
- The register rule: row prose is a scholar-facing record - no rule identifiers, ruling numbers, file or tool names,
  digests, review or wave talk, repair narration. Rotation: no 7-gram in more than a handful of rows, at least 4 distinct formulations.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `9abd545f4854c45610fb66a4b047d668596ed5fb492b348e76216dc220d13614` | the live rows |
| `SP\Ezek\repair2\step3\step3_slices.v1.json` | `a76d278556039dee8534b07309fe1d2636e820453645f773f7886a39d6d5a188` | per row: live fields and every owed item with its measured fact |
| `SP\Ezek\repair2\step3\step3_worklist.v1.json` | `6abae9b262f07cf99b797e534237629bf3d1c9dd92ca15b8681c6661d99b3494` | the worklist and the gate's scope |
| `SP\Ezek\repair2\step3\distinct_checks_q10.v1.json` | `9db639c824625ee585f01e2581bf8c1743ac12f0133693409f5c307299f275e1` | the 13 reproduced facts |
| `SP\Ezek\author\repair2_step3\lane_a\proposal.json` | `bf6ea2f08da06cb637159f50a8fa8bdd6e01ab40de07dfed24ae79974564b9e3` | blind lane A - proposal |
| `SP\Ezek\author\repair2_step3\lane_a\discharge.json` | `4406bdc38f6d22fd206e5d0774bb2be59c1cbf8114046b8c3f25f0951c5f409a` | blind lane A - per-item discharge |
| `SP\Ezek\author\repair2_step3\lane_b\proposal.json` | `31c2e0a82a14f94b49e1dbccd52a1948b0f2d7094154923fe23b813f12296db4` | blind lane B - proposal |
| `SP\Ezek\author\repair2_step3\lane_b\discharge.json` | `0208e19d95b0c6987805502f4dc0c4bca218308ccdc8f94f57f3ccb5df0b158d` | blind lane B - per-item discharge |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` | YOUR GATE (v3.1) - per-row checks as a delta against the live row, plus the whole pinned suite |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` | imported by v3.1 (the gate both lanes ran) |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` | imported by the gate |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` | imported by the gate |
| `SP\Ezek\tools\run_validator_suite.py` | `4c0caa08a2999089bcec23aee6e1a47963e4395fc86d75c1f8139c35775a78cb` | run by the gate |
| `SP\Ezek\tools\check_register.py` | `5106d1be66f3c7c860f98589b46ba52a5d5900cdb41251b54dd7021a7c06462d` | imported by the gate |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` | imported by the gate |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` | imported by the gate |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse ('clean') |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, K/Q, paseq, notes (single witness) |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | the device census |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT map |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | the controlling ruling |
| `SP\Ezek\repair2\step3\STEP3_AUTHOR_BRIEF.md` | `ad087c482d7d635bcdce86ccbb1692e4b2095f70ce529deb53ab1c9bf6c991ed` | the brief both lanes held |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `9abd545f4854c45610fb66a4b047d668596ed5fb492b348e76216dc220d13614` |
| `SP\Ezek\repair2\step3\step3_slices.v1.json` | `a76d278556039dee8534b07309fe1d2636e820453645f773f7886a39d6d5a188` |
| `SP\Ezek\repair2\step3\step3_worklist.v1.json` | `6abae9b262f07cf99b797e534237629bf3d1c9dd92ca15b8681c6661d99b3494` |
| `SP\Ezek\repair2\step3\distinct_checks_q10.v1.json` | `9db639c824625ee585f01e2581bf8c1743ac12f0133693409f5c307299f275e1` |
| `SP\Ezek\author\repair2_step3\lane_a\proposal.json` | `bf6ea2f08da06cb637159f50a8fa8bdd6e01ab40de07dfed24ae79974564b9e3` |
| `SP\Ezek\author\repair2_step3\lane_a\discharge.json` | `4406bdc38f6d22fd206e5d0774bb2be59c1cbf8114046b8c3f25f0951c5f409a` |
| `SP\Ezek\author\repair2_step3\lane_b\proposal.json` | `31c2e0a82a14f94b49e1dbccd52a1948b0f2d7094154923fe23b813f12296db4` |
| `SP\Ezek\author\repair2_step3\lane_b\discharge.json` | `0208e19d95b0c6987805502f4dc0c4bca218308ccdc8f94f57f3ccb5df0b158d` |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` |
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
| `SP\Ezek\repair2\step3\STEP3_AUTHOR_BRIEF.md` | `ad087c482d7d635bcdce86ccbb1692e4b2095f70ce529deb53ab1c9bf6c991ed` |

## The gate - run until ALL_CLEAN

`python -B <SP>\Ezek\repair2\step3\check_candidate_v3_1.py C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step3_adjudication\proposal.json --work C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step3_adjudication\gate_work`

It runs per-row checks and the WHOLE pinned suite on the candidate; no hard member may gain a flag. It is a floor.

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step3_adjudication\proposal.json` - `{"<row>": {"<field>": <full new value>}}`, only changed fields; refs and signals FULL.
2. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step3_adjudication\adjudication.json` - per item the decision above; per row the lane base or merge; top-level `gate`,
   `routed`, `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory. Never modify the corpus or a pinned file; never run git, write a receipt or touch a
registry. Escalate rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts
itself, a digest that differs from the table.
