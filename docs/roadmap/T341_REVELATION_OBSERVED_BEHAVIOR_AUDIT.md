# T341 Revelation Observed-Behavior Audit

## 1. Status

Status: diagnostic observation only.

No protected output was regenerated. Observed-behavior audit is limited to committed artifacts and
documentation.

This audit does not authorize Revelation implementation, reviewed gold promotion, route behavior,
chunk output changes, evaluator changes, leaderboard or scorecard updates, boundary import, T327G,
boundary/apocryphal material import, or whole-Bible improvement claims.

## 2. Artifacts Inspected

- `data/derived/chunks/variants/claude-opus-4.8__pass2__D_claude_pass2_post_t327__20260608T215149Z/chunks.jsonl`
- `eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md`
- `eval/chunking_gold/stress_atlas/OBSERVED_STRESS_BEHAVIOR.md`
- `eval/chunking_gold/stress_atlas/observed_stress_behavior.json`
- `eval/chunking_gold/stress_atlas/chunking_stress_cases.json`
- `registry/chunking/skill-toc.json`
- `registry/chunking/skill-graph-index.json`
- `config/chunking/book_genres.yaml`
- `config/chunking/form_registry.yaml`
- `docs/roadmap/T336_OPTIMIZED_WHOLE_BIBLE_CHUNKING_ROADMAP.md`
- `docs/roadmap/T340_PSALM_CANDIDATE_PROMOTION_DECISION.md`
- `docs/methodology/UNINTENDED_CONSEQUENCE_REVIEW.md`
- `docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md`

## 3. Current Committed Revelation Chunk Behavior

The committed post-T327 D / Claude pass2 canonical-66 variant contains 15 Revelation chunks. The
records are existing committed generated output; T341 read them but did not modify or regenerate
them.

| Chunk | Span | Genre | Boundary basis |
| ---: | --- | --- | --- |
| 1 | Rev.1.1-Rev.2.7 | apocalypse | english_sentence, usfm_paragraph |
| 2 | Rev.2.8-Rev.3.6 | apocalypse | english_sentence, usfm_paragraph |
| 3 | Rev.3.7-Rev.4.8 | apocalypse | english_sentence, usfm_paragraph |
| 4 | Rev.4.9-Rev.6.8 | apocalypse | english_sentence, usfm_paragraph |
| 5 | Rev.6.9-Rev.8.2 | apocalypse | english_sentence, usfm_paragraph |
| 6 | Rev.8.3-Rev.9.19 | apocalypse | english_sentence, usfm_paragraph |
| 7 | Rev.9.20-Rev.11.13 | apocalypse | english_sentence, usfm_paragraph |
| 8 | Rev.11.14-Rev.13.4 | apocalypse | english_sentence, usfm_paragraph |
| 9 | Rev.13.5-Rev.14.11 | apocalypse | english_sentence, usfm_paragraph |
| 10 | Rev.14.12-Rev.16.9 | apocalypse | english_sentence, usfm_paragraph |
| 11 | Rev.16.10-Rev.18.3 | apocalypse | english_sentence, usfm_paragraph |
| 12 | Rev.18.4-Rev.19.4 | apocalypse | english_sentence, usfm_paragraph |
| 13 | Rev.19.5-Rev.20.6 | apocalypse | english_sentence, usfm_paragraph |
| 14 | Rev.20.7-Rev.21.21 | apocalypse | english_sentence, usfm_paragraph |
| 15 | Rev.21.22-Rev.22.21 | apocalypse | book_boundary |

Observed pattern:

- Revelation is currently chunked as large apocalypse units.
- Current chunks often cross candidate macro-structure boundaries, for example Rev.1 into Rev.2,
  Rev.3 into Rev.4, Rev.11 into Rev.13, Rev.16 into Rev.18, and Rev.20 into Rev.21.
- Boundary basis is mostly `english_sentence` plus `usfm_paragraph`; the final chunk closes on
  `book_boundary`.
- This is observed behavior, not a claim that current output is bad or good.

## 4. Existing Stress-Atlas Evidence

The stress atlas already records `Rev.12-Rev.18` as a proposed apocalyptic vision-cycle case. It is
proposed only and has `implementation_allowed: false`.

The T318 observed-stress behavior record for `rev12_18_vision_cycle` says the case was split across
five chunks and mixed with extra context, with speaker marker evidence present. That audit also
states it was generated from a temporary local pre-T327 wider-corpus chunker run and should be
refreshed before future output-changing work cites current post-T327 behavior.

T341 therefore treats the T318 record as historical diagnostic triage, not current reviewed gold.

## 5. Known Limitations

- T341 did not regenerate chunks, scorecards, route ledgers, or canonical outputs.
- T341 did not run a new observed-behavior generator.
- T341 did not inspect raw Revelation source text beyond existing inventory/control surfaces.
- Existing committed chunks do not by themselves explain whether a split is intended, accidental,
  optimal, or harmful.
- Existing observations do not settle speaker, chronology, recapitulation, Babylon, millennium, or
  symbolic-identity questions.

## 6. Likely Failure Modes

- A large chunk may mix a letter, vision scene, hymn, oracle, or interlude with adjacent material.
- A split may divide a vision cycle without preserving parent unity.
- A boundary may imply chronology or recapitulation without review.
- A boundary may encode speaker or angelic-speech scope without human review.
- A boundary may encode Babylon or millennium interpretation.
- A future global apocalypse rule may affect prophets, Gospels, Daniel, Psalms, or epistles.
- Boundary/apocryphal material may be imported as context if future tasks bypass boundary-routing
  rules.
- A future master chunker may treat Revelation as a shared optimization signal across corpora.

## 7. Non-Authorizing Observations

- Current 15-chunk Revelation behavior is observed only.
- The Rev.12-Rev.18 stress case remains proposed/historical diagnostic evidence.
- No review packet is promoted.
- No reviewed gold exists for Revelation behavior change in this task.
- No route, skill, evaluator, leaderboard, scorecard, or generated-output behavior changed.

## 8. Candidate Review-Packet Targets

Recommended T342 candidates:

1. Rev.12-Rev.14: symbolic scenes, speaker shifts, and cycle/interlude risk.
2. Rev.17-Rev.18: Babylon scenes and laments without identity assumptions.
3. Rev.21-Rev.22: new creation and epilogue.
4. Rev.2-Rev.3: seven letters as a bounded parent/child candidate.
5. Rev.4-Rev.5: throne-room vision and hymnic material.

## 9. What Future T342 Should Review

T342 should select exactly one candidate and create a pending review packet. It should include:

- exact proposed scope;
- current committed chunk behavior;
- candidate parent and child spans if applicable;
- interpretive risks;
- required executable checks;
- non-target identity requirements;
- a human review decision box;
- `implementation_allowed: false`;
- `output_change_authorized: false`;
- `reviewed_gold_promoted: false`.

T342 should not implement Revelation chunking.
