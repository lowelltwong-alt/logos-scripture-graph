# T351 Bible-Wide Chunking Research Triage Atlas

## 1. Status

T351 is a Bible-wide research triage step before more chunking algorithm work.

It follows the owner guidance:

```text
Research the entire Bible first, decide where more research is needed and where review packets are enough, then chunk.
```

This is more faithful than moving directly from one hard-book packet into implementation because it
keeps the whole canon visible while still preserving the one-lane-at-a-time execution rule.

T351 does not implement chunks, promote reviewed gold, regenerate generated data, change evaluator
policy, import boundary material, create graph/vector/index outputs, or start T345.

## 2. Triage Rule

Every lane receives exactly one research status:

| Status | Meaning | Output authority |
| --- | --- | --- |
| `review_packet_ready` | Enough is known to create non-authorizing review packets. | None |
| `research_first` | More research/policy is needed before review packets can safely become gold candidates. | None |
| `governed_hold` | Prior governed work exists, but promotion or broader use remains blocked. | None |
| `implementation_blocked` | The lane must not be implemented until several upstream gates mature. | None |

All lanes keep `implementation_authorized: false`, `output_change_authorized: false`, and
`reviewed_gold_promoted: false`.

## 3. Whole-Bible Triage

| Lane | Triage status | First safe next action | Main theological risk |
| --- | --- | --- | --- |
| Psalms/poetry | `governed_hold` | Hold existing Psalm evidence; gather more controls before promotion. | Psalm forms could become global poetry rules. |
| Revelation/apocalyptic | `research_first` | Continue research/prep only under `REV-T344-E`. | Chronology, recapitulation, symbolic identity, millennium or eschatological school. |
| Epistle argument | `review_packet_ready` | Create review packets such as Eph.1.3-14, Rom.9-11, Heb.7-10, or 1Cor.8-10. | Argument boundaries can shift doctrinal context. |
| Narrative/pericope | `review_packet_ready` | Create representative review packets for genealogies, land allotments, and speech/narrative seams. | Boundaries can isolate covenant, fulfillment, genealogy, or causality context. |
| Legal/covenant | `review_packet_ready` | Create review packets for Decalogue/case-law/ritual/covenant-renewal samples. | Boundaries can imply covenant theology or law-category systems. |
| Wisdom/dialogue | `research_first` | Research speaker/dialogue/acrostic/poetic-voice policy before packets. | Speaker and poetic-voice boundaries can overclaim theology. |
| Prophetic oracle | `research_first` | Research oracle/vision/form boundaries before packets. | Fulfillment, messianic scope, temple interpretation, and source/tradition boundaries. |
| Gospel discourse/WJ | `research_first` | Research speaker policy before WJ/discourse packets can carry more weight. | WJ markers and punctuation can become speaker authority. |
| Textual variant/source tradition | `research_first` | Create policy before variant-sensitive packets can influence chunking. | Variant/source choices can become hidden canon or text authority. |
| Divine names/title capitalization | `research_first` | Inventory capitalization variants and create evidence-only policy before graph/chunk use. | Capitalization can silently encode divinity, Trinitarian relation, Christology, pneumatology, speaker attribution, or graph-edge truth. |
| Bible-wide orchestration | `implementation_blocked` | Wait for multiple reviewed lanes and same-baseline evaluations. | Global objectives can overwrite book-specific guardrails. |

## 4. Evidence Rules

These rules apply across all lanes:

- Source metadata is evidence only, not boundary, lexical, speaker, intertext, graph-edge, truth, or
  output authority.
- Internal cross-references and allusions may become review evidence, not automatic graph edges or
  chunk boundaries.
- Strong's-style numbers, Greek lexical rarity, and original-language claims require governed
  source, morphology, lemma normalization, and corpus-count policy before they can influence review.
- Headings, footnotes, paragraphing, poetry markers, punctuation, WJ/red-letter markers, and other
  edition formatting never become Scripture authority by themselves.
