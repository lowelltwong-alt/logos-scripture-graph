# T475 USFM Shadow Delta And Agent Hierarchy

## Purpose

T475 is the first live deployment of the task-local Sol/Terra/Luna hierarchy.
It measures the corpus-wide difference between the pre-T474 importer and the
T474 marker-anchor repair without replacing any committed data.

## Agent Hierarchy

- Sol is the architecture owner. Sol freezes inputs, acceptance criteria,
  escalation boundaries, and the pre-audit verdict.
- Terra is the medium-risk regeneration, parity, and measurement specialist.
- Luna is the bounded worker for exact commands, inventories, hashes, and
  repeated trials. Luna escalates every ambiguity to Terra.
- Claude is the independent checker. Claude receives only frozen evidence,
  cannot edit the implementation, and cannot repair its own findings.

The aliases and model identifiers exist only in the T475 task overlay. Durable
model routing remains capability-based.

## Balanced Value

Correctness, parity, determinism, and no authority leakage are mandatory.
Continuation of a Rust buildout also requires at least one measurable gain in
performance, deployment safety, operability, failure isolation, or repeated
compute cost. Speed cannot compensate for a mismatch. Correctness without any
operational value does not justify new Rust complexity.

Quality first does not mean giving every worker the whole repo. Each role gets
the smallest complete evidence slice needed for its responsibility, with
machine-readable checkpoints instead of silent truncation.

## Evidence Run

The baseline is commit c556f27510088a9f9fdac777fbd20c1817039448.
The candidate is T474 commit 2ea6db7b605400f1b9fcf1a05daacf6c752f63c8.
Both run against identical raw archive, source manifest, canon config, and
marker coverage. Three alternating trials must be deterministic.

Reports contain IDs, refs, marker metadata, field paths, and hashes, never full
Scripture text. Every importer output is counted and hashed. Witness, token,
event, boundary, heading, and chunk-input effects are separately visible.

## Stops

T475 does not run the chunker, emit chunks, replace canonical or processed data,
edit reviewed gold, choose a source tradition, change canon, or create theology,
graph, retrieval, vector, route, or evaluator authority.

T476 may begin only after Sol freezes the bundle and the independent audit
passes. T476 is still an owner packet, not regeneration authorization.

## Shadow Result

Three baseline/candidate trials were byte-deterministic. The exact ledger records
741,399 unchanged rows, 102,793 modified rows, five removals, and one modified
report file. Passage identity and cross-references are unchanged. The intended
repair removes 48 prior-heading/speaker witness contaminations and two bogus
Psalm 119 heading-derived tokens.

T475 is HOLD_WITH_FINDINGS because three footnotes embedded in Psalm descriptive
headings disappear from the typed footnote sidecar. Terra initially classified
that as expected editorial cleanup; Sol ruled that editorial-only content must
stay out of Scripture text and tokens while typed editorial metadata remains
recoverable. A separate narrow repair and new frozen run are required before
the independent audit and T476.

## CI Transition

The workflow deterministically regenerates candidate data before validate_all.
That state intentionally disagrees with seven pre-T474 generated-baseline
validators. T475 does not update those baselines. Instead, CI may defer exactly
those seven gates only after all ten generated JSONL surfaces match the frozen
candidate semantic digests. Any unknown or partial state fails closed. The
deferral expires with the repaired T475 revision and does not authorize T476.

The post-ingest DATA_MAP check follows the same rule: it may accept only the
exact five-row count delta proven by the frozen candidate manifest. The
committed DATA_MAP remains on the baseline until the repair and owner gate
authorize a real generated-baseline migration.

Pytest has a parallel finite transition list because several tests invoke the
same stale validators and Psalm-gold consumers directly. Exactly 25 named test
nodes may be skipped only after the frozen candidate semantic proof succeeds.
Baseline or unknown states skip nothing, and the list expires with the
T477-T479 baseline and gold migration.
