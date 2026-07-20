# Composer 2.5 / Cursor Handoff

## Task

- task_id: COMPOSER_2_5_BIBLICAL_CODEX_POINTER_REGISTRY
- owner: Lowell Wong
- mode: review, publish, and merge-gate
- requested runtime: Composer 2.5; if unavailable, state the substitution honestly
- created: 2026-07-19

## Completed immutable work

### Canonical Scripture

- worktree: `C:\\tmp\\logos-t518-codex-pointer-registry`
- repository: `lowelltwong-alt/logos-scripture-graph`
- branch: `codex/t518-codex-pointer-registry`
- commit: `1e4cb26becc9bbb7f8ae9b9f42e1749f1622f575`
- location: `data/candidate/source_catalog/biblical_codex_pointers/canonical_66/`
- inventory: 26 catalog roots + 24 direct witnesses = 50 pointers

### Boundary/noncanonical

- worktree: `C:\\tmp\\logos-boundary-t003-codex-pointer-registry`
- repository: `lowelltwong-alt/logos-boundary-literature`
- branch: `codex/t003-codex-pointer-registry`
- commit: `20c80c9261d235f07370d099dcbe1d229356be5b`
- location: `registries/biblical_codex_pointers/boundary_noncanonical/`
- inventory: 12 catalog roots + 8 direct witnesses = 20 pointers

### Shared contract

Both repositories contain `schemas/biblical_codex_pointer.schema.json`, SHA-256:

`CB7FAFC4E987DE633CCEF19D1DE6ED1B5CFAFC9E10BE7A73149ACFEF3B5162D0`

## Evidence

- Both worktrees were clean after commit and exactly one commit ahead of `origin/main`.
- Independent audit passed all 70 rows and all 13 cross-lane companion links.
- Manifest fingerprints and declared counts match committed files.
- Mixed codices use companion IDs and matching `physical_witness_id`.
- No text, images, OCR, downloads, embeddings, or canonical Scripture records were added.
- Every pointer denies download authority and item-level completeness.
- Boundary focused/schema/full checks passed: 58 tests.
- Scripture focused validator and focused registry test passed.
- Scripture full validation has a transparent baseline failure because generated sidecars such as `data/canonical/.../word_tokens.jsonl` are absent. Do not generate sidecars just to green this pointer-only work.

## Authority boundaries

- Canonical 66-book Scripture belongs only in `logos-scripture-graph`.
- Boundary, noncanonical, disputed, reception, and supporting material belongs only in `logos-boundary-literature`.
- Catalog roots are extensive discovery pointers; direct-witness rows are curated and non-exhaustive.
- Never describe the current registry as 100% complete.
- Do not claim canon status, preferred readings, licensing approval, or download/reuse permission.
- Do not import, download, OCR, transcribe, embed, regenerate canonical data, or alter graph/retrieval truth.
- Do not edit `.ai/control/MASTER_CONTEXT.md` or governance authority.
- Do not touch or clean the original dirty checkout or conflicted governance checkout.
- Never force-push, bypass branch protection, dismiss review threads, or merge an unverified head.

## Remaining execution plan

1. Verify each expected commit SHA, clean status, parent/base, exact pathset, and schema hash.
2. Inspect each remote, repository identity, default branch, existing PRs, current remote head, required checks, reviews, draft state, and branch protection.
3. Push only these branches, without force:

   `codex/t518-codex-pointer-registry` to `lowelltwong-alt/logos-scripture-graph`

   `codex/t003-codex-pointer-registry` to `lowelltwong-alt/logos-boundary-literature`

4. Open one PR per repository. Explain metadata-only scope, 50/20 counts, non-exhaustive coverage, and the missing-sidecar limitation.
5. Independently confirm exact remote head SHA, green required checks, non-draft state, resolved reviews, branch protection, and no dependency/security/privacy/scope issue.
6. Re-read the remote head immediately before each merge; merge only the permitted method; verify the merged SHA and final PR state.
7. If identity, checks, reviews, protection, head SHA, or network state is ambiguous, stop and report the exact blocker.

## Dirty-work roadmap

The original checkout remains intentionally dirty and must be split into separate tasks:

| Area | Judgment | Next action |
|---|---|---|
| T468 mirror-freshness files | Useful | Separate atomic branch/commit |
| T470–T478 rights, Leipzig, scholarship, NAS, AI-workspace plans | Mostly useful, distinct scopes | Nine separate task reviews |
| Leipzig raw images / `data/raw/primary_witnesses/` | High rights/provenance risk | Rights ledger and provenance review |
| `.t470-*`, `.t499-*`, `.t514-*` scratch/patch/merge notes | Potentially useful forensic material | Owner review before archive/deletion |
| Governance checkout | Existing conflicts | Separate master-architect/conflict-worker task |

Do not combine these changes with T518 or T003.

## Required final report

Separate:

1. completed and committed;
2. validated but limited by missing generated sidecars;
3. future work and owner/task boundary;
4. intentionally untouched dirty work and unresolved blockers.

Include exact commit SHAs, PR URLs/states, checks, merge SHAs, and actions not performed.

## Cursor pickup prompt

```text
Read and execute:
.ai/handoffs/COMPOSER_2_5_BIBLICAL_CODEX_POINTER_REGISTRY/handoff.md

This is Lowell Wong's authorized “push and merge” handoff for exactly two reviewed registry commits. First read AI_FRONT_DOOR.md, .ai/control/MASTER_CONTEXT.md (read-only), .ai/control/PROJECT_STATUS.md, the T518/T003 task and handoff files, and this handoff.

Verify the immutable SHAs, clean worktrees, exact pathsets, shared schema hash, remotes, PRs, remote heads, required checks, reviews, and branch protection. Push only the two named branches, create/update one PR per repository, independently pass the merge gate, merge only unchanged verified heads, and verify final merged SHAs/states.

Never force-push, bypass protection, dismiss reviews, generate Scripture sidecars, download/import/OCR/transcribe sources, change canon or rights status, edit master context, or touch the original dirty Scripture checkout or conflicted governance checkout. If any identity, check, review, protection, head-SHA, or network state is ambiguous, stop and report the exact blocker.
```

## Status

- Registry construction: complete.
- Independent audit: passed.
- Local commits: complete.
- Remote publication/merge: explicitly authorized, pending deterministic GitHub gates.
