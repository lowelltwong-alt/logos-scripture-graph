# Sol T475 Acceptance Report

## Verdict

HOLD_WITH_FINDINGS

The shadow evidence is deterministic, exact, no-text, and reusable. T476 and
T477 remain blocked.

## Findings

### P1: Editorial Footnote Sidecars Are Lost

Three real footnote records embedded in Psalm descriptive heading lines are
removed. Their raw marker evidence remains present in section-heading and USFM
event records, so Scripture text is not lost and no committed data was mutated.
However, the repaired importer sends editorial-only heading bodies around the
inline sidecar extractor. Typed footnote consumers therefore lose metadata that
the T474 preservation intent required to remain recoverable.

The correct separation is:

- heading prose never enters TranslationWitness text;
- heading words never create canonical WordTokens;
- embedded footnotes remain typed editorial/source sidecars;
- the heading's forward content anchor remains distinct from footnote scope.

This is blocking for regeneration but not a P0 because raw evidence remains
recoverable and T475 wrote only ignored shadows.

### P2: Fixture Coverage Missed Editorial Inline Sidecars

T474 fixtures checked headings, witness text, and tokens, but did not assert
that an embedded footnote in an editorial heading survives as a typed sidecar.

## Confirmed Intended Effects

- All 31,103 passage identities are unchanged.
- All 340 editorial cross-references are unchanged.
- Exactly 48 witness text hashes change: 21 Psalm 119 prior-heading
  contaminations and 27 Song prior-speaker contaminations.
- Exactly two known bogus Psalm 119 heading-derived tokens are removed.
- Explicit anchor metadata changes every event, boundary claim, and section
  heading as designed.
- The 2,727 unresolved rows occur only in excluded/noncanonical files and do not
  mutate canonical witness or token output.
- No chunker ran and no chunk output exists.

## Agent Disagreement

Terra considered the three unscoped footnotes expected removal. Sol rejects that
interpretation because canonical storage location does not turn an editorial
sidecar into Scripture text, and editorial-only disposition is not permission
to discard typed provenance. The disagreement and resolution are retained
explicitly.

## Balanced-Value Gate

Outcome: hold_and_defer_rust.

The candidate importer median is modestly faster than baseline, but this is not
a Rust comparison and the implementations have different semantics. The
bounded Python comparator also exposed and isolated the regression. There is no
evidence-based reason to build new Rust for this repair.

## Required Next Route

1. Obtain owner authorization for a separate narrow editorial-inline-sidecar
   preservation repair task.
2. Emit embedded heading footnotes without appending heading prose or creating
   heading-derived WordTokens.
3. Add a descriptive-heading fixture proving footnote preservation, clean
   witness text, and zero heading-derived tokens.
4. Rerun T475 as a new frozen evidence revision.
5. Require zero footnote removals, the same 48 intended witness changes, and the
   same two bogus-token removals.
6. Run the independent Claude audit on the revised frozen bundle.
7. Begin T476 only after that audit passes.

## Non-Authorizations

No committed data, reviewed gold, chunks, child spans, route/evaluator behavior,
graph/retrieval/vector truth, source-tradition preference, canon decision, or
theology authority is authorized.
