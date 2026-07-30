from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEWS = ROOT / "reviews" / "Eccl"
OUT = ROOT / "book_chunks" / "Eccl" / "chunks.jsonl"


def load(name: str) -> dict:
    return json.loads((REVIEWS / name).read_text(encoding="utf-8"))


def point(value: str) -> tuple[int, int]:
    value = value.replace("Eccl.", "").replace(".", ":")
    chapter, verse = value.split(":")
    return int(chapter), int(verse)


def pair(value: str) -> tuple[tuple[int, int], tuple[int, int]]:
    left, right = value.split("-")
    return point(left), point(right)


def full(value: str) -> str:
    (c1, v1), (c2, v2) = pair(value)
    return f"Eccl.{c1}.{v1}-Eccl.{c2}.{v2}"


def overlaps(left: str, right: str) -> bool:
    l0, l1 = pair(left)
    r0, r1 = pair(right)
    return l0 <= r1 and r0 <= l1


hebrew_rows = load("blind_proposal_hebrew_textual_v1.json")["proposed_chunks"]
literary_rows = load("blind_proposal_literary_v1.json")["proposal"]
canonical_rows = load("blind_proposal_canonical_premortem_v1.json")["chunks"]
rows: list[dict] = []

for index, selected in enumerate(hebrew_rows, 1):
    span = full(selected["span"])
    decision_id = f"M7_sol-Eccl-{index:03d}"
    literary_overlaps = [row for row in literary_rows if overlaps(span, row["span"])]
    canonical_overlaps = [row for row in canonical_rows if overlaps(span, row["span"])]
    hebrew_evidence = (
        f"{span}: form={selected['literary_form']}; marker={selected['deciding_marker']}; "
        f"risk={selected['risk']}; rejected={selected['rejected_alternative']}; "
        f"Hebrew/textual/translation evidence={selected['hebrew_textual_translation_evidence']}; "
        f"guard={selected['evidence_only_guard']}"
    )
    literary_evidence = " | ".join(
        f"{full(row['span'])}: title={row['title']}; form={row['literary_form']}; "
        f"marker={row['deciding_marker']}; risk={row['risk']}; "
        f"rejected={row['rejected_alternative']}; "
        f"alternatives={'; '.join(row.get('exact_alternatives', [])) or 'none stated'}"
        for row in literary_overlaps
    )
    canonical_evidence = " | ".join(
        f"{full(row['span'])}: form={row['form']}; marker={row['deciding_marker']}; "
        f"risk={row['premortem_risk']}; rejected={row['rejected_alternative']}; "
        f"hold={row['hold']}; alternatives={'; '.join(row.get('exact_alternatives', [])) or 'none stated'}"
        for row in canonical_overlaps
    )
    competing = (
        f"selected larger Hebrew/textual unit [{hebrew_evidence}]; "
        f"overlapping literary alternatives [{literary_evidence}]; "
        f"overlapping canonical-premortem alternatives [{canonical_evidence}]"
    )
    marker = selected["deciding_marker"].rstrip(".")
    form = selected["literary_form"]
    language_hold = (
        f"{span}: {selected['hebrew_textual_translation_evidence']} Risk: {selected['risk']}. "
        "Hebrew syntax, voice, morphology, accents, qere/ketiv, hebel/yitron semantic range, "
        "WEB/MT/LXX numbering and textual differences are evidence only. No preferred reading, "
        "speaker/editor reconstruction, authorship, chronology, gender ruling, afterlife, ethics or theology."
    )
    rows.append(
        {
            "model_id": "M7_sol",
            "book": "Eccl",
            "span": span,
            "chunk_index_in_book": index,
            "working_title": re.sub(r"_+", " ", form).capitalize(),
            "literature_type_guess": form,
            "literary_form": form,
            "boundary_evidence_refs": [
                f"direct_read:eng-web:{span}",
                f"direct_read:oshb:Eccl.xml#{span}",
                f"direct_read:uxlc:Eccl.xml#{span}",
                "book_strategy/Eccl.md",
                "reviews/Eccl/blind_proposal_hebrew_textual_v1.json",
                "reviews/Eccl/blind_proposal_literary_v1.json",
                "reviews/Eccl/blind_proposal_canonical_premortem_v1.json",
                "reviews/Eccl/peer_crosscheck_v1.json",
                "reviews/Eccl/boss_ruling_v1.json",
                "reviews/Eccl/decision_relations.jsonl",
            ],
            "strong_or_hebrew_tags_used": [
                "direct_Hebrew_Qohelet_discourse_considered",
                "voice_refrain_and_numbering_evidence_only",
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
                "Where voice, refrain or saying-chain seams are disputed, retain the larger investigation, "
                "poem, observation/refrain movement or epilogue and preserve every smaller alternative."
            ),
            "rejected_alternative": f"Preserved exact competing evidence for {span}: {competing}.",
            "defensible_basis": (
                f"{decision_id}: {marker}. Explicit frame, first-person quest, observation, rhetorical "
                "question, refrain, poem or epilogue closure - not chapter numbering, a fixed hebel gloss, "
                "hypothetical editor, later reuse or theology - supports this candidate."
            ),
            "review_revision": 1,
            "review_status": "final_deferred_appeal",
            "review_holds": ["deferred_human_or_external_ai", "external_provider_review_at_convergence"],
            "non_authorizing": True,
            "candidate_internal_seams": [competing + "."],
            "original_language_translation_holds": [language_hold],
            "cross_reference_holds": [
                "Relations to Genesis, Torah, royal narratives, Job, Psalms, Proverbs, prophets and later "
                "reuse are evidence only; they cannot identify Qohelet, settle voice, authorship, chronology, "
                "ethics, afterlife, preferred readings, seams or theology."
            ],
            "red_team_premortem_holds": [
                f"{span}: chapter fallback, refrain detachment, aphorism atomization, fixed-gloss, "
                f"voice/editor, autobiography, proof-texting, harmonization and theology-smuggling risks. "
                f"Exact evidence: {competing}."
            ],
            "working_title_is_boundary_authority": False,
            "working_title_origin": "independent_ecclesiastes_three_primary_larger_unit_reconciliation_v1",
            "candidate_only": True,
            "review_evidence_summary": marker + ". Candidate-only and non-authorizing.",
            "red_team_questions": [
                f"Does the seam after {span.split('-')[1]} survive removal of chapter divisions and headings?",
                f"Would an exact smaller alternative better preserve voice, refrain or rhetorical closure: {competing}?",
            ],
            "hard_passage_forecast": [language_hold],
            "candidate_hold_state": "deferred_human_or_external_ai",
            "candidate_hold_basis": "preserved_appeal",
        }
    )

assert len(rows) == 29
assert [row["chunk_index_in_book"] for row in rows] == list(range(1, 30))
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
