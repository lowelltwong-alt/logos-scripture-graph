# T467 Harness Hardening Notes

Source: T465 harness triage.

Decision: strengthen the T423 scratch harness with `T467_literary_coherence_v1` for future reruns, not retroactively mutate completed M1-M6 artifacts. The core aim is preserving larger coherent literary units when the text functions as a single unit.

Implemented requirements:

- Larger-unit preservation check for lists/registers/legal/allotment/census/worship/admin/battle/covenant units.
- epistle-unit checklist for greeting, thanksgiving/prayer, body argument, exhortation, household/church order, travel/mission notes, final greetings, doxology, and benediction.
- Source metadata guard: Strong's, lemma, morphology, WJ/red-letter, headings, notes, and cross-references are evidence only.
- Sidecar specificity rule: low-confidence/frontier/atlas rows must name concrete uncertainty.
- Validator coverage for the T467 overlay and T423 prompt/protocol/template wiring.

DAD reporting: deferred_due_to_interface_drift. T467 does not write `.digital-asset/` because the owner said DAD reporting is not working well and should not block the roadmap.

Non-authorizations: no model rerun, full comparison rerun, reviewed gold, chunk output, child spans, route/evaluator behavior, graph/retrieval/vector truth, source-tradition preference, canon change, or theology authority.
