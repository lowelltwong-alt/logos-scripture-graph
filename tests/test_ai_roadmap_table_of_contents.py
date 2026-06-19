from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_main_toc_links_to_local_roadmap_toc() -> None:
    assert "docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md" in read(MAIN_TOC)


def test_main_toc_exposes_functional_tags_and_use_when_routing() -> None:
    toc = read(MAIN_TOC)

    assert "## Functional Tag Index" in toc
    assert "AI-facing tables of contents in this repo are routing surfaces" in toc
    assert "WORKFLOW-LESSON-004" in toc
    assert "tags:" in toc
    assert "use when:" in toc
    for phrase in [
        "`audit`, `no-context-review`, `red-team`, `a-b-check`, `review-report`",
        ".ai/audits/README.md",
        "developer-engineering",
        "whole-bible-research",
        "bible_wide_chunking_research_registry.yaml",
        "source-metadata",
        "source_metadata_research_atlas.yaml",
        "apocalyptic_prophetic_intertext_dossier_queue.yaml",
        "epistle_argument_theological_issue_dossier_queue.yaml",
        "gospel_wj_discourse_dossier_queue.yaml",
        "narrative_legal_covenant_dossier_queue.yaml",
        "wisdom_dialogue_poetry_dossier_queue.yaml",
        "prophetic_oracle_vision_dossier_queue.yaml",
        "textual_variant_source_tradition_dossier_queue.yaml",
        "orthodox_original_language_pressure_dossier_queue.yaml",
        "orthodox_hermeneutic_firewall_docket.yaml",
        "textual_critical_policy_docket.yaml",
        "textual_critical_policy_owner_options.yaml",
        "t371_variant_dependency_owner_decision_packet.yaml",
        "1cor8_10_epistle_owner_review_docket.yaml",
        "chunking_human_decision_forecast.yaml",
        "governance_memory_durability_policy.yaml",
        "owner_decision_projection_policy.yaml",
        "owner-projection",
        "conflict-scan",
        "orthodox-hermeneutic-firewall",
        "textual-critical-policy",
        "owner-options",
        "case-by-case",
        "reviewed-gold-blocker",
        "owner-decision-packet",
        "1cor8-10",
        "human-decision",
        "chunking-ready",
        "servant-song",
        "textual-variant",
        "source-tradition",
        "original-language",
        "grammar-overlay",
        "non-orthodox",
        "lds",
        "watch-tower",
        "nwt",
        "divine-plurality",
        "comma-johanneum",
        "john3",
        "task-scope",
        "graph",
        "cross-repo",
    ]:
        assert phrase in toc


def test_local_roadmap_toc_links_back_to_main_toc() -> None:
    assert "AI_TABLE_OF_CONTENTS.md" in read(ROADMAP_TOC)


