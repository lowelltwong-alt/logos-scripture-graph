#!/usr/bin/env python3
"""Close the last two undeclared token blanks in Ezekiel's receipts, by AMENDMENT and never by edit.

WHY AMENDMENT AND NOT EDIT. Two phase-0 attempt receipts carry no tokens_reported field at all - the only
undeclared blanks left in the book's budget column. OW-18 says UNAVAILABLE is a VALUE, never a blank, because an
absent field in a summed column asserts zero. But those two rows were written by an earlier lane and their bytes
are not mine to rewrite; and a landed receipt is a record of what was recorded, not a draft. The campaign
already has the right instrument for this - schema m8_attempt_receipt_amendment.v1, which the receipts' own
how_to_read describes: "a consumer of these receipts resolves amendments". So the declaration is APPENDED,
addressed to one exact execution_id, and the original line stays untouched and is said to stay untouched.

WHAT IS AND IS NOT CLAIMED. That the field is absent is MEASURED - this script reads the row and asserts it.
WHY it is absent is INFERRED: the phase-0 landing script predates the per-attempt token column that later lanes
carry, which is visible in the row's own key set. No figure is estimated, reconstructed or inferred from
anything. The amendment's whole content is that the cost is UNAVAILABLE and why, so that a census counts the
attempt as UNKNOWN rather than as zero.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
P = EZ / "ezek_phase0_attempt_receipts.jsonl"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731

TARGETS = {"ezek_stage_p0_a1#e1": "ezek_phase0_staging",
           "ezek_toolkit_a1#e1": "ezek_phase0_toolkit"}

pre_bytes = P.read_bytes()
pre = sha(pre_bytes)
rows = [json.loads(l) for l in pre_bytes.decode("utf-8").splitlines() if l.strip()]
by_exec = {r.get("execution_id"): r for r in rows}

# THE EXPECTED-BEFORE CHECK: each target must exist, must be an attempt receipt, must have NO token field, and
# must not already carry a declaration. Anything else and nothing is written.
problems = []
for ex in TARGETS:
    r = by_exec.get(ex)
    if r is None:
        problems.append((ex, "no row with this execution_id"))
        continue
    if "tokens_reported" in r:
        problems.append((ex, "the row already carries tokens_reported=%r" % (r.get("tokens_reported"),)))
    if r.get("token_note"):
        problems.append((ex, "the row already carries a token_note"))
already = [r.get("amends_execution_id") for r in rows
           if str(r.get("schema", "")).endswith("_amendment.v1")]
for ex in TARGETS:
    if ex in already:
        problems.append((ex, "an amendment for this execution already exists"))
if problems:
    print(json.dumps({"REFUSED": problems}, indent=1))
    raise SystemExit("nothing written")

amendments = []
for ex, lane in TARGETS.items():
    r = by_exec[ex]
    amendments.append({
        "schema": "m8_attempt_receipt_amendment.v1",
        "amends_schema": "m8_attempt_receipt.v1",
        "amends_execution_id": ex,
        "amends_attempt_id": r.get("attempt_id"),
        "book": "Ezek",
        "lane": lane,
        "recorded_at": NOW,
        "recorded_by": "orchestrator (claude-opus-5), session 910cbe15",
        "original_line_unedited": True,
        "what_this_amendment_adds": "tokens_reported, as an explicit UNAVAILABLE value",
        "tokens_reported": ("UNAVAILABLE - this phase-0 receipt carries no token field at all. Written as a "
                            "VALUE under OW-18 rather than left absent, because an absent field in a summed "
                            "column asserts zero. A census counts this attempt as UNKNOWN and reports its "
                            "total as a LOWER BOUND."),
        "token_note": ("no figure is estimated or reconstructed. That the field is absent is MEASURED by the "
                       "script that wrote this amendment; WHY it is absent is INFERRED - the phase-0 landing "
                       "script predates the per-attempt token column later lanes carry, which is visible in "
                       "this row's own key set."),
        "tier": "MEASURED that the field is absent; INFERRED as to the cause; the cost itself is UNAVAILABLE",
        "why": ("OW-18 forbids a blank where a value belongs, and this was the last undeclared blank in "
                "Ezekiel's budget column. Closing it by amendment leaves the landed record intact."),
        "how_to_read": ("a consumer of these receipts resolves amendments: this execution's effective token "
                        "figure is UNAVAILABLE, declared, and must not be summed as zero"),
    })

with P.open("a", encoding="utf-8", newline="\n") as fh:
    for a in amendments:
        fh.write(json.dumps(a, ensure_ascii=False) + "\n")

post_bytes = P.read_bytes()
post = sha(post_bytes)
post_rows = [json.loads(l) for l in post_bytes.decode("utf-8").splitlines() if l.strip()]
assert post_bytes.startswith(pre_bytes), "the landed bytes must be a PREFIX of the file after an append"
assert len(post_rows) == len(rows) + len(amendments), "row count moved by something other than the append"
print(json.dumps({"file": P.name,
                  "preimage_sha256": pre, "postimage_sha256_measured_from_disk": post,
                  "rows_before": len(rows), "rows_after": len(post_rows),
                  "appended": [a["amends_execution_id"] for a in amendments],
                  "landed_bytes_unchanged": True,
                  "verified": "the pre-image is a byte prefix of the post-image, so no existing line moved"},
                 indent=1))
