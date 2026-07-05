# T430 Original-Language Goal Options

Status: planning options, evidence-only.
Task family: T430-T437.

This file gives future agents five defensible goal options from the current T431 raw-intake point. None of these options authorizes preferred readings, canon changes, theology authority, KG edges, reviewed gold, chunk output, retrieval truth, or source-tradition preference.

## Common Ground

T431 has two layers:

- immutable raw source packages under `data/raw/original_language/`;
- candidate canonical-only source views under `data/candidate/original_language_evidence/canonical_source_views/`.

Future work must consume the canonical source views by default, not raw archives directly. Raw archives contain extra documentation, code, media, metadata, duplicate formats, and unselected variants.

Strong's numbers are lookup and alignment hints. They are not Greek/Hebrew source text, lexical authority, theology authority, or proof that a translation decision is correct.

## Five Goal Options From Here

These are not mutually exclusive forever. They are owner-facing routes for deciding what the next implementation lane should optimize for.

1. Build the Greek/Hebrew-to-English alignment bridge first.
2. Build the manuscript witness chain and confidence atlas first.
3. Build the variant/copying-error transparency ledger first.
4. Build the early-creed and tradition-formula research lane first.
5. Build the integrated original-language evidence workbench after the smaller lanes prove themselves.

Recommended order: Option 1 first, Option 2 in parallel as catalog-only research, then Options 3 and 4 as evidence packets, then Option 5 as the integrated product. This gives the repo useful source-token scaffolding quickly while still preserving the long-term custody-chain goal.

## Owner Decision Menu

| Option | Short name | Main question it answers | First defensible output | Best first pilot | Completion signal |
|---|---|---|---|---|---|
| 1 | Alignment bridge | How does the current English wording relate to the Hebrew, Aramaic, or Greek source-token evidence we have? | candidate source-token and English-token alignment records | Philemon or Jonah | every pilot token/alignment row has source view, checksum, confidence, and non-authority fields |
| 2 | Manuscript custody chain | What witnesses, fragments, editions, and catalogs support this passage, and where are the gaps? | metadata-only passage witness coverage packet | Philemon or Jonah | oldest-known evidence, highest-confidence evidence, gaps, and rights limits are separated |
| 3 | Variant/error ledger | What known copying, spelling, omission/addition, punctuation, or editorial issues touch this span? | candidate variant/copying-error transparency rows | one tiny variant-sensitive span | every issue traces to a witness, edition, or catalog source without choosing a preferred reading |
| 4 | Early creed lane | Which passages may preserve early creed, confession, hymn, or tradition-formula material, and why? | non-authorizing research packet with cited pro/con views | `1Cor.15.3-1Cor.15.8` | claims about timing, formula language, and early tradition are cited, bounded, and frontier-reviewed |
| 5 | Integrated workbench | How do alignment, manuscripts, variants, translation notes, and early-tradition evidence appear together? | combined evidence dashboard after pilots | after Options 1-4 prove fields | the dashboard exposes uncertainty instead of compressing it into one hidden score |

T438 route update: Option 1 is now the selected next implementation lane as a planning/control gate, while Option 2 may continue as catalog-only research in parallel. This does not authorize production source-token rows, production alignment rows, source-language truth, translation-faithfulness judgments, preferred readings, source-tradition choices, witness-support rows, KG/retrieval truth, or theology authority.

Recommended owner choice from here: implement the Option 1 lane through the T439/T440/T441/T442 sequence, while allowing Option 2 to continue as catalog-only research in parallel. That gets the repo to useful Greek/Hebrew and English linking quickly, while laying the track for the richer chain-of-custody system.

The long destination is the Option 5 workbench: a passage-level evidence view that can eventually show source tokens, English alignments, manuscript witnesses, variant/copying-error trails, translation-faithfulness notes, and early-creed research packets side by side. It should be assembled from validated smaller lanes rather than built as one giant trust-me artifact.

## Option 1: Greek/Hebrew To English Alignment Bridge

Goal: build the first evidence bridge from Hebrew/Aramaic/Greek source tokens to the current English WEB layer.

Primary outputs:

- source-token candidates per verse;
- WEB token alignment candidates;
- Strong's/lemma/morphology evidence overlay;
- confidence and provenance fields for every alignment;
- disagreement queues where source packages or alignments diverge.

Best first pilot:

- Philemon for Greek, or Jonah for Hebrew.

Why this first:

- It creates the practical foundation for translation-faithfulness checks and later KG enrichment.
- It is smaller than manuscript-level reconstruction and can validate the source-view pipeline quickly.

Stop conditions:

- no preferred reading;
- no claim that Strong's reconstructs the original text;
- no translation judgment without a later owner-gated rubric.

## Option 2: Manuscript Witness Chain And Confidence Atlas

Goal: show what manuscript, fragment, edition, and catalog evidence supports each passage or book segment.

Primary outputs:

- witness catalog rows;
- passage coverage by witness;
- approximate date ranges;
- material type, language, and repository/source links;
- oldest-known-witness notes and highest-confidence-witness notes, kept separate;
- confidence notes and reuse/license status;
- gaps where only catalog metadata is allowed.

Target custody-chain depth:

