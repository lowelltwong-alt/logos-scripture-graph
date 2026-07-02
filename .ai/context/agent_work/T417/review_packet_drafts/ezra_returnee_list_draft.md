# Ezra Ezra.2.1-Ezra.2.70 Review Packet (Draft)

## Status

- Status: `draft_pending_standing_policy`
- T402 candidate ID: `T402-LC-015`
- Decision: pending
- Parent/child candidate: parent-only proposed
- Proposed parent unit for review: `Ezra.2.1-Ezra.2.70`
- Implementation allowed: false
- Output change authorized: false
- Reviewed gold promoted: false
- Strengthened packet: false
- Standing policy: `.ai/control/standing_owner_escalation_policy.yaml`
- Standing disposition when active: `proceed_parent_only_with_frontier_note`
- Escalation packet: `.ai/context/agent_work/T411/escalation_packets/T402-LC-015_theology_pressure.md`

This draft lives under `.ai/context/agent_work/T417/` only. It does not authorize output-changing work,
review-packet strengthening, reviewed gold, child spans, or theology authority.

## Review Target

`Ezra.2.1-Ezra.2.70` — Returnee list is structurally clear; restoration/covenant implications stay non-authorizing.

## Claim Traceability

- T411-CLAIM-105 (high): Substrate shows 70 verse rows in-span with markers ['c', 'f', 'fr', 'ft', 'p', 'v']..
- T411-CLAIM-106 (medium): Feature flags in-span include ['genre_narrative', 'has_footnote', 'has_strong_h']; metadata evidence.
- T411-CLAIM-107 (low): Queue theological pressure (restoration_theology_not_authorized) requires escalation before authorit.

## Premortem Red-Team Pass

1. Failure mode: theology pressure smuggled as boundary evidence. Fix: keep pressure in escalation note only.
2. Failure mode: draft treated as owner docket. Fix: require `APPROVE_STANDING_ESCALATION_POLICY` or explicit docket.
3. Failure mode: child spans created inside parent unit. Fix: parent-only remains unauthorized for children.

Theology pressure (T411-CLAIM-107) is non-boundary; see escalation packet.

No reviewed gold is promoted.
