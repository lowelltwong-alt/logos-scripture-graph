# M8 orchestration playbook v5 — 2026-11-03

Operational delta only. Preserve v1-v4 as history. Written at the 1 Corinthians close
(close-gate item 18, OW-14) because that book's evidence changed recommendations.
Candidate-only and non-authorizing: owner directives, the error-pattern ledger, the
close gate and the controlling agent's rulings outrank anything here.

No semantic method, gate, independent-review floor or authority is changed. Each
recommendation below names the learning-log entries that justify it
(orchestration_learning_log.v1.jsonl).

## Changed since v4

### Rounds and rulings
- Keep converging rounds narrow: rule on the findings, write the next check as a
  delta over the changed elements, carry unchanged rows by byte equality
  (L-0095, L-0096, L-0098, L-0103).
- Before any ruling round that orders row bytes, the orchestrator applies the
  candidate spans to a private copy, runs the tools, and pins that report, so the
  round reads a result and rules. A fix-up then becomes a mechanical apply with a
  known digest (L-0097, L-0102, L-0110, L-0111, L-0112).
- Every gate clause names the run that decides it, in the same sentence. A clause
  whose reach is ambiguous goes back to the controlling agent (L-0098, L-0099).
- On a hard book, keep one whole-row read after the delta reviews (boss audit),
  then a delta boss after an exact-span fix-up (L-0101, L-0103).
- Treat an all-ADOPT adjudication as a prompt to test the weakest two rulings, and
  report the changed-text count beside the adopt count (L-0107).
- Run the variant-disclosure check as a sweep before the primaries, and keep a
  reception lens on contested chapters (L-0090).

### Briefs and lanes
- Before a brief is built, sweep the book's rulings for duties laid on the lanes,
  and make the generator refuse until each is carried (L-0108).
- Generator lanes pin a frozen copy of the landed manifest, never the live file
  (L-0105). Before any launch, run every generator a lane pins in --check mode
  (L-0116, L-0117).
- Lanes see check output before installing deliverables; an 18-row sample is not
  enough for a merged verdict (L-0109).
- Budgets from units: about 35 calls for a narrow controlling round, about 50 (stop
  at 75) for a larger one, about 70 (stop at 100) for a delta boss (L-0099, L-0102,
  L-0103).
- Do not launch above about 60% of the 5-hour limit; plan parallel close lanes at
  about 3% of the limit per lane-minute (L-0100, L-0103, L-0105, L-0117).

### Landing and evidence
- At landing, check every brief-required field of a lane deliverable for presence
  and type and report all defects at once. Correct by continuation message plus an
  amendment row with a field-by-field check, never by hand (L-0118).
- Copy tools, messages and landed deliverables to a durable path at landing; land a
  failing deliverable with its failures recorded (L-0091).
- After any corpus change, refresh digest-bound carriers in one fixed order (suite
  report, hand record, parity record, close params, then the gate suite) (L-0113).
- Teach every new receipt row kind to _receipt_fold.py with a selftest case before a
  reader meets it; run a registry's --check on a scratch copy first (L-0114).
- Shape an evidence file from the reader's code (the absent() test), not from the
  ruling's prose (L-0115).
- At every close, reconcile the OW-12 figures for the closing book against the
  metrics tool and a count by distinct execution id before quoting either (L-0119).

### Tools
- Port tools by AST-derived member discovery, LF-only digest writes and a mutation
  run per fix; give every check on another tool's output a positive fixture
  (L-0088, L-0092, L-0093, L-0094).
- Later books run campaign/_make_close_params.py and port nothing (L-0100).
- When a gate gains a params-carried input, extend the gate suite's base-mirror
  fixture in the same change (L-0120).

## Open items routed, not adopted here
- land_merged_lanes.py: a pinned supersede/amend mode, and a mirror marker so a run
  landed in two receipts files counts once (L-0117, L-0119).
- gen_close_evidence.py: attempt suffixes as data rather than literals (L-0117).
