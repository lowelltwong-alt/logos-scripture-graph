# Task Handoff — T306: Codex 5.5 implementation sprint

## Task

- task_id: T306
- title: Codex 5.5 sprint — thorough code review + targeted mechanical fixes
- phase: phase_3
- status: in_progress

## Agent

- agent_name: codex-5.5
- mode: review
- stage: start
- updated_at: 2026-06-04T13:35:00+00:00
- handoff_id: 943f54d7a4753c73
- builds_on: T300→T305 (full review + remediation chain)

---

## Why this handoff is calibrated for Codex 5.5

Codex 5.5 outperforms Opus 4.8 at:
- **Rapid code execution and iteration** — run, read output, fix, repeat fast
- **Exhaustive systematic auditing** — check every file against a criterion, report completely
- **Test-driven implementation** — write the test first, iterate until it passes
- **Precise mechanical fixes** — given exact specs, produce exactly-correct code
- **Parallelism** — multiple independent tool calls simultaneously
- **Regression discipline** — run existing tests after every change

Codex 5.5 should NOT attempt (leave for Claude):
- Open-ended architectural design or new ADRs
- Biblical/literary scholarship judgment (Psalm/oracle/epistle chunking policy)
- Multi-tradition theological decisions
- Trust-zone and assertion-mode governance design

If you hit a design decision: write it in "Open questions" and stop. Do not guess.

---

## Mandatory start sequence (do not skip any step)

```bash
# 1. Read mandatory context (before any code)
# AI_FRONT_DOOR.md -> .ai/control/MASTER_CONTEXT.md -> .ai/control/PROJECT_STATUS.md
# -> .ai/control/DATA_MAP.md -> this file

# 2. Register your start
python scripts/agent/force_handoff.py --task-id T306 --agent codex-5.5 --stage start --mode review

# 3. Regenerate canonical data (gitignored; required for most tasks)
python pipelines/ingest/usfm_importer.py

# 4. Verify baseline — must be green before any work
python scripts/validate_all.py    # expect: All validation gates passed
python -m pytest -q               # expect: 11 passed
```

All gates must stay green after EVERY task. Run before stopping.

---

## Repo state entering T306

| What | State |
|------|-------|
| Git commits | 2 (initial scaffold + T305 remediation / CODEOWNERS fix) |
| Ingest | Complete: 38,058 passages, 864,904 total records |
| Canon profiles | On all 38,058 passages |
| Chunker | v0 working (1,310 chunks, 0 USFM leaks) |
| CI gates | validate_all (5 gates) + pytest (11 tests) |
| P0 blockers | All resolved |
| CP-1 | CODEOWNERS = @lowelltwong-alt; human must enable branch protection |
| Generated data | Gitignored; regenerate with importer |

---

## Deliverable A — Exhaustive code review

Read every file below in full and produce a structured findings report.
For each file report: bugs, regressions, missing coverage, Windows-specific risks, performance at 10× corpus.

**Files to review (read the actual source, do not summarise from prior context):**

```
pipelines/ingest/usfm_importer.py
pipelines/ingest/usfm_inline_parser.py
pipelines/util/usfm_to_osis.py
pipelines/util/canon.py
pipelines/chunking/chunker.py
pipelines/chunking/boundary_scorer.py
pipelines/validate/validate_manifest.py
scripts/validate_all.py
scripts/validate_control_plane.py
scripts/validate_jsonl.py
scripts/validate_schemas.py
scripts/generate_data_map.py
scripts/agent/force_handoff.py
scripts/agent/validate_handoffs.py
scripts/agent/approve_master_context.py
tests/test_chunker_smoke.py
tests/test_control_plane.py
tests/test_usfm_inline_parser.py
tests/test_web_usfm_feature_extraction.py
```

**Run while reviewing:**
```bash
python -m pytest -v 2>&1 | tee build/t306_pytest_full.txt
python pipelines/chunking/chunker.py \
  --passages data/canonical/scripture/passages/passages.jsonl \
  --witnesses data/canonical/translations/eng-web/translation_witnesses.jsonl \
  --out build/t306_chunks.jsonl
python scripts/validate_jsonl.py --require-canon \
  data/canonical/scripture/passages/passages.jsonl \
  data/canonical/translations/eng-web/translation_witnesses.jsonl
python scripts/validate_schemas.py --limit 2000 \
  data/canonical/scripture/passages/passages.jsonl \
  data/canonical/translations/eng-web/translation_witnesses.jsonl
python pipelines/validate/validate_manifest.py \
  data/raw/bible/eng-web/source_manifest.yaml
python scripts/generate_data_map.py --check
```

