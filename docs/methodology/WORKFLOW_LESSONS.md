# Workflow Lessons

Status: living control-plane lesson collector
Owner: methodology / roadmap governance
Last updated: 2026-06-21

This file collects reusable workflow lessons that apply across generated artifacts, control-plane
surfaces, boundary-source intake, and adjacent operational systems. It is not canonical Scripture
truth, not boundary corpus approval, and not authorization for output-changing work.

Expanded rule registry: see
[`LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md`](LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md) for rule
IDs, importance levels, enforcement notes, T327 root-cause lessons, and LawFirm transfer patterns.
This file remains the compact workflow lesson collector.

## How To Use This Collector

- Cite the relevant lesson in task handoffs when a task follows or updates one of these patterns.
- Update this file when a completed task exposes a reusable workflow rule that should survive the
  immediate PR.
- Keep implementation authority in the appropriate task, repo, and reviewed evidence surface.
- Do not use a lesson as a substitute for source review, owner authorization, tests, validation, or
  explicit downstream handoff.

## WORKFLOW-LESSON-001 - Generated Artifact Corrections Require Durable Generator + Gate

When a correction affects generated artifacts, ignored build outputs, derived evidence, chunks,
scores, sidecars, or workflow outputs, the correction is not durable merely because a local run
produced the right result.

The durable correction must live in committed generator behavior, committed policy/config,
fail-closed validation, CI regeneration, and task-scoped tests. If a downstream test fails because
the correction changes the corpus or baseline, that failure must be explicitly staged into the next
task with temporary quarantine or documented owner decision. Do not silently re-baseline in the wrong
task.

Applies to:

- Scripture canonical output regeneration.
- Chunk regeneration.
- Scorecard / leaderboard baseline resets.
- Boundary source intake.
- LawFirm exception-to-automation workflows.
- Agent harness outputs.
- Any system where generated artifacts are not committed as source truth.

## WORKFLOW-LESSON-002 - High-Leverage Changes Need an Unintended-Consequence Map

For roadmap, authority, routing, evaluator, chunker, generated-artifact, default-retrieval,
master-chunker, or automation changes, success is not only "does the intended change work?" The
agent must also ask what the change might accidentally authorize, weaken, contaminate, overfit,
globalize, or make harder to reverse.

Required question: What could this change accidentally authorize, weaken, contaminate, overfit, globalize, or make harder to reverse?

The answer must be recorded as an unintended-consequence map with:

- confirmed risks;
- plausible risks;
- unlikely but high-impact risks;
- watch-later conditions;
- tests or guards needed;
- owner decisions needed.

This applies to:

- canonical Scripture chunking;
- boundary/noncanonical routing;
- Revelation and other hard-book atlas lanes;
- future master-chunker extraction;
- LawFirm exception-to-automation workflows;
- cross-repo governance changes.

## WORKFLOW-LESSON-003 - No-Context Review Requires A Repo-Resident Audit Path

Independent review should not depend on chat memory, agent summaries, or a previous assistant's
interpretation of its own work. If a separate AI or human reviewer needs to A/B check, red-team, or
verify a branch after commit and push, the repo must provide a durable audit entry point and a
harness that reconstructs the work from repo state.

The required path is:

- `AI_FRONT_DOOR.md`
- `.ai/audits/README.md`
- `.ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md`
- `.ai/control/audit_surface_map.yaml`
- `.ai/control/harness_upgrade_roadmap.yaml`
- `.ai/audits/templates/REVIEW_REPORT_TEMPLATE.md`
- `.ai/audits/reports/`
- `scripts/agent/no_context_audit_harness.py`

The reviewer must reconstruct intent from roadmap state, project status, task files, handoffs, git
diffs, PR metadata, roadmap events, handoff ledger, decision registers, readiness maps, review
packets, and validation output. Chat-only rationale is unproven.

When a task needs independent review, point the reviewer to `.ai/audits/README.md` through the AI
front door and ask for findings-first output.

If a review discovers a repeated manual check, local/CI mismatch, authorization ambiguity,
protected-path risk, source-metadata authority risk, or cross-repo drift, update
`.ai/control/harness_upgrade_roadmap.yaml` or record why no harness is needed.

## WORKFLOW-LESSON-004 - AI Tables Of Contents Need Tags And Use-When Routing

