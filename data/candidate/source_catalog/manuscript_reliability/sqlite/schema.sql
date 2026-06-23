-- T395 manuscript source-catalog SQLite schema shell.
-- Metadata only: no Scripture text, manuscript transcription, preferred reading,
-- graph/retrieval/vector output, boundary material, doctrine lineage, or
-- apologetic-authority data.

PRAGMA foreign_keys = ON;

CREATE TABLE scripture_source_family (
  source_family TEXT PRIMARY KEY,
  family_label TEXT NOT NULL,
  correct_repo TEXT NOT NULL CHECK (correct_repo = 'logos-scripture-graph'),
  allowed_scope TEXT NOT NULL,
  routes_elsewhere TEXT NOT NULL,
  source_url TEXT NOT NULL CHECK (source_url LIKE 'https://%'),
  method TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  provenance_note TEXT NOT NULL,
  review_status TEXT NOT NULL,
  rights_access_status TEXT NOT NULL,
  non_authorizing_scope_label TEXT NOT NULL,
  stores_scripture_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_scripture_text = 0),
  stores_transcription_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_transcription_text = 0),
  stores_boundary_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_boundary_text = 0)
);

CREATE TABLE scripture_source_catalog (
  catalog_id TEXT PRIMARY KEY,
  source_family TEXT NOT NULL REFERENCES scripture_source_family(source_family),
  catalog_name TEXT NOT NULL,
  source_title TEXT NOT NULL,
  source_type TEXT NOT NULL,
  authority_tier TEXT NOT NULL,
  maintainer_or_institution TEXT NOT NULL,
  base_url TEXT NOT NULL CHECK (base_url LIKE 'https://%'),
  access_model TEXT NOT NULL,
  rights_statement TEXT NOT NULL,
  citation_policy TEXT NOT NULL,
  last_checked_date TEXT NOT NULL,
  source_url TEXT NOT NULL CHECK (source_url LIKE 'https://%'),
  method TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  provenance_note TEXT NOT NULL,
  review_status TEXT NOT NULL,
  rights_access_status TEXT NOT NULL,
  non_authorizing_scope_label TEXT NOT NULL,
  source_anchor_role TEXT NOT NULL,
  source_limits TEXT NOT NULL,
  stores_scripture_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_scripture_text = 0),
  stores_transcription_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_transcription_text = 0),
  stores_boundary_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_boundary_text = 0)
);

CREATE TABLE scripture_holding_institution (
  institution_id TEXT PRIMARY KEY,
  institution_name TEXT NOT NULL,
  country_or_region TEXT NOT NULL,
  collection_name TEXT NOT NULL,
  official_catalog_url TEXT NOT NULL CHECK (official_catalog_url LIKE 'https://%'),
  shelfmark_policy TEXT NOT NULL,
  rights_contact TEXT NOT NULL,
  source_family TEXT NOT NULL REFERENCES scripture_source_family(source_family),
  source_url TEXT NOT NULL CHECK (source_url LIKE 'https://%'),
  method TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  provenance_note TEXT NOT NULL,
  review_status TEXT NOT NULL,
  rights_access_status TEXT NOT NULL,
  non_authorizing_scope_label TEXT NOT NULL,
  stores_scripture_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_scripture_text = 0),
  stores_transcription_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_transcription_text = 0),
  stores_boundary_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_boundary_text = 0)
);

CREATE TABLE scripture_catalog_witness_record (
  catalog_record_id TEXT PRIMARY KEY,
  catalog_id TEXT NOT NULL REFERENCES scripture_source_catalog(catalog_id),
  witness_id_candidate TEXT NOT NULL,
  siglum TEXT NOT NULL,
  alternate_identifiers TEXT NOT NULL,
  shelfmark TEXT NOT NULL,
  holding_institution_id TEXT NOT NULL,
  record_accessed_at TEXT NOT NULL,
  source_family TEXT NOT NULL REFERENCES scripture_source_family(source_family),
  source_url TEXT NOT NULL CHECK (source_url LIKE 'https://%'),
  method TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  provenance_note TEXT NOT NULL,
  review_status TEXT NOT NULL,
  rights_access_status TEXT NOT NULL,
  non_authorizing_scope_label TEXT NOT NULL,
  stores_scripture_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_scripture_text = 0),
  stores_transcription_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_transcription_text = 0),
  stores_boundary_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_boundary_text = 0)
);