def test_local_roadmap_toc_has_tags_and_use_when_columns() -> None:
    toc = read(ROADMAP_TOC)

    assert "## AI Routing Tags" in toc
    assert "| Task | Purpose | Tags | Use when | Primary artifacts |" in toc
    assert "| Surface | Tags | Use when | Role |" in toc
    for phrase in [
        "`audit`",
        "`task-scope`",
        "`john3`, `owner-review`, `speaker-boundary`",
        "`divine-capitalization`, `source-metadata`, `harness`",
        "`source-metadata-atlas`, `cross-references`, `strongs`, `wj`, `capitalization`",
        "`apocalyptic-prophetic`, `revelation`, `daniel`, `intertext`, `hermeneutic-neutrality`",
        "`epistle`, `argument-boundary`, `election`, `law-gospel`, `faith-works`, `assurance`",
        "`gospel-discourse-wj`, `red-letter`, `speaker-boundary`, `john3`, `sermon-on-mount`, `farewell-discourse`",
        "`narrative`, `legal`, `covenant`, `genealogy`, `lists`, `typology`, `harmonization`",
        "`wisdom`, `dialogue`, `poetry`, `acrostic`, `refrain`, `speaker-boundary`, `job`, `song`, `lamentations`, `ps119`",
        "`prophetic`, `oracle`, `vision`, `servant-song`, `temple-vision`, `day-of-yahweh`",
        "`textual-variant`, `source-tradition`, `canon-scope`, `boundary-routing`, `mark16`, `pericope-adulterae`",
        "`original-language`, `grammar-overlay`, `greek`, `hebrew`, `non-orthodox`, `lds`",
        "`orthodox-hermeneutic-firewall`, `anti-smuggling`, `orthodoxy-boundary`, `canon-authority`",
        "`textual-critical-policy`, `variant-sensitive`, `canon-scope-gate`, `source-tradition-gate`",
        "`textual-critical-policy`, `owner-options`, `variant-sensitive`, `case-by-case`, `1cor9-20`, `1cor10-9`",
        "`t371`, `variant-dependency`, `owner-decision-packet`, `reviewed-gold-promotion`, `1cor9-20`, `1cor10-9`, `parent-only`",
        "`1cor8-10`, `epistle`, `owner-review`, `conscience`, `idol-food`, `sacramental`",
        "`human-decision`, `chunking-ready`, `goal-blocked`, `stop-conditions`, `owner-gate`",
        "`owner-projection`, `projected-owner-pattern`, `conflict-scan`",
        "A reviewer needs the packet queue",
        "Checking the `john3_wj_speaker_boundary` owner-review options and the later selected parent-only target.",
    ]:
        assert phrase in toc


def test_local_roadmap_toc_exposes_t337a_actual_artifact_trail() -> None:
    toc = read(ROADMAP_TOC)

    assert ".ai/tasks/T337A.task.yaml" in toc
    assert ".ai/handoffs/T337A/handoff.md" in toc
    assert "eval/chunking_gold/review_packets/ps89_boundary_review.md" in toc


