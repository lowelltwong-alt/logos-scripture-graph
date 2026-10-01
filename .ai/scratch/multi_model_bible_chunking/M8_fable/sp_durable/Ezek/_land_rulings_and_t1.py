#!/usr/bin/env python3
"""Land the T1 toolkit review or the controlling-agent rulings: verify form and digest binding -> receipt -> layer-C
note -> capture index. Same conventions as _land_writer_part.py.

The agent writes its deliverable directly to its exact path under SP/Ezek, so there is nothing to persist. This tool
never edits a deliverable and never judges its content: it proves FORM (parseable, complete, digest-bound) and
records what it found. A form defect lands as LANDED_WITH_FORM_DEFECTS with every defect named, never as a silent
pass and never as a rejection the controlling agent did not make.

  rulings: every item id of ezek_controlling_agent_queue.v1.json and of the addendum has exactly one ruling; R4 is
           deferred as instructed; each inputs_ruled_on digest equals the brief's launch digest AND today's bytes.
  t1:      verdict in the allowed set; every artifacts_reviewed entry carries artifact_sha256_at_review, equal to the
           brief's launch digest AND today's bytes (the OW-10 binding a later cure claim needs); answers q1-q9.

Usage: _land_rulings_and_t1.py --job rulings|t1 --record <agent OW-8 final message .json> --tokens N --tool-uses N
       [--ordinal N]   derived from the record's execution_id when omitted; refused when it disagrees (OW-11-k)
       _land_rulings_and_t1.py --selftest
       [--ordinal N]
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
SP = EZ.parent
CAMPAIGN = SP / "campaign"
RECEIPTS = EZ / "ezek_rulings_attempt_receipts.jsonl"
NOTES = EZ / "evidence_notes"
EXTRAS: dict = {}

JOBS = {
    "rulings": {"attempt": "ezek_controlling_rulings_a1", "deliverable": "ezek_controlling_agent_rulings.v1.json",
                "brief": "CONTROLLING_AGENT_BRIEF_RULINGS.md", "brief_v2": "CONTROLLING_AGENT_BRIEF_RULINGS.v2.md",
                "lane": "ezek_phase1_controlling_rulings",
                "agent": "controlling agent", "model": "claude-fable-5-1",
                "effort": "ORDERED high (hard-book track controlling agent), NOT VERIFIED",
                "producer": "OW-6b controlling agent ruling on the v1 queue and the addendum",
                "catcher": "SP/Ezek/_land_rulings_and_t1.py (form, completeness, digest binding only); the orchestrator "
                           "executes rulings and does not re-rule them"},
    "rulings_e3": {"attempt": "ezek_controlling_rulings_a1", "deliverable": "ezek_controlling_agent_rulings_e3.v1.json",
                   "brief": "CONTROLLING_AGENT_BRIEF_E3.md", "brief_v2": "CONTROLLING_AGENT_BRIEF_E3.md",
                   "lane": "ezek_phase1_controlling_rulings", "agent": "controlling agent", "model": "claude-fable-5-1",
                   "effort": "ORDERED high (hard-book track controlling agent), NOT VERIFIED",
                   "producer": "OW-6b controlling agent ruling on the #e3 queue (R4 follow-on and the repair wave's items)",
                   "catcher": "SP/Ezek/_land_rulings_and_t1.py (form, completeness, digest binding only); the orchestrator "
                              "executes rulings and does not re-rule them"},
    "rulings_e4": {"attempt": "ezek_controlling_rulings_a1", "deliverable": "ezek_controlling_agent_rulings_e4.v1.json",
                   "brief": "CONTROLLING_AGENT_BRIEF_E4.md", "brief_v2": "CONTROLLING_AGENT_BRIEF_E4.md",
                   "lane": "ezek_phase1_controlling_rulings", "agent": "controlling agent", "model": "claude-fable-5-1",
                   "effort": "ORDERED high (hard-book track controlling agent), NOT VERIFIED",
                   "producer": "OW-6b controlling agent ruling on the #e4 queue (items raised after #e3, T4 and S1) and the "
                               "primaries gate",
                   "catcher": "SP/Ezek/_land_rulings_and_t1.py (form, completeness, digest binding only); the orchestrator "
                              "executes rulings and does not re-rule them"},
    "rulings_e5": {"attempt": "ezek_controlling_rulings_a1", "deliverable": "ezek_controlling_agent_rulings_e5.v1.json",
                   "brief": "CONTROLLING_AGENT_BRIEF_E5.md", "brief_v2": "CONTROLLING_AGENT_BRIEF_E5.md",
                   "lane": "ezek_phase1_controlling_rulings", "agent": "controlling agent", "model": "claude-fable-5-1",
                   "effort": "ORDERED high (hard-book track controlling agent), NOT VERIFIED",
                   "producer": "OW-6b controlling agent ruling on the class TOOLFIX-2 condition (c) returned before install, and the "
                               "staged batch's FLAGS outcomes",
                   "catcher": "SP/Ezek/_land_rulings_and_t1.py (form, completeness, digest binding only); the orchestrator "
                              "executes rulings and does not re-rule them"},
    "rulings_e6": {"attempt": "ezek_controlling_rulings_a1", "deliverable": "ezek_controlling_agent_rulings_e6.v1.json",
                   "brief": "CONTROLLING_AGENT_BRIEF_E6.md", "brief_v2": "CONTROLLING_AGENT_BRIEF_E6.md",
                   "lane": "ezek_phase1_controlling_rulings", "agent": "controlling agent", "model": "claude-fable-5-1",
                   "effort": "ORDERED high (hard-book track controlling agent), NOT VERIFIED",
                   "producer": "OW-6b controlling agent ruling on T5's findings and the three questions CWO-EZ-18's dry run raised",
                   "catcher": "SP/Ezek/_land_rulings_and_t1.py (form, completeness, digest binding only); the orchestrator "
                              "executes rulings and does not re-rule them"},
    "rulings_e7": {"attempt": "ezek_controlling_rulings_a1", "deliverable": "ezek_controlling_agent_rulings_e7.v1.json",
                   "brief": "CONTROLLING_AGENT_BRIEF_E7.md", "brief_v2": "CONTROLLING_AGENT_BRIEF_E7.md",
                   "lane": "ezek_phase1_controlling_rulings", "agent": "controlling agent", "model": "claude-fable-5-1",
                   "effort": "ORDERED high (hard-book track controlling agent), NOT VERIFIED",
                   "producer": "OW-6b controlling agent ruling on the R1-shape assertion the amended CWO-EZ-18 dry run could not meet",
                   "catcher": "SP/Ezek/_land_rulings_and_t1.py (form, completeness, digest binding only); the orchestrator "
                              "executes rulings and does not re-rule them"},
    "rulings_e8": {"attempt": "ezek_controlling_rulings_a1", "deliverable": "ezek_controlling_agent_rulings_e8.v1.json",
                   "brief": "CONTROLLING_AGENT_BRIEF_E8.md", "brief_v2": "CONTROLLING_AGENT_BRIEF_E8.md",
                   "lane": "ezek_phase1_controlling_rulings", "agent": "controlling agent", "model": "claude-fable-5-1",
                   "effort": "ORDERED high (hard-book track controlling agent), NOT VERIFIED",
                   "producer": "OW-6b controlling agent ruling on T6's findings (T6-01, T6-02), the S1-19 claim timing and T6's disclosed deviations",
                   "catcher": "SP/Ezek/_land_rulings_and_t1.py (form, completeness, digest binding only); the orchestrator "
                              "executes rulings and does not re-rule them"},
    "rulings_e9": {"attempt": "ezek_controlling_rulings_a1", "deliverable": "ezek_controlling_agent_rulings_e9.v1.json",
                   "brief": "CONTROLLING_AGENT_BRIEF_E9.md", "brief_v2": "CONTROLLING_AGENT_BRIEF_E9.md",
                   "lane": "ezek_phase1_controlling_rulings", "agent": "controlling agent", "model": "claude-fable-5-1",
                   "effort": "ORDERED high (hard-book track controlling agent), NOT VERIFIED",
                   "producer": "OW-6b controlling agent ruling on S2's findings (routing and FIXUP-2's scope, the S2-04/S2-12/S2-13/S2-14 "
                               "classes, the S2-15 tool gaps, the S2-16/S2-17 notes, S2's disclosed deviations) and the gate for FIXUP-2, "
                               "S3, the rows cure claims and the primaries",
                   "catcher": "SP/Ezek/_land_rulings_and_t1.py (form, completeness, digest binding only); the orchestrator "
                              "executes rulings and does not re-rule them"},
    "s3": {"attempt": "ezek_fixup2_wave_review_s3_a1", "deliverable": "ezek_fixup2_wave_review_S3.json",
           "brief": "FIXUP2_WAVE_REVIEW_BRIEF_S3.md", "brief_v2": "FIXUP2_WAVE_REVIEW_BRIEF_S3.md",
           "lane": "ezek_post_wave_distinct_review", "agent": "S3 fresh distinct checker of the FIXUP-2 wave", "model": "claude-opus-5",
           "effort": "ORDERED high, NOT VERIFIED",
           "producer": "fresh distinct-checker review of the FIXUP-2 wave, its sweeps, tool plumbing and v5 coverage "
                       "(ezek_controlling_rulings_a1#e9 ruling S2-ROUTING (7))",
           "catcher": "SP/Ezek/_land_rulings_and_t1.py (form and digest binding only); its verdict gates the FIXUP-1 and FIXUP-2 rows "
                      "cure claims, and each finding routes to author fix-ups, the orchestrator or the controlling agent"},
    "rulings_e10": {"attempt": "ezek_controlling_rulings_a1", "deliverable": "ezek_controlling_agent_rulings_e10.v1.json",
                    "brief": "CONTROLLING_AGENT_BRIEF_E10.md", "brief_v2": "CONTROLLING_AGENT_BRIEF_E10.md",
                    "lane": "ezek_phase1_controlling_rulings", "agent": "controlling agent", "model": "claude-fable-5-1",
                    "effort": "ORDERED high (hard-book track controlling agent), NOT VERIFIED",
                    "producer": "OW-6b controlling agent ruling on S3's findings (routing and FIXUP-3's scope, the S3-03 and S3-16 classes, "
                                "S3-17's boundary question, S3-18's order-text record, TOOLFIX-5's timing and scope, S3's notes, the open "
                                "transcript and E-19 items) and the gate for FIXUP-3, S4, the rows cure claims and the primaries",
                    "catcher": "SP/Ezek/_land_rulings_and_t1.py (form, completeness, digest binding only); the orchestrator "
                               "executes rulings and does not re-rule them"},
    "s4": {"attempt": "ezek_fixup3_wave_review_s4_a1", "deliverable": "ezek_fixup3_wave_review_S4.json",
           "brief": "FIXUP3_WAVE_REVIEW_BRIEF_S4.md", "brief_v2": "FIXUP3_WAVE_REVIEW_BRIEF_S4.md",
           "lane": "ezek_post_wave_distinct_review", "agent": "S4 fresh distinct checker of the FIXUP-3 wave", "model": "claude-fable-5-1",
           "effort": "ORDERED high, NOT VERIFIED",
           "producer": "fresh distinct-checker review of the FIXUP-3 wave, CWO-EZ-23's pairs, TOOLFIX-5 and v6 coverage "
                       "(ezek_controlling_rulings_a1#e10 ruling S3-ROUTING (7); model by owner directive OW-13)",
           "catcher": "SP/Ezek/_land_rulings_and_t1.py (form and digest binding only); its verdict gates the FIXUP-1, FIXUP-2 and FIXUP-3 rows "
                      "cure claims, and each finding routes to author fix-ups, the orchestrator or the controlling agent"},
    "rulings_e11": {"attempt": "ezek_controlling_rulings_a1", "deliverable": "ezek_controlling_agent_rulings_e11.v1.json",
                    "brief": "CONTROLLING_AGENT_BRIEF_E11.md", "brief_v2": "CONTROLLING_AGENT_BRIEF_E11.md",
                    "lane": "ezek_phase1_controlling_rulings", "agent": "controlling agent", "model": "claude-fable-5-1",
                    "effort": "ORDERED high (hard-book track controlling agent), NOT VERIFIED",
                    "producer": "OW-6b controlling agent ruling on S4's twelve findings, the two residual 7-gram families at "
                                "headroom 0, the transcript-route finding (the census retention figure, the Ezek manifest v2 "
                                "candidate, the Q8 observed-now column and the OW-6 stage-1 slice denominator), the primaries' "
                                "lane models under OW-13, the primaries' shape and brief, the two retained Phase-0 lows, and "
                                "the gate that decides primaries_may_launch",
                    "catcher": "SP/Ezek/_land_rulings_and_t1.py (form, completeness, digest binding only); the orchestrator "
                               "executes rulings and does not re-rule them"},
    "s5": {"attempt": "ezek_cwo24_transcript_review_s5_a1", "deliverable": "ezek_cwo24_transcript_review_S5.json",
           "brief": "CWO24_TRANSCRIPT_REVIEW_BRIEF_S5.md", "brief_v2": "CWO24_TRANSCRIPT_REVIEW_BRIEF_S5.md",
           "lane": "ezek_post_cwo24_distinct_review", "agent": "distinct checker", "model": "claude-fable-5-1",
           "effort": "ORDERED high (OW-6b hard-book track distinct check), NOT VERIFIED",
           "producer": "OW-13 checker: a fresh claude-fable-5-1 execution reading the 18 CWO-EZ-24 pairs, the v7 suite "
                       "and coverage, TOOLFIX-6's diffs and selftests, the rebuilt transcript manifest, census v2 and "
                       "the pre_primaries statement",
           "catcher": "SP/Ezek/_land_rulings_and_t1.py (form, completeness, digest binding only); the orchestrator "
                      "executes rulings and does not re-rule them"},
    "t2": {"attempt": "ezek_toolkit_repair_review_t2_a1", "deliverable": "ezek_toolkit_repair_review_T2.json",
           "brief": "TOOLKIT_REPAIR_REVIEW_BRIEF_T2.md", "brief_v2": "TOOLKIT_REPAIR_REVIEW_BRIEF_T2.md",
           "lane": "ezek_phase1_toolkit_repair_review", "agent": "T2 fresh distinct checker", "model": "claude-sonnet-5",
           "effort": "ORDERED default, NOT VERIFIED",
           "producer": "fresh distinct-checker review of the orchestrator's repair of T1's findings",
           "catcher": "SP/Ezek/_land_rulings_and_t1.py (form and digest binding only); its cure statuses gate the cure "
                      "claims, and its verdict goes to the controlling agent with T1's for R4"},
    "s1": {"attempt": "ezek_author_wave_spot_review_s1_a1", "deliverable": "ezek_author_wave_spot_review_S1.json",
           "brief": "AUTHOR_WAVE_SPOT_REVIEW_BRIEF_S1.md", "brief_v2": "AUTHOR_WAVE_SPOT_REVIEW_BRIEF_S1.md",
           "lane": "ezek_post_wave_distinct_review", "agent": "S1 distinct checker of the author wave", "model": "claude-opus-5",
           "effort": "ORDERED default, NOT VERIFIED",
           "producer": "distinct-checker review of the author wave's amended rows, the sweep diffs and the T3-01 verifier change "
                       "(gate condition of ezek_controlling_rulings_a1#e3)",
           "catcher": "SP/Ezek/_land_rulings_and_t1.py (form and digest binding only); its findings route to author fix-ups, "
                      "orchestrator sweeps or the controlling agent"},
    "s2": {"attempt": "ezek_fixup_wave_review_s2_a1", "deliverable": "ezek_fixup_wave_review_S2.json",
           "brief": "FIXUP_WAVE_REVIEW_BRIEF_S2.md", "brief_v2": "FIXUP_WAVE_REVIEW_BRIEF_S2.md",
           "lane": "ezek_post_wave_distinct_review", "agent": "S2 fresh distinct checker of the FIXUP-1 wave", "model": "claude-opus-5",
           "effort": "ORDERED high, NOT VERIFIED",
           "producer": "fresh distinct-checker review of the FIXUP-1 wave, its coverage, the CWO-EZ-13/18 manifests, the TOOLFIX-2 "
                       "corpus-impact report and the TOOLFIX-4 verifier (ezek_controlling_rulings_a1#e4 gate condition 7; #e8 ruling T6-01)",
           "catcher": "SP/Ezek/_land_rulings_and_t1.py (form and digest binding only); its verdict gates the FIXUP-1 cure claims and the "
                      "S1-19 claim, and a blocker or a verifier finding returns to the controlling agent"},
    "t4": {"attempt": "ezek_toolkit_r4ii_review_t4_a1", "deliverable": "ezek_toolkit_r4ii_review_T4.json",
           "brief": "TOOLKIT_R4II_REVIEW_BRIEF_T4.md", "brief_v2": "TOOLKIT_R4II_REVIEW_BRIEF_T4.md",
           "lane": "ezek_phase1_toolkit_r4ii_review", "agent": "T4 supplementary distinct checker", "model": "claude-sonnet-5",
           "effort": "ORDERED default, NOT VERIFIED",
           "producer": "supplementary distinct-checker review of the R4(ii) + CAL-1 tool edit ordered by ezek_controlling_rulings_a1#e3",
           "catcher": "SP/Ezek/_land_rulings_and_t1.py (form and digest binding only); its verdict re-ratifies R4-ii only if it "
                      "finds nothing new, gates EZEK-P0-CURE-toolkit-v3, and goes to the controlling agent on R4ii-D1"},
    "t6": {"attempt": "ezek_toolkit_tf3_review_t6_a1", "deliverable": "ezek_toolkit_tf3_review_T6.json",
           "brief": "TOOLKIT_TF3_REVIEW_BRIEF_T6.md", "brief_v2": "TOOLKIT_TF3_REVIEW_BRIEF_T6.md",
           "lane": "ezek_phase1_toolkit_tf3_review", "agent": "T6 fresh distinct checker", "model": "claude-sonnet-5",
           "effort": "ORDERED high, NOT VERIFIED",
           "producer": "fresh distinct-checker review of TOOLFIX-3 (the hardened cure verifier and the corrected TOOLKIT.md) and the six "
                       "suite-file claims appended under it, ordered by ezek_controlling_rulings_a1#e6 ruling T5-SEQUENCE",
           "catcher": "SP/Ezek/_land_rulings_and_t1.py (form and digest binding only); its verdict gates the S1-19 cure claim and "
                      "EZEK-P0-CURE-toolkit-v3, and every finding returns to the controlling agent"},
    "t5": {"attempt": "ezek_toolkit_install_review_t5_a1", "deliverable": "ezek_toolkit_install_review_T5.json",
           "brief": "TOOLKIT_INSTALL_REVIEW_BRIEF_T5.md", "brief_v2": "TOOLKIT_INSTALL_REVIEW_BRIEF_T5.md",
           "lane": "ezek_phase1_toolkit_install_review", "agent": "T5 fresh distinct checker", "model": "claude-opus-5",
           "effort": "ORDERED high, NOT VERIFIED",
           "producer": "fresh distinct-checker review of both installed tool batches (t4fix_batch2, toolfix2_batch3), ordered by "
                       "ezek_controlling_rulings_a1#e4 gate condition 4 and #e5 ruling INSTALL-TF2-1 (5)",
           "catcher": "SP/Ezek/_land_rulings_and_t1.py (form and digest binding only); its verdict gates the tool cure claims, "
                      "EZEK-P0-CURE-toolkit-v3 and the Q3-1 rebinds, and every finding returns to the controlling agent"},
    "t3": {"attempt": "ezek_toolkit_supplementary_review_t3_a1", "deliverable": "ezek_toolkit_supplementary_review_T3.json",
           "brief": "TOOLKIT_SUPPLEMENTARY_REVIEW_BRIEF_T3.md", "brief_v2": "TOOLKIT_SUPPLEMENTARY_REVIEW_BRIEF_T3.md",
           "lane": "ezek_phase1_toolkit_supplementary_review", "agent": "T3 supplementary distinct checker",
           "model": "claude-sonnet-5", "effort": "ORDERED default, NOT VERIFIED",
           "producer": "supplementary distinct-checker review ordered by ruling T1 (items 1-7), plus the T2 repair batch, "
                       "D3, the calendar-date arm and the R5/R6 cure-gate controls",
           "catcher": "SP/Ezek/_land_rulings_and_t1.py (form and digest binding only); its verdicts gate "
                      "EZEK-P0-CURE-toolkit-v2 and the tool cure claims, and go to the controlling agent for R4 (i)-(iii)"},
    "t1": {"attempt": "ezek_toolkit_review_t1_a1", "deliverable": "ezek_toolkit_review_T1.json",
           "brief": "TOOLKIT_REVIEW_BRIEF_T1.md", "brief_v2": "TOOLKIT_REVIEW_BRIEF_T1.v2.md",
           "lane": "ezek_phase1_toolkit_review",
           "agent": "T1 distinct checker", "model": "claude-sonnet-5", "effort": "ORDERED default, NOT VERIFIED",
           "producer": "distinct-checker review of the toolkit the orchestrator staged",
           "catcher": "SP/Ezek/_land_rulings_and_t1.py (form and digest binding only); its verdict goes to the "
                      "controlling agent for R4"},
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rel_key(path: str) -> str:
    s = path.replace("\\", "/").strip()
    s = re.sub(r"^(?:.*?/sp_durable/|SP/)", "", s)
    return s


def brief_digests(brief: Path) -> dict:
    out = {}
    for line in brief.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| `SP\\(.+?)` \| `([0-9a-f]{64})` \|$", line)
        if m:
            out[m.group(1).replace("\\", "/")] = m.group(2)
    return out


def check_binding(entries, path_key, digest_key, launch, defects, label):
    seen = set()
    for e in entries:
        k = rel_key(str(e.get(path_key, "")))
        seen.add(k)
        got = str(e.get(digest_key, ""))
        if k not in launch:
            # read beyond the digest table (the brief itself, a path the brief names in prose): reported, not a defect
            EXTRAS.setdefault(label, []).append(k)
            continue
        if got != launch[k]:
            defects.append("%s: %s digest %s != launch digest %s" % (label, k, got[:16], launch[k][:16]))
        live = SP / k
        if live.is_file() and sha(live) != launch[k]:
            defects.append("%s: %s has CHANGED on disk since launch (now %s)" % (label, k, sha(live)[:16]))
    return seen


def validate_rulings(d, launch, defects):
    q1 = json.loads((EZ / "ezek_controlling_agent_queue.v1.json").read_text(encoding="utf-8"))
    add = json.loads((EZ / "ezek_controlling_agent_queue_addendum.v1.json").read_text(encoding="utf-8"))
    want = [i["id"] for k in ("orchestrator_items", "strategy_internal_questions", "granularity_and_seam_questions",
                             "process_items_for_the_record") for i in q1[k]] + [i["id"] for i in add["items"]]
    got = [r.get("id") for r in d.get("rulings", [])]
    missing = [i for i in want if i not in got]
    dup = sorted({i for i in got if got.count(i) > 1})
    extra = [i for i in got if i not in want]
    if missing:
        defects.append("rulings missing for: %s" % ", ".join(missing))
    if dup:
        defects.append("more than one ruling for: %s" % ", ".join(dup))
    if extra:
        defects.append("rulings for ids not in either queue: %s" % ", ".join(map(str, extra)))
    r4 = next((r for r in d.get("rulings", []) if r.get("id") == "R4"), None)
    if r4 is not None and r4.get("ruling") != "defer":
        defects.append("R4 was to be deferred until T1 lands; ruled %r" % r4.get("ruling"))
    if not isinstance(d.get("gate"), dict) or "primaries_may_launch" not in d["gate"]:
        defects.append("gate.primaries_may_launch absent")
    seen = check_binding(d.get("inputs_ruled_on", []), "path", "sha256", launch, defects, "inputs_ruled_on")
    unbound = sorted(set(launch) - seen)
    return {"expected_ids": len(want), "ruled_ids": len(set(got) & set(want)), "missing": missing,
            "rulings_by_kind": {k: sum(1 for r in d.get("rulings", []) if r.get("ruling") == k)
                                for k in sorted({str(r.get("ruling")) for r in d.get("rulings", [])})},
            "corpus_wide_orders": len(d.get("corpus_wide_orders", [])),
            "primaries_may_launch": (d.get("gate") or {}).get("primaries_may_launch"),
            "inputs_not_listed_in_inputs_ruled_on": unbound,
            "inputs_read_beyond_the_table": EXTRAS.get("inputs_ruled_on", [])}


def validate_s1(d, launch, defects):
    """S1 reviews the author wave. Form only: the verdict; the rows digest it reviewed equals the live chain head; the
    digest binding; every required section present with allowed verdicts; the CWO sample is at least 33 rows; every
    manifest names how many changes it checked; the tool questions are answered; findings carry an allowed route."""
    verdicts = ("fit_to_accept", "fit_with_changes", "not_fit")
    if d.get("verdict") not in verdicts:
        defects.append("verdict %r not in the allowed set" % d.get("verdict"))
    head = EZ / "repair" / "rows_v3_cwo12.jsonl"
    if (d.get("rows_file_reviewed") or {}).get("sha256") != sha(head):
        defects.append("rows_file_reviewed.sha256 is not the live chain head %s" % sha(head)[:16])
    for e in d.get("artifacts_reviewed", []):
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("artifact_sha256_at_review", ""))):
            defects.append("artifacts_reviewed entry without a sha256: %s" % e.get("path"))
    seen = check_binding(d.get("artifacts_reviewed", []), "path", "artifact_sha256_at_review", launch, defects,
                         "artifacts_reviewed")
    ok = ("accept", "defect")
    for sec in ("respans", "content_orders", "sweep_manifests"):
        items = d.get(sec)
        if not isinstance(items, list) or not items:
            defects.append("%s missing or empty" % sec)
            continue
        bad = [i for i in items if i.get("verdict") not in ok]
        if bad:
            defects.append("%s: %d entries without accept|defect" % (sec, len(bad)))
    if any(not isinstance(m.get("changes_checked"), int) for m in d.get("sweep_manifests") or []):
        defects.append("sweep_manifests entries without an integer changes_checked")
    sample = (d.get("cwo_sample") or {}).get("rows") or []
    if len(sample) < 33:
        defects.append("cwo_sample has %d rows; the brief asks for at least 33" % len(sample))
    for sec in ("apply", "coverage", "verifier", "flags"):
        if (d.get(sec) or {}).get("verdict") not in ok:
            defects.append("%s.verdict not accept|defect" % sec)
    tq = d.get("tool_questions") or []
    if len(tq) < 9 or any(q.get("disposition") not in ("tool_false_positive", "row_defect", "neither") for q in tq):
        defects.append("tool_questions: fewer than 9 or a disposition outside the allowed set")
    routes = [str(f.get("route", "")) for f in d.get("new_findings", [])]
    badr = [r for r in routes if not re.fullmatch(r"author_fixup:p\d\d|orchestrator|controlling_agent", r)]
    if badr:
        defects.append("new_findings with a route outside author_fixup:pNN|orchestrator|controlling_agent: %s" % badr[:5])
    sev = {}
    for f in d.get("new_findings", []):
        sev[str(f.get("severity"))] = sev.get(str(f.get("severity")), 0) + 1
    return {"verdict": d.get("verdict"), "respans": len(d.get("respans") or []),
            "respan_defects": sum(1 for i in d.get("respans") or [] if i.get("verdict") == "defect"),
            "content_order_defects": sum(1 for i in d.get("content_orders") or [] if i.get("verdict") == "defect"),
            "cwo_sample_rows": len(sample), "cwo_sample_defects": sum(1 for i in sample if i.get("verdict") == "defect"),
            "sweep_manifest_defects": sum(1 for i in d.get("sweep_manifests") or [] if i.get("verdict") == "defect"),
            "sections": {s: (d.get(s) or {}).get("verdict") for s in ("apply", "coverage", "verifier", "flags")},
            "tool_questions": {q.get("disposition"): sum(1 for x in tq if x.get("disposition") == q.get("disposition")) for q in tq},
            "new_findings_by_severity": sev, "routes": sorted(set(routes)),
            "artifacts_not_reviewed": sorted(set(launch) - seen),
            "artifacts_read_beyond_the_table": EXTRAS.get("artifacts_reviewed", [])}


def validate_t4(d, launch, defects):
    """T4 reviews the R4(ii) + CAL-1 edit. Form only: the verdict; the digest binding; a verdict for each of the five
    changes (the prose deviation with its own verb set); the TOOLKIT.md verdict with its sibling sweep (R6); suite parity;
    the tests counts."""
    verdicts = ("fit_to_accept", "fit_with_changes", "not_fit")
    if d.get("verdict") not in verdicts:
        defects.append("verdict %r not in the allowed set" % d.get("verdict"))
    for e in d.get("artifacts_reviewed", []):
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("artifact_sha256_at_review", ""))):
            defects.append("artifacts_reviewed entry without a sha256: %s" % e.get("path"))
    seen = check_binding(d.get("artifacts_reviewed", []), "path", "artifact_sha256_at_review", launch, defects,
                         "artifacts_reviewed")
    ch = d.get("changes") or {}
    for k in ("r4ii_parenthetical", "r4ii_distance_ref", "cal1_apposition", "cal1_parenthesis"):
        if not str((ch.get(k) or {}).get("verdict", "")).strip():
            defects.append("changes.%s has no verdict" % k)
    dev = (ch.get("r4ii_distance_prose_deviation") or {}).get("verdict")
    if dev not in ("accept_deviation", "reject_deviation", "alternative_proposed"):
        defects.append("changes.r4ii_distance_prose_deviation verdict %r not allowed" % dev)
    tk = d.get("toolkit_md") or {}
    if tk.get("verdict") not in verdicts:
        defects.append("toolkit_md.verdict %r not in the allowed set" % tk.get("verdict"))
    sw = tk.get("sibling_sweep") or {}
    if not (isinstance(sw.get("key_phrases"), list) and sw["key_phrases"] and isinstance(sw.get("statements_reviewed"), int)):
        defects.append("toolkit_md.sibling_sweep lacks non-empty key_phrases or an integer statements_reviewed (R6)")
    if not str((d.get("suite_parity") or {}).get("verdict", "")).strip():
        defects.append("suite_parity has no verdict")
    t = d.get("tests") or {}
    if not (isinstance(t.get("passed"), int) and isinstance(t.get("checks"), int)):
        defects.append("tests lacks integer passed/checks")
    sev = {}
    for f in d.get("new_findings", []):
        sev[str(f.get("severity"))] = sev.get(str(f.get("severity")), 0) + 1
    return {"verdict": d.get("verdict"), "changes": {k: (v or {}).get("verdict") for k, v in ch.items()},
            "toolkit_md_verdict": tk.get("verdict"),
            "sibling_sweep": {"key_phrases": len(sw.get("key_phrases") or []), "statements_reviewed": sw.get("statements_reviewed")},
            "suite_parity": (d.get("suite_parity") or {}).get("verdict"), "tests": t, "new_findings_by_severity": sev,
            "artifacts_not_reviewed": sorted(set(launch) - seen),
            "artifacts_read_beyond_the_table": EXTRAS.get("artifacts_reviewed", [])}


def validate_t5(d, launch, defects):
    """T5 reviews both installed tool batches. Form only:
      - the verdict and the digest binding;
      - a verdict for every question the brief asks, from the closed verb sets it names;
      - a boolean agree for each of the four hand-reviewed rows, and a non-empty implementation_readings list;
      - the TOOLKIT.md verdict with its sibling sweep (R6), suite parity and the three test counts;
      - a readiness entry, with a 64-hex digest and a boolean fit, for each of the seven cure-claim files."""
    verdicts = ("fit_to_accept", "fit_with_changes", "not_fit")
    if d.get("verdict") not in verdicts:
        defects.append("verdict %r not in the allowed set" % d.get("verdict"))
    for e in d.get("artifacts_reviewed", []):
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("artifact_sha256_at_review", ""))):
            defects.append("artifacts_reviewed entry without a sha256: %s" % e.get("path"))
    seen = check_binding(d.get("artifacts_reviewed", []), "path", "artifact_sha256_at_review", launch, defects, "artifacts_reviewed")
    closed = {"r4ii_at_new_digests": ("re_ratified", "findings"), "r4i_closure": ("closed", "not_closed"),
              "discrimination_discrepancy": ("confirmed", "refuted")}
    for k, allowed in closed.items():
        if (d.get(k) or {}).get("verdict") not in allowed:
            defects.append("%s.verdict %r not in %s" % (k, (d.get(k) or {}).get("verdict"), list(allowed)))
    for k in ("s1_07_and_newclass", "s1_06_ref_hebrew", "register_arms", "e15d", "verifier", "suite_parity"):
        if not str((d.get(k) or {}).get("verdict", "")).strip():
            defects.append("%s has no verdict" % k)
    fl = d.get("s1_22_and_flags_tf2_1") or {}
    for k in ("removals_review", "w1", "w2", "w5", "w6"):
        if not str((fl.get(k) or {}).get("verdict", "")).strip():
            defects.append("s1_22_and_flags_tf2_1.%s has no verdict" % k)
    strays = {str(x.get("row")): x.get("agree") for x in fl.get("hand_review_strays") or [] if isinstance(x, dict)}
    for row in ("P02-006", "P02-020", "P05-003", "P09-002"):
        if not isinstance(strays.get(row), bool):
            defects.append("s1_22_and_flags_tf2_1.hand_review_strays lacks a boolean agree for %s" % row)
    if not (isinstance(fl.get("implementation_readings"), list) and fl["implementation_readings"]):
        defects.append("s1_22_and_flags_tf2_1.implementation_readings is empty")
    tk = d.get("toolkit_md") or {}
    if tk.get("verdict") not in verdicts:
        defects.append("toolkit_md.verdict %r not in the allowed set" % tk.get("verdict"))
    sw = tk.get("sibling_sweep") or {}
    if not (isinstance(sw.get("key_phrases"), list) and sw["key_phrases"] and isinstance(sw.get("statements_reviewed"), int)):
        defects.append("toolkit_md.sibling_sweep lacks non-empty key_phrases or an integer statements_reviewed (R6)")
    t = d.get("tests") or {}
    for k, keys in (("zone", ("passed", "checks")), ("ezek_lib", ("passed", "checks")), ("verifier", ("vectors", "failed"))):
        if not all(isinstance((t.get(k) or {}).get(x), int) for x in keys):
            defects.append("tests.%s lacks integer %s" % (k, "/".join(keys)))
    ready = {}
    for e in d.get("cure_claim_readiness") or []:
        if not isinstance(e, dict):
            continue
        name = str(e.get("artifact", "")).replace("\\", "/").split("/")[-1]
        ready[name] = e
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("sha256", ""))) or not isinstance(e.get("fit"), bool):
            defects.append("cure_claim_readiness entry for %s lacks a 64-hex sha256 or a boolean fit" % e.get("artifact"))
    for name in ("citation_sweep.py", "check_marks.py", "ezek_lib.py", "check_register.py", "check_web_quotes.py",
                 "normalize_hebrew_in_json.py", "_cure_verification.py"):
        if name not in ready:
            defects.append("cure_claim_readiness has no entry for %s" % name)
    sev = {}
    for f in d.get("new_findings", []):
        sev[str(f.get("severity"))] = sev.get(str(f.get("severity")), 0) + 1
    return {"verdict": d.get("verdict"),
            "sections": {k: (d.get(k) or {}).get("verdict") for k in ("r4ii_at_new_digests", "r4i_closure", "s1_07_and_newclass",
                                                                   "s1_06_ref_hebrew", "register_arms", "e15d", "verifier",
                                                                   "discrimination_discrepancy", "suite_parity")},
            "flags_tf2_1": {k: (fl.get(k) or {}).get("verdict") for k in ("removals_review", "w1", "w2", "w5", "w6")},
            "hand_review_strays_agree": strays, "candidates": len(fl.get("candidates") or []),
            "toolkit_md_verdict": tk.get("verdict"),
            "sibling_sweep": {"key_phrases": len(sw.get("key_phrases") or []), "statements_reviewed": sw.get("statements_reviewed")},
            "tests": t, "cure_claim_readiness": {n: [e.get("fit"), str(e.get("sha256", ""))[:16]] for n, e in ready.items()},
            "new_findings_by_severity": sev, "artifacts_not_reviewed": sorted(set(launch) - seen),
            "artifacts_read_beyond_the_table": EXTRAS.get("artifacts_reviewed", [])}


def validate_rulings_e3(d, launch, defects):
    """#e3 rules on its own queue: one ruling per queue id, allowed ruling values, the gate with author_wave_may_launch,
    and the inputs digest binding."""
    q = json.loads((EZ / "ezek_controlling_agent_queue_e3.v1.json").read_text(encoding="utf-8"))
    want = [i["id"] for i in q["items"]]
    got = [r.get("id") for r in d.get("rulings", [])]
    missing = [i for i in want if i not in got]
    dup = sorted({i for i in got if got.count(i) > 1})
    extra = [i for i in got if i not in want]
    if missing:
        defects.append("rulings missing for: %s" % ", ".join(missing))
    if dup:
        defects.append("more than one ruling for: %s" % ", ".join(dup))
    if extra:
        defects.append("rulings for ids not in the #e3 queue: %s" % ", ".join(map(str, extra)))
    allowed = {"ratify", "ratify_with_changes", "reverse", "adopt", "reject", "close", "keep_open", "defer", "amend", "hold", "cut"}
    bad = [(r.get("id"), r.get("ruling")) for r in d.get("rulings", []) if r.get("ruling") not in allowed]
    if bad:
        defects.append("ruling values not allowed: %s" % bad)
    if d.get("previous_execution_id") != "ezek_controlling_rulings_a1#e2":
        defects.append("previous_execution_id %r is not ezek_controlling_rulings_a1#e2" % d.get("previous_execution_id"))
    gate = d.get("gate") or {}
    for k in ("author_wave_may_launch", "primaries_may_launch", "conditions_before_primaries"):
        if k not in gate:
            defects.append("gate.%s absent" % k)
    seen = check_binding(d.get("inputs_ruled_on", []), "path", "sha256", launch, defects, "inputs_ruled_on")
    return {"expected_ids": len(want), "ruled_ids": len(set(got) & set(want)), "missing": missing,
            "rulings_by_kind": {k: sum(1 for r in d.get("rulings", []) if r.get("ruling") == k)
                                for k in sorted({str(r.get("ruling")) for r in d.get("rulings", [])})},
            "corpus_wide_orders": len(d.get("corpus_wide_orders", [])),
            "author_wave_may_launch": gate.get("author_wave_may_launch"), "primaries_may_launch": gate.get("primaries_may_launch"),
            "inputs_not_listed_in_inputs_ruled_on": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("inputs_ruled_on", [])}


def validate_rulings_e4(d, launch, defects):
    """#e4 rules on its own queue: one ruling per queue id, allowed ruling values, the primaries gate, and the inputs
    digest binding. The author-wave gate is spent, so only primaries_may_launch and conditions_before_primaries are
    required."""
    q = json.loads((EZ / "ezek_controlling_agent_queue_e4.v1.json").read_text(encoding="utf-8"))
    want = [i["id"] for i in q["items"]]
    got = [r.get("id") for r in d.get("rulings", [])]
    missing = [i for i in want if i not in got]
    dup = sorted({i for i in got if got.count(i) > 1})
    extra = [i for i in got if i not in want]
    if missing:
        defects.append("rulings missing for: %s" % ", ".join(missing))
    if dup:
        defects.append("more than one ruling for: %s" % ", ".join(dup))
    if extra:
        defects.append("rulings for ids not in the #e4 queue: %s" % ", ".join(map(str, extra)))
    allowed = {"ratify", "ratify_with_changes", "reverse", "adopt", "reject", "close", "keep_open", "defer", "amend", "hold", "cut"}
    bad = [(r.get("id"), r.get("ruling")) for r in d.get("rulings", []) if r.get("ruling") not in allowed]
    if bad:
        defects.append("ruling values not allowed: %s" % bad)
    if d.get("previous_execution_id") != "ezek_controlling_rulings_a1#e3":
        defects.append("previous_execution_id %r is not ezek_controlling_rulings_a1#e3" % d.get("previous_execution_id"))
    gate = d.get("gate") or {}
    for k in ("primaries_may_launch", "conditions_before_primaries"):
        if k not in gate:
            defects.append("gate.%s absent" % k)
    seen = check_binding(d.get("inputs_ruled_on", []), "path", "sha256", launch, defects, "inputs_ruled_on")
    return {"expected_ids": len(want), "ruled_ids": len(set(got) & set(want)), "missing": missing,
            "rulings_by_kind": {k: sum(1 for r in d.get("rulings", []) if r.get("ruling") == k)
                                for k in sorted({str(r.get("ruling")) for r in d.get("rulings", [])})},
            "corpus_wide_orders": len(d.get("corpus_wide_orders", [])),
            "primaries_may_launch": gate.get("primaries_may_launch"),
            "conditions_before_primaries": len(gate.get("conditions_before_primaries") or []),
            "inputs_not_listed_in_inputs_ruled_on": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("inputs_ruled_on", [])}


def validate_rulings_e5(d, launch, defects):
    """#e5 rules on its own queue: one ruling per queue id, allowed ruling values, the gate (toolfix2_may_install,
    primaries_may_launch, conditions_before_primaries), and the inputs digest binding."""
    q = json.loads((EZ / "ezek_controlling_agent_queue_e5.v1.json").read_text(encoding="utf-8"))
    want = [i["id"] for i in q["items"]]
    got = [r.get("id") for r in d.get("rulings", [])]
    missing = [i for i in want if i not in got]
    dup = sorted({i for i in got if got.count(i) > 1})
    extra = [i for i in got if i not in want]
    if missing:
        defects.append("rulings missing for: %s" % ", ".join(missing))
    if dup:
        defects.append("more than one ruling for: %s" % ", ".join(dup))
    if extra:
        defects.append("rulings for ids not in the #e5 queue: %s" % ", ".join(map(str, extra)))
    allowed = {"ratify", "ratify_with_changes", "reverse", "adopt", "reject", "close", "keep_open", "defer", "amend", "hold", "cut"}
    bad = [(r.get("id"), r.get("ruling")) for r in d.get("rulings", []) if r.get("ruling") not in allowed]
    if bad:
        defects.append("ruling values not allowed: %s" % bad)
    if d.get("previous_execution_id") != "ezek_controlling_rulings_a1#e4":
        defects.append("previous_execution_id %r is not ezek_controlling_rulings_a1#e4" % d.get("previous_execution_id"))
    gate = d.get("gate") or {}
    for k in ("toolfix2_may_install", "primaries_may_launch", "conditions_before_primaries"):
        if k not in gate:
            defects.append("gate.%s absent" % k)
    seen = check_binding(d.get("inputs_ruled_on", []), "path", "sha256", launch, defects, "inputs_ruled_on")
    return {"expected_ids": len(want), "ruled_ids": len(set(got) & set(want)), "missing": missing,
            "rulings_by_kind": {k: sum(1 for r in d.get("rulings", []) if r.get("ruling") == k)
                                for k in sorted({str(r.get("ruling")) for r in d.get("rulings", [])})},
            "toolfix2_may_install": gate.get("toolfix2_may_install"), "primaries_may_launch": gate.get("primaries_may_launch"),
            "inputs_not_listed_in_inputs_ruled_on": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("inputs_ruled_on", [])}


def validate_rulings_e6(d, launch, defects):
    """#e6 rules on its own queue: one ruling per queue id, allowed ruling values, previous_execution_id #e5, the gate
    (cwo18_real_run_may_proceed, cure_claims_may_be_written, primaries_may_launch, conditions_before_primaries), and the
    inputs digest binding."""
    q = json.loads((EZ / "ezek_controlling_agent_queue_e6.v1.json").read_text(encoding="utf-8"))
    want = [i["id"] for i in q["items"]]
    got = [r.get("id") for r in d.get("rulings", [])]
    missing = [i for i in want if i not in got]
    dup = sorted({i for i in got if got.count(i) > 1})
    extra = [i for i in got if i not in want]
    if missing:
        defects.append("rulings missing for: %s" % ", ".join(missing))
    if dup:
        defects.append("more than one ruling for: %s" % ", ".join(dup))
    if extra:
        defects.append("rulings for ids not in the #e6 queue: %s" % ", ".join(map(str, extra)))
    allowed = {"ratify", "ratify_with_changes", "reverse", "adopt", "reject", "close", "keep_open", "defer", "amend", "hold", "cut"}
    bad = [(r.get("id"), r.get("ruling")) for r in d.get("rulings", []) if r.get("ruling") not in allowed]
    if bad:
        defects.append("ruling values not allowed: %s" % bad)
    if d.get("previous_execution_id") != "ezek_controlling_rulings_a1#e5":
        defects.append("previous_execution_id %r is not ezek_controlling_rulings_a1#e5" % d.get("previous_execution_id"))
    gate = d.get("gate") or {}
    for k in ("cwo18_real_run_may_proceed", "cure_claims_may_be_written", "primaries_may_launch", "conditions_before_primaries"):
        if k not in gate:
            defects.append("gate.%s absent" % k)
    seen = check_binding(d.get("inputs_ruled_on", []), "path", "sha256", launch, defects, "inputs_ruled_on")
    return {"expected_ids": len(want), "ruled_ids": len(set(got) & set(want)), "missing": missing,
            "rulings_by_kind": {k: sum(1 for r in d.get("rulings", []) if r.get("ruling") == k)
                                for k in sorted({str(r.get("ruling")) for r in d.get("rulings", [])})},
            "cwo18_real_run_may_proceed": gate.get("cwo18_real_run_may_proceed"),
            "cure_claims_may_be_written": gate.get("cure_claims_may_be_written"), "primaries_may_launch": gate.get("primaries_may_launch"),
            "inputs_not_listed_in_inputs_ruled_on": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("inputs_ruled_on", [])}


def validate_rulings_e7(d, launch, defects):
    """#e7 rules on its own queue: one ruling per queue id, allowed ruling values, previous_execution_id #e6, the gate
    (cwo18_real_run_may_proceed, primaries_may_launch, conditions_before_primaries), and the inputs digest binding."""
    q = json.loads((EZ / "ezek_controlling_agent_queue_e7.v1.json").read_text(encoding="utf-8"))
    want = [i["id"] for i in q["items"]]
    got = [r.get("id") for r in d.get("rulings", [])]
    missing = [i for i in want if i not in got]
    dup = sorted({i for i in got if got.count(i) > 1})
    extra = [i for i in got if i not in want]
    if missing:
        defects.append("rulings missing for: %s" % ", ".join(missing))
    if dup:
        defects.append("more than one ruling for: %s" % ", ".join(dup))
    if extra:
        defects.append("rulings for ids not in the #e7 queue: %s" % ", ".join(map(str, extra)))
    allowed = {"ratify", "ratify_with_changes", "reverse", "adopt", "reject", "close", "keep_open", "defer", "amend", "hold", "cut"}
    bad = [(r.get("id"), r.get("ruling")) for r in d.get("rulings", []) if r.get("ruling") not in allowed]
    if bad:
        defects.append("ruling values not allowed: %s" % bad)
    if d.get("previous_execution_id") != "ezek_controlling_rulings_a1#e6":
        defects.append("previous_execution_id %r is not ezek_controlling_rulings_a1#e6" % d.get("previous_execution_id"))
    gate = d.get("gate") or {}
    for k in ("cwo18_real_run_may_proceed", "primaries_may_launch", "conditions_before_primaries"):
        if k not in gate:
            defects.append("gate.%s absent" % k)
    seen = check_binding(d.get("inputs_ruled_on", []), "path", "sha256", launch, defects, "inputs_ruled_on")
    return {"expected_ids": len(want), "ruled_ids": len(set(got) & set(want)), "missing": missing,
            "rulings_by_kind": {k: sum(1 for r in d.get("rulings", []) if r.get("ruling") == k)
                                for k in sorted({str(r.get("ruling")) for r in d.get("rulings", [])})},
            "cwo18_real_run_may_proceed": gate.get("cwo18_real_run_may_proceed"), "primaries_may_launch": gate.get("primaries_may_launch"),
            "inputs_not_listed_in_inputs_ruled_on": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("inputs_ruled_on", [])}


def validate_t6(d, launch, defects):
    """T6 reviews TOOLFIX-3's two files and the six claims appended under it. Form only:
      - the verdict and the digest binding;
      - verifier: a verdict, a boolean implemented_as_ruled for each rule (1)-(6), a non-empty attacks list, and a real_claims
        entry for both claims files;
      - appended_claims: a verdict, one per_claim entry per appended claim id, and a boolean third_entry_drafting.sound;
      - toolkit_md: a verdict, the R6 sibling sweep, and a confirmed/refuted verdict for each of (1), (2), (3), (a), (b), (c), (d);
      - integer verifier test counts;
      - a readiness entry, with a 64-hex digest and a boolean fit, for each of the two files;
      - unique finding ids with allowed severities."""
    verdicts = ("fit_to_accept", "fit_with_changes", "not_fit")
    six = ("EZEK-TK-CURE-citation_sweep", "EZEK-TK-CURE-check_marks", "EZEK-TK-CURE-ezek_lib-v2", "EZEK-TK-CURE-check_register",
           "EZEK-TK-CURE-check_web_quotes", "EZEK-TK-CURE-normalizer-v2")
    if d.get("verdict") not in verdicts:
        defects.append("verdict %r not in the allowed set" % d.get("verdict"))
    for e in d.get("artifacts_reviewed", []):
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("artifact_sha256_at_review", ""))):
            defects.append("artifacts_reviewed entry without a sha256: %s" % e.get("path"))
    seen = check_binding(d.get("artifacts_reviewed", []), "path", "artifact_sha256_at_review", launch, defects, "artifacts_reviewed")
    v = d.get("verifier") or {}
    if v.get("verdict") not in verdicts:
        defects.append("verifier.verdict %r not in the allowed set" % v.get("verdict"))
    rules = {str(x.get("rule")).strip(): x.get("implemented_as_ruled") for x in v.get("rules_checked") or [] if isinstance(x, dict)}
    for r_ in ("(1)", "(2)", "(3)", "(4)", "(5)", "(6)"):
        if not isinstance(rules.get(r_), bool):
            defects.append("verifier.rules_checked lacks a boolean implemented_as_ruled for %s" % r_)
    if not (isinstance(v.get("attacks"), list) and v["attacks"]):
        defects.append("verifier.attacks is empty")
    for cf in ("ezek_cure_claims.v1.jsonl", "ezek_cure_claims_toolkit_repair.v1.jsonl"):
        if cf not in (v.get("real_claims") or {}):
            defects.append("verifier.real_claims lacks %s" % cf)
    ac = d.get("appended_claims") or {}
    if ac.get("verdict") not in ("confirmed", "findings"):
        defects.append("appended_claims.verdict %r not in ['confirmed', 'findings']" % ac.get("verdict"))
    got = {str(x.get("cure_id")) for x in ac.get("per_claim") or [] if isinstance(x, dict)}
    for cid in six:
        if cid not in got:
            defects.append("appended_claims.per_claim lacks %s" % cid)
    if not isinstance((ac.get("third_entry_drafting") or {}).get("sound"), bool):
        defects.append("appended_claims.third_entry_drafting lacks a boolean sound")
    tk = d.get("toolkit_md") or {}
    if tk.get("verdict") not in verdicts:
        defects.append("toolkit_md.verdict %r not in the allowed set" % tk.get("verdict"))
    sw = tk.get("sibling_sweep") or {}
    if not (isinstance(sw.get("key_phrases"), list) and sw["key_phrases"] and isinstance(sw.get("statements_reviewed"), int)):
        defects.append("toolkit_md.sibling_sweep lacks non-empty key_phrases or an integer statements_reviewed (R6)")
    corr = {str(x.get("id")).strip(): x.get("verdict") for x in tk.get("corrections") or [] if isinstance(x, dict)}
    for c_ in ("(1)", "(2)", "(3)", "(a)", "(b)", "(c)", "(d)"):
        if corr.get(c_) not in ("confirmed", "refuted"):
            defects.append("toolkit_md.corrections lacks a confirmed/refuted verdict for %s" % c_)
    t = (d.get("tests") or {}).get("verifier") or {}
    if not all(isinstance(t.get(k), int) for k in ("vectors", "failed")):
        defects.append("tests.verifier lacks integer vectors/failed")
    ready = {str(e.get("artifact")): e for e in d.get("cure_claim_readiness") or [] if isinstance(e, dict)}
    for art in ("campaign/_cure_verification.py", "tools/TOOLKIT.md"):
        e = ready.get(art) or {}
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("sha256", ""))) or not isinstance(e.get("fit"), bool):
            defects.append("cure_claim_readiness lacks a 64-hex sha256 and a boolean fit for %s" % art)
    findings = [f for f in d.get("new_findings") or [] if isinstance(f, dict)]
    ids = [f.get("id") for f in findings]
    if len(ids) != len(set(ids)):
        defects.append("new_findings ids are not unique")
    bad = [f.get("id") for f in findings if f.get("severity") not in ("blocker", "major", "minor", "note")]
    if bad:
        defects.append("new_findings with a severity outside blocker/major/minor/note: %s" % bad)
    sev = {}
    for f in findings:
        sev[f.get("severity")] = sev.get(f.get("severity"), 0) + 1
    return {"verdict": d.get("verdict"), "verifier": v.get("verdict"), "appended_claims": ac.get("verdict"), "toolkit_md": tk.get("verdict"),
            "readiness": {a_: (ready.get(a_) or {}).get("fit") for a_ in ("campaign/_cure_verification.py", "tools/TOOLKIT.md")},
            "findings_by_severity": sev, "inputs_not_listed_in_artifacts_reviewed": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("artifacts_reviewed", [])}


def validate_rulings_e8(d, launch, defects):
    """#e8 rules on its own queue: one ruling per queue id, allowed ruling values, previous_execution_id #e7, the gate
    (s1_19_claim_may_be_written, primaries_may_launch, conditions_before_primaries), and the inputs digest binding."""
    q = json.loads((EZ / "ezek_controlling_agent_queue_e8.v1.json").read_text(encoding="utf-8"))
    want = [i["id"] for i in q["items"]]
    got = [r.get("id") for r in d.get("rulings", [])]
    missing = [i for i in want if i not in got]
    dup = sorted({i for i in got if got.count(i) > 1})
    extra = [i for i in got if i not in want]
    if missing:
        defects.append("rulings missing for: %s" % ", ".join(missing))
    if dup:
        defects.append("more than one ruling for: %s" % ", ".join(dup))
    if extra:
        defects.append("rulings for ids not in the #e8 queue: %s" % ", ".join(map(str, extra)))
    allowed = {"ratify", "ratify_with_changes", "reverse", "adopt", "reject", "close", "keep_open", "defer", "amend", "hold", "cut"}
    bad = [(r.get("id"), r.get("ruling")) for r in d.get("rulings", []) if r.get("ruling") not in allowed]
    if bad:
        defects.append("ruling values not allowed: %s" % bad)
    if d.get("previous_execution_id") != "ezek_controlling_rulings_a1#e7":
        defects.append("previous_execution_id %r is not ezek_controlling_rulings_a1#e7" % d.get("previous_execution_id"))
    gate = d.get("gate") or {}
    for k in ("s1_19_claim_may_be_written", "primaries_may_launch", "conditions_before_primaries"):
        if k not in gate:
            defects.append("gate.%s absent" % k)
    seen = check_binding(d.get("inputs_ruled_on", []), "path", "sha256", launch, defects, "inputs_ruled_on")
    return {"expected_ids": len(want), "ruled_ids": len(set(got) & set(want)), "missing": missing,
            "rulings_by_kind": {k: sum(1 for r in d.get("rulings", []) if r.get("ruling") == k)
                                for k in sorted({str(r.get("ruling")) for r in d.get("rulings", [])})},
            "s1_19_claim_may_be_written": gate.get("s1_19_claim_may_be_written"), "primaries_may_launch": gate.get("primaries_may_launch"),
            "inputs_not_listed_in_inputs_ruled_on": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("inputs_ruled_on", [])}


def validate_s2(d, launch, defects):
    """S2 reviews the FIXUP-1 wave (#e4 FIXUP-1 (5) and gate condition 7, the #e5 and #e6 read-back additions, and #e8 T6-01's
    verifier section). Form only:
      - the verdict; the rows digest reviewed equals repair/rows_v4_fixup1.jsonl on disk; the digest binding;
      - s1_majors: exactly S1-01..S1-07, each cured|not_cured;
      - resplice_readback: integer derived_count and index_count, a boolean index_matches_derivation, and one accept|defect
        entry per derived run;
      - p03_006_readback, corpus_impact, apply, coverage (with a non-empty recomputed) and flags: accept|defect;
      - register_readback: exactly the three coverage-limit rows with accept|defect, at least five evasion shapes with integer
        hits, and accept|defect;
      - sweep_manifests: CWO-EZ-13 and CWO-EZ-18, each with an integer changes_checked and accept|defect;
      - fixup_rows: a selection rule and at least 22 rows with accept|defect;
      - question_dispositions: exactly the ids of fixup1/fixup1_questions.v1.json, each tool_false_positive|row_defect|neither;
      - verifier_toolfix4: an allowed verdict, accept|defect for each of (i)-(vi), a boolean diff_confined, integer selftest
        counts, a non-empty attacks list, and a real_claims entry for both claims files;
      - cure_claim_readiness for campaign/_cure_verification.py at the TOOLFIX-4 digest and for repair/rows_v4_fixup1.jsonl at the
        rows digest, the latter with a status for every S1 id; each has a boolean fit, and a fit=true verdict string carries an
        ACCEPT form and no REFUSE token (#e8 T6-02);
      - unique S2-NN finding ids, allowed severities and exactly one allowed route each."""
    verdicts = ("fit_to_accept", "fit_with_changes", "not_fit")
    ok = ("accept", "defect")
    tf4 = "e02491bfc4bea6b1111d3b12d32850e4f26b14780301420d895b597220445d8f"
    accept_re = re.compile(r"\b(fit_to_accept|fit_with_changes|confirmed|accept(?:ed|able)?)\b")
    refuse_re = re.compile(r"\b(not_fit|not fit|unfit|refut\w*|reject\w*|blocker\w*|red)\b")
    s1_ids = ["S1-%02d" % i for i in range(1, 24)]
    rows_p = EZ / "repair" / "rows_v4_fixup1.jsonl"
    if d.get("verdict") not in verdicts:
        defects.append("verdict %r not in the allowed set" % d.get("verdict"))
    if (d.get("rows_file_reviewed") or {}).get("sha256") != sha(rows_p):
        defects.append("rows_file_reviewed.sha256 is not rows_v4_fixup1.jsonl %s" % sha(rows_p)[:16])
    for e in d.get("artifacts_reviewed") or []:
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("artifact_sha256_at_review", ""))):
            defects.append("artifacts_reviewed entry without a sha256: %s" % e.get("path"))
    seen = check_binding(d.get("artifacts_reviewed") or [], "path", "artifact_sha256_at_review", launch, defects, "artifacts_reviewed")
    maj = {str(x.get("id")): x.get("verdict") for x in d.get("s1_majors") or [] if isinstance(x, dict)}
    if sorted(maj) != ["S1-%02d" % i for i in range(1, 8)] or any(v not in ("cured", "not_cured") for v in maj.values()):
        defects.append("s1_majors must be exactly S1-01..S1-07, each cured|not_cured")
    rs = d.get("resplice_readback") or {}
    runs = rs.get("runs") if isinstance(rs.get("runs"), list) else []
    if not (isinstance(rs.get("derived_count"), int) and isinstance(rs.get("index_count"), int)
            and isinstance(rs.get("index_matches_derivation"), bool) and isinstance(rs.get("runs"), list)):
        defects.append("resplice_readback lacks integer counts, a boolean index_matches_derivation or a runs list")
    elif len(runs) != rs["derived_count"] or any(not isinstance(x, dict) or x.get("verdict") not in ok for x in runs):
        defects.append("resplice_readback.runs must hold one accept|defect entry per derived run (%d entries, derived_count %d)"
                       % (len(runs), rs["derived_count"]))
    for sec in ("p03_006_readback", "corpus_impact", "apply", "coverage", "flags"):
        if (d.get(sec) or {}).get("verdict") not in ok:
            defects.append("%s.verdict not accept|defect" % sec)
    if not (isinstance((d.get("coverage") or {}).get("recomputed"), dict) and d["coverage"]["recomputed"]):
        defects.append("coverage.recomputed is empty")
    rg = d.get("register_readback") or {}
    lim = {str(x.get("row")): x.get("verdict") for x in rg.get("coverage_limit_rows") or [] if isinstance(x, dict)}
    if sorted(lim) != ["P07-009", "P09-002", "P10-007"] or any(v not in ok for v in lim.values()):
        defects.append("register_readback.coverage_limit_rows must be exactly P07-009, P09-002, P10-007, each accept|defect")
    shapes = [x for x in rg.get("evasion_shapes") or [] if isinstance(x, dict)]
    if len(shapes) < 5 or any(not isinstance(x.get("hits"), int) for x in shapes):
        defects.append("register_readback.evasion_shapes needs at least five shapes with integer hits")
    if rg.get("verdict") not in ok:
        defects.append("register_readback.verdict not accept|defect")
    man = {str(x.get("manifest")): x for x in d.get("sweep_manifests") or [] if isinstance(x, dict)}
    for m in ("CWO-EZ-13", "CWO-EZ-18"):
        x = man.get(m) or {}
        if not isinstance(x.get("changes_checked"), int) or x.get("verdict") not in ok:
            defects.append("sweep_manifests lacks %s with an integer changes_checked and accept|defect" % m)
    fr = d.get("fixup_rows") or {}
    frows = [x for x in fr.get("rows") or [] if isinstance(x, dict)]
    if not str(fr.get("selection_rule", "")).strip() or len(frows) < 22 or any(x.get("verdict") not in ok for x in frows):
        defects.append("fixup_rows needs a selection_rule and at least 22 rows with accept|defect")
    qids = [q["id"] for q in json.loads((EZ / "fixup1" / "fixup1_questions.v1.json").read_text(encoding="utf-8"))["questions"]]
    qd = {str(x.get("id")): x.get("disposition") for x in d.get("question_dispositions") or [] if isinstance(x, dict)}
    if sorted(qd) != sorted(qids) or any(v not in ("tool_false_positive", "row_defect", "neither") for v in qd.values()):
        defects.append("question_dispositions must answer exactly %s, each tool_false_positive|row_defect|neither" % ", ".join(qids))
    v = d.get("verifier_toolfix4") or {}
    if v.get("verdict") not in verdicts:
        defects.append("verifier_toolfix4.verdict %r not in the allowed set" % v.get("verdict"))
    items = v.get("items") if isinstance(v.get("items"), dict) else {}
    for k in ("(i)", "(ii)", "(iii)", "(iv)", "(v)", "(vi)"):
        if items.get(k) not in ok:
            defects.append("verifier_toolfix4.items lacks accept|defect for %s" % k)
    if not isinstance(v.get("diff_confined"), bool):
        defects.append("verifier_toolfix4.diff_confined is not a boolean")
    st = v.get("selftest") if isinstance(v.get("selftest"), dict) else {}
    if not (isinstance(st.get("vectors"), int) and isinstance(st.get("failed"), int)):
        defects.append("verifier_toolfix4.selftest lacks integer vectors and failed")
    if not (isinstance(v.get("attacks"), list) and v["attacks"]):
        defects.append("verifier_toolfix4.attacks is empty")
    for cf in ("ezek_cure_claims.v1.jsonl", "ezek_cure_claims_toolkit_repair.v1.jsonl"):
        if cf not in (v.get("real_claims") or {}):
            defects.append("verifier_toolfix4.real_claims lacks %s" % cf)
    ready = {str(x.get("artifact")): x for x in d.get("cure_claim_readiness") or [] if isinstance(x, dict)}
    for art, want in (("campaign/_cure_verification.py", tf4), ("repair/rows_v4_fixup1.jsonl", sha(rows_p))):
        x = ready.get(art)
        if not x:
            defects.append("cure_claim_readiness lacks %s" % art)
            continue
        if x.get("sha256") != want:
            defects.append("cure_claim_readiness %s sha256 is not %s" % (art, want[:16]))
        if not isinstance(x.get("fit"), bool):
            defects.append("cure_claim_readiness %s lacks a boolean fit" % art)
        elif x["fit"] and not (accept_re.search(str(x.get("verdict", ""))) and not refuse_re.search(str(x.get("verdict", "")))):
            defects.append("cure_claim_readiness %s: a fit=true verdict needs an ACCEPT form and no REFUSE token (#e8 T6-02)" % art)
    per = {str(x.get("id")): x.get("status") for x in (ready.get("repair/rows_v4_fixup1.jsonl") or {}).get("per_s1_id") or []
           if isinstance(x, dict)}
    if sorted(per) != s1_ids or any(s not in ("cured", "not_cured", "not_applicable") for s in per.values()):
        defects.append("cure_claim_readiness repair/rows_v4_fixup1.jsonl per_s1_id must give S1-01..S1-23, each "
                       "cured|not_cured|not_applicable")
    nf = [f for f in d.get("new_findings") or [] if isinstance(f, dict)]
    ids = [str(f.get("id")) for f in nf]
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r"S2-\d\d", i) for i in ids):
        defects.append("new_findings ids must be unique S2-NN")
    if any(f.get("severity") not in ("blocker", "major", "minor", "note") for f in nf):
        defects.append("new_findings with a severity outside blocker|major|minor|note")
    badr = [str(f.get("route")) for f in nf if not re.fullmatch(r"author_fixup:p\d\d|orchestrator|controlling_agent", str(f.get("route", "")))]
    if badr:
        defects.append("new_findings with a route outside author_fixup:pNN|orchestrator|controlling_agent: %s" % badr[:5])
    sev = {}
    for f in nf:
        sev[str(f.get("severity"))] = sev.get(str(f.get("severity")), 0) + 1
    return {"verdict": d.get("verdict"), "s1_majors": maj, "resplice_runs": rs.get("derived_count"),
            "resplice_defects": sum(1 for x in runs if isinstance(x, dict) and x.get("verdict") == "defect"),
            "fixup_rows": len(frows), "fixup_row_defects": sum(1 for x in frows if x.get("verdict") == "defect"),
            "question_dispositions": qd, "verifier": v.get("verdict"),
            "readiness": {k: x.get("fit") for k, x in ready.items()}, "new_findings_by_severity": sev,
            "inputs_not_listed_in_artifacts_reviewed": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("artifacts_reviewed", [])}


def validate_rulings_e9(d, launch, defects):
    """#e9 rules on its own queue: one ruling per queue id, allowed ruling values, previous_execution_id #e8, the gate
    (fixup2_may_launch, primaries_may_launch, conditions_before_primaries), and the inputs digest binding."""
    q = json.loads((EZ / "ezek_controlling_agent_queue_e9.v1.json").read_text(encoding="utf-8"))
    want = [i["id"] for i in q["items"]]
    got = [r.get("id") for r in d.get("rulings", [])]
    missing = [i for i in want if i not in got]
    dup = sorted({i for i in got if got.count(i) > 1})
    extra = [i for i in got if i not in want]
    if missing:
        defects.append("rulings missing for: %s" % ", ".join(missing))
    if dup:
        defects.append("more than one ruling for: %s" % ", ".join(dup))
    if extra:
        defects.append("rulings for ids not in the #e9 queue: %s" % ", ".join(map(str, extra)))
    allowed = {"ratify", "ratify_with_changes", "reverse", "adopt", "reject", "close", "keep_open", "defer", "amend", "hold", "cut"}
    bad = [(r.get("id"), r.get("ruling")) for r in d.get("rulings", []) if r.get("ruling") not in allowed]
    if bad:
        defects.append("ruling values not allowed: %s" % bad)
    if d.get("previous_execution_id") != "ezek_controlling_rulings_a1#e8":
        defects.append("previous_execution_id %r is not ezek_controlling_rulings_a1#e8" % d.get("previous_execution_id"))
    gate = d.get("gate") or {}
    for k in ("fixup2_may_launch", "primaries_may_launch", "conditions_before_primaries"):
        if k not in gate:
            defects.append("gate.%s absent" % k)
    seen = check_binding(d.get("inputs_ruled_on", []), "path", "sha256", launch, defects, "inputs_ruled_on")
    return {"expected_ids": len(want), "ruled_ids": len(set(got) & set(want)), "missing": missing,
            "rulings_by_kind": {k: sum(1 for r in d.get("rulings", []) if r.get("ruling") == k)
                                for k in sorted({str(r.get("ruling")) for r in d.get("rulings", [])})},
            "fixup2_may_launch": gate.get("fixup2_may_launch"), "primaries_may_launch": gate.get("primaries_may_launch"),
            "inputs_not_listed_in_inputs_ruled_on": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("inputs_ruled_on", [])}


def validate_s3(d, launch, defects):
    """S3 (#e9 S2-ROUTING (7)): the verdict; the rows file at rows_v5_fixup2's digest; artifacts bound by digest; S2-01's three rows read
    back first; one entry per replaced row; the governance-kin search; ten or more mark disclosures; one entry per per-element re-splice
    run; the three tool diffs; apply, coverage, sidecars and the CWO-EZ-19/20/21 manifests; every FIXUP-2 question; readiness for
    rows_v5_fixup2 in the #e8 T6-02 ACCEPT wording with per-S1 and per-S2 statuses; unique S3-NN findings with allowed routes."""
    verdicts = ("fit_to_accept", "fit_with_changes", "not_fit")
    ok = ("accept", "defect")
    statuses = ("cured", "not_cured", "not_applicable")
    accept_re = re.compile(r"\b(fit_to_accept|fit_with_changes|confirmed|accept(?:ed|able)?)\b")
    refuse_re = re.compile(r"\b(not_fit|not fit|unfit|refut\w*|reject\w*|blocker\w*|red)\b")
    rows_p = EZ / "repair" / "rows_v5_fixup2.jsonl"
    man = json.loads((EZ / "repair" / "rows_v5_fixup2.manifest.json").read_text(encoding="utf-8"))
    if d.get("verdict") not in verdicts:
        defects.append("verdict %r not in the allowed set" % d.get("verdict"))
    if (d.get("rows_file_reviewed") or {}).get("sha256") != sha(rows_p):
        defects.append("rows_file_reviewed.sha256 is not rows_v5_fixup2.jsonl %s" % sha(rows_p)[:16])
    for e in d.get("artifacts_reviewed") or []:
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("artifact_sha256_at_review", ""))):
            defects.append("artifacts_reviewed entry without a sha256: %s" % e.get("path"))
    seen = check_binding(d.get("artifacts_reviewed") or [], "path", "artifact_sha256_at_review", launch, defects, "artifacts_reviewed")
    s201 = {str(x.get("row")): x.get("verdict") for x in (d.get("s2_01_readback") or {}).get("rows") or [] if isinstance(x, dict)}
    if sorted(s201) != ["P08-001", "P08-002", "P08-004"] or any(v not in ("cured", "not_cured") for v in s201.values()):
        defects.append("s2_01_readback.rows must be exactly P08-001, P08-002, P08-004, each cured|not_cured")
    rr = {str(x.get("row")): x.get("verdict") for x in d.get("replaced_rows") or [] if isinstance(x, dict)}
    if sorted(rr) != sorted(man.get("replaced", [])) or any(v not in ok for v in rr.values()):
        defects.append("replaced_rows must give every replaced row of the apply manifest (%d), each accept|defect" % len(man.get("replaced", [])))
    gs = [x for x in (d.get("governance_search") or {}).get("shapes") or [] if isinstance(x, dict)]
    if len(gs) < 8 or any(not isinstance(x.get("hits"), int) for x in gs) or (d.get("governance_search") or {}).get("verdict") not in ok:
        defects.append("governance_search needs at least eight shapes with integer hits and an accept|defect verdict")
    ms = [x for x in (d.get("mark_sample") or {}).get("rows") or [] if isinstance(x, dict)]
    if len(ms) < 10 or any(x.get("verdict") not in ok for x in ms):
        defects.append("mark_sample needs at least ten disclosures, each accept|defect")
    rs = d.get("resplice_readback") or {}
    runs = rs.get("runs") if isinstance(rs.get("runs"), list) else []
    if not (isinstance(rs.get("derived_count"), int) and isinstance(rs.get("index_count"), int)
            and isinstance(rs.get("index_matches_derivation"), bool) and isinstance(rs.get("runs"), list)):
        defects.append("resplice_readback lacks integer counts, a boolean index_matches_derivation or a runs list")
    elif len(runs) != rs["derived_count"] or any(not isinstance(x, dict) or x.get("verdict") not in ok for x in runs):
        defects.append("resplice_readback.runs must hold one accept|defect entry per derived run (%d entries, derived_count %d)"
                       % (len(runs), rs["derived_count"]))
    td = d.get("tool_diffs") if isinstance(d.get("tool_diffs"), dict) else {}
    for f in ("_land_author_part_ezek.py", "_apply_author_wave_ezek.py", "_cwo_coverage_fixup1_ezek.py"):
        x = td.get(f) if isinstance(td.get(f), dict) else {}
        if x.get("verdict") not in ok or not isinstance(x.get("diff_confined"), bool):
            defects.append("tool_diffs lacks %s with an accept|defect verdict and a boolean diff_confined" % f)
    for sec in ("apply", "coverage", "sidecars"):
        if (d.get(sec) or {}).get("verdict") not in ok:
            defects.append("%s.verdict not accept|defect" % sec)
    if not (isinstance((d.get("coverage") or {}).get("recomputed"), dict) and d["coverage"]["recomputed"]):
        defects.append("coverage.recomputed is empty")
    sm = {str(x.get("manifest")): x for x in d.get("sweep_manifests") or [] if isinstance(x, dict)}
    for m in ("CWO-EZ-19", "CWO-EZ-20", "CWO-EZ-21"):
        x = sm.get(m) or {}
        if not isinstance(x.get("changes_checked"), int) or x.get("verdict") not in ok:
            defects.append("sweep_manifests lacks %s with an integer changes_checked and accept|defect" % m)
    qids = [q["id"] for q in json.loads((EZ / "fixup2" / "fixup2_questions.v1.json").read_text(encoding="utf-8"))["questions"]]
    qd = {str(x.get("id")): x.get("disposition") for x in d.get("question_dispositions") or [] if isinstance(x, dict)}
    if sorted(qd) != sorted(qids) or any(v not in ("tool_false_positive", "row_defect", "neither") for v in qd.values()):
        defects.append("question_dispositions must answer exactly %s, each tool_false_positive|row_defect|neither" % ", ".join(qids))
    ready = {str(x.get("artifact")): x for x in d.get("cure_claim_readiness") or [] if isinstance(x, dict)}
    x = ready.get("repair/rows_v5_fixup2.jsonl")
    if not x:
        defects.append("cure_claim_readiness lacks repair/rows_v5_fixup2.jsonl")
    else:
        if x.get("sha256") != sha(rows_p):
            defects.append("cure_claim_readiness rows_v5_fixup2 sha256 is not %s" % sha(rows_p)[:16])
        if not isinstance(x.get("fit"), bool):
            defects.append("cure_claim_readiness rows_v5_fixup2 lacks a boolean fit")
        elif x["fit"] and not (accept_re.search(str(x.get("verdict", ""))) and not refuse_re.search(str(x.get("verdict", "")))):
            defects.append("cure_claim_readiness rows_v5_fixup2: a fit=true verdict needs an ACCEPT form and no REFUSE token (#e8 T6-02)")
        p1 = {str(y.get("id")): y.get("status") for y in x.get("per_s1_id") or [] if isinstance(y, dict)}
        if not {"S1-05", "S1-15"} <= set(p1) or any(s not in statuses for s in p1.values()):
            defects.append("cure_claim_readiness per_s1_id must include S1-05 and S1-15, each cured|not_cured|not_applicable")
        p2 = {str(y.get("id")): y.get("status") for y in x.get("per_s2_id") or [] if isinstance(y, dict)}
        if sorted(p2) != ["S2-%02d" % i for i in range(1, 18)] or any(s not in statuses for s in p2.values()):
            defects.append("cure_claim_readiness per_s2_id must give S2-01..S2-17, each cured|not_cured|not_applicable")
    nf = [f for f in d.get("new_findings") or [] if isinstance(f, dict)]
    ids = [str(f.get("id")) for f in nf]
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r"S3-\d\d", i) for i in ids):
        defects.append("new_findings ids must be unique S3-NN")
    if any(f.get("severity") not in ("blocker", "major", "minor", "note") for f in nf):
        defects.append("new_findings with a severity outside blocker|major|minor|note")
    badr = [str(f.get("route")) for f in nf if not re.fullmatch(r"author_fixup:p\d\d|orchestrator|controlling_agent", str(f.get("route", "")))]
    if badr:
        defects.append("new_findings with a route outside author_fixup:pNN|orchestrator|controlling_agent: %s" % badr[:5])
    sev = {}
    for f in nf:
        sev[str(f.get("severity"))] = sev.get(str(f.get("severity")), 0) + 1
    return {"verdict": d.get("verdict"), "s2_01": s201, "replaced_rows": len(rr),
            "replaced_row_defects": sum(1 for v in rr.values() if v == "defect"), "resplice_runs": rs.get("derived_count"),
            "resplice_defects": sum(1 for y in runs if isinstance(y, dict) and y.get("verdict") == "defect"),
            "mark_sample": len(ms), "question_dispositions": qd,
            "readiness": {k: y.get("fit") for k, y in ready.items()}, "new_findings_by_severity": sev,
            "inputs_not_listed_in_artifacts_reviewed": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("artifacts_reviewed", [])}


