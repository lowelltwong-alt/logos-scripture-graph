# Biblical Chunking Stress Atlas

Status: proposed stress atlas only.

This atlas names Bible passages that are likely to expose weaknesses in chunking policy, evaluator
policy, source-tradition handling, punctuation assumptions, speaker boundaries, and parent/child
literary-unit modeling.

It does not approve expected output. It does not authorize output-changing work. Each case must be
promoted through review into per-form gold before it can drive chunker, orchestrator, evaluator, or
skill changes.

Current baseline remains D / Claude pass2 = 93.5 under T314 reviewed-structural-split evaluator
policy. That score is evaluator-policy correction for unchanged output, not chunking improvement.

## Structure

Machine-readable cases live in `eval/chunking_gold/stress_atlas/chunking_stress_cases.json`.
T318 observed current behavior for every case in
`eval/chunking_gold/stress_atlas/observed_stress_behavior.json`, with a human-readable summary in
`eval/chunking_gold/stress_atlas/OBSERVED_STRESS_BEHAVIOR.md`.

Every case records:

- `case_id`
- `passage`
- `book`
- `genre`
- `difficulty_types`
- `why_hard`
- `expected_chunking_risk`
- `text_critical_risk`
- `punctuation_risk`
- `translation_mismatch_risk`
- `speaker_boundary_risk`
- `parent_child_candidate`
- `proposed_gold_needed`
- `implementation_allowed: false`
- `status: proposed`
- `notes`

## Controlled Difficulty Types

| Difficulty type | What it flags |
| --- | --- |
| `long_structured_unit` | Long unit that may need internal children without losing parent unity. |
| `long_verse` | Verse-level unit may be too long or list-heavy for useful retrieval. |
| `short_context_dependent_unit` | Short unit needs surrounding context to avoid misleading retrieval. |
| `long_original_language_sentence` | Greek/Hebrew syntax may not match English sentence splits. |
| `punctuation_dependent` | Translation punctuation affects boundaries or interpretation. |
| `major_textual_variant` | Passage or phrase-level textual variant affects scope/status. |
| `textual_tradition_divergence` | MT/LXX/DSS or tradition alignment affects boundary planning. |
| `speaker_change_ambiguity` | Speaker/voice boundaries are hard or interpretively loaded. |
| `prophetic_oracle_collection` | Oracle/vision/woe units need review. |
| `apocalyptic_vision_sequence` | Vision sequence needs scene/voice hierarchy. |
| `legal_case_block` | Legal or covenant material has nested case/procedure units. |
| `genealogy_or_list` | Lists/genealogies need hierarchy-aware chunks. |
| `parallel_account_alignment` | Parallel passages require future alignment awareness. |
| `rhetorical_argument_section` | Argument chains should not be chopped by chapter alone. |
| `hard_exegesis` | Interpretive risk is high enough to require explicit review. |
| `parent_child_needed` | Both parent unity and internal child chunks may matter. |

## Stress Categories

The atlas currently covers all required categories:

1. Long structured units.
2. Long verses / administrative lists.
3. Very short context-dependent verses.
4. Greek long sentences.
5. Punctuation-dependent passages.
6. Major textual variants.
7. DSS / LXX / MT divergence zones.
8. Speaker-change ambiguity.
9. Prophetic oracle collections.
10. Apocalyptic vision sequences.
11. Legal/covenant/case-law blocks.
12. Genealogies/censuses/lists.
13. Parallel accounts.
14. Rhetorical argument sections.
15. Hard exegesis passages.
16. Parent/child literary-unit candidates.

## Highest-Risk Cases

| Case | Why it matters |
| --- | --- |
| Jeremiah MT/LXX divergence | Book-level tradition divergence can invalidate simple source-alignment assumptions. |
| Mark.16.9-20 | Major textual variant; inclusion/marking differs across editions and translations. |
| John.7.53-8.11 | Major variant plus dense dialogue and speaker-boundary risk. |
| 1Sam.10.27-11.1 | DSS/Nahash transition can change narrative context. |
| Deut.32.8-9 | Short unit with major textual-tradition and divine-council interpretation risk. |
| Isa.52.13-53.12 | Cross-chapter prophetic poem with debated speaker and servant-unit boundaries. |
| Dan.10-12 | Multi-chapter apocalyptic vision with angelic speech hierarchy. |
| Rev.12-18 | Large apocalyptic vision cycle with voices, hymns, and scene transitions. |
| John.13-17 | Long discourse with narrative, dialogue, teaching, and prayer subunits. |
| Rom.9-11 | Sustained argument where chapter splits can fracture rhetorical movement. |

## Marker-Sensitive Cases

T316c adds proposed cases for marker-sensitive review:

| Case | Marker concern |
| --- | --- |
| Gospels / Acts / Rev words-of-Jesus spans | `\wj` is red-letter/editorial evidence, not automatic speaker authority. |
| Psalms with Selah / `\qs` markers | `\qs` may be liturgical or performance evidence, not an automatic chunk boundary. |
| John.3 | Speaker-boundary ambiguity; `\wj` and punctuation cannot silently decide attribution. |
| Matt.5-Matt.7 | Long Jesus discourse; parent/child structure needs review before chunk changes. |
| John.13-John.17 | Farewell discourse marker focus; `\wj` cannot settle discourse/prayer boundaries by itself. |
| Matt.24-Matt.25 / Mark.13 | Apocalyptic Jesus discourse with parallel-account and speaker-scope risk. |
| John.7.53-John.8.11 | Textual-variant zone plus `\wj` speech evidence requires textual and speaker review. |

These cases are proposed only. Marker preservation is allowed, but marker-sensitive chunking must
not silently encode theological, speaker-attribution, textual-critical, source-language,
canon/boundary-text, or tradition-scoped interpretations without explicit human authorization and
reviewed evidence.

## Governance Rule

Stress atlas case status is `proposed`. Proposed stress cases are not reviewed gold, not
characterization-only current-output evidence, and not pending-human-review decisions. They are
future review candidates.

Before any output-changing work uses one of these cases:

1. Create a review packet or per-form gold manifest entry.
2. Decide whether the case is reviewed gold, characterization-only, pending human review, or an
   approved parent/child structural split.
3. Add executable checks or an explicit reviewed expected-output artifact.
4. Run evaluator sanity checks.
5. Keep raw/canonical data and runtime chunking behavior unchanged until the target is reviewed.

## Proposed Next Use

Use the atlas to select narrow future gold work:

- long Psalm review packets;
- prophetic oracle review packets;
- Gospel discourse review packets;
- Pauline argument review packets;
- text-critical / source-tradition boundary packets.

Do not use it as an implementation backlog by itself.

## T318 Observed Behavior Audit

T318 adds a diagnostic-only observed behavior surface for every stress-atlas case. It records which
current chunks touch each case, whether the case is contained, split, or mixed with extra context,
whether marker evidence is present, whether a review packet already exists, and the recommended
next review step.

The observed behavior audit is not reviewed gold and does not authorize output-changing work. It is
evidence triage for future review packets. A current split is not automatically bad fragmentation,
and a current whole-unit containment is not automatically approved expected output.
