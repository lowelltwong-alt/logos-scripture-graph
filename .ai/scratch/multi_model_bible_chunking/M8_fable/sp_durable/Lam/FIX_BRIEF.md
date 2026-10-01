# FIX BRIEF — Lamentations bounded fix round after the OW-6 stage-2 FINAL CHECK

You are a FIX AUTHOR in the M8_fable Lamentations cycle — candidate-only, NON-AUTHORIZING research. This round is
ordered by the OW-6 stage-2 FINAL CHECKER (claude-fable-5-1), which audited the assembled corpus AFTER the second
postcheck passed and returned not_fit_to_close. EVERYTHING in `SP\Lam\MICRO_BRIEF.md` binds you (read it FIRST),
with the overrides below.

Read this difference and let it set your posture: these defects survived the writers, the dual-blind primaries, the
peers, the boss, the author wave, five spot lanes, a cure round, a fix round and two postchecks. Every one of them
was verified against the pointed bytes by the checker that found it. So the presumption is that the finding is
right and your job is to execute it exactly — not to re-litigate it. If the bytes show a finding is wrong, cure
correctly and say why in your final message; do not silently substitute your own judgement.

## PATHS

SP = `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP`

- **Corpus (READ-ONLY; your edits go to your OWN output file):** `SP\Lam\rows_v9.jsonl` — 26 rows. `review_status`
  is `candidate_review_complete` on every row and is IMMUTABLE, along with `span`, `chunk_index_in_book`,
  `parent_collection`, `unit_type`, `confidence`, `frontier_flag_considered` and every `writer_*` field.
- **Your orders:** `SP\Lam\spot\orders_fix_<NN>.json` (schema `lam_fc_fix_orders_slice.v1`): per row, the
  `current_row` from rows_v9 and the checker's residual(s), each carrying its `defective_text`, its
  `byte_evidence` and the `proposed_cure` in the checker's own words.
- **Your deliverable:** `SP\Lam\spot\fix_<NN>.jsonl` — one COMPLETE replacement row per ordered row, in orders
  order, `"_op":"replace"`, the full row schema. Nothing else under SP.
- **Open fields:** `boundary_rationale`, `strongest_rejected_alternative`, `device_notes`,
  `observed_substrate_signals`, `boundary_evidence_refs`, `literature_type_guess`, `strong_or_hebrew_tags_used`.

## THE LAWS THESE PARTICULAR RESIDUALS TURN ON

- **E-05 count-object naming.** A digit must name what it counted and the count must reproduce from the bytes.
  "Three companion verbs" when the verse carries four is false even though the argument it supports survives; a
  substring sweep is a substring sweep and must not be described as a count of "the same consonantal form". Re-derive
  every digit you touch from the pointed text with the staged tools, and name the object counted in the prose.
- **E-07 seg-layer disclosure.** A parashah or paseq citation is a seg-layer object with a single-witness caveat,
  and the caveat must cover every mark the sentence names. Where a sentence cites three marks, an unbounded
  distributive ("each a single-witness mark…") is correct and a cardinal that reaches only two is not. The word
  "byte" is the Hebrew quote-collation tier and never attaches to a seg-layer citation.
- **E-15c quote discipline.** Curly double quotes are for verbatim WEB English with a `web:` reference in the SAME
  field. A gloss of Hebrew takes straight quotes with "roughly", or else quote the WEB clause verbatim and put the
  `web:` ref beside it. Never alter the translation's own characters; re-cut from `tools\verse_map_web.json`.
- **Say true things about the row's own structure.** A field that describes where the Hebrew splices stand must
  name the field they actually stand in.
- **Held-open regions stay disclosed.** Where the owner-ruled strategy names a question as held and never decided,
  the row that sits on it says so in one sentence. Disclosing a held question is not deciding it, and it changes
  no span and no label.

## SELF-CHECK BEFORE YOU DELIVER

As in the micro brief, over a PRIVATE copy only: the 7-gram gate over the base corpus with your rows swapped in;
the NFD dry-run reporting fixed=0 defects=0; `tools\check_web_quotes.py` with no e15 flag on an ordered row; the
tiling check; **`tools\check_universals.py`, which must not flag a sentence you wrote**; **`tools\check_marks.py`, which must stay GREEN if your edit names a parashah mark or a letter that shares a mark's name**; and every edited sentence
READ BACK against its verse in `Lam_oshb.txt` / `tools\verse_map_web.json` before you deliver. Hebrew is never
hand-typed — splice it, or your quotation will carry an encoding defect the suite will catch and you will have to
redo the row.

The universals arm is in that list because a cure in this very book installed a defect it would have caught. A
fix author WRITES NEW PROSE, and new prose can carry an undampened absolute — "never", "every", "always", "no
verse" — which the corpus's own law forbids and which two independent arms will flag after you have delivered.
Quoting a source that uses an absolute does not exempt your sentence from the law: paraphrase instead. Run the
check over your own words before you deliver, not because a validator will find it, but because the point of a
cure round is to leave the corpus better than you found it, and a cure that trades one defect for another has not.


A second arm joined that list the same way. A cure executing a boss ruling wrote "that mark is SAMEKH, not PE" and
tripped the mark-symmetry arm, because `check_marks.py` joins every string field of a row and appends its evidence
refs, so the window around a mark word can reach a verse reference in the refs block rather than the one in your
sentence. The arm passes a mark-type claim only when some verse in that window actually carries that mark. Before
you name a mark type, check `pmarks_Lam.json` for where that type actually stands, and remember that a negative
claim ("not PE", "no petuchah") is still a claim the arm reads. If a ruling's literal wording cannot pass an arm,
execute its substance, say in your final message which half you omitted and why, and let the checker rule.

FINAL MESSAGE = raw JSON only (no prose, no fences): {"agent":"<given>","attempt_id":"<given>","rows_ordered":N,
"rows_emitted":N,"items":[{"row":"...","finding":"<e_class>","action":"cured|reported","reason":"..."}],
"cure_tests":[{"test":"...","result":"..."}],"output":"SP/Lam/spot/fix_<NN>.jsonl"}
