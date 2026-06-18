---
object_type: roadmap_owner_decision_record
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-18 during T367 to record the owner's John 3, textual-critical policy, orthodox firewall, and next epistle target decisions."
reason_for_inclusion: "Keep the owner decisions no-context-auditable before any future John 3 gold, variant-sensitive packet, or epistle argument strengthening work."
---

# T367 Owner Decision Firewall And Next Target

## Owner Decisions Recorded

T367 records four owner decisions:

1. `JOHN3-T356-B` is selected: `John.3.1-John.3.36` is approved as a parent-only review target.
2. A textual-critical policy docket is required before variant-sensitive packets can be promoted,
   implemented, used as reviewed gold, or used for canon/source-tradition/boundary decisions.
3. An Orthodox Hermeneutic Firewall / Anti-Smuggling Docket is required before the next epistle
   packet is strengthened.
4. After the firewall is recorded, `1Cor.8-1Cor.10` is authorized as the next epistle argument
   review-packet strengthening target, review-only and non-output-changing.

## John 3 Decision

```yaml
john3_owner_review:
  owner_selection_status: selected
  selected_option: JOHN3-T356-B
  selected_parent: John.3.1-John.3.36
  selected_children: []
  selected_jesus_speech_span: null
  parent_only_review_target_authorized: true
  child_span_authorized: false
  jesus_narrator_boundary_authorized: false
  reviewed_gold_promoted: false
  route_behavior_authorized: false
  graph_or_retrieval_truth_authorized: false
  output_change_authorized: false
```

This approves the review target only. It does not make the parent span reviewed gold, does not
approve child spans, and does not decide whether the disputed John 3 material is Jesus speech,
narrator commentary, or unresolved for chunking.

## Policy Dockets

Machine-readable dockets:

```text
.ai/control/orthodox_hermeneutic_firewall_docket.yaml
.ai/control/textual_critical_policy_docket.yaml
```

The orthodox firewall affirms Nicene/Chalcedonian orthodox Christianity and canonical Scripture
authority. It refuses hidden anti-supernatural, anti-canonical, heterodox, or liberal-critical
defaults. It also refuses to hardcode one denominational systematic theology as chunk authority.

The textual-critical docket does not select a textual-critical policy. It records that a future
explicit policy decision is required before variant-sensitive packet promotion, implementation,
reviewed-gold use, canon/source-tradition decisions, boundary import, graph truth, or retrieval
truth.

## Next Review Lane

After this task, the readiness map may point to:

```yaml
next_route:
  task_id: T368
  route_type: epistle_argument_review_packet_strengthening
  selected_target: 1cor8_10_food_offered_to_idols
  selected_passage: 1Cor.8-1Cor.10
  review_only: true
  output_change_authorized: false
  implementation_authorized: false
  reviewed_gold_promoted: false
```

T368 may strengthen the existing `1Cor.8-1Cor.10` packet only as review prep. It may not promote
gold, change route behavior, change evaluator behavior, generate graph edges, assert retrieval
truth, or regenerate chunks.

## Non-Authorizations

T367 does not authorize:

- John 3 child spans;
- John 3 Jesus/narrator boundary decisions;
- John 3 reviewed-gold promotion;
- variant-sensitive reviewed-gold use without a later textual-critical policy;
- 1 Corinthians implementation;
- epistle route behavior;
- evaluator changes;
- generated chunk regeneration;
- graph edges;
- retrieval truth;
- boundary import;
- output changes.
