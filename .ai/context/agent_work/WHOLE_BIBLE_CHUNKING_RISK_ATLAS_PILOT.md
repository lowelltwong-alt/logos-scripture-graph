# Whole-Bible Chunking Risk Atlas (Pilot)

**Status:** `research_only_non_authorizing`
**Contract scope:** `planning_only`
**Governance authority:** `false`
**Corpus:** canonical_66 / eng-web (`data/raw/bible/eng-web/usfm/eng-web_usfm.zip`)
**Pilot scope:** raw-source glossary + Strong's handling notes + Torah (Genesis–Deuteronomy) + scaling method
**Generated:** 2026-06-29 (Cursor agent work; not control-plane authority)
**Location:** `.ai/context/agent_work/` — does not supersede `.ai/control/` surfaces

**Does not authorize:** chunk output, reviewed gold, implementation targets, route/evaluator
behavior, graph/retrieval/vector truth, boundary import, backend choice, retrieval-profile
promotion, source/manuscript rows, canon-scope change, or theology authority.

This atlas **synthesizes** governed research surfaces for human and Codex triage. It is not a
chunking algorithm, review packet, or promotion record.

---

## Method & limitations

This pilot was produced from governed repo surfaces plus the 2026-06-04
`.ai/control/RAW_SOURCE_INVENTORY.md` scan. Cursor did not read the full raw USFM archive
character by character, did not open every eng-web USFM book end to end, and did not verify every
Torah verse in situ against raw markers.

Marker counts in this file are quoted from `RAW_SOURCE_INVENTORY.md` and
`config/ingest/usfm_marker_coverage.yaml`. Torah risk labels are a cross-walk of T358, T386, T402,
and gap-register surfaces, not a per-verse raw-text verification pass.

Book-level and example-span labels are agent triage judgments for review planning only. They are
not governed classifications and do not authorize target selection, review packets, chunk output,
reviewed gold, theology claims, graph or retrieval truth, or control-plane promotion.

---

## Risk category vocabulary

| Category | Meaning | Chunking implication |
|----------|---------|----------------------|
| `low_risk` | Structurally bounded; low variant/speaker/intertext/theology pressure; parent-only review candidate plausible | May align with T402 `ready_for_review_packet` after **owner** supplies exact target; never auto-chunk |
| `medium_risk` | Bounded but needs context, original-language review, metadata review, or book/canonical framing | Research/context before review packet; often T402 `needs_context_research` |
| `high_risk` | Theological, variant, WJ/speaker, intertext, covenant/law-gospel, Christology, or canon-scope pressure; likely owner gate | Hold or owner decision; not Cursor low-risk prep |
| `complex` | Not suitable for Cursor prep; needs Codex/owner/dedicated research gate | No review packet until dedicated pass |

**Assignment rule:** Every category cites observable raw or governed evidence and explains why.
Metadata density alone never upgrades or downgrades risk to authority.

**Book vs span:** Book-level default risk and example span-level risk are **separate**. A book
marked `complex` does not invalidate a structurally bounded T402 low-complexity span inside it
(e.g. Gen.5 genealogy vs Gen.1 creation).

---

## Section A — Raw-source marker and symbol glossary

**Sources:** `.ai/control/RAW_SOURCE_INVENTORY.md` (scan 2026-06-04),
`config/ingest/usfm_marker_coverage.yaml`, enforced by `scripts/validate_raw_coverage.py`.

**Raw archive snapshot (eng-web full archive):** 83 USFM files, 38,058 verses, 1,402 chapters,
677,688 Strong's lexeme tags on `\w` (Hebrew 514,990 / Greek 162,698). This is the raw WEB archive
superset, including non-canonical/front-matter material. The governed `canonical_66` corpus remains
the 66-book, 31,103-verse scope; do not treat the 38,058 raw-archive count as canon-scope authority.

### A.1 Marker families and chunking risk if misread

