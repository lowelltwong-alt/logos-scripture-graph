from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEWS = ROOT / "reviews" / "Neh"
OUT = ROOT / "book_chunks" / "Neh" / "chunks.jsonl"


def load(name: str) -> dict:
    return json.loads((REVIEWS / name).read_text(encoding="utf-8"))


def point(value: str) -> tuple[int, int]:
    value = value.replace("Neh.", "")
    chapter, verse = value.split(".") if "." in value else value.split(":")
    return int(chapter), int(verse)


def span_pair(value: str) -> tuple[tuple[int, int], tuple[int, int]]:
    if "-" not in value:
        same = point(value)
        return same, same
    left, right = value.split("-")
    if ":" not in right and "." not in right:
        chapter = left.replace("Neh.", "").replace(".", ":").split(":")[0]
        right = f"{chapter}:{right}"
    return point(left), point(right)


def full_span(value: str) -> str:
    (sc, sv), (ec, ev) = span_pair(value)
    return f"Neh.{sc}.{sv}-Neh.{ec}.{ev}"


def short_span(value: str) -> str:
    (sc, sv), (ec, ev) = span_pair(value)
    return f"{sc}:{sv}-{ec}:{ev}"


def overlaps(a: str, b: str) -> bool:
    a0, a1 = span_pair(a)
    b0, b1 = span_pair(b)
    return a0 <= b1 and b0 <= a1


def joined_span(start: str, end: str) -> str:
    return f"{start}-{end}"


canonical_doc = load("blind_proposal_canonical_premortem_v1.json")
literary_doc = load("blind_proposal_literary_v1.json")
hebrew_doc = load("blind_proposal_hebrew_v1.json")
canonical = canonical_doc["chunks"]
literary = literary_doc["proposal"]
hebrew = hebrew_doc["chunks"]

literary_exact = {full_span(row["span"]) for row in literary}
hebrew_exact = {
    full_span(joined_span(row["start_ref"], row["end_ref"])) for row in hebrew
}

