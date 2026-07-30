# T544 Psalms Adversarial Postcheck

## Task

Read-only adversarial postcheck of the corrective M7_sol Psalms core.

- Agent: Codex / Psalms adversarial specialist
- Mode: review
- Scope: `.ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Ps/chunks.jsonl`, its Psalm review packets, canonical WEB text, and WEB USFM markers; Genesis, Exodus, and Leviticus were consulted only for review-quality shape.
- Exclusions honored: no sibling maps, no validator trust, no data or source mutation.
- Files changed: this handoff only.

## Systemic findings

The revised core contains 283 rows: 263 `candidate_review_complete` and 20 `final_deferred_appeal`. Its stated confidence distribution is 113 high, 150 medium, 6 medium-low, and 14 low.

The evidence does not support treating these counts as quality convergence.

1. **Mechanical rejected seams.** Every ordinary whole-psalm row with a `Rejected subdividing ... at verse N` alternative uses the arithmetic midpoint of the Psalm: **92 of 92**. The nine remaining whole rows use special hold language instead of naming an internal alternative. Thus the claimed rejected seams are not decision-local tests of the strongest plausible seam.

2. **Role-deterministic verdicts.** Across all 283 review packets:

   - Hebrew-poetics reviewer: `supports` 283/283.
   - Canonical/retrieval reviewer: `challenge` 283/283.
   - Literary-form reviewer: `supports` exactly 263/283, and `challenge` exactly the 20 held decisions.

   Consequently there are only two packet profiles: `support/support/challenge` (263) and `support/challenge/challenge` (20). This is a role-and-status template, not evidence-sensitive agreement or disagreement.

3. **Non-child-local forms.** All **49 of 49** structurally segmented Psalms apply exactly one `literary_form` value to every child. A parent genre can be useful metadata, but it cannot substitute for the requested child-local form.

4. **Template language remains material.** New start/end quotations make the rationales look passage-specific, but the recurring skeleton is: numbered poem opens, numbered poem closes, no internal shift outweighs the whole unit, midpoint seam rejected. The Hebrew review says the same thing in every row with a role prefix; the canonical review issues the same challenge in every row.

## Sampled decision IDs and actual-seam counterexamples

The midpoint pattern was directly sampled across 41 whole-psalm decisions, including:

`M7_sol-Ps-001`, `002`, `008`, `014`, `015`, `027`, `030`, `034`, `038`, `039`, `043`, `049`, `055`, `065`, `080`, `099`, `100`, `123`, `124`, `142`, `145`, `148`, `159`, `160`, `168`, `175`, `179`, `201`–`203`, `233`, `235`, `240`, `245`, `246`, `260`, `277`, and `283`.

These decisions must not retain a claim that their rejected alternative was individually audited unless a real alternative is added. Particularly clear counterexamples follow.

| Decision | Current defect | Text-local correction |
|---|---|---|
| `M7_sol-Ps-002` | Rejects v. 6, the midpoint, as though it were the relevant alternative. | Audit the speaker/decree movement at Ps.2.7 (with the surrounding royal speech), or retain only the whole-Psalm parent at reduced confidence. |
| `M7_sol-Ps-049` | Treats Ps.36.6 as the adverse seam. | The actual transition is at Ps.36.5: the wickedness oracle gives way to the address about Yahweh's steadfast love. WEB has a paragraph break there; it corroborates but does not decide the seam. |
| `M7_sol-Ps-065` | Tests only Ps.45.9. | The visible alternatives are the prologue/royal address at 1/2, the bride address at 9/10, and the dynastic close at 15/16. A high-confidence whole label cannot claim to have rejected only the midpoint. |
| `M7_sol-Ps-100` | Tests Ps.66.10. | The strong form shift is at Ps.66.13, from communal praise/testing to first-person vow and testimony. |
| `M7_sol-Ps-159` | Tests Ps.91.8. | Direct divine speech begins at Ps.91.14. That is the required alternative to assess. |
| `M7_sol-Ps-179` | Tests Ps.103.11. | The text's major movements begin at Ps.103.6, 15, and 19; the midpoint does not test them. |
| `M7_sol-Ps-245` | Tests Ps.132.9. | The responsive Yahweh-oath movement opens at Ps.132.11, after the petition at vv. 9–10. |