Paste exact outputs for each command into your findings.

---

## Deliverable B — Targeted mechanical fixes (clear acceptance criteria for each)

### B1 — Fix validate_manifest.py substring false-positive (VAL-1)

**The bug:** `REQUIRED = ["id:", ...]` checked via `if r not in text`. `"id:"` is a substring of
`"source_id:"`, so a manifest with `source_id:` but no top-level `id:` passes. Confirmed in T300.

**Exact fix — rewrite main() to use PyYAML (already in `[validate]` deps):**
```python
#!/usr/bin/env python3
"""Validate a source manifest."""
from __future__ import annotations
import hashlib, re, sys
from pathlib import Path

REQUIRED_KEYS = ["id", "source_family", "title", "language", "format", "license", "archive_path", "status"]

def main(argv=None):
    if argv is None: argv = sys.argv
    if len(argv) != 2:
        print("Usage: validate_manifest.py <manifest.yaml>", file=sys.stderr); return 2
    path = Path(argv[1])
    if not path.exists():
        print(f"Missing manifest: {path}", file=sys.stderr); return 1
    try:
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except ImportError:
        # fallback: line-based, anchored regex
        data = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)", line)
            if m: data.setdefault(m.group(1), m.group(2).strip().strip('"').strip("'"))
    except Exception as e:
        print(f"MANIFEST PARSE FAILED: {e}", file=sys.stderr); return 1
    failures = [f"missing key: {k}" for k in REQUIRED_KEYS if k not in data]
    sha = str(data.get("sha256", "") or "").strip()
    if sha and sha.lower() not in {"", "null"}:
        if not re.match(r"^[a-fA-F0-9]{64}$", sha):
            failures.append("sha256 must be 64 hex chars or null")
        else:
            archive = Path(str(data.get("archive_path", ""))).resolve()
            if not archive.is_absolute():
                archive = (Path(argv[1]).parent.parent.parent.parent / str(data.get("archive_path", ""))).resolve()
            if archive.exists():
                digest = hashlib.sha256(archive.read_bytes()).hexdigest()
                if digest.lower() != sha.lower():
                    failures.append(f"sha256 mismatch: manifest has {sha[:12]}... archive has {digest[:12]}...")
    if failures:
        print("MANIFEST VALIDATION FAILED")
        for f in failures: print(f"  - {f}")
        return 1
    print("Manifest validation passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

**Tests to write — `tests/test_validate_manifest.py`:**
```python
def test_missing_id_key_fails()             # manifest has source_id but not id
def test_source_id_is_not_id_confuser()     # source_id present, id absent -> fail
def test_bad_sha256_format_fails()          # sha256: "nothex" -> fail
def test_null_sha256_passes()               # sha256: null -> pass (no hash check)
def test_valid_manifest_example_passes()    # use source_manifest.example.yaml -> pass
def test_valid_manifest_real_passes()       # use source_manifest.yaml -> pass (with real hash check)
```

Run: `python -m pytest tests/test_validate_manifest.py -v`

---

### B2 — Corpus invariant tests

Add `tests/test_corpus_invariants.py`. These guard ingest regressions.
Skip silently when canonical data is absent (clean checkouts without running ingest):

```python
import pytest, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASSAGES = ROOT / "data/canonical/scripture/passages/passages.jsonl"
WITNESSES = ROOT / "data/canonical/translations/eng-web/translation_witnesses.jsonl"
WORD_TOKENS = ROOT / "data/canonical/translations/eng-web/word_tokens.jsonl"
FOOTNOTES = ROOT / "data/canonical/translations/eng-web/footnotes.jsonl"
BOUNDARY_CLAIMS = ROOT / "data/canonical/translations/eng-web/boundary_claims.jsonl"
RAW_USFM = re.compile(r"\\(?:\+?[A-Za-z0-9]+)\*?")

