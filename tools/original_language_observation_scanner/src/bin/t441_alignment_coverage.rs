use serde_json::{json, Value as JsonValue};
use serde_yaml::Value as YamlValue;
use std::collections::{BTreeMap, BTreeSet};
use std::env;
use std::fs::{self, File};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::{Path, PathBuf};

const SCHEMA_VERSION: &str = "t441_rust_alignment_coverage_index.v1";
const TASK_ID: &str = "T441";
const SCANNER: &str = "tools/original_language_observation_scanner/src/bin/t441_alignment_coverage.rs";
const SCANNER_VERSION: &str = "0.1.0";

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

#[derive(Debug)]
struct Args {
    t439_root: PathBuf,
    t436_root: PathBuf,
    t440_control: PathBuf,
    out: PathBuf,
    no_authority: bool,
    no_text: bool,
}

#[derive(Debug, Default)]
struct PhlmCoverage {
    refs: Vec<String>,
    source_tokens_by_ref: BTreeMap<String, usize>,
    alignment_rows: Vec<JsonValue>,
    editorial_layers: usize,
}

#[derive(Debug, Default, Clone)]
struct JonahSourceCoverage {
    source_id: String,
    verse_count: usize,
    token_count: usize,
    token_shape_count: usize,
    lemma_attr_count: usize,
    morph_attr_count: usize,
    strong_attr_count: usize,
    editorial_shape_count: usize,
    refs: BTreeSet<String>,
}

fn main() {
    if let Err(exc) = run() {
        eprintln!("t441_alignment_coverage failed: {exc}");
        std::process::exit(1);
    }
}

fn run() -> Result<()> {
    let args = parse_args()?;
    scan_alignment_coverage(&args)
}

fn parse_args() -> Result<Args> {
    let mut iter = env::args().skip(1);
    let mut t439_root = None;
    let mut t436_root = None;
    let mut t440_control = None;
    let mut out = None;
    let mut no_authority = false;
    let mut no_text = false;

    while let Some(flag) = iter.next() {
        match flag.as_str() {
            "--t439-root" => {
                t439_root = Some(PathBuf::from(
                    iter.next().ok_or("--t439-root requires a value")?,
                ))
            }
            "--t436-root" => {
                t436_root = Some(PathBuf::from(
                    iter.next().ok_or("--t436-root requires a value")?,
                ))
            }
            "--t440-control" => {
                t440_control = Some(PathBuf::from(
                    iter.next().ok_or("--t440-control requires a value")?,
                ))
            }
            "--out" => out = Some(PathBuf::from(iter.next().ok_or("--out requires a value")?)),
            "--no-authority" => no_authority = true,
            "--no-text" => no_text = true,
            other => return Err(format!("unknown argument {other:?}").into()),
        }
    }

    if !no_authority {
        return Err("--no-authority is required; T441 cannot authorize downstream truth".into());
    }
    if !no_text {
        return Err("--no-text is required; T441 ledgers must not emit biblical wording".into());
    }

    Ok(Args {
        t439_root: t439_root.ok_or("--t439-root is required")?,
        t436_root: t436_root.ok_or("--t436-root is required")?,
        t440_control: t440_control.ok_or("--t440-control is required")?,
        out: out.ok_or("--out is required")?,
        no_authority,
        no_text,
    })
}

fn scan_alignment_coverage(args: &Args) -> Result<()> {
    fs::create_dir_all(&args.out)?;

    let t439_manifest = read_yaml(&args.t439_root.join("manifest.yaml"))?;
    let t436_manifest = read_yaml(&args.t436_root.join("manifest.yaml"))?;
    let t436_parity = read_json(&args.t436_root.join("parity_summary.json"))?;
    let t440_control = read_yaml(&args.t440_control)?;

    let phlm = load_phlm_coverage(args)?;
    let jonah = load_jonah_coverage(args)?;
    validate_against_contracts(
        &phlm,
        &jonah,
        &t439_manifest,
        &t436_manifest,
        &t436_parity,
        &t440_control,
    )?;

    let mut source_ref_rows = Vec::new();
    source_ref_rows.push(phlm_source_ref_row(&phlm, &t439_manifest)?);
    for source in jonah.values() {
        source_ref_rows.push(jonah_source_ref_row(source, &t440_control)?);
    }

    let mut coverage_rows = phlm_alignment_rows(&phlm)?;
    coverage_rows.extend(jonah_coverage_rows(args)?);

    let guardrail_rows = semantic_guardrail_rows(&t440_control)?;
    let negative_summary = negative_fixture_summary(&t440_control)?;

    write_jsonl(&args.out.join("source_ref_coverage.jsonl"), &source_ref_rows)?;
    write_jsonl(&args.out.join("alignment_coverage_index.jsonl"), &coverage_rows)?;
    write_jsonl(&args.out.join("semantic_guardrail_index.jsonl"), &guardrail_rows)?;
    write_pretty_json(&args.out.join("negative_fixture_summary.json"), &negative_summary)?;
    write_manifest(
        args,
        &phlm,
        &jonah,
        &source_ref_rows,
        &coverage_rows,
        &guardrail_rows,
        &negative_summary,
    )?;

    println!(
        "T441 alignment coverage wrote {} source rows, {} coverage rows, {} guardrail rows to {}",
        source_ref_rows.len(),
        coverage_rows.len(),
        guardrail_rows.len(),
        normalize_path(&args.out)
    );
    Ok(())
}

