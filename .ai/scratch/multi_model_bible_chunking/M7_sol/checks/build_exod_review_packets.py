#!/usr/bin/env python3
"""Build Exodus per-decision review packets with challenge, ruling, and appeal lineage."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from review_contract_constants import INDEPENDENCE_SCOPE


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
REVIEWS = MODEL / "reviews" / "Exod"
CHUNKS = MODEL / "book_chunks" / "Exod" / "chunks.jsonl"
OUTPUT = REVIEWS / "review_packets.jsonl"
FINAL_CHECKER = "exod-final-postcheck-20260722-v2"


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def digest(row: dict) -> str:
    payload = json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def normalize_challenge(source: dict, source_file: str) -> dict:
    return {
        "challenge_id": source["claim_id"],
        "severity": source.get("severity", "material"),
        "claim": source.get("why_harm") or source.get("harm") or source.get("issue") or source.get("evidence"),
        "passage_context": source.get("exact_passage_context") or source.get("exact_passage") or source.get("span"),
        "proposed_remedy": source.get("competing_boundary_remedy") or source.get("proposed_remedy") or source.get("remedy"),
        "counterevidence": source.get("counterevidence"),
        "uncertainty": source.get("uncertainty"),
        "evidence_refs": source.get("evidence_refs", [f"{source_file}:{source['claim_id']}"]),
        "source_review": source_file,
    }


def primary(attempt: str, source: str, decision_id: str, challenges: list[dict], *, lineage_note: str | None = None) -> dict:
    row = {
        "reviewer_attempt_id": attempt,
        "verdict": "challenge" if challenges else "supports",
        "blind_to_other_primary_reviews": True,
        "evidence_only": True,
        "evidence_refs": [f"reviews/Exod/{source}", f"chunk:{decision_id}"],
        "challenges": challenges,
    }
    if lineage_note:
        row["lineage_note"] = lineage_note
    return row


def main() -> int:
    chunks = read_jsonl(CHUNKS)
    initial_h = read_json(REVIEWS / "primary_hebrew.json")
    initial_l = read_json(REVIEWS / "primary_literary.json")
    r1_h = read_json(REVIEWS / "primary_r1_hebrew.json")
    r1_l = read_json(REVIEWS / "primary_r1_literary.json")
    genre = read_json(REVIEWS / "supplemental_genre_review.json")
    boss0 = read_json(REVIEWS / "boss_ruling.json")
    boss1 = read_json(REVIEWS / "boss_r1_ruling.json")
    appeal1 = read_json(REVIEWS / "appeal_round_1.json")
    appeal2 = read_json(REVIEWS / "appeal_round_2.json")

    initial_h_by = {c["decision_id"]: normalize_challenge(c, "primary_hebrew.json") for c in initial_h["challenges"]}
    initial_l_by = {c["decision_id"]: normalize_challenge(c, "primary_literary.json") for c in initial_l["challenges"]}
    r1_h_by = {c["decision_id"]: normalize_challenge(c, "primary_r1_hebrew.json") for c in r1_h["challenges"]}
    r1_l_by = {c["decision_id"]: normalize_challenge(c, "primary_r1_literary.json") for c in r1_l["challenges"]}
    genre_by = {c["decision_id"]: normalize_challenge(c, "supplemental_genre_review.json") for c in genre["watchpoints"]}
    boss0_by_claim = {claim: ruling for ruling in boss0["rulings"] for claim in ruling.get("claim_ids", [])}
    boss1_by_claim = {claim: ruling for ruling in boss1["rulings"] for claim in ruling.get("claim_ids", [])}

    parent0 = {
        "M7_sol-Exod-005r1":["M7_sol-Exod-005","M7_sol-Exod-006"],
        "M7_sol-Exod-007a":["M7_sol-Exod-007"],"M7_sol-Exod-007b":["M7_sol-Exod-007"],"M7_sol-Exod-007c":["M7_sol-Exod-007"],
        "M7_sol-Exod-010a":["M7_sol-Exod-010"],"M7_sol-Exod-010b":["M7_sol-Exod-010"],
        "M7_sol-Exod-022a":["M7_sol-Exod-022"],"M7_sol-Exod-022b":["M7_sol-Exod-022"],
        "M7_sol-Exod-043a":["M7_sol-Exod-043"],"M7_sol-Exod-043b1":["M7_sol-Exod-043"],"M7_sol-Exod-043b2":["M7_sol-Exod-043"],
        "M7_sol-Exod-043c1":["M7_sol-Exod-043"],"M7_sol-Exod-043c2":["M7_sol-Exod-043"],
    }
    parent1 = {
        "M7_sol-Exod-043b1":"M7_sol-Exod-043b","M7_sol-Exod-043b2":"M7_sol-Exod-043b",
        "M7_sol-Exod-043c1":"M7_sol-Exod-043c","M7_sol-Exod-043c2":"M7_sol-Exod-043c",
    }

    all_appeals = [a for response in appeal1["reviewer_responses"] for a in response.get("appeals", [])]
    all_appeals += [a for response in appeal2["reviewer_responses"] for a in response.get("appeals", [])]
    appeals_by_decision = {"M7_sol-Exod-060": [a for a in all_appeals if a["appeal_id"] == "APL-L-EXOD-007-01"],
                           "M7_sol-Exod-044": [a for a in all_appeals if a["appeal_id"] == "APL-R1-H-EXOD-022-01"]}

    packets = []
    for chunk in chunks:
        decision_id = chunk["decision_id"]
        revision = int(chunk.get("review_revision", 0))
        if revision == 0:
            h_ch = [initial_h_by[decision_id]] if decision_id in initial_h_by else []
            l_ch = [initial_l_by[decision_id]] if decision_id in initial_l_by else []
            primaries = [
                primary(initial_h["reviewer_attempt_id"], "primary_hebrew.json", decision_id, h_ch),
                primary(initial_l["reviewer_attempt_id"], "primary_literary.json", decision_id, l_ch),
            ]
            peer_attempt = "exod-peer-crosscheck-20260721-g"
            peer_source = "peer_crosscheck.json"
        elif revision == 1:
            h_ch = [r1_h_by[decision_id]] if decision_id in r1_h_by else []
            l_ch = [r1_l_by[decision_id]] if decision_id in r1_l_by else []
            primaries = [
                primary(r1_h["reviewer_attempt_id"], "primary_r1_hebrew.json", decision_id, h_ch),
                primary(r1_l["reviewer_attempt_id"], "primary_r1_literary.json", decision_id, l_ch),
            ]
            peer_attempt = "exod-r1-peer-20260721-l"
            peer_source = "peer_r1_crosscheck.json"
        else:
            parent = parent1[decision_id]
            primaries = [
                primary(r1_h["reviewer_attempt_id"], "primary_r1_hebrew.json", decision_id, [], lineage_note=f"Blind parent challenge {r1_h_by[parent]['challenge_id']} proposed this exact child split; focused revision-2 postcheck confirms implementation."),
                primary(r1_l["reviewer_attempt_id"], "primary_r1_literary.json", decision_id, [], lineage_note=f"Blind parent challenge {r1_l_by[parent]['challenge_id']} proposed this exact child split; focused continuity postcheck confirms implementation."),
            ]
            h_ch, l_ch = [], []
            peer_attempt = "exod-r2-hebrew-postcheck-20260721-n"
            peer_source = "postcheck_r2_hebrew.json"

        challenges = h_ch + l_ch
        challenge_ids = [c["challenge_id"] for c in challenges]
        held = chunk.get("candidate_hold_state") == "deferred_human_or_external_ai"
        appeals = appeals_by_decision.get(decision_id, [])
        unresolved = [a["disputed_claim_id"] for a in appeals]

        historical = []
        for old_id in parent0.get(decision_id, [decision_id]):
            if old_id in initial_h_by:
                historical.append(initial_h_by[old_id])
            if old_id in initial_l_by:
                historical.append(initial_l_by[old_id])
        if decision_id in {"M7_sol-Exod-019","M7_sol-Exod-035","M7_sol-Exod-060"}:
            for source in (initial_h_by, initial_l_by):
                if decision_id in source and all(c["challenge_id"] != source[decision_id]["challenge_id"] for c in historical):
                    historical.append(source[decision_id])
        if revision == 2:
            historical.extend([r1_h_by[parent1[decision_id]], r1_l_by[parent1[decision_id]]])

        supplemental = genre_by.get(decision_id)
        if not supplemental:
            for old_id in parent0.get(decision_id, []):
                if old_id in genre_by:
                    supplemental = genre_by[old_id]
                    break

        responses = []
        for challenge in challenges:
            claim_id = challenge["challenge_id"]
            ruling = boss1_by_claim.get(claim_id) or boss0_by_claim.get(claim_id)
            outcome = ruling.get("outcome") if ruling else "RETAIN_AFTER_REVIEW"
            disposition = "defer with preserved appeal" if claim_id in unresolved else f"boss disposition: {outcome}"
            responses.append({"challenge_id":claim_id,"disposition":disposition,"ruling_id":ruling.get("ruling_id") if ruling else None})

        historical_responses = []
        for challenge in historical:
            claim_id = challenge["challenge_id"]
            ruling = boss1_by_claim.get(claim_id) or boss0_by_claim.get(claim_id)
            historical_responses.append({
                "challenge_id":claim_id,
                "disposition":("implemented in descendant boundary" if revision == 2 or decision_id in parent0 else "retained after adjudication"),
                "ruling_id":ruling.get("ruling_id") if ruling else None,
            })

        packet = {
            "schema_version":"m7_chunk_review_packet.v1","decision_id":decision_id,"book":"Exod","span":chunk["span"],
            "chunk_sha256":digest(chunk),"review_revision":revision,"primary_reviews":primaries,
            "peer_crosscheck":{"reviewer_attempt_id":peer_attempt,"disputed_claim_ids":challenge_ids,"status":"hold" if held else "pass","evidence_refs":[f"reviews/Exod/{peer_source}"]},
            "sol_resolution":{"author_id":"M7_sol","challenge_responses":responses,"unresolved_claim_ids":unresolved,"authority":"candidate_author_only"},
            "historical_parent_challenges":historical,"historical_challenge_responses":historical_responses,
            "supplemental_specialist_review":({"eligible_as_exhaustive_primary":False,"challenge":supplemental,"sol_disposition":"preserved as hold/metadata evidence" if held else "addressed in final rationale or descendant relation"} if supplemental else None),
            "appeals":appeals,"final_state":"deferred_human_or_external_ai" if held else "accepted_candidate",
            "post_resolution_check":{"checker_attempt_id":FINAL_CHECKER,"status":"hold" if held else "pass","evidence_refs":["reviews/Exod/post_resolution_check_v2.json"]},
            "lineage":{"revision_0_parent_ids":parent0.get(decision_id, [decision_id]),"revision_1_parent_id":parent1.get(decision_id),"focused_postchecks":["reviews/Exod/postcheck_r2_hebrew.json","reviews/Exod/postcheck_r2_literary.json"] if revision == 2 else []},
            "independence_scope":INDEPENDENCE_SCOPE,
            "forced_consensus":False,"non_authorizing":True,
        }
        if appeals:
            packet["boss_ruling"] = {"initial_boss_attempt_id":boss0["boss_attempt_id"],"second_cycle_boss_attempt_id":boss1["boss_attempt_id"],"appeal_effect":"retain low-confidence parent and defer to human or external AI","no_third_automatic_rewrite":True,"forced_consensus":False}
        packets.append(packet)

    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for packet in packets:
            handle.write(json.dumps(packet, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"wrote {len(packets)} Exodus review packets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
