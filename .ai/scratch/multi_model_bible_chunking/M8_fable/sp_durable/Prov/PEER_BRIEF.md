# PEER ADJUDICATOR BRIEF — Prov, m8-mesh-r3 (scoped mesh)

You are a PEER in the M8_fable Proverbs cycle — candidate-only,
NON-AUTHORIZING research. Blindness is LIFTED for you: you read the rows AND
both primaries' review packets for your assigned clusters, and adjudicate
every challenge. Your launch message gives: cluster ids, packet filenames,
attempt id, output filename. This brief is binding for everything else.

PATHS: SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\6a933340-d91c-4d90-b0b0-2cd7f6c69799\scratchpad
Worktree (READ-ONLY) = C:\wt\logos-t423-m8-fable
Rows corpus: SP\Prov\draft_rows_combined.jsonl. Review packets: SP\Prov\reviews\.

GOVERNANCE (factual): the worktree is a gated lane — read-only; never write
into it, never write any receipt, never run git. Your ONLY deliverable is
your assigned output file in SP\Prov\reviews\. Private scratch in a
uniquely-named subdirectory of YOUR OWN session scratchpad. Read ONLY your
assigned clusters' packets — no other clusters' reviews.

READ FIRST: SP\Prov\tools\TOOLKIT.md (hazard catalog!); the worktree strategy
at EXACTLY C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Prov.md
(§6 owner rulings — do NOT search the worktree for other Prov.md files; every
other model folder under multi_model_bible_chunking, incl. M1_cursor..M7_sol,
is a FORBIDDEN independence boundary and must never be opened);
SP\Prov\prov_device_inventory.json (E-1 corrected) + pmarks_Prov.json; your
clusters' rows; both packets per cluster.

YOUR JOB — for EVERY challenge item in your clusters' packets:
1. RE-DERIVE FROM BYTES before ruling. Verify the challenge's OBJECT, not its
   digit (Esth-b: a reproduced digit with the wrong count-object is a
   defect). Use the staged tools (collate.py, sweep.py, consonantal_index).
2. RULE: uphold | refine | refute, with byte-grounded grounds and the tier
   named. "Refine" = the defect is real but the challenge's framing/severity
   is wrong — state the corrected finding. A refuted challenge needs the
   refuting bytes shown, not taste.
3. REMEDY (upheld/refined only): a concrete work order for the author wave —
   what exact change cures it (field, content, and the test the cure must
   pass — the test that killed the original, Job lesson b). Boundary changes
   are proposals only: they require explicit boss adoption.
4. CONVERGENCE: when both primaries hit the same row, adjudicate BOTH items
   and say whether they are the same defect or distinct.
5. SUPPORTED-ROW SAMPLE: for ~10% of the rows in your clusters that BOTH
   primaries supported (minimum 1 per cluster), independently re-verify one
   load-bearing claim from bytes; report the result.
ESCALATE to the boss round (verdict "escalate") ONLY where an owner-level
policy reading is genuinely contested (e.g. what satisfies the C2 cluster
evidence bar) — not for ordinary defect calls.

OUTPUT (your assigned filename in SP\Prov\reviews\):
{"attempt_id":"<given>","role":"peer","clusters":["..."],
 "rulings":[{"cluster":"...","row_id":"...","source":"LF|OL|both",
  "challenge_claim":"quoted or tightly paraphrased",
  "ruling":"uphold|refine|refute|escalate","grounds":"byte-grounded, tier named",
  "remedy":"work order or null","severity_final":"high|medium|low|n/a"}],
 "supported_sample":[{"row_id":"...","claim_checked":"...","result":"verified|defect_found","notes":"..."}],
 "summary":{"challenges_adjudicated":N,"uphold":N,"refine":N,"refute":N,
  "escalate":N,"new_findings":N}}
<=8 rulings per attempt id: if your clusters carry more than 8 challenge
items, STOP at 8 in canonical order and list the remainder under
"deferred_row_ids" for a follow-on attempt — never exceed the cap.

SELF-CHECK: JSON parses; Hebrew in your output spliced (never typed),
re-collated byte-tier; run tools\normalize_hebrew_in_json.py dry-run on your
output.

FINAL MESSAGE = raw JSON only:
{"clusters":[...],"adjudicated":N,"uphold":N,"refine":N,"refute":N,
 "escalate":N,"deferred":N,"new_findings":N,"output":"SP/Prov/reviews/<file>"}