CREATE TABLE scripture_witness_identifier (
  identifier_id TEXT PRIMARY KEY,
  witness_id_candidate TEXT NOT NULL,
  identifier_value TEXT NOT NULL,
  identifier_system TEXT NOT NULL,
  identifier_scope TEXT NOT NULL,
  source_catalog_ref TEXT NOT NULL,
  source_family TEXT NOT NULL REFERENCES scripture_source_family(source_family),
  source_url TEXT NOT NULL CHECK (source_url LIKE 'https://%'),
  method TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  provenance_note TEXT NOT NULL,
  review_status TEXT NOT NULL,
  rights_access_status TEXT NOT NULL,
  non_authorizing_scope_label TEXT NOT NULL,
  stores_scripture_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_scripture_text = 0),
  stores_transcription_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_transcription_text = 0),
  stores_boundary_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_boundary_text = 0)
);

CREATE TABLE scripture_witness_date_claim (
  date_claim_id TEXT PRIMARY KEY,
  witness_id_candidate TEXT NOT NULL,
  date_earliest TEXT NOT NULL,
  date_latest TEXT NOT NULL,
  date_display TEXT NOT NULL,
  dating_method TEXT NOT NULL,
  dating_basis TEXT NOT NULL,
  date_precision TEXT NOT NULL,
  dissenting_date_note TEXT NOT NULL,
  source_ref TEXT NOT NULL,
  source_family TEXT NOT NULL REFERENCES scripture_source_family(source_family),
  source_url TEXT NOT NULL CHECK (source_url LIKE 'https://%'),
  method TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  provenance_note TEXT NOT NULL,
  review_status TEXT NOT NULL,
  rights_access_status TEXT NOT NULL,
  non_authorizing_scope_label TEXT NOT NULL,
  stores_scripture_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_scripture_text = 0),
  stores_transcription_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_transcription_text = 0),
  stores_boundary_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_boundary_text = 0)
);

CREATE TABLE scripture_witness_material_claim (
  material_claim_id TEXT PRIMARY KEY,
  witness_id_candidate TEXT NOT NULL,
  language TEXT NOT NULL,
  script TEXT NOT NULL,
  material TEXT NOT NULL,
  format TEXT NOT NULL,
  physical_description_summary TEXT NOT NULL,
  source_ref TEXT NOT NULL,
  source_family TEXT NOT NULL REFERENCES scripture_source_family(source_family),
  source_url TEXT NOT NULL CHECK (source_url LIKE 'https://%'),
  method TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  provenance_note TEXT NOT NULL,
  review_status TEXT NOT NULL,
  rights_access_status TEXT NOT NULL,
  non_authorizing_scope_label TEXT NOT NULL,
  stores_scripture_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_scripture_text = 0),
  stores_transcription_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_transcription_text = 0),
  stores_boundary_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_boundary_text = 0)
);

CREATE TABLE scripture_witness_coverage_claim (
  coverage_claim_id TEXT PRIMARY KEY,
  witness_id_candidate TEXT NOT NULL,
  scripture_scope_type TEXT NOT NULL,
  osis_scope TEXT NOT NULL,
  book_scope TEXT NOT NULL,
  chapter_verse_scope TEXT NOT NULL,
  coverage_precision TEXT NOT NULL,
  coverage_source_ref TEXT NOT NULL,
  stores_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_text = 0),
  source_family TEXT NOT NULL REFERENCES scripture_source_family(source_family),
  source_url TEXT NOT NULL CHECK (source_url LIKE 'https://%'),
  method TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  provenance_note TEXT NOT NULL,
  review_status TEXT NOT NULL,
  rights_access_status TEXT NOT NULL,
  non_authorizing_scope_label TEXT NOT NULL,
  stores_scripture_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_scripture_text = 0),
  stores_transcription_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_transcription_text = 0),
  stores_boundary_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_boundary_text = 0)
);

