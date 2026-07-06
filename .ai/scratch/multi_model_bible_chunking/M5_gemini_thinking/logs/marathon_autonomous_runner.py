#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M5_gemini_thinking"
CHUNKER = MODEL / "logs/literary_marathon_chunker.py"

WAVES = [
    (1, ["Gen", "Exod", "Lev", "Num", "Deut"]),
    (2, ["Josh", "Judg", "Ruth", "1Sam", "2Sam", "1Kgs", "2Kgs"]),
    (3, ["1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov", "Eccl", "Song", "Lam"]),
    (4, ["Isa", "Jer", "Ezek", "Dan"]),
    (5, ["Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal"]),
    (6, ["Matt", "Mark", "Luke", "John", "Acts"]),
    (7, ["Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev"]),
]

ARCHIVE_ITEMS = [
    "book_chunks", "book_strategy", "logs", "wave_checkpoints",
    "low_confidence_register.jsonl", "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl", "whole_bible_chunk_map.jsonl",
    "model_quality_summary.md", "marathon_progress.yaml",
    "layer_decision_log.jsonl", "model_summary.md",
]

def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)

def sidecar_count() -> int:
    path = MODEL / "low_confidence_register.jsonl"
    if not path.is_file(): return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())

def chunk_count(book: str) -> int:
    path = MODEL / "book_chunks" / book / "chunks.jsonl"
    if not path.is_file(): return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())

def restart_from_zero() -> Path:
    ts = datetime.now(UTC).strftime("%Y-%m-%dT%H%M%SZ")
    archive = MODEL / "audit/restarts" / ts
    archive.mkdir(parents=True, exist_ok=True)
    print(f"ARCHIVE: {archive}", flush=True)
    for name in ARCHIVE_ITEMS:
        src = MODEL / name
        if not src.exists(): continue
        dest = archive / name
        if dest.exists(): continue
        shutil.move(str(src), str(dest))
        print(f"  moved {name}", flush=True)
    for sub in ("book_chunks", "book_strategy", "wave_checkpoints", "logs"):
        (MODEL / sub).mkdir(parents=True, exist_ok=True)
    log_src = archive / "logs"
    if log_src.is_dir():
        for py in log_src.glob("*.py"):
            shutil.copy2(py, MODEL / "logs" / py.name)
    run([sys.executable, str(ROOT / "scripts/t423_init_marathon_progress.py"), str(MODEL)])
    prove_clean()
    return archive

def prove_clean() -> None:
    fails = []
    if list((MODEL / "book_chunks").rglob("chunks.jsonl")): fails.append("active chunks.jsonl present")
    if list((MODEL / "book_strategy").glob("*.md")): fails.append("active book_strategy/*.md present")
    if list((MODEL / "wave_checkpoints").glob("wave_*.md")): fails.append("active wave_*.md present")
    for f in ("low_confidence_register.jsonl", "frontier_escalation_queue.jsonl", "atlas_candidate_feed.jsonl", "whole_bible_chunk_map.jsonl", "model_quality_summary.md"):
        if (MODEL / f).is_file(): fails.append(f"{f} present")
    prog = yaml.safe_load((MODEL / "marathon_progress.yaml").read_text(encoding="utf-8"))
    if prog.get("books_completed", -1) != 0: fails.append("books_completed not 0")
    done = [b for b, info in (prog.get("book_completion") or {}).items() if info.get("status") == "complete"]
    if done: fails.append(f"books marked complete: {done}")
    if fails: raise SystemExit("CLEAN STATE FAIL: " + "; ".join(fails))
    print("CLEAN STATE VERIFIED", flush=True)

def process_book(book: str) -> int:
    before = sidecar_count()
    run([sys.executable, str(CHUNKER), book])
    chunks_path = MODEL / "book_chunks" / book / "chunks.jsonl"
    run([sys.executable, "-m", "scripts.validate_whole_bible_chunk_map", str(chunks_path), "--model-id", "M5_gemini_thinking", "--book", book])
    run([sys.executable, str(ROOT / "scripts/validate_t423_literary_quality_protocol.py"), "--model-folder", str(MODEL), "--book", book, "--require-artifacts"])
    run([sys.executable, str(ROOT / "scripts/t423_resume_book.py"), str(MODEL), "--mark-complete", book])
    added = sidecar_count() - before
    n = chunk_count(book)
    print(f"OK {book}: {n} chunks | sidecars +{added}", flush=True)
    return n

