# Codex Audit Bundle — Batch2 Multi-Model Scratch Ladder

**Purpose:** End-of-scratch review packet for Codex integrator after L2–L5 complete (or partial with documented gaps).

## Current state (2026-07-03)

| Layer | Model | Status |
|-------|-------|--------|
| L1 | Cursor | **complete** |
| L2 | Codex | **complete** — `APPROVE_SCRATCH_BUNDLE_FOR_CODEX_REVIEW` |
| L3 | Claude Opus | **complete** — `APPROVE_WEEKLY_LAYER` (P0:0 P1:4) |
| L4 | Gemini | pending |
| L5 | Hostile red-team | pending |

## L1 + L2 + L3 convergence

| Candidate | L1 | L2 | L3 | Convergence |
|-----------|----|----|-----|-------------|
| Jude T402-LC-065 | promote/high | promote/high | promote/high | **3/3 agree** |
| Phlm T402-LC-057 | promote/med | promote/med | promote/med | **3/3 agree** |
| Jonah T402-LC-032 | defer/low | defer/med | defer/**high** | **3/3 agree defer**; confidence rises |

## L3 Claude theology audit

- **Verdict:** `APPROVE_WEEKLY_LAYER` — no P0 theology smuggling
- **Jonah:** defer at **high** confidence; typology firewall insufficient (A-003)
- **Phlm:** promote with v7/v8 ethics-adjacent remediation (A-002)
- **Jude:** clearest gold candidate at theology tier

## L2 Codex integrator verdict

- **Bundle:** `APPROVE_SCRATCH_BUNDLE_FOR_CODEX_REVIEW`
- **P1 findings:** 5 strengthening gaps — see `L2_codex/strengthening_gaps.md`
- **Block now:** `eval/chunking_gold/` copy, harness, output, reviewed gold

## L1 Cursor summary (for Codex to verify or overturn)

### Suggest for gold (after layer convergence)

- **Jude `T402-LC-065`** — `Jude.1.1-Jude.1.2` (confidence: high)
- **Phlm `T402-LC-057`** — `Phlm.1.1-Phlm.1.7` (confidence: medium)

### Suggest defer / not gold yet

- **Jonah `T402-LC-032`** — `Jonah.1.1-Jonah.1.3` (typology firewall; confidence: low)

## Artifacts for Codex review

- Manifest: `.ai/context/agent_work/T417/model_layers/batch2/manifest.yaml`
- Comparison matrix: `decision_transparency/batch_comparison_matrix.yaml`
- Unified ledger: `decision_transparency/batch_decision_ledger.jsonl`
- L1 strengthened packets: `L1_cursor/strengthened_review_packets/`
- L1 gold assessment: `L1_cursor/gold_candidacy_assessment.yaml`
- Promotion packet: `.ai/scratch/submissions/SUB-012/promotion_packet.yaml`

## Codex verdict options (end of bundle)

1. `APPROVE_PROMOTION_PACKET` — scratch bundle safe; recommend which candidates may proceed toward canon strengthening
2. `HOLD_WITH_FINDINGS` — fix gaps before any canon promotion
3. `ESCALATE_OWNER` — theology or authority question needs owner

## What Codex must NOT authorize from this bundle

- Direct `eval/chunking_gold/` writes without owner per-step gate
- Chunk output or harness execution
- Treating L1 suggestions as reviewed gold

## Comparison audit checklist

- [ ] Do L2–L5 gold recommendations agree on Jude?
- [ ] Does any layer reject Phlm ethics handling?
- [ ] Does L3 or L5 escalate Jonah typology to defer/hold?
- [ ] Are all layer decision logs present with required transparency fields?
- [ ] Does comparison matrix `convergence` update after each layer completes?

## Suggested canon promotion path (if bundle approves)

1. Copy approved strengthened packets to `eval/chunking_gold/review_packets/` (separate PR)
2. Owner gate for reviewed gold (per candidate or batch)
3. Harness then output pilot per T415 precedent
