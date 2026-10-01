#!/usr/bin/env python3
"""OW-15 census, v2: first append full-digest amendments for five late receipts, then restate the position.

TWO CORRECTIONS THIS CARRIES.
(1) The late receipts for author lanes 01 and 04 and spot lanes 1-3 carried 12- or 16-character digest PREFIXES in a
    field named deliverable_sha256. Lanes 01 and 04 were paired to their digests by the ORDER of a sorted printout; the
    queue's own E13-71 maps them explicitly (lane_01 -> 34ed205e..., lane_04 -> 2378ecf9...), and the pairing proved
    right - by luck of order, not by reading. The amendments below write the FULL digests, each read from its source:
    the queue entry for the author lanes, the file on disk for the spot lanes.
(2) The v1 census counted an attempt whose receipt says UNAVAILABLE as unmeasured even when an amendment later supplied
    its FULL runtime figure. v2 resolves such an attempt to MEASURED; an amendment whose note says it covers a SEGMENT
    still leaves the attempt partial.

WHAT NO CENSUS OVER RECEIPTS CAN SEE: an attempt that produced no receipt at all. Ten such attempts were found on
2026-09-16 only by reading the runtime's notifications in the session transcript. The census states that limit, and
names the transcript read as the cross-check that caught it.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
EZ = SP / "Ezek"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

q = {x["id"]: x for x in (json.loads(l) for l in (EZ / "ezek_controlling_agent_queue_e13.v1.jsonl")
                          .read_text(encoding="utf-8").splitlines() if l.strip())}
FULL = {
    ("author/ezek_author_wave_attempt_receipts.jsonl", "ezek_author_wave_lane_01_a1#e1"):
        (q["E13-71"]["lane_01"]["deliverable_sha256"], "queue E13-71 lane_01.deliverable_sha256"),
    ("author/ezek_author_wave_attempt_receipts.jsonl", "ezek_author_wave_lane_04_a1#e1"):
        (q["E13-71"]["lane_04"]["deliverable_sha256"], "queue E13-71 lane_04.deliverable_sha256"),
    ("reviews/spot/ezek_spot_attempt_receipts.jsonl", "ezek_spot_s01_a1#e1"):
        (sha(EZ / "reviews" / "spot" / "ezek_spot_s01_findings.json"), "sha256 of reviews/spot/ezek_spot_s01_findings.json on disk"),
    ("reviews/spot/ezek_spot_attempt_receipts.jsonl", "ezek_spot_s02_a1#e1"):
        (sha(EZ / "reviews" / "spot" / "ezek_spot_s02_findings.json"), "sha256 of reviews/spot/ezek_spot_s02_findings.json on disk"),
    ("reviews/spot/ezek_spot_attempt_receipts.jsonl", "ezek_spot_s03_a1#e1"):
        (sha(EZ / "reviews" / "spot" / "ezek_spot_s03_findings.json"), "sha256 of reviews/spot/ezek_spot_s03_findings.json on disk"),
}
for (rel, ex), (full, src) in FULL.items():
    p = EZ / rel
    rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    orig = next((r for r in rows if r.get("execution_id") == ex), None)
    if orig is None:
        raise SystemExit("REFUSED: no receipt %s" % ex)
    if any(r.get("amends_execution_id") == ex and r.get("deliverable_sha256") == full for r in rows):
        continue
    if not full.startswith(str(orig.get("deliverable_sha256"))):
        raise SystemExit("REFUSED: the full digest for %s does not extend the prefix the receipt carries" % ex)
    pre = p.read_bytes()
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"schema": "m8_attempt_receipt_amendment.v1", "amends_schema": "m8_attempt_receipt.v1",
                             "amends_execution_id": ex, "book": "Ezek", "recorded_at": NOW,
                             "recorded_by": "orchestrator (claude-opus-5), session 910cbe15",
                             "original_line_unedited": True, "deliverable_sha256": full, "digest_source": src,
                             "why": "the original late receipt carried a digest PREFIX in a sha256 field",
                             "how_to_read": "a consumer resolves amendments: the full digest is the one given here"},
                            ensure_ascii=False) + "\n")
    if not p.read_bytes().startswith(pre):
        raise SystemExit("INTEGRITY FAILURE on %s" % rel)

carrier = json.loads((SP / "campaign" / "budget_ceilings.v1.json").read_text(encoding="utf-8"))
ceiling = carrier["books"]["Ezek"]["ceiling"]

# REGRESSION RESTORED: v1 resolved amendments that DECLARE a figure UNAVAILABLE (the two phase-0 attempts). My first v2
# resolved only amendments carrying an integer, so it reported two declared attempts as UNDECLARED.
amend_tokens, amend_partial, amend_declared = {}, set(), set()
receipt_files = sorted(p for p in EZ.rglob("*_attempt_receipts.jsonl") if ".pre_" not in p.name)
for p in receipt_files:
    for l in p.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        r = json.loads(l)
        if str(r.get("schema", "")).endswith("_amendment.v1") and isinstance(r.get("tokens_reported"), str)                 and "UNAVAILABLE" in r["tokens_reported"].upper():
            amend_declared.add(r.get("amends_execution_id"))
        if str(r.get("schema", "")).endswith("_amendment.v1") and isinstance(r.get("tokens_reported"), int):
            ex = r.get("amends_execution_id")
            amend_tokens[ex] = amend_tokens.get(ex, 0) + r["tokens_reported"]
            if "SEGMENT" in str(r.get("token_note", "")).upper() and "NOT A SEGMENT" not in str(r.get("token_note", "")).upper():
                amend_partial.add(ex)

total, measured, partial, declared, undeclared, attempts = 0, 0, [], [], [], 0
for p in receipt_files:
    for l in p.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        r = json.loads(l)
        if str(r.get("schema", "")).endswith("_amendment.v1"):
            continue
        attempts += 1
        ex, v = r.get("execution_id"), r.get("tokens_reported")
        if isinstance(v, int):
            total += v
            measured += 1
            continue
        if ex in amend_tokens:
            total += amend_tokens[ex]
            if ex in amend_partial:
                partial.append(ex)
            else:
                measured += 1
            continue
        if ex in amend_declared:
            declared.append(ex)
            continue
        note = str(v) + " " + str(r.get("token_note", ""))
        (declared if "UNAVAILABLE" in note.upper() or "no token count is recorded" in note else undeclared).append(ex)

out = {
    "schema": "ezek_ow15_position.v2", "restated_at": NOW,
    "ceiling": {"value": ceiling, "carrier": "sp_durable/campaign/budget_ceilings.v1.json",
                "carrier_sha256": sha(SP / "campaign" / "budget_ceilings.v1.json")},
    "census": {"LOWER_BOUND": total, "attempt_receipts": attempts, "measured_in_full": measured,
               "measured_only_in_part": partial, "unmeasured_declared": declared, "unmeasured_UNDECLARED": undeclared,
               "receipt_files": len(receipt_files)},
    "headroom": {"UPPER_BOUND": ceiling - total},
    "what_changed_since_v1": ("v1 stood at 39,426,659. Ten attempts had NO receipt (author-wave lanes 01-06, the "
                              "remediation batch, spot lanes 1-3: 3,476,769 tokens) and four receipts declared "
                              "UNAVAILABLE a figure the runtime had reported (#e12 502,905, #e13 365,746, #e14 221,050, "
                              "boss audit 847,447). Both were recovered from the runtime's completion notifications "
                              "in the session transcript, and the two REPAIR-2 step-2 lanes were receipted."),
    "limit": ("a census over receipts cannot see an attempt that produced none. The cross-check that found ten is the "
              "runtime's own notification log; it should be read at every book close, and the in-flight adjudication "
              "launched 2026-09-16 is not yet in any figure here."),
    "tier": "MEASURED for every figure present; attributions of runtime figures to attempts INFERRED as each receipt states",
}
(EZ / "ezek_ow15_position.v2.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8",
                                               newline="\n")
print(json.dumps({k: out[k] for k in ("ceiling", "census", "headroom")}, ensure_ascii=False, indent=1))
