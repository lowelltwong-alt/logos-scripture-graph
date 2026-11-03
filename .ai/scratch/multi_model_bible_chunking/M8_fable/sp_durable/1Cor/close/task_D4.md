You are a tool builder. You close nothing: you never run a close mode against the real tree, and the orchestrator
installs what you build. Daniel's close kit is hard-coded to Daniel; the owner's standing rule (TE-7) is that this port
is done ONCE, so 1 Corinthians and every later book run the same tools from a parameter file and port nothing.

**Units:** (1) read the templates; (2) the close tool; (3) the parameter maker and both parameter files; (4) the
builders and the packet generator; (5) the gate tests; (6) the regression and the dry run; (7) the result.

**1. `campaign/_close_book.py`, book-agnostic.** It takes `--book BOOK` and reads every constant now at lines 59-114 of
Daniel's tool from `<BOOK>/close/close_params.v1.json`. Keep the gates, the writes, the write order, the refusal rules,
the modes (`--dry-report DIR`, `--close`, `--acf`, `--next-book`, `--m8-root`, `--fixture-landed`, `@usage.json`) and
the OW-28 DEFERRED and OWED records exactly. **Add no shortcut. A gate that cannot be evaluated is UNMET, never
skipped. DEFERRED is never MET.** A gate family that does not apply to a book is switched off only by a named parameter
carrying its reason, and the switch prints as a gate line of its own with that reason: the language layer and the
numbering zone have no subject in 1 Corinthians. A book-specific library (Daniel's `dan_lib`) becomes a parameter
naming a module path, or a pure lookup in the parameters. The close-shape gate reads the carrier path and its generator
from the parameters: for 1 Corinthians `campaign/grader_models.v3.json` and `campaign/gen_grader_models_v3.py`, which the
orchestrator is building now and which do not exist yet, so that gate is UNMET in your dry run.

**The boss gate.** 1 Corinthians is on the hard track and a boss audit lane will run on the final rows after this lane.
Its record is `1Cor/review/1cor_boss_audit.v1.json`, in the same form as Daniel's, and its condition ids come from the
parameters. There may be one record or two, so `BOSS`, `BOSS_E2_SUPERSEDES` and the condition list are parameters and
"e2 answers exactly these" applies only when a second record is named. A NOT_TESTABLE or NOT_MET on any condition stays
UNMET, as it does in Daniel's tool. The lineage gate's `boss_audit_<tag>` names follow the parameter.

**2. `campaign/_make_close_params.py --book BOOK [--allow-pending]`.** Reads a short hand-written spec
`<BOOK>/close/close_spec.v1.json` (paths and facts) and writes `close_params.v1.json` with every pin MEASURED from disk at
the run. An absent input is refused, or with `--allow-pending` recorded as the literal `"PENDING"`, and the close tool
treats `"PENDING"` as UNMET. Write `close_spec.1Cor.v1.json` and `close_spec.Dan.v1.json`, and the parameter files
each produces when run with `--m8-root` pointing at the real tree and output into OUT.

1 Corinthians facts, each to be re-derived from the bytes and never taken from this brief: rows from
`1Cor/fixup/draft_rows_fixup4_applied.jsonl`; 16 chapters and 437 verses in WEB order (`1Cor/verse_inventory.json`); no
numbering zone; no language layer (the book is Greek); witnesses Byzantine RP primary and SBLGNT secondary (OW-31);
`decision_id` of the form `M8-1Cor-%03d`; books closed before and after 27 and 28; final corpus
`1Cor/rows_v1_final.jsonl`; the next book John, per OW-36. Close inputs at the same relative places as Daniel's:
`1Cor/scholar_record/`, `1Cor/deliverables/`, `1Cor/sidecar_src_1cor.jsonl`, `1Cor/merged_close/landing_manifest.v1.json`,
`1Cor/fable_end_review/`, `1Cor/cwo/`, `1Cor/1cor_retention_manifest.v1.jsonl`. The merged-verdict shape is granted by
OW-37 in place of OW-33; the close act is OW-37 point 3, not the owner's reservation.

**3. Builders, each book-agnostic, each with a `--check` that regenerates and compares bytes:**
- `campaign/_build_final_rows.py --book BOOK --from REL [--write]`: writes `<BOOK>/rows_v1_final.jsonl` and its manifest
  in the form of `Dan/rows_v1_final.manifest.json`, so that the lineage gates pass. No such tool exists: Daniel's were
  written by hand. Read `Dan/_close_book.py` lines 249-272 and the manifest. A value the tool cannot measure is a named
  argument, never a default.
- `campaign/_build_landed_manifest.py --book BOOK [--write]`: from the three receipt files named below, writes
  `<BOOK>/close/<book>_landed_outputs_manifest.v1.json` in the form of Daniel's v2, re-hashing each output and listing
  what does not match in `not_matching`.
- `campaign/_cwo_parity.py --book BOOK`: port of `Dan/_cwo_parity_dan.py`. The sweep tool's path is a parameter; for 1
  Corinthians it is `1Cor/review/cwo_sweep_1cor.py`.
- `campaign/gen_fable_end_packet.py --book BOOK [--check]`: port of Daniel's. It reads routed items, sidecars and the
  corpus from the parameters and records status DEFERRED (OW-28).

**4. `campaign/_test_close_book_gates.py --book BOOK`.** Port Daniel's: for each gate a private mirror with one planted
defect showing the gate refuses, and one clean mirror showing the intended inputs pass. Inputs that do not exist yet are
built in the mirror as fixtures of the right FORM, marked as fixtures. Add tests for what the port adds: a `"PENDING"`
pin refuses; a gate-family switch without a reason refuses; `--close` refuses on any unmet gate.

**5. Regression: the proof that nothing was weakened.** Run Daniel's installed tool `Dan/_close_book.py --dry-report` and
your tool `--book Dan --dry-report`, each into its own directory under OUT, and compare. Daniel is already closed, so
its target gates will not pass: that is expected and must be the same in both. Measure by script and record in
`regression`: every gate name in the old report and whether the new one has it, the verdict of each in both, and every
difference with its reason. Any gate lost, or any verdict that moved from UNMET to MET, is a defect to fix, not a note.

**6. One dry run for 1 Corinthians** with `--m8-root` the real tree and every output in OUT. Most gates are UNMET today
(no final rows, no merged lanes, no scholar record). List them in `gates_unmet_today`, each with what it waits on.

**Path rule.** The tools find the M8 tree from their own location and also accept `--m8-root`. No script scans a
directory: every input is a named path or a path read from a manifest or a parameter. No clock and no randomness in any
gate or preview; a second dry run must be byte-identical. `--close` writes whole files with LF bytes through a temporary
file and an atomic replace, under an exclusive lock, and rolls back on any failure.

**Deliverables, in OUT, at these names** (`campaign\` is a subdirectory of OUT that you create by writing into it):
`campaign\_close_book.py`, `campaign\_make_close_params.py`, `campaign\_build_final_rows.py`,
`campaign\_build_landed_manifest.py`, `campaign\_cwo_parity.py`, `campaign\gen_fable_end_packet.py`,
`campaign\_test_close_book_gates.py`, `close_spec.1Cor.v1.json`, `close_spec.Dan.v1.json`, `close_params.1Cor.v1.json`,
`close_params.Dan.v1.json`, `gate_test_result.json`, `regression\`, `dry_report\dry_report.json`, `build_notes.json`
(every gate ported, changed or switched, and every parameter with where it was measured), and the result JSON.
