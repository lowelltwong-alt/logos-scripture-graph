# T431 DAD Preflight

Task: T431 Original-Language Raw Intake And Strong's Overlay Plan
Agent: Codex
Mode: implementation

## Surfaces Checked

- `AI_FRONT_DOOR.md` Digital Asset Directory Enrollment section.
- `docs/methodology/WORKFLOW_LESSONS.md` WORKFLOW-LESSON-004.
- Local clean T431 worktree did not contain `.digital-asset/` mail or context-map files from `origin/main`.
- Central governance checkout was present at `C:/Users/lowel/OneDrive/Desktop/Git Projects/03_World_View/logos-governance-architecture`, but no DAD asset directory was found in the shallow preflight scan.

## Result

Status: `dad_bridge_not_present_on_origin_main`

T431 records this as environment/surface drift, not a blocker. The task adds a local preflight note and keeps DAD candidate adoption non-authorizing. If `.digital-asset/mail/outbox.jsonl` is later present on the integration branch, send a follow-up DAD message describing the reusable pattern:

- manifest-backed raw source intake,
- license-gated downloads,
- raw immutability,
- Strong's overlay as candidate evidence outside raw,
- catalog-only treatment for public-viewable manuscript libraries without cleared bulk reuse terms.

## Candidate Lesson For DAD

Source-access programs need a two-level requirement shape:

- minimum enforceable fields: URL, license, checksum, version/commit, attribution, allowed-use flags;
- extra context: why a source was accepted, why another source is catalog-only, and what downstream authority is explicitly not granted.

This matches the user's request that future DAD requirements include an extra-context area, not just a terse minimum checklist.

## DAD Candidate Reports Sent

Central DAD checkout observed:

`C:/Users/lowel/OneDrive/Desktop/Git Projects/04_Digital_Assett_Directory`

The checkout was dirty and was left untouched except for append-only candidate intake records.

- Lesson ledger id: `dad:rust-rollout-lesson:829dc53e-1688-5290-ab33-3352634c010d`
- Outbox mail id: `dad:mail:829dc53e-1688-5290-ab33-3352634c010d`
- Dirty-intake design outbox mail id: `dad:mail:019ab2a2-09ae-51e1-b77f-d55e6712b292`
- Canonical-66 validation-refresh lesson id: `dad:rust-rollout-lesson:0e46712a-0c4f-5ac2-89d4-0f2f4d431f66`
- Canonical-66 validation-refresh outbox mail id: `dad:mail:0e46712a-0c4f-5ac2-89d4-0f2f4d431f66`

The reports describe:

- raw source packages frequently containing Bible text plus docs, code, media, nested archives, metadata, duplicate renderings, and non-selected variants;
- the reusable raw-immutable plus canonical-source-view pattern;
- the need for DAD to handle very dirty multi-repo reports through categorized, append-only intake, dedupe, triage, and cleanup staging;
- the need for DAD requirements to include minimum enforceable fields plus an extra-context area.
- the need for generated canonical-output refreshes from mixed-scope raw archives to use an explicit canon-scope flag such as `--canonical-66-filter`.
