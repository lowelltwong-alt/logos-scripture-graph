# Biblical Codex Digital-Pointer Registry

This directory is the canonical-66 lane of a metadata-only, cross-repository catalog.
It stores URLs and provenance—not manuscript images, transcriptions, preferred readings,
or permission to download or reuse anything.

## Ownership

- `logos-scripture-graph` owns pointers whose admitted content is within the default
  66-book canonical scope.
- `logos-boundary-literature` owns deuterocanonical, apocryphal, pseudepigraphal,
  gnostic/heterodox, disputed, forged, and other non-canonical content pointers.
- `logos-governance-architecture` would own any future shared cross-repository policy.
  T518 does not modify that currently conflicted checkout and does not activate a shared
  contract there.

Physical manuscript identity and content-lane identity are deliberately separate. A mixed
codex such as Sinaiticus or Alexandrinus has the same `physical_witness_id` in both repos,
but each repo stores only its own content-lane pointer. `companion_pointer_ids` make that
split discoverable without importing boundary data here.

## Coverage Contract

The two files answer different questions:

- `canonical_66/catalog_roots.jsonl` points to the strongest enumerating scholarly catalogs,
  official collections, union catalogs, and holding-institution portals from which a much
  larger item inventory can be discovered.
- `canonical_66/direct_witnesses.jsonl` is a reviewed seed of important direct digital copies
  and known public mirrors.

The target for catalog-root coverage is extensive and continuously reviewable. Direct-witness
coverage is intentionally `curated_non_exhaustive`. No static list can honestly guarantee every
digital copy because collections add, remove, reidentify, split, merge, or migrate records.
Every row therefore fixes `item_level_complete` to `false`.

## Authority And Rights

`authority_class` describes why a pointer is useful. It never selects a reading or makes a
theological claim. Public mirrors are clearly distinguished from scholarly catalogs and physical
custodians.

All rows use:

```text
rights_status: not_reviewed_pointer_only
download_authorized: false
```

This follows the owner's request to catalog locations before licensing analysis while preserving
the existing acquisition gates. Later rights review must be object-specific.

## Validation

```powershell
python scripts\validate_biblical_codex_pointer_registry.py
python -m pytest -q tests\test_biblical_codex_pointer_registry.py
```

The validator checks schema validity, JSONL parsing, stable/unique identities, lane ownership,
counts, fingerprints, mixed-codex companion routing, and the no-download/no-completeness boundary.
