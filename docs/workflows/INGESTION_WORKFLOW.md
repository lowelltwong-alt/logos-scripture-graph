# Source Ingestion Workflow

## 1. Drop raw file

Place source files under `data/raw/`.

For WEB Classic USFM:

```text
data/raw/bible/eng-web/usfm/eng-web_usfm.zip
```

## 2. Create source manifest

Copy:

```text
data/raw/bible/eng-web/source_manifest.example.yaml
```

Populate:

- source id
- title
- language
- license
- source URL
- archive filename
- checksum
- date downloaded
- importer version

## 3. Validate source manifest

```bash
python pipelines/validate/validate_manifest.py data/raw/bible/eng-web/source_manifest.yaml
```

## 4. Run importer

Defaults read the manifest + zip and emit canonical + processed outputs:

```bash
python pipelines/ingest/usfm_importer.py
```

Canonical outputs land under `data/canonical/` (passages + per-translation
sidecars); processed reports under `data/processed/bible/eng-web/usfm/`.
Generated data is regenerable and is gitignored — re-run this step after a clone.

## 5. Run chunker

The chunker joins passages with translation witnesses by `passage_id`:

```bash
python pipelines/chunking/chunker.py \
  --passages data/canonical/scripture/passages/passages.jsonl \
  --witnesses data/canonical/translations/eng-web/translation_witnesses.jsonl \
  --policy config/chunking/chunking_policy.yaml \
  --out data/derived/chunks/eng-web/chunks.jsonl
```

> v0 is sentence-safe token grouping. Boundary-driven (genre/poetry/psalm/
> BoundaryClaim) chunking is Sprint 3 — see `docs/chunking/CHUNKING_DESIGN.md`.

## 6. Review outputs

Check:

- importer report (`data/processed/bible/eng-web/usfm/parser_report.yaml`)
- `python scripts/validate_all.py` (manifest + JSONL + canon gates)
- chunk output
- handoff file
