# Exod Exod.35.4-Exod.35.29 Review Packet (Draft)

## Status

- Status: `draft_pending_standing_policy`
- T402 candidate ID: `T402-LC-002`
- Decision: pending
- Parent/child candidate: parent-only proposed
- Proposed parent unit for review: `Exod.35.4-Exod.35.29`
- Implementation allowed: false
- Output change authorized: false
- Reviewed gold promoted: false
- Strengthened packet: false
- Standing policy: `.ai/control/standing_owner_escalation_policy.yaml`
- Standing disposition when active: `proceed_parent_only_with_frontier_note`
- Escalation packet: `.ai/context/agent_work/T411/escalation_packets/T402-LC-002_theology_pressure.md`

This draft lives under `.ai/context/agent_work/T417/` only. It does not authorize output-changing work,
review-packet strengthening, reviewed gold, child spans, or theology authority.

## Review Target

`Exod.35.4-Exod.35.29` — Offering instructions form a bounded list; tabernacle theology and typology remain non-authorizing.

## Claim Traceability

- T411-CLAIM-072 (high): Substrate shows 26 verse rows in-span with markers ['p', 'v', 'w']..
- T411-CLAIM-073 (medium): Feature flags in-span include ['genre_narrative', 'has_strong_h']; metadata evidence-only..
- T411-CLAIM-074 (low): Queue theological pressure (typology_not_authorized) requires escalation before authority-adjacent p.

## Premortem Red-Team Pass

1. Failure mode: theology pressure smuggled as boundary evidence. Fix: keep pressure in escalation note only.
2. Failure mode: draft treated as owner docket. Fix: require `APPROVE_STANDING_ESCALATION_POLICY` or explicit docket.
3. Failure mode: child spans created inside parent unit. Fix: parent-only remains unauthorized for children.

Theology pressure (T411-CLAIM-074) is non-boundary; see escalation packet.

No reviewed gold is promoted.