def validate_rulings_e10(d, launch, defects):
    """#e10 rules on its own queue: one ruling per queue id, allowed ruling values, previous_execution_id #e9, the gate
    (fixup3_may_launch, s4_may_launch, primaries_may_launch, conditions_before_primaries), and the inputs digest binding."""
    q = json.loads((EZ / "ezek_controlling_agent_queue_e10.v1.json").read_text(encoding="utf-8"))
    want = [i["id"] for i in q["items"]]
    got = [r.get("id") for r in d.get("rulings", [])]
    missing = [i for i in want if i not in got]
    dup = sorted({i for i in got if got.count(i) > 1})
    extra = [i for i in got if i not in want]
    if missing:
        defects.append("rulings missing for: %s" % ", ".join(missing))
    if dup:
        defects.append("more than one ruling for: %s" % ", ".join(dup))
    if extra:
        defects.append("rulings for ids not in the #e10 queue: %s" % ", ".join(map(str, extra)))
    allowed = {"ratify", "ratify_with_changes", "reverse", "adopt", "reject", "close", "keep_open", "defer", "amend", "hold", "cut"}
    bad = [(r.get("id"), r.get("ruling")) for r in d.get("rulings", []) if r.get("ruling") not in allowed]
    if bad:
        defects.append("ruling values not allowed: %s" % bad)
    if d.get("previous_execution_id") != "ezek_controlling_rulings_a1#e9":
        defects.append("previous_execution_id %r is not ezek_controlling_rulings_a1#e9" % d.get("previous_execution_id"))
    gate = d.get("gate") or {}
    for k in ("fixup3_may_launch", "s4_may_launch", "primaries_may_launch", "conditions_before_primaries"):
        if k not in gate:
            defects.append("gate.%s absent" % k)
    seen = check_binding(d.get("inputs_ruled_on", []), "path", "sha256", launch, defects, "inputs_ruled_on")
    return {"expected_ids": len(want), "ruled_ids": len(set(got) & set(want)), "missing": missing,
            "rulings_by_kind": {k: sum(1 for r in d.get("rulings", []) if r.get("ruling") == k)
                                for k in sorted({str(r.get("ruling")) for r in d.get("rulings", [])})},
            "fixup3_may_launch": gate.get("fixup3_may_launch"), "s4_may_launch": gate.get("s4_may_launch"),
            "primaries_may_launch": gate.get("primaries_may_launch"),
            "inputs_not_listed_in_inputs_ruled_on": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("inputs_ruled_on", [])}


