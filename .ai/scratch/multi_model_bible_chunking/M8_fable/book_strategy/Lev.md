# Leviticus (Lev) — Book Strategy Note — M8_fable (claude-sonnet-5, book_writer)

This note records my independent literary-chunking strategy for Leviticus, authored alone as a
fresh instance with no context from any other book in this campaign. I read the full WEB text
(Lev_web_clean.txt) chapter by chapter, cross-checked chapter-level substrate marker counts in
chapter_profile.json, verified exact verse totals against verse_inventory.json, and read the
Hebrew (Lev_oshb.txt, MT-numbered, verse-per-line) throughout to confirm formula wording before
citing it as evidence. I handled the one verified WEB/MT numbering offset (WEB Lev.6.1-6.30 = MT
Lev.5.20-6.23) using web_mt_crosswalk.json and cite both WEB and MT verse numbers for every
decision inside that zone. I worked in isolation, reading only the M8_fable folder and
shared_research_baseline/, and made every boundary call myself. This document is scratch,
non-authorizing candidate work for T423 — not canon, not a reviewed verdict, and not theology.
My strategy and the evidence weighing behind it follow the owner addendum m8-mesh-r2: the text's
own signals drive boundaries; Masoretic petuchah and disjunctive accents corroborate but never
originate one; setumah is weaker corroboration still; chapter and verse numbers, modern headings,
footnotes, and Strong's tags are metadata only, never boundary evidence.

## selected_strategy