requires_ingest = pytest.mark.skipif(not PASSAGES.exists(), reason="run importer first")

def count_lines(path): return sum(1 for l in path.open(encoding="utf-8") if l.strip())

@requires_ingest
def test_passage_count(): assert count_lines(PASSAGES) == 38058

@requires_ingest
def test_witness_count(): assert count_lines(WITNESSES) == 38058

@requires_ingest
def test_footnote_count(): assert count_lines(FOOTNOTES) == 1855

@requires_ingest
def test_word_token_count(): assert count_lines(WORD_TOKENS) == 677688

@requires_ingest
def test_boundary_claim_count(): assert count_lines(BOUNDARY_CLAIMS) == 34177

@requires_ingest
def test_all_passages_have_canon_profiles():
    for line in PASSAGES.open(encoding="utf-8"):
        if not line.strip(): continue
        r = json.loads(line)
        assert r.get("canon_profiles"), f"Missing canon_profiles: {r.get('id')}"

@requires_ingest
def test_all_passages_have_testament():
    valid = {"OT", "NT", "unknown"}
    for line in PASSAGES.open(encoding="utf-8"):
        if not line.strip(): continue
        r = json.loads(line)
        assert r.get("testament") in valid, f"Bad testament on {r.get('id')}: {r.get('testament')}"

@requires_ingest
def test_no_raw_usfm_in_witnesses():
    for line in WITNESSES.open(encoding="utf-8"):
        if not line.strip(): continue
        r = json.loads(line)
        assert not RAW_USFM.search(r.get("text", "")), f"Raw USFM in {r.get('id')}: {r.get('text','')[:80]}"

@requires_ingest
def test_witness_passage_refs_exist():
    passages = set()
    for line in PASSAGES.open(encoding="utf-8"):
        if line.strip(): passages.add(json.loads(line)["id"])
    for line in WITNESSES.open(encoding="utf-8"):
        if not line.strip(): continue
        r = json.loads(line)
        assert r.get("passage_id") in passages, f"Witness {r.get('id')} refs missing passage {r.get('passage_id')}"
```

Run: `python -m pytest tests/test_corpus_invariants.py -v`
(Will skip cleanly if ingest not run; on CI it runs after ingest.)

---

### B3 — Handoff orphan detector

Add to `scripts/agent/validate_handoffs.py`:

```python
def validate_no_orphan_handoffs(referenced_paths: list[str]) -> list[str]:
    """Handoff dirs on disk but not in ROADMAP_STATE = orphan (AGENT-1 residual)."""
    handoff_root = ROOT / ".ai" / "handoffs"
    SKIP_NAMES = {"_TEMPLATE.handoff.md", "README.md", "AGENT_ROUTING_GUIDE.md"}
    failures = []
    normalised = {p.replace("\\", "/").strip() for p in referenced_paths}
    for child in sorted(handoff_root.iterdir()):
        if child.name in SKIP_NAMES or child.is_file():
            continue
        if child.is_dir():
            expected = f".ai/handoffs/{child.name}/handoff.md"
            if expected not in normalised:
                failures.append(f"Orphan handoff dir not in ROADMAP_STATE: {expected}")
    return failures
```

Call from `main()` and include results in failures. Then handle the known orphan:
1. Read `.ai/handoffs/T001-web-usfm-ingest/handoff.md`.
2. It is a blank scaffold (verified in T300). Delete the directory.
3. Confirm `validate_handoffs.py` passes.

---

### B4 — Missing `book` guard on chunker join

Add this guard to `pipelines/chunking/chunker.py::join_passages_witnesses`:

```python
def join_passages_witnesses(passages_path: Path, witnesses_path: Path):
    text_by_passage = load_witness_text(witnesses_path)
    for passage in load_jsonl(passages_path):
        passage_id = passage.get("id")
        book = passage.get("book")
        if not book:
            raise ValueError(
                f"ScripturePassage missing 'book' field: {passage_id}. "
                "Re-run importer to regenerate canonical data."
            )
        yield {
            "osis_ref": passage.get("osis_ref"),
            "passage_id": passage_id,
            "book": book,
            "text": text_by_passage.get(passage_id, ""),
        }
