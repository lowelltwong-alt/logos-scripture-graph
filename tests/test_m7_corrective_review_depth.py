"""Exploit tests for the T544 M7 corrective-depth gate."""
from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_m7_corrective_review_depth import (
    BATCH_PROSE_SHELL_PATTERNS,
    PACKET_SCHEMA,
    REVIEW_REVISION,
    _chunk_sha256,
    _chunk_prose_aliases,
    _has_language_appropriate_source,
    _pervasive_prose_ngrams,
    _semantic_constructor_fingerprints,
    _validate_structured_web_quote_fidelity,
    validate,
)


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def _chunk(index: int, *, confidence: str, held: bool = False) -> dict:
    start = (index - 1) * 3 + 1
    end = start + 2
    decision_id = f"M7_sol-Test-{index:03d}"
    openings = (
        "temporal reset and new named setting",
        "geographical transfer followed by a crowd-gathering formula",
        "quotation formula that introduces a self-contained answer",
    )
    closures = (
        "completed response before the next speaker enters",
        "dismissal and departure before the next location",
        "quotation close followed by a narrator-level consequence",
    )
    opening = openings[(index - 1) % len(openings)]
    closure = closures[(index - 1) % len(closures)]
    return {
        "decision_id": decision_id,
        "book": "Test",
        "span": f"Test.1.{start}-Test.1.{end}",
        "literature_type_guess": "gospel_pericope",
        "literary_form": "gospel_pericope",
        "boundary_rationale": (
            f"The {opening} at Test 1:{start} opens this scene, while the {closure} at 1:{end} "
            f"closes it; splitting at 1:{start + 1} was rejected because it would detach the "
            f"scene's initiating speech from its answer and resulting action."
        ),
        "deciding_marker_or_seam": f"{opening.capitalize()} at Test.1.{start}",
        "rejected_alternative": f"Split at Test.1.{start + 1}, which severs question and answer.",
        "defensible_basis": "Scene, speaker, and response closure coincide without deciding theology.",
        "confidence": confidence,
        "review_holds": (
            ["Should this contested speech turn remain one hydrated scene, or split at the explicit quotation close?"]
            if held
            else []
        ),
        **(
            {
                "candidate_hold_state": "deferred_human_or_external_ai",
                "candidate_hold_basis": "specific quotation-close seam remains contested",
            }
            if held
            else {}
        ),
    }


def _review(decision_id: str, span: str, role: str, verdict: str) -> dict:
    return {
        "reviewer_attempt_id": f"{decision_id}-{role}",
        "role": role,
        "verdict": verdict,
        "evidence_refs": [f"direct_read:eng-web:{span}"],
        "counterevidence": "The adjacent movement shares vocabulary, but the speaker and response closure remain stronger.",
        "blind_to_other_primary_reviews": True,
        "evidence_only": True,
        "challenges": (
            [
                {
                    "challenge_id": f"{decision_id}-{role}-challenge",
                    "claim": "The quotation close could support a smaller retrievable unit.",
                    "proposed_remedy": "Hold the exact seam for a later specialist.",
                    "evidence_refs": [f"direct_read:eng-web:{span}"],
                    "counterevidence": "The response still completes the scene.",
                }
            ]
            if verdict == "challenge"
            else []
        ),
    }


