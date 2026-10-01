from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEWS = ROOT / "reviews" / "Song"
OUT = ROOT / "book_chunks" / "Song" / "chunks.jsonl"


def load(name: str) -> dict:
    return json.loads((REVIEWS / name).read_text(encoding="utf-8"))


def point(value: str) -> tuple[int, int]:
    value = value.replace("Song.", "").replace(".", ":")
    chapter, verse = value.split(":")
    return int(chapter), int(verse)


def pair(value: str) -> tuple[tuple[int, int], tuple[int, int]]:
    left, right = value.split("-")
    return point(left), point(right)


def full(value: str) -> str:
    (c1, v1), (c2, v2) = pair(value)
    return f"Song.{c1}.{v1}-Song.{c2}.{v2}"


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
    decision_id = f"M7_sol-Song-{index:03d}"
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
        f"{full(row['span'])}: form={row['form']}; marker={row['marker']}; risk={row['risk']}; "
        f"rejected={row['rejection']}; hold={row['hold']}; "
        f"alternatives={'; '.join(row.get('alternative', [])) or 'none stated'}"
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
        "Hebrew gender/number/person, suffixes, compact syntax, accents, qere/ketiv, rare imagery, "
        "WEB/MT/LXX numbering and speaker labels are evidence only. No preferred speaker, plot, "
        "gender identity, authorship, marriage/sexual ethic, allegorical/literal priority or theology."
    )
    rows.append(
        {
            "model_id": "M7_sol",
            "book": "Song",
            "span": span,
            "chunk_index_in_book": index,
            "working_title": re.sub(r"_+", " ", form).capitalize(),
            "literature_type_guess": form,
            "literary_form": form,
            "boundary_evidence_refs": [
                f"direct_read:eng-web:{span}",
                f"direct_read:oshb:Song.xml#{span}",
                f"direct_read:uxlc:Song.xml#{span}",
                "book_strategy/Song.md",
                "reviews/Song/blind_proposal_hebrew_textual_v1.json",
                "reviews/Song/blind_proposal_literary_v1.json",
                "reviews/Song/blind_proposal_canonical_premortem_v1.json",
                "reviews/Song/peer_crosscheck_v1.json",
                "reviews/Song/boss_ruling_v1.json",
                "reviews/Song/decision_relations.jsonl",
            ],
            "strong_or_hebrew_tags_used": [
                "direct_Hebrew_gender_number_and_lyric_form_considered",
                "speaker_labels_and_accents_evidence_only",
                "WEB_MT_LXX_versification_preserved",
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
                "Where speaker or scene assignment is disputed, retain the full lyric, dialogue, search, "
                "praise catalogue, invitation or adjuration-governed movement and preserve every alternative."
            ),
            "rejected_alternative": f"Preserved exact competing evidence for {span}: {competing}.",
            "defensible_basis": (
                f"{decision_id}: {marker}. Explicit address, response, setting, search/find, catalogue, "
                "invitation or refrain closure - not chapter numbering, supplied speakers, forced drama, "
                "allegory, later reuse or theology - supports this candidate."
            ),
            "review_revision": 1,
            "review_status": "final_deferred_appeal",
            "review_holds": ["deferred_human_or_external_ai", "external_provider_review_at_convergence"],
            "non_authorizing": True,
            "candidate_internal_seams": [competing + "."],
            "original_language_translation_holds": [language_hold],
            "cross_reference_holds": [
                "Relations to Genesis, Torah, royal/love psalms, Proverbs, prophetic marriage/vineyard "
                "imagery and later reuse are evidence only; they cannot identify speakers, determine plot, "
                "choose allegory/literal priority, settle ethics, force seams or authorize theology."
            ],
            "red_team_premortem_holds": [
                f"{span}: chapter fallback, line/metaphor atomization, supplied-speaker, forced-drama, "
                f"gender, authorship, marriage, erotic-sanitization, allegory and theology-smuggling risks. "
                f"Exact evidence: {competing}."
            ],
            "working_title_is_boundary_authority": False,
            "working_title_origin": "independent_song_three_primary_larger_unit_reconciliation_v1",
            "candidate_only": True,
            "review_evidence_summary": marker + ". Candidate-only and non-authorizing.",
            "red_team_questions": [
                f"Does the seam after {span.split('-')[1]} survive removal of chapter and supplied speaker labels?",
                f"Would an alternative better preserve the complete lyric/refrain function: {competing}?",
            ],
            "hard_passage_forecast": [language_hold],
            "candidate_hold_state": "deferred_human_or_external_ai",
            "candidate_hold_basis": "preserved_appeal",
        }
    )

assert len(rows) == 17
assert [row["chunk_index_in_book"] for row in rows] == list(range(1, 18))
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
