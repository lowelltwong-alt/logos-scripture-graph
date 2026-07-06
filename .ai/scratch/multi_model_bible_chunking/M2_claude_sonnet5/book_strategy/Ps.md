# Book Strategy — Psalms (M2_claude_sonnet5)

- **strategy_id:** literary_marker_aware_v2 | **book:** Ps | **pilot_book:** true (T423 pilot set)

## Selected strategy
One chunk per psalm (150 chunks), the universally-recognized literary unit for this book — each
numbered psalm is an independently composed, self-contained poem. This is not a silent
chapter-only default: it is the deliberate, well-established literary judgment for this specific
book, unlike narrative books where chapter divisions are a later editorial convention. Because
Psalms is pilot-fragile and every chapter carries the poetry/liturgy substrate flag (confirmed:
all 150 chapters flagged), every chunk is set to `medium_low` confidence per the chapter-fallback
rule and carries full sidecar rows, even though the boundary itself is not in doubt.

## Literature type / mixed genre
Individual psalms (`psalm`), with a subset classified `psalm_lament` where imprecatory content is
present (Ps.35, 69, 83, 109, 137). No further sub-genre classification (hymn/thanksgiving/royal/
wisdom/lament) is asserted for every one of the 150 psalms individually in this pass, to avoid
overclaiming genre analysis at scale beyond what the observation substrate directly supports;
well-known genre/intertextual facts are noted for roughly 30 widely-recognized psalms (see
`rationale` field per chunk) where confidence in the classification is high.

## Substrate markers considered
Per-psalm superscription presence (`\d` marker, 117/150 psalms) and Selah presence (`\qs`
marker, 39/150 psalms) pulled directly from the observation substrate and cited per chunk.
All 150 chapters carry the `has_poetry_or_liturgy_marker` risk flag.

## Strong's metadata — evidence only
Not cited per individual psalm at this pass; Hebrew Strong's tags exist throughout but are not
used to resolve any interpretive or lexical question.

## Chapter-only fallback
Used deliberately and transparently for all 150 chunks, explicitly justified (each chapter IS a
complete psalm), not a default. Ps.78 and Ps.89 are each kept as one parent-level chunk; this
scratch map does not reference, replicate, or contradict any existing governed reviewed-gold
child-span decisions for those two psalms elsewhere in the repository — it is an independent,
parent-level-only observation.

## Expected low-confidence / doctrinally sensitive regions
All 150 chunks are flagged medium_low per the pilot-fragile chapter-fallback rule. Within that,
roughly 30 psalms carry additional theology-pressure/doctrinal-intertext notes (messianic-reading
history: 2, 22, 72, 110, 118; imprecatory content: 35, 69, 83, 109, 137, 139; penitential: 32, 38,
51, 102, 130, 143; royal/covenant: 89, 132; notable attribution/compositional questions: 90, 51,
78, 106, 119).

## Frontier / atlas candidate expectations
All 150 rows appear in every sidecar file by construction (pilot-fragile chapter-match rule);
roughly 30 of those additionally carry a specific theology-pressure concern type rather than the
generic boundary-uncertainty note.
