# PRIMARY REVIEWER BRIEF — literary-form (LF) lens, Ezekiel, dual-blind round 1 (OW-6b hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible for an open-licensed scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World English Bible translation, verify quotations byte-for-byte, and review proposed literary-unit boundaries. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-11; read before your governance check)

Your global policy has you read `C:\Users\lowel\.agent-governance\ACTIVE_WORKTREES.yaml`. Its entry for this lane names Fable 5 as the only writer, and its progress fields are stale. On 2026-09-10 the owner, Lowell, explicitly approved the exact exception in chat. Asked "Do you explicitly authorize this Opus 5 session, and the Fable, Sonnet and Opus agents it launches, to write M8_fable work despite the registry's Fable-5-only rule?", the owner answered "Yes: Ezekiel, then Daniel". Asked "How should the exception be recorded?", the owner answered "M8 log only". The record is the OW-11 addendum (authorization_ref `lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan`) of `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\ERROR_PATTERN_LEDGER.v1.md`; open it by that exact path to verify. You do not mutate the lane. You read files under the worktree and write ONE deliverable outside it; the orchestrator lands it. You never run git, never write a receipt and never touch the registry.

## E-19 — the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your launch message names your output directory and it ALREADY EXISTS and is yours. Write your deliverable directly to the exact path it names. **Never run any existence check, listing, glob or recursive search against it or any other directory, your own scratch included.**

**EXACT-PATH LAW:**
- Every path you may read is named in this brief or your launch message, plus the governance files your own policy requires and the ledger named above. Open each by its exact path.
- A self-check is a stat or a digest, by exact path, of a FILE you are about to read or have written; a directory is never tested for — create it with New-Item -Force or os.makedirs(exist_ok=True); there is no listing, glob or recursive search anywhere, your own scratch included. **A tool call that carries a `glob` parameter, or whose `path` names a DIRECTORY rather than a file, is a glob in form even when it matches one file.**
- Private scratch goes in a uniquely named subdirectory of YOUR OWN session scratchpad. Never write into SP.
- State affirmatively in your final message that you ran no listing and no glob.

**GOVERNANCE:** the orchestrator ran `validate_workspace_policy.ps1 -ScopeWorktreeId logos-t423-m8-fable` before this launch: status pass, relationship_scoped, registry sha256 73b3113e25fda6fa..., lane HEAD 8dce6681685c (run 2026-09-15 14:09 UTC). You do not run it, because it runs git. You write NOTHING under `C:\wt\logos-t423-m8-fable`.

## BLINDNESS (#e11 PRIMARIES-SHAPE (12)) — this is the point of the whole round

You see: the rows file at its digest, the witness files, pmarks, the device inventory, the offset map, the verse inventory, the strategy, TOOLKIT.md, the disclosed-triage artifact and the suite report. **You never see:** the other lane's output, any other reviewer's output, the fix-up orders, the cure claims, the S-reviews, the controlling agent's rulings, or any transcript. Your review must be independent, because a second lane is reviewing the same rows and the value of the pair is that neither saw the other.

