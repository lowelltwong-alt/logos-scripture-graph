# M7 Sol candidate publication

This is the public, AI-readable index for the M7 Sol whole-Bible chunking research
snapshot at immutable commit
`eaf31a940d3166b49c38ca26eb279392e0a3b25b`. That source object is retained locally
and held from remote publication by T611; it is identified here for reproducibility,
not presented as a public GitHub commit.
It documents what was built, how the agent mesh worked, what failed, what was repaired,
and why the result remains candidate evidence rather than Scripture, graph, retrieval,
or theological authority.

## Honest progress at the frozen commit

| Measurement | Frozen result | Meaning |
|---|---:|---|
| Book-strategy coverage | **66/66 book strategies** | Every canonical book has a strategy record. This measures planning coverage. |
| Candidate-map coverage | **66/66 books; 1,178 candidate-map rows** | The final candidate map accounts for all books. This measures candidate inventory, not quality convergence. |
| Corrective rereview | **22/66 correctively rereviewed** | The corrective manifest was still in progress. Its narrower campaign target was 63 because three early books formed the original depth baseline. |
| Replay qualified | **no** | A process runbook and receipts exist, but there is no validated full replay at this freeze. |
| Release qualified | **no** | File-level provenance, independent convergence, remaining holds, and owner approval are incomplete. |

The older `marathon_progress.yaml` says 66/66 candidate-complete, while
`model_manifest.yaml` says the corrective rereview is 22 books complete. Those are
different stages, not competing percentages. Neither supports a claim that M7 is
production-ready or reviewed gold.

## What is published here

The tracked [`ARTIFACT_MANIFEST.json`](ARTIFACT_MANIFEST.json) is a default-deny,
hash-bound inventory of 279 immutable pointers. It covers:

- all 66 strategy records;
- the final 66-book candidate-map identity and coverage measurements;
- role, routing, campaign, and corrective-review contracts;
- 94 completion, freeze, and validation receipts, including superseded evidence;
- appeals, holds, dissent, and known-failure records selected by a deterministic rule;
- a deep Job worked-example chain; and
- the Psalm failure, repair, and remaining-hold record.

The publication contains **metadata and hashes only**. It does not copy the M7 payload
bytes. This is deliberate: the immutable research tree contains personal machine paths,
temporary raw XML, duplicate pass-one trees, source-derived quotations, and mixed source
licenses. A content-addressed metadata archive can be reproduced from this manifest;
publication of underlying evidence remains held until a file-level provenance and license
review approves an exact allowlist.

## How the Sol agent system worked

The detailed architecture is in
[`M7_SOL_AGENT_SYSTEM.md`](../../architecture/M7_SOL_AGENT_SYSTEM.md). Its essential
shape was a bounded evidence-and-challenge loop:

```text
book strategy
  -> candidate decision
     -> blind primary reviews
        -> peer challenges
           -> author responses
              -> candidate boss ruling
                 -> append-only appeals and dissent
                    -> role-separated postcheck
                       -> hash-bound completion receipt
```

There are 14 formal specialist packs: 11 form-owning primary packs and three
evidence-only packs. The primary routes cover prose/discourse, narrative scenes,
genealogies/lists, law/covenant, Psalms/poetry, wisdom/dialogue, prophecy, Gospel,
Acts, epistles, and apocalyptic literature. Huldah, Apollos, and Priscilla are the
three formal evidence-only packs for Hebrew structure, Greek structure, and explicit
quotation/parallel/intertext evidence.

Jeremiah and John are campaign roles for textual-witness pressure and speaker/discourse
ambiguity. Luke is a campaign evidence identity for verified historical context.
Solomon and Phoebe are campaign aliases for wisdom and epistle openings/closings.
These categories must not be inflated into extra formal packs or independent models.
Passage-level markers selected the actual route; a book genre was only a prior.

