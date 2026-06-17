# T350 Bible-Wide Chunking Readiness Plan

## 1. Status

Planning/control-plane only.

T350 answers the owner's current operating question: the project should keep the whole canonical
66-book Bible as the destination, but the faithful route is one reviewed lane at a time. This task
does not change chunking behavior, regenerate outputs, promote reviewed gold, update evaluator
policy, promote a skill, import boundary material, run embeddings, build indexes, generate graph
edges, or start Revelation implementation.

The machine-readable readiness surface is:

```text
.ai/control/bible_chunking_readiness_map.yaml
```

It is guarded by:

```text
scripts/validate_bible_chunking_readiness_map.py
tests/test_bible_chunking_readiness_map.py
```

## 2. Direct Answer

Yes, the repo is storing lessons learned. The durable surfaces are:

- `.ai/control/chunking_theological_decision_register.yaml`
- `docs/methodology/WORKFLOW_LESSONS.md`
- `docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `docs/methodology/UNINTENDED_CONSEQUENCE_REVIEW.md`
- `eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md`

Those surfaces now have two jobs:

- preserve reusable workflow lessons so agents do not rely on memory;
- preserve theological-downstream chunking decisions so future readers can see where a boundary,
  route, gold, evaluator, or default behavior decision might carry interpretive weight.

## 3. Faithful Route

Whole-Bible chunking is the objective, but a whole-Bible output-changing pass is not the next
faithful move.

The faithful route is:

```text
BIBLE-WIDE GOAL
  -> one reviewed lane
  -> exact target selection
  -> pending review packet
  -> owner decision
  -> executable reviewed gold
  -> route-isolated implementation
  -> same-baseline evaluation
  -> promotion/hold decision
  -> next lane
```

This is slower than one global algorithm pass, but it protects the text. The Bible contains genres
where chunk boundaries can accidentally imply theology, textual criticism, source/tradition scope,
speaker attribution, chronology, or canon status. A global heuristic would hide those decisions
inside software behavior.

## 4. Current Algorithm Readiness

| Surface | Status | Safe use now |
| --- | --- | --- |
| Monolith fallback | Baseline active | Current deterministic fallback only |
| Form detector | Candidate metadata only | Review/planning, not authority |
| Orchestrator | Byte-identical shim | Route ledger and isolation surface |
| Psalm candidate skill | Candidate hold | Exact Psalm 89 route-isolated behavior exists, but skill is not promoted |
| Revelation skill | Not implemented | Blocked until exact reviewed gold exists |
| Bible-wide orchestration | Blocked | Wait for multiple lane-level promotion/rejection cycles |

No new algorithm work is ready to start until the next review lane creates reviewed evidence.

## 5. Lane Readiness

Recommended implementation order remains:

1. Psalms / poetry stanza lane.
2. Epistle argument / paragraph lane.
3. Narrative / pericope lane.
4. Wisdom / dialogue lane.
5. Prophetic oracle lane.
6. Gospel discourse / words-of-Jesus lane.
7. Revelation / apocalypse lane.
8. Bible-wide orchestration / promotion pass.

Recommended review order remains different from implementation order:

1. Revelation review lane next.
2. Prophets atlas/review.
3. Gospel discourse/WJ atlas/review.
4. Job/Song/Wisdom atlas/review.
5. Daniel/apocalyptic-prophetic bridge review.

This is intentional. Revelation is high-risk, so evidence should be gathered early. Revelation is
late for implementation because its exact gold and route isolation must mature before output
changes.

## 6. Next Concrete Task

Proceed to T342 only:

```text
T342 - Revelation Review-Packet Candidate Selection
```

Recommended candidate:

```text
Rev.12-Rev.14
```

Why: T341 ranks this first because it concentrates symbolic scenes, speaker shifts, and
cycle/interlude risk while still being narrow enough for one review packet.

T342 should select exactly one Revelation review target and create a pending, non-authorizing
selection record. It must not implement Revelation behavior.

## 7. Required T342 Guardrails

T342 must keep:

- `implementation_allowed: false`
- `output_change_authorized: false`
- `reviewed_gold_promoted: false`
- Revelation route behavior unchanged
- chunk output unchanged
- evaluator policy unchanged
- raw and canonical data unchanged
- boundary/apocalyptic material outside this repo

If T342 touches `docs/roadmap/` or review/gold surfaces, it must update the chunking theological
decision register when the changed-path gate applies.

## 8. Unintended Consequence Review

RISK-GATE-001 question:

```text
What could this change accidentally authorize, weaken, contaminate, overfit, globalize, or make harder to reverse?
```

Confirmed risks:

- `current_focus.yaml` and project status were still pointing at T349 after the register merge.
- A Bible-wide readiness conversation could be misread as permission for immediate whole-Bible
  regeneration or global algorithm work.

Plausible risks:

- The phrase "get all the algos ready" could push future agents toward implementation before
  reviewed gold exists.
- Revelation review work could be mistaken for Revelation implementation authorization.
- A future master chunker could collapse Bible, boundary, commentary, legal, or noncanonical
  objectives into one optimization target.

Unlikely but high-impact risks:

- A whole-Bible pass could encode theological assumptions through boundaries before humans see the
  decisions.
- Boundary or apocalyptic literature could be imported as context authority through a review lane.

Tests or guards needed:

- Validate the readiness map as non-authorizing.
- Keep T342 as review-selection only.
- Keep the theological decision register current for roadmap/gold/route decisions.

Owner decisions needed:

- Owner must still select exact reviewed gold before any Revelation implementation.
- Owner must still decide any future skill lifecycle promotion.

## 9. Non-Authorizations

T350 does not authorize:

- raw or canonical mutation;
- generated chunk regeneration;
- chunk output change;
- evaluator formula change;
- leaderboard or scorecard update;
- Revelation implementation;
- global apocalypse, Psalm, poetry, WJ, or prophecy rule;
- reviewed-gold promotion;
- skill lifecycle promotion;
- embedding run;
- vector index build;
- graph edge generation;
- boundary import;
- T327G;
- master chunker global objective.

## 10. Bottom Line

The project is now pointed correctly:

```text
whole Bible as destination
one reviewed lane at a time as method
lessons and theological decisions stored in deterministic registers
T342 Revelation review selection next
```
