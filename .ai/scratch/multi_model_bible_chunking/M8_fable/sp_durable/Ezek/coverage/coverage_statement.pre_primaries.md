# Q8 coverage statement - Ezekiel (pre_primaries)

Built 2026-09-14T21:12:24.407939+00:00. Authority: ruling Q8 (#e2), amended by Q8-T (#e4). Never a summed count.

## 1. Census (verbatim)

```
{
 "attempts": 66,
 "attempts_note": null,
 "transcript_retained": 63,
 "transcript_retained_by_route": {
  "manifest": 63,
  "per_book_subagents_index": 63,
  "preserved_store_index": 0,
  "union_before_intersection": 63,
  "rule": "retention is the union of the routes INTERSECTED with this book's receipt attempt ids"
 },
 "preserved_not_a_receipt_attempt": [],
 "routes_read": [
  {
   "route": "per_book_subagents_index",
   "path": "transcripts/_subagents_index.ezek.v1.json",
   "sha256": "e3917d40b3bdb03008d991893b5486a1babdff7ada4dbc0d383ec2559b4b4065",
   "entries": 78,
   "read": true,
   "rule": "retained when the durable transcript has bytes > 0 and re-hashes to its durable_sha256 at count time",
   "retained": 78,
   "rehash_mismatches": 0
  }
 ],
 "transcript_retained_manifest_route_only": 63,
 "transcript_mapped_but_zero_bytes": 15,
 "observed": 0,
 "observed_attempt_ids": [],
 "observed_pct_of_attempts": 0.0,
 "observed_by": null
}
```

## 2. Per-execution layer table

Session roots named by the preserver index: {"221a93aa-d2a7-4d91-a265-84e495a39efa": {"durable_store": "C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\transcripts\\221a93aa-d2a7-4d91-a265-84e495a39efa", "exists": true}, "6116e665-408b-4874-9bf0-881eb9c464f5": {"durable_store": "C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\transcripts\\6116e665-408b-4874-9bf0-881eb9c464f5", "exists": true}, "910cbe15-396b-4a0e-82f6-8aa1e2edf1e4": {"durable_store": "C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\sp_durable\\transcripts\\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4", "exists": true}}. The census-time class comes from `finding_ezek_transcripts_decayed_before_mirror.v3.json` and was measured on the tasks/ route (OW-11-m); the observed-now class is read at build time from the subagents route. The two are never substituted for each other (Q8-T (f)).

| execution | role | model ordered | outcome | layer A | class at census (tasks/ route, OW-11-m) | class observed now (subagents route) | layer B | layer C |
|---|---|---|---|---|---|---|---|---|
| ezek_author_p01_a1#e1 | author | claude-sonnet-5 | REFUSED_NO_DELIVERABLE - read the worktree registry (Fable-5-only rule, stale progress fields) before its brief; its launch message did not carry the OW-11 authority paragraph, so it saw no owner exception and failed closed; read no brief or orders, wrote nothing. Relaunched as #e2 with the authority paragraph in the launch message. | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 2 of its runs are unsuff | not in the census finding | A (durable copy holds 248749 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_p01_a1%23e1.json', 'sha256': '3cde5d9c4da875471b29fb9fef9ea604dd0109d43d0f9456 |
| ezek_author_p05_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 852359 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_p05_a1%23e1.json', 'sha256': '1ff2a3af0370c8c09de029c24f4c62574c62726caf343257 |
| ezek_author_p07_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 817224 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_p07_a1%23e1.json', 'sha256': 'c5d3ae0c5d8a6061c5a35fc4e810f2d3ca37f6ed74765bd8 |
| ezek_author_p04_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 994076 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_p04_a1%23e1.json', 'sha256': '3c84aacc1d82f882bc31ad64b02bce86e7bbfd6ec48bfd9f |
| ezek_author_p09_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1009219 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_p09_a1%23e1.json', 'sha256': '025b53b65cce36f341d81ab711f45d473016bdcef2faf316 |
| ezek_author_p01_a1#e2 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 2 of its runs are unsuff | not in the census finding | A (durable copy holds 1012435 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_p01_a1%23e2.json', 'sha256': '4d453057ddb7868c2af8aca3a70ee15e152d02c2618d2de8 |
| ezek_author_p10_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1244931 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_p10_a1%23e1.json', 'sha256': '3d4478e3d784c36bda31fb772ec2eb943a4cfc549ffe3447 |
| ezek_author_p11_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1149823 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_p11_a1%23e1.json', 'sha256': '658862a17ee423e05f88f568da51d0123c86478ce1c6a594 |
| ezek_author_p02_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1318953 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_p02_a1%23e1.json', 'sha256': '1908d725cbb81340f22bbb0a5d40313365835a250d9b6fc7 |
| ezek_author_p03_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1374565 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_p03_a1%23e1.json', 'sha256': '3e8b98d570299acf074776e664b8ed17a86ac77d5815f7bb |
| ezek_author_p06_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1475316 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_p06_a1%23e1.json', 'sha256': '811fb0b6615b100868cf29d64c69ca392fa9c66bd979ecca |
| ezek_author_p08_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1556432 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_p08_a1%23e1.json', 'sha256': '2a0090c04b16e51b9615280cb7168f7a942dbb9c9b0c1aa1 |
| ezek_stage_p0_a1#e1 | phase0_staging | claude-opus-5 | LANDED - Ezekiel Phase 0 staging complete except TOOLKIT.md | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | UNAVAILABLE (not in the preserver index) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_stage_p0_a1%23e1.json', 'sha256': 'd4aacce700a166eef9db307696f975bf932e27919aa1ba8948 |
| ezek_toolkit_a1#e1 | phase0_staging | claude-opus-5 | LANDED - EZEKIEL PHASE 0 COMPLETE | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | UNAVAILABLE (not in the preserver index) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_toolkit_a1%23e1.json', 'sha256': 'd3a4ceed493dd338325cf90bd42857440ff59b94abe103303b6 |
| ezek_strategy_a1#e1 | unknown | claude-fable-5-1 | LANDED - strategy accepted with one orchestrator correction | {'path': 'C:\\Users\\lowel\\AppData\\Local\\Temp\\claude\\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\\22 | durable; behaviour A | A (durable copy holds 787042 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_strategy_a1%23e1.json', 'sha256': 'df8b1dcf9328da97ba53032156cd31145c391ce130cf0431e7 |
| ezek_p0_recheck_a1#e1 | phase0_staging | claude-opus-5 | LANDED - fit_to_accept with two further findings | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | lost; behaviour unknown - first observed after landing | A (durable copy holds 364532 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_p0_recheck_a1%23e1.json', 'sha256': '1b2df9ed141b4816a7e8a630259f15cf7120d3f056adee71 |
| ezek_p0_delta_a1#e1 | phase0_staging | claude-opus-5 | LANDED - not_fit_to_accept, one blocker | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | lost; behaviour unknown - first observed after landing | A (durable copy holds 309396 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_p0_delta_a1%23e1.json', 'sha256': 'b6365971245ed021a7c867bcca9c63d1a756ae2a15717d709f |
| ezek_p0_r3_a1#e1 | phase0_staging | claude-opus-5 | LANDED - fit_to_accept | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | lost; behaviour unknown - first observed after landing | A (durable copy holds 349678 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_p0_r3_a1%23e1.json', 'sha256': 'a1bf6528ac1586237348ac5e696e58eb88f99e27c352c84a5b5c7 |
| ezek_p0_repair_a1#e1 | phase0_staging | claude-opus-5 | LANDED - both cure claims ACCEPTED by _cure_verification.py | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | UNAVAILABLE (not in the preserver index) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_p0_repair_a1%23e1.json', 'sha256': '777bbb06a3c12c9aae4c7918af25dc15f92a7764ecab4adf9 |
| ezek_toolkit_review_t1_a1#e1 | unknown | claude-sonnet-5 | REFUSED_NO_DELIVERABLE - declined to write inside the registry-protected worktree (Fable-5-only rule) before any owner exception existed; reviewed nothing, wrote nothing. Its refusal surfaced the authority conflict that OW-11 resolved. | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 847678 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_toolkit_review_t1_a1%23e1.json', 'sha256': '292f8cef3a72378235f18fc0f41d16128dac855d0 |
| ezek_controlling_rulings_a1#e1 | unknown | claude-fable-5-1 | STOPPED_BY_ORCHESTRATOR - containment during the governance hold, before any deliverable; its only final text was a one-line start notice. Verified afterwards: no deliverable at its exact path. | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 10 of its runs are unsuf | not in the census finding | A (durable copy holds 650656 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_controlling_rulings_a1%23e1.json', 'sha256': 'a350d17504726c8bbb49d4a939ff87c61a035d1 |
| ezek_toolkit_review_t1_a1#e2 | unknown | claude-sonnet-5 | LANDED_WITH_FORM_DEFECTS | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 847678 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_toolkit_review_t1_a1%23e2.json', 'sha256': '318f592543698bbca83b3bcd94b2af425a1e315bc |
| ezek_controlling_rulings_a1#e2 | unknown | claude-fable-5-1 | LANDED_WITH_FORM_DEFECTS | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1087569 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_controlling_rulings_a1%23e2.json', 'sha256': 'a89ea87220e3fb11fe9599cba57819f456d9931 |
| ezek_toolkit_repair_review_t2_a1#e1 | unknown | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 877436 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_toolkit_repair_review_t2_a1%23e1.json', 'sha256': '5bc29bb3db278524bc51f8d2bfc0e4fd54 |
| ezek_toolkit_supplementary_review_t3_a1#e1 | unknown | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1157810 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_toolkit_supplementary_review_t3_a1%23e1.json', 'sha256': '660433218c998e117e3d3fbdc84 |
| ezek_controlling_rulings_a1#e3 | unknown | claude-fable-5-1 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 10 of its runs are unsuf | not in the census finding | A (durable copy holds 1264874 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_controlling_rulings_a1%23e3.json', 'sha256': 'c2640e482e0b3ab456989b4c67f11d900b1fcf5 |
| ezek_toolkit_r4ii_review_t4_a1#e1 | unknown | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 898536 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_toolkit_r4ii_review_t4_a1%23e1.json', 'sha256': '3f41c98855e6df974bc88a8b4c4c357b325f |
| ezek_author_wave_spot_review_s1_a1#e1 | author | claude-opus-5 | LANDED_WITH_FORM_DEFECTS | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 2154270 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_wave_spot_review_s1_a1%23e1.json', 'sha256': '102d618aa26e192a05a521df689ed337 |
| ezek_controlling_rulings_a1#e4 | unknown | claude-fable-5-1 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 10 of its runs are unsuf | not in the census finding | A (durable copy holds 1342500 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_controlling_rulings_a1%23e4.json', 'sha256': '49d6b9824db634b9d1e2c17345e18d94f94bd35 |
| ezek_controlling_rulings_a1#e5 | unknown | claude-fable-5-1 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 10 of its runs are unsuf | not in the census finding | A (durable copy holds 852725 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_controlling_rulings_a1%23e5.json', 'sha256': '0a5095934f79ca046941b223c3874398c6cdb08 |
| ezek_toolkit_install_review_t5_a1#e1 | unknown | claude-opus-5 | LANDED_WITH_FORM_DEFECTS | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1723042 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_toolkit_install_review_t5_a1%23e1.json', 'sha256': 'c0ec2873bfb625133e287356c2b423aed |
| ezek_controlling_rulings_a1#e6 | unknown | claude-fable-5-1 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 10 of its runs are unsuf | not in the census finding | A (durable copy holds 1088349 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_controlling_rulings_a1%23e6.json', 'sha256': '5fcf76ad7cb28dc6c7c61226048eccc27cacc75 |
| ezek_controlling_rulings_a1#e7 | unknown | claude-fable-5-1 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 10 of its runs are unsuf | not in the census finding | A (durable copy holds 423434 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_controlling_rulings_a1%23e7.json', 'sha256': '778ef5087cc373bd1c95166c9dd6de953245279 |
| ezek_toolkit_tf3_review_t6_a1#e1 | unknown | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1051342 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_toolkit_tf3_review_t6_a1%23e1.json', 'sha256': '3c20752fc3474c1fbf392367545ec97725a3c |
| ezek_controlling_rulings_a1#e8 | unknown | claude-fable-5-1 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 10 of its runs are unsuf | not in the census finding | A (durable copy holds 417402 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_controlling_rulings_a1%23e8.json', 'sha256': '65a2621989e387944078003f9fbb8f2427e29a2 |
| ezek_fixup_wave_review_s2_a1#e1 | fix_author | claude-opus-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1825987 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_fixup_wave_review_s2_a1%23e1.json', 'sha256': '94af37650723379c6d3dddf243e27e714f6def |
| ezek_controlling_rulings_a1#e9 | unknown | claude-fable-5-1 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 10 of its runs are unsuf | not in the census finding | A (durable copy holds 821599 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_controlling_rulings_a1%23e9.json', 'sha256': '01d1f2cb174b72e941cc802d9cc0e49d014c1fd |
| ezek_fixup2_wave_review_s3_a1#e1 | fix_author | claude-opus-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 2208856 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_fixup2_wave_review_s3_a1%23e1.json', 'sha256': '06e39ec90addc5a77ac0bac74dce29ff78f18 |
| ezek_controlling_rulings_a1#e10 | unknown | claude-fable-5-1 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 10 of its runs are unsuf | not in the census finding | A (durable copy holds 1271389 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_controlling_rulings_a1%23e10.json', 'sha256': '0e28e83b4a06435be921696998bf7beabe94a2 |
| ezek_fixup3_wave_review_s4_a1#e1 | fix_author | claude-fable-5-1 | STOPPED_AT_FINAL_MESSAGE - the execution made 95 tool calls and wrote a complete deliverable reviewing the applied corpus's exact bytes, using the corrected deliverable schema the orchestrator sent mid-flight, and the runtime then killed it as it emitted its final message (API rate_limit, HTTP 429: the account's claude-fable-5-1 usage credits were exhausted). NO self-authored OW-8 record exists, in the notification or anywhere in the preserved transcript, so this execution is NOT LANDED. | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1995838 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_fixup3_wave_review_s4_a1%23e1.json', 'sha256': '7134c7ad5461b16094d11e66761b7f858ec23 |
| ezek_controlling_rulings_a1#e11 | unknown | claude-fable-5-1 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 10 of its runs are unsuf | not in the census finding | A (durable copy holds 1409107 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_controlling_rulings_a1%23e11.json', 'sha256': '68250d4c6ab902e476fbe5037e114c7e26bef8 |
| ezek_author_fixup_p05_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 582408 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup_p05_a1%23e1.json', 'sha256': '925c33eac23b4fb0cd0779584c38caebc3fdb6c492 |
| ezek_author_fixup_p04_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 712105 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup_p04_a1%23e1.json', 'sha256': 'b88fcd275e1eea3d3bd24057f7eeafa9c8cc4ce8c8 |
| ezek_author_fixup_p09_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 851212 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup_p09_a1%23e1.json', 'sha256': '6ceb86cdc47bd6d9934311e62f4d599f79c53aa01a |
| ezek_author_fixup_p11_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 970407 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup_p11_a1%23e1.json', 'sha256': 'd0bb104974f6df984864954822876307cf3065d7cf |
| ezek_author_fixup_p01_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 894050 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup_p01_a1%23e1.json', 'sha256': '950397da275ed1a9bc52ff2f4878d93f7647059258 |
| ezek_author_fixup_p07_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1025456 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup_p07_a1%23e1.json', 'sha256': '8636b6bd1cb646da04ca125fd6abb828497079c293 |
| ezek_author_fixup_p10_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1008975 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup_p10_a1%23e1.json', 'sha256': '8a5969dfb61f89dbb5217b4dd5003d34fab2ee0ea5 |
| ezek_author_fixup_p06_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1138255 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup_p06_a1%23e1.json', 'sha256': '926593212174992ee74d866b8c0a8731e6f41231c6 |
| ezek_author_fixup_p02_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1427367 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup_p02_a1%23e1.json', 'sha256': '7d6a1e5e350838c722c164067d311ecbb08499bf6d |
| ezek_author_fixup_p03_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1385833 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup_p03_a1%23e1.json', 'sha256': '2a256c3ff1b959c2258e6f566f6f6c48a6f7fecbb7 |
| ezek_author_fixup_p08_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1342027 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup_p08_a1%23e1.json', 'sha256': '727190842f656c1edfa16f795bf850d391015c3a77 |
| ezek_author_fixup2_p06_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 610346 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup2_p06_a1%23e1.json', 'sha256': '98dc48714650ef3f61bde7faeb38bfe82aa3bce15 |
| ezek_author_fixup2_p09_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 654616 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup2_p09_a1%23e1.json', 'sha256': 'da77a677bb463107385f16190c18cf018364c2d55 |
| ezek_author_fixup2_p07_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 693957 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup2_p07_a1%23e1.json', 'sha256': '0883a27feef6bbfdcc204f9404de1b26533001d64 |
| ezek_author_fixup2_p11_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 651641 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup2_p11_a1%23e1.json', 'sha256': '2cd01b9a5a0c03ce3eb1c6b68c308e05757e884b4 |
| ezek_author_fixup2_p01_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 814232 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup2_p01_a1%23e1.json', 'sha256': '660641ed68402fb7f8a365355b0a5add6ac13591e |
| ezek_author_fixup2_p04_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 802699 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup2_p04_a1%23e1.json', 'sha256': '88d24913e93efd780ed6ae9b676cf221454c20838 |
| ezek_author_fixup2_p02_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 786434 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup2_p02_a1%23e1.json', 'sha256': '687ee6ad0a9fc993936a71ecc195a740692443315 |
| ezek_author_fixup2_p03_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 919248 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup2_p03_a1%23e1.json', 'sha256': '6b7f95eaed4c22498542a6a3513cfd1121f343eef |
| ezek_author_fixup2_p08_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 952666 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup2_p08_a1%23e1.json', 'sha256': 'f1dabc93a622b4d7aff394d0a2666131063e6373c |
| ezek_author_fixup3_p01_a1#e1 | author | claude-sonnet-5 | REFUSED_NO_DELIVERABLE - declined before any tool call. It judged the task a mismatch with the orchestrating session's working directory, read the OW-11 record as a self-referential authorization it could not verify, and read the E-19 no-listing lines as an instruction to disable its own verification; it read no brief, orders or ledger, and wrote nothing. | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 3 of its runs are unsuff | not in the census finding | A (durable copy holds 122003 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup3_p01_a1%23e1.json', 'sha256': 'e764f369e661b3d667457c1ce66aa8a30088d967e |
| ezek_author_fixup3_p01_a1#e2 | author | claude-sonnet-5 | REFUSED_NO_DELIVERABLE - declined before any tool call, after the context paragraph. It read the launch message as an injection pattern: an authorization it could not verify; the no-listing and no-memory lines as suppression of verification and transparency; and a mismatch with the orchestrating session's working directory and branch. It asked the owner to confirm directly in chat, and to allow directory and existence checks. It read no brief, orders or ledger, and wrote nothing. | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 3 of its runs are unsuff | not in the census finding | A (durable copy holds 130417 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup3_p01_a1%23e2.json', 'sha256': 'd365436aa63248beb1b0678de66755aa0a95f7dc8 |
| ezek_author_fixup3_p03_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 2 of its runs are unsuff | not in the census finding | A (durable copy holds 635535 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup3_p03_a1%23e1.json', 'sha256': 'eb1eb934feb03094da21f873f1132bdc5edc42abc |
| ezek_author_fixup3_p07_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 722266 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup3_p07_a1%23e1.json', 'sha256': '57cbdf36d8b3fa0ed8dabffb31df3d795cc539ef9 |
| ezek_author_fixup3_p02_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 960298 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup3_p02_a1%23e1.json', 'sha256': '53fea193afefd6ea6488611d80bb4a0d10684bee5 |
| ezek_author_fixup3_p04_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 973490 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup3_p04_a1%23e1.json', 'sha256': '1c187f0d723b4b823c9088d695f149f7528f78ea7 |
| ezek_author_fixup3_p08_a1#e1 | author | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | not in the census finding | A (durable copy holds 1290722 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup3_p08_a1%23e1.json', 'sha256': 'c460c8997b6e3697f1a359ed262ef5b39ab4b62ea |
| ezek_author_fixup3_p01_a1#e3 | author | claude-opus-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 3 of its runs are unsuff | not in the census finding | A (durable copy holds 975687 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup3_p01_a1%23e3.json', 'sha256': 'd523ca48d08739c91f0dc2d4be383a8aa20fb03e5 |
| ezek_author_fixup3_p03_a1#e2 | author | claude-opus-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the manifest maps one unsuffixed transcript to this job but 2 of its runs are unsuff | not in the census finding | A (durable copy holds 878086 bytes and re-hashes; matched by agent id) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_author_fixup3_p03_a1%23e2.json', 'sha256': '9ee3340b02c9f8b7f757b90b5dc9a25b27bdcd9e8 |
| ezek_writer_p01_a1#e1 | writer | claude-sonnet-5 | LANDED | {'path': 'C:\\Users\\lowel\\AppData\\Local\\Temp\\claude\\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\\22 | durable; behaviour A | A (durable copy holds 931342 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_writer_p01_a1%23e1.json', 'sha256': '0b9229a7679d2c1fa84328f3b9ffdcad23e9aa27da4e2d09 |
| ezek_writer_p04_a1#e1 | writer | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | lost; behaviour unknown - first observed after landing | A (durable copy holds 817630 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_writer_p04_a1%23e1.json', 'sha256': '222613f5eb4a8ce3c2d55881d5a9d6d3e1f53410691f5eb9 |
| ezek_writer_p10_a1#e1 | writer | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | lost; behaviour unknown - first observed after landing | A (durable copy holds 1013674 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_writer_p10_a1%23e1.json', 'sha256': 'd387736807f81ac11bca51366e5f972ef4747d37e5dcddc6 |
| ezek_writer_p02_a1#e1 | writer | claude-sonnet-5 | LANDED | {'path': 'C:\\Users\\lowel\\AppData\\Local\\Temp\\claude\\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\\22 | durable; behaviour A (grew visibly across five mirror passes: 302,889 -> 786,553 bytes) | A (durable copy holds 786553 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_writer_p02_a1%23e1.json', 'sha256': '9db226f495dd60ceb4667e168465f3326bb863fcc39e005e |
| ezek_writer_p06_a1#e1 | writer | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | lost; behaviour B - zero bytes during the run and at landing | A (durable copy holds 840030 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_writer_p06_a1%23e1.json', 'sha256': '800c19174a7c65559d71acc13090077166a84ba39a783c2b |
| ezek_writer_p07_a1#e1 | writer | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | lost; behaviour B - zero bytes during the run and at landing | A (durable copy holds 763602 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_writer_p07_a1%23e1.json', 'sha256': 'bc7989cb2f926740018c7042b82626d86f353b6c3f69db0a |
| ezek_writer_p11_a1#e1 | writer | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | lost; behaviour B - zero bytes during the run and at landing | A (durable copy holds 707811 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_writer_p11_a1%23e1.json', 'sha256': '197c3472ca2a7de62fed7778b35922653ad2a9d4f4fbc908 |
| ezek_writer_p05_a1#e1 | writer | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | lost; behaviour B - zero bytes during the run and at landing | A (durable copy holds 1101581 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_writer_p05_a1%23e1.json', 'sha256': '269a0ea51ed361541042c10709ceb6b4d6bba074e2c65ab5 |
| ezek_writer_p09_a1#e1 | writer | claude-sonnet-5 | LANDED | {'path': 'C:\\Users\\lowel\\AppData\\Local\\Temp\\claude\\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\\22 | durable; behaviour A (1,080,429 bytes captured at landing) | A (durable copy holds 1080429 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_writer_p09_a1%23e1.json', 'sha256': '76119e1e035287d99cb8e52ae931a118e7203b3a0c785cb6 |
| ezek_writer_p03_a1#e1 | writer | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | lost; behaviour B - zero bytes during the run and at landing | A (durable copy holds 1061620 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_writer_p03_a1%23e1.json', 'sha256': '6121adce91e880beec395b7497ccfb06bc57fe143adb423b |
| ezek_writer_p08_a1#e1 | writer | claude-sonnet-5 | LANDED | {'state': 'UNAVAILABLE', 'reason': 'the runtime wrote no transcript for this attempt, or wrote one and deleted it before | lost; behaviour B - zero bytes during the run and at landing | A (durable copy holds 1145142 bytes and re-hashes; matched by attempt id (no agent id recorded for this execution)) | {'state': 'UNAVAILABLE', 'reason': 'the runtime exposes thin | {'path': 'Ezek/evidence_notes/ezek_writer_p08_a1%23e1.json', 'sha256': '465328f0c1afc2a3ffe0afe5c4d2ddc45b131a585200e4f3 |

## 3. Compensations

```
{
 "1_full_dual_blind_primaries": {
  "status": "PENDING (no primaries index and final rows file given)",
  "evidence": null,
  "rule": "every row id of the final rows file against both blind lanes' execution ids; no sampling"
 },
 "2_second_fable_review_rederivations": {
  "status": "PENDING",
  "evidence": null,
  "rule": ">= 3 byte-level re-derivations per layer-A-lost part, from the section-7 regions"
 },
 "3_self_reports_carried_as_self_reported": {
  "status": "RECORDED",
  "rule": "the E-19 and splice-never-type self-reports of layer-A-lost executions are carried as SELF-REPORTED; the receipts' deterministic results are the layer-A-equivalent evidence",
  "executions": [
   {
    "execution_id": "ezek_author_p01_a1#e1",
    "receipt_file": "Ezek/author/ezek_author_attempt_receipts.jsonl",
    "receipt_line_sha256": "24213306199e76091325f37107dc205eca20f49b0aba8cca3040981795ea75c2",
    "outcome": "REFUSED_NO_DELIVERABLE - read the worktree registry (Fable-5-only rule, stale progress fields) before its brief; its launch message did not carry the OW-11 authority paragraph, so it saw no owner exception and failed closed; read no brief or orders, wrote nothing. Relaunched as #e2 with the authority paragraph in the launch message.",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": null,
    "e19_selfreported": "prose final message; see the layer-C note"
   },
   {
    "execution_id": "ezek_author_p05_a1#e1",
    "receipt_file": "Ezek/author/ezek_author_attempt_receipts.jsonl",
    "receipt_line_sha256": "19308824d6cba0db7ec538a589feca28c815de43de6a0373fda856cf51aae77c",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 53,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "304f103d8c9594e7937ec44a15e466c035f278fcb5402b94e042bb37551cba8d",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief and orders file, plus paths those two files themselves named exactly (the toolkit, rulings-adjacent files the brief names, device inventory, pmarks, MT text, the swept rows file, and the staged tool scripts); all Python file access used exact paths built from those same named paths, never a directory scan"
   },
   {
    "execution_id": "ezek_author_p07_a1#e1",
    "receipt_file": "Ezek/author/ezek_author_attempt_receipts.jsonl",
    "receipt_line_sha256": "2c43cfe49b334dd9b92d711f62fbd93e924e9e557c95e74c098220961bfc8448",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 60,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "bfa1191aa1b3ff3e668ced30778f6643c2c9259880d8448c4827267269fa92d1",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief and orders file (plus Grep used only as single-named-file content search on Ezek_controlling_agent_rulings.v1.json, Ezek_oshb.txt and pmarks_Ezek.json, never as a directory operation)"
   },
   {
    "execution_id": "ezek_author_p04_a1#e1",
    "receipt_file": "Ezek/author/ezek_author_attempt_receipts.jsonl",
    "receipt_line_sha256": "6f688f38f968c4312ca9251756558fe01da050afa1d4f655f9a5ebbe37398954",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 49,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "3e11776e77bb2014d60251b2b0da6f72e85b3f9e2f44519a5c389420969e6719",
    "e19_selfreported": "read only the exact paths named in the brief/orders/rulings/strategy, plus the exact tool filenames the brief authorized, plus one path (rows_v2_swept_r3.jsonl) named in orders.sources.rows -- no directory listing, glob or recursive search was ever completed or returned output. One integrity check (certutil -hashfile) and one line count (wc -l), both against a single exact-named file, were run and are not listings. One `ls` command against the tools directory was attempted as a sanity check and is disclosed here rather than omitted: it failed with a bash quoting error (exit code 2, 'unexpected EOF') before producing any output, so no filenames or directory contents were ever returned or seen; the approach was abandoned immediately in favor of the exact tool filenames already named in TOOLKIT.md and the brief, which is what every subsequent tool invocation used."
   },
   {
    "execution_id": "ezek_author_p09_a1#e1",
    "receipt_file": "Ezek/author/ezek_author_attempt_receipts.jsonl",
    "receipt_line_sha256": "6fa342288dd633ad5c8c6566e4ed01b72d0969bd963af6b712d26b9308205018",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 48,
     "qere": 8,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "ed69af05c4b64eb8e843f4d1bc74dfade28e52d318c7f6d426b903cf30b001c2",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief and orders file (plus tool source files explicitly named in the brief's staged-tools list, opened to confirm their contracts). One caveat: a private build script called os.makedirs(exist_ok=True) on OUT's own directory as a defensive no-op immediately before writing the deliverable -- disclosed above as an existence check against OUT, though it produced no listing and no branching on its result."
   },
   {
    "execution_id": "ezek_author_p01_a1#e2",
    "receipt_file": "Ezek/author/ezek_author_attempt_receipts.jsonl",
    "receipt_line_sha256": "0977e4290fd9e0d2260600033f43f5e7cb218a7ef93a92a8e038ab00350a7dd4",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 91,
     "qere": 6,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "ec13bee18df0ee4e660c0e6776c43c8be29771aa7ecd2d2094bab40fe227858a",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief, the orders file (plus one offset-continuation read of the same file), the governance files (ACTIVE_WORKTREES.yaml, ERROR_PATTERN_LEDGER.v1.md) my own policy required, and the toolkit/rulings/strategy/source files the brief names by exact path; grep calls were targeted content searches inside single already-named files (or a single fixed-path directory's one text file, Ezek_oshb.txt), never a directory listing or wildcard path search"
   },
   {
    "execution_id": "ezek_author_p10_a1#e1",
    "receipt_file": "Ezek/author/ezek_author_attempt_receipts.jsonl",
    "receipt_line_sha256": "1f2ee14602b06fa004aaaa7c70ff2c5385c96d3f59d51f960cf3479891b63dfb",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 101,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "c1e48fadc85c3211ff73160e04ad8dd3c68129c688fe7ede73748662f125173c",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief and orders file, plus the staged validator tools named exactly in the brief's MAY-run list (run over private copies only, in a uniquely-named subdirectory of my own session scratchpad); wrote nothing under SP and ran no git"
   },
   {
    "execution_id": "ezek_author_p11_a1#e1",
    "receipt_file": "Ezek/author/ezek_author_attempt_receipts.jsonl",
    "receipt_line_sha256": "a62b1dab1bec18375d8779721f517cdd752c0a8367b566cf3d63824b78a16d5c",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 57,
     "qere": 5,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "a82aa3a89c34c2d8e2965d94a2710c53dd75000dfd7c86e9dd8f1c07249541e5",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named"
   },
   {
    "execution_id": "ezek_author_p02_a1#e1",
    "receipt_file": "Ezek/author/ezek_author_attempt_receipts.jsonl",
    "receipt_line_sha256": "203bd57e0d2669139fa4cab9fab3427edf8e56bc70e4f54a597ff3bb17311076",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 61,
     "qere": 6,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "8b7b8dadf2f4daa02d11fa8ffeb804ca9d54c7431e147d9c80814852b814c1cb",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief and orders file, plus private scratch paths I created myself"
   },
   {
    "execution_id": "ezek_author_p03_a1#e1",
    "receipt_file": "Ezek/author/ezek_author_attempt_receipts.jsonl",
    "receipt_line_sha256": "159a8219eef3498b004ea80d9522d06c01b08c64fbfe58d7da8c3aa6871ec300",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 108,
     "qere": 10,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "d5740573762acc137cb3d9f14ef800c07c80af1790fef8119c4fb35f3ffccc98",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named"
   },
   {
    "execution_id": "ezek_author_p06_a1#e1",
    "receipt_file": "Ezek/author/ezek_author_attempt_receipts.jsonl",
    "receipt_line_sha256": "12a591ee88c2390321f5e666a09fc3a8f69f3537499c146d94f8e750d610f219",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 97,
     "qere": 7,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "8a920d710cdcf8689a9485e653c9afd650a15efa11d1e60e01725f5a7238caaf",
    "e19_selfreported": "Violation to disclose, not concealed: EXACT-PATH LAW and the AFFIRMATIVE NO-CHECK LINE were followed for every substantive read (brief, orders, rulings, strategy, toolkit, Ezek_oshb.txt, Ezek_web_clean.txt, pmarks_Ezek.json, ezek_lib.py, rows_v2_swept_r3.jsonl — all opened by exact path or exact-path grep) and OUT was never checked for pre-existence, only written to directly. However, late in the self-check I ran a bare `ls -la` with NO path argument inside the shared OUT directory (ezek_author_out) to eyeball the just-written file's size; because no argument was given it defaulted to the working directory and returned a DIRECTORY LISTING, which surfaced two sibling filenames belonging to other author executions (ezek_author_p01_a1_e2.jsonl, ezek_author_p02_a1.jsonl) that are FORBIDDEN under the brief ('any other part's orders or deliverable'). I did not open, read, or otherwise use either sibling file — only their bare filenames were exposed in terminal output — and no write, deletion, or other action touched them. This is a real breach of 'never run any existence check, listing, glob or recursive search against it or any other directory' and I am not minimizing it. All other file-presence/integrity checks in this run (source rows digest, orders digest, output digest, JSONL line-parse count) were done by exact-path hashing/reading of one named file at a time, never a directory enumeration."
   },
   {
    "execution_id": "ezek_author_p08_a1#e1",
    "receipt_file": "Ezek/author/ezek_author_attempt_receipts.jsonl",
    "receipt_line_sha256": "3e6332af42b9c04f1e80ca3f9b6678b99ee9cc1c5e501c9890e39808f38898a1",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 70,
     "qere": 11,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "ebe5d27c12ae93324819906a622f715b20a34a43f872d5376223db0acd206b11",
    "e19_selfreported": "one deviation to disclose honestly rather than claim clean: I ran `ls *.py` inside SP/Ezek/tools once, to see the staged tool filenames -- every name it returned was already listed exactly in TOOLKIT.md's own staged-tools table, so nothing new was discovered, but it was a glob and I should not have run it under the no-glob instruction. No other listing, glob, or recursive search was run anywhere in the session; `ls -la` was used once on one exact named file (repair/rows_v2_swept_r3.jsonl) only to read its size, not to enumerate a directory; Grep was used only against specific named files (Ezek_oshb.txt, pmarks_Ezek.json, the orders file, and three tool .py files) to search their content, never to discover file names. Every substantive input path read was named in the brief or the orders file. All private scratch work stayed under my own session scratchpad in a uniquely named subdirectory; nothing was written under SP/Ezek at any point (all run_validator_suite.py reports landed beside their private-scratch inputs, not beside the real rows file), no git command was run, and no receipt was written."
   },
   {
    "execution_id": "ezek_stage_p0_a1#e1",
    "receipt_file": "Ezek/ezek_phase0_attempt_receipts.jsonl",
    "receipt_line_sha256": "90501940c1d34e71ad17143b7f8d6479cb56de06b6262f8432c9d9eadf9cea3c",
    "outcome": "LANDED - Ezekiel Phase 0 staging complete except TOOLKIT.md",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": null,
    "e19_selfreported": null
   },
   {
    "execution_id": "ezek_toolkit_a1#e1",
    "receipt_file": "Ezek/ezek_phase0_attempt_receipts.jsonl",
    "receipt_line_sha256": "322badadf9885b18ec2a31752bfbdc0bfa6eafae5f1155b3cdbb1fd5bb2ac2b2",
    "outcome": "LANDED - EZEKIEL PHASE 0 COMPLETE",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": null,
    "e19_selfreported": null
   },
   {
    "execution_id": "ezek_p0_recheck_a1#e1",
    "receipt_file": "Ezek/ezek_phase0_attempt_receipts.jsonl",
    "receipt_line_sha256": "e5afb800a87e2357dfa8b7697f436907c9a51d6a9f9df9ef14bbb593807df4f1",
    "outcome": "LANDED - fit_to_accept with two further findings",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": null,
    "e19_selfreported": null
   },
   {
    "execution_id": "ezek_p0_delta_a1#e1",
    "receipt_file": "Ezek/ezek_phase0_attempt_receipts.jsonl",
    "receipt_line_sha256": "09b8441d34d08fddc06c7c4d924ceb210c98e8d05d9142c8db6765b29f9efff9",
    "outcome": "LANDED - not_fit_to_accept, one blocker",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": null,
    "e19_selfreported": null
   },
   {
    "execution_id": "ezek_p0_r3_a1#e1",
    "receipt_file": "Ezek/ezek_phase0_attempt_receipts.jsonl",
    "receipt_line_sha256": "e423580bf1a3e6b6e2539516d66321343767cca6443d6646d1421a3fd49685f3",
    "outcome": "LANDED - fit_to_accept",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": null,
    "e19_selfreported": null
   },
   {
    "execution_id": "ezek_p0_repair_a1#e1",
    "receipt_file": "Ezek/ezek_phase0_attempt_receipts.jsonl",
    "receipt_line_sha256": "416264833b68002df3759b92110a1ef09c3b506ae03c0a79981a077fbbf7d686",
    "outcome": "LANDED - both cure claims ACCEPTED by _cure_verification.py",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": null,
    "e19_selfreported": null
   },
   {
    "execution_id": "ezek_toolkit_review_t1_a1#e1",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "0bf3e71eb2518ca7bf803131d9105818362180f366fa7d7e0d960ce61e9e1f49",
    "outcome": "REFUSED_NO_DELIVERABLE - declined to write inside the registry-protected worktree (Fable-5-only rule) before any owner exception existed; reviewed nothing, wrote nothing. Its refusal surfaced the authority conflict that OW-11 resolved.",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": null,
    "e19_selfreported": "ran no listing, glob or recursive search; two exact-path reads: ACTIVE_WORKTREES.yaml and its brief"
   },
   {
    "execution_id": "ezek_controlling_rulings_a1#e1",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "6a165b4e36c48f16dba6428a876da5d3824b16d9595b72291102718ff424fd8b",
    "outcome": "STOPPED_BY_ORCHESTRATOR - containment during the governance hold, before any deliverable; its only final text was a one-line start notice. Verified afterwards: no deliverable at its exact path.",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": null,
    "e19_selfreported": "NOT REPORTED - stopped before any record"
   },
   {
    "execution_id": "ezek_toolkit_review_t1_a1#e2",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "0ac3811b6baf05df0c34832e6a06489155f95ee5d945e48613b4df7e2fb20e29",
    "outcome": "LANDED_WITH_FORM_DEFECTS",
    "form_defects": [
     "artifacts_reviewed entry without a sha256: C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\ERROR_PATTERN_LEDGER.v1.md",
     "artifacts_reviewed: Ezek/tools/normalize_hebrew_in_json.py has CHANGED on disk since launch (now 07b58b19f0883ecd)",
     "artifacts_reviewed: Ezek/tools/_test_zone_tools_ezek.py has CHANGED on disk since launch (now e0686ef2f9a39e86)"
    ],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "2a341d583b3d8d68d8f2f1a953bc40150d8ace090e66b70b1616ef13bbc96a0b",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief (plus the brief-named ERROR_PATTERN_LEDGER.v1.md addendum for OW-11 context); all self-checks and private test vectors were confined to a uniquely-named subdirectory of my own session scratchpad, which I created and later removed myself - never inspected via listing, only written to and executed against by exact path"
   },
   {
    "execution_id": "ezek_controlling_rulings_a1#e2",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "99814194158416313b8e6e3d2b4e48212e3c141a55633525f43f801cd68f8d0c",
    "outcome": "LANDED_WITH_FORM_DEFECTS",
    "form_defects": [
     "inputs_ruled_on: Ezek/writer/ezek_tier0_suite_summary.v1.json has CHANGED on disk since launch (now c06f8b6ef0392c30)"
    ],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "d9c54100570edca3e84694703ad294e92c068788eae614e0fb38184168c80d1e",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief; the only directory operation was creating my own uniquely-named private scratch subdirectory (scratchpad\\ezek_rulings_7f3a9c2e); every self-check ran over my own scratch files and the deliverable's exact path; nothing written under C:\\wt\\logos-t423-m8-fable; no git run"
   },
   {
    "execution_id": "ezek_toolkit_repair_review_t2_a1#e1",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "aeba4dc33f6507a9a31966de675db93c85b3d856345739f612f77e4e6316de0c",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "c2c8350c52a8fd09a2f650b10706e2b0fd1d6bc1b8355996fb36eb9cae717976",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named"
   },
   {
    "execution_id": "ezek_toolkit_supplementary_review_t3_a1#e1",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "260d87c13d6993488c6acf5fc2014560893dd0b41b653031cabf59438c056d22",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "5da968734972c4838fcfe441b372a96d4f1448fd8051b229b2a8f7e832e001ae",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief, plus a handful of filenames taken verbatim from the text of already-pinned, digest-verified files (TOOLKIT.md's own tool-name table and citation_sweep.py's own source) where running an explicitly-authorized tool required them; all private-scratch work in a uniquely-named subdirectory of my own session scratchpad"
   },
   {
    "execution_id": "ezek_controlling_rulings_a1#e3",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "a0d977b0476ea3b90554be3924d2850fb507524d167e04385aac0de962052921",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "6ecd9578593d4f85d4cccf0ce9a77334797de4d3330b34e5558ec6228ae56b7d",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named; private scratch in ezek_e3_7f3a9c2e under my own session scratchpad; wrote nothing under the worktree, ran no git, wrote no receipt, executed no tool under the worktree"
   },
   {
    "execution_id": "ezek_toolkit_r4ii_review_t4_a1#e1",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "0a2ca94187b2e7e278b3cf6c586ef5565f8aadf2293635f4fc8c6c7d6c472518",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "5aef6d15cc9d4581b6cf1fc41688413b38bdc962e27be6c58664636a9086e373",
    "e19_selfreported": "ran no listing, glob, or recursive search against SP, the review output directory, or any other shared/forbidden directory; read only the exact paths named in the brief, my own governance-required files, and the ledger. One Get-ChildItem was run, scoped to my own private scratch subdirectory (ezek_t4_9f21ab) only, to confirm my own file copy succeeded -- the self-check E-19 itself carves out as permitted."
   },
   {
    "execution_id": "ezek_author_wave_spot_review_s1_a1#e1",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "6ac1372264d974c9fca0bcf0e9731cd7faf320e7ef1d5f81b67177c86ade9fc8",
    "outcome": "LANDED_WITH_FORM_DEFECTS",
    "form_defects": [
     "artifacts_reviewed: Ezek/ezek_cure_claims.v1.jsonl has CHANGED on disk since launch (now cfb20d1e3610db14)",
     "new_findings with a route outside author_fixup:pNN|orchestrator|controlling_agent: ['author_fixup:p01|author_fixup:p06|author_fixup:p07|author_fixup:p08|author_fixup:p09|author_fixup:p10|author_fixup:p11|orchestrator', 'author_fixup:p01|orchestrator', 'author_fixup:p03|orchestrator', 'author_fixup:p03|author_fixup:p05|author_fixup:p06|author_fixup:p08', 'author_fixup:p06|orchestrator']"
    ],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "b9aaae75325c76e4aa24e5bddb775ef4ceea9e35f8d041beebb0f0ba37886421",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named (brief inputs, the OW-11 ledger, and the governance files my policy requires, read by exact path or with a pattern search inside that single file); every tool ran over private copies with PYTHONDONTWRITEBYTECODE=1; the only write outside my private scratch is the deliverable"
   },
   {
    "execution_id": "ezek_controlling_rulings_a1#e4",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "792c5d841a480ecd8f09d9fc28a9233e5ab31085745a516a3a7ae9cb2a21d1d6",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "e342344c08f63a2e17c1b2cb4e27a2ae399a92c6e8d4fcfef6ca9349811b038b",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief, and every content search was a pattern over one named file; wrote exactly one file, the deliverable, directly to the named path outside the worktree with no existence check; executed no tool under the worktree, ran no git, wrote no receipt. One deviation disclosed rather than omitted: the JSON self-check script was written to a uniquely named ezek_e4_<random> directory under the user's TEMP root (C:\\Users\\lowel\\AppData\\Local\\Temp) rather than under the session scratchpad the brief names for private scratch; it created that directory with -Force, listed nothing, branched on nothing, and read only the deliverable by exact path."
   },
   {
    "execution_id": "ezek_controlling_rulings_a1#e5",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "9a294c70ed1c5b3a5ae9586cbe38c8930f0d1bc77a3d7359eedc9c1c16863dcd",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "4ced2df78bf10426902aa5dc2d3e3a6d94a3a7d71b80027e2180b3f2ed730f27",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief (every content search was a pattern over one named file); created no scratch subdirectory; wrote exactly one file at the exact deliverable path and read its size and digest by exact path only; executed no tool under the worktree, ran no git, wrote no receipt"
   },
   {
    "execution_id": "ezek_toolkit_install_review_t5_a1#e1",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "079c9f9fbe0bcf17f09d9e390e96df2161dc9e58a1d9bd5431bfe9397e8cd5d8",
    "outcome": "LANDED_WITH_FORM_DEFECTS",
    "form_defects": [
     "cure_claim_readiness entry for Q3-1 rebinds lacks a 64-hex sha256 or a boolean fit"
    ],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "02ff699e6e27cb96b43538d3fd82d2e291cba3501f7d280842e4bc9085854940",
    "e19_selfreported": "Ran no directory listing and no recursive search, and read only the exact paths the brief names; the installed tools read their own dependencies when run. One disclosure: a single shell glob ('claims/*.jsonl') expanded inside my own private scratch subdirectory ezek_t5_q7m3x9, to hash my two private claim copies. No glob, listing or search touched the worktree, the deliverable directory or any other directory. Every Python run had PYTHONDONTWRITEBYTECODE=1 set, and I wrote nothing under C:\\wt\\logos-t423-m8-fable. I ran no git, wrote no receipt and did not touch the registry."
   },
   {
    "execution_id": "ezek_controlling_rulings_a1#e6",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "76253e0916cb21b14d80ea5473c6437a27337d2963576e7230936d5892cefdda",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "ed5d714518b5f7a09edeb593dc0982cc1301039be66ff3924f737bfa77282113",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named (every content search was a pattern over one named file; one in-file scope deviation disclosed: #e4 read as one contiguous range 339-486 covering the four named sections and their neighbours, only the four relied on); no private scratch subdirectory was created; wrote exactly one file, the deliverable, at the exact path named, and read its size and digest by exact path only; executed no tool under the worktree, ran no git, wrote no receipt"
   },
   {
    "execution_id": "ezek_controlling_rulings_a1#e7",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "88b6eeed64e3136a6f5877159c2580eb00ed40dc6b93b310f5325449d8b5a173",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "2f83b81c5dbaefd00c1489607114e0c766fe9b95c86dad23b3773ccc034c1e9c",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief (plus my own private scratch file and my own deliverable, by exact path); wrote nothing under C:\\wt\\logos-t423-m8-fable; ran no git; wrote no receipt; the only writes are the deliverable and one private scratch script under ezek_e7_7c3f9a2e in my own session scratchpad; all input digests re-verified unchanged after writing"
   },
   {
    "execution_id": "ezek_toolkit_tf3_review_t6_a1#e1",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "08c209bf7db79b8ce4383afca879e54734b4d87b89c436f809402e6c28692ba8",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "7e9c36a46cfbc0916cf23259d468e909612dd8acdb913ac35415a37cae26a181",
    "e19_selfreported": "ran no listing, no glob, no recursive search against the deliverable directory, SP, or the worktree; read only the exact paths named in the brief (or, for check_register.py/check_web_quotes.py, the exact path named by an artifact_path field inside a pinned input, as part B required). One `ls` was run once against my own private scratch subdirectory only, to confirm copied files existed before running the verifier over them."
   },
   {
    "execution_id": "ezek_controlling_rulings_a1#e8",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "6738f54419f107061abb77c5ce25c76a2b454f7941334561438529171ad420ca",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "bc8be4b09e01c6d9d6eb17feba921a3f56f3a45601fd04b891ccb0bb95e2f040",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named (Read, Get-FileHash/Get-Item -LiteralPath, ConvertFrom-Json over exact paths, one single-file pattern search of the verifier with no glob, read-only python over the two exact claims-file paths); the deliverable's size and digest were read by exact path; one private verifier copy and one synthetic artifact were written in my own scratch subdirectory ezek_e8_i6g59jy1; nothing under C:\\wt\\logos-t423-m8-fable was written; no git; no receipt"
   },
   {
    "execution_id": "ezek_fixup_wave_review_s2_a1#e1",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "56e2ab4e2c4bdfb877cdff9b7e843e73574fce155eca745af6a7c63399e1f243",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "f57bfd0b84d3a42a3199ad1919349bf6c644b71d9e0db8c72f5bd9f81df600e8",
    "e19_selfreported": "ran no listing, no glob, no recursive search, my own scratch included; the one breach is the Test-Path existence checks on subdirectories of my own private scratch disclosed above. I read only the exact paths the brief names, the governance files, the ledger, plus these paths taken from pinned inputs' own fields or code: SP\\Ezek\\verse_inventory.json cf48cac0132d0d06a1b5f7c3cb1e7fb437aebfcaa33a6272a2c8894129067a99 (FIXUP_BRIEF.md table), SP\\Ezek\\tools\\verse_map_web.json bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98 (rows_v3_cwo18.manifest web_text.verse_map_sha256), SP\\Ezek\\tools\\check_language_zones.py 6807b3b7b19000cb08a508ffb2b142959a8f275ceba12da0fd2bcd357efbc828 (cwo13/cwo18 manifests probe.tools_sha256), SP\\Ezek\\web_mt_verse_check.json c122c2ee1bac34317bfac8cd31442a659b071ae854c5079fd7b685e7935e4ed7 (ezek_lib.py code), SP\\Ezek\\tools\\verse_map_oshb.json 408b7ee74564aef902c5fc539d6577f7708fa9aa839c993ce6281d86dc3a7901 (ezek_lib.py and citation_sweep.py code)"
   },
   {
    "execution_id": "ezek_controlling_rulings_a1#e9",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "d11d86a6285136638e0cccad32b41febcb1a2606d0696d006854acf75be9385c",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "81057c53c1875b84bbf81bcffeab92741fb410f6f4c1920799016defc435ab80",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief, the three governance files my policy requires, and the ledger at its named path; content searches ran only inside single files opened by exact path (the ledger; private copies of check_register.py, check_web_quotes.py, _land_author_part_ezek.py, _apply_author_wave_ezek.py); private copies were created in ezek_e9_k7q2m9xv under the session scratchpad with New-Item -Force and Copy-Item by exact path, never tested for, every copy digest-equal to its SP source; the deliverable directory was written to directly and never checked; nothing written under C:\\wt\\logos-t423-m8-fable; no git; no validator run; no receipt; no registry write"
   },
   {
    "execution_id": "ezek_fixup2_wave_review_s3_a1#e1",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "82ef01ac2f53d1f9ba08d719aa7047cf0e51dc8e86b508c91b93326f93375034",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "41a20205c0c606bdda922fff06545bf0a9c08bf337bf29f147ffd0787d1993d7",
    "e19_selfreported": "ran no listing, no glob, no recursive search, my own scratch included; read only the exact paths named in the brief's table, plus the governance files my policy requires and the OW-11 ledger. Grep was used only on exact file paths (the registry, the ledger, private copies of book_strategy_Ezek.md, ezek_lib.py, check_marks.py and _land_author_part_ezek.py). No path was taken from a pinned input's own field; the tools I ran loaded only table-named data files from private copies. The private directory was created with New-Item -Force, and the deliverable was written directly to its named path, then stat-ed and hashed by exact path."
   },
   {
    "execution_id": "ezek_controlling_rulings_a1#e10",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "fbab90fa28687646c722cad689ce735875231aded3f903aaf586d0ce69fe4863",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "f3588288892a41c4d8f9df47f80d23929bbe666eb123c95888dcfe472d7689f4",
    "e19_selfreported": "ran no listing, no glob, no recursive search, my own scratch included; read only the exact paths named in the brief's table and authority paragraph, the governance files my policy requires (ACTIVE_WORKTREES.yaml, WORKSPACE_LIFECYCLE.md, WINDOWS_ADAPTER.md) and the ledger at its named path; content searches ran only inside the ledger opened by exact path (for the OW-11 and OW-10 line numbers); the private copy of rows_v5 hashes 41b19ad9874dbb56d53b5317572fff6f90879b9b297021e7afc3300dead3c8f2, equal to its source; nothing written under the worktree; no git; no receipt; no registry write"
   },
   {
    "execution_id": "ezek_fixup3_wave_review_s4_a1#e1",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "64e04ecf4c08789a488ff1d551cd5fa2a57da1bcd42c29246e6ace60266871f0",
    "outcome": "STOPPED_AT_FINAL_MESSAGE - the execution made 95 tool calls and wrote a complete deliverable reviewing the applied corpus's exact bytes, using the corrected deliverable schema the orchestrator sent mid-flight, and the runtime then killed it as it emitted its final message (API rate_limit, HTTP 429: the account's claude-fable-5-1 usage credits were exhausted). NO self-authored OW-8 record exists, in the notification or anywhere in the preserved transcript, so this execution is NOT LANDED.",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": null,
    "e19_selfreported": "none: the execution was stopped before its self-report"
   },
   {
    "execution_id": "ezek_controlling_rulings_a1#e11",
    "receipt_file": "Ezek/ezek_rulings_attempt_receipts.jsonl",
    "receipt_line_sha256": "274df72930e450ee553f5d164d99a4e139a8ee8c6a243ccb77fea8f21876b780",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "a738e182aaec269ce202774e2f50649d88e20e54561d26e969ec8bfc05248cc9",
    "e19_selfreported": "I ran NO listing, NO glob, NO recursive search and NO directory existence check at any point, my own scratch included; the one directory I created (ezek_e11_q4m8zt2c under the session scratchpad) was made with New-Item -Force, and the deliverable's directory was addressed with os.makedirs(exist_ok=True), neither tested for. I opened only the brief's table paths and its authority-paragraph ledger, the three governance files my policy requires, and one path outside the table, SP\\Ezek\\ezek_residual_gram_families_v6.v1.json, named with its digest by the orchestrator's mid-execution message and hashed equal before reading. Content searches ran only inside single files opened by exact path. Private copies were made by Copy-Item by exact path and each hashed equal to its source. No transcript, forbidden lane, receipt, evidence note or fix-up deliverable was opened; no _apply_/_build_/_cwo/_land_/install/patch script and nothing with --write was run; exactly one file was written outside my scratch, the deliverable; nothing under the worktree; no git; no validator; no receipt; no registry write. ON THE CORRECTION MESSAGE: it reached me BEFORE I ruled S4-GRAMS and before the deliverable was written - it arrived while my third fact-check script was being written, after my second script had already printed the v6 suite report's ngram7.worst_reuse showing five grams at 9 rows including 'no k q or paseq falls in', which I had already noted as a third family S4-11 did not name. I re-derived all three families myself from rows_v6 by my own token pass and found them equal to the artifact's and the message's; the ruling rests on the suite report and my own pass, with the artifact bound as agreeing evidence."
   },
   {
    "execution_id": "ezek_author_fixup_p05_a1#e1",
    "receipt_file": "Ezek/fixup1/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "03aea0341086f22d0c4ae6dfbbb8c6d2c3353ec45aa07e85403b843d4dc0f9ad",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 13,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "90631955302f25f69f478fba940b9393a162916e1b10681082852ce4dead544b",
    "e19_selfreported": "ran no listing, no glob, no recursive search on the output directory or any other directory; read only the exact paths named in the brief, the orders file, and the brief's staged-tools table (tool scripts invoked by exact path); two Grep calls each targeted a single named file's content (pmarks_Ezek.json, ezek_controlling_agent_rulings.v1.json) for exact-string lookups, never a directory or a glob pattern"
   },
   {
    "execution_id": "ezek_author_fixup_p04_a1#e1",
    "receipt_file": "Ezek/fixup1/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "0f42f71ecbac2f3908995fb606ceff68153cad85c2107ff6a245861a9db4a747",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 5,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "646461b1b38e361d3436bdeaad5e60a2113c13c2eac36cabed771546bc2df335",
    "e19_selfreported": "ran no listing, no glob, no recursive search, at any point, against the output directory or any other directory; read only the exact paths named in the brief and orders file (plus the six named ruling ids and the seven named staged tools), located specific lines inside those named files with grep/read by content pattern rather than by enumerating files; all self-check tool runs were over private copies in my own uniquely named scratch subdirectory"
   },
   {
    "execution_id": "ezek_author_fixup_p09_a1#e1",
    "receipt_file": "Ezek/fixup1/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "cd934892c5b3c87cebdb8b9e1f1e096ff70467a67b867c4992d6f7bb69a77965",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 39,
     "qere": 8,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "c2b58e2c589c33fe8d79b5b98f6cc3ce8276bf2b10a919c41cceba987808a123",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named"
   },
   {
    "execution_id": "ezek_author_fixup_p11_a1#e1",
    "receipt_file": "Ezek/fixup1/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "143416cf6fe7f5d21c6b29f742e51cbd735fc9165f52a5d4e49cefdbdf257c2b",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 33,
     "qere": 3,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "9f27645d4b799cfb7789d73f491b842b5ae02eee6188f5ca422aff808a1e6286",
    "e19_selfreported": "ran no directory listing, no glob, no recursive search, on any directory, at any point. Every file opened was named exactly in the brief or in the orders file (or, for the tools, named exactly in the brief's staged-tools table). Grep was used twice as an exact-file content search only -- inside the one rulings file the brief names, to locate ruling ids R1/R2/P2/P4/P5/G12 the brief instructed me to read in full; and inside the one MT text file the brief names, to pull three exact verse lines (Ezek.45.18, Ezek.46.21, Ezek.48.1) -- never to list or search a directory. All self-check tool runs and intermediate files were written under my own private, uniquely named scratch subdirectory (ezek_fixup_p11_q7m3) of my own session scratchpad, over private copies, never under SP. I wrote nothing anywhere under the worktree and ran no git. My one write outside that private scratch was the deliverable, written directly to the exact output path named in my launch message, with no existence check, listing or glob run against its directory before or after the write; its size and digest were read afterward by exact path only (wc -c / sha256sum on the named file, never a directory listing)."
   },
   {
    "execution_id": "ezek_author_fixup_p01_a1#e1",
    "receipt_file": "Ezek/fixup1/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "41e48a3c7eb11075994015c498aa218fe4e3b370ddb1ad4c64ecacd3078746d9",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 56,
     "qere": 3,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "b07a6f017e330c93109a370f7ce801d3958d13a3b10c1b9f11d62c2c3af28e90",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief, the orders file, and the brief's pinned-inputs table"
   },
   {
    "execution_id": "ezek_author_fixup_p07_a1#e1",
    "receipt_file": "Ezek/fixup1/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "49b017b4b7e4da96891b3d3e7887e9652ff00800264018d81458cd17ae635a9c",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 32,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "3da5edd293ab6c09fe318931a26ad8c2325eb122bf9f13abfcfbc8dd01d02a34",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief and orders file (plus tool source files explicitly authorized in the brief's MAY-run list, opened by exact path to learn their CLI usage); one Get-ChildItem was run, scoped only to my own newly-created private scratch subdirectory immediately after populating it, to confirm the copy succeeded -- never against the output directory or any SP path; the output file was written directly to its exact named path and its size/digest were read by exact path (Get-FileHash / Get-Item.Length), never via a directory listing"
   },
   {
    "execution_id": "ezek_author_fixup_p10_a1#e1",
    "receipt_file": "Ezek/fixup1/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "285bf23fe3f9edede2d5f3e997e78d37f5e2b2072cd5755c60764ba26632f931",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 43,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "f6e76af7295c08526e29fcfe2da94d57b3387909c2c5eb7924fbab35633a8fdd",
    "e19_selfreported": "read only the exact paths named in the brief, the orders file, and the brief's own pinned-inputs table; ran no listing, glob, or recursive search against SP, the OUTPUT directory, or any other shared/other-lane path. One exception, disclosed for honesty: immediately after `mkdir` I ran a single `ls -la` on my own freshly-created, empty, uniquely-named private scratch subdirectory to confirm its creation, before any content existed there; it enumerated nothing about SP, the OUTPUT directory, or any other agent's work, and I did not repeat it."
   },
   {
    "execution_id": "ezek_author_fixup_p06_a1#e1",
    "receipt_file": "Ezek/fixup1/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "b289b3cef1a824697790d085e8f92aba0a470984c6a8d6617159022ff499421c",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 99,
     "qere": 7,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "72772bc7afce7657e24856a4b72245c0ae057c641175fc7195331f7938308446",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief, the orders file, and paths I created myself under my own private scratch subdirectory (ezek_fixup_p06_7f3a9c2d) and the pre-existing OUT subdirectory; verified this with a post-hoc grep of my own scripts for any Glob/ls/dir/Get-ChildItem/os.listdir/glob. call, none found"
   },
   {
    "execution_id": "ezek_author_fixup_p02_a1#e1",
    "receipt_file": "Ezek/fixup1/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "1e4755dd256e6b52760d131fe5f0597238abb3c43e29f600030aa91a41ced1cc",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 62,
     "qere": 10,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "da925c33fc1d4ed633236d000150793a7243f24494dd898cbea9cfa78001c5f1",
    "e19_selfreported": "ran one listing in error early in the task, before creating my own private scratch subdirectory: `ls` against the shared session scratchpad ROOT (not my own output directory, not SP, not the worktree) surfaced filenames of what appear to be orchestrator working files (_state.json, _e3_queue_and_brief.py, etc.) and an 'SP' entry; I did not open, read, or act on any of those files, and made no further listing, glob or recursive search of any kind for the rest of the task. All other reads were exact-path opens of files named in the brief, the orders file, or my own private subdirectory (ezek_fixup_p02_7f3q2k, under my own session scratchpad, never under SP or the worktree). My deliverable's size and digest were read by exact path (Get-Item/Get-FileHash), never by listing a directory."
   },
   {
    "execution_id": "ezek_author_fixup_p03_a1#e1",
    "receipt_file": "Ezek/fixup1/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "d182bc8cf770661f749e96266019277d708db2a86cad5cd3234d270c3a36617b",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 75,
     "qere": 8,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "15c5a32c59588122a03f3000a66cff5abf8e032a157b17e874a10ac6b252499f",
    "e19_selfreported": "ran no listing, no glob, no recursive search, no directory enumeration against any path; opened only the exact paths named in the brief, the orders file, and (for the six rulings the brief names by id) the rulings file at its pinned digest; my private scratch subdirectory (ezek_fixup_p03_x7k2m9, under my own session scratchpad) held every working/private-copy file and was never listed either - each file in it was written or read by its own exact name"
   },
   {
    "execution_id": "ezek_author_fixup_p08_a1#e1",
    "receipt_file": "Ezek/fixup1/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "47dec81d73d60e5ff4134b2c8c462ae09a1178bbbc783dd955df3af84e5d8ca3",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 68,
     "qere": 11,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "b71891e5257283d7dd08e3fa3b3a069a28ae11b77e73c09e394c01e94953e25e",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named"
   },
   {
    "execution_id": "ezek_author_fixup2_p06_a1#e1",
    "receipt_file": "Ezek/fixup2/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "e086fa3855bc12a0a1f895f205e39959336b4e547e7eb170148737c23decb2b1",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 6,
     "qere": 2,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "4860b06676883edb37850dd70364be77aed2f5e831a4f994d121eb876ca986c8",
    "e19_selfreported": "Ran one directory listing (ls -la) against my own private scratch directory early in setup, in violation of the brief's AFFIRMATIVE NO-CHECK / EXACT-PATH LAW; caught immediately and disclosed. No listing, glob, or recursive search was run against OUT\\ or the worktree at any point, and none was run anywhere after that single lapse; every other path opened was named in the brief, the orders file, the required governance files, or (for check_tiling.py's CLI contract) a staged tool file explicitly named as usable in the brief."
   },
   {
    "execution_id": "ezek_author_fixup2_p09_a1#e1",
    "receipt_file": "Ezek/fixup2/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "f4564bc0342f36287cb7938710e9b8777ae1224d47d462d375b906de014230a5",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 37,
     "qere": 5,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "9543706851db344af7a21535d8436b3f09217424c7cd21083780c40ac980fe42",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief, the orders file, and the required governance/ledger files"
   },
   {
    "execution_id": "ezek_author_fixup2_p07_a1#e1",
    "receipt_file": "Ezek/fixup2/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "b6ed5c6691d8c1a07a056b02b5b97cb442b01e16742e1d3ab2aa285cffd2d324",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 56,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "c51ab2d6066d6143809ee6dd14340d8984c8997506df5c90fe0c32e4274e1193",
    "e19_selfreported": "one Glob call was run against the exact already-named tool path C:\\wt\\...\\Ezek\\tools\\run_validator_suite.py before invoking it (no wildcard, no directory contents beyond that path exposed) -- a violation of the no-existence-check/no-glob line, disclosed here rather than omitted. No other listing, glob, or recursive search was run anywhere, including my own scratch. All other paths were opened by their exact named path."
   },
   {
    "execution_id": "ezek_author_fixup2_p11_a1#e1",
    "receipt_file": "Ezek/fixup2/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "83e39e5211aaad32e9fc462db54e58279c1d483fab810be8069d0772f93385a1",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 14,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "0ba78986e6b3b8a59510bbb248044e0fa5236de622279ac8007cdc94769a8407",
    "e19_selfreported": "UNAVAILABLE as a structured field; the final message's prose is the agent's only statement on E-19, and it is kept verbatim in final_message_verbatim"
   },
   {
    "execution_id": "ezek_author_fixup2_p01_a1#e1",
    "receipt_file": "Ezek/fixup2/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "a1f65f4e878a91a897d4b61b9bdcb56ee221c788bf62542a57a9aa2f5796ccc2",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 60,
     "qere": 5,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "6e7fe08ce8c76faf595f39f5688f6fe7bd6873133e45e1bbcf0340f609929cfa",
    "e19_selfreported": "ran no listing, no glob, no recursive search, anywhere, including my own scratch; every path read was named in FIXUP2_BRIEF.md, orders_ezek_author_fixup2_p01_a1.json, or (for governance) ACTIVE_WORKTREES.yaml's own required-reading chain and the OW-11 ledger path named in the brief; Grep calls were content searches scoped to one exact already-named file, never a directory listing"
   },
   {
    "execution_id": "ezek_author_fixup2_p04_a1#e1",
    "receipt_file": "Ezek/fixup2/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "a65b1dcccebb63d89212569e70451674cc4e62f78c7dff33945ddceac3fb45d3",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 35,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "ab24d3d97b1fefcd30dad5620a5650e11d25e68ec1318f86012d1130c86722f2",
    "e19_selfreported": "ran no listing, no glob, no recursive search, anywhere, own scratch included; every path read was named in the brief, the orders file, the pmarks/toolkit pinned-input table, or the OW-11 ledger path the brief itself names for verification"
   },
   {
    "execution_id": "ezek_author_fixup2_p02_a1#e1",
    "receipt_file": "Ezek/fixup2/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "7151006f1abefdada05a88b63c29530c2ec992ed0af7745c9169dbd969f9917a",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 23,
     "qere": 5,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "f2ed1dbd3b869b629dc98648978751ad11f866f2fbcde72aac86a477ce163948",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named in the brief, the orders file, or the OW-11 ledger and table; the OUT execution subdirectory was written to directly per the affirmative no-check line"
   },
   {
    "execution_id": "ezek_author_fixup2_p03_a1#e1",
    "receipt_file": "Ezek/fixup2/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "7911666237209e41cf2b911b2104b4f785ed5f5f2411e1fc916845f4fa59bdfe",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 82,
     "qere": 9,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "912070b8a01c48928f5ea4730d088614106a785b8b541864be6cd5720aa7351f",
    "e19_selfreported": "ran no directory listing, no glob, and no recursive filesystem search anywhere, including my own scratch/output directories; every path opened was named in the brief, the orders file, the OW-11 ledger path in my launch instructions, or came from a pinned input's own field (pmarks_Ezek.json's marks dict, looked up by the exact verse keys my orders' mark_items name); a few Grep calls were used strictly as in-file navigation within one already-named file (never across a directory) to jump to a passage without reading the whole file"
   },
   {
    "execution_id": "ezek_author_fixup2_p08_a1#e1",
    "receipt_file": "Ezek/fixup2/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "10f50fdbf6cea97e8e19c897aa8b992536e060a746421ec729da309c9c846ef5",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 46,
     "qere": 2,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "c7ed046547406ba73a1281577b4530bd531310e6ba7045d782cb9c8b59e1c9b3",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named"
   },
   {
    "execution_id": "ezek_author_fixup3_p01_a1#e1",
    "receipt_file": "Ezek/fixup3/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "d2799a2bcd14021d7dd7b9bde1f4403ccdda81f69fac00e52f08f3d96035c843",
    "outcome": "REFUSED_NO_DELIVERABLE - declined before any tool call. It judged the task a mismatch with the orchestrating session's working directory, read the OW-11 record as a self-referential authorization it could not verify, and read the E-19 no-listing lines as an instruction to disable its own verification; it read no brief, orders or ledger, and wrote nothing.",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": null,
    "e19_selfreported": "prose final message; see the layer-C note"
   },
   {
    "execution_id": "ezek_author_fixup3_p01_a1#e2",
    "receipt_file": "Ezek/fixup3/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "26c54556d3d4d6c0392f980b9fe50f8b443eb1c6163a9ec05ca219ab4a5050e8",
    "outcome": "REFUSED_NO_DELIVERABLE - declined before any tool call, after the context paragraph. It read the launch message as an injection pattern: an authorization it could not verify; the no-listing and no-memory lines as suppression of verification and transparency; and a mismatch with the orchestrating session's working directory and branch. It asked the owner to confirm directly in chat, and to allow directory and existence checks. It read no brief, orders or ledger, and wrote nothing.",
    "form_defects": [],
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": null,
    "e19_selfreported": "prose final message; see the layer-C note"
   },
   {
    "execution_id": "ezek_author_fixup3_p03_a1#e1",
    "receipt_file": "Ezek/fixup3/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "99537553383f55da2b2df96effca59a5ac06ee386c5e4fc3a0a10193218ff704",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 68,
     "qere": 7,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "1d30a2239e24275d3582af5d4191357c8c1b2800d8c7fb415d08cfe0deaeddd4",
    "e19_selfreported": "ran no listing, no glob, no recursive search, no directory existence check, no memory write; read only the exact paths named (the brief and the orders file); all other file access was hashing or stat-by-exact-path of files I was about to read or had just written, or python opening the orders file by its exact named path"
   },
   {
    "execution_id": "ezek_author_fixup3_p07_a1#e1",
    "receipt_file": "Ezek/fixup3/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "2d82b2e996b385b4762426b349bfbb435e5c725a6ed0ad1af74b48d0669f4d90",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 40,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "570396575110718e9cdf73e0eeb5f75bad13d787fb04e086ed9816e12b136f2a",
    "e19_selfreported": "NOT a clean run: two Glob tool calls were made BEFORE opening the brief/orders, while independently assessing whether the launch text's authority claims were genuine (one wildcard glob over C:\\Users\\lowel\\.agent-governance\\*, one glob on the exact path of FIXUP3_BRIEF.md) -- both read-only, filenames only, no content opened. After reading the brief's E-19/exact-path law, no further listing, glob, or directory-existence check was run anywhere, including my own private scratch. Two Grep content-searches were run against exact-path files already being read (the orders JSON, to jump to a line range; the ledger, to locate the OW-11 heading) -- in-file content search, not directory listing. No memory file was written; every write landed under my own private scratch subdirectory or the named deliverable path."
   },
   {
    "execution_id": "ezek_author_fixup3_p02_a1#e1",
    "receipt_file": "Ezek/fixup3/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "7d6303a74552b5d0ee8a5924d92344f3df2d656cef0132cf201fc7709bdff86b",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 25,
     "qere": 4,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "351b68f7a1627aeb22c3e914fbf12902f9ee998927ea56abff763931440b884f",
    "e19_selfreported": "ran no listing, no glob, no recursive search, no directory existence check, no memory write outside this record; read only the exact paths named in the brief, the orders file, the pinned-input table, or the OW-11 ledger; the one out-of-scope write (a throwaway diagnostic file outside my private scratch subdirectory) was self-caught and deleted before use, disclosed above rather than concealed"
   },
   {
    "execution_id": "ezek_author_fixup3_p04_a1#e1",
    "receipt_file": "Ezek/fixup3/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "78066774c31bb8d9fd395b4f66c5183c8d8cb31b37c323522106bf1b81d250ed",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 35,
     "qere": 0,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "dfa0d9e4a4f0726cee3e65535cac4be37d2d232e64d6a6f0e7e005c372d25e8d",
    "e19_selfreported": "ran no listing, no glob, no recursive search, no directory existence check, no memory write; read only exact paths named in the brief, the orders file, the governance files my policy requires, and the ledger path the brief names; the one path taken from a pinned input's own field (rows_v5_cwo23.jsonl's path, named in orders.sources.rows) was opened by that exact path, hashed, and is disclosed above"
   },
   {
    "execution_id": "ezek_author_fixup3_p08_a1#e1",
    "receipt_file": "Ezek/fixup3/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "208a5d89cb73983bc1a0197fc76e3cfb3b262e10692c9e6a2101927a749e0bf0",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 34,
     "qere": 9,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "8fdcdea0c12f9498690a970eb18726e43a7b679fe91cdefbdf6154f80e515925",
    "e19_selfreported": "ran no listing, no glob, no recursive search, no directory existence check, no memory write; read only the exact paths named in the brief, the orders file, the AUTHORITY paragraph's ledger pointer, and pinned-input fields within those files (rows_v5_cwo23.jsonl, ezek_device_inventory.json, Ezek_oshb.txt, Ezek_web_clean.txt, and the staged tools in SP\\Ezek\\tools\\); private scratch and the deliverable directory were created with mkdir -p (POSIX equivalent of New-Item -Force / os.makedirs(exist_ok=True)), never a listing or existence check"
   },
   {
    "execution_id": "ezek_author_fixup3_p01_a1#e3",
    "receipt_file": "Ezek/fixup3/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "f2424fb12761561341ab5fc07b6f128bef3734a967488769364e5ceb5c1db3dc",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 31,
     "qere": 1,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "13192df7af821d79c430631d261b31d1025eacc613b103c619f022926956c133",
    "e19_selfreported": "ran no listing, no glob, no recursive search, no directory existence check, no memory write; read only the exact paths named. Grep calls targeted exact FILE paths only. Tool files outside the pin table were those in the brief's MAY-run list, hashed and listed in sources. One disclosed deviation: a setup script was written at the session scratchpad root, then moved into the private subdirectory (see unresolved_uncertainty[0]). No git was run, no receipt was written, and nothing was written under C:\\wt\\logos-t423-m8-fable."
   },
   {
    "execution_id": "ezek_author_fixup3_p03_a1#e2",
    "receipt_file": "Ezek/fixup3/ezek_author_fixup_attempt_receipts.jsonl",
    "receipt_line_sha256": "a575334bdf8cf3fbd2ef73d6522bf043ce8da316b20e015c94612d0c8adaddd7",
    "outcome": "LANDED",
    "form_defects": [],
    "local_tiling": "PASS",
    "e01_normalizer": {
     "ok": 68,
     "qere": 7,
     "fixed": 0,
     "defect_count": 0
    },
    "deliverable_sha256": "86e964b79f4e17e43a1561e1499f2a88cd22a7425c78c8c4ce5f7ca8e3840aa6",
    "e19_selfreported": "ran no listing, no glob, no recursive search, no directory existence check, no memory write; read only the exact paths named. Every path I opened is named in my brief, my orders file, my launch message, or the ledger the authority paragraph names, with one exception taken from the brief's own MAY-run tool list rather than its pin table: Ezek/tools/ngram7.py, opened by exact path, hashed (fe25efc22a0b01b099a8066b97a377ae125df349439d348074cb4fc5b04d271c) and disclosed above, read so the gate's tokenisation could be replicated exactly. My private scratch subdirectory and the per-execution output subdirectory were created with os.makedirs(exist_ok=True) and never tested for. Every self-check is a stat or a digest of a FILE by exact path. Every tool ran over PRIVATE COPIES in my own session scratchpad; nothing was written anywhere under C:\\wt\\logos-t423-m8-fable, no report landed under SP, I ran no git and no validate_workspace_policy.ps1, and I wrote no receipt and no registry entry."
   },
   {
    "execution_id": "ezek_writer_p04_a1#e1",
    "receipt_file": "Ezek/writer/ezek_writer_attempt_receipts.jsonl",
    "receipt_line_sha256": "37d0d0cf4d5b55ba0cedcfe2e451a7748fc8b5dad8615d0d708d778d6b78aff1",
    "outcome": "LANDED",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "7905e41cc77f2a78c23887b92eda1a873625760433cd14a754049bdeb8141b8e",
    "e19_selfreported": "ran no listing, no glob, no recursive search; the five tool paths were attempted individually by exact path and found absent"
   },
   {
    "execution_id": "ezek_writer_p10_a1#e1",
    "receipt_file": "Ezek/writer/ezek_writer_attempt_receipts.jsonl",
    "receipt_line_sha256": "e0c78fc8c714ed6462e172301450a6b6fc094c6803fb3385e0fe2fe71fbb9420",
    "outcome": "LANDED",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "4797fc9979142bdb1073ed4622efb498a1fb74899603b1847f5df0b68f696b47",
    "e19_selfreported": "PARTIAL COMPLIANCE, DISCLOSED: after the deliverable was already written, ran one `ls -la` against the shared writer-output directory, surfacing the filenames (not contents) of draft_p01.jsonl and draft_p04.jsonl. Neither was opened."
   },
   {
    "execution_id": "ezek_writer_p06_a1#e1",
    "receipt_file": "Ezek/writer/ezek_writer_attempt_receipts.jsonl",
    "receipt_line_sha256": "2b23bb959f2637b75e2acbffbc7f030cef1336fd5619e06d53dbbd5f799dd72f",
    "outcome": "LANDED",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "94d2b22de4c2787d48345b8e0f7955fd57d922ff45b386b5cda6de3dab3b72b5",
    "e19_selfreported": "ran no listing, no glob, no recursive search — against the output directory or any other directory; read only the exact paths named above, plus my own private scratch subdirectory (session-scratchpad\\ezek_writer_p06_priv_scratch) which I created and worked in directly by name"
   },
   {
    "execution_id": "ezek_writer_p07_a1#e1",
    "receipt_file": "Ezek/writer/ezek_writer_attempt_receipts.jsonl",
    "receipt_line_sha256": "b05c4dcd013b7ded890cac59db79b42854296411367d27bba6f41a63c91f4a83",
    "outcome": "LANDED",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "457dbafb733ffd8e56ffd7b88f49a61445ce33b3902465cd0ee539054b240592",
    "e19_selfreported": "ran no listing, no glob, no recursive search, against the output directory or any other directory, at any point, including after writing; read and wrote only the exact paths named in the brief and in my launch message; the two content searches I ran (Grep) were scoped to single, exactly-named files (Ezek_oshb.txt, Ezek_web_clean.txt), never to a directory"
   },
   {
    "execution_id": "ezek_writer_p11_a1#e1",
    "receipt_file": "Ezek/writer/ezek_writer_attempt_receipts.jsonl",
    "receipt_line_sha256": "be18f9df8f2e270bedc2d6512df48a67a0bdaa6dc05dd9e3d13239ac6d661fff",
    "outcome": "LANDED",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "4818ebe88bb2338fdc61ba265b60008d11774ebca55b000fdc12a009bcded7d7",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read only the exact paths named"
   },
   {
    "execution_id": "ezek_writer_p05_a1#e1",
    "receipt_file": "Ezek/writer/ezek_writer_attempt_receipts.jsonl",
    "receipt_line_sha256": "bccc987cd9fc404f9cbeda817d0787e8f7521475c3ca0f25b0db7675c08b199f",
    "outcome": "LANDED",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "fe85d381f15db85ef5aa22b13eb40e8cad1e9d847efdfd169f96a262047893c2",
    "e19_selfreported": "ran no listing, no glob, no recursive search, against the output directory or any other directory, at any point in this task; read only the exact paths named above, plus wrote to and read back only the exact deliverable path and my own private-scratch script/copy paths that I created and already knew"
   },
   {
    "execution_id": "ezek_writer_p03_a1#e1",
    "receipt_file": "Ezek/writer/ezek_writer_attempt_receipts.jsonl",
    "receipt_line_sha256": "3694dda7afcb03e589772b15a6775229079ca96eb6394f5ebec311ca0cdaa2b9",
    "outcome": "LANDED",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "cddb2c0f9d2294f3917aee3fc26a184248556b2507cc78c49ccc44538ba0263c",
    "e19_selfreported": "I ran no listing, glob, or recursive search against the output directory or any other directory after the start of the work proper, and never against the output directory at any point. One exception, disclosed rather than concealed: my very first tool call was ls -la on the read-only source lane directory (sp_durable\\Ezek\\) to confirm it existed, before I had read the brief in full — a technical breach of the EXACT-PATH LAW stated in my own launch message, though it touched only the authorized read-only source lane (revealing filenames of artifacts I went on to read by exact path anyway), never the forbidden output directory or any other model's lane."
   },
   {
    "execution_id": "ezek_writer_p08_a1#e1",
    "receipt_file": "Ezek/writer/ezek_writer_attempt_receipts.jsonl",
    "receipt_line_sha256": "faa3465a0f3bae56ef10b8e48ed22cee386de664111f7454587478a2597f5d78",
    "outcome": "LANDED",
    "form_defects": null,
    "local_tiling": null,
    "e01_normalizer": null,
    "deliverable_sha256": "22c70e89b510dec7bed5895346da608f92a6917bf4c3d2eebf4464c6f1bffe21",
    "e19_selfreported": "ran no listing, no glob, no recursive search; read/opened only the exact paths named in WRITER_BRIEF.md and TOOLKIT.md (plus Ezek.11.19 inside the already-authorized Ezek_oshb.txt, for the brief-mandated 36.26/11.19 new-heart contrast); the deliverable was written directly to the named output path with no existence check before or after"
   }
  ]
 }
}
```

## 4. What the audit read

deliverables; layer-C evidence notes; layer A only where present
