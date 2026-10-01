#!/usr/bin/env python3
"""Add append-only challenge and appeal records to each held B01 packet."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
BOOKS = ["Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]

def main() -> int:
    for book in BOOKS:
        run_id = f"{book.lower()}-r8-held-1"
        root = MODEL / "state/r8" / book / run_id
        ledger = root / "challenge_appeal_ledger"
        ledger.mkdir(parents=True, exist_ok=True)
        common = {"schema_version":"whole_bible_b01_challenge_appeal.v1", "book":book, "run_id":run_id, "stage_attempt_id":"b01-controller-1", "candidate_only":True, "non_authorizing":True, "identity":{"execution_id":f"exec-{book.lower()}-redteam", "assignment_id":f"asg-{book.lower()}-redteam", "agent_instance_id":f"codex-{book.lower()}-redteam", "role_id":"exploit_red_team", "provider_family":"codex-gpt5-correlated-local"}, "controller_event_ids":[f"evt-{book.lower()}-redteam"]}
        challenge = {**common, "kind":"challenge", "entry_id":f"{book}-CH-001", "reason_code":"QF-CORRELATED-SUBSTRATE", "target_artifact_id":"role-reports", "argument":"All four reports share one Codex substrate; agreement is not an independent-provider vote.", "status":"open", "resolution_route":"retain dissent for external-provider or human review"}
        appeal = {**common, "kind":"appeal", "entry_id":f"{book}-AP-001", "reason_code":"QF-ANCIENT-CONTEXT-GAP", "target_artifact_id":"ancient-context-role", "argument":"No qualified ancient corpus is active; remembered context must remain unasserted.", "status":"deferred_to_human", "resolution_route":"human or separately qualified corpus review"}
        (ledger / f"{book}-challenge.json").write_text(json.dumps(challenge, sort_keys=True, separators=(",", ":")), encoding="utf-8")
        (ledger / f"{book}-appeal.json").write_text(json.dumps(appeal, sort_keys=True, separators=(",", ":")), encoding="utf-8")
    print({"books": len(BOOKS), "ledgers": "challenge_and_appeal"})
    return 0

if __name__ == "__main__": raise SystemExit(main())
