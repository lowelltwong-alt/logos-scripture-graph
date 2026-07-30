# T544 Psalms confidence and hold calibration docket

## Scope and evidence identity

- Mode: read-only calibration of the intermediate Psalms decision ledger. This docket is the only
  file written.
- Audited ledger:
  `.ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Ps/decision_evidence_v2.jsonl`
- Ledger SHA-256:
  `7daf0cb09bfbd8324cda4cd6a4e37b8caec51c52535e8f3a054ecc442a29682d`
- Ledger decisions: `283/283`
- Read-only audit inputs:
  `.ai/handoffs/T544/psalms_adversarial_postcheck.md` and
  `.ai/handoffs/T544/psalms_hebrew_poetics_source_audit.md`
- Exclusions honored: no M1-M6 map, `comparison/`, or T417 layer was read.
- Authority: candidate evidence only. This docket does not authorize a boundary, chunk output,
  reviewed gold, source tradition, preferred reading, canon, theology, graph, or retrieval change.

This is a role-separated same-model check. It is not cross-model convergence and should be weighted
as one correlated model voice.

## Calibration verdict

The current confidence field is partly a proxy for `candidate_state`, not an independent measure of
boundary evidence:

| Current state | high | medium | medium_low | low |
|---|---:|---:|---:|---:|
| `accepted_candidate` | 53 | 210 | 0 | 0 |
| `held` | 0 | 0 | 6 | 14 |

There is no tier overlap at all. That is too exact to be an evidence-sensitive calibration. A
retrieval-parent or coda-policy hold can coexist with medium or high confidence in the observed
literary seam. Conversely, an accepted row can have weak evidence and need a low or medium-low
tier.

I audited all 283 rows on four separate axes:

1. the observable form or seam in the WEB text;
2. corroborating Hebrew evidence only where the source audit verified it;
3. the strongest live larger/smaller alternative; and
4. whether the unresolved issue concerns the boundary itself or a separate retrieval-parent,
   coda, or numbering policy.

Recommended result:

| Recommended state | high | medium | medium_low | low | total |
|---|---:|---:|---:|---:|---:|
| accepted candidate | 75 | 182 | 0 | 0 | 257 |
| held | 0 | 17 | 7 | 2 | 26 |
| total | 75 | 199 | 7 | 2 | 283 |

This changes 46 confidence tiers and adds six held rows in two genuine issue clusters. The remaining
237 tiers stay unchanged. Existing holds remain 20/20; no preserved appeal should be removed.

## Decision-local tier changes: formal seams currently under-scored

These accepted decisions have a form marker stronger than the ledger's default `medium` child tier.
They should remain accepted and move to `high`.

