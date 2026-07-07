# Per-book chunk storage

Each model saves one book at a time:

```
book_chunks/<Book>/chunks.jsonl
```

Example: `book_chunks/Gen/chunks.jsonl`

After all 66 books: `python scripts/t423_merge_book_chunks.py <model_folder>`
