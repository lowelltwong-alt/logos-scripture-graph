# T521 Literary-Scaffold Audit Handoff

- Task id: `T521_literary_scaffold_audit`
- Agent: Codex literary-scaffold-audit subagent
- Mode: read-only, adversarial literary/structural audit
- Files read:
  - `AI_FRONT_DOOR.md`
  - `.ai/control/MASTER_CONTEXT.md`
  - `.ai/control/PROJECT_STATUS.md`
  - `docs/governance/WHOLE_BIBLE_B01_REPLAY_RUNBOOK.md`
  - `docs/governance/M7_SOL_WISDOM_PROPHETS_LITERARY_WAVE_REVIEW.v1.json`
  - `.ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl`
- Files changed: this non-authorizing handoff only.
- Decisions made: none. No boundary proposal, source selection, theological decision, promotion, or claim of independent corroboration is made.

## Scope and method

This audit examined the whole-map JSONL as a record-indexed candidate artifact. A low-confidence record, an explicit “chapter frame retained”/“candidate chapter-span retained” rationale, or an unusually broad mixed-form record was treated as a review trigger—not as evidence that the existing outer span is wrong. The B01 runbook requires form/discourse/original-language/canonical evidence before any later internal seam could be considered; it explicitly forbids B01 from selecting B02 boundaries.

Same-model limitation: all inspected M7_sol material and its role packets are a correlated Codex substrate. The queue below is not independent validation and must be supplied to a separate provider or qualified human reviewer blind to sibling maps. Scripture text is deliberately not reproduced.

## Prioritized top-20 risk queue

