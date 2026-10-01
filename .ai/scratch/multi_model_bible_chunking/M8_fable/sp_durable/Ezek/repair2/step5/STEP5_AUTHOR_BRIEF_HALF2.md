# REPAIR-2 STEP 5 - THE REGISTER PROSE PASS. Author brief, HALF 2 (two blind lanes on this half)

You are ONE OF TWO BLIND LANES on half 2 (27 rows, 73 owed items); a Fable adjudicator reconciles you
with the other lane, whose work you never see. The other half has its own two lanes.

## What this step is - the ruling's own words govern

#e15 Q9(c): "Author work, not substitution, over the ~21 row-instances the lanes list (lane 01: 11 rows; lane 02: 10 rows, X1) plus every instance the new arms surface, plus the five grammatically broken sentences E13-86 repaired only for grammar (P06-009's twice-garbled sentence is the worst) — each field rewritten to state the substance, read back as English, then checked by the register member. The register member is run BEFORE the pass to fix its baseline and AFTER to prove the pass removed what it named without adding what the arms catch."

#e15 Q9(a), the rule you apply: "BARRED. Section 8 bars REFERENTS by class — decision-ids, strategy-file/section citations, erratum or repair narration, tool filenames, session/wave talk, staged-file names/stems, review actors — and the checker's patterns are a floor under that rule, not the rule. 'The division plan' refers to the strategy file; 'at its pinned digest', 'the pinned inventory', 'MEASURED from the section-mark record, kq' refer to staged files as objects; a key path names a file's internals; 'CUT-RULE', 'CONF-CAL', 'limb (b)', 'A9/A16', '#e14 Q2' are ruling ids; 'is withdrawn', 'CLASS CORRECTION, recorded not absorbed', 'the audit named this' are repair narration. All barred. Lane 02's uncertainty is answered: CUT-RULE and CONF-CAL are not sanctioned shorthand; section 8's one sanctioned shorthand is '(sweep: N verses)'. The line for evidence references: the row names the WITNESS and its layers — 'this witness records a samekh after MT 8:14, single witness', 'the K/Q apparatus at MT 33:13 reads …', 'the editors' note at MT 18:29' — and states counts with the sweep convention; it never names a record, census, plan, inventory, worklist, digest or key. OW-18 provenance survives: the tier word and the witness are stated; the FILE is not. The orchestrator's 30 register edits that introduced 'the division plan' are the orchestrator's defect and are undone in the prose pass by stating the rule's SUBSTANCE (section 13.2 of the brief already gives the pattern: 'a row under three verses is held only for a complete word-event unit')."

## A SUPERSESSION YOU MUST APPLY

