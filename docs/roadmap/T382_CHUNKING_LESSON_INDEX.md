---
object_type: roadmap_governance_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-20 during T382 after the maintainer asked for lessons learned to be saved into the appropriate preflight and exposed through a tagged lesson table-of-contents/graph."
reason_for_inclusion: "Give future chunking and audit agents a human-readable entry point for the new machine-readable lesson index."
---

# T382 Chunking Lesson Index

T382 adds `.ai/control/chunking_lesson_index.yaml` as a first-class lesson discovery surface.

The index records reusable lessons with:

- categories
- searchable tags
- use-when triggers
- related tasks
- related decision-register entries
- related workflow lessons
- required preflight surfaces
- downstream risks
- explicit non-authorizations
- validators
- graph edges to related lessons

This is a routing and memory layer. It does not authorize chunk output, reviewed-gold promotion,
route behavior, evaluator changes, graph edges, retrieval truth, vector/embedding work, boundary
import, or theological claims.

The index is now mandatory chunking-agent preflight reading. It is also a required midflight lesson
capture surface. If a task teaches a reusable lesson, future agents must update the appropriate
preflight/workflow/register surface and update the lesson index, or record in the handoff why no
durable lesson surface changed.

The validator is `scripts/validate_chunking_lesson_index.py`. It checks the index structure,
non-authorizations, related lesson/decision links, mandatory preflight integration, and changed-path
simulation for lesson/preflight/methodology/register/audit/TOC surfaces.

T382 leaves T376 as the next human decision gate.