def validate_s4(d, launch, defects):
    """S4 (#e10 S3-ROUTING (7)), a fresh distinct checker on claude-fable-5-1 (OW-13). It must give:
      - the verdict, and the rows file at rows_v6_fixup3's digest, with artifacts bound by digest;
      - P04-008 read back first, then one entry per replaced row of the v6 apply manifest;
      - all 33 CWO-EZ-23 pairs, and the governance-kin search with CWO-EZ-22's arms;
      - the twelve p03 prose disclosures and ten or more others, and one entry per per-element re-splice run;
      - the three tool diffs, the apply, and every CWO predicate recomputed (CWO-EZ-01..09, 14..23);
      - every FIXUP-3 question, and readiness for rows_v6_fixup3 in the #e8 T6-02 ACCEPT wording with per-S1, per-S2 and per-S3
        statuses;
      - unique S4-NN findings with allowed routes."""
    verdicts = ("fit_to_accept", "fit_with_changes", "not_fit")
    ok = ("accept", "defect")
    statuses = ("cured", "not_cured", "not_applicable")
    accept_re = re.compile(r"\b(fit_to_accept|fit_with_changes|confirmed|accept(?:ed|able)?)\b")
    refuse_re = re.compile(r"\b(not_fit|not fit|unfit|refut\w*|reject\w*|blocker\w*|red)\b")
    rows_p = EZ / "repair" / "rows_v6_fixup3.jsonl"
    man = json.loads((EZ / "repair" / "rows_v6_fixup3.manifest.json").read_text(encoding="utf-8"))
    if d.get("verdict") not in verdicts:
        defects.append("verdict %r not in the allowed set" % d.get("verdict"))
    if (d.get("rows_file_reviewed") or {}).get("sha256") != sha(rows_p):
        defects.append("rows_file_reviewed.sha256 is not rows_v6_fixup3.jsonl %s" % sha(rows_p)[:16])
    for e in d.get("artifacts_reviewed") or []:
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("artifact_sha256_at_review", ""))):
            defects.append("artifacts_reviewed entry without a sha256: %s" % e.get("path"))
    seen = check_binding(d.get("artifacts_reviewed") or [], "path", "artifact_sha256_at_review", launch, defects, "artifacts_reviewed")
    rb = d.get("p04_008_readback") if isinstance(d.get("p04_008_readback"), dict) else {}
    if rb.get("verdict") not in ("cured", "not_cured"):
        defects.append("p04_008_readback.verdict must be cured|not_cured")
    rr = {str(x.get("row")): x.get("verdict") for x in d.get("replaced_rows") or [] if isinstance(x, dict)}
    if sorted(rr) != sorted(man.get("replaced", [])) or any(v not in ok for v in rr.values()):
        defects.append("replaced_rows must give every replaced row of the apply manifest (%d), each accept|defect" % len(man.get("replaced", [])))
    cp = d.get("cwo_ez_23_pairs") if isinstance(d.get("cwo_ez_23_pairs"), dict) else {}
    if cp.get("pairs_checked") != 33 or cp.get("verdict") not in ok:
        defects.append("cwo_ez_23_pairs must check all 33 ruled pairs, with an accept|defect verdict")
    gs = [x for x in (d.get("governance_search") or {}).get("shapes") or [] if isinstance(x, dict)]
    if len(gs) < 8 or any(not isinstance(x.get("hits"), int) for x in gs) or (d.get("governance_search") or {}).get("verdict") not in ok:
        defects.append("governance_search needs at least eight shapes with integer hits and an accept|defect verdict")
    md = d.get("mark_disclosures") if isinstance(d.get("mark_disclosures"), dict) else {}
    p03 = [x for x in md.get("p03") or [] if isinstance(x, dict)]
    oth = [x for x in md.get("others") or [] if isinstance(x, dict)]
    if len(p03) != 12 or any(x.get("verdict") not in ok for x in p03):
        defects.append("mark_disclosures.p03 must hold the twelve S3-03 items, each accept|defect")
    if len(oth) < 10 or any(x.get("verdict") not in ok for x in oth):
        defects.append("mark_disclosures.others needs at least ten disclosures, each accept|defect")
    rs = d.get("resplice_readback") or {}
    runs = rs.get("runs") if isinstance(rs.get("runs"), list) else []
    if not (isinstance(rs.get("derived_count"), int) and isinstance(rs.get("index_count"), int)
            and isinstance(rs.get("index_matches_derivation"), bool) and isinstance(rs.get("runs"), list)):
        defects.append("resplice_readback lacks integer counts, a boolean index_matches_derivation or a runs list")
    elif len(runs) != rs["derived_count"] or any(not isinstance(x, dict) or x.get("verdict") not in ok for x in runs):
        defects.append("resplice_readback.runs must hold one accept|defect entry per derived run (%d entries, derived_count %d)"
                       % (len(runs), rs["derived_count"]))
    td = d.get("tool_diffs") if isinstance(d.get("tool_diffs"), dict) else {}
    for f in ("check_register.py", "check_web_quotes.py", "_cwo_coverage_s2_ezek.py"):
        x = td.get(f) if isinstance(td.get(f), dict) else {}
        if x.get("verdict") not in ok or not isinstance(x.get("diff_confined"), bool):
            defects.append("tool_diffs lacks %s with an accept|defect verdict and a boolean diff_confined" % f)
    if (d.get("apply") or {}).get("verdict") not in ok:
        defects.append("apply.verdict not accept|defect")
    cr = d.get("cwo_recomputed") if isinstance(d.get("cwo_recomputed"), dict) else {}
    res = cr.get("residuals") if isinstance(cr.get("residuals"), dict) else {}
    want = ["CWO-EZ-%02d" % i for i in list(range(1, 10)) + list(range(14, 24))]
    if sorted(res) != want or any(not isinstance(v, int) for v in res.values()) or cr.get("verdict") not in ok:
        defects.append("cwo_recomputed.residuals must give integer residuals for CWO-EZ-01..09 and 14..23, with an accept|defect verdict")
    qids = [q["id"] for q in json.loads((EZ / "fixup3" / "fixup3_questions.v1.json").read_text(encoding="utf-8"))["questions"]]
    qd = {str(x.get("id")): x.get("disposition") for x in d.get("question_dispositions") or [] if isinstance(x, dict)}
    if sorted(qd) != sorted(qids) or any(v not in ("tool_false_positive", "row_defect", "neither") for v in qd.values()):
        defects.append("question_dispositions must answer exactly %s, each tool_false_positive|row_defect|neither" % ", ".join(qids))
    if (d.get("flags") or {}).get("verdict") not in ok:
        defects.append("flags.verdict not accept|defect")
    ready = {str(x.get("artifact")): x for x in d.get("cure_claim_readiness") or [] if isinstance(x, dict)}
    x = ready.get("repair/rows_v6_fixup3.jsonl")
    if not x:
        defects.append("cure_claim_readiness lacks repair/rows_v6_fixup3.jsonl")
    else:
        if x.get("sha256") != sha(rows_p):
            defects.append("cure_claim_readiness rows_v6_fixup3 sha256 is not %s" % sha(rows_p)[:16])
        if not isinstance(x.get("fit"), bool):
            defects.append("cure_claim_readiness rows_v6_fixup3 lacks a boolean fit")
        elif x["fit"] and not (accept_re.search(str(x.get("verdict", ""))) and not refuse_re.search(str(x.get("verdict", "")))):
            defects.append("cure_claim_readiness rows_v6_fixup3: a fit=true verdict needs an ACCEPT form and no REFUSE token (#e8 T6-02)")
        p1 = {str(y.get("id")): y.get("status") for y in x.get("per_s1_id") or [] if isinstance(y, dict)}
        if not {"S1-05", "S1-15"} <= set(p1) or any(s not in statuses for s in p1.values()):
            defects.append("cure_claim_readiness per_s1_id must include S1-05 and S1-15, each cured|not_cured|not_applicable")
        p2 = {str(y.get("id")): y.get("status") for y in x.get("per_s2_id") or [] if isinstance(y, dict)}
        if sorted(p2) != ["S2-%02d" % i for i in range(1, 18)] or any(s not in statuses for s in p2.values()):
            defects.append("cure_claim_readiness per_s2_id must give S2-01..S2-17, each cured|not_cured|not_applicable")
        p3 = {str(y.get("id")): y.get("status") for y in x.get("per_s3_id") or [] if isinstance(y, dict)}
        if sorted(p3) != ["S3-%02d" % i for i in range(1, 21)] or any(s not in statuses for s in p3.values()):
            defects.append("cure_claim_readiness per_s3_id must give S3-01..S3-20, each cured|not_cured|not_applicable")
    nf = [f for f in d.get("new_findings") or [] if isinstance(f, dict)]
    ids = [str(f.get("id")) for f in nf]
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r"S4-\d\d", i) for i in ids):
        defects.append("new_findings ids must be unique S4-NN")
    if any(f.get("severity") not in ("blocker", "major", "minor", "note") for f in nf):
        defects.append("new_findings with a severity outside blocker|major|minor|note")
    badr = [str(f.get("route")) for f in nf if not re.fullmatch(r"author_fixup:p\d\d|orchestrator|controlling_agent", str(f.get("route", "")))]
    if badr:
        defects.append("new_findings with a route outside author_fixup:pNN|orchestrator|controlling_agent: %s" % badr[:5])
    sev = {}
    for f in nf:
        sev[str(f.get("severity"))] = sev.get(str(f.get("severity")), 0) + 1
    return {"verdict": d.get("verdict"), "p04_008": rb.get("verdict"), "replaced_rows": len(rr),
            "replaced_row_defects": sum(1 for v in rr.values() if v == "defect"), "cwo_ez_23_pairs": cp.get("verdict"),
            "resplice_runs": rs.get("derived_count"), "resplice_defects": sum(1 for y in runs if isinstance(y, dict) and y.get("verdict") == "defect"),
            "mark_disclosures": {"p03": len(p03), "others": len(oth)}, "cwo_recomputed": res, "question_dispositions": qd,
            "readiness": {k: y.get("fit") for k, y in ready.items()}, "new_findings_by_severity": sev,
            "inputs_not_listed_in_artifacts_reviewed": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("artifacts_reviewed", [])}


