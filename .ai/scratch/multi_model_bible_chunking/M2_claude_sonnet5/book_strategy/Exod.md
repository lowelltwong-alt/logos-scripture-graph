# Book Strategy — Exodus (M2_claude_sonnet5)

- **strategy_id:** literary_marker_aware_v2 | **book:** Exod | **pilot_book:** false (not in T423 pilot set, but Wave 1 continues under owner-authorized pilot-gate override; see layer_decision_log.jsonl)

## Selected strategy
Macro-narrative-then-legal-block chunking. Exodus substrate: 40 chapters, 1213 verses, 349 `\p` markers, genre_narrative overall but ch.20-31/34-40 are law/construction material. Chapter-only chunking would flatten the plague cycle (ch.7-11, naturally one-plague-per-chunk) and the Tabernacle instruction/execution blocks (ch.25-31 / 35-40, which mirror each other almost verbatim and are naturally grouped, not naturally split at arbitrary chapter lines).

## Literature type / mixed genre
Narrative (Exodus events, plagues, Sinai theophany narrative frame) interleaved with law_code (Decalogue, Book of the Covenant, Tabernacle instructions) and one major poetic inset (Song of the Sea/Miriam, Exod.15, substrate-confirmed q1/q2 markers, ch.15 flagged has_poetry_or_liturgy_marker).

## Substrate markers considered
Paragraph-marker density (349 `\p`) used only as corroborating evidence, not automatic boundary; poetry markers (q1=20, q2=28, concentrated in ch.15) confirmed against the well-known Song of the Sea; footnote presence noted but not used as boundary authority.

## Strong's metadata — evidence only
Exodus carries substantial Hebrew Strong's tags; cited only where a specific Hebrew term is structurally relevant (e.g., the divine name YHWH at 3:14, 6:2-3), never as lexical-truth or doctrinal authority.

## Chapter-only fallback
Not used as a default. Several chunks do coincide with single chapters (e.g., ch.1, most plague chunks) because the narrative scene genuinely is chapter-bounded in this book; several others deliberately span or subdivide chapters (ch.3-4 as one unit; ch.20-23, 25-27, 28-29, 30-31, 35-39 as large legal/construction blocks) to avoid a silent chapter default.

## Expected low-confidence / doctrinally sensitive regions
Divine-name revelation (3:1-4:17, 6:2-30), the Decalogue (20:1-21), the Song of the Sea (15:1-21), and the Golden Calf (32:1-35) are flagged medium_low with sidecar rows — not because the boundaries are disputed, but because the theological content weight is high and downstream review-packet authors should be aware of it.

## Frontier / atlas candidate expectations
Roughly 6 rows expected, concentrated at the divine-name, Decalogue, Song of the Sea, and Golden Calf spans.