| Marker family | Examples | eng-web count | `handling` | Chunker relevant | Risk if misread as authority |
|---------------|----------|---------------|------------|------------------|------------------------------|
| Reference structure | `\id`, `\c`, `\v` | 83 / 1,402 / 38,058 | book_id, chapter, verse | yes | Treating verse or chapter as discourse or meaning unit |
| Paragraph prose | `\p`, `\m`, `\mi`, `\pi1`, `\pc`, `\nb` | 9,254+ `\p` | paragraph | yes | Editorial paragraph = ancient discourse boundary |
| Poetry / liturgy | `\q1`, `\q2`, `\q3`, `\b` | 10,094 / 13,237 / 1,070 | poetry_line, stanza_break | yes | Mid-colon or mid-stanza splits (sparse in Torah) |
| Psalm superscription | `\d` | 139 | superscription | yes | Title genre label becomes doctrine or boundary |
| Headings / titles | `\mt1`, `\mt2`, `\mt3`, `\ms1`, `\s1` | 84 / 41 / 7 / 5 / 5 | major_title, heading | yes | Section heading defines pericope theology |
| Lists | `\ili`, `\li1` | 98 / 72 | list | yes | List item = independent theological unit without context |
| Inline lexeme | `\w` + `strong="G####"/"H####"` | 1,355,376 `\w` occurrences | inline_lexeme | yes | Strong's tag = lexical truth or chunk boundary |
| Footnotes | `\f`, `\fr`, `\ft`, `\fl`, `\fq` | 3,710 `\f` | footnote | yes (container) | Footnote text = preferred reading or doctrine |
| Alternate reading | `\fqa` | 519 | variant_reading | yes | Variant note = canon or textual-critical decision |
| Cross-reference | `\x`, `\xo`, `\xt` | 726 `\x` | crossref | yes | Editorial `\x` = graph edge or fulfillment claim |
| Words of Jesus | `\wj` | 4,580 | words_of_jesus | yes | Red-letter = speaker attribution (NT; absent in Torah) |
| Speaker label | `\sp` | 33 | speaker | yes | Speaker tag = reviewed speaker boundary (Job/Song) |
| Selah / rubric | `\qs` | 148 | variant_reading (Selah) | yes | Liturgical rubric governs chunk (mostly Psalms) |
| Glossary inline | `\k`, `\wh`, `\bk` | 188 / 160 / 94 | glossary, inline_format | mostly no | Glossary gloss = lexical or theological authority |
| Metadata / TOC | `\toc1`, `\h`, `\ide`, `\ip`, `\is1` | varies | metadata, running_header, intro | mostly no | Front matter mistaken for canonical text |

### A.2 Weird symbols and inline syntax (read before risk claims)

**Strong's on `\w`:** Words appear as `\w word|strong="H1234"` or `strong="G1234"`. The number
is a lexeme tag for sidecar ingest, not proof of meaning in isolation. Torah text is predominantly
Hebrew-tagged; Greek tags dominate NT books.

**Footnote subfields:** `\f` contains nested `\fr` (reference), `\ft` (text), `\fl` (label),
`\fq` (quotation). `\fqa` marks alternate/variant reading text — a **textual-variant seed**, not
a preferred reading selection.

**Cross-reference subfields:** `\xo` (origin), `\xt` (target citation). These are editorial
crossrefs; they must not auto-become `quotesFrom`, `fulfills`, or chunk boundaries per
`MASTER_CONTEXT.md` and `source_metadata_research_atlas.yaml`.

**`\wj` … `\wj*`:** Marks words attributed to Jesus in WEB red-letter tradition. Chunking must
not treat marker extent as reviewed speaker boundary without owner policy (Gospel lane).

**`\sp`:** Speaker label (e.g. Job dialogue). Evidence only until speaker policy review.

**`\qs` (Selah):** Liturgical rubric, mostly Psalms. Not a discourse boundary by itself.

**`\d`:** Descriptive title / superscription (Psalms). Keep with psalm unit; do not use as
genre theology.

**Torah USFM profile (pilot inference; not raw-verified in this session):** Based on genre
expectations and governed rollups, Torah likely relies heavily on `\p`, `\c`, `\v`, `\w`, section
headings where present, and list markers (`\ili`, `\li1`) in legal sections. This pilot did not
perform per-book marker recounts from raw USFM. Torah includes poetry and oracle sections such as
Exodus 15, Numbers 23-24, and Deuteronomy 32-33, so `\q*` and `\b` marker presence must be checked
per passage before use. `\wj` is not expected in Torah, but all marker claims remain evidence-only
and not boundary authority.

### A.3 Evidence-only rule (all markers)

Per `bible_chunking_research_triage_map.yaml` `evidence_rules` and `CHUNK-METADATA-001`:

- Source metadata, crossrefs, headings, speaker markers, capitalization, and Strong's tags are
  **evidence only**.
- They do not authorize Scripture truth, lexical truth, intertext truth, speaker attribution,
  graph edges, chunk boundaries, reviewed gold, or output changes.

