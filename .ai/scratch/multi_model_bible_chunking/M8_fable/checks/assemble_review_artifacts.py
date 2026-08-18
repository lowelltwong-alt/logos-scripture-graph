#!/usr/bin/env python3
"""Assemble M8_fable per-book review artifacts from mesh outputs (deterministic Tier-0).

Phase "packets": frozen rows (post-ruling) + primary/peer/author/boss inputs
  -> book_chunks/<Book>/chunks.jsonl
  -> reviews/<Book>/review_packets.jsonl (postcheck sections filled from postcheck input)
  -> reviews/<Book>/no_decision_relations_v1.json (unless relations provided)
  -> reviews/<Book>/appeal_ledger.jsonl
  -> sidecar rows replaced for this book in the three model-root sidecars
Phase "bind": hash review_packets.jsonl -> reviews/<Book>/post_resolution_check_v2.json

No judgment happens here; every semantic field comes from role inputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from review_contract_constants import INDEPENDENCE_SCOPE

ROOT = Path(__file__).resolve().parents[5]
MODEL_ROOT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M8_fable"
HELD_STATES = {"held_lower_confidence", "deferred_human_or_external_ai"}
LOW_CONFIDENCE = {"low", "medium_low"}


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def chunk_digest(row: dict) -> str:
    payload = json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_reviews(review_dir: Path, prefix: str) -> dict[str, dict]:
    """decision_id -> primary review entry (with attempt metadata folded in)."""
    out: dict[str, dict] = {}
    for path in sorted(review_dir.glob(f"{prefix}_cluster_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for review in data["reviews"]:
            entry = {
                "reviewer_attempt_id": data["reviewer_attempt_id"],
                "role": data["role"],
                "model_id": data["model_id"],
                "effort": data["effort"],
                "blind_to_other_primary_reviews": bool(data.get("blind_to_other_primary_reviews", False)),
                "evidence_only": bool(data.get("evidence_only", False)),
                "verdict": review["verdict"],
                "rationale": review["rationale"],
                "evidence_refs": review.get("evidence_refs", []),
                "challenges": review.get("challenges", []),
            }
            if review["decision_id"] in out:
                raise SystemExit(f"duplicate {prefix} review for {review['decision_id']}")
            out[review["decision_id"]] = entry
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--phase", choices=["packets", "bind"], required=True)
    parser.add_argument("--work-dir", type=Path, help="dir with frozen_rows_final.jsonl, reviews/, author_responses.json, boss_rulings.json, peer files, postcheck.json, sidecar_content.json")
    args = parser.parse_args()
    book = args.book
    reviews_out = MODEL_ROOT / "reviews" / book

    if args.phase == "bind":
        packets_path = reviews_out / "review_packets.jsonl"
        packets = read_jsonl(packets_path)
        postcheck_meta = json.loads((args.work_dir / "postcheck.json").read_text(encoding="utf-8"))
        digest = hashlib.sha256(packets_path.read_bytes()).hexdigest()
        checker_ids = sorted({p["post_resolution_check"]["checker_attempt_id"] for p in packets})
        final = {
            "schema_version": "m8_post_resolution_check.v2",
            "book": book,
            "checked_review_packets_sha256": digest,
            "checked_decision_ids": sorted(p["decision_id"] for p in packets),
            "checker_attempt_ids": checker_ids,
            "role_separated_checker_verdict_received": True,
            "independent_model_verdict_received": False,
            "checker_model_id": postcheck_meta.get("model_id"),
            "checker_effort": postcheck_meta.get("effort"),
            "defects_found": postcheck_meta.get("defects_found", []),
            "non_authorizing": True,
        }
        out = reviews_out / "post_resolution_check_v2.json"
        out.write_text(json.dumps(final, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"bound {out} to packets sha256 {digest[:16]}...")
        return 0

    work = args.work_dir
    frozen = read_jsonl(work / "frozen_rows_final.jsonl")
    review_dir = work / "reviews"
    ol = load_reviews(review_dir, "ol")
    lf = load_reviews(review_dir, "lf")
    rev_ol = load_reviews(review_dir, "rev_ol")
    rev_lf = load_reviews(review_dir, "rev_lf")
    micro_ol = load_reviews(review_dir, "micro_ol")
    micro_lf = load_reviews(review_dir, "micro_lf")
    peer_by_id: dict[str, dict] = {}
    peer_history: dict[str, list[dict]] = {}
    for pattern in ("peer_cluster_*.json", "rev_peer_cluster_*.json", "micro_peer_*.json"):
        for path in sorted(review_dir.glob(pattern)):
            data = json.loads(path.read_text(encoding="utf-8"))
            for entry in data["reviews"]:
                peer_entry = {
                    "reviewer_attempt_id": data["reviewer_attempt_id"],
                    "role": data["role"],
                    "model_id": data["model_id"],
                    "effort": data["effort"],
                    "assessment": entry.get("assessment", ""),
                    "disputed_claim_ids": entry.get("disputed_claim_ids", []),
                    "supported_claim_ids": entry.get("supported_claim_ids", []),
                    "evidence_refs": entry.get("evidence_refs", []),
                }
                previous = peer_by_id.get(entry["decision_id"])
                if previous:
                    peer_history.setdefault(entry["decision_id"], []).append(previous)
                peer_by_id[entry["decision_id"]] = peer_entry
    author = json.loads((work / "author_responses.json").read_text(encoding="utf-8"))
    boss = json.loads((work / "boss_rulings.json").read_text(encoding="utf-8"))
    postcheck = json.loads((work / "postcheck.json").read_text(encoding="utf-8"))
    postcheck_by_id = {row["decision_id"]: row for row in postcheck["decisions"]}
    sidecar_path = work / "sidecar_content_final.json"
    if not sidecar_path.is_file():
        sidecar_path = work / "sidecar_content.json"
    sidecar_content = json.loads(sidecar_path.read_text(encoding="utf-8"))

    chunk_rows: list[dict] = []
    packets: list[dict] = []
    appeal_rows: list[dict] = []

    for row in frozen:
        decision_id = row["decision_id"]
        ruling = boss[decision_id]
        final_state = ruling["final_state"]
        appeals = ruling.get("appeals", [])
        unresolved = ruling.get("unresolved_claim_ids", [])
        if (unresolved or appeals) and final_state not in HELD_STATES:
            raise SystemExit(f"{decision_id}: unresolved/appeals require held state")

        chunk = dict(row)
        if final_state == "accepted_candidate":
            chunk["review_status"] = "candidate_review_complete"
            chunk.pop("candidate_hold_state", None)
            chunk.pop("candidate_hold_basis", None)
        elif final_state in HELD_STATES:
            chunk["review_status"] = "final_deferred_appeal" if appeals else "final_deferred_review"
            chunk["candidate_hold_state"] = "deferred_human_or_external_ai"
            basis = ruling.get("hold_basis")
            if basis is None:
                basis = "preserved_appeal" if appeals else "specialist_or_external_review"
            chunk["candidate_hold_basis"] = basis
        else:
            raise SystemExit(f"{decision_id}: invalid final_state {final_state}")
        chunk_rows.append(chunk)

        primaries = []
        if decision_id in ol:
            primaries.append(ol[decision_id])
        if decision_id in lf:
            primaries.append(lf[decision_id])
        if decision_id in rev_ol:
            primaries.append(rev_ol[decision_id])
        if decision_id in rev_lf:
            primaries.append(rev_lf[decision_id])
        if decision_id in micro_ol:
            primaries.append(micro_ol[decision_id])
        if decision_id in micro_lf:
            primaries.append(micro_lf[decision_id])
        if len(primaries) < 2:
            raise SystemExit(f"{decision_id}: fewer than two primary reviews available")
        challenge_ids = [
            challenge["challenge_id"]
            for primary in primaries
            for challenge in primary["challenges"]
        ]
        responses = author[decision_id]["challenge_responses"]
        if {response["challenge_id"] for response in responses} != set(challenge_ids):
            raise SystemExit(f"{decision_id}: author responses do not cover challenges exactly")

        pc = postcheck_by_id[decision_id]
        expected_status = "pass" if final_state == "accepted_candidate" else "hold"
        if pc["status"] != expected_status:
            raise SystemExit(f"{decision_id}: postcheck status {pc['status']} != expected {expected_status}")

        packet = {
            "schema_version": "m8_review_packet.v1",
            "decision_id": decision_id,
            "book": book,
            "span": chunk["span"],
            "review_revision": chunk.get("review_revision", 0),
            "chunk_sha256": chunk_digest(chunk),
            "independence_scope": INDEPENDENCE_SCOPE,
            "primary_reviews": primaries,
            "peer_crosscheck": peer_by_id[decision_id],
            "peer_crosscheck_history": peer_history.get(decision_id, []),
            "sol_resolution": {
                "author_id": "M8_fable",
                "author_instance": author.get("_meta", {}).get("author_instance", "book_writer_sonnet"),
                "challenge_responses": responses,
                "unresolved_claim_ids": unresolved,
            },
            "boss_ruling": {
                "boss_attempt_id": ruling["boss_attempt_id"],
                "model_id": boss["_meta"]["model_id"],
                "effort": boss["_meta"]["effort"],
                "rulings": ruling["rulings"],
                "reasoning": ruling["reasoning"],
                "counterevidence_preserved": ruling.get("counterevidence_preserved", []),
            },
            "appeals": appeals,
            "final_state": final_state,
            "post_resolution_check": {
                "checker_attempt_id": pc["checker_attempt_id"],
                "status": pc["status"],
                "notes": pc.get("notes", ""),
                "evidence_refs": [f"reviews/{book}/post_resolution_check_v2.json"],
            },
            "routing_record": [
                {"role": "book_writer", **author["_meta"]["routing"]},
                *[
                    {
                        "role": primary["role"],
                        "model_id": primary["model_id"],
                        "effort": primary["effort"],
                        "attempt_id": primary["reviewer_attempt_id"],
                        "blind_to_other_primary": primary["blind_to_other_primary_reviews"],
                    }
                    for primary in primaries
                ],
                {
                    "role": "peer_crosschecker",
                    "model_id": peer_by_id[decision_id]["model_id"],
                    "effort": peer_by_id[decision_id]["effort"],
                    "attempt_id": peer_by_id[decision_id]["reviewer_attempt_id"],
                },
                {"role": "boss_adjudicator", "model_id": boss["_meta"]["model_id"], "effort": boss["_meta"]["effort"], "attempt_id": ruling["boss_attempt_id"]},
                {"role": "post_resolution_checker", "model_id": postcheck["model_id"], "effort": postcheck["effort"], "attempt_id": pc["checker_attempt_id"]},
            ],
            "non_authorizing": True,
        }
        packets.append(packet)
        for appeal in appeals:
            appeal_rows.append({"book": book, "decision_id": decision_id, **appeal, "non_authorizing": True})

    write_jsonl(MODEL_ROOT / "book_chunks" / book / "chunks.jsonl", chunk_rows)
    write_jsonl(reviews_out / "review_packets.jsonl", packets)
    write_jsonl(reviews_out / "appeal_ledger.jsonl", appeal_rows)

    relations = boss.get("_meta", {}).get("decision_relations") or []
    write_jsonl(reviews_out / "decision_relations.jsonl", relations)
    if not relations:
        receipt = {
            "schema_version": "m7_no_decision_relations.v1",
            "book": book,
            "reviewed_decision_ids": sorted(row["decision_id"] for row in chunk_rows),
            "reviewer_attempt_id": "boss_fable_c01_r1",
            "rationale": boss["_meta"]["no_relation_rationale"],
            "non_authorizing": True,
        }
        (reviews_out / "no_decision_relations_v1.json").write_text(
            json.dumps(receipt, indent=1, ensure_ascii=False), encoding="utf-8"
        )

    superseded_src = work / "superseded_decisions.jsonl"
    if superseded_src.is_file():
        superseded_rows = read_jsonl(superseded_src)
        for row in superseded_rows:
            retired_id = row["decision_id"]
            row["preserved_primary_reviews"] = [
                entry for entry in (ol.get(retired_id), lf.get(retired_id)) if entry
            ]
            row["preserved_peer_crosscheck"] = peer_by_id.get(retired_id)
            row["preserved_author_responses"] = author.get(retired_id, {}).get("challenge_responses", [])
        write_jsonl(reviews_out / "superseded_decisions.jsonl", superseded_rows)

    packet_by_id = {p["decision_id"]: p for p in packets}
    chunk_by_id = {c["decision_id"]: c for c in chunk_rows}
    low_ids = [c["decision_id"] for c in chunk_rows if c["confidence"] in LOW_CONFIDENCE]
    sidecar_rows: dict[str, list[dict]] = {"low_confidence_register.jsonl": [], "frontier_escalation_queue.jsonl": [], "atlas_candidate_feed.jsonl": []}
    for decision_id in low_ids:
        chunk = chunk_by_id[decision_id]
        packet = packet_by_id[decision_id]
        content = sidecar_content[decision_id]
        appeals = packet["appeals"]
        held = packet["final_state"] != "accepted_candidate"
        appeal_status = (
            "deferred_human_or_external_ai" if appeals
            else "no_appeal_specialist_or_external_review_hold" if held
            else "candidate_review_complete_specialist_followup_optional"
        )
        base = {
            "model_id": "M8_fable",
            "book": book,
            "span": chunk["span"],
            "chunk_decision_id": decision_id,
            "confidence": chunk["confidence"],
            "observed_substrate_signals": content["observed_substrate_signals"],
            "review_packet_final_state": packet["final_state"],
            "chunk_review_status": chunk["review_status"],
            "candidate_hold_state": chunk.get("candidate_hold_state"),
            "non_authorizing": True,
        }
        sidecar_rows["low_confidence_register.jsonl"].append({
            **base,
            "why_low_confidence": content["why_low_confidence"],
            "appeal_status": appeal_status,
        })
        sidecar_rows["frontier_escalation_queue.jsonl"].append({
            **base,
            "concern_type": content["concern_type"],
            "why_frontier_review_needed": content["why_frontier_review_needed"],
            "suggested_reviewer": content["suggested_reviewer"],
            "promotion_authority": "none",
        })
        sidecar_rows["atlas_candidate_feed.jsonl"].append({
            **base,
            "concern_type": content["concern_type"],
            "why_low_confidence": content["why_low_confidence"],
            "possible_downstream_risk": content["possible_downstream_risk"],
            "suggested_reviewer": content["suggested_reviewer"],
            "proposed_atlas_action": "consider_only",
            "atlas_promotion_authority": "none",
        })

    for filename, new_rows in sidecar_rows.items():
        path = MODEL_ROOT / filename
        existing = [row for row in read_jsonl(path) if row.get("book") != book] if path.is_file() else []
        write_jsonl(path, existing + new_rows)

    accepted = sum(1 for p in packets if p["final_state"] == "accepted_candidate")
    print(json.dumps({
        "book": book,
        "chunks": len(chunk_rows),
        "packets": len(packets),
        "accepted": accepted,
        "held": len(packets) - accepted,
        "appeals": len(appeal_rows),
        "sidecar_rows_per_file": len(low_ids),
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
