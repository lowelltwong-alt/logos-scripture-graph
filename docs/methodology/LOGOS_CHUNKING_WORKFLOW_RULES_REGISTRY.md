
---
title: Logos Chunking Workflow Rules Registry
type: workflow_rule_registry
project: Logos Scripture Graph
related_projects:
  - LawFirm OS
  - Legal Document Chunking
status: living_methodology
version: 0.3
created: 2026-06-08
updated: 2026-06-09
importance_scale:
  P0: Critical / stop-the-line
  P1: High / required gate
  P2: Medium / strong default
  P3: Low / advisory
tags:
  - logos
  - chunking
  - governance
  - workflow-rules
  - reviewed-gold
  - evaluator-safety
  - semantic-smuggling
  - corpus-scope
  - generated-artifact-gates
  - boundary-intake
  - lawfirm-os
  - legal-document-chunking
---

# Logos Chunking Workflow Rules Registry

## 1. Purpose

This file is the working rule registry for the chunking workflow developed during the Logos Scripture Graph project.

The goal is to preserve the lessons learned so future Codex, Claude, Cursor, and human-review sessions do not rely on memory.

This registry defines:

- stable rule IDs;
- rule names;
- importance levels;
- context for future AI systems;
- failure modes each rule prevents;
- when each rule applies;
- when it may be overridden;
- who may override it;
- enforcement methods;
- examples from Logos;
- how the rule transfers to LawFirm OS legal-document chunking;
- how to keep updating the rule registry.

This should be treated as a **living methodology artifact**, not a frozen constitution.

---

# 2. Meta-rule: every rule needs context

## RULE-META-001 — Rules Must Carry Context

**Importance:** P0 — Critical / stop-the-line for this registry

### Rule

Every rule in this registry must include enough context for a future AI or human reviewer to understand:

- why the rule exists;
- what failure it prevents;
- what kind of work triggers it;
- how important it is;
- what evidence satisfies it;
- who can override it;
- when it can be broken;
- what must be documented if it is broken.

### Why this rule exists

A future AI may understand a rule label but misunderstand the rule’s purpose.

Example:

```text
CHUNK-GOLD-001 — Reviewed Gold Before Output Change
```

A weak model might think:

```text
A review packet exists, so we can implement.
```

But that is wrong. The real context is:

```text
A review packet is not reviewed gold.
A human-approved expected behavior is required before output-changing work.
```

The rule name alone is not enough.

### What this prevents

This prevents shallow compliance.

A future AI can obey the words of a rule while violating its reason. This registry must make the reason explicit.

### When this applies

Always.

Any new rule must include:

```yaml
id:
name:
importance:
rule:
context:
failure_prevented:
applies_when:
does_not_apply_when:
override_policy:
required_evidence:
enforcement:
examples:
lawfirm_os_transfer:
```

### Override policy

This meta-rule should not be bypassed except for temporary draft rules. If a rule is draft-only, it must be marked:

```yaml
status: draft
context_incomplete: true
```

A draft rule should not be used as a hard gate until context is completed.

---

# 3. Importance scale

## P0 — Critical / stop-the-line

A P0 rule protects against corruption of output, source data, evaluator integrity, theology/textual-critical meaning, legal authority, or human-gated decisions.

If a P0 rule is violated:

```text
stop the task
do not merge
do not proceed to implementation
escalate to human review
```

### Can a P0 rule be broken?

Only with explicit human owner approval and recorded rationale. In many cases, the right action is not “break the rule” but “create a separate task/PR with a stronger gate.”

Examples:

- raw/canonical mutation;
- output-changing chunking;
- evaluator-policy change;
- textual-variant policy;
- legal privilege determination.

---

## P1 — High / required gate

A P1 rule must normally be followed. If skipped, the PR must explain why and get explicit review.

If a P1 rule is violated:

```text
revise before merge unless reviewer explicitly accepts the exception
```

### Can a P1 rule be broken?

Yes, but only with a documented reason and reviewer approval.

---

## P2 — Medium / strong default

A P2 rule is a strong process default. It protects clarity, maintainability, and reviewability.

If a P2 rule is violated:

```text
document rationale
fix if easy
do not block if no substantive safety risk exists
```

### Can a P2 rule be broken?

Yes, when following it would create unnecessary work or noise.

---

## P3 — Low / advisory

A P3 rule is useful but not usually blocking.

If a P3 rule is violated:

```text
note it as improvement/deferred work
```

---

# 4. How to decide which rule matters more

When rules conflict, use this order:

```text
P0 safety rules
> human authorization rules
> raw/canonical integrity
> evaluator integrity
> output integrity
> reviewed gold requirements
> non-authorizing status
> methodology cleanliness
> documentation completeness
```

Practical examples:

## Example 1: combining work vs safety

If CHUNK-RISK-001 says combining is okay but CHUNK-RISK-002 says one item changes output:

```text
CHUNK-RISK-002 wins.
Split the PR.
```

## Example 2: speed vs reviewed gold

If speed suggests implementing a chunk change but CHUNK-GOLD-001 requires reviewed gold:

```text
CHUNK-GOLD-001 wins.
Do not implement.
```

## Example 3: marker evidence vs speaker decision

If `\wj` markup suggests Jesus is speaking but CHUNK-WJ-001 says speaker attribution requires review:

```text
CHUNK-WJ-001 wins.
Create a review packet.
Do not encode the speaker boundary.
```

## Example 4: legal document automation

If a legal-document chunker can classify privilege automatically, but CHUNK-LEGAL-001 says privilege cannot be decided without human review:

```text
CHUNK-LEGAL-001 wins.
The system may flag possible privilege.
It may not decide privilege as canonical fact.
```

---

# 5. How handoffs should use these rules

Handoffs should cite rule IDs instead of copying full rule text.

Preferred handoff format:

```yaml
applicable_rules:
  - CHUNK-RISK-001
  - CHUNK-SEM-001
  - CHUNK-GOLD-001
  - CHUNK-EVAL-001

task_boundary:
  output_change_authorized: false
  evaluator_policy_change_authorized: false
  raw_canonical_mutation_authorized: false
  reviewed_gold_required_before_implementation: true
```

The full rule text lives in this registry and related methodology docs.

This avoids:

- copy/paste drift;
- bloated handoffs;
- conflicting versions of the same rule;
- stale rule text in old handoff files.

---

# 6. Rule summary table

