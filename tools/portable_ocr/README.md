# Portable OCR

`portable-ocr` is a domain-neutral, local-first OCR evidence and human-review package. Its Python import is `portable_ocr`. It has no Scripture Graph, Logos, legal-case, cloud, vector-database, or model-provider dependency.

## Boundary

```text
immutable hash-bound page image
  -> independently pinned Engine A and Engine B
  -> Unicode-aware pairwise comparison
  -> required Engine C when the approved policy triggers
  -> offline adaptive human-review HTML
  -> replay- and hash-validated reviewed-text handoff
  -> host application independently decides whether to promote
```

Engine C is evidence, not a vote or tiebreaker. Cross-engine confidence scores are not assumed comparable. Candidates and reviewed derivatives remain `not_source_truth`; only a host-owned human gate can promote them.

The comparator preserves NFC canonical equivalence while flagging Greek/Hebrew script changes, combining-mark/diacritic differences, punctuation differences (including Greek and Hebrew punctuation), layout changes, and suspected missing lines. A future scholarly layer may add manuscript-specific grapheme policies without changing this core.

## Local development

```powershell
cd tools/portable_ocr
python -m unittest discover -s tests -v
python -m pip install -e .
portable-ocr run --source C:\pages\page.png --config local.json --output-root C:\ocr-runs
portable-ocr build-review --run-dir C:\ocr-runs\RUN_ID --output C:\ocr-runs\review.html
portable-ocr build-handoff --run-dir C:\ocr-runs\RUN_ID --review C:\review.json --output C:\handoff.json
```

All adapters start disabled. Before enablement, pin executable and model hashes, verify language/model licensing, run synthetic Greek/Hebrew/Latin fixtures, and obtain an independent human approval. The HTML makes no network requests and uses no browser persistence.

## InduOCR research gate

InduOCR may be used only under the repository's separately approved academic-research and dataset-license decision. Do not download or redistribute it from this package. Record exact dataset revision, rights/terms, fixture hashes, language/script coverage, train/dev/test isolation, and before/after metrics. Never train on evaluation pages or human-review corrections without a new provenance and consent decision. Recommended measurements are CER, WER, grapheme/diacritic error, critical punctuation error, silent-error sampling, review burden, latency, and failure rate.

The portable, disabled profile is `benchmarks/induocr.profile.json`. It contains
no dataset and no downloader. A host may enable a copied, revision- and
hash-complete profile only after its own rights and execution gates pass.

This candidate is not OCR-certified, production-ready, or approved for confidential material.
