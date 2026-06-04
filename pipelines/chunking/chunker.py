#!/usr/bin/env python3
"""Bible chunker v1 — genre-aware, boundary-driven.

Upgrades the v0 token-grouper into a literary-structure-aware chunker that:
- reconstructs document order and attaches USFM structural boundary evidence
  (`boundary_claims.jsonl`: headings, paragraphs, poetry lines, psalm
  superscriptions) to each verse;
- selects the chunk UNIT by genre (`book_genres.yaml` + `chunking_policy.yaml`):
  whole psalm (superscription kept), heading-bounded prose section, paragraph +
  sentence subdivision under budget;
- NEVER splits mid-sentence (prose) and never separates a psalm superscription;
- carries concordance metadata through: footnote + editorial-crossref refs per
  chunk, and a lexeme-alignment flag (Strong's WordTokens are addressable by the
  chunk's OSIS range);
- emits a ContextPacket for epistolary chunks that open on a discourse connector.

Boundary evidence is OPTIONAL: with `--boundary-claims` the full genre-aware path
runs; without it the chunker falls back to sentence-safe grouping (v0 behavior).

Architecture note: this consumes canonical BoundaryClaim evidence (not raw
usfm_events) per T302. A standalone TextSpan generator (clause/sentence spans for
Hebrew/Greek alignment) remains a follow-up; v1's internal spans are verse-grained.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY = ROOT / "config" / "chunking" / "chunking_policy.yaml"
DEFAULT_GENRES = ROOT / "config" / "chunking" / "book_genres.yaml"

# Sentence end: . ! ? optionally followed by closing quotes/brackets incl. unicode
# curly quotes (” ’ » ) used by WEB at clause ends.
SENTENCE_END_RE = re.compile(r"[.!?][\"')\]”’»›]*$")

# USFM marker classes (from boundary_claims `marker` field)
HEADING_MARKERS = {"s", "s1", "s2", "ms", "ms1", "ms2", "mt", "mt1", "mt2", "mt3", "mte"}
PARAGRAPH_MARKERS = {"p", "m", "mi", "pi", "pi1", "pi2", "nb", "pc", "pmo", "po", "cls"}
POETRY_MARKERS = {"q", "q1", "q2", "q3", "qr", "qc"}
SUPERSCRIPTION_MARKERS = {"d"}
STANZA_MARKERS = {"b"}  # blank line between stanzas

# Epistolary discourse connectors that require prior context (chunking_policy epistles)
CONTEXT_CONNECTORS = ("therefore", "for this reason", "so then", "wherefore", "consequently", "for this cause")

POETRY_GENRES = {"psalms"}
PROSE_GENRES = {"narrative", "law", "wisdom", "prophets", "gospels", "acts", "epistles", "apocalypse"}


def read_policy_version(policy_path: Path) -> str:
    try:
        for line in policy_path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("version:"):
                return line.split(":", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return "chunk-policy-unknown"


def load_budgets(policy_path: Path) -> dict[str, int]:
    """Dependency-light read of budgets from chunking_policy.yaml."""
    budgets = {"target_tokens": 700, "soft_max_tokens": 1100, "hard_max_tokens": 1600}
    try:
        in_budgets = False
        for line in policy_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("budgets:"):
                in_budgets = True
                continue
            if in_budgets:
                if line and not line.startswith((" ", "\t")):
                    break
                m = re.match(r"\s+(\w+):\s*(\d+)", line)
                if m and m.group(1) in budgets:
                    budgets[m.group(1)] = int(m.group(2))
    except OSError:
        pass
    return budgets


def load_genres(genres_path: Path) -> tuple[dict[str, str], str]:
    """Read book -> genre from book_genres.yaml (dependency-light, flat block)."""
    genres: dict[str, str] = {}
    default = "narrative"
    try:
        in_genres = False
        for line in genres_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("default_genre:"):
                default = stripped.split(":", 1)[1].strip()
                continue
            if stripped.startswith("genres:"):
                in_genres = True
                continue
            if in_genres:
                if line and not line.startswith((" ", "\t")):
                    in_genres = False
                    continue
                m = re.match(r"\s+([A-Za-z0-9]+):\s*([a-z_]+)", line)
                if m:
                    genres[m.group(1)] = m.group(2)
    except OSError:
        pass
    return genres, default


def approx_tokens(text: str) -> int:
    return max(1, len(text.split()))


def sentence_ended(text: str) -> bool:
    return bool(SENTENCE_END_RE.search(text.strip()))


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def index_by_osis(path: Path, value_key: str | None = None):
    """Group records by osis_ref. If value_key, store that field; else the record."""
    out: dict[str, list] = {}
    if path is None or not path.exists():
        return out
    for record in load_jsonl(path):
        osis = record.get("osis_ref")
        if not osis:
            continue
        out.setdefault(osis, []).append(record[value_key] if value_key else record)
    return out


def build_units(passages_path: Path, witnesses_path: Path, boundary_claims_path: Path | None):
    """Yield per-verse units in document order with attached structural evidence."""
    text_by_passage: dict[str, str] = {}
    for w in load_jsonl(witnesses_path):
        if w.get("passage_id"):
            text_by_passage[w["passage_id"]] = w.get("text", "")

    markers_by_osis: dict[str, set[str]] = {}
    if boundary_claims_path is not None and boundary_claims_path.exists():
        for b in load_jsonl(boundary_claims_path):
            osis = b.get("osis_ref")
            if osis:
                markers_by_osis.setdefault(osis, set()).add(b.get("marker", ""))

    for passage in load_jsonl(passages_path):
        pid = passage.get("id")
        book = passage.get("book")
        if not book:
            raise ValueError(
                f"ScripturePassage missing 'book': {pid}. Re-run the importer."
            )
        osis = passage.get("osis_ref")
        markers = markers_by_osis.get(osis, set())
        yield {
            "passage_id": pid,
            "osis_ref": osis,
            "book": book,
            "chapter": passage.get("chapter"),
            "text": text_by_passage.get(pid, ""),
            "markers": markers,
            "has_heading": bool(markers & HEADING_MARKERS),
            "has_paragraph": bool(markers & PARAGRAPH_MARKERS),
            "has_superscription": bool(markers & SUPERSCRIPTION_MARKERS),
            "is_poetry": bool(markers & POETRY_MARKERS),
            "has_stanza_break": bool(markers & STANZA_MARKERS),
        }


def make_chunk(units, genre, boundary_basis, policy_version, index, footnotes_by_osis, crossrefs_by_osis):
    first, last = units[0], units[-1]
    text = " ".join(u["text"].strip() for u in units if u["text"].strip()).strip()
    osis_refs = [u["osis_ref"] for u in units]
    footnote_refs, crossref_refs = [], []
    for osis in osis_refs:
        footnote_refs.extend(footnotes_by_osis.get(osis, []))
        crossref_refs.extend(crossrefs_by_osis.get(osis, []))
    chunk_id = (
        f"chunk--eng-web--{policy_version}--{genre}--"
        f"{first['osis_ref']}--{last['osis_ref']}--{index:05d}"
    )
    return {
        "id": chunk_id,
        "type": "RetrievalChunk",
        "chunk_kind": f"{genre}_unit",
        "genre": genre,
        "source_text_id": "eng-web",
        "source_artifact_id": "eng-web_usfm",
        "osis_start": first["osis_ref"],
        "osis_end": last["osis_ref"],
        "text": text,
        "included_text_span_ids": [u["passage_id"] for u in units],
        "boundary_basis": sorted(boundary_basis),
        # Concordance / lexeme carry-through:
        "footnote_refs": footnote_refs,
        "editorial_crossref_refs": crossref_refs,
        "has_lexeme_alignment": True,  # Strong's WordTokens addressable by OSIS range
        "chunking_policy_version": policy_version,
        "license": "public-domain",
        "validation": {
            "sentence_ended": sentence_ended(text),
            "book_boundary_crossed": False,
            "starts_on_heading_or_superscription": bool(
                units[0]["has_heading"] or units[0]["has_superscription"]
            ),
        },
        "status": "active",
    }


def make_context_packet(chunk, prev_chunk):
    return {
        "id": f"context-packet--{chunk['osis_start']}--{chunk['osis_end']}",
        "type": "ContextPacket",
        "chunk_id": chunk["id"],
        "reason": "depends_on_prior_argument",
        "prior_context_refs": [prev_chunk["osis_start"], prev_chunk["osis_end"]] if prev_chunk else [],
        "following_context_refs": [],
        "warning": "Opens on a discourse connector; do not retrieve as a standalone prooftext.",
        "license": "public-domain",
        "generation_method": "chunker-v1",
        "status": "active",
    }


def chunk_book(units, genre, budgets, policy_version, footnotes_by_osis, crossrefs_by_osis, start_index):
    """Chunk one book's units by genre. Returns (chunks, next_index)."""
    chunks = []
    idx = start_index
    is_poetry = genre in POETRY_GENRES

    def flush(buf, basis):
        nonlocal idx
        if not buf:
            return
        chunks.append(make_chunk(buf, genre, basis, policy_version, idx,
                                 footnotes_by_osis, crossrefs_by_osis))
        idx += 1

    if is_poetry:
        # Unit = whole chapter (psalm/poem); superscription stays with it.
        current_chapter = None
        buf, basis = [], set()
        for u in units:
            if buf and u["chapter"] != current_chapter:
                basis.add("whole_psalm")
                basis.add("chapter_boundary")
                flush(buf, basis)
                buf, basis = [], set()
            current_chapter = u["chapter"]
            buf.append(u)
            joined = " ".join(x["text"] for x in buf)
            # Only split an over-long psalm at a stanza/paragraph boundary, never mid-verse.
            if approx_tokens(joined) >= budgets["hard_max_tokens"] and (u["has_stanza_break"] or u["has_paragraph"]):
                basis.add("poetic_stanza")
                flush(buf, basis)
                buf, basis = [], set()
        if buf:
            basis.add("whole_psalm")
            flush(buf, basis)
        return chunks, idx

    # Prose: heading-bounded sections, subdivided at paragraph + sentence under budget.
    buf, basis = [], set()
    for u in units:
        # A section heading starts a new unit (flush the prior, if any sentence-complete).
        if buf and u["has_heading"]:
            basis.add("usfm_section_heading")
            flush(buf, basis)
            buf, basis = [], set()
        buf.append(u)
        if u["has_heading"]:
            basis.add("usfm_section_heading")
        if u["has_superscription"]:
            basis.add("psalm_superscription")
        joined = " ".join(x["text"] for x in buf)
        tokens = approx_tokens(joined)
        ended = sentence_ended(u["text"])
        # Prefer paragraph boundary at/after target; force at soft max — but never mid-sentence.
        if ended and u["has_paragraph"] and tokens >= budgets["target_tokens"]:
            basis.add("usfm_paragraph")
            basis.add("english_sentence")
            flush(buf, basis)
            buf, basis = [], set()
        elif ended and tokens >= budgets["soft_max_tokens"]:
            basis.add("english_sentence")
            basis.add("token_budget")
            flush(buf, basis)
            buf, basis = [], set()
    if buf:
        basis.add("book_boundary")
        flush(buf, basis)
    return chunks, idx