| Rule ID | Name | Importance | One-line summary |
|---|---|---:|---|
| RULE-META-001 | Rules Must Carry Context | P0 | Every rule must explain why it exists, when it applies, and when it can be overridden. |
| CHUNK-RISK-001 | Combine Same-Risk Work Only | P1 | Combine work only when all tasks share the same safety class. |
| CHUNK-RISK-002 | Split When Risk Profile Changes | P0 | Split work if any item changes output, evaluator policy, raw/canonical data, runtime behavior, or human-gated decisions. |
| RISK-GATE-001 | High-Leverage Changes Require Unintended-Consequence Review | P0 / P1 | High-leverage changes must map what they could accidentally authorize, weaken, contaminate, overfit, globalize, or make harder to reverse before merge. |
| CHUNK-SEM-001 | No Semantic Smuggling Through Chunk Boundaries | P0 | Chunking may preserve structure but must not silently decide theology, text criticism, speaker attribution, canon status, privilege, or legal issue classification. |
| CHUNK-GOLD-001 | Reviewed Gold Before Output Change | P0 | Output-changing chunking requires reviewed gold, human decision, rationale, and tests. |
| CHUNK-GOLD-002 | Characterization Is Not Approval | P0 | Characterization describes behavior; it does not authorize implementation. |
| CHUNK-GOLD-003 | Gold Scaffold Is Not Promoted Gold | P1 | A gold plan/scaffold is not reviewed gold until promoted with review and tests. |
| CHUNK-GOLD-004 | Parent Unit Plus Child Chunks Is Valid When Reviewed | P1 | A whole literary unit can have child chunks if human review approves the parent/child model. |
| CHUNK-EVAL-001 | Verify Evaluator Before Optimization | P0 | Before optimizing a skill, verify the evaluator measures the intended behavior. |
| CHUNK-EVAL-002 | Fix Confounded Evaluators Separately | P0 | If the evaluator is wrong, fix it in a separate PR before claiming skill improvement. |
| CHUNK-EVAL-003 | Score Movement Is Not Output Improvement | P0 | If output is unchanged, score movement from evaluator change is evaluator correction, not chunking improvement. |
| CHUNK-MARKER-001 | Markers Are Evidence, Not Authority | P0 | USFM/formatting markers are evidence, not automatic boundary authority. |
| CHUNK-WJ-001 | Words-of-Jesus Markup Requires Speaker Review | P0 | `\wj` cannot decide Jesus/narrator speaker boundaries without review. |
| CHUNK-QS-001 | Selah / `\qs` Is Evidence, Not Automatic Boundary | P1 | Selah/liturgical rubric markers need review before becoming chunk boundaries. |
| CHUNK-VARIANT-001 | Textual Variants Require Textual-Criticism Review | P0 | Major textual variants require textual-criticism review before gold or output change. |
| CHUNK-CANON-001 | Boundary Texts Must Not Contaminate Canonical Scripture | P0 | Noncanonical/boundary texts may reference Scripture but must not become canonical truth by default. |
| CHUNK-BIBLE-001 | Bible-First Chunker Priority | P0 | Canonical 66-book Bible chunking is the highest-priority substrate; split/rebuild other harnesses if adaptation would degrade it. |
| CHUNK-ROUTE-002 | Route-Specific Skills Must Not Leak Globally | P0 | Book/genre-specific rules must stay behind route gates and reviewed gold, not become global heuristics. |
| CORPUS-SCOPE-001 | Raw Source Scope Is Not Canonical Output Scope | P0 | A raw archive may contain more material than the authorized canonical corpus; ingest must enforce the canonical scope. |
| CORPUS-SCOPE-002 | Generated Artifact Corrections Require Durable Generator + Gate | P0 | A local regeneration is not durable unless the generator/config/validator/CI path is committed and fail-closed. |
| CORPUS-SCOPE-003 | Canonical Scope Validation Fails Closed on Missing Identity | P0 | Canonical records without resolvable book/passage identity must fail validation, not silently pass. |
| CORPUS-SCOPE-004 | Corpus Baseline Reset Is Not Chunking Improvement | P0 | Score or chunk changes after corpus-scope correction are baseline resets unless compared within the same corpus/evaluator/gold baseline. |
| BOUNDARY-INTAKE-001 | Boundary Source Intake Is Planning-Gated and Owner-Authorized | P0 | Listing noncanonical source families as candidates does not authorize import, corpus records, default retrieval, or canonical claims. |
| BOUNDARY-GOV-001 | Governance Is Constraint, Not Obstacle | P0 | Boundary-layer agents must not treat governance as something to bypass, weaken, or optimize around. |
| BOUNDARY-GOV-002 | Owner-Reserved Authorization for Boundary-Originated Higher-Layer Changes | P0 | Boundary-originated changes to governance/canonical authority require explicit owner authorization; consensus or automation is insufficient. |
| WORKFLOW-EXCEPTION-001 | Exception-to-Action Requires Candidate, Gate, Ledger, and Scale Package | P1 / P0 when high-stakes | Operational exceptions must become reviewed candidates with evidence, gates, audit/run ledgers, and scale packages before automation. |
| CHUNK-PROFILE-001 | Interpretive Profiles Are Not Canonical Truth | P0 | Heiser/divine-council or other frameworks may be modeled as profiles, not imposed as truth. |
| CHUNK-TEST-001 | Tests Must Lock the Decision Actually Made | P1 | Tests should enforce the reviewed decision, not merely the existence of docs. |
| CHUNK-BYTE-001 | Non-Target Byte Identity Before Output Change | P0 | Output-changing work must prove non-target byte identity. |
| CHUNK-LEDGER-001 | Route/Decision Metadata Must Not Leak Into Chunk Records | P1 | Routing and governance metadata belong in ledgers/sidecars, not chunk records unless schema-approved. |
| CHUNK-HANDOFF-001 | Handoffs Cite Rule IDs | P2 | Handoffs should cite named rules rather than duplicating full doctrine. |
| CHUNK-UPDATE-001 | Methodology Must Learn From Each Increment | P1 | New lessons must update methodology or explicitly record why no update was needed. |
| CHUNK-LEGAL-001 | Legal Chunking Must Not Decide Privilege or Responsiveness Without Review | P0 | Legal chunking may preserve structure but may not decide legal status without human review. |

---

# 7. Detailed rules

---

## CHUNK-RISK-001 — Combine Same-Risk Work Only

**Importance:** P1 — High / required gate

### Rule

Combine related work into one PR only when all work items share the same safety class and risk profile.

### Context for future AI

This rule was created because the project needed to move faster without creating many tiny PRs. The safe compromise is to combine work that has the same kind of risk.

For example, these can often be bundled:

```text
review packets
stress atlas entries
methodology docs
handoffs
non-authorizing tests
status updates
```

They are all governance or evidence surfaces. They do not change chunk output.

### What this prevents

This prevents unnecessary fragmentation of work while still keeping PRs reviewable.

It prevents the project from slowing down due to excessive micro-PRs.

### Applies when

Use this rule when planning a Codex task or PR that includes multiple related non-output-changing items.

### Does not apply when

Do not use this rule to justify bundling evaluator changes, output changes, raw/canonical changes, or human-gated interpretive/legal decisions.

### Override policy

This is a P1 rule. It can be overridden if combining would make review harder, or if the reviewer requests a split.

### Required evidence

The PR report should include:

```text
What was combined
Why it was safe to combine
What was explicitly not touched
What remains human-gated
Whether output/evaluator/raw/canonical changed
```

### Logos example

T317 combined:

- Ps.105/Ps.106 reviewed current-behavior gold;
- John 3/Matthew 5–7 WJ review packets;
- T313 token-size analysis.

This was safe because no output, evaluator formula, raw/canonical data, or skill behavior changed.

### LawFirm OS transfer

Legal-document chunking may combine:

```text
deposition stress cases
email-thread review packets
contract clause packet templates
non-authorizing tests
roadmap docs
```

as long as none of them decide privilege, responsiveness, legal issue classification, evidentiary weight, or client position.

---

## CHUNK-RISK-002 — Split When Risk Profile Changes

**Importance:** P0 — Critical / stop-the-line

### Rule

Split work into separate PRs if any item changes or could change:

- chunk output;
- evaluator scoring policy;
- raw/canonical data;
- runtime skill behavior;
- theological/textual-critical/canon/speaker/tradition-scoped decisions;
- legal privilege/responsiveness/issue-classification decisions.

### Context for future AI

This is the companion rule to CHUNK-RISK-001. Combining is allowed only while risk is uniform. The moment a task crosses into a higher-risk category, it needs its own PR and review lane.

### What this prevents

This prevents dangerous changes from hiding inside large governance PRs.

### Applies when

Apply this whenever a task includes mixed work types or when a planned combined PR touches a higher-risk surface.

### Does not apply when

Does not require splitting purely mechanical or non-authorizing documentation work.

### Override policy

