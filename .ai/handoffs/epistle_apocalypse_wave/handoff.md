# Handoff: epistle_apocalypse_wave

- task id: epistle_apocalypse_wave
- agent name: Codex subagent
- mode: candidate-only literary refinement
- files read: `M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl`; NT `book_chunks/*/chunks.jsonl`; `scripts/validate_m7_sol_candidate_inventory.py`; `scripts/validate_whole_bible_chunk_map.py`
- files changed: `scripts/refine_sol_nt_epistles.py`; per-book chunks and consolidated candidate feed for Romans through Revelation
- decisions made: retained chapter-complete spans as provisional structural units; added discourse/literary-form labels and explicit Koine, cross-reference, and red-team holds; no theological or authoritative decisions
- validation performed: `python scripts/refine_sol_nt_epistles.py`; `python scripts/validate_m7_sol_candidate_inventory.py`; `python scripts/validate_whole_bible_chunk_map.py ... --require-full-bible --python-only` (all passed)
- risks introduced: metadata is deterministic scaffold enrichment, not independent specialist review; lexical/cross-reference entries are review leads only
- unresolved questions: specialist Greek/source verification, controller-backed B01 reports, boss adjudication and appeals remain pending
- exact next action: route Rom–Rev records through typed B01 role mesh and red-team packet; preserve all dissent and do not promote
