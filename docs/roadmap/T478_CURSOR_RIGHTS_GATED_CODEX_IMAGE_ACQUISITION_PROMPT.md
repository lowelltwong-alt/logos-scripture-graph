# T478 — Cursor Rights-Gated Codex Image Acquisition Prompt

## Outcome

T478 provides a copy-paste Cursor execution prompt for a long-running, resumable codex acquisition into the mapped `Z:` NAS workspace. T478 itself downloads nothing.

The prompt authorizes immediate full-resolution acquisition only for Leipzig University Library-held and Leipzig-digitized Codex Sinaiticus images covered by the library's 2026-07-15 PDM 1.0 permission reply. It allows another image source only after an exact source-level rights ledger proves download/local-storage scope and commercial/public-domain status. All other tracked codices and witnesses remain metadata-only until that gate passes.

## Storage result expected from Cursor

- Source images and exact remote metadata: `Z:\01-Projects\Logos\source-originals\manuscript-witnesses\...`
- Normalized witness catalog: `Z:\01-Projects\Logos\manuscript-witnesses\catalog\`
- Compact manifests: `Z:\01-Projects\Logos\manifests\logos-scripture-graph\codices\`
- Rights, checksums, and lineage: `Z:\01-Projects\Logos\provenance\logos-scripture-graph\codices\`
- Task staging/quarantine and AI run receipts: governed task-specific folders under the existing NAS front doors

The prompt requires Cursor to prove that `Z:` maps to `\\UNAS-Pro\AI.Workspace` before writing, retain 500 GiB free-space reserve, never overwrite, checksum every payload, and resume rather than redownload completed items.

## Research boundaries

This is artifact custody and catalog metadata only. It does not authorize OCR, transcription, embeddings, indexes, model training, textual-critical conclusions, preferred readings, canon changes, boundary-to-canonical import, graph/retrieval truth, release, or publication.

## Portability note

The rights gate, provenance schema, resumable-transfer behavior, verification rules, storage roles, and stop conditions form the provider-neutral core. The file is classified as a Cursor runtime adapter because its invocation and execution language is tailored to Cursor Agent mode. Cross-provider promotion requires a later behavior harness, not merely reuse of the text.