P0. Only a human owner may authorize combining mixed-risk work, and the PR must explicitly explain why.

### Required evidence

If split is not performed, the PR must include:

- explicit human authorization;
- combined-risk rationale;
- protected path check;
- reviewer acceptance.

### Unsafe example

```text
Add John 3 WJ review packet
+ decide Jesus/narrator boundary
+ change chunker output
+ update evaluator
```

This must be split.

### LawFirm OS transfer

Do not combine:

```text
create email-thread stress case
+ decide privilege
+ change email chunker
+ update legal responsiveness metric
```

That must be split into separate PRs.

---

## RISK-GATE-001 - High-Leverage Changes Require Unintended-Consequence Review

**Importance:** P0 for authority, routing, default-behavior, evaluator, corpus-scope, boundary, or
master-chunker changes; P1 for roadmap/control-plane changes

### Rule

Before a high-leverage change is merged, the agent must map what the change could accidentally
authorize, weaken, contaminate, overfit, globalize, or make harder to reverse.

Required review question:

```text
What could this change accidentally authorize, weaken, contaminate, overfit, globalize, or make harder to reverse?
```

Required output categories:

- confirmed risks;
- plausible risks;
- unlikely but high-impact risks;
- watch-later conditions;
- tests or guards needed;
- owner decisions needed.

### Context for future AI

T336 made Bible-first chunker priority, Revelation atlas sequencing, route isolation, and
master-chunker subordination explicit. Claude's post-merge audit found no corrective patch was
needed, but it recommended a deterministic guard for high-leverage follow-up changes.

This rule converts that recommendation into a repeatable review gate. It applies beyond Logos
Scripture work: the same pattern should travel to governance, boundary literature, LawFirm/FMG, and
future reusable architecture when those repos adopt it.

### What this prevents

This prevents roadmap or architecture changes from silently creating permission paths, global
heuristic leakage, canonical/boundary contamination, evaluator overfitting, accidental
implementation authorization, or future degradation of the Bible-first chunking objective.

### Applies when

Use this rule before merging changes that touch:

- authority hierarchy;
- canonical/boundary scope;
- routing/orchestrator behavior;
- chunker/evaluator behavior;
- default retrieval;
- score/leaderboard policy;
- generated artifact behavior;
- workflow rules;
- cross-repo contracts;
- automation permissions;
- master-chunker or reusable architecture;
- client-facing/legal-facing automation.

### Does not apply when

It does not need a full map for tiny typo fixes or formatting-only edits that do not affect rule
meaning, authority, routing, defaults, tests, generated artifacts, or future implementation
authorization. If uncertain, run the review.

### Override policy

P0 triggers cannot be waived by an agent. They require explicit owner or governance review if the
map identifies authority leakage, output authorization, corpus contamination, default-retrieval
change, evaluator/leaderboard meaning change, or unsafe automation.

P1 roadmap/control-plane risks may be accepted by a reviewer only when the map records the rationale
and the guard or watch condition.

### Required evidence

- unintended-consequence map using the categories above;
- tests or guards for machine-checkable risks;
- owner decision for risks that cannot be resolved in the PR;
- future task or watchlist item for deferred risks.

### Logos examples

- A future master chunker must not create a single shared cross-corpus optimization objective across
  Bible and non-Bible corpora.
- Non-Bible training/eval cases must not tune canonical Bible behavior.
- Revelation/apocalypse rules must remain route-isolated and must not leak globally.
- Boundary-source planning must not become backdoor boundary import or default retrieval.

### LawFirm OS transfer

Before a legal or client-facing automation change merges, map whether it could accidentally
authorize action, weaken review, overfit an exception pattern, globalize a client-specific rule, or
make rollback harder.

---

## CHUNK-SEM-001 — No Semantic Smuggling Through Chunk Boundaries

**Importance:** P0 — Critical / stop-the-line

### Rule

Chunking may preserve observed textual structure, but it may not silently encode theological, textual-critical, source-language, canon/boundary-text, speaker-attribution, or tradition-scoped interpretations without explicit human authorization and reviewed evidence/gold.

### Context for future AI

This is one of the core project doctrines.

A chunk boundary is not neutral. It can imply:

- this is one literary unit;
- this speaker continues here;
- this variant belongs here;
- this noncanonical source has authority;
- this theological interpretation is assumed.

The project decided that chunking must not make those decisions silently.

### What this prevents

It prevents chunking from becoming hidden theology, hidden textual criticism, hidden canon policy, or hidden speaker attribution.

### Applies when

Use this rule whenever a chunk boundary could imply interpretive meaning beyond surface structure.

### Does not apply when

It does not block preserving obvious low-risk structure, such as keeping a short psalm whole when there is no interpretive dispute and human-reviewed gold already approves it.

### Override policy

P0. Override requires explicit human decision, reviewed evidence/gold, and tests.

### Required evidence

- review packet;
- human decision;
- reviewed gold or characterization evidence;
- tests if output is changed;
- methodology note if a new class of semantic risk is discovered.

### Bible examples

- John 3: do not decide where Jesus stops speaking and narrator begins without review.
- Mark 16:9–20: do not treat the long ending as ordinary uncontested text without textual-criticism policy.
- John 7:53–8:11: do not silently split/mix the variant zone without review.
- Deut 32:8–9 / Ps 82 / Gen 6: do not impose divine-council interpretation as canonical truth.
- Song of Songs: do not assume speaker labels from editorial headings alone.

### LawFirm OS transfer

A legal chunk boundary may not silently decide:

- privilege;
- responsiveness;
- legal issue classification;
- evidentiary weight;
- legal conclusion;
- client position;
- work-product status.

---

## CHUNK-GOLD-001 — Reviewed Gold Before Output Change

**Importance:** P0 — Critical / stop-the-line

### Rule

Output-changing chunking work requires reviewed gold, explicit human decision, rationale, and tests or validation before implementation.

### Context for future AI

This rule was created after the project realized that output changes need something stronger than a plausible argument. They need an approved expected behavior.

### What this prevents

It prevents the chunker from changing output because Codex or another agent thinks a passage “looks wrong.”

### Applies when

Applies to any change that would alter chunk boundaries, chunk records, routing output, context packets, or other user-consumable output.

### Does not apply when

Does not apply to proposed stress cases, review packets, or analysis-only docs that do not change output.

### Override policy

P0. Human owner approval is required. In most cases, do not override; create reviewed gold first.

### Required evidence

Before output-changing implementation:

```text
review packet
human decision
reviewed gold manifest entry or equivalent
rationale
tests
non-target byte identity check
```

### LawFirm OS transfer

Before changing legal-document chunking:

```text
reviewed legal gold
human legal decision
evidence/rationale
tests locking expected behavior
```

Example: deposition Q/A chunking should not change until reviewed legal gold defines expected Q/A boundaries.

---

## CHUNK-GOLD-002 — Characterization Is Not Approval

**Importance:** P0 — Critical / stop-the-line

### Rule

A characterization packet describes current behavior or risk. It does not approve expected output and does not authorize implementation.

### Context for future AI

The project created review packets for hard cases. A future AI could mistakenly treat those packets as permission to implement changes.

This rule prevents that confusion.

### What this prevents

It prevents “review packet laundering,” where evidence is treated as approval.

### Applies when

Applies to review packets, observed behavior audits, stress atlas entries, and temporary current-behavior findings.

### Does not apply when

Does not apply after a human explicitly promotes a case to reviewed gold with a decision and tests.

### Override policy

P0. A human owner may promote a characterization to reviewed gold, but the promotion must be explicit.

### Required evidence

Promotion requires:

- decision status changed from pending to approved/reviewed;
- rationale;
- manifest or gold file update;
- tests or validation.

