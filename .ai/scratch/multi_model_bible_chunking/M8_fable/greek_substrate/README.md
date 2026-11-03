# greek_substrate — Greek NT substrate and Tier-0 tooling (OW-31, 2026-09-29)

This folder holds the staged Greek witnesses plus a small, deterministic validator toolkit. The toolkit is modelled on
`sp_durable/Dan/tools/` (dan_lib.py, citation_sweep.py, check_tiling.py, run_validator_suite.py). Those files were
read, never edited. Nothing here changes canonical Scripture, preferred readings, graph/retrieval truth, reviewed gold
or textual-critical policy. Nothing here is committed. The outcome is recorded in the ledger by the Daniel
orchestrator, not by this lane.

Provenance tiers are MEASURED, EXTRACTED, REPORTED, INFERRED, ASSUMED and UNAVAILABLE.
The authoritative per-file record is `STAGING_RECEIPT.v1.json`, regenerated from disk by `_build_receipt.py`.

## What was staged

| Set | Folder | Role | Disposition | Pin | Files / bytes (MEASURED) |
|---|---|---|---|---|---|
| A | `byzantine_rp_PRIMARY/` | PRIMARY witness: Robinson-Pierpont Byzantine Textform (RP2018 text) | newly_acquired (downloaded 2026-09-29T19:50:50Z) | byztxt/byzantine-majority-text tag v3.3.2, commit 27a45ff1b7be6c17ccbfeac414f3f55732ae8e28 | 32 / 1,753,195 |
| B | `sblgnt_SECONDARY/` | SECONDARY witness: SBLGNT v1.2, for critical-text disclosure | reuse_existing_governed_raw (extracted from `data/raw/original_language/greek/sblgnt/raw/sblgnt-c4d241a9c1c4.zip`; no download) | Faithlife/SBLGNT commit c4d241a9c1c479a55b989ba35a4976c1d0b8052c | 29 / 1,788,577 |
| B2 | `sblgnt_apparatus/` | SBLGNT apparatus, used as comparison evidence only | reuse_existing_governed_raw (same archive) | same commit | 27 / 511,907 |
| C | `swete_lxx_REFERENCE_ONLY/` | REFERENCE-ONLY Greek OT: Swete 1905 via First1KGreek (Daniel Theodotion and OG, Ezekiel, Zechariah) | downloaded 2026-09-29T19:34:31Z | OpenGreekAndLatin/First1KGreek commit 8ee111eb44ecef4120c844e10749178d95d1f30c | 5 / 1,141,232 |

**Correspondence checks (MEASURED).** `_stage_and_verify.py` checks two things:

- The governed archive's sha256, size and commit equal its `source_manifest.yaml`.
- Every file in A, B and B2 has a git blob sha1 equal to the upstream tree entry at the pinned ref (read with
  `gh api`, metadata only).

It also fails closed on any missing or unexpected file.

## Licences as verified (EXTRACTED from the staged source files, before any byte was used)

- **A (Byzantine RP): the Unlicense** (`LICENSE.txt`). README.md, under "Copyright", says "All the code and text
  contained in this folder is in the Public Domain." This matches the OW-31 assumption.
- **B / B2 (SBLGNT): CC BY 4.0** (`LICENSE`, README "License"). The required attribution is "Copyright 2010 by the
  Society of Biblical Literature and Logos Bible Software". This matches the OW-31 assumption.
  - B2 keeps its governed classification as excluded and noncanonical. It is never promoted to source-language text
    and never used to choose readings (owner terms, 2026-09-29).
- **C (Swete / First1KGreek): CC BY-SA 4.0.** This is stated in `license.md` and in every TEI header's
  `<availability>`. It **contradicts** the OW-31 public-domain assumption.
  - The printed 1905 edition is only INFERRED to be public domain, by its age. The digital transcription staged here
    is CC BY-SA.
  - The owner accepted it on 2026-09-29 as reference-only, on these terms:
    - Swete bytes stay isolated from canonical Scripture, shipped datasets, graph/retrieval truth, embeddings,
      reviewed gold and redistributable alignment outputs.
    - No substantial Swete text is reproduced.
    - Any later need to publish Swete wording or a derivative of the transcription STOPS for a separate
      licence/output review.
  - The full terms are in the receipt.
- **WEB:** read in place from `data/raw/bible/eng-web/usfm/eng-web_usfm.zip`. Its sha256 (a745365f…8e) is pinned in
  `greek_lib.py` and checked on every load. It is not copied here.

## Measured findings (2026-09-29, from the staged bytes)

These counts treat a verse as existing only if the witness prints text for it. `derived/crosswalk.v1.json` holds
flags only, never wording: 7,924 verse numbers are printed by all three witnesses unflagged, and 36 are exceptions.

**The OW-31 working claim "RP verse existence is one-to-one with WEB" is REFUTED at exactly one verse, Acts 24:7.**

- ACT.csv prints Acts 24:6 and 24:8 but not 24:7.
- A longer 24:6-8 exists only in the repository's separate `ACT24.csv`.
- WEB's `\v 7` is an empty, footnote-only marker.
- Nowhere else does RP print a verse WEB lacks, or the reverse.

**WEB prints five verse markers with no text:** Luke 17:36, Acts 8:37, Acts 15:34, Acts 24:7 and Rom 16:25.

- Counting a bare marker as a verse would falsely report Luke 17:36, Acts 8:37 and Acts 15:34 as "WEB but not RP".
- Rom 16:25's footnote says the doxology is printed at Rom 14:24-26. WEB and RP both print it at 14:24-26.

**The pericope adulterae (John 7:53-8:11) is printed inside JOH.csv itself.**

