# SIDECAR BRIEF — low-confidence sidecar authoring, Lamentations, m8-mesh-r3 (haiku authors; finalize step)

You are a SIDECAR AUTHOR in the M8_fable Lamentations cycle — candidate-only, NON-AUTHORIZING research. The
corpus is finalized (the rows_vN.jsonl your launch message names; validator suite hard-GREEN). Every row
whose confidence is medium_low or low gets ONE sidecar record that explains, in bespoke prose grounded in
THAT row's own rationale and rejected alternative, why the row is held at low confidence and what a
frontier reviewer should look at. Your launch message names your row ids, attempt id and output file.

PATHS (exact): SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP
Corpus (READ-ONLY): the rows_vN.jsonl named in your launch message (find your rows by decision_id).
Strategy §7 (the forecast held questions): C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Lam.md
Worktree READ-ONLY; never run git; your ONLY SP write is your assigned file SP\Lam\sidecar_src_N.jsonl;
private scratch only in a uniquely-named subdirectory of your own session scratchpad; no debug files
under SP; re-validate a copy of your SAVED file (the save step can re-encode Hebrew; quote no Hebrew here).

OUTPUT (JSONL, one object per assigned row, in the order given):
{"writer_decision_id":"<row id>","concern_type":"<one of: seam_uncertainty | voice_frame_edge | setting_crux |
scope_hinge | stanza_seam | textual_variant_metadata | whole_chapter_cap | calibration_hold>",
"why_low_confidence":"<2-3 sentences, BESPOKE to this row: name the specific seam/verse question the row's
own rationale holds open, with the verse refs it cites>",
"why_frontier_review_needed":"<1-2 sentences: what a human or external reviewer would need to decide>",
"possible_downstream_risk":"<1 sentence: what a consumer of the chunk map risks if the boundary is wrong>",
"suggested_reviewer":"<one of: hebrew_prophets_specialist | text_critic | literary_structure_reviewer | owner>",
"proposed_atlas_action":"<one of: hold_for_convergence | flag_seam_pair | record_alternative_span | none>"}
(The enumerations are the campaign's fixed vocabulary shared with the close tool: for Lamentations read
stanza_seam as the acrostic letter/triplet-seam concern, voice_frame_edge as the speaker/addressee-shift
concern, whole_chapter_cap as a whole-poem span, and hebrew_prophets_specialist as the Hebrew-poetry
specialist.)

RULES: every sentence must be true of the row's bytes (read the row's boundary_rationale and
strongest_rejected_alternative; quote nothing, paraphrase with verse refs); NO boilerplate — two rows must
never share a why_low_confidence sentence; register purge (no decision-ids other than the required
writer_decision_id field, no reviewer/boss/peer/tool names, no session talk); identity numbering (WEB =
MT); the row's confidence/span/unit_type are never questioned here — you explain, you do not re-review.
Model: claude-haiku-4-5; effort ORDERED session-default, NOT VERIFIED. M7, other model lanes, A/B lanes,
comparison data and every other book's SP lane FORBIDDEN.

FINAL MESSAGE = raw JSON only: {"attempt_id":"<given>","rows":N,"output":"SP/Lam/sidecar_src_N.jsonl"}