---

## Section B — Strong's / Greek / Hebrew metadata handling

**Sources:** `original_language_phrase_context_policy.yaml`, `source_metadata_research_atlas.yaml`,
`RAW_SOURCE_INVENTORY.md`.

| Observation | Handling | Chunking risk |
|-------------|----------|---------------|
| 677,688 Strong's-style tags on `\w` | Preserve as `WordToken` evidence | Isolated lemma or rarity used to set boundary or doctrine |
| Hebrew 514,990 / Greek 162,698 split | Tag language follows source word, not English surface alone | Wrong-language OL claim in review packet |
| No governed WLC/SBLGNT morphology in current eng-web corpus | Phrase/clause/discourse context required before OL affects review | Word-study smuggling (T381 warning) |
| Lexical rarity in metadata | May surface for review queue only | Rarity implies theological weight |
| Divine-name capitalization in tokens | Translation/editorial evidence (T386 flags) | Capitalization pattern implies Trinity or identity doctrine |

**Torah pilot note:** Genesis shows 31 passages with `known_non_orthodox_pressure_passage` and
`original_language_phrase_context_review` per T386 readiness matrix — OL metadata must not be used
to answer pressure-passage arguments in chunk boundaries.

**Required before OL affects any future review packet:** phrase, clause, syntax, discourse, genre,
textual, and canonical context per T381; governed source-language witness is a future horizon per
`MASTER_CONTEXT.md`.

---

## Section C — Torah book-by-book risk summary (pilot)

**Cross-walk sources:** `bible_wide_chunking_research_registry.yaml` (T358),
`bible_verse_passage_readiness_matrix.yaml` (T386), `whole_bible_low_complexity_chunking_candidate_queue.yaml`
(T402), `bible_verse_passage_gap_register.yaml` (T386 gaps).

Book-level atlas risk labels are Cursor/Codex triage judgments synthesized from T386, T358, and
T402 evidence. They are not governed classifications and do not authorize target selection, review
packets, or output.

### C.1 Summary table

| Book | T386 status rollup | T402 candidate | Book-level atlas risk | Example span risk | Why (evidence) |
|------|-------------------|----------------|----------------------|-------------------|----------------|
| Gen | 1502 deeper_review; 31 human_decision | T402-LC-001 `ready` (Gen.5.1–32) | **complex** | Gen.5.1–32: **low_risk** | Creation/theophany/OL pressure dominate book; genealogy list structurally bounded |
| Exod | 1042 routine; 171 deeper_review | T402-LC-002 `ready` (Exod.35.4–29) | **medium** | Exod.35.4–29: **low_risk** | Tabernacle offering list bounded; Sinai/divine-name/intertext hotspots elsewhere |
| Lev | 686 routine; 173 deeper_review | T402-LC-003 `needs_context` | **medium–high** | Lev.11.1–47: **medium_risk** | Ritual/holiness law; covenant/food-law theology pressure flags |
| Num | 1190 routine; 98 deeper_review | T402-LC-004 `ready` (Num.1.1–46) | **medium** | Num.1.1–46: **low_risk** | Census list text-local; narrative/oracle complexity elsewhere |
| Deut | 280 routine; 671 deeper_review; **2 blocked**; 6 human_decision | T402-LC-005 `needs_context` | **high** | Deut.27.11–26: **medium_risk** | Covenant speech/law corpus; Deut.32 variant + blocked passages |

### C.2 Genesis

- **Registry lanes:** `narrative_pericope`; secondary: `legal_covenant`, `genealogy`, `source_metadata_features`
- **Metadata watchpoints:** section headings, genealogies, divine names, crossrefs
- **T386 flags:** divine_name (1033), OL pressure (31), theological_downstream (1533), review_packet_needed (1533)
- **USFM profile:** prose `\p` dominant; genealogies use list-like structure; Strong's on most verses

**Passage/feature examples:**

| Ref / feature | Category | Why |
|---------------|----------|-----|
| Gen.1.1–Gen.1.27 | **high_risk** | T386-GAP-003 divine_name capitalization samples; creation discourse; OL pressure passages |
| Gen.5.1–Gen.5.32 (T402-LC-001) | **low_risk** | Genealogy formulae; T402 `ready_for_review_packet`; genealogy theology explicitly not authorized |
| Gen.12–Gen.17 (registry candidate) | **complex** | Covenant promise narratives; registry flags covenant continuity risks |
| Gen.22 (binding of Isaac) | **high_risk** | Theological downstream; not a low-complexity auto-candidate |

