# REPAIR-2 STEP 4c - THE AUTHOR VOCABULARY BATCH. Author brief (two blind lanes)

You are ONE OF TWO BLIND LANES; a Fable adjudicator reconciles you with the other lane, whose work you never see.

## What this step installs

#e15 Q5 amended the argued-citation definition ("clause 6 v2", carried verbatim in the slices): the layer that
records warrants must be able to say WHICH FACE of a seam a warrant sits on, because the confidence scale is about
faces. A mechanical sweep has already given 124 onset and close warrants their derived face qualifier. What is left
needs a reader: 103 owed items on 64 rows - 75 WARRANT-rival tokens that need a SEAM PAIR and a face
qualifier, 5 onset/close warrants the geometry could not qualify (three in the renumbering zone, two interior
without a device word), two ANCHOR absences to re-tokenise, two device entries the census does not support, and the
re-face and re-gloss items the rulings and the earlier adjudications carried to this step.

## Clause 6 v2, and one worked example per token

A **face qualifier** is ':near' (the seam verse INSIDE the unit the seam bounds - the row's first verse for its onset,
its last verse for its close, the candidate onset verse for a rival), ':far' (the adjacent verse ACROSS the seam), or
':interior' (an in-span verse a warrant rests on that is neither - for onset and close only when the annotation names
the device). The hard role_tokens member DERIVES the face for onset and close from verse and span and FAILS LOUD on a
mismatch; for a rival it checks the SEAM PAIR.

- `oshb:Ezek.33.10 [WARRANT-onset:near] ve'attah re-address opens the unit` - the row's first verse
- `oshb:Ezek.33.20 [WARRANT-onset:far] pe-marked close behind the dateline` - the verse before the first verse
- `oshb:Ezek.24.24 [WARRANT-close:interior] sign formula partner of the close` - in span, device named
- `oshb:Ezek.33.12 [WARRANT-rival:near] 33.11/33.12 ve'attah same audience unlicensed` - the annotation's FIRST token is
  the seam pair (two adjacent verses, dotted); the rival's candidate onset verse is :near, the verse behind it :far
- `oshb:Ezek.40.38 [WARRANT-absence] no formula mark K/Q or paseq here` - the boundary RESTS on the absence
- `oshb:Ezek.41.9 [DISCLOSURE-absence] census records no stroke here` - recorded, the boundary does not rest on it
- `oshb:Ezek.8.14 [DISCLOSURE-mark] samekh on this verse single-witness` - a mark (recorded on the verse it FOLLOWS)
- `oshb:Ezek.33.13 [DISCLOSURE-kq] ketiv and qere recorded here`, `[DISCLOSURE-paseq]`, `[DISCLOSURE-note]` likewise
- `oshb:Ezek.21.14 [DISCLOSURE-device] in-span messenger short form` - an inventoried device the boundary does not rest on
- `web:Ezek.11.13 [QUOTE] Pelatiah's death and the cry` - an English quotation, on the web: face
- `oshb:Ezek.37.9 [ANCHOR] the four winds content only` - a content statement the boundary does not rest on

**The three cases an earlier lane found divergent, decided:** (1) a verse with neither device nor mark that the
rationale RESTS on is a WARRANT with :near or :far and its ground named - content is a warrant when the rationale
rests on it; (2) an inventoried device the boundary does NOT rest on is DISCLOSURE-device, never ANCHOR; (3) a device
the census does NOT record is never DISCLOSURE-device - it is ANCHOR, or WARRANT-absence / DISCLOSURE-absence for a
true absence.

## Rules for what you may write

- **Change only what an owed item names.** Qualify, re-token, re-face or re-gloss the named entries. A prose sentence
  may change only where an item's order names it (a re-gloss that the rationale must match). No grade, span, identity
  or signals changes. A false only-ground is a STOP, never a substitution.
- **Read the seam pair off the row.** A rival's seam is where the rejected alternative would cut - read it from the
  strongest_rejected_alternative field and the rationale, and check it against the bytes. If the row does not let you
  determine it, STOP with the evidence.
- **Faces:** MT-borne devices and formula memberships on the oshb: face; English quotations on the web: face. **The
  zone:** MT 21:1-5 = WEB 20:45-49 and MT 21:6-37 = WEB 21:1-32 - an entry touching it is written on BOTH faces,
  `web:... = oshb:...`, mapped by the offset map, never by arithmetic.