| Decision | Current -> recommended | Specific basis |
|---|---|---|
| `M7_sol-Ps-023` | medium -> high | Ps 19:1-6 is a complete creation/heavens witness; verse 7 changes subject to the repeated Torah/decree vocabulary rather than merely continuing the sky hymn. |
| `M7_sol-Ps-024` | medium -> high | Ps 19:7-11 is the internally parallel Torah catalogue; verse 12 changes to first-person self-scrutiny, so the catalogue has both a clear opening and close. |
| `M7_sol-Ps-025` | medium -> high | Ps 19:12-14 is a compact first-person cleansing and acceptable-speech petition, formally distinct from the impersonal Torah praise at 7-11. |
| `M7_sol-Ps-028` | medium -> high | Ps 22:1-21 sustains lament and direct rescue petition through “save me from the lion’s mouth”; verse 22 explicitly begins the assembly declaration/praise vow. |
| `M7_sol-Ps-029` | medium -> high | Ps 22:22-31 opens with “I will declare your name to my brothers” and expands into assembly and worldwide praise, a direct form change from the preceding lament. |
| `M7_sol-Ps-031` | medium -> high | Ps 24:1-2 is a two-verse creator-kingship proclamation; verse 3 begins a new entrance question. |
| `M7_sol-Ps-032` | medium -> high | Ps 24:3-6 is an explicit question-and-answer entrance exchange; verse 7 changes to repeated commands addressed to the gates. |
| `M7_sol-Ps-033` | medium -> high | Ps 24:7-10 is a self-contained gate antiphony with repeated command, question, and answer, ending the poem. |
| `M7_sol-Ps-066` | medium -> high | Ps 46:1-3 completes the refuge/cosmic-disturbance strophe and closes with Selah; Selah is only corroboration, while the river/Zion subject at verse 4 supplies the deciding transition. |
| `M7_sol-Ps-067` | medium -> high | Ps 46:4-7 is the Zion/river strophe and ends with the refrain “Yahweh of Armies is with us”; verse 8 begins the invitation to behold Yahweh’s works. |
| `M7_sol-Ps-068` | medium -> high | Ps 46:8-11 contains the behold/cease oracle movement and repeats the verse-7 refrain at verse 11, giving the strophe a formal close. |
| `M7_sol-Ps-087` | medium -> high | Ps 57:1-5 moves from refuge petition to the exaltation refrain at verse 5; verse 6 then reports the trap reversal. |
| `M7_sol-Ps-088` | medium -> high | Ps 57:6-11 begins with the enemy’s fall, turns to a steadfast-heart praise vow, and closes by repeating the verse-5 refrain. |
| `M7_sol-Ps-136` | medium -> high | Ps 80:1-3 is the shepherd invocation closed by the first “turn us again” refrain. |
| `M7_sol-Ps-137` | medium -> high | Ps 80:4-7 is a communal lament closed by the second occurrence of the same refrain; verse 8 begins the extended vine figure. |
| `M7_sol-Ps-138` | medium -> high | Ps 80:8-19 sustains the vine lament and closes with the expanded third refrain, giving the unit an observable formal boundary despite the larger parent. |
| `M7_sol-Ps-188` | medium -> high | Ps 107:4-9 is the complete desert-wanderer cycle: distress, repeated cry, deliverance, repeated thanks, and satisfaction. Verse 10 starts a new prisoner case. |
| `M7_sol-Ps-189` | medium -> high | Ps 107:10-16 repeats the same full cycle for prisoners and closes with broken gates/bars; verse 17 starts the sickness case. |
| `M7_sol-Ps-190` | medium -> high | Ps 107:17-22 repeats the cycle for the sick and closes with thanksgiving sacrifices; verse 23 starts the seafarer case. |
| `M7_sol-Ps-191` | medium -> high | Ps 107:23-32 repeats the cycle for the storm at sea and closes in the elders’ assembly; verse 33 leaves the case-cycle form for generalized reversals. |
| `M7_sol-Ps-208` | medium -> high | Ps 118:1-4 is a three-group antiphonal thanksgiving summons; verse 5 changes to first-person distress testimony. |
| `M7_sol-Ps-209` | medium -> high | Ps 118:5-18 is the sustained deliverance testimony; verse 19 changes to a direct gate-opening liturgy. |

## Decision-local tier changes: held policy questions currently under-score the seam

These rows should remain held, but their boundary evidence is stronger than their present
`medium_low` or `low` tier. The unresolved relation or retrieval policy belongs in `candidate_state`
and the hold question, not in an automatic confidence penalty.

