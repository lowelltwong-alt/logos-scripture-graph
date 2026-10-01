#!/usr/bin/env python3
"""Compact current-state index for the M8_fable lane (owner ruling OWNER_REPAIR_ADVANCE_2026-09-06
item 4). Generated FROM DISK — every hash and count is computed, never typed; the latest CURSOR
phase is read from the immutable CYCLE_STATE log; docket open/resolved counts and pending span
proposals come from the dispositions ledgers; gate status is evaluated from those ledgers.
Writes M8_fable/CURRENT_STATE.v1.json (the verified current state the resume prompt binds to).
Usage: _build_current_state.py --next "<exact next authorized job>" [--spend '{"session_reported": N, ...}']
       [--cycle-state <path to the live book's freeze/CYCLE_STATE.md>] [--dry-run]"""
import hashlib
import importlib.util
import sys as _sys
_sys.dont_write_bytecode = True   # never drop a __pycache__ stray into the shared SP (E-21)
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent          # SP/Jer
SP = HERE.parent
OW2 = SP / "OW2_audit"
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
CYCLE_STATE = HERE / "freeze" / "CYCLE_STATE.md"
OUT = M8 / "CURRENT_STATE.v1.json"
RULING = "OWNER_REPAIR_ADVANCE_2026-09-06.md"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_checker():
    spec = importlib.util.spec_from_file_location("stc", HERE / "_safe_to_clear_check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def latest_cursor(cs_path=None):
    txt = (cs_path or CYCLE_STATE).read_text(encoding="utf-8", errors="replace")
    ms = list(re.finditer(r"CURSOR: phase = ([A-Za-z0-9_]+)([^\n]*)", txt))
    if not ms:
        return "UNKNOWN", ""
    m = ms[-1]
    return m.group(1), (m.group(1) + m.group(2)).strip()[:600]


def docket_state(disp_path: Path, docket_path: Path):
    d = json.load(open(M8 / disp_path, encoding="utf-8"))
    items = d["items"]
    opn = [i for i in items if i.get("disposition") == "open"]
    resolved = [i for i in items if i.get("disposition") != "open"]

    def final(i):
        ra = i.get("readjudication") or {}
        return (ra.get("final_severity") or i["adjudicated"].get("final_severity"),
                ra.get("span_ruling") or i["adjudicated"].get("span_ruling"))
    med_high_open = [i["item_id"] for i in opn if final(i)[0] in ("medium", "high")]
    span_pending = [i["item_id"] for i in opn if final(i)[1] == "endorse_proposal"]
    return {
        "dispositions_ledger": {"path": disp_path.as_posix(), "sha256": sha(M8 / disp_path)},
        "docket": {"path": docket_path.as_posix(), "sha256": sha(M8 / docket_path)},
        "items": len(items), "open": len(opn), "resolved": len(resolved),
        "repairs_applied": sum(1 for i in items if i.get("repair_applied")),
        "open_medium_high": len(med_high_open), "open_medium_high_ids": med_high_open,
        "span_proposals_endorsed_pending": span_pending,
        "low_findings_retained": (d.get("low_findings") or {}).get("count"),
    }


def carrier_counts():
    out = {}
    for c in ("ow2lf", "ow2adj", "ow2i2", "ow2i2adj", "ow2p38", "ow2adj_re"):
        p = OW2 / f"{c}_attempt_receipts.jsonl"
        out[c] = sum(1 for l in p.read_text(encoding="utf-8").splitlines() if l.strip()) if p.is_file() else 0
    p = HERE / "author" / "jer_author_attempt_receipts.jsonl"
    out["jer_author"] = sum(1 for l in p.read_text(encoding="utf-8").splitlines() if l.strip()) if p.is_file() else 0
    lam = SP / "Lam"
    for c, rel in (("lam_writer", "writer/lam_writer_attempt_receipts.jsonl"), ("lam_pr", "reviews/lam_pr_attempt_receipts.jsonl"), ("lam_peer", "reviews/lam_peer_attempt_receipts.jsonl"), ("lam_boss", "reviews/lam_boss_attempt_receipts.jsonl"), ("lam_author", "author/lam_author_attempt_receipts.jsonl"), ("lam_cwo", "cwo/lam_cwo_attempt_receipts.jsonl"), ("lam_spot", "spot/lam_spot_attempt_receipts.jsonl"), ("lam_micro", "spot/lam_micro_attempt_receipts.jsonl"), ("lam_finalize", "postcheck/lam_finalize_attempt_receipts.jsonl")):
        q = lam / rel
        out[c] = sum(1 for l in q.read_text(encoding="utf-8").splitlines() if l.strip()) if q.is_file() else 0
    return out


def main():
    args = sys.argv[1:]
    nxt = args[args.index("--next") + 1] if "--next" in args else ""
    spend = json.loads(args[args.index("--spend") + 1]) if "--spend" in args else {}
    dry = "--dry-run" in args
    chk = load_checker()
    cs_path = Path(args[args.index("--cycle-state") + 1]) if "--cycle-state" in args else chk.live_cycle_state()   # 2026-09-07 s3: ONE source for the cursor - the checker's live-book resolution, so index and checker cannot drift
    cs_label = "sp_durable/" + cs_path.parent.parent.name + "/freeze/CYCLE_STATE.md (live SP copy)"
    jer_done = (M8 / "receipts" / "Jer_completion.json").is_file()
    phase, cursor_line = latest_cursor(cs_path)

    dockets = {
        "isaiah_lf": docket_state(Path("receipts/OW2_isa_lf_remediation_dispositions.v1.json"),
                                  Path("receipts/OW2_isa_lf_remediation_docket.v1.json")),
        "five_book": docket_state(Path("receipts/OW2_five_book_remediation_dispositions.v1.json"),
                                  Path("receipts/OW2_five_book_remediation_docket.v1.json")),
        "prov38": docket_state(Path("receipts/OW2_prov38_remediation_dispositions.v1.json"),
                               Path("receipts/OW2_prov38_remediation_docket.v1.json")),
    }
    receipts_done = {p: sha(M8 / p) for p in chk.DONE_RECEIPTS if (M8 / p).is_file()}
    receipts_all_present = all((M8 / p).is_file() for p in chk.DONE_RECEIPTS)
    rep_state, rep_info = chk.repairs_applied_state()
    total_open = sum(d["open"] for d in dockets.values())
    total_mh_open = sum(d["open_medium_high"] for d in dockets.values())
    span_pending = [x for d in dockets.values() for x in d["span_proposals_endorsed_pending"]]
    owner_gates_open = []   # the Prov crux-zones denominator gate was CLOSED by OWNER_REPAIR_ADVANCE_2026-09-06
    ow2d = {
        "criterion_1_three_audit_receipts_done": receipts_all_present,
        "criterion_2_every_required_repair_swept": (total_open == 0),
        "criterion_3_zero_unresolved_medium_high_span_systemic_owner_gate":
            (total_mh_open == 0 and not span_pending and not owner_gates_open),
        "open_items_total": total_open, "open_medium_high_total": total_mh_open,
        "span_proposals_endorsed_pending": span_pending, "owner_gates_open": owner_gates_open,
    }
    ow2d["satisfied"] = all(ow2d[k] for k in ("criterion_1_three_audit_receipts_done",
                                               "criterion_2_every_required_repair_swept",
                                               "criterion_3_zero_unresolved_medium_high_span_systemic_owner_gate"))
    carriers = {"ERROR_PATTERN_LEDGER.v1.md": sha(M8 / "ERROR_PATTERN_LEDGER.v1.md"),
                "error_pattern_ledger.v1.jsonl": sha(M8 / "error_pattern_ledger.v1.jsonl"),
                "CAMPAIGN_CLOSE_GATE.v1.md": sha(M8 / "CAMPAIGN_CLOSE_GATE.v1.md"),
                cs_label: sha(cs_path)}
    # OW-10 control surfaces: the contract that defines execution identity, and the two tools that make the cure
    # rule and the coverage claim mechanical rather than remembered. Pinned so a successor notices if one moves.
    for label, rel in (("sp_durable/campaign/CAPTURE_CONTRACT.v3.md", "campaign/CAPTURE_CONTRACT.v3.md"),
                       ("sp_durable/campaign/_capture_index.py", "campaign/_capture_index.py"),
                       ("sp_durable/campaign/_cure_verification.py", "campaign/_cure_verification.py"),
                       ("sp_durable/campaign/_transcript_coverage_census.py",
                        "campaign/_transcript_coverage_census.py"),
                       ("sp_durable/campaign/transcript_coverage_census.v1.json",
                        "campaign/transcript_coverage_census.v1.json"),
                       ("sp_durable/campaign/breach_report.v1.json", "campaign/breach_report.v1.json")):
        p = SP / rel
        if p.is_file():
            carriers[label] = sha(p)
    archive_dir = M8 / "receipts" / "prompt_archive"
    archived = sorted(archive_dir.glob("RESUME_PROMPT_*.md")) if archive_dir.is_dir() else []
    index = {
        "schema": "m8_current_state_index.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": {"path": "sp_durable/Jer/_build_current_state.py", "sha256": sha(Path(__file__))},
        "authority": "OWNER_REPAIR_ADVANCE_2026-09-06 item 4: this verified current state plus the canonical active rules replaces the mandatory full-history CYCLE_STATE reread; CYCLE_STATE stays the immutable append-only log",
        "active_directives": [
            {"id": "OWNER_REPAIR_ADVANCE_2026-09-06", "pointer": RULING, "sha256": sha(M8 / RULING),
             "kind": "standing owner ruling (repair with delegated judgment; advance; continuity)"},
            {"id": "OW-10", "pointer": "ERROR_PATTERN_LEDGER.v1.md#Addendum-2026-09-08-OW-10",
             "gate": "CAMPAIGN_CLOSE_GATE.v1.md#Item-14",
             "kind": "execution identity separated from the stable job; layers attributed per execution; a cure "
                     "requires artifact-bound verification plus a distinct checker; coverage reported from a "
                     "per-book census; the five restart-prompt duties made permanent and mechanically checked"},
            {"id": "OW-9", "pointer": "ERROR_PATTERN_LEDGER.v1.md#Addendum-2026-09-08-OW-9",
             "kind": "stop-and-clear cycle at every book boundary; the prompt is always printed in chat"},
            {"id": "OW-8", "pointer": "ERROR_PATTERN_LEDGER.v1.md#Addendum-2026-09-07-OW-8",
             "kind": "the record is an accountable work summary; audit scope is what exists; missing logs are not "
                     "a stop condition"},
            {"id": "OW-7", "pointer": "ERROR_PATTERN_LEDGER.v1.md#Addendum-2026-09-07-OW-7",
             "gate": "CAMPAIGN_CLOSE_GATE.v1.md#Item-13",
             "kind": "universal per-attempt capture; three layers never merged; lineage; blindness survives the index"},
            {"id": "OW-6 / OW-6b / OW-6c", "pointer": "ERROR_PATTERN_LEDGER.v1.md#Addendum-2026-09-07",
             "kind": "Fable final-checker gate and boss escalation authority; hard-book track; end-of-campaign "
                     "re-check decision (the CONTINUATION half of OW-6 is superseded by OW-9)"},
            {"id": "OW-4 (+ confirmations #1 and #2)", "pointer": "ERROR_PATTERN_LEDGER.v1.md#Addendum-2026-09-05-OW-4", "kind": "complete Jeremiah now (SPENT: Jeremiah closed 2026-09-07)"},
            {"id": "OW-3", "pointer": "ERROR_PATTERN_LEDGER.v1.md#Addendum-2026-09-04", "kind": "quality-control follow-up (seven permanent safeguards)"},
            {"id": "OW-2 / OW-2C", "pointer": "ERROR_PATTERN_LEDGER.v1.md#Addendum-2026-08-31", "kind": "hard close gates; idempotency; permanent safeguards"},
            {"id": "OW-1", "pointer": "ERROR_PATTERN_LEDGER.v1.md#Addendum-2026-08-31-OW-1", "kind": "process-quality warning (E-18/E-23/E-17 lanes)"},
        ],
        "superseded_controls_history_preserved": [
            "OW-2D owner-only docket-triage WAIT and 'STOP and report the decision needed' arm (gate item 7; ledger row OW-2D) — superseded by OWNER_REPAIR_ADVANCE_2026-09-06",
            "per-proposal owner span approval — superseded (orchestrator accepts/rejects within the owner-ruled strategy, reasons + evidence in the dispositions ledgers)",
            "owner-only pre-Lamentations pause — lifts when Jeremiah passes its hard close gates",
            "Prov crux-zones denominator owner gate — CLOSED (38 stays the historical denominator; supplemental observations recorded separately)",
            "OW-6 CONTINUATION CLAUSE ('every book close is followed immediately by the next book; clear and "
            "re-prompt only when needed') — SUPERSEDED by OW-9. A book close is a HARD STOP. Kept, marked "
            "superseded, not deleted. Everything else in OW-6 stands.",
            "OW-5's straight-through clause — SPENT (it was scoped to Jeremiah and Lamentations; both are closed)",
            "CAPTURE_CONTRACT.v2.md identity section (attempt_id doing duty as both the stable job and the "
            "physical run) — SUPERSEDED by CAPTURE_CONTRACT.v3.md under OW-10; v2 and v1 retained beside it",
            "breach_report.v1.json's 'for none of the earlier books' coverage wording, and its 'the 43 "
            "Lamentations attempts and all Jeremiah attempts' residual wording — SUPERSEDED by the per-book "
            "census under OW-10; the superseded text is retained inside the report under superseded_statements",
        ],
        "binding_active_rules": {"canonical_clauses": chk.CANONICAL, "carriers": carriers,
                                 "checker": {"path": "sp_durable/Jer/_safe_to_clear_check.py", "sha256": sha(HERE / "_safe_to_clear_check.py")}},
        "phase": phase, "cursor_line": cursor_line, "next_authorized_job": nxt,
        "accepted_artifacts": {"done_receipts": receipts_done, "shipped_corpora_check": rep_info,
                               "repairs_applied_state": rep_state},
        "dockets": dockets,
        "attempt_dispositions": carrier_counts(),
        "spend": spend,
        "gate_status": {"ow2d": ow2d,
                        "jeremiah_hard_close": ("CLOSED 2026-09-07 (receipts/Jer_completion.json sha256 " + sha(M8 / "receipts" / "Jer_completion.json") + ")") if jer_done else "pending (book not closed)",
                        "pre_lamentations_pause": "LIFTED (Jeremiah passed its hard close gates 2026-09-07; OW-5 proceeded to Lamentations without the clear/re-prompt step)" if jer_done else "lifts when Jeremiah passes its hard close gates (OWNER_REPAIR_ADVANCE_2026-09-06 item 3)",
                        "lamentations_hard_close": ("CLOSED (receipts/Lam_completion.json sha256 " + sha(M8 / "receipts" / "Lam_completion.json") + ")") if (M8 / "receipts" / "Lam_completion.json").is_file() else "pending (book not closed)"},
        "prompt_slot": {"path": "RESUME_PROMPT_CURRENT.md",
                        "archive": [{"path": p.relative_to(M8).as_posix(), "sha256": sha(p)} for p in archived]},
    }
    if dry:
        print(json.dumps(index, ensure_ascii=False, indent=1)[:3000]); return 0
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    tmp.replace(OUT)
    print(json.dumps({"written": str(OUT), "sha256": sha(OUT), "phase": phase, "ow2d_satisfied": ow2d["satisfied"],
                      "open_items_total": total_open, "open_medium_high_total": total_mh_open,
                      "span_pending": span_pending, "carriers": index["attempt_dispositions"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