fn load_phlm_coverage(args: &Args) -> Result<PhlmCoverage> {
    let manifest = read_yaml(&args.t439_root.join("manifest.yaml"))?;
    let refs = string_sequence(&manifest, "exact_refs")?;
    let token_rows = read_jsonl(&args.t439_root.join("source_language_tokens.jsonl"))?;
    let editorial_rows = read_jsonl(&args.t439_root.join("editorial_layers.jsonl"))?;
    let alignment_rows = read_jsonl(&args.t439_root.join("alignment_records.jsonl"))?;
    let mut coverage = PhlmCoverage {
        refs,
        alignment_rows,
        editorial_layers: editorial_rows.len(),
        ..PhlmCoverage::default()
    };
    for (index, row) in token_rows.iter().enumerate() {
        reject_text_leak(row, &format!("t439 source token row {}", index + 1))?;
        require_authority_false(row, "t439 source token")?;
        if row.get("source_id").and_then(JsonValue::as_str) != Some("sblgnt") {
            return Err("T439 source token rows must remain SBLGNT".into());
        }
        if row.get("strong_id").is_some_and(|value| !value.is_null())
            || row.get("lemma").is_some_and(|value| !value.is_null())
            || row.get("morphology").is_some_and(|value| !value.is_null())
        {
            return Err("T439 source token rows must not populate Strong's, lemma, or morphology".into());
        }
        let osis_ref = string_field_json(row, "osis_ref")?;
        *coverage.source_tokens_by_ref.entry(osis_ref).or_insert(0) += 1;
    }
    for (index, row) in editorial_rows.iter().enumerate() {
        reject_text_leak(row, &format!("t439 editorial row {}", index + 1))?;
        require_authority_false(row, "t439 editorial")?;
    }
    for (index, row) in coverage.alignment_rows.iter().enumerate() {
        reject_text_leak(row, &format!("t439 alignment row {}", index + 1))?;
        require_authority_false(row, "t439 alignment")?;
        if row.get("confidence").and_then(JsonValue::as_str) != Some("low")
            || row.get("review_status").and_then(JsonValue::as_str) != Some("unreviewed")
        {
            return Err("T439 alignment rows must remain low-confidence and unreviewed".into());
        }
    }
    Ok(coverage)
}

