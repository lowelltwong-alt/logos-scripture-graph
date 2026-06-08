# T327B.1 Canonical Scope Validator Fail-Closed

## Status

- Task: T327B.1
- Mode: build
- Status: complete
- Branch: `t327b1-canonical-scope-validator-fail-closed`
- Data mutation: none
- Output regeneration: none
- T327C/D/E/F/G: not started

## Summary

T327B.1 hardens canonical 66-scope validation so records in canonical Scripture outputs or canonical
Scripture sidecars cannot pass when no book identity can be resolved.

## Rule

`CANON-SCOPE-VALIDATOR-001 - Canonical scope validation fails closed on unclassified records`

Any record in a canonical Scripture output or canonical Scripture sidecar must either expose a valid
canonical 66-book identity or be explicitly kept outside canonical Scripture outputs as
non-scripture/supporting metadata.

Records with no `book`, `osis_book`, `usfm_book`, `osis_ref`, or `passage_id` identity must not pass
canonical-scope validation.

## Glossary and Front-Matter Boundary

Glossary, front-matter, concordance, and source metadata may be preserved as supporting/reference
artifacts when separately scoped. They must not be treated as canonical Scripture passages,
canonical chunks, canonical witness text, leaderboard inputs, scorecard inputs, or default
Scripture retrieval text.

`GLO` and `FRT` records must not silently pass canonical output validation because they lack book
metadata or because they are supporting/source metadata.

## Non-Protection Boundary

This validator proves canonical-scope classification, not text authenticity. A record falsely
labeled with an allowed book identity, such as `book: Mark`, still requires raw source provenance,
source-manifest checksums, parser determinism, and raw immutability controls to prove that the text
actually derives from the approved source file for Mark.

Fake, substituted, or altered content under an allowed book label is a source-integrity and
provenance failure, not a canonical-scope-filter success. Future hardening may add content
authenticity checks that compare generated records back to approved raw manifests and source hashes.

## Scope

- Updates fail-closed validation behavior.
- Adds synthetic tests for valid canonical, excluded-book, `GLO`, `FRT`, missing-identity, and
  glossary-like records.
- Does not validate existing generated canonical outputs by default until T327C regeneration.
- Does not mutate raw or canonical data.
- Does not regenerate outputs, chunks, scorecards, or leaderboard.
- Does not import or move excluded material.

## Deferred Sequence

- T327C uses the canonical-66 filter and fail-closed validator for regeneration.
- T327D regenerates chunks, scorecards, leaderboard, and score language as corpus-scope correction.
- T327E cleans gold/stress/observed/index surfaces.
- T327F plans boundary repo source intake.
- T327G optionally plans raw source artifact replacement or migration.