def _packet(chunk: dict, *, held: bool = False) -> dict:
    decision_id = chunk["decision_id"]
    span = chunk["span"]
    reviews = [
        _review(decision_id, span, "literary", "challenge" if held else "supports"),
        _review(decision_id, span, "language", "supports"),
    ]
    challenge_ids = [c["challenge_id"] for review in reviews for c in review["challenges"]]
    return {
        "schema_version": PACKET_SCHEMA,
        "review_revision": REVIEW_REVISION,
        "decision_id": decision_id,
        "book": "Test",
        "span": span,
        "chunk_content_sha256": _chunk_sha256(chunk),
        "primary_reviews": reviews,
        "peer_crosscheck": {
            "reviewer_attempt_id": f"{decision_id}-peer",
            "reviewer_role": "adversarial_peer_crosscheck",
            "rationale": "The two primaries address the same scene envelope and preserve the quotation-seam objection.",
            "counterevidence": "The quotation close remains a plausible smaller-unit seam.",
            "source_refs": [f"WEB:{span}"],
        },
        "sol_resolution": {
            "author_attempt_id": f"{decision_id}-boss",
            "unresolved_claim_ids": challenge_ids if held else [],
            "challenge_responses": [
                {
                    "challenge_id": challenge_id,
                    "disposition": "preserve_for_external_review" if held else "resolved",
                    "rationale": "The quotation close is genuine counterevidence and remains visible to the next reviewer.",
                    "rejected_alternative": "Do not erase the challenge merely because the larger scene is coherent.",
                }
                for challenge_id in challenge_ids
            ],
        },
        "appeals": [],
        "final_state": "deferred_human_or_external_ai" if held else "accepted_candidate",
        "human_review_question": (
            "Should this contested speech turn remain one hydrated scene, or split at the explicit quotation close?"
            if held
            else None
        ),
        "human_review_route": "external_ai_or_human_literary_form_specialist" if held else None,
        "post_resolution_check": {
            "checker_attempt_id": f"{decision_id}-post",
            "status": "pass_with_hold" if held else "pass",
            "chunk_content_sha256": _chunk_sha256(chunk),
        },
        "independence_scope": {
            "independent_from_sibling_model_maps": True,
            "primaries_blind_to_each_other_artifacts": True,
            "roles_separated": True,
            "shared_model_substrate": True,
            "counts_as_cross_model_independent_votes": False,
            "independent_model_or_human_evidence_required_at_convergence": True,
            "reviewer_count_is_not_authority": True,
        },
        "boss_ruling": {
            "ruling_id": f"{decision_id}-boss",
            "outcome": "hold" if held else "accept",
            "rationale": "The scene envelope is strong, with one preserved quotation-seam counterargument.",
            "counterevidence": "The quotation close could support a smaller child.",
            "rejected_alternative": "Do not split until the quotation-to-response relation is independently checked.",
        },
    }


def _fixture(root: Path) -> tuple[list[dict], list[dict]]:
    chunks = [
        _chunk(1, confidence="high"),
        _chunk(2, confidence="medium"),
        _chunk(3, confidence="low", held=True),
    ]
    packets = [_packet(chunks[0]), _packet(chunks[1]), _packet(chunks[2], held=True)]
    _write_jsonl(root / "book_chunks" / "Test" / "chunks.jsonl", chunks)
    _write_jsonl(root / "reviews" / "Test" / "review_packets.jsonl", packets)
    return chunks, packets


def test_prose_ngram_gate_detects_substitution_shell_across_decisions() -> None:
    rows = [
        {
            "decision_id": f"D-{index}",
            "boundary_rationale": (
                f"Decision {index} supplies the local basis; its rival remains explicit and reviewable."
            ),
        }
        for index in range(10)
    ]
    violations = _pervasive_prose_ngrams(rows)
    assert violations
    assert violations[0][0] == 10
    assert any("supplies the local basis its rival remains" in ngram for _count, ngram, _ids in violations)


def test_structured_web_quote_rejects_clipped_complete_verse() -> None:
    canonical = {"WEB:Ps.1.6": "For Yahweh knows the way of the righteous, but the way of the wicked shall perish."}
    errors, checked = _validate_structured_web_quote_fidelity(
        {"ref": "WEB:Ps.1.6", "text": "For Yahweh knows the way of the righteous,", "extent": "complete_verse"},
        canonical,
    )
    assert checked == 1
    assert errors == ["$: complete_verse text must equal canonical WEB exactly"]


def test_structured_web_quote_accepts_trailing_ellipsized_exact_excerpt() -> None:
    canonical = {"WEB:Ps.1.6": "For Yahweh knows the way of the righteous, but the way of the wicked shall perish."}
    errors, checked = _validate_structured_web_quote_fidelity(
        {"ref": "WEB:Ps.1.6", "text": "For Yahweh knows the way…", "extent": "opening_excerpt"},
        canonical,
    )
    assert checked == 1
    assert errors == []


