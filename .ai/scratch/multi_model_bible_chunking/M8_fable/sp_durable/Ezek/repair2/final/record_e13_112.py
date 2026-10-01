#!/usr/bin/env python3
"""Queue E13-112: the deterministic sweeps and tool orders before the final remediation; the worklist v2, gate v6; the pilot."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
F = EZ / "repair2" / "final"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
before = Q.read_bytes()
if any(json.loads(l).get("id") == "E13-112" for l in before.decode("utf-8").splitlines() if l.strip()):
    raise SystemExit("REFUSED: E13-112 already recorded")
wl = json.loads((F / "final_worklist.v2.json").read_text(encoding="utf-8"))
e = {
    "id": "E13-112", "opened_at": datetime.now(timezone.utc).isoformat(), "severity": "HIGH", "tier": "MEASURED",
    "blocks_close": True, "raised_by": "orchestrator (claude-opus-5)",
    "status": "DONE for the sweeps, tool orders and worklist; the final remediation PILOT is IN FLIGHT (slices 1-2 of 6)",
    "applied": [
        {"sweep": "repair2_final_tier_label_deletion", "pre": "e6f74aea60208af4e8b2f933fafefb6701e634a56781942cc08be0f7909c31d9",
         "post": "5cbb069167194156c409222e85ed587ba36de80c645f529e4bf7a85ba8080477", "parity": "46/46 fields on 35 rows",
         "what": "79 evidence-tier scale labels removed by seven fixed meaning-preserving rules (#e16 bars them); 22 left for the authors",
         "suite": "register 225 -> 146; every other member unchanged; post-image equals the suite-checked candidate"},
        {"sweep": "repair2_final_e17_t2_quote_recase", "pre": "5cbb069167194156c409222e85ed587ba36de80c645f529e4bf7a85ba8080477",
         "post": "03327cf4fda47bc27ace213188c221be6bc4864eb6ba917181a3ed68aac94554", "parity": "1/1",
         "what": "#e17 T-2: O-64's six quotations re-run byte for byte against verse_map_web.json 'text' without '[fn]'; five are byte-equal; one surviving difference (P10-014 refs: 'these' where the WEB reads 'These') recased"}],
    "t2_member_finding": ("check_web_quotes.py already reads 'text' through ezek_lib.norm_english, which removes '[fn]' and folds quotes, "
                          "apostrophes and dashes (case kept). A patch to strip '[fn]' was written, proved redundant by a vector "
                          "that passed without it, and reverted; the member's bytes are unchanged (8f0f2540...)."),
    "tools": {"confcal_audit_v4": {"file": "Ezek/repair2/step7/confcal_audit_v4.py", "output_sha256": sha(EZ / "repair2" / "step7" / "confcal_audit.v4.json"),
                                   "orders": "#e17 T-1 (K1 fixture replaces the extracted R-6 list) and T-5 (said-to-me interior tokens)",
                                   "result": "17 rows outside the derived range, 14 rows with a prose-weighed rival and no token, 22 said-to-me seams untokened on 15 rows"},
              "gate_v6": {"file": "Ezek/repair2/final/check_candidate_v6.py", "sha256": sha(F / "check_candidate_v6.py"),
                          "change": "v5 unchanged except claim accounting REPORTED, not enforced, on the 8 re-tiled rows (seed prose); selftest 12 + 4"},
              "t3": "done earlier (t3_low_ground_check.v1.json)", "t4": "the re-tiling's tiling check (138 rows, 1,273 verses, exact)"},
    "worklist": {"file": "Ezek/repair2/final/final_worklist.v2.json", "sha256": sha(F / "final_worklist.v2.json"), "items": len(wl["items"]),
                 "items_by_class": wl["items_by_class"], "rows_owed": wl["rows_owed"], "not_items": wl["not_items"]},
    "pilot": {"why": ("the worklist is ~2.5x the rows and ~6x the bytes of step 5 or 6 (each ~2.6M); the orchestrator launches two of six "
                      "slices first and re-forecasts from their measured cost before launching the rest (OW-22: forecasts from "
                      "measured per-step actuals; excess brought as a named scope cut)"),
              "launched": ["ezek_final_s1_lane_a_a1", "ezek_final_s1_lane_b_a1", "ezek_final_s2_lane_a_a1", "ezek_final_s2_lane_b_a1"],
              "mapped": "Ezek/_transcript_map.ezek.json (pin guard reads the rows PINNED)"},
    "budget_at_launch": {"measured_lower_bound": 60363467, "ceiling": 72000000, "headroom": 11636533},
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(e, ensure_ascii=False) + "\n")
after = Q.read_bytes()
assert after.startswith(before) and after.count(b"\n") == before.count(b"\n") + 1
print("E13-112 appended; queue rows:", sum(1 for l in after.decode("utf-8").splitlines() if l.strip()))