---

## CHUNK-GOLD-003 — Gold Scaffold Is Not Promoted Gold

**Importance:** P1 — High / required gate

### Rule

A gold plan, scaffold, or proposed manifest is not reviewed gold until it is explicitly promoted with review and tests.

### Context for future AI

The project initially had gold scaffold files. They were useful, but they did not authorize output-changing work.

### What this prevents

It prevents draft plans from being treated as accepted truth.

### Applies when

Applies to any file named plan, scaffold, proposed, candidate, or pending.

### Override policy

P1. A scaffold may be promoted if reviewed and tested.

---

## CHUNK-GOLD-004 — Parent Unit Plus Child Chunks Is Valid When Reviewed

**Importance:** P1 — High / required gate

### Rule

A whole literary unit may be represented as a parent unit with child structural chunks when human review approves that both unity and internal structure matter.

### Context for future AI

Psalm 78 and Psalm 119 showed that “one unit” and “multiple physical chunks” are not contradictions.

A psalm can be one literary unit while still having child sections.

### What this prevents

It prevents treating every multi-chunk psalm as bad fragmentation.

It also prevents flattening meaningful structure into one chunk merely to improve a metric.

### Applies when

Use this rule for long or structured literary units:

- long psalms;
- acrostics;
- speeches;
- discourses;
- legal blocks;
- complex legal documents.

### Required evidence

- parent unit span;
- child chunk spans;
- rationale;
- human approval;
- tests.

### Logos example

Ps.78:

```text
Parent: Ps.78.1–72
Children:
- Ps.78.1–69
- Ps.78.70–71
- Ps.78.72
```

### LawFirm OS transfer

Legal examples:

```text
Parent document: deposition
Child chunks: Q/A blocks
Parent document: contract
Child chunks: sections/clauses/exceptions
Parent document: motion
Child chunks: argument headings and subarguments
```

---

## CHUNK-EVAL-001 — Verify Evaluator Before Optimization

**Importance:** P0 — Critical / stop-the-line

### Rule

Before optimizing a skill, verify that the evaluator is measuring the intended behavior and not a confounded proxy.

### Context for future AI

This rule came from the `psalms_fragmented` bug. The evaluator grouped all psalm-like chunks by bare chapter number, so Psalm, Song, and Lamentations chapters collided.

### What this prevents

It prevents optimizing against a broken or misleading metric.

### Applies when

Use before any score-moving implementation or skill optimization.

### Required evidence

- evaluator formula inspected;
- metric definition understood;
- target cases identified;
- false positives/false negatives checked.

---

## CHUNK-EVAL-002 — Fix Confounded Evaluators Separately

**Importance:** P0 — Critical / stop-the-line

### Rule

If the evaluator is wrong, fix the evaluator in a separate PR before claiming skill improvement.

### Context for future AI

T311 fixed the evaluator before any Psalm optimization. This prevented score gaming.

### What this prevents

It prevents mixing evaluator correction with output changes and then falsely claiming chunking improvement.

### Applies when

Any metric is discovered to be confounded, book-blind, route-blind, tradition-blind, or otherwise measuring the wrong thing.

### Required evidence

- evaluator bug report;
- before/after metrics;
- proof output did not change;
- score language says evaluator correction, not chunk improvement.

---

## CHUNK-EVAL-003 — Score Movement Is Not Output Improvement

**Importance:** P0 — Critical / stop-the-line

### Rule

If the same output scores differently because the evaluator or evaluator policy changed, describe the change as evaluator/evaluator-policy correction, not chunking improvement.

### Context for future AI

The score moved:

```text
88.5 → 93.0 → 93.5
```

But output did not change. The score moved because the ruler changed.

### What this prevents

It prevents false improvement claims.

### Applies when

Any score changes without chunk output changes.

### Required evidence

- same run ID or byte-identical output;
- old vs new score;
- explanation of evaluator/policy change.

---

## CHUNK-MARKER-001 — Markers Are Evidence, Not Authority

**Importance:** P0 — Critical / stop-the-line

### Rule

USFM and formatting markers are evidence. They are not automatic chunk-boundary authority unless reviewed and promoted to gold.

### Context for future AI

Markers like `\b`, `\wj`, `\qs`, `\q1`, and `\q2` are meaningful but not self-interpreting.

### What this prevents

It prevents mechanical over-splitting or over-trusting editorial markup.

### Applies when

Any chunking decision depends on formatting/source markers.

### Examples

- `\b` = blank/stanza/formatting break.
- `\wj` = words-of-Jesus/red-letter markup.
- `\qs` = Selah/liturgical rubric.
- `\q1`, `\q2` = poetry line markers.

### Override policy

A marker can become boundary authority only through reviewed gold.

---

## CHUNK-WJ-001 — Words-of-Jesus Markup Requires Speaker Review

**Importance:** P0 — Critical / stop-the-line

### Rule

Words-of-Jesus / red-letter markup (`\wj`) may be evidence of speaker markup, but it may not decide Jesus/narrator boundaries without human speaker-boundary review.

### Context for future AI

John 3 and other Gospel passages may have disputed speaker boundaries. Red-letter markup is often editorial.

### What this prevents

It prevents chunking from silently deciding where Jesus speaks.

### Applies when

- `\wj` spans are present;
- Gospel discourse boundaries are being considered;
- speaker attribution affects interpretation.

### Required evidence

- review packet;
- speaker-boundary analysis;
- human decision;
- reviewed gold before output change.

---

## CHUNK-QS-001 — Selah / `\qs` Is Evidence, Not Automatic Boundary

**Importance:** P1 — High / required gate

### Rule

Selah / `\qs` markers are evidence of liturgical/rubric structure, not automatic chunk-boundary authority.

### Context for future AI

Selah may mark pause, musical/liturgical instruction, or structure, but its exact function is not always certain.

### What this prevents

It prevents splitting psalms mechanically at every Selah.

### Applies when

A Psalm stress case includes `\qs` / Selah evidence.

### Required evidence

Human review before Selah becomes a child-boundary rule.

---

## CHUNK-VARIANT-001 — Textual Variants Require Textual-Criticism Review

**Importance:** P0 — Critical / stop-the-line

### Rule

Major textual variants require textual-criticism review before gold, evaluator policy, or output-changing chunking work.

### Context for future AI

Mark 16:9–20 and John 7:53–8:11 are major textual-variant zones. Chunking them as ordinary text can encode a decision about inclusion.

### What this prevents

It prevents chunking from deciding textual inclusion, authenticity, or authority.

### Applies when

- Mark 16:9–20;
- John 7:53–8:11;
- any major textual variant;
- DSS/LXX/MT divergence zones;
- variant footnotes that affect boundaries.

### Required evidence

- textual-criticism review;
- variant-aware policy;
- human decision;
- gold only after review.

---

## CHUNK-CANON-001 — Boundary Texts Must Not Contaminate Canonical Scripture

**Importance:** P0 — Critical / stop-the-line

### Rule

Noncanonical and boundary texts may reference Scripture, but they must not be absorbed into canonical Scripture truth by default.

### Context for future AI

The project identified the need for a separate `logos-boundary-literature` repository for noncanonical, gnostic, heterodox, forged/disputed, and high-trust supporting literature.

### What this prevents

It prevents:

- Gospel of Thomas claims from being treated like canonical Gospel claims;
- Enochic background from becoming universal doctrine;
- forged/fake texts from contaminating canonical Scripture.

### Why this rule was not sufficient by itself in T327

CHUNK-CANON-001 was directionally correct but too high-level to stop the T327 failure. It described the semantic/governance boundary between canonical Scripture and boundary texts, but the failure happened lower in the pipeline: raw-source scope was allowed to become canonical-output scope.

