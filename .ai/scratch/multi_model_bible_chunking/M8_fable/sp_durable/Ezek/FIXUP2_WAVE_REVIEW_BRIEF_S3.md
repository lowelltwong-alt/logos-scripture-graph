# S3 — FRESH DISTINCT-CHECKER REVIEW of the Ezekiel FIXUP-2 wave, its sweeps, tool plumbing and v5 coverage (OW-6b hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible for an open-licensed scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World English Bible translation, verify quotations byte-for-byte, and review proposed literary-unit boundaries. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-11; read before your governance check)

Your global policy has you read `C:\Users\lowel\.agent-governance\ACTIVE_WORKTREES.yaml`. Its entry for this lane names Fable 5 as the only writer, and its progress fields are stale. On 2026-09-10 the owner, Lowell, explicitly approved the exact exception in chat. Asked "Do you explicitly authorize this Opus 5 session, and the Fable, Sonnet and Opus agents it launches, to write M8_fable work despite the registry's Fable-5-only rule?", the owner answered "Yes: Ezekiel, then Daniel". Asked "How should the exception be recorded?", the owner answered "M8 log only". The record is the OW-11 addendum (authorization_ref `lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan`) of `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\ERROR_PATTERN_LEDGER.v1.md`; open it by that exact path to verify. You do not mutate the lane. You read files under the worktree and write ONE deliverable outside it; the orchestrator lands it. You never run git, never write a receipt and never touch the registry.

## E-19 — the two binding lines (as amended by ezek_controlling_rulings_a1#e8 T6-E19 and #e9 S2-E19)

**AFFIRMATIVE NO-CHECK LINE:** `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\6116e665-408b-4874-9bf0-881eb9c464f5\scratchpad\ezek_rulings_out\s3_ezek_fixup2_wave_review_s3_a1\` already exists and is yours. Write your deliverable directly to `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\6116e665-408b-4874-9bf0-881eb9c464f5\scratchpad\ezek_rulings_out\s3_ezek_fixup2_wave_review_s3_a1\ezek_fixup2_wave_review_S3.json`. **Never run any existence check, listing, glob or recursive search against it or any other directory, your own scratch included.**

**EXACT-PATH LAW:**
- Every path you may read is named in this brief, plus the governance files your own policy requires and the ledger named above. Open each by its exact path.
- A self-check is a stat or a digest, by exact path, of a FILE you are about to read or have written; a directory is never tested for - create it with New-Item -Force or os.makedirs(exist_ok=True); there is no listing, glob or recursive search anywhere, your own scratch included.
- You may take a path the table does not name ONLY from a pinned input's own field (artifact_path, evidence_path, staged_path, preimage, diff and the like), and never a FORBIDDEN path below. Open it by that exact path, hash it, and disclose it in your e19_selfreport and in artifacts_reviewed. A path from any other source is a stop-and-report, not a read.
- Run every tool over PRIVATE COPIES in a uniquely named `ezek_s3_<random>` subdirectory of your own session scratchpad. Create and read each file there by its exact name.
- State affirmatively in your final message that you ran no listing and no glob.

**GOVERNANCE:** the orchestrator ran `validate_workspace_policy.ps1 -ScopeWorktreeId logos-t423-m8-fable` before this launch: status pass, relationship_scoped, no blocking failure, registry sha256 70ff849fcd80af95..., lane HEAD 8dce6681685c (output saved 2026-09-11 17:06 UTC). You do not run it, and you run no git. You write nothing under the worktree `C:\wt\logos-t423-m8-fable`.

**FORBIDDEN:**
- any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`, `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or `comparison\`;
- every other book's lane, and M7 or comparison data of any kind;
- transcripts, the capture index, CYCLE_STATE and the other campaign logs;
- the FIXUP-1 and FIXUP-2 authors' deliverables, records, receipts and evidence notes, including `SP\Ezek\fixup2\ezek_author_fixup2_*` and `SP\Ezek\fixup2\ezek_author_fixup_attempt_receipts.jsonl`, `SP\Ezek\fixup1\ezek_author_fixup_*` and `SP\Ezek\evidence_notes\`. The apply manifest names some of them in its own fields; this list prevails. You review what landed in the rows, not what the authors say about it.

Run every tool as `PYTHONIOENCODING=utf-8 python <tool> ...`.

## Your role

You are a FRESH DISTINCT CHECKER. Attempt id `ezek_fixup2_wave_review_s3_a1`, execution id `ezek_fixup2_wave_review_s3_a1#e1` (first execution). You authored none of the rows, the orders, the fix-ups, the sweeps, the tools or any earlier review: you are not S1, not S2, not T1-T6, and not an author.

