# Exodus (Exod) — Book Strategy Note — M8_fable (claude-sonnet-5, book_writer)

This note records my independent literary-chunking strategy for Exodus. I read the full WEB
text (Exod_web_clean.txt) chapter by chapter, cross-checked chapter-level substrate marker
counts in chapter_profile.json, verified exact verse totals against verse_inventory.json, and
handled the two WEB/MT numbering offsets (WEB 8:1-32 = MT 7:26-8:28; WEB 22:1-31 = MT
21:37-22:30) using web_mt_crosswalk.json. I worked alone, isolated to the M8_fable folder and
shared_research_baseline/, and made every boundary call myself. This document is scratch,
non-authorizing candidate work for T423 — it is not canon, not a reviewed verdict, and not
theology. My strategy and the evidence weighing behind it follow the owner addendum
m8-mesh-r2: the text's own signals drive boundaries; petuchah and Masoretic disjunctive
accents corroborate but never originate one; setumah is weaker corroboration still; chapter
and verse numbers, modern headings, footnotes, and Strong's tags are metadata only.

## selected_strategy

My strategy is to let Exodus's own recurring structural devices do the work: the plague
cycle's announcement-execution-hardening formula; the shift between direct divine speech (the
Decalogue, the altar law) and casuistic "if" case law (the Covenant Code); the register
distinction between future-tense tabernacle INSTRUCTION panels (chs. 25-31, "you shall make")
and past-tense EXECUTION panels (chs. 35-40, "he/they made... as Yahweh commanded Moses"); the
prose-to-poetry shift in ch. 15; itinerary and time notices that mark journey stages; and
scene/participant/addressee changes within dialogue-heavy narrative (the burning-bush
objection cycle, the golden-calf aftermath). I did not use chapter numbers as boundary
evidence anywhere. Three chunks deliberately cross chapter lines because the text's own
causal or resumptive logic outweighs the printed chapter division: Exod.5.22-6.1 (Moses's
complaint and Yahweh's immediate one-verse reply); Exod.6.28-7.7 (a resumptive repetition,
Wiederaufnahme, that reopens the commission dialogue almost verbatim after the Levite
genealogy interrupts it, closed by an ages colophon); and Exod.31.18-32.6 (the tablets-given
notice that directly triggers the golden-calf crisis). Only one chunk happens to span an
entire chapter (Exod.11.1-11.10); I explain why that is coincidental, not chapter-driven,
under chapter_only_fallback_reason_if_used below.

## literature_type_or_mixed_genre

Exodus is mixed genre throughout, more so than a single narrative-versus-list split can
capture: bondage and deliverance narrative (chs. 1-2, 5, 14); call-narrative dialogue (chs.
3-4); a formulaic plague cycle mixing royal-audience scene with repeated
announcement/execution/hardening beats (chs. 7-11); embedded cultic law delivered mid-
narrative (the Passover and Unleavened Bread instructions of ch. 12, interrupting the tenth
plague's own payoff); victory poetry (the Song of the Sea, 15:1-19, with its own antiphonal
response in 15:20-21); wilderness itinerary and provision narrative (chs. 15-18); theophany
and covenant-ratification narrative (chs. 19, 24); an apodictic law collection in a register
of its own (the Decalogue, 20:1-17); a casuistic case-law corpus, the Covenant Code
(20:22-23:33); tabernacle instruction panels organized as a repeated "Yahweh spoke to Moses,
saying" list of building and ordination specifications (chs. 25-31); a golden-calf crisis
narrative with its own intercession-and-judgment shape (ch. 32-34); and tabernacle execution
panels that mirror the instruction panels clause for clause in a compliance register (chs.
35-40), closing on a theophanic notice. No single genre label covers the book, and I treated
each chunk's local form on its own terms.

## literary_form_decision_matrix