def test_structured_web_quote_accepts_leading_ellipsized_exact_excerpt() -> None:
    canonical = {"WEB:Ps.1.6": "For Yahweh knows the way of the righteous, but the way of the wicked shall perish."}
    errors, checked = _validate_structured_web_quote_fidelity(
        {"ref": "WEB:Ps.1.6", "text": "…the way of the wicked shall perish.", "extent": "closing_excerpt"},
        canonical,
    )
    assert checked == 1
    assert errors == []


def test_structured_web_quote_ignores_unrelated_text_dict() -> None:
    errors, checked = _validate_structured_web_quote_fidelity(
        {"text": "Hebrew feature prose without a WEB locator", "kind": "hebrew_feature"},
        {},
    )
    assert checked == 0
    assert errors == []


def test_structured_web_quote_accepts_exact_complete_verse() -> None:
    verse = "For Yahweh knows the way of the righteous, but the way of the wicked shall perish."
    errors, checked = _validate_structured_web_quote_fidelity(
        {"wrapper": [{"ref": "WEB:Ps.1.6", "text": verse, "extent": "complete_verse"}]},
        {"WEB:Ps.1.6": verse},
    )
    assert checked == 1
    assert errors == []


def test_batch_shell_patterns_cover_semantic_child_constructors() -> None:
    samples = {
        'terminal_change_bounds_constructor': 'This terminal change bounds Ps.18.1-Ps.18.6, whose local function is petition.',
        'opening_through_close_constructor': 'From that opening through Ps.18.19, the child carries the rescue function.',
        'two_observed_turns_bracket_constructor': 'Those two observed turns bracket Ps.18.20-Ps.18.30 as testimony.',
        'adjacent_alternative_constructor': 'Ps.18.1-Ps.18.19 is the adjacent alternative, but it erases the turn.',
        'directly_inspectable_web_transition_constructor': 'M7_sol-Ps-023 has directly inspectable WEB transition evidence at the seam.',
        'received_web_psalm_constructor': 'M7_sol-Ps-001 covers the complete received WEB Psalm while retaining its close.',
        "web_completes_initiates_retain": "WEB:Ps.18.6 completes distress plea; WEB:Ps.18.7 initiates theophany. Retain Ps.18.1-Ps.18.6 inside prayer.",
        "web_closes_initiates_preserve": "WEB:Ps.18.19 closes rescue; WEB:Ps.18.20 initiates vindication. Preserve Ps.18.20-Ps.18.30 as the next act.",
        "web_leaves_then_opens_keep": "WEB:Ps.18.20 leaves rescue for vindication; WEB:Ps.18.31 then opens praise. Keep Ps.18.20-Ps.18.30 between those functions.",
        "merge_cost_constructor": "Merge Ps.18.1-Ps.18.6 with Ps.18.7-Ps.18.19; cost: the theophany opening becomes implicit.",
        "absorb_cost_constructor": "Absorb Ps.18.20-Ps.18.30 into Ps.18.31-Ps.18.45; cost: the vindication movement loses a locator.",
    }
    for name, prose in samples.items():
        assert BATCH_PROSE_SHELL_PATTERNS[name].search(prose), name


def test_known_semantic_constructor_is_zero_tolerance_for_small_book(tmp_path: Path) -> None:
    chunks, packets = _fixture(tmp_path)
    chunks[0]["boundary_rationale"] = (
        "WEB:Test.1.3 completes the opening appeal; WEB:Test.1.4 initiates the answer. "
        "Retain Test.1.1-Test.1.3 inside the complete discourse."
    )
    packets[0]["chunk_content_sha256"] = _chunk_sha256(chunks[0])
    packets[0]["post_resolution_check"]["chunk_content_sha256"] = _chunk_sha256(chunks[0])
    _write_jsonl(tmp_path / "book_chunks" / "Test" / "chunks.jsonl", chunks)
    _write_jsonl(tmp_path / "reviews" / "Test" / "review_packets.jsonl", packets)
    errors, _summary = validate(tmp_path, "Test")
    joined = "\n".join(errors)
    assert "repeated prose-shell substitution signature remains" in joined
    assert "web_completes_initiates_retain" in joined


