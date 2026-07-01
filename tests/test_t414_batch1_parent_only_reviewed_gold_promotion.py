from __future__ import annotations

from scripts.validate_t414_batch1_parent_only_reviewed_gold_promotion import validate_t414_batch1


def test_t414_batch1_promotion_validates() -> None:
    validate_t414_batch1()
