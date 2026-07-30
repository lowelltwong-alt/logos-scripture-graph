import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
BOOKS = {"Matt": 28, "Mark": 16, "Luke": 24, "John": 21, "Acts": 28}

def _chapters(book):
    out = set()
    with (ROOT / "data/canonical/scripture/passages/passages.jsonl").open(encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            if row.get("book") == book:
                out.add(int(row["chapter"]))
    return out

def test_gospels_acts_have_exact_nonoverlapping_chapter_coverage():
    for book, expected in BOOKS.items():
        rows = [json.loads(x) for x in (MODEL / "book_chunks" / book / "chunks.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
        assert len(rows) > 1
        covered = []
        for row in rows:
            assert row["book"] == book
            assert row["candidate_only"] if "candidate_only" in row else row["non_authorizing"]
            assert row["non_authorizing"] is True
            assert row["review_status"] == "candidate_structural_unit_pending_b01_mesh"
            assert row["literature_type_guess"]
            span = row["span"].split("-")
            covered.append((int(span[0].split(".")[1]), int(span[1].split(".")[1])))
        assert covered[0][0] == 1 and covered[-1][1] == expected
        for prior, current in zip(covered, covered[1:]):
            assert current[0] == prior[1] + 1
        assert set(range(1, expected + 1)) == set(c for a, b in covered for c in range(a, b + 1))

def test_difficult_lanes_and_cross_reference_holds_are_present():
    for book in BOOKS:
        rows = [json.loads(x) for x in (MODEL / "book_chunks" / book / "chunks.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
        assert all(row["difficulty_classes"] for row in rows)
        assert all("original_language_translation_review" in row["review_holds"] for row in rows)
        assert all("canonical_cross_reference_premortem" in row["review_holds"] for row in rows)
        assert any(row["cross_reference_seed_refs"] for row in rows)