def test_known_review_shell_is_zero_tolerance_for_small_book(tmp_path: Path) -> None:
    _chunks, packets = _fixture(tmp_path)
    packets[0]["primary_reviews"][0]["support"] = (
        f"The WEB coordinates for {packets[0]['span']} are stable, but this is a known review shell."
    )
    _write_jsonl(tmp_path / "reviews" / "Test" / "review_packets.jsonl", packets)
    errors, _summary = validate(tmp_path, "Test")
    joined = "\n".join(errors)
    assert "repeated review-prose substitution signature remains" in joined
    assert "web_coordinates_are_stable" in joined


def test_corrective_depth_accepts_bespoke_mixed_review(tmp_path: Path) -> None:
    _fixture(tmp_path)
    errors, summary = validate(tmp_path, "Test")
    assert errors == []
    assert summary["accepted"] == 2
    assert summary["held"] == 1


def test_corrective_depth_rejects_owner_named_smells(tmp_path: Path) -> None:
    chunks, packets = _fixture(tmp_path)
    chunks[0]["literary_form"] = "larger narrative-discourse episode"
    chunks[0]["boundary_rationale"] = "Prefer the complete larger narrative-discourse episode Test.1.1-Test.1.3."
    for chunk in chunks:
        chunk["confidence"] = "low"
    for packet in packets:
        packet["final_state"] = "deferred_human_or_external_ai"
        packet["human_review_question"] = "Should this exact boundary remain or be split at the stated alternative seam?"
        packet["primary_reviews"][0]["reviewer_attempt_id"] = "one-book-wide-attempt"
    _write_jsonl(tmp_path / "book_chunks" / "Test" / "chunks.jsonl", chunks)
    _write_jsonl(tmp_path / "reviews" / "Test" / "review_packets.jsonl", packets)

    errors, _summary = validate(tmp_path, "Test", max_attempt_reuse=2)
    joined = "\n".join(errors)
    assert "generic literary form" in joined
    assert "templated boundary" in joined
    assert "accepted decisions must be" in joined
    assert "uniform confidence" in joined
    assert "attempt IDs exceed" in joined