def chunk_corpus(units_iter, genres, default_genre, budgets, policy_version,
                 footnotes_by_osis, crossrefs_by_osis):
    """Group units by book, chunk each book by genre, emit chunks + context packets."""
    all_chunks = []
    context_packets = []
    book_units, current_book = [], None
    idx = 1

    def process_book(bunits, book):
        nonlocal idx
        genre = genres.get(book, default_genre)
        chunks, idx = chunk_book(bunits, genre, budgets, policy_version,
                                 footnotes_by_osis, crossrefs_by_osis, idx)
        all_chunks.extend(chunks)

    for u in units_iter:
        if book_units and u["book"] != current_book:
            process_book(book_units, current_book)
            book_units = []
        current_book = u["book"]
        book_units.append(u)
    if book_units:
        process_book(book_units, current_book)

    # Context packets for epistolary chunks opening on a discourse connector.
    prev = None
    for chunk in all_chunks:
        if chunk["genre"] == "epistles":
            head = chunk["text"].lstrip().lower()
            if any(head.startswith(c) for c in CONTEXT_CONNECTORS):
                context_packets.append(make_context_packet(chunk, prev))
        prev = chunk
    return all_chunks, context_packets


def main() -> int:
    parser = argparse.ArgumentParser(description="Bible chunker v1 (genre-aware, boundary-driven)")
    parser.add_argument("--passages", required=True)
    parser.add_argument("--witnesses", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--boundary-claims", default=None, help="BoundaryClaim JSONL (enables genre-aware path)")
    parser.add_argument("--footnotes", default=None, help="Footnote JSONL (metadata carry-through)")
    parser.add_argument("--crossrefs", default=None, help="EditorialCrossReference JSONL (carry-through)")
    parser.add_argument("--genres", default=str(DEFAULT_GENRES))
    parser.add_argument("--policy", default=str(DEFAULT_POLICY))
    parser.add_argument("--context-out", default=None, help="Optional ContextPacket JSONL output")
    args = parser.parse_args()

    policy_version = read_policy_version(Path(args.policy))
    budgets = load_budgets(Path(args.policy))
    genres, default_genre = load_genres(Path(args.genres))
    bclaims = Path(args.boundary_claims) if args.boundary_claims else None
    footnotes_by_osis = index_by_osis(Path(args.footnotes), "id") if args.footnotes else {}
    crossrefs_by_osis = index_by_osis(Path(args.crossrefs), "id") if args.crossrefs else {}

    units = build_units(Path(args.passages), Path(args.witnesses), bclaims)
    chunks, packets = chunk_corpus(units, genres, default_genre, budgets, policy_version,
                                   footnotes_by_osis, crossrefs_by_osis)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as handle:
        for chunk in chunks:
            handle.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    if args.context_out and packets:
        cpath = Path(args.context_out)
        cpath.parent.mkdir(parents=True, exist_ok=True)
        with cpath.open("w", encoding="utf-8", newline="\n") as handle:
            for p in packets:
                handle.write(json.dumps(p, ensure_ascii=False) + "\n")

    print(f"Wrote {len(chunks)} chunks to {out} (policy {policy_version}); {len(packets)} context packets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