The failure chain was:

```text
raw WEB source archive included 83 USFM files
→ intended canonical output scope was 66 books
→ ingest/generation lacked a hard 66-book allow-list
→ generated canonical outputs contained 81 books / 38,058 records
→ 6,955 non-66 passage/witness records entered generated canonical outputs
→ chunks, scorecards, stress surfaces, and live controls were built on the wider corpus
```

The lesson is architectural and deterministic: a P0 semantic rule must be backed by an ingest-time allow-list, fail-closed validators, CI regeneration checks, and corpus-baseline labeling. A prose rule alone cannot enforce canonical scope.

### Required deterministic enforcement after T327

CHUNK-CANON-001 must be enforced by the newer corpus-scope rules below:

- `CORPUS-SCOPE-001` — raw source scope is not canonical output scope;
- `CORPUS-SCOPE-002` — generated artifact corrections require durable generator + gate;
- `CORPUS-SCOPE-003` — canonical scope validation fails closed on missing identity;
- `CORPUS-SCOPE-004` — corpus baseline reset is not chunking improvement;
- `BOUNDARY-INTAKE-001` — boundary source intake is planning-gated and owner-authorized.

### Applies when

Any task involves:

- 1 Enoch;
- Jubilees;
- Gospel of Thomas;
- Gospel of Judas;
- Apocryphon of John;
- fake gospels;
- known/disputed forgeries;
- gnostic material;
- patristic/Qumran/Josephus/Philo supporting texts.

### Required evidence

- separate boundary-text trust zone;
- tradition-scoped status;
- attribution status;
- contamination controls.

---


## CHUNK-BIBLE-001 - Bible-First Chunker Priority

**Importance:** P0 - Critical / stop-the-line

### Rule

The canonical 66-book Bible chunker is the highest-priority chunking substrate. Future boundary,
noncanonical, commentary/reception, legal-document, or master-chunker adaptations must remain
separate from and subordinate/non-superior to canonical Bible chunking.

If adapting the chunker for noncanonical or boundary material would degrade canonical Bible
chunking quality, split or rebuild a separate chunker/harness rather than compromising the Bible
chunker.

### Context for future AI

T336 records the optimized post-T327 roadmap. Psalms are the current implementation lane because
reviewed evidence and a candidate skill seam already exist. Revelation is likely a harder
interpretive book and should move early in atlas/review work, but no Revelation implementation may
start until reviewed gold exists.

### What this prevents

This prevents future agents from treating a master chunker, boundary corpus, legal-document chunker,
or Revelation-specific work as permission to weaken the canonical Bible chunker.

### Applies when

Use this rule whenever work touches chunker sequencing, skill promotion, future master-chunker
planning, boundary/noncanonical adaptation, or cross-domain chunking transfer.

### Required evidence

- protected-path check for raw/canonical/chunk/evaluator surfaces;
- explicit corpus/authority lane;
- reviewed gold before output-changing Bible chunking;
- separate harness plan if noncanonical/boundary/legal adaptation could degrade Bible chunking.

---

## CHUNK-ROUTE-002 - Route-Specific Skills Must Not Leak Globally

**Importance:** P0 - Critical / stop-the-line

### Rule

Book-specific and genre-specific chunking rules must stay behind router/orchestrator gates and must
not leak globally.

### Context for future AI

The optimized roadmap teaches structural primitives through routed skills rather than one global
heuristic pile. Revelation/apocalypse assumptions must not leak into Psalms, Psalm marker rules
must not leak into prophets, WJ/speaker assumptions must not leak into Revelation, and specialized
rules must not degrade simple books.

### What this prevents

This prevents semantic smuggling and quality regressions caused by applying a hard-book rule to the
wrong book or genre.

### Applies when

Use this rule whenever adding, promoting, or planning a skill for Psalms, epistles, narrative,
wisdom/dialogue, prophetic oracle, Gospel discourse/WJ, Revelation/apocalypse, or a master
orchestrator.

### Required evidence

- route ledger or route plan;
- applies-to scope;
- forbidden global applications;
- reviewed gold or explicit non-authorizing status;
- fail-closed behavior when evidence is insufficient.

---

## CORPUS-SCOPE-001 — Raw Source Scope Is Not Canonical Output Scope

**Importance:** P0 — Critical / stop-the-line

### Rule

A raw source archive may contain more material than the authorized canonical corpus. The authorized canonical output scope must be enforced explicitly by policy/config, ingest filters, validation, and CI.

Raw-source presence is not authorization to emit canonical Scripture records.

### Context for future AI

T327A found the major corpus-scope incident: the raw WEB USFM archive contained 83 USFM files, but `logos-scripture-graph` was intended to serve a 66-book canonical Scripture corpus. Generated canonical passages contained 81 books and 38,058 records, including 6,955 non-66/deuterocanonical/apocryphal records.

The failure was not that a raw archive had extra material. The failure was that the ingest/generation path treated raw archive scope as canonical output scope.

This is the core lesson of how non-biblical material got into the Bible graph:

```text
raw archive included wider material
→ importer/generation path lacked a hard canonical allow-list
→ generated canonical outputs inherited the wider source scope
→ downstream chunks, scorecards, stress surfaces, and gold controls were built on the wrong corpus
```

### What this prevents

This prevents a source package, vendor archive, client production, or document bundle from silently defining the authoritative corpus.

It protects against:

- deuterocanonical/apocrypha entering canonical Scripture outputs;
- front matter/glossary becoming Scripture content;
- noncanonical/boundary texts becoming default retrieval;
- legal discovery productions becoming the authoritative evidence set without scoping;
- raw/intake scope becoming output/authority scope.

### Applies when

Use this rule whenever:

- raw archives are ingested;
- source manifests are introduced;
- canonical outputs are regenerated;
- a new corpus is attached;
- a sidecar or derived output is produced from raw material;
- a legal-document or LawFirm OS corpus is created from productions, DMS exports, client folders, or portal downloads.

### Does not apply when

It does not prohibit preserving raw archives as immutable source evidence. It requires that raw archives be treated as source inputs, not as authority definitions.

### Override policy

P0. Only the project owner or explicit governance process may change the authorized canonical scope. The change must be separate from ordinary ingestion/regeneration work.

### Required evidence

- explicit source inventory;
- authorized corpus scope policy;
- allow-list or equivalent scope contract;
- ingest filter;
- fail-closed validation;
- CI regeneration or validation gate;
- DATA_MAP / count surface showing before/after counts;
- protected path check;
- explicit baseline-reset framing if downstream outputs change.

### Enforcement

- canonical allow-list enforced at ingest;
- validator fails on excluded books and missing identity;
- CI regenerates or validates outputs under the authorized scope;
- count deltas are recorded in DATA_MAP or equivalent surfaces;
- downstream chunks/scorecards/leaderboards carry `corpus_baseline` labels.

### Logos example

T327 corrected the failure by adding:

- canonical 66-book allow-list;
- `--canonical-66-filter`;
- fail-closed validator;
- canonical output regeneration;
- chunk baseline reset;
- stress/gold/index cleanup;
- boundary intake planning for excluded material.

### LawFirm OS transfer

A legal corpus may include produced documents, raw client folders, exports, privileged materials, irrelevant records, drafts, and system metadata. Those may be preserved as raw evidence, but the legal chunker must not treat all raw intake as the authoritative review/output corpus.

Examples:

```text
raw production != responsive set
email export != privilege decision
client folder != filing record
portal download != approved billing rule
```

---

## CORPUS-SCOPE-002 — Generated Artifact Corrections Require Durable Generator + Gate

