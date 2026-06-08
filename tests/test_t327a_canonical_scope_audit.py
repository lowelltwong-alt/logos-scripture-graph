from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "roadmap" / "T327A_FORENSIC_CANONICAL_CORPUS_SCOPE_AUDIT.md"
POLICY = ROOT / "docs" / "roadmap" / "CANONICAL_66_BOOK_SCOPE_POLICY.md"
TASK = ROOT / ".ai" / "tasks" / "T327A.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T327A" / "handoff.md"

REQUIRED_EXCLUDED_IDS = {
    "Tob",
    "Jdt",
    "AddEsth",
    "Wis",
    "Sir",
    "Bar",
    "1Macc",
    "2Macc",
    "1Esd",
    "PrMan",
    "Ps151",
    "3Macc",
    "2Esd",
    "4Macc",
    "AddDan",
    "FRT",
    "GLO",
}

FUTURE_TASKS = {"T327B", "T327C", "T327D", "T327E", "T327F", "T327G"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_t327a_audit_and_policy_documents_exist() -> None:
    assert AUDIT.exists()
    assert POLICY.exists()
    assert TASK.exists()
    assert HANDOFF.exists()


def test_canonical_policy_records_owner_scope_and_exclusions() -> None:
    text = read(POLICY)
    lowered = text.lower()
    assert "66-book canon" in lowered
    assert "owner decision" in lowered
    assert "deuterocanonical" in lowered
    assert "apocrypha" in lowered
    assert "front matter and glossary" in lowered
    assert "logos-boundary-literature" in text
    assert "do not hand-edit raw archives" in lowered
    for excluded_id in REQUIRED_EXCLUDED_IDS:
        assert excluded_id in text


def test_audit_records_current_counts_and_affected_surfaces() -> None:
    text = read(AUDIT)
    assert "archive entries: 87" in text
    assert "USFM files: 83" in text
    assert "15 deuterocanonical/apocrypha/non-66 USFM files" in text
    assert "total records: 38,058" in text
    assert "books: 81" in text
    assert "canonical 66-book records: 31,103" in text
    assert "excluded deuterocanonical/apocrypha records: 6,955" in text
    for surface in [
        "data/processed/bible/eng-web/usfm/usfm_events.jsonl",
        "data/canonical/scripture/passages/passages.jsonl",
        "data/canonical/translations/eng-web/translation_witnesses.jsonl",
        "data/derived/chunks/variants/*/chunks.jsonl",
        "eval/chunking_runs/*.json",
        "eval/LEADERBOARD.md",
        "eval/chunking_gold/**",
        "tests/**",
    ]:
        assert surface in text


def test_audit_records_forensic_commits_and_prs() -> None:
    text = read(AUDIT)
    for commit in [
        "63d74b4",
        "e191420",
        "1a8c3fd",
        "5313b0f",
        "e8d9993",
        "d64ea59",
        "7c5dbb0",
        "72e9c14",
    ]:
        assert commit in text
    for pr in ["#1", "#3", "#4", "#6", "#13", "#17", "#22"]:
        assert pr in text
    for command in [
        "git show --stat",
        "git show --name-status",
        "gh pr diff",
        "gh pr view",
    ]:
        assert command in text


def test_t327a_is_planning_only_and_non_authorizing() -> None:
    combined = "\n".join(read(path) for path in [AUDIT, POLICY, TASK, HANDOFF])
    lowered = combined.lower()
    assert "audit only" in lowered
    assert "does not implement removal" in lowered
    assert "do not implement" in lowered or "not implemented in t327a" in lowered
    assert "do not mutate raw" in lowered or "no raw/canonical mutation" in lowered
    assert "does not claim chunking improvement" in lowered or "not chunking improvement" in lowered
    assert "leaderboard is not run" in lowered or "did not run the leaderboard" in lowered
    forbidden_positive_phrases = {
        "implementation_allowed: true",
        "output_change_authorized: true",
        "authorizes output-changing work",
        "this is a chunking improvement",
    }
    for phrase in forbidden_positive_phrases:
        assert phrase not in lowered


def test_future_sequence_is_split_into_isolated_tasks() -> None:
    text = read(AUDIT)
    for task_id in FUTURE_TASKS:
        assert task_id in text
    assert "allow-list / ingest filter" in text
    assert "Regenerate Canonical Outputs" in text
    assert "Regenerate Chunks, Scorecards, Leaderboard" in text
    assert "Clean Gold / Stress / Observed / Index Surfaces" in text
    assert "Boundary Repo Source-Intake Plan" in text
    assert "Optional Raw Source Artifact Replacement / Migration Plan" in text


def test_task_handoff_records_protected_paths() -> None:
    task_text = read(TASK)
    for protected_path in [
        "data/raw/",
        "data/canonical/",
        "data/processed/",
        "data/derived/chunks/",
        "pipelines/ingest/",
        "pipelines/chunking/chunker.py",
        "pipelines/chunking/orchestrator.py",
        "pipelines/chunking/evaluate_chunks.py",
        "pipelines/chunking/leaderboard.py",
        "eval/chunking_runs/",
        "eval/LEADERBOARD.md",
    ]:
        assert protected_path in task_text
