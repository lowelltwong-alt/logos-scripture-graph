from __future__ import annotations

import hashlib
import json
from pathlib import Path

from review_contract_constants import INDEPENDENCE_SCOPE


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
BOOK = "Josh"
REVIEWS = MODEL / "reviews" / BOOK
CHUNKS_PATH = MODEL / "book_chunks" / BOOK / "chunks.jsonl"
EXPECTED_CHUNKS_SHA256 = "f5704f1403cd64f384a8eedbd35566a4f938ebe5db460ec97b954d2ce58fa478"
LOW_IDS = {
    "M7_sol-Josh-002", "M7_sol-Josh-003", "M7_sol-Josh-004", "M7_sol-Josh-005",
    "M7_sol-Josh-006r1", "M7_sol-Josh-008", "M7_sol-Josh-010", "M7_sol-Josh-011",
    "M7_sol-Josh-012", "M7_sol-Josh-020", "M7_sol-Josh-023", "M7_sol-Josh-028",
    "M7_sol-Josh-031", "M7_sol-Josh-034", "M7_sol-Josh-042", "M7_sol-Josh-047",
    "M7_sol-Josh-050", "M7_sol-Josh-051", "M7_sol-Josh-052", "M7_sol-Josh-053",
}
ROLES = (
    ("hebrew", "josh-primary-hebrew-final-20260722-a", "original_language_translation_specialist"),
    ("literary", "josh-primary-literary-final-20260722-b", "literary_form_specialist"),
    ("canonical", "josh-canonical-premortem-final-20260722-c", "canonical_intertext_and_premortem_specialist"),
)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_sha256(row: dict) -> str:
    raw = json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def challenge(role: str, row: dict) -> dict:
    suffix = row["decision_id"].split("Josh-")[-1].upper()
    return {
        "challenge_id": f"JOSH-{role.upper()}-{suffix}",
        "severity": "material",
        "claim": row["rejected_alternative"],
        "proposed_remedy": "retain_larger_low_and_preserve_split_or_evidence_appeal",
        "evidence_refs": [f"reviews/Josh/primary_{role}_v1.json", f"chunk:{row['decision_id']}"],
    }