AI tables of contents are operational routing surfaces, not title lists. A no-context agent,
software engineer, auditor, reviewer, or maintainer should be able to search the TOC for the kind
of work they are doing and know which files become relevant before they already understand the
architecture.

Every AI-facing TOC should include:

- a functional tag index;
- `tags:` or `Tags` values for files, task rows, or artifact groups;
- `use when:` or `Use when` triggers that describe the situation where the file matters;
- start-here paths for audit, current state, roadmap, validation, task scope, source metadata,
  theological-risk, owner-decision, data-plane, graph/vector/retrieval, cross-repo governance, and
  developer-engineering work;
- enough vocabulary that another AI can search for likely user phrases such as audit, red-team,
  A/B check, validation, harness, PR review, chunking, WJ, red-letter, capitalization, Strong's,
  cross-reference, owner decision, graph edge, retrieval, raw, canonical, pipeline, schema, or
  governance.

When a maintainer says a file should have been easier to find, treat that as a lesson candidate.
Update the relevant AI TOC and, if the pattern is reusable, this lesson collector. If it can be
checked mechanically, add a test or validator that fails when AI TOCs lose the relevant tag/use-when
routing.

## WORKFLOW-LESSON-005 - Lessons Need A Tagged Index And Graph

Reusable lessons should not live only as prose notes or chat memory. When an increment teaches a
lesson that future agents need before, during, or after chunking work, record it in the appropriate
preflight/workflow/register surface and in the machine-readable chunking lesson index:

- `.ai/control/chunking_lesson_index.yaml`

That index must include:

- searchable tags;
- use-when triggers;
- categories;
- related tasks, decisions, and workflow lessons;
- source and preflight surfaces;
- downstream risks;
- non-authorizations;
- validators;
- graph edges to related lessons.

The point is not to create a new authority layer. The index is a routing and memory surface. It does
not authorize chunk output, reviewed-gold promotion, graph/retrieval truth, route behavior,
evaluator changes, boundary import, or theological claims by itself.

When a task changes lesson/preflight/methodology/register/audit/TOC surfaces, update the lesson
index or record in the task handoff why the change taught no reusable lesson. If the relationship is
machine-checkable, update `scripts/validate_chunking_lesson_index.py` and focused tests.

## T327-LESSON-001 - Untracked Generated Outputs Move the Burden to Generator and CI

T327C showed that `data/canonical/**` can be intentionally gitignored generated output. In that
model, correctness cannot be reviewed by committed JSONL diffs. It must be reviewed through exact
regeneration command, committed generator flags, fail-closed scope validator, CI regeneration path,
DATA_MAP count deltas, protected-path checks, and explicit downstream fallout handoff.

If full pytest fails because downstream gold/chunk baselines still reflect the prior corpus, do not
silently re-baseline. Either quarantine exactly the known fallout with a task-bound xfail, or require
explicit owner decision to merge red. The next task must remove the quarantine and perform the real
re-baseline.

Outcome from T327:

- T327C corrected canonical generated outputs.
- T327D performed the real chunk/gold/score re-baseline.
- T327E cleaned residual eval/stress/review surfaces.
- T327F documented planning-only boundary intake controls.

## BOUNDARY-WORKFLOW-LESSON-001 - Boundary Source Intake Requires Planning, Authority Scope, and Owner Authorization

Boundary-source intake must begin as planning and control metadata, not corpus import. Listing a
source family as a future candidate does not approve source acquisition, normalization,
corpus-record creation, default retrieval, or canonical claim promotion.

Future boundary intake requires:

- Owner authorization.
- Source identity.
- License review.
- Provenance.
- Trust level.
- Tradition scope.
- Profile scope.
- Contamination controls.
- Retrieval-default policy.
- Explicit cross-repo contract with `logos-boundary-literature`.

Boundary material must not override, equal, contaminate, or silently reinterpret canonical Scripture
authority. `logos-scripture-graph` remains the canonical 66-book Scripture graph.

## BIBLE-CHUNKING-WORKFLOW-LESSON-001 - Bible-First Chunker Priority and Route Isolation

The canonical 66-book Bible chunker is the highest-priority chunking substrate. Future
noncanonical, boundary, commentary/reception, legal-document, or master-chunker adaptations must be
separate from and subordinate/non-superior to that priority.

The optimized post-T327 roadmap teaches structural primitives behind route-specific skills instead
of one global heuristic pile. Psalms are the current implementation lane because reviewed evidence
and a candidate-skill seam already exist. Revelation is likely a harder interpretive book and should
receive an early hard-book atlas/review-packet lane, but no Revelation implementation should begin
until reviewed gold exists.

