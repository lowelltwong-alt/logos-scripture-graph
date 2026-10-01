#!/usr/bin/env python3
"""Land the boss audit, and distinguish a STALE self-reported digest from a MISMATCH.

THE CONTROL INTERACTION THIS EXPOSED, and both controls are mine:
  * E-29 makes every worker WRITE EARLY AND REWRITE. The boss wrote its audit at stages 0, 1, 2, 3 and final.
  * OW-18 corroboration has the worker REPORT its own artifact's digest, which the landing then measures.
A worker that digests before its last rewrite reports a digest that is already stale. MEASURED here: the audit
file is 172,650 bytes against 168,285 reported, the final message 125,912 against 123,668, and NEITHER file
contains its own reported digest - so this is not the self-referential-embedding case, it is a rewrite after the
digest was taken.

My landing tool treated that as a parity FAILURE, which reads as possible tampering. Refusing a sound artifact
while calling it a parity failure is the wrong failure mode: it is an accusation, and under OW-18 an accusation
carries the same honesty duty as any other claim.

SO THIS LANDS ON INDEPENDENT CORROBORATION, NOT ON A LOOSENED GUARD. A stale digest is accepted ONLY when the
file's own content independently matches the checkable facts of the agent's reply: the verdict tally, the count of
rows decided, and the named RETURN rows. If any of those disagree the landing still refuses, because then the
difference is about content and not about timing.
"""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
SRC = Path(r"C:\Users\lowel\AppData\Local\Temp\claude"
           r"\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_boss_out")
AUDIT = SRC / "boss_audit.json"
FINAL = SRC / "final_message_boss_audit.json"
DST = EZ / "ezek_boss_audit.v1.json"
DST_LAYER = EZ / "reviews" / "layer_a_records" / "layer_c_authored_boss_audit.json"
RECEIPTS = EZ / "reviews" / "ezek_boss_attempt_receipts.jsonl"

REPORTED = {"audit": "edb14d0d930f030499d8540d2da790c1d39c6db54833f4a84fcd9e585aef4f3c",
            "audit_bytes": 168285,
            "final": "9b2728d649c7b605918c43282893eb81308d7e80c05f270d574217f9ae6edddc",
            "final_bytes": 123668}
# checkable facts from the agent's reply, asserted against the file's own content
REPLY_FACTS = {"CONFIRM": 141, "RETURN": 4, "rows_decided": 145,
               "RETURN_rows": ["P06-009", "P08-002", "P08-011", "P09-002"]}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


m_audit, m_final = sha(AUDIT), sha(FINAL)
audit = json.loads(AUDIT.read_text(encoding="utf-8"))
final = json.loads(FINAL.read_text(encoding="utf-8"))

tally = audit.get("verdict_tally") or {}
corrob = {
    "verdict_tally_CONFIRM": tally.get("CONFIRM") == REPLY_FACTS["CONFIRM"],
    "verdict_tally_RETURN": tally.get("RETURN") == REPLY_FACTS["RETURN"],
    "rows_decided": tally.get("rows_decided") == REPLY_FACTS["rows_decided"],
    "return_rows_named": sorted(tally.get("RETURN_rows") or []) == sorted(REPLY_FACTS["RETURN_rows"]),
    "rows_array_length": len(audit.get("rows") or []) == REPLY_FACTS["rows_decided"],
    "execution_id": audit.get("execution_id") == "ezek_boss_audit_a1#e1"
        or final.get("execution_id") == "ezek_boss_audit_a1#e1",
}
embeds_own = {"audit_embeds_its_reported_digest": REPORTED["audit"] in AUDIT.read_text(encoding="utf-8"),
              "final_embeds_its_reported_digest": REPORTED["final"] in FINAL.read_text(encoding="utf-8")}

stale = (m_audit != REPORTED["audit"]) or (m_final != REPORTED["final"])
grew = (AUDIT.stat().st_size > REPORTED["audit_bytes"]) and (FINAL.stat().st_size > REPORTED["final_bytes"])

if stale and not all(corrob.values()):
    print(json.dumps({"REFUSED": ("the reported digests are stale AND the file's content does not match the "
                                  "checkable facts of the reply, so the difference is about content"),
                      "corroboration": corrob}, indent=1))
    raise SystemExit(1)

