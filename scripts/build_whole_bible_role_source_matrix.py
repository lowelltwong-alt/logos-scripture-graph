#!/usr/bin/env python3
"""Build a privacy-safe OT/NT source-routing matrix for all 66 B01 jobs."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OT = ["Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal"]
NT = ["Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]
COMMON = ["campaign_registry","workflow","prompt_pack","runtime_adapter","canonical_passages","translation_witness"]
OT_SOURCES = ["oshb_manifest","oshb_archive","oshb_view_manifest","oshb_book_view","uxlc_manifest","uxlc_archive","uxlc_view_manifest","uxlc_book_view"]
NT_SOURCES = ["sblgnt_or_qualified_greek_manifest","greek_view_manifest","greek_book_view"]
ROLE_EXTRA = {
    "original_language_translation_scout": ["original_language_policy", "textual_variant_policy"],
    "literary_form_scout": ["form_registry", "literary_marker_protocol", "owner_faithful_policy"],
    "canonical_relations_and_premortem_scout": ["bible_wide_research_registry", "contextual_reading_policy", "dossier_queues"],
    "second_temple_rabbinic_context_scout": ["corpus_inventory", "ancient_context_gap_policy"],
}

def main() -> int:
    rows = []
    for book in OT + NT:
        testament = "OT" if book in OT else "NT"
        lang = "hebrew_aramaic" if testament == "OT" else "koine_greek"
        sources = COMMON + (OT_SOURCES if testament == "OT" else NT_SOURCES)
        rows.append({"book": book, "testament": testament, "original_language_scope": lang, "common_input_artifact_ids": COMMON, "original_language_input_artifact_ids": sources, "role_extra_input_artifact_ids": ROLE_EXTRA, "ancient_context_status": "gap_until_qualified_corpus", "candidate_only": True, "non_authorizing": True})
    out = ROOT / "docs/governance/WHOLE_BIBLE_B01_ROLE_SOURCE_MATRIX.v1.json"
    out.write_text(json.dumps({"schema_version":"whole_bible_b01_role_source_matrix.v1","book_count":66,"rows":rows,"B01_authorized":False,"non_authorizing":True}, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(out); return 0
if __name__ == "__main__": raise SystemExit(main())
