# Titus Titus.1.1-Titus.1.4 Review Packet (Draft)

## Status

- Status: `draft_pending_standing_policy`
- T402 candidate ID: `T402-LC-056`
- Decision: pending
- Parent/child candidate: parent-only proposed
- Proposed parent unit for review: `Titus.1.1-Titus.1.4`
- Implementation allowed: false
- Output change authorized: false
- Reviewed gold promoted: false
- Strengthened packet: false
- Standing policy: `.ai/control/standing_owner_escalation_policy.yaml`
- Standing disposition when active: `proceed_parent_only_with_frontier_note`
- Escalation packet: `.ai/context/agent_work/T411/escalation_packets/T402-LC-056_theology_pressure.md`

This draft lives under `.ai/context/agent_work/T417/` only. It does not authorize output-changing work,
review-packet strengthening, reviewed gold, child spans, or theology authority.

## Review Target

`Titus.1.1-Titus.1.4` — Opening greeting is bounded, but elder/office context later in the book remains non-authorizing.

## Claim Traceability

- T411-CLAIM-054 (high): Substrate shows 4 verse rows in-span with markers ['f', 'fr', 'ft', 'p', 'v', 'w']..
- T411-CLAIM-055 (medium): Feature flags in-span include ['genre_epistles', 'has_footnote', 'has_strong_g']; metadata evidence-.
- T411-CLAIM-056 (low): Queue theological pressure (church_office_theology_not_authorized) requires escalation before author.

## Premortem Red-Team Pass

1. Failure mode: theology pressure smuggled as boundary evidence. Fix: keep pressure in escalation note only.
2. Failure mode: draft treated as owner docket. Fix: require `APPROVE_STANDING_ESCALATION_POLICY` or explicit docket.
3. Failure mode: child spans created inside parent unit. Fix: parent-only remains unauthorized for children.

Theology pressure (T411-CLAIM-056) is non-boundary; see escalation packet.

No reviewed gold is promoted.
