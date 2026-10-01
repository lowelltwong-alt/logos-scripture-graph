# REPAIR-2 STEP 6 - THE TRANSPORT BATCH AND THE ROUTED REPAIRS. Author brief, HALF 2 (two blind lanes)

You are ONE OF TWO BLIND LANES on half 2; a Fable adjudicator reconciles you with the other lane, whose work
you never see. The other half has its own two lanes. Your half: 23 rows, 43 owed items: A16 5, ONSET5 1, REG6 19, REL03 2, REL10 1, ROUTED5 13, STALE20 2.
Some classes below may have no item in your half.

## What this step executes - #e15 Q8, carried verbatim in the substance file

The transport class is what its STATED predicate defines: 33 verses / 46 occurrences, a strict superset of an older
closed list of 20. The orchestrator ran every membership two ways before issuing an item - the census list and an
independent scan of the witness bytes with the stated predicate - and both agree book-wide (33/33; recognition family
64/64, 2mp 21/21, 2fp 2/2). The results travel with each item as data; you rely on them, and re-derive any you doubt.

- **REL10** - peer_10's four transport rows, held while the class was undefined. Each verse IS a member. A reading
  that depended on its being inside the class stands; one that depended on its being outside fails. The row may name
  the verse a transport verse of the counted class, stated as "(sweep: 33 verses / 46 occurrences)".
- **REL03** - peer_03's four findings resting on recognition memberships that now have pinned lists. Score each
  finding against the row AS IT STANDS NOW: repair what still stands; NO_DEFECT with evidence where an earlier repair
  already cured it.
