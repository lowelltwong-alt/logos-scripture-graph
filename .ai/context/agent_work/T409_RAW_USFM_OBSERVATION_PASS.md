---
object_type: agent_work_raw_observation_ledger
trust_zone: learning-sidecar
lifecycle_status: active
provenance_note: "T409 full read-only pass over eng-web_usfm.zip (83 files) in canonical order."
reason_for_inclusion: "Per-file proof and in-situ marker inventory; qualifies atlas pilot synthesis."
---

# T409 Raw USFM Observation Pass

**Status:** `read_only_raw_source_observation`
**Contract scope:** `planning_only`
**Governance authority:** `false`
**Corpus:** `data/raw/bible/eng-web/usfm/eng-web_usfm.zip`
**Completed:** 2026-06-29

## Method

Every `.usfm` entry in `eng-web_usfm.zip` was opened, fully decoded (UTF-8-sig), and scanned
in canonical order per `config/canon/canonical_66_books.yaml` (66 canonical + 17 excluded appendix).
Observation used the same regex patterns as `scripts/scan_raw_sources.py` (LINE_MARKER, ANY_MARKER,
STRONG, VERSE, CHAPTER). Inline marker counts may double-count open/close pairs (known scan caveat).

**Does not authorize:** chunk output, reviewed gold, targets, route/evaluator, graph/retrieval truth,
boundary import, backend choice, canon-scope change, or control-plane promotion.

## Completion proof

- **Files opened:** 83 / 83
- **All files_read true:** True

