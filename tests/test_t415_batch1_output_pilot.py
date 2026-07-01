from __future__ import annotations

from scripts.validate_t415_batch1_output_pilot import validate_t415_batch1


def test_t415_batch1_output_pilot_validates() -> None:
    manifest = validate_t415_batch1()
    assert manifest["output_change"]["baseline_chunk_count"] == 1138
    assert manifest["output_change"]["candidate_chunk_count"] == 1143
    assert manifest["output_change"]["added_overlay_count"] == 5
