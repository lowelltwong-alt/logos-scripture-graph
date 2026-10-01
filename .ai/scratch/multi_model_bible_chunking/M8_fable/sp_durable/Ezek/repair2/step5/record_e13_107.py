#!/usr/bin/env python3
"""Queue E13-107: REPAIR-2 step 5 landed; two suite members widened after it; what they newly found goes to step 6."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
before = Q.read_bytes()
if any(json.loads(l).get("id") == "E13-107" for l in before.decode("utf-8").splitlines() if l.strip()):
    raise SystemExit("REFUSED: E13-107 already recorded")
if sha(EZ / "repair" / "rows_v7_cwo24.jsonl") != "a2e51d689bcb8e656ece9e657521407facf5eeecd67cbf06d4214ef2e8dd601f":
    raise SystemExit("REFUSED: rows are not at the step-5 post-image")
routed = {h: json.loads((EZ / "author" / "repair2_step5" / ("h%d_adjudication" % h) / "adjudication.json").read_text(encoding="utf-8")).get("routed")
          for h in (1, 2)}
e = {
    "id": "E13-107", "opened_at": datetime.now(timezone.utc).isoformat(), "severity": "HIGH", "tier": "MEASURED",
    "blocks_close": True, "raised_by": "orchestrator (claude-opus-5)",
    "status": "DONE for step 5; the routed repairs and the members' new findings are OWED in step 6",
    "headline": ("REPAIR-2 STEP 5 LANDED: four blind Opus lanes (two per half) and two Fable adjudications; 58 prose "
                 "edits on 45 rows, rows 2d7160f7 -> a2e51d68; register flags 90 -> 0, web_quotes 36 -> 13, triage "
                 "810 -> 700, no hard member gained a flag. Then TWO SUITE MEMBERS WERE WIDENED: the register checker's "
                 "selftest had SANCTIONED referents #e15 Q9(a) bars ('this extract', 'the inventory'), and the universals "
                 "member read a clause 6 v2 seam pair as an N/N count and silently dropped the claims beside it. The "
                 "widened members find 43 register flags on 29 rows and 8 more universals claims; all are owed in step 6."),
    "step_5": {
        "lanes": {"h1_a": "45 discharged, 15 no-defect, 1 stop", "h1_b": "45 discharged, 14 no-defect, 2 stops",
                  "h2_a": "58 discharged, 14 no-defect, 1 stop", "h2_b": "60 discharged, 12 no-defect, 1 stop"},
        "adjudications": {"h1": "46 discharged, 13 no-defect, 2 stops; 8 fields from A, 7 from B, 4 reconciled, 10 identical; 11 routed",
                          "h2": "60 discharged, 12 no-defect, 1 stop; 17 fields from A, 4 from B, 1 reconciled, 7 identical; 16 routed"},
        "claims": "every anchor removed was accounted for, by every lane and both adjudicators (gate v5 claim arm; 0 unaccounted)",
        "merge": {"file": "Ezek/author/repair2_step5/merged/proposal.json", "sha256": sha(EZ / "author" / "repair2_step5" / "merged" / "proposal.json"),
                  "rows": 45, "fields": 58, "halves_disjoint": True},
        "orchestrator_checks": ["digests of every deliverable match the agents' reports",
                                "gate v5 re-run by the orchestrator on every lane, each adjudication and the merge: all ALL_CLEAN, hard GREEN",
                                "the merge's gate candidate equals the harness's planned post-image (a2e51d68)",
                                "apply 58/58, protected fields unchanged, no row outside the proposal changed",
                                "suite delta against the post-4c report: NO HARD MEMBER GAINED A FLAG"],
        "routed": routed,
    },
    "member_fixes": {
        "script": "Ezek/repair2/step5/patch_members_after_step5.py (exact-once anchors, backups, selftests or restore)",
        "check_register.py": {"before": "5106d1be66f3c7c860f98589b46ba52a5d5900cdb41251b54dd7021a7c06462d", "after": sha(EZ / "tools" / "check_register.py"),
                              "what": "arm (iii) gains extract, inventory, census, worklist, disclosure layer, N-list labels, the operative category/classification label; the two wrong GREEN vectors became FIRE vectors; witness-naming forms are the GREEN vectors",
                              "found_by": "step-5 half-2 lane B; routed by the half-2 adjudicator (R-05)"},
        "check_universals.py": {"before": "198e0c4cd20ca495b4e33a3df639b9e1e61320286a88db870ff5797a640dc341", "after": sha(EZ / "tools" / "check_universals.py"),
                                "what": "seam pairs masked before the sweep arm; --selftest added with a hide case and a still-sourced case",
                                "found_by": "step-4c lane A's triage-delta reading; routed by the step-4c adjudicator"},
        "effect_on_the_live_rows": {"register": "0 -> 43 flags on 29 rows (extract 12, N-list labels 17, operative-category/classification 6, inventory 5)",
                                    "universals": "683 -> 691", "triage_total": "700 -> 751", "hard_status": "GREEN"},
    },
    "the_lesson": ("E-40 one layer down: the ruling barred a referent class, the brief was corrected in step 5, and the checker's own "
                   "selftest still asserted the barred phrases were fine - so a GREEN register report after step 5 would have been "
                   "the tool's older sanction, not the rule. The sibling audit (E-36 addendum) is what turned 0 into 43."),
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(e, ensure_ascii=False) + "\n")
after = Q.read_bytes()
assert after.startswith(before) and after.count(b"\n") == before.count(b"\n") + 1
print("E13-107 appended; queue rows:", sum(1 for l in after.decode("utf-8").splitlines() if l.strip()))