- A fresh messenger/speech formula ("Yahweh said to Moses," "Yahweh spoke to Moses and Aaron,
  saying") that opens materially new content after a prior speech-unit has closed → candidate
  boundary, weighed against whether it is still the same continuous scene (I merged
  same-scene speech beats where the addressee and topic had not genuinely changed; see
  over_split_risk_check).
- A new participant, location, or addressee introduced mid-scene → new chunk (e.g. 8:1's shift
  from the sign contest to the frog plague; 18:1's reintroduction of Jethro by name and
  relation).
- The plague cycle's own internal shape (announcement → execution → hardening/removal) → each
  plague is its own chunk; where a single plague's text itself shows a second imperative
  reopening execution after a threat-speech (9:13-21 vs. 9:22-35; 10:1-11 vs. 10:12-20), I
  split there rather than treating the whole plague as one undifferentiated unit.
- A shift from casuistic "if/when" case law to terse apodictic command, or vice versa → new
  chunk (20:22-26's apodictic altar law versus 21:1's casuistic "these are the ordinances"
  superscription; 22:17/22:18's shift from casuistic property law to apodictic capital
  crimes).
- A list-superscription formula ("these are the ordinances," "these are the garments which
  they shall make," "these are the amounts of materials") → new chunk start, and a shift in
  the underlying list's own function (not just its topic) → a further split within what looks
  like one list; see list_register_function_check.
- The instruction/execution tense pair: future "you shall make" (chs. 25-31) versus past
  "he/they made... as Yahweh commanded Moses" (chs. 35-40) → each named component (ark,
  table, lampstand, altar, garments) is its own chunk on both sides, unless the underlying
  content is too thin to justify independence, in which case I consolidated (see
  over_split_risk_check).
- Prose-to-poetry substrate shift (marked by q1/q2 line tags) → new chunk, kept whole as a
  self-contained composition rather than split by strophe or addressee (15:1-19).
- An inclusio or refrain (Miriam's 15:20-21 repeating the song's opening line; the "pattern
  shown to you on the mountain" refrain closing 25:40, 26:30, 27:8; the sevenfold "as Yahweh
  commanded Moses" compliance refrain climaxing at 39:32-43) → treated as corroborating
  evidence for a boundary already indicated by a participant, speech, or register change, not
  as a boundary-driver on its own.
- An itinerary formula ("they took their journey from X... and encamped in Y") after a scene
  has closed → new chunk start (12:37; 13:17; 16:1; 17:1).

## substrate_markers_considered

I read chapter_profile.json's per-chapter marker counts alongside the WEB text's own ¶, |q1/
|q2, and [fn] tags directly. Exactly one chapter in this book carries the
has_poetry_or_liturgy_marker flag: Exod.15, with q1=20 and q2=28, concentrated entirely in
15:1-19 (the Song of the Sea) and its 15:20-21 antiphon; no other chapter in the book shows
any q/qs/qr/d/b markers at all, which is itself useful negative evidence that Exodus is
overwhelmingly prose narrative and instruction rather than a book with scattered embedded
verse. Paragraph (p) density tracks usefully with dialogue intensity: chapters like 4 (p=24),
32 (p=19), and 34 (p=16) are dialogue- and event-dense and supported finer splitting, while
low-p chapters like 25 (p=4), 27 (p=3), and 40 (p=5) are list-like instruction/execution
material where I let list-item boundaries, not paragraph density, drive the splits. Footnote
density (f/fr/ft) spikes at Exod.38 (f=22) because of the repeated unit-conversion footnotes
attached to talent/shekel/cubit measurements in the materials-accounting section; I treated
those footnotes as metadata only, never as evidence for a boundary, per
strongs_metadata_considered_evidence_only below and the owner addendum's tier-4 rule that
footnotes are never boundary evidence.

## strongs_metadata_considered_evidence_only

No Strong's numbers, lemma tags, or morphology codes are present in this cleaned WEB
substrate, so none were available to weigh as direct evidence anywhere in this chunk map.
Where WEB footnotes gloss a Hebrew word or name-etymology (e.g. [fn 2:10] "Moses" sounds like
the Hebrew for "draw out"; [fn 15:23] "Marah" means bitter; [fn 17:7] "Massah" means testing
and "Meribah" means quarreling), I used that only as color confirming a naming-etiology beat
already visible in the plain English narrative, never as the reason for a boundary. No
decision in draft_decisions.json rests on Strong's or lemma evidence; every
boundary_evidence_refs entry cites either the WEB text itself or the chapter_profile
substrate, and the strategy throughout treats Strong's-tier metadata exactly as tier 4 under
the owner addendum: available for color, never for boundary authority.

## source_metadata_evidence_only_check

I did not use documentary-hypothesis source labels (J/E/P), nor any theory about which strand
"wrote" the instruction panels versus the narrative frame, as boundary authority anywhere in
this chunk map. Exodus is a natural place where a source-critical reader might want to
attribute the whole of chs. 25-31 and 35-40 to one hand and the golden-calf narrative to
another; I deliberately did not do this. Where the instruction and execution panels parallel
each other almost clause for clause (compare 26:1 "you shall make the tabernacle with ten
curtains" to 36:8 "they made the tabernacle with ten curtains"), I treated the parallel as a
literary/compositional feature of the text as given — a real register pair (future
instruction vs. past compliance) — and cited it as such, never invoking a hypothetical
redaction history or two source documents standing behind the two panels.

## larger_unit_preservation_check

I actively resisted splitting: the Song of the Sea stays one 19-verse unit (15:1-19) rather
than being chopped by strophe; the whole tenth-plague announcement plus cycle-summary stays
one unit (11:1-10) rather than being split into private announcement versus public speech;
the Sea crossing itself stays as two large action-units (14:15-25, 14:26-31) rather than being
fragmented into every beat (pillar repositioning, sea splitting, crossing, Egyptian confusion)
separately; the Decalogue stays one 17-verse unit despite covering ten distinct commands,
because it is a single unmediated speech-act addressed to the whole people in one register;
Moses's catechetical exhortation in 13:3-16 stays merged across the Unleavened-Bread and
firstborn topics because the "you shall tell your son" formula brackets both as one teaching
rather than two; and the whole casuistic property/marital law list of 22:1-17 stays one chunk
despite covering theft, grazing damage, fire, bailment, borrowing, and seduction, because the
list's function (casuistic conditional restitution law) does not actually change until v.18's
shift to apodictic capital crimes. In each case a less careful pass would have produced a
finer split; I judged the additional split would have cut one coherent literary action or one
genuinely single-function list in half without a real formal seam to justify it.

## list_register_function_check

I split a list only where its own function changed, not merely where its topic drifted. The
clearest case is the Covenant Code: 21:1-11's servitude ordinances, 21:12-27's
injury/capital-crime cases, and 21:28-36's animal-liability cases are three separate chunks
because each addresses a legally distinct class of harm even though all three share casuistic
form; but I did not split 22:1-17 internally (theft/damage/bailment/borrowing/seduction)
because all of it remains one function — casuistic property-and-restitution law — until the
register itself changes to apodictic command at 22:18. The tabernacle instruction panels are
the book's second major list-register case: I split by named furniture item (ark, table,
lampstand, tent coverings, frame, veil, altar, court) because each item is its own
self-contained specification with its own "you shall make" opening and its own closing
formula, but I consolidated the smaller priestly-garment items (robe, gold plate, tunics,
turban, sash, undergarments) into one chunk at 28:31-43 rather than five, because none of
those items individually carries content proportionate to the ephod or breastplate — a
judgment I flag as contestable in over_split_risk_check. The execution panels (chs. 35-40)
mirror this same item-by-item logic but are not always split at matching granularity: the
incense altar and the anointing-oil/incense recipes were three separate instruction chunks
(30:1-10, 30:22-33, 30:34-38) but compress into one execution chunk (37:25-29), an asymmetry I
flag explicitly rather than forcing artificial parity between the two panels.

## epistle_unit_check_if_applicable

Not an epistle. Exodus contains no epistolary material; the epistle_unit_checklist in the
quality protocol does not apply to this book.

## over_split_risk_check

My working read of the burning-bush call narrative (3:1-4:31) produced nine chunks driven by
each successive objection-and-response movement (identity, name, elders'-instructions, signs,
eloquence, Jethro's leave, the bridegroom-of-blood episode, Aaron's reunion). On review I kept
this granularity because each movement is marked by its own speech-formula and addresses a
genuinely distinct concern, but I recognize a less granular reading could merge several of
these Q&A beats (e.g. 3:11-15's two identity questions, or 4:10-17's eloquence objection and
Aaron's appointment) into fewer, larger dialogue chunks, since no scene relocation separates
them. Similarly, I split the tabernacle instruction panels (chs. 25-31) into 25 chunks and the
execution panels (chs. 35-40) into 24 chunks by named component; a strategy that instead
treated "the furniture" or "the priestly garments" as one function-level unit each (as I did
consolidate for the minor garment items at 28:31-43) would produce a substantially shorter
map. I settled at 144 decisions for the whole book, which is above a 45-90 rule-of-thumb
range; I judged that outcome to be the honest one rather than force further merges, because
Exodus's plague cycle (ten formulaically-repeated but individually distinct scenes), its
two-panel tabernacle complex (each with a dozen-plus named components), and its layered legal
material (Decalogue, Covenant Code, covenant-renewal restatement) are unusually dense in real,
independently-marked seams that a "larger unit" reading cannot honestly absorb into fewer
chunks without erasing boundaries the text itself marks with its own recurring formulas. Where
I was genuinely unsure whether a split was earning its keep, I flagged it in notes_for_review
rather than silently picking a side (e.g. the one-verse bronze-basin notice folded into
38:1-8; the 27:20-21 priestly-oil coda; the compressed 37:25-29 execution panel).

## sidecar_specificity_plan

Sidecar rows (low_confidence_register, frontier_escalation_queue, atlas_candidate_feed) will
each name the concrete uncertainty driving the row, not a generic "low confidence" label —
for example "two-verse firstborn command (13:1-2) whose independence from Moses's following
address rests entirely on a speaker change, not on any length-appropriate content" for
M8-Exod-043, versus "poetry-frame boundary in 15:1-19 where exactly the hymn's prose closing
frame ends is genuinely debatable even though the span is not chapter-shaped" for M8-Exod-050,
versus "execution panel 37:25-29 compresses two separate instruction chunks (30:1-10 and
30:22-38) into one, an instruction/execution granularity asymmetry worth a downstream look"
for M8-Exod-132. Exodus has no frontier-book status and no apocalyptic-visionary risk
category, so I expect the frontier_escalation_queue to stay thin or empty; the
atlas_candidate_feed will draw primarily from the instruction/execution panel-pairing
question (chs. 25-31 vs. 35-40, where matching every instruction chunk to its execution
counterpart is itself a downstream-useful cross-reference task) and from the two deliberate
chapter-boundary crossings at 5:22-6:1 and 6:28-7:7.

## chapter_only_fallback_reason_if_used

Exactly one chunk in this book happens to span an entire chapter: Exod.11.1-11.10, the
tenth-plague announcement plus cycle-summary coda. This is not a fallback for lack of a finer
signal — the chapter's own ten verses read as one functionally unified unit (a private
announcement to Moses followed by a narrator's summary looking back across the whole plague
cycle, "Moses and Aaron did all these wonders before Pharaoh"), bounded on both sides by real
seams (10:29's closing personal exchange before it; 12:1's shift to Passover legislation after
it). Because chapter_profile.json shows no poetry/liturgy marker for chapter 11
(risk_flags=[]), the pilot book's mechanical chapter-shape confidence cap does not apply here,
and I assigned this chunk medium confidence on its own honest merits (there is a real, if
secondary, question of whether vv.9-10 belong with this unit or are a floating cycle-summary
that could be read with what follows). No other chunk in the book happens to equal a full
chapter; every other chapter is either split internally or merged across its boundary with a
neighbor, for a reason stated in that decision's boundary_rationale.

## expected_low_confidence_regions

I expect reviewer disagreement to cluster around: (1) the granularity of the burning-bush call
narrative (3:1-4:31) and whether several of its nine objection-response chunks should merge;
(2) the consolidation of the minor priestly-garment items at 28:31-43 into one chunk versus
splitting robe/plate/tunics/turban/sash into as many as five; (3) the instruction/execution
granularity mismatch at 37:25-29, where two instruction-side chunks compress into one
execution-side chunk; (4) the register split inside 22:18-31 between the terse capital-crime
triad and the longer motive-clause social-justice commands, both nominally "apodictic" but
rhetorically distinct; (5) the two deliberate chapter-boundary crossings at 5:22-6:1 and
6:28-7:7, which a strict chapter-respecting reviewer might reject even though I judge the
resumptive-repetition and Q&A evidence for each to be strong; and (6) the poetry-frame
boundary of 15:1-19, where the exact point at which the Song of the Sea's prose frame closes
before Miriam's antiphon is a genuinely debatable call.

## frontier_or_atlas_candidate_expectations

Exodus is not a frontier book (frontier status applies only to Dan and Rev per the quality
protocol), so I expect zero frontier_escalation_queue rows driven by apocalyptic/visionary
risk. I do expect several atlas_candidate_feed rows: the instruction/execution panel-pairing
structure across chs. 25-31 and 35-40 (a natural cross-reference table a downstream atlas pass
could build directly from this chunk map); the two deliberate chapter-boundary crossings
(5:22-6:1, 6:28-7:7) as examples of resumptive-repetition detection; and the Song of the Sea
(15:1-19) as the book's one clear poetry-substrate region, flagged not because I doubt the
chunk boundary but because it is the single place in Exodus where a downstream reviewer is
most likely to propose a different frame-boundary in either direction.

## post_adjudication_outcome

This section records the outcome of the blind review mesh and boss-adjudication rounds that
followed the candidate chunk map above. It is a factual summary, added after the fact; the
sections above are the original, unaltered candidate authoring.

- Final decision count: 158 (started at 144; net +14 across two merges and sixteen splits).
- The mesh changed 2 pairs of decisions by merging them (3:11-15/3:16-22 into one call-narrative
  unit at 3:11-22, and 40:9-15 into the 40:1-16 instruction speech) and split 16 decisions into
  new siblings (M8-Exod-145 through M8-Exod-160), plus rebalanced 7 further neighbor pairs
  (16:4-12/13-21, 19:1-8/9-15, 31:12-17/18, 33:12-17/18-23, 34:10-26/27-35, 35:30-35/36:1-7,
  40:16/17-33) where the true seam sat one or more verses off from my original cut.
- The book's only chapter-shaped chunk was dissolved: Exod 11 (my M8-Exod-037, 11:1-10) split
  three ways at genuine formula-plus-paragraph seams (11:4, 11:9), so no chunk in the final
  layout happens to span a whole chapter by coincidence or otherwise.
- The controlling grammatical precedent across the mesh was עוד as a same-speaker continuation
  particle: the identical construction at 3:15 and 4:6 was read consistently (non-boundary at
  both), which is why 3:11-22 merged into one unit rather than splitting at 3:15/16 as one
  challenge proposed.
- A colophon-family criterion emerged and was applied consistently at three separate sites:
  the backward-facing compliance formula "ככל אשר צוה/צויתך...כן עשה/עשו" closes what precedes
  it at 31:11, 39:32, and 40:16 alike, never opens what follows -- corroborated by the boss's
  own recorded decision_relations note (M8-Exod-REL-002) tying all three together as one
  construction family.
- Every overrule sustained my originally held position (9 held, 0 reversed against me); two of
  those overrules were issued in part rather than in whole (7:14-25's blood-plague seam and
  38:21-39:1's accounting-section boundary), preserving the challenger's counterevidence on
  record without adopting the proposed re-cut. Zero human holds were needed.
- One symmetry ruling struck WEB paragraph-marking from both sides of two separate disputes
  (7:18/19 and 38:24/39:1) as metadata under the owner addendum's tier-4 rule, leaving those
  two boundaries resting on formula class, participant continuity, and Masoretic corroboration
  only -- exactly the evidence-weighting discipline the addendum was written to enforce.
- Citation hygiene was tightened wherever a speech formula was named as boundary-driving:
  WEB's uniform "spoke"/"said" rendering had erased the וידבר/ויאמר distinction the campaign's
  evidence tiers treat separately, so OSHB citations were added alongside the WEB quotations
  in the plague-cycle cluster to make the formula type auditable without re-deriving it.
- Two one-verse decisions survived on formula evidence despite their thinness (M8-Exod-136 at
  Exod.39.1 and M8-Exod-158 at Exod.38.8), both flagged in the sidecar register as candidates
  for a minimum-chunk-length policy rather than as unresolved boundary disputes.
