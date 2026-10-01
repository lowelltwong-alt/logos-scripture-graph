#!/usr/bin/env python3
r"""OW-2-CARRY-IDEMPOTENCY mechanical pre-print verifier — v3 (OWNER_REPAIR_ADVANCE_2026-09-06
item 4, 2026-09-06: ruling + current-state-index pointers with hashes; stale owner-triage
waits rejected; the ruling's binding clauses canonical; STATE-BINDING carries ruling= and
index= hashes; index phase must equal the immutable log's latest cursor; every v2 arm kept —
v2 preserved byte-identical as _safe_to_clear_check.v2_2026-09-04.py). v2 (OW-3 hardening,
2026-09-04). v1 (2026-08-31; path-arms hardened per OW-2D) tested keywords; the
owner's 2026-09-04 review (OW-3 item 1) showed it passed a bogus cursor, a
reversed M7 prohibition, a reversed tier-4 prohibition, and the removal of the
Isaiah remediation-docket pointer (a checker weakness — the saved prompt itself
carried the correct rules). v2 verifies, for the prompt it is given:

  1. CANONICAL PROHIBITIONS — every permanent safeguard must appear as its
     canonical clause (exact substring, whitespace-normalized), not a keyword;
     the OW-3 safeguards are part of that canonical set.
  2. CONTRADICTION REJECTION — any clause reversing a prohibition fails:
     read/inspect/consult/imitate/use M7 or another model lane, comparison
     data allowed, tier-4 / punctuation / headings / metadata may drive or
     warrant a boundary, repairs applied/complete/done or rows repaired
     without a negation, an audit-DONE receipt paired with repairs-complete
     language.
  3. STATE BINDING — the prompt must carry ONE `STATE-BINDING:` line whose
     fields EQUAL the durable evidence recomputed here: the LATEST `CURSOR:
     phase = ...` in freeze/CYCLE_STATE.md, the attempt counts in every OW-2
     receipts carrier under ../OW2_audit, the shipped Isaiah corpus sha256
     prefix, and repairs_applied=none (true ONLY while the shipped corpora
     still equal the receipts'/frames' pinned hashes).
  4. AUDIT != REPAIR — the canonical distinction clause is required.
  5. DONE-RECEIPT + DOCKET POINTERS WITH HASHES — every DONE receipt path and
     the Isaiah remediation docket path must be present, each followed (within
     240 chars) by the first 8 hex of that file's CURRENT on-disk sha256.
  6. EXACT-PATH ARMS (v1, preserved) — the two required path strings intact;
     the known backslash-dropped variants rejected.
  7. Marker, cursor line, and the generate-next-prompt instruction (v1).

A prompt that fails is NOT printed — regenerate from actual state. The
generator obtains the STATE-BINDING line from `--binding` so prompt and checker
can never drift. Negative fixtures cover every OW-3 case plus the v1 cases.

Usage: _safe_to_clear_check.py PROMPT_FILE
       _safe_to_clear_check.py --binding      (print the current STATE-BINDING line)
       _safe_to_clear_check.py --selftest     (negative-fixture proof run)
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent            # SP/Jer
SP = HERE.parent
OW2 = SP / "OW2_audit"
CYCLE_STATE = HERE / "freeze" / "CYCLE_STATE.md"          # the Jeremiah log (closed history from 2026-09-07)
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")


def live_cycle_state() -> Path:
    """The immutable log of the LIVE book, resolved from marathon_progress.yaml current_book.

    A closed book's log never moves again, so the cursor that governs must come from the book the
    campaign is actually on. Falls back to the Jeremiah log when the live book has no log on disk."""
    prog = M8 / "marathon_progress.yaml"
    if prog.is_file():
        m = re.search(r"^current_book:\s*(\S+)\s*$", prog.read_text(encoding="utf-8"), re.M)
        if m:
            p = SP / m.group(1) / "freeze" / "CYCLE_STATE.md"
            if p.is_file():
                return p
    return CYCLE_STATE

DONE_RECEIPTS = [
    "receipts/OW2_review_status_resolution.json",
    "receipts/OW2_audit_budget_checkpoint.json",
    "receipts/OW2_isa_lf_audit.json",                 # item 1 DONE 2026-09-03
    "receipts/OW2_five_book_semantic_audit.json",        # item 2 DONE 2026-09-05
    "receipts/OW2_prov38_opus_review.json",              # item 3 DONE 2026-09-05
]
DOCKET_POINTERS = [
    "receipts/OW2_isa_lf_remediation_docket.v1.json",  # OW-3 item 1: pointer + hash REQUIRED
    "receipts/OW2_five_book_remediation_docket.v1.json",  # item 2 DONE: pointer + hash REQUIRED
    "receipts/OW2_prov38_remediation_docket.v1.json",  # item 3 DONE: pointer + hash REQUIRED
]
RECEIPT_CARRIERS = ["ow2lf", "ow2adj", "ow2i2", "ow2i2adj", "ow2p38", "ow2adj_re"]
# v3 (2026-09-06, OWNER_REPAIR_ADVANCE_2026-09-06 item 4): the standing ruling and the verified
# current-state index must be POINTED AT with their current on-disk sha256 prefixes.
RULING_POINTERS = [
    "OWNER_REPAIR_ADVANCE_2026-09-06.md",   # canonical verbatim standing ruling
    "CURRENT_STATE.v1.json",               # compact verified current-state index (generated from disk)
]

EXACT_PATHS_REQUIRED = [
    r"C:\Users\lowel\.agent-governance\validate_workspace_policy.ps1",
    r"SP\Jer\_safe_to_clear_check.py",
]
CORRUPTED_VARIANTS_REJECTED = [
    r"C:\Users\lowel.agent-governance\validate_workspace_policy.ps1",
    r"SP\Jer_safe_to_clear_check.py",
]

# canonical clauses (whitespace-normalized exact substrings; case-insensitive)
CANONICAL = {
    "no_m7_or_comparison_reads": "no M7 or comparison-data reads ever",
    "tier4_never_drives": "translation punctuation, editorial headings, and other tier-4 metadata never drive a boundary",
    "cwo_execution_parity": "corpus-wide-order execution parity",
    "hard_book_close_gates": "the hard book-close gates of CAMPAIGN_CLOSE_GATE.v1.md bind every book close",
    "second_gen_sweep_role_separation": "a fresh full second-generation sweep runs after each repair wave with a checker distinct from the repair author",
    "attempt_receipt_recording": "attempt receipts record actual model/effort, exact denominators, producer/catcher roles, evidence paths, findings, and hashes",
    "one_correlated_voice": "Anthropic-family agreement is one correlated M8 voice, never independent confirmation",
    "revelation_requirements": "Revelation requires Opus 5 high review plus Fable 5 high adversarial adjudication",
    # OW-3 (2026-09-04) permanent safeguards
    "ow3_audit_ne_repair": "audit completion is distinct from repair completion",
    "ow3_docket_dispositions": "remediation docket's open/resolved dispositions and independent post-repair evidence are tracked",
    "ow3_low_findings": "low findings are retained with explicit handling",
    "ow3_repair_proposals_adversarial": "every repair proposal is validated as adversarially as the row it repairs",
    "ow3_placeholders_rejected": "unexpanded placeholders are rejected by every lane verifier",
    "ow3_both_sides": "seams are assessed from both sides under the book's governing rules",
    "ow3_refrains_close": "refrains close units",
    "ow3_dependency_record": "a dependency-applicability record preserves the old evidence, records old/new hashes and the scope of change",
    "ow3_history_never_rewritten": "history is never silently rewritten",
    "ow3_honest_effort": "high ordered is not high verified",
    "ow3_baseline_preserved": "the pre-feedback baseline is preserved and every subsequent repair or re-adjudication is labeled",
    "ow3_checker_binding": "binds the prompt to the latest durable cursor, attempt dispositions and audit-versus-repair state",
    "ow3_no_rerun_after_clear": "completed one-time checks stay completed",
    # OWNER_REPAIR_ADVANCE_2026-09-06 binding clauses (v3)
    "ora_delegated_repair": "repairs proceed under OWNER_REPAIR_ADVANCE_2026-09-06 with delegated judgment",
    "ora_rejection_resolved": "an evidence-backed rejection is resolved-no-change, not an applied repair",
    "ora_prelam_lift": "the pre-Lamentations pause lifts when Jeremiah passes its hard close gates",
    "ora_prov38_denominator": "38 stays the historical denominator of the completed Prov-38 review",
    # OW-6 / OW-6b / OW-6c (owner directives, 2026-09-07) - persistent by owner requirement
    "ow6_final_checker": "no book closes without a claude-fable-5-1 final checker verdict of fit_to_close over the whole book, its audit logs and every subagent artifact including captured reasoning transcripts",
    "ow6_fable_boss_escalation": "claude-fable-5-1 is the boss; every escalation routes to it and it decides when risk, dependencies and blast radius require a human",
    "ow6_escalation_packet": "an escalation to the human presents the choices: the recommendation with its reason and every other choice with pros and cons",
    "ow6_continue_next_book": "OW-6 continuation clause SUPERSEDED by OW-9: a book close is a HARD STOP - the orchestrator does not open the next book",
    "ow6b_hard_track": "books classified HARD run with claude-fable-5-1 as the controlling agent and the extra-scrutiny arms; Revelation and Daniel are owner-named HARD",
    "ow6c_end_of_campaign_recheck": "when the last book closes the controlling agent presents the owner a decision packet on re-checking all work and all captured reasoning, weighted to the early books",
    # 2026-09-07 evidence-integrity controls (Lam). Each must survive a clear or the control is lost with it.
    "ev_transcript_decay": "the runtime deletes written transcripts mid-session",
    "ev_content_not_directory": "kind is decided by its content, never by its directory or extension",
    "ev_coverage_reconciled": "a coverage statement is not coverage",
    # OW-7 (owner directive, 2026-09-07). Each must survive a clear or the control is lost with it.
    "ow7_three_layers": "three layers never merged",
    "ow7_lineage": "a nested subagent's records belong to the child",
    "ow7_blindness": "collecting records does not authorize sharing them",
    # OW-8 (owner directive, 2026-09-07)
    "ow8_accountable_summary": "not chain of thought and not independent proof",
    "ow8_scope_what_exists": "do not fabricate missing historical records",
    "ow8_not_a_stop_condition": "missing logs are not a stop condition",
    # OW-9 (owner directive, 2026-09-07) - reverses the continuation half of OW-6
    "ow9_stop_at_book_boundary": "a book close is a hard stop",
    "ow9_prompt_printed_in_chat": "printed in full in the chat for copy-paste",
    # OW-10 (owner directive, 2026-09-08) - execution identity, cure binding, census coverage, prompt duties
    "ow10_execution_identity": "attempt_id is the STABLE LOGICAL JOB and is never renamed; execution_id identifies ONE PHYSICAL RUN",
    "ow10_retry_vs_rerun": "re-running the same job is previous_execution_id; correcting a different job is retry_of",
    "ow10_cure_binding": "verification results bound to the exact resulting artifact plus the distinct-checker review",
    "ow10_self_report_insufficient": "a self-reported passed is not sufficient",
    "ow10_census_coverage": "transcript coverage is reported from an explicit per-book census",
    "ow10_prompt_duties": "generated from current durable state, checked for stale instructions and retry-identity confusion, saved, read back, verified, printed in full, and carried to its successor",
    # OW-11 (owner directive, 2026-09-10) - registry exception for Ezekiel and Daniel, one-boundary continuation, ceiling
    "ow11_write_authority": "the owner explicitly authorized this Opus 5 orchestration, and the Fable, Sonnet and Opus agents it launches, to write M8_fable work for Ezekiel and then Daniel despite the registry's Fable-5-only rule",
    "ow11_scope": "the exception covers Ezekiel and Daniel only and expires at Daniel's close",
    "ow11_one_boundary": "at Ezekiel's close the run continues into Daniel; at Daniel's close the OW-9 hard stop applies",
    "ow11_budget": "one combined 15M subagent-token ceiling for Ezekiel plus Daniel, with an owner check-in before crossing it",
    "ow11_registry_read": "before the first M8 write, read the active-worktree registry's owner and identity rule for the lane",
    "ow11_deliverables_outside_worktree": "subagents write deliverables outside the worktree and the authorized orchestrator lands them",
    "ow11_authority_in_every_launch": "the OW-11 authority paragraph goes in every launch message, not only in the brief",
}

# OW-10: clauses that may not appear ALONE. A prompt that restates E-14's re-launch ladder without the execution-id
# amendment reintroduces exactly the contradiction OW-10 resolved, and it does so in language that reads correct.
PAIRED_CLAUSES = [
    ("retry_identity_confusion",
     re.compile(r"\b(same|identical)\s+attempt[ _-]?id\b", re.I),
     re.compile(r"\bexecution[ _-]?id\b", re.I),
     "a re-launch under the SAME attempt id must be stated together with execution_id; without it the prompt "
     "revives the OW-7/E-14 contradiction"),
    ("cure_without_binding",
     re.compile(r"\bcure[ds]?\b|\brepair (?:is|was) (?:accepted|cured)\b", re.I),
     re.compile(r"\bbound to the exact resulting artifact\b", re.I),
     "a prompt that speaks of cures must carry the artifact-binding rule, or a self-reported cure passes again"),
    # OW-11: the one-boundary exception and the registry exception may never appear without their limits
    ("continuation_without_daniel_stop",
     re.compile(r"\bcontinue[sd]?\s+(?:straight\s+)?into\s+Daniel\b", re.I),
     re.compile(r"at Daniel's close the OW-9 hard stop applies", re.I),
     "a prompt that continues into Daniel must carry OW-11's stop at Daniel's close, or a one-boundary exception "
     "becomes the permanent continuation OW-9 superseded"),
    ("registry_exception_without_expiry",
     re.compile(r"\bFable-5-only rule\b", re.I),
     re.compile(r"expires at Daniel's close", re.I),
     "a prompt that cites the registry exception must carry its expiry, or a later book inherits an authority the "
     "owner scoped to two books"),
]

ABSOLUTE_CONTRADICTIONS = {"stop_reissue_decision", "owner_decision_pending"}
NEG = re.compile(r"\b(never|no|not|nothing|none|forbidden|banned|without|do not|don't|cannot|can't)\b", re.I)


def _negated(text: str, start: int, end: int | None = None, span: int = 40, after: int = 28) -> bool:
    """A match is not a contradiction when a negation token stands within `span`
    chars before it OR within `after` chars after it inside the same clause
    (e.g. 'a DONE audit receipt never implies repairs' is the prohibition itself,
    while 'audit DONE - repairs applied to the rows' has no negation either side)."""
    before = text[max(0, start - span):start]
    tail = text[end:end + after] if end is not None else ""
    tail = re.split(r"[.;\n]", tail)[0]
    return bool(NEG.search(before)) or bool(NEG.search(tail))


CONTRADICTIONS = [
    ("m7_read_verb", re.compile(r"\b(read|reads|reading|inspect|inspects|inspecting|consult|consults|imitate|imitates|use|uses|open|opens|compare against|copy from)\s+(the\s+)?(M7|M[1-6]|other model lanes?|comparison (data|outputs?))\b", re.I)),
    ("m7_allowed", re.compile(r"\b(M7|M[1-6]|comparison[- ]data|comparison outputs?|other model lanes?)\b[^.\n]{0,60}\b(allowed|permitted|permissible|may be read|can be read|may now be read|is fine|are fine|okay|ok to read)\b", re.I)),
    ("tier4_may_drive", re.compile(r"\b(tier-4|tier 4|translation punctuation|editorial headings?|punctuation|headings?|paragraphing|metadata)\b[^.\n]{0,80}\b(may|can|could|should|shall|will|does|do|now)\s+(drive|decide|warrant|cut|set|carry)\b", re.I)),
    ("repairs_done", re.compile(r"\b(repairs?|remediation|fixes|respans?)\b[^.\n]{0,50}\b(applied|complete|completed|done|finished|landed|adopted)\b", re.I)),
    ("rows_repaired", re.compile(r"\b(rows?|corpus|corpora|seams?)\b[^.\n]{0,30}\b(repaired|remediated|respanned)\b", re.I)),
    # v3: stale owner-triage waits (superseded by OWNER_REPAIR_ADVANCE_2026-09-06) are rejected
    ("stale_owner_triage_wait", re.compile(r"\b(await|awaits|awaiting|wait for|waits for|waiting for|pending)\s+(the\s+)?owner(['\u2019]s)?\s+(triage|ruling|decision|sequencing)\b", re.I)),
    ("owner_decision_pending", re.compile(r"\bowner decision pending\b", re.I)),
    ("stop_reissue_decision", re.compile(r"\bre-issue the decision request\b", re.I)),
    ("do_not_resume_jeremiah", re.compile(r"\b(do not|don['\u2019]t|never) resume jeremiah\b", re.I)),
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def latest_cursor_phase() -> str:
    txt = live_cycle_state().read_text(encoding="utf-8", errors="replace")
    m = list(re.finditer(r"CURSOR: phase = ([A-Za-z0-9_]+)", txt))
    return m[-1].group(1) if m else "UNKNOWN"


def carrier_counts() -> dict:
    out = {}
    for c in RECEIPT_CARRIERS:
        p = OW2 / f"{c}_attempt_receipts.jsonl"
        n = 0
        if p.is_file():
            n = sum(1 for l in p.read_text(encoding="utf-8").splitlines() if l.strip())
        out[c] = n
    return out


def repairs_applied_state() -> tuple[str, dict]:
    """'none' only while every shipped corpus that a receipt/frame pins still hashes to its pin."""
    checks = {}
    isa = M8 / "book_chunks" / "Isa" / "chunks.jsonl"
    isa_now = sha(isa)[:8] if isa.is_file() else "ABSENT"
    r1 = M8 / "receipts" / "OW2_isa_lf_audit.json"
    if r1.is_file():
        pin = json.load(open(r1, encoding="utf-8"))["shipped_corpus_preserved"]["book_chunks/Isa/chunks.jsonl"]
        checks["Isa"] = (isa_now == pin[:8])
    f2 = OW2 / "frame_item2.v1.json"
    if f2.is_file():
        for k, v in json.load(open(f2, encoding="utf-8"))["pinned"].items():
            if k.startswith("book_chunks/") and (M8 / k).is_file():
                checks[k.split("/")[1]] = (sha(M8 / k) == v)
    return ("none" if all(checks.values()) else "SOME"), {"isa_corpus": isa_now, "checks": checks}


def state_binding() -> str:
    cc = carrier_counts()
    rep, info = repairs_applied_state()
    fields = [f"phase={latest_cursor_phase()}"] + [f"{c}={cc[c]}" for c in RECEIPT_CARRIERS] + \
             [f"isa_corpus={info['isa_corpus']}", f"repairs_applied={rep}"] + \
             [f"ruling={sha(M8 / RULING_POINTERS[0])[:8] if (M8 / RULING_POINTERS[0]).is_file() else 'ABSENT'}",
              f"index={sha(M8 / RULING_POINTERS[1])[:8] if (M8 / RULING_POINTERS[1]).is_file() else 'ABSENT'}"]
    return "STATE-BINDING: " + "; ".join(fields)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def check_text(text: str, binding: str | None = None):
    missing = []
    t = norm(text)
    if "OW-2-CARRY-IDEMPOTENCY" not in t:
        missing.append("required:marker")
    if not re.search(r"phase\s*=", t):
        missing.append("required:cursor")
    if not re.search(r"(print|generate)[^.]{0,200}(resume prompt|SAFE-TO-CLEAR|next session)", t, re.I):
        missing.append("required:generate_next_prompt")
    # 1. canonical clauses
    tl = t.lower()
    for name, clause in CANONICAL.items():
        if norm(clause).lower() not in tl:
            missing.append(f"canonical_missing:{name}")
    # 2. contradictions (negation-guarded)
    for name, pat in CONTRADICTIONS:
        for m in pat.finditer(t):
            # v3: the stale-wait arms are ABSOLUTE - a nearby "no"/"not" (e.g. "if NO ruling
            # exists, STOP and re-issue the decision request") never excuses them
            # v3.1: a genuine post-feedback repair statement is NOT the audit-implies-repair
            # contradiction: it must be labeled post-feedback or point at its OW2_repairs_ receipt
            # within 160 chars after the match (the label the ruling requires)
            if name in ("repairs_done", "rows_repaired") and re.search(r"post-feedback|OW2_repairs_", t[m.end():m.end() + 160], re.I):
                continue
            if name in ABSOLUTE_CONTRADICTIONS or not _negated(t, m.start(), m.end()):
                missing.append(f"contradiction:{name}:'{m.group(0)[:60]}'")
                break
    # 2b. OW-10 paired clauses: a trigger that appears without its required partner
    for name, trigger, partner, why in PAIRED_CLAUSES:
        if trigger.search(t) and not partner.search(t):
            missing.append(f"unpaired:{name}: {why}")
    # 3. state binding
    want = binding or state_binding()
    got = re.search(r"STATE-BINDING: [^\n]+", text)
    if not got:
        missing.append("state_binding:line_missing")
    elif norm(got.group(0)).strip() != norm(want).strip():
        missing.append(f"state_binding:mismatch got '{norm(got.group(0)).strip()[:120]}' want '{want[:120]}'")
    # 5. receipt + docket + ruling/index pointers with current hashes
    for p in DONE_RECEIPTS + DOCKET_POINTERS + RULING_POINTERS:
        if p not in t:
            missing.append(f"pointer_missing:{p}")
            continue
        fp = M8 / p
        if not fp.is_file():
            missing.append(f"pointer_file_absent_on_disk:{p}")
            continue
        h8 = sha(fp)[:8]
        window = t[t.index(p): t.index(p) + len(p) + 240]
        if h8 not in window:
            missing.append(f"pointer_hash_missing_or_stale:{p} (current {h8})")
    # 5b. v3: the current-state index must agree with the immutable log's latest cursor
    idx = M8 / RULING_POINTERS[1]
    if idx.is_file():
        try:
            ip = json.load(open(idx, encoding="utf-8")).get("phase")
            if ip != latest_cursor_phase():
                missing.append(f"index_phase_mismatch: index {ip} vs cursor {latest_cursor_phase()}")
        except Exception as e:
            missing.append(f"index_unreadable:{e!r}")
    # 6. exact-path arms
    for p in EXACT_PATHS_REQUIRED:
        if p not in text:
            missing.append(f"exact_path_missing:{p}")
    for v in CORRUPTED_VARIANTS_REJECTED:
        if v in text:
            missing.append(f"corrupted_variant_present:{v}")
    return missing


def good_fixture() -> str:
    b = state_binding()
    canon = ". ".join(CANONICAL.values())
    # exercise the FULL OW-3 safeguard sentences the generator embeds (not only the
    # short canonical cores) so a contradiction arm can never misfire on the
    # prohibition text itself without the selftest noticing
    full = HERE.parent.parent / "_ow3_safeguards.json"
    if full.is_file():
        canon += ". " + "; ".join(json.load(open(full, encoding="utf-8")))
    hashes = {p: sha(M8 / p)[:8] for p in DONE_RECEIPTS + DOCKET_POINTERS + RULING_POINTERS if (M8 / p).is_file()}
    ptrs = "; ".join(f"{p} (sha256 {h}…)" for p, h in hashes.items())
    return (f"OW-2-CARRY-IDEMPOTENCY. cursor: phase = {latest_cursor_phase()}. {b}\n"
            f"DONE receipts: {ptrs}. NOTHING has been applied to the shipped Isaiah corpus. "
            f"PERMANENT SAFEGUARDS: {canon}. "
            r"Run C:\Users\lowel\.agent-governance\validate_workspace_policy.ps1 first, and verify mechanically with "
            r"SP\Jer\_safe_to_clear_check.py before printing. "
            "At close, generate the next session's resume prompt and print it.")


def selftest() -> int:
    good = good_fixture()
    docket = DOCKET_POINTERS[0]
    dh = sha(M8 / docket)[:8]
    fixtures = [
        ("good_prompt_passes", good, True),
        ("bogus_cursor_fails", good.replace(f"phase={latest_cursor_phase()}", "phase=ow2_bogus_phase")
                                   .replace(f"phase = {latest_cursor_phase()}", "phase = ow2_bogus_phase"), False),
        ("reversed_m7_prohibition_fails", good + " Read M7 before auditing the next book.", False),
        ("m7_allowed_fails", good + " Comparison data may be read for context.", False),
        ("reversed_tier4_prohibition_fails", good + " Tier-4 metadata may drive a boundary where the Hebrew is silent.", False),
        ("docket_pointer_removed_fails", good.replace(docket, "receipts/OW2_isa_lf_docket.json"), False),
        ("docket_hash_wrong_fails", good.replace(dh, ("0" if dh[0] != "0" else "1") + dh[1:]), False),
        ("audit_done_implies_repairs_done_fails", good + " Item 1 audit DONE - repairs applied to the Isaiah rows.", False),
        ("rows_repaired_fails", good + " The Isaiah rows repaired under the docket are final.", False),
        ("canonical_clause_missing_fails", good.replace("refrains close units", "refrains may close units"), False),
        ("state_binding_line_missing_fails", re.sub(r"STATE-BINDING: [^\n]+", "", good), False),
        ("dropped_backslash_governance_path_fails",
         good.replace(r"C:\Users\lowel\.agent-governance\validate_workspace_policy.ps1",
                      r"C:\Users\lowel.agent-governance\validate_workspace_policy.ps1"), False),
        ("dropped_backslash_checker_path_fails",
         good.replace(r"SP\Jer\_safe_to_clear_check.py", r"SP\Jer_safe_to_clear_check.py"), False),
        ("missing_marker_fails", good.replace("OW-2-CARRY-IDEMPOTENCY", "OW-2-CARRY"), False),
        ("missing_receipt_pointer_fails", good.replace("receipts/OW2_audit_budget_checkpoint.json", "receipts/OW2_audit_budget.json"), False),
        ("negated_prohibition_still_passes", good + " Never read M7; comparison data is not allowed; no repairs applied.", True),
        # v3 fixtures (OWNER_REPAIR_ADVANCE_2026-09-06 item 4)
        ("stale_owner_triage_wait_fails", good + " Await the owner's triage ruling before resuming Jeremiah.", False),
        ("owner_decision_pending_fails", good + " OWNER DECISION PENDING: triage of the three dockets.", False),
        ("reissue_decision_request_fails", good + " If no ruling exists, STOP and re-issue the decision request.", False),
        ("do_not_resume_jeremiah_fails", good + " Do not resume Jeremiah until the owner rules.", False),
        ("ruling_pointer_removed_fails", good.replace(RULING_POINTERS[0], "OWNER_REPAIR_ADVANCE.md"), False),
        ("ruling_hash_wrong_fails", good.replace(sha(M8 / RULING_POINTERS[0])[:8], "deadbeef"), False),
        ("index_pointer_removed_fails", good.replace(RULING_POINTERS[1], "CURRENT_STATE.json"), False),
        ("ora_clause_missing_fails", good.replace("resolved-no-change, not an applied repair", "resolved-no-change, an applied repair"), False),
        ("no_wait_remains_still_passes", good + " No owner triage wait remains; the dockets are repaired under delegated judgment.", True),
        # v3.1 fixtures: labeled post-feedback repairs pass; unlabeled audit-implies-repair still fails
        ("labeled_postfeedback_repairs_pass", good + " Song repairs applied (post-feedback; receipts/OW2_repairs_Song.v1.json).", True),
        ("unlabeled_repairs_done_still_fails", good + " Item 2 audit DONE - repairs applied to the Psalms rows.", False),
        # v3.2 fixtures (OW-10): execution identity, cure binding, census coverage, prompt duties
        ("ow10_execution_identity_clause_missing_fails",
         good.replace("execution_id identifies ONE PHYSICAL RUN", "execution_id identifies the job"), False),
        ("ow10_retry_vs_rerun_clause_missing_fails",
         good.replace("re-running the same job is previous_execution_id; correcting a different job is retry_of",
                      "a retry is its own attempt record"), False),
        ("ow10_cure_binding_clause_missing_fails",
         good.replace("verification results bound to the exact resulting artifact plus the distinct-checker review",
                      "verification results and the distinct-checker review"), False),
        ("ow10_census_clause_missing_fails",
         good.replace("transcript coverage is reported from an explicit per-book census",
                      "transcript coverage is reported honestly"), False),
        # NOTE: this one is caught by the canonical arm, because stripping every "execution_id" also strips the
        # ow10_execution_identity clause. It is kept because it proves the strip is caught at all; the PAIRED arm
        # itself is proven separately below, at unit level, where nothing else can catch it first.
        ("retry_identity_strip_fails_somehow",
         re.sub(r"\bexecution[ _-]?id\b", "attempt marker", good, flags=re.I)
         + " A later attempt or a resume-in-place runs as a FRESH agent under the SAME attempt id.", False),
        ("retry_identity_paired_passes",
         good + " A later attempt runs as a FRESH agent under the SAME attempt id and records its own execution_id.",
         True),
        # v3.3 fixtures (OW-11): the registry exception's scope and expiry, the one-boundary continuation, the ceiling
        ("ow11_scope_clause_missing_fails",
         good.replace("the exception covers Ezekiel and Daniel only and expires at Daniel's close",
                      "the exception covers every later book"), False),
        ("ow11_one_boundary_clause_missing_fails",
         good.replace("at Ezekiel's close the run continues into Daniel; at Daniel's close the OW-9 hard stop applies",
                      "at each close the run continues into the next book"), False),
        ("ow11_registry_read_clause_missing_fails",
         good.replace("before the first M8 write, read the active-worktree registry's owner and identity rule for the lane",
                      "a validator PASS is enough to write"), False),
        ("ow11_budget_clause_missing_fails",
         good.replace("one combined 15M subagent-token ceiling for Ezekiel plus Daniel, with an owner check-in before crossing it",
                      "no budget applies"), False),
        # OW-11-h (2026-09-11): the authority paragraph travels in every launch message, not only in the brief
        ("ow11_authority_in_every_launch_clause_missing_fails",
         good.replace("the OW-11 authority paragraph goes in every launch message, not only in the brief",
                      "the authority text lives in the brief"), False),
    ]
    all_ok = True
    for name, text, expect_pass in fixtures:
        missing = check_text(text)
        did_pass = not missing
        ok = did_pass == expect_pass
        all_ok = all_ok and ok
        detail = "" if did_pass else f" (caught: {missing[0][:90]})"
        print(f"  {'OK' if ok else 'SELFTEST-BROKEN'}: {name} -> {'PASS' if did_pass else 'FAIL'}{detail}")

    # PAIRED-ARM UNIT VECTORS. In a full prompt the canonical arm catches a stripped execution_id first, so a
    # whole-prompt fixture can never prove the paired arm fires. These minimal texts isolate it. A control that is
    # only ever caught by a different control is not a proven control.
    unit = [
        ("paired:same_attempt_id_without_execution_id",
         "A later attempt runs as a FRESH agent under the SAME attempt id.", "retry_identity_confusion", True),
        ("paired:same_attempt_id_with_execution_id",
         "A later attempt runs as a FRESH agent under the SAME attempt id and records its own execution_id.",
         "retry_identity_confusion", False),
        ("paired:cure_without_binding",
         "The micro round cured the flagged rows.", "cure_without_binding", True),
        ("paired:cure_with_binding",
         "The micro round cured the flagged rows, with verification results bound to the exact resulting "
         "artifact.", "cure_without_binding", False),
        ("paired:continue_into_daniel_without_stop",
         "At Ezekiel's close the run continues into Daniel.", "continuation_without_daniel_stop", True),
        ("paired:continue_into_daniel_with_stop",
         "At Ezekiel's close the run continues into Daniel; at Daniel's close the OW-9 hard stop applies.",
         "continuation_without_daniel_stop", False),
        ("paired:registry_exception_without_expiry",
         "The owner lifted the Fable-5-only rule for this orchestration.", "registry_exception_without_expiry", True),
        ("paired:registry_exception_with_expiry",
         "The owner lifted the Fable-5-only rule for this orchestration; the exception expires at Daniel's close.",
         "registry_exception_without_expiry", False),
    ]
    for name, text, arm, expect_fire in unit:
        t = norm(text)
        fired = any(a == arm and trig.search(t) and not part.search(t)
                    for a, trig, part, _ in PAIRED_CLAUSES)
        ok = fired == expect_fire
        all_ok = all_ok and ok
        print(f"  {'OK' if ok else 'SELFTEST-BROKEN'}: {name} -> "
              f"{'FIRED' if fired else 'silent'} (expected {'FIRED' if expect_fire else 'silent'})")
    print("SELFTEST:", "PASS (all fixtures behave as required)" if all_ok
          else "FAIL — the checker itself is broken; do not print any prompt")
    return 0 if all_ok else 2


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    if len(sys.argv) > 1 and sys.argv[1] == "--binding":
        print(state_binding())
        return 0
    text = Path(sys.argv[1]).read_text(encoding="utf-8-sig")
    missing = check_text(text)
    if missing:
        print("SAFE_TO_CLEAR_CHECK: FAIL")
        for m in missing:
            print("  MISSING", m)
        return 1
    print("SAFE_TO_CLEAR_CHECK: PASS "
          f"(marker + bound cursor + {len(DONE_RECEIPTS)} receipt pointers + {len(DOCKET_POINTERS)} docket pointers + {len(RULING_POINTERS)} ruling/index pointers with hashes + "
          f"{len(CANONICAL)} canonical clauses + {len(CONTRADICTIONS)} contradiction arms + state binding + "
          f"{len(EXACT_PATHS_REQUIRED)} exact paths + corrupted-variant rejection + next-prompt instruction)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
