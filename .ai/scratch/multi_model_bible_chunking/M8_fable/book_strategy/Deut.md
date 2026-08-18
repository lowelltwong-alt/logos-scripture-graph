# Deuteronomy (Deut) — Book Strategy Note — M8_fable (claude-sonnet-5, book_writer)

This note records my independent literary-chunking strategy for Deuteronomy, authored alone as
a fresh instance with no context from any other book in this campaign. I read the full WEB text
(Deut_web_clean.txt) chapter by chapter, cross-checked chapter-level substrate marker counts in
chapter_profile.json, verified exact verse totals against verse_inventory.json (959 verses,
1:1-34:12), and read the Hebrew (Deut_oshb.txt, MT-numbered, verse-per-line) in full to confirm
every quoted formula before citing it as evidence. I handled the three verified WEB/MT
versification offsets flagged in web_mt_crosswalk.json — the 12:32/MT 13:1 seam (WEB 12:32-13:18
= MT 13:1-19, "the classic ch.13 offset"), the 22:30/MT 23:1 seam (WEB 22:30-23:25 = MT 23:1-26,
"the classic ch.23 offset"), and the 29:1/MT 28:69 seam (WEB 29:1-29 = MT 28:69-29:28, the Moab
covenant superscription) — by citing both WEB and MT verse numbers at every decision inside those
zones and by defaulting sub-verse mapping claims to caution rather than certainty. I worked in
isolation, reading only the M8_fable folder and shared_research_baseline/, and made every boundary
call myself. This document is scratch, non-authorizing candidate work for T423 — not canon, not a
reviewed verdict, and not theology. My strategy and the evidence weighing behind it follow the
owner addendum m8-mesh-r2: the text's own signals drive boundaries; Masoretic petuchah and
disjunctive accents corroborate but never originate one; setumah is weaker corroboration still;
chapter and verse numbers, modern headings, footnotes, and Strong's tags are metadata only, never
boundary evidence.

## selected_strategy

My strategy lets Deuteronomy's own recurring covenant-document devices do the boundary work,
weighted in this order: (1) the book's three explicit superscription/colophon formulas —
אֵלֶּה הַדְּבָרִים אֲשֶׁר דִּבֶּר מֹשֶׁה (1:1), וְזֹאת הַתּוֹרָה / אֵלֶּה הָעֵדֹת (4:44-45), and
אֵלֶּה דִבְרֵי הַבְּרִית (29:1/MT 28:69) — each of which I treat as opening rather than closing
material, on the strength of how "אֵלֶּה/וְזֹאת" consistently functions elsewhere in this book's
own usage; (2) recurring narrative-and-speech frames — the וַיְדַבֵּר/וַיֹּאמֶר יְהוָה אֵלַי
formula marking Moses's recalled divine speech throughout the historical retrospective (chs.1-3),
the בָּעֵת הַהִוא ("at that time") formula marking a fresh charge to a new addressee, and the
שְׁמַע יִשְׂרָאֵל summons opening major discourse turns (5:1, 6:4, 9:1, 20:3) — weighed against
whether the surrounding material had genuinely closed before I let a fresh occurrence drive a
boundary; (3) the law code's own protasis/apodosis case-law chains, where a fresh כִּי/אִם/לֹא
opening reliably marks a new case even when the case is only one or two verses long, the single
strongest and most consistent evidence type in chs.12-26; (4) list/register formulas — the
Decalogue's ten commands (5:6-21), the twelve Ebal curses (27:15-26), the six-fold blessing and
curse mirrors (28:3-6, 28:16-19), and the Blessing of Moses's eleven "About X he said" tribal
sayings (33:6-29) — each judged on its own internal structure for whether its entries vary in
real content or merely repeat one template with a name or number changing, discussed at length in
list_register_function_check; and (5) the poem's own explicit formal markers in the two poetic
insets (chs.32-33), where I let the WEB layout's own |b (blank poetry line) stanza-break markers
in the Song of Moses and the poem's own eleven-times-repeated "About X he said" formula in the
Blessing of Moses carry primary evidentiary weight, corroborated by chapter_profile.json's q1/q2
poetry-marker counts but never driven by them alone. I settled at 241 decisions for 959 verses, a
density of 3.98 verses/decision — denser than this campaign's precedent for narrative-and-register
books, which I read as proportionate rather than inflated given how much of this particular book
is genuinely case-law material (chs.12-26) whose own כִּי-chains mark real seams every one to
four verses, and liturgical register material (the twelve Ebal curses, the Decalogue's terse
second table, the six-fold blessing/curse mirrors) whose granularity I judged case by case rather
than defaulting to either extreme. Every claim in this strategy rests on textual evidence drawn
directly from Deut_web_clean.txt and Deut_oshb.txt; no claim rests on Strong's-tier metadata (see
strongs_metadata_considered_evidence_only) or on source-critical labels (see
source_metadata_evidence_only_check).