My strategy is to let Leviticus's own five recurring structural devices do the boundary work,
in this order of priority: (1) the וידבר יהוה אל משה לאמר ("Yahweh spoke to Moses, saying") and
ויאמר יהוה אל משה ("Yahweh said to Moses") messenger formulas that open every torah unit in
chs.1-27, weighed against whether a fresh formula is truly reopening a new topic or merely
resuming an already-open one; (2) the addressee shift baked into the offering laws themselves —
chs.1-5 are addressed to Israel generally ("speak to the children of Israel"), while 6:8-7:36
readdresses the same offering types to "Aaron and his sons" specifically, producing five
recognizable זאת תורת ("this is the law of...") priestly-procedure superscriptions layered on
top of the lay-facing torot of chs.1-5; (3) the זאת תורת / התורה colophon system that closes
whole legal units retrospectively (7:37-38; 11:46-47; 12:7; 13:59; 14:54-57; 15:32-33; and the
book-spanning colophons at 26:46 and 27:34); (4) the casuistic protasis/apodosis pattern (אם/כי
+ verdict) that structures the purity-law case series in chs.13-15 and the capital/cut-off
penalty lists in ch.20; and (5) the אני יהוה / אני יהוה אלהיכם ("I am Yahweh" / "I am Yahweh your
God") refrain that closes individual law-clusters throughout chs.11 and 18-22, and which I
treated as corroborating evidence for a boundary already indicated by a formula or topic change,
never as a sole driver on its own. I did not use chapter numbers as boundary evidence anywhere;
no chunk in my 180-decision map happens to span a whole chapter (see
chapter_only_fallback_reason_if_used below). Leviticus's own internal seams are dense enough —
five separate offering torot in seven chapters, five purity-law torot with their own colophons
in five chapters, seven festival entries in one chapter, five escalating curse tiers in one
chapter — that chapter divisions were never in danger of doing any real work in this book.

## literature_type_or_mixed_genre

Leviticus is not one genre but a sequence of distinct legal-cultic sub-genres, each with its own
form: sacrificial procedure organized as offering torot with two addressee layers, lay (chs.1-5)
and priestly (6:8-7:36), each offering type further subdivided by animal-source or occasion
class (herd/flock/bird; raw/cooked/firstfruits); an ordination-and-inauguration narrative
(chs.8-9) in the book's plain prose-narrative register, interrupted by a priestly-crisis
narrative (ch.10, the Nadab/Abihu incident and its aftermath rulings); a purity-law case series
(chs.11-15) built from casuistic diagnostic protases with their own zot torat colophons; a
single elaborate ritual-procedure chapter (ch.16, the Day of Atonement); a centralized-worship
and blood-sanctity law (ch.17); a run of Holiness-collection material (chs.18-26) itself mixed —
apodictic prohibition lists with kinship-formula repetition (ch.18), a dense miscellaneous
ethical-cultic command list closed by refrains (ch.19), capital and cut-off penalty lists
(ch.20), priestly-class holiness restrictions (chs.21-22), a festival calendar organized as a
repeated messenger-formula list (ch.23) interrupted by its own narrative (24:10-23, the
blasphemer incident), agrarian-economic law tied to a ritual calendar (chs.25, sabbatical/
jubilee), and a covenant blessings-and-curses conclusion in an escalating five-tier structure
(ch.26); and finally a vow-and-valuation appendix (ch.27) explicitly outside the Sinai-corpus
colophon that closes ch.26. No single label covers the book, and I treated each chunk's local
form on its own terms rather than forcing "law" or "ritual" as a blanket genre tag; the
literature_type_guess field in every decision names a specific, book-local form (e.g.
"burnt_offering_torah_herd_case," "purity_case_series_boil_scar," "covenant_curses_tier_two")
rather than a generic category.

## literary_form_decision_matrix

- A fresh messenger formula (וידבר/ויאמר יהוה אל משה, sometimes with "and to Aaron") that opens
  materially new legal content → candidate boundary, weighed against whether the prior speech
  unit had genuinely closed (I did not split every internal "Yahweh spoke" repetition inside
  ch.23's festival calendar into isolated single-verse fragments where the surrounding content
  was clearly one continuous festival entry; see over_split_risk_check).
- A זאת תורת / זה הדבר ("this is the law of..." / "this is the thing...") superscription →
  strong boundary, whether or not it is preceded by a fresh messenger formula, since it functions
  as the book's own recognizable torah-opening tag independent of speech-formula placement
  (e.g. 6:14's meal-offering torah opens mid-speech-unit with no new messenger formula, yet still
  marks a fresh chunk).
- A retrospective זאת/אלה + summary colophon ("this is the law of X, Y, and Z...which Yahweh
  commanded...in Mount Sinai") → strong boundary, closing rather than opening a unit, distinct in
  direction from the forward-looking superscription formula above.
- A new casuistic protasis (אם/כי + a fresh triggering condition) within a case-list chapter →
  new chunk, weighted against genuinely thin or purely animal-name variants of an
  already-established procedure, which I sometimes merged (see list_register_function_check).
- An addressee change (Israel generally / Aaron and sons / the priests / the high priest
  specifically) → new chunk, the device that separates the priestly-procedure torot of 6:8-7:36
  from the lay-facing torot of chs.1-5, and that separates ordinary-priest holiness rules from
  high-priest-specific rules in ch.21.
- A participant/scene-class change in narrative material → new chunk, the device separating the
  ordination narrative (ch.8) from the inauguration narrative (ch.9) from the Nadab/Abihu crisis
  and its aftermath rulings (ch.10), and separating the lamp/bread instructions from the
  blasphemer narrative in ch.24.
- A recurring escalation formula (ch.26's five "if you still will not listen...seven times more"
  cycles) → new chunk at each recurrence, since the text itself marks each tier as a fresh,
  intensified stage rather than a mere continuation.
- The אני יהוה / אני יהוה אלהיכם refrain → treated as corroborating evidence for a boundary
  already indicated by topic, protasis, or formula change, never as a sole driver (a bare refrain
  closing a clause is not by itself sufficient evidence per the owner addendum's
  marker_only_claim_is_insufficient_evidence rule).

## substrate_markers_considered

I read chapter_profile.json's per-chapter marker counts alongside the WEB text's own ¶ and [fn]
tags directly. Exactly one chapter in this book carries the has_poetry_or_liturgy_marker flag:
Lev.10 (q1=1, q2=1). On inspection against the Hebrew (oshb Lev.10.3), this is entirely the
two-line embedded divine saying Moses quotes to Aaron, "I will show myself holy to those who come
near me, and before all the people I will be glorified" — a brief quoted oracle inside an
otherwise fully prosaic narrative verse, not a chapter-wide poetic register. I did not treat
ch.10 as poetry-substrate for chunking purposes; per the CHAPTER-SHAPE RULE, this means no
chapter in Leviticus carries a genuine poetry/liturgy marker of the kind that would cap
chapter-shaped-chunk confidence, and in any case no chunk in my map happens to equal a whole
chapter (see chapter_only_fallback_reason_if_used). Paragraph (¶) density is highest in chs.18
(p=21), 19 (p=33), and 20 (p=18) — exactly the three chapters whose apodictic prohibition-and-
penalty lists are the most granular in the book — and lowest in the offering-procedure chapters
(ch.3 p=4, ch.9 p=4), where I let casuistic protasis boundaries and offering-object changes, not
paragraph density, drive the splits, consistent with how Exodus's book-writer treated WEB ¶ as
metadata-only context rather than boundary authority. Footnote density spikes at ch.23 (f=14,
the festival calendar's unit-conversion and calendar-term glosses) and ch.27 (f=10, valuation
weights); I treated every footnote strictly as metadata, per strongs_metadata_considered_
evidence_only below, never as boundary evidence anywhere in this map.

## strongs_metadata_considered_evidence_only

No Strong's numbers, lemma tags, or morphology codes are present in this cleaned WEB substrate,
so none were available to weigh as direct evidence anywhere in this chunk map. Where WEB
footnotes gloss a Hebrew term or unit of measure (e.g. [fn 5:11] an ephah is about 22 liters;
[fn 19:16] "endanger the life" is literally "blood"; [fn 27:3] a shekel is about 10 grams), I
used that only as background color, never as the reason for a boundary. No decision in
draft_decisions.json rests on Strong's-tier evidence; every boundary_evidence_refs entry cites
either the WEB text itself or the OSHB Hebrew consonantal-plus-pointed text directly, and the
strategy throughout treats Strong's-tier metadata exactly as tier 4 under the owner addendum:
available for color, never for boundary authority. I want to be explicit that this is a
considered position, not an oversight: Leviticus's dense terminology (weights, measures, animal
and skin-condition vocabulary) is exactly the kind of book where a chunker might be tempted to
lean on lexical apparatus for boundary confidence, and I deliberately did not.

## source_metadata_evidence_only_check

I did not use documentary-hypothesis source labels (P, H, or any other siglum), nor any theory
about which strand or redactional layer "wrote" chs.1-16 versus chs.17-26, as boundary authority
anywhere in this chunk map. Leviticus is a textbook case where a source-critical reader might
want to treat the whole "Holiness Code" (chs.17-26) as one compositional unit distinguished from
the surrounding "Priestly" material purely on stylistic-source grounds (the recurring אני יהוה
refrain is a favorite marker in that scholarship); I deliberately did not do this. Where the
refrain recurs, I cited it as a literary/compositional feature of the text as given — a real
repeated closing formula corroborating a boundary already indicated by topic or protasis change
— never as evidence for, or against, a hypothetical redactional seam between a "P" and an "H"
source. Similarly, I did not treat the offset zone at WEB Lev.6.1-30 (MT 5:20-6:23) as evidence
of a seam between two compositional layers; I treated it purely as a numbering-convention fact
requiring dual citation, per web_mt_crosswalk.json, and nothing more.

## larger_unit_preservation_check

I actively resisted splitting in several places: the whole thirteen-item kinship-incest
prohibition list (18:6-18) stays one chunk despite covering thirteen distinct relatives, because
every item shares one identical ervat-X-lo-tegalleh formula, one addressee, and one function,
the same reasoning Exodus applied to keep its Decalogue as one 17-verse chunk; the eight-case
מות יומת ("shall surely be put to death") capital-crime list in 20:9-16 stays one chunk rather
than eight, because no internal register change interrupts the repeated protasis-apodosis
formula until the penalty class itself shifts at v.17; the whole five-blessing sequence in
26:3-13 stays merged despite covering agricultural, military, and covenantal-presence blessings,
because all three sub-lists hang off the chapter's single opening protasis with no fresh
conditional reopening the topic; and the bed/seat/touch/spittle/saddle/vessel contamination
register for a man with a discharge (15:4-12) stays one chunk despite eight distinct contact
objects, because every case shares one identical wash-bathe-unclean-until-evening apodosis and
none introduces a new legal principle, only a new object touched. In each case a less careful
pass would have produced a finer split; I judged the additional split would have cut one
coherent literary register in half without a real formal seam — a change in the underlying
legal principle, not just the topic or object named — to justify it.

## list_register_function_check

I split a list only where its own function changed, not merely where its topic drifted. The
clearest positive case is ch.4's sin-offering torah: the anointed-priest case (4:3-12), the
whole-congregation case (4:13-21), the ruler's case (4:22-26), and the two commoner cases
(4:27-31, 4:32-35) are five separate chunks because each addresses a legally distinct offender
class with its own procedure (the priest's and congregation's cases require crossing the veil
and outside-camp burning; the ruler's and commoners' cases use a simpler horn-and-base
procedure), even though all five share the same underlying casuistic form. By contrast, I did
not split the flock sub-cases of the peace-offering torah (3:6-16, lamb then goat) or the person-
valuation and animal-substitution vow rules' internal sub-clauses, because the procedure does
not functionally change between them — only the animal named does. The purity case series in
ch.13 is the book's clearest list/register case: I split at each new diagnostic protasis (general
swelling, chronic/advanced disease, boil-scar, burn-scar, scalp/beard scall, benign bright spot,
baldness, garment mildew) because each names a genuinely distinct triggering condition with its
own examine-isolate-pronounce cycle, but I kept the chronic-case and all-over-white extension
(13:9-17) merged, since v.12's further condition continues describing the same referent rather
than opening an independent new case. I flag as a genuine, closer call the bed/seat contamination
register in 15:4-12 discussed above under larger_unit_preservation_check, and the eight-item
mixed cluster in 19:26-31 (divination, mourning rites, prostitution, Sabbath reverence, mediums),
which I consolidated into one chunk on the judgment that none of its five sub-topics carries its
own distinguishing introductory formula, though a reviewer favoring finer per-topic granularity
could reasonably split it into as many as five.