def test_language_source_gate_distinguishes_testament_and_translation() -> None:
    span = "Matt.1.1-Matt.1.17"
    assert _has_language_appropriate_source([f"SBLGNT:Matt.xml#{span}"], span, "Matt")
    assert _has_language_appropriate_source([f"direct_read:ugnt:{span}"], span, "Matt")
    assert not _has_language_appropriate_source([f"WEB:{span}"], span, "Matt")
    ps_span = "Ps.1.1-Ps.1.6"
    assert not _has_language_appropriate_source([f"OSHB:Ps.xml#{ps_span}"], ps_span, "Ps")
    assert _has_language_appropriate_source(
        [
            {
                "source_id": "oshb",
                "web_span": ps_span,
                "source_span": "Ps.1.1-Ps.1.6",
                "crosswalk_status": "validated_web_mt_verse_mapping",
                "observation": "Psalm 1 has no superscription offset in this mapped span.",
                "source_metadata_boundary_authority": False,
            }
        ],
        ps_span,
        "Ps",
    )
    assert not _has_language_appropriate_source([f"SBLGNT:Ps.xml#{ps_span}"], ps_span, "Ps")
    dan_span = "Dan.4.1-Dan.4.3"
    dan_source_span = "Dan.3.31-Dan.3.33"
    dan_refs = [
        {
            "source_id": source_id,
            "span": dan_source_span,
            "web_span": dan_span,
            "source_span": dan_source_span,
            "coordinate_system": "MT_WLC",
            "crosswalk_status": "validated_web_mt_verse_mapping",
            "observation": (
                f"WEB Daniel 4:1-3 maps to MT/WLC Daniel 3:31-33 in {source_id}."
            ),
            "source_metadata_boundary_authority": False,
        }
        for source_id in ("oshb", "uxlc")
    ]
    assert _has_language_appropriate_source(dan_refs, dan_span, "Dan")
    assert not _has_language_appropriate_source(
        dan_refs[:1],
        dan_span,
        "Dan",
    )
    assert not _has_language_appropriate_source(
        [
            {
                **ref,
                "span": dan_span,
                "source_span": dan_span,
            }
            for ref in dan_refs
        ],
        dan_span,
        "Dan",
    )
    assert not _has_language_appropriate_source(
        [{**ref, "source_span": "Dan.3.30-Dan.3.32"} for ref in dan_refs],
        dan_span,
        "Dan",
    )
    assert not _has_language_appropriate_source(
        [{**ref, "coordinate_system": "WEB"} for ref in dan_refs],
        dan_span,
        "Dan",
    )
    hos_span = "Hos.1.10-Hos.2.1"
    hos_source_span = "Hos.2.1-Hos.2.3"
    hos_refs = [
        {
            "source_id": source_id,
            "span": hos_source_span,
            "web_span": hos_span,
            "source_span": hos_source_span,
            "coordinate_system": "MT_WLC",
            "crosswalk_status": "validated_web_mt_verse_mapping",
            "observation": (
                "WEB Hosea 1:10-2:1 maps to MT/WLC Hosea 2:1-3 "
                f"in {source_id}."
            ),
            "source_metadata_boundary_authority": False,
        }
        for source_id in ("oshb", "uxlc")
    ]
    assert _has_language_appropriate_source(hos_refs, hos_span, "Hos")
    assert not _has_language_appropriate_source(hos_refs[:1], hos_span, "Hos")
    assert not _has_language_appropriate_source(
        [
            {
                **ref,
                "span": hos_span,
                "source_span": hos_span,
            }
            for ref in hos_refs
        ],
        hos_span,
        "Hos",
    )
    assert not _has_language_appropriate_source(
        [{**ref, "coordinate_system": "WEB"} for ref in hos_refs],
        hos_span,
        "Hos",
    )
    hos_end_span = "Hos.13.16-Hos.14.9"
    hos_end_source_span = "Hos.14.1-Hos.14.10"
    hos_end_refs = [
        {
            **ref,
            "span": hos_end_source_span,
            "web_span": hos_end_span,
            "source_span": hos_end_source_span,
            "observation": (
                "WEB Hosea 13:16-14:9 maps to MT/WLC Hosea 14:1-10."
            ),
        }
        for ref in hos_refs
    ]
    assert _has_language_appropriate_source(
        hos_end_refs,
        hos_end_span,
        "Hos",
    )
    source_gap = {
        "source_id": "oshb",
        "web_span": ps_span,
        "source_span": None,
        "crosswalk_status": "unverified_web_mt_verse_mapping",
        "evidence_status": "source_gap_no_boundary_claim",
        "observation": "Superscription offset is not crosswalked for this WEB span.",
        "source_metadata_boundary_authority": False,
    }
    assert _has_language_appropriate_source([source_gap], ps_span, "Ps", "insufficient_evidence")
    assert not _has_language_appropriate_source([source_gap], ps_span, "Ps", "supports")


def test_corrective_depth_rejects_blindness_and_evidence_authority_spoof(tmp_path: Path) -> None:
    _chunks, packets = _fixture(tmp_path)
    packets[0]["primary_reviews"][0]["blind_to_other_primary_reviews"] = False
    packets[0]["primary_reviews"][1]["evidence_only"] = False
    packets[0]["independence_scope"]["counts_as_cross_model_independent_votes"] = True
    _write_jsonl(tmp_path / "reviews" / "Test" / "review_packets.jsonl", packets)

    errors, _summary = validate(tmp_path, "Test")
    joined = "\n".join(errors)
    assert "blind_to_other_primary_reviews=true" in joined
    assert "evidence_only=true" in joined
    assert "counts_as_cross_model_independent_votes must be false" in joined


