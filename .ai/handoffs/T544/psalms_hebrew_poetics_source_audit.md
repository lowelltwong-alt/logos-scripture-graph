# T544 Psalms Hebrew-poetics and source-fidelity audit

## Scope and authority

Read-only specialist audit of the active `M7_sol` Psalms chunks and review packets against:

- canonical WEB Psalm passage coordinates and translation-witness text;
- the permitted OSHB and UXLC Psalm source views and their manifests;
- `book_strategy/Ps.md`; and
- the prior T544 adversarial docket.

No M1-M6 map, comparison output, or T417 layer was read. No M7 artifact was edited. This memo and
its machine-readable appendix are candidate evidence only. They do not decide a boundary, canon,
authorship, theology, preferred reading, source tradition, or reviewed-gold status. This audit is a
role-separated check within the same model substrate, not an independent-provider result.

## Executive verdict

The current Psalms rewrite has real text-local insights, but its Hebrew-source citations are not
yet auditable as written. All 283 packets give the first primary an OSHB locator formed by copying
the WEB span unchanged. That is unsafe: 62 Psalm chapters have different WEB and MT verse counts,
and 110 of the current 283 decisions fall in those chapters. Equal chapter counts also do not
guarantee equal content starts: titles can occur before a WEB/KJV segment inside the same MT verse,
and WEB Psalms 13:5-6 occupy two word segments inside MT Psalm 13:6.

The repair should use the generated crosswalk:

- artifact: `.ai/handoffs/T544/psalms_web_mt_crosswalk.json`
- SHA-256: `a83b101fe1ad3e36b3aa2282656afd88ba2fd5925b7f5a6e0511a7d5eb56975d`
- coverage: 2,461/2,461 canonical WEB Psalm verses
- explicit OSHB `KJV:` note mappings: 1,042
- structural-identity mappings without an explicit note: 1,419
- chapter-count shape: 88 same-count, 58 MT `+1`, four MT `+2`
- MT `+2` Psalms: 51, 52, 54, and 60
- MT-only title verses not mapped to WEB content: 67
- UXLC MT target existence: 2,461/2,461
- exceptional split: WEB Psalms 13:5 and 13:6 are disjoint OSHB word segments in MT Psalm 13:6

Until the packets cite mapped OSHB segments, a generic `OSHB:Ps.xml#<WEB span>` reference is a
source-family pointer, not exact-span Hebrew evidence.

## Deterministic WEB-to-MT citation procedure

The local source and field pattern are:

```text
data/candidate/original_language_evidence/canonical_source_views/
  openscriptures_oshb/files/Ps.xml

<note>KJV:Ps.<chapter>.<WEB/KJV verse></note>
```

The XPath recorded in the appendix is:

```text
//o:verse/o:note[starts-with(normalize-space(.),"KJV:Ps.")]
```

Use the following deterministic procedure:

1. Read the 2,461 WEB Psalm OSIS references from
   `data/canonical/scripture/passages/passages.jsonl`.
2. In OSHB, a matching `KJV:Ps.C.V` note opens the WEB/KJV-coordinate content segment inside its
   enclosing MT verse. The segment starts at the next OSHB `<w>` and ends before the next `KJV:`
   note in that MT verse, or at the MT verse end.
3. If no explicit note exists, use the identical OSHB/UXLC OSIS ID only when that target exists.
   Label this `structural_identity_no_explicit_note`; it is inferred coordinate parity, not an
   explicit crosswalk assertion.
4. Map every verse in a WEB chunk, not only its endpoints. Cite the ordered OSHB segment locators.
   This prevents losing the Psalm 13:5-6 intra-verse split or including a title prefix.
5. Use UXLC to confirm the mapped MT verse exists. The word-range locator is OSHB-specific; do not
   claim identical OSHB and UXLC tokenization.
6. Preserve all unmapped MT title material as superscription metadata. It is evidence, not part of
   the WEB chunk text and not automatic boundary or authorship authority.

The appendix distinguishes `explicit_oshb_kjv_note` from
`structural_identity_no_explicit_note` on every verse. Absence of an offset is never reported as an
explicit crosswalk fact unless an OSHB note actually supplies it.

## Exact evidence the writer may safely state

