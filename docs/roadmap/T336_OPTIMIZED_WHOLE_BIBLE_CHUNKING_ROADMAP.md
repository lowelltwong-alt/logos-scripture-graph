# T336 Optimized Whole-Bible Chunking Roadmap

## 1. Status

planning/control-plane only

T336 updates roadmap, methodology, and AI-readable control surfaces after the T327 contamination
correction and the post-T327 Psalm guardrail sequence. It does not change chunking behavior,
regenerate outputs, change evaluator policy, import source texts, create boundary corpus records, or
start T327G.

## 2. Why This Update Exists

This update exists after:

- T327 corrected the canonical corpus scope to the owner-approved 66-book Bible.
- T331 reset the post-T327 chunking backlog around the canonical-66 baseline.
- T332 selected Psalms / poetry stanza behavior as the next narrow implementation lane.
- T333 added a safe behavior-preserving Psalm candidate-skill guardrail.
- T334 confirmed the Psalm guardrail caused no output/default behavior change or score movement.
- T335 expanded Psalm stress/gold coverage with pending, non-authorizing review packets.

The repo now needs a clear AI-readable roadmap so future agents preserve the Bible-first priority,
understand why Psalms are the current implementation lane, and do not confuse future Revelation,
boundary, or master-chunker work with current authorized implementation.

## 3. Primary Objective

The highest priority is a highly reliable, near-perfect / perfectly governed chunker for the
canonical 66-book Bible.

All future chunker adaptations for boundary literature, noncanonical corpora, legal documents,
commentary/reception corpora, or a future master chunker are subordinate to that goal.

If adapting the chunker for noncanonical or boundary material would degrade canonical Bible
chunking quality, the project should fork, split, or rebuild a separate chunker or harness for that
material rather than compromising the Bible chunker.

## 4. Non-Negotiable Boundaries

- No boundary import.
- No T327G.
- No noncanonical influence on canonical chunking.
- No global heuristic leakage.
- No score movement claims without same-baseline evidence.
- No raw/canonical data mutation.
- No generated output regeneration.
- No chunk regeneration.
- No evaluator formula change.
- No leaderboard or scorecard update.
- No chunker/orchestrator behavior change.
- No Revelation implementation until reviewed gold exists.
- No future master-chunker design may collapse corpora into one authority layer.

The T327 incident showed that raw source scope must not become canonical output scope. Boundary and
noncanonical material may be studied, referenced, compared, or chunked in a separate boundary
context later, but it must not become canonical Scripture authority, default Scripture retrieval, or
canonical chunking evidence.

## 5. Why Psalms First

Psalms are the current implementation lane because the repo already has the strongest local safety
infrastructure there:

- reviewed Psalm gold already exists;
- Psalm 78 has a reviewed parent/child structural split;
- Psalms 105 and 106 have reviewed current whole-psalm preservation;
- Psalm 119 provides a strong sectioning precedent;
- Psalm stress cases and observed behavior surfaces already exist;
- T333/T334 established a candidate Psalm skill seam that fails closed on reviewed-gold drift;
- T335 added additional pending Psalm review packets without authorizing output changes.

This does not mean Psalms are harder than Revelation. It means Psalms are the safest first
post-T327 implementation loop because evidence, guardrails, and review surfaces are already in
place.

## 6. Why Revelation Is Likely Hardest

Revelation is likely one of the hardest books because it combines:

- epistolary frame;
- prophetic oracle;
- apocalyptic vision;
- hymns;
- judgment cycles;
- interludes;
- angelic speeches;
- symbolic scenes;
- OT allusion-heavy blocks.

Chunking Revelation can accidentally encode chronology vs recapitulation, preterist/futurist/
idealist/historicist framing, symbolic identities, millennium interpretation, Babylon identity, and
cycle boundaries.

Therefore Revelation should receive an early hard-book stress atlas and review-packet lane, but no
output-changing Revelation implementation should begin until reviewed gold exists.

## 7. Implementation Order

Recommended implementation order:

1. Psalms / poetry stanza lane.
2. Epistle argument/paragraph lane.
3. Narrative/pericope lane.
4. Wisdom/dialogue lane.
5. Prophetic oracle lane.
6. Gospel discourse / words-of-Jesus lane.
7. Revelation / apocalypse lane.
8. Bible-wide orchestration/promotion pass.

Implementation should teach safe reusable primitives first, then harder interpretive books later.
Each lane needs reviewed gold and fail-closed validation before output-changing behavior.

## 8. Hard-Book Atlas Order

The atlas/review lane can run ahead of implementation.

Recommended hard-book atlas order:

1. Revelation hard-book atlas.
2. Prophets atlas.
3. Gospel discourse/WJ atlas.
4. Job/Song/Wisdom atlas.
5. Daniel/apocalyptic-prophetic bridge atlas.

