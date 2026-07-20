from __future__ import annotations

import json
from pathlib import Path
import zipfile

from pipelines.ingest.usfm_importer import main, resolve_line_marker


def _read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _run_fixture(tmp_path: Path, filename: str, usfm: str) -> dict[str, list[dict]]:
    archive = tmp_path / "fixture.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr(filename, usfm)
    canonical = tmp_path / "canonical"
    processed = tmp_path / "processed"
    assert (
        main(
            [
                "--archive",
                str(archive),
                "--canonical-root",
                str(canonical),
                "--processed-root",
                str(processed),
                "--skip-sha-check",
                "--canonical-66-filter",
            ]
        )
        == 0
    )
    translation = canonical / "translations" / "eng-web"
    return {
        "witnesses": _read_jsonl(translation / "translation_witnesses.jsonl"),
        "tokens": _read_jsonl(translation / "word_tokens.jsonl"),
        "footnotes": _read_jsonl(translation / "footnotes.jsonl"),
        "boundaries": _read_jsonl(translation / "boundary_claims.jsonl"),
        "headings": _read_jsonl(translation / "section_headings.jsonl"),
        "events": _read_jsonl(processed / "usfm_events.jsonl"),
    }


def _by_ref(rows: list[dict]) -> dict[str, dict]:
    return {row["osis_ref"]: row for row in rows}


def test_marker_resolution_distinguishes_ownership_from_body_disposition() -> None:
    forward = resolve_line_marker(
        "p",
        "",
        current_osis_ref="Gen.1.2",
        prior_osis_ref="Gen.1.2",
        next_osis_ref="Gen.1.3",
        book="GEN",
    )
    assert forward.anchor_kind == "next_content_start"
    assert forward.anchor_osis_ref == "Gen.1.3"
    assert forward.body_disposition == "none"

    continuation = resolve_line_marker(
        "q2",
        "continued poetry",
        current_osis_ref="Ps.3.2",
        prior_osis_ref="Ps.3.2",
        next_osis_ref="Ps.3.3",
        book="PSA",
    )
    assert continuation.anchor_kind == "current_content"
    assert continuation.anchor_osis_ref == "Ps.3.2"
    assert continuation.body_disposition == "append_current"

    terminal_break = resolve_line_marker(
        "b",
        "",
        current_osis_ref=None,
        prior_osis_ref="Ps.78.72",
        next_osis_ref=None,
        book="PSA",
    )
    assert terminal_break.anchor_kind == "between_units"
    assert terminal_break.prior_osis_ref == "Ps.78.72"
    assert terminal_break.next_osis_ref is None
    assert terminal_break.anchor_osis_ref is None

    chapter = resolve_line_marker(
        "cl",
        "Psalm",
        current_osis_ref=None,
        prior_osis_ref=None,
        next_osis_ref="Ps.1.1",
        book="PSA",
    )
    assert chapter.anchor_kind == "chapter_context"
    assert chapter.anchor_osis_ref is None

    inline_only_as_line = resolve_line_marker(
        "qs",
        "Selah",
        current_osis_ref="Ps.3.2",
        prior_osis_ref="Ps.3.2",
        next_osis_ref="Ps.3.3",
        book="PSA",
    )
    assert inline_only_as_line.anchor_kind == "unresolved"
    assert inline_only_as_line.anchor_osis_ref is None


