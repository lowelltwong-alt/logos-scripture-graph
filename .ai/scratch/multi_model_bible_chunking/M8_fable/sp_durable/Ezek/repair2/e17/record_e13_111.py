#!/usr/bin/env python3
"""Queue E13-111: the second review and #e17 landed; the three scope cuts bind; the #e16/#e17 mechanical orders, grade moves
and #e17's re-tiling are applied."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
before = Q.read_bytes()
if any(json.loads(l).get("id") == "E13-111" for l in before.decode("utf-8").splitlines() if l.strip()):
    raise SystemExit("REFUSED: E13-111 already recorded")
man = json.loads((EZ / "repair2" / "e17" / "retile_e17.manifest.json").read_text(encoding="utf-8"))
if man["postimage_sha256_measured_from_disk"] != sha(EZ / "repair" / "rows_v7_cwo24.jsonl"):
    raise SystemExit("REFUSED: the live rows are not the re-tiling's post-image")
e = {
    "id": "E13-111", "opened_at": datetime.now(timezone.utc).isoformat(), "severity": "HIGH", "tier": "MEASURED",
    "blocks_close": True, "raised_by": "orchestrator (claude-opus-5)",
    "status": "DONE for the landings and the mechanical application; the final remediation batch is OWED",
    "headline": ("The OW-6b(b) second Fable review (two blind lanes) and #e17 LANDED. #e17 ordered seven re-tilings (15 rows retired, "
                 "8 written; 145 -> 138), settled 55 grade decisions, issued 31 orders and 5 tool orders, and escalated nothing to "
                 "the owner. The merged #e16/#e17 mechanical text orders (27 on 24 rows) and 37 grade moves were applied by guarded "
                 "sweep; the re-tiling by a separately reviewed tool (retile_e17.py; the harness refuses identity fields by design)."),
    "landed": {"second_review": {"lane_a": {"attempt": "ezek_second_review_lane_a_a1", "tokens_reported": 439350},
                                 "lane_b": {"attempt": "ezek_second_review_lane_b_a1", "tokens_reported": 419686}},
               "e17": {"attempt": "ezek_controlling_agent_ruling_e17_a1", "tokens_reported": 366823,
                       "file": "Ezek/author/e17/ruling_e17.json", "sha256": sha(EZ / "author" / "e17" / "ruling_e17.json")}},
    "scope_cuts_bound": ["close-gate items 21-23 take ONE Fable check (the method-change proposer included)",
                         "the final check is scoped to rows changed, rows never touched by a review, and rows flagged",
                         "a LOW defect raised by only one step-7 reader takes one author lane plus the Fable adjudicator"],
    "scope_cuts_basis": ("the owner dismissed the scope-cut question and then set the goal 'get me to 99 percent done of ezekiel or "
                         "completed' without pausing to ask; the orchestrator took the three recommended cuts (~3.3M saved) and "
                         "stops at the 72,000,000 line if a launch would cross it (OW-22)"),
    "applied": [
        {"sweep": "repair2_final_mechanical_e16_e17", "pre": "78a092c3a2ebf27d44dea346029e3d1940578caaca609827083756ce505dfd35",
         "post": "5d55bb0850925de211fddf129bd25736119eb21c0653d7ba29b289f79988f60e", "parity": "24/24 rows"},
        {"sweep": "repair2_final_grade_moves_e16_e17", "pre": "5d55bb0850925de211fddf129bd25736119eb21c0653d7ba29b289f79988f60e",
         "post": "f5315a8ac64976e7111a87b792a672b22d2b2a10f0c96e775388547c9ba99b32", "parity": "37/37",
         "suite": "hard GREEN, triage 933 (post-image equals the candidate suite-checked before the write)"},
        {"tool": "retile_e17.py", "pre": man["preimage_sha256"], "post": man["postimage_sha256_measured_from_disk"],
         "manifest_sha256": sha(EZ / "repair2" / "e17" / "retile_e17.manifest.json"), "new_row_ids": man["new_row_ids"],
         "tiling": man["tiling"], "refs_left_out": len(man["refs_left_out_as_invalid_on_the_new_span"]),
         "suite_on_the_post_image": ("hard RED, CONFINED to the 8 new rows (measured: 21 citation-sweep problems and 1 role-token "
                                     "flag, every one on a new row; no surviving row gained a hard flag); triage 929")}],
    "found_in_the_ruling_text": ["#e17's required tokens place a samekh on the verse AFTER the mark (16:51, 17:19, 18:24, 18:27 and "
                                 "others); the mark is recorded on the verse it follows, so the citation member refuses them",
                                 "#e17's RT-7 token 'oshb:Ezek.36.12 [WARRANT-rival:far] 36.11/36.12' names the pair's later verse "
                                 ":far; the role-token member requires :near"],
    "new_rows_are_seeds": ("identity, span, grade, unit type and collection are final; the prose is a seed (the ruling's ground, "
                           "the retired rows' texts joined) that the final remediation authors rewrite whole"),
    "cost_measured": {"second_review": 859036, "e17": 366823},
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(e, ensure_ascii=False) + "\n")
after = Q.read_bytes()
assert after.startswith(before) and after.count(b"\n") == before.count(b"\n") + 1
print("E13-111 appended; queue rows:", sum(1 for l in after.decode("utf-8").splitlines() if l.strip()))