**Importance:** P0 — Critical / stop-the-line

### Rule

When a correction affects generated artifacts, ignored build outputs, derived evidence, chunks, scorecards, sidecars, or workflow outputs, the correction is not durable merely because a local run produced the right result.

The durable correction must live in committed generator behavior, committed policy/config, fail-closed validation, CI regeneration, and task-scoped tests or reports.

### Context for future AI

T327C showed that `data/canonical/**` and chunk outputs can be intentionally gitignored generated artifacts. In that model, reviewers cannot rely on committed JSONL or chunk diffs to prove correction.

Correctness moves from file diffs to the generation contract:

```text
exact command
+ committed generator flag
+ committed allow-list/config
+ fail-closed validator
+ CI regeneration path
+ count/provenance surfaces
+ handoff into downstream reset task
```

### What this prevents

This prevents false confidence from a local regeneration that is not reproducible or enforced.

It also prevents silent re-baselining in the wrong task.

### Applies when

Applies to:

- canonical output regeneration;
- chunk regeneration;
- derived sidecars;
- scorecard/leaderboard baselines;
- LawFirm exception outputs;
- AI harness outputs;
- any generated artifact not committed as source truth.

### Does not apply when

It does not require committing large generated artifacts if the repo policy intentionally treats them as build outputs. It requires a durable generator-and-gate contract instead.

### Override policy

P0. If generated artifacts are not committed, the PR must prove durability through generator/config/validation/CI surfaces. If this is not possible, stop and redesign the workflow.

### Required evidence

- exact regeneration command;
- generator/config change committed;
- validation command over generated outputs;
- CI or documented local regeneration path;
- DATA_MAP/count report;
- protected path check;
- downstream task handoff for expected fallout;
- no hidden score/improvement claim.

### Enforcement

- generated artifact policy documented;
- generator flags/config committed;
- validation runs against generated outputs where present;
- downstream tests explicitly quarantined or re-baselined in the correct task.

### Logos example

T327C regenerated 66-book canonical outputs into gitignored `data/canonical/**`. Claude approved the design only after verifying that repo policy intentionally treats canonical outputs as generated artifacts and that validation/CI carried the durable correction.

### LawFirm OS transfer

An Exception Lake or automation sprint may produce local “fixed” outputs, but the fix is not durable unless the generator, workflow rule, validation gate, audit/run ledger, and promotion path are committed.

---

## CORPUS-SCOPE-003 — Canonical Scope Validation Fails Closed on Missing Identity

**Importance:** P0 — Critical / stop-the-line

### Rule

Canonical-scope validation must fail closed when a record in a canonical output or canonical sidecar lacks resolvable book/passage identity.

A record with no `book`, `osis_book`, `usfm_book`, `osis_ref`, `passage_id`, or equivalent identity must not silently pass.

### Context for future AI

T327B.1 was created after a review found that glossary-like records could return `record_book_id() == None` and pass validation. That could allow GLO/FRT/supporting material to remain in canonical outputs while the validator reported success.

The fix was to fail closed on unclassified records.

### What this prevents

This prevents:

- glossary/front matter slipping into canonical outputs;
- sidecars with missing identity bypassing scope checks;
- validators reporting success because they cannot classify a record;
- legal metadata or attachments entering a scoped corpus because the validator cannot identify them.

### Applies when

Use this rule when validating:

- canonical passages;
- translation witnesses;
- boundary claims;
- footnotes;
- cross-references;
- section headings;
- word tokens;
- sidecars used by default Scripture retrieval or chunk generation.

### Does not apply when

Supporting/reference metadata may exist outside canonical Scripture outputs if explicitly labeled, scoped, and excluded from default Scripture retrieval. It must not be accepted in canonical outputs by omission.

### Override policy

P0. Missing identity in canonical outputs is a hard failure unless a human owner approves a new schema/path with explicit non-Scripture scope.

### Required evidence

- validator test for missing identity failure;
- excluded-book tests;
- FRT/GLO tests;
- synthetic glossary-like failure test;
- no broad `allow_missing_book` escape for canonical outputs.

### Enforcement

- canonical-scope validator fails on missing identity;
- validators include FRT/GLO and excluded-book tests;
- canonical sidecars must carry resolvable canonical identity or be outside canonical outputs.

### Logos example

T327B.1 added synthetic tests for:

- valid canonical record passing;
- excluded book failing;
- GLO/FRT failing;
- missing identity failing;
- glossary-like unclassified record failing.

### LawFirm OS transfer

Legal record validation must fail closed when a record lacks matter ID, document ID, source system, privilege scope, or production/source identity where required. “Unknown” metadata must not become an unscoped legal corpus record.

---

## CORPUS-SCOPE-004 — Corpus Baseline Reset Is Not Chunking Improvement

**Importance:** P0 — Critical / stop-the-line

### Rule

Score, count, or chunk changes after corpus-scope correction are baseline resets unless compared within the same corpus baseline, evaluator formula, and gold set.

Do not describe cross-corpus movement as chunking improvement.

### Context for future AI

After T327D, the score moved from 93.5 on the pre-T327 wider corpus to 93.6 on the post-T327 canonical-66 corpus. That movement was not chunking improvement. The corpus changed.

The right language is:

```text
pre-T327 wider-corpus baseline
post-T327 canonical-66 baseline
corpus-scope correction / baseline reset
compare rows within the same corpus_baseline
```

### What this prevents

This prevents false progress claims and score gaming.

### Applies when

Applies to any score or metric change caused by:

- corpus shrink/expansion;
- evaluator policy change;
- gold-set change;
- source-scope correction;
- regenerated outputs under a different baseline.

### Does not apply when

If the same corpus, evaluator formula, gold set, and baseline are held constant, a score change may be evaluated as a candidate chunking improvement.

### Override policy

P0. No override for mislabeling. A human may decide to publish a cross-baseline comparison, but it must be explicitly labeled as non-comparable for improvement claims.

### Required evidence

- corpus baseline label;
- evaluator version;
- gold set/version;
- before/after counts;
- provenance note;
- leaderboard/scorecard warning if rows are displayed together.

### Enforcement

- scorecards include `corpus_baseline`;
- leaderboard warns about cross-baseline comparison;
- PR reports must classify score movement as baseline reset or same-baseline improvement.

### Logos example

T327D added `corpus_baseline` labels and preserved the old 93.5 row as historical provenance while adding the post-T327 93.6 canonical-66 baseline.

### LawFirm OS transfer

Do not claim automation improvement when the underlying matter set, carrier mix, billing rule set, client guidelines, or exception taxonomy changed. Label it as a baseline reset unless the comparison set is stable.

---

## BOUNDARY-INTAKE-001 — Boundary Source Intake Is Planning-Gated and Owner-Authorized

**Importance:** P0 — Critical / stop-the-line

### Rule

Boundary-source intake must begin as planning and control metadata, not corpus import. Listing a source family as a future candidate does not authorize source acquisition, normalization, corpus-record creation, default retrieval, or canonical claim promotion.

### Context for future AI

After T327 removed non-66 material from canonical outputs, T327F created planning-only controls for future boundary-source intake. This was intentionally not an import task.

Boundary material may be useful, but it belongs in a supporting repo and must remain subordinate/non-superior to canonical Scripture authority.

### What this prevents

This prevents the project from removing noncanonical material from the Scripture graph and then accidentally reintroducing it through boundary intake, commentary, or retrieval defaults.

### Applies when

Applies to:

- deuterocanonical/apocrypha;
- noncanonical boundary literature;
- gnostic or heterodox texts;
- disputed/forged/fake texts;
- commentary/reception corpora;
- Josephus/Philo;
- DSS/Qumran;
- patristic corpora;
- front matter/glossary as non-Scripture artifacts.

