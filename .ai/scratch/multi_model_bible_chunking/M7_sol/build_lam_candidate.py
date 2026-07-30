from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEWS = ROOT / "reviews" / "Lam"
OUT = ROOT / "book_chunks" / "Lam" / "chunks.jsonl"


def load(name: str) -> dict:
    return json.loads((REVIEWS / name).read_text(encoding="utf-8"))


def point(value: str) -> tuple[int, int]:
    value = value.replace("Lam.", "").replace(".", ":")
    chapter, verse = value.split(":")
    return int(chapter), int(verse)


def pair(value: str) -> tuple[tuple[int, int], tuple[int, int]]:
    left, right = value.split("-")
    return point(left), point(right)


def full(value: str) -> str:
    (c1, v1), (c2, v2) = pair(value)
    return f"Lam.{c1}.{v1}-Lam.{c2}.{v2}"


def overlaps(left: str, right: str) -> bool:
    l0, l1 = pair(left)
    r0, r1 = pair(right)
    return l0 <= r1 and r0 <= l1


hebrew_doc = load("blind_proposal_hebrew_textual_v1.json")
literary_doc = load("blind_proposal_literary_v1.json")
canonical_doc = load("blind_proposal_canonical_premortem_v1.json")
hebrew_rows = hebrew_doc["units"]
literary_rows = literary_doc["chunks"]
canonical_rows = canonical_doc["chunks"]
global_guard = hebrew_doc["evidence_only_guard"]
def render(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)


global_parents = (
    "Hebrew macro parents=" + " | ".join(render(x) for x in hebrew_doc.get("macro_parent_alternatives", []))
    + "; literary macro parents=" + " | ".join(render(x) for x in literary_doc.get("macro_parent_alternatives", []))
)
global_canonical = (
    "canonical premortem holds=" + " | ".join(render(x) for x in canonical_doc.get("premortem_holds", []))
    + "; canonical evidence-only relations=" + " | ".join(render(x) for x in canonical_doc.get("evidence_only_canonical_relations", []))
    + "; canonical hardest-boundary order=" + " | ".join(render(x) for x in canonical_doc.get("hardest_boundary_order", []))
    + "; canonical global guards=" + " | ".join(render(x) for x in canonical_doc.get("global_guards", []))
)

rows: list[dict] = []

for index, selected in enumerate(canonical_rows, 1):
    span = full(selected["span"])
    decision_id = f"M7_sol-Lam-{index:03d}"
    hebrew_overlaps = [row for row in hebrew_rows if overlaps(span, row["span"])]
    literary_overlaps = [row for row in literary_rows if overlaps(span, row["span"])]
    hebrew_evidence = " | ".join(
        f"{full(row['span'])}: form={row['literary_form']}; marker={row['deciding_marker']}; "
        f"risk={row['risk']}; rejected={row['rejected_alternative']}; "
        f"Hebrew/textual/translation evidence={row['hebrew_textual_translation_evidence']}; "
        f"global guard={global_guard}"
        for row in hebrew_overlaps
    )
    literary_evidence = " | ".join(
        f"{full(row['span'])}: title={row['title']}; form={row['literary_form']}; "
        f"marker={row['deciding_marker']}; risk={row['risk']}; rejected={row['rejected_alternative']}; "
        f"alternatives={'; '.join(row.get('exact_alternatives', [])) or 'none stated'}"
        for row in literary_overlaps
    )
    canonical_evidence = (
        f"{span}: form={selected['form']}; marker={selected['marker']}; risk={selected['risk']}; "
        f"rejected={selected['rejected_alternative']}; hold={selected['hold']}; "
        f"alternatives={'; '.join(selected.get('exact_alternatives', [])) or 'none stated'}"
    )
    competing = (
        f"selected larger canonical-premortem unit [{canonical_evidence}]; "
        f"overlapping Hebrew/textual alternatives [{hebrew_evidence}]; "
        f"overlapping literary alternatives [{literary_evidence}]; {global_parents}; {global_canonical}"
    )
    marker = selected["marker"].rstrip(".")
    form = selected["form"]
    language_hold = (
        f"{span}: {' | '.join(row['hebrew_textual_translation_evidence'] for row in hebrew_overlaps)}. "
        f"Risks: {' | '.join(row['risk'] for row in hebrew_overlaps)}. {global_guard} "
        "No preferred witness, emendation, speaker/addressee identity, qinah-meter theory, chronology, Jeremiah authorship/date, "
        "historicity, fulfillment, ethics, divine-agency ruling, canon or theology."
    )
    rows.append(
        {
            "model_id": "M7_sol",
            "book": "Lam",
            "span": span,
            "chunk_index_in_book": index,
            "working_title": re.sub(r"_+", " ", form).capitalize(),
            "literature_type_guess": form,
            "literary_form": form,
            "boundary_evidence_refs": [
                f"direct_read:eng-web:{span}",
                f"direct_read:oshb:Lam.xml#{span}",
                f"direct_read:uxlc:Lam.xml#{span}",
                "book_strategy/Lam.md",
                "reviews/Lam/blind_proposal_hebrew_textual_v1.json",
                "reviews/Lam/blind_proposal_literary_v1.json",
                "reviews/Lam/blind_proposal_canonical_premortem_v1.json",
                "reviews/Lam/peer_crosscheck_v1.json",
                "reviews/Lam/boss_ruling_v1.json",
                "reviews/Lam/decision_relations.jsonl",
            ],
            "strong_or_hebrew_tags_used": [
                "direct_Hebrew_acrostic_and_lament_form_considered",
                "MT_LXX_DSS_versions_and_pe_ayin_order_evidence_only",
                "speaker_authorship_history_and_theology_not_decided",
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
                "Where an internal acrostic block, voice, address, lament, prayer, wisdom-reflection or catalogue seam is disputed, "
                "retain the larger form-governed unit and preserve every exact alternative."
            ),
            "rejected_alternative": f"Preserved exact competing evidence for {span}: {competing}.",
            "defensible_basis": (
                f"{decision_id}: {marker}. Sustained voice/addressee, lament-to-prayer or wisdom turn, imperative, rhetorical question, acrostic block, "
                "image catalogue, repeated stanza, communal confession, direct address or petition closure "
                "- not chapters, source strata, later reuse, fulfillment or theology - supports this candidate."
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
                "identify voices, establish Jeremiah authorship/date, select readings, settle divine agency, force seams or theology."
            ],
            "red_team_premortem_holds": [
                f"{span}: chapter fallback, one-letter atomization, qinah-meter overreach, famous-verse proof-texting, Jeremiah/Kings harmonization, "
                f"witness preference, identity, strata, fulfillment, proof-texting and theology-smuggling risks. "
                f"Exact evidence: {competing}."
            ],
            "working_title_is_boundary_authority": False,
            "working_title_origin": "independent_lamentations_three_primary_larger_unit_reconciliation_v1",
            "candidate_only": True,
            "review_evidence_summary": marker + ". Candidate-only and non-authorizing.",
            "red_team_questions": [
                f"Does the seam after {span.split('-')[1]} survive removal of chapters, headings and later reuse?",
                f"Would an exact alternative better preserve voice, acrostic block, lament, prayer or catalogue integrity: {competing}?",
            ],
            "hard_passage_forecast": [language_hold],
            "candidate_hold_state": "deferred_human_or_external_ai",
            "candidate_hold_basis": "preserved_appeal",
        }
    )

assert len(rows) == 21
assert [row["chunk_index_in_book"] for row in rows] == list(range(1, 22))
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
