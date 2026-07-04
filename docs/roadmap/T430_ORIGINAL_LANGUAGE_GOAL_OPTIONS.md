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
- confidence notes and reuse/license status;
- gaps where only catalog metadata is allowed.

Best first pilot:

- Philemon for NT manuscript-chain mechanics, or Jonah for Hebrew witness/source-family mechanics.

Why this matters:

- It starts the "chain of custody" layer the user wants: how we know the text, where witnesses are, and where uncertainty remains.

Stop conditions:

- do not download manuscript images or transcriptions unless terms are cleared;
- "oldest witness" is evidence, not automatic authority;
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

Best first candidates:

- `1Cor.15.3-1Cor.15.8`;
- `Phil.2.6-Phil.2.11`;
- `Rom.1.3-Rom.1.4`;
- `1Tim.3.16`.

Why this matters:

- It supports the user's long-term goal of tracing how early Christian tradition material appears in the biblical text.
- Claims such as "months after the resurrection" require a dedicated evidence packet, source citations, and frontier review. T430 does not assert that conclusion by itself.

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
