# DAD Mail Cache

This directory is a repo-local runtime transport surface. Logos-local tools may
append candidate metadata to `outbox.jsonl`; DAD may read approved candidate
metadata into its central data root. All JSONL, lock, and temporary files stay
untracked.

DAD may not create, modify, deliver, archive, or delete any file in this Logos
repository. Candidate responses are read or pulled from DAD centrally and do
not authorize a local change.
