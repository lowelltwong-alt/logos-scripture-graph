# sp_durable — campaign-scratchpad durable set (M8_fable)

Copied 2026-08-18 (owner-authorized commit/push checkpoint) from the 6a933340
campaign scratchpad:
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\6a933340-d91c-4d90-b0b0-2cd7f6c69799\scratchpad`

Contents:
- `Ps/freeze/` — the complete, closed Psalms cycle state (append-only
  CYCLE_STATE.md + CYCLE_STATE_CLOSE.md, frozen row generations, review
  manifests, suite reports). This is the durable checkpoint the workspace
  registry's owner_checkpoint_ref names.
- `Ps/deliverables/` — frozen Ps deliverables (chunks.jsonl sha eaa5606d…,
  Ps_completion.json, build_report.json). The sha-verified worktree install
  of these is at `../book_chunks/Ps/` and `../receipts/Ps_completion.json`.
- `Prov/` — the complete Prov Phase-0/Phase-1 staging: extraction inputs,
  byte-proven identity offset map, pmarks, device inventory, and the shared
  verification toolkit (`Prov/tools/`, smoke-tested), plus
  `Prov/freeze/CYCLE_STATE.md` through the resolved owner gate.

AUTHORITY NOTE: for the IN-FLIGHT Prov cycle the live campaign scratchpad
(SP) remains the working authority; this copy is a point-in-time durability
checkpoint taken at the Phase-1 boundary (before writer launches). At Prov
book close the final state is re-synced here. Ps is CLOSED — its copy here
is final. Everything is candidate-only, non-authorizing.