def test_psalm_headings_anchor_forward_without_entering_scripture_text_or_tokens(
    tmp_path: Path,
) -> None:
    rows = _run_fixture(
        tmp_path,
        "20-PSAeng-web.usfm",
        "\n".join(
            [
                r"\id PSA Test",
                r"\c 119",
                r'\d \w ALEPH|strong="H1"\w*',
                r"\q1",
                r"\v 1 First \qs Selah.\qs*",
                r"\q2 continuation.",
                r'\d \w BETH|strong="H2"\w*',
                r"\q1",
                r"\v 9 Ninth.",
                r"\b",
                r"\q1",
                r"\v 10 Tenth.",
                r"\b",
            ]
        ),
    )
    witnesses = _by_ref(rows["witnesses"])
    assert witnesses["Ps.119.1"]["text"] == "First Selah. continuation."
    assert "ALEPH" not in witnesses["Ps.119.1"]["text"]
    assert "BETH" not in witnesses["Ps.119.1"]["text"]
    assert {row.get("strong") for row in rows["tokens"]}.isdisjoint({"H1", "H2"})

    headings = [row for row in rows["headings"] if row["marker"] == "d"]
    assert [row["osis_ref"] for row in headings] == ["Ps.119.1", "Ps.119.9"]
    assert all(row["anchor_kind"] == "next_content_start" for row in headings)
    assert all(row["body_disposition"] == "editorial_only" for row in headings)

    d_claims = [row for row in rows["boundaries"] if row["marker"] == "d"]
    assert [row["anchor_osis_ref"] for row in d_claims] == ["Ps.119.1", "Ps.119.9"]
    q2 = next(row for row in rows["boundaries"] if row["marker"] == "q2")
    assert q2["anchor_kind"] == "current_content"
    assert q2["osis_ref"] == "Ps.119.1"
    assert not any(row["marker"] == "qs" for row in rows["boundaries"])

    breaks = [row for row in rows["boundaries"] if row["marker"] == "b"]
    assert breaks[0]["anchor_kind"] == "between_units"
    assert breaks[0]["prior_osis_ref"] == "Ps.119.9"
    assert breaks[0]["next_osis_ref"] == "Ps.119.10"
    assert breaks[0]["osis_ref"] == "Ps.119.10"
    assert breaks[1]["prior_osis_ref"] == "Ps.119.10"
    assert breaks[1]["next_osis_ref"] is None
    assert breaks[1]["osis_ref"] is None


def test_editorial_heading_footnotes_are_typed_sidecars_without_witness_or_tokens(
    tmp_path: Path,
) -> None:
    """T519: \\f inside \\d must survive in footnotes.jsonl (T475 P1/P2)."""
    rows = _run_fixture(
        tmp_path,
        "20-PSAeng-web.usfm",
        "\n".join(
            [
                r"\id PSA Test",
                r"\c 46",
                r"\d For the Chief Musician. According to Alamoth."
                r"\f + \fr 46:0 \ft Alamoth is a musical term.\f*",
                r"\q1",
                r"\v 1 God is our refuge.",
                r"\c 90",
                r"\d A Prayer by Moses, the man of God."
                r'\f + \fr 90:0 \ft The Hebrew word rendered “God” is “\+wh אֱלֹהִ֑ים\+wh*” (Elohim).\f*',
                r"\q1",
                r"\v 1 Lord, you have been our dwelling place.",
            ]
        ),
    )
    witnesses = _by_ref(rows["witnesses"])
    assert witnesses["Ps.46.1"]["text"] == "God is our refuge."
    assert "Alamoth" not in witnesses["Ps.46.1"]["text"]
    assert "musical term" not in witnesses["Ps.46.1"]["text"]
    assert witnesses["Ps.90.1"]["text"] == "Lord, you have been our dwelling place."
    assert "Elohim" not in witnesses["Ps.90.1"]["text"]
    assert not any(row.get("strong") for row in rows["tokens"])

    headings = [row for row in rows["headings"] if row["marker"] == "d"]
    assert [row["osis_ref"] for row in headings] == ["Ps.46.1", "Ps.90.1"]
    assert all(row["body_disposition"] == "editorial_only" for row in headings)
    assert "Alamoth is a musical term" not in headings[0]["text"]
    assert "Alamoth" in headings[0]["text"]

    footnotes = rows["footnotes"]
    assert len(footnotes) == 2
    assert all(row["osis_ref"] is None for row in footnotes)
    assert all(row["passage_id"] is None for row in footnotes)
    by_ref = {row["reference"]: row for row in footnotes}
    assert by_ref["46:0"]["text"] == "Alamoth is a musical term."
    assert "Elohim" in by_ref["90:0"]["text"]
    assert by_ref["90:0"]["hebrew_word_spans"] == ["אֱלֹהִ֑ים"]
    assert by_ref["46:0"]["id"].startswith("footnote:eng-web:20-PSAeng-web.usfm:")
    assert by_ref["90:0"]["id"].startswith("footnote:eng-web:20-PSAeng-web.usfm:")


