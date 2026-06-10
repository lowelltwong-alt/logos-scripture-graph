"""Tests for the T310 byte-identical chunking orchestrator."""
from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHUNKER = ROOT / "pipelines" / "chunking" / "chunker.py"
ORCHESTRATOR = ROOT / "pipelines" / "chunking" / "orchestrator.py"
CANON = ROOT / "data" / "canonical"
PASSAGES = CANON / "scripture" / "passages" / "passages.jsonl"
WITNESSES = CANON / "translations" / "eng-web" / "translation_witnesses.jsonl"
BOUNDARIES = CANON / "translations" / "eng-web" / "boundary_claims.jsonl"
FOOTNOTES = CANON / "translations" / "eng-web" / "footnotes.jsonl"
CROSSREFS = CANON / "translations" / "eng-web" / "editorial_cross_references.jsonl"

SMOKE_PASSAGES = [
    {"id": "scripture:John.1.1", "type": "ScripturePassage", "osis_ref": "John.1.1", "book": "John"},
    {"id": "scripture:John.1.2", "type": "ScripturePassage", "osis_ref": "John.1.2", "book": "John"},
    {"id": "scripture:John.1.3", "type": "ScripturePassage", "osis_ref": "John.1.3", "book": "John"},
]
SMOKE_WITNESSES = [
    {
        "id": "w1",
        "type": "TranslationWitness",
        "passage_id": "scripture:John.1.1",
        "osis_ref": "John.1.1",
        "text": "In the beginning was the Word.",
    },
    {
        "id": "w2",
        "type": "TranslationWitness",
        "passage_id": "scripture:John.1.2",
        "osis_ref": "John.1.2",
        "text": "The same was in the beginning with God.",
    },
    {
        "id": "w3",
        "type": "TranslationWitness",
        "passage_id": "scripture:John.1.3",
        "osis_ref": "John.1.3",
        "text": "All things were made through him.",
    },
]

CONTEXT_PASSAGES = [
    {
        "id": "scripture:Rom.1.1",
        "type": "ScripturePassage",
        "osis_ref": "Rom.1.1",
        "book": "Rom",
        "chapter": 1,
    },
    {
        "id": "scripture:Rom.1.2",
        "type": "ScripturePassage",
        "osis_ref": "Rom.1.2",
        "book": "Rom",
        "chapter": 1,
    },
]
CONTEXT_WITNESSES = [
    {
        "id": "w1",
        "type": "TranslationWitness",
        "passage_id": "scripture:Rom.1.1",
        "osis_ref": "Rom.1.1",
        "text": "Grace peace.",
    },
    {
        "id": "w2",
        "type": "TranslationWitness",
        "passage_id": "scripture:Rom.1.2",
        "osis_ref": "Rom.1.2",
        "text": "Therefore, stand firm.",
    },
]
CONTEXT_BOUNDARIES = [
    {"id": "b1", "type": "BoundaryClaim", "osis_ref": "Rom.1.1", "marker": "p"},
    {"id": "b2", "type": "BoundaryClaim", "osis_ref": "Rom.1.2", "marker": "p"},
]
CONTEXT_POLICY = """version: test-policy-v0
budgets:
  target_tokens: 1
  soft_max_tokens: 4
  hard_max_tokens: 10
"""

LEDGER_REQUIRED_FIELDS = {
    "type",
    "run_id",
    "source_corpus",
    "source_text_id",
    "chunking_policy_version",
    "registry_surface_sha",
    "route_mode",
    "skill_id",
    "skill_version",
    "registry_ref",
    "input_hash",
    "output_hash",
    "context_output_hash",
    "created_at",
    "validation_status",
    "form_based_routing_enabled",
    "detect_form_consumed",
}
ROUTE_METADATA_KEYS = {
    "route_mode",
    "skill_id",
    "skill_version",
    "registry_surface_sha",
    "input_hash",
    "output_hash",
    "form_based_routing_enabled",
    "detect_form_consumed",
    "route_reason",
    "candidate_skill_ids",
    "skills_used",
}
ROUTE_BOOKS = ("Ps", "Song", "Lam", "John")

requires_data = pytest.mark.skipif(
    not (PASSAGES.exists() and WITNESSES.exists() and BOUNDARIES.exists()),
    reason="canonical data not generated; run the importer first",
)


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return result


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _outside_ps89(records: list[dict]) -> list[dict]:
    return [
        record for record in records
        if not (
            str(record.get("osis_start", "")).startswith("Ps.89.")
            or str(record.get("osis_end", "")).startswith("Ps.89.")
        )
    ]


