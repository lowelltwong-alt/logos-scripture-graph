"""Gold-set tests for the genre-aware, boundary-driven chunker (v1).

These encode the non-negotiable "world-class for a Bible" properties from
docs/chunking/CHUNKING_DESIGN.md and EVALUATION_PLAN.md. They run against the
real canonical corpus, so they SKIP cleanly when the generated data is absent
(run `python pipelines/ingest/usfm_importer.py` first; CI regenerates it).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHUNKER = ROOT / "pipelines" / "chunking" / "chunker.py"
CANON = ROOT / "data" / "canonical"
PASSAGES = CANON / "scripture" / "passages" / "passages.jsonl"
WITNESSES = CANON / "translations" / "eng-web" / "translation_witnesses.jsonl"
BOUNDARIES = CANON / "translations" / "eng-web" / "boundary_claims.jsonl"
FOOTNOTES = CANON / "translations" / "eng-web" / "footnotes.jsonl"
CROSSREFS = CANON / "translations" / "eng-web" / "editorial_cross_references.jsonl"

RAW_USFM = re.compile(r"\\(?:\+?[A-Za-z0-9]+)\*?")

requires_data = pytest.mark.skipif(
    not (PASSAGES.exists() and WITNESSES.exists() and BOUNDARIES.exists()),
    reason="canonical data not generated; run the importer first",
)


@pytest.fixture(scope="module")
def chunks(tmp_path_factory):
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
    return [json.loads(l) for l in out.read_text(encoding="utf-8").splitlines() if l.strip()]


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
def test_psalm_23_is_one_whole_psalm_chunk(chunks):
    ps23 = [c for c in chunks if c["osis_start"].startswith("Ps.23.") or c["osis_end"].startswith("Ps.23.")]
    assert len(ps23) == 1, f"Psalm 23 split into {len(ps23)} chunks (expected 1 whole psalm)"
    c = ps23[0]
    assert c["genre"] == "psalms"
    assert c["osis_start"] == "Ps.23.1" and c["osis_end"] == "Ps.23.6"
    assert "whole_psalm" in c["boundary_basis"]


@requires_data
def test_short_psalms_are_not_fragmented(chunks):
    # Psalms 1-50 are mostly short; none should fragment into >1 chunk at v1 budgets
    # except the long ones. Spot-check a few classic short psalms.
    for ref in ("Ps.1.", "Ps.8.", "Ps.23.", "Ps.100.", "Ps.117."):
        hits = [c for c in chunks if c["osis_start"].startswith(ref)]
        assert len(hits) == 1, f"{ref} fragmented into {len(hits)} chunks"


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
