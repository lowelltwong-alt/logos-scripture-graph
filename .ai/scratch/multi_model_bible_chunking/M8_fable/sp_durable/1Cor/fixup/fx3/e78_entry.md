
## E-78 (2026-11-01) - 1 CORINTHIANS FIXUP-3 LANDING: A LANDER THAT READ A KEY THE SUITE NEVER PRINTS, A SUITE SUMMARY THAT CANNOT SHOW ONE MEMBER'S FLAGS, A FIELD LICENCE WRITTEN FROM EXPECTATION, AND A HELP PROBE THAT WROTE FILES

**What happened (MEASURED unless marked).**

- **(a) A dead read in my lander (my error).** `land_fixup3.py validators()` read `j.get("members")`. The suite prints `per_check`, so `not_green` was always empty. W4's author reported refs_mirror FLAGS on four citations, and my lander showed clean. The `offending` field for ngram7 was dead in the same way: the report key is `offending_7grams`.
- **(b) A summary figure that cannot show one member (found by the same read).** The suite's `triage_flags` sums `flag_count`, and refs_mirror reports no such key, so that figure reads 0 whatever refs_mirror finds. The suite is a pinned tool and was not changed; the item went to S5 through `author_unresolved_for_S5.md`.
- **(c) A field licence written from expectation (my error).** `build_fixup3.py`'s EXTRA list and the lander both omitted `W2-006.literature_type_guess`, which R4-W2-006 orders. The author blocked and reported, which was the correct act. The sibling audit of every order's named fields found only W2-006, W5-002 and W6-007, -013, -014 outside the base licence.
- **(d) A change-log match that failed on indexed fields (my error).** The lander compared `boundary_evidence_refs[3]` with the bare field name and gave 13 false problems at the first real lane. It was fixed before any row was appended.
- **(e) A probe that wrote files (my error).** `build_fixup3.py --help` was run on a generator with no argument parser, which took `--help` as a part name and wrote stray brief and message files. They were disclosed and removed, and all twelve real digests were re-measured unchanged.
- **(f) Notification time is not landing time (candidate).** `make_review_landing.py`'s docstring records the difference. This entry records it so that the candidate has a home.

**Containment (MEASURED).** For (a), every saved report for W1, W2, W3 and W5 was read: all members GREEN, so the recorded values were true although the check behind them was dead. Only W4 flags. The W4 row's note carries the correction, and its `orchestrator_verification.problems` carries the flags.

**Root cause.** In (a), (c) and (d), a tool of mine was written from what I expected the other side to contain, and nothing proved that the read could ever return a positive. (e) is the same fault applied to a command line.

**Not settled here.** Still owed, and still not recorded because each needs a fresh read of its own source: the tier-template ambiguity, the registry-authority and scoped-parity incident, and the `python -c` deviations. The resume of the `cwo05_ref` author (114156 tokens, 1 tool use, 25823 ms) has no receipt row. Whether the suite's summary should sum refs_mirror is a ruled matter, not mine.

**Corrective controls (MEASURED).** `validators()` now refuses with SystemExit when `per_check` is absent, excludes `greek_normalize_dryrun` only when its string says `defects=0`, and adds `refs_mirror_worklist`. `land()` records a problem when a triage member is not GREEN. Regression evidence is one positive (W4 shows its flags) and one negative (W5 shows none). `land_fixup3.py.pre_83da5bcb5841` keeps the former bytes. `licence_table.py` classifies every changed field from the orders' own text.

**Lesson.** A check on another tool's output needs a positive fixture before it is trusted: if no input can make it say no, it is not a check. A summary figure is a claim about each member, so read the per-member record. Derive a licence from the orders' text, not from a list of what you expect them to name. Never pass an argument to a generator until its code shows a parser.
