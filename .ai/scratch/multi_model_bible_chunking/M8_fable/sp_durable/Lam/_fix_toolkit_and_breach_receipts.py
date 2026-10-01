#!/usr/bin/env python3
"""Fix-round item (6), two of the low residuals: the toolkit's parashah erratum, and the breach-disclosure
amendments for a02, a03 and cwo04.

(A) THE TOOLKIT ERRATUM is the more dangerous of the two despite its severity. The toolkit is the file every agent
is told to trust and not re-derive, and its parashah paragraph says every verse of chapters 1-4 carries a mark,
including "3:1-65 SAMEKH". pmarks_Lam.json marks chapter 3 at 22 verses only - a SAMEKH at every third verse, 3:3
through 3:63, and a PE at 3:66 - which is what the toolkit's own digits (5 PE / 84 SAMEKH / 89 verses) require. The
paragraph contradicts the digits three lines above it. No shipped row carries the false prose, because a primary and
the boss each re-derived the layer and corrected it in their own work; the erratum is recorded so the next agent who
trusts the file as instructed is not the one who finds it.

An erratum, not an edit: the original sentence stays and is marked wrong beside its correction. A "trust this" file
that silently changes is worse than one with a visible correction, because an agent who quoted the old text has no
way to discover that it moved.

(B) THE BREACH AMENDMENTS record, append-only, what three authors' transcripts showed and their receipts did not.
Each amendment states the breach, whether the agent disclosed it, and whether residue remains - all three have none,
confirmed by exact-path check and a CLEAN stray sweep. The receipts themselves are not rewritten: a receipt's
e19_selfreported field records what the AGENT reported, and filling it in on the agent's behalf would destroy the
distinction between a breach an agent disclosed and one an auditor found. That distinction is the finding.
Usage: _fix_toolkit_and_breach_receipts.py [--apply]"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLKIT = HERE / "tools" / "TOOLKIT.md"
AMEND = HERE / "final_check" / "receipt_amendments.v1.jsonl"
LOG = HERE / "freeze" / "CYCLE_STATE.md"
NL = "\n"

BREACHES = [
    {"attempt_id": "lam_auth_a02_a1", "receipt_file": "author/lam_author_attempt_receipts.jsonl",
     "breaches": [
         {"what": "created its private scratch at SP/Lam/author/lam_lam_auth_a02_a1_private and wrote ~25 files "
                  "into it, including a swapped copy of the frozen corpus and two validator reports",
          "self_disclosed": False, "residue": "NONE - relocated out of SP with digest verification at the wave close"},
         {"what": "ran a listing against SP/Lam/tools", "self_disclosed": False, "residue": "n/a (a read)"},
         {"what": "redirected collate.py stdout and stderr into SP/Lam/tools as collate_out.tmp and collate_err.tmp",
          "self_disclosed": False, "residue": "NONE - both absent at exact-path check"}],
     "receipt_said": "tokens_note named the scratch-directory location only; e19_selfreported null"},
    {"attempt_id": "lam_auth_a03_a1", "receipt_file": "author/lam_author_attempt_receipts.jsonl",
     "breaches": [
         {"what": "listed SP/Lam/tools and SP/Lam/author, the latter surfacing the other authors' output filenames",
          "self_disclosed": False, "residue": "n/a (a read); no other author's packet CONTENT was read"},
         {"what": "ran the validator suite over its SP deliverable, writing a transient report under SP",
          "self_disclosed": False, "residue": "NONE - the transient report was deleted in-run"}],
     "receipt_said": "e19_selfreported null; tokens_note null"},
    {"attempt_id": "lam_cwo_04_a1", "receipt_file": "cwo/lam_cwo_attempt_receipts.jsonl",
     "breaches": [
         {"what": "ran listings against SP/Lam/cwo and SP/Lam/tools", "self_disclosed": True,
          "residue": "n/a (a read)",
          "note": "disclosed twice in its own final message; the disclosure understated the exposure slightly by "
                  "saying the listed tool filenames were 'already documented in TOOLKIT.md' - five were not"},
         {"what": "redirected two sweep.py outputs into SP/Lam/tools as out_bat_edom.txt and out_bat_tsiyon.txt",
          "self_disclosed": False, "residue": "NONE - both absent at exact-path check"}],
     "receipt_said": "e19_selfreported named the listings only"},
]

ERRATUM = """

---

## ERRATUM 2026-09-07 (recorded during the OW-6 fix round; raised by the stage-2 final checker)

**The parashah paragraph above is WRONG where it says every verse of chapters 1-4 carries a mark, and specifically
where it writes "3:1-65 SAMEKH".** The original sentence is left standing above rather than edited, because this is
a file agents are told to trust and not re-derive: an agent that already quoted the old text must be able to find
out that it moved.

**The fact, from `pmarks_Lam.json`:** chapter 3 carries marks at **22 verses only** - a SAMEKH at every third verse,
3:3, 3:6, 3:9 … 3:63, and a PE at 3:66. Chapter 3's marks track the acrostic TRIPLETS, one mark per triplet, not one
per verse.

