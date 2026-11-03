**Your role.** You are a builder, not a reviewer of the rows: you change no row and judge no boundary. Two blind lanes will
later grade what you build against the primary sources, so state limits plainly; a record that hides a gap fails later.

**What to do.** Build {{BOOK_NAME}}'s scholar record as close-gate item 20 demands (read the item's own words in the gate
file). The record speaks in scripture references and never in campaign vocabulary (row ids, lane names, rule codes,
process nouns); the checker enforces a blocklist. Every factual sentence about the text is composed from a landed packet's
fields, verbatim or by mechanical transformation, and every structural sentence comes from a listed template string. The
checker must test: every landed review packet represented; every high-severity finding present; every cross-lane
disagreement surfaced; nothing asserted that is not in a packet; every routed open question present as open (measure the
count); regeneration byte-identical. Include the witnesses' licence and attribution terms, checked against what the book's
own files say.

{{PORT_RULE}}
{{GROUND}}

**Deliverables, in OUT:** `scholar_record\gen_scholar_record.py`, `scholar_record\check_scholar_record.py`,
`scholar_record\{{BOOK_UPPER}}_SCHOLAR_RECORD.v1.md` (written by the generator), `scholar_record\scholar_record_check.v1.json`
(written by the checker; it must say PASS with every sub-check and its count, or you report honestly which sub-check fails
and why), `scholar_record\book_params.v1.json`, and `build_notes.json`: what you ported, what you changed and why, every
packet class you found with its count, and every limit.
