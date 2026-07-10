# T473 Semantic Harness And Source-Marker Anchor Integrity Gate

## Purpose

T473 was opened to define a four-scope semantic proposer/critic pilot after T472 corrected the multi-model comparison. Preflight inspection found a more fundamental source-integrity defect, so T473 defines the future harness but blocks all model execution.

## P0 Finding

The importer associates a structural marker with state.current. When a marker appears between verses and declares the start of the next unit, state.current is still the verse just completed. The resulting BoundaryClaim and SectionHeading point backward. If the marker carries body text, that text is also appended to the prior canonical translation witness and parsed for inline sidecars.

This is previous-versus-next ownership, not inclusive-versus-half-open range arithmetic.

Confirmed consequences:

- Psalm 119 BETH precedes verse 9 in raw USFM but appears in the Ps.119.8 witness.
- Psalm 119 heading words HE/H3588 and AND/H4941 became canonical WordTokens.
- Beloved and other sp speaker labels entered 27 Song of Songs witnesses.
- A read-only characterization found 15,303 next-bound claims; 13,977 currently point backward and 1,326 are null.
- Psalm 119 reviewed gold and the candidate guardrail encode shifted stanzas.
- Psalm 78's terminal b evidence needs owner re-review.

Passage identities/counts, footnotes, and cross-references were not shown wrong by this audit.

## Binding Contract

T474 must represent marker ownership explicitly:

- current_content
- next_content_start
- between_units
- chapter_context
- book_context
- unresolved

Start-bound markers must be queued until the next verse is known. Relational markers such as b must preserve both sides. Body-bearing poetry/list continuations can remain attached to current content. Unresolved ownership fails closed.

Heading and speaker-label body text must never become canonical Bible witness text or canonical Scripture WordTokens.

## Revised T473-T480 Route

1. **T473:** Contract, characterization, owner options, and failing integrity gate only.
2. **T474:** Importer repair and focused fixture matrix; no canonical regeneration.
3. **T475:** Ignored shadow regeneration with exact witness/token/sidecar/chunk deltas and hashes.
4. **T476:** Exact owner packet for canonical WEB repair.
5. **T477:** Owner-approved canonical regeneration and baseline reset.
6. **T478:** Psalm 119 and Psalm 78 reviewed-gold re-review; no gold edits.
7. **T479:** Owner-approved gold and guardrail corrections; no chunk output.
8. **T480:** Chunker/form-consumer repair with route-isolated candidate proof; no promoted output.

The four-scope semantic proposer/critic pilot moves to T481+.

## Four Future Calibration Scopes

- 2Kgs.18.1-2Kgs.19.37
- 1Chr.23.1-1Chr.27.34
- 2John.1.1-2John.1.13, research-only and overlap-blocked
- Ps.119.1-Ps.119.176, blocked until source and gold integrity are repaired

The typed schema distinguishes calibration scope, literary parent, internal structure, exact model span, disagreement region, candidate span, and reviewed-gold/output overlap. A region, union, envelope, vote, pair, or confidence rollup can never become a candidate span.

## Non-Authorizations

T473 does not change canonical data, reviewed gold, chunk output, child spans, route/evaluator behavior, graph/retrieval/vector truth, source tradition, canon scope, or theology authority. It executes no model pilot.
