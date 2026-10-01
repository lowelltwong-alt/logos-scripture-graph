rec("E", ["E-68"], "E-68", "a_validator_suite_fails_closed_and_a_toolkit_is_read_against_its_tools_code",
    "a validator suite could report GREEN with a HARD member dead and a toolkit stated its tools' contracts more "
    "strongly than their code",
    ["Each HARD member's predicate was written as that member's own failure status one member at a time so a member "
     "that crashed or printed no JSON object became ERROR and counted as nothing unless it was one of three named "
     "members. A crash in the member that refuses fabricated references could sit under a GREEN verdict",
     "The suite parsed the review normalizer's whole stdout as one object while the normalizer prints one JSON line per "
     "input file - so any review file made the member ERROR and the option was a false RED every time. No fixture ran "
     "the suite with more than one input",
     "The toolkit's tool table was written from docstrings and stated intent rather than read clause by clause against "
     "the code: it omitted three write sites and put a hard-errors heading over two FLAGS tools and said enforces where "
     "a selfcheck runs only a floor. Only the review lane that read the code could see it",
     "Rule: a suite fails closed. A member that produced no evidence is a HARD failure whatever its tier and is listed "
     "by name. A toolkit's account of a tool is read against the tool's code - write sites first - before it is pinned",
     "A toolkit that restates an owner directive quotes the owner's words and labels the orchestrator's reading of them "
     "as INFERRED",
     "This is E-64's and E-67's family: acting on an unread assumption about a tool",
     "APPLIES to any validator suite that aggregates member verdicts and to any toolkit or contract document that "
     "describes tools a lane will trust. DOES NOT APPLY to the suites of closed books which keep the old predicate and "
     "are not reopened for this",
     "DANGER IF STRIPPED: a crashed reference-refusal member under a GREEN verdict lets fabricated citations pass the "
     "HARD gate and a lane trusting an overstated contract under-checks exactly where the contract overstates"],
    ["of 115 suite reports under the campaign none reports GREEN while any member is ERROR - observed harm nil",
     "7 of the 8 suite files in the campaign lack a dead-member rule by a text search whose predicates were not read "
     "one by one - so the exposure is INFERRED to be campaign-wide",
     "the code-reading review lane found 13 defects and each was confirmed against the cited lines before any "
     "correction - the byte-reading lane found none",
     "the amended suite passed a 4-case regression run in a scratch copy with the other members stubbed: dead members "
     "turn RED and a two-file normalizer run turns GREEN",
     "the corrected toolkit passed its selfcheck in full and in artifacts-only scope and both zone fixture tests exit 0"],
    "MEASURED", "the ledger entry records the confirmed defects and the before and after regression runs and the "
    "selfcheck results - the campaign-wide exposure is labelled INFERRED in the entry")