rows: list[dict] = []
for index, source in enumerate(canonical, 1):
    span = full_span(joined_span(source["start"], source["end"]))
    did = f"M7_sol-Neh-{index:03d}"
    heb_overlaps = [
        row
        for row in hebrew
        if overlaps(span, joined_span(row["start_ref"], row["end_ref"]))
    ]
    lit_overlaps = [row for row in literary if overlaps(span, row["span"])]
    exact_all = span in hebrew_exact and span in literary_exact
    low = (
        not exact_all
        or source["confidence"].upper() == "LOW"
        or bool(source.get("exact_alternative"))
        or any(row["confidence"].upper() == "LOW" or row.get("low_hold") for row in heb_overlaps)
        or any(row["confidence"].upper() == "LOW" for row in lit_overlaps)
    )

    canonical_alt = source.get("exact_alternative", "none stated")
    heb_chosen = " + ".join(
        short_span(joined_span(row["start_ref"], row["end_ref"])) for row in heb_overlaps
    )
    heb_rejected = " | ".join(row["rejected_alternative"] for row in heb_overlaps)
    heb_low_holds = " | ".join(
        f"{row['decision_id']} {row['start_ref']}-{row['end_ref']}: {row['low_hold']}"
        for row in heb_overlaps
        if row.get("low_hold")
    ) or "none stated"
    lit_chosen = " + ".join(short_span(row["span"]) for row in lit_overlaps)
    lit_internal = " | ".join(
        alt
        for row in lit_overlaps
        for alt in row.get("exact_internal_alternatives", [])
    ) or "none stated"
    competing = (
        f"canonical exact alternative {canonical_alt}; "
        f"Hebrew primary overlap {heb_chosen}; "
        f"Hebrew rejected alternatives {heb_rejected}; "
        f"Hebrew low holds {heb_low_holds}; "
        f"literary primary overlap {lit_chosen}; "
        f"literary exact internal alternatives {lit_internal}"
    )

    mappings = [
        hold
        for hold in hebrew_doc["translation_versification_holds"]
        if overlaps(span, hold["web_span"])
    ]
    mapping_text = " | ".join(
        f"{hold['mt_mapping']}: {hold['reason']}" for hold in mappings
    ) or "no cross-system numbering offset identified for this span"
    hebrew_detail = " | ".join(
        f"{row['start_ref']}-{row['end_ref']} [{row['confidence']}]: "
        f"{row['deciding_marker_or_seam']}; hold={row.get('low_hold') or 'none'}"
        for row in heb_overlaps
    )
    language_hold = (
        f"{span}: overlapping Hebrew evidence: {hebrew_detail}. "
        f"WEB/MT mapping evidence: {mapping_text}. Exact competing spans: {competing}. "
        "Hebrew wording, qere/ketiv, accents, Persian/Aramaic terms, names, lists, numbers, "
        "memoir voice, and document formulas are evidence only; no preferred reading, chronology, "
        "identity reconstruction, ethnic/marriage/Sabbath doctrine, cultic/legal authority, "
        "imprecatory theology, or providential ruling."
    )

    form = source["literary_form"]
    marker = source["macro_unit_rationale"].rstrip(".")
    row = {
        "model_id": "M7_sol",
        "book": "Neh",
        "span": span,
        "chunk_index_in_book": index,
        "working_title": re.sub(r"_+", " ", form).capitalize(),
        "literature_type_guess": form,
        "literary_form": form,
        "boundary_evidence_refs": [
            f"direct_read:eng-web:{span}",
            f"direct_read:oshb:Neh.xml#{span}",
            f"direct_read:uxlc:Neh.xml#{span}",
            "book_strategy/Neh.md",
            "reviews/Neh/blind_proposal_hebrew_v1.json",
            "reviews/Neh/blind_proposal_literary_v1.json",
            "reviews/Neh/blind_proposal_canonical_premortem_v1.json",
            "reviews/Neh/peer_crosscheck_v1.json",
            "reviews/Neh/boss_ruling_v1.json",
            "reviews/Neh/decision_relations.jsonl",
        ],
        "strong_or_hebrew_tags_used": [
            "direct_Hebrew_wording_considered",
            "WEB_MT_versification_preserved",
            "qere_ketiv_evidence_only",
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
            f"{did}: {marker}. Local memoir, report-prayer, petition-response, register-function, "
            "opposition-response, assembly, covenant, dedication, reform, or remembrance-prayer "
            "evidence—not headings, chronology, identity, list harmonization, or doctrine—supports this candidate."
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
            "Relations to Torah, Kings-Chronicles, Ezra, Psalms, prophets, Daniel, Esther, and later "
            "reuse are evidence only and cannot harmonize lists or chronology, define ethnicity, "
            "select witnesses, force boundary symmetry, or authorize legal/cultic/theological conclusions."
        ],
        "red_team_premortem_holds": [
            f"{span}: chapter fallback, register atomization, prayer proof-texting, memoir-voice "
            f"overreach, Ezra-list harmonization, chronology, and doctrine-smuggling risks. "
            f"Exact alternatives: {competing}."
        ],
        "working_title_is_boundary_authority": False,
        "working_title_origin": "independent_nehemiah_three_primary_reconciliation_v1",
        "candidate_only": True,
        "review_evidence_summary": marker + ". Candidate-only and non-authorizing.",
        "red_team_questions": [
            f"Does the seam after {span.split('-')[1]} survive removal of headings and chapter numbers?",
            f"Does one of these exact alternatives better preserve the governing memoir/register/assembly function: {competing}?",
        ],
        "hard_passage_forecast": [language_hold],
    }
    if low:
        row["candidate_hold_state"] = "deferred_human_or_external_ai"
        row["candidate_hold_basis"] = "preserved_appeal"
    rows.append(row)

assert len(rows) == 24
assert [row["chunk_index_in_book"] for row in rows] == list(range(1, 25))
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
