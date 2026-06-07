# T316 Biblical Chunking Stress Atlas

Status: complete as planning/gold inventory. No chunking implementation authorized.

## Purpose

T316 creates a proposed stress atlas for future chunking review. It identifies difficult passages
before any broad output-changing work, so target selection can proceed through reviewed gold instead
of aggregate score levers.

## Confirmed

- Main includes T315 and T314.
- Current official baseline remains D / Claude pass2 = 93.5 under T314 policy.
- Chunk output is unchanged.
- T316 does not change evaluator formula, chunker/orchestrator behavior, raw/canonical data, or
  runtime skill code.

## Deliverables

- `eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md`
- `eval/chunking_gold/stress_atlas/chunking_stress_cases.json`
- `tests/test_chunking_stress_atlas.py`

## Case Categories

The atlas covers:

- long structured units;
- long verses / administrative lists;
- very short context-dependent units;
- Greek long sentences;
- punctuation-dependent passages;
- major textual variants;
- DSS / LXX / MT divergence zones;
- speaker-change ambiguity;
- prophetic oracle collections;
- apocalyptic vision sequences;
- legal/covenant/case-law blocks;
- genealogies/censuses/lists;
- parallel accounts;
- rhetorical argument sections;
- hard exegesis passages;
- parent/child literary-unit candidates.

## Proposed High-Priority Follow-Ups

1. Text-critical boundary packet: Mark.16.9-20, John.7.53-8.11, Deut.32.8-9, 1Sam.10.27-11.1.
2. Long Psalm packet: Ps.89, Ps.105, Ps.106, Ps.136.
3. Prophetic/apocalyptic packet: Isa.52.13-53.12, Dan.10-12, Rev.12-18, Ezek.1, Zech.1-6.
4. Discourse/argument packet: John.13-17, Matt.24-25, Rom.9-11, Heb.7-10, 1Cor.8-10.
5. List/legal packet: Esther.8.9, 1Chr.1-9, Josh.13-21, Lev.16, Exod.20-23.

## Implementation Boundary

T316 is not a chunking improvement claim. A proposed stress case:

- is not reviewed gold;
- is not approved expected output;
- does not authorize output-changing work;
- must become reviewed gold or a reviewed packet before implementation;
- must pass evaluator sanity checks before score movement is trusted.

## Proposed Sequencing

1. Select a small packet from the atlas.
2. Convert it into review packets or per-form gold.
3. Add executable checks for reviewed cases.
4. Only then consider evaluator or chunking changes.

## Unknown

- Which packet should be reviewed first.
- Whether text-critical cases should wait for source-language witness work.
- Whether future stress packets need a dedicated manifest schema.