def test_corrective_depth_rejects_question_mark_quote_corruption(tmp_path: Path) -> None:
    chunks, packets = _fixture(tmp_path)
    chunks[0]["boundary_rationale"] += " Its incipit was corrupted to ?Blessed rather than a real quotation mark."
    packets[0]["primary_reviews"][0]["support"] = "The line begins ?Blessed, which exposes lost opening punctuation."
    packets[0]["chunk_content_sha256"] = _chunk_sha256(chunks[0])
    packets[0]["post_resolution_check"]["chunk_content_sha256"] = _chunk_sha256(chunks[0])
    _write_jsonl(tmp_path / "book_chunks" / "Test" / "chunks.jsonl", chunks)
    _write_jsonl(tmp_path / "reviews" / "Test" / "review_packets.jsonl", packets)

    errors, _summary = validate(tmp_path, "Test")
    joined = "\n".join(errors)
    assert "quote/Unicode or doubled-terminal punctuation corruption" in joined
    assert "punctuation corruption in chunks" in joined
    assert "punctuation corruption in review packets" in joined


def test_corrective_depth_rejects_doubled_terminal_punctuation(tmp_path: Path) -> None:
    chunks, packets = _fixture(tmp_path)
    chunks[0]["boundary_rationale"] += ' The quotation was rendered "Why?." with a duplicate terminator.'
    packets[0]["chunk_content_sha256"] = _chunk_sha256(chunks[0])
    packets[0]["post_resolution_check"]["chunk_content_sha256"] = _chunk_sha256(chunks[0])
    _write_jsonl(tmp_path / "book_chunks" / "Test" / "chunks.jsonl", chunks)
    _write_jsonl(tmp_path / "reviews" / "Test" / "review_packets.jsonl", packets)
    errors, _summary = validate(tmp_path, "Test")
    assert "doubled-terminal punctuation corruption in chunks" in "\n".join(errors)


def test_corrective_depth_rejects_clipped_quote_and_review_shell_batch(tmp_path: Path) -> None:
    chunks = [_chunk(index, confidence="high" if index < 10 else "medium") for index in range(1, 11)]
    packets = [_packet(chunk) for chunk in chunks]
    chunks[0]["boundary_rationale"] += ' The clipped witness begins "Blessed is the man in the".'
    packets[0]["chunk_content_sha256"] = _chunk_sha256(chunks[0])
    packets[0]["post_resolution_check"]["chunk_content_sha256"] = _chunk_sha256(chunks[0])
    for packet in packets:
        packet["primary_reviews"][0]["support"] = (
            f"The WEB coordinates for {packet['span']} are stable, but this sentence is a stamped review shell."
        )
    _write_jsonl(tmp_path / "book_chunks" / "Test" / "chunks.jsonl", chunks)
    _write_jsonl(tmp_path / "reviews" / "Test" / "review_packets.jsonl", packets)

    errors, _summary = validate(tmp_path, "Test")
    joined = "\n".join(errors)
    assert "probable clipped source quotation" in joined
    assert "repeated review-prose substitution signature" in joined
    assert "web_coordinates_are_stable" in joined


def test_corrective_depth_rejects_missing_mesh_and_stale_hash(tmp_path: Path) -> None:
    chunks, packets = _fixture(tmp_path)
    packets[0].pop("peer_crosscheck")
    packets[0].pop("post_resolution_check")
    packets[0]["chunk_content_sha256"] = "0" * 64
    _write_jsonl(tmp_path / "reviews" / "Test" / "review_packets.jsonl", packets)

    errors, _summary = validate(tmp_path, "Test")
    joined = "\n".join(errors)
    assert "peer_crosscheck is required" in joined
    assert "post_resolution_check is required" in joined
    assert "chunk_content_sha256 is stale" in joined


