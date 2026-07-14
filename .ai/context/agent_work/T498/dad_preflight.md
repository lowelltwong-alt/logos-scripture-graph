# T498 DAD preflight

- session: `dad:session:33313a13-888f-4d56-a894-cc5ffe486e3e`
- trace: `dad:trace:0c906e30-e002-5570-9210-e98230628278`
- risk: medium, additive shared tooling contract with no consumers
- selected branches: software contract, schema, Git subprocess, fixture tests,
  rollback, and later migration parity
- DAD asset search: no narrower reviewed changed-path implementation was offered;
  Rust and shadow-parity assets were not adopted because this PR establishes the
  Python reference and has no measured CPU/parser hotspot
- stop conditions: any consumer migration, existing validator behavior change,
  canonical data access, unresolved Git ambiguity, or authority-bearing change
- review lanes: checklist red-team, reusable asset/deduplication review, learning
  loop, pattern discovery, and prompt-value minimization at postflight

DAD is candidate guidance only and does not override OD-K or repository authority.

## CI correction session

- session: `dad:session:f10623ee-e43e-41d5-aaa0-1688d2434186`
- trace: `dad:trace:4027f9eb-36d8-5f25-b31a-c39b882dab1d`
- scope: approved Git 2.54 shallow-deepen portability correction, focused tests,
  documentation, and T498 lifecycle evidence only
- asset decisions: performance and Rust offerings were not adopted because the
  failure is one Git refspec portability defect with no measured parser hotspot
- stop conditions: consumer migration, unbounded fetch, temporary ref creation,
  Scripture data access, or authority-bearing change
- review mode: explicit local checklists; subagents are not authorized for this task

DAD daemon and mail freshness warnings do not affect local source authority or
the approved narrow CI correction.