```

Add to `tests/test_chunker_smoke.py`:
```python
def test_chunker_raises_on_missing_book(tmp_path):
    passages = tmp_path / "passages.jsonl"
    witnesses = tmp_path / "witnesses.jsonl"
    out = tmp_path / "chunks.jsonl"
    passages.write_text('{"id":"scripture:X.1.1","osis_ref":"X.1.1"}\n', encoding="utf-8")
    witnesses.write_text('{"id":"w1","passage_id":"scripture:X.1.1","text":"test."}\n', encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(CHUNKER), "--passages", str(passages),
         "--witnesses", str(witnesses), "--out", str(out)],
        cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0, "Chunker must fail when book is missing"
    assert "book" in result.stderr.lower() or "book" in result.stdout.lower()
```

---

### B5 — Ledger path normalisation (DET-1 residual)

Check the existing ledger for Windows backslashes:
```bash
python -c "
import json
with open('.ai/control/handoff_ledger.jsonl', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        r = json.loads(line)
        if '\\\\' in r.get('handoff_path', ''):
            print(f'Line {i}: backslash path: {r[\"handoff_path\"]}')
"
```

In `scripts/agent/force_handoff.py`, change the event dict to write posix paths:
```python
event = {
    ...
    "handoff_path": path.relative_to(ROOT).as_posix(),   # was: str(path.relative_to(ROOT))
    ...
}
```

Existing historical backslash entries are fine to leave. Add a test:
```python
# tests/test_control_plane.py — add
def test_force_handoff_ledger_uses_posix_paths(tmp_path):
    # run force_handoff and check the last ledger entry
    import subprocess, json
    result = subprocess.run(
        [sys.executable, "scripts/agent/force_handoff.py",
         "--task-id", "T999", "--agent", "test", "--stage", "start", "--mode", "build"],
        cwd=ROOT, capture_output=True, text=True)
    # Clean up
    import shutil
    shutil.rmtree(ROOT / ".ai" / "handoffs" / "T999", ignore_errors=True)
    ledger = ROOT / ".ai" / "control" / "handoff_ledger.jsonl"
    last = json.loads(ledger.read_text(encoding="utf-8").splitlines()[-1])
    # Remove the test entry so it doesn't pollute state
    lines = ledger.read_text(encoding="utf-8").splitlines()
    ledger.write_text("\n".join(l for l in lines if "T999" not in l) + "\n", encoding="utf-8")
    assert "\\" not in last["handoff_path"], f"Backslash in path: {last['handoff_path']}"
```

---

### B6 — DATA_MAP round-trip verification

Verify `--check` works correctly:
```bash
python scripts/generate_data_map.py                # regenerate
python scripts/generate_data_map.py --check        # expect: current

# Simulate stale:
python -c "
with open('.ai/control/DATA_MAP.md', 'a', encoding='utf-8') as f:
    f.write('\nSTALE LINE\n')
"
python scripts/generate_data_map.py --check        # expect: STALE

# Restore:
python scripts/generate_data_map.py
python scripts/generate_data_map.py --check        # expect: current
```

Report exact outputs. If any step produces wrong result, fix `_strip_timestamp`.

---

### B7 — CRLF safety for `parse_lock`

Add to `tests/test_control_plane.py`:
```python
def test_parse_lock_strips_crlf(tmp_path):
    from scripts.validate_control_plane import parse_lock
    lock_file = tmp_path / "test.lock.yaml"
    lock_file.write_bytes(b"version: 1\r\nsha256: abc123\r\napproved_by: human\r\n")
    data = parse_lock(lock_file)
    assert data["sha256"] == "abc123", f"CRLF not stripped: {data['sha256']!r}"
    assert data["approved_by"] == "human"
```

Run `python -m pytest tests/test_control_plane.py -v`. If it fails, add `.rstrip()` to `parse_lock()` values.

---

## Deliverable C — Data quality checks (run, report exact numbers)

### C1 — Empty witness text
```python
# run this inline
import json
empty = [json.loads(l)["id"] for l in open(
    "data/canonical/translations/eng-web/translation_witnesses.jsonl", encoding="utf-8")
    if l.strip() and not json.loads(l).get("text","").strip()]
print(f"Empty text witnesses: {len(empty)}")
if empty[:5]: print(empty[:5])
```

### C2 — Non-standard OSIS refs
```python
import json, re
PAT = re.compile(r"^[1-4]?[A-Z][a-z][a-zA-Z0-9]*\.[0-9]+\.[0-9]+$")
bad = [json.loads(l).get("osis_ref") for l in open(
    "data/canonical/scripture/passages/passages.jsonl", encoding="utf-8")
    if l.strip() and not PAT.match(json.loads(l).get("osis_ref",""))]
print(f"Non-matching OSIS: {len(bad)}")
if bad[:10]: print(bad[:10])
```

### C3 — Sidecar referential integrity (all types)
```python
import json
from pathlib import Path
passages = {json.loads(l)["id"] for l in open(
    "data/canonical/scripture/passages/passages.jsonl", encoding="utf-8") if l.strip()}
for fname in ["word_tokens.jsonl","footnotes.jsonl","editorial_cross_references.jsonl",
              "section_headings.jsonl","boundary_claims.jsonl","glossary_entries.jsonl"]:
    path = Path("data/canonical/translations/eng-web") / fname
    if not path.exists(): continue
    bad = 0; null_pid = 0
    for l in path.open(encoding="utf-8"):
        if not l.strip(): continue
        r = json.loads(l); pid = r.get("passage_id")
        if pid is None: null_pid += 1
        elif pid not in passages: bad += 1
    print(f"{fname}: bad_ref={bad} null_pid={null_pid}")
```

### C4 — Chunk sentence integrity
```python
import json
chunks = [json.loads(l) for l in open("build/t306_chunks.jsonl", encoding="utf-8") if l.strip()]
cand = [c for c in chunks if c["status"] == "candidate"]
print(f"Total={len(chunks)} candidate(not-sentence-ended)={len(cand)}")
if cand[:3]: print("Sample candidate osis_end:", [c["osis_end"] for c in cand[:3]])
```

---

## What NOT to implement (escalate to Claude)

| Topic | Why not Codex |
|-------|---------------|
| TextSpan generator | Requires biblical literary boundary judgment |
| Boundary-driven chunker | Requires genre/psalm/oracle/epistle policy decisions |
| Gold set curation (Ps 23, Rom 7-8, John 1) | Scholar-level chunk evaluation |
| ProvenanceRecord migration | Cross-cutting 864k-record rewrite (ADR-0007, Claude to scope) |
| New ADRs | Architecture decisions |
| Source-language alignment | Phase 5, multilingual boundary ADR required |

If you find bugs in any of the above: document in findings. Do not fix without escalation.

---

## Files read

- AI_FRONT_DOOR.md, MASTER_CONTEXT.md, PROJECT_STATUS.md, DATA_MAP.md
- T300–T305 handoffs (this file's context chain)
- All pipeline + script files listed in Deliverable A

## Files changed

- .ai/handoffs/T306/handoff.md (this file)
- (Codex: fill in on completion)

## Decisions made

- T306 is calibrated for Codex 5.5: exhaustive code review, targeted mechanical fixes, explicit tests. Design decisions escalate to Claude.

## Validation run

- command: (Codex: paste after running)
- result: (Codex: paste)
- failures: (Codex: paste)

## Known risks

- `data/canonical/` is gitignored; regenerate via `python pipelines/ingest/usfm_importer.py` before running checks.
- OneDrive file locks: if tests fail with permission errors, retry.
- Windows CRLF: `.gitattributes` normalises to LF; `read_text()` handles CRLF on read.

## Open questions

- Orphan `.ai/handoffs/T001-web-usfm-ingest/`: confirmed blank scaffold in T300 — safe to delete, but read and confirm before removing.

## Next agent instruction

After T306 review + mechanical fixes:
1. Mark T306 complete: ROADMAP_STATE, PROJECT_STATUS, current_focus, roadmap_events.
2. Commit all changes.
3. Run final `validate_all.py` + `pytest -q`.
4. Hand Sprint 3 to Claude (NOT Codex): TextSpan generator schema → boundary-driven chunker → gold set curation.
5. Human: enable branch protection on default branch (CODEOWNERS = @lowelltwong-alt).

---

## FINDINGS (Codex 5.5: fill in here on completion)

### Summary table

| ID | Severity | File | Issue | Status |
|----|----------|------|-------|--------|
| (fill in) | | | | |
