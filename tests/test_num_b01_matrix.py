from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_numbers_b01_role_input_matrix import build  # noqa: E402


def test_numbers_matrix_is_reproducible_and_candidate_only():
    matrix = build()
    assert matrix["book"] == "Num"
    assert matrix["candidate_only"] is True
    assert matrix["non_authorizing"] is True
    assert matrix["contains_scripture_text"] is False
    assert matrix["contains_source_rows"] is False
    assert len(matrix["roles"]) == 4
    assert all(item["candidate_boundary"] is False for item in matrix["hard_passage_forecast"])


def test_numbers_matrix_role_input_closure_is_disjoint():
    matrix = build()
    common = set(matrix["common_input_artifact_ids"])
    paths = {row["path"] for row in matrix["inputs"]}
    assert len(paths) == len(matrix["inputs"])
    for role in matrix["roles"]:
        required = set(role["required_input_artifact_ids"])
        assert common <= required
        assert not (required & set(role["forbidden_input_artifact_ids"]))
