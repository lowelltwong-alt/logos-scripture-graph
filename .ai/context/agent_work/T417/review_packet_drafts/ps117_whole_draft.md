# Ps Ps.117.1-Ps.117.2 Review Packet (Draft)

## Status

- Status: `draft_pending_standing_policy`
- T402 candidate ID: `T402-LC-019`
- Decision: pending
- Parent/child candidate: parent-only proposed
- Proposed parent unit for review: `Ps.117.1-Ps.117.2`
- Implementation allowed: false
- Output change authorized: false
- Reviewed gold promoted: false
- Strengthened packet: false
- Standing policy: `.ai/control/standing_owner_escalation_policy.yaml`
- Standing disposition when active: `proceed_parent_only_with_frontier_note`
- Escalation packet: `.ai/context/agent_work/T411/escalation_packets/T402-LC-019_theology_pressure.md`

This draft lives under `.ai/context/agent_work/T417/` only. It does not authorize output-changing work,
review-packet strengthening, reviewed gold, child spans, or theology authority.

## Review Target

`Ps.117.1-Ps.117.2` — Short whole-psalm parent can be reviewed without child spans; liturgical and canonical use remain evidence only.

## Claim Traceability

- T411-CLAIM-111 (high): Substrate shows 2 verse rows in-span with markers ['c', 'q1', 'q2', 'v', 'w']..
- T411-CLAIM-112 (medium): Feature flags in-span include ['genre_psalms', 'has_poetry_or_liturgy_marker', 'has_strong_h']; meta.
- T411-CLAIM-113 (low): Queue theological pressure (liturgical_use_not_authorized) requires escalation before authority-adja.

## Premortem Red-Team Pass

1. Failure mode: theology pressure smuggled as boundary evidence. Fix: keep pressure in escalation note only.
2. Failure mode: draft treated as owner docket. Fix: require `APPROVE_STANDING_ESCALATION_POLICY` or explicit docket.
3. Failure mode: child spans created inside parent unit. Fix: parent-only remains unauthorized for children.

Theology pressure (T411-CLAIM-113) is non-boundary; see escalation packet.

No reviewed gold is promoted.