1. OSHB and UXLC are verified local Hebrew source packages exposed here through candidate
   canonical-only views. Their manifests expressly deny boundary, canon, preferred-reading,
   reviewed-gold, graph, retrieval, and theology authority.
2. OSHB contains accented Hebrew word forms and source-provided morphology. Its `lemma`
   attributes are Strong-style lookup hints under the manifest, not locally authoritative lemmas,
   roots, or lexical meanings. UXLC supplies Hebrew text but no source-provided morphology.
3. A superscription can be quoted as source text at its MT location. Its attribution or historical
   occasion cannot be treated as proven by the label.
4. `סֶלָה` is encoded in OSHB as a word (`<w lemma="5542" morph="HTj">`), and UXLC likewise places
   it in a `<w>` element. Its occurrence at a verse end may be noted. Neither source encodes it as
   a mandatory stanza boundary.
5. Psalm 119 has a particularly strong local acrostic signal: in both OSHB and UXLC, every verse
   in 1-8 begins with aleph, every verse in 9-16 with beth, and so on through taw in 169-176. The
   safe claim is “eight verse-initial consonants,” not “an acrostic heading,” because the scoped
   Hebrew XML has no Aleph/Beth heading element.
6. Psalms 42:5, 42:11, and 43:5 contain a recurring refrain. It is a variant refrain, not a
   verbatim-identical line. WEB wording differs, and OSHB MT 42:6 differs from MT 42:12/43:5.
7. Psalm 72:18-20 visibly moves from blessing to “Amen and amen” and then the explicit colophon
   “This ends the prayers by David, the son of Jesse.” The text supports a coda/colophon question;
   it does not by itself decide standalone retrieval.
8. Psalms 41:13, 89:52, and 106:48 visibly contain closing blessing/Amen formulas in WEB. They may
   be called doxological formulas. “Collection-book boundary” remains a literary classification
   and retrieval decision, not a source tag.
9. Psalm 110:4 begins a new oath formula, `נִשְׁבַּע יְהוָה`, and introduces the priestly statement.
   This is strong evidence for a movement at verse 4, while the complete Psalm remains the parent.
10. Psalm 132:2 says David swore to Yahweh; verse 11 says Yahweh swore to David. The paired oath
    language is textually visible and supports testing verse 11 as a response movement.
11. Psalm 148:7 begins “Praise Yahweh from the earth” after verses 1-6 summon the heavens. This is
    direct evidence for a heaven-to-earth strophe alternative, while retrieval treatment remains a
    legitimate hold.
12. WEB Psalms 108:1-5 closely parallel WEB 57:7-11, and WEB 108:6-13 closely parallel WEB
    60:5-12, with wording variations. This supports an internal reuse/composite-form relation; it
    does not prove a source-history or authorship theory.

## Claims the scoped local sources do not support

- Greek/LXX combined or split numbering for Psalms 9-10, 114-115, 116, or 147. No scoped LXX
  source, versification table, or Greek witness was present. Keep these relations as source gaps
  requiring external/human evidence.
- “Aleph heading,” “Beth heading,” or any other Psalm 119 letter-heading claim from OSHB/UXLC.
  The initials prove the acrostic blocks; the XML does not supply those headings.
- A complete, mechanically regular Psalm 9-10 acrostic that by itself requires a merged retrieval
  parent. The Hebrew initials supply linked alphabetic pressure, but the pattern is irregular and
  the retrieval consequence remains contested.
- An identical refrain across Psalms 42-43. The refrain recurs with textual variation.
- Selah as a pause of known duration, stanza divider, speaker divider, or boundary authority.
- A stanza seam merely because a Masoretic accent appears. A specific accentual claim needs a
  documented parsing rule and phrase-level comparison; the Unicode accents are evidence only.
- Explicit divine-speaker metadata at Psalm 91:14. The shift to first-person promise is visible,
  but the scoped XML does not label the speaker. Speaker identification remains contextual
  inference.
- Rabbinic, ancient Jewish, ANE, Second-Temple, patristic, or reception-history claims. No such
  source was in the permitted audit set.
- Any Hebrew root, etymology, or lexical-theological conclusion derived from OSHB `lemma`
  attributes alone.
