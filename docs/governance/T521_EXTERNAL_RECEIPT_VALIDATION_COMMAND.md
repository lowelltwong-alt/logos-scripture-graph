# External receipt validation command

When the reviewer uses the copy/paste prompt, validate the returned receipt against that exact prompt:

```powershell
python scripts/validate_t521_external_review_receipt.py `
  <receipt-path> `
  --map .ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl `
  --prompt docs/governance/T521_EXTERNAL_REVIEWER_COPY_PASTE_PROMPT.md
```

The generated template is intentionally incomplete and must fail until an external provider fills it.
