from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "ps89_boundary_review.md"
MANIFEST = ROOT / "eval" / "chunking_gold" / "per_form" / "psalms_gold_manifest.json"
ROADMAP = ROOT / "docs" / "roadmap" / "T337B_PS89_OWNER_DECISION_OPTION_C.md"


APPROVED_SPANS = [
    ("Ps.89.1", "Ps.89.4"),
    ("Ps.89.5", "Ps.89.18"),
    ("Ps.89.19", "Ps.89.37"),
    ("Ps.89.38", "Ps.89.45"),
    ("Ps.89.46", "Ps.89.48"),
    ("Ps.89.49", "Ps.89.52"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def manifest_case(case_id: str) -> dict:
    manifest = json.loads(read(MANIFEST))
    for case in manifest["reviewed_gold"]:
        if case["case_id"] == case_id:
            return case
    raise AssertionError(f"missing reviewed case {case_id}")


def test_owner_decision_box_records_option_c_authorization() -> None:
    text = read(PACKET)

    assert "reviewer: Lowell Wong" in text
    assert "date: 2026-06-10" in text
    assert "decision: approved_with_scope_note" in text
    assert "implementation_allowed: true" in text
    assert "output_change_authorized: true" in text
    assert "reviewed_gold_promoted: true" in text
    assert "Option C" in text


def test_ps89_option_c_spans_and_book_iii_doxology_are_locked() -> None:
    text = read(PACKET)
    case = manifest_case("ps89_owner_decision_option_c")
    observed_spans = [
        (chunk["osis_start"], chunk["osis_end"])
        for chunk in case["expected"]["child_chunks"]
    ]

    assert observed_spans == APPROVED_SPANS
    assert "`Ps.89.49-Ps.89.52`" in text
    assert "Book III doxology" in text
    assert "ordinary continuation of the lament appeal" in text
    assert "one-verse orphan" in text
    final_child = case["expected"]["child_chunks"][-1]
    assert final_child["book_iii_doxology_ref"] == "Ps.89.52"
    assert final_child["no_one_verse_orphan_split"] is True


def test_option_c_is_psalm_89_only_and_not_a_global_rule() -> None:
    combined = "\n".join([read(PACKET), read(ROADMAP)])

    assert "Psalm 89 only" in combined
    assert "global Selah rule" in combined
    assert "global blank-line rule" in combined
    assert "global doxology rule" in combined
    assert "global poetry rule" in combined
    assert "Revelation implementation" in combined
    assert "boundary import" in combined
    assert "T327G" in combined
    assert "T338 has not started" in read(PACKET)