| order | book_id | verses | sha256_short | files_read | risk_class |
|-------|---------|--------|--------------|------------|------------|
| 1 | Gen | 1533 | `b372891300de24c1` | True | `medium_risk` |
| 2 | Exod | 1213 | `cb6049c79104322c` | True | `medium_risk` |
| 3 | Lev | 859 | `46cdb8fb230227fc` | True | `medium_risk` |
| 4 | Num | 1288 | `4d970ffb1ca932c9` | True | `medium_risk` |
| 5 | Deut | 959 | `74b7d735d0b10801` | True | `medium_risk` |
| 6 | Josh | 658 | `1fa5301a06581cd3` | True | `low_risk` |
| 7 | Judg | 618 | `a357aba8519f73f7` | True | `low_risk` |
| 8 | Ruth | 85 | `0bff2c99d7d9e7a4` | True | `low_risk` |
| 9 | 1Sam | 810 | `e36ef4f76582f4e3` | True | `low_risk` |
| 10 | 2Sam | 695 | `5e4a90f474adfe9b` | True | `low_risk` |
| 11 | 1Kgs | 816 | `308d82320a010b5f` | True | `low_risk` |
| 12 | 2Kgs | 719 | `496072c3bea3e40d` | True | `low_risk` |
| 13 | 1Chr | 942 | `6e2af278e1ec8a83` | True | `low_risk` |
| 14 | 2Chr | 822 | `74a1682e1048bd5c` | True | `low_risk` |
| 15 | Ezra | 280 | `4b370951577f8d2b` | True | `medium_risk` |
| 16 | Neh | 406 | `ff83a1784ec29862` | True | `medium_risk` |
| 17 | Esth | 167 | `4cf6bbd3e566f96d` | True | `low_risk` |
| 18 | Job | 1070 | `0a26a0f438b5a1e4` | True | `high_risk` |
| 19 | Ps | 2461 | `396a93dd10087234` | True | `medium_risk` |
| 20 | Prov | 915 | `d8af12f9422a6b68` | True | `medium_risk` |
| 21 | Eccl | 222 | `9a72fa832bcc6665` | True | `low_risk` |
| 22 | Song | 117 | `3fb80c8e6b5bff0b` | True | `high_risk` |
| 23 | Isa | 1292 | `ce2eca09d1e89505` | True | `medium_risk` |
| 24 | Jer | 1364 | `17c5b2e6db5a2f45` | True | `medium_risk` |
| 25 | Lam | 154 | `952406886920c227` | True | `medium_risk` |
| 26 | Ezek | 1273 | `e8e3bf3c4207c5da` | True | `medium_risk` |
| 27 | Dan | 357 | `b5a967cabbfbec9b` | True | `medium_risk` |
| 28 | Hos | 197 | `8822524c87fab4a8` | True | `medium_risk` |
| 29 | Joel | 73 | `62f6d8f2b91f2812` | True | `medium_risk` |
| 30 | Amos | 146 | `22d85ec0ce20f2cd` | True | `medium_risk` |
| 31 | Obad | 21 | `afb16f1e5c6013f3` | True | `low_risk` |
| 32 | Jonah | 48 | `48809869414aecad` | True | `low_risk` |
| 33 | Mic | 105 | `efc32317b61ce2db` | True | `medium_risk` |
| 34 | Nah | 47 | `c4d0341d1608c3c7` | True | `low_risk` |
| 35 | Hab | 56 | `8d063f7bdf631634` | True | `low_risk` |
| 36 | Zeph | 53 | `e83b57ef78253d2a` | True | `low_risk` |
| 37 | Hag | 38 | `f0834e7a8798ea41` | True | `low_risk` |
| 38 | Zech | 211 | `e77fdd3eaa75a729` | True | `low_risk` |
| 39 | Mal | 55 | `fa50d3b312bb8664` | True | `low_risk` |
| 40 | Matt | 1071 | `d3badee3bbf638c1` | True | `medium_risk` |
| 41 | Mark | 678 | `4d8e70559f5c9152` | True | `medium_risk` |
| 42 | Luke | 1151 | `5080f1e4ccebc447` | True | `medium_risk` |
| 43 | John | 879 | `63b137c56182c894` | True | `high_risk` |
| 44 | Acts | 1007 | `dd2c9cab2078ad80` | True | `medium_risk` |
| 45 | Rom | 434 | `871701dbefcf2937` | True | `high_risk` |
| 46 | 1Cor | 437 | `ad005fab15ff20ed` | True | `high_risk` |
| 47 | 2Cor | 257 | `57c7d8e654913e9d` | True | `high_risk` |
| 48 | Gal | 149 | `6c4b5459ad5da171` | True | `high_risk` |
| 49 | Eph | 155 | `46217a837fec2e68` | True | `high_risk` |
| 50 | Phil | 104 | `38550627bef8473f` | True | `low_risk` |
| 51 | Col | 95 | `2de43728c5d7ff5a` | True | `low_risk` |
| 52 | 1Thess | 89 | `3ec133dfc226adf6` | True | `low_risk` |
| 53 | 2Thess | 47 | `96d5a75b573720be` | True | `low_risk` |
| 54 | 1Tim | 113 | `ce4db8f6e373c0d0` | True | `low_risk` |
| 55 | 2Tim | 83 | `316eb9ac78ef84a4` | True | `low_risk` |
| 56 | Titus | 46 | `b0972f9a19795a2d` | True | `low_risk` |
| 57 | Phlm | 25 | `69e84c056319dc36` | True | `low_risk` |
| 58 | Heb | 303 | `f09379a65743ef9b` | True | `high_risk` |
| 59 | Jas | 108 | `152bacb6d707cd4d` | True | `low_risk` |
| 60 | 1Pet | 105 | `b69835c9d7a4335a` | True | `low_risk` |
| 61 | 2Pet | 61 | `5e9be2935698fc22` | True | `low_risk` |
| 62 | 1John | 105 | `9489b5936979157a` | True | `low_risk` |
| 63 | 2John | 13 | `0d5f2e7d78908fd3` | True | `low_risk` |
| 64 | 3John | 14 | `e3398c33b667a77f` | True | `low_risk` |
| 65 | Jude | 25 | `9ed25eca8d7afc02` | True | `low_risk` |
| 66 | Rev | 404 | `5611fc446010957b` | True | `high_risk` |
| excluded | FRT | 0 | `09ecf533d97af7e0` | True | `complex` |
| excluded | GLO | 0 | `82933d659dc27b4a` | True | `medium_risk` |
| excluded | Tob | 244 | `683f9eaebd16cfa1` | True | `complex` |
| excluded | Jdt | 339 | `d8d450dec5bd9cce` | True | `complex` |
| excluded | AddEsth | 205 | `872957c59c2bee8b` | True | `complex` |
| excluded | Wis | 436 | `d06898f80170f21a` | True | `medium_risk` |
| excluded | Sir | 1383 | `102424b55c3e48a2` | True | `medium_risk` |
| excluded | Bar | 213 | `ec251954c01deff8` | True | `complex` |
| excluded | 1Macc | 924 | `44cfd0193d3d760a` | True | `medium_risk` |
| excluded | 2Macc | 555 | `cb76a13985932620` | True | `medium_risk` |
| excluded | 1Esd | 448 | `7d05bfcd8356d134` | True | `medium_risk` |
| excluded | PrMan | 15 | `018518186f0722c3` | True | `complex` |
| excluded | Ps151 | 7 | `1fb30c4c048b6fec` | True | `complex` |
| excluded | 3Macc | 228 | `02e9245f072fda29` | True | `complex` |
| excluded | 2Esd | 944 | `96cfee2e746cb0c8` | True | `medium_risk` |
| excluded | 4Macc | 484 | `5a55fef9593503a0` | True | `complex` |
| excluded | AddDan | 530 | `01ce54762a8be2ca` | True | `complex` |

