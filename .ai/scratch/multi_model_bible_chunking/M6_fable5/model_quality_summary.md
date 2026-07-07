# M6_fable5 — Quality Summary (literary_marker_aware_v2)

## Validators run

| Check | Result |
|---|---|
| `validate_whole_bible_chunk_map.py --book <B>` per book (via mark-complete) | PASS x66 |
| `validate_t423_literary_quality_protocol.py --book <B> --require-artifacts` per book | PASS x66 |
| `t423_merge_book_chunks.py` | PASS (1,456 chunks merged) |
| `validate_whole_bible_chunk_map.py --require-full-bible` | PASS |
| `validate_t423_literary_quality_protocol.py --require-artifacts` (whole folder) | PASS |
| `validate_t423_parallel_isolation.py` | FAIL — pre-existing condition, see below |

**Isolation validator note:** the failure names
`comparison/model_agreement_matrix.yaml`, a one-line **uncommitted owner modification that
predates this session** (it appears in the session-start `git status` snapshot, before any M6
write). All M6_fable5 content is untracked new files under the M6 folder only (`git status`
confirms `?? .../M6_fable5/`), and no comparison file was read or written by this run. The
validator fails closed on any dirty forbidden path and cannot distinguish pre-existing
working-tree state from agent writes — recorded as a harness gap (see
harness_recommendations.md #10). The owner's file was left untouched.

## Low-confidence profile (474 rows in each sidecar)

- **315 chapter-coincident caps** — literary units that legitimately equal a chapter (whole
  psalms, Lamentations' acrostic poems, Job speech-chapters, tale/vision chapters of Dan/Rev,
  Genesis scene-chapters). Boundary confidence is genuinely high for most of these; the cap is a
  protocol artifact and the dominant sidecar-noise source (top harness finding).
- **19 proverb-cluster chapter fallbacks** — the only true chapter-fallback in the map, logged
  per protocol for sentence-literature with no internal literary seams (Prov 10-22:16; 25-29;
  Eccl 10).
- **17 textual-variant pressure spans** — isolated precisely so variant-policy-first review can
  act: Mark 16:9-20; John 7:53-8:11; John 5:3b-4; Luke 22:19b-20; 22:43-44; 23:34a; Matt 6:13;
  Acts 8:37; 15:34; 24:6-8; Rom 16:25-27; 1Cor 14:33b-35; 1Tim 3:16; 1John 5:7-8; Mal 2:15-16;
  Jude 22-23; 1Sam 13:1 / 17-18 LXX block; Jer 25 and 49 MT/LXX order.
- **Theology/intertext/apocalyptic pressure spans (31)** — servant songs, Immanuel, seventy
  weeks, Olivet (x3), millennium, man of lawlessness, John 1:1/8:58/10:30, Matt 16:18 and 28:19,
  Rom 5:12-21 and 9-11, Heb warning passages, Jas 2:14-26, 1Pet 3:18-22, Zech 9-14 passion
  intertexts — all evidence-only, no doctrinal claim.
- **Speaker/discourse debates (14)** — John 3 voice boundaries (owner-review span respected,
  no attribution asserted), Job 27-28 voice mixing, Song poem edges, Rev 22 voice shifts,
  Gal 2:14-21 speech end, Rom 7 "I".
- **List/genealogy/regnal partitions (24)** — Chronicles registers, censuses, allotments,
  rosters, northern-king blocks.

## Frontier books

Dan (12 chunks) and Rev (33 chunks): every chunk `frontier_flag_considered: true`; 11 and 16
frontier-queue rows respectively — far above the one-row minimum.

## Self-assessment

Strongest: speech/oracle/discourse-formula books (Job, Haggai, the epistles) where explicit
formulae make seams machine-confirmable. Weakest: books whose true structure is invisible to the
substrate — unmarked hymns in prose epistles (Phil 2; Col 1), hidden acrostics (Nah 1), language
shifts (Ezra/Daniel Aramaic), and refrain-bounded units (Isa 9:8-10:4) — all logged in
grammar_literary_gap_register.jsonl.