If adapting the chunker for boundary or noncanonical material would degrade canonical Bible
chunking quality, split or rebuild a separate chunker/harness rather than compromising the Bible
chunker.

## BIBLE-CHUNKING-WORKFLOW-LESSON-002 - Whole-Bible Readiness Requires Lane Evidence, Not Global Permission

A whole-Bible chunker is the destination, but whole-Bible algorithm work should not begin as a
single global pass. The faithful route is one reviewed lane at a time: target selection, pending
review packet, owner decision, executable reviewed gold, route-isolated implementation, same-baseline
evaluation, and then a promotion or hold decision.

This lesson exists because "get the algorithms ready for the whole Bible" can sound like permission
to run broad output-changing work. It is not. Whole-Bible readiness is a map of prerequisites,
lane status, algorithm surfaces, and lesson/decision registers. It does not authorize output
changes by itself.

Applies to:

- Revelation review and future Revelation implementation.
- Epistle, narrative, wisdom/dialogue, prophetic, Gospel discourse/WJ, and Bible-wide
  orchestration lanes.
- Any future master-chunker or cross-corpus adaptation.

Required posture:

- Keep the canonical 66-book Bible goal visible.
- Choose one lane and one exact target at a time.
- Keep route-specific assumptions isolated.
- Record theological-downstream decisions in the chunking theological decision register.
- Update this lesson collector or record a no-change rationale when an increment teaches a reusable
  workflow lesson.

## BIBLE-CHUNKING-WORKFLOW-LESSON-003 - Source Metadata Must Be Read First And Kept Non-Authorizing

Every chunking agent must read the chunking-agent preflight and source-metadata rule before doing
chunking, review-packet, evaluator, route, graph, or ingest work. The raw Bible source includes
metadata such as internal cross-references, Strong's-style Hebrew/Greek word numbers, lexeme tags,
footnotes, headings, words-of-Jesus markers, paragraph/poetry markers, alternate readings, and other
edition formatting.

That metadata must be preserved as provenance-bearing evidence, but it must not become automatic
Scripture authority, lexical authority, intertext authority, speaker authority, graph-edge
authority, or chunk-boundary authority. If a future task wants any metadata type to influence
output-changing behavior, it needs owner review, reviewed gold or equivalent governed evidence,
explicit scope, tests, and a decision-register entry.

Enforcement surfaces:

- `.ai/control/chunking_agent_preflight.yaml`
- `scripts/validate_chunking_agent_preflight.py`
- `docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md` rule `CHUNK-METADATA-001`
- `.ai/control/chunking_theological_decision_register.yaml` decision `CD-015`

## BIBLE-CHUNKING-WORKFLOW-LESSON-004 - Midflight Lessons Must Feed Back Into Preflight

A task has learned a durable lesson when the maintainer has to remind the agent of context the repo
should already provide, when an agent discovers that required context was missing from preflight or
handoff, or when the same warning would otherwise need to be repeated across future tasks.

Treat the issue as a lesson candidate when it could recur and it affects source metadata authority,
theology, canon scope, speaker attribution, intertext claims, graph edges, output changes, reviewed
gold, or chunking workflow. The closeout question is: What did this task teach that future chunking
agents must receive before or during similar work?

Required routing:

- If future agents must know it before work starts, update `.ai/control/chunking_agent_preflight.yaml`.
- If agents must do or check it during work, update `.ai/workflows/chunking-skill-supply-chain.workflow.md`.
- If it is a reusable chunking rule, update the methodology/rules registry.
- If it can create theological downstream effects, update the chunking theological decision register.
- If it is machine-checkable, add or update a validator/test.
- If no durable surface changes, record the no-change rationale in the task handoff.

## WORKFLOW-LESSON-006 - Context Always Matters Before Chunking

Every Bible passage must be read in context before a chunking, review-packet, graph, retrieval,
route, evaluator, or theological-risk task treats it as evidence. At minimum, future agents should
check the immediate previous/following unit, paragraph or section context, chapter and book flow,
canonical context, original-language context if used, historical/cultural background if relevant,
and source metadata context if cited.

This lesson exists because a verse, phrase, or proposed boundary isolated from its setting can
become proof-texting, hidden system selection, anti-orthodox smuggling, or accidental output
authority.

