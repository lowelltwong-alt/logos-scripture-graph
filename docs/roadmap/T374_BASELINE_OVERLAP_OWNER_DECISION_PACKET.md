---
object_type: roadmap_task_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-20 during T374 after baseline inspection found the current 1 Corinthians chunks overlap the exact owner-authorized parent span."
reason_for_inclusion: "Give future agents and auditors a human-readable explanation of why T374 stopped before implementation and what owner options remain."
---

# T374 Baseline-Overlap Owner Decision Packet

T374 began from the T373-A authorization for an exact parent-only `1Cor.8.1-1Cor.10.33` route-isolated pilot. Before implementation, a baseline inspection found that the current generated chunk windows cross the target:

- `1Cor.7.25-1Cor.9.2`
- `1Cor.9.3-1Cor.10.5`
- `1Cor.10.6-1Cor.11.10`

That means a replacement-style implementation would affect adjacent non-target material: `1Cor.7.25-1Cor.7.40` and `1Cor.11.1-1Cor.11.10`. T372 required non-target identity proof, so implementation is paused until the owner selects output semantics.

Machine-readable packet:

- `.ai/control/t374_baseline_overlap_owner_decision_packet.yaml`

## Owner Options

- `T374-OVERLAP-A`: conservative hold; no output change.
- `T374-OVERLAP-B`: additive parent overlay; preserve existing baseline chunks and add an exact parent-only overlay. This is recommended if the owner wants output movement now.
- `T374-OVERLAP-C`: replacement with adjacent spill splits; requires explicit owner acceptance that adjacent non-target chunk records will change.
- `T374-OVERLAP-D`: widen the target to a baseline-aligned span; not recommended because it would require fresh review/gold for a materially different passage.
- `T374-OVERLAP-E`: dry-run/report only; gather more evidence without output changes.

The recommendation is not owner selection. No chunk output, route behavior, evaluator behavior, graph/retrieval truth, child span, preferred reading, source-tradition preference, boundary import, vector work, or whole-Bible output change is authorized by this packet.

## Current Stop Rule

Do not implement chunks until Lowell selects one exact `T374-OVERLAP-*` option and the selected semantics are recorded in the decision register, readiness map, task scope, validators/tests, and handoff.
