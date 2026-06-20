from __future__ import annotations

from pathlib import Path

from scripts.validate_chunking_agent_preflight import validate_preflight


ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
REGISTRY = ROOT / "docs" / "methodology" / "LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md"
SUPPLY_CHAIN = ROOT / "docs" / "methodology" / "CHUNKING_SKILL_SUPPLY_CHAIN.md"
LESSONS = ROOT / "docs" / "methodology" / "WORKFLOW_LESSONS.md"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"


def test_chunking_agent_preflight_validates() -> None:
    data = validate_preflight(PREFLIGHT)

    assert data["object_type"] == "chunking_agent_preflight_contract"
    assert "divine_name_title_capitalization" in data["non_authorizing_metadata_types"]
    assert "divine_pronoun_capitalization" in data["non_authorizing_metadata_types"]
    assert data["metadata_authority_policy"]["may_preserve_as_evidence"] is True
    assert data["metadata_authority_policy"]["authorizes_chunk_boundaries"] is False
    assert data["metadata_authority_policy"]["authorizes_graph_edges"] is False
    assert data["metadata_authority_policy"]["authorizes_output_change"] is False
    reading = {item["path"]: item for item in data["mandatory_reading"]}
    assert ".ai/control/wj_marker_inventory.yaml" in reading
    assert ".ai/control/wj_speaker_discourse_policy.yaml" in reading
    assert ".ai/control/john3_wj_owner_review_docket.yaml" in reading
    assert ".ai/control/bible_wide_chunking_research_registry.yaml" in reading
    assert ".ai/control/source_metadata_research_atlas.yaml" in reading
    assert ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml" in reading
    assert ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml" in reading
    assert ".ai/control/gospel_wj_discourse_dossier_queue.yaml" in reading
    assert ".ai/control/narrative_legal_covenant_dossier_queue.yaml" in reading
    assert ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml" in reading
    assert ".ai/control/prophetic_oracle_vision_dossier_queue.yaml" in reading
    assert ".ai/control/textual_variant_source_tradition_dossier_queue.yaml" in reading
    assert ".ai/control/orthodox_original_language_pressure_dossier_queue.yaml" in reading
    assert ".ai/control/original_language_phrase_context_policy.yaml" in reading
    assert ".ai/control/orthodox_hermeneutic_firewall_docket.yaml" in reading
    assert ".ai/control/textual_critical_policy_docket.yaml" in reading
    assert ".ai/control/textual_critical_policy_owner_options.yaml" in reading
    assert ".ai/control/textual_critical_case_policy.yaml" in reading
    assert ".ai/control/t371_variant_dependency_owner_decision_packet.yaml" in reading
    assert ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml" in reading
    assert ".ai/control/t372_route_isolation_harness_plan.yaml" in reading
    assert ".ai/control/t373_owner_implementation_authorization.yaml" in reading
    assert ".ai/control/owner_decision_option_presentation_policy.yaml" in reading
    assert ".ai/control/1cor8_10_epistle_owner_review_docket.yaml" in reading
    assert ".ai/control/chunking_human_decision_forecast.yaml" in reading
    assert ".ai/control/governance_memory_durability_policy.yaml" in reading
    assert ".ai/control/owner_decision_projection_policy.yaml" in reading
    assert "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml" in reading
    assert "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json" in reading