def _write_smoke_inputs(tmp_path: Path) -> tuple[Path, Path]:
    passages = tmp_path / "passages.jsonl"
    witnesses = tmp_path / "witnesses.jsonl"
    _write_jsonl(passages, SMOKE_PASSAGES)
    _write_jsonl(witnesses, SMOKE_WITNESSES)
    return passages, witnesses


def _write_context_inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    passages = tmp_path / "passages.jsonl"
    witnesses = tmp_path / "witnesses.jsonl"
    boundaries = tmp_path / "boundary_claims.jsonl"
    policy = tmp_path / "chunking_policy.yaml"
    _write_jsonl(passages, CONTEXT_PASSAGES)
    _write_jsonl(witnesses, CONTEXT_WITNESSES)
    _write_jsonl(boundaries, CONTEXT_BOUNDARIES)
    policy.write_text(CONTEXT_POLICY, encoding="utf-8")
    return passages, witnesses, boundaries, policy


def _write_route_inputs(tmp_path: Path) -> tuple[Path, Path]:
    passages = tmp_path / "route-passages.jsonl"
    witnesses = tmp_path / "route-witnesses.jsonl"
    passage_rows = []
    witness_rows = []
    for book in ROUTE_BOOKS:
        osis = f"{book}.1.1"
        passage_id = f"scripture:{osis}"
        passage_rows.append({
            "id": passage_id,
            "type": "ScripturePassage",
            "osis_ref": osis,
            "book": book,
            "chapter": 1,
        })
        witness_rows.append({
            "id": f"witness:{osis}",
            "type": "TranslationWitness",
            "passage_id": passage_id,
            "osis_ref": osis,
            "text": f"{book} control sentence.",
        })
    _write_jsonl(passages, passage_rows)
    _write_jsonl(witnesses, witness_rows)
    return passages, witnesses


def _tree_snapshot(root: Path) -> dict[str, tuple[int, int]]:
    if not root.exists():
        return {}
    return {
        path.relative_to(ROOT).as_posix(): (path.stat().st_size, path.stat().st_mtime_ns)
        for path in sorted(root.rglob("*"), key=lambda p: p.as_posix())
        if path.is_file()
    }


def _assert_no_route_metadata(path: Path) -> None:
    for record in _read_jsonl(path):
        leaked = ROUTE_METADATA_KEYS & set(record)
        assert not leaked, f"{path} leaked route metadata keys: {sorted(leaked)}"


def test_orchestrator_output_byte_identical_to_chunker_smoke(tmp_path: Path) -> None:
    passages, witnesses = _write_smoke_inputs(tmp_path)
    direct = tmp_path / "direct-chunks.jsonl"
    orchestrated = tmp_path / "orchestrated-chunks.jsonl"

    _run([
        sys.executable,
        str(CHUNKER),
        "--passages",
        str(passages),
        "--witnesses",
        str(witnesses),
        "--out",
        str(direct),
    ])
    _run([
        sys.executable,
        str(ORCHESTRATOR),
        "--passages",
        str(passages),
        "--witnesses",
        str(witnesses),
        "--out",
        str(orchestrated),
    ])

    assert direct.read_bytes() == orchestrated.read_bytes()
    assert _sha256(direct) == _sha256(orchestrated)
    _assert_no_route_metadata(orchestrated)


def test_orchestrator_context_output_byte_identical(tmp_path: Path) -> None:
    passages, witnesses, boundaries, policy = _write_context_inputs(tmp_path)
    direct_chunks = tmp_path / "direct-chunks.jsonl"
    direct_context = tmp_path / "direct-context.jsonl"
    orchestrated_chunks = tmp_path / "orchestrated-chunks.jsonl"
    orchestrated_context = tmp_path / "orchestrated-context.jsonl"

    _run([
        sys.executable,
        str(CHUNKER),
        "--passages",
        str(passages),
        "--witnesses",
        str(witnesses),
        "--boundary-claims",
        str(boundaries),
        "--policy",
        str(policy),
        "--out",
        str(direct_chunks),
        "--context-out",
        str(direct_context),
    ])
    _run([
        sys.executable,
        str(ORCHESTRATOR),
        "--passages",
        str(passages),
        "--witnesses",
        str(witnesses),
        "--boundary-claims",
        str(boundaries),
        "--policy",
        str(policy),
        "--out",
        str(orchestrated_chunks),
        "--context-out",
        str(orchestrated_context),
    ])

    assert direct_chunks.read_bytes() == orchestrated_chunks.read_bytes()
    assert direct_context.read_bytes() == orchestrated_context.read_bytes()
    assert _sha256(direct_chunks) == _sha256(orchestrated_chunks)
    assert _sha256(direct_context) == _sha256(orchestrated_context)
    assert len(_read_jsonl(direct_context)) == 1
    _assert_no_route_metadata(orchestrated_chunks)
    _assert_no_route_metadata(orchestrated_context)


