# OWNER GATE — New Testament / Greek Preflight (v1.1)

**Authority: Lowell Wong, 2026-07-30; amended 2026-07-31 after the Matthew first-Gospel review.
Binding for every model slot (M7_sol, M8_fable, M9+, any future rerun) and for ALL 27 New
Testament books — the entire NT is Greek; no NT book is outside this gate.**

**RE-READ RULE (v1.1): Because model context clears between books, this gate must be re-read at
the START OF EVERY NT BOOK — not only the first. Re-pin the current file sha256 in your
model_manifest under `nt_greek_preflight_gate` each time. A completion receipt for any NT book
that does not re-pin this gate's current hash is invalid.**

## Per-book NT requirements (v1.1 — added from the Matthew review; binding every NT book)

1. **Demonstrate the Greek, don't assert it.** Any boundary-relevant original-language claim must
   QUOTE the actual Greek form (e.g. καὶ εὐθύς, ἤρξατο λέγειν, a γενομένης δέ frame, τότε at an
   episode seam) — the way the OT reviews quote Hebrew. `direct_read:sblgnt` refs without a single
   quoted Greek form are insufficient evidence of engagement. (Matthew finding: 0/94 packets
   quoted any Greek.)
2. **Cite tiers per packet.** Every non-textual signal cited in every review packet lists its tier
   (1–4) inline. (Matthew finding: 0/94 packets did this despite the manifest acknowledgment.)
3. **Genuine adversarial pressure.** Reviewers must challenge genuinely contestable seams —
   transitional pericopes, Markan sandwiches, parable-cluster internal seams, travel-narrative
   joins — not reflex-support. (Matthew finding: 2 challenges in 188 primary reviews, implausibly
   soft next to Psalms' 153/566.)
4. **Matthew follow-up rows** for items 1–2 are logged as append-only deltas; Matthew itself is
   accepted and is NOT reworked.

## Why this gate exists

Every model in this campaign learned its boundary discipline on the Hebrew Bible, where the
Masoretic layer (petuchah/setumah, accents) at least reflects an ancient scribal tradition.
**The Greek New Testament has no Masoretic layer.** The nearest-looking substitutes are far
weaker, and the predictable failure mode is treating modern editorial paragraphing as if it were
ancient structure. It is not.

## Tier rules for the NT (extends scribal_and_editorial_layer_weights)

**Tier 1 — the text's own signals; may drive a boundary:**
- discourse connectives and shifts (καί / δέ / οὖν / τότε / μετὰ ταῦτα patterns at episode scale)
- speech frames and quotation formulas (ἀμὴν λέγω ὑμῖν, ἀποκριθεὶς εἶπεν, ἤρξατο λέγειν)
- explicit scene / participant / location / time changes (travel notices, ἐγένετο δέ frames)
- parable frames and their interpretations (never sever a parable from its interpretation)
- epistolary formulae: greeting, thanksgiving/prayer, body-opening (παρακαλῶ δέ, οὐ θέλω ὑμᾶς
  ἀγνοεῖν), paraenesis shift, travelogue, greetings list, doxology, benediction
- argument movement markers (διό, ἄρα οὖν, τί οὖν ἐροῦμεν) at unit scale
- inclusio, refrain, sevenfold/cyclical structures (Revelation), genealogy/list formulas
- vocatives and direct-address shifts (ἀδελφοί, τεκνία) when they open a unit
- OT quotation blocks with their introduction formulas (γέγραπται, ἵνα πληρωθῇ) — the frame is
  tier-1 evidence; the quotation's OT origin is a typed relation, never boundary authority

**Tier 2 — strong corroboration; cannot drive a boundary alone:**
- genitive absolutes at genuine scene seams
- major uncial paragraphing where witnesses agree (e.g. Vaticanus/Sinaiticus section practice),
  WITH the witness named
- kephalaia / Eusebian sections (ancient, but reading aids — corroboration only)

**Tier 3 — weak corroboration:**
- single-witness ancient paragraphing; disputed kephalaia divisions

**Tier 4 — metadata only; NEVER boundary evidence, and NEVER counterevidence by absence:**
- NA28 / UBS5 / SBLGNT / THGNT paragraphing and pericope headings (20th–21st-century editorial)
- chapter divisions (Langton, 13th c.) and verse divisions (Estienne, 16th c.)
- modern section headings in any translation (including WEB)
- red-letter / words-of-Jesus marking, cross-references, footnotes, Strong's numbers
- versification differences between editions (record as crosswalk metadata)

## NT-specific holds (never decide; hold with an answerable human question)

- Mark 16:9–20 (longer ending) · John 7:53–8:11 (pericope adulterae) · Luke 22:43–44 ·
  Acts 8:37 · Rom 16:25–27 placement · 1 John 5:7–8 (Comma) — variant zones: chunk around them
  without selecting a reading; hold the affected seam.
- Synoptic parallels: record as typed relations (decision_relations), never as boundary
  authority. Matthew's seam is decided from Matthew's text, not from Mark's.
- Speeches in Acts and the Gospels: the narrative frame + speech = default larger unit; split
  only at a tier-1 seam inside.

## Sources

Original-language claims require SBLGNT / UGNT / CNTR (per the campaign contract). English (WEB)
alone cannot satisfy an original-language review. Greek/LXX numbering claims require a scoped,
pinned source or an explicit gap record. No fabricated Second-Temple / patristic / text-critical
scholarship: absent corpus ⇒ record the gap, verdict insufficient_evidence.

## Symmetry (unchanged, restated)

A tier-2/3/4-only claim is `insufficient_evidence` whether it appears in a challenge, a defense,
or a boss ruling. Absence of any marker (ancient or modern) is never counterevidence against a
boundary. Single-witness claims disclose the witness.
