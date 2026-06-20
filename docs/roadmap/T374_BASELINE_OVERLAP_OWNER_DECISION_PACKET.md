---
object_type: roadmap_task_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-20 during T374 after baseline inspection found the current 1 Corinthians chunks overlap the exact owner-authorized parent span; updated after Lowell selected T374-OVERLAP-B and after the exact additive parent overlay was implemented."
reason_for_inclusion: "Give future agents and auditors a human-readable explanation of why T374 stopped before implementation, which option was selected, how the later implementation was constrained, and what remains unauthorized."
---

# T374 Baseline-Overlap Owner Decision Packet

T374 began from the T373-A authorization for an exact parent-only `1Cor.8.1-1Cor.10.33` route-isolated pilot. Before implementation, a baseline inspection found that the current generated chunk windows cross the target:

- `1Cor.7.25-1Cor.9.2`
- `1Cor.9.3-1Cor.10.5`
- `1Cor.10.6-1Cor.11.10`

That means a replacement-style implementation would affect adjacent non-target material: `1Cor.7.25-1Cor.7.40` and `1Cor.11.1-1Cor.11.10`. T372 required non-target identity proof, so implementation paused until the owner selected output semantics.

Machine-readable packet:

- `.ai/control/t374_baseline_overlap_owner_decision_packet.yaml`
- `.ai/control/t374_additive_parent_overlay_manifest.yaml`

## Owner Options

- `T374-OVERLAP-A`: conservative hold; no output change.
- `T374-OVERLAP-B`: additive parent overlay; preserve existing baseline chunks and add an exact parent-only overlay. This is selected by the owner.
- `T374-OVERLAP-C`: replacement with adjacent spill splits; requires explicit owner acceptance that adjacent non-target chunk records will change.
- `T374-OVERLAP-D`: widen the target to a baseline-aligned span; not recommended because it would require fresh review/gold for a materially different passage.
- `T374-OVERLAP-E`: dry-run/report only; gather more evidence without output changes.

## Selected Semantics

Lowell selected `T374-OVERLAP-B` on 2026-06-20. The later output-changing implementation adds only an exact additive parent overlay for `1Cor.8.1-1Cor.10.33` while preserving all existing baseline chunks byte-identical.

The selection record itself changes no chunk output. The implementation manifest records the output change and still does not authorize deleting or replacing existing chunks, adjacent spill splits, child spans, graph/retrieval truth, evaluator behavior changes, broader epistle generalization, preferred reading selection, source-tradition preference, boundary import, vector work, or whole-Bible output.

## Implementation Result

T374 now appends one non-truth-bearing overlay chunk:

- `chunk--eng-web--chunk-policy-v0.1.0--epistles-parent-overlay--1Cor.8.1--1Cor.10.33--T374-OVERLAP-B`

The baseline prefix remains byte-identical, `selected_children` remains empty, and T375 is the next review-only gate for same-baseline review, no-context audit review, and child-necessity review.
