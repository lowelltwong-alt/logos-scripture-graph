# Ezekiel v10 delta re-check, blind lane B (model claude-opus-5-5, grader_fallback (OW-25))

assembly_verdict: fit_to_assemble. verdict: fit_to_close. bounded_fix: null.

- All 28 pinned digests match disk. v10 has 138 lines, and 137 of them are byte-identical to v9. P10-016 (line 113) differs only in review_status and the two inserted hold fields, and its key order is kept. All six manifest sha256 values recompute. build_rows_v10.py --check prints MATCH for both files.
- The shipped suite report is hard_status GREEN over v10. The mirror suite differs only in rows_file. CWO parity is GREEN over 106f3553.
- All eight ruled rows are implemented as ruled. 113 is held in both the corpus and the feed. 082 (graded high) is gone from the feed, the dimensions and the sidecars, and its corpus row is unchanged. For 035, 037, 038, 039, 049 and 083, the corpus rows are unchanged, the feed rows carry no hold, and the referral sentence is gone.
- gen_atlas_rows --check and gen_sidecars --check both print MATCH. The mirror's atlas record is byte-equal to the shipped one. The selftest PASSES: tamper_packet_state trips feed_mirrors_the_corpus_hold.

Defects that stand. All are low, and none is in the corpus delta:
- L1 (check_atlas_rows.py): the check names `held_rows_are_exactly_the_referred_ones` and `off_vocabulary_grades_are_referred_rows` still say "referred", though both now test the corpus hold.
- L2 (gen_atlas_rows.py): the risk sentence "declined to act here and referred the question onward" is now triggered by the corpus hold, not by the referral. It is true for 113 today. It would be false for a later corpus-held row that was never referred.
- L3 (method_change_proposals): "On a book with 102 rows" reads as a current fact. The feed now has 101 rows and the book 138. The file's other two "102" counts are past-tense measurements.

For the Fable end review:
- M8-Ezek-113 is still defective as measured, so keep_held fits P3. Its rationale says 40:31 stands "immediately before 40:38", but in the witness 40:37 does. It also counts "this row's four occurrences and 40:24" as 6 verses, but the witness has the refrain at 40:24, 28, 29, 32, 33 and 35, which is five verses inside the row. The corrected row must fix both.
- The six released rows' judged score still gets +2 for the old referral (dimensions only, disclosed). 082 and 083 carry the utterance.mid_unit class question (B19), as the ruling routes it.

What I could not do:
- The stage-1 transcript audit is OWED, NOT MET (OW-26). This pass read no transcript.
- I could not measure the paseq or K/Q-note counts. Ezek_oshb.txt has no paseq glyph anywhere (0 in the file) and no K/Q markup.
- I did not verify repoint_generators_v10.py, the Fable end packet, or whether any suite member checks the hold-field vocabulary.
