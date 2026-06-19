---
object_type: roadmap_task_record
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-19 during T380 to package the T371 owner decision after TCP-T378-B was selected."
reason_for_inclusion: "Make the T371 variant-dependency and parent-only reviewed-gold promotion decision transparent before any promotion or implementation work."
---

# T380 - T371 Variant-Dependency Owner Decision Packet

T380 creates a non-authorizing owner-decision packet for the next gate:

`T371 - Owner reviewed-gold promotion decision`

The packet asks whether the `1Cor.8.1-1Cor.10.33` parent-only boundary and reviewed-gold claim
are variant-non-dependent with respect to `1Cor.9.20` and `1Cor.10.9`, and whether parent-only
reviewed-gold promotion is authorized.

## Primary Artifact

`.ai/control/t371_variant_dependency_owner_decision_packet.yaml`

## Owner Options

- `T371-A`: confirm variant-non-dependent and promote parent-only reviewed gold.
- `T371-B`: hold for a focused textual-variant mini-dossier.
- `T371-C`: keep the evidence packet unpromoted.
- `T371-D`: re-route to a different review target.

The conditional recommendation is `T371-A` only if the owner confirms variant non-dependency.
If there is any doubt, `T371-B` is the conservative hold.

## Non-Authorizations

T380 does not authorize:

- variant dependency or non-dependency findings;
- preferred readings;
- source-tradition preference;
- reviewed-gold promotion;
- child spans;
- route or evaluator behavior;
- graph or retrieval truth;
- embeddings or vectors;
- chunk output;
- implementation.

T371 remains blocked until the owner gives an exact response.