def test_corrective_depth_rejects_unanswered_challenge_and_spoofed_source(tmp_path: Path) -> None:
    _chunks, packets = _fixture(tmp_path)
    packets[2]["sol_resolution"]["challenge_responses"] = []
    packets[2]["primary_reviews"][0]["evidence_refs"] = [f"Review:{packets[2]['span']}"]
    _write_jsonl(tmp_path / "reviews" / "Test" / "review_packets.jsonl", packets)

    errors, _summary = validate(tmp_path, "Test")
    joined = "\n".join(errors)
    assert "every primary challenge needs exactly one author response" in joined
    assert "lacks a resolved exact-span source reference" in joined


def test_corrective_depth_rejects_packet_chunk_hold_mismatch(tmp_path: Path) -> None:
    chunks, packets = _fixture(tmp_path)
    chunks[0]["candidate_hold_state"] = "deferred_human_or_external_ai"
    chunks[0]["candidate_hold_basis"] = "stale hold accidentally retained"
    packets[0]["chunk_content_sha256"] = _chunk_sha256(chunks[0])
    packets[0]["post_resolution_check"]["chunk_content_sha256"] = _chunk_sha256(chunks[0])
    _write_jsonl(tmp_path / "book_chunks" / "Test" / "chunks.jsonl", chunks)
    _write_jsonl(tmp_path / "reviews" / "Test" / "review_packets.jsonl", packets)

    errors, _summary = validate(tmp_path, "Test")
    assert "accepted packet conflicts with chunk candidate_hold_state" in "\n".join(errors)

def test_corrective_depth_rejects_mechanical_midpoint_batch(tmp_path: Path) -> None:
    chunks = [_chunk(index, confidence="high") for index in range(1, 11)]
    for chunk in chunks:
        start = int(chunk["span"].split(".")[2].split("-")[0])
        end = int(chunk["span"].rsplit(".", 1)[1])
        midpoint = (start + end) // 2
        chunk["rejected_alternative"] = (
            f"Rejected subdividing {chunk['span']} at verse {midpoint}: this mathematical midpoint is not literary evidence."
        )
    packets = [_packet(chunk) for chunk in chunks]
    _write_jsonl(tmp_path / "book_chunks" / "Test" / "chunks.jsonl", chunks)
    _write_jsonl(tmp_path / "reviews" / "Test" / "review_packets.jsonl", packets)

    errors, _summary = validate(tmp_path, "Test")
    assert "mechanical midpoint batch signature" in "\n".join(errors)

def test_corrective_depth_rejects_role_and_parent_form_batch(tmp_path: Path) -> None:
    chunks = []
    for index in range(1, 11):
        chunk = _chunk(index, confidence="high")
        chapter = (index + 1) // 2
        chunk["span"] = f"Test.{chapter}.1-Test.{chapter}.2"
        chunks.append(chunk)
    packets = [_packet(chunk) for chunk in chunks]
    _write_jsonl(tmp_path / "book_chunks" / "Test" / "chunks.jsonl", chunks)
    _write_jsonl(tmp_path / "reviews" / "Test" / "review_packets.jsonl", packets)

    errors, _summary = validate(tmp_path, "Test")
    joined = "\n".join(errors)
    assert "copied parent-form batch signature" in joined
    assert "primary role verdicts are mechanically uniform" in joined
def test_slot_masked_semantic_gate_detects_variable_constructor() -> None:
    rows = []
    for index in range(12):
        marker = f'Speaker turn {chr(65 + index)} closes one movement and opens another'
        form = f'local_form_{index}'
        span = f'Ps.{index + 1}.1-Ps.{index + 1}.4'
        flag = ('H', 'R', 'RC')[index % 3]
        rows.append({
            'decision_id': f'M7_sol-Ps-{index + 1:03d}',
            'span': span,
            'literary_form': form,
            'deciding_marker_or_seam': marker,
            'specialist_advisory_flag': flag,
            'source_observations': [{'ref': f'WEB:Ps.{index + 1}.1', 'text': f'Quoted witness {index}'}],
            'boundary_rationale': (
                f'{marker}. Consequently {span} receives a separate retrieval identity as {form}; '
                f'the {flag} advisory remains evidence only.'
            ),
        })
    violations = _semantic_constructor_fingerprints(rows)
    assert violations
    assert any(kind == 'sentence' and field == 'boundary_rationale' for _count, kind, field, _fp, _ids in violations)


