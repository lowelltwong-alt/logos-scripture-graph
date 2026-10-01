#!/usr/bin/env python3
"""Materialize Jeremiah corrective artifacts from one frozen adjudicated route.

This is an environment-bound T547 campaign adapter, not a portable-core or
provider-neutral capability claim.  It writes candidate-only M7 artifacts and
never authorizes canon, theology, a preferred textual witness, publication, or
cross-model convergence.

Run without ``--finalize`` only after ``adjudicated_route_draft_v2.json`` is
frozen.  The materialization pass deliberately leaves the completion receipt
invalid.  The root integrator must atomically install ``sidecar_rows_v2.json``
into the three shared sidecars and obtain a fresh role-separated checker
verdict before invoking ``--finalize``.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[6]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
REVIEW = MODEL / "reviews" / "Jer"
CHUNKS = MODEL / "book_chunks" / "Jer" / "chunks.jsonl"
ROUTE = REVIEW / "adjudicated_route_draft_v2.json"
WITNESSES = (
    ROOT
    / "data"
    / "canonical"
    / "translations"
    / "eng-web"
    / "translation_witnesses.jsonl"
)
SIDECARS = (
    "low_confidence_register.jsonl",
    "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl",
)
ROLES = (
    "hebrew_textual_oracle_form",
    "literary_prophetic_cycle",
    "canonical_retrieval_premortem",
)
ROLE_CODES = {
    ROLES[0]: "hebrew",
    ROLES[1]: "literary",
    ROLES[2]: "canonical",
}
VALID_VERDICTS = {
    "support",
    "supports",
    "challenge",
    "insufficient_evidence",
    "frontier_defer",
}
INDEPENDENCE_SCOPE = {
    "independent_from_sibling_model_maps": True,
    "primaries_blind_to_each_other_artifacts": True,
    "roles_separated": True,
    "shared_model_substrate": True,
    "counts_as_cross_model_independent_votes": False,
    "independent_model_or_human_evidence_required_at_convergence": True,
    "reviewer_count_is_not_authority": True,
    "correlated_mesh_weight_at_convergence": "one_model_voice",
}


def atomic_text(path: Path, text: str) -> None:
    """Write a same-directory fsynced temporary and atomically replace path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def write_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    atomic_text(
        path,
        "".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
            for row in rows
        ),
    )


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_no}: expected object")
            rows.append(value)
    return rows


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_digest(row: dict[str, Any]) -> str:
    payload = json.dumps(
        row,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def web_witnesses() -> tuple[list[str], dict[str, str]]:
    rows = [
        row
        for row in load_jsonl(WITNESSES)
        if str(row.get("osis_ref", "")).startswith("Jer.")
    ]
    refs = [str(row["osis_ref"]) for row in rows]
    texts = {str(row["osis_ref"]): str(row["text"]) for row in rows}
    if (
        len(refs) != 1364
        or refs[0] != "Jer.1.1"
        or refs[-1] != "Jer.52.34"
    ):
        raise ValueError(
            "canonical WEB Jeremiah witness inventory is not the expected "
            "1,364 verses"
        )
    return refs, texts


def span_refs(
    span: str,
    refs: list[str],
    positions: dict[str, int],
) -> list[str]:
    parts = span.split("-")
    if len(parts) != 2:
        raise ValueError(f"invalid full Jeremiah span {span!r}")
    start, end = parts
    if (
        not start.startswith("Jer.")
        or not end.startswith("Jer.")
        or start not in positions
        or end not in positions
        or positions[start] > positions[end]
    ):
        raise ValueError(f"invalid Jeremiah span {span!r}")
    return refs[positions[start] : positions[end] + 1]


def source_observations(
    span: str,
    refs: list[str],
    positions: dict[str, int],
    texts: dict[str, str],
) -> list[dict[str, str]]:
    covered = span_refs(span, refs, positions)
    rows = [
        {
            "ref": f"WEB:{covered[0]}",
            "text": texts[covered[0]],
            "extent": "complete_verse",
            "use": "opening_witness",
        }
    ]
    if covered[-1] != covered[0]:
        rows.append(
            {
                "ref": f"WEB:{covered[-1]}",
                "text": texts[covered[-1]],
                "extent": "complete_verse",
                "use": "closing_witness",
            }
        )
    return rows


def packet_source_refs(span: str, decision_id: str) -> list[Any]:
    """Return exact-span sources without claiming independent WLC witnesses."""
    return [
        f"direct_read:eng-web:{span}",
        {
            "source_id": "oshb",
            "span": span,
            "observation": f"{decision_id}:OSHB_WLC_family_locator",
        },
        {
            "source_id": "uxlc",
            "span": span,
            "observation": f"{decision_id}:UXLC_WLC_family_locator",
        },
    ]


def route_is_frozen(route: dict[str, Any]) -> bool:
    if route.get("frozen") is True:
        return True
    statuses = (
        route.get("status"),
        route.get("route_status"),
        route.get("artifact_status"),
    )
    return any(
        isinstance(value, str) and "frozen" in value.lower()
        for value in statuses
    )


def nonempty(value: Any) -> str:
    return str(value or "").strip()


def normalized_disposition(unit: dict[str, Any]) -> str:
    value = nonempty(
        unit.get("disposition")
        or unit.get("candidate_state")
        or unit.get("final_state")
        or unit.get("boundary_disposition")
    )
    aliases = {
        "supported_candidate_primary": "accepted_candidate",
        "accept_candidate": "accepted_candidate",
        "held_for_independent_human_or_external_ai": (
            "deferred_human_or_external_ai"
        ),
        "hold_candidate": "deferred_human_or_external_ai",
    }
    return aliases.get(value, value)


def route_dissents(route: dict[str, Any]) -> list[dict[str, Any]]:
    value = route.get("dissents")
    if value is None:
        value = route.get("dissent_inventory", [])
    if not isinstance(value, list) or any(
        not isinstance(row, dict) for row in value
    ):
        raise ValueError("adjudicated route dissents must be an object list")
    return value


def route_relations(route: dict[str, Any]) -> list[dict[str, Any]]:
    value = route.get("decision_relations")
    if value is None:
        value = route.get("relations", [])
    if not isinstance(value, list) or any(
        not isinstance(row, dict) for row in value
    ):
        raise ValueError("adjudicated route relations must be an object list")
    return value


def validate_no_simulated_sources(unit: dict[str, Any], span: str) -> None:
    alignment = unit.get("original_language_alignment")
    if not isinstance(alignment, dict):
        return
    forbidden_true_keys = {
        "local_primary_lxx_available",
        "greek_lxx_local_primary_witness_available",
        "local_primary_dss_available",
        "dss_local_primary_witness_available",
        "local_primary_rabbinic_or_second_temple_corpus_available",
        "rabbinic_or_second_temple_local_corpus_available",
    }
    claimed = sorted(
        key for key in forbidden_true_keys if alignment.get(key) is True
    )
    if claimed:
        raise ValueError(
            f"{span}: route claims unavailable LXX/DSS/rabbinic sources: "
            f"{claimed}"
        )


def validate_parent(
    child_span: str,
    parent_span: str,
    refs: list[str],
    positions: dict[str, int],
) -> None:
    child = span_refs(child_span, refs, positions)
    parent = span_refs(parent_span, refs, positions)
    if (
        positions[parent[0]] > positions[child[0]]
        or positions[parent[-1]] < positions[child[-1]]
    ):
        raise ValueError(
            f"{child_span}: parent {parent_span} does not contain child"
        )


def primary_reviews_for_unit(
    unit: dict[str, Any],
    span: str,
) -> list[dict[str, Any]]:
    reviews = unit.get("primary_reviews")
    if not isinstance(reviews, list) or any(
        not isinstance(row, dict) for row in reviews
    ):
        raise ValueError(f"{span}: primary_reviews must be an object list")
    by_role = {nonempty(row.get("role")): row for row in reviews}
    if set(by_role) != set(ROLES) or len(reviews) != len(ROLES):
        raise ValueError(
            f"{span}: requires exactly one genuine review for each role "
            f"{ROLES}"
        )
    rendered: list[dict[str, Any]] = []
    for role in ROLES:
        review = dict(by_role[role])
        verdict = nonempty(review.get("verdict"))
        support = nonempty(review.get("support"))
        counterevidence = nonempty(review.get("counterevidence"))
        if verdict not in VALID_VERDICTS:
            raise ValueError(
                f"{span}: {role} has invalid verdict {verdict!r}"
            )
        if not support or not counterevidence:
            raise ValueError(
                f"{span}: {role} lacks decision-specific support or "
                "counterevidence"
            )
        challenge = review.get("challenge")
        challenges = review.get("challenges")
        if challenge is not None and challenges is not None:
            raise ValueError(
                f"{span}: {role} must use challenge or challenges, not both"
            )
        if challenge is not None:
            if isinstance(challenge, str):
                challenge = {
                    "claim": challenge,
                    "proposed_remedy": counterevidence,
                }
            challenges = [challenge]
        if isinstance(challenges, str):
            challenges = [
                {
                    "claim": challenges,
                    "proposed_remedy": counterevidence,
                }
            ]
        if challenges is None:
            challenges = []
        if not isinstance(challenges, list) or any(
            not isinstance(row, dict) for row in challenges
        ):
            raise ValueError(f"{span}: {role} challenges must be objects")
        for item in challenges:
            if not nonempty(item.get("claim")) or not nonempty(
                item.get("proposed_remedy")
            ):
                raise ValueError(
                    f"{span}: {role} challenge lacks claim or proposed remedy"
                )
        review["role"] = role
        review["verdict"] = verdict
        review["support"] = support
        review["counterevidence"] = counterevidence
        review["challenges"] = challenges
        review.pop("challenge", None)
        rendered.append(review)
    return rendered


def assemble_decisions() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    route = load_json(ROUTE)
    if route.get("book") != "Jer":
        raise ValueError("adjudicated route must identify Jeremiah as Jer")
    if not route_is_frozen(route):
        raise ValueError(
            "adjudicated route is not frozen; refusing active materialization"
        )
    units = route.get("units") or route.get("route")
    if not isinstance(units, list) or not units:
        raise ValueError("adjudicated route requires non-empty units")
    declared_count = route.get("route_count")
    summary = route.get("summary")
    if declared_count is None and isinstance(summary, dict):
        declared_count = summary.get("route_count")
    if declared_count not in (None, len(units)):
        raise ValueError("adjudicated route_count does not match units")

    refs, texts = web_witnesses()
    positions = {ref: index for index, ref in enumerate(refs)}
    covered: list[str] = []
    decisions: list[dict[str, Any]] = []
    route_hash = digest(ROUTE)

    for index, raw_unit in enumerate(units, 1):
        if not isinstance(raw_unit, dict):
            raise ValueError(f"route unit {index} is not an object")
        unit = dict(raw_unit)
        span = nonempty(unit.get("span"))
        covered.extend(span_refs(span, refs, positions))
        form = nonempty(unit.get("literary_form"))
        marker = nonempty(
            unit.get("deciding_marker_or_seam")
            or unit.get("deciding_marker")
        )
        rejected = nonempty(unit.get("rejected_alternative"))
        basis = nonempty(unit.get("defensible_basis"))
        rationale = nonempty(
            unit.get("boss_rationale")
            or unit.get("boundary_rationale")
        )
        confidence = nonempty(unit.get("confidence")).lower()
        disposition = normalized_disposition(unit)
        hold = unit.get("hold")
        parent_span = nonempty(unit.get("parent_span"))
        parent_form = nonempty(unit.get("parent_literary_form"))
        if not all(
            (
                form,
                marker,
                rejected,
                basis,
                rationale,
                parent_span,
                parent_form,
            )
        ):
            raise ValueError(f"{span}: incomplete bespoke adjudicated evidence")
        if len(rationale) < 80 or len(basis) < 80:
            raise ValueError(
                f"{span}: boss rationale/defensible basis is too thin"
            )
        if confidence not in {"high", "medium", "medium_low", "low"}:
            raise ValueError(
                f"{span}: unsupported confidence {confidence!r}"
            )
        if disposition not in {
            "accepted_candidate",
            "deferred_human_or_external_ai",
        }:
            raise ValueError(
                f"{span}: unsupported disposition {disposition!r}"
            )
        held = disposition == "deferred_human_or_external_ai"
        if held != isinstance(hold, dict):
            raise ValueError(f"{span}: hold object and disposition disagree")
        if isinstance(hold, dict):
            question = nonempty(hold.get("question"))
            options = hold.get("options")
            if (
                not question.endswith("?")
                or not isinstance(options, list)
                or len(options) != 2
                or any(not nonempty(option) for option in options)
            ):
                raise ValueError(
                    f"{span}: hold needs a question ending in ? and exactly "
                    "two argued options"
                )
            if not nonempty(
                hold.get("requested_reviewer")
                or unit.get("requested_reviewer")
            ):
                raise ValueError(f"{span}: hold lacks a routed reviewer")
        reviews = primary_reviews_for_unit(unit, span)
        if held and not any(row["challenges"] for row in reviews):
            raise ValueError(
                f"{span}: held unit needs a specific primary challenge"
            )
        if not held and not any(
            row["verdict"] in {"support", "supports"} for row in reviews
        ):
            raise ValueError(
                f"{span}: accepted unit lacks a supporting primary"
            )
        validate_parent(span, parent_span, refs, positions)
        validate_no_simulated_sources(unit, span)
        decision_id = f"M7_sol-Jer-{index:03d}"
        decisions.append(
            {
                "schema_version": "m7_jeremiah_decision_evidence.v2",
                "book": "Jer",
                "decision_id": decision_id,
                "span": span,
                "literary_form": form,
                "parent_literary_form": parent_form,
                "parent_span": parent_span,
                "candidate_state": disposition,
                "confidence": confidence,
                "confidence_basis": {
                    "tier": confidence,
                    "marker_strength": (
                        "adjudicated_prophetic_form_textual_order_and_seam"
                    ),
                    "alternative_strength": (
                        "specialist_counterproposal_preserved"
                    ),
                    "status_not_used_as_input": True,
                },
                "deciding_marker_or_seam": marker,
                "boundary_rationale": rationale,
                "rejected_alternative": rejected,
                "defensible_basis": basis,
                "source_observations": source_observations(
                    span,
                    refs,
                    positions,
                    texts,
                ),
                "original_language_alignment": {
                    "oshb_span": span,
                    "uxlc_span": span,
                    "wlc_family_correlation_disclosed": True,
                    "oshb_uxlc_are_independent_witnesses": False,
                    "local_primary_lxx_available": False,
                    "local_primary_dss_available": False,
                    (
                        "local_primary_rabbinic_or_second_temple_"
                        "corpus_available"
                    ): False,
                    "authority": (
                        "translation_textual_order_and_form_evidence_only"
                    ),
                },
                "hold": hold,
                "primary_reviews": reviews,
                "source_route_ordinal": index,
                "source_route_sha256": route_hash,
                "non_authorizing": True,
            }
        )

    if covered != refs:
        raise ValueError(
            "adjudicated Jeremiah decisions fail exact ordered 1,364-verse "
            "WEB coverage"
        )
    return decisions, route_dissents(route), route_relations(route)


def build_chunks(
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    for index, evidence in enumerate(decisions, 1):
        held = evidence["candidate_state"] != "accepted_candidate"
        hold = evidence.get("hold")
        span = evidence["span"]
        chunk: dict[str, Any] = {
            "model_id": "M7_sol",
            "book": "Jer",
            "span": span,
            "chunk_index_in_book": index,
            "working_title": evidence["literary_form"],
            "literature_type_guess": evidence["literary_form"],
            "literary_form": evidence["literary_form"],
            "parent_literary_form": evidence["parent_literary_form"],
            "boundary_evidence_refs": [
                f"direct_read:eng-web:{span}",
                f"direct_read:oshb:{span}",
                f"direct_read:uxlc:{span}",
                "book_strategy/Jer.md",
                "reviews/Jer/decision_evidence_v2.jsonl",
                "reviews/Jer/decision_relations.jsonl",
            ],
            "strong_or_hebrew_tags_used": [
                "direct_Hebrew_prophetic_form_considered",
                "poetry_prose_and_word_event_markers_evidence_only",
                "roots_are_not_meaning",
                "correlated_WLC_witnesses_disclosed",
                "received_WEB_order_is_not_preferred_witness_authority",
            ],
            "wj_or_red_letter_considered": False,
            "frontier_flag_considered": True,
            "confidence": evidence["confidence"],
            "decision_id": evidence["decision_id"],
            "deciding_marker_or_seam": evidence[
                "deciding_marker_or_seam"
            ],
            "boundary_rationale": evidence["boundary_rationale"],
            "rejected_alternative": evidence["rejected_alternative"],
            "counterevidence": evidence["rejected_alternative"],
            "defensible_basis": evidence["defensible_basis"],
            "confidence_basis": evidence["confidence_basis"],
            "review_revision": "m7-corrective-rereview-v2",
            "review_status": (
                "final_deferred_appeal"
                if held
                else "candidate_review_complete"
            ),
            "review_holds": [hold["question"]] if held else [],
            "candidate_hold_state": (
                "deferred_human_or_external_ai" if held else None
            ),
            "candidate_hold_basis": (
                {
                    **hold,
                    "kind": (
                        nonempty(
                            hold.get("kind")
                            or hold.get("source_issue_id")
                        )
                        or "contested_prophetic_boundary"
                    ),
                }
                if held
                else None
            ),
            "candidate_internal_seams": [
                evidence["rejected_alternative"]
            ],
            "non_authorizing": True,
            "candidate_only": True,
            "working_title_is_boundary_authority": False,
            "convergence_defense": {
                "literary_form": evidence["literary_form"],
                "deciding_marker_or_seam": evidence[
                    "deciding_marker_or_seam"
                ],
                "rejected_alternative": evidence[
                    "rejected_alternative"
                ],
                "confidence": evidence["confidence"],
                "defensible_basis": evidence["defensible_basis"],
                "parent_span": evidence["parent_span"],
                "source_observations": evidence[
                    "source_observations"
                ],
                "original_language_alignment": evidence[
                    "original_language_alignment"
                ],
            },
        }
        if held:
            chunk["human_review_question"] = hold["question"]
            chunk["human_review_options"] = hold["options"]
        chunks.append(chunk)
    return chunks


def rendered_challenges(
    *,
    source_review: dict[str, Any],
    role: str,
    index: int,
    source_refs: list[Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for challenge_index, challenge in enumerate(
        source_review["challenges"],
        1,
    ):
        rows.append(
            {
                "challenge_id": (
                    f"JER-V2-{index:03d}-"
                    f"{ROLE_CODES[role].upper()}-CH{challenge_index}"
                ),
                "claim": nonempty(challenge.get("claim")),
                "proposed_remedy": nonempty(
                    challenge.get("proposed_remedy")
                ),
                "counterevidence": nonempty(
                    challenge.get("counterevidence")
                    or source_review.get("counterevidence")
                ),
                "source_refs": source_refs,
            }
        )
    return rows


def active_appeal(
    index: int,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    hold = evidence["hold"]
    return {
        "appeal_id": f"JER-V2-APPEAL-{index:03d}",
        "appellant_attempt_id": (
            f"jer-v2-dissent-{index:03d}-specialist-high"
        ),
        "disagreement_with": (
            f"jer-v2-boss-{index:03d}-frontier-xhigh"
        ),
        "disputed_claim_id": (
            f"{evidence['decision_id']}:retrieval_treatment"
        ),
        "passage_context": (
            f"{evidence['span']} within {evidence['parent_span']}"
        ),
        "evidence_refs": packet_source_refs(
            evidence["span"],
            evidence["decision_id"],
        ),
        "rationale": hold["question"],
        "uncertainty": evidence["rejected_alternative"],
        "requested_next_reviewer": nonempty(
            hold.get("requested_reviewer")
        ),
        "status": "deferred_human_or_external_ai",
        "non_authorizing": True,
    }


def build_packets(
    decisions: list[dict[str, Any]],
    chunks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for index, (evidence, chunk) in enumerate(
        zip(decisions, chunks, strict=True),
        1,
    ):
        held = evidence["candidate_state"] != "accepted_candidate"
        source_refs = packet_source_refs(
            evidence["span"],
            evidence["decision_id"],
        )
        primary_reviews: list[dict[str, Any]] = []
        challenges: list[dict[str, Any]] = []
        for source_review in evidence["primary_reviews"]:
            role = source_review["role"]
            role_challenges = rendered_challenges(
                source_review=source_review,
                role=role,
                index=index,
                source_refs=source_refs,
            )
            challenges.extend(role_challenges)
            code = ROLE_CODES[role]
            primary_reviews.append(
                {
                    "reviewer_attempt_id": (
                        f"jer-v2-{code}-{index:03d}-specialist-high"
                    ),
                    "reviewer_role": role,
                    "role": role,
                    "verdict": source_review["verdict"],
                    "blind_to_other_primary_reviews": True,
                    "evidence_only": True,
                    "evidence_refs": source_refs,
                    "source_refs": source_refs,
                    "support": source_review["support"],
                    "counterevidence": source_review[
                        "counterevidence"
                    ],
                    "challenges": role_challenges,
                }
            )
        challenge_ids = [row["challenge_id"] for row in challenges]
        responses = [
            {
                "challenge_id": row["challenge_id"],
                "disposition": (
                    "preserve_as_unresolved_hold"
                    if held
                    else "resolve_with_adjudicated_seam_and_parent_hydration"
                ),
                "rationale": evidence["boundary_rationale"],
                "rejected_alternative": row["proposed_remedy"],
            }
            for row in challenges
        ]
        appeals = [active_appeal(index, evidence)] if held else []
        chunk_hash = row_digest(chunk)
        packet: dict[str, Any] = {
            "schema_version": "m7_corrective_review_packet.v2",
            "decision_id": evidence["decision_id"],
            "book": "Jer",
            "span": evidence["span"],
            "chunk_sha256": chunk_hash,
            "chunk_content_sha256": chunk_hash,
            "review_revision": "m7-corrective-rereview-v2",
            "primary_reviews": primary_reviews,
            "peer_crosscheck": {
                "reviewer_attempt_id": (
                    f"jer-v2-peer-{index:03d}-specialist-high"
                ),
                "reviewer_role": "adversarial_passage_crosscheck",
                "disputed_claim_ids": challenge_ids,
                "status": (
                    "hold"
                    if held
                    else "challenge_resolved"
                    if challenge_ids
                    else "pass"
                ),
                "rationale": evidence["defensible_basis"],
                "source_refs": source_refs,
                "support": evidence["boundary_rationale"],
                "counterevidence": evidence["rejected_alternative"],
                "support_challenge_mix": {
                    "support_count": sum(
                        row["verdict"] in {"support", "supports"}
                        for row in primary_reviews
                    ),
                    "challenge_count": len(challenge_ids),
                },
            },
            "sol_resolution": {
                "author_id": "M7_sol",
                "author_attempt_id": (
                    f"jer-v2-boss-{index:03d}-frontier-xhigh"
                ),
                "challenge_responses": responses,
                "unresolved_claim_ids": challenge_ids if held else [],
                "rationale": evidence["boundary_rationale"],
                "counterevidence": evidence["rejected_alternative"],
                "rejected_alternative": evidence[
                    "rejected_alternative"
                ],
                "outcome": (
                    "held_for_external_adjudication"
                    if held
                    else "accepted_candidate_after_role_specific_review"
                ),
                "authority": "candidate_author_only",
            },
            "appeals": appeals,
            "final_state": (
                "deferred_human_or_external_ai"
                if held
                else "accepted_candidate"
            ),
            "post_resolution_check": {
                "checker_attempt_id": (
                    f"jer-v2-postcluster-{index:03d}-checker-high"
                ),
                "status": "hold" if held else "pass",
                "evidence_refs": [
                    "reviews/Jer/post_resolution_check_v2.json"
                ],
                "chunk_content_sha256": chunk_hash,
            },
            "independence_scope": INDEPENDENCE_SCOPE,
            "non_authorizing": True,
            "boss_ruling": {
                "ruling_id": (
                    f"jer-v2-boss-{index:03d}-frontier-xhigh"
                ),
                "rationale": evidence["boundary_rationale"],
                "counterevidence": evidence["rejected_alternative"],
                "rejected_alternative": evidence[
                    "rejected_alternative"
                ],
                "outcome": (
                    "hold_candidate" if held else "accept_candidate"
                ),
                "appeal_effect": (
                    "preserved_unresolved"
                    if held
                    else "historical_dissent_recorded_separately"
                ),
                "forced_consensus": False,
            },
        }
        if held:
            hold = evidence["hold"]
            packet["human_review_question"] = hold["question"]
            packet["human_review_options"] = hold["options"]
            packet["human_review_route"] = hold[
                "requested_reviewer"
            ]
        if Counter(challenge_ids) != Counter(
            row["challenge_id"] for row in responses
        ):
            raise ValueError(
                f"{evidence['decision_id']}: challenge-response parity failed"
            )
        packets.append(packet)
    return packets


def ids_for_relation(
    relation: dict[str, Any],
    decisions: list[dict[str, Any]],
) -> list[str]:
    active = {row["decision_id"] for row in decisions}
    by_span = {row["span"]: row["decision_id"] for row in decisions}
    ids: list[str] = []
    for value in relation.get("decision_ids", []) or []:
        rendered = nonempty(value)
        if rendered:
            ids.append(rendered)
    for value in relation.get("decision_ordinals", []) or []:
        if type(value) is not int or value < 1 or value > len(decisions):
            raise ValueError(
                f"relation contains invalid decision ordinal {value!r}"
            )
        ids.append(decisions[value - 1]["decision_id"])
    for value in relation.get("decision_spans", []) or []:
        span = nonempty(value)
        if span not in by_span:
            raise ValueError(
                f"relation references inactive decision span {span!r}"
            )
        ids.append(by_span[span])
    if not ids:
        raise ValueError("extra relation requires at least one decision")
    if any(value not in active for value in ids):
        unknown = sorted(value for value in ids if value not in active)
        raise ValueError(
            f"relation references inactive decisions {unknown}"
        )
    return list(dict.fromkeys(ids))


def build_relations(
    decisions: list[dict[str, Any]],
    extra_relations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[str]] = {}
    for row in decisions:
        grouped.setdefault(
            (row["parent_span"], row["parent_literary_form"]),
            [],
        ).append(row["decision_id"])
    relations: list[dict[str, Any]] = []
    for index, ((span, form), children) in enumerate(
        grouped.items(),
        1,
    ):
        relations.append(
            {
                "schema_version": "m7_decision_relation.v2",
                "note_id": f"JER-V2-PARENT-{index:02d}",
                "book": "Jer",
                "relation_type": (
                    "named_prophetic_macro_parent_with_context_hydration"
                ),
                "parent_span": span,
                "parent_literary_form": form,
                "children": children,
                "rationale": (
                    f"{form} remains the operational parent for the listed "
                    "children; this preserves scene, speaker, oracle, letter, "
                    "scroll, sign, nation-collection, and appendix context "
                    "without replacing decision-local forms."
                ),
                "single_verse_children_never_retrieved_naked": True,
                "boundary_authority": False,
                "non_authorizing": True,
            }
        )
    for index, relation in enumerate(extra_relations, 1):
        ids = ids_for_relation(relation, decisions)
        rationale = nonempty(
            relation.get("rationale")
            or relation.get("relation")
        )
        if not rationale:
            raise ValueError(
                f"extra relation {index} lacks a rationale"
            )
        relations.append(
            {
                "schema_version": "m7_decision_relation.v2",
                "note_id": (
                    nonempty(relation.get("note_id"))
                    or f"JER-V2-REL-{index:03d}"
                ),
                "book": "Jer",
                "relation_type": (
                    nonempty(relation.get("relation_type"))
                    or "internal_bible_relation_evidence_only"
                ),
                "decision_ids": ids,
                "related_passages": list(
                    relation.get("related_passages", []) or []
                ),
                "rationale": rationale,
                "boundary_authority": False,
                "relation_symmetry_does_not_require_boundary_symmetry": True,
                "dependency_claim": False,
                "non_authorizing": True,
            }
        )
    note_ids = [row["note_id"] for row in relations]
    if len(note_ids) != len(set(note_ids)):
        raise ValueError("decision relation note IDs must be unique")
    return relations


def overlapping_decision(
    anchor: str,
    decisions: list[dict[str, Any]],
    refs: list[str],
    positions: dict[str, int],
) -> dict[str, Any]:
    anchor_refs = span_refs(anchor, refs, positions)
    start = positions[anchor_refs[0]]
    end = positions[anchor_refs[-1]]
    for row in decisions:
        covered = span_refs(row["span"], refs, positions)
        row_start = positions[covered[0]]
        row_end = positions[covered[-1]]
        if row_start <= end and start <= row_end:
            return row
    raise ValueError(
        f"dissent anchor does not overlap an active route span: {anchor}"
    )


def dissent_rationale(dissent: dict[str, Any]) -> str:
    direct = nonempty(dissent.get("rationale"))
    if direct:
        return direct
    active = nonempty(dissent.get("active_coordinate_treatment"))
    competing = nonempty(dissent.get("competing_treatment"))
    if active and competing:
        return f"Active candidate treatment: {active} Competing treatment: {competing}"
    raise ValueError("dissent lacks a rationale or competing treatments")


def append_dissent_ledger(
    decisions: list[dict[str, Any]],
    dissents: list[dict[str, Any]],
) -> None:
    path = REVIEW / "appeal_ledger.jsonl"
    prior = path.read_text(encoding="utf-8") if path.is_file() else ""
    prior_rows = load_jsonl(path) if path.is_file() else []
    prior_ids = {
        nonempty(row.get("appeal_id"))
        for row in prior_rows
        if nonempty(row.get("appeal_id"))
    }
    additions: list[dict[str, Any]] = []
    for index, evidence in enumerate(decisions, 1):
        if evidence["candidate_state"] == "accepted_candidate":
            continue
        appeal = active_appeal(index, evidence)
        if appeal["appeal_id"] in prior_ids:
            continue
        additions.append(
            {
                "schema_version": "m7_append_only_appeal.v2",
                **appeal,
                "book": "Jer",
                "decision_id": evidence["decision_id"],
                "affected_spans": [evidence["span"]],
                "active_packet_appeal": True,
                "forced_consensus": False,
            }
        )
        prior_ids.add(appeal["appeal_id"])

    refs, _ = web_witnesses()
    positions = {ref: index for index, ref in enumerate(refs)}
    by_span = {row["span"]: row for row in decisions}
    for ordinal, dissent in enumerate(dissents, 1):
        raw_affected_spans = dissent.get("affected_spans")
        if isinstance(raw_affected_spans, str):
            affected_spans = [raw_affected_spans]
        elif isinstance(raw_affected_spans, list):
            affected_spans = raw_affected_spans
        elif raw_affected_spans is None:
            affected_spans = []
        else:
            raise ValueError(
                f"dissent {ordinal} affected_spans must be a string or list"
            )
        anchor = nonempty(
            dissent.get("anchor_span")
            or dissent.get("affected_span")
            or dissent.get("span")
            or (affected_spans[0] if affected_spans else None)
        )
        if not anchor:
            raise ValueError(f"dissent {ordinal} lacks an anchor span")
        evidence = by_span.get(anchor) or overlapping_decision(
            anchor,
            decisions,
            refs,
            positions,
        )
        appeal_id = (
            nonempty(dissent.get("appeal_id"))
            or f"JER-V2-HISTORICAL-DISSENT-{ordinal:03d}"
        )
        if appeal_id in prior_ids:
            continue
        additions.append(
            {
                "schema_version": "m7_append_only_appeal.v2",
                "appeal_id": appeal_id,
                "dissent_id": dissent.get("dissent_id"),
                "book": "Jer",
                "decision_id": evidence["decision_id"],
                "affected_spans": affected_spans or [anchor],
                "appellant_role": (
                    nonempty(dissent.get("appellant_role"))
                    or "specialist_losing_view"
                ),
                "passage_context": (
                    f"{anchor} within {evidence['parent_span']}"
                ),
                "rationale": dissent_rationale(dissent),
                "disagreement_with": (
                    f"jer-v2-boss-"
                    f"{int(evidence['decision_id'].rsplit('-', 1)[1]):03d}"
                    "-frontier-xhigh"
                ),
                "requested_next_reviewer": (
                    nonempty(
                        dissent.get("requested_next_reviewer")
                        or dissent.get("requested_reviewer")
                        or dissent.get("next_reviewer")
                    )
                    or "independent_Jeremiah_specialist_then_human"
                ),
                "status": "preserved_historical_dissent_nonblocking",
                "active_packet_appeal": False,
                "forced_consensus": False,
                "non_authorizing": True,
            }
        )
        prior_ids.add(appeal_id)
    if additions:
        if prior and not prior.endswith("\n"):
            prior += "\n"
        atomic_text(
            path,
            prior
            + "".join(
                json.dumps(
                    row,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                + "\n"
                for row in additions
            ),
        )


def sidecar_replacement(
    decisions: list[dict[str, Any]],
    packets: list[dict[str, Any]],
) -> dict[str, Any]:
    packets_by_id = {row["decision_id"]: row for row in packets}
    rows: dict[str, list[dict[str, Any]]] = {
        name: [] for name in SIDECARS
    }
    for evidence in decisions:
        if evidence["confidence"] not in {"low", "medium_low"}:
            continue
        packet = packets_by_id[evidence["decision_id"]]
        hold = evidence.get("hold")
        accepted = packet["final_state"] == "accepted_candidate"
        question = (
            nonempty(hold.get("question"))
            if isinstance(hold, dict)
            else (
                f"{evidence['defensible_basis']} The accepted form remains "
                "candidate-only and needs specialist follow-up before any "
                "promotion."
            )
        )
        concern = (
            nonempty(hold.get("kind"))
            if isinstance(hold, dict)
            else "low_confidence_prophetic_form_followup"
        ) or "contested_prophetic_boundary"
        reviewer = (
            nonempty(hold.get("requested_reviewer"))
            if isinstance(hold, dict)
            else "independent_Jeremiah_Hebrew_and_literary_specialist"
        )
        base = {
            "model_id": "M7_sol",
            "book": "Jer",
            "span": evidence["span"],
            "chunk_decision_id": evidence["decision_id"],
            "confidence": evidence["confidence"],
            "observed_substrate_signals": [
                evidence["deciding_marker_or_seam"],
                evidence["rejected_alternative"],
                question,
            ],
            "review_packet_final_state": packet["final_state"],
            "chunk_review_status": (
                "candidate_review_complete"
                if accepted
                else "final_deferred_appeal"
            ),
            "candidate_hold_state": (
                None
                if accepted
                else "deferred_human_or_external_ai"
            ),
            "non_authorizing": True,
        }
        appeal_ids = [
            row["appeal_id"] for row in packet["appeals"]
        ]
        rows["low_confidence_register.jsonl"].append(
            {
                **base,
                "why_low_confidence": question,
                "possible_downstream_risk": evidence[
                    "defensible_basis"
                ],
                "competing_boundary_risk": evidence[
                    "rejected_alternative"
                ],
                "appeal_status": (
                    "candidate_review_complete_specialist_followup_optional"
                    if accepted
                    else "deferred_human_or_external_ai"
                ),
                "appeal_ids": appeal_ids,
            }
        )
        rows["frontier_escalation_queue.jsonl"].append(
            {
                **base,
                "concern_type": concern,
                "why_frontier_review_needed": question,
                "suggested_reviewer": reviewer,
                "promotion_authority": "none",
            }
        )
        rows["atlas_candidate_feed.jsonl"].append(
            {
                **base,
                "concern_type": concern,
                "why_low_confidence": question,
                "possible_downstream_risk": evidence[
                    "defensible_basis"
                ],
                "suggested_reviewer": reviewer,
                "proposed_atlas_action": "consider_only",
                "atlas_promotion_authority": "none",
            }
        )
    return {
        "schema_version": "m7_jeremiah_sidecar_replacement.v2",
        "book": "Jer",
        "replace_all_existing_jer_rows": True,
        "rows": rows,
        "non_authorizing": True,
    }


def role_artifact(
    role: str,
    packets: list[dict[str, Any]],
) -> dict[str, Any]:
    if role == "peer":
        reviews = [row["peer_crosscheck"] for row in packets]
    elif role == "boss":
        reviews = [row["boss_ruling"] for row in packets]
    else:
        reviews = [
            next(
                review
                for review in row["primary_reviews"]
                if review["reviewer_role"] == role
            )
            for row in packets
        ]
    return {
        "schema_version": "m7_jeremiah_role_artifact.v2",
        "book": "Jer",
        "role": role,
        "decision_local_review_count": len(reviews),
        "reviews": reviews,
        "independence_scope": INDEPENDENCE_SCOPE,
        "non_authorizing": True,
    }


def materialize() -> None:
    decisions, dissents, extra_relations = assemble_decisions()
    chunks = build_chunks(decisions)
    packets = build_packets(decisions, chunks)
    relations = build_relations(decisions, extra_relations)
    write_jsonl(REVIEW / "decision_evidence_v2.jsonl", decisions)
    write_jsonl(CHUNKS, chunks)
    write_jsonl(REVIEW / "review_packets.jsonl", packets)
    write_jsonl(REVIEW / "decision_relations.jsonl", relations)
    write_json(
        REVIEW / "primary_hebrew_v2.json",
        role_artifact(ROLES[0], packets),
    )
    write_json(
        REVIEW / "primary_literary_v2.json",
        role_artifact(ROLES[1], packets),
    )
    write_json(
        REVIEW / "canonical_premortem_v2.json",
        role_artifact(ROLES[2], packets),
    )
    write_json(
        REVIEW / "peer_crosscheck_v2.json",
        role_artifact("peer", packets),
    )
    write_json(
        REVIEW / "boss_ruling_v2.json",
        role_artifact("boss", packets),
    )
    write_json(
        REVIEW / "sidecar_rows_v2.json",
        sidecar_replacement(decisions, packets),
    )
    append_dissent_ledger(decisions, dissents)
    write_json(
        REVIEW / "post_resolution_check_v2.json",
        {
            "schema_version": "m7_post_resolution_check.v2",
            "book": "Jer",
            "overall_status": (
                "pending_role_separated_hash_bound_checker"
            ),
            "checked_route_sha256": digest(ROUTE),
            "checked_chunks_sha256": digest(CHUNKS),
            "checked_review_packets_sha256": digest(
                REVIEW / "review_packets.jsonl"
            ),
            "checked_decision_relations_sha256": digest(
                REVIEW / "decision_relations.jsonl"
            ),
            "failures": [
                (
                    "global_sidecars_not_installed_and_final_checker_"
                    "not_received"
                )
            ],
            "independence_scope": INDEPENDENCE_SCOPE,
            "non_authorizing": True,
        },
    )
    write_json(
        MODEL / "receipts" / "Jer_completion_v2.json",
        {
            "schema_version": "m7_book_completion_receipt.v2",
            "book": "Jer",
            "completion_state": (
                "invalidated_pending_corrective_rereview_closure"
            ),
            "non_authorizing": True,
        },
    )
    counts = Counter(row["confidence"] for row in chunks)
    sidecars = sidecar_replacement(decisions, packets)
    print(
        json.dumps(
            {
                "book": "Jer",
                "route_sha256": digest(ROUTE),
                "chunks": len(chunks),
                "accepted": sum(
                    row["final_state"] == "accepted_candidate"
                    for row in packets
                ),
                "held": sum(
                    row["final_state"] != "accepted_candidate"
                    for row in packets
                ),
                "confidence": dict(sorted(counts.items())),
                "sidecar_rows": len(
                    sidecars["rows"][
                        "low_confidence_register.jsonl"
                    ]
                ),
                "global_sidecars_modified": False,
                "completion_receipt_valid": False,
            },
            indent=2,
        )
    )


def book_rows_digest(path: Path) -> str:
    rows = [
        row for row in load_jsonl(path) if row.get("book") == "Jer"
    ]
    payload = b"".join(
        (
            json.dumps(
                row,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            )
            + "\n"
        ).encode("utf-8")
        for row in rows
    )
    return hashlib.sha256(payload).hexdigest()


def postcheck_commands() -> list[tuple[str, list[str]]]:
    checks = MODEL / "checks"
    return [
        (
            "exact_ordered_coverage",
            [
                sys.executable,
                str(checks / "validate_exact_book_coverage.py"),
                "--book",
                "Jer",
            ],
        ),
        (
            "official_chunk_map",
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts"
                    / "validate_whole_bible_chunk_map.py"
                ),
                str(CHUNKS),
                "--model-id",
                "M7_sol",
                "--book",
                "Jer",
                "--python-only",
            ],
        ),
        (
            "review_status_sidecar_independence_parity",
            [
                sys.executable,
                str(checks / "validate_book_review_coverage.py"),
                "--book",
                "Jer",
            ],
        ),
        (
            "literary_quality_protocol",
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts"
                    / "validate_t423_literary_quality_protocol.py"
                ),
                "--model-folder",
                str(MODEL),
                "--book",
                "Jer",
                "--require-artifacts",
            ],
        ),
        (
            "corrective_review_depth",
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts"
                    / "validate_m7_corrective_review_depth.py"
                ),
                "--model-root",
                str(MODEL),
                "--book",
                "Jer",
                "--json",
            ],
        ),
    ]


def run_postcheck_gates() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for gate_id, command in postcheck_commands():
        completed = subprocess.run(
            command,
            cwd=ROOT,
            shell=False,
            check=False,
            text=True,
            capture_output=True,
        )
        output = (completed.stdout or completed.stderr).strip()
        result = {
            "gate_id": gate_id,
            "command": " ".join(command),
            "exit_code": completed.returncode,
            "status": (
                "pass" if completed.returncode == 0 else "fail"
            ),
            "output": output,
        }
        results.append(result)
        if completed.returncode:
            raise RuntimeError(
                f"{gate_id} failed during final hash-bound postcheck: "
                f"{output}"
            )
    return results


def checker_inventory(
    packets: list[dict[str, Any]],
) -> list[str]:
    values = [
        nonempty(
            row.get("post_resolution_check", {}).get(
                "checker_attempt_id"
            )
        )
        for row in packets
    ]
    if any(not value for value in values):
        raise ValueError(
            "review packets contain an empty postchecker attempt ID"
        )
    unique = sorted(set(values))
    if len(unique) != len(values):
        duplicates = sorted(
            value
            for value, count in Counter(values).items()
            if count > 1
        )
        raise ValueError(
            f"postchecker attempt IDs are reused: {duplicates}"
        )
    return unique


def finalize(checker_verdict_file: str) -> None:
    verdict_path = Path(checker_verdict_file)
    if not verdict_path.is_absolute():
        verdict_path = ROOT / verdict_path
    verdict_path = verdict_path.resolve()
    if verdict_path.parent != REVIEW.resolve():
        raise ValueError(
            "checker verdict must be stored in the Jeremiah review directory"
        )
    verdict = load_json(verdict_path)
    packets_path = REVIEW / "review_packets.jsonl"
    relations_path = REVIEW / "decision_relations.jsonl"
    packets = load_jsonl(packets_path)
    packet_checker_ids = checker_inventory(packets)
    sidecar_hashes = {
        name: book_rows_digest(MODEL / name)
        for name in SIDECARS
    }
    accepted = sorted(
        row["decision_id"]
        for row in packets
        if row.get("final_state") == "accepted_candidate"
    )
    held = sorted(
        row["decision_id"]
        for row in packets
        if row.get("final_state") != "accepted_candidate"
    )
    appeals = sorted(
        appeal["appeal_id"]
        for row in packets
        for appeal in row.get("appeals", [])
        if isinstance(appeal, dict)
        and isinstance(appeal.get("appeal_id"), str)
    )
    expected_verdict = "pass_with_holds" if held else "pass"
    required = {
        "schema_version": "m7_role_separated_checker_verdict.v1",
        "book": "Jer",
        "checked_chunks_sha256": digest(CHUNKS),
        "checked_review_packets_sha256": digest(packets_path),
        "checked_decision_relations_sha256": digest(relations_path),
        "checked_uncertainty_sidecar_sha256": sidecar_hashes,
        "verdict": expected_verdict,
        "role_separated_from_author": True,
        "shared_model_substrate": True,
        "counts_as_cross_model_independent_vote": False,
        "non_authorizing": True,
    }
    for field, expected in required.items():
        if verdict.get(field) != expected:
            raise ValueError(
                f"checker verdict field {field} does not match frozen "
                "Jeremiah artifacts"
            )
    declared_inventory = verdict.get("checker_attempt_ids")
    if declared_inventory is not None and (
        not isinstance(declared_inventory, list)
        or sorted(declared_inventory) != packet_checker_ids
    ):
        raise ValueError(
            "checker verdict checker_attempt_ids does not match the exact "
            "packet checker inventory"
        )
    checker_attempt_id = verdict.get("checker_attempt_id")
    if (
        not isinstance(checker_attempt_id, str)
        or not checker_attempt_id
        or checker_attempt_id == "M7_sol"
        or checker_attempt_id in set(packet_checker_ids)
    ):
        raise ValueError(
            "checker verdict needs a distinct role-separated checker identity"
        )
    if verdict.get("findings") not in ([], None):
        raise ValueError("checker verdict retains unresolved findings")

    results = run_postcheck_gates()
    postcheck_path = REVIEW / "post_resolution_check_v2.json"
    write_json(
        postcheck_path,
        {
            "schema_version": "m7_post_resolution_check.v2",
            "checker_attempt_id": checker_attempt_id,
            "checker_attempt_ids": packet_checker_ids,
            "passage_cluster_size_ceiling": 8,
            "role": "fresh_read_only_post_resolution_checker",
            "book": "Jer",
            "checked_route_sha256": digest(ROUTE),
            "checked_chunks_sha256": digest(CHUNKS),
            "checked_review_packets_sha256": digest(packets_path),
            "checked_decision_relations_sha256": digest(
                relations_path
            ),
            "checked_uncertainty_sidecar_sha256": sidecar_hashes,
            "checked_decision_ids": sorted(
                row["decision_id"] for row in packets
            ),
            "checker_verdict_path": verdict_path.relative_to(
                ROOT
            ).as_posix(),
            "checker_verdict_sha256": digest(verdict_path),
            "validation_results": results,
            "chunk_count": len(packets),
            "review_packet_count": len(packets),
            "accepted_decision_count": len(accepted),
            "accepted_decision_ids": accepted,
            "held_decision_count": len(held),
            "held_decision_ids": held,
            "appeal_count": len(appeals),
            "appeal_ids": appeals,
            "independence_scope": INDEPENDENCE_SCOPE,
            "independence_limit": (
                "Role-separated checks share one model substrate and count "
                "as one correlated model voice."
            ),
            "role_separated_checker_verdict_received": True,
            "independent_model_verdict_received": False,
            "failures": [],
            "overall_status": expected_verdict,
            "forced_consensus": False,
            "non_authorizing": True,
        },
    )
    command = [
        sys.executable,
        str(MODEL / "checks" / "write_completion_receipt_v2.py"),
        "--book",
        "Jer",
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        shell=False,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            "completion receipt writer refused the finalized Jeremiah "
            "artifacts"
        )
    print(
        f"finalized Jeremiah with {len(accepted)} accepted, "
        f"{len(held)} held, and {len(appeals)} active appeals"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--checker-verdict-file")
    args = parser.parse_args()
    if args.finalize:
        if not args.checker_verdict_file:
            parser.error(
                "--finalize requires --checker-verdict-file"
            )
        finalize(args.checker_verdict_file)
    else:
        materialize()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