- #e9 ruled S2's findings. Three deterministic sweeps ran over rows_v4_fixup1 first: CWO-EZ-19 (oss keys that encode a parashah mark), CWO-EZ-20 (one-word curly spans) and CWO-EZ-21's deterministic half (ledger-id tags), giving rows_v4_cwo21.
- FIXUP-2 then ran as nine claude-sonnet-5 executions, one per part, on `SP\Ezek\FIXUP2_BRIEF.md` and per-part orders files. The orders carried S2's findings verbatim, the CWO-EZ-21 author half and the S2-14 mark items. The wave allowed replace only.
- The orchestrator landed the parts and applied them to rows_v4_cwo21: replaced 67, of which 0 no-op, whole-book tiling 1273/1273. The suite reads HARD GREEN, and coverage reads COVERED on CWO-EZ-01, 02, 04..09 and 14..21. The mark_symmetry_gap residual is exactly the two p05 flags #e9 left to the primaries.
- Under #e9 S2-ROUTING (5) the orchestrator changed the landing and apply tools' labels and paths. Under S2-15 it generalized the CWO-EZ-14..18 coverage tool's wave labels, so FIXUP-2's reports name FIXUP-2 and CWO-EZ-14's carries the FIELD SCOPE sentence. You read all three diffs.

**#e9 S2-ROUTING (7), verbatim:** (7) S3: a fresh distinct checker that is not S1, S2, T1-T6 or an author; it reads S2-01's three rows back first, then every replaced row's diff against rows_v4_cwo21, then every string field of every row for the governance kin S2 named (strategy, brief, ruling, campaign, wave, session, posture, officially, E-NN, tool and staged-file names) and for the T5 evasions, then a sample of ten mark disclosures against pmarks; its readiness verdict is in the #e8 T6-02 ACCEPT form.

Your verdict gates the FIXUP-1 and FIXUP-2 rows cure claims and the owner check-in before the primaries. Give every finding exactly one route: author_fixup:pNN, orchestrator or controlling_agent. Split a finding that spans routes.

## Inputs (read by exact path; the digests bind what you reviewed)