### C.3 Exodus

- **Registry lanes:** `legal_covenant`; secondary: `narrative_pericope`, `worship_tabernacle`
- **Metadata watchpoints:** section headings, divine names, crossrefs, paragraph markers
- **T386 flags:** cross_reference_or_intertext (2), divine_name (693), review_packet_needed (169)

**Passage/feature examples:**

| Ref / feature | Category | Why |
|---------------|----------|-----|
| Exod.19.5–Exod.19.6 | **high_risk** | T386-GAP-002 cross_reference_or_intertext_risk sample; covenant language |
| Exod.35.4–Exod.35.29 (T402-LC-002) | **low_risk** | Offering instruction list; typology/law-covenant flags non-authorizing in T402 |
| Exod.3–Exod.4 (registry candidate) | **medium_risk** | Theophany + divine name; needs context before packet |
| Exod.25–Exod.31 (tabernacle instructions) | **medium_risk** | Long instruction block; worship theology not boundary authority |

### C.4 Leviticus

- **Registry lanes:** `legal_covenant`; secondary: `ritual_law`, `holiness_code`
- **T386:** 173 deeper_review; law/theology flags on review_packet_needed (172)

**Passage/feature examples:**

| Ref / feature | Category | Why |
|---------------|----------|-----|
| Lev.11.1–Lev.11.47 (T402-LC-003) | **medium_risk** | T402 `needs_context_research`; clean/unclean list visible but law/gospel/covenant flags |
| Lev.16 (Day of Atonement) | **high_risk** | Registry future candidate; atonement theology pressure |
| Lev.17–Lev.26 (Holiness Code) | **medium–high** | Sustained legal corpus; repeated formulae need book context |

### C.5 Numbers

- **Registry lanes:** `narrative_pericope`; secondary: `legal_covenant`, `census`, `wilderness_journey`
- **T386:** mostly routine (1190); 96 theological_downstream flagged

**Passage/feature examples:**

| Ref / feature | Category | Why |
|---------------|----------|-----|
| Num.1.1–Num.1.46 (T402-LC-004) | **low_risk** | Census list; T402 ready; tribal theology not authorized |
| Num.13–Num.14 (spy narrative) | **medium_risk** | Narrative scene; faith/rebellion themes need context |
| Num.22–Num.24 (Balaam oracles) | **medium–high** | Oracle units; intertext and prophecy framing |

### C.6 Deuteronomy

- **Registry lanes:** `legal_covenant`; secondary: `discourse_argument_flow`, `covenant_speech`
- **T386:** 2 `blocked_before_chunking`; 8 human_owner_decision; variant_sensitive (2)

**Passage/feature examples:**

| Ref / feature | Category | Why |
|---------------|----------|-----|
| Deut.32.8–Deut.32.9 | **high_risk** | T386-GAP-001 blocked_authority_action sample; textual_variant_source_tradition |
| Deut.27.11–Deut.27.26 (T402-LC-005) | **medium_risk** | Curse list structurally clear; T402 needs_context; covenant/law-gospel flags |
| Deut.5–Deut.11 (covenant speech) | **high_risk** | Registry candidate; law/gospel and covenant theology pressure |
| Deut.6.4 (Shema) | **high_risk** | Divine-name and monotheism pressure; not low-complexity |

---

## Section D — Scaling method (remaining 61 books)

**Do not execute in pilot.** Use this workflow per batch (5–8 books max per edit).

1. **Book pull:** `bible_wide_chunking_research_registry.yaml` entry + `bible_verse_passage_readiness_matrix.yaml` row + T402 queue row if present.
2. **Lane map:** Align to `bible_chunking_research_triage_map.yaml` lane (`psalms_poetry`, `revelation_apocalyptic`, `epistle_argument`, `narrative_pericope`, `legal_covenant`, `gospel_discourse_wj`, etc.).
3. **Flag rollup:** Top `flag_counts` from T386 matrix; sample refs from `bible_verse_passage_gap_register.yaml`.
4. **Raw-source overlay:** Dominant USFM markers by genre (see table below).
5. **Assign risks:** Book-level default + 2–4 example spans (never conflate).
6. **Stop:** Owner/Codex approval before next batch.

### D.1 Genre → dominant raw markers (eng-web)