- English capitalization of divine names, titles, pronouns, and identity terms is translation or
  editorial evidence only. `God/god`, `LORD/Lord/lord`, `Spirit/spirit`, `Father/father`,
  `Son/son`, `Word/word`, `Christ/christ`, `Messiah/messiah`, `Holy Spirit/holy spirit`,
  `He/he`, `Him/him`, and `His/his` do not by themselves authorize divine identity,
  Trinitarian relation, speaker attribution, graph edges, chunk boundaries, lexical truth, or output
  changes.
- Labels must remain descriptive and text-local. They must not select chronology, covenant system,
  eschatological school, speaker attribution, symbolic identity, or textual-critical decision.

## 4a. Divine Name/Title Capitalization Watchlist

Before graph, retrieval, or chunking logic uses capitalization, create review packets or an
inventory policy for at least these cases:

- `John.1.1-John.1.18` for `Word/word`.
- `Gen.1.1-Gen.1.3`, `John.3`, `Rom.8`, and `1John.4` for `Spirit/spirit`.
- `Ps.110.1` for `LORD/Lord/lord`.
- `Matt.6` for `Father/father`.
- Any edition that capitalizes pronouns for God, Christ, or the Spirit.

The inventory should preserve observed forms and source provenance. It must not infer ontology,
Trinitarian relation, Christology, pneumatology, speaker identity, or graph-edge truth from
capitalization alone.

## 5. Recommended Route After T351

After T351 validates, the next faithful step is to select one `review_packet_ready` lane and create
non-authorizing review packets. Epistle argument boundaries are still a strong candidate because
the cases are identifiable and the risk can be reviewed without first solving Revelation or
prophetic-apocalyptic hermeneutics.

That is not implementation authority. It only means a lane is ready for review packets.

## 6. Non-Authorizations

T351 does not authorize:

- raw or canonical data mutation;
- generated chunk regeneration;
- chunk output change;
- reviewed-gold promotion;
- evaluator formula, leaderboard, or scorecard change;
- route behavior, skill lifecycle promotion, or global orchestration;
- Revelation implementation or T345;
- graph edges, embedding runs, or vector indexes;
- boundary, apocalyptic, apocryphal, or noncanonical material import;
- source metadata as authority;
- capitalization-driven divine identity, speaker attribution, graph edge, chunk boundary, or
  Trinitarian relation;
- whole-Bible improvement claims.

## 7. RISK-GATE-001 Map

Required question:

```text
What could this change accidentally authorize, weaken, contaminate, overfit, globalize, or make harder to reverse?
```

### Confirmed Risks

- A Bible-wide triage table could be mistaken for permission to chunk the whole Bible.
- A lane marked `review_packet_ready` could be mistaken for reviewed gold.
- Epistle argument boundaries could be selected too quickly if the packet remains too thin.
- Divine-name/title capitalization could be treated as ontology or graph truth instead of
  translation/editorial evidence.

### Plausible Risks

- Research labels could encode theological systems.
- Source metadata or cross-references could become hidden authority.
- God/god, LORD/Lord/lord, Spirit/spirit, Father/father, Son/son, Word/word, and pronoun
  capitalization could bias retrieval, speaker attribution, Christology, or pneumatology.
- A broad atlas could become too abstract to guide concrete review packets.

### Unlikely But High-Impact Risks

- A future agent could treat this as a global optimizer plan and overwrite lane-specific guardrails.
- Boundary or noncanonical sources could be imported as research context into canonical Scripture
  chunking.

### Tests Or Guards Needed

- A validator must fail if the triage map becomes authorizing.
- Tests must assert each lane has a controlled triage status and false output/implementation flags.
- Tests must assert divine-name/title capitalization remains `research_first` and non-authorizing.
- HARN-012 must keep T345 blocked while T351 triage is active.

## 8. Next Step

Finish T351 validation. Then choose one review-packet-ready lane from the triage map. Do not start
implementation until a later owner decision authorizes exact reviewed gold and executable checks.