`M7_sol-Ps-036` (Psalm 27), `099` (Psalm 65), `160` (Psalm 92), and `168` (Psalm 96) need the same repair: audit actual competing movements, not a generated midpoint.

## Segmented child-form correction docket

Keep an outer/parent form where useful, but assign the following child-local forms to the existing segmented spans.

| Psalm / decisions | Required child-form sequence |
|---|---|
| 18 / `018`–`022` | distress invocation; theophanic deliverance; vindication/recompense; warrior-victory recital; royal thanksgiving close |
| 19 / `023`–`025` | creation hymn; Torah praise; personal cleansing petition |
| 22 / `028`–`029` | lament/petition; thanksgiving-praise/testimony |
| 24 / `031`–`033` | creator-kingship proclamation; entrance question-and-answer; gate antiphony |
| 31 | refuge/remembered deliverance; renewed lament; praise/exhortation |
| 35 | plea and praise-vow; false-witness lament; vindication and praise |
| 37 | acrostic counsel; wicked-fate contrast; righteous conduct; closing refuge |
| 40 | thanksgiving testimony; urgent lament |
| 42 / `059`–`060` | thirst/refrain; renewed distress/refrain |
| 44 | historic confidence; present defeat; innocence/petition |
| 46 | refuge/cosmic disturbance; Zion/refrain; works/refrain |
| 49 | wisdom summons; wealth/mortality meditation; closing mortality warning |
| 50 | theophanic court; worship critique; wicked-covenant indictment |
| 51 | confession; cleansing/restoration; vow/community close |
| 55 | distress/escape; betrayal; trust/petition |
| 57 / `087`–`088` | refuge/refrain; reversal-praise/refrain |
| 59 | plea/enemy watch; strength/trust |
| 62 | trust claim; self-address/exhortation; wealth/frailty wisdom |
| 67 | blessing/refrain; nations-and-justice/refrain; harvest coda |
| 68 | opening/procession; Sinai march; deliverance/procession; global doxology |
| 69 | flood/alienation; appeal; imprecation; praise/Zion |
| 71 | refuge plea; hope/testimony |
| 73 / `116`–`119` | prosperity problem; sanctuary turn; judgment/self-correction; nearness testimony |
| 74 | sanctuary lament; creation kingship; covenant petition |
| 77 | lament/questions; remembrance; exodus theophany |
| 78 | teaching; Ephraim/exodus; rebellion/provision; continued sin/mercy; plagues/exodus; rebellion/Shiloh; Judah-David close |
| 80 | shepherd/refrain; communal lament/refrain; vine petition/refrain |
| 81 | festival summons; exodus speech; refusal/consequence |
| 83 | coalition lament; historical petition |
| 89 / `150`–`155` | covenant opening; heavenly praise; Davidic oracle; humiliation; how-long lament; covenant petition/coda |
| 90 | transience; wrath/wisdom; petition |
| 94 | vengeance complaint; rebuke; instruction; testimony/requital |
| 95 / `166`–`167` | worship hymn; warning oracle |
| 99 | enthronement; justice/worship; mediation/holiness |
| 102 | affliction; Zion restoration; mortality/creator permanence |
| 104 | cosmic ordering; habitats; seasons; sea/dependence; praise close |
| 107 / `187`–`193` | summons; desert; prison; sickness; storm; reversals; wisdom coda |
| 108 / `194`–`195` | praise; petition/oracle |
| 109 | accusation; imprecation; personal plea |
| 110 / `199`–`200` | royal oracle; priestly oath/victory |
| 118 | responsive summons; testimony; gate liturgy |
| 119 / `211`–`232` | alphabetic Torah stanza, explicitly named Aleph through Taw for the respective octets |
| 135 | summons; divine acts; idol polemic/house blessing |
| 136 / `251`–`256` | opening thanks; creation refrain; exodus refrain; conquest refrain; provision refrain; doxological coda |
| 137 / `257`–`259` | exile lament; Jerusalem oath; imprecation |
| 139 / `261`–`265` | knowledge; presence; formation praise; imprecatory protest; self-examination |
| 144 / `270`–`273` | warrior/reflection; theophanic petition; new-song/rescue; household blessing |
| 145 / `274`–`276` | greatness; gracious kingdom; providence/close |
| 147 / `278`–`280` | restoration; providence; Zion-word/Torah |

