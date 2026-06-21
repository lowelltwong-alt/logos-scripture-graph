---
object_type: roadmap_governance_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-21 during T383 after the maintainer asked how to encode that context always matters when reading the Bible."
reason_for_inclusion: "Give future chunking and review agents a human-readable entry point for the contextual reading policy."
---

# T383 Contextual Reading Policy

T383 adds `.ai/control/contextual_reading_policy.yaml` as a first-class non-output-changing
preflight policy.

The policy requires future chunking and review work to account for context in layers:

- immediate previous/following discourse or narrative context
- paragraph, section, stanza, speech, oracle, or marker context
- chapter and book argument or narrative flow
- canonical context, including quotations, allusions, cross-references, typology, and repeated phrases
- original-language phrase/clause/syntax/discourse context when Greek/Hebrew evidence is used
- historical and cultural background when it helps the text be read in context
- source metadata context when headings, cross-references, WJ/red-letter markers, capitalization,
  Strong's-style numbers, footnotes, or formatting are used

This is a discipline for faithful reading and review. It does not authorize chunk output, reviewed
gold, route behavior, evaluator changes, graph edges, retrieval truth, vector/embedding work,
boundary import, doctrine, or historical background as Scripture authority.

T383 does not create a separate history repo. A later historical-background sidecar may be proposed
only as lower-trust evidence and would require owner authorization, a cross-repo governance
contract, trust-zone policy, anti-smuggling validation, and explicit denial of chunk/retrieval/graph
authority.

At T383 creation, T376 owner lane selection was the next human decision gate. T376 later selected
the epistle argument research/prep runway, and the active next route is T384 epistle argument
research/options matrix work.