def validate_rulings_e11(d, launch, defects):
    """#e11 rules on its own queue: one ruling per queue id, allowed ruling values, previous_execution_id #e10, the gate
    (primaries_may_launch, conditions_before_primaries, and the lane models OW-13 requires it to name), and the inputs
    digest binding. Form only: the orchestrator executes rulings and never re-rules them."""
    q = json.loads((EZ / "ezek_controlling_agent_queue_e11.v1.json").read_text(encoding="utf-8"))
    want = [i["id"] for i in q["items"]]
    got = [r.get("id") for r in d.get("rulings", [])]
    missing = [i for i in want if i not in got]
    dup = sorted({i for i in got if got.count(i) > 1})
    extra = [i for i in got if i not in want]
    if missing:
        defects.append("rulings missing for: %s" % ", ".join(missing))
    if dup:
        defects.append("more than one ruling for: %s" % ", ".join(dup))
    if extra:
        defects.append("rulings for ids not in the #e11 queue: %s" % ", ".join(map(str, extra)))
    allowed = {"ratify", "ratify_with_changes", "reverse", "adopt", "reject", "close", "keep_open", "defer", "amend", "hold", "cut"}
    bad = [(r.get("id"), r.get("ruling")) for r in d.get("rulings", []) if r.get("ruling") not in allowed]
    if bad:
        defects.append("ruling values not allowed: %s" % bad)
    if d.get("previous_execution_id") != "ezek_controlling_rulings_a1#e10":
        defects.append("previous_execution_id %r is not ezek_controlling_rulings_a1#e10" % d.get("previous_execution_id"))
    gate = d.get("gate") or {}
    for k in ("primaries_may_launch", "conditions_before_primaries"):
        if k not in gate:
            defects.append("gate.%s absent" % k)
    lanes = d.get("lane_models") or {}
    if not isinstance(lanes, dict) or not lanes:
        defects.append("lane_models absent: OW-13 requires this execution to name the model for each lane it authorises")
    else:
        for lane in ("primaries_lf", "primaries_ol", "peer", "boss", "author_wave"):
            e = lanes.get(lane)
            if not isinstance(e, dict) or not str(e.get("model", "")).strip() or not str(e.get("reason", "")).strip():
                defects.append("lane_models.%s needs a model and a reason (OW-13)" % lane)
    seen = check_binding(d.get("inputs_ruled_on", []), "path", "sha256", launch, defects, "inputs_ruled_on")
    return {"expected_ids": len(want), "ruled_ids": len(set(got) & set(want)), "missing": missing,
            "rulings_by_kind": {k: sum(1 for r in d.get("rulings", []) if r.get("ruling") == k)
                                for k in sorted({str(r.get("ruling")) for r in d.get("rulings", [])})},
            "primaries_may_launch": gate.get("primaries_may_launch"),
            "lane_models": {k: (v or {}).get("model") for k, v in (lanes.items() if isinstance(lanes, dict) else [])},
            "corpus_wide_orders": len(d.get("corpus_wide_orders", [])),
            "inputs_not_listed_in_inputs_ruled_on": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("inputs_ruled_on", [])}


