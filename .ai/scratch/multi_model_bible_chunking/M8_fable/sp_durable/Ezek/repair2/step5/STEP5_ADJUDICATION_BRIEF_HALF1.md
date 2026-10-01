# REPAIR-2 STEP 5 - ADJUDICATION OF TWO BLIND PROSE LANES, HALF 1 (Fable)

Attempt `ezek_repair2_step5_h1_adjudication_a1`, execution `ezek_repair2_step5_h1_adjudication_a1#e1`. You are
the controlling adjudicator (OW-13: Fable adjudicates). Two blind Opus lanes answered the same 61 owed items of
the register prose pass on this half; you produce ONE proposal. The other half has its own adjudicator.

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

- items whose statuses differ: 4; items missing from a discharge: A 0, B 0
- fields only lane A changed: 2; only lane B: 2; both changed differently: 15; identically: 10
- stops: lane A 1, lane B 2

The full lists are in the pinned divergence file. A field only one lane changed is a question in itself: was the other
lane right to leave it (NO_DEFECT), or did it miss an owed item?

## Rules - the lanes' brief is pinned and binds you identically

State substance, never a barred referent: no rule ids, ruling numbers, file or tool names, digests, record, census,
plan, inventory, worklist or key names, review or wave talk, repair narration. The register rule: a row is a
scholar-facing record. Name the witness and its layers; "(sweep: N verses)" is the one sanctioned count shorthand.
Change no claim; no grade, span, identity, signals or refs change. "single-witness" on any mark, paseq or puncta
mention; a mark is recorded on the verse it FOLLOWS; never hand-type Hebrew - SLICED from the witness or the live row;
five or more WEB words take double curly quotes and a web: reference, a counted device's fixed rendering is exempt
(A6-b); C2-amended - unsourced means absent from BOTH pinned inputs; DEF-A4-ARGUED - every argued citation stays
mirrored by a refs entry with a ROLE token, whose face qualifier and seam pair must still agree with the prose; the
zone - MT 21:1-5 = WEB 20:45-49 - on BOTH faces; rotation - no 7-gram in more than a handful of rows, at least 4
distinct formulations.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `2d7160f7d838d1c111791b6dc2e35b457d7899e4641a43371b1de99bd8eae422` | the live rows |
| `SP\Ezek\repair2\step5\step5_slices_half1.v1.json` | `8d9547dd652154a0ad0555329b6f69d8194d5bbe03427bdee5497dc46d6f9372` | this half's rows, prose and owed items |
| `SP\Ezek\repair2\step5\step5_worklist.v1.json` | `e46d0241cb9f42fd50172d25f0369e5aa41771c873b8f7d707e9c5d132a23f6e` | the worklist and the gate's scope |
| `SP\Ezek\repair2\step5\step5_rule_substance.v1.json` | `b309bcc9c9a03798b665da67cb8b7765254a4c566529c6cbb5ac929539551b9b` | the substance of every barred rule id, verbatim |
| `SP\Ezek\repair2\step5\STEP5_AUTHOR_BRIEF_HALF1.md` | `b8131d50c53d628a2ceb62d6e335e27b590b404c6a24dd314a46dae05abcfcbf` | the brief both lanes held; its rules bind you identically |
| `SP\Ezek\author\repair2_step5\h1_lane_a\proposal.json` | `2b9f3738f9f4457bc2dd8df5e7137c031ff254e42168689614eb20353085d0b2` | blind lane A - proposal |
| `SP\Ezek\author\repair2_step5\h1_lane_a\discharge.json` | `1d9ce13375d8d55f5c13511efe2b632c9694200fc5f37ad2bb77c503e262c02c` | blind lane A - per-item discharge and claim accounting |
| `SP\Ezek\author\repair2_step5\h1_lane_b\proposal.json` | `368458f486ae31e89951f6f3712823ccbb50093f45be9eb949dd2b8622e86679` | blind lane B - proposal |
| `SP\Ezek\author\repair2_step5\h1_lane_b\discharge.json` | `74363b8d750ebfec2fbc1660b0fe628e6bf9a3f5e6313e706628ff6459954018` | blind lane B - per-item discharge and claim accounting |
| `SP\Ezek\repair2\step5\step5_divergence_half1.v1.json` | `33ed7151949bb2b04099a6d939c30878e1febe009533273ae8ca0c9e9dd5c8d5` | where the lanes diverge, computed from their files (a map, not a reading) |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | the ruling: q9_section8_register governs |
| `SP\Ezek\repair2\step5\check_candidate_v5.py` | `392f23aeb1a67f951ddb6ed64a0b27a5129582f2d3e03130211ea99b22cadbe1` | YOUR GATE (v5) |
| `SP\Ezek\repair2\step4\check_candidate_v4.py` | `9ef213b6c3c24ca15c9abc449ca30d72471d650cd29d67f083c4984be6846883` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` | imported by the gate |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` | imported by the gate |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` | imported by the gate |
| `SP\Ezek\tools\run_validator_suite.py` | `d7778f83eb0afff94a63dc7d8aad8ed7908b52bdaca4724b615f2fc30d35bf69` | run by the gate |
| `SP\Ezek\tools\check_register.py` | `5106d1be66f3c7c860f98589b46ba52a5d5900cdb41251b54dd7021a7c06462d` | the register member |
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

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `2d7160f7d838d1c111791b6dc2e35b457d7899e4641a43371b1de99bd8eae422` |
| `SP\Ezek\repair2\step5\step5_slices_half1.v1.json` | `8d9547dd652154a0ad0555329b6f69d8194d5bbe03427bdee5497dc46d6f9372` |
| `SP\Ezek\repair2\step5\step5_worklist.v1.json` | `e46d0241cb9f42fd50172d25f0369e5aa41771c873b8f7d707e9c5d132a23f6e` |
| `SP\Ezek\repair2\step5\step5_rule_substance.v1.json` | `b309bcc9c9a03798b665da67cb8b7765254a4c566529c6cbb5ac929539551b9b` |
| `SP\Ezek\repair2\step5\STEP5_AUTHOR_BRIEF_HALF1.md` | `b8131d50c53d628a2ceb62d6e335e27b590b404c6a24dd314a46dae05abcfcbf` |
| `SP\Ezek\author\repair2_step5\h1_lane_a\proposal.json` | `2b9f3738f9f4457bc2dd8df5e7137c031ff254e42168689614eb20353085d0b2` |
| `SP\Ezek\author\repair2_step5\h1_lane_a\discharge.json` | `1d9ce13375d8d55f5c13511efe2b632c9694200fc5f37ad2bb77c503e262c02c` |
| `SP\Ezek\author\repair2_step5\h1_lane_b\proposal.json` | `368458f486ae31e89951f6f3712823ccbb50093f45be9eb949dd2b8622e86679` |
| `SP\Ezek\author\repair2_step5\h1_lane_b\discharge.json` | `74363b8d750ebfec2fbc1660b0fe628e6bf9a3f5e6313e706628ff6459954018` |
| `SP\Ezek\repair2\step5\step5_divergence_half1.v1.json` | `33ed7151949bb2b04099a6d939c30878e1febe009533273ae8ca0c9e9dd5c8d5` |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` |
| `SP\Ezek\repair2\step5\check_candidate_v5.py` | `392f23aeb1a67f951ddb6ed64a0b27a5129582f2d3e03130211ea99b22cadbe1` |
| `SP\Ezek\repair2\step4\check_candidate_v4.py` | `9ef213b6c3c24ca15c9abc449ca30d72471d650cd29d67f083c4984be6846883` |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` |
| `SP\Ezek\tools\run_validator_suite.py` | `d7778f83eb0afff94a63dc7d8aad8ed7908b52bdaca4724b615f2fc30d35bf69` |
| `SP\Ezek\tools\check_register.py` | `5106d1be66f3c7c860f98589b46ba52a5d5900cdb41251b54dd7021a7c06462d` |
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

`python -B <SP>\Ezek\repair2\step5\check_candidate_v5.py C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step5_adjudication\h1\proposal.json --work C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step5_adjudication\h1\gate_work --discharge C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step5_adjudication\h1\adjudication.json`

Run it until ALL_CLEAN is true; report the completion measure (register flags left on the owed rows) beside it, and
account for every flag you leave with its reason.

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step5_adjudication\h1\proposal.json` - only changed prose fields, FULL new values.
2. `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step5_adjudication\h1\adjudication.json` - per item the decision; per field the lane followed or the reconciled text and why;
   top-level `claim_accounting`, `gate` with the completion measure, `routed`, `what_i_could_not_verify`,
   `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. Escalate
rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts itself, a digest that
differs from the table.