| Decision | Current -> recommended | Specific basis |
|---|---|---|
| `M7_sol-Ps-009` | low -> medium | Psalm 9 is a complete received WEB Psalm with an internal praise-to-petition turn at verse 13. The hold concerns a possible Ps 9-10 alphabetic/numbering parent, not evidence that the Psalm 9 unit is weak. |
| `M7_sol-Ps-010` | low -> medium | Psalm 10 is a complete WEB lament with a portrait-to-petition turn at verse 12. Irregular alphabetic continuation and the absent scoped LXX witness keep the parent relation held without making the local unit low-confidence. |
| `M7_sol-Ps-058` | medium_low -> medium | Ps 41:1-12 is a coherent lament and verse 13 is a visible blessing/double-Amen coda. The unresolved question is whether to expose the coda separately while retaining the whole parent. |
| `M7_sol-Ps-059` | low -> medium | Ps 42:1-5 closes with the first verified variant refrain; verse 6 renews remembrance lament. The Ps 42-43 parent relation is unresolved, but the stanza seam is not low-evidence. |
| `M7_sol-Ps-060` | low -> medium | Ps 42:6-11 begins a renewed remembrance movement and closes with the second variant refrain. Parent retrieval remains held independently. |
| `M7_sol-Ps-061` | low -> medium | Psalm 43 is a complete received lament ending in the linked variant refrain; its relation to Psalm 42 is a parent-policy question rather than weak local form evidence. |
| `M7_sol-Ps-115` | medium_low -> medium | Ps 72:1-17 completes the royal prayer, verses 18-19 are a blessing/double-Amen, and verse 20 is an explicit colophon. The coda-child policy is unresolved, but the whole-Psalm candidate is moderately supported. |
| `M7_sol-Ps-186` | medium_low -> medium | Psalm 106 is a coherent historical confession and verses 47-48 form petition plus collection coda. The hold is coda retrieval, not uncertainty that the received Psalm is a larger unit. |
| `M7_sol-Ps-194` | low -> medium | Ps 108:1-5 is a stable praise movement closely paralleling WEB Ps 57:7-11; verse 6 opens the rescue/oracle movement. The hold concerns mandatory whole-parent priority, not the visibility of the seam. |
| `M7_sol-Ps-195` | low -> medium | Ps 108:6-13 is the rescue/oracle movement closely paralleling WEB Ps 60:5-12. Final-form reuse does not prove source history, but it gives moderate boundary evidence. |
| `M7_sol-Ps-204` | low -> medium | Psalm 114 is a complete WEB/MT exodus hymn; the absent Greek/LXX combination witness affects only the proposed cross-Psalm numbering relation. |
| `M7_sol-Ps-205` | low -> medium | Psalm 115 is a complete WEB/MT liturgical hymn with visible trust and blessing movements. Missing LXX evidence keeps alternate numbering held but does not reduce the received whole below medium. |
| `M7_sol-Ps-206` | low -> medium | Psalm 116 is a complete WEB/MT thanksgiving poem with a real testimony-to-vow alternative at verse 12. The unsourced Greek split is a relation gap, not low local confidence. |
| `M7_sol-Ps-210` | medium_low -> medium | Verse 19's gate-opening command clearly begins the final liturgical movement after the deliverance testimony. Whether verse 29 should be separately exposed as a coda remains a retrieval-policy hold. |
| `M7_sol-Ps-278` | low -> medium | Ps 147:1-6 is the Jerusalem-restoration movement; verse 7 renews the praise summons and changes to creator care. The missing LXX witness affects numbering, not the local seam. |
| `M7_sol-Ps-279` | low -> medium | Ps 147:7-11 is a creator-care hymn framed by the renewed summons; verse 12 renews praise again and turns to Zion, word, and Torah. |
| `M7_sol-Ps-280` | low -> medium | Ps 147:12-20 is the Zion/word/Torah movement beginning with a direct renewed summons. Alternate numbering remains held separately. |
| `M7_sol-Ps-281` | low -> medium_low | The heaven summons at 1-6 and “from the earth” summons at verse 7 make a real two-strophe alternative, while the whole creation litany is still coherent. This is genuine boundary uncertainty, but not absence of evidence. |

## Decision-local tier and hold changes: accepted seams currently over-scored

### Psalm 37 — new four-row hold cluster

The continuous alphabetic wisdom form and repeated righteous/wicked contrast do not make the current
11/12, 20/21, and 31/32 seams clearly stronger than nearby alternatives. The existing
`answered_with_local_evidence` response for `Ps-051` points back to fields but does not state a new
answer. Preserve the whole Psalm as the larger unit and hold the child scheme as one issue cluster.

| Decision | Current -> recommended | Specific basis |
|---|---|---|
| `M7_sol-Ps-050` | medium accepted -> medium_low held | Verse 12 does begin an enemy-attack portrait, but verses 9-11 already contrast the wicked and righteous; the acrostic counsel continues across the proposed seam. |
| `M7_sol-Ps-051` | medium accepted -> medium_low held | Verse 21 continues the same wicked/righteous contrast already active in verses 12-20 rather than opening a demonstrably new form. |
| `M7_sol-Ps-052` | medium accepted -> medium_low held | Verses 21-31 mix contrast, autobiographical testimony, exhortation, and inheritance; verse 32 resumes the same conflict rather than closing a stable prior unit. |
| `M7_sol-Ps-053` | medium accepted -> medium_low held | Verse 32 is another wicked-versus-righteous saying; verse 34's renewed imperative or later observational sayings are comparable alternatives, so 32 is not independently decisive. |

Recommended issue question:

> Do the topical transitions at Ps 37:12, 21, and 32 warrant separately retrievable children under
> the alphabetic parent, or should the continuous acrostic wisdom poem remain the only stable unit?

### Psalm 59 — new two-row hold cluster

The current 1-9/10-17 split conflicts with the more visible recurrence architecture: enemy dogs at
verses 6 and 14, Selah after verses 5 and 13, and strength/high-tower language at verses 9 and
16-17. The literary challenge to `Ps-090` is not answered by merely pointing back to the same
alternative.

