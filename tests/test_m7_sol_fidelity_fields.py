from scripts.validate_m7_sol_fidelity_fields import validate


class MemoryPath:
    def __init__(self, text):
        self.text = text

    def read_text(self, encoding="utf-8"):
        return self.text


def test_valid_candidate_row():
    path = MemoryPath('{"book":"Gen","span":"Gen.1.1-Gen.1.2","candidate_only":true,"non_authorizing":true,"working_title_is_boundary_authority":false,"candidate_internal_seams":["scene"],"original_language_translation_holds":["review"],"cross_reference_holds":["lead"],"red_team_premortem_holds":["test"]}\n')
    count, errors = validate(path)
    assert count == 1
    assert errors == []


def test_missing_fields_fail_closed():
    path = MemoryPath('{"book":"Gen","span":"Gen.1.1-Gen.1.2","candidate_only":true,"non_authorizing":true,"working_title_is_boundary_authority":false}\n')
    count, errors = validate(path)
    assert count == 1
    assert any("candidate_internal_seams" in error for error in errors)
    assert any("cross_reference_holds" in error for error in errors)
    assert any("red_team_premortem_holds" in error for error in errors)