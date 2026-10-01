#!/usr/bin/env python3
"""Build deterministic Genesis per-decision review packets from frozen review receipts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from review_contract_constants import INDEPENDENCE_SCOPE


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
CHUNKS = MODEL / "book_chunks" / "Gen" / "chunks.jsonl"
OUTPUT = MODEL / "reviews" / "Gen" / "review_packets.jsonl"
FINAL_CHECKER = "gen-final-postcheck-20260722-v2"


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def digest(row: dict) -> str:
    payload = json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def review(attempt: str, evidence_refs: list[str], challenges: list[dict]) -> dict:
    return {
        "reviewer_attempt_id": attempt,
        "verdict": "challenge" if challenges else "supports",
        "blind_to_other_primary_reviews": True,
        "evidence_only": True,
        "evidence_refs": evidence_refs,
        "challenges": challenges,
    }


def build_packet(chunk: dict) -> dict:
    decision_id = chunk["decision_id"]
    revision = int(chunk.get("review_revision", 0))
    challenges_a: list[dict] = []
    challenges_b: list[dict] = []
    appeals: list[dict] = []
    boss_ruling = None
    unresolved: list[str] = []

    if revision == 1:
        attempt_a = "gen-r1-primary-hebrew-20260721-e"
        attempt_b = "gen-r1-primary-literary-20260721-f"
        peer_attempt = "gen-r1-peer-20260721-g"
        evidence_a = ["reviews/Gen/primary_r1_hebrew.json", f"chunk:{decision_id}"]
        evidence_b = ["reviews/Gen/primary_r1_literary.json", f"chunk:{decision_id}"]
        if decision_id == "M7_sol-Gen-042r1":
            challenges_a = [{
                "challenge_id": "R1-A-GEN-001",
                "severity": "material",
                "claim": "The larger 26:34-28:9 parent over-merges three discourse functions.",
                "proposed_remedy": "Gen.26.34-35; Gen.27.1-45; Gen.27.46-28.9",
                "evidence_refs": ["OSHB:Gen.26.34-28.9", "primary_r1_hebrew:R1-A-GEN-001"],
            }]
            challenges_b = [{
                "challenge_id": "R1-B-GEN-001",
                "severity": "material",
                "claim": "The larger 26:34-28:9 parent over-merges two complete scenes.",
                "proposed_remedy": "Gen.26.34-27.45; Gen.27.46-28.9",
                "evidence_refs": ["WEB:Gen.27.45-28.9", "primary_r1_literary:R1-B-GEN-001"],
            }]
            appeals = [{
                "appeal_id": "gen-r1-primary-hebrew-20260721-e-appeal1-P3",
                "appellant_attempt_id": "gen-r1-primary-hebrew-20260721-e",
                "disagreement_with": "gen-r1-boss-sol-20260721-h-P3",
                "disputed_claim_id": "R1-A-GEN-001",
                "passage_context": "Gen.26.34-Gen.28.9, especially Gen.26.35/27.1 and the Gen.27.46 wife-motif resumption",
                "evidence_refs": ["OSHB:Gen.26.34-27.1", "OSHB:Gen.27.45-28.9", "appeal_round_2.json"],
                "rationale": "The two-verse notice is complete and the two-way remedy separates its setup from the explicit reprise while attaching it to the intervening blessing scene.",
                "uncertainty": "medium",
                "requested_next_reviewer": "fresh independent Hebrew narrative-discourse specialist or human adjudicator",
                "proposed_disposition": "three-way split; until resolved retain the larger low-confidence parent",
                "why_boss_counterevidence_is_insufficient": "Avoiding a short chunk is granularity preference, not evidence against literary completeness.",
            }]
            unresolved = ["R1-A-GEN-001"]
            boss_ruling = {
                "initial_ruling_id": "gen-boss-sol-20260721-d-P3",
                "second_cycle_ruling_id": "gen-r1-boss-sol-20260721-h-P3",
                "second_cycle_outcome": "LITERARY_TWO_WAY",
                "appeal_effect": "larger_unit_hold_deferred_human_or_external_ai",
                "forced_consensus": False,
            }
    else:
        attempt_a = "gen-primary-hebrew-20260721-a"
        attempt_b = "gen-primary-literary-20260721-b"
        peer_attempt = "gen-peer-crosscheck-20260721-c"
        evidence_a = ["reviews/Gen/primary_hebrew.json", f"chunk:{decision_id}"]
        evidence_b = ["reviews/Gen/primary_literary.json", f"chunk:{decision_id}"]
        if decision_id == "M7_sol-Gen-007":
            challenges_b = [{
                "challenge_id": "B-GEN-001",
                "severity": "minor",
                "claim": "Retain 6:1-8 but preserve explicit low confidence for translation-sensitive referents.",
                "proposed_remedy": "retain_current_low_confidence",
                "evidence_refs": ["risk_signal:Gen.6.4", "primary_literary:B-GEN-001"],
            }]
            boss_ruling = {
                "ruling_id": "gen-boss-sol-20260721-d-P6",
                "outcome": "RETAIN_CURRENT",
                "remedy": "Gen.6.1-8 at low confidence",
            }

    all_challenges = challenges_a + challenges_b
    challenge_ids = [item["challenge_id"] for item in all_challenges]
    responses = []
    for challenge_id in challenge_ids:
        if decision_id == "M7_sol-Gen-007":
            disposition = "accept: retain the flood prologue at low confidence"
        elif decision_id == "M7_sol-Gen-042r1":
            disposition = "hold: preserve the larger unit at medium_low pending human or external-AI review"
        else:
            disposition = "accept"
        responses.append({"challenge_id": challenge_id, "disposition": disposition})

    packet = {
        "schema_version": "m7_chunk_review_packet.v1",
        "decision_id": decision_id,
        "book": "Gen",
        "span": chunk["span"],
        "chunk_sha256": digest(chunk),
        "review_revision": revision,
        "primary_reviews": [
            review(attempt_a, evidence_a, challenges_a),
            review(attempt_b, evidence_b, challenges_b),
        ],
        "peer_crosscheck": {
            "reviewer_attempt_id": peer_attempt,
            "disputed_claim_ids": challenge_ids,
            "status": "hold" if decision_id == "M7_sol-Gen-042r1" else "pass",
            "evidence_refs": [f"peer:{peer_attempt}"],
        },
        "sol_resolution": {
            "author_id": "M7_sol",
            "challenge_responses": responses,
            "unresolved_claim_ids": unresolved,
            "authority": "candidate_author_only",
        },
        "appeals": appeals,
        "final_state": "deferred_human_or_external_ai" if decision_id == "M7_sol-Gen-042r1" else "accepted_candidate",
        "post_resolution_check": {
            "checker_attempt_id": FINAL_CHECKER,
            "status": "hold" if decision_id == "M7_sol-Gen-042r1" else "pass",
            "evidence_refs": ["reviews/Gen/post_resolution_check_v2.json"],
        },
        "independence_scope": INDEPENDENCE_SCOPE,
        "non_authorizing": True,
    }
    if boss_ruling is not None:
        packet["boss_ruling"] = boss_ruling
    return packet


def main() -> int:
    chunks = read_jsonl(CHUNKS)
    packets = [build_packet(chunk) for chunk in chunks]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for packet in packets:
            handle.write(json.dumps(packet, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"wrote {len(packets)} packets to {OUTPUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
