# Job audit toolkit — provenance

Rebuilt 2026-09-03 by the M8_fable orchestrator (Fable 5) for OW-2 item 2 (the
213-row Ps/Job/Prov/Eccl/Song semantic audit). The original Job campaign toolkit was
never mirrored into sp_durable and its session scratchpad no longer exists on disk,
so this AUDIT subset was regenerated deterministically from the same raw witnesses
(data/raw/bible/eng-web USFM + the OSHB Job.xml source view) with zero subagent
tokens: extract -> build_offset_map.py (byte proofs) -> build_verse_maps.py ->
build_pmarks.py -> _adapt_tools.py (mechanical tools from the Song r3 lineage).
Every numbering and marks fact is proven in web_mt_offset_map.json / pmarks_Job.json
and summarized in tools/TOOLKIT_AUDIT.md. Candidate-only, non-authorizing; the
shipped Job corpus (book_chunks/Job/chunks.jsonl) was NOT modified.