**FORBIDDEN:** every other model lane (`M1_cursor`, `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol`, `comparison\`); every other book's lane; `SP\Ezek\reviews\` (other reviews live there — even a filename listing breaches blindness); `SP\Ezek\fixup1\`, `fixup2\`, `fixup3\`, `repair\` beyond the rows file named in your table; the rulings files; CYCLE_STATE and the campaign logs.

## Inputs (read by exact path; the digests bind what you reviewed)

| path | sha256 at launch |
|---|---|
| `SP\Ezek\repair\rows_v7_cwo24.jsonl` | `25cdba568d98ec60aa719606be7b273e6a7c7256c55b79a3c579ada3c21d0ecc` |
| `SP\Ezek\review_clusters.json` | `e6267c8342a477892af8fcadd5cca0cbbac4390ba1dc003f800a34045410daf7` |
| `SP\Ezek\ezek_primaries_disclosed_triage.v2.json` | `5a49733a45aaaee2a2b40d43c236ef2a9c5522320e10bd59190397be16e6c020` |
| `SP\Ezek\repair\suite_v7_6c843b14\rows.jsonl.validator_report.json` | `d392dd29c89ae9b674ac6bdd67a75e4f24cbc08cbea97b64b5842dcce034a01a` |
| `SP\Ezek\book_strategy_Ezek.md` | `4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\ezek_device_inventory.json` | `0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\Ezek_web_clean.txt` | `a7e59bcbcd19607485cfb6c6c1f8f831eb63fd2a81d164ce8e25fcb1a7a2088a` |
| `SP\Ezek\verse_inventory.json` | `cf48cac0132d0d06a1b5f7c3cb1e7fb437aebfcaa33a6272a2c8894129067a99` |
| `SP\Ezek\tools\TOOLKIT.md` | `b247cea5b0af11a7708b5b0a53383d4b5abd9940b016e045bd1f317d97c1c0b6` |
| `SP\Ezek\ezek_p0_retained_lows.v1.json` | `519dda47167a3a32aa0f079284387ca0eaccbc0ccc6dfdfc6cc417f69711d12c` |

## The corpus and your cluster

The rows file is `repair/rows_v7_cwo24.jsonl` at `25cdba568d98ec60aa719606be7b273e6a7c7256c55b79a3c579ada3c21d0ecc` — 145 rows tiling Ezekiel's 1,273 verses exactly. Your launch message names your cluster id and its row ids. **Review every row in your cluster. There is no sampling** (#e4 (11) / ruling Q8 compensation 1: full dual-blind coverage of every row).

## Triage you are given, and must answer

`ezek_primaries_disclosed_triage.v2.json` carries two entries. If either falls in your cluster, you must decide it and say so explicitly:

- **TRIAGE-EZ-01 — P04-008** (`Ezek.21.8-Ezek.21.17`): whether the seam at MT 21:18/21:19 (= WEB 21:13/21:14) should be a cut, and **whether the row's confidence `high` survives**. The artifact carries the pmarks lookup, the dual bytes of MT 21:17-19 and 21:22, and the 3:27/4:1 comparison. Decide from BOTH sides of the seam (OW-3), not from the onset alone.
- **TRIAGE-EZ-02**: the two p05 mark flags, P05-004 (`Ezek.22.31`) and P05-008 (`Ezek.24.14`) — whether each mark is disclosed as the corpus requires.

**FLAGS members over your rows** are digest-bound triage input, not defects: the suite at `d392dd29c89ae9b674ac6bdd67a75e4f24cbc08cbea97b64b5842dcce034a01a` reads web_quotes 3, mark_symmetry 12, universals 584, refs_mirror 115 over the whole corpus. `review_clusters.json` lists, per cluster, the flags that fall on its own rows. A flag is a question to answer, never a verdict to repeat.

## The checklists, verbatim from their rulings

1. **CAL-1** — for any row spanning MT 45:17-45:25, check the festival-calendar dates against the inventory before asserting a dateline.
2. **R4ii-D1 (permanent)** — for any row covering MT 41:20 or MT 46:22, hand-check prose puncta numbers beyond 60 characters.
3. **T4-03** — a denial placed behind a comma reads RED and is a rewording order, never a pass. This is true of **dateline claims**.
4. **T5-11 (a)-(f)** — the disclosed triage classes, each decided by its pmarks lookup, stated in the checked exclusivity form.
5. **T5-06 (P1)** — hand-check "expected"/"anticipated" for puncta and dateline claims in any row. **(P2)** — the comma-separated puncta denial hand-check on rows covering MT 41:20 or 46:22.
6. **T5-REGISTER (a) and (b)** — for any prose you write: no strategy section-citations, no decision ids, no reviewer names, no tool filenames, no positional or staged-file talk. State grounds by content.
7. **#e9 (6)** — the two p05 mark flags, the false_mark_absence_claim and kq_claim flags.
8. **#e10 (5)** — the MT 21:18/21:19 seam and P04-008's confidence, with the pmarks lookup, the dual bytes of MT 21:17-19 and 21:22, the 3:27/4:1 comparison and the P08-002 condition.
9. **TIER-0 NUMBERING ZONE** — Ezekiel has its own: MT 21:1-5 = WEB 20:45-49 and MT 21:6-37 = WEB 21:1-32, identity in every other chapter. **Any structured reference touching WEB 20:45-49, WEB ch 21 or MT ch 21 MUST carry an explicit dual or numeric qualifier — in prose too.**
10. **Two retained lows, as triage notes, not defects** — a hand-of-YHWH re-derivation that reads 6 is NOT a contradiction of the inventory's 7 (the inventory matches on the construct alone, deliberately; MT 8:1 reads the divine-name pair). And Hebrew in TOOLKIT.md is citation form, never a byte quote: quote bytes from `Ezek_oshb.txt`, never from the toolkit. **Both cures those two lows offered are ALREADY IN the live toolkit.** And read that record's bindings correctly: its top-level `bound_to_artifacts` is deliberately HISTORICAL — it holds the digests a round-3 distinct checker accepted, and overwriting it would erase what that review accepted. The CURRENT binding is the newest entry of `bound_to_artifacts_rebinds`. A mismatch between that top-level key and the live file is expected and is NOT a finding.

## DO NOT REUSE these grams (#e11 S4-GRAMS, read from the CURRENT ngram7 report at brief time)

The HARD ngram7 gate fails at 10 rows sharing a seven-word run. These already stand at 8 or more, so **one more row carrying any of them turns the gate RED**. Do not use these runs, or any five- or six-word run inside them, in any prose you write:

- `a samekh recorded on this same verse` — stands on 8 rows
- `by a samekh recorded on this same` — stands on 8 rows
- `intra verse position is sourceable from the` — stands on 8 rows
- `matched by a samekh recorded on this` — stands on 8 rows
- `no intra verse position is sourceable from` — stands on 8 rows
- `no k q or paseq falls in` — stands on 8 rows
- `opens with the strict word event formula` — stands on 8 rows
- `verse position is sourceable from the extract` — stands on 8 rows

**A finding names the FACT and the VERSE to install, never a sentence to paste.** That is the rule that keeps this list from growing: if every reviewer proposes wording, the wording converges and the gate fails.

## Your lens — LITERARY FORM (LF)

You are the **literary-form primary**, ordered at HIGH effort on claude-opus-5. Your question is whether each row is a coherent literary unit under Ezekiel's own conventions, and whether its boundaries fall where the text's form says they fall.

**READ IN THIS ORDER** (your reading order is deliberately different from the other lane's):
1. `book_strategy_Ezek.md` — the eight parents, the ruled granularity, the unit-type vocabulary. Read this FIRST; it is the frame everything else sits in.
2. `ezek_device_inventory.json` — the formula census. **Read the counts from that file, not from this sentence.** Measured from the inventory at the digest pinned in your table: word-event (strict) 39; word-event any-form 41; son-of-man address 93; recognition formula 28; recognition 2ms 5; messenger formula 122; utterance formula 81; hand-of-YHWH 7; set-your-face 9; I-Yahweh-have-spoken 14; dated oracles 14; calendar dates kept separate 4. A brief that prints a count is repeating a number; the inventory is the artifact, and where the two ever differ the inventory wins and the difference is a finding against the brief.
3. Your rows, in `repair/rows_v7_cwo24.jsonl`.
4. `Ezek_web_clean.txt` for the run of the text, then `Ezek_oshb.txt` only where a form question turns on the Hebrew.
5. `pmarks_Ezek.json` and the offset map only to check a mark or a reference a row asserts.

**Judge:** unit_type against the book's vocabulary; whether the opening formula actually opens a unit and the closing device actually closes one; whether a refrain or recognition formula closes the unit BEFORE the seam rather than opening the one after; whether the row's span holds one literary movement or two; whether confidence matches the strength of the form evidence.

**A refrain closes the unit before it.** Assess every seam FROM BOTH SIDES: an onset-only diagnosis is incomplete until the adjacent unit's close is weighed.
## Deliverable

Your launch message names the exact output path. Write JSON only:

```
{"attempt_id":"<from your launch message>","execution_id":"<from your launch message>",
 "book":"Ezek","role":"primary_LF","cluster":"<cluster id from your launch message>",
 "model_ordered":"claude-opus-5 at high effort",
 "rows_file":{"path":"Ezek/repair/rows_v7_cwo24.jsonl","sha256":"<the digest you hashed>"},
 "artifacts_reviewed":[{"path":"SP\\...","artifact_sha256_at_review":"<digest>"}],
 "rows_reviewed":["<every row id in your cluster; no sampling>"],
 "items":[{"row_id":"P01-001",
    "verdict":"support | challenge",
    "severity":"high | medium | low   (present EXACTLY when verdict is challenge, and absent on a support)",
    "claim":"the fact, stated by content, with its verse",
    "decision":"keep | cut at <exact verse> | confidence stands | confidence moves to <level>",
    "both_sides":"what the evidence on EACH side of the seam says (required for every cut you propose and every triage entry)",
    "suggested_fix":{"fact":"the fact to install","verse":"the verse it rests on"},
    "evidence":["<exact ref or byte quote>"]}],
 "triage_answers":[{"id":"TRIAGE-EZ-01","in_my_cluster":true,"decision":"...","confidence_high_survives":true,
    "both_sides":"...","evidence":["..."]}],
 "summary":{"supports":0,"challenges":0,"by_severity":{"high":0,"medium":0,"low":0}},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"<state that you ran no listing and no glob>",
 "limit":"one lens on one cluster; candidate-only, non-authorizing research review"}
```

**THE FIELD NAMES ABOVE ARE THE CONTRACT AND THE LANDING VALIDATOR ENFORCES THEM EXACTLY.** In particular: `role` is the string `primary_LF`, not the bare lens; items are keyed `row_id`, not `row`; the fact field is `claim`; and `summary` uses `supports`, `challenges` and `by_severity`. `severity` takes `high`, `medium` or `low` — no other vocabulary — and is present exactly when `verdict` is `challenge`. `attempt_id`, `execution_id` and `cluster` must equal your launch message's exactly.

`summary.supports`, `summary.challenges` and `summary.by_severity` must equal the recomputed counts over `items`; a non-zero entry in `by_severity` that the items do not support is refused, and so is a zero one that they do. One item per row in your cluster, no more and no fewer, each with a non-empty `claim` and a non-empty `evidence`.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only: `attempt_id`, `execution_id`, `cluster`, `sources` (exact paths), `deliverable`, `deliverable_sha256`, `rows_reviewed`, `summary`, `changes_made_or_no_change`, `verification_evidence`, `unresolved_uncertainty`, `e19_selfreport`, `limit`.

**Do not soften a challenge to make the round look clean, and do not manufacture one to look thorough.** A row that is right is supported with its reason.