- **Annotations** are one to six words (seven when a rival's first word is its seam pair). DEF-A4-ARGUED: every argued
  citation stays mirrored by an entry carrying a ROLE token. A mark, paseq or puncta mention carries "single-witness".
- **Hebrew:** never hand-type Hebrew - SLICED from `Ezek_oshb.txt` or the live row. **English:** five or more WEB words
  take double curly quotes and a web: reference (A6-b exempts a named formula rendering). **Categorical claims:**
  C2-amended - unsourced means absent from BOTH pinned inputs. **The register rule:** a row is a scholar-facing record -
  no rule ids, ruling numbers, file or tool names, digests, review or wave talk, repair narration. **Rotation:** no
  7-gram in more than a handful of rows, at least 4 distinct formulations for repeated statements.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `32f33f05e8adb185027b278813537b8b466f58a7a82eabad186e5ad72dcf398e` | the live rows after step 4a |
| `SP\Ezek\repair2\step4\step4c_slices.v1.json` | `dd25e38b14e22b1525803f9899f542dc9f55f8d28f41d337cab7374d7bf22d5b` | per row: span, prose, refs, owed items; clause 6 v2 verbatim |
| `SP\Ezek\repair2\step4\step4c_worklist.v1.json` | `40036cc483f451e10e650dedf9cbc87a1e732828cefbcdedb07c38f5b7fc7d12` | the worklist and the gate's scope |
| `SP\Ezek\repair2\step4\check_candidate_v4.py` | `9ef213b6c3c24ca15c9abc449ca30d72471d650cd29d67f083c4984be6846883` | YOUR GATE - form, delta checks, the whole suite, and the completion measure |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` | imported by the gate |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` | imported by the gate |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` | imported by the gate |
| `SP\Ezek\tools\run_validator_suite.py` | `d7778f83eb0afff94a63dc7d8aad8ed7908b52bdaca4724b615f2fc30d35bf69` | run by the gate - now with the hard role_tokens member |
| `SP\Ezek\tools\check_role_tokens.py` | `6fc5fb3ff5e35a99b0d132f42f842b99784bb0b5b86254c2f895732be1872d64` | the member that verifies every face qualifier and seam pair |
| `SP\Ezek\tools\role_tokens_phase.json` | `1a70b7a300486f361c9a793cdeb6ebd473b85519ed0b2a14515f99f1f35f94aa` | the member's pinned phase |
| `SP\Ezek\tools\check_register.py` | `5106d1be66f3c7c860f98589b46ba52a5d5900cdb41251b54dd7021a7c06462d` | imported by the gate |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` | imported by the gate |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` | imported by the gate |
| `SP\Ezek\verse_inventory.json` | `7314690191ec380b25578ca33d4745f4e60196b9f0e1dda4a1bcc9286c19cf54` | per-chapter verse counts on the WEB face (for the verse across a chapter seam) |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, K/Q, paseq, notes (single witness) |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | the device census |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT map |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | the ruling whose clause 6 v2 you install |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `32f33f05e8adb185027b278813537b8b466f58a7a82eabad186e5ad72dcf398e` |
| `SP\Ezek\repair2\step4\step4c_slices.v1.json` | `dd25e38b14e22b1525803f9899f542dc9f55f8d28f41d337cab7374d7bf22d5b` |
| `SP\Ezek\repair2\step4\step4c_worklist.v1.json` | `40036cc483f451e10e650dedf9cbc87a1e732828cefbcdedb07c38f5b7fc7d12` |
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

## Your gate - run it until the verdict is clean, and drive the completion measure to zero

`python -B <SP>\Ezek\repair2\step4\check_candidate_v4.py <your dir>\proposal.json --work <your ABSOLUTE dir>\gate_work`

It checks entry form and the flags your proposal introduces, runs the WHOLE pinned suite - including the hard
role_tokens member, which verifies every qualifier and seam pair - and then reports the warrants still unqualified on
your candidate. Use an ABSOLUTE --work path. Run no validator any other way.

## Outputs - write early and rewrite at every stage (E-29); digest after the final write

1. `proposal.json` - `{"<row>": {"<field>": <full new value>}}`, only changed fields; refs as FULL lists.
2. `discharge.json` - per item id (S4-nnn): `status` DISCHARGED | NO_DEFECT | STOP, `what_i_wrote` or `evidence`,
   `facts_reproduced` with tiers; top-level `gate` (the final verdict and the completion measure),
   `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. Escalate
rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts itself, a digest that
differs from the table.