def validate_s5(d, launch, defects):
    """S5 (#e11 S4-ROUTING (8) + TRANSCRIPT-ROUTE): the narrow distinct check over CWO-EZ-24 and the transcript batch.
    Form only. Every key read here appears in the brief's deliverable schema (L-0018)."""
    verdicts = ("fit_to_accept", "fit_with_changes", "not_fit")
    ok = ("accept", "defect")
    # CASE-INSENSITIVE, unlike the three sibling validators above. S5 returned the textbook ACCEPT sentence
    # "ACCEPT: rows_v7_cwo24.jsonl is fit for the primaries" and the case-sensitive pattern refused it, because
    # \baccept\b does not match "ACCEPT". The refuse set is made case-insensitive in the same step, since a
    # verdict shouting "REJECT" must still be caught. The same latent defect stands in the sibling validators
    # and is RECORDED for the controlling agent rather than changed here: they have landed executions and their
    # behaviour is part of that record.
    accept_re = re.compile(r"\b(fit_to_accept|fit_with_changes|confirmed|accept(?:ed|able)?)\b", re.I)
    refuse_re = re.compile(r"\b(not_fit|not fit|unfit|refut\w*|reject\w*|blocker\w*|red)\b", re.I)
    rows_p = EZ / "repair" / "rows_v7_cwo24.jsonl"
    if d.get("verdict") not in verdicts:
        defects.append("verdict %r not in the allowed set" % d.get("verdict"))
    if (d.get("rows_file_reviewed") or {}).get("sha256") != sha(rows_p):
        defects.append("rows_file_reviewed.sha256 is not rows_v7_cwo24.jsonl %s" % sha(rows_p)[:16])
    for e in d.get("artifacts_reviewed") or []:
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("artifact_sha256_at_review", ""))):
            defects.append("artifacts_reviewed entry without a sha256: %s" % e.get("path"))
    seen = check_binding(d.get("artifacts_reviewed") or [], "path", "artifact_sha256_at_review", launch, defects,
                         "artifacts_reviewed")
    pairs = d.get("cwo_ez_24_pairs") if isinstance(d.get("cwo_ez_24_pairs"), dict) else {}
    if pairs.get("pairs_checked") != 18 or pairs.get("verdict") not in ok:
        defects.append("cwo_ez_24_pairs must check all 18 ruled pairs, with an accept|defect verdict")
    per = [x for x in pairs.get("per_pair") or [] if isinstance(x, dict)]
    if len(per) != 18 or any(x.get("verdict") not in ok for x in per):
        defects.append("cwo_ez_24_pairs.per_pair must give all 18 pairs, each accept|defect")
    suite = d.get("suite_rerun") if isinstance(d.get("suite_rerun"), dict) else {}
    for k in ("hard_status", "web_quotes_flag_count", "ngram7_max_rows_per_gram", "tiling_verses",
              "mark_symmetry_gap_residual", "verdict"):
        if k not in suite:
            defects.append("suite_rerun.%s absent" % k)
    if suite.get("verdict") not in ok:
        defects.append("suite_rerun.verdict must be accept|defect")
    cov = d.get("coverage_rerun") if isinstance(d.get("coverage_rerun"), dict) else {}
    if cov.get("verdict") not in ok or not isinstance(cov.get("per_cwo"), (dict, list)):
        defects.append("coverage_rerun needs per_cwo and an accept|defect verdict")
    tb = d.get("transcript_batch") if isinstance(d.get("transcript_batch"), dict) else {}
    for k in ("toolfix6_diffs", "selftests_rerun", "manifest_vs_index", "census_v2_vs_v1", "pre_primaries_statement",
              "verdict"):
        if k not in tb:
            defects.append("transcript_batch.%s absent" % k)
    if tb.get("verdict") not in ok:
        defects.append("transcript_batch.verdict must be accept|defect")
    rd = d.get("rows_readiness") if isinstance(d.get("rows_readiness"), dict) else {}
    if rd.get("fit") not in (True, False):
        defects.append("rows_readiness.fit must be a boolean")
    sent = str(rd.get("verdict") or "")
    if rd.get("fit") is True and (not accept_re.search(sent) or refuse_re.search(sent)):
        defects.append("rows_readiness.verdict must take the #e8 T6-02 ACCEPT form with no refuse token")
    if rd.get("artifact_sha256") != sha(rows_p):
        defects.append("rows_readiness.artifact_sha256 is not rows_v7_cwo24.jsonl")
    routes = {"author_fixup", "controlling_agent", "orchestrator", "primaries", "final_check"}
    ids = []
    for f in d.get("new_findings") or []:
        ids.append(f.get("id"))
        if not re.fullmatch(r"S5-\d{2}", str(f.get("id") or "")):
            defects.append("finding id %r is not S5-NN" % f.get("id"))
        if f.get("severity") not in ("blocker", "major", "minor", "note"):
            defects.append("finding %s has no allowed severity" % f.get("id"))
        if str(f.get("route", "")).split(":")[0] not in routes:
            defects.append("finding %s has route %r outside the allowed set" % (f.get("id"), f.get("route")))
    if len(set(ids)) != len(ids):
        defects.append("duplicate finding ids")
    to_ca = [f.get("id") for f in d.get("new_findings") or []
             if str(f.get("route", "")).startswith("controlling_agent")]
    return {"verdict": d.get("verdict"),
            "cwo_ez_24_pairs": pairs.get("pairs_checked"),
            "suite": {k: suite.get(k) for k in ("hard_status", "web_quotes_flag_count", "tiling_verses")},
            "coverage": cov.get("verdict"), "transcript_batch": tb.get("verdict"),
            "rows_readiness_fit": rd.get("fit"),
            "new_findings_by_severity": {s: sum(1 for f in d.get("new_findings") or [] if f.get("severity") == s)
                                         for s in sorted({str(f.get("severity")) for f in d.get("new_findings") or []})},
            "findings_routed_to_the_controlling_agent": to_ca,
            "primaries_blocked_by_this_review": bool(to_ca) or rd.get("fit") is not True,
            "artifacts_not_listed": sorted(set(launch) - seen),
            "inputs_read_beyond_the_table": EXTRAS.get("artifacts_reviewed", [])}


