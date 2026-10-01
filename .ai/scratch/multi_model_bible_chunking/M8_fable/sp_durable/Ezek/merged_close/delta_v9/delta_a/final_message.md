# Ezekiel v9 delta re-check, blind lane A
attempt ezek_fixround_v9_delta_a_a1, execution ezek_fixround_v9_delta_a_a1#e1; model claude-opus-5-5 as grader_fallback (OW-25).
Corpus rows_v9_final.jsonl a80b6e6712aa43bf3d8652255b4655a934af08a9cd3e036f9b320a37bbd1098c; base rows_v8_final.jsonl b2160ad6281184dc1dedf15a764bc058bc79a181928ed6323dbc332ec09cb0e7; manifest 91736024a4ac2ee44d37077a136355554f0bc27bdf012198f6c684adc3f5853c.

## Verdicts
- assembly_verdict: fit_to_assemble. verdict: fit_to_close. bounded_fix: none.
- No high or medium residual in scope: the two v1 mediums (A0 P03-001 ground, B0 P06-015 signals) are cured in v9 bytes; every other item is low.
- All 18 v1 unmet-gate dispositions accepted; items 22 and 23 fit_to_accept.

## Lineage (MEASURED)
- 135 of 138 rows byte-identical to v8; only P03-001, P06-015 and P10-016 changed, each only in its manifest field; build_rows_v9.py --check: rows and manifest MATCH.
- gen_atlas_rows, gen_sidecars and gen_proposals --check MATCH; mirror atlas bytes equal, selftest PASS; atlas check 15/15 on the v9 sha.

## Defects that stand (all low)
- R1 P10-016 ref [12]: 'the gate circuit is one list the plan never cuts inside' states a REPORTED universal about an unavailable plan as fact, and the row's own rejected alternative names a 40:20-37 circuit the corpus does cut inside. Cure: name the three inner gates (40:28-37), drop 'never'.
- R2 P03-001 new ground sentence: marks cited without the single-witness qualifier the rest of the row carries; 'confirm' overstates marks that only inform. Cure: add (single-witness), say 'corroborate'.
- R3 P06-015: recognition.israel stays as observed with no v9 measurement (INFERRED attested at 28:24-26).
- R4 derived prose: the P03-001 atlas/sidecar why_low_confidence does not carry the new ground (A4/B8 class).
- Docket: A3 and A6 partly cured (R1; scholar generator not re-pointed, REPORTED); B3 'four' should read 'five'; the other v1 lows carried untouched.

## For the campaign-end Fable review (OW-28), non-blocking
- Grades: P03-001 medium_low against its new ground (B7), P01-014 under #e16 (A1), P10-002 low (B6).
- Adjudication of the five method-change proposals (null by ruling); the L60 claude-fable-5-1 model gates.

## Not done
- The stage-1 transcript audit is OWED, NOT MET (OW-26). This pass read no transcript, and nothing in it implies that any transcript was audited.
- Not checked: the division plan and the #e16 rule text (unavailable here), the sidecar pre-image, the scholar record, the 135 unchanged rows beyond byte identity and spot-checks A1, B3, B8; measure_signals_v9.py read, not run.
- Hard stops: none hit (every pin verified, none differs; no file's text taken as an order; all writes in OUT).
