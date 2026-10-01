from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEWS = ROOT / "reviews" / "Ezra"
OUT = ROOT / "book_chunks" / "Ezra" / "chunks.jsonl"


def load(name: str) -> dict:
    return json.loads((REVIEWS / name).read_text(encoding="utf-8"))


def point(value: str) -> tuple[int, int]:
    value = value.replace("Ezra.", "")
    chapter, verse = value.split(".") if "." in value else value.split(":")
    return int(chapter), int(verse)


def span_pair(value: str) -> tuple[tuple[int, int], tuple[int, int]]:
    if "-" not in value:
        same = point(value)
        return same, same
    left, right = value.split("-")
    if ":" not in right and "." not in right:
        chapter = left.replace("Ezra.", "").replace(".", ":").split(":")[0]
        right = f"{chapter}:{right}"
    return point(left), point(right)


def full_span(value: str) -> str:
    (sc, sv), (ec, ev) = span_pair(value)
    return f"Ezra.{sc}.{sv}-Ezra.{ec}.{ev}"


def short_span(value: str) -> str:
    (sc, sv), (ec, ev) = span_pair(value)
    return f"{sc}:{sv}-{ec}:{ev}"


def overlaps(a: str, b: str) -> bool:
    a0, a1 = span_pair(a)
    b0, b1 = span_pair(b)
    return a0 <= b1 and b0 <= a1


def canonical_span(row: dict) -> str:
    return f"{row['start']}-{row['end']}"


canonical_doc = load("blind_proposal_canonical_premortem_v1.json")
literary_doc = load("blind_proposal_literary_v1.json")
language_doc = load("blind_proposal_hebrew_aramaic_v1.json")
canonical = canonical_doc["chunks"]
literary = literary_doc["proposal"]
language = language_doc["proposed_chunks"]

literary_spans = [row["span"] for row in literary]
language_spans = [full_span(row["span"]) for row in language]
literary_exact = {full_span(value) for value in literary_spans}
language_exact = set(language_spans)
qere_points = [point(value) for value in language_doc["qere_ketiv_evidence_only"]]