def validate_t1(d, launch, defects):
    if d.get("verdict") not in ("fit_to_accept", "fit_with_changes", "not_fit"):
        defects.append("verdict %r not in the allowed set" % d.get("verdict"))
    for e in d.get("artifacts_reviewed", []):
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("artifact_sha256_at_review", ""))):
            defects.append("artifacts_reviewed entry without a sha256: %s" % e.get("path"))
    seen = check_binding(d.get("artifacts_reviewed", []), "path", "artifact_sha256_at_review", launch, defects,
                         "artifacts_reviewed")
    answers = d.get("answers") or {}
    missing_q = ["q%d" % i for i in range(1, 10) if not str(answers.get("q%d" % i, "")).strip()]
    if missing_q:
        defects.append("answers missing: %s" % ", ".join(missing_q))
    sev = {}
    for f in d.get("findings", []):
        sev[str(f.get("severity"))] = sev.get(str(f.get("severity")), 0) + 1
    return {"verdict": d.get("verdict"), "findings_by_severity": sev,
            "hard_gate_weakening_entries": len(d.get("hard_gate_weakening", [])),
            "artifacts_not_reviewed": sorted(set(launch) - seen),
            "artifacts_read_beyond_the_table": EXTRAS.get("artifacts_reviewed", [])}


