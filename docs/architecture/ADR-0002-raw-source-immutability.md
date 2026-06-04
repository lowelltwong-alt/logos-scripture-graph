# ADR-0002: Raw source immutability

## Status

Accepted

## Decision

All downloaded Bible files, lexical datasets, morphology datasets, and cross-reference datasets are stored under `data/raw/` and treated as immutable source artifacts.

## Rationale

A source corpus must be reproducible. If raw files are edited, derived chunks and graph claims cannot be audited back to source.

## Rules

- Raw files are never hand edited.
- Every raw source has a manifest and checksum.
- Derived outputs go under `data/processed/`, `data/canonical/`, `data/derived/`, or `build/`.
- If a source must be corrected, add a patch artifact and provenance record rather than changing the raw file.