rows: list[dict] = []
for index, source in enumerate(canonical, 1):
    span = full_span(canonical_span(source))
    start, end = span_pair(span)
    did = f"M7_sol-Ezra-{index:03d}"
    lang_overlaps = [row for row in language if overlaps(span, row["span"])]
    lit_overlaps = [row for row in literary if overlaps(span, row["span"])]
    exact_all = span in language_exact and span in literary_exact
    low = (
        not exact_all
        or source["confidence"].upper() == "LOW"
        or bool(source.get("exact_alternative"))
        or any(row["confidence"].upper() == "LOW" for row in lang_overlaps)
        or any(row["confidence"].upper() == "LOW" for row in lit_overlaps)
    )

    canonical_alt = source.get("exact_alternative", "none stated")
    lang_chosen = " + ".join(short_span(row["span"]) for row in lang_overlaps)
    lang_rejected = " | ".join(row["rejected_alternative"] for row in lang_overlaps)
    lit_chosen = " + ".join(short_span(row["span"]) for row in lit_overlaps)
    lit_internal = " | ".join(
        alt
        for row in lit_overlaps
        for alt in row.get("exact_internal_alternatives", [])
    ) or "none stated"
    competing = (
        f"canonical exact alternative {canonical_alt}; "
        f"Hebrew/Aramaic primary overlap {lang_chosen}; "
        f"Hebrew/Aramaic rejected alternatives {lang_rejected}; "
        f"literary primary overlap {lit_chosen}; "
        f"literary exact internal alternatives {lit_internal}"
    )

    routes = [
        row for row in language_doc["language_routing"] if overlaps(span, row["span"])
    ]
    route_text = " | ".join(
        f"{row['span']} {row['language']}: {row['hold']}" for row in routes
    )
    qere_here = [
        f"{chapter}:{verse}"
        for chapter, verse in qere_points
        if start <= (chapter, verse) <= end
    ]
    detail = " | ".join(
        f"{row['span']} [{row['risk']}]: {row['deciding_marker']}"
        for row in lang_overlaps
    )
    language_hold = (
        f"{span}: {route_text}. Overlapping source-language evidence: {detail}. "
        f"Exact competing spans: {competing}. "
        + (f"Qere/ketiv evidence points: {', '.join(qere_here)}. " if qere_here else "")
        + "Hebrew/Imperial-Aramaic language, lexical roots, document formulas, names, titles, "
        "numbers, and witness metadata are evidence only; no preferred reading, chronology, "
        "ethnic/marriage doctrine, cultic/legal authority, or theological ruling."
    )

    # Normalize one editorial typo from the immutable blind proposal without altering its evidence.
    form = source["literary_form"].replace("aramic", "aramaic")
    marker = source["macro_unit_rationale"].rstrip(".")
    row = {
        "model_id": "M7_sol",
        "book": "Ezra",
        "span": span,
        "chunk_index_in_book": index,
        "working_title": re.sub(r"_+", " ", form).capitalize(),
        "literature_type_guess": form,
        "literary_form": form,
        "boundary_evidence_refs": [
            f"direct_read:eng-web:{span}",
            f"direct_read:oshb:Ezra.xml#{span}",
            f"direct_read:uxlc:Ezra.xml#{span}",
            "book_strategy/Ezra.md",
            "reviews/Ezra/blind_proposal_hebrew_aramaic_v1.json",
            "reviews/Ezra/blind_proposal_literary_v1.json",
            "reviews/Ezra/blind_proposal_canonical_premortem_v1.json",
            "reviews/Ezra/peer_crosscheck_v1.json",
            "reviews/Ezra/boss_ruling_v1.json",
            "reviews/Ezra/decision_relations.jsonl",
        ],
        "strong_or_hebrew_tags_used": [
            "direct_Hebrew_and_Imperial_Aramaic_wording_considered",
            "language_switch_is_evidence_not_authority",
            "source_metadata_corrob_only",
            "roots_are_not_meaning",
        ],
        "wj_or_red_letter_considered": False,
        "frontier_flag_considered": True,
        "confidence": "low" if low else "medium",
        "decision_id": did,
        "deciding_marker_or_seam": marker + ".",
        "boundary_rationale": (
            f"Prefer the complete {form} unit {span}. {marker}. "
            "Where blind proposals remain unresolved, retain the larger coherent macro-unit."
        ),
        "rejected_alternative": f"Preserved exact competing boundary evidence for {span}: {competing}.",
        "defensible_basis": (
            f"{did}: {marker}. Local document-response, scene, speaker, prayer-response, "
            "register-function, journey, assembly, or closure evidence—not headings, language alone, "
            "imperial chronology, ethnicity, marriage doctrine, or canonical harmonization—supports this candidate."
        ),
        "review_revision": 1,
        "review_status": "final_deferred_appeal" if low else "candidate_review_complete",
        "review_holds": (
            ["deferred_human_or_external_ai", "external_provider_review_at_convergence"]
            if low
            else ["external_provider_review_at_convergence"]
        ),
        "non_authorizing": True,
        "candidate_internal_seams": [competing + "."],
        "original_language_translation_holds": [language_hold],
        "cross_reference_holds": [
            "Relations to Torah, Kings-Chronicles, Haggai-Zechariah, Nehemiah, Daniel, Esther, "
            "and prophetic restoration texts are evidence only and cannot harmonize lists or chronology, "
            "define ethnicity, select witnesses, force boundary symmetry, or authorize doctrine."
        ],
        "red_team_premortem_holds": [
            f"{span}: chapter fallback, document detachment, register atomization, language-switch "
            f"overreach, imperial harmonization, and doctrine-smuggling risks. Exact alternatives: {competing}."
        ],
        "working_title_is_boundary_authority": False,
        "working_title_origin": "independent_ezra_three_primary_reconciliation_v1",
        "candidate_only": True,
        "review_evidence_summary": marker + ". Candidate-only and non-authorizing.",
        "red_team_questions": [
            f"Does the seam after {span.split('-')[1]} survive removal of headings and chapter numbers?",
            f"Does one of these exact alternatives better preserve document-with-response or register function: {competing}?",
        ],
        "hard_passage_forecast": [language_hold],
    }
    if low:
        row["candidate_hold_state"] = "deferred_human_or_external_ai"
        row["candidate_hold_basis"] = "preserved_appeal"
    rows.append(row)

assert len(rows) == 16
assert [row["chunk_index_in_book"] for row in rows] == list(range(1, 17))
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
