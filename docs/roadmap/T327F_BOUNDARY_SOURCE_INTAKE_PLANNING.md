# T327F Boundary Source Intake Planning

## Status

- Task: T327F
- Mode: planning
- Status: complete
- Branch: `t327f-boundary-source-intake-planning`
- Planning only: yes
- Source text import: none
- Boundary corpus records: none
- Raw mutation: none
- Canonical mutation: none
- Chunk regeneration: none
- T327G: not started

## Purpose

T327F records the Scripture-side plan for future boundary-source intake work that belongs in
`logos-boundary-literature`, not in `logos-scripture-graph`.

This document answers what excluded or noncanonical material could eventually be considered by the
boundary repo, what controls must exist before any intake, and what must never flow back into the
canonical Scripture graph.

## Scope

This is planning and governance documentation only.

T327F does not:

- import texts;
- download texts;
- move excluded material to `logos-boundary-literature`;
- create boundary corpus records;
- mutate `data/raw/**`;
- mutate `data/canonical/**`;
- regenerate canonical outputs;
- regenerate chunks;
- change chunker, orchestrator, evaluator, leaderboard, or scorecard behavior;
- start T327G.

## Authority Rule

`logos-scripture-graph` remains the canonical 66-book Scripture graph.

`logos-boundary-literature` is a supporting boundary/reception repo. It may provide background,
comparison, reception history, refutation targets, tradition-scoped claims, and commentary/reception
claims, but it is subordinate to, or at minimum never above, canonical Scripture authority.

Boundary material must not override, equal, contaminate, or silently reinterpret canonical Scripture
authority in `logos-scripture-graph`.

Cross-repo authority and registry policy remains owned by `logos-governance-architecture`.

## Excluded Categories For Future Boundary Planning

The following categories are excluded from canonical Scripture passages, chunks, evaluator inputs,
leaderboard inputs, and default Scripture retrieval. They may be future candidates for
`logos-boundary-literature` only after separate source/license/provenance review:

- deuterocanonical/apocrypha;
- noncanonical boundary literature;
- gnostic or heterodox texts;
- disputed or forged texts;
- fake gospels;
- commentary/reception corpora;
- Josephus / Philo / DSS / Qumran / patristic corpora as source texts;
- front matter and glossary as Scripture content.

## Candidate Future Source Families

Candidate future source families, without acquiring or importing them:

| Source family | Possible boundary-repo role | Required pre-intake review |
| --- | --- | --- |
| WEB excluded deuterocanonical/apocrypha files | Boundary/tradition-scoped comparison corpus | License, source provenance, tradition scope, boundary repo schema |
| Septuagint-associated boundary books | Tradition-scoped reception/comparison | Source edition, language scope, copyright, canon-status profile |
| Dead Sea Scrolls / Qumran witnesses | Source-tradition and textual-background evidence | Edition/license review, fragment scope, witness/provenance metadata |
| Josephus and Philo | Historical/reception background | Translation license, work/section identifiers, claim trust level |
| Patristic corpora | Reception history and doctrinal development evidence | Edition/license review, author/work attribution, tradition scope |
| Gnostic and heterodox texts | Refutation targets and reception comparison | Attribution/forgery policy, trust level, contamination controls |
| Disputed/forged/fake gospel materials | Boundary-literature catalog and refutation targets | Explicit noncanonical status, forgery/dispute labeling, source review |
| Commentary corpora | Commentary/reception claims | Claim scoping, provenance, author/tradition metadata |
| Front matter and glossary artifacts | Source/editorial metadata or supporting references | Non-Scripture artifact classification and retrieval exclusion |

This list authorizes no source acquisition.

## License And Provenance Checklist

Before any future boundary-source intake, the boundary repo needs documented evidence for:

- public domain, permissive license, or explicit permission;
- exact source edition and URL or archive provenance;
- source checksum and immutable source manifest;
- translation status and translator/editor attribution;
- copyright and redistribution permissions;
- source language and translation language;
- work title, section identifiers, and stable citation scheme;
- whether the text is source text, translation, paraphrase, commentary, reception claim, or metadata;
- source integrity checks against accidental alteration;
- explicit owner authorization for intake.

No boundary-source text should be imported until these controls are reviewed.

## Tradition-Scoped Canon Status Model

Boundary literature needs canon-status fields that are scoped by tradition and profile. A single
global canonical/noncanonical boolean is not enough.

