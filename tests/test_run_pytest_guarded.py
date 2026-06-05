from scripts.run_pytest_guarded import parse_collected_nodeids, segment_nodeids


def test_parse_collected_nodeids_filters_summary_lines():
    stdout = """
tests/test_alpha.py::test_one
tests/test_alpha.py::test_two
2 tests collected in 0.01s
"""
    assert parse_collected_nodeids(stdout) == [
        "tests/test_alpha.py::test_one",
        "tests/test_alpha.py::test_two",
    ]


def test_segment_nodeids_runs_known_timeouts_first_and_isolated():
    nodeids = [
        "tests/test_alpha.py::test_fast",
        "tests/test_alpha.py::test_slow",
        "tests/test_beta.py::test_other",
    ]
    hints = {"tests": {"tests/test_alpha.py::test_slow": {"likely_timeout": True}}}
    assert segment_nodeids(nodeids, hints, max_segment_size=10) == [
        ["tests/test_alpha.py::test_slow"],
        ["tests/test_alpha.py::test_fast"],
        ["tests/test_beta.py::test_other"],
    ]