Required routing:

- Read `.ai/control/contextual_reading_policy.yaml` before chunking or review-packet work.
- Record immediate, local, book, canonical, language, historical, and metadata context fields in
  future review packets when applicable.
- Keep historical/cultural background lower than canonical Scripture authority.
- Do not create a separate history repo unless later owner authorization, trust-zone policy,
  cross-repo governance, and anti-smuggling validation exist.
- Treat context as required evidence and guardrail, not automatic doctrine, chunk-boundary,
  reviewed-gold, graph, retrieval, route, evaluator, or output authority.

## WORKFLOW-LESSON-007 - Research Autonomy Is Not Authority Autonomy

When the owner authorizes non-output-changing research/prep to continue, agents may compile target
options, risks, evidence, review-packet drafts, metadata watchpoints, contextual reading fields,
and original-language or textual-variant sensitivities without stopping at every research step.

That speed-up does not authorize target selection, reviewed-gold promotion, child spans,
implementation, output, route/evaluator behavior, graph/retrieval/vector truth, boundary import,
preferred readings, source-tradition preference, canon-scope change, or theological authority.

Required routing:

- Record the runway in a machine-readable control surface such as
  `.ai/control/t376_epistle_research_runway.yaml`.
- Add the theological-downstream decision to `.ai/control/chunking_theological_decision_register.yaml`.
- Add the reusable lesson to `.ai/control/chunking_lesson_index.yaml`.
- Update `.ai/control/chunking_agent_preflight.yaml` if future agents must read it before work.
- Add validators/tests that fail if a research surface becomes authorizing.
- Return to the owner before any promotion, implementation, output, graph/retrieval/vector,
  boundary-import, or theological-authority decision.

## WORKFLOW-LESSON-008 - Bible-Wide Research Readiness Must Be Synthesized Before Chunking Resumes

Broad Bible-wide research can continue faster than target-by-target owner decisions, but it is not
complete until the repo has one deterministic synthesis that future agents can read before chunking
resumes.

That synthesis must show:

- what is ready for review-packet strengthening;
- what still needs more research;
- which human decisions are required, with serious faithful options and repercussions;
- which authority-changing actions remain blocked;
- and the exact next non-output-changing step.

Required routing:

- Record the synthesis in a machine-readable control surface such as
  `.ai/control/t384_bible_wide_research_readiness_synthesis.yaml`.
- Add the theological-downstream decision to `.ai/control/chunking_theological_decision_register.yaml`.
- Add the reusable lesson to `.ai/control/chunking_lesson_index.yaml`.
- Add the synthesis to `.ai/control/chunking_agent_preflight.yaml` and the AI TOCs.
- Add validators/tests that fail if the synthesis becomes target selection, reviewed gold, child-span
  promotion, output authority, route/evaluator behavior, graph/retrieval/vector truth, boundary
  import, preferred reading/source-tradition selection, canon-scope change, or theology authority.
- Return to the owner through the next explicit owner-decision packet before promotion,
  implementation, or output work.

## WORKFLOW-LESSON-009 - Every Canonical Passage Needs Coverage Before Chunking Resumes

Bible-wide research is not enough if future agents cannot prove every canonical passage was
accounted for. Before new chunk-output work resumes, the repo needs deterministic verse/passage
coverage that maps all 31,103 canonical passage records to routine status, deeper-review needs,
owner-decision needs, and blocked authority actions.

That coverage must show source-metadata sensitivity, Strong's-style number presence, original
language phrase/context needs, textual-variant/source-tradition sensitivity, WJ/red-letter and
speaker/discourse risk, cross-reference/intertext risk, divine-name/title capitalization signals,
known non-orthodox pressure passages, theological downstream risk, and which passages need human
owner review before promotion or implementation.

Required routing:

- Record the coverage as deterministic machine-readable surfaces, including a one-record-per-passage
  inventory, taxonomy, summary, readiness matrix, gap register, and owner-review docket.
- Add the theological-downstream decision to `.ai/control/chunking_theological_decision_register.yaml`.
- Add the reusable lesson to `.ai/control/chunking_lesson_index.yaml`.
- Add the summary, gap register, docket, and target-passage inventory lookup to
  `.ai/control/chunking_agent_preflight.yaml` and AI TOCs.
- Add validators/tests that fail if canonical passages are missing, duplicated, mislabeled as
  routine while blocked, or disconnected from the owner-review docket.