| Priority | Candidate record(s) / evidence of scaffold weakness | Literary seam / genre questions for a future reviewer | Language and canonical-relation risks; red-team test |
|---|---|---|---|
| 1 | `Job.4.1–Job.27.23`, `M7_sol-Job-004..027`, JSONL lines 475–498. Each chapter is separately called `dialogue_speech_poetry` and acknowledges speech turns may cross chapters. | Map each speaker handoff and each speech closure before retaining any chapter edge; test whether the third dialogue cycle has asymmetric or interrupted turns. | Hebrew poetic syntax, ellipsis, and quotation-like address can mask speaker changes. Test that no proposed seam strands a response or falsely turns a translation paragraph into a speaker change. |
| 2 | `Song.1.1–Song.8.14`, `M7_sol-Song-001..008`, lines 707–714. All are chapter-wide `lyric_dialogue_and_chorus`; the wave review itself says speaker attribution, chorus/refrain, and scene shifts are unresolved. | Establish only evidence-backed speaker/refrain/scene candidates; especially test whether recurring adjuration/refrain material joins or separates neighboring lyric units. | Compact Hebrew lyric grammar and uncertain speaker labels make English layout unreliable. Test competing speaker maps without importing a later interpretive drama. |
| 3 | `Isa.40.1–Isa.55.13`, records 754–769 (e.g. 754, 756, 763, 766–769), all chapter-sized `consolation_servant_poetry`. | Audit heading, messenger/speaker, servant-song, disputation, and hymn-like transitions which may begin/end within or cross chapters. | Hebrew participant/reference ambiguity and shifts in direct address are high-risk; structural parallels must not decide identity or theology. Red-team test: remove English headings and see whether the proposed seam evidence survives. |
| 4 | `Jer.26.1–Jer.29.32`, `M7_sol-Jer-026..029`, lines 806–809; four chapter spans under `conflict_and_narrative_cycle`, despite the wave review flagging heading/chronology holds. | Separate narrated setting, sign/action, competing speech, letter/document, and collection heading only where textual markers warrant it. | Hebrew/Greek textual and ordering/versification issues, plus cross-book parallels, can tempt harmonization. Test that chronological reconstruction is not used as a seam rule. |
| 5 | `Rev.4.1–Rev.22.21`, records 1152–1170, mostly one chapter each with generic cycle rationales. | Test vision-introduction formulas, audition/vision shifts, interludes, hymnic material, cycle recapitulation, and epistolary closure independently of modern chapters. | Koine aspect, symbolic allusions, and OT echo density make section labels precarious. Test whether every candidate edge has a local discourse/form marker rather than a presumed linear chronology or system. |
| 6 | `Num.16.1–Num.18.32`, `M7_sol-Num-009`, line 230, one broad record containing rebellion, judgment, memorial, plague/atonement, rod test, and priestly duties. | Require scene/function inventory before retaining the macro span: conflict, adjudication, memorial, test, then statute. | Hebrew labels and versification crosswalks are explicitly required by the record; canonical echoes must not collapse distinct functions. Test coverage after any future split and prevent a legal corpus from being absorbed into narrative causation. |
| 7 | `Ezek.40.1–Ezek.48.35`, `M7_sol-Ezek-040..048`, lines 877–885, chapter-sized visionary/architectural records. | Test vision frame, guide speech, measurement sequence, instruction blocks, allocation material, and closing formula as separate literary movements only when marked. | Technical Hebrew, measurement vocabulary, textual witnesses, and translation normalization create high segmentation risk. Test that diagrammatic/architectural conventions are not mistaken for boundaries. |
| 8 | `Heb.3.1–Heb.10.39`, `M7_sol-Heb-003..010`, lines 1117–1124, each “scriptural exposition with exhortation” at chapter size. | Map quotation citation, exposition, warning/exhortation, and resumption markers; review transitions around the chapter 3–4 and 4–5 joins without assuming either side is an independent argument. | Koine participial chains and embedded citations can cross modern divisions. Test that quoted-source boundaries and authorial discourse boundaries are not conflated. |
| 9 | `Deut.1.1–Deut.4.49`, `M7_sol-Deut-001..004`, lines 240–243, each explicitly says “Chapter frame retained as a conservative candidate.” | Examine retrospective speech, narration, legal/covenant transition, and repeated address formulas across chapter seams. | Hebrew discourse particles and deictic shifts may differ from English paragraphing. Test that a chapter boundary is never the only evidence and that later canonical recollection is not used as a boundary authority. |
| 10 | `Deut.27.1–Deut.30.20`, `M7_sol-Deut-027..030`, lines 266–269, still chapter-scaffolded amid ceremony, blessing/curse, covenant renewal, and choice discourse. | Identify speaker/ceremony/inscription/recitation and blessing/curse refrain transitions before treating any modern division as structural. | Formulaic repetition may be either internal architecture or a boundary. Test alternative groupings with no theological ranking and preserve versification-sensitive references. |
| 11 | `Prov.22.1–Prov.24.34`, `M7_sol-Prov-022..024`, lines 685–687. Chapter spans obscure the known collection-heading and “sayings” scope questions recorded in the literary-wave review. | Independently locate collection headings, instruction blocks, numerical/rhetorical units, and aphorism clusters; do not force an entire chapter into one collection because of its label. | Hebrew parallelism and heading syntax are decisive but English punctuation is not. Test if heading scope crosses a chapter boundary and retain alternate scopes in an appeal ledger. |
| 12 | `Ps.42.1–Ps.43.5`, records `M7_sol-Ps-042..043`, lines 555–556, two psalm records despite a potential refrain/inclusio relation; collection seams 72/89/106/150 are separately flagged at lines 585/602/619/663. | Test refrain, superscription, acrostic/parallelism, doxology, and collection-closure signals; compare each claim with psalm-level integrity rather than presuming a merge or split. | Hebrew superscriptions and refrain wording need source-level verification. Red-team test: prohibit a reviewer from using later liturgical grouping as seam evidence. |
| 13 | `Eccl.11.1–Eccl.12.14`, `M7_sol-Eccl-011..012`, lines 705–706. Chapter separation can obscure closing poem, frame/voice, and epilogue transitions flagged by the wave review. | Mark voice/frame shifts, poem onset/closure, and editorial-style epilogue only where explicit textual evidence supports them. | Hebrew lexical repetition and mood/voice ambiguity affect segmentation. Test a boundary hypothesis against both the recurring refrain and the book-level frame without resolving authorship. |
| 14 | `Isa.1.1–Isa.12.6`, `M7_sol-Isa-001..012`, lines 715–726, an oracle cycle represented as chapter units despite song/woe/vision diversity. | Review superscription, vision report, woe sequence, poetry/song, and oracle formula transitions across chapters. | Dense Hebrew poetry and shifts between address/addressee are unstable in English. Test that a thematic label does not replace a local form marker. |
| 15 | `Jer.30.1–Jer.33.26`, `M7_sol-Jer-030..033`, lines 810–813, chapter units under one consolation cycle. | Check document/frame markers, prose/poetry alternation, sign/transaction narrative, and oracle transitions; distinguish adjacent but different forms. | Textual-order and chronology questions are particularly tempting here. Test that no reconstruction from external chronology or later reception determines the seam. |
| 16 | `Dan.2.1–Dan.7.28`, records 887–892, all chapter containers spanning court narrative and vision material; the Aramaic transition/vision cycle is a special preflight risk. | Review language-switch boundaries, court tale framing, reported speech, dream/vision interpretation, and poem/hymn insertions as candidate signals. | Hebrew/Aramaic shifts and textual traditions require explicit source qualification. Test that language change is not automatically a boundary and that vision sequencing is not made linear by assumption. |
| 17 | `Zech.9.1–Zech.14.21`, records 955–960, chapter-wide late prophetic/oracle records. | Test heading formulae, burden/oracle introductions, speaker shifts, embedded lament/vision, and eschatological scene transitions. | Hebrew ambiguity and dense intertextual resonance create allusion-driven overchunking risk. Test seams without importing later canonical fulfillment frameworks. |
| 18 | `Acts.19.1–Acts.20.38`, `M7_sol-Acts-009`, line 1023, broad `mission+riot+farewell_speech` record spanning chapters. | Inventory location changes, crowd/official/author speech, narration, travel notices, and farewell discourse; test whether any candidate children retain their complete narrative frame. | Koine discourse markers and embedded speech introduce quotation scope risk; related Pauline material must not be harmonized into Acts. Test an edge with all cross-book comparison withheld. |
| 19 | `Rom.9.1–Rom.11.36`, `M7_sol-Rom-009..011`, lines 1036–1038, chapter units labeled scriptural reasoning/paraenesis despite a sustained argumentative block. | Map objection/response, citation-catena, discourse resumption, doxology, and addressee shifts before accepting chapter breaks. | Greek rhetorical questions, quotations, and diatribe voices are vulnerable to misattribution. Test that embedded citations are not misread as authorial section endings. |
| 20 | `Lev.13.1–Lev.15.33`, records `M7_sol-Lev-027..031`, lines 176–180, contains very large diagnostic/ritual manuals; line 176 alone compresses many bodily conditions. | Review divine-speech openings, condition-class changes, diagnosis/quarantine/cleansing sequence, and summary colophons as functional candidates. | Technical Hebrew and ancient ritual terminology make translation categories an unsafe seam proxy. Test whether every future split preserves conditional logic, prescribed action, result, and closure. |