CREATE TABLE scripture_witness_discovery_event (
  event_id TEXT PRIMARY KEY,
  event_date_earliest TEXT NOT NULL,
  event_date_latest TEXT NOT NULL,
  event_type TEXT NOT NULL,
  witness_or_catalog_ref TEXT NOT NULL,
  what_became_known TEXT NOT NULL,
  what_remained_unknown TEXT NOT NULL,
  reliability_relevance_scope TEXT NOT NULL,
  source_ref TEXT NOT NULL,
  source_family TEXT NOT NULL REFERENCES scripture_source_family(source_family),
  source_url TEXT NOT NULL CHECK (source_url LIKE 'https://%'),
  method TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  provenance_note TEXT NOT NULL,
  review_status TEXT NOT NULL,
  rights_access_status TEXT NOT NULL,
  non_authorizing_scope_label TEXT NOT NULL,
  stores_scripture_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_scripture_text = 0),
  stores_transcription_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_transcription_text = 0),
  stores_boundary_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_boundary_text = 0)
);

CREATE TABLE evidence_source_catalog_method_profile (
  method_profile_id TEXT PRIMARY KEY,
  source_family TEXT NOT NULL REFERENCES scripture_source_family(source_family),
  method_scope TEXT NOT NULL,
  proves TEXT NOT NULL,
  does_not_prove TEXT NOT NULL,
  required_cross_checks TEXT NOT NULL,
  source_url TEXT NOT NULL CHECK (source_url LIKE 'https://%'),
  method TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  provenance_note TEXT NOT NULL,
  review_status TEXT NOT NULL,
  rights_access_status TEXT NOT NULL,
  non_authorizing_scope_label TEXT NOT NULL,
  stores_scripture_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_scripture_text = 0),
  stores_transcription_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_transcription_text = 0),
  stores_boundary_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_boundary_text = 0)
);

CREATE TABLE evidence_source_trust_rule (
  trust_rule_id TEXT PRIMARY KEY,
  source_family TEXT NOT NULL REFERENCES scripture_source_family(source_family),
  applies_to_source_family TEXT NOT NULL,
  rule TEXT NOT NULL,
  failure_mode TEXT NOT NULL,
  required_action TEXT NOT NULL,
  source_url TEXT NOT NULL CHECK (source_url LIKE 'https://%'),
  method TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  provenance_note TEXT NOT NULL,
  review_status TEXT NOT NULL,
  rights_access_status TEXT NOT NULL,
  non_authorizing_scope_label TEXT NOT NULL,
  stores_scripture_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_scripture_text = 0),
  stores_transcription_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_transcription_text = 0),
  stores_boundary_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_boundary_text = 0)
);

CREATE TABLE evidence_catalog_review_queue (
  queue_id TEXT PRIMARY KEY,
  witness_group TEXT NOT NULL,
  source_family TEXT NOT NULL REFERENCES scripture_source_family(source_family),
  priority TEXT NOT NULL,
  blocker TEXT NOT NULL,
  required_reviewer TEXT NOT NULL,
  next_action TEXT NOT NULL,
  source_url TEXT NOT NULL CHECK (source_url LIKE 'https://%'),
  method TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
  provenance_note TEXT NOT NULL,
  review_status TEXT NOT NULL,
  rights_access_status TEXT NOT NULL,
  non_authorizing_scope_label TEXT NOT NULL,
  stores_scripture_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_scripture_text = 0),
  stores_transcription_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_transcription_text = 0),
  stores_boundary_text INTEGER NOT NULL DEFAULT 0 CHECK (stores_boundary_text = 0)
);
