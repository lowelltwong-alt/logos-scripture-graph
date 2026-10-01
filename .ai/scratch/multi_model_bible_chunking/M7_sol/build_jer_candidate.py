from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEWS = ROOT / "reviews" / "Jer"
OUT = ROOT / "book_chunks" / "Jer" / "chunks.jsonl"


def load(name: str) -> dict:
    return json.loads((REVIEWS / name).read_text(encoding="utf-8"))


def point(value: str) -> tuple[int, int]:
    value = value.replace("Jer.", "").replace(".", ":")
    chapter, verse = value.split(":")
    return int(chapter), int(verse)


def pair(value: str) -> tuple[tuple[int, int], tuple[int, int]]:
    left, right = value.split("-")
    return point(left), point(right)


def overlaps(left: str, right: str) -> bool:
    l0, l1 = pair(left)
    r0, r1 = pair(right)
    return l0 <= r1 and r0 <= l1


hebrew_doc = load("blind_proposal_hebrew_textual_v1.json")
canonical_doc = load("blind_proposal_canonical_premortem_v1.json")
hebrew_rows = hebrew_doc["proposed_chunks"]
canonical_rows = canonical_doc["chunks"]
global_guard = hebrew_doc["evidence_only_guard"]
global_parents = " | ".join(hebrew_doc.get("macro_parent_alternatives", []))
failed_literary_attempts = (
    "Three dedicated literary-primary attempts failed to materialize a validated proposal and "
    "therefore count as no vote; their unvalidated outlines were not imported or inferred."
)
rows: list[dict] = []

for index, selected in enumerate(canonical_rows, 1):
    span = selected["span"]
    decision_id = f"M7_sol-Jer-{index:03d}"
    hebrew_overlaps = [row for row in hebrew_rows if overlaps(span, row["span"])]
    assert hebrew_overlaps, span
    hebrew_evidence = " | ".join(
        f"{row['span']}: form={row['literary_form']}; marker={row['deciding_marker']}; "
        f"risk={row['risk']}; rejected={row['rejected_alternative']}; "
        f"Hebrew/textual/translation evidence={row['hebrew_textual_translation_evidence']}"
        for row in hebrew_overlaps
    )
    alternatives = "; ".join(selected.get("exact_alternatives", [])) or "none stated"
    canonical_evidence = (
        f"{span}: form={selected['form']}; marker={selected['marker']}; risk={selected['risk']}; "
        f"rejected={selected['rejected_alternative']}; hold={selected['hold']}; "
        f"alternatives={alternatives}"
    )
    competing = (
        f"selected larger canonical-premortem unit [{canonical_evidence}]; "
        f"overlapping Hebrew/textual alternatives [{hebrew_evidence}]; "
        f"Hebrew macro parents [{global_parents}]. {failed_literary_attempts}"
    )
    marker = selected["marker"].rstrip(".")
    form = selected["form"]
    language_hold = (
        f"{span}: {' | '.join(row['hebrew_textual_translation_evidence'] for row in hebrew_overlaps)}. "
        f"Risks: {' | '.join(row['risk'] for row in hebrew_overlaps)}. {global_guard} "
        "No preferred MT/LXX/DSS witness, Greek/Hebrew order, emendation, speaker identity, chronology, "
        "authorship/redaction stratum, historicity, fulfillment, ethics, divine-agency ruling, canon or theology."
    )
    rows.append(
        {
            "model_id": "M7_sol",
            "book": "Jer",
            "span": span,
            "chunk_index_in_book": index,
            "working_title": re.sub(r"_+", " ", form).capitalize(),
            "literature_type_guess": form,
            "literary_form": form,
            "boundary_evidence_refs": [
                f"direct_read:eng-web:{span}",
                f"direct_read:oshb:Jer.xml#{span}",
                f"direct_read:uxlc:Jer.xml#{span}",
                "book_strategy/Jer.md",
                "reviews/Jer/blind_proposal_hebrew_textual_v1.json",
                "reviews/Jer/blind_proposal_canonical_premortem_v1.json",
                "reviews/Jer/peer_crosscheck_v1.json",
                "reviews/Jer/boss_ruling_v1.json",
                "reviews/Jer/decision_relations.jsonl",
            ],
            "strong_or_hebrew_tags_used": [
                "direct_Hebrew_prophetic_form_considered",
                "MT_LXX_DSS_order_and_variants_evidence_only",
                "speaker_chronology_strata_fulfillment_not_decided",
                "roots_are_not_meaning",
                "source_metadata_corrob_only",
            ],
            "wj_or_red_letter_considered": False,
            "frontier_flag_considered": True,
            "confidence": "low",
            "decision_id": decision_id,
            "deciding_marker_or_seam": marker + ".",
            "boundary_rationale": (
                f"Prefer the complete larger {form} unit {span}. {marker}. "
                "Where an internal oracle, lament, confession, sign-act, prose scene, letter, scroll, "
                "nation oracle or appendix seam is disputed, retain the larger form-governed unit and "
                "preserve every exact alternative."
            ),
            "rejected_alternative": f"Preserved exact competing evidence for {span}: {competing}.",
            "defensible_basis": (
                f"{decision_id}: {marker}. Superscription, word-event, vision question, vocative, addressee "
                "change, sign command/performance/interpretation, date/scene reset, letter/scroll frame, "
                "poetry-prose transition, nation heading or appendix frame—not chapter fallback, witness "
                "preference, reconstructed chronology, later reuse or theology—supports this candidate."
            ),
            "review_revision": 1,
            "review_status": "final_deferred_appeal",
            "review_holds": ["deferred_human_or_external_ai", "external_provider_review_at_convergence"],
            "non_authorizing": True,
            "candidate_internal_seams": [competing + "."],
            "original_language_translation_holds": [language_hold],
            "cross_reference_holds": [
                "Relations to Torah, Samuel-Kings/Chronicles, Psalms, wisdom, other prophets and later "
                "canonical reuse are evidence only; they cannot harmonize Kings, settle chronology/authorship, "
                "identify speakers, select MT/LXX/DSS readings or order, claim fulfillment, force seams or theology."
            ],
            "red_team_premortem_holds": [
                f"{span}: chapter fallback, formula over-split, sign/narrative detachment, chronology repair, "
                f"Kings harmonization, witness/order preference, speaker/identity/strata/fulfillment, proof-texting "
                f"and theology-smuggling risks. Exact evidence: {competing}."
            ],
            "working_title_is_boundary_authority": False,
            "working_title_origin": "independent_jeremiah_two_valid_primary_larger_unit_reconciliation_v1",
            "candidate_only": True,
            "review_evidence_summary": marker + ". Candidate-only and non-authorizing.",
            "red_team_questions": [
                f"Does the seam after {span.split('-')[1]} survive removal of chapters, headings and later reuse?",
                f"Would a preserved Hebrew/textual alternative better retain the complete literary movement: {competing}?",
            ],
            "hard_passage_forecast": [language_hold],
            "candidate_hold_state": "deferred_human_or_external_ai",
            "candidate_hold_basis": "preserved_appeal",
        }
    )

assert len(rows) == 99
assert [row["chunk_index_in_book"] for row in rows] == list(range(1, 100))
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
    encoding="utf-8",
    newline="\n",
)
print(
    json.dumps(
        {
            "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
            "chunks": len(rows),
            "low": sum(row["confidence"] == "low" for row in rows),
        }
    )
)