@requires_data
def test_orchestrator_real_corpus_preserves_non_ps89_identity_when_data_present(tmp_path: Path) -> None:
    direct_chunks = tmp_path / "direct-chunks.jsonl"
    direct_context = tmp_path / "direct-context.jsonl"
    orchestrated_chunks = tmp_path / "orchestrated-chunks.jsonl"
    orchestrated_context = tmp_path / "orchestrated-context.jsonl"

    _run([
        sys.executable,
        str(CHUNKER),
        "--passages",
        str(PASSAGES),
        "--witnesses",
        str(WITNESSES),
        "--boundary-claims",
        str(BOUNDARIES),
        "--footnotes",
        str(FOOTNOTES),
        "--crossrefs",
        str(CROSSREFS),
        "--out",
        str(direct_chunks),
        "--context-out",
        str(direct_context),
    ])
    _run([
        sys.executable,
        str(ORCHESTRATOR),
        "--passages",
        str(PASSAGES),
        "--witnesses",
        str(WITNESSES),
        "--boundary-claims",
        str(BOUNDARIES),
        "--footnotes",
        str(FOOTNOTES),
        "--crossrefs",
        str(CROSSREFS),
        "--out",
        str(orchestrated_chunks),
        "--context-out",
        str(orchestrated_context),
    ])

    direct_records = _read_jsonl(direct_chunks)
    orchestrated_records = _read_jsonl(orchestrated_chunks)
    assert _outside_ps89(orchestrated_records) == _outside_ps89(direct_records)
    if direct_context.exists() or orchestrated_context.exists():
        assert direct_context.read_bytes() == orchestrated_context.read_bytes()
        assert _sha256(direct_context) == _sha256(orchestrated_context)
        _assert_no_route_metadata(orchestrated_context)
    ps23 = [c for c in orchestrated_records if c["osis_start"].startswith("Ps.23.") or c["osis_end"].startswith("Ps.23.")]
    assert len(ps23) == 1
    assert ps23[0]["osis_start"] == "Ps.23.1"
    assert ps23[0]["osis_end"] == "Ps.23.6"
    ps89 = [c for c in orchestrated_records if c["osis_start"].startswith("Ps.89.")]
    assert [(c["osis_start"], c["osis_end"]) for c in ps89] == [
        ("Ps.89.1", "Ps.89.4"),
        ("Ps.89.5", "Ps.89.18"),
        ("Ps.89.19", "Ps.89.37"),
        ("Ps.89.38", "Ps.89.45"),
        ("Ps.89.46", "Ps.89.48"),
        ("Ps.89.49", "Ps.89.52"),
    ]
    assert not any(c["osis_start"] == "Ps.89.52" and c["osis_end"] == "Ps.89.52" for c in ps89)
    ps119 = [c for c in orchestrated_records if c["osis_start"].startswith("Ps.119.")]
    assert len(ps119) > 1
    _assert_no_route_metadata(orchestrated_chunks)


