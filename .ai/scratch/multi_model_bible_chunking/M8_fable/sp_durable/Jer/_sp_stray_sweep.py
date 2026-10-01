#!/usr/bin/env python3
"""Deterministic stray sweep of the shared SP/Jer tree (E-21 detector):
every file must match the expected-artifact allowlist; anything else is a
stray to inspect. Run at every wave close."""
import fnmatch
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

ALLOW = [
    # staged inputs + inventories (Phase 0)
    "Jer_web.usfm", "Jer_web_clean.txt", "Jer_oshb.txt",
    "book_observation.jsonl", "chapter_profile.json", "risk_signals.jsonl",
    "span_features.jsonl", "verse_inventory.json", "web_mt_offset_map.json",
    "web_mt_verse_check.json", "pmarks_Jer.json", "jer_device_inventory.json",
    "_inv_before_*.json",
    # plans, briefs, corpora (Phase 1-2)
    "writer_parts.json", "WRITER_BRIEF.md",
    "PRIMARY_BRIEF_LF.md", "PRIMARY_BRIEF_OL.md",
    "review_clusters.json", "flags_by_row.json",
    "draft_rows_combined.jsonl", "draft_rows_combined.jsonl.validator_report.json",
    # orchestrator probes/verifiers
    "_probe_phase0.py", "_phase1_partplan_probe.py", "_resume_smoke.py",
    "_wave_verify.py", "_phase2_build_clusters.py", "_pr_wave_verify.py",
    "_sp_stray_sweep.py",
    # subtrees
    "freeze/CYCLE_STATE.md",
    "tools/*.py", "tools/TOOLKIT.md", "tools/__pycache__/*",
    "tools/consonantal_index.json", "tools/verse_map_web.json", "tools/verse_map_oshb.json",
    "writer/writer_p[0-9][0-9].jsonl",
    "writer/writer_p[0-9][0-9].jsonl.validator_report.json",
    "reviews/rev_LF_c[0-9][0-9].json", "reviews/rev_OL_c[0-9][0-9].json",
    # peer round (r3 scoped) — added at primaries close, 2026-08-28
    "PEER_BRIEF.md", "peer_scope.json", "_peer_verify.py",
    "reviews/peer_[0-9][0-9].json", "reviews/peer_[0-9][0-9]_r[0-9].json",
    # remedy consolidation — added at peer-round close, 2026-08-31
    "_build_remedy_docket.py", "remedy_docket.v1.json",
    # boss round — added at boss-round open, 2026-08-31
    "BOSS_BRIEF.md", "_build_boss_docket.py", "_boss_verify.py",
    "boss_docket.json", "boss_docket_b[0-9].json",
    "reviews/boss_jer_b[0-9].json",
    # author wave — added at author-round open, 2026-08-31
    "AUTHOR_BRIEF.md", "_build_author_orders.py", "author_orders_summary.json",
    "author/orders_a[0-9][0-9].json", "author/author_a[0-9][0-9].jsonl",
    "_author_census.py",
    "author/jer_author_attempt_receipts.jsonl",
    "_build_current_state.py", "_safe_to_clear_check.v2_2026-09-04.py", "_apply_author_jer.py",
    "_build_repair_orders.py", "_book_repair_sweep.py", "_repair_stray_sweep.py",
    "_build_semcheck_slices.py", "_apply_repairs_to_shipped.py", "_update_dispositions.py", "_cwo_scan.py",
    "_build_r2_orders.py",
    "_build_cwo_orders.py", "cwo_orders.v1.json", "CWO_BRIEF.md", "cwo/orders_cwo_[0-9][0-9].json", "cwo/orders_cwo_[0-9][0-9]_c[0-9].json", "cwo/cwo_parity.v1.json", "cwo/jer_cwo_attempt_receipts.jsonl", "cwo/cwo_unify_c[0-9].jsonl", "cwo/cwo_[0-9][0-9].jsonl",
    "rows_v2.jsonl", "rows_v2.jsonl.validator_report.json", "_apply_author_report.json", "rows_v3.jsonl", "rows_v3.jsonl.validator_report.json",  # OW-2 backlog repair lane tools (2026-09-06)  # OWNER_REPAIR_ADVANCE_2026-09-06 item 4 (2026-09-06)  # item-6 carrier for the author lane, added 2026-09-05 (OW-4 resume)
    # OW-2 item-4 per-wave fresh-sweep runner — added 2026-08-31
    "_wave_repair_sweep.py",
    # OW-2C mechanical prompt verifier — added 2026-08-31
    "_safe_to_clear_check.py",
    "_safe_to_clear_check.v1_2026-08-31.py",
    "_book_repair_sweep.v2_2026-09-06_e24.py",
    "_dep_pin_check.py",   # E-25 dependency-pin reconciliation control, 2026-09-06 s3
    "_cwo_census.py",   # CWO-wave landing census, 2026-09-06 s3
    "_apply_cwo.py", "_apply_cwo_report.json",   # guarded CWO apply, 2026-09-06 s3
    "_build_lf_frame.py", "lf_support_sample.json", "_build_spot_scope.py", "spot_scope.json", "SPOT_BRIEF.md", "POSTCHECK_BRIEF.md", "_spot_verify.py", "spot/*", "postcheck/*", "rows_v3.jsonl.punct_e23.json", "_e23_rev.json",   # rev/spot/postcheck lane, 2026-09-07
    "MICRO_BRIEF.md", "_build_micro_docket.py", "_apply_micro.py", "spot/micro_docket.json", "spot/orders_micro_[0-9][0-9].json", "spot/micro_[0-9][0-9].jsonl", "_apply_micro_report.json", "rows_v4.jsonl", "rows_v4.jsonl.validator_report.json", "_e23_post.json", "_micro_census.py", "SIDECAR_BRIEF.md", "_finalize.py", "_close_book.py", "_cwo10_paseq_scan.py", "_cwo10_paseq_scan.json", "_cwo10_disposition.json", "rows_v5.jsonl", "rows_v5.jsonl.validator_report.json", "sidecar_src_[0-9].jsonl", "postcheck/postcheck_01.json", "FIX_BRIEF.md", "_fix_census.py", "_apply_fix.py", "_post_apply_checks.py", "_apply_fix_report.json", "rows_v6.jsonl", "rows_v6.jsonl.validator_report.json", "_e23_post_v6.json",   # bounded fix round after postcheck_01, 2026-09-07   # micro round, 2026-09-07   # pre-cycle-N sweep preserved verbatim (E-24 build), 2026-09-06   # pre-OW-3 checker preserved verbatim (baseline)
]

strays = []
for p in sorted(HERE.rglob("*")):
    if p.is_dir():
        continue
    rel = p.relative_to(HERE).as_posix()
    if not any(fnmatch.fnmatch(rel, pat) for pat in ALLOW):
        strays.append({"path": rel, "bytes": p.stat().st_size})
print(json.dumps({"sweep": "CLEAN" if not strays else "STRAYS_FOUND",
                  "files_checked": sum(1 for p in HERE.rglob("*") if p.is_file()),
                  "strays": strays}, indent=1))
sys.exit(1 if strays else 0)