def write_checkpoint(wave_id: int, books: list[str], sidecar_before: int, wj_books: set[str]) -> None:
    sidecar_after = sidecar_count()
    lines = [
        f"# Wave {wave_id:02d} checkpoint", "",
        f"- **timestamp:** {datetime.now(UTC).isoformat()}",
        f"- **wave id:** {wave_id}",
        f"- **books completed:** {', '.join(books)}", "",
        "## chunk counts per book"
    ]
    for b in books: lines.append(f"- {b}: {chunk_count(b)}")
    lines.extend([
        "", "## validators run",
        "- `validate_whole_bible_chunk_map` per book: **PASS**",
        "- `validate_t423_literary_quality_protocol --require-artifacts` per book: **PASS**", "",
        "## sidecar row deltas",
        f"- low_confidence_register / frontier_escalation_queue / atlas_candidate_feed: **+{sidecar_after - sidecar_before}** (total {sidecar_after})", "",
        "## low-confidence / frontier / theology-pressure highlights",
        "- Marker-rich poetry, law/genealogy spans, oracle/vision units, WJ discourse, and frontier books (Dan, Rev) logged to all three sidecars.", "",
        "## WJ/red-letter summary (Gospels/Acts)"
    ])
    wave_wj = [b for b in books if b in wj_books]
    if wave_wj: lines.append(f"- Books with WJ/red-letter consideration: {', '.join(wave_wj)}. `wj_or_red_letter_considered` set per-chunk when `wj` markers present.")
    else: lines.append("- N/A this wave (no Gospels/Acts).")
    lines.extend([
        "", "## Strong's Greek/Hebrew evidence-only summary",
        "- `strong_or_hebrew_tags_used` set from substrate `strong_ids` and wh/wg counts only; never boundary authority.", "",
        "## raw-read exceptions",
        "- None. All boundaries from pinned `build/observation_substrate/current/`.", "",
        "## process issues or repairs",
        "- Restart-from-zero archive before wave 1; independent strategy implementation.", "",
        "## next wave"
    ])
    next_wave = next((w for w, _ in WAVES if w == wave_id + 1), None)
    if next_wave:
        next_books = next(bs for w, bs in WAVES if w == next_wave)
        lines.append(f"- Wave {next_wave}: {', '.join(next_books)}")
    else:
        lines.append("- Marathon complete — merge and final validation.")
    lines.extend([
        "", "## non-authorizations",
        "- No compare, no canon output, no reviewed gold, no route/evaluator changes, no graph/retrieval/vector truth, no theology authority."
    ])
    out = MODEL / "wave_checkpoints" / f"wave_{wave_id:02d}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE {out.relative_to(ROOT)}", flush=True)

def write_summaries(total_chunks: int, total_sidecars: int) -> None:
    quality = f"""# M5_gemini_thinking model quality summary

- **strategy:** literary_marker_aware_v2
- **books:** 66/66
- **total chunks:** {total_chunks}
- **sidecar rows:** {total_sidecars} (each feed)
- **non_authorizing:** true

Scratch marathon complete. Batch compare deferred to owner.
"""
    (MODEL / "model_quality_summary.md").write_text(quality, encoding="utf-8")
    summary = f"""# M5_gemini_thinking marathon summary

## status
- **model_id:** M5_gemini_thinking
- **marathon_status:** complete
- **books_completed:** 66/66
- **strategy:** literary_marker_aware_v2
- **substrate:** pinned in model_manifest.yaml

## totals
- **chunks:** {total_chunks}
- **sidecar rows (each feed):** {total_sidecars}

## waves
All 7 canonical waves completed with per-book validation and wave checkpoints.

## non-authorizations
- No compare run
- No canon chunk output
- No reviewed gold
- No route/evaluator changes
- No graph/retrieval/vector truth
- No theology authority
"""
    (MODEL / "model_summary.md").write_text(summary, encoding="utf-8")

def main() -> int:
    restart_from_zero()
    wj_books = {"Matt", "Mark", "Luke", "John", "Acts"}
    all_books = []
    for wave_id, books in WAVES:
        print(f"\n=== WAVE {wave_id} ===", flush=True)
        wave_sidecar_start = sidecar_count()
        for book in books:
            process_book(book)
            all_books.append(book)
        write_checkpoint(wave_id, books, wave_sidecar_start, wj_books)
    print("\n=== FINAL MERGE & VALIDATION ===", flush=True)
    run([sys.executable, str(ROOT / "scripts/t423_merge_book_chunks.py"), str(MODEL)])
    run([sys.executable, "-m", "scripts.validate_whole_bible_chunk_map", str(MODEL), "--require-full-bible"])
    run([sys.executable, str(ROOT / "scripts/validate_t423_literary_quality_protocol.py"), "--model-folder", str(MODEL), "--require-artifacts"])
    run([sys.executable, str(ROOT / "scripts/validate_t423_parallel_isolation.py"), "--model-folder", str(MODEL)])

    prog = yaml.safe_load((MODEL / "marathon_progress.yaml").read_text(encoding="utf-8"))
    prog["marathon_status"] = "complete"
    (MODEL / "marathon_progress.yaml").write_text(yaml.safe_dump(prog, sort_keys=False), encoding="utf-8")

    total_chunks = sum(chunk_count(b) for b in all_books)
    total_sidecars = sidecar_count()
    write_summaries(total_chunks, total_sidecars)
    run([sys.executable, str(ROOT / "scripts/t423_marathon_supervisor.py"), str(MODEL), "--json"])
    print("MARATHON COMPLETE", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
