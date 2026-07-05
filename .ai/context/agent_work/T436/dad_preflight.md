# T436 DAD Preflight

Task: T436 Jonah Hebrew metadata bridge pilot.
Agent: Codex.
Mode: evidence-only implementation.

## DAD Assets Checked

- Local repo DAD outbox pattern: `.digital-asset/mail/outbox.jsonl`
- Central DAD lesson ledger pattern: `C:\Users\lowel\OneDrive\Desktop\Git Projects\04_Digital_Assett_Directory\lessons\rust_rollout\lesson_ledger.jsonl`
- Prior Rust rollout lesson from T435: use Rust for deterministic high-volume scanners only after row shape and Python authority validation are proven.

## Applied Lesson

T436 does not add Rust. It first proves the Hebrew observation semantics over Jonah with no-text ledgers:

- UXLC is the clean source-token baseline.
- OSHB morphology is metadata evidence.
- OSHB `lemma` attributes are recorded as metadata-flag drift because the T431 source view says `contains_source_provided_lemmas: false`.
- OSHB morphology and lemma values are not stored in T436 outputs, only counts and hashes.

This keeps the later Rust scanner from scaling a wrong abstraction quickly.

## Candidate DAD Lesson To Send After Validation

Hebrew source-view pilots should separate clean source-token baselines from metadata-rich morphology sources and should detect source-view manifest drift before Rust expansion. A fast Rust scanner should follow only after Python validators prove which source attributes are observed text, source metadata hints, editorial layers, and prohibited authority surfaces.