def test_slot_masked_semantic_gate_ignores_genuinely_distinct_small_set() -> None:
    rows = [
        {'decision_id': 'D-1', 'span': 'Ps.1.1-Ps.1.6', 'boundary_rationale': 'Beatitude and two-way contrast resolve when the closing knowledge formula judges both paths.'},
        {'decision_id': 'D-2', 'span': 'Ps.2.1-Ps.2.12', 'boundary_rationale': 'Four changing voices cooperate in one royal drama whose warning answers the nations opening revolt.'},
        {'decision_id': 'D-3', 'span': 'Ps.3.1-Ps.3.8', 'boundary_rationale': 'Complaint yields to shield confession and then petition before the final blessing widens toward the people.'},
    ]
    assert _semantic_constructor_fingerprints(rows) == []
def test_prose_alias_gate_rejects_embedded_rationale_and_defense_alias() -> None:
    chunk = _chunk(1, confidence='high')
    rationale = chunk['boundary_rationale']
    chunk['rejected_alternative'] = f'A nominal rival was recorded. {rationale} This does not analyze a rival.'
    chunk['confidence_basis'] = rationale
    chunk['defensible_basis'] = {'rationale': rationale}
    violations = _chunk_prose_aliases(chunk)
    assert 'rejected_alternative embeds the full boundary_rationale' in violations
    assert 'confidence_basis aliases boundary_rationale' in violations
    assert 'defensible_basis aliases boundary_rationale' in violations


def test_prose_alias_gate_accepts_independent_counterargument_and_basis() -> None:
    chunk = _chunk(1, confidence='high')
    assert _chunk_prose_aliases(chunk) == []
def test_validate_rejects_slot_masked_semantic_constructor_batch(tmp_path: Path) -> None:
    chunks = []
    for index in range(1, 11):
        chunk = _chunk(index, confidence='high' if index < 10 else 'medium')
        marker = f'Decision-local marker {index} closes one movement and opens another'
        chunk['deciding_marker_or_seam'] = marker
        chunk_span = chunk['span']
        chunk_form = chunk['literary_form']
        chunk['boundary_rationale'] = (
            f'{marker}. Consequently {chunk_span} receives a separate retrieval identity as '
            f'{chunk_form}; the numbered advisory remains evidence only.'
        )
        chunks.append(chunk)
    packets = [_packet(chunk) for chunk in chunks]
    _write_jsonl(tmp_path / 'book_chunks' / 'Test' / 'chunks.jsonl', chunks)
    _write_jsonl(tmp_path / 'reviews' / 'Test' / 'review_packets.jsonl', packets)
    errors, _summary = validate(tmp_path, 'Test')
    assert 'repeated slot-masked semantic chunk constructors' in '\n'.join(errors)
def test_semantic_gate_allows_repeated_formal_acrostic_observation() -> None:
    rows = []
    for index in range(12):
        rows.append({
            'decision_id': f'M7_sol-Ps-{index + 211:03d}',
            'local_function': f'letter_{index}_alphabetic_torah_stanza',
            'claim': f'WEB:Ps.119.{8 * index + 8}/WEB:Ps.119.{8 * index + 9}: Aleph/Beth OSHB=UXLC initials',
        })
    assert _semantic_constructor_fingerprints(rows) == []
def test_semantic_gate_allows_full_ledger_acrostic_review_claim() -> None:
    rows = []
    for index in range(12):
        rows.append({
            'decision_id': f'M7_sol-Ps-{index + 211:03d}',
            'literary_form': f'letter_{index}_alphabetic_torah_stanza',
            'claim': f'Ps.119.{8 * index + 1}-Ps.119.{8 * index + 8}: both Hebrew witnesses verify eight letter initials; no heading element is asserted.',
        })
    assert _semantic_constructor_fingerprints(rows) == []


