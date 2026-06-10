# T341 Revelation Hard-Book Atlas

## 1. Purpose

T341 creates a Revelation hard-book atlas as evidence, planning, and control-plane work only. It
maps why Revelation is high-risk for chunking, records current committed observations where they can
be inspected without regeneration, and names future review-packet candidates.

T341 does not implement Revelation chunking behavior, create a Revelation route, promote reviewed
gold, change chunk output, or authorize a global apocalypse rule.

## 2. Why Revelation Is Hard

Revelation combines an epistolary frame, prophetic oracle, apocalyptic vision, hymns, judgment
cycles, interludes, angelic speeches, symbolic scenes, and dense Old Testament allusion. A boundary
choice can imply more than retrieval convenience.

Chunking Revelation can accidentally encode:

- chronology versus recapitulation;
- interlude recognition;
- symbolic identity;
- repeated sevenfold cycle boundaries;
- hymns inside visions;
- angelic speech scope;
- speaker shifts;
- Old Testament allusion density;
- letter, vision, oracle, and discourse structure;
- preterist, futurist, idealist, or historicist assumptions;
- Babylon identity assumptions;
- millennium interpretation assumptions;
- boundary or apocalyptic literature as contextual authority.
- boundary/apocryphal material as contextual authority.

## 3. Canonical Scope

The scope is the canonical 66-book Revelation text already present in the Scripture graph. T341 does
not import, normalize, quote, or depend on boundary/apocalyptic literature outside the canonical
66-book corpus. It also does not import boundary/apocryphal material.

Reference scope:

- book: `Rev`
- canonical book: Revelation
- current genre label: `apocalypse`
- current route/skill status: declared gap handled by monolith fallback surfaces

## 4. What T341 Does Not Authorize

T341 does not authorize:

- Revelation implementation;
- output-changing Revelation chunking;
- a Revelation route or route behavior;
- reviewed gold promotion;
- boundary import;
- boundary/apocryphal material import;
- boundary corpus records;
- source acquisition;
- raw or canonical data mutation;
- chunk regeneration;
- evaluator formula changes;
- leaderboard or scorecard changes;
- skill lifecycle promotion;
- T327G;
- whole-Bible improvement claims;
- global apocalypse, prophecy, poetry, words-of-Jesus, discourse, chronology, interlude, doxology,
  or marker rules.

## 5. Revelation Macro-Structure Candidates

These are review candidates, not approved expected output:

| Area | Candidate scope | Review question |
| --- | --- | --- |
| Prologue / commission / initial vision | Rev.1 | Should the prologue, epistolary greeting, Patmos commission, and first vision be parent/child units? |
| Seven letters | Rev.2-Rev.3 | Should each letter be reviewed as its own child under a seven-letter parent unit? |
| Throne-room vision and hymns | Rev.4-Rev.5 | How should vision scene, throne imagery, scroll scene, and hymns relate? |
| Seals and interlude | Rev.6-Rev.8 | How should the seal cycle and interlude be represented without assuming a chronology model? |
| Trumpets and interlude | Rev.8-Rev.11 | How should trumpets, woes, interlude, and worship material be separated or nested? |
| Woman, dragon, beast, lamb, harvest | Rev.12-Rev.14 | How should linked symbolic scenes be chunked without deciding symbolic identities? |
| Bowls | Rev.15-Rev.16 | How should preparatory vision, bowls, interjection, and Armageddon language be reviewed? |
| Babylon | Rev.17-Rev.18 | How should Babylon scenes and laments be represented without identity assumptions? |
| Victory, millennium, judgment | Rev.19-Rev.20 | How should victory, millennium, final conflict, and judgment be reviewed without eschatology assumptions? |
| New creation / epilogue | Rev.21-Rev.22 | How should new creation, city vision, river/tree imagery, and epilogue warnings be reviewed? |

## 6. Hard Chunking Problems

- Chronology and recapitulation must remain review questions, not default assumptions.
- Interludes may need parent/child modeling, but interlude labels are not automatic boundary
  authority.
- Symbolic identities must not be encoded by chunk boundaries.
- Repeated sevenfold cycles need cycle-aware review before implementation.
- Hymns inside visions may need child chunks without losing the parent vision scene.
- Angelic speeches need speaker-scope review.
- Speaker shifts and voice changes must not be inferred solely from punctuation or marker evidence.
- Old Testament allusion density may require future context packets, but allusion density is not a
  chunk boundary by itself.
- Letter, vision, and oracle forms may overlap; a single book-level genre label is too coarse.
- Boundary/apocalyptic literature may not be imported as context for canonical Revelation chunking.
- The final canonical text must be preserved without importing boundary/apocryphal material.

## 7. Current Observed Behavior

Committed current-output inspection was limited to existing artifacts. No protected output was
regenerated.

The committed post-T327 D / Claude pass2 canonical-66 chunk variant at
`data/derived/chunks/variants/claude-opus-4.8__pass2__D_claude_pass2_post_t327__20260608T215149Z/chunks.jsonl`
contains 15 Revelation chunks:

