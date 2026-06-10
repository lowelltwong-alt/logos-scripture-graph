"""Gold-set tests for the genre-aware, boundary-driven chunker (v1).

These encode the non-negotiable "world-class for a Bible" properties from
docs/chunking/CHUNKING_DESIGN.md and EVALUATION_PLAN.md. They run against the
real canonical corpus, so they SKIP cleanly when the generated data is absent
(run `python pipelines/ingest/usfm_importer.py` first; CI regenerates it).
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from pipelines.chunking.evaluate_chunks import score

ROOT = Path(__file__).resolve().parents[1]
CHUNKER = ROOT / "pipelines" / "chunking" / "chunker.py"
ORCHESTRATOR = ROOT / "pipelines" / "chunking" / "orchestrator.py"
CANON = ROOT / "data" / "canonical"
PASSAGES = CANON / "scripture" / "passages" / "passages.jsonl"
WITNESSES = CANON / "translations" / "eng-web" / "translation_witnesses.jsonl"
BOUNDARIES = CANON / "translations" / "eng-web" / "boundary_claims.jsonl"
FOOTNOTES = CANON / "translations" / "eng-web" / "footnotes.jsonl"
CROSSREFS = CANON / "translations" / "eng-web" / "editorial_cross_references.jsonl"
PSALMS_GOLD = ROOT / "eval" / "chunking_gold" / "per_form" / "psalms_gold_manifest.json"
BASELINE_D_SHA256 = "4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025"

RAW_USFM = re.compile(r"\\(?:\+?[A-Za-z0-9]+)\*?")

requires_data = pytest.mark.skipif(
    not (PASSAGES.exists() and WITNESSES.exists() and BOUNDARIES.exists()),
    reason="canonical data not generated; run the importer first",
)


@pytest.fixture(scope="module")
def psalms_gold_manifest():
    return json.loads(PSALMS_GOLD.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def chunk_output(tmp_path_factory):
    out = tmp_path_factory.mktemp("chunks") / "gold.jsonl"
    result = subprocess.run(
        [sys.executable, str(CHUNKER),
         "--passages", str(PASSAGES), "--witnesses", str(WITNESSES),
         "--boundary-claims", str(BOUNDARIES),
         "--footnotes", str(FOOTNOTES), "--crossrefs", str(CROSSREFS),
         "--out", str(out)],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return {
        "path": out,
        "records": [json.loads(l) for l in out.read_text(encoding="utf-8").splitlines() if l.strip()],
    }


@pytest.fixture(scope="module")
def chunks(chunk_output):
    return chunk_output["records"]


@pytest.fixture(scope="module")
def route_ledger(tmp_path_factory):
    temp = tmp_path_factory.mktemp("psalm-routes")
    out = temp / "chunks.jsonl"
    ledger = temp / "route_ledger.jsonl"
    result = subprocess.run(
        [sys.executable, str(ORCHESTRATOR),
         "--passages", str(PASSAGES), "--witnesses", str(WITNESSES),
         "--boundary-claims", str(BOUNDARIES),
         "--footnotes", str(FOOTNOTES), "--crossrefs", str(CROSSREFS),
         "--out", str(out), "--route-ledger", str(ledger)],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return [json.loads(l) for l in ledger.read_text(encoding="utf-8").splitlines() if l.strip()]


def _chapter_chunks(chunks: list[dict], book: str, chapter: str) -> list[dict]:
    prefix = f"{book}.{chapter}."
    return [
        c for c in chunks
        if c["osis_start"].startswith(prefix) or c["osis_end"].startswith(prefix)
    ]


def _case(manifest: dict, section: str, case_id: str) -> dict:
    for case in manifest[section]:
        if case["case_id"] == case_id:
            return case
    raise AssertionError(f"missing Psalm gold case {section}/{case_id}")


def _approx_tokens(text: str) -> int:
    return max(1, len(text.split()))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _boundary_claims() -> list[dict]:
    return [json.loads(l) for l in BOUNDARIES.read_text(encoding="utf-8").splitlines() if l.strip()]


@requires_data
def test_psalms_gold_manifest_separates_reviewed_gold_from_characterization(psalms_gold_manifest):
    assert psalms_gold_manifest["target_form"] == "literal_book_psalms"
    reviewed = {case["case_id"]: case for case in psalms_gold_manifest["reviewed_gold"]}
    characterization = {case["case_id"]: case for case in psalms_gold_manifest["characterization_only"]}
    assert set(reviewed) == {
        "ps23_whole_psalm",
        "ps119_acrostic_sections",
        "short_psalm_holdouts",
        "ps3_superscription_attached",
        "non_target_poetry_controls",
        "ps78_parent_child_structural_split",
        "ps105_whole_psalm",
        "ps106_whole_psalm_with_b_marker_note",
        "ps89_owner_decision_option_c",
    }
    assert set(characterization) == {
        "ps136_refrain_litany_pending_review",
    }
    for case in characterization.values():
        assert case["status"] == "pending_human_review"
        assert case["implementation_allowed"] is False
        assert case["output_change_authorized"] is False
    assert reviewed["ps78_parent_child_structural_split"]["status"] == \
        "approved_structural_split_under_parent_whole_psalm"


@requires_data
def test_current_chunk_output_sha_matches_corrected_baseline(chunk_output):
    assert _sha256(chunk_output["path"]) == BASELINE_D_SHA256


@requires_data
def test_no_chunk_contains_raw_usfm(chunks):
    leaks = [c["id"] for c in chunks if RAW_USFM.search(c["text"])]
    assert not leaks, f"raw USFM leaked into {len(leaks)} chunks"


@requires_data
def test_no_prose_chunk_ends_mid_sentence(chunks):
    bad = [
        f"{c['osis_start']}->{c['osis_end']}"
        for c in chunks
        if c["genre"] != "psalms" and not c["validation"]["sentence_ended"]
    ]
    assert not bad, f"prose chunks ending mid-sentence: {bad[:10]}"


@requires_data
def test_psalm_23_is_one_whole_psalm_chunk(chunks, psalms_gold_manifest):
    expected = _case(psalms_gold_manifest, "reviewed_gold", "ps23_whole_psalm")["expected"]
    ps23 = [c for c in chunks if c["osis_start"].startswith("Ps.23.") or c["osis_end"].startswith("Ps.23.")]
    assert len(ps23) == expected["chunk_count"], f"Psalm 23 split into {len(ps23)} chunks (expected 1 whole psalm)"
    c = ps23[0]
    assert c["genre"] == expected["genre"]
    assert c["osis_start"] == expected["osis_start"] and c["osis_end"] == expected["osis_end"]
    assert set(expected["required_boundary_basis"]) <= set(c["boundary_basis"])


@requires_data
def test_short_psalm_holdouts_are_not_fragmented(chunks, psalms_gold_manifest):
    case = _case(psalms_gold_manifest, "reviewed_gold", "short_psalm_holdouts")
    for chapter_ref in case["osis_chapters"]:
        book, chapter = chapter_ref.split(".")
        hits = _chapter_chunks(chunks, book, chapter)
        assert len(hits) == case["expected"]["chunk_count_per_chapter"], \
            f"{chapter_ref} fragmented into {len(hits)} chunks"
        assert set(case["expected"]["required_boundary_basis"]) <= set(hits[0]["boundary_basis"])


@requires_data
def test_psalm_105_reviewed_whole_psalm_gold(chunks, psalms_gold_manifest):
    case = _case(psalms_gold_manifest, "reviewed_gold", "ps105_whole_psalm")
    expected = case["expected"]
    ps105 = _chapter_chunks(chunks, "Ps", "105")
    assert len(ps105) == expected["chunk_count"]
    assert ps105[0]["osis_start"] == expected["osis_start"]
    assert ps105[0]["osis_end"] == expected["osis_end"]
    assert ps105[0]["genre"] == expected["genre"]
    assert _approx_tokens(ps105[0]["text"]) == expected["tokens"]
    assert set(expected["required_boundary_basis"]) <= set(ps105[0]["boundary_basis"])
    assert expected["reviewed_whole_psalm"] is True
    assert expected["child_chunks_required"] is False


@requires_data
def test_psalm_106_reviewed_whole_psalm_gold_with_b_marker_note(chunks, psalms_gold_manifest):
    case = _case(psalms_gold_manifest, "reviewed_gold", "ps106_whole_psalm_with_b_marker_note")
    expected = case["expected"]
    ps106 = _chapter_chunks(chunks, "Ps", "106")
    assert len(ps106) == expected["chunk_count"]
    assert ps106[0]["osis_start"] == expected["osis_start"]
    assert ps106[0]["osis_end"] == expected["osis_end"]
    assert ps106[0]["genre"] == expected["genre"]
    assert _approx_tokens(ps106[0]["text"]) == expected["tokens"]
    assert set(expected["required_boundary_basis"]) <= set(ps106[0]["boundary_basis"])
    assert expected["reviewed_whole_psalm"] is True
    assert expected["child_chunks_required"] is False
    assert case["internal_marker_note"]["markers_observed"] == ["b"]
    assert "not sufficient" in case["internal_marker_note"]["boundary_authority"]


@requires_data
def test_psalm_119_has_22_sections_and_is_not_penalized(chunks, psalms_gold_manifest):
    case = _case(psalms_gold_manifest, "reviewed_gold", "ps119_acrostic_sections")
    ps119 = _chapter_chunks(chunks, "Ps", "119")
    assert len(ps119) == case["expected"]["chunk_count"]
    assert [[c["osis_start"], c["osis_end"]] for c in ps119] == case["expected"]["spans"]

    metrics = score(ps119)
    assert metrics["psalm119_section_chunks"] == case["expected"]["psalm119_section_chunks"]
    assert metrics["literal_psalms_fragmented"] == case["expected"]["literal_psalms_fragmented_for_case"]
    assert metrics["poetry_books_fragmented"] == case["expected"]["poetry_books_fragmented_for_case"]


@requires_data
def test_real_superscription_psalm_has_no_orphan_title_chunk(chunks, psalms_gold_manifest):
    case = _case(psalms_gold_manifest, "reviewed_gold", "ps3_superscription_attached")
    evidence = case["source_evidence"]
    matching_evidence = [
        claim for claim in _boundary_claims()
        if claim.get("source_file") == evidence["source_file"]
        and claim.get("source_line") == evidence["source_line"]
        and claim.get("marker") == evidence["marker"]
        and claim.get("raw_marker") == evidence["raw_marker"]
    ]
    assert matching_evidence, "expected real Psalm superscription source evidence"

    ps3 = _chapter_chunks(chunks, "Ps", "3")
    expected = case["expected"]
    assert len(ps3) == expected["chunk_count"]
    assert ps3[0]["osis_start"] == expected["osis_start"]
    assert ps3[0]["osis_end"] == expected["osis_end"]
    assert set(expected["required_boundary_basis"]) <= set(ps3[0]["boundary_basis"])

    title_text = evidence["raw_marker"].removeprefix("\\d").strip()
    orphan_title_chunks = [
        c for c in chunks
        if c["osis_start"].split(".")[0] == "Ps" and c["text"].strip() == title_text
    ]
    assert not orphan_title_chunks


@requires_data
def test_non_target_poetry_books_remain_on_monolith_fallback(route_ledger, psalms_gold_manifest):
    case = _case(psalms_gold_manifest, "reviewed_gold", "non_target_poetry_controls")
    routes = {
        record["book"]: record
        for record in route_ledger
        if record.get("type") == "ChunkingRouteLedgerRoute"
    }
    for book in case["books"]:
        route = routes[book]
        assert route["skill_id"] == case["expected"]["route_skill_id"]
        assert route["route_reason"] == case["expected"]["route_reason"]
        assert route["detect_form_consumed"] is case["expected"]["detect_form_consumed"]
        assert route["form_based_routing_enabled"] is case["expected"]["form_based_routing_enabled"]


@requires_data
def test_psalm_78_reviewed_parent_child_structural_split(chunks, psalms_gold_manifest):
    case = _case(psalms_gold_manifest, "reviewed_gold", "ps78_parent_child_structural_split")
    assert case["status"] == "approved_structural_split_under_parent_whole_psalm"
    assert case["parent_literary_unit"] == {
        "osis_start": "Ps.78.1",
        "osis_end": "Ps.78.72",
        "unit_type": "whole_psalm",
        "literary_unity": True,
    }
    assert case["expected"]["reviewed_structural_split"] is True
    assert case["expected"]["not_bad_fragmentation_gold"] is True
    assert case["evaluator_context"]["evaluator_formula_changed"] is False

    ps78 = _chapter_chunks(chunks, "Ps", "78")
    observed = [
        {
            "osis_start": c["osis_start"],
            "osis_end": c["osis_end"],
            "tokens": _approx_tokens(c["text"]),
            "boundary_basis": c["boundary_basis"],
        }
        for c in ps78
    ]
    assert observed == case["expected"]["child_chunks"]
    assert _approx_tokens(" ".join(c["text"] for c in ps78)) == case["expected"]["merged_tokens"]
    assert case["expected"]["hard_max_violation_if_merged"] is False
    metrics = score(chunks)
    assert metrics["literal_psalms_fragmented_raw"] == 1
    assert metrics["literal_psalms_fragmented"] == 0
    assert metrics["reviewed_structural_splits"] == [{
        "case_id": "ps78_parent_child_structural_split",
        "osis_span": "Ps.78.1-Ps.78.72",
        "parent": {"osis_start": "Ps.78.1", "osis_end": "Ps.78.72"},
        "child_spans": [
            {"osis_start": "Ps.78.1", "osis_end": "Ps.78.69"},
            {"osis_start": "Ps.78.70", "osis_end": "Ps.78.71"},
            {"osis_start": "Ps.78.72", "osis_end": "Ps.78.72"},
        ],
    }]


@requires_data
def test_every_chunk_has_required_fields(chunks):
    for c in chunks:
        assert c["type"] == "RetrievalChunk"
        assert c["osis_start"] and c["osis_end"]
        assert c["genre"]
        assert c["boundary_basis"], f"{c['id']} has no boundary basis"
        assert c["chunking_policy_version"]
        assert c["license"] == "public-domain"
        assert c["text"].strip()


@requires_data
def test_no_chunk_crosses_a_book(chunks):
    for c in chunks:
        assert c["osis_start"].split(".")[0] == c["osis_end"].split(".")[0], \
            f"chunk crosses books: {c['osis_start']} -> {c['osis_end']}"


@requires_data
def test_metadata_carry_through(chunks):
    # Strong's lexeme alignment flagged on all; footnotes/crossrefs carried where present.
    assert all(c["has_lexeme_alignment"] for c in chunks)
    assert any(c["footnote_refs"] or c["editorial_crossref_refs"] for c in chunks)
