# Genesis (Gen) — Book Strategy Note — M8_fable (claude-sonnet-5, book_writer)

This note records my independent literary-chunking strategy for Genesis, formed by reading
the full WEB text (Gen_web_clean.txt) chapter by chapter alongside the substrate marker
counts in chapter_profile.json and the exact verse counts in verse_inventory.json. I worked
alone, did not consult any other model's output, and made every boundary call myself. This
document is scratch, non-authorizing candidate work for T423 — it is not canon, not a
reviewed verdict, and not theology.

## selected_strategy

My strategy is: let the recurring Hebrew-narrative structural formula "This is the history
of the generations of ..." (Hebrew *toledot*, WEB wording preserved above) do the heavy
lifting for the primeval history and the patriarchal hinge points, and otherwise let scene
boundaries (new location, new time notice, new speaker constellation, closing formula) and
genre boundaries (narrative vs. genealogical list vs. embedded poem vs. covenant-ceremony
ritual action) mark chunk edges. I did not use chapter numbers as boundary evidence anywhere;
several of my chunks deliberately cross chapter boundaries (2:1-3 attaches to Gen 1, not
Gen 2; 9:1-17 vs 9:18-29 splits mid-chapter; 25:19-34 crosses no chapter but folds two of my
earlier candidate sub-splits into one so the twins' introduction stays whole), and several
others land on a full chapter only because that is genuinely where the literary unit begins
and ends (Gen 3, 5, 7, 10, 13, 16, 20, 23) — in every one of those cases I applied the pilot
book's mechanical medium_low confidence cap rather than claiming spurious certainty.

## literature_type_or_mixed_genre

Genesis is mixed genre throughout: cosmogonic narrative (Gen 1-2), prose etiological
narrative (the bulk of the book), formulaic linear and segmented genealogies (Gen 5, 10, 11,
25, 36, 46), embedded poetry (Gen 3:14-19 judgment oracles, 4:23-24 Lamech's sword song,
9:25-27 Noah's curse/blessing, 27:27-29 and 27:39-40 Isaac's blessings, 48:15-16 Jacob's
blessing of Joseph's sons, 49:1-27 the Testament of Jacob), covenant-ceremony ritual action
(Gen 15, 17), legal/real-estate transaction narrative (Gen 23), and dream/vision reports
(Gen 15, 20, 28, 31, 37, 40-41). No single genre label covers the book; I treated each
chunk's local form on its own terms rather than importing a single book-wide template.

## literary_form_decision_matrix

- New toledot formula ("This is the history of the generations of ...") → new chunk start,
  almost always high confidence (Gen 2:4; 5:1; 6:9; 10:1; 11:10; 11:27; 25:12; 25:19; 36:1;
  36:9; 37:2).
- New itinerary/travel notice ("X traveled/went up/journeyed to Y") after a scene has closed
  → new chunk start (e.g. 13:14 "after Lot was separated"; 26:23 "he went up from there";
  33:18; 46:1).
- Divine speech opening ("Yahweh said to X," "God said to X") that begins a materially new
  topic after a prior speech-unit has closed → candidate boundary, weighed against whether
  it is still the same continuous audience/scene (I merged same-scene divine speech beats;
  see over_split_risk_check).
  - Explicit closing/summary formula ("Thus X did," "he was buried," "these are the sons of
  Y by their families") → chunk end.
- Shift from narrative prose to embedded verse (marked by |q1/|q2 substrate tags) that is a
  self-contained composition (Gen 49) → kept whole as one poem, never split by addressee.
- Shift from genealogy/list to a *different* list form (father-son genealogy → regnal
  succession list → chief-list) → new chunk, per list_register_function_check.
- A closing legal or ritual action (deed of sale, oath, covenant cutting) → chunk end even
  mid-chapter.

## substrate_markers_considered

I read the ¶ (paragraph), |q1/|q2 (poetry line) and [fn] footnote markers in the WEB text
directly, and cross-checked chapter-level counts in chapter_profile.json. The q1/q2 spikes
in Gen 3 (q1=10,q2=14), Gen 49 (q1=35,q2=43,b=11) and Gen 27 (q1=10,q2=6) confirmed where
embedded poetry sits and how much of each chapter it occupies — this is why Gen 49 is kept
as one 27-verse poem chunk rather than chopped per tribe, and why Gen 3's judgment oracles
stay inside the single fall-and-expulsion narrative chunk rather than being pulled out (they
are addressed mid-scene to serpent/woman/man in one continuous confrontation, not a separate
composition). High paragraph (p) density in Gen 18 (p=23), 24 (p=23) and 27 (p=30) tracks
with their dialogue-heavy, multi-beat structure and supported finer-grained splitting there;
low p density in Gen 5, 10, 13, 36 (p=4-10 across many verses) tracks with their list-like,
repetitive-formula character and supported keeping those as single (sometimes chapter-length)
units instead of over-slicing a repeating pattern.

## strongs_metadata_considered_evidence_only

No Strong's numbers, lemma tags, or morphology codes are present in this cleaned WEB text
substrate, so none were available to weigh directly. Where the underlying WEB footnotes gloss
a Hebrew word or name-etymology (e.g. [fn 25:30] "Edom" means "red"; [fn 32:2] "Mahanaim"
means "two camps"), I used that only as color confirming a naming-etiology beat already
visible in the plain English text, never as the reason for a boundary. No boundary in
draft_decisions.json rests on Strong's or lemma evidence; every boundary_evidence_refs entry
cites either the WEB text itself or the chapter_profile substrate.

## source_metadata_evidence_only_check

I did not use J/E/P source-critical labels, divine-name alternation (Elohim vs. Yahweh),
or any authorship/tradition theory as boundary authority anywhere in this chunk map. Where
the divine name does shift (e.g., "God" in 1:1-2:3 versus the compound "Yahweh God" from
2:4 onward), I noted the shift only as one small piece of internal textual evidence
alongside the explicit toledot formula and the change of narrative content (cosmic week
structure versus an intimate garden-formation scene) — never as the sole or primary reason,
and never as a claim about a hypothetical source document. No chunk decision or rationale in
this book invokes documentary-hypothesis vocabulary.

## larger_unit_preservation_check

I actively resisted splitting: the seven-day creation account stays one unit through 2:3
(not stopped at 1:31 on a chapter line); Gen 49's tribal blessing poem stays one 27-verse
unit rather than 12 per-tribe fragments; the Table of Nations (Gen 10) stays one list despite
being a full chapter; Sarah's burial-plot purchase (Gen 23) stays one legal-transaction scene
despite three rounds of negotiation rhetoric; Abraham/Abimelech at Gerar (Gen 20) stays one
continuous encounter rather than being split at the restitution beat; the flood's onset
(7:1-24) stays one continuous rising-waters unit; and Jacob's two surrogate-motherhood birth
cycles (30:1-13, Bilhah then Zilpah) stay merged as one unit since they share identical form
and function. In every one of these cases a less careful pass would have produced a finer
split; I judged the additional split would have cut a single coherent literary action in half
without a real formal seam to justify it.

## list_register_function_check

Genealogies and lists were kept whole by default. I split a list only where the list's own
*function* changed mid-stream, which happens twice in this book in a textually obvious way:
Genesis 4:17-24 shifts from a father-son begetting list to Lamech's first-person boast poem
(a genuinely different form, not just a new name), and Genesis 36 shifts three times — from
a sons-of-Esau genealogy (36:1-19), to the genealogy of an *unrelated* indigenous lineage,
the Horites (36:20-30), to a regnal succession list of Edom's kings ("X died, and Y reigned
in his place" — a king list, not a father-son genealogy, 36:31-39), and back to a chiefs list
(36:40-43). Every other genealogy in the book (Gen 5, 10, 11:10-32, 25:12-18, 46:8-27) is one
list, one function, one chunk, even where that produces a full-chapter chunk.

## epistle_unit_check_if_applicable

Not an epistle. Genesis contains no epistolary material; the epistle_unit_checklist in the
quality protocol does not apply to this book.

## over_split_risk_check

My first working pass over the text produced roughly 139 candidate boundaries, driven by
tagging every beat-change inside continuous scenes (e.g. splitting a single royal audience
in Gen 41 into "cupbearer recalls Joseph," "Joseph is summoned," "Pharaoh recounts the
dream," and "Joseph interprets" as four separate chunks). On review I judged many of these
were beat-changes within one continuous scene (same participants, same location, no time
jump, no genre change) rather than real literary seams, and merged them — for example Gen
41:9-36 is now one chunk (the whole royal audience, cupbearer's recollection through Joseph's
administrative counsel, is one uninterrupted exchange in one throne-room scene), Gen 7 is one
chunk (the flood's rise is one continuous action even though it opens with a distinct divine
instruction), and Gen 30:1-13 merges Bilhah's and Zilpah's birth-notice cycles. I settled at
118 decisions for the whole book. That is above the 45-90 rule-of-thumb range given in this
task's brief; I judged that outcome to be the honest one rather than force further merges,
because Genesis is unusually dense in real, independently-attested seams — eleven distinct
toledot formulas, dozens of itinerary notices, and a book-length habit of short self-contained
type-scenes (three separate wife-sister endangerment episodes in Gen 12, 20, 26 alone) that a
"larger unit" reading cannot honestly absorb into fewer chunks without erasing real boundaries
the text itself marks. Where I was genuinely unsure whether a split was earning its keep
(e.g. Gen 35:16-22, merging Rachel's death with Reuben's sin into one "itinerant crises"
chunk; Gen 4:25-26, a two-verse Seth/Enosh coda), I flagged it explicitly in
notes_for_review rather than silently picking a side.

## sidecar_specificity_plan

Sidecar rows (low_confidence_register, frontier_escalation_queue, atlas_candidate_feed) will
each name the concrete uncertainty driving the row, not a generic "low confidence" label —
e.g. "mechanical chapter-shape cap applied to a legal-transaction scene that is not actually
in doubt" for Gen 23, versus "genuinely thin evidence for merging Rachel's death notice with
the Reuben/Bilhah notice under one itinerary heading" for Gen 35:16-22, versus "poem kept as
a single 27-verse unit despite covering twelve addressees — over-split risk was the concern,
not under-split" for Gen 49:1-27. Genesis has no frontier-book status and no apocalyptic or
epistolary risk categories, so the frontier_escalation_queue is expected to stay thin or
empty; the atlas_candidate_feed will draw primarily from the mechanically-capped
chapter-shape chunks (Gen 3, 5, 7, 10, 13, 16, 20, 23) since those are the rows most likely
to interest a downstream stress-atlas pass.

## chapter_only_fallback_reason_if_used

Eight chunks in this book happen to span exactly one whole chapter: Gen 3 (the fall and
judgment, one continuous confrontation scene), Gen 5 (the Sethite genealogy, one unbroken
formula repeated ten times), Gen 7 (the flood's onset and rise, one continuous action), Gen
10 (the Table of Nations, one list), Gen 13 (Abram-Lot separation plus the renewed land
promise, judged as one unit because the promise is Yahweh's direct response to Lot's
departure in the same scene), Gen 16 (Hagar's flight and return, one scene bound by an
inclusio between the angel's promise and the birth notice that fulfills it), Gen 20 (the
Abimelech/Sarah encounter at Gerar, one continuous two-party exchange), and Gen 23 (the
Machpelah purchase, one legal-transaction scene). None of these is a silent fallback for lack
of a finer signal — in every case I identified real sub-beats and deliberately judged the
larger unit more faithful to the text than chopping it, and I have applied the mandatory
medium_low confidence cap to each per the pilot-book chapter-shape rule, noting in each
decision's notes_for_review that the cap is mechanical, not literary doubt.

## expected_low_confidence_regions

I expect reviewer disagreement to cluster around: (1) the eight chapter-shape chunks listed
above, purely because of the mechanical cap; (2) my merge decisions inside the Joseph
narrative (Gen 41:9-36, 41:46-57, 43:15-34, 44:1-17, 45:16-28) where a finer-grained reviewer
might prefer to split scene-beats I judged were continuous; (3) short transitional notices
under 5 verses that I chose to keep as their own chunk rather than folding into a neighbor
(Gen 4:25-26; 26:34-35; 33:18-20); (4) the Gen 35:16-22 merge of two thematically different
crises (Rachel's death, Reuben's sin) under one itinerary umbrella; and (5) whether Gen
13:1-18 and Gen 30:1-13 should have stayed split rather than merged.

## frontier_or_atlas_candidate_expectations

Genesis is not a frontier book (frontier status applies only to Dan and Rev per the quality
protocol), so I expect zero frontier_escalation_queue rows driven by apocalyptic/visionary
risk. I do expect several atlas_candidate_feed rows: the eight mechanically-capped
chapter-shape chunks, the Gen 36 list-register cluster (four function changes in one
chapter is an unusual density worth a downstream look), and the Gen 49 whole-poem decision
(flagged not because I doubt it, but because it is the single highest-value place in this
book where a downstream reviewer might disagree in the opposite direction — under-splitting
rather than over-splitting).

## post_adjudication_outcome

This section records the outcome of the blind review mesh and boss-adjudication rounds that
followed the candidate chunk map above. It is a factual summary, added after the fact; the
sections above are the original, unaltered candidate authoring.

- Final decision count: 117 (started at 118; net -1 across two consolidation rounds).
- The mesh changed 4 pairs of decisions by merging them (Gen 15 vision-and-covenant sequence;
  Gen 27:41-28:9 aftermath-and-departure unit; Gen 40 dream-report chapter; Gen 46:28-47:12
  announcement-and-fulfillment unit) and split 3 decisions into new ones (Gen 9:1-7/9:8-17 at
  the covenant-sign re-introduction; Gen 30:1-8/30:9-13, the Bilhah/Zilpah surrogate cycles;
  and a 2-verse Mahanaim theophany carved out of Gen 32:1-21).
- Boundary shifts included one full reversal: my round-1 move of Gen.18:16 into the Sodom
  material was reverted after a revision-round finding that 18:16 and 18:22 form a resumptive
  discourse bracket around the intervening soliloquy. Two other shifts corrected an internal
  inconsistency in my own location-continuity reasoning: Gen.24's household scene now opens
  at 24:32 (the actual relocation into the house) rather than 24:29, and Gen.35's Rachel-death
  unit now closes at 35:20 (its own etiological "to this day" formula) rather than 35:21,
  which also resolved a stranded locative anaphor at the head of the following unit.
- 9 spans in the final map exactly equal a whole chapter (Gen 3, 7, 10, 13, 16, 20, 23, plus
  two produced by the Gen 15 and Gen 40 merges); all 9 carry the pilot-book's mechanical
  medium_low/low confidence cap. In the two merge-derived cases the underlying evidence is
  unusually strong for a capped row (e.g. Gen 15's total absence of any WLC division across
  the whole chapter); the cap there reflects the mechanical rule, not doubt about the merge.
- 12 decisions carry sidecar rows (low-confidence register): the original 10 chapter-shaped
  or thin-evidence rows, plus the two merge-derived chapter-shaped rows above.
- One decision remains formally held: M8-Gen-084 (Gen.37:1-11), on whether 37:1's settlement
  notice closes the preceding Esau/Edom toledot block (paired with 36:8's identical formula)
  or opens the Jacob toledot as its narrative frame before the 37:2 superscription. Both
  readings have live, unresolved text signals; the adjudicator declined to force a resolution.
- Corpus-defect find and fix: the original WEB text extraction had silently dropped ~65
  same-line clauses following paragraph marks throughout the book (e.g. Gen.35:22b, "Now the
  sons of Jacob were twelve"; Gen.39:6b, "Joseph was well-built and handsome"; Gen.40:8b,
  Joseph's own request to the cupbearer). The defect was identified and corrected mid-review;
  every decision touching an affected verse was re-checked against the corrected text, and in
  three cases (Gen.35:22, Gen.39:6, Gen.40:8) the recovered clause materially changed the
  boundary reasoning.
- The owner addendum's evidence-weighing rules were decisive throughout: Masoretic
  petuchah/setumah divisions are single-witness, at most corroborating, and can never drive a
  boundary alone; marker absence is never counter-evidence either way; and modern editorial
  paragraphing (including WEB's own) is metadata only, never boundary evidence — which is why
  two revision-round challenges grounded in WEB paragraph-grouping alone were held even though
  their conclusions happened to be correct on independent Hebrew-side grounds.