| Current span | Current genre | Boundary basis |
| --- | --- | --- |
| Rev.1.1-Rev.2.7 | apocalypse | english_sentence, usfm_paragraph |
| Rev.2.8-Rev.3.6 | apocalypse | english_sentence, usfm_paragraph |
| Rev.3.7-Rev.4.8 | apocalypse | english_sentence, usfm_paragraph |
| Rev.4.9-Rev.6.8 | apocalypse | english_sentence, usfm_paragraph |
| Rev.6.9-Rev.8.2 | apocalypse | english_sentence, usfm_paragraph |
| Rev.8.3-Rev.9.19 | apocalypse | english_sentence, usfm_paragraph |
| Rev.9.20-Rev.11.13 | apocalypse | english_sentence, usfm_paragraph |
| Rev.11.14-Rev.13.4 | apocalypse | english_sentence, usfm_paragraph |
| Rev.13.5-Rev.14.11 | apocalypse | english_sentence, usfm_paragraph |
| Rev.14.12-Rev.16.9 | apocalypse | english_sentence, usfm_paragraph |
| Rev.16.10-Rev.18.3 | apocalypse | english_sentence, usfm_paragraph |
| Rev.18.4-Rev.19.4 | apocalypse | english_sentence, usfm_paragraph |
| Rev.19.5-Rev.20.6 | apocalypse | english_sentence, usfm_paragraph |
| Rev.20.7-Rev.21.21 | apocalypse | english_sentence, usfm_paragraph |
| Rev.21.22-Rev.22.21 | apocalypse | book_boundary |

The earlier T318 observed-stress audit includes `rev12_18_vision_cycle`, but it states that its
observations came from a temporary local pre-T327 wider-corpus chunker run. Treat that record as
historical diagnostic triage, not current post-T327 implementation evidence.

## 8. Risk Map

RISK-GATE-001 question: What could this change accidentally authorize, weaken, contaminate, overfit,
globalize, or make harder to reverse?

### Confirmed Risks

- T341 names possible Revelation structures. Without explicit language, those structures could be
  misread as approved boundaries.
- Existing committed output can be read, but reading it does not make it reviewed gold.

### Plausible Risks

- Revelation atlas language could be misread as implementation authorization.
- Revelation/apocalypse structures could become global rules for prophets, Gospels, epistles,
  Psalms, Daniel, or the monolith fallback.
- Interpretive traditions could be encoded accidentally through labels such as interlude,
  recapitulation, Babylon, or millennium.
- Words-of-Jesus and speaker evidence could leak from Gospel discourse rules into Revelation or
  vice versa.
- A future master chunker could use Revelation as a shared cross-corpus optimization signal.

### Unlikely But High-Impact Risks

- Boundary/apocalyptic literature or boundary/apocryphal material could be imported as context and
  contaminate canonical authority.
- A future agent could cite Revelation difficulty to justify weakening Bible-first chunking
  priority.
- A future implementation could optimize Revelation at the expense of simpler books through a global
  heuristic pile.

### Watch-Later Conditions

- Any PR that edits Revelation chunker, route, skill, registry, evaluator, leaderboard, or generated
  output files.
- Any PR that treats `apocalyptic_cycle` as approved or active without reviewed gold.
- Any PR that cites T341 as evidence of output improvement.
- Any PR that imports noncanonical apocalyptic material into this repo.

### Tests Or Guards Needed

- Keep T341 tests focused on non-authorization and required reviewed gold.
- Future T342 review-packet tests should assert pending status until human review.
- Any future output-changing Revelation task must prove non-target identity and cite executable
  reviewed gold.
- Any future Revelation route must fail closed and remain book/form isolated.

### Owner Decisions Needed

- Which Revelation macro-area should become the first review packet.
- Whether each reviewed target should use parent/child units, preservation, or another structure.
- Whether speaker/voice boundaries require a separate review standard before Revelation gold.
- Whether Revelation implementation should remain late in the implementation order after review
  packets are created.

## 9. Candidate Future Review Packets

Priority candidates for T342:

1. Rev.12-Rev.14: symbolic scenes, speaker shifts, and cycle/interlude risk.
2. Rev.17-Rev.18: Babylon scenes and laments without identity assumptions.
3. Rev.21-Rev.22: new creation and epilogue scope.
4. Rev.2-Rev.3: seven letters as a lower-risk parent/child candidate.
5. Rev.4-Rev.5: throne-room vision and hymns.

## 10. Required Guardrails Before Implementation

Before any output-changing Revelation work:

- create one specific review packet;
- promote exact spans to reviewed gold by human decision;
- set `implementation_allowed: true` and `output_change_authorized: true` for that exact target;
- add executable reviewed-gold checks;
- preserve non-target identity;
- prove route isolation;
- keep Revelation-specific behavior out of global rules;
- avoid interpretive tradition assumptions;
- avoid boundary import;
- run same-baseline evaluation before any improvement claim.

## 11. Next-Task Recommendation

Next should be T342 Revelation review-packet candidate selection. T342 should choose exactly one
Revelation review target and create a pending, non-authorizing review packet. Do not start
Revelation implementation, import boundary texts, start T327G, or promote the Psalm candidate skill.
