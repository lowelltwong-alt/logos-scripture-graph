# T432 DAD Preflight

Task: T432 Original-Language Schema Contracts.
Mode: read-only DAD preflight; no DAD authority over Scripture Graph.

## Sources Checked

- `C:/Users/lowel/OneDrive/Desktop/Git Projects/04_Digital_Assett_Directory/lessons/rust_rollout/lesson_ledger.jsonl`
- `C:/Users/lowel/OneDrive/Desktop/Git Projects/04_Digital_Assett_Directory/docs/HARNESS_VS_DETERMINISTIC_ENFORCEMENT.md`
- `C:/Users/lowel/OneDrive/Desktop/Git Projects/04_Digital_Assett_Directory/docs/rust/`
- `C:/Users/lowel/OneDrive/Desktop/Git Projects/04_Digital_Assett_Directory/assets/dad-rust-upgrade-starter-pack/`

## Relevant DAD Lessons

- `dad:rust-rollout-lesson:829dc53e-1688-5290-ab33-3352634c010d`: raw source archives with mixed corpus/support material need deterministic filtered source views before tokenization.
- `dad:rust-rollout-lesson:0e46712a-0c4f-5ac2-89d4-0f2f4d431f66`: canonical output refreshes need explicit canonical-66 scope when raw packages include appendix or deuterocanonical material.
- `dad:rust-rollout-lesson:8f6a8b1d-3be5-5e4e-8b52-9acff7fc0b04`: diff-aware validators need post-commit/base-ref parity for governance watched paths.
- `dad:rust-rollout-lesson:7c2cf2ca-c3ff-4f58-ab7c-087b36ab5f29`: derived source views need byte-for-byte lineage back to immutable raw inputs before downstream use.
- `dad:rust-rollout-lesson:0492d351-6444-4fa2-bc85-15ad0c4349ae`: Rust fast paths must prove negative-case parity before replacing Python governance validators.

## Rust Fit Verdict

T432 should stay Python/control-plane. The work is semantic schema design and authority-boundary validation, not high-volume deterministic scanning.

Rust is a strong later fit for T435 after these schemas stabilize:

- stream source-view token ledgers;
- validate large alignment JSONL files;
- compute per-book/source hashes and offsets;
- compare source-token and English-token indexes at scale;
- emit JSON summaries consumed by Python governance validators.

## DAD Outbound Lesson

No new DAD lesson is emitted from T432 yet. T432 applies existing DAD guidance: define schema contracts before Rust scanner implementation, keep Python as governance orchestrator, and reserve Rust for stable high-volume data passes with parity fixtures.