- `PA.csv` is a separate form of the passage and differs from JOH.csv in 11 of its 12 verses. Its editorial status is
  UNKNOWN.
- `load_rp()` keeps the main-file text and records each differing separate-file reading. It never chooses between
  them.
- SBLGNT v1.2 prints John 7:53-8:11 as well.

**SBLGNT existence and numbering differences:**

- SBLGNT does not print: Matt 17:21, 18:11, 23:14; Mark 7:16, 9:44, 9:46, 11:26, 15:28; Luke 23:17; John 5:4;
  Acts 19:41, 24:7, 28:29; Rom 14:24-26; 2Cor 13:14.
- SBLGNT prints verses WEB and RP do not: 3John 1:15 and Rev 12:18. These are numbering splits.

**The Hardness file's `greek_substrate_ruling` list was not accurate for these witnesses.** Part of it assumed
critical-edition absences that the staged SBLGNT v1.2 does not show. For example, it prints John 7:53-8:11, Mark
16:9-20 and Rom 16:24. The measured crosswalk supersedes that list for tooling purposes. The ruling itself is not
edited here.

## Tools (`tools/`, every one prints one JSON object with status GREEN/RED)

| Tool | Purpose | Selftest |
|---|---|---|
| `greek_lib.py` | Book table; WEB/RP/SBL loaders (WEB sha-pinned); tiers byte / nfc / accent_stripped / skeleton; word-boundary `bounded_find`; ordered, ellipsis-aware `collate_greek`; range-guarded `expand_ref` (refuses, never clamps); `crosswalk`; Swete shingle hashes (hashes only); `verify_staged` | `python greek_lib.py` |
| `build_crosswalk.py` | WEB↔RP↔SBL verse-existence flags + the one-to-one measurement → `derived/crosswalk.v1.json` | `--selftest` |
| `collate.py` | Tier of a quote at a ref in rp or sbl | `--selftest` |
| `normalize_greek_in_json.py` | Dry-run only: ok / fixed (NFC-only) / mention / defects; Swete-isolation arm (5-word skeleton shingles present in Swete and in neither NT witness) | `--selftest` |
| `word_index.py` | Skeleton form → refs, reporting tokens and verses separately | `--selftest` |
| `citation_sweep.py` | Span ends exist in WEB; every ref exists in its own witness; quote collates at the cited ref; claimed tier not overclaimed (E-05); NFC-degraded count (E-01); verse-existence disclosure required for crosswalk exceptions in or just after the span | `--selftest` |
| `stray_sweep.py` | Allowlist sweep of this folder; Swete files outside their folder; staging hash drift against the receipt | `--selftest` (live tree + an adversarial temp tree) |
| `run_suite.py` | Fail-closed runner (details below) | `--selftest` |

`run_suite.py` runs citation_sweep, the normalize dry-run and stray_sweep, all as HARD members.

- E-68 / Dan D1: a member is dead, and the suite RED, if any of these holds:
  - its stdout is not exactly one JSON object;
  - it has no valid status;
  - its exit code contradicts its status;
  - it crashes, or its script is missing.
- E-01: a normalize dry-run with fixed > 0 is HARD.
- E-20: a flag-shaped first argument writes nothing.

The fixture is `fixture/rows.good.jsonl`, 5 rows:

- 3John with the 1:15 split;
- all of Philemon;
- the pericope adulterae;
- Acts 8:36-38 with 8:37 disclosed;
- Acts 24:6-8.

`fixture/rows.bad.jsonl` has 6 adversarial rows, each carrying `_expect`. Both fixtures are generated from RP/SBLGNT by
`fixture/_make_fixture.py`. Quotes are at most 4 words. No Swete bytes are ever written to the fixture: the Swete arm
is tested in memory.

## Selftest and fixture results (MEASURED, 2026-09-29)

- Selftests: greek_lib, build_crosswalk, collate, word_index, citation_sweep, normalize_greek_in_json, stray_sweep and
  run_suite are all **GREEN**.
- `run_suite.py fixture/rows.good.jsonl`: **GREEN**, exit 0, with all 3 members GREEN and no dead members.
- `run_suite.py fixture/rows.bad.jsonl`: **RED**, exit 1.
  - citation_sweep found span_end_absent, ref_absent_in_witness, tier_overclaim, missing_disclosure and
    quote_not_at_ref.
  - normalize found fixed=1 (E-01 HARD).
  - stray_sweep was GREEN, and there were no dead members.
- Dead-member adversarial test (inside `run_suite.py --selftest`): six injected members are each listed as dead and
  make the suite RED. They are a crash, non-JSON output, two JSON lines, a statusless object, a GREEN-with-exit-1 lie,
  and a missing script.
- A single dead member next to a GREEN member also makes the suite RED.
- E-20: `run_suite.py --help` and `build_crosswalk.py --help` exit 2 and write nothing.

## Not verified / open

- **WEB's own textual base** is UNKNOWN for this lane. It was not traced. Only its verse existence was measured.
- **Swete tooling was not built.** Swete is not a collation witness. Its TEI verse structure (`textpart`
  chapter/verse) was observed but not validated, and there is no Daniel/Ezekiel/Zechariah crosswalk. Only the
  hash-based isolation arm reads it.
- **The editorial status of PA.csv and ACT24.csv** (why the RP repository prints them separately) is UNKNOWN. The
  tools disclose them and never rank them.
- **The B2 apparatus** is staged and hash-verified, but no tool parses it yet.
- **The tools were validated on the small fixture only**, not on real campaign rows. The crosswalk measurement itself
  covers all 27 books.
- **The disclosure rule** (exceptions inside the span, plus any non-WEB verses after a chapter-final span end) is a
  working design. It is not an owner-ratified policy.
