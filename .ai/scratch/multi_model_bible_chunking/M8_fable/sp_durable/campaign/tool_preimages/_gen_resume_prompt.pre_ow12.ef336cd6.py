#!/usr/bin/env python3
"""Generate the next session's resume prompt FROM STATE (OWNER_REPAIR_ADVANCE_2026-09-06 item 4):
STATE-BINDING from the checker's --binding; the ruling + index pointers with current hashes; the
DONE receipts + dockets with current hashes; every canonical clause the checker requires (read from
the checker module so prompt and checker never drift); the exact paths; the generate/check/save/
read-back/print duties; the live cursor + next authorized job from a small state JSON the
orchestrator writes at close. Then: archive the prior slot prompt hash-addressed, write the slot,
read it back, verify with the checker, and print the verified text.
Usage: _gen_resume_prompt.py state.json"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

SC = Path(__file__).resolve().parent
SP = SC / "SP"
JER = SP / "Jer"
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
SLOT = M8 / "RESUME_PROMPT_CURRENT.md"
sys.dont_write_bytecode = True


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_checker():
    spec = importlib.util.spec_from_file_location("stc", JER / "_safe_to_clear_check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    st = json.load(open(sys.argv[1], encoding="utf-8"))
    chk = load_checker()
    binding = subprocess.run([sys.executable, str(JER / "_safe_to_clear_check.py"), "--binding"], capture_output=True, text=True, encoding="utf-8").stdout.strip()
    assert binding.startswith("STATE-BINDING: ")
    ptr = {p: sha(M8 / p)[:8] for p in chk.DONE_RECEIPTS + chk.DOCKET_POINTERS + chk.RULING_POINTERS}
    canon = chk.CANONICAL
    ow3_full = json.load(open(SC / "_ow3_safeguards.json", encoding="utf-8"))
    safeguards = [
        canon["no_m7_or_comparison_reads"] + " (nor A/B lanes, mixed-lane or broad project-status context)",
        canon["tier4_never_drives"] + " (E-23)",
        canon["cwo_execution_parity"] + " - every CWO executes as its OWN sweep, never folded per-row (E-18)",
        canon["hard_book_close_gates"],
        canon["second_gen_sweep_role_separation"] + " (_wave_repair_sweep.py / _book_repair_sweep.py are the staged deterministic arms; a deterministic pass is not semantic verification)",
        canon["attempt_receipt_recording"],
        canon["one_correlated_voice"],
        canon["revelation_requirements"] + " on the six named seam classes (vision-cycle, speaker/voice, quotation, recapitulation-versus-sequence, textual-variant, cross-chapter)",
    ] + ow3_full + [
        canon["ora_delegated_repair"] + " (no per-item owner approval; span proposals accepted or rejected inside the owner-ruled book strategy with reasons + evidence in the dispositions ledgers)",
        canon["ora_rejection_resolved"],
        canon["ora_prelam_lift"] + "; Lamentations and the following books then proceed in canonical order without a routine permission request",
        canon["ora_prov38_denominator"] + "; supplemental crux-site observations are recorded separately with their own scope",
        # OW-6 / OW-6b / OW-6c (owner directives, 2026-09-07) - the checker requires each of these verbatim
        canon["ow6_final_checker"] + " (stage 1: Fable transcript auditors read the runtime records in full over disjoint slices; stage 2: ONE Fable final checker consolidates and rules; not_fit_to_close orders a bounded fix round and a fresh final check)",
        canon["ow6_fable_boss_escalation"] + " (the orchestrator does not decide an escalated question itself)",
        canon["ow6_escalation_packet"],
        canon["ow6_continue_next_book"] + " (OW-6's straight-through continuation is SUPERSEDED and is kept in the ledger marked as superseded, not deleted; OW-5's straight-through clause is spent, having been scoped to Jeremiah and Lamentations)",
        canon["ow9_stop_at_book_boundary"] + ": when the hard close gate passes and the completion receipt is written, STOP. Do not open the next book, do not start Phase 0, do not launch a probe. Run the durability checkpoint (mirrors, CYCLE_STATE cursor, CURRENT_STATE rebuild), regenerate the prompt slot, VERIFY it, then end the turn. The owner clears and re-prompts with that text. OW-11 EXCEPTION, ONE BOUNDARY ONLY: " + canon["ow11_one_boundary"] + "; at Ezekiel's close the durability checkpoint still runs and the slot is still regenerated and verified, then Daniel's Phase 0 opens without a stop",
        canon["ow9_prompt_printed_in_chat"] + ": every resume prompt is PRINTED IN FULL IN THE CHAT for copy and paste, in addition to being saved to the slot and verified. A file the owner must open is not a prompt they can paste, and attaching it does not satisfy this",
        canon["ow6b_hard_track"] + " (hard-track arms: Fable boss at high effort, raised peer and spot coverage with no sampling shortcut on flagged regions, whole-book final audit, and a second independent Fable review of the flagged regions before the close)",
        canon["ow6c_end_of_campaign_recheck"] + " (transcripts are indexed per book and copied to sp_durable/transcripts/ so the option stays real; where an early book's transcripts were never captured the packet says so plainly)",
        # 2026-09-07 evidence-integrity controls, learned the hard way in Lam and binding on every later book
        "TRANSCRIPT EVIDENCE DECAYS: the runtime deletes written transcripts mid-session, so _mirror_transcripts.py "
        "runs at every wave landing and BEFORE any final check is launched; a transcript held nowhere is reported as "
        "permanently lost, never silently omitted from a slice (SP/campaign/finding_transcript_decay.v1.json)",
        "A FILE'S KIND IS DECIDED BY ITS CONTENT, NEVER BY ITS DIRECTORY OR EXTENSION: the session tasks/ directory "
        "holds subagent transcripts AND captured orchestrator shell output under the same <id>.output name. Every "
        "tool that enumerates it applies is_subagent_transcript() and REPORTS what it excluded. Conflating the two "
        "put 18 shell outputs into four Fable audit slices before it was caught "
        "(SP/campaign/finding_orchestrator_shell_output_conflation.v1.json)",
        # OW-7 (owner directive, 2026-09-07) - answers B3-2 and four final-check escalations
        "OW-7 UNIVERSAL PER-ATTEMPT CAPTURE, THREE LAYERS NEVER MERGED: every attempt of every role, "
        "including nested subagents, records layer A (runtime-captured actions, tool calls, results, file "
        "writes - NOT self-authored), layer B (exposed thinking summaries - sporadic, never full) and layer "
        "C (the agent's own evidence note - self-authored). They are stored separately, never merged into "
        "one apparent chain of thought, and layer C is never presented as chain of thought. A layer that "
        "does not exist is written UNAVAILABLE with its reason, never blank and never filled from another "
        "layer (SP/campaign/CAPTURE_CONTRACT.v3.md)",
        "OW-7 IDENTITY AND LINEAGE: every attempt carries book, task, agent id, PARENT agent id, role, "
        "model ordered, model ACTUAL where a runtime record shows it (else UNAVAILABLE - never inferred), "
        "and a unique attempt id. A nested subagent's records belong to the CHILD and are never attributed "
        "to the parent. A retry is its own attempt record carrying retry_of; the original is never "
        "overwritten",
        # OW-10 (owner directive, 2026-09-08) - resolves the OW-7 / E-14 identity contradiction
        canon["ow10_execution_identity"] + " (`<attempt_id>#e<N>`, with execution_of, execution_ordinal and "
        "previous_execution_id). E-14's ladder still keys off the STABLE attempt_id - that is what keeps it "
        "idempotent - and the fresh agent it launches ALSO records its own execution_id. Historical ids are never "
        "renamed, ordinals derive deterministically from receipt order, no completed work is duplicated. Layers A, "
        "B and C attach to the EXECUTION, not the job; where a manifest maps a transcript to a job and cannot say "
        "which run produced it, layer A is UNAVAILABLE with the ambiguity NAMED, never handed to whichever run was "
        "first (SP/campaign/CAPTURE_CONTRACT.v3.md; v2 and v1 retained, superseded on identity)",
        canon["ow10_retry_vs_rerun"] + "; the two relations are never conflated, and a close packet that conflates "
        "them fails gate item 14",
        "OW-10 A CURE IS NOT CURED BECAUSE ITS AUTHOR SAYS SO: before a repair is accepted as cured, "
        + canon["ow10_cure_binding"] + " - three digests must agree (artifact_sha256_at_run, the claim's "
        "artifact_sha256, and the artifact on disk now). " + canon["ow10_self_report_insufficient"] + ". Refused: "
        "any verification with no machine result; any result whose artifact_sha256_at_run != the shipped artifact; "
        "a distinct_checker naming the author's own attempt or execution; and the bare words passed/cured/verified "
        "standing in for any of these (SP/campaign/_cure_verification.py, selftest 8 vectors GREEN). This does NOT "
        "replace the distinct-checker second-generation sweep",
        "OW-10 COVERAGE IS COUNTED, NEVER REMEMBERED: " + canon["ow10_census_coverage"]
        + " (SP/campaign/_transcript_coverage_census.py -> transcript_coverage_census.v1.json), which counts "
        "attempts, transcript_retained and observed per book and NEVER adds them together. Producing the census is "
        "not authority to launch another blanket audit",
        "OW-10 THE FIVE RESTART-PROMPT DUTIES ARE PERMANENT: every restart prompt is "
        + canon["ow10_prompt_duties"] + ". 'Safe to clear' may not be said unless every required state and prompt "
        "save is verified; on failure, preserve the work and report the specific blocker",
        # OW-11 (owner directive, 2026-09-10) - registry exception, one-boundary continuation, combined ceiling
        "OW-11 WRITE AUTHORITY (owner directive 2026-09-10, recorded in the M8 log only by owner choice; authorization_ref "
        "lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan): " + canon["ow11_write_authority"] + ". "
        + canon["ow11_scope"] + "; it grants no commit, push, merge, cleanup or comparison authority, and "
        "ACTIVE_WORKTREES.yaml is updated by the owner, never by the orchestrator",
        "OW-11 RESUME DISCIPLINE: " + canon["ow11_registry_read"] + " - the scoped validator passes owner-scoped "
        "uncommitted work without checking which identity wrote it, so a PASS is not authority; "
        + canon["ow11_deliverables_outside_worktree"] + " (an orchestrator-created directory outside "
        "C:\\wt\\logos-t423-m8-fable; landing verifies parity, writes the receipt and the layer-C note, and rebuilds the index); "
        + canon["ow11_authority_in_every_launch"] + " (OW-11-h: a subagent may read the registry before it opens its brief, so the "
        "owner's verbatim answers, the authorization_ref and the ledger path go in the launch message itself; an agent that "
        "stops again with the paragraph present goes to the owner, not to a third launch)",
        "OW-11 BUDGET: " + canon["ow11_budget"] + "; for these two books it replaces the ~7M soft cap and the pre-8M check-in, "
        "and every close packet states cumulative spend counted from receipts",
        "OW-7 REVIEWER BLINDNESS SURVIVES THE INDEX: SP/campaign/capture_index.v1.jsonl links the records "
        "and never holds their content, but collecting records does not authorize sharing them. A lane "
        "still under a blindness constraint is never given the index, another lane's records, or any "
        "conclusion drawn from them, before its own independent review has landed; the index is a "
        "permitted read for the orchestrator and post-review lanes only",
        # OW-8 (owner directive, 2026-09-07) - refines OW-7
        "OW-8 THE RECORD IS AN ACCOUNTABLE WORK SUMMARY, not chain of thought and not independent proof: "
        "attempt id, source/artifact references, the changes made OR an explicit no-change outcome, "
        "verification evidence, and unresolved uncertainty. A MECHANICAL attempt may use a compact "
        "machine-receipt pointer instead of prose (SP/campaign/CAPTURE_CONTRACT.v3.md, which supersedes v2 on "
        "identity; v2 and v1 retained)",
        "OW-8 AUDIT SCOPE IS WHAT EXISTS: OW-6 and OW-6c audit available deliverables, evidence records, "
        "receipts, observable actions and retained transcripts. Existing transcripts are preserved and the "
        "records SUPPLEMENT rather than replace them. Do NOT fabricate missing historical records and do NOT "
        "restart completed audits merely because transcripts are absent",
        "OW-8 MISSING LOGS ARE NOT A STOP CONDITION: an evidence gap is not a defect and the campaign "
        "continues under the existing substantive quality gates; demonstrated material defects still require "
        "containment and repair. The breach report is SP/campaign/breach_report.v1.json. Runtime-capture "
        "changes remain a SEPARATE open owner decision",
        "A COVERAGE STATEMENT IS NOT COVERAGE: _final_check_reconcile.py compares every stage-1 packet against the "
        "slice plan and the manifest (assigned vs reported, disjointness, union, byte arithmetic) and the close gate "
        "refuses on RED. The stage-2 checker states transcript coverage explicitly and the gate asserts it is stated",
    ]
    lines = []
    lines.append("Continue the M8_fable whole-Bible chunking marathon from disk state only. OW-2-CARRY-IDEMPOTENCY.")
    lines.append(binding)
    lines.append(f"STANDING OWNER RULING: OWNER_REPAIR_ADVANCE_2026-09-06.md (sha256 {ptr['OWNER_REPAIR_ADVANCE_2026-09-06.md']}…; canonical verbatim copy at C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\OWNER_REPAIR_ADVANCE_2026-09-06.md - read it in full first) plus OW-4 (\"get this book compleyted\", confirmed twice \"yes complete jeremiah\": complete Jeremiah now). The OW-2D owner-only docket-triage wait, per-proposal owner span approval, and the owner-only pre-Lamentations pause are SUPERSEDED as active controls (history preserved in the ledger, gate item 9 and CYCLE_STATE); never reactivate a superseded wait after a clear. VERIFIED CURRENT STATE: CURRENT_STATE.v1.json (sha256 {ptr['CURRENT_STATE.v1.json']}…; M8_fable root; generated from disk by sp_durable/Jer/_build_current_state.py) - it plus the canonical active rules (ERROR_PATTERN_LEDGER.v1.md addenda through 2026-09-10 incl. OW-6/OW-6b/OW-6c, OW-7, OW-8, OW-9, OW-10 and OW-11, and CAMPAIGN_CLOSE_GATE.v1.md items 1-15) REPLACES the full-history CYCLE_STATE reread; sp_durable/<LIVE BOOK>/freeze/CYCLE_STATE.md is the immutable append-only log of the book in progress (Ezekiel's is sp_durable/Ezek/freeze/CYCLE_STATE.md; the Jer and Lam logs are closed history), consulted only when needed (its LAST 'CURSOR: phase =' line must equal the index's phase).")
    lines.append("STATE: " + st["state_text"])
    lines.append(f"cursor: phase = {chk.latest_cursor_phase()}. NEXT AUTHORIZED JOB: " + st["next_job"])
    lines.append("GOVERNANCE FIRST: before the first M8 write, read the active-worktree registry's owner and identity rule for the lane (C:\\Users\\lowel\\.agent-governance\\ACTIVE_WORKTREES.yaml, entry logos-t423-m8-fable) and the OW-11 record in ERROR_PATTERN_LEDGER.v1.md; then run C:\\Users\\lowel\\.agent-governance\\validate_workspace_policy.ps1 -ScopeWorktreeId logos-t423-m8-fable (expect PASS; verify live HEAD == remote == 8dce6681685c7a1d89978a9d90a11046e74fdfcc and the delta owner-scoped M8 material only; a NEW mismatch is a stop condition - but a NEW confirmed owner durability commit is surfaced, confirmed in chat, and re-pinned in all THREE typed-record copies per the 2026-08-27 precedent). Probe: python scripts/t423_resume_book.py .ai/scratch/multi_model_bible_chunking/M8_fable --json in C:\\wt\\logos-t423-m8-fable (expect " + st["probe_expect"] + "). Read: the standing ruling in full; CURRENT_STATE.v1.json (hash-verify against this prompt; every pinned artifact hash inside it must still match disk); model_manifest.yaml subagent_routing; mesh_structure_r3 in M8_fable/corrective_rereview_contract.v1.yaml; ERROR_PATTERN_LEDGER.v1.md addenda OW-1..OW-4 + OWNER_REPAIR_ADVANCE + OW-6..OW-11 (the FORWARD-APPLICATION LAW stands: briefs re-derive every carried behavior from the ledger, never from this prompt); CAMPAIGN_CLOSE_GATE.v1.md items 1-15 (item 15 carries OW-11's scoped write authority, one-boundary continuation and combined ceiling; items 10-12 carry OW-6, OW-6b and OW-6c: the Fable final-checker gate, the hard-book track with Fable as controlling agent, and the end-of-campaign re-check decision; item 13 carries OW-7's universal per-attempt capture; item 14 carries OW-10's execution identity, cure binding, census coverage and the five permanent restart-prompt duties). OWNER_LESSONS stays hash-only. " + st["rebuild_text"])
    lines.append("ONE-TIME OW-2 ITEMS (receipt-gated idempotency law: never rerun a DONE item unless its receipt is absent or failed, a pinned hash invalidates the applicable gate, or the owner explicitly orders a rerun; completed one-time checks stay completed):")
    lines.append(f"* DONE: the 347 review_status correction - receipts/OW2_review_status_resolution.json (sha256 {ptr['receipts/OW2_review_status_resolution.json']}…; verify its pinned hashes on resume; never perform the correction again).")
    lines.append(f"* DONE: the audit-budget checkpoint - receipts/OW2_audit_budget_checkpoint.json (sha256 {ptr['receipts/OW2_audit_budget_checkpoint.json']}…).")
    lines.append(f"* DONE (audit completion only): item 1, the 155/155 Isaiah LF-support audit - receipts/OW2_isa_lf_audit.json (sha256 {ptr['receipts/OW2_isa_lf_audit.json']}…) with its read-only baseline docket receipts/OW2_isa_lf_remediation_docket.v1.json (sha256 {ptr['receipts/OW2_isa_lf_remediation_docket.v1.json']}…) and its dispositions ledger receipts/OW2_isa_lf_remediation_dispositions.v1.json (live open/resolved state; every resolution carries independent post-repair evidence and the post-feedback label). Never rerun the audit.")
    lines.append(f"* DONE (audit completion only): item 2, the 213-row Ps/Job/Prov/Eccl/Song semantic scope - receipts/OW2_five_book_semantic_audit.json (sha256 {ptr['receipts/OW2_five_book_semantic_audit.json']}…) with docket receipts/OW2_five_book_remediation_docket.v1.json (sha256 {ptr['receipts/OW2_five_book_remediation_docket.v1.json']}…) and ledger receipts/OW2_five_book_remediation_dispositions.v1.json. Never rerun the audit.")
    lines.append(f"* DONE (audit completion only): item 3, the deferred 38-row Proverbs Opus review - receipts/OW2_prov38_opus_review.json (sha256 {ptr['receipts/OW2_prov38_opus_review.json']}…) with docket receipts/OW2_prov38_remediation_docket.v1.json (sha256 {ptr['receipts/OW2_prov38_remediation_docket.v1.json']}…) and ledger receipts/OW2_prov38_remediation_dispositions.v1.json. Never rerun the review.")
    lines.append("* BACKLOG REPAIR LANE (under the standing ruling): " + st["backlog_text"])
    lines.append("* OW-3 (2026-09-04) one-time checks DONE: checker hardening (v3.1 live; v2 and v1 preserved), the bounded Isaiah re-adjudication, placeholder resolution + rejection arms, the dispositions ledgers, the dependency-applicability records - never rerun merely after a clear.")
    lines.append("PERMANENT SAFEGUARDS (every generated prompt carries these until the marathon completes at 66/66): " + "; ".join(safeguards) + ".")
    lines.append("OPERATIONAL LAWS (pointers - the ledger is the carrier): the E-13 research-context preamble PLUS both E-19 lines (the affirmative no-check line and the exact-path law line) go in EVERY launch message; SendMessage is unavailable in this runtime, so a later attempt or a resume-in-place runs as a FRESH agent under the SAME attempt id that appends to the existing deliverable, AND that fresh agent records its own execution_id (E-14 ladder, as amended by OW-10: deliverable ABSENT -> fresh launch under the same STABLE attempt id, allocating the next execution_id `<attempt_id>#e<N>` with previous_execution_id set; PRESENT -> validate, never re-run. The stable attempt id is what makes the ladder idempotent; the execution id is what stops a re-launch from being silently dropped, as four Lamentations transcript-auditor runs were before OW-10); E-22 governs HTTP-429 spend-limit kills (stop launching, record state, re-verify governance on reset, then the E-14 ladder per agent); census numbers come from the tool's COUNT, never from prose arithmetic; every lane verifier accepts grounds as a string or a list of strings, reports any other type, and rejects unexpanded placeholders; the owner budget law stands (soft cap ~7M subagent tokens/session, MANDATORY owner check-in before crossing 8M; overrun OK when necessary, the bar is no WASTED tokens; " + st["spend_text"] + ").")
    lines.append("AT SESSION CLOSE (or any boundary): append the batch census + cursor to the LIVE book's log SP/<Book>/freeze/CYCLE_STATE.md (Ezekiel: SP/Ezek/freeze/CYCLE_STATE.md) - never to a closed book's log; record any NEW owner directive received during the session VERBATIM (ledger MD + JSONL, gate, CYCLE_STATE) BEFORE closing; mirror the changed durable set with per-file hash verification (_mirror_jer.py / _mirror_durable.py, fail-closed); rebuild CURRENT_STATE.v1.json from disk (python SP\\Jer\\_build_current_state.py --next \"<exact next job>\"); then GENERATE the next session's resume prompt fresh from that state (python _gen_resume_prompt.py state.json: STATE-BINDING from python SP\\Jer\\_safe_to_clear_check.py --binding; never carry consumed batch instructions, stale counts, or completed rechecks as active work; include the ruling pointer + hash and the index pointer + hash), verify it MECHANICALLY with SP\\Jer\\_safe_to_clear_check.py (v3.2: it must print PASS - canonical clauses incl. the ruling's, contradiction rejection incl. stale owner-triage waits, state binding incl. ruling= and index=, receipt + docket + ruling + index pointers with current hashes; run --selftest first, including its OW-10 paired-arm unit vectors), ARCHIVE the prior slot prompt hash-addressed under receipts/prompt_archive/ (immutable), WRITE the verified prompt to C:\\wt\\logos-t423-m8-fable\\.ai\\scratch\\multi_model_bible_chunking\\M8_fable\\RESUME_PROMPT_CURRENT.md (the EXISTING single current slot), READ IT BACK and re-verify the saved file, and only then PRINT that EXACT saved prompt to the owner as the session's final message in a clearly labeled copyable block (\"Paste this after clearing context.\") with its absolute saved path - never claim safe-to-clear if persistence or verification failed; always including this same generate/check/save/read-back/print duty plus the durable ruling pointer so every session ends by handing the owner the prompt that starts the next one. Do not auto-clear the owner's context. RECOVERY RULE: if no prompt was pasted, read and verify RESUME_PROMPT_CURRENT.md at that exact path, then its named ruling and CURRENT_STATE.v1.json; if stale or contradictory, reconcile from durable evidence before any write - never guess, never fall back silently to an archived prompt.")
    text = "\n".join(lines) + "\n"
    draft = SC / "_resume_prompt_draft.md"
    draft.write_text(text, encoding="utf-8", newline="\n")
    r = subprocess.run([sys.executable, str(JER / "_safe_to_clear_check.py"), str(draft)], capture_output=True, text=True, encoding="utf-8")
    print(r.stdout.strip())
    if r.returncode != 0:
        print("DRAFT FAILED THE CHECKER - not written to the slot"); return 1
    if "--draft-only" in sys.argv:
        print("DRAFT ONLY (slot untouched):", draft); return 0
    # archive prior slot (hash-addressed, immutable), write, read back, re-verify
    arch = M8 / "receipts" / "prompt_archive"
    arch.mkdir(exist_ok=True)
    if SLOT.is_file():
        old = sha(SLOT)
        ap = arch / f"RESUME_PROMPT_{date.today().isoformat()}_{old[:8]}.md"
        if not ap.is_file():
            ap.write_bytes(SLOT.read_bytes())
        assert sha(ap) == old
        print("archived prior slot ->", ap.name, old[:16])
    SLOT.write_text(text, encoding="utf-8", newline="\n")
    back = SLOT.read_text(encoding="utf-8")
    assert back == text, "read-back differs from the generated text"
    r2 = subprocess.run([sys.executable, str(JER / "_safe_to_clear_check.py"), str(SLOT)], capture_output=True, text=True, encoding="utf-8")
    print("READ-BACK:", r2.stdout.strip())
    if r2.returncode != 0:
        print("SAVED SLOT FAILED RE-VERIFICATION"); return 1
    print("SLOT WRITTEN:", SLOT, "sha256", sha(SLOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