- A same-coordinate WEB/OSHB/UXLC span claim without using the crosswalk.

## Hardest decision-local examples

| Decision(s) | Source-local result and required treatment |
|---|---|
| `M7_sol-Ps-003` — Ps 3:1-8 | MT/OSHB has title-only 3:1; WEB 3:1 maps to MT 3:2. Selah is a word in MT 3:3 and 3:5 (WEB 3:2 and 3:4), not a stanza tag. Cite mapped segments and keep title/Selah evidence-only. |
| `M7_sol-Ps-009` — Ps 9 | WEB 9:1 maps to MT 9:2 after title-only MT 9:1. Hebrew initials show alphabetic pressure, but neither a required Ps 9-10 parent nor alternate Greek numbering is locally established. The hold is warranted. |
| `M7_sol-Ps-010` — Ps 10 | Later Hebrew verse initials include qoph/resh/shin/taw signals, supporting relation to the alphabetic pressure in Ps 9. The sequence is irregular and does not decide merger or numbering. |
| `M7_sol-Ps-059/060/061` — Ps 42-43 | WEB 42:5/11 map to MT 42:6/12; Psalm 43 is identity-mapped. The refrain is recurring but variant. Preserve the linked-parent question without claiming identical text or a settled parent. |
| `M7_sol-Ps-058` — Ps 41 | WEB 41:13 maps to MT 41:14. The blessing plus double Amen is visible; “collection coda” and standalone retrieval remain adjudication questions. |
| `M7_sol-Ps-077/078/079` — Ps 51 | This is a `+2` chapter: WEB 51:1 begins at MT 51:3 after two title verses. Every Hebrew seam and quotation must use the mapped segment, not the copied WEB coordinate. |
| `M7_sol-Ps-069` — Ps 47 | Selah occurs after WEB verse 4 (mapped to MT verse 5 because of the title offset). It corroborates a possible 1-4/5-9 movement but cannot decide the split. |
| `M7_sol-Ps-115` — Ps 72 | Verses 18-19 give blessing/Amen language; verse 20 explicitly closes the Davidic prayers. This is strong coda evidence but still leaves two serious retrieval options. |
| `M7_sol-Ps-155` — Ps 89:49-52 | WEB 89:49-52 maps to MT 89:50-53; the doxology is MT 89:53. The current same-coordinate OSHB locator is wrong. Preserve the coda hold. |
| `M7_sol-Ps-159` — Ps 91 | Verse 14 visibly shifts to first-person promises after third/second-person protection language. The text does not supply a speaker label, so describe a first-person oracle-like shift and retain speaker ambiguity. |
| `M7_sol-Ps-166/167` — Ps 95 | The current 7/8 split is a hot zone. WEB 95:7 ends “Today, oh that you would hear his voice!” and Hebrew continues `הַיּוֹם אִם־בְּקֹלוֹ תִשְׁמָעוּ / אַל־תַּקְשׁוּ לְבַבְכֶם` across verses 7-8. Audit 1-6 plus 7-11 and whole-Psalm alternatives; do not call verse 8 an unqualified standalone opening. |
| `M7_sol-Ps-194/195` — Ps 108 | WEB 108 maps to MT with a `+1` title offset. Canonical WEB comparison supports the Ps 57/Ps 60 reuse relation and the 5/6 final-form movement, but not a source-history conclusion. The whole-parent priority question remains legitimate. |
| `M7_sol-Ps-199/200` — Ps 110 | Verse 4’s explicit Yahweh-oath formula is strong local evidence for the child seam. Speaker/addressee and later theological use remain outside boundary authority. |
| `M7_sol-Ps-204/205` — Ps 114-115 | The two complete WEB/MT poems are locally available. The claimed Greek combination is not locally sourced, so the alternate-numbering relation must remain an external-source gap. |
| `M7_sol-Ps-206` — Ps 116 | The complete WEB/MT poem is locally available. The claimed Greek split is not locally sourced. Do not use it as evidence until an exact witness/table is supplied. |
| `M7_sol-Ps-211` — Ps 119:1-8 | Both Hebrew witnesses show eight aleph initials. High confidence for the eight-verse alphabetic block is source-supported; replace “Aleph heading” with the verified initial pattern. |
| `M7_sol-Ps-212` — Ps 119:9-16 | Both witnesses show eight beth initials. The 8/9 seam is materially stronger than a translated-topic shift and may be stated directly. |
| `M7_sol-Ps-232` — Ps 119:169-176 | Both witnesses show eight taw initials and the block ends the poem. Preserve the whole-Psalm parent; the stanza evidence itself is strong. |
| `M7_sol-Ps-245` — Ps 132 | Verses 2 and 11 contain the paired David-to-Yahweh and Yahweh-to-David oaths. This is a real response seam at verse 11, not a generated midpoint. |
| `M7_sol-Ps-274/275/276` — Ps 145 | OSHB 145:1 contains title words before `<note>KJV:Ps.145.1>`; mapped content begins at `Ps.145.1#w3`. The MT/UXLC acrostic content then lacks a nun line between mem and samekh. Say incomplete/alphabetic praise; do not import an LXX nun line without an LXX source. |
| `M7_sol-Ps-278/279/280` — Ps 147 | Verses 7 and 12 visibly renew the praise summons and subject focus, so the internal movements are textually plausible. The Greek split-numbering claim is unsupported by the scoped sources and must remain a gap. |
| `M7_sol-Ps-281` — Ps 148 | Verse 7’s “from the earth” after the heavenly summons is a real competing seam. Holding the whole-Psalm versus heaven/earth children question is evidence-sensitive, not lazy deferral. |

