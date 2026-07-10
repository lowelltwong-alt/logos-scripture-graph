from scripts.validate_t472_model_panel_calibration_gate import ROOT, validate_t472


def test_former_2john_owner_packet_is_withdrawn() -> None:
    errors = validate_t472(ROOT)
    assert errors == []