def validate_t2(d, launch, defects):
    """T2 reviews the REPAIR of T1's findings: the verdict, the digest binding (the distinct_checker side of every cure
    claim needs artifact_sha256_at_review), one cure status per T1 item, and answers q1-q6."""
    if d.get("verdict") not in ("fit_to_accept", "fit_with_changes", "not_fit"):
        defects.append("verdict %r not in the allowed set" % d.get("verdict"))
    for e in d.get("artifacts_reviewed", []):
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("artifact_sha256_at_review", ""))):
            defects.append("artifacts_reviewed entry without a sha256: %s" % e.get("path"))
    seen = check_binding(d.get("artifacts_reviewed", []), "path", "artifact_sha256_at_review", launch, defects,
                         "artifacts_reviewed")
    allowed = {"cured", "not_cured", "partially_cured", "no_change_needed"}
    statuses = {}
    for c in d.get("cure_status", []):
        if c.get("status") not in allowed:
            defects.append("cure_status %r has status %r" % (c.get("t1_item"), c.get("status")))
        statuses[str(c.get("t1_item"))] = c.get("status")
    for item in ("T1-01", "T1-02", "T1-03", "T1-04", "T1-05"):
        if not any(k.startswith(item) for k in statuses):
            defects.append("no cure_status for %s" % item)
    answers = d.get("answers") or {}
    missing_q = ["q%d" % i for i in range(1, 7) if not str(answers.get("q%d" % i, "")).strip()]
    if missing_q:
        defects.append("answers missing: %s" % ", ".join(missing_q))
    sev = {}
    for f in d.get("new_findings", []):
        sev[str(f.get("severity"))] = sev.get(str(f.get("severity")), 0) + 1
    return {"verdict": d.get("verdict"), "cure_status": statuses, "new_findings_by_severity": sev,
            "artifacts_not_reviewed": sorted(set(launch) - seen),
            "artifacts_read_beyond_the_table": EXTRAS.get("artifacts_reviewed", [])}