| Decision | Current -> recommended | Specific basis |
|---|---|---|
| `M7_sol-Ps-090` | medium accepted -> low held | Verse 9 is itself the strength/high-tower refrain or hinge; ending the child there separates it from the assurance in verse 10 and does not align with the 5/6 or 13/14 recurring-cycle seams. |
| `M7_sol-Ps-091` | medium accepted -> low held | Beginning at verse 10 omits the verse-9 trust hinge, while the return of prowling dogs at verse 14 presents a stronger competing strophe opening. |

Recommended issue question:

> Should Psalm 59 be retained only as a whole parent, or should children follow the recurrent
> 1-5 / 6-13 / 14-17 cycle rather than the present 1-9 / 10-17 division?

## Required red-team dispute resolutions

| Psalm | Resolution | Reason |
|---|---|---|
| 37 | New hold/appeal cluster required for `050-053`. | The proposed child seams do not yet overcome continuous acrostic and contrastive-wisdom structure. |
| 59 | New hold/appeal cluster required for `090-091`. | The current split cuts across the stronger dog/Selah/strength recurrence pattern. |
| 62 | No new hold; retain `094-096` at medium. | Repeated trust formulas at 1-2 and 5-6, Selah closes at 4 and 8, and the class/wealth warning at 9 support the three movements. Selah corroborates but does not decide. |
| 67 | No new hold; retain `101-103` at medium. | The repeated praise line at 3 and 5 closes the first two strophes around the nations/judgment center; verse 6 clearly turns to harvest blessing. |
| 109 | No new hold; retain `196-198` at medium. | Verse 6 begins the sustained third-person imprecatory sequence and “But deal with me” at verse 21 returns to first-person rescue petition. Speaker attribution can remain ambiguous without erasing these form seams. |
| 145 | Retain `274-275` accepted at medium and the existing `276` hold at medium-low. | Verse 8 begins the graciousness/kingship movement and verse 14 the providence/nearness movement, while the alphabetic parent remains mandatory context. The unresolved verse-21 coda exposure is genuine; no additional hold is required. |

## Source-fidelity ceilings without tier changes

The fresh Hebrew-source audit identified five repairable evidence-linkage defects. Their current
`medium` tiers should not change, because the underlying observations are independently verified in
the source memo, but none should be promoted to `high` until its record is repaired:

- `M7_sol-Ps-166` and `M7_sol-Ps-167`: name the OSHB witness and deterministic normalization for
  the Ps 95:7-8 sequence.
- `M7_sol-Ps-199` and `M7_sol-Ps-200`: add the mapped Ps 110:4 neighbor locator, feature object, and
  normalization declaration for the oath formula.
- `M7_sol-Ps-245`: add the mapped feature object comparing the Ps 132:2 and 132:11 oath segments.

These are provenance ceilings, not reasons to manufacture new disagreement.

## Issue-cluster accounting

| Cluster | Decision rows | Independent issue clusters | Recommendation |
|---|---:|---:|---|
| Existing held rows | 20 | 7 substantive clusters | Preserve all holds; recalibrate 18 tiers upward because the policy hold is distinct from seam strength. |
| Strong formal seams defaulted to medium | 22 | 8 Psalms | Upgrade to high. |
| Psalm 37 child scheme | 4 | 1 | Add one held/appeal cluster; medium-low. |
| Psalm 59 child scheme | 2 | 1 | Add one held/appeal cluster; low. |
| Source-linkage repair ceiling | 5 | 3 source defects | Keep medium; block high until repaired. |
| Specified disputes resolved without new hold | 11 | 4 Psalms plus two accepted Ps 145 rows | Retain medium acceptance. |

The 20 existing held rows still represent seven substantive matters, not 20 independent dissent
topics: Ps 9-10; Ps 42-43; collection/poem codas; Ps 108 parent priority; Ps 114-116 numbering;
Ps 147 numbering; and Ps 148's heaven/earth strophe.

## Stop conditions and handoff

- Do not change confidence alone without also updating review packets, convergence-defense records,
  low-confidence partitions, checker hashes, postcheck hashes, and the eventual receipt.
- Append any new Ps 37 and Ps 59 appeals; do not rewrite or delete prior appeals.
- Keep `candidate-only`, `non_authorizing`, source-metadata evidence limits, and the same-model
  correlation disclosure.
- This calibration does not cure the adversarial memo's earlier prose-shell verdict or the fresh
  source memo's five evidence-linkage defects. A new hash-bound postcheck is still required after
  materialization.
