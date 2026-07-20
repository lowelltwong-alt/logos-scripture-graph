# T511 iteration measurement

- `python scripts/validate_all.py`: 211.3 seconds, correctness pass in clean mode.
- Final cached handoff-inclusive aggregate: 93.7 seconds, correctness pass in clean mode.
- Initial full pytest: 679.46 seconds, four compatibility-test failures.
- Final full pytest: 602.49 seconds, 996 passed and 55 explicit generated-data skips.
- Bottleneck class: broad repository validation/process and test workload, not the new registry
  scheduler; scheduler unit work is sub-second and parses no canonical corpus.
- Decision: no runtime rewrite or cache was added in T511. Focused lifecycle replay (18 passed,
  2 skipped) completes in 4.54 seconds and is the iteration loop; full gates remain final evidence.
- Future optimization requires separate profiling and exact parity/failure-path proof. Rust is not
  justified for this filesystem-policy orchestration surface.