| Genre / lane | Dominant markers | Typical chunking pressure |
|--------------|------------------|---------------------------|
| Torah narrative/law | `\p`, `\v`, `\w`, `\ili`/lists | Pericope vs law block; divine names |
| Historical narrative | `\p`, headings | Scene boundaries vs chapter breaks |
| Psalms / poetry | `\q1`, `\q2`, `\b`, `\d`, `\qs` | Whole-psalm vs stanza; Selah |
| Prophets | `\p`, `\q1`, oracle headings | Oracle units vs editorial chapters |
| Gospels | `\p`, `\wj`, `\x` | Speaker/WJ boundaries; pericopes |
| Epistles | `\p`, `\w` (Greek tags) | Argument chains vs greeting/closing |
| Apocalyptic | `\p`, symbols, `\x` | Vision cycles; intertext; **complex** lane |

### D.2 Proposed expansion order (after pilot approval)

1. **Joshua–Judges** — `narrative_pericope` lane; moderate T386 routine share
2. **Psalms** — `governed_hold` in triage map; poetry markers critical
3. **Pauline epistles** — `review_packet_ready` lane; argument-boundary risk
4. **Revelation** — `research_first`; do not fast-track

### D.3 Relationship to existing control surfaces

| Surface | Role for atlas | Atlas must not |
|---------|----------------|----------------|
| T398 phase-one synthesis | Whole-corpus accounted at triage depth | Claim deep exegesis complete |
| T399 focused queue | Ranked high-risk passages | Select implementation target |
| T402 low-complexity queue | Span-level review eligibility | Auto-chunk or Cursor-select |
| T359 metadata atlas | Canonical sidecar counts/policies | Duplicate as authority |
| This pilot file | Agent-work synthesis for Codex | Promote to `.ai/control/` without review |

---

## Section E — Stop conditions, open questions, recommended actions

### E.1 Stop conditions

Stop work immediately if:

- Cursor or agent would **choose** a chunking implementation target without owner/Codex supply
- Any edit is requested under `data/raw/`, `data/canonical/`, `data/derived/`, `eval/chunking_gold/`,
  `.ai/control/`, chunk pipelines, routes, or evaluators
- Atlas categories are treated as reviewed gold, chunk boundaries, or theology authority
- Expansion beyond Torah pilot is attempted without owner/Codex approval
- Metadata alone is used to justify doctrine, preferred readings, graph edges, or boundaries

### E.2 Unresolved questions

1. **Book `complex` vs span `low_risk`:** Recommend keeping separate (pilot uses this rule); confirm with owner.
2. **Machine-readable YAML sidecar** in `agent_work/` for later batches — defer until batch 2.
3. **`scan_raw_sources.py --check`:** Raw unchanged since 2026-06-04 inventory; re-scan only if `data/raw/` changes.
4. **Canonical sidecars locally absent:** Torah current-chunk tables deferred; T386 used instead.

### E.3 Recommended next Codex / owner actions

1. **Codex:** Review this pilot diff; confirm glossary and Torah assignments are evidence-only.
2. **Owner:** Approve next atlas batch (Joshua–Judges or Poetry).
3. **Promotion:** If glossary items should enter `source_metadata_research_atlas.yaml`, open a
   **separate** Codex-reviewed PR to `.ai/control/` — not from this file alone.
4. **Chunking:** No target selection from this atlas; use T402 + owner supply for low-risk prep.

---

## Dependencies cited

- `.ai/control/RAW_SOURCE_INVENTORY.md`
- `config/ingest/usfm_marker_coverage.yaml`
- `.ai/control/source_metadata_research_atlas.yaml`
- `.ai/control/contextual_reading_policy.yaml`
- `.ai/control/original_language_phrase_context_policy.yaml`
- `.ai/control/bible_wide_chunking_research_registry.yaml`
- `.ai/control/bible_chunking_research_triage_map.yaml`
- `.ai/control/bible_verse_passage_readiness_matrix.yaml`
- `.ai/control/bible_verse_passage_gap_register.yaml`
- `.ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml`
- `.ai/control/t398_bible_wide_phase_one_research_synthesis.yaml`
- `.ai/control/t399_focused_bible_wide_research_queue.yaml`
- `.ai/control/chunking_agent_preflight.yaml`
- `.ai/control/chunking_lesson_index.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/bible_chunking_readiness_map.yaml`
- `docs/chunking/CHUNKING_DESIGN.md`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `AI_FRONT_DOOR.md`, `AGENTS.md` (governance repo conventions mirrored in scripture graph workflow)
