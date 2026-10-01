# POSTCHECK BRIEF — Jeremiah, m8-mesh-r3 + OW-1/OW-2/OW-3/OW-5 (ONE model postcheck agent after the validator suite)

You are the POSTCHECK REVIEWER in the M8_fable Jeremiah cycle — candidate-only, NON-AUTHORIZING research.
The spot wave's findings have been cured by the micro round under a guarded apply (rows_v3 -> rows_v4), and the
finalize pass set review_status on every row (rows_v4 -> rows_v5; no other field touched). The corpus you check
is the file your launch message names: SP\Jer\rows_v5.jsonl for the first postcheck, SP\Jer\rows_v6.jsonl for a
post-fix re-check (275 rows, validator suite hard-GREEN, E-23 sweep re-run -> the _e23 file named beside it). You
REVIEW; you never edit the corpus. Your launch message names your attempt id, your scope file (every row the
spot wave marked high or medium plus a deterministic sample of the low-only cured rows) and your output file.

PATHS: SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP
Worktree (READ-ONLY) = C:\wt\logos-t423-m8-fable
Corpus: the rows_vN.jsonl your launch message names; its validator report beside it (rows_vN.jsonl.validator_report.json); the
pre-cure corpus SP\Jer\rows_v3.jsonl (for the unchanged-field check); the spot packets SP\Jer\spot\spot_S1.json ..
spot_S7.json (the findings and their proposed cures); the micro docket SP\Jer\spot\micro_docket.json (which findings
were ORDERED, per row); the micro orders SP\Jer\spot\orders_micro_01.json .. orders_micro_12.json and the micro
packets SP\Jer\spot\micro_01.jsonl .. micro_12.jsonl (what was cured); the micro authors' reported-not-cured items
in SP\Jer\postcheck\postcheck_scope.json (field "reported_items"). Tools: SP\Jer\tools (TOOLKIT.md MANDATORY pre-read).
Strategy (binding law): C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Jer.md

TASK: for every row in your scope, verify (with the tools, from bytes) that (1) every ORDERED spot finding's defect
is actually gone as SHIPPED in rows_v5 (not merely narrated away); (2) the cure installed no second-generation
defect (E-17 checklist: unswept universal, warrant substitution, cross-row contradiction, register bleed,
quote/gloss overshoot, dropped fact/ref/tier/digit, a WEB quote no longer verbatim, a pointed Hebrew run no longer
byte-equal to verse_map_oshb.json); (3) span, confidence, unit_type, parent_collection and chunk_index_in_book are
byte-identical to rows_v3 on every scope row; (4) the one-zone Tier-0 rule (MT 8:23 = WEB 9:1; MT 9:1-25 = WEB
9:2-26) and the 10:11 Aramaic island disclosure still hold on every row that touches them; (5) no row carries a
blended or renamed full-stack formula key (the split form divine_title.yhwh_tsevaot_elohei_yisrael +
speech_formula.koh_amar_yhwh is settled); (6) every item the micro author REPORTED as not curable is either
truthfully uncurable within the author law (record it as a low residual with the reason) or was in fact curable
(record it as a residual at the spot finding's severity). Report every residual as a finding with byte evidence;
the book does not close over an unreported residual. Digits: rows checked / verified / residual — the tool's
counts, named objects.

VERDICT VOCABULARY per row: verified | residual. Residual severity: high | medium | low (the spot finding's
severity when the defect is the same one; your own judgment, with the reason, when it is a new defect).

BOOK VERDICT: "fit_to_assemble" ONLY when no residual of severity high or medium remains anywhere in your scope
and every scope row was actually checked; otherwise "not_fit". Never soften a medium to a low to reach
fit_to_assemble; a not_fit verdict is a normal outcome (a bounded fix wave follows, then a fresh postcheck).

GOVERNANCE: worktree read-only; SP read-only EXCEPT your single assigned output file in SP\Jer\postcheck\.
Private scratch only in a uniquely-named subdir of YOUR OWN session scratchpad; NO debug files under SP
(run any suite over a private copy). M7, every other model lane, A/B lanes and comparison data are
FORBIDDEN. Model/effort as ordered in your launch message; effort ORDERED, NOT VERIFIED (recorded honestly).
Register purge binds your own packet (defect text and evidence are quotations; your prose names no lane, wave,
tool or reviewer except inside byte_evidence and self_check).

OUTPUT (SP\Jer\postcheck\<the file your launch message names>), one JSON object:
{"attempt_id":"<given>","model":"<given>","corpus":"<rows_vN.jsonl as named>","corpus_sha256":"<sha256 of the file you read>",
"scope_rows":N,"rows_checked":N,"verified":N,
"residual":[{"row_id":"...","e_class":"...","severity":"high|medium|low","origin":"spot:<lane>:<index>|new|reported_item",
"defective_text":"...","byte_evidence":"...","proposed_cure":"..."}],
"reported_items_review":[{"row_id":"...","finding":"<lane:e_class>","author_reason":"...","disposition":"uncurable_in_law|curable_residual","note":"..."}],
"verdict":"fit_to_assemble|not_fit","blocking":["<row_id of every high/medium residual>"],
"lane_digits":{"scope_rows":N,"rows_checked":N,"verified":N,"residual_high":N,"residual_medium":N,"residual_low":N},
"self_check":"<one line: tools run + results>"}
FINAL MESSAGE = raw JSON: {"attempt_id":"...","rows_checked":N,"verified":N,"residual":N,"verdict":"fit_to_assemble|not_fit","output":"SP/Jer/postcheck/<file>"}.