fn load_jonah_coverage(args: &Args) -> Result<BTreeMap<String, JonahSourceCoverage>> {
    let verse_rows = read_jsonl(&args.t436_root.join("verse_token_observations.jsonl"))?;
    let token_rows = read_jsonl(&args.t436_root.join("token_shape_index.jsonl"))?;
    let editorial_rows = read_jsonl(&args.t436_root.join("editorial_metadata_shape_index.jsonl"))?;
    let mut by_source: BTreeMap<String, JonahSourceCoverage> = BTreeMap::new();

    for (index, row) in verse_rows.iter().enumerate() {
        reject_text_leak(row, &format!("t436 verse row {}", index + 1))?;
        require_authority_false(row, "t436 verse")?;
        let source_id = string_field_json(row, "source_id")?;
        let osis_ref = string_field_json(row, "osis_ref")?;
        let token_count = usize_field_json(row, "token_count")?;
        let entry = by_source
            .entry(source_id.clone())
            .or_insert_with(|| JonahSourceCoverage {
                source_id,
                ..JonahSourceCoverage::default()
            });
        entry.verse_count += 1;
        entry.token_count += token_count;
        entry.refs.insert(osis_ref);
    }

    for (index, row) in token_rows.iter().enumerate() {
        reject_text_leak(row, &format!("t436 token row {}", index + 1))?;
        require_authority_false(row, "t436 token")?;
        reject_metadata_value_hashes(row)?;
        let source_id = string_field_json(row, "source_id")?;
        let entry = by_source
            .get_mut(&source_id)
            .ok_or_else(|| format!("T436 token row references source without verse rows: {source_id}"))?;
        entry.token_shape_count += 1;
        if row.get("has_lemma_attr").and_then(JsonValue::as_bool) == Some(true) {
            entry.lemma_attr_count += 1;
        }
        if row.get("has_morph_attr").and_then(JsonValue::as_bool) == Some(true) {
            entry.morph_attr_count += 1;
        }
        if row.get("has_strong_attr").and_then(JsonValue::as_bool) == Some(true) {
            entry.strong_attr_count += 1;
        }
        for key in [
            "stores_source_text",
            "stores_lemma_value",
            "stores_morphology_value",
            "stores_strongs_value",
        ] {
            if row.get(key).and_then(JsonValue::as_bool) != Some(false) {
                return Err(format!("T436 token row must keep {key}=false").into());
            }
        }
    }

    for (index, row) in editorial_rows.iter().enumerate() {
        reject_text_leak(row, &format!("t436 editorial metadata row {}", index + 1))?;
        require_authority_false(row, "t436 editorial metadata")?;
        let source_id = string_field_json(row, "source_id")?;
        let entry = by_source
            .get_mut(&source_id)
            .ok_or_else(|| format!("T436 editorial row references source without verse rows: {source_id}"))?;
        entry.editorial_shape_count += 1;
    }
    Ok(by_source)
}

#[allow(clippy::too_many_arguments)]
fn validate_against_contracts(
    phlm: &PhlmCoverage,
    jonah: &BTreeMap<String, JonahSourceCoverage>,
    t439_manifest: &YamlValue,
    t436_manifest: &YamlValue,
    t436_parity: &JsonValue,
    t440_control: &YamlValue,
) -> Result<()> {
    let counts = t439_manifest
        .get("counts")
        .ok_or("T439 manifest counts missing")?;
    if usize_field_path(counts, &["source_language_tokens"])? != 334
        || usize_field_path(counts, &["editorial_layers"])? != 98
        || usize_field_path(counts, &["alignment_records"])? != 25
        || phlm.source_tokens_by_ref.values().sum::<usize>() != 334
        || phlm.editorial_layers != 98
        || phlm.alignment_rows.len() != 25
        || phlm.refs.len() != 25
    {
        return Err("T439 Philemon coverage/count contract drifted".into());
    }
    let t436_counts = t436_manifest
        .get("counts")
        .ok_or("T436 manifest counts missing")?;
    if usize_field_path(t436_counts, &["verse_token_observations"])? != 96
        || usize_field_path(t436_counts, &["token_shape_index"])? != 1376
        || usize_field_path(t436_counts, &["editorial_metadata_shape_index"])? != 20
    {
        return Err("T436 generated count contract drifted".into());
    }
    if t436_parity.get("refs_match").and_then(JsonValue::as_bool) != Some(true)
        || t436_parity
            .get("per_verse_token_counts_match")
            .and_then(JsonValue::as_bool)
            != Some(true)
        || t436_parity
            .get("exact_token_hashes_all_match")
            .and_then(JsonValue::as_bool)
            != Some(false)
    {
        return Err("T436 parity summary contract drifted".into());
    }
    for source_id in ["openscriptures_oshb", "tanach_us_uxlc"] {
        let source = jonah
            .get(source_id)
            .ok_or_else(|| format!("missing Jonah source coverage for {source_id}"))?;
        if source.verse_count != 48 || source.token_count != 688 || source.token_shape_count != 688 {
            return Err(format!("Jonah {source_id} verse/token counts drifted").into());
        }
    }
    let oshb = jonah
        .get("openscriptures_oshb")
        .ok_or("missing OSHB Jonah coverage")?;
    if oshb.lemma_attr_count != 688 || oshb.morph_attr_count != 688 || oshb.strong_attr_count != 0 {
        return Err("OSHB lemma/morph/Strong attribute count semantics drifted".into());
    }
    let uxlc = jonah
        .get("tanach_us_uxlc")
        .ok_or("missing UXLC Jonah coverage")?;
    if uxlc.lemma_attr_count != 0 || uxlc.morph_attr_count != 0 || uxlc.strong_attr_count != 0 {
        return Err("UXLC must remain no-lemma/no-morph/no-Strong baseline".into());
    }
    if t440_control
        .get("rust_policy")
        .and_then(|rust| rust.get("t441_may_design_no_text_rust_checker_after_t440"))
        .and_then(YamlValue::as_bool)
        != Some(true)
    {
        return Err("T440 must explicitly allow separate T441 no-text Rust checker design".into());
    }
    Ok(())
}