def test_front_door_requires_metadata_preflight() -> None:
    text = FRONT_DOOR.read_text(encoding="utf-8")

    assert ".ai/control/chunking_agent_preflight.yaml" in text
    assert "CHUNK-METADATA-001" in text
    assert "Source metadata is evidence, not authority" in text
    assert "divine-name/title capitalization" in text
    assert "wj_marker_inventory.yaml" in text
    assert "wj_speaker_discourse_policy.yaml" in text
    assert "john3_wj_owner_review_docket.yaml" in text
    assert "bible_wide_chunking_research_registry.yaml" in text
    assert "source_metadata_research_atlas.yaml" in text
    assert "apocalyptic_prophetic_intertext_dossier_queue.yaml" in text
    assert "epistle_argument_theological_issue_dossier_queue.yaml" in text
    assert "gospel_wj_discourse_dossier_queue.yaml" in text
    assert "narrative_legal_covenant_dossier_queue.yaml" in text
    assert "wisdom_dialogue_poetry_dossier_queue.yaml" in text
    assert "prophetic_oracle_vision_dossier_queue.yaml" in text
    assert "textual_variant_source_tradition_dossier_queue.yaml" in text
    assert "orthodox_original_language_pressure_dossier_queue.yaml" in text
    assert "original_language_phrase_context_policy.yaml" in text
    assert "validate_original_language_phrase_context_policy.py" in text
    assert "orthodox_hermeneutic_firewall_docket.yaml" in text
    assert "textual_critical_policy_docket.yaml" in text
    assert "textual_critical_policy_owner_options.yaml" in text
    assert "textual_critical_case_policy.yaml" in text
    assert "t371_variant_dependency_owner_decision_packet.yaml" in text
    assert "t371_parent_only_reviewed_gold_promotion.yaml" in text
    assert "t372_route_isolation_harness_plan.yaml" in text
    assert "t373_owner_implementation_authorization.yaml" in text
    assert "owner_decision_option_presentation_policy.yaml" in text
    assert "epistle_argument_gold_manifest.json" in text
    assert "1cor8_10_epistle_owner_review_docket.yaml" in text
    assert "chunking_human_decision_forecast.yaml" in text
    assert "governance_memory_durability_policy.yaml" in text
    assert "owner_decision_projection_policy.yaml" in text
    assert "1cor8_10_parent_only_evidence_packet.yaml" in text
    assert "conflicting prior owner decisions" in text
    assert "projected owner pattern" in text
    assert "predictable owner decisions" in text
    assert "T352 is the next" not in text
    assert "currently points to T374 first route-isolated" in text
    assert "God/god" in text
    assert "Spirit/spirit" in text
    assert "Word/word" in text
    assert "graph edges" in text