## Quote and citation fidelity rules

1. Decode JSONL/XML explicitly as UTF-8. Do not let a shell default turn `doesn’t` into mojibake.
2. Quote WEB only from
   `data/canonical/translations/eng-web/translation_witnesses.jsonl`. A shortened quotation must
   use an ellipsis and be called an excerpt. Do not call a clipped clause a complete “line.”
3. Never cut a quotation mid-word. Preserve punctuation inside the quotation; do not add a second
   terminal mark after a quoted sentence.
4. Quote Hebrew from the mapped OSHB segment or mapped UXLC MT verse. State whether cantillation,
   vowel points, maqqef, paseq, or morphology were omitted or normalized.
5. A Hebrew citation must carry both coordinates when they differ, for example:
   `WEB Ps.89.52 -> OSHB/UXLC MT Ps.89.53`.
6. For Psalm 13:5-6, cite the OSHB word segments, not only `MT Ps.13.6`:
   `Ps.13.6#w1-w6` and `Ps.13.6#w7-w11`.
7. A source locator alone is not evidence prose. State the exact observed lexical, syntactic,
   refrain, acrostic, oath, speaker, or coda feature and the strongest counterevidence.
8. OSHB morphology and lemma attributes must be labeled source metadata. Do not infer a root,
   etymology, doctrinal meaning, or preferred translation from a lookup hint.
9. Superscriptions, Selah, accents, WEB punctuation, and versification may corroborate a seam but
   must be labeled `translation_versification_metadata_not_boundary_authority`.
10. If the necessary witness is absent, record a source gap. Do not turn a familiar scholarly fact
    into a locally verified claim.

## Required repair before a Hebrew-source pass

- Replace copied same-coordinate OSHB/UXLC locators with ordered crosswalk segment locators.
- Rewrite Hebrew-primary prose to name a decision-local Hebrew observation, not merely source
  availability and a metadata disclaimer.
- Re-audit Psalm 95 at 7/8 as a syntax-sensitive hot zone.
- Replace Psalm 119 “heading” language with verified initial-letter evidence.
- Describe Psalms 42-43 as a variant refrain.
- Keep all LXX/Greek numbering claims as explicit source gaps until an exact local or external
  witness is supplied.
- Preserve appeals and candidate-only status; none of these source observations force consensus.

## Fresh post-repair source-fidelity verdict — 2026-07-24

Audited artifact:

```text
.ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Ps/decision_evidence_v2.jsonl
SHA-256 7daf0cb09bfbd8324cda4cd6a4e37b8caec51c52535e8f3a054ecc442a29682d
```