def test_speaker_labels_are_editorial_and_anchor_the_following_content(tmp_path: Path) -> None:
    rows = _run_fixture(
        tmp_path,
        "23-SNGeng-web.usfm",
        "\n".join(
            [
                r"\id SNG Test",
                r"\c 1",
                r"\v 1 Opening.",
                r'\sp Beloved \w HE|strong="H3588"\w*',
                r"\q1",
                r"\v 2 Answer.",
            ]
        ),
    )
    witnesses = _by_ref(rows["witnesses"])
    assert witnesses["Song.1.1"]["text"] == "Opening."
    assert witnesses["Song.1.2"]["text"] == "Answer."
    assert all("Beloved" not in row["text"] for row in rows["witnesses"])
    assert all(row.get("strong") != "H3588" for row in rows["tokens"])
    speaker = next(row for row in rows["headings"] if row["marker"] == "sp")
    assert speaker["anchor_kind"] == "next_content_start"
    assert speaker["prior_osis_ref"] == "Song.1.1"
    assert speaker["next_osis_ref"] == "Song.1.2"
    assert speaker["osis_ref"] == "Song.1.2"


def test_content_lines_stay_current_and_no_break_retains_cross_chapter_neighbors(
    tmp_path: Path,
) -> None:
    rows = _run_fixture(
        tmp_path,
        "05-NUMeng-web.usfm",
        "\n".join(
            [
                r"\id NUM Test",
                r"\c 13",
                r"\v 4 Verse four.",
                r'\m \w Of|strong="H1121"\w* Reuben.',
                r"\m",
                r"\v 5 Verse five.",
                r"\c 14",
                r"\nb",
                r"\v 1 Chapter start.",
            ]
        ),
    )
    witnesses = _by_ref(rows["witnesses"])
    assert witnesses["Num.13.4"]["text"] == "Verse four. Of Reuben."
    token = next(row for row in rows["tokens"] if row.get("strong") == "H1121")
    assert token["osis_ref"] == "Num.13.4"
    m_claims = [row for row in rows["boundaries"] if row["marker"] == "m"]
    assert m_claims[0]["anchor_kind"] == "current_content"
    assert m_claims[0]["osis_ref"] == "Num.13.4"
    assert m_claims[1]["anchor_kind"] == "next_content_start"
    assert m_claims[1]["osis_ref"] == "Num.13.5"
    no_break = next(row for row in rows["boundaries"] if row["marker"] == "nb")
    assert no_break["anchor_kind"] == "between_units"
    assert no_break["prior_osis_ref"] == "Num.13.5"
    assert no_break["next_osis_ref"] == "Num.14.1"
    assert no_break["osis_ref"] == "Num.14.1"


def test_unresolved_marker_body_fails_closed_without_text_or_token_mutation(tmp_path: Path) -> None:
    rows = _run_fixture(
        tmp_path,
        "73-JHNeng-web.usfm",
        "\n".join(
            [
                r"\id JHN Test",
                r"\c 1",
                r"\v 1 Base.",
                r'\zfoo \w Mystery|strong="G9999"\w*',
                r"\b invalid body",
            ]
        ),
    )
    assert rows["witnesses"][0]["text"] == "Base."
    assert all(row.get("strong") != "G9999" for row in rows["tokens"])
    unresolved = [row for row in rows["events"] if row["marker"] in {"zfoo", "b"}]
    assert len(unresolved) == 2
    assert all(row["anchor_kind"] == "unresolved" for row in unresolved)
    assert all(row["anchor_osis_ref"] is None for row in unresolved)
    bad_break = next(row for row in rows["boundaries"] if row["marker"] == "b")
    assert bad_break["osis_ref"] is None
    assert bad_break["anchor_resolved"] is False