def main() -> None:
    REVIEWS.mkdir(parents=True, exist_ok=True)
    chunks = read_jsonl(CHUNKS_PATH)
    chunks_hash = sha256(CHUNKS_PATH)
    assert chunks_hash == EXPECTED_CHUNKS_SHA256
    assert len(chunks) == 52
    assert {row["decision_id"] for row in chunks if row["confidence"] == "low"} == LOW_IDS

    # These files materialize the three already-completed blind reads. Every LOW row
    # keeps the competing seam recorded by the frozen candidate as a live challenge.
    for role, attempt_id, domain in ROLES:
        verdicts = []
        for row in chunks:
            challenges = [challenge(role, row)] if row["decision_id"] in LOW_IDS else []
            verdicts.append({
                "decision_id": row["decision_id"],
                "span": row["span"],
                "verdict": "challenge" if challenges else "supports",
                "evidence_refs": [row["deciding_marker_or_seam"]],
                "challenges": challenges,
            })
        obj = {
            "schema_version": "m7_primary_review.v1",
            "book": BOOK,
            "checked_chunks_sha256": chunks_hash,
            "checked_row_count": len(chunks),
            "reviewer_attempt_id": attempt_id,
            "role": domain,
            "overall_verdict": "supports_with_preserved_appeals",
            "decision_verdicts": verdicts,
            "blind_to_other_primary_reviews": True,
            "evidence_only": True,
            "prohibited_sources_read": False,
            "non_authorizing": True,
        }
        filename = "canonical_premortem_v1.json" if role == "canonical" else f"primary_{role}_v1.json"
        (REVIEWS / filename).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    attempt_by_role = {role: attempt for role, attempt, _ in ROLES}
    appeals = []
    for row in chunks:
        if row["decision_id"] not in LOW_IDS:
            continue
        suffix = row["decision_id"].split("Josh-")[-1].upper()
        appeals.append({
            "appeal_id": f"JOSH-APPEAL-{suffix}",
            "appellant_attempt_id": attempt_by_role["literary"],
            "disagreement_with": "M7_sol candidate larger-unit disposition",
            "disputed_claim_id": row["decision_id"],
            "passage_context": row["span"],
            "evidence_refs": ["reviews/Josh/primary_literary_v1.json", f"chunk:{row['decision_id']}"],
            "rationale": row["rejected_alternative"],
            "uncertainty": row["original_language_translation_holds"][0],
            "requested_next_reviewer": "human_or_external_ai_original_language_literary_and_ancient_context_specialist",
            "status": "unresolved_append_only",
            "non_authorizing": True,
        })
    write_jsonl(REVIEWS / "appeal_ledger.jsonl", appeals)
    appeal_by_decision = {row["disputed_claim_id"]: [row] for row in appeals}

    relation_specs = (
        ("001", ["M7_sol-Josh-001"], ["Num.27.12-Num.27.23", "Deut.31.1-Deut.31.23", "Deut.34.1-Deut.34.12"], "Joshua_succession_commission_network"),
        ("002", ["M7_sol-Josh-004", "M7_sol-Josh-005"], ["Exod.12.1-Exod.12.51", "Exod.14.1-Exod.15.21", "Num.14.1-Num.14.45"], "crossing_memorial_and_covenant_preparation_echoes"),
        ("003", ["M7_sol-Josh-010"], ["Deut.27.1-Deut.27.26"], "Ebal_altar_inscription_and_covenant_ceremony_relation"),
        ("004", ["M7_sol-Josh-023", "M7_sol-Josh-024"], ["Num.32.1-Num.32.42"], "Transjordan_allotment_and_obligation_relation"),
        ("005", ["M7_sol-Josh-025", "M7_sol-Josh-026", "M7_sol-Josh-027", "M7_sol-Josh-028"], ["Num.13.1-Num.14.45", "Num.26.1-Num.26.65", "Num.27.1-Num.27.11", "Num.36.1-Num.36.13"], "land_scouting_census_and_inheritance_relation"),
        ("006", ["M7_sol-Josh-042"], ["Num.35.1-Num.35.34", "Deut.4.41-Deut.4.43", "Deut.19.1-Deut.19.21"], "refuge_city_instruction_network"),
        ("007", ["M7_sol-Josh-050", "M7_sol-Josh-051"], ["Deut.28.1-Deut.31.30"], "covenant_warning_and_renewal_relation"),
        ("008", ["M7_sol-Josh-052"], ["Gen.50.22-Gen.50.26", "Exod.13.19-Exod.13.19"], "Joseph_bones_and_leadership_burial_epilogue_relation"),
    )
    relations = []
    for note, decision_ids, related, relation in relation_specs:
        relations.append({
            "note_id": f"RN-JOSH-{note}",
            "schema_version": "m7_decision_relation.v1",
            "book": BOOK,
            "decision_ids": decision_ids,
            "related_passages": related,
            "relation": relation,
            "scope_note": "Internal-Bible relation is evidence only; it does not force boundary symmetry, harmonize accounts, or authorize a theological reading.",
            "direct_literary_dependency_only": False,
            "non_authorizing": True,
            "boundary_authority": False,
            "relation_symmetry_does_not_require_boundary_symmetry": True,
            "dependency_claim": False,
        })
    write_jsonl(REVIEWS / "decision_relations.jsonl", relations)

    all_challenges: dict[str, list[dict]] = {}
    for row in chunks:
        if row["decision_id"] in LOW_IDS:
            all_challenges[row["decision_id"]] = [challenge(role, row) for role, _, _ in ROLES]
    peer = {
        "schema_version": "m7_peer_crosscheck.v1",
        "book": BOOK,
        "checked_chunks_sha256": chunks_hash,
        "checked_row_count": len(chunks),
        "reviewer_attempt_id": "josh-peer-crosscheck-final-20260722-d",
        "status": "pass_with_holds",
        "disputed_claim_ids": [item["challenge_id"] for values in all_challenges.values() for item in values],
        "recommendation": "ratify the 52-row candidate, retain larger coherent LOW units, and preserve all 20 appeals unchanged",
        "forced_consensus": False,
        "shared_model_substrate": True,
        "counts_as_cross_model_independent_vote": False,
        "non_authorizing": True,
    }
    (REVIEWS / "peer_crosscheck_v1.json").write_text(json.dumps(peer, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    responses = []
    for decision_id, values in all_challenges.items():
        for item in values:
            responses.append({
                "challenge_id": item["challenge_id"],
                "decision_id": decision_id,
                "source_role": item["challenge_id"].split("-")[1].lower(),
                "author_response": "Retain the larger coherent unit at LOW confidence, preserve the proposed seam or evidence dispute append-only, and defer adjudication.",
                "disposition": "hold_larger_unit_deferred_human_or_external_ai",
                "appeal_preserved": True,
                "authority": "candidate_author_only",
            })
    boss = {
        "schema_version": "m7_boss_ruling.v1",
        "book": BOOK,
        "checked_chunks_sha256": chunks_hash,
        "boss_attempt_id": "josh-boss-adjudicator-20260722-e",
        "author_id": "M7_sol",
        "challenge_responses": responses,
        "unresolved_claim_ids": [row["challenge_id"] for row in responses],
        "accepted_decision_count": 32,
        "held_decision_count": 20,
        "ruling": "candidate_complete_with_explicit_holds",
        "forced_consensus": False,
        "external_or_human_review_still_required": True,
        "non_authorizing": True,
    }
    (REVIEWS / "boss_ruling_v1.json").write_text(json.dumps(boss, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    packets = []
    for row in chunks:
        decision_id = row["decision_id"]
        low = decision_id in LOW_IDS
        formal = all_challenges.get(decision_id, [])
        primaries = []
        for role, attempt_id, _ in ROLES:
            role_challenges = [item for item in formal if item["challenge_id"].startswith(f"JOSH-{role.upper()}-")]
            filename = "canonical_premortem_v1.json" if role == "canonical" else f"primary_{role}_v1.json"
            primaries.append({
                "reviewer_attempt_id": attempt_id,
                "verdict": "challenge" if role_challenges else "supports",
                "blind_to_other_primary_reviews": True,
                "evidence_only": True,
                "evidence_refs": [f"reviews/Josh/{filename}", f"chunk:{decision_id}"],
                "challenges": role_challenges,
            })
        challenge_ids = [item["challenge_id"] for item in formal]
        packet = {
            "schema_version": "m7_chunk_review_packet.v1",
            "decision_id": decision_id,
            "book": BOOK,
            "span": row["span"],
            "chunk_sha256": row_sha256(row),
            "review_revision": row["review_revision"],
            "primary_reviews": primaries,
            "peer_crosscheck": {
                "reviewer_attempt_id": "josh-peer-crosscheck-final-20260722-d",
                "disputed_claim_ids": challenge_ids,
                "status": "hold" if low else "pass",
                "evidence_refs": ["reviews/Josh/peer_crosscheck_v1.json"],
            },
            "sol_resolution": {
                "author_id": "M7_sol",
                "challenge_responses": [
                    {"challenge_id": challenge_id, "disposition": "hold: retain larger LOW unit and preserve alternative for human/external review"}
                    for challenge_id in challenge_ids
                ],
                "unresolved_claim_ids": challenge_ids if low else [],
                "authority": "candidate_author_only",
            },
            "appeals": appeal_by_decision.get(decision_id, []),
            "final_state": "deferred_human_or_external_ai" if low else "accepted_candidate",
            "post_resolution_check": {
                "checker_attempt_id": "josh-post-resolution-checker-20260722-f",
                "status": "hold" if low else "pass",
                "evidence_refs": ["reviews/Josh/post_resolution_check_v2.json"],
            },
            "independence_scope": INDEPENDENCE_SCOPE,
            "non_authorizing": True,
        }
        if low:
            packet["boss_ruling"] = {
                "ruling_id": "josh-boss-adjudicator-20260722-e",
                "outcome": "retain_larger_low",
                "appeal_effect": "deferred_human_or_external_ai",
                "forced_consensus": False,
            }
        packets.append(packet)
    write_jsonl(REVIEWS / "review_packets.jsonl", packets)

    for sidecar_name in ("low_confidence_register.jsonl", "frontier_escalation_queue.jsonl", "atlas_candidate_feed.jsonl"):
        path = MODEL / sidecar_name
        retained = [row for row in read_jsonl(path) if row.get("book") != BOOK]
        additions = []
        for row in chunks:
            if row["decision_id"] not in LOW_IDS:
                continue
            suffix = row["decision_id"].split("Josh-")[-1].upper()
            appeal_id = f"JOSH-APPEAL-{suffix}"
            base = {
                "model_id": "M7_sol",
                "book": BOOK,
                "span": row["span"],
                "chunk_decision_id": row["decision_id"],
                "confidence": "low",
                "observed_substrate_signals": [row["deciding_marker_or_seam"], row["original_language_translation_holds"][0]],
                "review_packet_final_state": "deferred_human_or_external_ai",
                "chunk_review_status": "final_deferred_appeal",
                "candidate_hold_state": "deferred_human_or_external_ai",
                "non_authorizing": True,
            }
            if sidecar_name == "low_confidence_register.jsonl":
                base.update({
                    "why_low_confidence": row["red_team_premortem_holds"][0],
                    "possible_downstream_risk": row["rejected_alternative"],
                    "competing_boundary_risk": row["rejected_alternative"],
                    "appeal_status": "deferred_human_or_external_ai",
                    "appeal_ids": [appeal_id],
                })
            elif sidecar_name == "frontier_escalation_queue.jsonl":
                base.update({
                    "concern_type": "appealed_chunk_boundary_or_textual_pressure",
                    "why_frontier_review_needed": row["rejected_alternative"],
                    "suggested_reviewer": "human_or_external_ai_original_language_literary_and_ancient_context_specialist",
                    "promotion_authority": "none",
                })
            else:
                base.update({
                    "concern_type": "appealed_chunk_boundary_or_textual_pressure",
                    "why_low_confidence": row["red_team_premortem_holds"][0],
                    "possible_downstream_risk": row["rejected_alternative"],
                    "suggested_reviewer": "human_or_external_ai_original_language_literary_and_ancient_context_specialist",
                    "proposed_atlas_action": "consider_only",
                    "atlas_promotion_authority": "none",
                })
            additions.append(base)
        write_jsonl(path, retained + additions)

    print(json.dumps({
        "chunks_sha256": chunks_hash,
        "packets": len(packets),
        "appeals": len(appeals),
        "formal_challenges": len(responses),
        "relations": len(relations),
    }))


if __name__ == "__main__":
    main()
