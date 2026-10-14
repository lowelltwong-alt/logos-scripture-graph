# M8 reviewer continuation contract v1 — neutral procedural input

This contains no other lane's answers or scholarly conclusions. Your exact brief,
source-reading obligations, role restrictions, allowed paths, model authority and
legacy final deliverable schema still apply. A continuity record does not confer
acceptance or another reviewer's personal reading credit.

Write early: save each complete bounded evidence unit and its actual next cursor
in your authorized OUT, with your reviewer/execution identity, exact source and
dependency hashes, full findings/arguments and outstanding checks. Do not wait
until the whole review is finished. Partial output is never a passing final file.

Use named immutable delta sidecars or the existing early-write working format;
do not overwrite accepted evidence. The optional exact-path helper is
`sp_durable/campaign/m8_execution_efficiency.py`; it must be explicitly allowed
and hash-pinned by the brief before you import it. Its save_delta(path, data)
accepts schema m8_review_delta.v1, reviewer_id, execution_id, input_identities
(named SHA256 values), previous (null or same-directory filename+sha256),
completed_units (unique id and full evidence), next_cursor, pending_checks,
status and accepted:false. Status is partial, interrupted, quota_blocked or
ready_for_final_check. Every path must remain within your authorized OUT.
load_chain(last, reviewer, inputs, expected_last_sha) refuses changed identities,
corrupt/missing predecessors, duplicate units and acceptance. Neither helper
generates the legacy final deliverable or grants semantic approval.

Resume only your own verified completed work. A new physical run needs correct
execution lineage under the existing capture contract. Do not read another
blind lane's output, transcripts or campaign history. Do not list/glob/probe
for files in violation of the brief; use its exact paths. Delta predecessors
must be named explicitly by your own continuity record and allowed brief.

Record interruption/blocked/unknown status honestly. A prior launch is not proof
you are running. Preserve all required independent review, uncertainty, holds,
appeals, counterarguments, original source bytes and scope qualifications.
Engineering reuse does not waive your own required reading or semantic check.
Return the unchanged required final deliverable only when that work is complete.
