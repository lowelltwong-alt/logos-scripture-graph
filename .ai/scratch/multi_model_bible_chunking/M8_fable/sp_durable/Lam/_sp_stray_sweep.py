#!/usr/bin/env python3
"""Deterministic stray sweep of the shared SP/Lam tree (E-21 detector): every file must match the
expected-artifact allowlist; anything else is a stray to inspect. Run at every wave close."""
import fnmatch, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ALLOW = [
    # staged inputs + inventories (Phase 0)
    "Lam_web.usfm", "Lam_web_clean.txt", "Lam_oshb.txt", "book_observation.jsonl", "chapter_profile.json",
    "risk_signals.jsonl", "span_features.jsonl", "verse_inventory.json", "web_mt_offset_map.json",
    "web_mt_verse_check.json", "pmarks_Lam.json", "lam_device_inventory.json",
    # plans, briefs, corpora (Phase 1-2)
    "writer_parts.json", "WRITER_BRIEF.md", "PRIMARY_BRIEF_LF.md", "PRIMARY_BRIEF_OL.md", "PEER_BRIEF.md", "BOSS_BRIEF.md",
    "AUTHOR_BRIEF.md", "CWO_BRIEF.md", "SPOT_BRIEF.md", "POSTCHECK_BRIEF.md", "MICRO_BRIEF.md", "SIDECAR_BRIEF.md", "FIX_BRIEF.md", "lf_support_sample.json", "sidecar_src_[0-9].jsonl", "_e23_*.json", "_micro_census.py", "_fix_census.py", "_finalize.py", "_close_book.py", "_post_apply_checks.py", "_cwo_census.py", "_spot_verify.py", "_micro_key_unify_report.json", "_dep_pin_check.py",
    "review_clusters.json", "flags_by_row.json", "review_scope.json", "peer_scope.json", "boss_docket*.json", "remedy_docket.v1.json",
    "author_orders_summary.json", "cwo_orders.v1.json", "spot_scope.json", "author_overrides.json", "boss_docket_overrides.json",
    "draft_rows_combined.jsonl", "draft_rows_combined.jsonl.validator_report.json",
    # two-digit versions: the book passed rows_v9 during the OW-6 fix round and the single-digit pattern
    # would have quietly reported every later corpus as a stray
    "rows_v[0-9].jsonl", "rows_v[0-9].jsonl.validator_report.json",
    "rows_v[0-9][0-9].jsonl", "rows_v[0-9][0-9].jsonl.validator_report.json", "_apply_*_report.json",
    # orchestrator probes/verifiers
    "_probe_phase0_lam.py", "_phase1_partplan_probe.py", "_wave_verify.py", "_sp_stray_sweep.py", "_resume_smoke.py",
    "_phase2_build_clusters.py", "_pr_wave_verify.py", "_peer_verify.py", "_boss_verify.py", "_build_*.py", "_apply_*.py",
    "_author_census.py", "_cwo_census.py", "_cwo_scan.py", "_wave_repair_sweep.py", "_e23_rev.json",
    "_cwo_parity.py", "cwo/cwo_parity.v1.json", "cwo/cwo_unify_c[0-9].jsonl", "cwo/*_attempt_receipts.jsonl", "usage.json", "_dep_record_*.json",
    # subtrees
    "freeze/CYCLE_STATE.md", "freeze/*.md", "freeze/*.jsonl",
    "tools/*.py", "tools/TOOLKIT.md", "tools/__pycache__/*", "tools/consonantal_index.json", "tools/verse_map_web.json",
    "tools/verse_map_oshb.json", "tools/acrostic_spine.json",
    "writer/writer_p[0-9][0-9].jsonl", "writer/writer_p[0-9][0-9].jsonl.validator_report.json", "writer/*_attempt_receipts.jsonl", "reviews/*_attempt_receipts.jsonl",
    "reviews/*.json", "reviews/*.jsonl", "slices/*.json", "author/orders_a*.json", "author/author_a*.jsonl", "author/*_attempt_receipts.jsonl",
    "cwo/orders_cwo_[0-9][0-9].json", "cwo/orders_cwo_[0-9][0-9]_c[0-9].json", "cwo/cwo_[0-9][0-9].jsonl",
    "cwo/corr/*.json", "cwo/corr/*.jsonl", "cwo/corr2/*.json", "cwo/corr2/*.jsonl",
    "cwo/corr3/*.json", "cwo/corr3/*.jsonl", "sidecar_corr.jsonl", "spot/orders_fix_[0-9][0-9].json", "spot/fix_[0-9][0-9].jsonl", "_apply_fix_report.json", "_build_fix_orders.py", "cwo/scan_correction_record.v1.json", "cwo/*_attempt_receipts.jsonl",
    "spot/*.json", "spot/*.jsonl", "postcheck/*.json", "postcheck/*.jsonl",
    "final_check/*.json", "final_check/*.jsonl", "FINAL_CHECKER_BRIEF.md", "TRANSCRIPT_AUDIT_BRIEF.md",
    # the manifest is versioned: v2 is the one built by the tool that can tell a subagent transcript from
    # captured orchestrator shell output; v1 is retained as history and never rewritten
    "transcript_manifest.v[0-9].json", "_final_check_reconcile.py", "_final_check_receipts.py",
    "_record_audit_scope.py", "_answer_auditor_path_checks.py", "_verify_cross_book_highs.py", "_append_cycle_state.py", "_stage2_receipt.py",
    # fix-round tooling and the records it produced (OW-6 stage-2 residuals)
    "_fix_parity_versioning.py", "_amend_orchestrator_model.py", "_correct_log_lineage.py",
    "_write_missing_receipts.py", "_record_cwo1_ruling.py", "_fix_toolkit_and_breach_receipts.py",
    "_build_fc_fix_orders.py", "_correct_log_lineage.py", "_build_followon_orders.py", "_fcfix_receipts.py",
    "_amend_reconstructed_models.py", "_clear_fc02_lows.py", "_record_b3_rulings.py",
    "_build_e05_sweep_orders.py", "_receipt_census.py", "_record_launch_base_mismatch.py",
    "_convergence_record.py",
    "reviews/ruling_execution_ledger.v1.json", "reviews/ruling_ground_notes.v1.jsonl",
    "cwo/cwo1_predicate_label.v1.json", "cwo/cwo_parity.rows_v[0-9][0-9].finals[0-9].json",
    "_amend_orchestrator_model.py", "FIX_BRIEF.md",
    "cwo/cwo_parity.rows_v[0-9].json", "cwo/cwo_parity.rows_v[0-9][0-9].json", "spot/*_attempt_receipts.jsonl",
    "postcheck/*_attempt_receipts.jsonl",
]
files = [p for p in HERE.rglob("*") if p.is_file()]
strays = []
for p in files:
    rel = p.relative_to(HERE).as_posix()
    if not any(fnmatch.fnmatch(rel, pat) for pat in ALLOW):
        strays.append({"path": rel, "bytes": p.stat().st_size})
print(json.dumps({"sweep": "CLEAN" if not strays else "STRAYS", "files_checked": len(files), "strays": strays}, ensure_ascii=False, indent=1))
sys.exit(1 if strays else 0)
