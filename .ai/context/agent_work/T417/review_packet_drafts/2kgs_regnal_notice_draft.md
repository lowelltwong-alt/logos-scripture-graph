# 2Kgs 2Kgs.15.32-2Kgs.15.38 Review Packet (Draft)

## Status

- Status: `draft_pending_standing_policy`
- T402 candidate ID: `T402-LC-012`
- Decision: pending
- Parent/child candidate: parent-only proposed
- Proposed parent unit for review: `2Kgs.15.32-2Kgs.15.38`
- Implementation allowed: false
- Output change authorized: false
- Reviewed gold promoted: false
- Strengthened packet: false
- Standing policy: `.ai/control/standing_owner_escalation_policy.yaml`
- Standing disposition when active: `proceed_parent_only_with_frontier_note`
- Escalation packet: `.ai/context/agent_work/T411/escalation_packets/T402-LC-012_theology_pressure.md`

This draft lives under `.ai/context/agent_work/T417/` only. It does not authorize output-changing work,
review-packet strengthening, reviewed gold, child spans, or theology authority.

## Review Target

`2Kgs.15.32-2Kgs.15.38` — A regnal notice has formulaic boundaries; kingdom theology is not authorized.

## Claim Traceability

- T411-CLAIM-096 (high): Substrate shows 7 verse rows in-span with markers ['c', 'p', 'v', 'w']..
- T411-CLAIM-097 (medium): Feature flags in-span include ['genre_narrative', 'has_strong_h']; metadata evidence-only..
- T411-CLAIM-098 (low): Queue theological pressure (kingdom_theology_not_authorized) requires escalation before authority-ad.

## Premortem Red-Team Pass

1. Failure mode: theology pressure smuggled as boundary evidence. Fix: keep pressure in escalation note only.
2. Failure mode: draft treated as owner docket. Fix: require `APPROVE_STANDING_ESCALATION_POLICY` or explicit docket.
3. Failure mode: child spans created inside parent unit. Fix: parent-only remains unauthorized for children.

Theology pressure (T411-CLAIM-098) is non-boundary; see escalation packet.

No reviewed gold is promoted.
