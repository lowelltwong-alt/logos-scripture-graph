# Ezra peer crosscheck findings

Candidate-only, non-authorizing review of the independent M7_sol Ezra route.

## Result

PASS at candidate SHA-256
`c0f45529e723e5d755298c24ae7c04db4b6d1d30e46bec9f74273c9a0c9a6c57`.

- 16 positive contiguous integer-indexed larger coherent units.
- Exact ordered coverage: 280/280.
- All canonical `exact_alternative` values preserved verbatim.
- Every overlapping Hebrew/Aramaic chosen span and rejected alternative preserved.
- Every overlapping literary chosen span and exact internal alternative preserved.
- Hebrew through 4:7, Imperial Aramaic 4:8–6:18, Hebrew 6:19–7:11, Imperial Aramaic
  7:12–26, and Hebrew thereafter are routed correctly and remain evidence only.
- All 29 qere/ketiv evidence points are attached to their containing decisions without selecting
  a reading.
- Whole-chapter units have specific document, response, register, prayer, journey, or assembly
  functions; no fallback logic remains.
- Confidence is conservatively calibrated at 15 LOW/deferred and one MEDIUM accepted decision.

The initial pass found one editorial typo in synthesized D010. The immutable blind proposal remains
unchanged; the generator normalizes `aramic` to `aramaic` only in the synthesis. A targeted recheck
proved the candidate diff was limited to four synthesized spelling occurrences and changed no
span, confidence, hold, evidence, or coverage content.

This peer pass does not remove appeals or authorize promotion.