def test_metadata_rule_is_first_class_methodology() -> None:
    registry = REGISTRY.read_text(encoding="utf-8")
    supply = SUPPLY_CHAIN.read_text(encoding="utf-8")
    lessons = LESSONS.read_text(encoding="utf-8")
    register = REGISTER.read_text(encoding="utf-8")

    assert "CHUNK-METADATA-001" in registry
    assert "Source Metadata Is Evidence, Not Authority" in registry
    assert "internal cross-references" in registry
    assert "Strong's-style" in registry
    assert "graph-edge authority" in registry
    assert "10o. Chunking-agent preflight and source-metadata rule" in supply
    assert "BIBLE-CHUNKING-WORKFLOW-LESSON-003" in lessons
    assert "BIBLE-CHUNKING-WORKFLOW-LESSON-004" in lessons
    assert "WORKFLOW-LESSON-004" in lessons
    assert "AI Tables Of Contents Need Tags And Use-When Routing" in lessons
    assert "CD-015" in register
    assert "CD-018" in register
    assert "CD-021" in register
    assert "CD-022" in register
    assert "CD-023" in register
    assert "CD-024" in register
    assert "CD-025" in register
    assert "CD-026" in register
    assert "CD-027" in register
    assert "CD-028" in register
    assert "CD-029" in register
    assert "CD-030" in register
    assert "CD-031" in register
    assert "CD-032" in register
    assert "CD-033" in register
    assert "CD-034" in register
    assert "CD-035" in register
    assert "CD-036" in register
    assert "CD-037" in register
    assert "CD-038" in register
    assert "CD-039" in register
    assert "CD-040" in register
    assert "CD-041" in register
    assert "CD-042" in register
    assert "CD-043" in register
    assert "CD-044" in register
    assert "CD-045" in register
    assert "CD-046" in register
    assert "CD-047" in register
    assert "CD-048" in register
    assert "CD-049" in register
    assert "CD-050" in register
    assert "CD-051" in register
    assert "CD-052" in register
    assert "CD-053" in register
    assert "Bible-wide research registry is canonical coverage for review prep only" in register
    assert "Source-metadata research atlas is evidence-only review memory" in register
    assert "Apocalyptic and prophetic intertext dossiers preserve hermeneutic options" in register
    assert "Epistle argument issue dossiers preserve theological options" in register
    assert "Gospel/WJ discourse dossiers preserve speaker-boundary neutrality" in register
    assert "Narrative/legal covenant dossiers preserve covenant-boundary neutrality" in register
    assert "Wisdom/dialogue/poetry dossiers preserve poetic-boundary neutrality" in register
    assert "Prophetic/oracle/vision dossiers preserve fulfillment-boundary neutrality" in register
    assert "Textual-variant/source-tradition dossiers preserve canon-boundary neutrality" in register
    assert "Original-language pressure passages require governed review before chunk authority" in register
    assert "Original-language word evidence requires phrase and discourse context" in register
    assert "Textual-critical policy options block variant-sensitive reviewed-gold promotion" in register
    assert "TCP-T378-B case-by-case textual-critical policy selected as process pattern" in register
    assert "T371 variant-dependency owner decision packet is non-authorizing" in register
    assert "T372 route-isolation harness plan is non-authorizing" in register
    assert "T373-A authorizes exact parent-only 1 Corinthians 8-10 implementation pilot" in register
    assert "Owner gates must present options and repercussions" in register
    assert "Parent-first pilot then child-necessity review is an authorized general pattern" in register
    assert "Greek and Hebrew chunking evidence requires governed language lessons" in register
    assert "Divine-name capitalization is evidence, not graph or chunk authority" in register
    assert "Words-of-Jesus marker inventory is observed evidence only" in register
    assert "WJ speaker and discourse policy selects John 3 for review only" in register
    assert "1 Corinthians 8-10 strengthened packet remains non-authorizing" in register
    assert "Human decision forecast front-loads chunking gates" in register