The model roles could observe, challenge, preserve alternatives, and issue candidate
rulings. They could not select doctrine, canon, translation, preferred reading, source
tradition, reviewed gold, graph truth, or retrieval truth. The full Sol mesh is one
**correlated model voice**, even where role identities and attempt IDs were separated.

## Graph engineering and learning loops

M7's strongest technical contribution is not a flat list of chunks. It is a typed,
provenance-bearing evidence graph connecting strategies, decisions, exact source refs,
review attempts, challenges, responses, rulings, appeals, parent-hydration relations,
postchecks, and receipts. Relations are directional and explicitly non-authorizing;
similarity or later canonical reuse cannot silently become a symmetric or theological
edge.

The learning loop is visible because failed evidence was retained and converted into
stronger gates. The Psalm campaign is the clearest example:

- historical rounds exposed templated rationales and arithmetic-midpoint alternatives;
- copied parent forms obscured child-local literary function;
- clipped quotations and terminal-punctuation/text-hygiene defects weakened evidence;
- role-deterministic verdict patterns showed that apparent multi-agent agreement could
  still be correlated behavior; and
- repairs removed those measured signatures, while 36 substantive decisions remained
  held with append-only appeals.

The final Psalm receipt reports zero detected encoding-corruption/mojibake cases after
repair. Intermediate clipped-quotation and terminal-punctuation failures remain indexed
as historical evidence rather than being erased.

That history is not hidden. It demonstrates a serious correction loop, but a local pass
does not retroactively prove the entire 66-book candidate map or an independent provider
review.

## Job worked example

Job is included as a high-detail worked example, not a clean gold exemplar. The
superseding `Job_literary_completion_owner_ruling_v1.json` records 93 candidate chunks,
exact 1,070/1,070 verse coverage, 87 accepted decisions, six held decisions, 279 unique
primary attempts, 465 workflow attempts, 80 answered challenge claims, 162 typed
decision relations, and three active appeals. The earlier `Job_completion_v2.json`
remains indexed as superseded evidence instead of being erased.

The Job graph shows why context hydration matters: a small retrieval unit can remain
useful only when it preserves its dialogue cycle, speech parent, prose frame, or sibling
context. Each relation states that it is non-authorizing and lacks boundary authority.

## Excluded or quarantined surfaces

The publication does not copy:

- `.ai/scratch/pytest-*`, runtime, temporary, recovery, or build trees;
- the duplicate `_pass1_archive` tree;
- raw XML, copied source corpora, or source material without clear redistribution
  authority;
- personal absolute paths, OneDrive/AppData locations, or attachment/upload locations;
- untracked defective artifacts from the recovery-held M7 checkout;
- tests separated from absent implementation modules; or
- redundant generated payloads.

The dirty M7 recovery checkout was not edited or cleaned. Every M7 fact in this
publication was reconstructed from immutable Git objects at the pinned commit.

## M8 and convergence gate

M8 is not part of this task. Fable's active lane must finish and freeze independently.
This publication does not read, copy, rebase, clean, compare, or modify M8, and it makes
no full-Bible release-readiness claim.

Only after M8 has its own publication using this contract shape may a small comparison
PR be proposed. That future PR must contain frozen manifest hashes, per-book coverage,
an agreement/disagreement matrix, holds/appeals/dissent/missing evidence, correlated-
model and independence disclosure, and explicit human-review questions. **Any automatic reviewed-gold promotion is forbidden.**

## Reproduction and validation

With the immutable source commit available locally:

```powershell
python scripts/build_candidate_publication.py `
  --check-manifest docs/publications/m7-sol-candidate-v1/ARTIFACT_MANIFEST.json `
  --json
```

The source-independent repository gate is:

```powershell
python scripts/validate_candidate_publication.py
```

To build the metadata-only archive, use a registered task build or temporary path:

```powershell
python scripts/build_candidate_publication.py --package <approved-output-directory> --json
```

The archive name includes its SHA-256. Rebuilding from the same contract and immutable
source produces identical bytes. Final GitHub release publication, PR merge, and any
underlying M7 payload release remain separate human gates.