## Replay recommendations

1. Treat the queue as an external-review worklist, not an edit list. Give the independent reviewer only the record IDs, spans, source-manifest hashes, and the B01 role contract; withhold sibling maps and previous suggested boundaries until its report is frozen.
2. Require each review response to name one local literary/discourse signal, one falsification condition, original-language/source adequacy, and any internal relation that could distort the decision. “Chapter” or an English heading alone fails the review.
3. Route these by specialty in bounded waves: Hebrew/Aramaic poetry and technical law; Koine epistle/apocalypse; then a separate literary/canonical red team. Preserve dissent/appeals as typed ledger rows even after a boss receipt-only ruling.
4. Re-run exact coverage, no-overlap, packet-binding, and correlated-substrate honesty validation after any candidate-map revision; require a new immutable attempt whenever a map byte or governed input changes.
5. Do not treat external agreement as authorization. A later B02 migration needs its own contract, evidence, boss conditions, independent reviewer receipt, and human gate.

## Validation performed

- Read-only JSONL record inspection for all 1,170 map rows and targeted line/record references.
- Cross-checked risks against the replay runbook’s hard-passage rules and the wisdom/prophets wave review’s explicit holds.
- No map/source/packet content was written or changed.

## Risks introduced

None to Scripture data or candidate map. The report itself is a same-model, non-authorizing triage artifact and may be incomplete; it must not be used to assert original-language claims without the cited pinned-source review.

## Unresolved questions

- Does a qualified external provider/human receipt exist for each high-priority scope, independent of the correlated M7_sol mesh?
- Are exact book-level Hebrew/Aramaic and per-book Greek source views available and qualified for the designated reviewers?
- Which review wave has human approval to create a new candidate revision after evidence is frozen?

## Exact next action

Provide the top-20 queue to an external blind literary/original-language reviewer, require typed non-authorizing findings and appeals, then compare them to the frozen M7_sol map without promoting any candidate boundary.