## epistle_unit_check_if_applicable

Not an epistle. Leviticus contains no epistolary material of any kind; the epistle_unit_checklist
in the quality protocol does not apply to this book.

## over_split_risk_check

My working read of the offering torot in chs.1-7 produced 33 chunks across 166 verses (roughly
5 verses per chunk), splitting each animal-source or occasion sub-case of every offering type as
its own unit, matching the granularity Exodus's own tabernacle-furniture-panel chunking used for
comparably repetitive ritual-specification material. I recognize a less granular reading could
merge, for example, the peace offering's herd case with its flock cases into two chunks instead
of three, or fold ch.2's raw and cooked meal-offering cases into one continuous unit; I settled
on the finer reading because each animal-class or preparation-type protasis is a real,
independently marked seam (tier-1 syntactic protasis/apodosis evidence under the owner addendum),
not merely a convenient dividing point. Against that, I deliberately consolidated several places
where I judged a per-protasis split would cross into over-fragmentation of genuinely repetitive
list material that T467 specifically flags as a risk for this book: the eight-item discharge-
contamination register in 15:4-12 (kept as one chunk rather than six or more single-object
cases); the eight-case מות יומת capital-crime list in 20:9-16 (kept as one chunk rather than
eight); the thirteen-item kinship-incest list in 18:6-18 (kept as one chunk); and the dense
single-clause command clusters in 19:11-14 and 19:26-31 (kept as two chunks covering nine verses
and five distinct sub-topics rather than nine or more single-verse fragments). I settled at 180
decisions for the whole book, above a 45-90 rule-of-thumb range but proportionate to the
Exodus book-writer's own precedent (144 decisions for a longer book with comparably dense
ritual-specification and legal-list material); I judged this the honest outcome rather than
force further merges, because Leviticus's five-layer offering-torah system (lay-facing plus
priestly-facing, five offering types each further subdivided), its five-chapter purity-law
case series with its own colophon system, and its Holiness-collection prohibition and penalty
lists are unusually dense in real, independently-marked seams that a "larger unit" reading
cannot honestly absorb into fewer chunks without erasing distinctions the text itself marks with
its own recurring formulas. Where I was genuinely unsure whether a split (or a merge) was earning
its keep, I flagged it in notes_for_review rather than silently picking a side (e.g. the
flock lamb/goat merger in 3:6-16; the vessel-contamination scope question in 11:29-38; the
19:5-10 and 19:11-14 cluster mergers; the 22:26-30 age/thanksgiving-timing merger; and the
question of whether 15:31's rationale clause belongs with its preceding case or with the
chapter's closing colophon).

## sidecar_specificity_plan

Sidecar rows (low_confidence_register, frontier_escalation_queue, atlas_candidate_feed) will
each name the concrete uncertainty driving the row, not a generic "low confidence" label — for
example "13:38-39's two-verse benign-bright-spot case could merge with the adjacent baldness case
into one 'minor conditions' chunk (13:38-44) rather than staying split, since the formula break
between them is real but thin" for M8-Lev-076/077, versus "the WEB/MT offset zone spanning all of
WEB Lev.6.1-30 means every decision in that span requires dual-numbering citation discipline
downstream, not just a one-time note" for the five ch.6 decisions, versus "the eight-case capital
crime list in 20:9-16 was deliberately kept as one chunk against T467's over-split caution; a
reviewer applying stricter per-offense granularity would produce a substantially different
sub-map for this one span" for M8-Lev-133. Leviticus has no frontier-book status and no
apocalyptic-visionary risk category, so I expect the frontier_escalation_queue to stay thin or
empty; the atlas_candidate_feed will draw primarily from the offering-torah addressee-layer
pairing (chs.1-5 lay-facing versus 6:8-7:36 priestly-facing torot for the same five offering
types, a natural cross-reference table a downstream atlas pass could build directly from this
chunk map), the five-torah purity-law colophon system (11:46-47, 12:7, 13:59, 14:54-57,
15:32-33), and the two narrative interruptions (ch.10; 24:10-23) as examples of scene-class
detection inside an otherwise legal book.

## chapter_only_fallback_reason_if_used

No chunk in this 180-decision map happens to span an entire chapter. This is not a coincidence I
need to explain away as a fallback; it follows directly from Leviticus's own density of internal
seams. Even the shortest and structurally simplest chapters carry a real internal break: ch.12
(8 verses) splits at its own zot torat colophon (12:7) and its own means-tested poor-provision
clause (12:8); ch.17 (16 verses) splits at its own resumptive "you shall say to them" reopening
formula (17:8); ch.21 (24 verses) splits at the addressee shift from ordinary priests to the high
priest specifically (21:10) and again at its own fresh messenger formula (21:16). Per the
CHAPTER-SHAPE RULE, a chunk that happens to equal one whole chapter would still be fine at honest
confidence in this book, since Leviticus is not pilot-fragile and carries no genuine chapter-wide
poetry/liturgy substrate (see substrate_markers_considered); it simply never arose here, because
every chapter boundary in this book coincides with, or falls inside, a stronger formula-marked
seam of its own.

## expected_low_confidence_regions

I expect reviewer disagreement to cluster around: (1) the granularity of the offering torot in
chs.1-7, where a reviewer favoring larger units could plausibly collapse my 33 chunks toward
half that number by merging animal-class sub-cases within a single offering type; (2) the
several deliberate consolidations flagged above under over_split_risk_check and
list_register_function_check (15:4-12, 18:6-18, 19:11-14, 19:26-31, 20:9-16), any of which a
stricter per-protasis or per-topic reader could split further; (3) the WEB/MT offset zone in
ch.6, where the dual-citation discipline itself (not the boundary placement) is the likely
friction point; (4) the boundary treatment of ch.16's Day of Atonement narrative, where I split
by ritual-action object (bull, then goat, then scapegoat) rather than by a formula, since the
chapter contains no internal messenger-formula breaks at all after v.1-2 — every boundary from
16:6 onward rests on participant/object-change evidence alone, which is real but softer than a
fresh speech formula; and (5) the exact point at which ch.23's Booths entry closes (23:37-38's
summary formula) before its own supplementary material resumes at v.39, which I read as one
interrupted entry rather than two independently closed units, a genuinely debatable call I
flagged in that decision's notes_for_review.