## Risk rollup (canonical 66 only)

- `high_risk`: 10 books
- `low_risk`: 34 books
- `medium_risk`: 22 books

## Glossary deltas vs RAW_SOURCE_INVENTORY

Corpus-level totals from T409 per-file scan align with committed inventory (2026-06-04):
83 files, ~38,058 verses, ~1,402 chapters. Per-book marker sets match inventory families;
no new unknown line-leading markers observed beyond `usfm_marker_coverage.yaml` registry.

Notable per-book concentrations confirmed in situ:
- `\wj` — Gospels/Acts (NT red-letter); absent in Torah
- `\sp` — Job, Song (speaker dialogue)
- `\d` — Psalms superscriptions
- `\fqa` — variant readings distributed; higher in Torah historical books
- `\x`/ `\xo`/ `\xt` — cross-references throughout

## Atlas pilot qualifications (Torah)

T406 atlas pilot labeled Torah books from synthesis, not in-situ reading. T409 confirms:
- **Gen–Deut:** `medium_risk` at book_level from observed prose/law/list/footnote density;
  not `low_risk` as a whole-book default. Bounded spans (e.g. genealogies) remain `example_span_level` candidates.
- **No `\wj` in Torah** — atlas WJ notes apply to NT only; confirmed absent.
- Footnote (`\f`) and xref (`\x`) present in all Torah books; chunking must not treat as authority.

## Batch checkpoints

| Batch | File | Books |
|-------|------|-------|
| 01 | T409_BATCH_01.md | Gen–Ruth |
| 02 | T409_BATCH_02.md | 1Sam–2Chr |
| 03 | T409_BATCH_03.md | Ezra–Song |
| 04 | T409_BATCH_04.md | Isa–Mic |
| 05 | T409_BATCH_05.md | Nah–Mal |
| 06 | T409_BATCH_06.md | Matt–John |
| 07 | T409_BATCH_07.md | Acts–Col |
| 08 | T409_BATCH_08.md | 1Thess–Phlm |
| 09 | T409_BATCH_09.md | Heb–Rev |
| Appendix | T409_BATCH_APPENDIX.md | FRT, GLO, deuterocanonical |
