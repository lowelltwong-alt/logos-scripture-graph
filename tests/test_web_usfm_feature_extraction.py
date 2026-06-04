import json
import zipfile
from pathlib import Path

from pipelines.ingest.usfm_importer import main


def read_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def test_small_fixture_end_to_end_feature_extraction(tmp_path):
    archive = tmp_path / "fixture.zip"
    usfm = "\n".join(
        [
            r"\id JHN Test",
            r"\c 1",
            r"\s1 The Word",
            r"\p",
            r'\v 1 \w In|strong="G1722"\w* the beginning\f + \fr 1:1 \ft note \+wh λόγος\+wh*\f*.',
            r"\q1 poetry line",
            r"\v 2 child\x + \xo 1:2 \xt Isaiah 7:14\x* text",
        ]
    )
    glossary = "\n".join([r"\id GLO", r"\ili \k Abba\k* Abba means father."])
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("73-JHNeng-web.usfm", usfm)
        zf.writestr("106-GLOeng-web.usfm", glossary)

    canonical = tmp_path / "canonical"
    processed = tmp_path / "processed"
    assert main(
        [
            "--archive",
            str(archive),
            "--canonical-root",
            str(canonical),
            "--processed-root",
            str(processed),
            "--skip-sha-check",
        ]
    ) == 0

    witnesses = read_jsonl(canonical / "translations" / "eng-web" / "translation_witnesses.jsonl")
    tokens = read_jsonl(canonical / "translations" / "eng-web" / "word_tokens.jsonl")
    footnotes = read_jsonl(canonical / "translations" / "eng-web" / "footnotes.jsonl")
    crossrefs = read_jsonl(canonical / "translations" / "eng-web" / "editorial_cross_references.jsonl")
    boundaries = read_jsonl(canonical / "translations" / "eng-web" / "boundary_claims.jsonl")
    glossary_entries = read_jsonl(canonical / "translations" / "eng-web" / "glossary_entries.jsonl")

    assert witnesses[0]["text"] == "In the beginning. poetry line"
    assert "\\" not in witnesses[0]["text"]
    assert tokens[0]["surface_text"] == "In"
    assert tokens[0]["strong"] == "G1722"
    assert footnotes[0]["hebrew_word_spans"] == ["λόγος"]
    assert crossrefs[0]["candidate_osis_refs"] == ["Isa.7.14"]
    assert any(record["marker"] == "q1" for record in boundaries)
    assert glossary_entries[0]["term"] == "Abba"
    assert glossary_entries[0]["definition"] == "Abba means father."
