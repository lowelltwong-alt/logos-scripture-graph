from __future__ import annotations

from scripts.validate_t416_batch1_post_pilot_review import validate_t416_batch1_post_pilot_review


def test_t416_batch1_post_pilot_review_validates() -> None:
    record = validate_t416_batch1_post_pilot_review()
    assert record["verdict"] == "APPROVE_BATCH1_POST_PILOT"
    assert record["same_baseline_review"]["baseline_chunk_count"] == 1138
    assert record["same_baseline_review"]["candidate_chunk_count"] == 1143
    assert record["child_necessity_review"]["selected_children"] == []
