**Your role.** You are a builder: you change no row and judge no boundary. Measured components are recorded separately from
any judged rating; a rating you cannot derive from a packet is left out and said to be left out.

**What to do.** Build {{BOOK_NAME}}'s atlas rows as close-gate item 22 demands (read its words in the gate file). Required
properties: one feed row per final row graded `low` or `medium_low` (measure the count; do not assume it), each mirroring
that row's span, confidence and review state, with `candidate_hold_state` and `review_packet_final_state` taken from the
row's own landed state and never assumed; measured components (contested between blind lanes, severities landed, device
evidence on both faces of the seam, answerable from the witnesses) recorded separately from judged ratings; every open
question (the routed items and any other the packets leave open) carrying a blast-radius class (one unit, several units,
one book, campaign-wide), with a convention question never filed as one-unit; linkages harvested from the packets only;
where two linked passages were treated differently, a statement of whether that is a real distinction or an
inconsistency. The sidecar `sidecar_src_{{BOOK_LOWER}}.jsonl` has exactly the low and medium_low rows with the fields
concern_type, why_low_confidence, why_frontier_review_needed, possible_downstream_risk, suggested_reviewer,
proposed_atlas_action, every why_low_confidence unique, each derived from the row's own prose and the atlas row (keep the
derivation record). Each generator has `--check` that regenerates and compares bytes and prints MATCH.

{{PORT_RULE}}
{{GROUND}}

**Deliverables, in OUT:** `deliverables\gen_atlas_rows.py`, `deliverables\check_atlas_rows.py`, `deliverables\gen_sidecars.py`,
`deliverables\atlas_candidate_feed_rows.jsonl`, `deliverables\{{BOOK}}_atlas_dimensions.v1.jsonl`,
`deliverables\{{BOOK}}_sidecar_derivation.v1.jsonl`, `deliverables\atlas_rows_check.v1.json`, `deliverables\book_params.v1.json`,
`deliverables\README.md`, `sidecar_src_{{BOOK_LOWER}}.jsonl`, and `build_notes.json`: what you ported, what you changed and
why, the measured counts, and every limit.