| path | sha256 at launch |
|---|---|
| `SP\Ezek\repair\rows_v5_fixup2.jsonl` | `41b19ad9874dbb56d53b5317572fff6f90879b9b297021e7afc3300dead3c8f2` |
| `SP\Ezek\repair\rows_v5_fixup2.manifest.json` | `c0b43691a61f5cc4dd7d5926c567574af2b657b299bd859d5f2fdd042fc45ebc` |
| `SP\Ezek\repair\rows_v4_cwo21.jsonl` | `3e7e43267cbfe8bf72458bacdeba112a8930499a84bfe8d6f3721048008b6f51` |
| `SP\Ezek\repair\rows_v4_cwo21.manifest.json` | `1fe5cd03cbdafb72a5ce0f6a89db5be21459bdd50a175f8230fb6cebbe5e7901` |
| `SP\Ezek\repair\rows_v4_cwo20.jsonl` | `89ebcddc568797fc7fb363180a3ebc4dcb9eea03c540c478c40a2d20e37bfecd` |
| `SP\Ezek\repair\rows_v4_cwo20.manifest.json` | `16ed75aa698db8d1a5d399f2ccb71c51e85d4ec9639cc608cca10ccb66bb36ba` |
| `SP\Ezek\repair\rows_v4_cwo19.jsonl` | `208c45038cbe600b5cde92a83d667a7f3ebaec696f2dfb78b3a1f4dbdeca6686` |
| `SP\Ezek\repair\rows_v4_cwo19.manifest.json` | `5d2d56a5b1539bcf81a984cd2402b505c98a4182e2cb1cb3d6adc36da0cd49da` |
| `SP\Ezek\repair\rows_v4_fixup1.jsonl` | `63ac467713fc1542dbdb394787770becce4f77d3a50b92944b9285f1aee992ac` |
| `SP\Ezek\repair\rows_v4_fixup1.manifest.json` | `4a49efca37b0705a34522008a9a2f25e892fccfc069d2d4997fc13f34c195d09` |
| `SP\Ezek\repair\rows_v4_fixup1.manifest.addendum.v1.json` | `902fe1b7f8495f60ee505cdb6a7b95bf083952587443c51b4ed6cc5870028b7f` |
| `SP\Ezek\repair\rows_v3_cwo18.jsonl` | `568f004b6a4512f6de91e6c6aeaa10d80fa3956bbafad9454e79544dd8ed15d4` |
| `SP\Ezek\fixup1\fixup1_resplice_index.v1.json` | `99740d00bfb92d69f704056e9cefd74c86cc294cae36d7f9f2776171cfa3b755` |
| `SP\Ezek\fixup1\fixup1_resplice_index.addendum.v1.json` | `cb8e3ec91ff4d8977515abf661f30f56d0f083a6a375ef71b054ea77fef17293` |
| `SP\Ezek\repair\suite_v4cwo21_6c843b14\rows.jsonl.validator_report.json` | `daa27726c3982cd2f6735b7f78357491a34fcb5555e70c8e459012f81f0c2d67` |
| `SP\Ezek\repair\suite_v5_6c843b14\rows.jsonl.validator_report.json` | `dd1c0a9d310d580e5d080324817a2a8da657d6a078deec40b684ba31efc51828` |
| `SP\Ezek\repair\cwo_coverage_v4\CWO-EZ-19.json` | `1155acba4a5252202d50471205d1e00bca980d8af2d9570ff12482124fc81fd0` |
| `SP\Ezek\repair\cwo_coverage_v4\CWO-EZ-20.json` | `4dc9e1909e2719f5ad01f39a3603a29cc80f4626066323f7182c574a85b03b0b` |
| `SP\Ezek\repair\cwo_coverage_v4\CWO-EZ-21.json` | `39765744870aea97e177d113fec14a63a86a27da591c635028d0a0e5343a5b33` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-01.json` | `af5b16e590a756ed387764c321aa0486e97be0137ba3bf24a4754294872bb556` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-02.json` | `a40390e1477dbd62c3c47845375aa36f2c3e96728882d5213b16163593ce6995` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-04.json` | `d14330b98b7a3e291acc6a67c751ac6383cf2380977242b23a5de0ca1ce61782` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-05.json` | `fd3870ebdd786d559cabe78b7a050dd0ac5c0c7377ce4441943a1d826b08045c` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-06.json` | `63982971d2576a47f5ae3e933ac834565bfeb209f3afd2a47b5d9654d3822bc8` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-07.json` | `4ebb6fe791c6b5864ddea4b4029457294806fc5211b365a79dcb25630a035933` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-08.json` | `8c5a5bcc4e1a9128e90ad4a3cfe1b3b88efc90af27e7e3c0030d34b2c19fb3e9` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-09.json` | `b4b32f0817757f096849c4234c3ac39956ab6d1eb1f5fc37684dc121cd98eab3` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-14.json` | `8d0a76d51d14e7b617ac5ccf0ab19880c30339d040e45d715852b7b37e0cf7b3` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-15.json` | `0ec4b18e7d51d504a907de7019ce0cf2024f3a10c1b0fb837de50b8f0c6944e0` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-16.json` | `a2939cc6184b7caa1681884e33cd484b7f42be5a52f60defd1164ccec8af9308` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-17.json` | `37625341cebb361be088fd55ec9a739345c0f6f1ac88938d1c7447ffbae8e78e` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-18.json` | `4c6e027d2944010e669d60e89ae2bcc4f60135972b9044252090edb106b84d54` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-19.json` | `f1f026fa299de4aa6fd6117a30c39884d953501151927c32e52afab7a04f3102` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-20.json` | `84c11972ab0d7a1e076ae9deae384039c86ed0f9851e140f1acade4b0ecf1943` |
| `SP\Ezek\repair\cwo_coverage_v5\CWO-EZ-21.json` | `4c8551b5ed11805126a5552905b5c2cce3cd926fa49f6f76c170d2f0ba9f2777` |
| `SP\Ezek\fixup2\orders_index.json` | `1d88ce24d5d0aafd42510ce603517932b601f885749fe3d4836fe0e1dcfae03b` |
| `SP\Ezek\fixup2\orders_ezek_author_fixup2_p01_a1.json` | `8d3cf257adebeb6a6fcd681d36b8d075c91eea3b6a20271fa5a7447380aad6e1` |
| `SP\Ezek\fixup2\orders_ezek_author_fixup2_p02_a1.json` | `e95e330d4dbb428470cfb114f7241bb246e2421fc74930a7bbaf9b26fd236205` |
| `SP\Ezek\fixup2\orders_ezek_author_fixup2_p03_a1.json` | `cdf4d67eb7f3049106d1e0219b30eaafe710df2fd06cbecb31d303cb3ff3b905` |
| `SP\Ezek\fixup2\orders_ezek_author_fixup2_p04_a1.json` | `47ff5b0b0b326ff47321a29c78db94a6baee4a4b12eee444c931bf57a465a202` |
| `SP\Ezek\fixup2\orders_ezek_author_fixup2_p06_a1.json` | `1eb412b949d739c6d97d1cf9c93f4218215f38dec9da37da29ecdc8a3d922760` |
| `SP\Ezek\fixup2\orders_ezek_author_fixup2_p07_a1.json` | `357748a7bbcfc6e2566b885e18299d75c960e423cfeaf543bb98b985a5d5c743` |
| `SP\Ezek\fixup2\orders_ezek_author_fixup2_p08_a1.json` | `f123ba365d3001c9b085c82a12ab3b66e9a807934672bae5b139784b044a2763` |
| `SP\Ezek\fixup2\orders_ezek_author_fixup2_p09_a1.json` | `245e875ed0dbb6dce6373bae730e47941933c59970fd179be818c9b84133ccfd` |
| `SP\Ezek\fixup2\orders_ezek_author_fixup2_p11_a1.json` | `cdda426dd24a8bee12409a00a90163dd96c6a053dd70a4d7d375bd767133296b` |
| `SP\Ezek\FIXUP2_BRIEF.md` | `aff56edd47bd3e4592aad0200966b7b74b0c12dda8510a8050ed977fa5cc003a` |
| `SP\Ezek\ezek_author_wave_spot_review_S1.json` | `b9aaae75325c76e4aa24e5bddb775ef4ceea9e35f8d041beebb0f0ba37886421` |
| `SP\Ezek\ezek_fixup_wave_review_S2.json` | `f57bfd0b84d3a42a3199ad1919349bf6c644b71d9e0db8c72f5bd9f81df600e8` |
| `SP\Ezek\_land_author_part_ezek.py` | `cd0b1678473d3d6f2b4ed3dde47ad11f7ba9150963a96307bdf85c33f0ba34e5` |
| `SP\Ezek\_apply_author_wave_ezek.py` | `14e4f5dcfb50b36214d7358677fce8fcfb68da6fd288f902ceb69bdda49344e0` |
| `SP\Ezek\_cwo_coverage_fixup1_ezek.py` | `f2ebfe985210488dab1f9cea1eb13812c12e6487266526f539f794a79a4381e2` |
| `SP\Ezek\_cwo_coverage_ezek.py` | `e302347b873ade5286eda3722732a774754a55b75605f0e7bb84874be46f3991` |
| `SP\Ezek\_cwo_coverage_s2_ezek.py` | `996d431bd5418b9235c208613ebb10cbebcbf780807015f0f151d689a98971b7` |
| `SP\Ezek\_cwo19_oss_mark_keys.py` | `e5daf671ba673a78357766d3f269513ecf6af255c5541bedb0442721a390cd59` |
| `SP\Ezek\_cwo20_one_word_curly.py` | `b9d0a29cc97ccb8bfa66502888e6ca6e90c0667454f17630c84d94343fbccfca` |
| `SP\Ezek\_cwo21_ledger_id_tags.py` | `d306bf7942cc87060146f00b9b78b2abc3cd6ed68f6d7a41c94c56d99d9cb0cc` |
| `SP\Ezek\_sweep_common.py` | `6f5915ae0ca6cd5d2fc7e6ae1dae2c4400ed5819c5c727adf3d0ebb6b8820c5c` |
| `SP\Ezek\_build_fixup2_orders_ezek.py` | `ed95542dea68fad2eacf00f31c60953c77e21b9129ab65526374e3ec2beee5ad` |
| `SP\Ezek\proposals\fixup2_plumbing\_land_author_part_ezek.diff` | `af26257907b69f72a165189e02b71330c3904890a781d975b7605864f56d798f` |
| `SP\Ezek\proposals\fixup2_plumbing\_apply_author_wave_ezek.diff` | `040601e89c839fb108cf860cd68491f923259a5fe0f1c017060ba63576d4a987` |
| `SP\Ezek\proposals\fixup2_coverage_labels\_cwo_coverage_fixup1_ezek.diff` | `10371d64873c662e7e264c78179cfdc8ed17ae5d54c0153ed8218066670ac7b2` |
| `SP\campaign\receipts\ezek_tools_install_fixup2_plumbing.json` | `71052740a17e0eb81bcad0a2016f797fc7b6c184138f414f0fc3ade14894a92a` |
| `SP\campaign\receipts\ezek_tools_install_fixup2_coverage_labels.json` | `26875b39e73495fae99276edb38e7e06f8110c09bb7d2500e60b6fbef7a332d7` |
| `SP\Ezek\ezek_controlling_agent_rulings.v1.json` | `d9c54100570edca3e84694703ad294e92c068788eae614e0fb38184168c80d1e` |
| `SP\Ezek\ezek_controlling_agent_rulings_e3.v1.json` | `6ecd9578593d4f85d4cccf0ce9a77334797de4d3330b34e5558ec6228ae56b7d` |
| `SP\Ezek\ezek_controlling_agent_rulings_e4.v1.json` | `e342344c08f63a2e17c1b2cb4e27a2ae399a92c6e8d4fcfef6ca9349811b038b` |
| `SP\Ezek\ezek_controlling_agent_rulings_e5.v1.json` | `4ced2df78bf10426902aa5dc2d3e3a6d94a3a7d71b80027e2180b3f2ed730f27` |
| `SP\Ezek\ezek_controlling_agent_rulings_e6.v1.json` | `ed5d714518b5f7a09edeb593dc0982cc1301039be66ff3924f737bfa77282113` |
| `SP\Ezek\ezek_controlling_agent_rulings_e7.v1.json` | `2f83b81c5dbaefd00c1489607114e0c766fe9b95c86dad23b3773ccc034c1e9c` |
| `SP\Ezek\ezek_controlling_agent_rulings_e8.v1.json` | `bc8be4b09e01c6d9d6eb17feba921a3f56f3a45601fd04b891ccb0bb95e2f040` |
| `SP\Ezek\ezek_controlling_agent_rulings_e9.v1.json` | `81057c53c1875b84bbf81bcffeab92741fb410f6f4c1920799016defc435ab80` |
| `SP\Ezek\book_strategy_Ezek.md` | `4c7847535a29c046c160635936275177b696836019f8e6f7a368bceda38330f3` |
| `SP\Ezek\Ezek_oshb.txt` | `337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e` |
| `SP\Ezek\Ezek_web_clean.txt` | `a7e59bcbcd19607485cfb6c6c1f8f831eb63fd2a81d164ce8e25fcb1a7a2088a` |
| `SP\Ezek\pmarks_Ezek.json` | `25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315` |
| `SP\Ezek\ezek_device_inventory.json` | `0112add3b18927e9d23f09ecb850e3aa1ef9b1220c073063d49a377cf8929142` |
| `SP\Ezek\web_mt_offset_map.json` | `b14304e57d730f7372cb861dd1c6d31bbcb7704060b2a3ec963e2eaab32a7887` |
| `SP\Ezek\verse_inventory.json` | `cf48cac0132d0d06a1b5f7c3cb1e7fb437aebfcaa33a6272a2c8894129067a99` |
| `SP\Ezek\web_mt_verse_check.json` | `c122c2ee1bac34317bfac8cd31442a659b071ae854c5079fd7b685e7935e4ed7` |
| `SP\Ezek\ezek_kjv_variance_crosscheck.json` | `cb461dd4f70fbf345893dfe2c614d6dd19bf51f82f13b0f0597b865e92e80b2b` |
| `SP\Ezek\ezek_denominator_reconciliation.v1.json` | `e8f2860e1585b4b0de9f155dd6ba113efdf3b941f651a26002e9e218adf9b1bc` |
| `SP\Ezek\ezek_p0_retained_lows.v1.json` | `519dda47167a3a32aa0f079284387ca0eaccbc0ccc6dfdfc6cc417f69711d12c` |
| `SP\Ezek\writer\draft_rows_combined.jsonl` | `7b1a16ba5f07aa3443df2be423d6b1618319163720c8c3673409ff06198c6c0e` |
| `SP\Ezek\tools\TOOLKIT.md` | `b247cea5b0af11a7708b5b0a53383d4b5abd9940b016e045bd1f317d97c1c0b6` |
| `SP\Ezek\tools\ezek_lib.py` | `ab2431fecebee9c8f1e673aa70a8aac83d69f647b2fa76102efb5aa81904ef69` |
| `SP\Ezek\tools\collate.py` | `7ec9050cde6c03d0ad94b8c8abb68e1a8b7b33f7d1dc129bb5a0774f85cab249` |
| `SP\Ezek\tools\citation_sweep.py` | `6c843b14a604ec0cdb4ee52043cdd5ae30d6735b0a7d66d72ff28d9f00a39054` |
| `SP\Ezek\tools\check_marks.py` | `a63107199dfee8fe833494b7acad3a1a922fbd4f2f435eacf92d55418fbb2ce0` |
| `SP\Ezek\tools\check_universals.py` | `198e0c4cd20ca495b4e33a3df639b9e1e61320286a88db870ff5797a640dc341` |
| `SP\Ezek\tools\check_register.py` | `130948439528d5d6988c4ca8ab0da8bf853749541edbae89c5d44162deeffa72` |
| `SP\Ezek\tools\check_web_quotes.py` | `74fb717927c77faf3cde0d9d8e82b2077c5ba774cb1d275733129c9c5ed793e4` |
| `SP\Ezek\tools\check_refs_mirror.py` | `8abcfa2bf58e04093fc7a1881968e3d0ca2949cbebf6d4bfe9bbc63320d51d88` |
| `SP\Ezek\tools\normalize_hebrew_in_json.py` | `c23e837638edc891712efefe2e5ab3aae21bf87c2c602fb769bb23ecda1d73e9` |
| `SP\Ezek\tools\cap_sweep.py` | `07ff84e3c6ec8b05f46afe6e823c07771f7e031dee753376df027af6fe95223b` |
| `SP\Ezek\tools\ngram7.py` | `fe25efc22a0b01b099a8066b97a377ae125df349439d348074cb4fc5b04d271c` |
| `SP\Ezek\tools\check_tiling.py` | `6a92f6f4be73dc6ea804d7e1c4f639939e141c6f337a772db5889b21895da854` |
| `SP\Ezek\tools\run_validator_suite.py` | `4c0caa08a2999089bcec23aee6e1a47963e4395fc86d75c1f8139c35775a78cb` |
| `SP\Ezek\tools\check_language_zones.py` | `6807b3b7b19000cb08a508ffb2b142959a8f275ceba12da0fd2bcd357efbc828` |
| `SP\Ezek\tools\verse_map_web.json` | `bb588eacecb2559d29fc7199331cc161d0ffe2200f1c2ff8b5d34419d6ca5d98` |
| `SP\Ezek\tools\verse_map_oshb.json` | `408b7ee74564aef902c5fc539d6577f7708fa9aa839c993ce6281d86dc3a7901` |
| `SP\Ezek\proposals\fixup2_coverage_labels\_cwo_coverage_fixup1_ezek.py` | `f2ebfe985210488dab1f9cea1eb13812c12e6487266526f539f794a79a4381e2` |
| `SP\Ezek\proposals\fixup2_plumbing\_apply_author_wave_ezek.py` | `14e4f5dcfb50b36214d7358677fce8fcfb68da6fd288f902ceb69bdda49344e0` |
| `SP\Ezek\proposals\fixup2_plumbing\_land_author_part_ezek.py` | `cd0b1678473d3d6f2b4ed3dde47ad11f7ba9150963a96307bdf85c33f0ba34e5` |
| `SP\campaign\tool_preimages\_apply_author_wave_ezek.pre_fixup2_plumbing.390c7807.py` | `390c78076d857e74ef7e7fe79df097abfa9252c81833272aaa2f44b47c904812` |
| `SP\campaign\tool_preimages\_cwo_coverage_fixup1_ezek.pre_fixup2_labels.9d7f550e.py` | `9d7f550e93612c40d5d424fe44d78f3d8505ed186e27e53048ed17af14f8aae2` |
| `SP\campaign\tool_preimages\_land_author_part_ezek.pre_fixup2_plumbing.da3c871e.py` | `da3c871e3682fb0a163bc760d48d63682452c20b0bcc05d9da3bc6c55233411b` |
| `SP\Ezek\fixup2\fixup2_resplice_index.v1.json` | `7cd7e3ca1843878727283e5303b15ac6d8436ed7ad73ae1af5c7342769a1a892` |
| `SP\Ezek\fixup2\fixup2_questions.v1.json` | `cc4356be7a35401bfdbb46285f9cafef17b35ee81c9ff7bba0af4038c84a74b5` |

Paths named in these inputs' own fields may be opened under the exact-path law above.

## Questions — answer every one, from the bytes and from your own runs

1. **S2-01 FIRST.** S2-01 (major), verbatim: claim "S1-05 is not cured on three of the strategy-citation rows S1 named: section-8 strategy citations remain in forms the possessive-only arm cannot see."; evidence "P08-001 boundary_rationale 'it also carries the parent seam named in the binding strategy (P6/P7)'; P08-002 strongest_rejected_alternative 'the identical 'you say ... but I say' disputation pattern the strategy holds as one row'; P08-004 device_notes 'a book-wide device the strategy sweeps at 15 verses across chs. 6 and 33-39'. All three were in v3 and survive; the orders carried S1-05 plus CWO-EZ-14 items (matches only on \"strategy's\"), and the authors removed only those matches."; suggested_fix "Reword each as a byte or verse argument (e.g. the addressee return at 33:2 and the P6/P7 seam at 32:32/33:1; the continuous 'you say ... but I say' disputation across 33:10-20; 'mountains of Israel' recurs (sweep: 15 verses)) with no strategy citation. Spans unchanged.". Read P08-001, P08-002 and P08-004 back against rows_v5's bytes. For each row: is every strategy citation gone, and does the argument now stand on bytes or verses?
2. **EVERY REPLACED ROW.** Diff each of the 67 replaced rows against rows_v4_cwo21. For each row, check that:
   - it does what its part's orders file says, and nothing the orders do not name changed;
   - no new unsupported claim entered, and every universal carries a digit-bearing sweep citation (E-16);
   - the register follows strategy section 8, and K/Q exclusivity follows #e6 T5-MARKS (1);
   - refs touching WEB 20:45-49, WEB ch 21 or MT ch 21 are dual, and no span, id, unit_type, confidence or parent changed;
   - curly double quotes hold WEB text with its web: ref, and every gloss matches its splice's extent.
   Give one entry per row.
3. **GOVERNANCE-KIN SEARCH.** Search every string field of all 145 rows for the kin S2 named: strategy, brief, ruling, campaign, wave, session, posture, officially, E-NN, tool filenames and staged-file names or stems (Ezek_oshb, Ezek_web, pmarks, verse_map, TOOLKIT, ezek_lib, offset_map, device_inventory). Search too for T5's five evasions and their kin, and for positional row references. Use your own patterns and reading. Report at least eight shapes, each with integer hits and its rows.
4. **MARK DISCLOSURES.** Read at least ten S2-14 disclosures, from at least five parts, against pmarks. Check the verse, the mark type, the role, 'single witness', no oss key, no intra-verse position, and dual refs in the numbering zone. Answer FQ2-01 on placement too.
5. **EVERY RE-SPLICE READ BACK, PER ELEMENT.**
   - Derive for yourself every Hebrew run (`ezek_lib.HEB_RUN`) in a replaced row of rows_v5 that is absent from the same element of the same field in rows_v4_cwo21. Compare list element i with element i before, skipping an unchanged element; compare a string field with the field before.
   - Compare your set with `fixup2\fixup2_resplice_index.v1.json`, including its moved_elements. The index is the orchestrator's aid, not proof, and a mismatch is a finding.
   - Check each run: it collates at its cited ref (byte tier if pointed, skeleton if unpointed); a Qere matches its note's raw bytes and carries a ketiv/qere label; it stands on whole words; and the gloss beside it matches its extent. Give one runs entry per derived run.
6. **TOOL DIFFS.** Read `proposals\fixup2_plumbing\_land_author_part_ezek.diff`, `proposals\fixup2_plumbing\_apply_author_wave_ezek.diff` and `proposals\fixup2_coverage_labels\_cwo_coverage_fixup1_ezek.diff` against the installed files and the install receipts. For each diff, check that:
   - it is confined to labels, paths and the stated additions;
   - the FIXUP-1 labels and path stay byte-identical by default;
   - `--selftest` reads GREEN on a private copy;
   - no suite member moved.
7. **APPLY AND COVERAGE.**
   - Apply: only the replaced rows changed, the no-op statement is true, and whole-book tiling holds.
   - Coverage: recompute over rows_v5 the residuals of CWO-EZ-14 (over the fields its FIELD SCOPE sentence names, and with the sentence present; question 3 covers every other string field), CWO-EZ-18, CWO-EZ-19, CWO-EZ-20 and CWO-EZ-21. Compare them with the reports.
   - Confirm the v5 mark_symmetry_gap residual is exactly P05-004 (Ezek.22.31) and P05-008 (Ezek.24.14).
8. **SIDECARS.** Check `repair\rows_v4_fixup1.manifest.addendum.v1.json`'s no-op line digests against rows_v3_cwo18 and rows_v4_fixup1. Check `fixup1\fixup1_resplice_index.addendum.v1.json`'s moved element against both rows files.
9. **SWEEP MANIFESTS.** For CWO-EZ-19, CWO-EZ-20 and CWO-EZ-21, check that each change is lossless, bound to its ruled predicate or ruled pair, and touches nothing else. Verify every change: the three manifests hold 26.
10. **QUESTIONS** (`fixup2\fixup2_questions.v1.json`, 11 questions). For each, decide tool_false_positive, row_defect or neither, with evidence.
11. **FLAGS.** Run the suite over private copies of rows_v4_cwo21 and rows_v5. Where a FLAGS member rose on a replaced row, is the new text supported, or is it an unsupported claim that routes to a fix-up?

## Verdict wording (#e8 ruling T6-02)

A cure_claim_readiness verdict string with fit=true must contain an ACCEPT form: `fit_to_accept`, `fit_with_changes`, `confirmed`, `accept`, `accepted` or `acceptable`. It must contain NO REFUSE token: `red`, `reject...`, `blocker...`, `refut...`, `unfit`, `not fit` or `not_fit`. The verifier refuses those tokens even in negated or benign prose, so write 'no open finding', never 'no blocker'.

For repair/rows_v5_fixup2.jsonl:
- per_s1_id gives at least S1-05 and S1-15 a status: cured, not_cured or not_applicable;
- per_s2_id gives every S2 id from S2-01 to S2-17 one status: cured means the rows or the records now show the cure; not_applicable means the finding was recorded or ruled without a row change.

## What you may run, and what you must not

- MAY run, over PRIVATE COPIES: `ezek_lib.py`, `collate.py`, `citation_sweep.py`, `check_marks.py`, `check_universals.py`, `check_register.py`, `check_web_quotes.py`, `check_refs_mirror.py`, `normalize_hebrew_in_json.py` (never `--write`), `cap_sweep.py`, `ngram7.py`, `check_tiling.py`, `run_validator_suite.py`, and the `--selftest` of `_land_author_part_ezek.py`, `_apply_author_wave_ezek.py` and `_cwo_coverage_fixup1_ezek.py`. You may also run small scripts of your own in your private scratch.
- MUST NOT run: any other `_apply_*`, `_build_*`, `_cwo*`, `_land_*` or `_adapt_*` invocation, `_guarded_json_patch.py`, `_inflight_pin_guard.py`, `_brief_pin_check.py` or an install script; or anything with `--write`. Never edit any file under the worktree.

## Deliverable — `ezek_fixup2_wave_review_S3.json`

```
{"attempt_id":"ezek_fixup2_wave_review_s3_a1","execution_id":"ezek_fixup2_wave_review_s3_a1#e1",
 "verdict":"fit_to_accept|fit_with_changes|not_fit",
 "rows_file_reviewed":{"path":"SP\\Ezek\\repair\\rows_v5_fixup2.jsonl","sha256":"<digest you read>"},
 "artifacts_reviewed":[{"path":"SP\\...","artifact_sha256_at_review":"<digest>"}],
 "s2_01_readback":{"rows":[{"row":"P08-001","verdict":"cured|not_cured","findings":["..."]}]},
 "replaced_rows":[{"row":"...","part":"pNN","verdict":"accept|defect","findings":["..."]}],
 "governance_search":{"verdict":"accept|defect","shapes":[{"shape":"...","pattern":"...","hits":0,"rows":["..."]}]},
 "mark_sample":{"rows":[{"row":"...","pmarks_key":"...","role":"...","placement":"prose|refs|both","verdict":"accept|defect","findings":["..."]}]},
 "resplice_readback":{"derived_count":0,"index_count":0,"index_matches_derivation":true,
   "runs":[{"row":"...","field":"...","run":"...","ref":"...","verdict":"accept|defect","findings":["..."]}]},
 "tool_diffs":{"_land_author_part_ezek.py":{"verdict":"accept|defect","diff_confined":true,"findings":["..."]},
               "_apply_author_wave_ezek.py":{"verdict":"accept|defect","diff_confined":true,"findings":["..."]},
               "_cwo_coverage_fixup1_ezek.py":{"verdict":"accept|defect","diff_confined":true,"findings":["..."]}},
 "apply":{"verdict":"accept|defect","findings":["..."]},
 "coverage":{"verdict":"accept|defect","recomputed":{"CWO-EZ-14":0},"findings":["..."]},
 "sidecars":{"verdict":"accept|defect","findings":["..."]},
 "sweep_manifests":[{"manifest":"CWO-EZ-19","changes_checked":0,"verdict":"accept|defect","findings":["..."]}],
 "question_dispositions":[{"id":"FQ2-01","disposition":"tool_false_positive|row_defect|neither","evidence":"..."}],
 "flags":{"verdict":"accept|defect","findings":["..."]},
 "cure_claim_readiness":[{"artifact":"repair/rows_v5_fixup2.jsonl","sha256":"<64 hex>","fit":true,"verdict":"<an ACCEPT form, no REFUSE token>","why":"...",
   "per_s1_id":[{"id":"S1-05","status":"cured|not_cured|not_applicable","evidence":"..."}],
   "per_s2_id":[{"id":"S2-01","status":"cured|not_cured|not_applicable","evidence":"..."}]}],
 "new_findings":[{"id":"S3-01","severity":"blocker|major|minor|note","row_or_artifact":"...","claim":"...","evidence":"...",
                  "suggested_fix":"...","route":"author_fixup:pNN|orchestrator|controlling_agent"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}]}
```

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"ezek_fixup2_wave_review_s3_a1","execution_id":"ezek_fixup2_wave_review_s3_a1#e1",
 "sources":["<exact paths you read>"],
 "outcome":{"changed":[{"what":"<your deliverable>","why":"..."}]},
 "verification":[{"claim":"...","how":"<tool + argument>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, my own scratch included; read only the exact paths named, plus <each path taken from a pinned input's own field, with its digest>",
 "verdict":"...","new_finding_count":0,
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
