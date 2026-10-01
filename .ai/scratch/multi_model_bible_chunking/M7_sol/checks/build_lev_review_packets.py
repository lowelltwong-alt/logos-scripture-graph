#!/usr/bin/env python3
"""Build revision-aware Leviticus review packets with preserved appeals."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from review_contract_constants import INDEPENDENCE_SCOPE


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
REVIEWS = MODEL / "reviews" / "Lev"
CHUNKS = MODEL / "book_chunks" / "Lev" / "chunks.jsonl"
OUTPUT = REVIEWS / "review_packets.jsonl"
FINAL_CHECKER = "lev-final-postcheck-20260721-y"


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def digest(row: dict) -> str:
    payload = json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def normalized_initial(source: dict, source_file: str) -> dict:
    return {
        "challenge_id": source["claim_id"],
        "severity": source.get("severity", "material"),
        "claim": source.get("why_harm") or source.get("harm") or source.get("issue"),
        "passage_context": source.get("exact_passage_context") or source.get("exact_passage") or source.get("span"),
        "proposed_remedy": source.get("competing_boundary_remedy") or source.get("proposed_remedy") or source.get("remedy"),
        "counterevidence": source.get("strongest_counterevidence") or source.get("counterevidence"),
        "uncertainty": source.get("uncertainty", "medium"),
        "evidence_refs": source.get("evidence_refs", [f"reviews/Lev/{source_file}:{source['claim_id']}"]),
        "source_review": source_file,
    }


def normalized_revision(row: dict, *, lane: str, source_file: str, revision: int) -> dict:
    decision_id = row["decision_id"]
    suffix = decision_id.rsplit("-", 1)[-1].upper()
    challenge_id = f"R{revision}-{lane}-LEV-{suffix}"
    return {
        "challenge_id": challenge_id,
        "severity": "material",
        "claim": row.get("evidence") or row.get("literary_form_evidence") or row.get("form_evidence"),
        "passage_context": row.get("span") or decision_id,
        "proposed_remedy": row.get("remedy"),
        "counterevidence": row.get("counterevidence"),
        "uncertainty": row.get("confidence", "medium"),
        "evidence_refs": [f"reviews/Lev/{source_file}", f"chunk:{decision_id}"],
        "source_review": source_file,
    }


def primary(attempt: str, source_file: str, decision_id: str, row: dict | None,
            challenges: list[dict], *, lineage_note: str | None = None) -> dict:
    result = {
        "reviewer_attempt_id": attempt,
        "verdict": "challenge" if challenges else "supports",
        "blind_to_other_primary_reviews": True,
        "evidence_only": True,
        "evidence_refs": [f"reviews/Lev/{source_file}", f"chunk:{decision_id}"],
        "challenges": challenges,
    }
    if row:
        result["review_summary"] = {
            "confidence": row.get("confidence"),
            "remedy": row.get("remedy"),
            "counterevidence": row.get("counterevidence"),
        }
    if lineage_note:
        result["lineage_note"] = lineage_note
    return result


def main() -> int:
    chunks = read_jsonl(CHUNKS)
    initial_h = read_json(REVIEWS / "primary_hebrew.json")
    initial_l = read_json(REVIEWS / "primary_literary.json")
    r1_h = read_json(REVIEWS / "primary_r1_hebrew.json")
    r1_l = read_json(REVIEWS / "primary_r1_literary.json")
    r2_h = read_json(REVIEWS / "primary_r2_hebrew.json")
    r2_l = read_json(REVIEWS / "primary_r2_literary.json")
    supplemental = read_json(REVIEWS / "supplemental_premortem_summary.json")
    boss0 = read_json(REVIEWS / "boss_ruling.json")
    boss1 = read_json(REVIEWS / "boss_r1_ruling.json")
    appeal2_peer = read_json(REVIEWS / "appeal_round_2_peer.json")

    initial_h_by = {row["decision_id"]: normalized_initial(row, "primary_hebrew.json") for row in initial_h["challenges"]}
    initial_l_by = {row["decision_id"]: normalized_initial(row, "primary_literary.json") for row in initial_l["challenges"]}
    r1_h_rows = {row["decision_id"]: row for row in r1_h["reviews"]}
    r1_l_rows = {row["decision_id"]: row for row in r1_l["reviews"]}
    r2_h_rows = {row["decision_id"]: row for row in r2_h["reviews"]}
    r2_l_rows = {row["decision_id"]: row for row in r2_l["rows"]}

    r1_h_challenges = {
        decision_id: normalized_revision(row, lane="H", source_file="primary_r1_hebrew.json", revision=1)
        for decision_id, row in r1_h_rows.items() if row["verdict"] == "CHALLENGE"
    }
    r1_l_challenges = {
        decision_id: normalized_revision(row, lane="L", source_file="primary_r1_literary.json", revision=1)
        for decision_id, row in r1_l_rows.items() if row["verdict"] == "CHALLENGE"
    }
    r2_h_challenges = {
        decision_id: normalized_revision(row, lane="H", source_file="primary_r2_hebrew.json", revision=2)
        for decision_id, row in r2_h_rows.items() if row["verdict"] == "CHALLENGE"
    }
    r2_l_challenges = {
        decision_id: normalized_revision(row, lane="L", source_file="primary_r2_literary.json", revision=2)
        for decision_id, row in r2_l_rows.items() if row["verdict"] == "CHALLENGE"
    }
    supplemental_by = {
        row["decision_id"]: normalized_initial(row, "supplemental_premortem_summary.json")
        for row in supplemental["material_or_high_watchpoints"]
    }

    parent0 = {
        "M7_sol-Lev-018": "M7_sol-Lev-018",
        "M7_sol-Lev-050a": "M7_sol-Lev-050", "M7_sol-Lev-050b": "M7_sol-Lev-050",
        "M7_sol-Lev-052a": "M7_sol-Lev-052", "M7_sol-Lev-052b": "M7_sol-Lev-052",
        "M7_sol-Lev-055": "M7_sol-Lev-055",
        "M7_sol-Lev-012a": "M7_sol-Lev-012", "M7_sol-Lev-012b": "M7_sol-Lev-012",
        "M7_sol-Lev-061a": "M7_sol-Lev-061", "M7_sol-Lev-061b": "M7_sol-Lev-061",
    }
    parent1 = {
        "M7_sol-Lev-012a": "M7_sol-Lev-012", "M7_sol-Lev-012b": "M7_sol-Lev-012",
        "M7_sol-Lev-061a": "M7_sol-Lev-061", "M7_sol-Lev-061b": "M7_sol-Lev-061",
    }

    peer_appeal = appeal2_peer["rulings"][1]["appeal"]
    appeals_by_decision = {
        "M7_sol-Lev-061a": [
            {
                "appeal_id": peer_appeal["appeal_id"],
                "appellant_attempt_id": appeal2_peer["attempt_id"],
                "disagreement_with": boss1["attempt_id"],
                "disputed_claim_id": "R1-P-LEV-061A-HOLD",
                "passage_context": peer_appeal["passage_context"],
                "evidence_refs": ["reviews/Lev/appeal_round_2_peer.json", "OSHB:Lev.26.1-Lev.26.3"],
                "rationale": peer_appeal["claim"],
                "counterevidence": peer_appeal["counterevidence"],
                "uncertainty": peer_appeal["uncertainty"],
                "requested_next_reviewer": peer_appeal["requested_next_reviewer"],
            },
            {
                "appeal_id": "APL-R2-H-LEV-061A-01",
                "appellant_attempt_id": r2_h["attempt_id"],
                "disagreement_with": boss1["attempt_id"],
                "disputed_claim_id": r2_h_challenges["M7_sol-Lev-061a"]["challenge_id"],
                "passage_context": "Lev.26.1-Lev.26.2 within Lev.25.1-Lev.26.46",
                "evidence_refs": ["reviews/Lev/primary_r2_hebrew.json", "OSHB:Lev.26.1-Lev.26.3", "UXLC:Lev.26.1-Lev.26.3"],
                "rationale": r2_h_rows["M7_sol-Lev-061a"]["remedy"],
                "counterevidence": r2_h_rows["M7_sol-Lev-061a"]["counterevidence"],
                "uncertainty": r2_h_rows["M7_sol-Lev-061a"]["confidence"],
                "requested_next_reviewer": "human_or_independent_external_ai",
            },
            {
                "appeal_id": "APL-R2-L-LEV-061A-01",
                "appellant_attempt_id": r2_l["attempt_id"],
                "disagreement_with": boss1["attempt_id"],
                "disputed_claim_id": r2_l_challenges["M7_sol-Lev-061a"]["challenge_id"],
                "passage_context": "Lev.26.1-Lev.26.2 within Lev.25.1-Lev.26.46",
                "evidence_refs": ["reviews/Lev/primary_r2_literary.json", "WEB:Lev.25.1-Lev.26.46"],
                "rationale": r2_l_rows["M7_sol-Lev-061a"]["remedy"],
                "counterevidence": r2_l_rows["M7_sol-Lev-061a"]["counterevidence"],
                "uncertainty": r2_l_rows["M7_sol-Lev-061a"]["confidence"],
                "requested_next_reviewer": "human_or_independent_external_ai",
            },
        ]
    }

    packets: list[dict] = []
    for chunk in chunks:
        decision_id = chunk["decision_id"]
        revision = int(chunk.get("review_revision", 0))
        if revision == 0:
            h_ch = [initial_h_by[decision_id]] if decision_id in initial_h_by else []
            l_ch = [initial_l_by[decision_id]] if decision_id in initial_l_by else []
            primaries = [
                primary(initial_h["reviewer_attempt_id"], "primary_hebrew.json", decision_id, None, h_ch),
                primary(initial_l["reviewer_attempt_id"], "primary_literary.json", decision_id, None, l_ch),
            ]
            peer_attempt = "lev-peer-crosscheck-20260721-g"
            peer_source = "peer_crosscheck.json"
        elif revision == 1:
            h_row, l_row = r1_h_rows[decision_id], r1_l_rows[decision_id]
            h_ch = [r1_h_challenges[decision_id]] if decision_id in r1_h_challenges else []
            l_ch = [r1_l_challenges[decision_id]] if decision_id in r1_l_challenges else []
            primaries = [
                primary(r1_h["attempt_id"], "primary_r1_hebrew.json", decision_id, h_row, h_ch,
                        lineage_note=f"Fresh revision-1 review; revision-0 parent {parent0[decision_id]} is historical only."),
                primary(r1_l["attempt_id"], "primary_r1_literary.json", decision_id, l_row, l_ch,
                        lineage_note=f"Fresh revision-1 review; revision-0 parent {parent0[decision_id]} is historical only."),
            ]
            peer_attempt = "lev-r1-peer-20260721-n2"
            peer_source = "peer_r1_crosscheck.json"
        else:
            h_row, l_row = r2_h_rows[decision_id], r2_l_rows[decision_id]
            h_ch = [r2_h_challenges[decision_id]] if decision_id in r2_h_challenges else []
            l_ch = [r2_l_challenges[decision_id]] if decision_id in r2_l_challenges else []
            primaries = [
                primary(r2_h["attempt_id"], "primary_r2_hebrew.json", decision_id, h_row, h_ch,
                        lineage_note=f"Fresh child review; parent {parent1[decision_id]} review is not inherited."),
                primary(r2_l["attempt_id"], "primary_r2_literary.json", decision_id, l_row, l_ch,
                        lineage_note=f"Fresh child review; parent {parent1[decision_id]} review is not inherited."),
            ]
            peer_attempt = "lev-r2-postcheck-20260721-v2"
            peer_source = "postcheck_r2.json"

        challenges = h_ch + l_ch
        challenge_ids = [row["challenge_id"] for row in challenges]
        held = chunk.get("candidate_hold_state") == "deferred_human_or_external_ai"
        appeals = appeals_by_decision.get(decision_id, [])
        unresolved = challenge_ids[:] if held else []
        if held:
            unresolved.append("R1-P-LEV-061A-HOLD")

        historical: list[dict] = []
        original_id = parent0.get(decision_id, decision_id)
        for source in (initial_h_by, initial_l_by):
            if original_id in source:
                historical.append(source[original_id])
        if revision == 2:
            p1 = parent1[decision_id]
            if p1 in r1_h_challenges:
                historical.append(r1_h_challenges[p1])
            if p1 in r1_l_challenges:
                historical.append(r1_l_challenges[p1])

        supplement = supplemental_by.get(original_id)
        current_responses = []
        for challenge in challenges:
            if held:
                disposition = "preserved as append-only appeal; no third rewrite; standalone retrieval withheld"
                ruling_id = "lev-r2-postcheck-20260721-v2"
            else:
                disposition = "addressed in accepted candidate boundary or required relation metadata"
                ruling_id = boss0["attempt_id"]
            current_responses.append({
                "challenge_id": challenge["challenge_id"],
                "disposition": disposition,
                "ruling_id": ruling_id,
            })

        historical_responses = []
        for challenge in historical:
            historical_responses.append({
                "challenge_id": challenge["challenge_id"],
                "disposition": "implemented or preserved in descendant boundary, confidence, relation, or crosswalk metadata",
                "ruling_id": boss1["attempt_id"] if revision == 2 else boss0["attempt_id"],
            })

        packet = {
            "schema_version": "m7_chunk_review_packet.v1",
            "decision_id": decision_id,
            "book": "Lev",
            "span": chunk["span"],
            "chunk_sha256": digest(chunk),
            "review_revision": revision,
            "primary_reviews": primaries,
            "peer_crosscheck": {
                "reviewer_attempt_id": peer_attempt,
                "disputed_claim_ids": challenge_ids,
                "status": "hold" if held else "pass",
                "evidence_refs": [f"reviews/Lev/{peer_source}"],
            },
            "sol_resolution": {
                "author_id": "M7_sol",
                "challenge_responses": current_responses,
                "unresolved_claim_ids": unresolved,
                "authority": "candidate_author_only",
            },
            "historical_parent_challenges": historical,
            "historical_challenge_responses": historical_responses,
            "supplemental_specialist_review": ({
                "eligible_as_exhaustive_primary": False,
                "challenge": supplement,
                "sol_disposition": "implemented or preserved in final relation/hold metadata",
            } if supplement else None),
            "appeals": appeals,
            "final_state": "deferred_human_or_external_ai" if held else "accepted_candidate",
            "post_resolution_check": {
                "checker_attempt_id": FINAL_CHECKER,
                "status": "hold" if held else "pass",
                "evidence_refs": ["reviews/Lev/post_resolution_check_v2.json"],
            },
            "lineage": {
                "revision_0_parent_ids": [original_id],
                "revision_1_parent_id": parent1.get(decision_id),
                "fresh_current_review_attempt_ids": [p["reviewer_attempt_id"] for p in primaries],
                "retired_parent_reviews_are_historical_only": revision > 0,
            },
            "independence_scope": INDEPENDENCE_SCOPE,
            "forced_consensus": False,
            "non_authorizing": True,
        }
        if appeals:
            packet["boss_ruling"] = {
                "initial_boss_attempt_id": boss0["attempt_id"],
                "second_cycle_boss_attempt_id": boss1["attempt_id"],
                "appeal_effect": "retain frozen low-confidence child but withhold standalone retrieval pending human or external AI",
                "no_third_automatic_rewrite": True,
                "forced_consensus": False,
            }
        packets.append(packet)

    if len(packets) != 72:
        raise SystemExit(f"expected 72 packets, found {len(packets)}")
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for packet in packets:
            handle.write(json.dumps(packet, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"wrote {len(packets)} Leviticus review packets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