fn phlm_source_ref_row(phlm: &PhlmCoverage, manifest: &YamlValue) -> Result<JsonValue> {
    Ok(json!({
        "id": "t441:source-ref-coverage:sblgnt:Phlm",
        "type": "T441SourceRefCoverage",
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "source_id": "sblgnt",
        "language": "greek",
        "book_id": "Phlm",
        "span": "Phlm.1.1-Phlm.1.25",
        "input_task_id": "T439",
        "coverage_kind": "full_book_philemon_candidate_bridge_coverage",
        "ref_count": phlm.refs.len(),
        "source_token_count": phlm.source_tokens_by_ref.values().sum::<usize>(),
        "alignment_record_count": phlm.alignment_rows.len(),
        "editorial_layer_count": phlm.editorial_layers,
        "source_view_path": string_field(manifest, "source_view_path")?,
        "source_file_sha256": string_field(manifest, "source_file_sha256")?,
        "stores_source_text": false,
        "stores_translation_text": false,
        "evidence_mode": "coverage_index_from_no_text_candidate_rows",
        "inferred_vs_observed": "observed_count_rollup",
        "trust_zone": "candidate",
        "status": "coverage_shadow",
        "text_storage_policy": no_text_policy(),
        "authority": authority(),
        "non_authorizations": non_authorizations()
    }))
}

fn jonah_source_ref_row(source: &JonahSourceCoverage, t440_control: &YamlValue) -> Result<JsonValue> {
    let contract = parser_contract(t440_control, &source.source_id)?;
    Ok(json!({
        "id": format!("t441:source-ref-coverage:{}:Jonah", source.source_id),
        "type": "T441SourceRefCoverage",
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "source_id": source.source_id,
        "language": "hebrew",
        "book_id": "Jonah",
        "span": "Jonah.1.1-Jonah.4.11",
        "input_task_id": "T436/T440",
        "coverage_kind": "jonah_source_specific_parser_contract_coverage",
        "ref_count": source.refs.len(),
        "verse_observation_count": source.verse_count,
        "source_token_count": source.token_count,
        "token_shape_count": source.token_shape_count,
        "editorial_metadata_shape_count": source.editorial_shape_count,
        "lemma_attr_count": source.lemma_attr_count,
        "morph_attr_count": source.morph_attr_count,
        "strong_attr_count": source.strong_attr_count,
        "source_view_path": string_field(contract, "source_view_path")?,
        "source_view_sha256": string_field(contract, "source_view_sha256")?,
        "count_parity_is_semantic_authority": false,
        "evidence_mode": "coverage_index_from_no_text_candidate_rows",
        "inferred_vs_observed": "observed_count_rollup",
        "trust_zone": "candidate",
        "status": "coverage_shadow",
        "text_storage_policy": no_text_policy(),
        "authority": authority(),
        "non_authorizations": non_authorizations()
    }))
}

