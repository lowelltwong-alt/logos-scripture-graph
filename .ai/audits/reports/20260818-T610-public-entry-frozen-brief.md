Mission: design the public AI-facing entry architecture and safe publication/merge strategy for lowelltwong-alt/logos-scripture-graph, especially PR #194, without mutating any repository or worktree.

Confirmed facts at 2026-08-18:
- PR #194 targets main from scratch/t423-m8-fable at 5c6c36106c49e2ac5795cb98956129cb4fab0620; base snapshot b71b291aaabe20717b5fec8d2eb01209167aaec2.
- It is open, non-draft, CONFLICTING/DIRTY, REVIEW_REQUIRED, has no check runs, 5,923 files, +1,246,177/-28 lines, and an unfilled template.
- Its three commits are: M7 slot registration (0/66), an M7 candidate checkpoint at 22/66 that excluded known oversized defective untracked files, and an M8 checkpoint at 19/66 through Psalms with Proverbs staged.
- Every campaign artifact is candidate-only and non-authorizing; reviewed-gold, canonical Scripture, graph/retrieval truth, and theology authority remain separately human-gated.
- The current local checkout is scratch/t423-m7-sol, held for recovery, 8 commits ahead of origin/main, with 642 tracked and 3,715 untracked paths. PROJECT_STATUS reports later M7 work at 59/66 and current book 1 Peter; do not infer completion.
- M8 is owned by Fable 5, active, protected from mutation by other agents, at 19/66/current book Proverbs. Its pushed checkpoint intentionally moved beyond an older resume snapshot; the global validator currently fails on that stale probe.
- Prior cleanup checkpointed Boundary and Doctrine dashboards; the latest audit says only protected M7 and M8 remain dirty.
- The repo is public-facing and is the canonical 66-book Scripture data/knowledge-plane implementation governed upstream by logos-governance-architecture. Boundary literature and doctrine genealogy are separate sibling repositories with asymmetric authority.
- Existing .digital-asset/dad-integration.json exposes a local stdio read-only MCP surface; remote MCP is disabled, vendor SDK is not required, and write tools are disabled.
- User wants a concise but credible AI_FRONT_DOOR that lets any AI/human understand Christian ministry mission, repository family, current capabilities, current progress, major workstreams, technical strengths (knowledge graphs, graph engineering, validation, multi-model convergence, learning loops), bronze/silver/gold roadmap, MCP-server path, and exact current-vs-planned boundaries.
- User wants visible independent A/B architecture work followed by convergence, suitable for GitHub and potential employer review.
- User has asked to merge PR #194, but safety, protected-lane, validator, scope, privacy, and non-vacuous test gates remain binding. Do not equate the request with force-push, protection bypass, destructive cleanup, or false completion claims.

Primary local sources to inspect read-only:
AI_FRONT_DOOR.md; .ai/control/MASTER_CONTEXT.md; .ai/control/PROJECT_STATUS.md; ROADMAP.md; ROADMAP_STATE.yaml; docs/architecture/ARCHITECTURE.md; AI_TABLE_OF_CONTENTS.md; docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md; .digital-asset/dad-integration.json; config/governance/repository_link_contract.yaml; .ai/control/governance_dependency_map_mirror.yaml; .ai/control/ai_pr_lifecycle_policy.yaml; .ai/audits/README.md; .ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md.

Output contract:
1. Recommend the smallest coherent public AI entry-point information architecture.
2. Propose exact current/bronze/silver/gold capability language, including the MCP path and ministry/governance boundary.
3. Recommend whether PR #194 should be merged as-is, repaired, split, replaced, or closed, with evidence-based gates and a publication plan for M7/M8 that preserves active research.
4. Identify cleanup that improves employer-facing credibility without erasing research provenance.
5. Provide falsifiers, risks, rollback/kill criteria, and unresolved human choices.
6. Cite local file paths/sections or confirmed PR facts for each load-bearing claim.
7. Do not write files, change Git/GitHub state, read or modify C:\wt\logos-t423-m8-fable, spawn agents, or claim validation not executed.

Privacy/authority: public repository metadata and the named local source files only; no secrets, private rows, raw conversations, or protected M8 worktree content. Stop if a conclusion needs prohibited data or an unapproved mutation.
