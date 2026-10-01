#!/usr/bin/env python3
"""Land one primary-review packet (LF or OL) for Ezekiel: verify -> persist -> receipt -> layer-C note -> capture index.

Under OW-11 a primary writes its packet OUTSIDE the worktree and the authorized orchestrator lands it. The checks are
Lam's _pr_wave_verify.py checks, applied per packet at landing instead of per wave afterwards: role and cluster fields
match; rows_reviewed equals the cluster assignment exactly; exactly one item per assigned row; verdict vocabulary;
severity present iff challenge; claim and evidence non-empty; summary tallies equal recomputed counts; the normalizer
dry-run over the landed copy is byte-clean (E-01 applies to review prose too). Added for execution identity: the packet's
attempt_id and execution_id must match the launch.

A packet with form problems still LANDS (as LANDED_WITH_FORM_DEFECTS, every problem named), because it is evidence and is
dispositioned, never silently dropped. A landed packet is never replaced; a genuine re-run lands under the next execution.
The tool prints form results only and never packet content, so the orchestrator stays out of the review's substance.

Usage: _land_review_packet_ezek.py --cluster c01 --role LF|OL --attempt <aid> [--ordinal N] --src <packet outside the
       worktree> --record <agent OW-8 final message .json> --tokens N --tool-uses N --model <ordered model>
"""
import argparse
import hashlib
import json
import re
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
SP = EZ.parent
REVIEWS = EZ / "reviews"
RECEIPTS = REVIEWS / "ezek_primaries_attempt_receipts.jsonl"
NOTES = EZ / "evidence_notes"
VERDICTS = {"support", "challenge"}
SEVERITIES = {"high", "medium", "low"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def verify(doc, cid, role, assigned, aid, xid):
    probs = []
    if doc.get("role") != "primary_%s" % role:
        probs.append("role=%r" % doc.get("role"))
    if doc.get("cluster") != cid:
        probs.append("cluster=%r" % doc.get("cluster"))
    if doc.get("attempt_id") != aid:
        probs.append("attempt_id=%r, launched %s" % (doc.get("attempt_id"), aid))
    if doc.get("execution_id") != xid:
        probs.append("execution_id=%r, launched %s" % (doc.get("execution_id"), xid))
    rr = doc.get("rows_reviewed") or []
    if sorted(rr) != sorted(assigned):
        probs.append("rows_reviewed mismatch: %s" % rr)
    items = doc.get("items") or []
    item_rows = [i.get("row_id") for i in items]
    if sorted(item_rows) != sorted(assigned):
        probs.append("items rows mismatch: %s" % item_rows)
    if len(item_rows) != len(set(item_rows)):
        probs.append("duplicate item row_ids")
    sup = ch = 0
    sev = {"high": 0, "medium": 0, "low": 0}
    for i in items:
        v = i.get("verdict")
        if v not in VERDICTS:
            probs.append("%s: bad verdict %r" % (i.get("row_id"), v))
            continue
        if v == "support":
            sup += 1
            if i.get("severity") in SEVERITIES:
                probs.append("%s: severity on a support" % i.get("row_id"))
        else:
            ch += 1
            s = i.get("severity")
            if s not in SEVERITIES:
                probs.append("%s: challenge missing severity (%r)" % (i.get("row_id"), s))
            else:
                sev[s] += 1
        if not (i.get("claim") and i.get("evidence")):
            probs.append("%s: empty claim/evidence" % i.get("row_id"))
    summ = doc.get("summary") or {}
    if summ.get("supports") != sup or summ.get("challenges") != ch:
        probs.append("summary tallies %s/%s != recomputed %d/%d" % (summ.get("supports"), summ.get("challenges"), sup, ch))
    declared = {k: v for k, v in (summ.get("by_severity") or {}).items() if v}
    recomputed = {k: v for k, v in sev.items() if v}
    if declared != recomputed:
        probs.append("summary by_severity %s != recomputed %s" % (declared, recomputed))
    return probs, {"supports": sup, "challenges": ch, "by_severity": recomputed}


def resolve_ordinal(aid, record_xid, arg_ordinal):
    """(ordinal, None) or (None, reason). OW-11-k (2026-09-11): a defaulted --ordinal landed a deliverable under the wrong
    execution. The ordinal comes from the agent record's execution_id when --ordinal is omitted; disagreement, a foreign
    attempt, a malformed id, or absence of both sources is refused before anything is landed."""
    m = re.fullmatch(r"(.+)#e(\d+)", str(record_xid)) if record_xid else None
    if record_xid and (not m or m.group(1) != aid):
        return None, "the agent record names execution %r, which is not an execution of %s" % (record_xid, aid)
    rec_ord = int(m.group(2)) if m else None
    if arg_ordinal is None and rec_ord is None:
        return None, "no --ordinal given and the agent record names no execution_id; an explicit ordinal is required"
    if arg_ordinal is not None and rec_ord is not None and arg_ordinal != rec_ord:
        return None, "--ordinal %d disagrees with the agent record's execution %s; nothing landed" % (arg_ordinal, record_xid)
    return (arg_ordinal if arg_ordinal is not None else rec_ord), None


def capture_tier(carrier, transcript_bytes, orchestrator_note, authored_bytes=None):
    """OW-18: return (TIER, None) or (None, refusal). The tool MEASURES the claim instead of trusting the label.

    A record may claim EXTRACTED only when a transcript actually carried bytes; claiming it against a 0-byte or
    absent transcript is the exact half-truth OW-18 forbids, so it is refused rather than annotated. A TRANSCRIBED
    record must say so in its own note, so the weaker tier survives in the record and not only in the receipt.
    transcript_bytes is None when no transcript path was given at all.
    """
    if carrier == "extracted_from_transcript":
        if transcript_bytes is None:
            return None, ("OW-18: --capture-carrier extracted_from_transcript requires --transcript, whose byte "
                          "size is measured here; no path was given")
        if transcript_bytes <= 0:
            return None, ("OW-18: the record claims EXTRACTED but the named transcript carries %d bytes, so there "
                          "was nothing to extract from; land it as transcribed_from_notification with the weaker "
                          "tier disclosed in the record" % transcript_bytes)
        return "EXTRACTED", None
    if carrier == "transcribed_from_notification":
        if not orchestrator_note or "TRANSCRIBED" not in str(orchestrator_note):
            return None, ("OW-18: a transcribed record must carry the word TRANSCRIBED in its own "
                          "_orchestrator_note, so the weaker tier travels with the record and not only with this "
                          "receipt; the note does not")
        return "TRANSCRIBED", None
    if carrier == "extracted_from_authored_file":
        if authored_bytes is None:
            return None, ("OW-18: --capture-carrier extracted_from_authored_file requires --authored-file, "
                          "whose byte size is measured here; no path was given")
        if authored_bytes <= 0:
            return None, ("OW-18: the record claims extraction from the agent's own durable final-message "
                          "file, but that file carries %d bytes, so there was nothing to extract from"
                          % authored_bytes)
        if not orchestrator_note or "SELF-AUTHORED CARRIER" not in str(orchestrator_note):
            return None, ("OW-18: a record extracted from the agent's OWN file must carry the words "
                          "SELF-AUTHORED CARRIER in its own _orchestrator_note. The content is durable and "
                          "re-readable, so the tier is EXTRACTED rather than TRANSCRIBED; but the carrier "
                          "was written BY the agent rather than held by the runtime, so it is not "
                          "tamper-evident against the agent and OW-7 Layer A is NOT restored by it. That "
                          "distinction must travel with the record, not only with this receipt")
        return "EXTRACTED", None
    return None, "OW-18: unknown capture carrier %r" % (carrier,)


def selftest():
    aid = "ezek_primary_lf_c01_a1"
    vectors = [
        ("the ordinal is derived from the record when --ordinal is omitted", (aid, aid + "#e2", None), 2),
        ("an explicit ordinal agreeing with the record", (aid, aid + "#e2", 2), 2),
        ("REGRESSION OW-11-k: ordinal 1 against a #e2 record is refused", (aid, aid + "#e2", 1), None),
        ("no ordinal and no execution id in the record is refused", (aid, None, None), None),
        ("an explicit ordinal with a record that names no execution id", (aid, None, 1), 1),
        ("a record naming another attempt's execution is refused", (aid, "ezek_primary_ol_c01_a1#e1", None), None),
        ("a malformed execution id is refused", (aid, aid + "-e2", None), None),
    ]
    results = []
    for name, args, want in vectors:
        got, _why = resolve_ordinal(*args)
        results.append({"vector": name, "want": want, "got": got, "ok": got == want})
    failed = [r for r in results if not r["ok"]]

    # OW-18 gate vectors. The third is the regression for the defect that produced the directive: two executions
    # landed with a 0-byte transcript, and an EXTRACTED claim over one of those must be impossible to land.
    cap_vectors = [
        ("a real transcript with bytes is EXTRACTED", ("extracted_from_transcript", 893983, None), "EXTRACTED"),
        ("REGRESSION OW-18: EXTRACTED over a 0-byte transcript is refused",
         ("extracted_from_transcript", 0, None), None),
        ("EXTRACTED with no transcript path at all is refused", ("extracted_from_transcript", None, None), None),
        ("a transcribed record whose note says TRANSCRIBED is TRANSCRIBED",
         ("transcribed_from_notification", None, "PROVENANCE EXCEPTION ... TRANSCRIBED by the orchestrator"),
         "TRANSCRIBED"),
        ("a transcribed record whose note hides the tier is refused",
         ("transcribed_from_notification", None, "verbatim final message; runtime usage at landing"), None),
        ("a transcribed record with no note at all is refused", ("transcribed_from_notification", None, None), None),
        ("an unknown carrier is refused", ("read_it_somewhere", 10, "TRANSCRIBED"), None),
        ("REGRESSION OW-19: an authored-file record with bytes and its carrier disclosed is EXTRACTED",
         ("extracted_from_authored_file", None, "SELF-AUTHORED CARRIER; tier EXTRACTED", 14975),
         "EXTRACTED"),
        ("an authored-file record over a 0-byte file is refused",
         ("extracted_from_authored_file", None, "SELF-AUTHORED CARRIER", 0), None),
        ("an authored-file record with no path given is refused",
         ("extracted_from_authored_file", None, "SELF-AUTHORED CARRIER", None), None),
        ("an authored-file record that hides its self-authored carrier is refused",
         ("extracted_from_authored_file", None, "verbatim final message, EXTRACTED programmatically", 500),
         None),
    ]
    cap_results = []
    for name, args, want in cap_vectors:
        got, _why = capture_tier(*args)
        cap_results.append({"vector": name, "want": want, "got": got, "ok": got == want})
    cap_failed = [r for r in cap_results if not r["ok"]]

    print(json.dumps({"selftest": ["resolve_ordinal", "capture_tier (OW-18)"],
                      "vectors": len(results) + len(cap_results),
                      "failed": failed + cap_failed,
                      "verdict": "GREEN" if not (failed or cap_failed) else "RED"}, indent=1))
    return 1 if (failed or cap_failed) else 0


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("--cluster", required=True)
    ap.add_argument("--role", required=True, choices=["LF", "OL"])
    ap.add_argument("--attempt", required=True)
    ap.add_argument("--ordinal", type=int, default=None,
                    help="derived from the agent record's execution_id when omitted; refused when it disagrees (OW-11-k)")
    ap.add_argument("--src", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--tokens", type=int, required=True)
    ap.add_argument("--tool-uses", type=int, required=True)
    ap.add_argument("--model", required=True)
    # OW-18: how the agent's final message reached this record. Required, because a silent record asserts by its
    # identical shape that nothing changed about how it was produced.
    ap.add_argument("--capture-carrier", required=True,
                    choices=["extracted_from_transcript", "extracted_from_authored_file",
                             "transcribed_from_notification"])
    ap.add_argument("--transcript", default=None,
                    help="required with extracted_from_transcript; its byte size is MEASURED here, never trusted")
    ap.add_argument("--authored-file", default=None,
                    help="required with extracted_from_authored_file: the agent's own durable "
                         "final-message file, whose byte size is MEASURED here, never trusted")
    a = ap.parse_args()
    cid, role, aid = a.cluster, a.role, a.attempt
    rec = json.loads(Path(a.record).read_text(encoding="utf-8"))
    tpath = Path(a.transcript) if a.transcript else None
    tbytes = (tpath.stat().st_size if (tpath and tpath.is_file()) else (0 if tpath else None))
    apath = Path(a.authored_file) if a.authored_file else None
    abytes = (apath.stat().st_size if (apath and apath.is_file()) else (0 if apath else None))
    tier, tier_why = capture_tier(a.capture_carrier, tbytes, rec.get("_orchestrator_note"), abytes)
    if tier is None:
        print(json.dumps({"cluster": cid, "role": role, "verdict": "REFUSED", "why": tier_why, "actions": []},
                         ensure_ascii=False, indent=1))
        return 1
    ordinal, why = resolve_ordinal(aid, rec.get("execution_id"), a.ordinal)
    if ordinal is None:
        print(json.dumps({"cluster": cid, "role": role, "verdict": "REFUSED", "why": why, "actions": []}, ensure_ascii=False, indent=1))
        return 1
    a.ordinal = ordinal
    xid = "%s#e%d" % (aid, a.ordinal)
    out = {"cluster": cid, "role": role, "execution_id": xid, "actions": [], "form_problems": []}

    plan = json.loads((EZ / "review_clusters.json").read_text(encoding="utf-8"))
    assigned = next(c["row_ids"] for c in plan["clusters"] if c["id"] == cid)
    src = Path(a.src)
    if not src.is_file():
        out["verdict"] = "NOT_LANDED"
        out["form_problems"].append("packet absent at %s" % src)
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 1
    REVIEWS.mkdir(exist_ok=True)
    dest = REVIEWS / ("rev_%s_%s.json" % (role, cid))
    if dest.is_file():
        if sha(dest) != sha(src):
            out["verdict"] = "REFUSED"
            out["form_problems"].append("%s already landed with DIFFERENT bytes; land a re-run under the next execution" % dest.name)
            print(json.dumps(out, ensure_ascii=False, indent=1))
            return 1
        out["actions"].append("already landed with identical bytes - no-op")
    else:
        shutil.copyfile(src, dest)
        assert sha(dest) == sha(src), "persist parity failure"
        out["actions"].append("landed from outside the worktree, parity verified")

    try:
        doc = json.loads(dest.read_text(encoding="utf-8"))
        probs, tally = verify(doc, cid, role, assigned, aid, xid)
    except json.JSONDecodeError as exc:
        probs, tally = ["packet is not valid JSON: %s" % exc], {}
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    norm = subprocess.run([sys.executable, str(EZ / "tools" / "normalize_hebrew_in_json.py"), str(dest)],
                          capture_output=True, text=True, encoding="utf-8", env=env)
    try:
        n = json.loads(norm.stdout.strip().splitlines()[-1])
        if n.get("fixed", 0) or n.get("defect_count", 0):
            probs.append("normalizer: fixed=%s defects=%s" % (n.get("fixed"), n.get("defect_count")))
    except (json.JSONDecodeError, IndexError):
        probs.append("normalizer output unparseable")
    out["form_problems"] += probs
    out["tally"] = tally
    status = "LANDED" if not out["form_problems"] else "LANDED_WITH_FORM_DEFECTS"

    have = set()   # the agent record was read before landing (OW-11-k)
    if RECEIPTS.is_file():
        have = {json.loads(l).get("execution_id") for l in RECEIPTS.read_text(encoding="utf-8").splitlines() if l.strip()}
    if xid in have:
        out["actions"].append("receipt already present - not appended twice")
    else:
        receipt = {"schema": "m8_attempt_receipt.v1", "lane": "ezek_primaries", "book": "Ezek", "attempt_id": aid,
                   "execution_id": xid, "execution_of": aid, "execution_ordinal": a.ordinal,
                   "previous_execution_id": ("%s#e%d" % (aid, a.ordinal - 1)) if a.ordinal > 1 else None,
                   "retry_of": None, "agent": "primary_%s %s" % (role, cid), "parent_agent_id": "orchestrator",
                   "model": a.model,
                   "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
                   "effort": "ORDERED as launched, NOT VERIFIED", "producer": "primary reviewer (%s lens)" % role,
                   "catcher": "SP/Ezek/_land_review_packet_ezek.py (form only), then the peer and boss rounds",
                   "role_separation": "a primary never sees the other lens's packet; the landing tool never judges content",
                   "outcome": status, "recorded_at": datetime.now(timezone.utc).isoformat(),
                   "output_file": "Ezek/reviews/" + dest.name, "output_sha256": sha(dest), "deliverable_source": str(src),
                   "form_problems": out["form_problems"], "tally": tally,
                   "tokens_reported": a.tokens, "tool_uses": a.tool_uses,
                   "unresolved_uncertainty": rec.get("unresolved_uncertainty", []),
                   # the agent's own account of what it wrote and what it did not touch - the field in which an agent
                   # discloses a defect in ITSELF. It was dropped here until 2026-09-15, when one such disclosure
                   # (16 of 19 corrupted Hebrew runs, caught by the agent before return) proved to exist nowhere in SP
                   "changes_made_or_no_change_selfreported": (rec.get("changes_made_or_no_change")
                                                              or "NOT REPORTED by the agent"),
                   "e19_selfreported": rec.get("e19_selfreport") or "NOT REPORTED by the agent",
                   # OW-18: the evidence tier of the Layer A record itself, measured here rather than asserted.
                   "layer_a_capture": {
                       "carrier": a.capture_carrier, "tier": tier,
                       "transcript_path": (str(tpath) if tpath else "NONE GIVEN"),
                       "transcript_bytes": (tbytes if tbytes is not None else
                                            "UNAVAILABLE - no transcript path was given"),
                       "authored_file_path": (str(apath) if apath else "NONE GIVEN"),
                       "authored_file_bytes": (abytes if abytes is not None else
                                               "UNAVAILABLE - no authored-file path was given"),
                       "carrier_held_by": (
                           "the runtime" if a.capture_carrier == "extracted_from_transcript" else
                           "the agent itself"
                           if a.capture_carrier == "extracted_from_authored_file" else
                           "nothing durable - the orchestrator's context only"),
                       "ow7_layer_a_runtime_capture": (
                           "PRESENT - extracted from the runtime's own transcript"
                           if a.capture_carrier == "extracted_from_transcript" else
                           "UNAVAILABLE - the runtime transcript was empty or absent. This record may still "
                           "be durable, but it is SELF-AUTHORED, so it is an OW-7 Layer C artifact and does "
                           "not restore Layer A."),
                       "basis": "MEASURED by the landing tool at land time; an EXTRACTED claim over an empty or "
                                "absent transcript is refused, not annotated",
                       "law": "OW-18"}}
        with RECEIPTS.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(receipt, ensure_ascii=False) + "\n")
        out["actions"].append("receipt appended")

    NOTES.mkdir(exist_ok=True)
    note_p = NOTES / (xid.replace("#", "%23") + ".json")
    if note_p.is_file():
        out["actions"].append("evidence note already present - kept, never overwritten")
    else:
        note_p.write_text(json.dumps({"attempt_id": aid, "execution_id": xid, "sources": rec.get("sources", []),
                                      "outcome": rec.get("outcome", {}), "verification": rec.get("verification", []),
                                      "unresolved_uncertainty": rec.get("unresolved_uncertainty", []),
                                      "self_authored": True,
                                      "limit": "accountable work summary; not chain of thought and not independent proof"},
                                     ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        out["actions"].append("evidence note written")
    ci = SP / "campaign" / "_capture_index.py"
    subprocess.run([sys.executable, str(ci), "--book", "Ezek", "--write"], capture_output=True, text=True, encoding="utf-8")
    chk = subprocess.run([sys.executable, str(ci), "--check"], capture_output=True, text=True, encoding="utf-8")
    out["capture_index"] = json.loads(chk.stdout)["verdict"]
    out["verdict"] = status
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if status == "LANDED" else 2


if __name__ == "__main__":
    sys.exit(main())