fn phlm_alignment_rows(phlm: &PhlmCoverage) -> Result<Vec<JsonValue>> {
    let mut rows = Vec::new();
    for row in &phlm.alignment_rows {
        let osis_ref = string_field_json(row, "osis_ref")?;
        let source = row
            .get("source")
            .and_then(JsonValue::as_object)
            .ok_or("T439 alignment source object missing")?;
        let source_ids = source
            .get("source_token_ids")
            .and_then(JsonValue::as_array)
            .ok_or("T439 alignment source_token_ids missing")?;
        let translation_ids = row
            .get("translation_token_ids")
            .and_then(JsonValue::as_array)
            .ok_or("T439 alignment translation_token_ids missing")?;
        let strong_hints = row
            .get("translation_side_strong_hints")
            .and_then(JsonValue::as_array)
            .map_or(0, Vec::len);
        rows.push(json!({
            "id": format!("t441:alignment-coverage:sblgnt-eng-web:{osis_ref}"),
            "type": "T441AlignmentCoverageObservation",
            "schema_version": SCHEMA_VERSION,
            "task_id": TASK_ID,
            "input_task_id": "T439",
            "coverage_kind": "verse_level_many_to_many_bridge_coverage",
            "book_id": "Phlm",
            "osis_ref": osis_ref,
            "source_id": "sblgnt",
            "source_language": "greek",
            "translation_id": row.get("translation_id").and_then(JsonValue::as_str).unwrap_or("eng-web"),
            "source_token_id_count": source_ids.len(),
            "translation_token_id_count": translation_ids.len(),
            "translation_side_strong_hint_count": strong_hints,
            "translation_side_strong_hints_are_source_text": false,
            "alignment_basis": row.get("alignment_basis").cloned().unwrap_or(json!("source_token_order")),
            "alignment_type": row.get("alignment_type").cloned().unwrap_or(json!("many_to_many")),
            "confidence": row.get("confidence").cloned().unwrap_or(json!("low")),
            "review_status": row.get("review_status").cloned().unwrap_or(json!("unreviewed")),
            "word_level_alignment_truth": false,
            "translation_judgment": false,
            "evidence_mode": "coverage_index_from_t439_candidate_bridge",
            "inferred_vs_observed": "observed_count_rollup",
            "trust_zone": "candidate",
            "status": "coverage_shadow",
            "text_storage_policy": no_text_policy(),
            "authority": authority(),
            "non_authorizations": non_authorizations()
        }));
    }
    Ok(rows)
}

fn jonah_coverage_rows(args: &Args) -> Result<Vec<JsonValue>> {
    let verse_rows = read_jsonl(&args.t436_root.join("verse_token_observations.jsonl"))?;
    let mut rows = Vec::new();
    for row in verse_rows {
        let source_id = string_field_json(&row, "source_id")?;
        let osis_ref = string_field_json(&row, "osis_ref")?;
        let token_count = usize_field_json(&row, "token_count")?;
        rows.push(json!({
            "id": format!("t441:alignment-coverage:{}:{osis_ref}", source_id),
            "type": "T441AlignmentCoverageObservation",
            "schema_version": SCHEMA_VERSION,
            "task_id": TASK_ID,
            "input_task_id": "T436/T440",
            "coverage_kind": "source_view_ref_token_count_coverage",
            "book_id": "Jonah",
            "osis_ref": osis_ref,
            "source_id": source_id,
            "source_language": "hebrew",
            "source_token_id_count": token_count,
            "token_hash_chain_sha256": string_field_json(&row, "token_hash_chain_sha256")?,
            "count_parity_is_semantic_authority": false,
            "word_level_alignment_truth": false,
            "translation_judgment": false,
            "preferred_source_tradition": false,
            "evidence_mode": "coverage_index_from_t436_t440_no_text_rows",
            "inferred_vs_observed": "observed_count_rollup",
            "trust_zone": "candidate",
            "status": "coverage_shadow",
            "text_storage_policy": no_text_policy(),
            "authority": authority(),
            "non_authorizations": non_authorizations()
        }));
    }
    Ok(rows)
}

fn semantic_guardrail_rows(t440_control: &YamlValue) -> Result<Vec<JsonValue>> {
    let mut rows = vec![
        guardrail("no_visible_biblical_text", "T441 stores refs, IDs, counts, hashes, checksums, and policy labels only; no Greek, Hebrew, or English wording is emitted."),
        guardrail("generated_build_outputs_only", "T441 Rust outputs stay under build/original_language_observation and are not committed source rows."),
        guardrail("python_authority_validator", "Rust emits deterministic coverage ledgers; Python validates governance, source semantics, and non-authority constraints."),
        guardrail("t439_bridge_low_confidence", "Philemon bridge rows remain verse-level, many-to-many, low-confidence, unreviewed coverage evidence only."),
        guardrail("count_parity_not_semantic_parity", "UXLC/OSHB matching refs and token counts do not create word-level alignment truth, source-language truth, translation judgment, or theology authority."),
        guardrail("oshb_lemma_lookup_hint_only", "OSHB w@lemma remains Strong lookup-hint metadata only, not local lemma, strong_id, lexical truth, or theology authority."),
        guardrail("oshb_morph_metadata_only", "OSHB w@morph remains source morphology metadata only, not local morphology-row population or doctrine."),
        guardrail("no_production_roots_opened", "T441 does not open source_tokens, strong_alignment, lemma_morphology, textual_variants, witness_support, or editorial_layers production roots."),
    ];
    let negative_count = negative_fixture_ids(t440_control)?.len();
    rows.push(guardrail(
        "t440_negative_fixtures_carried_forward",
        &format!("T441 generated validation must enforce all {negative_count} T440 negative fixture requirements."),
    ));
    Ok(rows)
}

