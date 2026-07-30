from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEWS = ROOT / "reviews" / "2Chr"
OUT = ROOT / "book_chunks" / "2Chr" / "chunks.jsonl"


def load(name: str) -> dict:
    return json.loads((REVIEWS / name).read_text(encoding="utf-8"))


def point(value: str) -> tuple[int, int]:
    value = value.replace("2Chr.", "")
    chapter, verse = value.split(".") if "." in value else value.split(":")
    return int(chapter), int(verse)


def span_pair(value: str) -> tuple[tuple[int, int], tuple[int, int]]:
    if "-" not in value:
        same = point(value)
        return same, same
    left, right = value.split("-")
    if ":" not in right and "." not in right:
        chapter = left.replace("2Chr.", "").replace(".", ":").split(":")[0]
        right = f"{chapter}:{right}"
    return point(left), point(right)


def full_span(value: str) -> str:
    (sc, sv), (ec, ev) = span_pair(value)
    return f"2Chr.{sc}.{sv}-2Chr.{ec}.{ev}"


def short_span(value: str) -> str:
    (sc, sv), (ec, ev) = span_pair(value)
    return f"{sc}:{sv}-{ec}:{ev}"


def overlaps(a: str, b: str) -> bool:
    a0, a1 = span_pair(a)
    b0, b1 = span_pair(b)
    return a0 <= b1 and b0 <= a1


def canonical_span(row: dict) -> str:
    return f"{row['start']}-{row['end']}"


hebrew_doc = load("blind_proposal_hebrew_v1.json")
literary_doc = load("blind_proposal_literary_v1.json")
canonical_doc = load("blind_proposal_canonical_premortem_v1.json")

hebrew = hebrew_doc["proposed_chunks"]
literary = literary_doc["proposal"]
canonical = canonical_doc["chunks"]

hebrew_spans = [full_span(row["span"]) for row in hebrew]
literary_spans = [row["span"] for row in literary]
canonical_spans = [canonical_span(row) for row in canonical]
hebrew_exact = set(hebrew_spans)
literary_exact = {full_span(span) for span in literary_spans}
canonical_exact = {full_span(span) for span in canonical_spans}

qere_points = [point(value) for value in hebrew_doc["qere_ketiv_evidence_only"]]

