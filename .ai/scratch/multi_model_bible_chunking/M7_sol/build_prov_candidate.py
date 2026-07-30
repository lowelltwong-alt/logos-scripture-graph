from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEWS = ROOT / "reviews" / "Prov"
OUT = ROOT / "book_chunks" / "Prov" / "chunks.jsonl"


def load(name: str) -> dict:
    return json.loads((REVIEWS / name).read_text(encoding="utf-8"))


def point(value: str) -> tuple[int, int]:
    value = value.replace("Prov.", "").replace(".", ":")
    chapter, verse = value.split(":")
    return int(chapter), int(verse)


def pair(value: str) -> tuple[tuple[int, int], tuple[int, int]]:
    left, right = value.split("-")
    return point(left), point(right)


def full(value: str) -> str:
    (c1, v1), (c2, v2) = pair(value)
    return f"Prov.{c1}.{v1}-Prov.{c2}.{v2}"


def short(value: str) -> str:
    (c1, v1), (c2, v2) = pair(value)
    return f"{c1}:{v1}-{c2}:{v2}"


def overlaps(left: str, right: str) -> bool:
    l0, l1 = pair(left)
    r0, r1 = pair(right)
    return l0 <= r1 and r0 <= l1


hebrew_doc = load("blind_proposal_hebrew_textual_v1.json")
literary_doc = load("blind_proposal_literary_v1.json")
canonical_doc = load("blind_proposal_canonical_premortem_v1.json")
hebrew_rows = hebrew_doc["proposed_chunks"]
literary_rows = literary_doc["proposal"]
canonical_rows = canonical_doc["chunks"]

rows: list[dict] = []
for index, selected in enumerate(hebrew_rows, 1):
    span = full(selected["span"])
    decision_id = f"M7_sol-Prov-{index:03d}"
    literary_overlaps = [row for row in literary_rows if overlaps(span, row["span"])]
    canonical_overlaps = [row for row in canonical_rows if overlaps(span, row["span"])]

    literary_evidence = " | ".join(
        f"{full(row['span'])}: form={row['literary_form']}; marker={row['deciding_marker']}; "
        f"risk={row['risk']}; rejected={row['rejected_alternative']}; "
        f"alternatives={'; '.join(row.get('exact_alternatives', [])) or 'none stated'}"
        for row in literary_overlaps
    )
    canonical_evidence = " | ".join(
        f"{full(row['span'])}: form={row['form']}; marker={row['marker']}; risk={row['risk']}; "
        f"rejected={row['rejection']}; hold={row['hold']}; "
        f"alternatives={'; '.join(row.get('alternative', [])) or 'none stated'}"
        for row in canonical_overlaps
    )
    hebrew_evidence = (
        f"{span}: form={selected['literary_form']}; marker={selected['deciding_marker']}; "
        f"risk={selected['risk']}; rejected={selected['rejected_alternative']}; "
        f"Hebrew/textual evidence={selected['hebrew_textual_evidence']}; "
        f"guard={selected['evidence_only_guard']}"
    )
    competing = (
        f"selected larger Hebrew/textual unit [{hebrew_evidence}]; "
        f"overlapping literary alternatives [{literary_evidence}]; "
        f"overlapping canonical-premortem alternatives [{canonical_evidence}]"
    )
    marker = selected["deciding_marker"].rstrip(".")
    form = selected["literary_form"]
    language_hold = (
        f"{span}: {selected['hebrew_textual_evidence']} Risk: {selected['risk']}. "
        "Hebrew syntax, parallelism, accents, morphology, qere/ketiv, roots, semantic ranges, "
        "WEB/MT/LXX differences, names and superscriptions are evidence only. No preferred reading, "
        "authorship, chronology, gender referent, personification ontology, ethics, doctrine or theology."
    )
    row = {
        "model_id": "M7_sol",
        "book": "Prov",
        "span": span,
        "chunk_index_in_book": index,
        "working_title": re.sub(r"_+", " ", form).capitalize(),
        "literature_type_guess": form,
        "literary_form": form,
        "boundary_evidence_refs": [
            f"direct_read:eng-web:{span}",
            f"direct_read:oshb:Prov.xml#{span}",
            f"direct_read:uxlc:Prov.xml#{span}",
            "book_strategy/Prov.md",
            "reviews/Prov/blind_proposal_hebrew_textual_v1.json",
            "reviews/Prov/blind_proposal_literary_v1.json",
            "reviews/Prov/blind_proposal_canonical_premortem_v1.json",
            "reviews/Prov/peer_crosscheck_v1.json",
            "reviews/Prov/boss_ruling_v1.json",
            "reviews/Prov/decision_relations.jsonl",
        ],
        "strong_or_hebrew_tags_used": [
            "direct_Hebrew_wisdom_form_considered",
            "parallelism_and_collection_form_evidence_only",
            "WEB_MT_LXX_pressure_preserved",
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
            "Where smaller aphoristic clusters are disputed, retain the explicit instruction, speech, "
            "numerical form, poem or superscription-governed collection and preserve every smaller alternative."
        ),
        "rejected_alternative": f"Preserved exact competing evidence for {span}: {competing}.",
        "defensible_basis": (
            f"{decision_id}: {marker}. Explicit speaker, instruction, superscription, list function, "
            "numerical formula or alphabetic-poem closure - not chapter numbering, famous-verse isolation, "
            "later reuse or theology - supports this candidate."
        ),
        "review_revision": 1,
        "review_status": "final_deferred_appeal",
        "review_holds": [
            "deferred_human_or_external_ai",
            "external_provider_review_at_convergence",
        ],
        "non_authorizing": True,
        "candidate_internal_seams": [competing + "."],
        "original_language_translation_holds": [language_hold],
        "cross_reference_holds": [
            "Relations to Torah, royal narratives, Job, Psalms, Ecclesiastes, prophets and later reuse "
            "are evidence only; they cannot identify Wisdom, settle authorship, chronology, ethics, "
            "preferred readings, seams or theology."
        ],
        "red_team_premortem_holds": [
            f"{span}: chapter fallback, couplet atomization, weak thematic clustering, famous-verse "
            f"proof-texting, authorship and personified-Wisdom theology-smuggling risks. Exact evidence: {competing}."
        ],
        "working_title_is_boundary_authority": False,
        "working_title_origin": "independent_proverbs_three_primary_larger_unit_reconciliation_v1",
        "candidate_only": True,
        "review_evidence_summary": marker + ". Candidate-only and non-authorizing.",
        "red_team_questions": [
            f"Does the seam after {span.split('-')[1]} survive removal of chapters and headings?",
            f"Would any exact smaller alternative better preserve a complete instruction, speech, cluster or list: {competing}?",
        ],
        "hard_passage_forecast": [language_hold],
        "candidate_hold_state": "deferred_human_or_external_ai",
        "candidate_hold_basis": "preserved_appeal",
    }
    rows.append(row)

assert len(rows) == 36
assert [row["chunk_index_in_book"] for row in rows] == list(range(1, 37))
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
            "accepted": sum(row["confidence"] != "low" for row in rows),
        }
    )
)
