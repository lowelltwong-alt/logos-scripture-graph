#!/usr/bin/env python3
"""Build a privacy-safe, candidate-only Numbers B01 role-input matrix."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMON = {
    "campaign_registry": "config/agents/families/scripture-first-biblical-chunking/whole_bible_campaign_registry.v1.json",
    "workflow": "config/agents/families/scripture-first-biblical-chunking/whole_bible_candidate_workflow.v2.yaml",
    "prompt_pack": "config/agents/families/scripture-first-biblical-chunking/whole_bible_candidate_prompt_pack.v2.yaml",
    "runtime_adapter": "config/agents/families/scripture-first-biblical-chunking/codex_desktop_campaign_adapter.v2.yaml",
    "canonical_passages": "data/canonical/scripture/passages/passages.jsonl",
    "web_witness": "data/canonical/translations/eng-web/translation_witnesses.jsonl",
}
EXTRA = {
    "oshb_source_manifest": "data/raw/original_language/hebrew/openscriptures_oshb/source_manifest.yaml", "oshb_raw_archive": "data/raw/original_language/hebrew/openscriptures_oshb/raw/openscriptures_oshb-3d15126fb1ef.zip", "oshb_view_manifest": "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/canonical_source_view_manifest.yaml", "oshb_included_files": "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/included_files.jsonl", "oshb_book_view": "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/Num.xml",
    "uxlc_source_manifest": "data/raw/original_language/hebrew/tanach_us_uxlc/source_manifest.yaml", "uxlc_raw_archive": "data/raw/original_language/hebrew/tanach_us_uxlc/raw/Tanach.xml.zip", "uxlc_view_manifest": "data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/canonical_source_view_manifest.yaml", "uxlc_included_files": "data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/included_files.jsonl", "uxlc_book_view": "data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/files/Num.xml",
    "form_registry": "config/chunking/form_registry.yaml", "literary_marker_protocol": ".ai/control/t423_literary_marker_quality_protocol.yaml", "owner_faithful_policy": ".ai/control/t468_owner_faithful_chunking_policy.yaml", "canonical_research_registry": ".ai/control/bible_wide_chunking_research_registry.yaml", "narrative_legal_dossier_queue": ".ai/control/narrative_legal_covenant_dossier_queue.yaml", "source_metadata_atlas": ".ai/control/source_metadata_research_atlas.yaml", "original_language_context_policy": ".ai/control/original_language_phrase_context_policy.yaml", "contextual_reading_policy": ".ai/control/contextual_reading_policy.yaml", "corpus_inventory": ".ai/control/autonomous_corpus_processor.yaml",
}
SOURCES = {**COMMON, **EXTRA}
ROLE_EXTRA = {
    "original_language_translation_scout": ["oshb_source_manifest", "oshb_raw_archive", "oshb_view_manifest", "oshb_included_files", "oshb_book_view", "uxlc_source_manifest", "uxlc_raw_archive", "uxlc_view_manifest", "uxlc_included_files", "uxlc_book_view", "source_metadata_atlas", "original_language_context_policy"],
    "literary_form_scout": ["form_registry", "literary_marker_protocol", "owner_faithful_policy"],
    "canonical_relations_and_premortem_scout": ["canonical_research_registry", "narrative_legal_dossier_queue", "contextual_reading_policy"],
    "second_temple_rabbinic_context_scout": ["corpus_inventory"],
}
FOCUS = {"original_language_translation_scout": ["Hebrew morphology and syntax", "qere/ketiv and reversed-nun metadata", "MT/WEB reference-label alignment", "translation divergence requiring contextual review"], "literary_form_scout": ["narrative/law/ritual transitions", "embedded songs and oracles", "lists, itineraries, speeches, and framing prose", "markers are evidence only"], "canonical_relations_and_premortem_scout": ["internal cross-reference candidates", "quotation/allusion and repeated motifs", "versification shifts", "boundary leakage and theology-smuggling risks"], "second_temple_rabbinic_context_scout": ["qualified corpus-only context", "absence/gap receipts when no corpus is qualified", "ancient sources cannot authorize boundaries"]}
HARD = [("Num.5.11-Num.5.31", ["mixed_ritual_law", "translation_ambiguity"]), ("Num.10.1-Num.10.36", ["departure_frame", "embedded_song", "refrain"]), ("Num.11.1-Num.12.16", ["interleaved_narrative", "speech", "translation_ambiguity"]), ("Num.13.1-Num.14.45", ["paired_report", "refrain", "narrative_turn"]), ("Num.16.1-Num.18.32", ["revolt_narrative", "ritual_law", "repeated_authority_claims"]), ("Num.20.1-Num.21.35", ["narrative_transition", "song", "geographic_itinerary"]), ("Num.22.1-Num.24.25", ["oracle_cycle", "poetry_in_narrative", "speaker_shift"]), ("Num.25.1-Num.27.23", ["census_frame", "ritual_law", "inheritance_case"]), ("Num.28.1-Num.36.13", ["law_collections", "lists", "itinerary_and_boundary_data"])]

def digest(path: Path) -> str:
    h = hashlib.sha256();
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""): h.update(block)
    return "sha256:" + h.hexdigest()

def build() -> dict:
    rows = []
    for aid, rel in SOURCES.items():
        path = ROOT / rel
        if not path.is_file(): raise FileNotFoundError(rel)
        rows.append({"artifact_id": aid, "path": rel.replace("\\", "/"), "sha256": digest(path), "scope": "governed_input"})
    common = list(COMMON)
    roles = [{"role_id": role, "required_input_artifact_ids": common + extra, "forbidden_input_artifact_ids": ["other_role_reports", "synthesis_lineage", "boss_authorization"], "focus": FOCUS[role]} for role, extra in ROLE_EXTRA.items()]
    return {"schema_version": "whole_bible_num_b01_role_input_matrix.v1", "book": "Num", "stage_id": "B01", "candidate_only": True, "non_authorizing": True, "contains_scripture_text": False, "contains_source_rows": False, "boundary_authority": "none", "contract_schema": "whole_bible_b01_typed_contract.schema.v2", "common_input_artifact_ids": common, "inputs": rows, "roles": roles, "hard_passage_forecast": [{"ref_scope": ref, "difficulty_classes": kinds, "required_evidence": ["literary_form", "original_language", "canonical_relations"], "candidate_boundary": False} for ref, kinds in HARD], "cross_reference_seed_refs": ["Num.17.1-Num.17.15", "Num.17.16-Num.17.28", "Num.25.19", "Num.26.1", "Num.30.1", "Num.30.2-Num.30.17"], "review_holds": ["no_final_chunk_map", "no_theological_decision", "no_source_tradition_preference", "ancient_context_gap_requires_qualified_corpus"]}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--output", type=Path, default=ROOT / "docs/governance/NUMBERS_B01_ROLE_INPUT_MATRIX.v1.json"); ap.add_argument("--check", action="store_true"); args = ap.parse_args()
    value = build(); encoded = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != encoded: raise SystemExit("Numbers B01 matrix is stale or missing")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(encoded, encoding="utf-8", newline="\n")
    print(args.output); return 0
if __name__ == "__main__": raise SystemExit(main())