## literature_type_or_mixed_genre

Deuteronomy presents as a single sustained address in Moses's voice, but it is not one genre
throughout, and I treated each chunk's local form on its own terms. The book opens and re-opens
three times on a covenant-document superscription (1:1-5, 4:44-49, 29:1/MT 28:69), a distinct
documentary-framing genre that names speaker, audience, place, and occasion before the address
itself begins. The historical retrospective (chs.1-3) is narrative prose in Moses's own recalled
first-person voice, built from repeating command-and-report beats (Edom, Moab, Ammon, Sihon, Og)
that I judged individually rather than mechanically. The motivational discourse (chs.4, 6-11) is
hortatory prose built on recurring imperatives ("Only take heed," "Be very careful," "Now, Israel,
what does Yahweh require") and the Shema's own confessional core (6:4-9). Chapter 5 is a hybrid:
a narrative frame (5:1-5, 5:22-33) bracketing the Decalogue's own apodictic legal register
(5:6-21), which I treated with mixed granularity (see literary_form_decision_matrix). The law code
proper (chs.12-26) is casuistic case law, structurally the closest material in this book to
Leviticus's own legal register, built almost entirely from כִּי/אִם-opened cases that I split at
a rate close to one decision per one-to-four verses because the text's own case-chain evidence is
that dense and that consistent. The Ebal ceremony (ch.27) is covenant liturgy — a scripted,
congregationally-responsive curse series distinct in form from the surrounding case law. The
blessing-and-curse address (ch.28) is prophetic-style poetic-prose escalation, the longest single
chapter in the book, alternating liturgical registers (the six-fold parallel blessings and curses)
with sustained narrative-style catastrophe description. The Moab covenant address (chs.29-30) is
hortatory prose resembling chs.6-11 but explicitly framed as a second, distinct covenant occasion.
The succession material (ch.31) is narrative prose covering several distinct scenes (farewell,
Joshua's commissioning, the law's deposit, the Tent-of-Meeting theophany, the Song's
commissioning). The Song of Moses (32:1-43) and the Blessing of Moses (33:1-29) are this book's
only sustained poetry, each with its own distinct internal structure — the Song built in
formally-marked strophes, the Blessing built as eleven tribal sayings each introduced by its own
formula — and I treated each on the strength of its own formal markers rather than importing one
poetry-splitting rule across both. The closing death narrative (ch.34) returns to narrative prose.
Every literature_type_guess field in draft_decisions.json names a specific, book-local form (e.g.
"apostate_city_herem_law," "curse_five_perverting_justice," "sixfold_blessing_register") rather
than a generic label, and I did not let the book's overall "law and covenant" reputation flatten
the real formal differences between, say, a two-verse casuistic pledge-etiquette case and a
twelve-entry liturgical curse series.

## literary_form_decision_matrix

- A superscription formula (אֵלֶּה הַדְּבָרִים, וְזֹאת הַתּוֹרָה / אֵלֶּה הָעֵדֹת, אֵלֶּה דִבְרֵי
  הַבְּרִית) → strong boundary opening a fresh major section, read as forward-looking on the
  strength of the book's own consistent usage of אֵלֶּה/וְזֹאת elsewhere, not as a backward-looking
  colophon summarizing what precedes — the single interpretive commitment this book most depends
  on, discussed fully at 29:1 in expected_low_confidence_regions.
- A recalled-speech formula naming a fresh addressee (וַיְדַבֵּר/וַיֹּאמֶר יְהוָה אֵלַי, וָאֲצַוֶּה
  אֶתְכֶם בָּעֵת הַהִוא) → candidate boundary, weighed against whether the prior scene had
  genuinely closed; I did not split a single continuous scene merely because "at that time"
  recurs mid-scene without a genuine addressee or topic change (e.g. I kept 1:9-15 as one unit
  despite "at that time" also appearing at its close).
- A casuistic protasis opening a law-code case (כִּי/אִם/לֹא beginning a fresh scenario) → strong
  boundary in chs.12-26, the single most consistent evidence type in this book, honored even when
  the resulting case is a single verse (e.g. 19:14's landmark prohibition, 24:6's millstone-pledge
  rule) — see law-code granularity policy below.
- A list/register formula (the Decalogue's ten commands, the Ebal curses' אָרוּר...אָמֵן refrain,
  the blessing/curse sixfold mirrors, the Blessing of Moses's "About X he said" tribal formula) →
  a candidate internal boundary within the register, weighed case by case against whether the
  register's own content genuinely varies entry to entry or merely repeats one template with a
  name, number, or life-domain changing — the specific test discussed at length in
  list_register_function_check, where I reached opposite conclusions for the twelve Ebal curses
  (split) and the sixfold blessing/curse mirrors (kept whole).
- An explicit poetic-performance or strophe marker (the Song of Moses's own |b blank-poetry-line
  stanza breaks in the WEB layout; the Blessing of Moses's eleven-times-repeated "About X he said"
  formula) → strong boundary, the strongest available formal evidence in this book's two poems,
  weighted above chapter_profile.json's q1/q2 marker counts, which corroborate but never
  originate a split (see substrate_markers_considered).
- A dual WEB/MT citation requirement inside the three flagged crosswalk zones (12:32-13:18,
  22:30-23:25, 29:1-29) → does not by itself drive a boundary, but requires dual verse citation
  in every decision whose span touches those zones, and at the two chapter-line seams themselves
  (12:32/MT13:1 and 29:1/MT28:69) I flagged the decision itself as a genuine cross-tradition
  ambiguity at low confidence rather than presenting either reading as settled.
- Chapter and verse numbers, WEB's own paragraph (¶) marks, and footnotes → metadata only, never
  boundary authority on their own; where a paragraph mark coincides with a real content seam I
  cited the content seam, not the mark, as the evidence (e.g. 14:21's internal ¶ before the
  kid-in-milk clause corroborates but does not by itself establish the seam I already read from
  the topic shift).

## substrate_markers_considered

I read chapter_profile.json's per-chapter marker counts alongside the WEB text's own ¶, [fn], and
|q1/|q2/|b poetic-lineation tags directly. Two chapters carry the has_poetry_or_liturgy_marker
flag with substantial q1/q2 counts: ch.32 (q1=59, q2=85, b=6 — the Song of Moses) and ch.33
(q1=40, q2=56, b=2 — the Blessing of Moses); ch.31 carries a single q1=1 marker (the brief poetic
cue at 31:19 introducing the coming Song). In both major poems I treated the marker counts as
corroboration that real verse is present, but let the poems' own more specific formal devices —
the Song's five internal |b blank-poetry-line stanza breaks (falling after 32:22, 32:27, 32:33,
32:38, and 32:42, which I used as primary strophe-boundary evidence for decisions M8-Deut-217
through M8-Deut-222) and the Blessing's eleven-times-repeated "About X he said" tribal formula —
actually decide where each poetic unit starts and ends, exactly as the campaign's evidence-weight
ordering requires: the marker corroborates that a chapter contains real verse, but the formula or
stanza break is what tells me where. Paragraph (¶) density is highest in ch.27 (p=26, the Ebal
ceremony's own dense turn-taking between narration and the twelve-times-repeated "All the people
shall say, Amen" congregational response) and lowest in chs.7 and 15 (p=1 each, sustained
hortatory prose with few typographic breaks); I let ch.27's high ¶ density inform my sense that
WEB itself marks a fresh typographic beat at every curse-and-Amen pair, corroborating (though not
solely driving, per the campaign's evidence weighting) my decision to split the twelve curses
individually rather than merge them (see list_register_function_check). Footnote density spikes at
ch.1 (f=8, mostly proper-name and Hebrew-term glosses) and ch.22 (f=6, mostly measurement glosses
for the fifty/hundred-shekel fines); I treated every footnote strictly as metadata, never as
boundary evidence, consistent with strongs_metadata_considered_evidence_only below. The one
chapter with a m=1 marker (ch.5, a musical/liturgical notation cue at the Decalogue's own opening
in WEB's rendering, "¶(m)" before v.6) corroborated my reading of 5:6 as functioning differently
in mood from the surrounding narrative frame, though I grounded that decision primarily in the
verse's own declarative (not apodictic) syntax, not in the marker.

## strongs_metadata_considered_evidence_only

No Strong's numbers, lemma tags, or morphology codes are present in this cleaned WEB substrate, so
none were available to weigh as direct evidence anywhere in this chunk map. This is a considered
position stated for the record, not an oversight: Deuteronomy's case-law chapters (12-26) are
exactly the kind of material where a chunker might be tempted to lean on lexical apparatus to
distinguish, say, whether two occurrences of a term like "gate" (שַׁעַר) mark parallel legal
registers or independent local rulings, and I deliberately did not reach for that kind of
evidence even where it was unavailable to reach for. Where WEB footnotes gloss a Hebrew term (e.g.
"Elohim" at 1:6, "Yahweh" at 1:3, a shekel's weight at 22:19, a cubit's length at 3:11) or note a
textual variant (the LXX reading appended at 32:43's footnote), I used that only as background
color, never as the reason for a boundary — the 32:43 LXX variant note in particular did not move
my strophe boundary there, which rests instead on the WEB poem's own final |b marker before it.
Every boundary_evidence_refs entry in draft_decisions.json cites either the WEB text itself or the
OSHB Hebrew text directly, and the strategy throughout treats Strong's-tier metadata exactly as
tier 4 under the owner addendum: available for color, never for boundary authority.

## source_metadata_evidence_only_check

I did not use documentary-hypothesis source labels (D, Dtr, P, or any other siglum), nor any
theory about which redactional layer produced the historical retrospective versus the law code
versus the poems, as boundary authority anywhere in this chunk map. Deuteronomy is a textbook
case where a source-critical reader might want to treat the three address-openings (1:1, 4:44,
29:1) as evidence of distinct compositional strata later stitched together, or read the law code's
own internal doublets (two herem-conquest reports for Sihon and Og in chs.2-3; the centralization
law's own repeated formula appearing at 12:5, 12:11, 12:14, 12:18, 12:21, and 12:26) as evidence
of redactional accretion. I deliberately did not do this: my boundary at each of the three
superscriptions rests on the same אֵלֶּה/וְזֹאת-colophon logic I apply consistently across the
whole book, not on any prior theory about which "layer" produced which address, and my splitting
of the centralization law's repeated "the place which Yahweh your God shall choose" formula
(chs.12, 14, 15, 16) rests on each occurrence's own local case-chain context (a fresh כִּי-opened
case each time), not on a claim that the repetitions reveal compositional history. I likewise did
not treat the book's well-known internal doublets — the Decalogue itself echoing Exodus 20 (a
comparison outside this book's own scope, which I did not import), or the near-identical
"remember you were a slave in Egypt" rationale clause recurring at 5:15, 15:15, 16:12, 24:18, and
24:22 — as evidence of, or against, a redactional seam; I read each recurrence as the text's own
deliberate rhetorical refrain reinforcing distinct local cases, and cited that literary function
directly in the relevant decisions, never a source-critical theory about how the refrain came to
recur.

## larger_unit_preservation_check

I actively resisted splitting in several places where a less careful pass might over-atomize. The
whole firstfruits recitation liturgy (26:5-10) stays one chunk despite covering several distinct
historical beats (bondage, affliction, deliverance, land-gift), because it is one continuous
scripted performance-speech bounded by a single explicit introducing formula ("You shall answer
and say before Yahweh your God") and closed by its own presentation clause, not a chain of
independent cases. The whole Levi tribal saying (33:8-11) stays one chunk despite covering
priestly testing, teaching function, and altar service, because all three remain governed by the
single "About Levi he said" formula with no fresh introducing clause dividing them — the same
"one governing formula, multiple content beats" logic that keeps the Joseph saying (33:13-17)
whole despite its own long agricultural-and-military catalog. The whole unsolved-murder expiation
ritual (21:1-9) stays one chunk despite covering the elders' measuring procedure, the heifer rite,
and the priestly declaration, because the measuring procedure exists only to identify which city
performs the single ritual that follows, one continuous procedure rather than a chain of
independent cases. The whole vine-and-corruption reflection in the Song of Moses (32:28-33) stays
one strophe because no |b marker interrupts it, even though a less careful pass might split the
folly-reflection (vv.28-30) from the vine-of-Sodom image (vv.31-33) on thematic grounds alone. In
each case a finer split would have cut one coherent scripted performance, ritual, tribal saying,
or poetic strophe in half at a point the text itself marks with nothing more than a topic
sub-beat, not a real formal seam.

## list_register_function_check

I split a register only where its own content genuinely varied entry to entry, not merely where a
name, number, or life-domain changed. Three decisions anchor this test explicitly, because they
produce genuinely opposite outcomes on materially similar-looking liturgical registers, and I want
to be explicit about why.

**The twelve Ebal curses (27:15-26).** Each curse opens on the identical אָרוּר...וְאָמַר כָּל
הָעָם אָמֵן template, and a less careful pass could read this as one repeated-template register
the way a census tally or an offering catalog might be kept whole. I rejected that reading and
split the series into twelve separate decisions (M8-Deut-165 through M8-Deut-176), because every
single entry names a genuinely distinct moral offense — idolatry, filial dishonor, boundary-moving,
misleading the blind, denying justice to the vulnerable, five separate incest/bestiality cases,
secret murder, judicial bribery, and a closing general-noncompliance formula — with no two curses
addressing the same underlying wrong. This is the single most contestable granularity call in the
whole book, and I have flagged it explicitly in notes_for_review at M8-Deut-165: a reviewer
applying a stricter "one register, one decision" rule to any uniformly-templated liturgical series
would produce a substantially different, single-decision reading of this whole span.

**The sixfold blessing and curse mirrors (28:3-6, 28:16-19).** These four short parallel clauses
each (city/field, body/ground/animals, basket, coming/going) look formally identical to the Ebal
curses — a repeated template performed in sequence — but unlike the Ebal curses, every entry
varies only the life-domain named within one undifferentiated prosperity-or-ruin statement, not
the underlying moral content. I kept each of these two four-clause registers as a single decision
apiece (M8-Deut-178, M8-Deut-181), the opposite granularity from the Ebal curses, and I flagged
this contrast explicitly in a notes_for_review on M8-Deut-178: the same repeated אָרוּר/בָּרוּךְ
surface form produced opposite splitting decisions in this book depending on whether the
underlying content varied (Ebal: yes, twelve distinct offenses) or did not (ch.28's sixfold
mirrors: no, one undifferentiated prosperity template repeated across four life-domains).

**The Decalogue's second table (5:17-21).** I kept the five terse commands — murder, adultery,
theft, false witness, coveting — as one register decision (M8-Deut-037) rather than splitting each
into its own decision the way I split every elaborated first-table command (5:7, 5:8-10, 5:11,
5:12-15, 5:16). This is a genuinely different case from either curse series above: each of the
five second-table commands is topically distinct (murder is not theft), which would argue for a
finer split on the same content-variance logic that split the Ebal curses; but every one of the
five is also a single unelaborated clause with no rationale of its own, structurally uniform in a
way none of the first-table commands are, which argues for treating them as one terse register. I
resolved this tension toward the register reading and flagged it explicitly at low confidence in
notes_for_review, since I judge this the closer call of the two register questions in this book —
closer than the Ebal-curses call, where the twelve curses' shared "identical template" surface
form is thinner justification for merging than the second table's genuinely uniform terse
structure.

## epistle_unit_check_if_applicable

Not an epistle. Deuteronomy contains no epistolary material of any kind; the epistle_unit_checklist
in the quality protocol does not apply to this book.

## over_split_risk_check

My working read of the law code (chs.12-26) produced roughly 145 decisions across about 350
verses, a density near 2.4 verses/decision, markedly finer than the book's own 3.98
verses/decision average. I recognize a less granular reading could merge several of the
shortest single-verse cases (19:14's landmark prohibition, 24:6's millstone-pledge rule, 22:5's
cross-dressing prohibition, 22:8's rooftop-railing law, 22:12's tassels law) into their nearest
neighbors rather than giving each its own decision; I settled on the finer reading because every
one of these short cases opens on its own fresh casuistic protasis with no shared vocabulary or
rationale linking it to the case before or after it — the campaign's own weighting explicitly
names case-law protasis/apodosis chains as boundary-driving evidence, and I judged it inconsistent
to honor that evidence for four-verse cases while waiving it for one-verse cases that carry the
identical formal marker. Against that, I deliberately consolidated several places where I judged a
per-item split would cross into over-fragmentation of genuinely uniform material: the whole
sixfold blessing and curse mirrors (28:3-6, 28:16-19, discussed above); the whole officers'
four-category military exemption speech (20:5-9, kept whole because all four exemptions share one
identical "מִי הָאִישׁ...יֵלֵךְ וְיָשֹׁב לְבֵיתוֹ" template varying only the disqualifying
circumstance); the whole gleaning-laws register (24:19-22, kept whole because grain, olive, and
vineyard gleaning share one identical closing formula applied three times); and the whole
Zebulun/Issachar paired tribal saying (33:18-19, kept as one decision because the poem itself
addresses both tribes under a single introducing formula rather than two). I settled at 241
decisions for the whole book — well above the 45-90 rule-of-thumb range, but at a verses-per-
decision rate (3.98) that reflects genuine textual density in this book's dominant case-law and
liturgical-register material rather than an inflated count; two of this book's longest single
spans (the 32:1-3 Song invocation's surrounding strophes and the 26:5-10 firstfruits liturgy) are
single decisions that pull the book's average chunk size up, not down, against the ~145
decision-heavy law-code chapters that pull it down. Where I was genuinely unsure whether a split
was earning its keep, I flagged it in notes_for_review rather than silently picking a side —
most notably the 27:15-26 Ebal-curse twelve-way split (M8-Deut-165), the 5:17-21 Decalogue
second-table register call (M8-Deut-037), and the three WEB/MT chapter-boundary seams
(M8-Deut-076 at 12:32/MT13:1, M8-Deut-132 at 22:30/MT23:1, M8-Deut-194 at 29:1/MT28:69).

## sidecar_specificity_plan

Sidecar rows (low_confidence_register, frontier_escalation_queue, atlas_candidate_feed) will each
name the concrete uncertainty driving the row, not a generic "low confidence" label — for example
"the 27:15-26 Ebal-curse series was deliberately split into twelve single-curse decisions against
a plausible one-register reading matching the sixfold blessing/curse mirrors elsewhere in this
book; a reviewer applying a stricter uniform-template rule would produce a single-decision reading
of this whole span" for M8-Deut-165 through M8-Deut-176, versus "WEB Deut.29.1 = MT Deut.28.69,
and while I read the אֵלֶּה-colophon as forward-looking (opening the Moab covenant address) on the
strength of this book's own consistent אֵלֶּה-usage, MT's own chapter division reads the same
verse backward as ch.28's closing colophon; a reviewer honoring MT's own chapter boundary as
corroborating evidence would side differently" for M8-Deut-194, versus "the Decalogue's second
table (5:17-21) was kept as one register decision despite each of its five commands naming a
genuinely distinct offense, on the strength of their shared unelaborated one-clause structure; a
reviewer applying the same content-variance test used for the Ebal curses would split this into
five decisions" for M8-Deut-037. Deuteronomy has no frontier-book status (frontier status applies
only to Dan and Rev per the quality protocol), so I expect the frontier_escalation_queue to stay
thin or empty despite the covenant-curse material's own intensity (chs.27-28's sustained
catastrophe imagery) — this is covenant-liturgical and hortatory material, not apocalyptic-
visionary material, and I did not treat it as frontier-adjacent. The atlas_candidate_feed will draw
primarily from the three-superscription structural pattern (1:1, 4:44-49, 29:1/MT28:69) as a
worked example of how a single book can mark multiple internal covenant-document openings, the
Song-of-Moses/Blessing-of-Moses pairing (chs.32-33) as this book's two formally distinct poems each
governed by a different kind of internal marker (stanza breaks versus a repeated tribal formula),
the twelve-curse-versus-sixfold-mirror contrast (chs.27-28) as a worked example for any downstream
methodology pass of how superficially identical liturgical templates can license opposite
splitting decisions depending on real content variance, and the three WEB/MT crosswalk zones as a
concentrated case study in dual-tradition versification citation discipline.

## chapter_only_fallback_reason_if_used

No chunk in this 241-decision map happens to span an entire chapter. This follows directly from
how densely this book marks its own internal seams even in its shortest or most narratively simple
chapters: even ch.13 (18 verses, entirely inside the first WEB/MT offset zone) splits into three
case-chain decisions on its own three-fold prophet/family/city escalation structure; even ch.34
(12 verses, the book's shortest and closing chapter) splits into four decisions on its own
viewing/death/succession/colophon structure; even ch.6 (25 verses, mostly the tightly unified
Shema material) splits into five decisions on its own heading/Shema/warning/warning/catechesis
turns. Per the CHAPTER-SHAPE RULE, a chunk that happens to equal one whole chapter would still be
fine at honest confidence in this book, since Deuteronomy is not pilot-fragile and carries genuine
poetry/liturgy substrate concentrated in only three chapters (5's Decalogue register, 32's Song,
33's Blessing) rather than throughout; it simply never arose here, because even this book's
plainest hortatory or narrative chapters carry at least one internal formula-, addressee-, or
case-marked seam of their own.

## expected_low_confidence_regions

I expect reviewer disagreement to cluster around: (1) the three WEB/MT chapter-boundary seams
(12:32/MT13:1, 22:30/MT23:1, and especially 29:1/MT28:69), where the very choice of which
tradition's chapter division to honor as corroborating evidence is the likely friction point, not
the underlying content itself — marked low confidence at M8-Deut-076, M8-Deut-132, and
M8-Deut-194; (2) the 27:15-26 Ebal-curse twelve-way split, where a reviewer could reasonably prefer
a single-register reading matching the sixfold blessing/curse mirrors of ch.28, discussed at
length in list_register_function_check; (3) the Decalogue's second-table register call (5:17-21),
the closest single register-granularity judgment call in the book, discussed above; (4) the long,
interleaved curse-escalation catalog of ch.28 (vv.20-57), where my thematic-wave groupings
(disease, property loss, exile, agricultural futility, siege horror) rest on real but softer
content-cluster evidence than the case-law chains elsewhere in the book, since the catalog itself
supplies no fresh formula at every wave boundary the way the law code's כִּי-clauses do — several
of these decisions (M8-Deut-182 through M8-Deut-189) carry low confidence and explicit
notes_for_review flagging plausible alternative groupings; and (5) several of the shortest law-code
cases (19:14, 22:5, 22:8, 22:12, 24:6, 24:7), which rest on their own casuistic opening formula as
essentially their only evidence, each a single verse with no elaboration, flagged low-to-medium
confidence throughout as genuinely thinner-evidenced calls than the book's longer, more heavily
signaled cases.

## frontier_or_atlas_candidate_expectations

Deuteronomy is not a frontier book (frontier status applies only to Dan and Rev per the quality
protocol), so I expect zero frontier_escalation_queue rows driven by apocalyptic/visionary risk,
notwithstanding ch.28's sustained catastrophe imagery and the Song of Moses's own cosmic-witness
invocation, both of which I read as covenant-liturgical and hortatory intensity rather than
apocalyptic vision. I do expect several atlas_candidate_feed rows: the three-superscription
covenant-document structure (1:1, 4:44-49, 29:1/MT28:69) as a template for how this campaign might
track a single book's own internal re-opening of its address frame; the Song-of-Moses/Blessing-of-
Moses pairing (chs.32-33) as a worked example of two formally distinct marker types (explicit
typeset stanza breaks versus a repeated introducing formula) governing poetry within the same
book; the twelve-Ebal-curse-versus-sixfold-blessing-mirror contrast as a clean worked example, for
any downstream methodology pass, of how a chunker should test a liturgical register's real content
variance rather than mechanically splitting or merging on template-uniformity alone; and the three
WEB/MT crosswalk zones as a concentrated case study in cross-tradition versification citation
discipline, complementing whatever comparable zones other Torah books in this campaign surface in
their own crosswalks.

## post_adjudication_outcome

Final map: 246 active decisions (241 frozen, 3 retired by merge — 185, 201, 218 — and 8 created by
split: 242, 243, 244, 250, 251, 252, 253, 254), exact 959/959 coverage, zero chapter-shaped rows.
Confidence spread 39 high / 188 medium / 19 low; final states 244 accepted_candidate, 2
held_lower_confidence (101 king-law internal seam, 193 inside the marker-silent 28:15-68 stretch —
both insufficient_evidence conceded honestly). Zero appeals, zero ultra requests, zero human holds.

Round 1 ran two blind primaries per decision (4 OL opus + 4 LF sonnet instances) yielding 51
challenge objects + 1 frontier_defer + 3 insufficient_evidence flags over 49 decisions; 4 peer
crosscheckers supported 54 of 56 digest rows and disputed 2. The author answered all 56 (52
accept / 4 dispute, every dispute aligned with the peer). Boss rulings: 51 upheld_as_amendment, 2
upheld (the two IE concessions), 3 overruled. A single-reviewer opus revision round (52 materially
changed rows, then 8-row and 5-row follow-ups) filed 25 further challenge objects, all upheld as
amendments across micro rounds r2-r5; a decorrelated sonnet second primary + revision peer covered
the 8 round-created rows (all supports). The named crux WEB 12:32 = MT 13:1 resolved at candidate
level (petuchah after MT 13:1 two-witness, doubled shamor closing frame, cataphoric ha-davar), so
the frontier queue stayed empty.

Signature findings: the twelve Ebal curse decisions survived a genuine 3-vs-1 register dispute and
now stand on the per-curse performative Amen closure (v.15 plural variant disclosed) at medium —
the closure-formula criterion, not offense-count, differentiates them from the merged 28:38-42
futile-labor chain (REL-001). The Song of Moses (32:1-43) and MT 28:15-68 carry no internal
pe/samekh, so every seam there is text-signal-only; two WEB \b-driven claims were retired as
metadata. Deuteronomy's parashah record is two-witness exact (OSHB=UXLC: 32 pe / 135 samekh,
site-level diff clean). A deterministic consonantal citation sweep (ellipsis-aware,
ketiv/qere-aware) now guards every oshb: ref — it caught 3 defects the mesh missed and should be
run for every remaining book.
