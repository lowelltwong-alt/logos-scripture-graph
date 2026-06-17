# T342 Revelation Review-Packet Candidate Selection

## 1. Status

Selection/control-plane only.

T342 selects exactly one Revelation review-packet target for the next task. It does not create a
review packet, promote reviewed gold, implement Revelation chunking, create a Revelation route,
regenerate chunks, alter evaluator policy, import boundary material, or authorize output-changing
work.

T342 does not create a review packet. T343 owns packet creation.

## 2. Decision

Selected target:

```text
Rev.12-Rev.14
```

Machine target id:

```text
rev12_14_symbolic_scenes
```

Exact selected scope for T343 packet creation:

```text
Rev.12.1-Rev.14.20
```

T343 should create a pending, non-authorizing review packet for this exact selected target.

## 3. Why This Target

T341 ranked `Rev.12-Rev.14` first because it concentrates several Revelation-specific risks while
remaining narrow enough for one review packet:

- woman / dragon / male child symbolic scene;
- heavenly conflict imagery;
- beast imagery and worship/mark material;
- Lamb / 144,000 scene;
- angelic proclamations;
- harvest / judgment imagery;
- speaker and voice shifts;
- possible cycle/interlude questions.

The target is strong because it makes Revelation risks visible without forcing a full-book
interpretive model.

## 4. Candidate Review

| Candidate | T341 priority | T342 result | Reason |
| --- | ---: | --- | --- |
| `Rev.12-Rev.14` | 1 | selected | Highest concentration of symbolic scenes, speaker shifts, and cycle/interlude risk while still narrow enough for one packet. |
| `Rev.17-Rev.18` | 2 | not selected | Babylon scenes and laments remain important, but identity-assumption risk is better handled after the first Revelation packet pattern exists. |
| `Rev.21-Rev.22` | 3 | not selected | New creation and epilogue are high-value, but less central to first testing symbolic-cycle risk. |
| `Rev.2-Rev.3` | 4 | not selected | Seven letters are bounded and useful, but lower-risk than the symbolic middle section. |
| `Rev.4-Rev.5` | 5 | not selected | Throne-room vision and hymns remain future candidates after the first selected target. |

## 5. T343 Gate

T343 should create the actual review packet and gold-candidate surfaces. T343 must keep:

- `implementation_allowed: false`;
- `output_change_authorized: false`;
- `reviewed_gold_promoted: false`.

T343 may record proposed parent/child options, current committed chunk behavior, marker evidence,
speaker/symbolic risks, and review questions. T343 must not resolve the review question or promote
gold by itself.

## 6. Non-Authorizations

T342 does not authorize:

- Revelation implementation;
- output-changing Revelation chunking;
- reviewed-gold promotion;
- a Revelation route or route behavior;
- global apocalypse, prophecy, discourse, chronology, interlude, symbolic-identity, Babylon, or
  millennium rules;
- boundary/apocalyptic material import;
- boundary/apocryphal material import;
- source acquisition;
- raw or canonical data mutation;
- generated chunk regeneration;
- evaluator formula changes;
- leaderboard or scorecard changes;
- skill lifecycle promotion;
- whole-Bible improvement claims;
- T327G;
- embedding runs;
- vector index builds;
- graph-edge generation;
- Psalm candidate promotion.

## 7. Required T343 Packet Contents

The T343 review packet should include:

- target id `rev12_14_symbolic_scenes`;
- exact scope `Rev.12.1-Rev.14.20`;
- current committed Revelation chunk behavior touching the selected scope;
- candidate parent unit and child span options, if any;
- explicit non-authorization flags;
- symbolic-identity risk notes;
- speaker/voice-shift risk notes;
- chronology/recapitulation/interlude risk notes;
- boundary-import prohibition;
- required future executable checks if the owner later promotes exact reviewed gold;
- human review decision box with all authorization fields initially false.

## 8. RISK-GATE-001 Map

Required question:

```text
What could this change accidentally authorize, weaken, contaminate, overfit, globalize, or make harder to reverse?
```

### Confirmed Risks

- Selecting `Rev.12-Rev.14` could be misread as approving boundaries for that section.
- Advancing the readiness map to T343 could be misread as implementation momentum.

### Plausible Risks

- Symbolic scene labels could be read as symbolic-identity claims.
- Cycle/interlude language could imply chronology or recapitulation.
- Revelation-specific observations could leak into prophets, Gospel discourse, Daniel, Psalms, or
  the monolith fallback.

### Unlikely But High-Impact Risks

- Boundary/apocalyptic or boundary/apocryphal material could be imported as supposed review context.
- A future global apocalypse rule could optimize Revelation at the expense of simpler canonical
  books.

### Watch-Later Conditions

- Any PR that edits chunker, orchestrator, evaluator, leaderboard, generated chunks, route registry,
  or skill lifecycle while claiming to be T342/T343.
- Any PR that sets `implementation_allowed: true` or `output_change_authorized: true` before owner
  review.
- Any PR that imports noncanonical apocalyptic or boundary material into this repo.

### Tests Or Guards Needed

- T342 tests should lock the selected target and non-authorizing status.
- T343 tests should assert pending packet status and false authorization flags.
- Any future implementation task must prove reviewed gold exists and non-target identity is
  preserved.

### Owner Decisions Needed

- Owner must decide exact reviewed spans in a later task before any Revelation implementation.
- Owner must decide whether speaker/voice boundaries require a separate review standard before
  reviewed gold promotion.

## 9. Discoverability Note

T342 also adds a local AI roadmap table of contents because T337A was harder to find than it should
have been. Future agents should use:

```text
docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md
```

before guessing roadmap or review-packet filenames.