1. book and passage coverage;
2. verse or phrase coverage where catalog data supports it;
3. witness or fragment identifier, date range, language, material, repository, and source URL;
4. edition or catalog source used to map the witness to the passage;
5. known variants, spelling differences, omission/addition evidence, punctuation/editorial differences, and confidence notes;
6. whether the row is observed from source data, inferred from a catalog, or blocked by licensing/rights;
7. downstream consequence notes for source-language alignment, translation comparison, KG, retrieval, and chunking.

Best first pilot:

- Philemon for NT manuscript-chain mechanics, or Jonah for Hebrew witness/source-family mechanics.

Why this matters:

- It starts the "chain of custody" layer the user wants: how we know the text, where witnesses are, and where uncertainty remains.
- It should eventually support a passage-by-passage custody trail down to spelling, omission/addition, punctuation/editorial, and other minute-error classes where the evidence permits.
- It separates "oldest known evidence" from "highest confidence evidence" so future agents do not accidentally treat age alone as authority.

Stop conditions:

- do not download manuscript images or transcriptions unless terms are cleared;
- "oldest witness" is evidence, not automatic authority;
- "highest confidence" must explain why, and must not hide minority evidence;
- do not silently choose between Byzantine, Alexandrian, Masoretic, DSS, LXX, Samaritan, or other traditions.

## Option 3: Variant And Copying-Error Transparency Ledger

Goal: represent known variants, spelling differences, punctuation/editorial differences, omissions, additions, and uncertainty without flattening them into one hidden answer.

Primary outputs:

- textual variant candidate rows;
- affected verse/span;
- witnesses or edition sources;
- variant class and confidence;
- whether the issue is spelling, word order, omission/addition, punctuation/editorial, or meaning-bearing;
- downstream caution notes for chunking, retrieval, KG, and translation comparison.

Best first pilot:

- a tiny variant-sensitive NT sample after source/license review, or a Hebrew sample with known textual-tradition pressure.

Why this matters:

- It makes future copying-error claims auditable instead of relying on model memory or a single edition.

Stop conditions:

- no preferred reading until owner-gated textual-critical policy exists;
- no apologetic, skeptical, liberal, or conservative backdoor claims;
- every asserted variant must trace to a source, witness, or edition note.

## Option 4: Early Creed And Tradition-Formula Research Lane

Goal: identify candidate early Christian creed, confession, hymn, or tradition-formula passages and trace the evidence for how scholars date and classify them.

Primary outputs:

- candidate passage docket;
- formula markers such as "received/delivered" language where present;
- source-language and discourse evidence;
- scholarly-source packet with agreement/disagreement;
- manuscript and edition evidence links where relevant;
- confidence, unresolved questions, and downstream risks.
- explicit separation between manuscript evidence, source-language discourse evidence, and scholarly historical argument.

Required evidence separation:

- manuscript or edition evidence: what witnesses show the passage is in the textual tradition;
- source-language/discourse evidence: formula markers, parallel structures, quoted/delivered language, hymnic or confessional form;
- historical argument: scholarly reasoning about pre-Pauline, early church, liturgical, or oral-tradition origin;
- downstream consequence: what the claim would affect if later promoted into an atlas or KG.

Best first candidates:

- `1Cor.15.3-1Cor.15.8`;
- `Phil.2.6-Phil.2.11`;
- `Rom.1.3-Rom.1.4`;
- `1Tim.3.16`.

Why this matters:

- It supports the user's long-term goal of tracing how early Christian tradition material appears in the biblical text.
- Claims such as "months after the resurrection" require a dedicated evidence packet, source citations, and frontier review. T430 does not assert that conclusion by itself.
- The lane should preserve contrary scholarly views and confidence limits so apologetic or skeptical pressure cannot become hidden data.
- The target is not to smuggle a conclusion into the data. The target is to make the evidence trail strong enough that a later human/frontier review can see exactly what is known, what is argued, and what remains disputed.

Stop conditions:

- no doctrinal assertion as data;
- no dating claim without cited reasoning and confidence;
- frontier review required before any high-impact claim enters an atlas or KG.

## Option 5: Integrated Original-Language Evidence Workbench

Goal: combine Options 1-4 into one later user-facing evidence layer after the smaller pilots are validated.

Primary outputs:

- per-book evidence dashboards;
- source-token to English alignment;
- manuscript witness coverage;
- variant transparency;
- translation-faithfulness notes;
- confidence, provenance, and open-dispute trails;
- export surfaces for KG and retrieval only after owner authorization.

Best first path:

1. finish Option 1 pilot;
2. add Option 2 witness pilot;
3. add Option 3 variant pilot;
4. add Option 4 early-creed packet pilot;
5. integrate only the validated fields into a combined workbench.

Why this last:

- It is the richest target, but it should not come before the evidence schemas, licensing rules, and validators are proven.

Stop conditions:

- no full-Bible manuscript claims before source catalog and licensing are validated;
- no KG edges or retrieval truth until a later owner-gated promotion task;
- no "single confidence score" that hides variant, translation, and manuscript uncertainty.

## Recommended Route From Here

Default next move: Option 1 as T432/T433, with a small Philemon or Jonah pilot.

Parallel planning move: Option 2 catalog expansion can proceed read-only while Option 1 builds alignment schemas.

Hold for later: Options 3 and 4 need stronger source-license and citation rules before any data beyond planning packets.

The long-range destination is Option 5, but the safe path is to assemble it from audited smaller lanes.