- Do not treat coverage status as chunk output authority, reviewed gold, graph/retrieval truth,
  route/evaluator behavior, preferred reading/source-tradition selection, canon-scope change, or
  denominational theology authority.

## WORKFLOW-LESSON-010 - Test Runtime Preflight Prevents Tool-Timeout Confusion

When a validation or pytest command exceeds the default tool timeout, agents must record that as a
runtime lesson rather than letting future agents rediscover it. A timeout is not a passing test and
is not an excuse to skip the gate. The right response is to rerun with an appropriate timeout,
split the suite to isolate failures when useful, and update deterministic runtime guidance.

Required routing:

- Read `.ai/control/test_runtime_preflight.yaml` before repo-wide validation or full pytest runs.
- Use the recorded timeout for known slow commands, especially `python -m pytest -q`.
- Run focused tests first when a changed area is narrow, then run the full suite with the recorded
  longer timeout before claiming completion.
- If a command times out or becomes reliably slow, update the runtime profile with command,
  observed context, observed result, recommended timeout, split strategy, and do-not rules.
- Record tool timeouts and reruns in the handoff.
- Never treat timeout as green, hide it from the handoff, or mark a goal complete from focused
  tests only when the task requires the full suite.

## WORKFLOW-LESSON-011 - PR Queue Hygiene Requires Escalation Before Work Piles Up

When agents create staged work, local branches, draft PRs, or ready PRs, that work must not sit
quietly while new dependent work keeps building on top of it. A pile of unmerged branches turns
ordinary integration into conflict archaeology, hides stale validation results, and makes it hard to
know whether failures are real regressions or old branch drift.

Required routing:

- Before opening a PR, record the exact next action: keep building, request review, merge when green,
  hold with findings, or close as superseded.
- If a PR or staged branch is not merged promptly, escalate to the owner or integrator instead of
  letting new branches stack silently on top of it.
- When many related PRs exist, create an explicit integration branch/task that merges them in
  dependency order and records which branches are still useful, superseded, or abandoned.
- Do not keep starting new work from stale local state when the correct next step is to merge,
  rebase, close, or ask the owner.
- Report the reusable pattern to DAD as candidate-only cross-repo guidance; DAD may route the lesson,
  but it cannot override local repo authority or merge anything by itself.

This lesson applies especially when multiple AI agents are building in parallel, Rust validator
rollouts are underway, or generated/scratch artifacts are large enough that repeated rework becomes
expensive.

## LAW-FIRM-WORKFLOW-LESSON-001 - Exception-to-Action Requires Candidate, Gate, Ledger, and Scale Package

Operational exceptions, defect clusters, billing/portal/client-carrier deltas, and workflow failures
must first become normalized candidate records with root-cause tags, owner, risk, evidence, and
proposed action. They must not directly become automation, policy, or client-facing behavior.
Promotion requires validation gates, run ledger/audit evidence, approval where needed, and a scale
package.

This Scripture-side collector records the analogue because local LawFirm/FMG worktrees were present
but not safe to update in this PR: at least one candidate repo was on an unrelated branch, and other
candidate repos had untracked or modified local files. Cross-repo LawFirm/FMG updates should be a
separate, repo-scoped PR after selecting the authoritative repo and confirming a clean worktree.

## WORKFLOW-LESSON-004 - Experimental Forks Notify DAD And Reserve Lesson Slots

When this repo tries an experimental strategy fork (e.g. T423 whole-Bible multi-model chunking),
record it for the Digital Asset Directory hub before marathons start:

- Append to `.digital-asset/mail/outbox.jsonl` (candidate-only, local adoption required).
- Add or update `.digital-asset/context-map.json` entry.
- Reserve `.digital-asset/lessons/<fork>.yaml` with `status: pending_experiment`.
- On success or failure, append follow-up outbox message and fill lesson fields — do not treat
  DAD mail as canon authority.

DAD integration: `.digital-asset/dad-integration.json` | Hub: `dad://hub/Digital-Assett-Directory`

## T327 Application Notes

- Generated canonical outputs were corrected by generator/config/CI validation, not by committing
  raw JSONL diffs as source truth.
- T327D was the correct task for chunk/gold/score re-baselining after the corpus-scope correction.
- T327E cleaned live eval/governance surfaces after the baseline reset.
- T327F kept boundary-source intake as planning/control metadata only.
- T327G remains separate and must not begin unless explicitly authorized.