def validate_t3(d, launch, defects):
    """T3 is the supplementary review ruling T1 ordered. Form only: the verdict; the digest binding; the TOOLKIT.md verdict
    with its sibling sweep (R6: a .md cure claim needs key_phrases and an integer statements_reviewed); a verdict for each
    of items 2-6; one R4 verdict each for (i)-(iii); a cure status for T2-01..T2-05 and D3; the cure-gate verdict."""
    verdicts = ("fit_to_accept", "fit_with_changes", "not_fit")
    if d.get("verdict") not in verdicts:
        defects.append("verdict %r not in the allowed set" % d.get("verdict"))
    for e in d.get("artifacts_reviewed", []):
        if not re.fullmatch(r"[0-9a-f]{64}", str(e.get("artifact_sha256_at_review", ""))):
            defects.append("artifacts_reviewed entry without a sha256: %s" % e.get("path"))
    seen = check_binding(d.get("artifacts_reviewed", []), "path", "artifact_sha256_at_review", launch, defects,
                         "artifacts_reviewed")
    tk = d.get("toolkit_md") or {}
    if tk.get("verdict") not in verdicts:
        defects.append("toolkit_md.verdict %r not in the allowed set" % tk.get("verdict"))
    sw = tk.get("sibling_sweep") or {}
    if not (isinstance(sw.get("key_phrases"), list) and sw["key_phrases"] and isinstance(sw.get("statements_reviewed"), int)):
        defects.append("toolkit_md.sibling_sweep lacks non-empty key_phrases or an integer statements_reviewed (R6)")
    items = d.get("items") or {}
    for k in ("item2_calendar_arm", "item3_families", "item4_kq_split", "item5_u05c4", "item6_suite_direct"):
        if not str((items.get(k) or {}).get("verdict", "")).strip():
            defects.append("items.%s has no verdict" % k)
    r4 = d.get("r4") or {}
    for k in ("i_qere_tier", "ii_puncta_arms", "iii_editorial_note_tier"):
        if (r4.get(k) or {}).get("verdict") not in ("ratify", "ratify_with_changes", "reverse"):
            defects.append("r4.%s verdict %r not in ratify|ratify_with_changes|reverse" % (k, (r4.get(k) or {}).get("verdict")))
    allowed = {"cured", "not_cured", "partially_cured", "no_change_needed"}
    statuses = {}
    for c in d.get("t2_cure_status", []):
        if c.get("status") not in allowed:
            defects.append("t2_cure_status %r has status %r" % (c.get("item"), c.get("status")))
        statuses[str(c.get("item"))] = c.get("status")
    for item in ("T2-01", "T2-02", "T2-03", "T2-04", "T2-05", "D3"):
        if not any(k.startswith(item) for k in statuses):
            defects.append("no t2_cure_status for %s" % item)
    if not str((d.get("cure_gate") or {}).get("verdict", "")).strip():
        defects.append("cure_gate has no verdict")
    sev = {}
    for f in d.get("new_findings", []):
        sev[str(f.get("severity"))] = sev.get(str(f.get("severity")), 0) + 1
    return {"verdict": d.get("verdict"), "toolkit_md_verdict": tk.get("verdict"),
            "sibling_sweep": {"key_phrases": len(sw.get("key_phrases") or []), "statements_reviewed": sw.get("statements_reviewed")},
            "items": {k: (items.get(k) or {}).get("verdict") for k in items},
            "r4": {k: (r4.get(k) or {}).get("verdict") for k in r4}, "t2_cure_status": statuses,
            "cure_gate": (d.get("cure_gate") or {}).get("verdict"), "new_findings_by_severity": sev,
            "artifacts_not_reviewed": sorted(set(launch) - seen),
            "artifacts_read_beyond_the_table": EXTRAS.get("artifacts_reviewed", [])}


def resolve_ordinal(aid, record_xid, arg_ordinal):
    """(ordinal, None) or (None, reason). OW-11-k (2026-09-11): a defaulted --ordinal once landed #e4's deliverable under #e1.
    The ordinal now comes from the agent record's execution_id when --ordinal is omitted, and any disagreement, foreign
    attempt, malformed id, or absence of both sources is refused before anything is landed."""
    m = re.fullmatch(r"(.+)#e(\d+)", str(record_xid)) if record_xid else None
    if record_xid and (not m or m.group(1) != aid):
        return None, "the agent record names execution %r, which is not an execution of %s" % (record_xid, aid)
    rec_ord = int(m.group(2)) if m else None
    if arg_ordinal is None and rec_ord is None:
        return None, "no --ordinal given and the agent record names no execution_id; an explicit ordinal is required"
    if arg_ordinal is not None and rec_ord is not None and arg_ordinal != rec_ord:
        return None, "--ordinal %d disagrees with the agent record's execution %s; nothing landed" % (arg_ordinal, record_xid)
    return (arg_ordinal if arg_ordinal is not None else rec_ord), None


def selftest():
    aid = "ezek_controlling_rulings_a1"
    vectors = [
        ("the ordinal is derived from the record when --ordinal is omitted", (aid, aid + "#e4", None), 4),
        ("an explicit ordinal agreeing with the record", (aid, aid + "#e4", 4), 4),
        ("REGRESSION OW-11-k: ordinal 1 against a #e4 record is refused", (aid, aid + "#e4", 1), None),
        ("no ordinal and no execution id in the record is refused", (aid, None, None), None),
        ("an explicit ordinal with a record that names no execution id", (aid, None, 2), 2),
        ("a record naming another attempt's execution is refused", (aid, "ezek_toolkit_review_t1_a1#e2", None), None),
        ("a malformed execution id is refused", (aid, aid + "-e4", None), None),
    ]
    results = []
    for name, args, want in vectors:
        got, _why = resolve_ordinal(*args)
        results.append({"vector": name, "want": want, "got": got, "ok": got == want})
    failed = [r for r in results if not r["ok"]]
    print(json.dumps({"selftest": "_land_rulings_and_t1.resolve_ordinal", "vectors": len(results), "failed": failed,
                      "verdict": "GREEN" if not failed else "RED"}, indent=1))
    return 1 if failed else 0


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True, choices=sorted(JOBS))
    ap.add_argument("--record", required=True)
    ap.add_argument("--tokens", type=int, required=True)
    ap.add_argument("--tool-uses", type=int, required=True)
    ap.add_argument("--ordinal", type=int, default=None,
                    help="derived from the agent record's execution_id when omitted; refused when it disagrees (OW-11-k)")
    ap.add_argument("--src", help="deliverable written OUTSIDE the worktree (OW-11); landed here with parity")
    a = ap.parse_args()
    job = JOBS[a.job]
    aid = job["attempt"]
    rec = json.loads(Path(a.record).read_text(encoding="utf-8"))
    ordinal, why = resolve_ordinal(aid, rec.get("execution_id"), a.ordinal)
    if ordinal is None:
        print(json.dumps({"job": a.job, "verdict": "REFUSED", "why": why, "actions": []}, ensure_ascii=False, indent=1))
        return 1
    xid = "%s#e%d" % (aid, ordinal)
    brief_name = job["brief"] if ordinal == 1 else job["brief_v2"]
    out = {"job": a.job, "execution_id": xid, "brief": brief_name, "actions": [], "form_defects": []}

    deliverable = EZ / job["deliverable"]
    if a.src:
        # OW-11: the agent wrote OUTSIDE the worktree; the authorized orchestrator lands it here, byte for byte
        src = Path(a.src)
        if not src.is_file():
            out["verdict"] = "NOT_LANDED"
            out["form_defects"].append("source deliverable absent: %s" % src)
            print(json.dumps(out, ensure_ascii=False, indent=1))
            return 1
        if deliverable.is_file():
            if sha(deliverable) == sha(src):
                out["actions"].append("already landed with identical bytes - no-op")
            else:
                out["verdict"] = "REFUSED"
                out["form_defects"].append("SP/Ezek/%s already exists with DIFFERENT bytes; a landed deliverable is "
                                           "never replaced" % job["deliverable"])
                print(json.dumps(out, ensure_ascii=False, indent=1))
                return 1
        else:
            shutil.copyfile(src, deliverable)
            assert sha(deliverable) == sha(src), "persist parity failure"
            out["actions"].append("landed from outside the worktree, parity verified")
    if not deliverable.is_file():
        out["verdict"] = "NOT_LANDED"
        out["form_defects"].append("deliverable absent at its exact path: SP/Ezek/%s" % job["deliverable"])
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 1
    # the agent record was read, and its execution id resolved against the landing, before anything landed (OW-11-k)
    launch = brief_digests(EZ / brief_name)
    try:
        d = json.loads(deliverable.read_text(encoding="utf-8"))
        summary = {"rulings": validate_rulings, "rulings_e3": validate_rulings_e3, "rulings_e4": validate_rulings_e4, "rulings_e5": validate_rulings_e5, "rulings_e6": validate_rulings_e6, "rulings_e7": validate_rulings_e7, "rulings_e8": validate_rulings_e8, "rulings_e9": validate_rulings_e9, "rulings_e10": validate_rulings_e10, "rulings_e11": validate_rulings_e11, "s5": validate_s5, "s3": validate_s3, "s4": validate_s4,
                   "t1": validate_t1, "t2": validate_t2,
                   "t3": validate_t3, "t4": validate_t4, "t5": validate_t5, "t6": validate_t6, "s1": validate_s1, "s2": validate_s2}[a.job](d, launch, out["form_defects"])
    except json.JSONDecodeError as exc:
        d, summary = None, {}
        out["form_defects"].append("deliverable is not valid JSON: %s" % exc)
    status = "LANDED" if not out["form_defects"] else "LANDED_WITH_FORM_DEFECTS"
    out["summary"] = summary

    existing = set()
    if RECEIPTS.is_file():
        existing = {json.loads(l).get("execution_id") for l in RECEIPTS.read_text(encoding="utf-8").splitlines() if l.strip()}
    if xid in existing:
        out["actions"].append("receipt for %s already present - not appended twice" % xid)
    else:
        e19 = rec.get("e19_selfreport") or rec.get("e19_selfreported") or "NOT REPORTED by the agent"
        receipt = {
            "schema": "m8_attempt_receipt.v1", "lane": job["lane"], "book": "Ezek",
            "attempt_id": aid, "execution_id": xid, "execution_of": aid, "execution_ordinal": ordinal,
            "previous_execution_id": ("%s#e%d" % (aid, ordinal - 1)) if ordinal > 1 else None, "retry_of": None,
            "agent": job["agent"], "parent_agent_id": "orchestrator", "model": job["model"],
            "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
            "effort": job["effort"], "producer": job["producer"], "catcher": job["catcher"],
            "role_separation": "the landing tool proves form only; it does not review or re-rule content",
            "outcome": status, "recorded_at": datetime.now(timezone.utc).isoformat(),
            "brief": {"path": "Ezek/" + brief_name, "sha256": sha(EZ / brief_name)},
            "deliverable_source": a.src,
            "output_file": "Ezek/" + job["deliverable"], "output_sha256": sha(deliverable),
            "form_defects": out["form_defects"], "landing_summary": summary,
            "tokens_reported": a.tokens, "tool_uses": a.tool_uses,
            "token_note": "runtime-reported subagent tokens for this execution",
            "unresolved_uncertainty": rec.get("unresolved_uncertainty", []),
            "e19_selfreported": e19,
        }
        with RECEIPTS.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(receipt, ensure_ascii=False) + "\n")
        out["actions"].append("receipt appended for %s" % xid)

    NOTES.mkdir(exist_ok=True)
    note_p = NOTES / (xid.replace("#", "%23") + ".json")
    if note_p.is_file():
        out["actions"].append("evidence note for %s already present - kept, never overwritten" % xid)
    else:
        note = {"attempt_id": aid, "execution_id": xid, "sources": rec.get("sources", []),
                "outcome": rec.get("outcome", {}), "verification": rec.get("verification", []),
                "unresolved_uncertainty": rec.get("unresolved_uncertainty", []), "self_authored": True,
                "limit": "accountable work summary; not chain of thought and not independent proof. Built verbatim "
                         "from the agent's own OW-8 final message."}
        note_p.write_text(json.dumps(note, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        out["actions"].append("evidence note written")

    subprocess.run([sys.executable, str(CAMPAIGN / "_capture_index.py"), "--book", "Ezek", "--write"],
                   capture_output=True, text=True, encoding="utf-8")
    chk = subprocess.run([sys.executable, str(CAMPAIGN / "_capture_index.py"), "--check"],
                         capture_output=True, text=True, encoding="utf-8")
    out["capture_index"] = json.loads(chk.stdout)["verdict"]
    out["verdict"] = status
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if status == "LANDED" else 2


if __name__ == "__main__":
    sys.exit(main())