def test_divine_capitalization_is_mandatory_preflight_reading() -> None:
    data = validate_preflight(PREFLIGHT)
    reading = {item["path"]: item for item in data["mandatory_reading"]}
    register_entry = reading[".ai/control/chunking_theological_decision_register.yaml"]
    triage_entry = reading[".ai/control/bible_chunking_research_triage_map.yaml"]

    assert ".ai/control/divine_capitalization_inventory.yaml" in reading
    assert ".ai/control/wj_marker_inventory.yaml" in reading
    assert ".ai/control/wj_speaker_discourse_policy.yaml" in reading
    assert ".ai/control/john3_wj_owner_review_docket.yaml" in reading
    assert ".ai/control/bible_wide_chunking_research_registry.yaml" in reading
    assert ".ai/control/source_metadata_research_atlas.yaml" in reading
    assert ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml" in reading
    assert ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml" in reading
    assert ".ai/control/gospel_wj_discourse_dossier_queue.yaml" in reading
    assert ".ai/control/narrative_legal_covenant_dossier_queue.yaml" in reading
    assert ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml" in reading
    assert ".ai/control/prophetic_oracle_vision_dossier_queue.yaml" in reading
    assert ".ai/control/textual_variant_source_tradition_dossier_queue.yaml" in reading
    assert ".ai/control/orthodox_original_language_pressure_dossier_queue.yaml" in reading
    assert ".ai/control/original_language_phrase_context_policy.yaml" in reading
    assert ".ai/control/orthodox_hermeneutic_firewall_docket.yaml" in reading
    assert ".ai/control/textual_critical_policy_docket.yaml" in reading
    assert ".ai/control/textual_critical_policy_owner_options.yaml" in reading
    assert ".ai/control/textual_critical_case_policy.yaml" in reading
    assert ".ai/control/t371_variant_dependency_owner_decision_packet.yaml" in reading
    assert ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml" in reading
    assert ".ai/control/t372_route_isolation_harness_plan.yaml" in reading
    assert ".ai/control/t373_owner_implementation_authorization.yaml" in reading
    assert ".ai/control/owner_decision_option_presentation_policy.yaml" in reading
    assert ".ai/control/1cor8_10_epistle_owner_review_docket.yaml" in reading
    assert ".ai/control/chunking_human_decision_forecast.yaml" in reading
    assert ".ai/control/governance_memory_durability_policy.yaml" in reading
    assert ".ai/control/owner_decision_projection_policy.yaml" in reading
    assert "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml" in reading
    assert "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json" in reading
    assert "CD-018" in register_entry["required_decision_ids"]
    assert "CD-021" in register_entry["required_decision_ids"]
    assert "CD-022" in register_entry["required_decision_ids"]
    assert "CD-023" in register_entry["required_decision_ids"]
    assert "CD-024" in register_entry["required_decision_ids"]
    assert "CD-025" in register_entry["required_decision_ids"]
    assert "CD-026" in register_entry["required_decision_ids"]
    assert "CD-027" in register_entry["required_decision_ids"]
    assert "CD-028" in register_entry["required_decision_ids"]
    assert "CD-029" in register_entry["required_decision_ids"]
    assert "CD-030" in register_entry["required_decision_ids"]
    assert "CD-031" in register_entry["required_decision_ids"]
    assert "CD-032" in register_entry["required_decision_ids"]
    assert "CD-033" in register_entry["required_decision_ids"]
    assert "CD-034" in register_entry["required_decision_ids"]
    assert "CD-035" in register_entry["required_decision_ids"]
    assert "CD-036" in register_entry["required_decision_ids"]
    assert "CD-037" in register_entry["required_decision_ids"]
    assert "CD-038" in register_entry["required_decision_ids"]
    assert "CD-039" in register_entry["required_decision_ids"]
    assert "CD-040" in register_entry["required_decision_ids"]
    assert "CD-041" in register_entry["required_decision_ids"]
    assert "CD-042" in register_entry["required_decision_ids"]
    assert "CD-043" in register_entry["required_decision_ids"]
    assert "CD-044" in register_entry["required_decision_ids"]
    assert "CD-045" in register_entry["required_decision_ids"]
    assert "CD-046" in register_entry["required_decision_ids"]
    assert "CD-047" in register_entry["required_decision_ids"]
    assert "CD-048" in register_entry["required_decision_ids"]
    assert "CD-049" in register_entry["required_decision_ids"]
    assert "CD-050" in register_entry["required_decision_ids"]
    assert "CD-051" in register_entry["required_decision_ids"]
    assert "CD-052" in register_entry["required_decision_ids"]
    assert "CD-053" in register_entry["required_decision_ids"]
    assert "WORKFLOW-LESSON-004" in reading["docs/methodology/WORKFLOW_LESSONS.md"]["required_sections"]
    assert "divine_name_title_capitalization" in triage_entry["required_lane_ids"]
    assert "gospel_discourse_wj" in triage_entry["required_lane_ids"]


def test_midflight_lesson_capture_is_enforced() -> None:
    data = validate_preflight(PREFLIGHT)
    capture = data["midflight_lesson_capture"]

    assert capture["status"] == "required"
    assert "human_corrects_or_reminds_agent_about_a_rule_or_context" in capture["recognize_as_lesson_when"]
    assert "issue_could_recur_in_future_chunking_work" in capture["recognize_as_lesson_when"]
    assert "add_or_update_validator_or_test_if_machine_checkable" in capture["required_action_before_task_close"]
    assert ".ai/control/chunking_agent_preflight.yaml" in capture["required_surfaces"]
