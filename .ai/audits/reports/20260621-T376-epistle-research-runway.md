# T376 No-Context Audit Surface

## Scope

T376 is a non-output-changing owner lane-selection and research-runway task. It records `T376-A`:
continue epistle argument review/prep only, and let future agents research all serious faithful
target options before returning to the owner for binding decisions.

## Primary Artifacts

- `.ai/control/t376_epistle_research_runway.yaml`
- `docs/roadmap/T376_EPISTLE_RESEARCH_RUNWAY.md`
- `scripts/validate_t376_epistle_research_runway.py`
- `tests/test_t376_epistle_research_runway.py`
- `.ai/tasks/T376.task.yaml`
- `.ai/handoffs/T376/handoff.md`

## What Changed

- Recorded owner selection of `T376-A`.
- Added the research/autonomy boundary: research/options may continue, authority-changing actions
  must stop for owner decision.
- Added six serious epistle argument target options for T384 research.
- Added `CD-060` to the chunking theological decision register.
- Added `LSN-012` to the lesson index: Research autonomy is not authority autonomy.
- Updated preflight, readiness map, roadmap state, TOCs, audit report index, and validators/tests.

## Non-Authorizations

T376 does not authorize:

- exact target selection
- reviewed-gold promotion
- child spans
- chunk output changes
- route behavior changes
- evaluator changes
- graph edge generation
- retrieval truth
- vector or embedding work
- boundary import
- whole-Bible output
- preferred readings or source-tradition preference
- canon-scope change
- denominational systematic theology as chunk authority

## Next Gate

T384 may proceed as non-output-changing epistle argument research/options work. It must stop before
any target selection, promotion, implementation, output, graph/retrieval/vector, boundary-import, or
theological-authority decision.
