---
object_type: roadmap_task_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-18 during T358 after the maintainer asked to begin whole-Bible research while keeping chunk output work blocked."
reason_for_inclusion: "Explain the non-output-changing Bible-wide research registry and how it prepares later chunking packets without authorizing implementation."
---

# T358 Bible-Wide Chunking Research Registry

Status: complete as non-output-changing research infrastructure.

## Purpose

T358 starts the next safe workstream after T356: Bible-wide research preparation. It does not
select a John 3 option, does not create reviewed gold, and does not implement any chunking
behavior.

The durable artifact is:

```text
.ai/control/bible_wide_chunking_research_registry.yaml
```

The registry gives future agents a canonical 66-book queue with:

- book-level `use_when` routing;
- primary and secondary research lanes;
- representative boundary questions;
- theological downstream risks;
- source-metadata watchpoints;
- future review-packet candidates;
- explicit false authorization flags.

## Why This Is The Right Overnight Work

This work is useful while the owner sleeps because it creates research structure without requiring a
new theological decision. It lets future PRs add narrower packets or inventories in a predictable
place.

It is safer than implementing chunks because:

- Revelation remains research/prep only under `REV-T344-E`.
- John 3 parent-only review target selection is now recorded as `JOHN3-T356-B` after T367.
- Epistle packets remain pending review packets, not reviewed gold.
- Source metadata remains evidence only.
- Whole-Bible orchestration remains implementation-blocked.

## Non-Authorizations

T358 does not authorize:

- raw or canonical data mutation;
- generated chunk regeneration;
- chunk output changes;
- reviewed-gold promotion;
- graph edges;
- retrieval truth;
- embeddings or vector work;
- source metadata authority;
- speaker attribution;
- boundary import;
- Revelation, epistle, WJ, or John 3 implementation;
- T345.

## Suggested Next Research PRs

These can stack after T358 as independent research-only increments:

1. T359: source-metadata research packet atlas covering cross-references, Strong's-style numbers,
   headings, footnotes, WJ markers, and capitalization watchpoints.
2. T360: apocalyptic/prophetic intertext research dossiers for Daniel, Ezekiel, Zechariah, Isaiah,
   and Revelation.
3. T361: Gospel discourse and WJ speaker-boundary research dossiers beyond John 3.
4. T362: epistle argument packet expansion and owner-review queue.

None of those suggested tasks should implement chunks or promote reviewed gold unless a later owner
decision explicitly changes the route.

## Validation

Validator:

```bash
python scripts/validate_bible_wide_chunking_research_registry.py
```

Test:

```bash
python -m pytest -q tests/test_bible_wide_chunking_research_registry.py
```