## Boundaries not shown wrong by this postcheck

The template defect does **not** prove that all selected boundaries are wrong. Direct WEB discourse/form transitions support retaining the current candidate seams in Psalms 18, 19, 22 (especially v. 22), 24, 31, 35, 40, 42, 44, 46, 49–51, 55, 57, 62, 67–69, 73–81, 83, 89, 90, 94–95, 99, 102, 104, 107–110, 118–119, 135–137, 139, 144–145, and 147.

They remain candidate-only: each needs a locally authored rationale and a real rejected alternative before a support verdict is meaningful.

## Holds

The 20 held rows are not random. They collapse into seven substantive retrieval-schema issue clusters:

1. Psalms 9–10 linked acrostic/alternate-numbering parent (2 rows).
2. Psalms 42–43 refrain parent (3 rows).
3. Collection or poem coda-child policy (6 rows: Psalms 41, 72, 89, 106, 118, 145).
4. Psalm 108 whole-parent priority (2 rows).
5. Psalms 114–115 combination and Psalm 116 alternate split (3 rows).
6. Psalm 147 alternate-numbering parent (3 rows).
7. Psalm 148 heaven/earth strophe (1 row).

Those questions are legitimate. However, the apparent total of 20 exaggerates the number of independent dissent topics, and the selection does not explain why comparable live alternatives in decisions `002`, `049`, `065`, `100`, `159`, `179`, and `245` are high-confidence acceptances rather than holds.

## Comparison shape only

Genesis (82 rows), Exodus (67), and Leviticus (72) show materially varied confidence distributions and more scene/procedure/register-specific form labels. Their outer-unit rationale wording is also generic, so they are not a green quality benchmark. They do demonstrate that nonuniform confidence and child-level form typing are possible; the Psalms core's count distribution alone cannot demonstrate reliability.

## Final owner self-smell verdict

| Test | Verdict |
|---|---|
| Decision-local rationales/reviews | **FAIL** |
| Rejected seams genuinely tested | **FAIL** |
| Child-local form labels | **FAIL** |
| Support/challenge verdicts reflect evidence | **FAIL** |
| Holds are genuine rather than arbitrary | **PARTIAL** — topics are genuine, calibration is not |

**Overall: FAIL.** The 283-row corrective core is evidence-preserving and candidate-only, but it does not pass a substantive adversarial review until the midpoint alternatives, role-deterministic review logic, and child-form metadata are corrected.

---

## Second-round adversarial postcheck — repaired active core

**Scope and mode.** Fresh read-only inspection of the current M7 Psalms core, using role-separated checks inside the same model substrate. This is **not** cross-model convergence, and no M7 artifact was edited.

### Recomputed active-artifact identity

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| `book_chunks/Ps/chunks.jsonl` | `e03a193500222404770e24f62827f5569768e7a450c7e59a864f8120ea39b5a3` | 1,612,532 |
| `reviews/Ps/review_packets.jsonl` | `7c8e0137a1690b7b7c720136de8e9a1c168c4e76ad363989ec64f70d9d32fa73` | 3,120,721 |
| `reviews/Ps/decision_relations.jsonl` | `e2cc67bc1594d00d2fa9d5ef597a61141ed49b7933d4054548a8492f41198d35` | 23,239 |
| `reviews/Ps/sidecar_rows_v2.json` | `0bd1f9b9d2521c048b190583da008cf2534b5ffc77be601246a6caa1f7e22ca2` | 154,622 |

All four recomputed digests match the requested active-core identities. The three active Ps sidecar partitions each contain the same 20 held decision IDs as the source sidecar replacement. The appeal ledger's recorded pre-append prefix digest and byte count also reproduce; the active appeal is append-only rather than a rewrite.

### What the repaired core did fix

