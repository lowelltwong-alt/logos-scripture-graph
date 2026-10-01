#!/usr/bin/env python3
"""OW-2-CARRY-IDEMPOTENCY mechanical pre-print verifier (owner clarification
2026-08-31; HARDENED per the OW-2D sequencing ruling — transport/copy-resilience
control). Every generated SAFE-TO-CLEAR prompt is checked BEFORE printing:

  1. the OW-2-CARRY-IDEMPOTENCY marker;
  2. the latest unresolved-item cursor (a "phase =" cursor line);
  3. the completed-receipt pointers (every receipt in DONE_RECEIPTS);
  4. every permanent prospective safeguard (keyword arms below);
  5. the instruction to generate the following prompt at next session close;
  6. EXACT-PATH ARMS (OW-2D): the two required path strings present with
     their backslashes intact, and the known backslash-dropped render/copy
     variants ABSENT. The chat-rendered copy of the 2026-08-31 prompt
     dropped two backslashes in transit while the durable prompt was
     correct — this arm makes any such transport corruption fail closed.

A prompt that fails is NOT printed — fix and re-check. When a one-time item
completes, append its receipt path to DONE_RECEIPTS (orchestrator-owned
edit, mirrored durable, supersede-with-note in the census).

Usage: _safe_to_clear_check.py PROMPT_FILE
       _safe_to_clear_check.py --selftest   (negative-fixture proof run)
"""
import re
import sys
from pathlib import Path

DONE_RECEIPTS = [
    "receipts/OW2_review_status_resolution.json",
    "receipts/OW2_audit_budget_checkpoint.json",
    "receipts/OW2_isa_lf_audit.json",  # item 1 DONE 2026-09-03
]

EXACT_PATHS_REQUIRED = [
    r"C:\Users\lowel\.agent-governance\validate_workspace_policy.ps1",
    r"SP\Jer\_safe_to_clear_check.py",
]
CORRUPTED_VARIANTS_REJECTED = [
    r"C:\Users\lowel.agent-governance\validate_workspace_policy.ps1",
    r"SP\Jer_safe_to_clear_check.py",
]

SAFEGUARDS = {
    "no_m7_or_comparison_reads": re.compile(r"\bM7\b", re.I),
    "tier4_never_drives": re.compile(
        r"tier-4|translation punctuation", re.I),
    "cwo_execution_parity": re.compile(r"execution parity", re.I),
    "hard_book_close_gates": re.compile(
        r"close gates|book-close gates|CAMPAIGN_CLOSE_GATE", re.I),
    "second_gen_sweep_role_separation": re.compile(
        r"second-generation[^.]{0,120}(checker|author)", re.I),
    "attempt_receipt_recording": re.compile(
        r"(model|effort)[^.]{0,160}denominators|producer/catcher", re.I),
    "one_correlated_voice": re.compile(r"one correlated", re.I),
    "revelation_requirements": re.compile(
        r"Revelation[^.]{0,160}Opus 5 high[^.]{0,80}Fable 5 high", re.I),
}

REQUIRED = {
    "marker": re.compile(r"OW-2-CARRY-IDEMPOTENCY"),
    "cursor": re.compile(r"phase\s*="),
    "generate_next_prompt": re.compile(
        r"(print|generate)[^.]{0,200}(resume prompt|SAFE-TO-CLEAR|next session)",
        re.I),
}


def check_text(text: str):
    missing = []
    for name, pat in REQUIRED.items():
        if not pat.search(text):
            missing.append(f"required:{name}")
    for r in DONE_RECEIPTS:
        if r not in text:
            missing.append(f"done_receipt_pointer:{r}")
    for name, pat in SAFEGUARDS.items():
        if not pat.search(text):
            missing.append(f"safeguard:{name}")
    for p in EXACT_PATHS_REQUIRED:
        if p not in text:
            missing.append(f"exact_path_missing:{p}")
    for v in CORRUPTED_VARIANTS_REJECTED:
        if v in text:
            missing.append(f"corrupted_variant_present:{v}")
    return missing


def selftest():
    good = (
        "OW-2-CARRY-IDEMPOTENCY. cursor: phase = ow2_checkpoint_pause. "
        "receipts/OW2_review_status_resolution.json, "
        "receipts/OW2_audit_budget_checkpoint.json, and "
        "receipts/OW2_isa_lf_audit.json are DONE. "
        "No M7 reads; translation punctuation and tier-4 metadata never drive "
        "a boundary; execution parity holds; the book-close gates of "
        "CAMPAIGN_CLOSE_GATE bind; a fresh second-generation sweep runs with a "
        "checker distinct from the repair author; receipts record actual "
        "model/effort, exact denominators, producer/catcher roles, evidence "
        "paths, and hashes; agreement is one correlated M8 voice; Revelation "
        "requires Opus 5 high review plus Fable 5 high adversarial "
        "adjudication. Run "
        r"C:\Users\lowel\.agent-governance\validate_workspace_policy.ps1"
        " first, and verify mechanically with "
        r"SP\Jer\_safe_to_clear_check.py"
        " before printing. At close, generate the next session's resume "
        "prompt and print it."
    )
    fixtures = [
        ("good_prompt_passes", good, True),
        ("dropped_backslash_governance_path_fails",
         good.replace(r"C:\Users\lowel\.agent-governance\validate_workspace_policy.ps1",
                      r"C:\Users\lowel.agent-governance\validate_workspace_policy.ps1"),
         False),
        ("dropped_backslash_checker_path_fails",
         good.replace(r"SP\Jer\_safe_to_clear_check.py",
                      r"SP\Jer_safe_to_clear_check.py"),
         False),
        ("missing_marker_fails",
         good.replace("OW-2-CARRY-IDEMPOTENCY", "OW-2-CARRY"), False),
        ("missing_receipt_pointer_fails",
         good.replace("receipts/OW2_audit_budget_checkpoint.json",
                      "receipts/OW2_audit_budget.json"), False),
    ]
    all_ok = True
    for name, text, expect_pass in fixtures:
        missing = check_text(text)
        did_pass = not missing
        ok = did_pass == expect_pass
        all_ok = all_ok and ok
        verdict = "OK" if ok else "SELFTEST-BROKEN"
        detail = "" if did_pass else f" (caught: {missing[0]}...)" if missing else ""
        print(f"  {verdict}: {name} -> {'PASS' if did_pass else 'FAIL'}{detail}")
    print("SELFTEST:", "PASS (all fixtures behave as required)" if all_ok
          else "FAIL — the checker itself is broken; do not print any prompt")
    return 0 if all_ok else 2


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    text = Path(sys.argv[1]).read_text(encoding="utf-8-sig")
    missing = check_text(text)
    if missing:
        print("SAFE_TO_CLEAR_CHECK: FAIL")
        for m in missing:
            print("  MISSING", m)
        return 1
    print("SAFE_TO_CLEAR_CHECK: PASS "
          f"(marker + cursor + {len(DONE_RECEIPTS)} receipt pointer(s) + "
          f"{len(SAFEGUARDS)} safeguards + {len(EXACT_PATHS_REQUIRED)} exact "
          "paths + corrupted-variant rejection + next-prompt instruction)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