The ledger and crosswalk hashes were stable before this check. All 283 decisions pinned the
crosswalk SHA-256 `a83b101fe1ad3e36b3aa2282656afd88ba2fd5925b7f5a6e0511a7d5eb56975d`
and this memo's pre-append SHA-256
`9424a48201ea4f643d2771bd71d5aa90a2424e74b7fba7990e82bf3f474a2c98`.
Appending this verdict necessarily changes the memo's current hash; the ledger correctly identifies
the pre-verdict source-audit input, not this later audit result.

### Deterministic results

- `830/830` WEB observations match the canonical translation-witness text exactly, including
  punctuation, and all are labeled `complete_verse`. Their opening, closing, left-context, and
  right-context roles match the decision spans. Fifty-two observation copies contain ellipsis-like
  punctuation already present in the canonical verse; none is an editorial truncation.
- The 283 ordered mappings aggregate to all `2,461/2,461` canonical WEB Psalm verses exactly once:
  `1,042` use `explicit_oshb_kjv_note` and `1,419` use
  `structural_identity_no_explicit_note`. Every mapped OSHB word range and UXLC MT target exists in
  the pinned source snapshots.
- WEB Psalm 13:5 and 13:6 retain the required disjoint OSHB segments
  `Ps.13.6#w1-w6` and `Ps.13.6#w7-w11`.
- Psalms 42:5, 42:11, and 43:5 are correctly represented as a *variant* refrain. All three WEB
  texts and the three supplied OSHB texts match their witnesses; the record does not call them
  identical.
- Psalm 95 is correctly resegmented as 1-6 and 7-11. The Hebrew words at MT 95:7-8 support keeping
  the hearing condition and heart-hardening prohibition together, so the former 7/8 seam is
  rejected while the 6/7 seam remains viable.
- All 22 Psalm 119 decisions are eight-verse blocks. Independent recalculation from both OSHB and
  UXLC verifies eight identical verse-initial consonants in each block, aleph through taw, and the
  ledger expressly denies a source heading element.
- The eight numbering-sensitive records for Psalms 9-10, 114-116, and 147 carry both
  `LXX_WITNESS_GAP` and `unresolved_no_scoped_greek_lxx_witness`. All 283 decisions set
  `greek_lxx_source_available: false`.
- Source locators are correctly fenced from authority in all 283 alignments:
  `authority` is `translation_versification_metadata_not_boundary_authority`,
  `locator_existence_is_not_boundary_evidence` is true, and `selah_boundary_authority` is false.
  All 71 referenced Selah occurrences were independently found inside their exact mapped OSHB
  segments.

### Repairable source-evidence failures

1. `M7_sol-Ps-199` and `M7_sol-Ps-200` give the Hebrew review
   `feature_kind: mapped_lexical_formula`, but both have an empty
   `observed_poetic_features` array. `Ps-199` also claims that WEB 110:4 maps to the Hebrew oath
   opening even though its chunk-local ordered mapping ends at 110:3; only the WEB right-context
   observation is present. The formula itself is real: OSHB MT 110:4 opens
   `נִשְׁבַּ֤ע יְהוָ֨ה`, and the review's form is accurate after stripping cantillation. Add a
   mapped neighbor locator, a feature record, and an explicit normalization declaration.
2. `M7_sol-Ps-245` gives the Hebrew review `feature_kind: mapped_lexical_pair` while its
   `observed_poetic_features` array is empty. Its ordered mapping contains MT 132:2 and 132:11 and
   the paired-oath claim is textually correct, but the review lacks the feature object that should
   cite and compare those mapped source segments.
3. `M7_sol-Ps-166` and `M7_sol-Ps-167` cite OSHB segments but store a normalized
   `observed_sequence` without naming the text witness or declaring that cantillation and OSHB
   morpheme separators were omitted. The syntax finding is correct; its quotation provenance is
   incomplete. Record either exact OSHB text or the witness plus deterministic normalization.

### Verdict and scope

**FAIL-REPAIRABLE for source-evidence linkage; no overall pass.** The exhaustive WEB and
WEB-to-MT citation repairs are sound, and the named Psalms edge cases are substantively faithful,
but the five decisions above need provenance repairs before a Hebrew-source pass.

This verdict is source-fidelity only. It does not cure the separately reported semantic-shell
failure in which most child rationales and rejected alternatives remain generated constructors.
Source-correct quotations and locators cannot make templated literary reasoning individualized.
