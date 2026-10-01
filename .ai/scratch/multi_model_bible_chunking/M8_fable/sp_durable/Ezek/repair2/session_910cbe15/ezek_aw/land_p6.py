#!/usr/bin/env python3
"""Land P6: the device inventory's next version and its derivation record, with digest parity measured.

THE BRIEF CARRIED A WRONG FIGURE-SET AND THE AGENT CAUGHT IT. My brief said "D1 - a note at MT 1:3 explaining
the word-event label set (the 49 / 41 / 48 figures: strict vayehi-adjacent, vayehi-any including infixed date,
hayah-perfect)". That mapping does not reproduce: MEASURED, strict is 39 and hayah-perfect is 7, while 49 / 41 /
48 are three of the FIVE figures in the family (any_form 49, vayehi_any 41, family_total 48). I took #e12's
label string "D1 word-event 49/41/48 labels" and glossed it as the three sub-labels, which it is not. The agent
re-derived rather than fitting its measurement to my gloss - which is the behaviour the brief asked for and the
opposite of what a compliant agent would have done.

ITS OWN SELF-DISCLOSED DEFECT IS THE MORE VALUABLE FINDING: its first hand-of-YHWH predicate returned 5 by
matching bare יד and dropping ויד, and BOTH OF ITS DERIVATIONS AGREED AT THE WRONG ANSWER. Two derivations by
one agent are not two lenses (OW-19); they share the agent's misreading of the predicate. What caught it was
comparing every class against the v1 list verse for verse - an external reference, not a second internal pass.
"""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
SRC = Path(r"C:\Users\lowel\AppData\Local\Temp\claude"
           r"\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_p6_work_a1_7f3c")
INV = SRC / "ezek_device_inventory.v2.json"
REC = SRC / "p6_derivation_record.json"
REPORTED = {"inv": "356ba38093e7621bc0ef046fc33e9b07e015bc0082457f5f043b5b492480561f",
            "inv_bytes": 74550,
            "rec": "14cd1ef0f7493d56c845549b782f87bcc52dc730b6e3bed5796f531273291905",
            "rec_bytes": 41946}
DST_INV = EZ / "ezek_device_inventory.v2.json"
DST_REC = EZ / "p6_derivation_record.v1.json"
RECEIPTS = EZ / "ezek_phase0_attempt_receipts.jsonl"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

m_inv, m_rec = sha(INV), sha(REC)
parity = {
    "status": "EXACT" if (m_inv == REPORTED["inv"] and m_rec == REPORTED["rec"]) else "MISMATCH",
    "inventory": {"reported": REPORTED["inv"], "measured": m_inv, "equal": m_inv == REPORTED["inv"],
                  "bytes_reported": REPORTED["inv_bytes"], "bytes_measured": INV.stat().st_size},
    "record": {"reported": REPORTED["rec"], "measured": m_rec, "equal": m_rec == REPORTED["rec"],
               "bytes_reported": REPORTED["rec_bytes"], "bytes_measured": REC.stat().st_size},
    "why_exact_this_time": ("the brief told the agent to digest AFTER its final write. The boss audit's "
                            "digests were STALE because E-29's write-early-and-rewrite discipline collides "
                            "with self-reported digests when the agent digests before its last rewrite. This "
                            "is the second consecutive landing with exact parity since the brief changed."),
}
if parity["status"] != "EXACT":
    raise SystemExit("REFUSED: digest parity failed:\n" + json.dumps(parity, indent=1))

# the v1 inventory must be UNTOUCHED - the next version never overwrites its predecessor
V1 = EZ / "ezek_device_inventory.json"
v1_sha = sha(V1)
if v1_sha != "0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142":
    raise SystemExit("REFUSED: the v1 inventory moved; it is pinned by every artifact that cites it")

for dst, src in ((DST_INV, INV), (DST_REC, REC)):
    if dst.is_file() and sha(dst) != sha(src):
        raise SystemExit("REFUSED: %s exists with different bytes" % dst.name)
    shutil.copy2(src, dst)

rec = json.loads(DST_REC.read_text(encoding="utf-8"))
receipt = {
    "schema": "m8_attempt_receipt.v1", "book": "Ezek", "lane": "ezek_p6_inventory",
    "attempt_id": "ezek_p6_inventory_a1", "execution_id": "ezek_p6_inventory_a1#e1", "execution_ordinal": 1,
    "role": "P6 of ruling #e13: the device inventory's next version, distinct-checked",
    "model": "claude-opus-5", "model_actual": "UNAVAILABLE - no runtime record of the served model",
    "producer": "claude-opus-5 subagent", "catcher": "claude-opus-5 orchestrator",
    "outcome": "LANDED",
    "output_file": "Ezek/%s" % DST_INV.name, "output_sha256": sha(DST_INV),
    "output_bytes": DST_INV.stat().st_size,
    "derivation_record": "Ezek/%s" % DST_REC.name, "derivation_record_sha256": sha(DST_REC),
    "predecessor_untouched": {"file": "Ezek/ezek_device_inventory.json", "sha256": v1_sha},
    "tokens_reported": 245535,
    "tool_uses_reported": 58,
    "duration_ms_reported": 1654063,
    "tokens_basis": "REPORTED by the runtime in the task notification, not self-reported by the agent",
    "layer_a_capture": {
        "carrier": "extracted_from_authored_file", "tier": "EXTRACTED", "carrier_held_by": "the agent itself",
        "authored_file_path": str(REC), "authored_file_bytes": REC.stat().st_size,
        "transcript_path": "UNAVAILABLE - no runtime transcript was read (reading it would overflow the "
                           "orchestrator's context and the runtime's own note forbids it)",
        "ow7_layer_a_runtime_capture": ("UNAVAILABLE - durable but SELF-AUTHORED, an OW-7 Layer C artifact "
                                        "that does not restore Layer A"),
        "deliverable_digest_parity": parity,
        "basis": "MEASURED by the landing script at land time", "law": "OW-18",
    },
    "distinct_check_shape": ("every class double- or triple-derived by the agent AND compared against the v1 "
                             "list verse for verse. The agent disclosed that on one class BOTH of its "
                             "derivations agreed at the WRONG answer (hand-of-YHWH, 5 for 7, dropping ויד) and "
                             "that only the v1 comparison caught it - so the external reference, not the "
                             "second internal pass, was the effective check. Two derivations by one agent are "
                             "not two lenses (OW-19)."),
    "findings_routed_upward": rec.get("findings_routed_upward_not_resolved")
                              or "see p6_derivation_record.v1.json",
    "e19_selfreported": rec.get("e19_selfreport", "NOT REPORTED"),
    "unresolved_uncertainty": rec.get("unresolved_uncertainty"),
    "recorded_at": NOW,
}
with RECEIPTS.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(receipt, ensure_ascii=False) + "\n")

print(json.dumps({"landed": [DST_INV.name, DST_REC.name],
                  "inventory_sha256": sha(DST_INV), "record_sha256": sha(DST_REC),
                  "parity": parity["status"],
                  "v1_untouched": True,
                  "tokens_reported": 245535,
                  "receipt_rows": len(RECEIPTS.read_text(encoding="utf-8").strip().splitlines())},
                 indent=1, ensure_ascii=False))
