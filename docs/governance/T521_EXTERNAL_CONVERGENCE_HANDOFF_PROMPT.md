# T521 external convergence handoff — Sol candidate map

This handoff asks an external provider or human reviewer to independently audit Sol’s candidate-only whole-Bible map. It is deliberately not a promotion request.

## Frozen input

- Candidate map: `.ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl`
- Packet audit: `.ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/packet_convergence_audit.json`
- Expected scope: all 66 Protestant-canon book IDs in the map
- Candidate-only and non-authorizing: required
- Sol packet hash: compute SHA-256 locally at receipt time and record it in the reviewer receipt

Do not read Opus, Codex, Fable, or any sibling-model map before producing the independent review. Do not infer agreement from the existence of Sol’s role reports. Sol’s reports disclose one correlated Codex substrate.

## Reviewer prompt

> You are an independent literary-structural reviewer. Audit the supplied Sol map book by book without deciding theology, canon, authorship, preferred translation, or textual tradition. Check whether each proposed span preserves the smallest coherent literary unit while avoiding chapter-only fragmentation, over-merging, orphaned songs/poems, broken speeches, broken legal procedures, broken parable/oracle cycles, and contextless sensitive passages.
>
> For OT books, identify Hebrew/Aramaic translation and versification risks. For NT books, identify Koine Greek discourse, lexical, and translation risks. Treat roots, glosses, morphology, accents, headings, superscriptions, and cross-references as evidence or review prompts—not boundary authority.
>
> Check internal biblical relations as candidate context only. Record whether a proposed relation is direct, probable, weak, or unresolved; never let a later passage override local literary form.
>
> Red-team every difficult passage. Record the exact scope, the suspected failure mode, counterevidence, an alternative segmentation, confidence, and whether the issue requires human or another-provider review. Preserve reasoned disagreement rather than forcing consensus.
>
> Return a machine-readable report with: `book`, `scope`, `finding_type`, `claim`, `counterevidence`, `recommended_action`, `confidence`, `independence_attested`, `candidate_only`, `non_authorizing`, and an append-only `appeals` array. A clean result means “no issue found in this review,” not “authoritative.”

## Required independence receipt

The reviewer must state provider/model family, whether sibling maps were read (must be false before the review), source artifacts actually consulted, map digest, runtime date, unresolved appeals, and whether the reviewer believes the packet is suitable only for convergence comparison. Any disagreement remains preserved for human adjudication.

No external reviewer may promote a boundary or modify canonical data. The only permitted output is a read-only review receipt and append-only challenge/appeal evidence.
