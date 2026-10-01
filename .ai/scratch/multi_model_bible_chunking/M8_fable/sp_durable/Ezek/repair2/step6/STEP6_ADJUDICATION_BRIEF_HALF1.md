# REPAIR-2 STEP 6 - ADJUDICATION OF TWO BLIND AUTHOR LANES, HALF 1 (Fable)

Attempt `ezek_repair2_step6_h1_adjudication_a1`, execution `ezek_repair2_step6_h1_adjudication_a1#e1`. You are
the controlling adjudicator (OW-13: Fable adjudicates). Two blind Opus lanes answered the same 41 owed items of
the transport batch, the routed repairs and the register items on this half; you produce ONE proposal. The other half has its own adjudicator.

## What you decide, recorded in adjudication.json

1. Per item (S5-nnn): DISCHARGED (with the text you adopt), NO_DEFECT (with evidence) or STOP (with evidence).
2. Per changed field: which lane's text you adopt, or a reconciled text of your own where neither lane's text both
   states the substance and reads as English - and why. A reconciled text owes everything a lane's text owes.
3. READ EVERY ADOPTED FIELD IN FULL AS ENGLISH after your final edit. This is the second reading #e15 Q9(b) requires
   under OW-19; the gate's English arm is a floor that cannot see a doubled article across a noun or a dropped clause
   boundary. Record `read_back: true` per field only after you have read it.
4. CLAIMS: any anchor the gate reports removed must be accounted for in your own `claim_accounting[row]`, taken from
   the lane you followed or written by you; a claim neither lane can account for is restored, never dropped.
5. ROUTED: anything beyond this step - a claim you believe false, a grade question, a class question for #e16, the
   second Fable review - listed with its reason.

## Where the lanes diverge - computed from their files, stated without a preference

- items whose statuses differ: 0; items missing from a discharge: A 0, B 0
- fields only lane A changed: 2; only lane B: 1; both changed differently: 28; identically: 5
- stops: lane A 0, lane B 0

The full lists are in the pinned divergence file. A field only one lane changed is a question in itself: was the other
lane right to leave it (NO_DEFECT), or did it miss an owed item?

## Rules - the lanes' brief is pinned and binds you identically