**This is what the toolkit's own digits already require.** The 5 PE / 84 SAMEKH / 89 marked-verse totals recorded
above are only reachable with chapter 3 at 22, not at 66; the paragraph contradicted the digits three lines above
it. Tier is unchanged: the parashah layer stays **tier-3, single-witness**, and never drives a boundary.

**Shipped impact: none.** No corpus row carries the false prose. One primary reviewer and the boss each re-derived
the layer from `pmarks_Lam.json` rather than trusting the paragraph, and corrected it inside their own work - which
is the behaviour the hazard catalog asks for, and the reason this stayed an erratum instead of a defect.
"""


def main():
    apply = "--apply" in sys.argv
    now = datetime.now(timezone.utc).isoformat()
    tk = TOOLKIT.read_text(encoding="utf-8")
    already_tk = "ERRATUM 2026-09-07" in tk

    sys.stdout.reconfigure(encoding="utf-8")
    if not apply:
        print(json.dumps({"dry_run": True, "toolkit_erratum_needed": not already_tk,
                          "toolkit_sha16_now": hashlib.sha256(TOOLKIT.read_bytes()).hexdigest()[:16],
                          "breach_amendments": [b["attempt_id"] for b in BREACHES]}, indent=1))
        return 0

    if not already_tk:
        TOOLKIT.write_text(tk + ERRATUM, encoding="utf-8", newline=NL)
    new_digest = hashlib.sha256(TOOLKIT.read_bytes()).hexdigest()

    rec = {"schema": "m8_receipt_amendment.v1", "amendment_id": "author_breach_disclosure",
           "recorded_at": now,
           "raised_by": "the OW-6 stage-2 final checker (claude-fable-5-1), attempt lam_final_check_01_a1",
           "what_this_records": "breaches the transcripts show and the receipts did not, for three authors whose "
                                "output was applied to the corpus",
           "originals_rewritten": False,
           "why_not_rewritten": "e19_selfreported records what the AGENT reported. Filling it in on the agent's "
                                "behalf would erase the distinction between a breach an agent disclosed and one an "
                                "auditor found in its transcript - and that distinction is the finding.",
           "residue_check": "SP/Lam/final_check/_orchestrator_path_checks.v1.json - every alleged stray absent; "
                            "the stray sweep is CLEAN",
           "attempts": BREACHES}
    AMEND.parent.mkdir(parents=True, exist_ok=True)
    with open(AMEND, "a", encoding="utf-8", newline=NL) as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    entry = ["",
             f"## TOOLKIT ERRATUM + BREACH AMENDMENTS {datetime.now(timezone.utc).strftime('%Y-%m-%d')} (session dce0b6e2) - fix-round item 6",
             "- tools/TOOLKIT.md carried a parashah paragraph saying every verse of chs 1-4 is marked ('3:1-65",
             "  SAMEKH'). pmarks_Lam.json marks ch 3 at 22 verses only (SAMEKH every third verse 3:3..3:63, PE at",
             "  3:66) - which is what the toolkit's OWN digits (5 PE / 84 SAMEKH / 89 verses) require. The paragraph",
             "  contradicted the digits three lines above it.",
             "- an ERRATUM was appended; the wrong sentence stands beside it. A 'trust this, do not re-derive' file",
             "  that silently changes is worse than one with a visible correction: an agent that already quoted the",
             "  old text would have no way to discover it had moved.",
             f"- TOOLKIT.md new sha256 {new_digest[:16]}... (a dependency-record entry follows this line's digest).",
             "- SHIPPED IMPACT NONE: a primary and the boss each re-derived the layer from pmarks_Lam.json instead of",
             "  trusting the paragraph and corrected it inside their own work, which is what the hazard catalog asks",
             "  for and the reason this is an erratum and not a defect.",
             "- breach amendments for lam_auth_a02_a1, lam_auth_a03_a1 and lam_cwo_04_a1 appended to",
             "  final_check/receipt_amendments.v1.jsonl: each names the breach, whether the agent disclosed it and",
             "  whether residue remains (none does). The receipts are NOT rewritten - e19_selfreported records what",
             "  the agent reported, and filling it in for them would erase the difference between a disclosed breach",
             "  and one an auditor found.",
             ""]
    pre = LOG.read_bytes()
    body = pre if pre.endswith(b"\n") else pre + b"\n"
    LOG.write_bytes(body + NL.join(entry).encode("utf-8"))
    assert LOG.read_bytes().startswith(body), "log preimage not intact"

    print(json.dumps({"status": "DONE", "toolkit_erratum_appended": not already_tk,
                      "toolkit_new_sha256": new_digest,
                      "breach_amendments": len(BREACHES),
                      "amendments_file_sha16": hashlib.sha256(AMEND.read_bytes()).hexdigest()[:16],
                      "log_appended": True}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
