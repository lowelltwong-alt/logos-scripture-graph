# Q8 COVERAGE STATEMENT — Ezekiel (template)

Authority: ruling Q8 of `ezek_controlling_rulings_a1#e2`, carried into the primaries gate by `ezek_controlling_rulings_a1#e3`,
and ratified with five amendments by ruling Q8-T of `ezek_controlling_rulings_a1#e4`. None of the amendments weakens
compensation 1; each is marked below with its letter.
The generator is `SP/Ezek/_coverage_statement_ezek.py`. This file fixes the statement's shape, and it also lists what
every execution from the primaries onward must capture from its first launch, so the statement can be built from the
record and never from prose.

## The rule (Q8, verbatim)

> Coverage statement = census output verbatim + per-execution layer table (A/B/C: present|UNAVAILABLE+reason) + the three
> compensations above with their evidence pointers. Never a summed count.

On a HARD book the whole-book final audit on deliverables plus OW-8 records is SUFFICIENT for the close, with three
compensations:

1. FULL dual-blind primary coverage of every row (no sampling).
2. The OW-6b second independent Fable review re-derives from bytes at least three rows per layer-A-lost part, chosen from
   the §7 regions.
3. The E-19 and splice-never-type self-reports of the lost-transcript executions are carried as SELF-REPORTED, not
   verified. The deterministic landing validator and the normalizer supply the layer-A-equivalent evidence for Hebrew
   byte-truth.

## Statement sections (the generator writes them in this order)

1. **CENSUS** — the Ezekiel block of `SP/campaign/_transcript_coverage_census.py`, copied verbatim: `attempts`,
   `transcript_retained`, `observed` and their notes. Never retyped, never summed with anything.
2. **PER-EXECUTION LAYER TABLE** — one line per execution id in `SP/campaign/capture_index.v1.jsonl` for book Ezek:
   - execution id, role, model ordered, outcome;
   - layer A: present, with the transcript's bytes and sha256, or UNAVAILABLE with the index's reason. It carries TWO
     behaviour classes side by side, each labelled, neither substituted for the other (Q8-T (b)):
     - the census-time class, from `SP/campaign/finding_ezek_transcripts_decayed_before_mirror.v3.json`;
     - the class observed when the statement is built: A = retained with bytes, B = the runtime file holds zero bytes.
     The statement records the runtime tasks root the generator probed and whether it exists. When it is absent, the
     class-now column reads 'UNAVAILABLE (runtime root not present)', never 'unknown', which would misreport decay as
     absence (Q8-T (c));
   - layer B: present or UNAVAILABLE with a reason;
   - layer C: the evidence note's path and sha256.
   The writer wave and Phase 0 classes come from `SP/campaign/finding_ezek_transcripts_decayed_before_mirror.v3.json`.
3. **COMPENSATIONS**, one block each, with evidence pointers:
   1. the primaries index — every row against both blind lanes, no sampling. The pointer reads EVIDENCE PRESENT only when
      the index lists every row id of the final rows file against both blind lanes' execution ids. The generator
      asserts the row-count and id-set equality, and otherwise writes 'PENDING (index covers N of M rows)' (Q8-T (d));
   2. the second Fable review's deliverable, listing its three or more byte-level re-derivations per layer-A-lost part;
   3. the executions whose self-reports are carried as SELF-REPORTED. Each layer-A-lost execution is listed with its
      landing receipt's path and sha256 and the deterministic results that receipt carries (parity, form defects, local
      tiling where applicable, E-01 normalizer counts), read from the receipts and never as a generic sentence (Q8-T (a)).
   A compensation whose evidence does not yet exist reads PENDING. It is never written as met.
   The generator's stdout per-class tally is a tally of table rows. It is never copied into the statement, and the
   statement's JSON keeps never_summed: true (Q8-T (e)). A dry-run statement is built over the current record before
   primaries launch, so the shape is proven on real inputs while compensations 1 and 2 read PENDING; a real build labelled
   'pre_primaries' follows before the primaries gate, and its digests are recorded (Q8-T orders).
4. **WHAT THE AUDIT READ** — the deliverables, the layer-C records, and layer A only where present.

## Capture checklist for every execution from the primaries onward (from the first launch)

- The launch message carries the E-13 preamble, both E-19 lines and the OW-11 authority paragraph (OW-11-h).
- At launch, the transcript map records the attempt (or `<attempt>_waveN`) against the runtime agent id, the model
  ordered and the execution id, through the guarded patch. The scratchpad copy is synced afterwards.
- The deliverable is written outside the worktree and landed with parity. Its receipt carries execution_id,
  previous_execution_id, tokens, tool uses, outcome, the brief and orders digests, and every form defect.
- The agent's final message is saved VERBATIM as the layer-C evidence note. When the runtime transcript holds zero bytes,
  it is taken from the completion notification. It is never reconstructed.
- Layer B is recorded UNAVAILABLE unless the runtime surfaced the agent's thinking.
- An execution that ends without a deliverable gets its own receipt and a verbatim note, and is relaunched under the next
  execution id. A second stop goes to the owner.
- `_mirror_transcripts.py` runs at every landing, and `_capture_index.py --write` is followed by `--check` GREEN.