### Does not apply when

It does not prohibit planning, metadata, trust hierarchy design, license review planning, or source family inventory. It prohibits treating those as import authorization.

### Override policy

P0. Future boundary intake requires explicit owner authorization and must occur through the boundary repo under separate source/license/provenance/trust controls.

### Required evidence

Future intake requires:

- owner authorization;
- source identity;
- license review;
- provenance;
- trust level;
- tradition scope;
- profile scope;
- contamination controls;
- retrieval-default policy;
- cross-repo contract with `logos-boundary-literature`.

### Enforcement

- planning YAML must set imports/downloads/corpus records to false until intake is explicitly authorized;
- boundary repo schema/validators must exist before records;
- default retrieval must exclude boundary material unless specifically scoped;
- Scripture repo must never ingest boundary text corpus as canonical data.

### Logos example

T327F set:

```yaml
status: planning_only
imports_allowed: false
downloads_allowed: false
corpus_records_allowed: false
canonical_override_allowed: false
boundary_material_can_equal_scripture_authority: false
future_intake_requires_owner_authorization: true
```

### LawFirm OS transfer

External/client/carrier source intake must begin as planning, source review, and approval gates. Listing a carrier portal, guideline source, or client repository as a candidate does not authorize automation, default retrieval, or client-facing behavior.

---

## BOUNDARY-GOV-001 — Governance Is Constraint, Not Obstacle

**Importance:** P0 — Critical / stop-the-line

### Rule

A boundary/reception/noncanonical layer must treat governance-layer constraints as binding upstream authority, not as blockers to be optimized around.

If a boundary task conflicts with governance, the system must stop and report. It must not recommend weakening, bypassing, reclassifying, or automatically escalating governance policy for the purpose of completing the boundary task.

### Context for future AI

The boundary repo AI front door intentionally makes agents aware of the wider repo topology. That awareness is for routing and authority preservation only.

A dangerous failure mode is:

```text
boundary AI sees governance as a blocker
→ tries to change governance for boundary purposes
→ lower-authority layer pressures higher-authority layer
```

This is an authority inversion.

### What this prevents

This prevents boundary material from becoming a pressure engine against governance or canonical Scripture authority.

### Applies when

Applies whenever a boundary-layer workflow, source-intake process, document, routing policy, or claim appears blocked by:

- governance policy;
- canonical authority;
- repository-link contracts;
- trust hierarchy;
- canonical scope;
- cross-repo policy.

### Does not apply when

It does not block a human-readable escalation warning. It blocks automated permission requests, approval routing, bundled governance changes, or direct edits from the boundary layer.

### Override policy

P0. Only the project owner can authorize a boundary-originated higher-layer change, and authorization must occur in the higher-authority repo.

### Required evidence

- stop-and-report warning;
- origin repo;
- target repo;
- requested change/conflict;
- downstream authority risk;
- contamination risk;
- maintainer/owner review requirement.

### Enforcement

- AI front doors must state governance is constraint, not obstacle;
- boundary-originated higher-layer requests stop with warning;
- no automated permission-request path from boundary layer to governance layer.

### Logos example

The P0 stop-rule PRs added `BOUNDARY-GOV-001` across governance, boundary, and Scripture repos.

### LawFirm OS transfer

A low-authority operational workflow must not treat legal risk, privilege, client policy, or governance constraints as blockers to optimize around. It must stop and escalate to the proper authority.

---

## BOUNDARY-GOV-002 — Owner-Reserved Authorization for Boundary-Originated Higher-Layer Changes

**Importance:** P0 — Critical / stop-the-line

### Rule

Only Lowell Wong, as project owner, may authorize a boundary-originated request to change higher-authority governance, canonical Scripture authority, repository-link contracts, canonical scope, trust hierarchy, or cross-repo policy.

Contributor consensus, contributor volume, automated recommendation, agent routing, or boundary-layer operational need is not sufficient authority.

### Context for future AI

This rule exists because future contributors or automated agents might attempt to normalize boundary-originated governance changes through volume or consensus.

The owner-reserved gate makes clear that no amount of boundary-layer pressure authorizes changing higher-authority layers.

### What this prevents

This prevents authority inversion by popularity, automation, or local operational need.

### Applies when

Any boundary-originated task targets:

- `logos-governance-architecture`;
- `logos-scripture-graph`;
- canonical Scripture authority;
- repository-link contracts;
- canonical scope;
- trust hierarchy;
- cross-repo policy.

### Does not apply when

It does not block ordinary boundary-repo work within its own authority scope. It applies when the boundary layer seeks to change a higher-authority layer.

### Override policy

P0. Explicit Lowell Wong owner authorization is required. It must be recorded in the higher-authority repo.

### Required evidence

- explicit owner authorization;
- decision record;
- rationale;
- target repo;
- risk assessment;
- tests/validation if policy changes.

### Enforcement

- machine-readable policy must set consensus/automation/agent-routing/boundary-need to insufficient;
- AI front doors must stop and warn;
- higher-authority repo must record any allowed exception.

### Logos example

The boundary/governance stop-rule updates encoded that contributor consensus, contributor volume, automated recommendation, agent routing, and boundary-layer need are all insufficient.

### LawFirm OS transfer

Only authorized firm leadership/assigned legal authority may approve changes to legal risk policy, privilege rules, client-communication authority, or billing-governance rules. Operational teams or automation cannot escalate around those authorities.

---

## WORKFLOW-EXCEPTION-001 — Exception-to-Action Requires Candidate, Gate, Ledger, and Scale Package

**Importance:** P1 — High / required gate  
**Escalates to P0** when client-facing, billing, legal-risk, external-representation, privilege, or canonical-authority effects are possible.

### Rule

Operational exceptions, defect clusters, client/carrier deltas, and workflow failures must first become normalized candidate records with evidence, owner, risk, and proposed action. They must not directly become automation, policy, canonical truth, default retrieval, or client-facing behavior.

Promotion requires validation gates, run ledger/audit evidence, approval where needed, and a scale package.

### Context for future AI

This rule transfers the T327 lesson to LawFirm OS and agent-harness workflows. It is the same pattern as:

```text
Exception Lake defect cluster
→ candidate record
→ evidence packet
→ approval gate
→ implementation
→ scale package
```

not:

```text
exception detected
→ automation changes behavior immediately
```

### What this prevents

It prevents defect discovery from becoming ungated automation.

### Applies when

Applies to:

- billing denials;
- carrier portal changes;
- OCG/client guideline deltas;
- workflow exceptions;
- legal document chunking errors;
- retrieval failure clusters;
- AI harness tool failures;
- chunking stress failures.

### Does not apply when

It does not block read-only analysis or candidate drafting. It blocks direct promotion from exception to action.

### Override policy

P1 normally. Escalates to P0 for legal, client-facing, billing-integrity, privilege, or canonical-authority effects.

### Required evidence

- normalized candidate;
- root-cause tag;
- owner;
- risk;
- evidence;
- proposed action;
- approval gate if needed;
- run ledger/audit trace;
- scale package before broad rollout.

### Enforcement

- candidate-only status for detected defects;
- approval required before external/client/canonical effects;
- run ledger for action execution;
- scale package before rollout.

### Logos example

T327 discovered a corpus-scope failure and converted it into staged corrective tasks: audit, guardrail, filter, validator, regeneration, baseline reset, cleanup, boundary planning, and workflow lessons.

### LawFirm OS transfer

Operational exceptions, defect clusters, billing/portal/client-carrier deltas, and workflow failures must first become normalized candidate records with root-cause tags, owner, risk, evidence, and proposed action. They must not directly become automation, policy, or client-facing behavior.

