# DANIEL PHASE 0 - LANE K2: TOOLKIT REVIEW, CODE (blind; claude-opus-5-5, OW-25)

Attempt `dan_toolkit_review_k2_a1`, execution `dan_toolkit_review_k2_a1#e1`. The orchestrator wrote Daniel's shared
verification toolkit, `TOOLKIT.md`, pinned below. Every later lane that annotates Daniel reads its account of the
tools and runs them as it says, so a wrong contract in it reaches every one of them. OW-19 makes two blind review lanes
the floor. You are one of them. The other works by a different method; you will not see it, and it will not see you.
Do not try to find it. You AUDIT the toolkit; you do not rewrite it. Fable reviews every book at the campaign's end
(OW-28); your findings are an input to that, not a substitute for it.

`SP` below is `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`. Your output directory, `OUT`, is `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\dan_p0\lane_K2`.

Your method is the code. Every statement `TOOLKIT.md` makes about a tool, its invocation, what it checks, what it
refuses, what it writes and where, and what the toolkit's own selfcheck enforces, is checked against the tool's source,
read in ranges. You do not re-measure the book's figures; the other lane does that. **You run no pinned file**: E-67
records a smoke run that wrote into SP. Where a contract can only be settled by running the tool, say so under
`what_i_could_not_verify`.

## Your authority, and what is not yours (OW-11)

You write in `OUT`, and nowhere else. You never commit, push, merge, clean or prune; never run git; never write
receipts or touch any registry; never modify, re-serialise, re-generate or run any pinned file. Scripts of yours, if
you need any to scan source text, live in `OUT`, run from there with `python -B`, and open pinned files read-only by
exact path. Never print a whole file; print line ranges of at most 120 lines, counts and short slices.

## What you verify, recorded in `toolkit_review_k2.json`

1. **The tool table.** For each row of "Staged tools": the invocation and arguments, each check or arm it lists, each
   thing it says is RED, HARD or refused, and every write site (which file, where, under what condition). Record
   `confirmed` or `defect` with the source lines. A write site the toolkit does not state is a DEFECT (E-67). The
   suite's HARD member list is checked against `run_validator_suite.py`.
2. **Invocation and encoding.** The run instruction (`PYTHONIOENCODING=utf-8`, the working directory) and every claim
   in "Encoding + skeleton notes" about code behaviour, above all what `dan_lib.skeleton` does with maqaf and what its
   docstring says, against `dan_lib.py`'s source.
3. **What the selfcheck enforces.** `_toolkit_selfcheck.py` claims to check "every pinned claim in this file". Map each
   of its toolkit pins to the `TOOLKIT.md` line it guards, and list the figures in `TOOLKIT.md` that no pin guards.
   Check that each pin reads its figure from the artifact it names rather than from a literal, and that
   `--artifacts-only` skips exactly the toolkit's own checks.
4. **E-65's item.** E-65 bans any Ezekiel figure from a Daniel artifact, and the toolkit says the selfcheck enforces it.
   Read the guard's code and state exactly what it can see and what it cannot. It is known to ignore every number
   below 100, to be unable to flag a number that is also a true Daniel figure, and to be blind to non-integers; confirm
   or refute each from the code, name any further blind spot, and say where the list of Ezekiel figures it checks
   against comes from. Give, as `judgement`, the options for closing each blind spot, each with its cost.
5. **Rules that name a tool.** Each standing rule or fact that says a tool enforces it: the named tool exists among
   your pins and its code enforces it as stated. A rule naming a tool you were not given is recorded under
   `what_i_could_not_verify`, not guessed.
6. **Provenance (OW-18).** A contract stated more strongly than the code supports is flagged: implication is
   assertion.

## Verdict

`fit_to_accept` only if no DEFECT stands; otherwise `not_fit`. Every DEFECT carries one of:

- an EXACT correction: the text to find (unique in `TOOLKIT.md`) and the text to replace it with, so the orchestrator
  can apply it by a guarded edit and re-verify; or
- where no exact correction is yours to make (a tool whose code is wrong, a guard that cannot see), `judgement`: the
  evidence and the options, for adjudication.

## Budget

About 60 tool calls. Read each tool in the ranges its contract needs; do not survey code the toolkit makes no claim
about.

## Pinned inputs

