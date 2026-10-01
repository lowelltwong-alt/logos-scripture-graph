# Numbers (Num) — Book Strategy Note — M8_fable (claude-sonnet-5, book_writer)

This note records my independent literary-chunking strategy for Numbers, authored alone as a
fresh instance with no context from any other book in this campaign. I read the full WEB text
(Num_web_clean.txt) chapter by chapter, cross-checked chapter-level substrate marker counts in
chapter_profile.json, verified exact verse totals against verse_inventory.json, and read the
Hebrew (Num_oshb.txt, MT-numbered, verse-per-line) throughout to confirm formula wording before
citing it as evidence. I handled the five verified WEB/MT numbering offsets flagged in
web_mt_crosswalk.json — chapter 16 (web_extra_15, WEB 16:36-50 = MT 17:1-15), chapter 17
(mt_extra_15, all of WEB 17 = MT 17:16-28, no WEB superscription), chapter 25 (mt_extra_1, MT
25:19 folds into WEB 26:1's opening clause), chapter 29 (web_extra_1) and chapter 30
(mt_extra_1, the WEB 29:40/MT 30:1-2 seam) — by citing both WEB and MT verse numbers at every
decision inside those zones and by defaulting sub-verse mapping claims to caution rather than
certainty, exactly as the crosswalk's own citation_rule fields specify. I worked in isolation,
reading only the M8_fable folder and shared_research_baseline/, and made every boundary call
myself. This document is scratch, non-authorizing candidate work for T423 — not canon, not a
reviewed verdict, and not theology. My strategy and the evidence weighing behind it follow the
owner addendum m8-mesh-r2: the text's own signals drive boundaries; Masoretic petuchah and
disjunctive accents corroborate but never originate one; setumah is weaker corroboration still;
chapter and verse numbers, modern headings, footnotes, and Strong's tags are metadata only,
never boundary evidence.

## selected_strategy

My strategy is to let Numbers's own recurring structural devices do the boundary work, weighted
in this order: (1) the וידבר/ויאמר יהוה אל משה [ואל אהרן] לאמר ("Yahweh spoke/said to
Moses [and to Aaron], saying") messenger formula that opens nearly every legal and priestly unit
from ch.1 through ch.36, always checked against whether the prior unit had genuinely closed
before I let a fresh occurrence drive a boundary; (2) command/execution pairing, a device this
book uses constantly (a census commanded, then counted; a war commanded, then fought; a rod
sign commanded, then observed) that I treat as two beats when a real narrative or reporting gap
separates them and as one beat when the fulfillment is compressed into the same breath as the
command with no complicating detail between; (3) register and list formulas — the twelve-tribe
census tallies of chs.1 and 26, the four-camp standards of ch.2, the Levite-clan duty rosters of
chs.3-4, the twelve-prince dedication offerings of ch.7, the day-by-day festival calendar of
chs.28-29, and the station-by-station itinerary of ch.33 — each judged on its own internal
structure rather than mechanically split or merged, discussed at length below in
list_register_function_check; (4) scene, participant, and location changes in the extensive
narrative material (chs.11-14, 16-17, 20-25, 31-32), which carries roughly a third of this
book's verses and required ordinary narrative-seam judgment rather than legal-formula parsing;
and (5) the poetic insets this book scatters through its narrative — the priestly blessing
(6:24-26), the ark song (10:35-36), the well song (21:17-18), the Heshbon taunt song
(21:27-30), and the seven Balaam oracles across chs.23-24 — each treated as its own formally
marked unit distinct from its prose frame, using the explicit performance-introducing formulas
(אָז יָשִׁיר, עַל כֵּן יֹאמְרוּ הַמֹּשְׁלִים, וַיִּשָּׂא מְשָׁלוֹ וַיֹּאמַר) the text itself
supplies rather than the chapter_profile.json poetry markers alone (see
substrate_markers_considered). I did not treat Numbers's length or its mixture of genres as
license to default to chapter-sized chunks; per the CHAPTER-SHAPE RULE, whole-chapter chunks
would be fine here at honest confidence, but in practice every chapter in this book carries at
least one real internal seam, so none of my 260 decisions happens to span an entire chapter (see
chapter_only_fallback_reason_if_used). I settled at 260 decisions for 1,288 verses, a density
(4.95 verses/decision) close to the Leviticus book-writer's own 859-verse/180-decision rate
(4.77 v/decision), which I read as a reasonable, non-inflated outcome given how much of Numbers
genuinely is register-and-list material of the same granularity Leviticus's law code produced —
even though Numbers, unlike Leviticus, also contains large registers (ch.7, ch.33) I
deliberately chose NOT to atomize, which pulls the average back down toward something close to
Leviticus's own rate rather than well above it.

## literature_type_or_mixed_genre

Numbers is not one genre but an alternation of at least six distinct forms, and I treated each
chunk's local form on its own terms rather than forcing "law" or "narrative" as a blanket label.
Census and muster registers open and close the book (chs.1-4, 26), each with its own
person-counting or duty-assigning formula. Camp-and-march organizational material (chs.2, 10)
uses a standard-and-ordinal register distinct from a pure census tally. Priestly and purity law
(chs.5-6, 8-9, 15, 18-19, 28-30) is casuistic, protasis-driven material structurally close to
Leviticus's own legal register, but interleaved with narrative rather than block-collected. A
sustained rebellion-narrative cycle (chs.11-14, 16-17, 20, 25) supplies the book's dominant
scene-by-scene prose, complete with named participants, direct dialogue, and etiological place-
naming closures. A discrete embedded narrative-with-oracles cycle (chs.22-24) supplies this
book's most sustained poetic material, seven separate performed oracles inside one prose-framed
diplomatic-and-supernatural narrative. Two large self-contained registers — the twelve-prince
dedication-offering catalog of ch.7 and the forty-two-station itinerary of ch.33 — are genuinely
sui generis within this book, each built from one formula repeated with only the identifying
data changing, and each is the specific "hard test" case the campaign brief names explicitly
(discussed fully in list_register_function_check). Boundary and allotment law (chs.34-36) closes
the book in a register-and-instruction blend similar to the camp-organization material that
opened it. The literature_type_guess field in every decision names a specific, book-local form
(e.g. "twelve_tribe_census_tally_register," "booths_day_one_offering," "heshbon_taunt_song_
poetic_inset") rather than a generic category, and I did not let the book's overall narrative-
plus-law reputation flatten the real formal differences between, say, a casuistic vow-law case
and a station-by-station travel notice.

## literary_form_decision_matrix

- A fresh messenger formula (וידבר/ויאמר יהוה אל משה, sometimes "ואל אהרן") opening
  materially new legal or narrative content → candidate boundary, weighed against whether the
  prior unit had genuinely closed; I did not split every "Yahweh spoke to Moses" repetition
  inside a single continuous ritual (e.g. the Nazirite completion rite of 6:13-20) where the
  surrounding content plainly continued one procedure.
- Command paired with its own execution, when compressed into the same narrative breath with no
  complicating detail → one chunk (e.g. the lamp-lighting of 8:1-4, the Passover keeping of
  9:1-5); when separated by a real narrative gap, added complication, or a fresh formula of its
  own → two chunks (e.g. the census command of 1:1-16 versus its execution notice at 1:17-19).
- A list/register formula (a tribe-naming clause, a day-ordinal, a ויסעו/ויחנו travel pair) →
  a candidate internal boundary within a register, weighed against whether the register's own
  content genuinely varies at that point or is purely repeating a template with only names,
  numbers, or dates swapped — the specific test discussed in list_register_function_check.
- An explicit performance-introducing formula for embedded poetry (אָז יָשִׁיר יִשְׂרָאֵל,
  עַל כֵּן יֹאמְרוּ הַמֹּשְׁלִים, וַיִּשָּׂא מְשָׁלוֹ וַיֹּאמַר) → strong boundary separating
  the poem from its prose narrative frame, since this book itself marks these insets as
  formally distinct performed material rather than leaving them for a modern reader to infer
  from meter alone.
- A participant, addressee, or location change in narrative material, with the underlying
  scene's own cast, setting, or grievance genuinely changing, → new chunk; a naming-etiology
  closure (וַיִּקְרָא שֵׁם הַמָּקוֹם, "the name of that place was called...") or a
  seven-day-mourning/thirty-day-mourning notice → closes the scene it belongs to rather than
  opening the next one.
- A זֹאת/אֵלֶּה colophon (זֹאת תּוֹרַת הַקְּנָאֹת at 5:29, זֹאת עֲבֹדַת בְּנֵי קְהָת at
  4:4, אֵלֶּה הַחֻקִּים at 30:16, אֵלֶּה הַמִּצְוֺת וְהַמִּשְׁפָּטִים closing the whole book
  at 36:13) → strong boundary, generalizing a specific case or procedure into a standing rule
  or closing a whole legal complex, treated consistently whether it opens or closes a span.
- A dual WEB/MT citation requirement inside the five flagged crosswalk zones → does not by
  itself drive a boundary (per the crosswalk's own instruction that these are versification
  facts, not compositional evidence), but requires dual verse citation in every decision whose
  span touches those zones, and I defaulted sub-verse claims inside them to caution.

## substrate_markers_considered

I read chapter_profile.json's per-chapter marker counts alongside the WEB text's own ¶, [fn],
and |q1/|q2 poetic-lineation tags directly. Four chapters carry the has_poetry_or_liturgy_marker
flag: ch.6 (q1=2, q2=3 — the priestly blessing, 6:24-26), ch.21 (q1=8, q2=11, bk=2 — the well
song at 17-18 and the Heshbon taunt song at 27-30), ch.23 (q1=18, q2=18 — the first two Balaam
oracles), and ch.24 (q1=21, q2=31 — the third and fourth Balaam oracles plus the four short
closing oracles against Amalek, the Kenite, and Kittim/Asshur/Eber). In every one of these four
chapters I treated the poetic material as its own chunk (or chunks, where multiple oracles occur
in sequence) distinct from its prose narrative frame, using the text's own explicit performance-
introducing formula rather than the chapter_profile.json marker count alone to decide exactly
where the poem starts and ends — the marker corroborates that a chapter contains real verse, but
the formula (אָז יָשִׁיר, עַל כֵּן יֹאמְרוּ, וַיִּשָּׂא מְשָׁלוֹ) is what actually tells me
where. I also verified that 10:35-36 (the ark song) carries no chapter_profile.json poetry flag
at all despite being genuine, tightly patterned verse; I treated this as an instance of the
addendum's own rule that absence of a marker is never counter-evidence, and split it as a poetic
inset anyway on the strength of its own explicit "Moses said" framing and its bracketing
rise-up/return structure. Paragraph (¶) density is highest in ch.7 (p=114, the dedication-
offering register) and ch.22 (p=24, the Balaam narrative's own dense turn-taking dialogue), and
lowest in chs.26 and 33 (p=4 and p=2 respectively — both large, largely uninterrupted registers).
I let ch.7's high ¶ density inform my sense that the register has many surface-level typesetting
breaks (one for nearly every clause of the twelve-fold offering list) without treating that
density as evidence for splitting the register by prince or by day — see list_register_function_
check and over_split_risk_check below for why I read that density as WEB's own line-wrapping of a
single repeated template, not as marked literary structure. Footnote density spikes at ch.15
(f=14, unit-conversion glosses for the offering-scale supplement) and ch.28 (f=10, similar
measurement glosses); I treated every footnote strictly as metadata, never as boundary evidence,
consistent with strongs_metadata_considered_evidence_only below.

## strongs_metadata_considered_evidence_only

No Strong's numbers, lemma tags, or morphology codes are present in this cleaned WEB substrate,
so none were available to weigh as direct evidence anywhere in this chunk map. One footnote in
the WEB text (at 21:14) does carry an embedded Strong's-tagged USFM run inside its citation of
"the Book of the Wars of Yahweh" (\+w The|strong="H5921"\+w* ...); I read this purely as a
substrate artifact of how the WEB source marks up a proper-noun title, not as evidence bearing on
whether that citation is its own literary unit, and my decision at 21:10-16 keeps the citation
embedded in its surrounding itinerary notice on independent grounds (it functions as evidentiary
support within one ongoing travel notice, not as a separately staged performance the way the
well song at 21:17-18 is). Where WEB footnotes gloss a Hebrew measure or term (e.g. an ephah is
about 22 liters at 5:15, a homer is about 220 liters at 11:32, a cubit is about 18 inches at
11:31 and 35:4), I used that only as background color, never as the reason for a boundary. No
decision in draft_decisions.json rests on Strong's-tier evidence; every boundary_evidence_refs
entry cites either the WEB text itself or the OSHB Hebrew text directly, and the strategy
throughout treats Strong's-tier metadata exactly as tier 4 under the owner addendum: available
for color, never for boundary authority. This is a considered position, not an oversight — a
book this dense with technical measurement footnotes (offering quantities, tabernacle-object
weights, land-boundary distances) is exactly the kind where a chunker might be tempted to lean on
lexical apparatus for confidence, and I deliberately did not.

## source_metadata_evidence_only_check

I did not use documentary-hypothesis source labels (P, J, E, or any other siglum), nor any
theory about which strand or redactional layer produced the census material versus the
narrative material versus the itinerary catalog, as boundary authority anywhere in this chunk
map. Numbers is a textbook case where a source-critical reader might want to treat the "P"
census-and-law chapters (1-10, 15, 18-19, 26, 28-30, 33-36) as one compositional stratum
distinguished from the surrounding narrative chapters on stylistic-source grounds; I deliberately
did not do this — my chunk boundaries inside the census material (e.g. splitting each Levite
clan's duty entry in ch.3-4) rest on the same formula-and-content criteria I applied inside the
narrative material (e.g. splitting each stage of the Balaam donkey episode), not on any prior
sorting of which chapters "belong" to a hypothetical priestly source. Similarly, I did not treat
the book's own well-documented internal doublets (two full censuses in chs.1 and 26; two water-
from-rock episodes echoed at 20:1-13 and recalled again at 27:14; the Zelophehad's-daughters
case opened in ch.27 and resolved in ch.36) as evidence of, or against, a redactional seam
between sources. I read each doublet as the text's own deliberate narrative or administrative
structure — the second census exists to replace the generation the first census counted and then
condemned in ch.14, and the Zelophehad frame brackets the whole second half of the book — and
cited that literary function directly in the relevant decisions' rationale, never a source-
critical theory about how the doublet came to exist.

## larger_unit_preservation_check

I actively resisted splitting in several places. The whole twelve-tribe census tally of 1:20-46
stays one chunk despite covering twelve distinct tribes, because every entry shares one
identical lineage-family-age-tally template with no legal or procedural variation tribe to
tribe — the same reasoning that keeps the whole dedication-offering register of 7:12-83 as one
chunk (see list_register_function_check for the fuller argument, since this is the campaign's
named hard test). The whole first leg of the itinerary catalog (33:5-37) and its second leg
(33:41-49) each stay one chunk despite covering thirty-plus named stations, because every entry
is the identical וַיִּסְעוּ מִ...וַיַּחֲנוּ בְּ... formula with only a place name changing.
The Kohathite most-holy-things wrapping procedure (4:4-14) stays one chunk despite covering six
distinct sacred objects (ark, table, lampstand, golden altar, other vessels, bronze altar),
because every object is wrapped under one identical governing clause and closed with one
identical pole-insertion refrain. The whole deliberate-murder weapon list in 35:16-21 (iron,
stone, wood) stays one chunk rather than three, on the same "identical apodosis, only the means
changes" logic Leviticus applied to its own eight-case capital-crime list at 20:9-16. In each
case a less careful pass would have produced a finer split by tribe, station, object, or weapon;
I judged the additional split would have cut one coherent register in half at a point the text
itself marks with nothing more than a name change, not a real formal seam.

## list_register_function_check

I split a register only where its own function changed, not merely where a name, number, or
date changed. Two decisions anchor this test explicitly, because the campaign brief names both
as hard cases.

**Chapter 7's dedication-offering register (7:12-83).** Every one of the twelve princes' daily
offerings is the identical six-item template — silver platter (130 shekels), silver bowl (70
shekels), golden ladle of incense (10 shekels), three burnt-offering animals, one sin-offering
goat, and the same peace-offering tally — differing from entry to entry only in the day-ordinal,
the prince's name, and the tribe named. The day-ordinal itself is a real, textually marked
recurring formula, and a reviewer could reasonably read it as licensing a twelve-way split, one
decision per prince, the over-split reading. I rejected that reading and kept 7:12-83 as one
72-verse chunk, because not one of the twelve entries introduces a new item, quantity, or
procedural element — splitting at every day would manufacture eleven near-duplicate decisions
whose only content difference is a proper name, exactly the kind of arithmetic, convenience-
driven split the anti-over-split guidance warns against. I did, however, keep the narrative
frame (7:1-3), the wagon-distribution instruction (7:4-9), the "one prince per day" rule
(7:10-11), the grand-total colophon (7:84-88), and the closing theophany note (7:89) as five
separate surrounding decisions, since each of those five performs a genuinely distinct function
the pure offering-template does not share.

**Chapter 33's itinerary catalog (33:5-49).** The station-by-station register is even more
extreme in its uniformity than ch.7's — every entry is a two-verb clause, וַיִּסְעוּ מִ...
וַיַּחֲנוּ בְּ..., naming only a departure point and an arrival point. Per the instruction not
to atomize this list per station, I read the whole run as two large chunks (33:5-37 and
33:41-49), split only where the pure travel formula itself genuinely breaks — at 33:38-40, where
Aaron's dated death notice and the Arad-king flashback interrupt the register with real
narrative content carrying no travel verb at all. I judged that interruption a real formal seam
(a change of genre within the register, not just a change of place name) and everything else in
the two long runs a non-seam, the same "identical apodosis, only the identifying data changes"
principle applied to ch.7.

**The contrasting case: chapter 29's Booths offerings (29:12-38).** I split this eight-day
sequence into eight separate day-by-day decisions, the opposite granularity from ch.7, and I
want to be explicit about why the two registers are not treated the same way despite both being
day-ordered lists. Every one of ch.7's twelve entries is genuinely identical content; every one
of ch.29's eight Booths-day entries carries a different, decreasing bull count (thirteen, twelve,
eleven, ten, nine, eight, seven, then a reset to one on the eighth-day solemn assembly) — real
numerical content the register itself marks fresh each day. Splitting ch.29 by day reflects a
register genuinely doing new work each entry; keeping ch.7 as one chunk reflects a register doing
no new work at all beyond the name and day. I judged the second census's tribal register (ch.26)
similarly on a case-by-case basis against the first census (ch.1): I kept ch.1's twelve tribes as
one chunk because every entry is pattern-identical, but split ch.26's twelve tribes into eleven
separate entries because the genealogical depth genuinely differs tribe to tribe (Reuben's entry
carries the Dathan/Abiram/Korah retrospective; Manasseh's carries the Gilead genealogy and the
Zelophehad's-daughters notice; several others are bare two-verse entries with no sub-clan
elaboration at all) — a real content variance ch.1's register never has.

## epistle_unit_check_if_applicable

Not an epistle. Numbers contains no epistolary material of any kind; the epistle_unit_checklist
in the quality protocol does not apply to this book.

## over_split_risk_check

My working read of the four-camp arrangement in ch.2 and its execution in ch.10 produced seven
and ten decisions respectively across sixty-two verses combined, splitting each camp (and each
transitional hinge verse marking the Levites' or Kohathites' position in the march order) as its
own unit. I recognize a less granular reading could merge all four camps of ch.2 into two or
three chunks, or merge the hinge verses into their neighboring camp entries without a separate
decision; I settled on the finer reading because each camp's own orientation clause (east/south/
west/north) and its own distinguishing ordinal-position close (first/second/third/last) are real,
independently marked seams, not a convenient dividing point — the same device that separates
ch.7's twelve princes' offerings would, if applied there, be over-splitting, but here the
material genuinely differs camp to camp (different tribes, different totals, different march
positions), so the finer reading is earning its keep rather than manufacturing boundaries. Against
that, I deliberately consolidated several places where I judged a per-item split would cross into
over-fragmentation of genuinely repetitive material: the whole ch.7 dedication-offering register
(72 verses, one chunk, discussed above); both long legs of the ch.33 itinerary (42 verses across
two chunks rather than forty-two station-level chunks); the twelve-name census-witness roster of
1:5-15 and the twelve-name spy roster of 13:4-16 (each kept fused with its introducing and
closing clauses as one register rather than split by name); the Kohathite object-wrapping
procedure of 4:4-14 (six sacred objects, one chunk); and the deliberate-murder weapon list of
35:16-21 (three weapons, one chunk). I settled at 260 decisions for the whole book — above the
45-90 rule-of-thumb range, but at a verses-per-decision rate (4.95) close to the Leviticus book-
writer's own precedent (4.77) for a book 1.5 times longer, which I read as proportionate rather
than inflated, especially since two of Numbers's largest single spans (the 72-verse ch.7 register
and the 33-verse first itinerary leg) are single decisions that materially pull the book's average
chunk size up, not down. Where I was genuinely unsure whether a split was earning its keep, I
flagged it in notes_for_review rather than silently picking a side — most notably the 29:40/30:1
WEB-versus-MT chapter-boundary seam (M8-Num-211), and the ch.7 register's own explicit
over/under-split framing recorded as a standing flag on decision M8-Num-052.

## sidecar_specificity_plan

Sidecar rows (low_confidence_register, frontier_escalation_queue, atlas_candidate_feed) will each
name the concrete uncertainty driving the row, not a generic "low confidence" label — for example
"the WEB 29:40/MT 30:1-2 seam follows WEB's own chapter placement for the offering-calendar
closing fulfillment notice, but the Masoretic tradition opens ch.30 one clause earlier at the
identical verse, a genuine cross-tradition versification difference a reviewer may weigh
differently" for M8-Num-211, versus "the ch.7 dedication-offering register was deliberately kept
as one 72-verse chunk against a plausible twelve-way per-prince split; a reviewer applying
stricter per-day granularity would produce a substantially different sub-map for this one span"
for M8-Num-052, versus "ch.26's per-tribe census splitting treats several two-to-three-verse
entries (Simeon, Gad, Issachar, Zebulun, Ephraim, Benjamin, Dan, Asher) as full decisions on
formula grounds alone, since the register's recurring tribe-naming clause is the only marker
available for entries this short" for the low-confidence run at M8-Num-176 through M8-Num-185.
Numbers has no frontier-book status (frontier
status applies only to Dan and Rev per the quality protocol), so I expect the
frontier_escalation_queue to stay thin or empty despite the Balaam cycle's supernatural content
(a talking donkey, a divinely dispatched angel with a drawn sword) — this is narrative, not
apocalyptic-visionary material, and I did not treat it as frontier-adjacent. The atlas_candidate_
feed will draw primarily from the two-census structural pairing (ch.1's first-generation muster
against ch.26's second-generation muster, a natural before/after comparison table a downstream
atlas pass could build directly from this chunk map), the twelve-tribe camp-and-march system
(chs.2 and 10 describing the same four-standard arrangement in static and dynamic form), the
Zelophehad's-daughters frame bracketing chs.27 and 36, and the seven-oracle Balaam cycle as an
example of embedded performed poetry inside a prose diplomatic-and-supernatural narrative.

## chapter_only_fallback_reason_if_used

No chunk in this 260-decision map happens to span an entire chapter. This is not a coincidence I
need to explain away as a fallback; it follows directly from how densely this book marks its own
internal seams even in its most narratively simple chapters. Even ch.12 (16 verses, the Miriam/
Aaron rebellion, the book's shortest narrative chapter) splits into four scenes on real
participant and dialogue-turn changes; even ch.17 (13 verses, entirely inside a flagged MT-offset
zone) splits into four stages of the rod sign on its own instruction/execution/preservation/
response structure; even ch.36 (13 verses, the book's closing chapter) splits into four beats on
petition/ruling/compliance/colophon lines. Per the CHAPTER-SHAPE RULE, a chunk that happens to
equal one whole chapter would still be fine at honest confidence in this book, since Numbers is
not pilot-fragile and carries genuine poetry/liturgy substrate in only four chapters (6, 21, 23,
24, discussed in substrate_markers_considered) rather than throughout; it simply never arose here,
because even Numbers's plainest administrative or narrative chapters carry at least one internal
formula-, participant-, or scene-marked seam of their own.

## expected_low_confidence_regions

I expect reviewer disagreement to cluster around: (1) the ch.7-versus-ch.29 register-granularity
contrast discussed at length in list_register_function_check, where a reviewer could reasonably
prefer either a finer ch.7 split or a coarser ch.29 merge, or challenge the very distinction I
drew between "identical content" and "genuinely varying content" registers; (2) the ch.26 tribal-
census splitting, where several two-to-three-verse tribal entries (Simeon, Gad, Issachar,
Zebulun, Ephraim, Benjamin, Dan, Asher) rest on the register's own recurring formula as their
only real evidence, marked low confidence throughout that run; (3) the WEB/MT versification
seams in chs.16-17, 25-26, and 29-30, where the dual-citation discipline itself, and in one case
(29:40/30:1) the very choice of which tradition's chapter boundary to honor, is the likely
friction point rather than the underlying boundary placement; (4) the itinerary-notice treatment
in ch.21 (21:10-16, 21:19-20, 21:31-32), where short transitional travel notices around the well
song and the Sihon narrative rest on thinner formula evidence than the book's stronger register
and narrative-scene decisions, marked low confidence accordingly; and (5) several of the shorter
Levite genealogical entries in chs.3-4 (the Gershonite, Kohathite, and Merarite census-execution
reports at 4:38-41 and 4:42-45), which repeat a near-identical age-threshold clause with only the
resulting number changing and could arguably be merged the way I merged ch.1's census tally,
flagged low confidence as a genuinely closer call than the fuller duty-register entries that
precede them.

## frontier_or_atlas_candidate_expectations

Numbers is not a frontier book (frontier status applies only to Dan and Rev per the quality
protocol), so I expect zero frontier_escalation_queue rows driven by apocalyptic/visionary risk,
notwithstanding the Balaam cycle's supernatural donkey-and-angel content, which I read as
narrative marvel rather than apocalyptic vision. I do expect several atlas_candidate_feed rows:
the two-census structural pairing (chs.1 and 26) as a template for how this campaign might track
a book's own internal before/after administrative doublets; the four-standard camp system in its
static (ch.2) and dynamic march (ch.10) forms as a worked example of the same underlying
structure described twice for different purposes; the Zelophehad's-daughters frame spanning
chs.27 and 36 as a clean example of a narrative and legal thread deliberately left open across
many intervening chapters and then closed; the seven-oracle Balaam cycle (23:7-10, 18-24; 24:3-9,
15-19, 20, 21-22, 23-24) as the book's most sustained embedded-poetry sequence and a natural
comparison point against the priestly blessing (6:24-26) and the two shorter travel songs
(10:35-36; 21:17-18); and the deliberately non-atomized ch.7 and ch.33 registers as worked
examples, for any downstream methodology pass, of how a chunker should read a repeated-template
list honestly rather than mechanically split it at every date, name, or station.
