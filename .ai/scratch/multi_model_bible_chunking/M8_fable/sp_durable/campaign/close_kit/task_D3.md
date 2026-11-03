**Your role.** You are the proposer. You do not edit the method record and you do not adjudicate your own proposals; someone
who is neither you nor the orchestrator will. 'No proposal, and here is why' is an acceptable result.

**What to do.** Execute `METHOD_PROPOSER_BRIEF.md` (pinned below) for {{BOOK_NAME}}. It is binding on what you read and on the
form of each proposal (`m8_method_change_proposal.v1`); where it says the output path is named by the launch message, the
path is your OUT, at the name below. Read this book's own landed evidence itself (the packets in the manifest of landed
outputs, including their free-text uncertainty fields, and the routed questions), never a summary. Read the current method
record in full, and the existing proposals log so that you do not re-propose what is already adjudicated (say so where an
observation here repeats one). Read packets by script extracts of the fields you need; never print one whole.

{{GROUND}}

**Deliverables, in OUT:** `method_change_proposals.{{BOOK}}.candidate.jsonl`: one proposal per line in the brief's schema, each
with `book`:"{{BOOK}}" and a `proposal_id` of the form `{{BOOK}}-P01`; or zero lines. `proposer_notes.json`: the packets you
read (path and sha256), the count of proposals, and, if zero, why.