Revelation is early in the atlas queue because it is high-risk and needs evidence before
implementation. It is late in the implementation queue because reviewed gold and interpretation
guardrails must come first.

## 9. Router/Orchestrator Skill-Isolation Model

The chunker should evolve by teaching reusable structural primitives and keeping them behind a
router/orchestrator.

Bad pattern:

```text
global heuristic pile
-> Revelation rules leak into Psalms
-> Psalm marker rules leak into prophets
-> WJ/speaker assumptions leak into Revelation
-> generic rules degrade simple books
```

Good pattern:

```text
book/form classifier
-> route ledger
-> skill selection
-> skill-specific policy
-> reviewed gold / validator gates
-> fail closed if evidence is insufficient
```

Conceptual route model only, not runtime config:

```yaml
routes:
  psalm_poetry:
    applies_to:
      - Psalms
    skills:
      - whole_psalm_preservation
      - reviewed_parent_child_sections
      - selah_evidence_only
      - superscription_attachment
    forbidden:
      - automatic_selah_split
      - non_66_canonical_controls

  epistle_argument:
    applies_to:
      - Romans
      - 1Cor
      - 2Cor
      - Gal
      - Eph
      - Phil
      - Col
      - 1Thess
      - 2Thess
      - 1Tim
      - 2Tim
      - Titus
      - Phlm
      - Heb
      - Jas
      - 1Pet
      - 2Pet
      - 1John
      - 2John
      - 3John
      - Jude
    skills:
      - opening_body_closing
      - argument_paragraphs
      - doxology_blocks
    forbidden:
      - apocalyptic_cycle_assumptions

  revelation_apocalyptic:
    applies_to:
      - Rev
    skills:
      - epistle_frame
      - vision_scene
      - hymn_block
      - judgment_cycle
      - interlude
      - angelic_speech
      - symbolic_scene
    forbidden:
      - default_chronology_theology
      - default_recapitulation_theology
      - millennium_interpretation
      - babylon_identity_claim
      - global_application_to_non_revelation_books
```

Book-specific or genre-specific skills must be activated only where appropriate. Revelation-specific
assumptions must not leak into Psalms, prophecy, Gospel discourse, epistles, or the monolith
fallback.

## 10. Future Master Chunker Boundary

A future master chunker may eventually coordinate multiple chunking harnesses:

- canonical Bible chunker;
- boundary/noncanonical literature chunker;
- legal-document chunker;
- commentary/reception chunker.

The master chunker must be an orchestrator/harness, not a reason to collapse all corpora into one
authority layer. The canonical Bible chunker remains the highest-priority substrate.

A master chunker must not create a single shared global optimization objective across Bible and
non-Bible corpora. Non-Bible training/eval cases must not tune canonical Bible behavior. It must
isolate corpora, routes, skills, objectives, eval sets, default retrieval policy, and
authority/trust profiles.

If boundary or noncanonical adaptation interferes with canonical Bible quality, split or rebuild a
separate chunker or harness rather than degrading Bible chunking.

## 11. Next Task Sequence

T336 records the optimized roadmap. The next intended sequence is:

1. T337 - Select One Psalm Behavior Change.
2. T338 - Implement One Psalm Behavior Change.
3. T339 - Evaluate Same-Baseline Psalm Improvement.
4. T340 - Promote/Reject Psalm Candidate Skill.
5. T341 - Revelation Hard-Book Stress Atlas.
6. T342 - Revelation Observed Behavior Audit.
7. T343 - Revelation Review Packets / Gold Candidates.
8. T344 - Select One Revelation Behavior Target.
9. T345 - Implement One Revelation Behavior Only If Reviewed Gold Exists.
10. T346 - Revelation Same-Baseline Evaluation.
11. T347 - Select Next Genre Lane.

T337-T340 remain the Psalm implementation lane. T341-T343 are Revelation atlas/review only.
Revelation implementation waits until reviewed gold exists. T327G and boundary import remain
deferred unless separately authorized.

## 12. Validation And Review Rules

- Reviewed gold is required before output-changing work.
- Non-target identity must be protected before output-changing work.
- Same-baseline evaluation is required before improvement claims.
- Score movement is not a chunking improvement unless same-baseline target output evidence supports
  that claim.
- Claude Opus high/max review is recommended when a task changes reviewed-gold meaning, introduces
  high-risk interpretive boundaries, or prepares Revelation implementation.
- Marker evidence is not authority.
- Route-specific metadata must stay in ledgers/sidecars unless schema-approved.
- Boundary/noncanonical material remains subordinate/non-superior and outside canonical chunking.

## 13. Not Started

- T327G.
- Boundary import.
- Revelation implementation.
- Master chunker repo creation.
- Canonical output regeneration.
- Chunk regeneration.
- Evaluator formula change.
- Leaderboard or scorecard update.
