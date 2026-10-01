rec("E", ["E-66"], "E-66", "an_audit_that_derives_its_input_set_by_pairing_must_list_every_file_it_did_not_pair",
    "a token-transform audit paired ported files by same name so it skipped a renamed port in silence and audited "
    "an authored file as a port",
    ["The audit's input set was implicit: the Daniel files that have a same-name source. The rename map lived only in "
     "a lane's scratch. The silent skip merged two states - a file that is not a port and a port under a new name - so "
     "a clean result meant only nothing in the set it looked at. This is E-65's shape again",
     "State an audit's input set explicitly: pair by name and failing that by the adapter's filename token transform "
     "and report each row's source and pairing basis. Declare every authored file with its reason and never align it. "
     "List every remaining unpaired file so an absence is visible and not silent",
     "A clean report over an incomplete set is a half-truth (OW-18) and a renamed port is where a transform rewrites "
     "the most",
     "A guard for a class of leaked predecessor figures states its blind spots: a whole-token search for integers of "
     "100 or more cannot see a smaller figure or a figure true for both books or a non-integer - so the review-lane "
     "control stands beside it unchanged",
     "A review script that reads Hebrew imports the book library's skeleton function and never hand-rolls a strip: "
     "putting a space in place of each mark split every word into letters",
     "APPLIES to any audit or census whose input set is derived by pairing or matching files rather than enumerated. "
     "DOES NOT APPLY where the input set is an explicit enumerated list that is itself checked for completeness",
     "DANGER IF STRIPPED: a renamed port escapes the only control for history rewritten by the book-token transform "
     "and the audit still reports clean"],
    ["the renamed port _test_zone_tools_dan.py went unaudited: 148 source-token lines and 16 lines pairing a Daniel "
     "token with a lineage word",
     "at the fix all 16 unread lines were read and each is true lineage - observed impact nil",
     "after the cure the audit covers 20 files with 416 source-token lines (414 changed and 2 kept verbatim) and 23 "
     "Daniel lines naming the source book and 31 lineage-signature lines",
     "a compaction summary had framed a later-created data file as an omission of an earlier entry and a fresh read "
     "of the file times corrected it before anything was written - E-59's rule working",
     "the Hebrew misread was seen in output and corrected before any record used it and the corrected strip equals "
     "the library skeleton on all 357 verses with 0 differences"],
    "MEASURED", "the ledger entry records a before and after run of the audit with a row diff and a measured equality "
    "of the corrected strip against the library skeleton")

rec("E", ["E-67"], "E-67", "a_gate_is_not_a_pure_reader_read_its_write_sites_and_rerun_it_after_placing_a_file",
    "a smoke run on another book's brief wrote a Daniel-named report into durable state and a recorded GREEN went "
    "stale when a file was placed into the directory the gate scans",
    ["Both slips treated a gate as a pure reader of its own inputs. The brief check wrote its report to a fixed path "
     "beside itself whatever brief it was given. A gate that scans a directory gives a verdict about that directory's "
     "state when it runs - placing a file changes the state and the verdict expires",
     "Before smoke-running a tool in durable state read its write sites. Run tools on foreign inputs only from scratch "
     "copies. Re-run every gate that scans a directory after placing a file into it",
     "Tie a tool's durable write target to its input: write the durable report only for an input inside the tool's "
     "own book and for any other input print the verdict and write nothing. A selftest proves that a foreign passing "
     "input and a foreign failing input and a missing input each leave the report byte-for-byte unchanged",
     "When a recorded pass expires correct the carrier by amendment: a stale GREEN is a half-truth (OW-18) that a "
     "resume could launch review lanes against",
     "This is E-64's family: acting on an unread assumption about a tool",
     "APPLIES to any smoke run or gate run in a durable directory and to any recorded verdict of a gate that scans a "
     "directory. DOES NOT APPLY to a run whose write sites were read in the same session on scratch copies of its "
     "inputs",
     "DANGER IF STRIPPED: once a real brief exists the same smoke run overwrites the book's own PASS or FAIL record "
     "with another book's verdict under the book's own filename"],
    ["the stray report was moved to scratch evidence under a pinned digest before anything used it and no Daniel "
     "authoring brief existed so no real report was overwritten",
     "the selfcheck pre-image executed against the current tree gave 155/157 RED on two checks while the carrier "
     "still claimed GREEN",
     "after the cure and after the toolkit file was placed every gate that scans the tree was re-run: selfcheck "
     "232/232 full scope and 157/157 artifacts-only GREEN",
     "a write-site audit of every Daniel tool found 10 files that write and no other tool writes a fixed durable "
     "path from a foreign input"],
    "MEASURED", "the ledger entry records the pre-image run against the current tree and the post-cure runs and a "
    "write-site audit of every Daniel tool")