fn guardrail(guardrail_id: &str, summary: &str) -> JsonValue {
    json!({
        "id": format!("t441:semantic-guardrail:{guardrail_id}"),
        "type": "T441SemanticGuardrail",
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "guardrail_id": guardrail_id,
        "summary": summary,
        "evidence_mode": "policy_guardrail",
        "trust_zone": "candidate",
        "status": "coverage_shadow",
        "text_storage_policy": no_text_policy(),
        "authority": authority(),
        "non_authorizations": non_authorizations()
    })
}

fn negative_fixture_summary(t440_control: &YamlValue) -> Result<JsonValue> {
    let ids = negative_fixture_ids(t440_control)?;
    Ok(json!({
        "object_type": "t441_negative_fixture_summary",
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "source_task_id": "T440",
        "negative_fixture_ids": ids,
        "negative_fixture_count": ids.len(),
        "status": "carried_forward",
        "note": "This summary carries T440 negative fixture requirements into the T441 generated validation contract. It is not output, gold, or source-language authority.",
        "text_storage_policy": no_text_policy(),
        "authority": authority(),
        "non_authorizations": non_authorizations()
    }))
}

fn write_manifest(
    args: &Args,
    phlm: &PhlmCoverage,
    jonah: &BTreeMap<String, JonahSourceCoverage>,
    source_ref_rows: &[JsonValue],
    coverage_rows: &[JsonValue],
    guardrail_rows: &[JsonValue],
    negative_summary: &JsonValue,
) -> Result<()> {
    let output_files = vec![
        "coverage_manifest.json",
        "source_ref_coverage.jsonl",
        "alignment_coverage_index.jsonl",
        "semantic_guardrail_index.jsonl",
        "negative_fixture_summary.json",
    ];
    let jonah_token_count: usize = jonah.values().map(|source| source.token_count).sum();
    let manifest = json!({
        "object_type": "t441_rust_alignment_coverage_manifest",
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "scanner": SCANNER,
        "scanner_version": SCANNER_VERSION,
        "command": "t441_alignment_coverage",
        "inputs": {
            "t439_root": normalize_path(&args.t439_root),
            "t436_root": normalize_path(&args.t436_root),
            "t440_control": normalize_path(&args.t440_control)
        },
        "no_authority": args.no_authority,
        "no_text": args.no_text,
        "coverage_scope": {
            "philemon_refs": phlm.refs.len(),
            "philemon_source_tokens": phlm.source_tokens_by_ref.values().sum::<usize>(),
            "philemon_alignment_records": phlm.alignment_rows.len(),
            "philemon_editorial_layers": phlm.editorial_layers,
            "jonah_sources": jonah.keys().cloned().collect::<Vec<_>>(),
            "jonah_refs_per_source": 48,
            "jonah_tokens_all_sources": jonah_token_count,
            "count_parity_is_semantic_authority": false
        },
        "row_counts": {
            "source_ref_coverage": source_ref_rows.len(),
            "alignment_coverage_index": coverage_rows.len(),
            "semantic_guardrail_index": guardrail_rows.len(),
            "negative_fixture_summary": negative_summary.get("negative_fixture_count").and_then(JsonValue::as_u64).unwrap_or(0)
        },
        "output_files": output_files,
        "generated_outputs_committed": false,
        "evidence_mode": "deterministic_no_text_coverage_index",
        "trust_zone": "candidate",
        "status": "coverage_shadow",
        "text_storage_policy": no_text_policy(),
        "authority": authority(),
        "non_authorizations": non_authorizations()
    });
    write_pretty_json(&args.out.join("coverage_manifest.json"), &manifest)
}

fn parser_contract<'a>(control: &'a YamlValue, source_id: &str) -> Result<&'a YamlValue> {
    let contracts = control
        .get("parser_contracts")
        .and_then(YamlValue::as_sequence)
        .ok_or("T440 parser_contracts missing")?;
    for contract in contracts {
        if contract.get("source_id").and_then(YamlValue::as_str) == Some(source_id) {
            return Ok(contract);
        }
    }
    Err(format!("T440 parser contract missing {source_id}").into())
}

fn negative_fixture_ids(control: &YamlValue) -> Result<Vec<String>> {
    let rows = control
        .get("negative_fixture_requirements")
        .and_then(YamlValue::as_sequence)
        .ok_or("T440 negative_fixture_requirements missing")?;
    let mut ids = Vec::new();
    for row in rows {
        ids.push(string_field(row, "id")?);
    }
    Ok(ids)
}