---

## CHUNK-PROFILE-001 — Interpretive Profiles Are Not Canonical Truth

**Importance:** P0 — Critical / stop-the-line

### Rule

Interpretive frameworks such as Heiser’s divine council model may be represented as profiles, not imposed as canonical truth.

### Context for future AI

The user wants the system to understand divine council ideas, watchers, principalities, powers, and related terms without forcing one interpretive framework onto the text.

### What this prevents

It prevents the graph or chunking system from encoding a particular theological school as default truth.

### Applies when

Working with:

- divine council;
- sons of God;
- watchers;
- Nephilim;
- Prince of Persia;
- Baal/Mammon/rival gods;
- principalities and powers.

### Required evidence

- tradition/profile scope;
- asserted vs inferred separation;
- no default canonical imposition.

---

## CHUNK-TEST-001 — Tests Must Lock the Decision Actually Made

**Importance:** P1 — High / required gate

### Rule

Tests should enforce the reviewed decision, not merely the existence of documentation.

### Context for future AI

A test that only checks a file exists does not prove behavior is locked.

### What this prevents

It prevents weak tests from creating false confidence.

### Applies when

Any reviewed gold or human decision is added.

### Good test

```text
Ps.106 is exactly one chunk, Ps.106.1–Ps.106.48, token count matches current output, reviewed_whole_psalm is true.
```

### Weak test

```text
ps106_boundary_review.md exists.
```

Both can be useful, but only the first locks behavior.

---

## CHUNK-BYTE-001 — Non-Target Byte Identity Before Output Change

**Importance:** P0 — Critical / stop-the-line

### Rule

Any output-changing work must prove non-target byte identity.

### Context for future AI

T310 3a proved the skill seam by preserving byte-identical output. This became a safety pattern.

### What this prevents

It prevents a targeted change from drifting unrelated books or forms.

### Applies when

Any chunker/skill/routing change can affect output.

### Required evidence

- baseline output hash;
- new output hash;
- target diff only;
- non-target chunks/context packets byte-identical.

---

## CHUNK-LEDGER-001 — Route/Decision Metadata Must Not Leak Into Chunk Records

**Importance:** P1 — High / required gate

### Rule

Routing, review, and governance metadata should live in ledgers, sidecars, or manifests, not in chunk/context records, unless the schema explicitly authorizes it.

### Context for future AI

T310 kept route facts in the route ledger, not in output chunks, to preserve byte identity.

### What this prevents

It prevents metadata churn and output contamination.

### Applies when

Adding routing, skill, decision, or review metadata.

---

## CHUNK-HANDOFF-001 — Handoffs Cite Rule IDs

**Importance:** P2 — Medium / strong default

### Rule

Handoffs should cite named rule IDs rather than duplicating full doctrine.

### Context for future AI

Copying full rules into every handoff creates drift and bloat.

### What this prevents

- inconsistent rule wording;
- stale handoffs;
- noisy context windows.

### Applies when

Creating or updating handoffs.

### Override policy

It is acceptable to quote full rule text for high-risk tasks or when a human needs the full doctrine inline.

---

## CHUNK-UPDATE-001 — Methodology Must Learn From Each Increment

**Importance:** P1 — High / required gate

### Rule

When an increment produces a reusable workflow lesson, update the methodology docs or explicitly record that no methodology change was needed.

### Context for future AI

This is the “updater” loop. It made the chunking workflow improve over time.

### What this prevents

It prevents lessons from being lost in chat context or handoffs.

### Applies when

A task discovers:

- evaluator bug;
- gold maturity lesson;
- marker governance lesson;
- semantic-smuggling risk;
- review packet pattern;
- combining/splitting PR pattern.

### Required evidence

- methodology doc update; or
- handoff note: “Methodology reviewed: no change required — rationale.”

---

## CHUNK-LEGAL-001 — Legal Chunking Must Not Decide Privilege or Responsiveness Without Review

**Importance:** P0 — Critical / stop-the-line

### Rule

Legal document chunking may preserve document structure, but it may not silently decide privilege, responsiveness, issue classification, evidentiary weight, legal conclusion, or client position without reviewed human authorization.

### Context for future AI

This transfers the Logos chunking doctrine to LawFirm OS. Legal chunking has high-stakes semantic risks similar to theological chunking.

### What this prevents

It prevents AI chunking from accidentally making legal determinations.

### Applies when

Chunking or classifying:

- emails;
- email threads;
- depositions;
- pleadings;
- motions;
- contracts;
- exhibits;
- privilege logs;
- discovery productions;
- settlement communications;
- OCG/carrier guidelines.

### Legal examples

Do not:

- mark an email privileged just because a lawyer is copied;
- split a deposition answer away from its question without review;
- treat a generated issue tag as a legal conclusion;
- treat a document as responsive without reviewed criteria;
- merge thread emails in a way that loses sender/date context.

### Required evidence

- legal review packet;
- human legal decision;
- reviewed legal gold;
- tests;
- audit trail.

---

# 8. How to keep updating this registry

## Update trigger

Update this registry whenever the project learns a reusable workflow rule or changes the importance of an existing rule.

Examples:

- a new evaluator failure mode appears;
- a review packet gets misused;
- a marker behaves differently than expected;
- a legal-document chunking analogue is discovered;
- raw source scope differs from authorized output scope;
- a generated artifact correction depends on a local run or ignored build output;
- a validator silently accepts unknown or unclassified records;
- a baseline reset could be mistaken for improvement;
- Claude flags a new governance risk;
- a rule is repeatedly cited in handoffs and should become named.

## Update process

1. Add or modify a rule.
2. Include context, failure mode, applies-when, override policy, and examples.
3. Assign importance P0–P3.
4. Update handoff guidance if needed.
5. Add or update tests/validators only if the rule is machine-checkable.
6. Record in methodology/handoff that the registry changed.

## Rule update template

```yaml
id:
name:
importance:
status:
rule:
context:
failure_prevented:
applies_when:
does_not_apply_when:
override_policy:
required_evidence:
enforcement:
logos_examples:
lawfirm_os_transfer:
notes:
```

## When a rule can be broken

Rules are not all equal.

A future AI should treat overrides like this:

| Importance | Can be broken? | Who can approve? | Required record |
|---|---|---|---|
| P0 | Rarely | Human owner / explicit governance gate | Decision record + rationale + tests if applicable |
| P1 | Sometimes | Reviewer or owner | PR rationale + reviewer acceptance |
| P2 | Yes | Implementer with rationale | Note in PR/handoff |
| P3 | Yes | Implementer | Optional note |

If uncertain:

```text
Do not break the rule.
Stop and ask for review.
```

---

# 9. Relationship to LawFirm OS

This registry should eventually be copied or adapted into LawFirm OS as a legal-document chunking governance registry.

The legal version should preserve these ideas:

- combine same-risk work;
- split high-risk decisions;
- review packet before legal authority decisions;
- legal gold before output-changing chunker behavior;
- no legal semantic smuggling through boundaries;
- markers/metadata are evidence, not authority;
- evaluator sanity before optimization.

LawFirm OS should add legal-specific rules for:

- privilege;
- responsiveness;
- work product;
- issue classification;
- evidentiary use;
- settlement sensitivity;
- client position;
- confidentiality;
- court filing status;
- billing guideline authority.

---

# 10. Bottom line

The rules are not just restrictions. They are how the project moves fast safely.

The core operating law is:

```text
Move fast inside a single safety class.
Stop when the safety class changes.
```

And the core semantic law is:

```text
Chunking may preserve structure.
Chunking may not decide meaning without reviewed human authorization.
```