def test_local_roadmap_toc_exposes_t342_and_next_route() -> None:
    toc = read(ROADMAP_TOC)

    assert "docs/roadmap/T342_REVELATION_REVIEW_PACKET_CANDIDATE_SELECTION.md" in toc
    assert ".ai/tasks/T342.task.yaml" in toc
    assert ".ai/handoffs/T342/handoff.md" in toc
    assert "docs/roadmap/T343_REVELATION_REVIEW_PACKETS_AND_GOLD_CANDIDATES.md" in toc
    assert "eval/chunking_gold/review_packets/rev12_14_symbolic_scenes_review.md" in toc
    assert ".ai/control/chunking_agent_preflight.yaml" in toc
    assert "T353 | Divine capitalization inventory harness" in toc
    assert "Rev.12.1-Rev.14.20" in toc
    assert "docs/roadmap/T344_REVELATION_OWNER_SELECTION_DOCKET.md" in toc
    assert "docs/roadmap/T351_BIBLE_WIDE_CHUNKING_RESEARCH_TRIAGE_ATLAS.md" in toc
    assert "docs/roadmap/T352_EPISTLE_ARGUMENT_REVIEW_PACKETS.md" in toc
    assert ".ai/tasks/T352.task.yaml" in toc
    assert ".ai/handoffs/T352/handoff.md" in toc
    assert "docs/roadmap/T353_DIVINE_CAPITALIZATION_INVENTORY_HARNESS.md" in toc
    assert ".ai/control/divine_capitalization_inventory.yaml" in toc
    assert ".ai/tasks/T353.task.yaml" in toc
    assert ".ai/handoffs/T353/handoff.md" in toc
    assert "T354 | WJ/red-letter marker inventory harness" in toc
    assert "docs/roadmap/T354_WJ_MARKER_INVENTORY_HARNESS.md" in toc
    assert ".ai/control/wj_marker_inventory.yaml" in toc
    assert ".ai/tasks/T354.task.yaml" in toc
    assert ".ai/handoffs/T354/handoff.md" in toc
    assert "T355 | WJ speaker/discourse policy and target selection" in toc
    assert "docs/roadmap/T355_WJ_SPEAKER_POLICY_AND_TARGET_SELECTION.md" in toc
    assert ".ai/control/wj_speaker_discourse_policy.yaml" in toc
    assert ".ai/tasks/T355.task.yaml" in toc
    assert ".ai/handoffs/T355/handoff.md" in toc
    assert "T356 | John 3 WJ owner-review docket" in toc
    assert "docs/roadmap/T356_JOHN3_WJ_OWNER_REVIEW_DOCKET.md" in toc
    assert ".ai/control/john3_wj_owner_review_docket.yaml" in toc
    assert ".ai/tasks/T356.task.yaml" in toc
    assert ".ai/handoffs/T356/handoff.md" in toc
    assert "T358 | Bible-wide chunking research registry" in toc
    assert "docs/roadmap/T358_BIBLE_WIDE_CHUNKING_RESEARCH_REGISTRY.md" in toc
    assert ".ai/control/bible_wide_chunking_research_registry.yaml" in toc
    assert ".ai/tasks/T358.task.yaml" in toc
    assert ".ai/handoffs/T358/handoff.md" in toc
    assert "T359 | Source metadata research atlas" in toc
    assert "docs/roadmap/T359_SOURCE_METADATA_RESEARCH_ATLAS.md" in toc
    assert ".ai/control/source_metadata_research_atlas.yaml" in toc
    assert ".ai/tasks/T359.task.yaml" in toc
    assert ".ai/handoffs/T359/handoff.md" in toc
    assert "T360 | Apocalyptic prophetic intertext dossier queue" in toc
    assert "docs/roadmap/T360_APOCALYPTIC_PROPHETIC_INTERTEXT_DOSSIERS.md" in toc
    assert ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml" in toc
    assert ".ai/tasks/T360.task.yaml" in toc
    assert ".ai/handoffs/T360/handoff.md" in toc
    assert "T361 | Epistle argument theological issue dossier queue" in toc
    assert "docs/roadmap/T361_EPISTLE_ARGUMENT_THEOLOGICAL_ISSUE_DOSSIERS.md" in toc
    assert ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml" in toc
    assert ".ai/tasks/T361.task.yaml" in toc
    assert ".ai/handoffs/T361/handoff.md" in toc
    assert "T362 | Gospel WJ discourse dossier queue" in toc
    assert "docs/roadmap/T362_GOSPEL_WJ_DISCOURSE_DOSSIERS.md" in toc
    assert ".ai/control/gospel_wj_discourse_dossier_queue.yaml" in toc
    assert ".ai/tasks/T362.task.yaml" in toc
    assert ".ai/handoffs/T362/handoff.md" in toc
    assert "T363 | Narrative legal covenant dossier queue" in toc
    assert "docs/roadmap/T363_NARRATIVE_LEGAL_COVENANT_DOSSIERS.md" in toc
    assert ".ai/control/narrative_legal_covenant_dossier_queue.yaml" in toc
    assert ".ai/tasks/T363.task.yaml" in toc
    assert ".ai/handoffs/T363/handoff.md" in toc
    assert "T364 | Wisdom dialogue poetry dossier queue" in toc
    assert "docs/roadmap/T364_WISDOM_DIALOGUE_POETRY_DOSSIERS.md" in toc
    assert ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml" in toc
    assert ".ai/tasks/T364.task.yaml" in toc
    assert ".ai/handoffs/T364/handoff.md" in toc
    assert "T365 | Prophetic oracle vision dossier queue" in toc
    assert "docs/roadmap/T365_PROPHETIC_ORACLE_VISION_DOSSIERS.md" in toc
    assert ".ai/control/prophetic_oracle_vision_dossier_queue.yaml" in toc
    assert ".ai/tasks/T365.task.yaml" in toc
    assert ".ai/handoffs/T365/handoff.md" in toc
    assert "T366 | Textual variant source tradition dossier queue" in toc
    assert "docs/roadmap/T366_TEXTUAL_VARIANT_SOURCE_TRADITION_DOSSIERS.md" in toc
    assert ".ai/control/textual_variant_source_tradition_dossier_queue.yaml" in toc
    assert ".ai/tasks/T366.task.yaml" in toc
    assert ".ai/handoffs/T366/handoff.md" in toc
    assert "scripts/validate_textual_variant_source_tradition_dossier_queue.py" in toc
    assert "T367 | Owner decision firewall and next target" in toc
    assert "docs/roadmap/T367_OWNER_DECISION_FIREWALL_AND_NEXT_TARGET.md" in toc
    assert ".ai/control/orthodox_hermeneutic_firewall_docket.yaml" in toc
    assert ".ai/control/textual_critical_policy_docket.yaml" in toc
    assert ".ai/tasks/T367.task.yaml" in toc
    assert ".ai/handoffs/T367/handoff.md" in toc
    assert "T368 | 1 Corinthians 8-10 packet strengthening" in toc
    assert "docs/roadmap/T368_1COR8_10_PACKET_STRENGTHENING.md" in toc
    assert ".ai/control/1cor8_10_epistle_owner_review_docket.yaml" in toc
    assert ".ai/control/chunking_human_decision_forecast.yaml" in toc
    assert ".ai/tasks/T368.task.yaml" in toc
    assert ".ai/handoffs/T368/handoff.md" in toc
    assert "T369 |" in toc
    assert "docs/roadmap/T369_HUMAN_DECISION_FORECAST_AND_CHUNKING_READY_ROADMAP.md" in toc
    assert "scripts/validate_chunking_human_decision_forecast.py" in toc
    assert ".ai/control/owner_decision_projection_policy.yaml" in toc
    assert ".ai/control/governance_memory_durability_policy.yaml" in toc
    assert "scripts/validate_owner_decision_projection_policy.py" in toc
    assert "scripts/validate_governance_memory_durability.py" in toc
    assert "T370 | 1Cor.8-10 parent-only evidence packet" in toc
    assert "T377 | Orthodox original-language pressure passage queue" in toc
    assert "docs/roadmap/T377_ORTHODOX_ORIGINAL_LANGUAGE_PRESSURE_DOSSIERS.md" in toc
    assert ".ai/control/orthodox_original_language_pressure_dossier_queue.yaml" in toc
    assert "scripts/validate_orthodox_original_language_pressure_dossier_queue.py" in toc
    assert ".ai/tasks/T377.task.yaml" in toc
    assert ".ai/handoffs/T377/handoff.md" in toc
    assert "T378 | Textual-critical policy owner options" in toc
    assert "docs/roadmap/T378_TEXTUAL_CRITICAL_POLICY_OWNER_OPTIONS.md" in toc
    assert ".ai/control/textual_critical_policy_owner_options.yaml" in toc
    assert "scripts/validate_textual_critical_policy_owner_options.py" in toc
    assert ".ai/tasks/T378.task.yaml" in toc
    assert ".ai/handoffs/T378/handoff.md" in toc
    assert "T379 | Textual-critical case-by-case policy selection" in toc
    assert "docs/roadmap/T379_TEXTUAL_CRITICAL_CASE_POLICY_SELECTION.md" in toc
    assert ".ai/control/textual_critical_case_policy.yaml" in toc
    assert "scripts/validate_textual_critical_case_policy.py" in toc
    assert ".ai/tasks/T379.task.yaml" in toc
    assert ".ai/handoffs/T379/handoff.md" in toc
    assert "ODP-005" in toc
    assert "T380 | T371 owner decision packet" in toc
    assert "docs/roadmap/T380_T371_VARIANT_DEPENDENCY_OWNER_DECISION_PACKET.md" in toc
    assert ".ai/control/t371_variant_dependency_owner_decision_packet.yaml" in toc
    assert "scripts/validate_t371_variant_dependency_owner_decision_packet.py" in toc
    assert ".ai/tasks/T380.task.yaml" in toc
    assert ".ai/handoffs/T380/handoff.md" in toc
    assert "T371 - Owner reviewed-gold promotion decision" in toc
    assert "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml" in toc
    assert "john3_wj_speaker_boundary" in toc
    assert "REV-T344-E" in toc
    assert "review_packet_ready" in toc