fn read_yaml(path: &Path) -> Result<YamlValue> {
    let text = fs::read_to_string(path)?;
    Ok(serde_yaml::from_str(&text)?)
}

fn read_json(path: &Path) -> Result<JsonValue> {
    let text = fs::read_to_string(path)?;
    Ok(serde_json::from_str(&text)?)
}

fn read_jsonl(path: &Path) -> Result<Vec<JsonValue>> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let mut rows = Vec::new();
    for line in reader.lines() {
        let line = line?;
        if line.trim().is_empty() {
            continue;
        }
        rows.push(serde_json::from_str(&line)?);
    }
    Ok(rows)
}

fn write_jsonl(path: &Path, rows: &[JsonValue]) -> Result<()> {
    let file = File::create(path)?;
    let mut writer = BufWriter::new(file);
    for row in rows {
        writeln!(writer, "{}", serde_json::to_string(row)?)?;
    }
    Ok(())
}

fn write_pretty_json(path: &Path, payload: &JsonValue) -> Result<()> {
    fs::write(path, serde_json::to_string_pretty(payload)? + "\n")?;
    Ok(())
}

fn string_field(value: &YamlValue, key: &str) -> Result<String> {
    value
        .get(key)
        .and_then(YamlValue::as_str)
        .map(ToString::to_string)
        .ok_or_else(|| format!("YAML field {key:?} must be a string").into())
}

fn string_field_json(value: &JsonValue, key: &str) -> Result<String> {
    value
        .get(key)
        .and_then(JsonValue::as_str)
        .map(ToString::to_string)
        .ok_or_else(|| format!("JSON field {key:?} must be a string").into())
}

fn usize_field_json(value: &JsonValue, key: &str) -> Result<usize> {
    value
        .get(key)
        .and_then(JsonValue::as_u64)
        .and_then(|item| usize::try_from(item).ok())
        .ok_or_else(|| format!("JSON field {key:?} must be a non-negative integer").into())
}

fn usize_field_path(value: &YamlValue, keys: &[&str]) -> Result<usize> {
    let mut current = value;
    for key in keys {
        current = current
            .get(*key)
            .ok_or_else(|| format!("missing YAML field path {}", keys.join(".")))?;
    }
    current
        .as_i64()
        .and_then(|item| usize::try_from(item).ok())
        .ok_or_else(|| {
            format!(
                "YAML field path {} must be a non-negative integer",
                keys.join(".")
            )
            .into()
        })
}

fn string_sequence(value: &YamlValue, key: &str) -> Result<Vec<String>> {
    let seq = value
        .get(key)
        .and_then(YamlValue::as_sequence)
        .ok_or_else(|| format!("manifest field {key:?} must be a sequence"))?;
    let mut result = Vec::new();
    for item in seq {
        result.push(
            item.as_str()
                .ok_or_else(|| format!("manifest field {key:?} contains a non-string item"))?
                .to_string(),
        );
    }
    Ok(result)
}

fn reject_text_leak(row: &JsonValue, label: &str) -> Result<()> {
    const FORBIDDEN_KEYS: &[&str] = &[
        "surface_text",
        "normalized_text",
        "source_text",
        "translation_text",
        "visible_text",
        "full_text",
        "manuscript_text",
        "manuscript_transcription",
        "lemma_value_hash",
        "morph_value_hash",
        "morphology_value_hash",
        "strong_value_hash",
        "strongs_value_hash",
    ];
    match row {
        JsonValue::Object(map) => {
            for (key, value) in map {
                if FORBIDDEN_KEYS.contains(&key.as_str()) {
                    return Err(format!("{label}: forbidden text/metadata key {key}").into());
                }
                if let JsonValue::String(text) = value {
                    if contains_biblical_script(text) {
                        return Err(format!("{label}: visible Greek/Hebrew text leaked in {key}").into());
                    }
                }
                reject_text_leak(value, label)?;
            }
        }
        JsonValue::Array(items) => {
            for item in items {
                reject_text_leak(item, label)?;
            }
        }
        JsonValue::String(text) if contains_biblical_script(text) => {
            return Err(format!("{label}: visible Greek/Hebrew text leaked").into());
        }
        _ => {}
    }
    Ok(())
}