`AUTHOR_WAVE_BRIEF.v1.md` section 13.2 once told authors to say "the section-mark record", "the verse census", "the
device census" and "the division plan" instead of file names. #e15 Q9(a) BARS those phrases: a row "never names a
record, census, plan, inventory, worklist, digest or key". Q9(a) governs; 13.2's substitution list does not. Name the
WITNESS and its layers ("this witness records a samekh after MT 8:14, single witness"; "the K/Q apparatus at MT 33:13
reads ..."; "the editors' note at MT 18:29"), state counts with the one sanctioned shorthand "(sweep: N verses)", and
state a method rule by its SUBSTANCE ("a row under three verses is held only for a complete word-event unit"), never
by its source. The rest of the author-wave brief is pinned only as the source of the rule substance it quotes.

## The owed items, by class (each item carries its data in your slices)

- **REG** - register flags on a field. Rewrite so the field states the substance and no flag remains. The substance of
  each barred id is in the rule-substance file, verbatim from the record that defines it: take only what the row's
  argument needs.
- **READBACK** - a field the orchestrator's own register, residue or grammar sweep edited and nobody read back. READ
  THE WHOLE FIELD AS ENGLISH. Repair what does not read (a doubled article, colliding substitutions, a dropped clause
  boundary, a paraphrase of a barred referent). If it reads correctly and bars nothing, it is NO_DEFECT with the
  sentence you read as evidence.
- **SPOT** - a spot lane's register finding; discharge it or show it is already gone.
- **ROUTED** - an earlier adjudication's routing to this step, verbatim; do what it names or STOP with evidence.
- **NEARFAR** - rejected-alternative prose that uses near and far in an older sense. Under clause 6 v2 a rival's near
  face is its candidate onset verse and its far face the verse behind it; reword so the prose and the tokens agree, or
  use wording that needs no face term. The refs are read-only here.
- **WEBQ** - a web_quotes flag. Five or more consecutive WEB words are a quotation whatever the delimiter and take
  double curly quotes and an in-field web: reference; a run that is nothing but the WEB's fixed rendering of a counted
  device is exempt (A6-b) - say so as NO_DEFECT. A case or apostrophe mismatch: quote the English exactly or quote
  fewer than five words.

## Rules for what you may write

- **Change no claim.** The gate extracts every face reference, verse number, Hebrew run, evidence-tier word, count and
  curly-quoted English from a row's prose; any that your rewrite removes must be ACCOUNTED FOR in discharge.json under
  `claim_accounting[row]` as `{"anchor": <exact string the gate prints>, "why": <barred referent removed | restated as
  ... | duplicate | moved to another field>}`. An unaccounted removal fails the gate.
- **Scope:** the prose fields of your rows only. No grade, span, identity, signals or refs change. If a rewrite would
  orphan a mirrored citation, keep the citation in the prose. HIGH rows are in scope for register rewrites and nothing
  else.
- **OW-18 survives:** the tier word and the witness are stated; the file is not. A mark, paseq or puncta mention keeps
  "single-witness". **Hebrew:** never hand-type it - SLICED from the witness or the live row. **Rotation:** do not
  template - no 7-gram in more than a handful of rows, at least 4 distinct formulations for a repeated statement.
- **The register rule:** a row is a scholar-facing record - no rule ids, ruling numbers, file or tool names,
  digests, review or wave talk, repair narration ("is withdrawn", "the earlier denial", "corrected here").
- **What a prose rewrite can break although the refs are read-only - the suite checks each:**
  DEF-A4-ARGUED - every argued citation in the prose stays mirrored by a refs entry carrying a ROLE token, so do not
  introduce an argued verse the refs do not carry; clause 6 v2 - the refs' face qualifier and seam pair on each
  WARRANT must still agree with what the prose says about near and far; the mark convention - a mark is recorded on
  the verse it FOLLOWS, and prose that restates a mark keeps that direction; C2-amended - a categorical claim you
  restate is unsourced only when absent from BOTH pinned inputs, so do not sharpen a claim into a universal the
  inputs do not carry; the zone - MT 21:1-5 = WEB 20:45-49 and MT 21:6-37 = WEB 21:1-32, and a verse in it that the
  prose names is written on BOTH faces, mapped by the offset map, never by arithmetic.
- **Read back as English:** every field you rewrite is read in full after your final edit; record `read_back: true`
  per item only after you have done it.

## Pinned inputs

| input | sha256 | what it is |
|---|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `2d7160f7d838d1c111791b6dc2e35b457d7899e4641a43371b1de99bd8eae422` | the live rows |
| `SP\Ezek\repair2\step5\step5_slices_half2.v1.json` | `432091f8f11d64189585eec1ed026a54749603218564aa6baf4303f2eda96dac` | YOUR ROWS: span, confidence, live prose, refs (read only), and the owed items as data |
| `SP\Ezek\repair2\step5\step5_worklist.v1.json` | `e46d0241cb9f42fd50172d25f0369e5aa41771c873b8f7d707e9c5d132a23f6e` | the whole worklist and the gate's scope |
| `SP\Ezek\repair2\step5\step5_rule_substance.v1.json` | `b309bcc9c9a03798b665da67cb8b7765254a4c566529c6cbb5ac929539551b9b` | the substance of every barred rule id, verbatim from the record that defines it |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` | the ruling: q9_section8_register governs this step |
| `SP\Ezek\ezek_controlling_agent_ruling_e12.v1.json` | `19ea3831e91481beb154061e36dcb81cfb3dc3da32e2c28c066aba56a2c512af` | the source of the A-class substance entries |
| `SP\Ezek\AUTHOR_WAVE_BRIEF.v1.md` | `31f58d77c318ef8e9d2b6c746f3de56ea39884d63650290f1e2765c453eaf5ad` | the source of CONF-CAL, CUT-RULE and A9/A16 substance; its 13.2 is SUPERSEDED in part (below) |
| `SP\Ezek\repair2\step5\check_candidate_v5.py` | `392f23aeb1a67f951ddb6ed64a0b27a5129582f2d3e03130211ea99b22cadbe1` | YOUR GATE (v5): claim accounting, English form, completion measure, the whole suite |
| `SP\Ezek\repair2\step4\check_candidate_v4.py` | `9ef213b6c3c24ca15c9abc449ca30d72471d650cd29d67f083c4984be6846883` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3_1.py` | `e4ab06227aaf974b2200454ee7b9eb865c365f5ed10b524ef48c926ccabc10f9` | imported by the gate |
| `SP\Ezek\repair2\step3\check_candidate_v3.py` | `5513efd8576de83bce47f43699045e0ca6d51195a0bae0aacd3485bb51edc71f` | imported by the gate |
| `SP\Ezek\repair2\step2_reconciliation\check_candidate_v2.py` | `dc87f57d0d5b7a41b8c2bfe42e65b878a78e5a547f33a1654dfb2b223be2d1a6` | imported by the gate |
| `SP\Ezek\repair2\suite_delta.py` | `e280bb7459a5b1e5576f2c8607685d6937b84fd2efe1253fd3b21805ca8195ac` | imported by the gate |
| `SP\Ezek\tools\run_validator_suite.py` | `d7778f83eb0afff94a63dc7d8aad8ed7908b52bdaca4724b615f2fc30d35bf69` | run by the gate |
| `SP\Ezek\tools\check_register.py` | `5106d1be66f3c7c860f98589b46ba52a5d5900cdb41251b54dd7021a7c06462d` | the register member, with the three arms #e15 Q9(b) ordered |
| `SP\Ezek\tools\check_role_tokens.py` | `6fc5fb3ff5e35a99b0d132f42f842b99784bb0b5b86254c2f895732be1872d64` | a hard member of the suite |
| `SP\Ezek\tools\role_tokens_phase.json` | `1a70b7a300486f361c9a793cdeb6ebd473b85519ed0b2a14515f99f1f35f94aa` | that member's pinned phase |
| `SP\Ezek\tools\check_refs_mirror.py` | `e34154c7d26b5a400765d2d4228b2ac635664a690e0e32af33359b6217ad1ced` | imported by the gate |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` | imported by the gate |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` | the English version by verse (for quotations) |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` | the Hebrew witness (WLC/OSHB) |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` | marks, K/Q, paseq, notes (single witness) |
| `SP\Ezek\ezek_device_inventory.v2.json` | `356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f` | the device census |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` | the WEB/MT map |

Pin rows for the pre-launch check:

| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `2d7160f7d838d1c111791b6dc2e35b457d7899e4641a43371b1de99bd8eae422` |
| `SP\Ezek\repair2\step5\step5_slices_half2.v1.json` | `432091f8f11d64189585eec1ed026a54749603218564aa6baf4303f2eda96dac` |
| `SP\Ezek\repair2\step5\step5_worklist.v1.json` | `e46d0241cb9f42fd50172d25f0369e5aa41771c873b8f7d707e9c5d132a23f6e` |
| `SP\Ezek\repair2\step5\step5_rule_substance.v1.json` | `b309bcc9c9a03798b665da67cb8b7765254a4c566529c6cbb5ac929539551b9b` |
| `SP\Ezek\ezek_controlling_agent_ruling_e15.v1.json` | `40bf0afbb8c6d5e51a130f639bff992fb2a86bbafe4903e92f668453866413a3` |
| `SP\Ezek\ezek_controlling_agent_ruling_e12.v1.json` | `19ea3831e91481beb154061e36dcb81cfb3dc3da32e2c28c066aba56a2c512af` |
| `SP\Ezek\AUTHOR_WAVE_BRIEF.v1.md` | `31f58d77c318ef8e9d2b6c746f3de56ea39884d63650290f1e2765c453eaf5ad` |
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

## Your gate - run it until the verdict is clean, and drive the completion measure down honestly

`python -B <SP>\Ezek\repair2\step5\check_candidate_v5.py <your dir>\proposal.json --work <your ABSOLUTE dir>\gate_work --discharge <your dir>\discharge.json`

It checks the per-row delta (no new register flag, unmirrored citation, orphan ref or mirror disagreement), the claim
accounting, new English-form problems, the WHOLE pinned suite with no hard member gaining a flag, and reports the
register flags left on the owed rows. Its English arm is a floor: it cannot see a doubled article across a noun or a
dropped clause boundary. Your reading can.

## Outputs - write early and rewrite at every stage (E-29); digest after the final write

1. `proposal.json` - `{"<row>": {"<field>": <full new value>}}`, only changed prose fields.
2. `discharge.json` - per item id (S5-nnn): `status` DISCHARGED | NO_DEFECT | STOP, `what_i_wrote` or `evidence`,
   `read_back`, `facts_reproduced` with tiers; top-level `claim_accounting`, `gate` (final verdict and completion
   measure), `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. Escalate
rather than write: any claim you believe false (that is not this step's repair), any grade you believe wrong, a
pinned input that contradicts itself, a digest that differs from the table.
