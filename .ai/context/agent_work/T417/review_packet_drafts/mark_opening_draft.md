# Mark Mark.1.1-Mark.1.8 Review Packet (Draft)

## Status

- Status: `draft_pending_standing_policy`
- T402 candidate ID: `T402-LC-041`
- Decision: pending
- Parent/child candidate: parent-only proposed
- Proposed parent unit for review: `Mark.1.1-Mark.1.8`
- Implementation allowed: false
- Output change authorized: false
- Reviewed gold promoted: false
- Strengthened packet: false
- Standing policy: `.ai/control/standing_owner_escalation_policy.yaml`
- Standing disposition when active: `proceed_parent_only_with_frontier_note`
- Escalation packet: `.ai/context/agent_work/T411/escalation_packets/T402-LC-041_theology_pressure.md`

This draft lives under `.ai/context/agent_work/T417/` only. It does not authorize output-changing work,
review-packet strengthening, reviewed gold, child spans, or theology authority.

## Review Target

`Mark.1.1-Mark.1.8` — Opening messenger unit is bounded; Isaiah/Malachi intertext and Christology remain evidence only.

## Claim Traceability

- T411-CLAIM-117 (high): Substrate shows 8 verse rows in-span with markers ['f', 'fr', 'ft', 'p', 'q1', 'q2']..
- T411-CLAIM-118 (medium): Feature flags in-span include ['genre_gospels', 'has_crossref', 'has_footnote', 'has_poetry_or_litur.
- T411-CLAIM-119 (low): Queue theological pressure (christology_not_authorized) requires escalation before authority-adjacen.

## Premortem Red-Team Pass

1. Failure mode: theology pressure smuggled as boundary evidence. Fix: keep pressure in escalation note only.
2. Failure mode: draft treated as owner docket. Fix: require `APPROVE_STANDING_ESCALATION_POLICY` or explicit docket.
3. Failure mode: child spans created inside parent unit. Fix: parent-only remains unauthorized for children.

Theology pressure (T411-CLAIM-119) is non-boundary; see escalation packet.

No reviewed gold is promoted.