fn reject_metadata_value_hashes(row: &JsonValue) -> Result<()> {
    if let JsonValue::Object(map) = row {
        for key in map.keys() {
            if matches!(
                key.as_str(),
                "lemma_value_hash"
                    | "morph_value_hash"
                    | "morphology_value_hash"
                    | "strong_value_hash"
                    | "strongs_value_hash"
            ) {
                return Err(format!("forbidden metadata-value authority key {key}").into());
            }
        }
    }
    Ok(())
}

fn require_authority_false(row: &JsonValue, label: &str) -> Result<()> {
    let authority = row
        .get("authority")
        .and_then(JsonValue::as_object)
        .ok_or_else(|| format!("{label}: authority mapping missing"))?;
    for (key, value) in authority {
        if key.starts_with("authorizes_")
            || key.starts_with("creates_")
            || key.starts_with("changes_")
            || key.starts_with("runs_")
            || key.starts_with("selects_")
            || key.starts_with("opens_")
        {
            if value != &JsonValue::Bool(false) {
                return Err(format!("{label}: authority.{key} must be false").into());
            }
        }
    }
    Ok(())
}

fn contains_biblical_script(value: &str) -> bool {
    value.chars().any(|ch| {
        ('\u{0370}'..='\u{03ff}').contains(&ch)
            || ('\u{1f00}'..='\u{1fff}').contains(&ch)
            || ('\u{0590}'..='\u{05ff}').contains(&ch)
    })
}

fn normalize_path(path: &Path) -> String {
    path.to_string_lossy().replace('\\', "/")
}

fn no_text_policy() -> JsonValue {
    json!({
        "stores_source_text": false,
        "stores_translation_text": false,
        "stores_manuscript_transcription": false,
        "stores_manuscript_image": false,
        "stores_metadata_values": false,
        "no_text": true,
        "storage_note": "T441 stores only refs, IDs/counts, hashes, checksums, and policy labels; no biblical wording or metadata values are emitted."
    })
}

fn authority() -> JsonValue {
    json!({
        "authorizes_source_language_truth": false,
        "authorizes_lexical_truth": false,
        "authorizes_word_level_alignment_truth": false,
        "authorizes_strongs_as_source_text": false,
        "authorizes_lemma_or_morphology_population": false,
        "authorizes_preferred_reading": false,
        "authorizes_source_tradition_preference": false,
        "authorizes_textual_critical_decision": false,
        "authorizes_manuscript_witness_support": false,
        "authorizes_canon_scope_change": false,
        "authorizes_translation_judgment": false,
        "authorizes_chunk_boundary": false,
        "authorizes_reviewed_gold": false,
        "authorizes_chunk_output": false,
        "authorizes_route_behavior": false,
        "authorizes_evaluator_behavior": false,
        "authorizes_graph_or_retrieval_truth": false,
        "authorizes_embeddings_or_indexes": false,
        "authorizes_theology_authority": false
    })
}

fn non_authorizations() -> Vec<&'static str> {
    vec![
        "source_language_truth",
        "lexical_truth",
        "word_level_alignment_truth",
        "strongs_number_as_source_text",
        "strongs_overlay_population",
        "lemma_or_morphology_population",
        "preferred_reading",
        "source_tradition_preference",
        "textual_critical_decision",
        "manuscript_witness_support",
        "translation_faithfulness_judgment",
        "chunk_boundary",
        "reviewed_gold",
        "chunk_output",
        "graph_or_retrieval_truth",
        "theology_authority",
    ]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rejects_biblical_script_in_generated_rows() {
        let row = json!({"note": "logos"});
        assert!(reject_text_leak(&row, "row").is_ok());
        let leaked = json!({"note": "\u{05d9}\u{05d5}\u{05e0}\u{05d4}"});
        assert!(reject_text_leak(&leaked, "row").is_err());
    }

    #[test]
    fn rejects_metadata_value_hash_key() {
        let row = json!({"lemma_value_hash": "abc"});
        assert!(reject_text_leak(&row, "row").is_err());
    }

    #[test]
    fn authority_flags_must_be_false() {
        let row = json!({"authority": {"authorizes_translation_judgment": true}});
        assert!(require_authority_false(&row, "row").is_err());
    }

    #[test]
    fn guardrail_rows_are_no_text_and_non_authorizing() {
        let row = guardrail("test", "ASCII-only no-text guardrail.");
        assert_eq!(row["task_id"], "T441");
        assert_eq!(row["text_storage_policy"]["stores_source_text"], false);
        assert_eq!(row["authority"]["authorizes_source_language_truth"], false);
        reject_text_leak(&row, "guardrail").expect("guardrail is no-text");
    }
}
