# Judg Judg.12.8-Judg.12.15 Review Packet (Draft)

## Status

- Status: `draft_pending_standing_policy`
- T402 candidate ID: `T402-LC-007`
- Decision: pending
- Parent/child candidate: parent-only proposed
- Proposed parent unit for review: `Judg.12.8-Judg.12.15`
- Implementation allowed: false
- Output change authorized: false
- Reviewed gold promoted: false
- Strengthened packet: false
- Standing policy: `.ai/control/standing_owner_escalation_policy.yaml`
- Standing disposition when active: `proceed_parent_only_with_frontier_note`
- Escalation packet: `.ai/context/agent_work/T411/escalation_packets/T402-LC-007_theology_pressure.md`

This draft lives under `.ai/context/agent_work/T417/` only. It does not authorize output-changing work,
review-packet strengthening, reviewed gold, child spans, or theology authority.

## Review Target

`Judg.12.8-Judg.12.15` — Minor-judge notices are discrete and formulaic; moral or covenant assessment is not authorized.

## Claim Traceability

- T411-CLAIM-081 (high): Substrate shows 8 verse rows in-span with markers ['c', 'p', 'v', 'w']..
- T411-CLAIM-082 (medium): Feature flags in-span include ['genre_narrative', 'has_strong_h']; metadata evidence-only..
- T411-CLAIM-083 (low): Queue theological pressure (covenant_cycle_theology_not_authorized) requires escalation before autho.

## Premortem Red-Team Pass

1. Failure mode: theology pressure smuggled as boundary evidence. Fix: keep pressure in escalation note only.
2. Failure mode: draft treated as owner docket. Fix: require `APPROVE_STANDING_ESCALATION_POLICY` or explicit docket.
3. Failure mode: child spans created inside parent unit. Fix: parent-only remains unauthorized for children.

Theology pressure (T411-CLAIM-083) is non-boundary; see escalation packet.

No reviewed gold is promoted.
