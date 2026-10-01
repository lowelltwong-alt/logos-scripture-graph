# WRITER BRIEF — draft chunk rows, Ezekiel, m8-mesh-r3 (OW-6b hard-book track; OW-1..OW-10)

You are one of ELEVEN part-writers in the M8_fable Ezekiel cycle — candidate-only, NON-AUTHORIZING,
adversarially reviewed research. Your launch message gives: part id (pNN), WEB verse range, verse count,
parent(s), attempt id, execution id, output filename. This brief is binding for everything else.

## E-19 — the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** `SP\Ezek\writer\` already exists — write your deliverable directly to the exact
filename your launch message names; **never run any existence check, listing, glob or recursive search against it
or any other directory.**

**EXACT-PATH LAW:** every path you may read is named below. Open those, by exact path. No directory listing, no
glob, no recursive search, no "looking around". Scope any self-check to YOUR OWN private scratch. State
affirmatively in your final message that you ran no listing and no glob.

## PATHS (absolute; lesson-c hygiene)

- Toolkit (**READ FIRST**): `SP\Ezek\tools\TOOLKIT.md` — book facts + hazard catalog. USE the staged tools; never rebuild them.
- Strategy (**BINDING**): `SP\Ezek\book_strategy_Ezek.md` — §5 parents, §6 unit_type + granularity, §7 low-confidence, §8 register
- Text: `SP\Ezek\Ezek_oshb.txt` (MT, `ref<TAB>text`), `SP\Ezek\Ezek_web_clean.txt` (WEB)
- Inventories: `SP\Ezek\ezek_device_inventory.json`, `SP\Ezek\pmarks_Ezek.json`, `SP\Ezek\web_mt_offset_map.json`, `SP\Ezek\verse_inventory.json`, `SP\Ezek\writer_parts.json`
- Reconciliations you MUST read: `SP\Ezek\ezek_denominator_reconciliation.v1.json`, `SP\Ezek\ezek_p0_retained_lows.v1.json`
- Tools present in `SP\Ezek\tools\`: **`TOOLKIT.md` only** (plus `_toolkit_selfcheck.py`, which is the
  orchestrator's, not yours). The shared Jer/Isa validator toolchain is **NOT staged for Ezekiel** — see the
  self-check section below. Do not go looking for it: another book's tools operate on another book's data.

**GOVERNANCE:** the worktree `C:\wt\logos-t423-m8-fable` is a gated lane — read-only; never write into it, never
write a receipt, never run git. Your ONLY SP write is your one deliverable. Private scratch goes in a
uniquely-named subdirectory of YOUR OWN session scratchpad — never in `SP\Ezek`, never at any scratchpad root, and
**no debug files anywhere under SP**, including during self-check (run the validator over a PRIVATE COPY of your
deliverable so its report never lands under SP).

**FORBIDDEN LANES:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol`, or
`comparison\`; and every other book's lane under SP. Never read another model's output; never seek convergence.

---

## CRITICAL BOOK FACTS

**1. NUMBERING IS NOT IDENTITY — one offset zone (byte-proven, corroborated 37/37 by the OSHB's own KJV layer):**

```
MT 21:1-5    =  WEB 20:45-49
MT 21:6-37   =  WEB 21:1-32
identity in every other chapter
```

**TIER-0: any structured ref touching WEB 20:45-49, WEB ch 21, or MT ch 21 MUST carry an explicit dual or numeric
qualifier** — `web:Ezek.20.45 = oshb:Ezek.21.1`, or `(MT 21:1)` after a `web:` ref. Bare coordinates are ambiguous
there and **only** there. Row spans and bare/`web:` refs are WEB; `oshb:`/pmarks are MT. Convert with
`web_mt_offset_map.json` — never hand-assume. **p04 contains the entire zone.**

**2. HEBREW THROUGHOUT.** Morph prefixes are H across 18,866 tokens; there is no Aramaic island. An Aramaic label
anywhere in Ezekiel is a hard error.

**3. THE FRAME SPINE is the tier-1 seam skeleton.** Consume `ezek_device_inventory.json`; do NOT re-derive.
Onsets: the **14 oracle datelines** (MT 1:1, 1:2, 8:1, 20:1, 24:1, 26:1, 29:1, 29:17, 30:20, 31:1, 32:1, 32:17,
33:21, 40:1), the word-event formula, hand-of-YHWH (7), "set your face" (9), "and you, son of man".
Closes: the recognition formula (28 + 5 second-person), the utterance formula (81), "I YHWH have spoken" (14).

- **A REFRAIN CLOSES A UNIT.** A recognition or utterance formula belongs to the unit **BEFORE** it, not the one
  after. This is owner-ruled and not negotiable.
- **A SEAM IS ASSESSED FROM BOTH SIDES.** An onset-only diagnosis is incomplete until the adjacent unit's close is
  weighed from bytes. Say what you weighed on both sides.
- These are **evidence, not verdicts**. No boundary is set by a formula count alone, and tier-4 translation
  punctuation or editorial headings never drive one at all (E-23).

**4. THREE WORD-EVENT DENOMINATORS, NEVER BLENDED.** Read `ezek_denominator_reconciliation.v1.json` before you
cite any of them.

| count | predicate |
|---|---|
| **39** | `ויהי דבר יהוה אלי לאמר` strict, אלי and לאמר adjacent |
| **41** | `ויהי דבר יהוה אלי` allowing an infixed temporal phrase (adds MT 12:8, 24:1) |
| **48** | the whole FIRST-PERSON family: 41 + the 7 perfect `היה` verses |
| **49** | `דבר יהוה אל` in ANY form — the 48 plus **MT 1:3 only**, the superscription `הָיֹה הָיָה דְבַר יְהוָה אֶל יְחֶזְקֵאל` (infinitive absolute, third-person addressee) |

Quoting one where another is meant is a hard error. **MT 1:3 is a real onset** — excluded from 48 by predicate,
not by judgment — and p01 must weigh it.

**5. DATE FORMULAE THAT OPEN NOTHING.** MT **45:18**, 45:20, 45:21, 45:25 are festival-calendar dates inside the
temple law. **45:18 is the trap**: it carries a full month+day formula *and* the messenger formula. Reading any of
the four as a unit onset puts a false boundary inside a law block.

**6. MARKS.** 113 samekh + 71 pe = 184 occurrences over 183 verses (**MT 43:27 carries two**). Masoretic paragraph
evidence: it informs a boundary, never decides one alone, and is disclosed single-witness at every span-relevant
verse. **Chapters 10, 40, 41 and 42 carry no marks at all** — the stretch MT 40:1-43:8 is 103 unmarked verses, so
p10 argues its seams without parashah corroboration anywhere.

**7. HAZARD FLAGSHIPS** (read the full TOOLKIT catalog before ANY digit):
- **Paseq is COUNT-ONLY** (136 over 121 verses). An intra-verse position claim is unsourceable from the extract.
- **K/Q: 134 notes over 99 verses, 23 doubled.** Eleven doubled verses sit in ch 40 — the disputed forms are
  frequently the temple **measurements themselves**. Check `pmarks kq` BEFORE counting or slicing in any K/Q verse.
- **71 verses carry OSHB editorial notes** — single-witness apparatus. **MT 33:20 has no sof-pasuq**, standing
  instead with a punctuation note and a pe.
- **Puncta extraordinaria are IN the verse bytes**: U+05C4, five at MT 41:20, seven at MT 46:22. A row splicing
  either carries them; that is source-true, not degradation.
- **FABRICATION CLASSES** (byte-swept, absence proven): no selah, no large or small letters, no reversed nun, no
  suspended letter. A claim of any of these is a fabrication.
- **The extract carries NO maqaf, NO paseq, NO sof-pasuq and no morpheme `/`.** A pattern written with them
  matches nothing, and "absent from the text" would be a claim about the extract, not the source.
- **Never quote Hebrew from TOOLKIT.md or the strategy** — their Hebrew is citation form. Row bytes come from
  `Ezek_oshb.txt`, always.

---

## TASK

Tile your assigned WEB range **EXACTLY** — no gaps, no overlaps; verify with
`tools\check_tiling.py <file> --range <your range>` — into chunk rows per the strategy:

- **§5 parents.** Rows NEVER straddle a parent seam, and never straddle a **hard seam** (any of the 14 datelines,
  any vision onset). If your launch message names an INTERNAL PARENT SEAM inside your part, a row stops there.
- **§6 unit_type** — the closed 12-value vocabulary: `vision_report`, `commission_narrative`, `sign_act`,
  `judgment_oracle`, `oracle_against_nation`, `lament_qinah`, `parable_allegory`, `disputation_oracle`,
  `salvation_oracle`, `temple_measurement`, `temple_law`, `land_allotment`. Operative-category law: a per-bytes
  deviation is allowed with a one-sentence disclosure in `device_notes`; no free text.
- **§6 granularity** — one formula-bounded unit per row; 7-10 verses typical, measured and listed blocks to 14-16.
  Chapter divisions do not cut unless they coincide with a real seam (§6 names 10:1, 36:1, 39:1, 45:1 as
  non-cutting). Guard against over-splitting: a single verse is never its own row without a disclosed tier-1 reason.
- **§7 low-confidence posture** — HOLD honestly at `medium_low`/`low` with a bespoke rationale rather than forcing
  a boundary. The flagged regions (chs 1-3, 8-11, the 20/21 zone, 25-32, 38-39, 40-48) are expected to carry them.
- **§8 register** — binding verbatim.

## OUTPUT — one JSONL row per chunk, 22 fields, to the exact filename your launch message names

```
decision_id            "PNN-001" ascending within your part
book                   "Ezek"
model_id               "M8_fable"
chunk_index_in_book    integer, ascending within your part
span                   "Ezek.C.V-Ezek.C.V"  (WEB numbering)
boundary_rationale     prose: the onset evidence, the close evidence, BOTH SIDES of the seam, byte-cited
boundary_evidence_refs list of refs, each with its disclosure (parashah / K-Q / paseq / single-witness / dual)
strongest_rejected_alternative  the best boundary you did NOT take, and why
literature_type_guess  free label
confidence             high | medium | medium_low | low
strong_or_hebrew_tags_used      list
wj_or_red_letter_considered     bool
frontier_flag_considered        bool
non_authorizing        true
review_status          "pending"
parent_collection      "P1".."P8" with the §5 label
unit_type              one of the 12
writer_part            your part id
writer_decision_id     "<part>-<n>"
writer_attempt_id      your attempt id
observed_substrate_signals  list
device_notes           disclosures: category deviations, K/Q, paseq counts, zone duals, puncta, 33:20
```

## HEBREW: SPLICE IT, NEVER TYPE IT

**Build every Hebrew string in your rows by reading it programmatically out of `Ezek_oshb.txt` and splicing it in.
Never hand-type Hebrew, and never write it as unicode escapes.** A writer in this same wave hand-typed several
escapes, got at least four byte-wrong, caught it in self-check and had to regenerate the entire file. Hand-typed
Hebrew is the E-01 failure class and it is completely avoidable: the source is right there and you can read from it.

A **Qere** is the one legitimate exception to "it must be in the verse bytes" — a Qere lives in the OSHB note
layer, not in the verse text. Cite it from `pmarks_Ezek.json` `kq`, strip the morpheme separators `/`, and
disclose it as a Qere. That is wanted, not merely tolerated: K/Q sites are textual-variant sites.

## SELF-CHECK BEFORE YOU RETURN (write these yourself, in YOUR OWN private scratch)

**The shared validator toolchain is not staged for Ezekiel.** Do not claim you ran a tool that does not exist, and
do not go hunting for one. Write your own checks as short scripts in your private scratch directory, run them over
a PRIVATE COPY of your deliverable, and report in your final message exactly what you ran and what it returned. An
honest "I wrote my own tiling check because none is staged" is correct and expected; a claimed tool run that did
not happen is the single worst thing you can put in a receipt.

1. **Tiling** — your rows cover your assigned range exactly: no gap, no overlap, no verse outside it. Sum the
   per-chapter counts from `verse_inventory.json` and check contiguity.
2. **Schema** — all 22 fields on every row; `unit_type` one of the 12; `confidence` one of
   high/medium/medium_low/low; `non_authorizing` true.
3. **Hebrew byte-truth** — every Hebrew run you quote is a substring of `Ezek_oshb.txt`, or a Qere from the K/Q
   note layer with its separators stripped. Check this **programmatically, on the finished file**.
4. **Zone duals** — every ref touching WEB 20:45-49 or WEB ch 21 carries its `oshb:` dual **on the same line**,
   including second and later mentions.
5. **Disclosures** — every K/Q, paseq, puncta and the MT 33:20 sof-pasuq gap that your spans cover.
6. **Seams** — no row straddles a parent seam or a hard seam (the 14 datelines, the vision onsets). MT 1:1-3 is
   ONE superscription and is never split, so 1:2 inside a row opening at 1:1 is correct.
7. **Fabrication classes** — no selah, no large or small letter, no reversed or suspended nun, no Aramaic label.

The orchestrator runs `_validate_writer_part.py` over your deliverable independently. It checks tiling, seams,
zone duals, Hebrew byte-truth against both the verse bytes and the K/Q layer, disclosures and schema. It is a
DETERMINISTIC pass and proves form, not judgment — your seams are judged by the peer and boss rounds.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"...","execution_id":"...",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<rows written>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search; read only the exact paths named",
 "rows_written":0,"span_covered":"...","tiling_check":"PASS|FAIL",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```

`unresolved_uncertainty` is the field most worth having and the easiest to leave empty. A part of Ezekiel that
raised no hard question either had a trivial stretch or is not saying. **Held low confidence is a result, not a
failure** — this campaign would far rather have an honest `low` with a bespoke rationale than a forced `high`.
