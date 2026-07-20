---
object_type: roadmap
trust_zone: candidate
lifecycle_status: candidate_foundation_only
task_id: T513
---

# T513 Portable OCR Research Adoption

## Outcome

Logos receives a reusable, domain-neutral OCR comparison and review tool under
`tools/portable_ocr/`, plus a thin metadata-only admission adapter under
`pipelines/ingest/`. The tool is connected to Scripture Graph only through
governed manifests and future human-reviewed results. It has no direct write
path into Scripture, graph, retrieval, vector, preferred-reading, or theology
truth.

This task builds the tool boundary. It does **not** download InduOCR, run OCR on
a manuscript, import OCR text, train a model, or activate a new pipeline.

## Architecture

```text
external authorized image or benchmark root
  -> rights + provenance + hash admission manifest
  -> Logos metadata-only preliminary admission adapter
  -> separately implemented future execution-boundary verifier
  -> portable OCR engine A/B[/C] runner
  -> character, punctuation, layout, and Unicode comparison
  -> natural-language human review artifact
  -> immutable review/result manifest outside the repository
  -> later, separately authorized Logos promotion adapter
  -> Scripture Graph candidate evidence (never automatic truth)
```

The portable core owns engine contracts, paired or tie-break routing,
comparison, review presentation, and review-result validation. Logos owns
rights, source authority, storage, graph admission, and human promotion.
Runtime adapters are replaceable and revision-pinned; no permanent model or
provider identity is part of the core contract.

The current Logos adapter never grants payload access or execution, even if a
future policy copy flips its feature booleans. It emits only a preliminary
metadata plan. A later task must implement an execution-boundary verifier that
rehashes an existing regular input file, validates the structured rights record
and immutable benchmark/source manifest, attests genuinely independent engine
identities, and then obtains a separate owner gate.

## InduOCR decision

InduOCRBench is useful as a hard generic transfer benchmark. Its 570 PDFs and
3,402 pages span normal documents and eleven difficult categories, including
history books, handwriting, multi-font documents, microtext, complex
backgrounds, watermarks, multiple columns, visual styles, and extreme layouts.
Those are valuable degradation and layout stresses.

It is not a Bible-manuscript benchmark. The published materials do not
demonstrate Greek, Hebrew, Aramaic, or Latin coverage; accents, vowels,
cantillation, ligatures, nomina sacra, marginalia, critical apparatus, or verse
alignment; or Scripture Graph retrieval and anchor quality. Passing it cannot
establish biblical OCR fitness.

Its rights are also unresolved. The official repository has no LICENSE file,
while the README describes research/academic use. Logos therefore must not
vendor, redistribute, train on, or automatically download it. The adapter is
disabled, points only to an external user-provisioned root, pins the currently
researched Hugging Face revision, and fails closed until a named rights decision
and hash inventory exist.

The initial adapter excludes InduOCR's heavyweight model-bound RAG track.
Deterministic OCR metrics and separate Scripture Graph retrieval metrics are
more portable and less costly. A full battery is a later explicit task after a
tiny category-stratified smoke and independent review.

## Domain-gold requirement

Before Logos can claim manuscript fitness, it needs a separately authorized,
public-domain or licensed evaluation set with human-verified transcriptions and
page/line/verse anchors. It must cover the relevant scripts and difficult
features, and remain isolated from training and tuning.

Required measurements include character and word error by script, exact-span
and punctuation/diacritic preservation, reading order, columns, marginalia,
critical apparatus, verse anchors, graph-anchor resolution, and deterministic
retrieval Recall@k, MRR, and nDCG. Small high-consequence errors must be reported
separately from aggregate character error.

## Deployment contract

- Install the Python package from `tools/portable_ocr/` in an isolated local
  environment.
- Install engine binaries/models separately and pin their revisions and hashes.
- Set `LOGOS_EXTERNAL_ASSET_ROOT` to a protected location outside the repository
  and outside OneDrive.
- Keep input images, OCR candidates, review pages, benchmark content, and engine
  caches outside Git. Only metadata and aggregate result receipts may be
  proposed for tracking.
- Require at least two genuinely distinct engine families or versions. A third
  adapter may act as a tie-breaker, but agreement never becomes truth without
  human review at the applicable gate.
- Retraining or fine-tuning is never assumed. A new engine first passes the
  synthetic/domain benchmark and revision-bound acceptance harness.

## Sequential gates

1. Validate the portable core with synthetic Greek/Hebrew/Latin Unicode,
   punctuation, layout, missing-line, and engine-disagreement fixtures.
2. Obtain a written InduOCR rights/license decision; externally provision and
   hash the exact approved revision.
3. Run a small category-stratified InduOCR smoke and compare it against a frozen
   no-change baseline.
4. If the smoke passes, authorize and measure the full InduOCR hard battery with
   a lower-cost execution worker; keep higher-intelligence review for error
   taxonomy, benchmark design, and consequential deltas.
5. Build and approve the separate biblical-manuscript domain gold set.
6. Only then propose one rights-cleared manuscript OCR pilot and a human-reviewed
   candidate import boundary.

## Stop conditions

Stop on unclear rights, a changed dataset/evaluator revision, absent hashes,
payloads inside Git or OneDrive, cross-source contamination, missing independent
engine identity, benchmark tuning leakage, unexplained regression in a
high-consequence token class, or any attempted automatic promotion to Scripture
Graph truth.

## Current acceptance boundary

T513 is acceptable only as a candidate tool foundation: portable imports,
content-hash provenance, synthetic contract tests, disabled InduOCR profile,
fail-closed external storage and rights gates, repository validation, and a
distinct independent checker. Activation and all real-data execution remain
separate owner decisions.
