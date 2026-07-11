# DAD Candidate Fixtures

`candidate_messages.jsonl` is immutable test and provenance evidence copied
from the former tracked runtime outbox during the transport 1.0.0 cutover. It
is not a transport spool and must never be collected or appended to by DAD.

Validators use it to preserve historical candidate-envelope, linkage, and
non-authorization checks while `.digital-asset/mail/*.jsonl` remains local and
gitignored.