## frontier_or_atlas_candidate_expectations

Leviticus is not a frontier book (frontier status applies only to Dan and Rev per the quality
protocol), so I expect zero frontier_escalation_queue rows driven by apocalyptic/visionary risk.
I do expect several atlas_candidate_feed rows: the lay-facing/priestly-facing offering-torah
pairing across chs.1-5 and 6:8-7:36 (a natural cross-reference table, structurally analogous to
Exodus's instruction/execution tabernacle-panel pairing); the five-chapter purity-law colophon
system (11:46-47 through 15:32-33) as a template for how zot torat closing formulas function
across the book, including the two book-spanning colophons at 26:46 and 27:34; the two narrative
interruptions of otherwise legal material (ch.10's Nadab/Abihu crisis, 24:10-23's blasphemer
incident) as examples of scene-class detection inside a predominantly legal book; and the
ch.26 five-tier covenant curse escalation as a clean example of a repeated intensification
formula driving chunk boundaries independent of any messenger-formula or addressee change.

## post_adjudication_outcome

This section records the outcome of the blind review mesh and boss-adjudication rounds that
followed the candidate chunk map above. It is a factual summary, added after the fact; the
sections above are the original, unaltered candidate authoring.

- Final decision count: 184 (started at 180; net +4 across four merges and eight splits).
- Merges: 4:1-2 into 4:3-12 (010→011), 12:6-7 into 12:1-5 (063→062), 14:4-7 into 14:1-3
  (075→074), and 16:11-14 into 16:6-10 (094→093) on a corrected reading of the 16:11
  Wiederaufnahme: v.11's near-verbatim repetition of v.6 resumes one interrupted sin-offering
  procedure across the vv.7-10 goat-lot digression rather than opening a second one; the real
  seam moved to 16:15's new sacrificial object and widening scope.
- Splits: 2:4-13, 3:6-16, 15:28-31, 19:5-10, 19:32-34, 21:16-24, and 23:33-38 each split once
  (new siblings M8-Lev-181-185, 187-188), and 21:7-9 was re-cut into a four-way layout with
  21:1-6 (new sibling M8-Lev-186 for 21:9) after both primaries' partial challenges were
  synthesized into one reading neither had stated in full: 21:1-4 (3ms) | 21:5-8 (3mp, absorbing
  the wrongly-truncated 21:5-6) | 21:9 (fresh 3fs case) | 21:10-15 (unaffected).
- Four shift-pairs moved a boundary between existing neighbors without changing decision count:
  8:22-30/8:31-36 to 8:22-29/8:30-36 (honoring the כאשר צוה יהוה את משה refrain at v.29, which
  the original span crossed unremarked); 24:13-16/24:17-22 to 24:13-14/24:15-22 (the addressee
  redirect at v.15 plus the כגר כאזרח envelope, correcting a cut that split an identical ואיש כי
  construction left unsplit at v.19); and 25:8-12/25:13-17 to 25:8-13/25:14-17 (v.13 closes the
  Jubilee proclamation's own return-to-holding inclusio; v.14 is the actual sale-case protasis).
- A coda-genre family was formalized (2:11-13, 3:17, 7:22-27, 11:41-45) after the 2:11-13 split
  applied the identical 2mp-addressee-shift criterion that already kept 3:17 standalone; a
  parallel transmission-notice family (21:24, 23:44, 24:23) was brought to one consistent
  treatment after 21:24 split to match the other two sites' refrain-closure-plus-Moses-wayyiqtol
  profile, which the original draft had applied inconsistently.
- Every hold was sustained: 7 of 7 (6 overruled challenges plus 1 ruled insufficient-evidence/
  marker-only), including 3:17's standalone status, 15:16-18's asher-vs-ki list-item reading,
  18:6-18's kinship-list boundary (the 18:17b laqach-construction straddle preserved as
  counterevidence against moving 18:18), 22:26-30's metadata-only paragraph-break challenge, and
  the ch.26 tier-five/exile boundaries at 26:33/34 (the WEB v.36 alternative preserved on record,
  not adopted, since the אז-plus-land-subject-shift at v.34 outranks paragraph metadata). Zero
  human holds were needed.
- Confidence recalibrations: two decisions were raised from low (4:32-35, 8:10-13) on review
  that their boundary evidence was as strong as structurally identical neighbors already rated
  medium/high; one (26:40-45) was lowered from high to medium after its "protasis" claim was
  shown to rest on a WEB conditional rendering rather than a marked Hebrew אם/כי, re-grounded
  instead on the או אז discourse pivot and the וזכרתי covenant-remembrance chain.

**Correction (post-postcheck, boss-recorded):** the final count is 185, not 184 — a final micro-round split M8-Lev-189 (Lev.21.8) out of the ch. 21 layout after this section was written, making ch. 21 five-way (1-4 | 5-7 | 8 | 9 | 10-15) per the revision peer's verified grammar; the packet history records the overruled boss differentiator honestly.