- The prior mechanical midpoint signature is gone: `0/0` current alternatives match the old `rejected subdividing ... at verse N` pattern. The few remaining explicit internal alternatives are real local seams, including Ps 10:12, Ps 60:6, Ps 117:2, and Ps 148:7.
- All 49 segmented Psalms now have non-uniform child forms (`0/49` copied-parent-form cases). Re-reading the difficult seams confirms real differentiations at Ps 19:7/12, Ps 22:22, Ps 110:4, and the alphabetic Psalm 119 stanzas.
- Primary verdicts are not mechanically uniform by role: Hebrew/textual `218 support / 65 challenge`, literary `169 / 114`, canonical/retrieval `252 / 31`. The resulting status split is `263 accepted / 20 held`; confidence is `53 high, 210 medium, 6 medium_low, 14 low`.
- Exact-span WEB plus OSHB/UXLC references are present for the original-language primary reviews. The 20 holds still reduce to the seven real issue clusters recorded above, and their questions/routes and preserved appeals are present.

These are real improvements, but they cannot make a `PASS_WITH_HOLDS` verdict while repairable evidence-quality defects remain.

### Independently reproduced repairable defects

| Defect | Independent result | Why it fails substantive review |
|---|---:|---|
| Whole-Psalm rationale shell | `101/283` (all are whole-Psalm rows) | The phrases `follows a poem-specific arc`, `material counterproposal assessed`, and `audited poem-specific movement` substitute for individual reasoning. |
| Adjacent-unit rationale shell | `182/283` (`49` whole parents and `133` child rows) | `The strongest larger-child alternative` is a batch wrapper, not a demonstrated alternative at the actual seam. |
| Templated rationale detection | `283/283` | Every current boundary rationale triggers the corrective gate's template rule; this is not cured by varying the embedded Psalm names or verse numbers. |
| Review-prose shells | seven signatures at `283/283` each | The stable-WEB, metadata-disclaimer, Hebrew/versification caveat, neighboring-movement, whole-parent, retrieval, and peer-comparison sentences occur in every packet. Exact source locators alone do not turn this boilerplate into passage-specific original-language evidence. |
| Clipped source quotations | `34/283` chunks, duplicated into packets | Examples include a quotation ending `"Blessed is the man who doesn’t walk in the"`; quotation fragments must be corrected or removed rather than presented as source support. |
| Doubled terminal punctuation after a closing quote | `4` decision IDs, duplicated in packets: `029`, `060`, `088`, `195` | Examples include `"lion’s mouth!".` and `"despair, my soul?".`. These are data-quality defects, not merely console-display encoding. |

The current hardened corrective-depth gate independently returns failure for exactly these classes. Its summary also confirms `283` chunks/packets, `1168` distinct review/check identities, maximum attempt reuse `8`, no generic form labels, and the corrected midpoint/form findings above.

### Re-read seam and hold judgment

The direct local-seam results for the prior difficult docket (`002`, `049`, `065`, `100`, `159`, `179`, `245`; Ps 19, 22, 110, and 119) remain plausible candidate mappings; this postcheck found no new evidence that they are individually wrong. Nor does it invalidate the 20 held rows' substantive topics: Ps 9–10, 42–43, coda policy, Ps 108, 114–116 numbering, Ps 147 numbering, and Ps 148. The defect is that generalized prose makes the claimed review discipline and confidence calibration non-auditable across the entire active core.

### Required repair before another postcheck

1. Rewrite every boundary rationale and every review-prose field from the actual local evidence; do not make a lexical substitution in the existing shells.
2. For all 101 whole-Psalm rows, name the actual movement(s), the strongest real alternative, and why the complete poem remains preferable. For all 182 adjacency cases, identify the actual neighboring span and its concrete functional/seam counterevidence.
3. Repair or omit the 34 clipped quotations, and repair the four quoted-terminal punctuation cases in both chunks and packets. Regenerate dependent packet content hashes afterward.
4. Make Hebrew/textual review prose passage-specific: retain exact OSHB/UXLC references, but add the precise lexical, poetic, accentual, or versification observation actually relied on, and retain meaningful counterevidence.
5. Preserve the 20 held rows, active-sidecar replacement identity, and append-only appeal history unless a new evidence-backed decision changes them. Rerun the hardened corrective gate and this postcheck only after the active-core hashes change.

### Second-round verdict

**FAIL_REPAIRABLE.** `PASS_WITH_HOLDS` is not available: pervasive chunk and packet prose shells, 34 clipped quotations, and four terminal-punctuation defects are all repairable defects in the active core. The prior midpoint, copied-form, and deterministic-role findings are improved, but they do not overcome this evidence-integrity failure.