| input | sha256 |
|---|---|
| `SP\Dan\tools\TOOLKIT.md` | `d9bc3a0a17fb8aacfbaf4b84303b15e01560eb57e10c76cacd90f9d497c8abd2` |
| `SP\Dan\tools\run_validator_suite.py` | `3760fd45d5a626fbf2d1b6630c1717acc84b9433ef1596c721bd7f7d355e2aad` |
| `SP\Dan\tools\citation_sweep.py` | `d5bd9b33a9c050a96932fe410c6f935cab94c12282f80593340fd7aa1c5ec652` |
| `SP\Dan\tools\normalize_hebrew_in_json.py` | `50aac534effc00af91a766dc91151cc39f86b6af4a7db104048e6097de2be693` |
| `SP\Dan\tools\check_marks.py` | `df1818f72467102408985321848c63b79e4e4ba018a8b67d768a65107a3ab3b7` |
| `SP\Dan\tools\check_language_zones.py` | `8bbf3049eca2bda24620e96188d8907330140b8122e9152b098601fc2cea67c3` |
| `SP\Dan\tools\check_role_tokens.py` | `097af5cb8d29d21dbc7d265ef887a5fc761cbd4f4b412cb2a4e70efc8e40c8a3` |
| `SP\Dan\tools\check_brief_vs_suite.py` | `2a37dd83f84e01a58bd146c4645993529a1c3b3c8088b690e400f52e2bd8a876` |
| `SP\Dan\tools\cap_sweep.py` | `91be20cb82dd861a093fbf2957a95ba3b7fcaec5df66bceac0c7c64c5f8fdfa1` |
| `SP\Dan\tools\build_verse_maps.py` | `2806313706d8ae803599b62f5c6f42e97188fc7a5f1e7b6b44d2abe368fc3c19` |
| `SP\Dan\tools\dan_lib.py` | `1f397a7a08aba99cad67b0a59378eafa961130559bd8d07a7a9ed9d2f3043361` |
| `SP\Dan\tools\_toolkit_selfcheck.py` | `3fe5e2e50e03cced96cabb9354f4a57f40ba18d3e3a510523feb087e015de86f` |
| `SP\Dan\tools\_test_zone_tools_dan.py` | `a3aa391251b9e76c27780dd0b699eaa614cb637f9cf81b98cfc9a7487f318431` |
| `SP\Dan\tools\_test_language_zones_dan.py` | `9c99a56c61683166cb5d1e385b11e010956e842e72e4252600a7f14383113332` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `8a9b0b431b35c39fa022818a653f80a32fc6241ef636b4b11ec1682d80b7ee11` |

How you may use each input:

- `SP\Dan\tools\TOOLKIT.md`: READ whole. The toolkit under review.
- `SP\Dan\tools\run_validator_suite.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\Dan\tools\citation_sweep.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\Dan\tools\normalize_hebrew_in_json.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\Dan\tools\check_marks.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\Dan\tools\check_language_zones.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\Dan\tools\check_role_tokens.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\Dan\tools\check_brief_vs_suite.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\Dan\tools\cap_sweep.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\Dan\tools\build_verse_maps.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\Dan\tools\dan_lib.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\Dan\tools\_toolkit_selfcheck.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\Dan\tools\_test_zone_tools_dan.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\Dan\tools\_test_language_zones_dan.py`: READ ONLY - NEVER RUN; in ranges. A staged tool the toolkit describes.
- `SP\campaign\grader_models.v1.json`: READ. The grader carrier: the OW-25 fallback model and its statement.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 807-874 only. The M8 ledger: OW-11, the owner's exception, and OW-11-h.

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. **`OUT\final_message.md`**, at most 20 lines, written FIRST and rewritten at the end: the verdict, the DEFECT count
   by section, the sha256 of `toolkit_review_k2.json`, and the statement that you ran no listing and no glob.
2. **`OUT\toolkit_review_k2.json`**, one object: `verdict`, `tool_table` (per tool: each claim, `confirmed` or
   `defect`, source lines), `invocation_and_encoding`, `selfcheck_coverage` (`pins`, `unguarded_figures`),
   `e65_guard` (`sees`, `blind_spots`, `options`), `rules_naming_tools`, `provenance`, `defects` (each: `id`,
   `section`, `finding`, `evidence`, and `exact_correction` {`find`, `replace`} or `judgement` {`options`}),
   `what_i_could_not_verify`, `e19_selfreport`, `tool_calls_used`, `limit`.

## Hard stops

A pinned digest that differs from the table: record both and stop. Never list, glob or search a directory; a shell
wildcard is a glob, even inside `OUT`. Never write outside `OUT`. Never run a pinned file.