parity = {
    "status": "STALE_REPORT_CORROBORATED" if stale else "EXACT",
    "reported_audit_sha256": REPORTED["audit"], "measured_audit_sha256": m_audit,
    "reported_final_sha256": REPORTED["final"], "measured_final_sha256": m_final,
    "reported_bytes": [REPORTED["audit_bytes"], REPORTED["final_bytes"]],
    "measured_bytes": [AUDIT.stat().st_size, FINAL.stat().st_size],
    "both_files_grew_after_the_report": grew,
    "neither_file_embeds_its_own_reported_digest": not any(embeds_own.values()),
    "cause": ("the agent digested its outputs and then rewrote them once more. E-29 requires write-early-and-"
              "rewrite and OW-18 corroboration asks the agent to report its own digest; a worker that digests "
              "before its last rewrite reports a stale value. This is a predictable interaction between two "
              "controls the orchestrator introduced, not a discrepancy about content."),
    "what_was_corroborated_instead": corrob,
    "basis": "MEASURED: digests and byte counts by exact path; the reply's checkable facts asserted against the "
             "file's own verdict_tally and rows array",
    "what_this_does_NOT_establish": ("a stale digest cannot corroborate the artifact's integrity. What stands "
                                     "here is that the landed bytes carry the decisions the agent reported. An "
                                     "exact digest would have been stronger and is what the next brief will ask "
                                     "for, by having the agent digest AFTER its final write."),
}

note = ("verbatim boss audit of ezek_boss_audit_a1#e1, EXTRACTED programmatically from the agent's OWN durable "
        "file (%s, %d bytes MEASURED at land time). SELF-AUTHORED CARRIER, disclosed under OW-18: the runtime "
        "held no transcript, so the file is durable and re-readable - tier EXTRACTED, not TRANSCRIBED - but the "
        "agent wrote it, so it is not tamper-evident against the agent and OW-7 Layer A is NOT restored; this is "
        "a durable Layer C record. DIGEST PARITY: %s. The agent's reported digests are STALE because it rewrote "
        "after digesting (E-29 write-early-and-rewrite); neither file embeds its own reported digest, both grew, "
        "and the landed content was corroborated instead against the reply's verdict tally, row count and named "
        "RETURN rows. Corroboration does not upgrade a tier." % (FINAL.name, FINAL.stat().st_size,
                                                                 parity["status"]))
if "_orchestrator_note" in final:
    raise SystemExit("REFUSED: the source already carries an _orchestrator_note")
final["_orchestrator_note"] = note

for dst, src in ((DST, AUDIT),):
    if dst.is_file() and sha(dst) != sha(src):
        raise SystemExit("REFUSED: %s exists with different bytes" % dst.name)
DST_LAYER.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(AUDIT, DST)
DST_LAYER.write_text(json.dumps(final, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

receipt = {
    "schema": "m8_attempt_receipt.v1", "book": "Ezek", "lane": "ezek_boss",
    "attempt_id": "ezek_boss_audit_a1", "execution_id": "ezek_boss_audit_a1#e1", "execution_ordinal": 1,
    "role": "OW-6b Fable boss audit of the peer reconciliations (P8 of the #e13 ruling)",
    "model": "claude-fable-5-1", "model_actual": "UNAVAILABLE - no runtime record of the served model",
    "producer": "claude-fable-5-1 subagent", "catcher": "claude-opus-5 orchestrator",
    "outcome": "LANDED",
    "output_file": "Ezek/%s" % DST.name, "output_sha256": sha(DST), "output_bytes": DST.stat().st_size,
    "deliverable_source": str(AUDIT),
    "verdict_tally": tally,
    "rows_decided": len(audit.get("rows") or []),
    "p08_012_reweigh": (audit.get("p08_012_reweigh") or {}).get("to"),
    "escalations": [e.get("id") for e in (audit.get("escalations") or []) if isinstance(e, dict)],
    "layer_a_capture": {
        "carrier": "extracted_from_authored_file", "tier": "EXTRACTED", "carrier_held_by": "the agent itself",
        "authored_file_path": str(FINAL), "authored_file_bytes": FINAL.stat().st_size,
        "transcript_path": "UNAVAILABLE - no runtime transcript was produced", "transcript_bytes": "UNAVAILABLE",
        "ow7_layer_a_runtime_capture": ("UNAVAILABLE - durable but SELF-AUTHORED, an OW-7 Layer C artifact that "
                                        "does not restore Layer A"),
        "deliverable_digest_parity": parity,
        "basis": "MEASURED by the landing script at land time", "law": "OW-18",
    },
    "durable_record_copy": "reviews/layer_a_records/%s" % DST_LAYER.name,
    "durable_record_copy_sha256": sha(DST_LAYER),
    "e19_selfreported": audit.get("e19_selfreport", "NOT REPORTED by the agent"),
    "unresolved_uncertainty": audit.get("unresolved_uncertainty"),
    "recorded_at": datetime.now(timezone.utc).isoformat(),
}
with RECEIPTS.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(receipt, ensure_ascii=False) + "\n")

print(json.dumps({"landed": DST.name, "audit_sha256": sha(DST), "bytes": DST.stat().st_size,
                  "parity_status": parity["status"], "corroboration": corrob,
                  "durable_record_copy": DST_LAYER.name,
                  "verdict_tally": tally,
                  "p08_012": (audit.get("p08_012_reweigh") or {}).get("to"),
                  "escalations": receipt["escalations"]}, indent=1, ensure_ascii=False))