Minimum future fields:

- `tradition_scope`, such as Protestant, Roman Catholic, Eastern Orthodox, Jewish, academic, or
  other explicit profile;
- `canon_status`, such as included, deuterocanonical, appendix, disputed, excluded, reception-only,
  forged, fake, or commentary;
- `authority_scope`, such as source text, historical background, reception claim, refutation target,
  commentary, or metadata;
- `claim_scope`, such as background-only, comparison-only, tradition-scoped, author-scoped, or
  disputed;
- `provenance_ref` and `license_ref`.

## Trust-Level Model

Boundary material needs a trust hierarchy that prevents semantic smuggling into canonical Scripture.

Proposed levels:

| Trust level | Meaning |
| --- | --- |
| `canonical_scripture` | Owned only by `logos-scripture-graph`; not assignable by boundary repo. |
| `boundary_source_text` | Text preserved for comparison or reception, not canonical authority. |
| `historical_background` | Contextual evidence with provenance and limits. |
| `tradition_scoped_claim` | Claim valid only inside an explicit tradition/profile. |
| `commentary_reception_claim` | Interpretive or reception-history claim, not default Scripture meaning. |
| `disputed_or_forged` | Marked as disputed, forged, fake, heterodox, or noncanonical where applicable. |
| `candidate_unreviewed` | Not usable in retrieval or claims until reviewed. |

Boundary trust levels must never become canonical Scripture authority.

## Source-Intake Decision Gates

Future boundary-source intake must pass these gates before any text or corpus records are created:

1. Owner authorizes the intake task.
2. Governance repo confirms the repo relationship and authority contract still apply.
3. Boundary repo defines or confirms source-intake policy.
4. License/provenance review is complete.
5. Trust hierarchy and tradition-scope model are active.
6. Corpus schema and claim schema are approved.
7. Contamination-control tests are defined.
8. Retrieval defaults exclude boundary material unless explicitly requested.
9. Scripture graph read/write protections are confirmed.
10. A separate boundary-repo branch and PR is opened for any actual intake.

## Contamination-Control Rules

Boundary material must not:

- create or mutate canonical Scripture passage records;
- create or mutate canonical Scripture chunks;
- enter canonical Scripture evaluator, leaderboard, or scorecard inputs;
- become default Scripture retrieval text;
- become default Scripture meaning;
- override or equal canonical Scripture authority;
- mutate canon-status decisions in `logos-scripture-graph`;
- silently provide theological, textual-critical, source-language, speaker-attribution, or
  tradition-scoped conclusions to Scripture graph outputs;
- bypass `logos-governance-architecture` repository-link contracts.

Allowed cross-repo flows:

- Scripture references may point outward to scoped boundary/reception materials as background or
  comparison.
- Boundary literature may reference Scripture.
- Commentary may discuss Scripture and boundary literature.
- Claims may flow only with trust level, tradition scope, profile scope, and provenance.

## Cross-Repo Contract Expectations

Expected future contract:

| Repo | Role |
| --- | --- |
| `logos-governance-architecture` | Owns cross-repo policy, repo registry, link contracts, and authority rules. |
| `logos-scripture-graph` | Owns canonical 66-book Scripture records, chunks, gold/evaluator surfaces, and canonical Scripture authority. |
| `logos-boundary-literature` | Owns boundary/noncanonical/source-intake governance, trust hierarchy, commentary/reception claims, and supporting literature metadata. |

Future boundary intake work should happen in `logos-boundary-literature` under a separate branch and
PR. If a task appears to require boundary material to modify canonical Scripture outputs, stop and
route the conflict to the higher-authority repo.

## Future Tasks Before Any Boundary Corpus Import

No import is authorized by T327F. Future tasks should be isolated:

1. Boundary repo source-intake schema design.
2. Boundary repo license/provenance registry.
3. Boundary repo trust hierarchy and tradition-scope schema.
4. Boundary repo contamination-control tests.
5. Boundary repo retrieval-default policy.
6. Governance repo contract update, if new data flows are introduced.
7. Owner-approved source selection packet for a single source family.
8. Source manifest and checksum-only dry run.
9. Small fixture-only parser/importer test, without real corpus import.
10. Separate source-specific intake PR, only after all gates pass.

## Current Recommendation

Claude Opus max review should review this plan before merge. After merge, T327F remains planning
only. Do not import boundary texts. Do not start T327G unless separately authorized.
