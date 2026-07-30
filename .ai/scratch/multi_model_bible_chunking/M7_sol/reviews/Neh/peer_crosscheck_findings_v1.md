# Nehemiah peer crosscheck findings

Candidate-only, non-authorizing review of the independent M7_sol Nehemiah route.

## Initial finding and repair

The initial 24-unit candidate preserved Hebrew chosen spans and rejected alternatives, but 20
decisions carried the Hebrew primary's non-empty `low_hold` only in the language hold. The peer
required verbatim preservation in all four review surfaces. The generator now includes each
Hebrew decision ID, exact span, and `low_hold` in `rejected_alternative`,
`candidate_internal_seams`, `original_language_translation_holds`, and
`red_team_premortem_holds`.

## Re-audit

PASS at SHA-256
`d8686deef49f0d82fdff6c2ca819717530d8fb63b05e6d07c72a4b71708c1253`.

- 24 positive contiguous integer-indexed larger units.
- Exact ordered WEB coverage: 406/406.
- Zero omitted canonical, Hebrew, or literary exact alternatives or Hebrew low holds.
- WEB 4:1-6 = MT 3:33-38, WEB 4:7-23 = MT 4:1-17, and WEB 9:38 = MT 10:1 are preserved.
- Qere/ketiv, identity, chronology, covenant, marriage, Sabbath, legal/cultic, and theological
  questions remain evidence-only/non-authorizing.
- No fallback logic remains.
- Confidence remains 22 LOW/deferred and 2 MEDIUM accepted.

The peer pass does not remove appeals or authorize promotion.