State substance, never a barred referent: no rule ids, ruling numbers, file or tool names, digests, record, census,
plan, inventory, worklist or key names, review or wave talk, repair narration. The register rule: a row is a
scholar-facing record. Name the witness and its layers; "(sweep: N verses)" is the one sanctioned count shorthand.
Change no claim beyond an item's order; refs change only where an item names them, each entry passing the gate's form; no grade, span, identity or signals change. RE-MEASURE every routed claim before adopting a repair of it. No grade moves in this step. "single-witness" on any mark, paseq or puncta
mention; a mark is recorded on the verse it FOLLOWS; never hand-type Hebrew - SLICED from the witness or the live row;
five or more WEB words take double curly quotes and a web: reference, a counted device's fixed rendering is exempt
(A6-b); C2-amended - unsourced means absent from BOTH pinned inputs; DEF-A4-ARGUED - every argued citation stays
mirrored by a refs entry with a ROLE token, whose face qualifier and seam pair must still agree with the prose; the
zone - MT 21:1-5 = WEB 20:45-49 - on BOTH faces; rotation - no 7-gram in more than a handful of rows, at least 4
distinct formulations.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `a2e51d689bcb8e656ece9e657521407facf5eeecd67cbf06d4214ef2e8dd601f` | the live rows |
| `SP\Ezek\repair2\step6\step6_slices_half1.v1.json` | `7f3ce81c4ced11f7d23ab41cd2d1555b52b0fc372d63db8ade2124be40da732c` | this half's rows, prose and owed items |
| `SP\Ezek\repair2\step6\step6_worklist.v1.json` | `bd03f40a67079fd27efef62dec971cbcac4b8c7a7932e46357df7ef4d90a919d` | the worklist and the gate's scope |
| `SP\Ezek\repair2\step6\step6_substance.v1.json` | `5e6dff35eb7adbc8201bac6a8816281d2bff5b85607ae46e64dc86ec1058f9c7` | the substance this step applies, verbatim from the records that define it |
| `SP\Ezek\repair2\step6\STEP6_AUTHOR_BRIEF_HALF1.md` | `eabd7feff6246d1009912e20149db8bfc9f2b2cabbb5a9072c1d4fe7c41e54e1` | the brief both lanes held; its rules bind you identically |
| `SP\Ezek\author\repair2_step6\h1_lane_a\proposal.json` | `660f294025e93c9e8d4b773cc742f4b5a1483c2a59a1da4bf1cfe09031993cd7` | blind lane A - proposal |
| `SP\Ezek\author\repair2_step6\h1_lane_a\discharge.json` | `5eaf58f006f519383e152387d570a2337a476ab2442619c7dfa3b00dc52bc7a2` | blind lane A - per-item discharge and claim accounting |
| `SP\Ezek\author\repair2_step6\h1_lane_b\proposal.json` | `c572cf5194933f37ca66ff0c1c560524849c2635d80d412a8df12e9929ff0b2e` | blind lane B - proposal |
| `SP\Ezek\author\repair2_step6\h1_lane_b\discharge.json` | `7748ca4bbccd2519292fadc618e71e4dccd087e3c676771cd33ec88d27d31447` | blind lane B - per-item discharge and claim accounting |
| `SP\Ezek\repair2\step6\step6_divergence_half1.v1.json` | `e322181a2c62dfa363bb3dbe7f5898edf679af85e754936d6f91fff23e0a44a4` | where the lanes diverge, computed from their files (a map, not a reading) |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | the ruling: q8_transport_class governs the transport items, q9 the register items |
| `SP\Ezek\repair2\step5\check_candidate_v5.py` | `c98a74d01aa5c7ed79f30b1e15fd23dd4896c2f8fab8641f247c8a8df768333c` | YOUR GATE (v5, run with the step-6 worklist) |
| `SP\Ezek\repair2\step4\check_candidate_v4.py` | `9ef213b6c3c24ca15c9abc449ca30d72471d650cd29d67f083c4984be6846883` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` | imported by the gate |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` | imported by the gate |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` | imported by the gate |
| `SP\Ezek\tools\run_validator_suite.py` | `d7778f83eb0afff94a63dc7d8aad8ed7908b52bdaca4724b615f2fc30d35bf69` | run by the gate |
| `SP\Ezek\tools\check_register.py` | `2073135c343b5d89ef16e69599fc3c300c6d3fabb7aacddbcfe8200797380f22` | the register member |
| `SP\Ezek\tools\check_role_tokens.py` | `6fc5fb3ff5e35a99b0d132f42f842b99784bb0b5b86254c2f895732be1872d64` | a hard member |
| `SP\Ezek\tools\role_tokens_phase.json` | `1a70b7a300486f361c9a793cdeb6ebd473b85519ed0b2a14515f99f1f35f94aa` | its pinned phase |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` | imported by the gate |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` | imported by the gate |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, K/Q, paseq, notes (single witness) |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | the device census |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT map |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `a2e51d689bcb8e656ece9e657521407facf5eeecd67cbf06d4214ef2e8dd601f` |
| `SP\Ezek\repair2\step6\step6_slices_half1.v1.json` | `7f3ce81c4ced11f7d23ab41cd2d1555b52b0fc372d63db8ade2124be40da732c` |
| `SP\Ezek\repair2\step6\step6_worklist.v1.json` | `bd03f40a67079fd27efef62dec971cbcac4b8c7a7932e46357df7ef4d90a919d` |
| `SP\Ezek\repair2\step6\step6_substance.v1.json` | `5e6dff35eb7adbc8201bac6a8816281d2bff5b85607ae46e64dc86ec1058f9c7` |
| `SP\Ezek\repair2\step6\STEP6_AUTHOR_BRIEF_HALF1.md` | `eabd7feff6246d1009912e20149db8bfc9f2b2cabbb5a9072c1d4fe7c41e54e1` |
| `SP\Ezek\author\repair2_step6\h1_lane_a\proposal.json` | `660f294025e93c9e8d4b773cc742f4b5a1483c2a59a1da4bf1cfe09031993cd7` |
| `SP\Ezek\author\repair2_step6\h1_lane_a\discharge.json` | `5eaf58f006f519383e152387d570a2337a476ab2442619c7dfa3b00dc52bc7a2` |
| `SP\Ezek\author\repair2_step6\h1_lane_b\proposal.json` | `c572cf5194933f37ca66ff0c1c560524849c2635d80d412a8df12e9929ff0b2e` |
| `SP\Ezek\author\repair2_step6\h1_lane_b\discharge.json` | `7748ca4bbccd2519292fadc618e71e4dccd087e3c676771cd33ec88d27d31447` |
| `SP\Ezek\repair2\step6\step6_divergence_half1.v1.json` | `e322181a2c62dfa363bb3dbe7f5898edf679af85e754936d6f91fff23e0a44a4` |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` |
| `SP\Ezek\repair2\step5\check_candidate_v5.py` | `c98a74d01aa5c7ed79f30b1e15fd23dd4896c2f8fab8641f247c8a8df768333c` |
| `SP\Ezek\repair2\step4\check_candidate_v4.py` | `9ef213b6c3c24ca15c9abc449ca30d72471d650cd29d67f083c4984be6846883` |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` |
| `SP\Ezek\tools\run_validator_suite.py` | `d7778f83eb0afff94a63dc7d8aad8ed7908b52bdaca4724b615f2fc30d35bf69` |
| `SP\Ezek\tools\check_register.py` | `2073135c343b5d89ef16e69599fc3c300c6d3fabb7aacddbcfe8200797380f22` |
| `SP\Ezek\tools\check_role_tokens.py` | `6fc5fb3ff5e35a99b0d132f42f842b99784bb0b5b86254c2f895732be1872d64` |
| `SP\Ezek\tools\role_tokens_phase.json` | `1a70b7a300486f361c9a793cdeb6ebd473b85519ed0b2a14515f99f1f35f94aa` |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |

## The gate

`python -B <SP>\Ezek\repair2\step5\check_candidate_v5.py C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step6_adjudication\h1\proposal.json --work C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step6_adjudication\h1\gate_work --discharge C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step6_adjudication\h1\adjudication.json --worklist <SP>\Ezek\repair2\step6\step6_worklist.v1.json`

Run it until ALL_CLEAN is true; report the completion measure (register flags left on the owed rows) beside it, and
account for every flag you leave with its reason.

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step6_adjudication\h1\proposal.json` - only changed prose fields, FULL new values.
2. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step6_adjudication\h1\adjudication.json` - per item the decision; per field the lane followed or the reconciled text and why;
   top-level `claim_accounting`, `gate` with the completion measure, `routed`, `what_i_could_not_verify`,
   `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. Escalate
rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts itself, a digest that
differs from the table.