def test_route_ledger_emitted_jsonl(tmp_path: Path) -> None:
    passages, witnesses = _write_smoke_inputs(tmp_path)
    chunks_without_ledger = tmp_path / "chunks-no-ledger.jsonl"
    missing_ledger = tmp_path / "not-requested-ledger.jsonl"
    chunks = tmp_path / "chunks.jsonl"
    ledger_path = tmp_path / "route-ledger.jsonl"

    _run([
        sys.executable,
        str(ORCHESTRATOR),
        "--passages",
        str(passages),
        "--witnesses",
        str(witnesses),
        "--out",
        str(chunks_without_ledger),
    ])
    assert not missing_ledger.exists()

    _run([
        sys.executable,
        str(ORCHESTRATOR),
        "--passages",
        str(passages),
        "--witnesses",
        str(witnesses),
        "--out",
        str(chunks),
        "--route-ledger",
        str(ledger_path),
    ])

    raw_lines = ledger_path.read_text(encoding="utf-8").splitlines()
    assert len(raw_lines) >= 2
    record = json.loads(raw_lines[0])
    assert set(record) >= LEDGER_REQUIRED_FIELDS
    assert record["type"] == "ChunkingRouteLedger"
    assert record["output_hash"] == _sha256(chunks)
    assert record["context_output_hash"] is None
    assert len(record["input_hash"]) == 64
    assert len(record["registry_surface_sha"]) == 64
    assert record["route_mode"] == "literal_psalm_candidate_seam"
    assert record["candidate_skill_ids"] == ["psalm-whole-then-stanza-v1"]
    assert record["validation_status"] in {
        "byte_identical_pending",
        "byte_identical_passed",
        "same_baseline_ps89_only_pending",
    }
    assert any(json.loads(line)["type"] == "ChunkingRouteLedgerRoute" for line in raw_lines[1:])


def test_route_ledger_declares_no_form_routing(tmp_path: Path) -> None:
    passages, witnesses = _write_smoke_inputs(tmp_path)
    chunks = tmp_path / "chunks.jsonl"
    ledger_path = tmp_path / "route-ledger.jsonl"

    _run([
        sys.executable,
        str(ORCHESTRATOR),
        "--passages",
        str(passages),
        "--witnesses",
        str(witnesses),
        "--out",
        str(chunks),
        "--route-ledger",
        str(ledger_path),
    ])

    record = _read_jsonl(ledger_path)[0]
    assert record["route_mode"] == "literal_psalm_candidate_seam"
    assert record["form_based_routing_enabled"] is False
    assert record["detect_form_consumed"] is False


def test_route_ledger_records_literal_psalm_candidate_and_non_ps_fallback(tmp_path: Path) -> None:
    passages, witnesses = _write_route_inputs(tmp_path)
    direct_chunks = tmp_path / "direct-chunks.jsonl"
    orchestrated_chunks = tmp_path / "orchestrated-chunks.jsonl"
    ledger_path = tmp_path / "route-ledger.jsonl"

    _run([
        sys.executable,
        str(CHUNKER),
        "--passages",
        str(passages),
        "--witnesses",
        str(witnesses),
        "--out",
        str(direct_chunks),
    ])
    _run([
        sys.executable,
        str(ORCHESTRATOR),
        "--passages",
        str(passages),
        "--witnesses",
        str(witnesses),
        "--out",
        str(orchestrated_chunks),
        "--route-ledger",
        str(ledger_path),
    ])

    assert direct_chunks.read_bytes() == orchestrated_chunks.read_bytes()
    records = _read_jsonl(ledger_path)
    routes = {record["book"]: record for record in records if record["type"] == "ChunkingRouteLedgerRoute"}
    assert routes["Ps"]["skill_id"] == "psalm-whole-then-stanza-v1"
    assert routes["Ps"]["route_reason"] == "literal_book_ps_candidate_seam"
    for book in ("Song", "Lam", "John"):
        assert routes[book]["skill_id"] == "monolith-pass2-v1"
        assert routes[book]["route_reason"] == "monolith_fallback_non_target_book"
    assert all(record["detect_form_consumed"] is False for record in records)
    assert all(record["form_based_routing_enabled"] is False for record in records)
    _assert_no_route_metadata(orchestrated_chunks)


def test_orchestrator_does_not_import_detect_form() -> None:
    source = ORCHESTRATOR.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.append(node.module)

    assert "pipelines.chunking.detect_form" not in imported_modules
    assert all(not name.endswith(".detect_form") for name in imported_modules)
    assert "--form-assignments" not in source
    assert "form_assignments" not in source


def test_no_raw_or_canonical_mutation(tmp_path: Path) -> None:
    before_raw = _tree_snapshot(ROOT / "data" / "raw")
    before_canonical = _tree_snapshot(ROOT / "data" / "canonical")
    passages, witnesses = _write_smoke_inputs(tmp_path)

    _run([
        sys.executable,
        str(ORCHESTRATOR),
        "--passages",
        str(passages),
        "--witnesses",
        str(witnesses),
        "--out",
        str(tmp_path / "chunks.jsonl"),
        "--route-ledger",
        str(tmp_path / "route-ledger.jsonl"),
    ])

    assert _tree_snapshot(ROOT / "data" / "raw") == before_raw
    assert _tree_snapshot(ROOT / "data" / "canonical") == before_canonical
