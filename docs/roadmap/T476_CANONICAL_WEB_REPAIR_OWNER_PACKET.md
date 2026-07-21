# T476 — Canonical WEB Repair Owner Packet

**Status:** awaiting_owner_decision  
**Depends on:** T475 independent audit PASS (post-T519)  
**Does not authorize:** T477 regeneration until you explicitly say yes

## Why this packet exists

T474/T519 repaired the importer. T475 measured the exact corpus delta in ignored
shadows and passed independent audit with **zero footnote removals**. Committed
`data/canonical` is still on the pre-repair baseline. T476 is the owner decision
whether to authorize the next task (**T477**) to regenerate committed WEB
canonical surfaces and reset downstream baselines.

## Evidence summary (frozen)

| Surface | Delta vs pre-T474 baseline |
|---|---|
| Footnotes | removed **0**, unchanged **1130** (heading footnotes restored) |
| Word tokens | removed **2** (known bogus Ps.119 heading tokens), unchanged 677686 |
| Translation witnesses | modified **48** (Ps.119 prior-heading + Song prior-speaker cleanups) |
| Passages | unchanged 31103 |
| Cross-refs | unchanged 340 |
| Chunker | not run; no chunk output |

Candidate tip: `0ca574668be2fe7e2df8f2f3e7f26bb91a669355` (PR #189)  
Audit: `.ai/audits/reports/20260720-T475-independent-shadow-delta-audit-post-t519.md` → **PASS**

## Owner options

### Option A — Authorize T477 (recommended to unblock Bible chunking)

Approve a **separately scoped** T477 task to:

1. Regenerate committed eng-web canonical/processed surfaces from the audited importer tip  
2. Reset DATA_MAP / transitional deferrals that were holding pre-T474 baselines  
3. Keep gold/chunk output unauthorized until T478–T480  

**Unblocks:** T500 candidate-only controlled pilots after T477–T479 chain.

### Option B — Hold regeneration

Keep committed canonical as-is; T500 pilots remain held on source-integrity.

### Option C — Narrow regenerate only footnotes/tokens

Usually worse than A (partial baselines confuse validators). Not recommended.

## Explicit non-authorizations (even if you pick A)

Choosing A authorizes **only** opening T477 under a new task scope. It does **not**
by itself:

- change reviewed gold  
- emit chunk output  
- change routes/evaluators  
- create graph/retrieval/vector truth  
- change canon, preferred reading, or theology authority  

## Decision block (owner fills)

```yaml
t476_owner_decision:
  decision: null  # A | B | C
  authorize_T477_canonical_regeneration: false
  decided_by: null
  decided_at: null
  notes: ""
```

## Exact next step after A

1. Set `authorize_T477_canonical_regeneration: true` in the decision block (or reply "authorize T477").  
2. Open T477 with allowed regeneration paths and a full validate_all + pytest gate.  
3. Then T478–T480 / T500 pilots for finishing Bible chunking.