rows: list[dict] = []
for index, source in enumerate(canonical, 1):
    span = full_span(canonical_span(source))
    did = f"M7_sol-2Chr-{index:03d}"
    heb_overlaps = [row for row in hebrew if overlaps(span, full_span(row["span"]))]
    lit_overlaps = [short_span(item) for item in literary_spans if overlaps(span, item)]
    exact_all = span in hebrew_exact and span in literary_exact
    low = (
        not exact_all
        or source["confidence"].upper() == "LOW"
        or bool(source.get("exact_alternative"))
        or any(row["confidence"].upper() == "LOW" for row in heb_overlaps)
    )

    competing = (
        f"canonical exact alternative {source.get('exact_alternative', 'none stated')}; "
        f"Hebrew primary overlap {' + '.join(short_span(row['span']) for row in heb_overlaps)}; "
        f"Hebrew rejected alternatives {' | '.join(row['rejected_alternative'] for row in heb_overlaps)}; "
        f"literary primary overlap {' + '.join(lit_overlaps)}"
    )
    start, end = span_pair(span)
    qere_here = [
        f"{chapter}:{verse}"
        for chapter, verse in qere_points
        if start <= (chapter, verse) <= end
    ]
    hebrew_details = " | ".join(
        f"{row['span']} [{row['risk']}]: {row['deciding_marker']}"
        for row in heb_overlaps
    )
    language_hold = (
        f"{span}: canonical premortem risk: {source['risk']}. "
        f"Overlapping Hebrew evidence: {hebrew_details}. "
        f"Exact competing spans: {competing}. "
        + (f"Qere/ketiv evidence points within span: {', '.join(qere_here)}. " if qere_here else "")
        + "Hebrew paragraphing, lexical roots, names, numerals, textual notes, and translation choices "
        "are evidence only and do not select a reading or authorize this boundary."
    )
    relevant_maps = [
        item
        for item in hebrew_doc["web_mt_versification_mappings"]
        if overlaps(span, item["web"])
    ]
    if relevant_maps:
        language_hold += " Relevant exact versification mapping(s): " + "; ".join(
            f"WEB {item['web']} = MT {item['mt']}: {item['hold']}"
            for item in relevant_maps
        )

    form = source["literary_form"].strip()
    title = re.sub(r"\s+", " ", form).capitalize()
    status = "final_deferred_appeal" if low else "candidate_review_complete"
    holds = (
        ["deferred_human_or_external_ai", "external_provider_review_at_convergence"]
        if low
        else ["external_provider_review_at_convergence"]
    )
    row = {
        "model_id": "M7_sol",
        "book": "2Chr",
        "span": span,
        "chunk_index_in_book": index,
        "working_title": title,
        "literature_type_guess": form,
        "literary_form": form,
        "boundary_evidence_refs": [
            f"direct_read:eng-web:{span}",
            f"direct_read:oshb:2Chr.xml#{span}",
            f"direct_read:uxlc:2Chr.xml#{span}",
            "book_strategy/2Chr.md",
            "reviews/2Chr/blind_proposal_hebrew_v1.json",
            "reviews/2Chr/blind_proposal_literary_v1.json",
            "reviews/2Chr/blind_proposal_canonical_premortem_v1.json",
            "reviews/2Chr/peer_crosscheck_v1.json",
            "reviews/2Chr/boss_ruling_v1.json",
            "reviews/2Chr/decision_relations.jsonl",
        ],
        "strong_or_hebrew_tags_used": [
            "direct_hebrew_wording_considered",
            "web_mt_versification_preserved",
            "source_metadata_corrob_only",
            "roots_are_not_meaning",
            "original_language_is_not_boundary_authority",
        ],
        "wj_or_red_letter_considered": False,
        "frontier_flag_considered": True,
        "confidence": "low" if low else "medium",
        "decision_id": did,
        "deciding_marker_or_seam": source["macro_unit_rationale"].rstrip(".") + ".",
        "boundary_rationale": (
            f"Prefer the complete {form} unit {span}. "
            f"{source['macro_unit_rationale'].rstrip('.')}. "
            "Where blind proposals remain unresolved, this macro-unit implements the contract's larger-coherent-unit rule."
        ),
        "rejected_alternative": f"Preserved exact competing boundary evidence for {span}: {competing}.",
        "defensible_basis": (
            f"{did}: {source['macro_unit_rationale'].rstrip('.')}. "
            "The candidate rests on local scene, speaker, discourse, list-function, prayer/oracle, "
            "or regnal-closure evidence—not chapter headings, root etymology, chronology, harmonization, "
            "royal/cultic legitimacy, or later canonical reuse."
        ),
        "review_revision": 1,
        "review_status": status,
        "review_holds": holds,
        "non_authorizing": True,
        "candidate_internal_seams": [competing + "."],
        "original_language_translation_holds": [language_hold],
        "cross_reference_holds": [
            "Relations to Samuel-Kings, Psalms, prophetic books, Ezra-Nehemiah, or later reuse are "
            "recorded separately as evidence only; they cannot harmonize accounts or force boundary symmetry."
        ],
        "red_team_premortem_holds": [
            f"{span}: oversplit, chapter-fallback, harmonization, and chronology risks remain. "
            f"Exact competing spans: {competing}."
        ],
        "working_title_is_boundary_authority": False,
        "working_title_origin": "independent_2chronicles_three_primary_reconciliation_v1",
        "candidate_only": True,
        "review_evidence_summary": (
            f"{source['macro_unit_rationale'].rstrip('.')}. Candidate-only and non-authorizing."
        ),
        "red_team_questions": [
            f"Does the seam after {span.split('-')[1]} survive removal of headings and chapter numbers?",
            f"Does one of these exact alternatives better retain the governing function: {competing}?",
        ],
        "hard_passage_forecast": [language_hold],
    }
    if low:
        row["candidate_hold_state"] = "deferred_human_or_external_ai"
        row["candidate_hold_basis"] = "preserved_appeal"
    rows.append(row)

assert len(rows) == 58
assert [row["chunk_index_in_book"] for row in rows] == list(range(1, 59))

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
