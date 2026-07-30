# T521 M7 Sol marathon — iteration baseline and reusable optimization lead

Candidate-only process note; not an authority or completion receipt.

## Measured baseline

- Date: 2026-07-22
- Command: `write_completion_receipt_v2.py --book Deut` followed by `validate_book_completion_bundle.py --book Deut`
- Frozen input: Deut chunks SHA-256 `ab73ee7a888cd9a6f324d4c5d54bf99243cecd7a29c4316bd526be9a8d5d405f`
- Wall time: about 95 seconds for the combined completion command
- Correctness result: all five receipt gates and the completion-bundle closure passed
- Resource signal: subprocess-heavy repeated validation and repeated canonical JSONL parsing; no CPU/memory profile was taken

## Bottleneck hypothesis

The receipt writer runs exact coverage, official map validation, review parity, literary quality, and workflow validation. The completion bundle immediately repeats the same gates against unchanged hash-bound inputs. Several validators independently reparse the full canonical passage inventory and shared sidecars. The measured delay is therefore likely redundant process startup and I/O/parsing rather than a demonstrated language-level CPU hotspot.

## Safe optimization candidate

Preserve immutable gate evidence keyed by the complete input digest set (chunk map, packets, relations, postcheck, sidecar book projections, canonical passages, validator code/policy, and campaign contract). The bundle may reuse a passing gate receipt only when every invalidation key matches; otherwise it must rerun. Batch canonical passage parsing within one process where possible. Do not cache mutable state without exact content keys and do not weaken the role-separated postcheck or final receipt ordering.

## Limits and next experiment

No implementation or speedup claim is made. Profile one unchanged representative book completion, identify per-gate time and repeated parse counts, then compare a state-keyed evidence reuse path against the same workload with parity and failure-path tests. Rust is not indicated unless profiling later isolates a deterministic CPU/parsing hotspot with a stable boundary.

## Related deterministic repair

After controller metadata changes, revision-6 campaign jobs carried stale `model_manifest.yaml` pins. A scoped refresher updated only existing file-backed digest entries, preserved the campaign-self B00 receipt sentinel, and restored workflow validation. This is the previously known T521 stale-digest failure mode, not a new independent lesson.