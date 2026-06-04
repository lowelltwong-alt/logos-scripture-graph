# ADR-0005: Canon profiles for a multi-tradition corpus

## Status

Accepted (2026-06-03)

## Context

The WEB Classic archive includes 15 deuterocanonical / additional books beyond the
66-book Protestant canon (Tob, Jdt, AddEsth, Wis, Sir, Bar, 1Macc, 2Macc, AddDan,
1Esd, PrMan, Ps151, 3Macc, 2Esd, 4Macc). Before this ADR, all 38,058 passages were
emitted with no canon metadata. Per MASTER_CONTEXT §7 and "Explicit rejections",
publishing `data/canonical/` without canon metadata is an implicit canon-theology
decision and is forbidden (this was blocker CANON-1).

## Decision

1. Every `ScripturePassage` carries a `canon_profiles` object and a `testament` field.
2. `canon_profiles` records membership **per tradition** — it asserts nothing globally.
   Recording that a book is canonical in a tradition is not a project endorsement.
3. Tradition membership statuses: `included`, `deuterocanonical`, `appendix`, `excluded`.
4. Authoritative mapping lives in `pipelines/util/canon.py` (dependency-free, deterministic).
   `config/canon/canon_profiles.yaml` is a human-readable mirror.
5. Traditions modeled at v0: `protestant`, `roman_catholic`, `eastern_orthodox`.
   Additional traditions/profiles may be added later without breaking consumers
   (`additionalProperties` allowed on the CanonProfile schema).

## Consequences

- The importer is the source of truth: re-running ingest re-derives canon metadata.
- `schemas/canon_profile.schema.json` defines the contract; `scripts/validate_jsonl.py
  --require-canon` fails if any passage lacks `canon_profiles` (regression guard).
- Consumers (retrieval, UI) can filter by tradition without re-deriving membership.
- A future `TraditionScopedCanonClaim` object can layer authority/ordering claims on
  top of membership without changing passage records.

## Alternatives considered

- Splitting JSONL by canon scope (rejected: bakes a tradition assumption into the
  filesystem; unified records + metadata is more honest).
- Tagging only deuterocanonical books (rejected: consumers would still have to
  re-derive protocanon membership; explicit-everywhere is safer).