- **A16** - seven interior transport verses are now licensed rivals and must be WEIGHED: the strongest rival stays in
  the rejected-alternative field; any further live candidate is disclosed in one clause of device_notes as weighed and
  not taken, naming the device, with the guard or ground that holds the row ("a row under three verses is held only
  for a complete word-event unit" is the over-split guard's substance). A weighing is argued, so its verse is
  mirrored by a refs entry: `[WARRANT-rival:near]` or `:far` with the seam pair as the annotation's first token.
- **A16-DISCLOSE** - the ruling carries MT 37:2 to a disclosure (a one-verse remainder): confirm the row discloses it
  as a device the boundary does not rest on (`[DISCLOSURE-device]`); weigh nothing.
- **ONSET5** - five rows whose onset verse is a transport verse MAY name that licensed driver (with a
  `[WARRANT-onset:near]` entry if it is argued). Optional: NO_DEFECT is complete where naming adds nothing.
- **STALE20** - a "20" figure for the transport class; correct it to the counted class.
- **REG6** - a register flag on any row: state the substance the flagged words point at and name the witness and its
  layers ("this witness", "the K/Q apparatus at MT 33:13") instead of a record, file, list label or classification
  label; "(sweep: N verses)" is the one sanctioned count shorthand. Change no claim.
- **ROUTED5** - what the register prose pass's adjudicators routed onward: a claim two authors or an adjudicator
  measured false outside that pass, or a repair that sat in a refs entry the pass held read-only. The routed entry
  travels verbatim. RE-MEASURE before writing: repair what reproduces (the smallest change that makes the claim true),
  NO_DEFECT with evidence what does not, STOP what needs a ruling. A repair here is a claim correction, so account
  for every anchor it removes exactly as for any other edit.

**No grade moves in this step.** If a weighing makes you believe a confidence limb rises or falls, record it as an
observation for the confidence audit; never write it.

## Rules for what you may write

- **Change no claim beyond an item's order.** The gate extracts every face reference, verse number, Hebrew run,
  evidence-tier word, count and curly-quoted English from a row's prose; anything your edit removes must be ACCOUNTED
  FOR in discharge.json under `claim_accounting[row]` as `{"anchor": <exact string the gate prints>, "why": ...}`.
- **Refs:** you may ADD or re-gloss the entries an item needs; each new entry takes a ROLE token and, on a WARRANT,
  a verified face qualifier (and a seam pair on a rival). DEF-A4-ARGUED: every argued citation is mirrored by a refs
  entry carrying a ROLE token. MT-borne devices sit on the oshb: face; English quotations on the web: face.
- **Quotations:** five or more consecutive WEB words are a quotation whatever the delimiter and take double curly
  quotes and an in-field web: reference; a run that is nothing but the WEB's fixed rendering of a counted device is
  exempt (A6-b).
- **The mark convention:** a mark is recorded on the verse it FOLLOWS. A mark, paseq or puncta mention carries
  "single-witness". **Hebrew:** never hand-type it - SLICED from the witness or the live row. **Categorical claims:**
  C2-amended - unsourced means absent from BOTH pinned inputs. **The zone:** MT 21:1-5 = WEB 20:45-49 and MT 21:6-37 =
  WEB 21:1-32; an entry touching it is written on BOTH faces, mapped by the offset map. **Rotation:** no 7-gram in
  more than a handful of rows, at least 4 distinct formulations for repeated statements - seven weighings must not
  read as one template.
- **The register rule:** a row is a scholar-facing record - no rule ids, ruling numbers, file or tool names,
  digests, record/census/plan/inventory names, review or wave talk, repair narration. State substance; name the
  witness and its layers; "(sweep: N verses)" is the one sanctioned count shorthand. **Read back as English** every
  field you change, after your final edit, and record `read_back: true` per item only then.
- No grade, span, identity or signals change. A false only-ground is a STOP, never a substitution.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `a2e51d689bcb8e656ece9e657521407facf5eeecd67cbf06d4214ef2e8dd601f` | the live rows |
| `SP\Ezek\repair2\step6\step6_slices_half2.v1.json` | `fab58a4ecec9f33a184fceca1e36a12d533b39923ab9738686686fbab2a4d8ef` | YOUR ROWS: span, confidence, prose, refs, the owed items with their distinct checks as data |
| `SP\Ezek\repair2\step6\step6_worklist.v1.json` | `bd03f40a67079fd27efef62dec971cbcac4b8c7a7932e46357df7ef4d90a919d` | the worklist and the gate's scope |
| `SP\Ezek\repair2\step6\step6_substance.v1.json` | `5e6dff35eb7adbc8201bac6a8816281d2bff5b85607ae46e64dc86ec1058f9c7` | the substance you apply, verbatim from the records that define it |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | the ruling (q8_transport_class governs this step) |
| `SP\Ezek\ezek_controlling_agent_ruling_e12.v1.json` | `19ea3831e91481beb154061e36dcb81cfb3dc3da32e2c28c066aba56a2c512af` | the source of A12 and A16 |
| `SP\Ezek\AUTHOR_WAVE_BRIEF.v1.md` | `31f58d77c318ef8e9d2b6c746f3de56ea39884d63650290f1e2765c453eaf5ad` | the source of the weighing duty, CUT-RULE and CONF-CAL substance |
| `SP\Ezek\repair2\step5\check_candidate_v5.py` | `c98a74d01aa5c7ed79f30b1e15fd23dd4896c2f8fab8641f247c8a8df768333c` | YOUR GATE (v5, run with the step-6 worklist) |
| `SP\Ezek\repair2\step4\check_candidate_v4.py` | `9ef213b6c3c24ca15c9abc449ca30d72471d650cd29d67f083c4984be6846883` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` | imported by the gate |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` | imported by the gate |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` | imported by the gate |
| `SP\Ezek\tools\run_validator_suite.py` | `d7778f83eb0afff94a63dc7d8aad8ed7908b52bdaca4724b615f2fc30d35bf69` | run by the gate |
| `SP\Ezek\tools\check_register.py` | `2073135c343b5d89ef16e69599fc3c300c6d3fabb7aacddbcfe8200797380f22` | the register member |
| `SP\Ezek\tools\check_role_tokens.py` | `6fc5fb3ff5e35a99b0d132f42f842b99784bb0b5b86254c2f895732be1872d64` | the hard member that verifies every face qualifier and seam pair |
| `SP\Ezek\tools\role_tokens_phase.json` | `1a70b7a300486f361c9a793cdeb6ebd473b85519ed0b2a14515f99f1f35f94aa` | that member's pinned phase |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` | imported by the gate |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` | imported by the gate |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, K/Q, paseq, notes (single witness) |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | the device census |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT map |
| `SP\Ezek\reviews\peer_10.json` | `99e493068246bf75c4d3980492a678270f80941e502c7e5f1dbaf961616c0db6` | peer_10's own words on its four held rows |
| `SP\Ezek\reviews\peer_03.json` | `a32d8f8919af2c233c10702625f77d862d523f8816f3442eb569b8e294194197` | peer_03's own words and per-row readings |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `a2e51d689bcb8e656ece9e657521407facf5eeecd67cbf06d4214ef2e8dd601f` |
| `SP\Ezek\repair2\step6\step6_slices_half2.v1.json` | `fab58a4ecec9f33a184fceca1e36a12d533b39923ab9738686686fbab2a4d8ef` |
| `SP\Ezek\repair2\step6\step6_worklist.v1.json` | `bd03f40a67079fd27efef62dec971cbcac4b8c7a7932e46357df7ef4d90a919d` |
| `SP\Ezek\repair2\step6\step6_substance.v1.json` | `5e6dff35eb7adbc8201bac6a8816281d2bff5b85607ae46e64dc86ec1058f9c7` |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` |
| `SP\Ezek\ezek_controlling_agent_ruling_e12.v1.json` | `19ea3831e91481beb154061e36dcb81cfb3dc3da32e2c28c066aba56a2c512af` |
| `SP\Ezek\AUTHOR_WAVE_BRIEF.v1.md` | `31f58d77c318ef8e9d2b6c746f3de56ea39884d63650290f1e2765c453eaf5ad` |
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
| `SP\Ezek\reviews\peer_10.json` | `99e493068246bf75c4d3980492a678270f80941e502c7e5f1dbaf961616c0db6` |
| `SP\Ezek\reviews\peer_03.json` | `a32d8f8919af2c233c10702625f77d862d523f8816f3442eb569b8e294194197` |

## Your gate

`python -B <SP>\Ezek\repair2\step5\check_candidate_v5.py <your dir>\proposal.json --work <your ABSOLUTE dir>\gate_work --discharge <your dir>\discharge.json --worklist <SP>\Ezek\repair2\step6\step6_worklist.v1.json`

It checks the per-row delta, the claim accounting, new English-form problems, the entry form of every added refs
entry (clause 6 v2 qualifiers included), and the WHOLE pinned suite - including the hard role_tokens member, which
verifies every face qualifier and seam pair - with no hard member allowed to gain a flag.

## Outputs - write early and rewrite at every stage (E-29); digest after the final write

1. `proposal.json` - `{"<row>": {"<field>": <full new value>}}`, only changed fields; refs as FULL lists.
2. `discharge.json` - per item id (S6-nnn): `status` DISCHARGED | NO_DEFECT | STOP, `what_i_wrote` or `evidence`,
   `read_back`, `facts_reproduced` with tiers; top-level `claim_accounting`, `confidence_observations`, `gate`,
   `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. Escalate
rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts itself, a digest that
differs from the table.
