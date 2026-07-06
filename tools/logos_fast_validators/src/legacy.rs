use serde_json::{json, Map, Value as JsonValue};
use serde_yaml::Value as YamlValue;
use std::collections::{BTreeMap, BTreeSet, HashSet};
use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader, Write};
use std::path::{Path, PathBuf};

pub(crate) type AnyResult<T> = Result<T, Box<dyn Error>>;

const REQUIRED_EXCLUDED: &[&str] = &[
    "FRT", "GLO", "Tob", "Jdt", "AddEsth", "Wis", "Sir", "Bar", "1Macc", "2Macc", "1Esd", "PrMan",
    "Ps151", "3Macc", "2Esd", "4Macc", "AddDan",
];
const PASSAGES_REL: &str = "scripture/passages/passages.jsonl";
const WITNESSES_REL: &str = "translations/eng-web/translation_witnesses.jsonl";
const GLOSSARY_REL: &str = "translations/eng-web/glossary_entries.jsonl";
const WORD_TOKENS_REL: &str = "translations/eng-web/word_tokens.jsonl";
const SIDECAR_RELS: &[&str] = &[
    "translations/eng-web/boundary_claims.jsonl",
    "translations/eng-web/footnotes.jsonl",
    "translations/eng-web/editorial_cross_references.jsonl",
    "translations/eng-web/section_headings.jsonl",
];
const KNOWN_EMPTY_WITNESS_REFS: &[&str] = &[
    "Luke.17.36",
    "Acts.8.37",
    "Acts.15.34",
    "Acts.24.7",
    "Rom.16.25",
];
const NON_SCRIPTURE_GLOSSARY_SCOPES: &[&str] = &[
    "non_scripture",
    "non_scripture_support",
    "supporting_reference",
    "source_metadata",
];

pub(crate) fn jsonl_scan(args: &[String]) -> AnyResult<()> {
    let mut translation_id = "eng-web".to_string();
    let mut require_canon = false;
    let mut summary_json: Option<PathBuf> = None;
    let mut paths: Vec<PathBuf> = Vec::new();
    let mut index = 0;

    while index < args.len() {
        match args[index].as_str() {
            "--translation-id" => {
                index += 1;
                translation_id = args
                    .get(index)
                    .ok_or("--translation-id requires a value")?
                    .to_string();
            }
            "--require-canon" => require_canon = true,
            "--summary-json" => {
                index += 1;
                summary_json = Some(PathBuf::from(
                    args.get(index).ok_or("--summary-json requires a value")?,
                ));
            }
            value if value.starts_with('-') => {
                return Err(format!("unknown jsonl-scan flag: {value}").into())
            }
            value => paths.push(PathBuf::from(value)),
        }
        index += 1;
    }

    if paths.is_empty() {
        return Err("jsonl-scan requires at least one JSONL path".into());
    }

    let mut failures: Vec<String> = Vec::new();
    let mut ids: BTreeSet<String> = BTreeSet::new();
    let mut passages: BTreeSet<String> = BTreeSet::new();
    let mut witnesses: Vec<(String, String)> = Vec::new();
    let mut record_count = 0usize;

    for path in &paths {
        if !path.exists() {
            failures.push(format!("Missing JSONL file: {}", path.display()));
            continue;
        }
        let file = File::open(path)?;
        let reader = BufReader::new(file);
        for (line_no, line_result) in reader.lines().enumerate() {
            let line_no = line_no + 1;
            let line = line_result?;
            if line.trim().is_empty() {
                continue;
            }
            let record: JsonValue = match serde_json::from_str(&line) {
                Ok(value) => value,
                Err(err) => {
                    failures.push(format!("{}:{line_no}: invalid JSON: {err}", path.display()));
                    continue;
                }
            };
            let Some(record) = record.as_object() else {
                failures.push(format!(
                    "{}:{line_no}: JSONL row is not an object",
                    path.display()
                ));
                continue;
            };
            record_count += 1;
            validate_jsonl_record(
                path,
                line_no,
                record,
                &translation_id,
                require_canon,
                &mut failures,
                &mut ids,
                &mut passages,
                &mut witnesses,
            );
        }
    }

    for (witness_id, passage_id) in &witnesses {
        if !passages.contains(passage_id) {
            failures.push(format!(
                "{witness_id}: points to missing ScripturePassage {passage_id}"
            ));
        }
    }

    let summary = json!({
        "validator": "logos_fast_validators jsonl-scan",
        "status": if failures.is_empty() { "passed" } else { "failed" },
        "files": paths.len(),
        "records": record_count,
        "unique_ids": ids.len(),
        "passages": passages.len(),
        "witnesses": witnesses.len(),
        "failures": failures.len(),
        "translation_id": translation_id,
        "require_canon": require_canon,
    });
    emit_summary(summary_json.as_deref(), &summary)?;

    if !failures.is_empty() {
        println!("FAST JSONL VALIDATION FAILED");
        for failure in failures.iter().take(200) {
            println!("- {failure}");
        }
        if failures.len() > 200 {
            println!("- ... {} additional failures", failures.len() - 200);
        }
        return Err(format!("{} JSONL validation failure(s)", failures.len()).into());
    }

    println!("Fast JSONL validation passed for {record_count} records.");
    Ok(())
}

#[allow(clippy::too_many_arguments)]
fn validate_jsonl_record(
    path: &Path,
    line_no: usize,
    record: &Map<String, JsonValue>,
    expected_translation: &str,
    require_canon: bool,
    failures: &mut Vec<String>,
    ids: &mut BTreeSet<String>,
    passages: &mut BTreeSet<String>,
    witnesses: &mut Vec<(String, String)>,
) {
    let rid = str_field(record, "id");
    match rid {
        Some(id) if !id.is_empty() => {
            if !ids.insert(id.to_string()) {
                failures.push(format!("{}:{line_no}: duplicate id {id}", path.display()));
            }
        }
        _ => failures.push(format!("{}:{line_no}: missing id", path.display())),
    }

    for key in ["source_sha256", "license"] {
        if str_field(record, key).is_none_or(str::is_empty) {
            failures.push(format!("{}:{line_no}: missing {key}", path.display()));
        }
    }

    if let Some(osis_ref) = str_field(record, "osis_ref") {
        if !valid_osis_ref(osis_ref) {
            failures.push(format!(
                "{}:{line_no}: malformed OSIS reference {osis_ref}",
                path.display()
            ));
        }
    }

    let record_type = str_field(record, "type");
    if record_type == Some("ScripturePassage") {
        if let Some(id) = rid {
            passages.insert(id.to_string());
        }
        if require_canon && !json_truthy(record.get("canon_profiles")) {
            failures.push(format!(
                "{}:{line_no}: ScripturePassage {} missing canon_profiles (CANON-1)",
                path.display(),
                rid.unwrap_or("<missing-id>")
            ));
        }
    }

    if record_type == Some("TranslationWitness") {
        if contains_usfm_marker(str_field(record, "text").unwrap_or("")) {
            failures.push(format!(
                "{}:{line_no}: TranslationWitness.text contains raw USFM marker",
                path.display()
            ));
        }
        if str_field(record, "translation_id") != Some(expected_translation) {
            failures.push(format!(
                "{}:{line_no}: unexpected translation_id {}",
                path.display(),
                str_field(record, "translation_id").unwrap_or("null")
            ));
        }
        witnesses.push((
            rid.unwrap_or("null").to_string(),
            str_field(record, "passage_id")
                .unwrap_or("null")
                .to_string(),
        ));
    }

    if json_truthy(record.get("translation_id")) {
        match str_field(record, "translation_id") {
            Some(actual) if actual == expected_translation => {}
            Some(actual) => failures.push(format!(
                "{}:{line_no}: generated output translation_id {actual} != expected {expected_translation}",
                path.display()
            )),
            None => failures.push(format!(
                "{}:{line_no}: generated output translation_id {} != expected {expected_translation}",
                path.display(),
                field_for_message(record, "translation_id")
            )),
        }
    }

    if json_truthy(record.get("relation_type")) {
        match str_field(record, "relation_type") {
            Some("editorial_cross_reference") => {}
            Some(relation_type) => failures.push(format!(
                "{}:{line_no}: disallowed relation_type {relation_type}",
                path.display()
            )),
            None => failures.push(format!(
                "{}:{line_no}: disallowed relation_type {}",
                path.display(),
                field_for_message(record, "relation_type")
            )),
        }
    }
}

fn field_for_message(record: &Map<String, JsonValue>, key: &str) -> String {
    match record.get(key) {
        None | Some(JsonValue::Null) => "null".to_string(),
        Some(JsonValue::String(value)) => value.clone(),
        Some(value) => value.to_string(),
    }
}

pub(crate) fn canonical_scope(args: &[String]) -> AnyResult<()> {
    let mut canon = PathBuf::from("config/canon/canonical_66_books.yaml");
    let mut summary_json: Option<PathBuf> = None;
    let mut paths: Vec<PathBuf> = Vec::new();
    let mut index = 0;

    while index < args.len() {
        match args[index].as_str() {
            "--canon" => {
                index += 1;
                canon = PathBuf::from(args.get(index).ok_or("--canon requires a value")?);
            }
            "--summary-json" => {
                index += 1;
                summary_json = Some(PathBuf::from(
                    args.get(index).ok_or("--summary-json requires a value")?,
                ));
            }
            value if value.starts_with('-') => {
                return Err(format!("unknown canonical-scope flag: {value}").into())
            }
            value => paths.push(PathBuf::from(value)),
        }
        index += 1;
    }

    let (canonical_books, excluded_books) = load_canon_config(&canon)?;
    validate_canon_config(&canonical_books, &excluded_books)?;

    let canonical_set: HashSet<&str> = canonical_books.iter().map(String::as_str).collect();
    let excluded_set: HashSet<&str> = excluded_books.iter().map(String::as_str).collect();
    let mut failures: Vec<String> = Vec::new();
    let mut records = 0usize;

    for path in &paths {
        if !path.exists() {
            failures.push(format!("Missing JSONL file: {}", path.display()));
            continue;
        }
        let file = File::open(path)?;
        let reader = BufReader::new(file);
        for (line_no, line_result) in reader.lines().enumerate() {
            let line_no = line_no + 1;
            let line = line_result?;
            if line.trim().is_empty() {
                continue;
            }
            let record: JsonValue = match serde_json::from_str(&line) {
                Ok(value) => value,
                Err(err) => {
                    failures.push(format!("{}:{line_no}: invalid JSON: {err}", path.display()));
                    continue;
                }
            };
            let Some(record) = record.as_object() else {
                failures.push(format!(
                    "{}:{line_no}: JSONL row is not an object",
                    path.display()
                ));
                continue;
            };
            records += 1;
            let record_id = str_field(record, "id").unwrap_or("<missing-id>");
            let book = record_book_id(record);
            match book {
                None => failures.push(format!(
                    "{}:{line_no}: {record_id} is missing canonical book identity",
                    path.display()
                )),
                Some(book)
                    if excluded_set.contains(book.as_str())
                        || !canonical_set.contains(book.as_str()) =>
                {
                    failures.push(format!(
                        "{}:{line_no}: {record_id} uses non-66 canonical-scope book {book}",
                        path.display()
                    ));
                }
                Some(_) => {}
            }
        }
    }

    let summary = json!({
        "validator": "logos_fast_validators canonical-scope",
        "status": if failures.is_empty() { "passed" } else { "failed" },
        "canon": canon,
        "canonical_books": canonical_books.len(),
        "excluded_books": excluded_books.len(),
        "files": paths.len(),
        "records": records,
        "failures": failures.len(),
    });
    emit_summary(summary_json.as_deref(), &summary)?;

    if !failures.is_empty() {
        println!("FAST CANONICAL SCOPE VALIDATION FAILED");
        for failure in failures.iter().take(200) {
            println!("- {failure}");
        }
        if failures.len() > 200 {
            println!("- ... {} additional failures", failures.len() - 200);
        }
        return Err(format!("{} canonical-scope validation failure(s)", failures.len()).into());
    }

    if paths.is_empty() {
        println!("Fast canonical 66 scope config validation passed.");
    } else {
        println!(
            "Fast canonical 66 scope validation passed for {} JSONL file(s).",
            paths.len()
        );
    }
    Ok(())
}

pub(crate) fn canonical_qa(args: &[String]) -> AnyResult<()> {
    let mut canon = PathBuf::from("config/canon/canonical_66_books.yaml");
    let mut canonical_root = PathBuf::from("data/canonical");
    let mut include_word_tokens = true;
    let mut summary_json: Option<PathBuf> = None;
    let mut index = 0;
    while index < args.len() {
        match args[index].as_str() {
            "--canon" => {
                index += 1;
                canon = PathBuf::from(args.get(index).ok_or("--canon requires a value")?);
            }
            "--canonical-root" => {
                index += 1;
                canonical_root =
                    PathBuf::from(args.get(index).ok_or("--canonical-root requires a value")?);
            }
            "--skip-word-tokens" => include_word_tokens = false,
            "--summary-json" => {
                index += 1;
                summary_json = Some(PathBuf::from(
                    args.get(index).ok_or("--summary-json requires a value")?,
                ));
            }
            value if value.starts_with('-') => {
                return Err(format!("unknown canonical-qa flag: {value}").into())
            }
            value => {
                return Err(
                    format!("canonical-qa does not accept positional path yet: {value}").into(),
                )
            }
        }
        index += 1;
    }

    let (canonical_books, excluded_books) = load_canon_config(&canon)?;
    validate_canon_config(&canonical_books, &excluded_books)?;
    let canonical_set: HashSet<&str> = canonical_books.iter().map(String::as_str).collect();
    let excluded_set: HashSet<&str> = excluded_books.iter().map(String::as_str).collect();

    let mut failures: Vec<String> = Vec::new();
    let mut required = vec![
        canonical_root.join(PASSAGES_REL),
        canonical_root.join(WITNESSES_REL),
        canonical_root.join(GLOSSARY_REL),
    ];
    required.extend(SIDECAR_RELS.iter().map(|rel| canonical_root.join(rel)));
    if include_word_tokens {
        required.push(canonical_root.join(WORD_TOKENS_REL));
    }
    for path in required {
        if !path.is_file() {
            failures.push(format!(
                "missing required canonical output: {}",
                path.display()
            ));
        }
    }
    if !failures.is_empty() {
        return emit_canonical_qa_result(
            summary_json.as_deref(),
            &canonical_root,
            &canonical_books,
            0,
            0,
            &BTreeMap::new(),
            None,
            &BTreeSet::new(),
            failures,
        );
    }

    let passages_path = canonical_root.join(PASSAGES_REL);
    let witnesses_path = canonical_root.join(WITNESSES_REL);
    let glossary_path = canonical_root.join(GLOSSARY_REL);

    let mut passage_ids: BTreeSet<String> = BTreeSet::new();
    let mut books_in_order: Vec<String> = Vec::new();
    let mut seen_books: HashSet<String> = HashSet::new();
    let mut passage_count = 0usize;
    stream_jsonl_objects(
        &passages_path,
        &mut failures,
        |line_no, record, failures| {
            let book = validate_qa_book_identity(
                record,
                &passages_path,
                line_no,
                &canonical_set,
                &excluded_set,
                failures,
            );
            if let Some(book) = book {
                if seen_books.insert(book.clone()) {
                    books_in_order.push(book);
                }
            }
            match str_field(record, "id") {
                Some(id) if !id.is_empty() => {
                    if !passage_ids.insert(id.to_string()) {
                        push_limited(
                            failures,
                            format!(
                                "{}:{line_no}: duplicate passage id {id}",
                                passages_path.display()
                            ),
                        );
                    }
                }
                _ => push_limited(
                    failures,
                    format!(
                        "{}:{line_no}: passage record is missing id",
                        passages_path.display()
                    ),
                ),
            }
            if record.contains_key("text") && json_text(record.get("text")).trim().is_empty() {
                push_limited(
                    failures,
                    format!(
                        "{}:{line_no}: passage text field is empty",
                        passages_path.display()
                    ),
                );
            }
            passage_count += 1;
        },
    )?;

    if books_in_order != canonical_books {
        failures.push(format!(
            "passage book order/set mismatch: expected {:?}, observed {:?}",
            canonical_books, books_in_order
        ));
    }

    let mut witness_passage_ids: BTreeSet<String> = BTreeSet::new();
    let mut allowed_empty_witness_refs: BTreeSet<String> = BTreeSet::new();
    let mut witness_count = 0usize;
    stream_jsonl_objects(
        &witnesses_path,
        &mut failures,
        |line_no, record, failures| {
            validate_qa_book_identity(
                record,
                &witnesses_path,
                line_no,
                &canonical_set,
                &excluded_set,
                failures,
            );
            match str_field(record, "passage_id") {
                Some(passage_id) if !passage_id.is_empty() => {
                    if !witness_passage_ids.insert(passage_id.to_string()) {
                        push_limited(
                            failures,
                            format!(
                                "{}:{line_no}: duplicate witness passage_id {passage_id}",
                                witnesses_path.display()
                            ),
                        );
                    }
                }
                _ => push_limited(
                    failures,
                    format!(
                        "{}:{line_no}: witness is missing passage_id",
                        witnesses_path.display()
                    ),
                ),
            }
            if json_text(record.get("text")).trim().is_empty() {
                let osis_ref = str_field(record, "osis_ref").unwrap_or("");
                if KNOWN_EMPTY_WITNESS_REFS.contains(&osis_ref) {
                    allowed_empty_witness_refs.insert(osis_ref.to_string());
                } else {
                    push_limited(
                        failures,
                        format!(
                            "{}:{line_no}: witness text is empty",
                            witnesses_path.display()
                        ),
                    );
                }
            }
            witness_count += 1;
        },
    )?;

    if witness_count != passage_count {
        failures.push(format!(
            "translation_witnesses count {witness_count} != passages count {passage_count}"
        ));
    }
    let missing_witnesses: Vec<String> = passage_ids
        .difference(&witness_passage_ids)
        .take(10)
        .cloned()
        .collect();
    if !missing_witnesses.is_empty() {
        failures.push(format!(
            "translation_witnesses missing passage ids: {:?}",
            missing_witnesses
        ));
    }
    let extra_witnesses: Vec<String> = witness_passage_ids
        .difference(&passage_ids)
        .take(10)
        .cloned()
        .collect();
    if !extra_witnesses.is_empty() {
        failures.push(format!(
            "translation_witnesses contain unknown passage ids: {:?}",
            extra_witnesses
        ));
    }

    let mut sidecar_counts: BTreeMap<String, usize> = BTreeMap::new();
    let mut footnote_passage_ids: BTreeSet<String> = BTreeSet::new();
    for rel in SIDECAR_RELS {
        let path = canonical_root.join(rel);
        let mut count = 0usize;
        stream_jsonl_objects(&path, &mut failures, |line_no, record, failures| {
            validate_qa_book_identity(
                record,
                &path,
                line_no,
                &canonical_set,
                &excluded_set,
                failures,
            );
            if let Some(passage_id) = str_field(record, "passage_id") {
                if !passage_ids.contains(passage_id) {
                    push_limited(
                        failures,
                        format!(
                            "{}:{line_no}: unknown passage_id {passage_id}",
                            path.display()
                        ),
                    );
                }
                if *rel == "translations/eng-web/footnotes.jsonl"
                    && !json_text(record.get("text")).trim().is_empty()
                {
                    footnote_passage_ids.insert(passage_id.to_string());
                }
            }
            count += 1;
        })?;
        sidecar_counts.insert((*rel).to_string(), count);
    }

    for osis_ref in &allowed_empty_witness_refs {
        let passage_id = format!("scripture:{osis_ref}");
        if !footnote_passage_ids.contains(&passage_id) {
            failures.push(format!(
                "{passage_id} has allowed empty witness text but no explanatory footnote"
            ));
        }
    }

    let mut glossary_count = 0usize;
    stream_jsonl_objects(
        &glossary_path,
        &mut failures,
        |line_no, record, failures| {
            if !is_non_scripture_glossary_record(record) {
                failures.push(format!(
                    "{}:{line_no}: glossary entry is not explicitly marked non-Scripture",
                    glossary_path.display()
                ));
            }
            glossary_count += 1;
        },
    )?;
    sidecar_counts.insert(GLOSSARY_REL.to_string(), glossary_count);

    let word_token_count = if include_word_tokens {
        let word_token_path = canonical_root.join(WORD_TOKENS_REL);
        let mut count = 0usize;
        stream_jsonl_objects(
            &word_token_path,
            &mut failures,
            |line_no, record, failures| {
                validate_qa_book_identity(
                    record,
                    &word_token_path,
                    line_no,
                    &canonical_set,
                    &excluded_set,
                    failures,
                );
                if let Some(passage_id) = str_field(record, "passage_id") {
                    if !passage_ids.contains(passage_id) {
                        push_limited(
                            failures,
                            format!(
                                "{}:{line_no}: unknown passage_id {passage_id}",
                                word_token_path.display()
                            ),
                        );
                    }
                }
                count += 1;
            },
        )?;
        Some(count)
    } else {
        None
    };

    emit_canonical_qa_result(
        summary_json.as_deref(),
        &canonical_root,
        &canonical_books,
        passage_count,
        witness_count,
        &sidecar_counts,
        word_token_count,
        &allowed_empty_witness_refs,
        failures,
    )
}

#[allow(clippy::too_many_arguments)]
fn emit_canonical_qa_result(
    summary_json: Option<&Path>,
    canonical_root: &Path,
    canonical_books: &[String],
    passage_count: usize,
    witness_count: usize,
    sidecar_counts: &BTreeMap<String, usize>,
    word_token_count: Option<usize>,
    allowed_empty_witness_refs: &BTreeSet<String>,
    failures: Vec<String>,
) -> AnyResult<()> {
    let summary = json!({
        "validator": "logos_fast_validators canonical-qa",
        "status": if failures.is_empty() { "passed" } else { "failed" },
        "canonical_root": canonical_root,
        "authoritative_validator": "scripts/qa_canonical_corpus.py",
        "authority": "deterministic_structural_check_only",
        "non_authorizing": true,
        "canonical_books": canonical_books.len(),
        "passage_records": passage_count,
        "translation_witness_records": witness_count,
        "sidecar_counts": sidecar_counts,
        "word_token_records": word_token_count,
        "allowed_empty_witness_refs": allowed_empty_witness_refs,
        "failures": failures.len(),
    });
    emit_summary(summary_json, &summary)?;
    if !failures.is_empty() {
        println!("FAST CANONICAL CORPUS QA FAILED");
        for failure in failures.iter().take(200) {
            println!("- {failure}");
        }
        if failures.len() > 200 {
            println!("- ... {} additional failures", failures.len() - 200);
        }
        return Err(format!("{} canonical corpus QA failure(s)", failures.len()).into());
    }
    println!("Fast canonical corpus QA passed.");
    println!("- canonical root: {}", canonical_root.display());
    println!("- canonical books: {}", canonical_books.len());
    println!("- passage records: {passage_count}");
    println!("- translation witness records: {witness_count}");
    if !allowed_empty_witness_refs.is_empty() {
        println!(
            "- allowed empty textual-variant witnesses: {}",
            allowed_empty_witness_refs.len()
        );
        for osis_ref in allowed_empty_witness_refs {
            println!("  - {osis_ref}");
        }
    }
    for (rel, count) in sidecar_counts {
        println!("- {rel}: {count}");
    }
    if let Some(count) = word_token_count {
        println!("- {WORD_TOKENS_REL}: {count}");
    }
    Ok(())
}

pub(crate) fn word_token_signals(args: &[String]) -> AnyResult<()> {
    let mut translation_id = "eng-web".to_string();
    let mut summary_json: Option<PathBuf> = None;
    let mut paths: Vec<PathBuf> = Vec::new();
    let mut index = 0;

    while index < args.len() {
        match args[index].as_str() {
            "--translation-id" => {
                index += 1;
                translation_id = args
                    .get(index)
                    .ok_or("--translation-id requires a value")?
                    .to_string();
            }
            "--summary-json" => {
                index += 1;
                summary_json = Some(PathBuf::from(
                    args.get(index).ok_or("--summary-json requires a value")?,
                ));
            }
            value if value.starts_with('-') => {
                return Err(format!("unknown word-token-signals flag: {value}").into())
            }
            value => paths.push(PathBuf::from(value)),
        }
        index += 1;
    }

    if paths.is_empty() {
        return Err("word-token-signals requires at least one word_tokens JSONL path".into());
    }

    let mut failures: Vec<String> = Vec::new();
    let mut records = 0usize;
    let mut source_files: BTreeSet<String> = BTreeSet::new();
    let mut translation_ids: BTreeSet<String> = BTreeSet::new();
    let mut book_token_counts: BTreeMap<String, usize> = BTreeMap::new();
    let mut book_wj_token_counts: BTreeMap<String, usize> = BTreeMap::new();
    let mut books_with_wj: BTreeSet<String> = BTreeSet::new();
    let mut wj_word_tokens = 0usize;
    let mut wj_token_runs = 0usize;
    let mut in_wj_run = false;
    let mut current_wj_book = String::new();
    let mut strong_occurrences_total = 0usize;
    let mut strong_h_occurrences = 0usize;
    let mut strong_g_occurrences = 0usize;
    let mut strong_other_occurrences = 0usize;
    let mut tokens_with_strong = 0usize;
    let mut tokens_with_surface_text = 0usize;
    let mut tokens_with_nesting_context = 0usize;

    for path in &paths {
        if !path.is_file() {
            failures.push(format!("Missing word-token JSONL file: {}", path.display()));
            continue;
        }
        stream_jsonl_objects(path, &mut failures, |line_no, record, failures| {
            records += 1;

            let actual_translation = str_field(record, "translation_id").unwrap_or("");
            if actual_translation.is_empty() {
                push_limited(
                    failures,
                    format!("{}:{line_no}: missing translation_id", path.display()),
                );
            } else {
                translation_ids.insert(actual_translation.to_string());
                if actual_translation != translation_id {
                    push_limited(
                        failures,
                        format!(
                            "{}:{line_no}: translation_id {actual_translation} != expected {translation_id}",
                            path.display()
                        ),
                    );
                }
            }

            let book = str_field(record, "book")
                .and_then(normalize_book_id)
                .or_else(|| record_book_id(record))
                .unwrap_or_default();
            if book.is_empty() {
                push_limited(
                    failures,
                    format!("{}:{line_no}: missing book identity", path.display()),
                );
            } else {
                *book_token_counts.entry(book.clone()).or_default() += 1;
            }

            if str_field(record, "osis_ref").is_none_or(|value| !valid_osis_ref(value)) {
                push_limited(
                    failures,
                    format!(
                        "{}:{line_no}: missing or malformed osis_ref",
                        path.display()
                    ),
                );
            }

            if let Some(source_file) = str_field(record, "source_file") {
                if !source_file.is_empty() {
                    source_files.insert(source_file.to_string());
                }
            }
            if str_field(record, "surface_text").is_some_and(|value| !value.is_empty()) {
                tokens_with_surface_text += 1;
            }
            if json_array_contains_str(record.get("nesting_context"), "wj") {
                wj_word_tokens += 1;
                if !book.is_empty() {
                    books_with_wj.insert(book.clone());
                    *book_wj_token_counts.entry(book.clone()).or_default() += 1;
                }
                if !in_wj_run || current_wj_book != book {
                    wj_token_runs += 1;
                    current_wj_book = book.clone();
                }
                in_wj_run = true;
            } else {
                in_wj_run = false;
                current_wj_book.clear();
            }
            if record
                .get("nesting_context")
                .and_then(JsonValue::as_array)
                .is_some_and(|items| !items.is_empty())
            {
                tokens_with_nesting_context += 1;
            }

            let mut strong_values: Vec<String> = Vec::new();
            collect_strong_values(record.get("strong"), &mut strong_values);
            collect_strong_values(record.get("strong_id"), &mut strong_values);
            collect_strong_values(record.get("strong_ids"), &mut strong_values);
            collect_strong_values(record.get("strongs"), &mut strong_values);
            if !strong_values.is_empty() {
                tokens_with_strong += 1;
            }
            for strong in strong_values {
                strong_occurrences_total += 1;
                if strong.starts_with('H') {
                    strong_h_occurrences += 1;
                } else if strong.starts_with('G') {
                    strong_g_occurrences += 1;
                } else {
                    strong_other_occurrences += 1;
                }
            }
        })?;
    }

    let summary = json!({
        "validator": "logos_fast_validators word-token-signals",
        "status": if failures.is_empty() { "passed" } else { "failed" },
        "files": paths.len(),
        "records": records,
        "failures": failures.len(),
        "translation_id": translation_id,
        "translation_ids_observed": translation_ids,
        "source_file_count": source_files.len(),
        "book_count": book_token_counts.len(),
        "book_token_counts": book_token_counts,
        "wj_word_tokens": wj_word_tokens,
        "wj_token_runs": wj_token_runs,
        "books_with_wj": books_with_wj,
        "book_wj_token_counts": book_wj_token_counts,
        "tokens_with_nesting_context": tokens_with_nesting_context,
        "tokens_with_surface_text": tokens_with_surface_text,
        "tokens_with_strong": tokens_with_strong,
        "strong_occurrences_total": strong_occurrences_total,
        "strong_h_occurrences": strong_h_occurrences,
        "strong_g_occurrences": strong_g_occurrences,
        "strong_other_occurrences": strong_other_occurrences,
        "non_authorizing": true,
        "no_text": true,
        "authority": "deterministic_word_token_signal_counts_only",
    });
    emit_summary(summary_json.as_deref(), &summary)?;

    if !failures.is_empty() {
        println!("FAST WORD-TOKEN SIGNAL SCAN FAILED");
        for failure in failures.iter().take(200) {
            println!("- {failure}");
        }
        if failures.len() > 200 {
            println!("- ... {} additional failures", failures.len() - 200);
        }
        return Err(format!("{} word-token signal failure(s)", failures.len()).into());
    }

    println!("Fast word-token signal scan passed for {records} record(s).");
    println!("- files: {}", paths.len());
    println!("- source files: {}", source_files.len());
    println!("- books: {}", summary["book_count"]);
    println!("- WJ tokens: {wj_word_tokens}");
    println!("- WJ token runs: {wj_token_runs}");
    println!("- Strong occurrences: {strong_occurrences_total}");
    Ok(())
}

fn stream_jsonl_objects<F>(path: &Path, failures: &mut Vec<String>, mut visit: F) -> AnyResult<()>
where
    F: FnMut(usize, &Map<String, JsonValue>, &mut Vec<String>),
{
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    for (line_no, line_result) in reader.lines().enumerate() {
        let line_no = line_no + 1;
        let line = line_result?;
        if line.trim().is_empty() {
            continue;
        }
        let record: JsonValue = match serde_json::from_str(&line) {
            Ok(value) => value,
            Err(err) => {
                failures.push(format!("{}:{line_no}: invalid JSON: {err}", path.display()));
                continue;
            }
        };
        let Some(record) = record.as_object() else {
            failures.push(format!(
                "{}:{line_no}: JSONL row is not an object",
                path.display()
            ));
            continue;
        };
        visit(line_no, record, failures);
    }
    Ok(())
}

fn validate_qa_book_identity(
    record: &Map<String, JsonValue>,
    source: &Path,
    line_no: usize,
    expected_books: &HashSet<&str>,
    blocked_books: &HashSet<&str>,
    failures: &mut Vec<String>,
) -> Option<String> {
    let record_id = str_field(record, "id").unwrap_or("<missing-id>");
    let book = record_book_id(record);
    match book {
        None => {
            failures.push(format!(
                "{}:{line_no}: {record_id} is missing canonical book identity",
                source.display()
            ));
            None
        }
        Some(book)
            if blocked_books.contains(book.as_str()) || !expected_books.contains(book.as_str()) =>
        {
            failures.push(format!(
                "{}:{line_no}: {record_id} uses non-66 book {book}",
                source.display()
            ));
            Some(book)
        }
        Some(book) => Some(book),
    }
}

fn push_limited(failures: &mut Vec<String>, message: String) {
    const LIMIT: usize = 50;
    if failures.len() < LIMIT {
        failures.push(message);
    } else if failures.len() == LIMIT {
        failures.push("additional QA failures suppressed".to_string());
    }
}

fn json_text(value: Option<&JsonValue>) -> String {
    match value {
        None | Some(JsonValue::Null) => String::new(),
        Some(JsonValue::String(value)) => value.clone(),
        Some(value) => value.to_string(),
    }
}

fn json_array_contains_str(value: Option<&JsonValue>, needle: &str) -> bool {
    value
        .and_then(JsonValue::as_array)
        .is_some_and(|items| items.iter().any(|item| item.as_str() == Some(needle)))
}

fn collect_strong_values(value: Option<&JsonValue>, out: &mut Vec<String>) {
    match value {
        Some(JsonValue::String(value)) if !value.trim().is_empty() => {
            out.push(value.trim().to_string());
        }
        Some(JsonValue::Array(values)) => {
            for value in values {
                collect_strong_values(Some(value), out);
            }
        }
        _ => {}
    }
}

fn json_false(value: Option<&JsonValue>) -> bool {
    matches!(value, Some(JsonValue::Bool(false)))
}

fn is_non_scripture_glossary_record(record: &Map<String, JsonValue>) -> bool {
    if json_false(record.get("scripture_content")) || json_false(record.get("canonical_scripture"))
    {
        return true;
    }
    for key in ["scope", "content_scope", "record_scope"] {
        if let Some(value) = str_field(record, key) {
            if NON_SCRIPTURE_GLOSSARY_SCOPES.contains(&value) {
                return true;
            }
        }
    }
    false
}

pub(crate) fn chunk_map(args: &[String]) -> AnyResult<()> {
    let mut canon = PathBuf::from("config/canon/canonical_66_books.yaml");
    let mut summary_json: Option<PathBuf> = None;
    let mut expected_model_id: Option<String> = None;
    let mut require_full_bible = false;
    let mut allowed_books: BTreeSet<String> = BTreeSet::new();
    let mut path: Option<PathBuf> = None;
    let mut index = 0;

    while index < args.len() {
        match args[index].as_str() {
            "--canon" => {
                index += 1;
                canon = PathBuf::from(args.get(index).ok_or("--canon requires a value")?);
            }
            "--summary-json" => {
                index += 1;
                summary_json = Some(PathBuf::from(
                    args.get(index).ok_or("--summary-json requires a value")?,
                ));
            }
            "--model-id" => {
                index += 1;
                expected_model_id = Some(
                    args.get(index)
                        .ok_or("--model-id requires a value")?
                        .to_string(),
                );
            }
            "--require-full-bible" => require_full_bible = true,
            "--book" => {
                index += 1;
                allowed_books.insert(
                    normalize_book_id(args.get(index).ok_or("--book requires a value")?)
                        .ok_or("--book cannot be empty")?,
                );
            }
            value if value.starts_with('-') => {
                return Err(format!("unknown chunk-map flag: {value}").into())
            }
            value => {
                if path.is_some() {
                    return Err("chunk-map accepts exactly one JSONL path".into());
                }
                path = Some(PathBuf::from(value));
            }
        }
        index += 1;
    }

    let path = path.ok_or("chunk-map requires one JSONL path")?;
    if !path.is_file() {
        return Err(format!("missing chunk-map JSONL file: {}", path.display()).into());
    }

    let (canonical_books, excluded_books) = load_canon_config(&canon)?;
    validate_canon_config(&canonical_books, &excluded_books)?;
    let canonical_set: HashSet<&str> = canonical_books.iter().map(String::as_str).collect();

    let file = File::open(&path)?;
    let reader = BufReader::new(file);
    let mut failures: Vec<String> = Vec::new();
    let mut seen_decision_ids: BTreeSet<String> = BTreeSet::new();
    let mut by_book: BTreeMap<String, Vec<ChunkEntry>> = BTreeMap::new();
    let mut records = 0usize;

    for (line_no, line_result) in reader.lines().enumerate() {
        let line_no = line_no + 1;
        let line = line_result?;
        if line.trim().is_empty() {
            continue;
        }
        let record: JsonValue = match serde_json::from_str(&line) {
            Ok(value) => value,
            Err(err) => {
                failures.push(format!("{}:{line_no}: invalid JSON: {err}", path.display()));
                continue;
            }
        };
        let Some(record) = record.as_object() else {
            failures.push(format!(
                "{}:{line_no}: JSONL row is not an object",
                path.display()
            ));
            continue;
        };
        records += 1;
        validate_chunk_record(
            &path,
            line_no,
            record,
            expected_model_id.as_deref(),
            &canonical_set,
            &allowed_books,
            &mut seen_decision_ids,
            &mut by_book,
            &mut failures,
        );
    }

    for (book, chunks) in by_book.iter_mut() {
        chunks.sort_by_key(|chunk| chunk.index);
        let indices: Vec<i64> = chunks.iter().map(|chunk| chunk.index).collect();
        let expected: Vec<i64> = (1..=(indices.len() as i64)).collect();
        if indices != expected {
            failures.push(format!(
                "{} book {book}: chunk_index_in_book must be contiguous from 1",
                path.display()
            ));
        }
        for pair in chunks.windows(2) {
            let cur = &pair[0].span;
            let next = &pair[1].span;
            if cur.end_key() >= next.start_key() {
                failures.push(format!(
                    "{} book {book}: chunk {} overlaps or inverts order with chunk {}",
                    path.display(),
                    pair[0].index,
                    pair[1].index
                ));
            }
        }
    }

    if require_full_bible {
        let present: HashSet<&str> = by_book.keys().map(String::as_str).collect();
        let missing: Vec<&str> = canonical_books
            .iter()
            .map(String::as_str)
            .filter(|book| !present.contains(book))
            .collect();
        if !missing.is_empty() {
            failures.push(format!(
                "{}: missing books: {}",
                path.display(),
                missing.join(", ")
            ));
        }
    }

    let summary = json!({
        "validator": "logos_fast_validators chunk-map",
        "status": if failures.is_empty() { "passed" } else { "failed" },
        "file": path,
        "records": records,
        "books": by_book.len(),
        "failures": failures.len(),
        "require_full_bible": require_full_bible,
        "expected_model_id": expected_model_id,
        "non_authorizing": true,
        "authority": "deterministic_structure_check_only",
    });
    emit_summary(summary_json.as_deref(), &summary)?;

    if !failures.is_empty() {
        println!("FAST CHUNK-MAP VALIDATION FAILED");
        for failure in failures.iter().take(200) {
            println!("- {failure}");
        }
        if failures.len() > 200 {
            println!("- ... {} additional failures", failures.len() - 200);
        }
        return Err(format!("{} chunk-map validation failure(s)", failures.len()).into());
    }

    println!("Fast chunk-map validation passed for {records} record(s).");
    Ok(())
}

#[allow(clippy::too_many_arguments)]
fn validate_chunk_record(
    path: &Path,
    line_no: usize,
    record: &Map<String, JsonValue>,
    expected_model_id: Option<&str>,
    canonical_set: &HashSet<&str>,
    allowed_books: &BTreeSet<String>,
    seen_decision_ids: &mut BTreeSet<String>,
    by_book: &mut BTreeMap<String, Vec<ChunkEntry>>,
    failures: &mut Vec<String>,
) {
    const REQUIRED_CHUNK_FIELDS: &[&str] = &[
        "model_id",
        "book",
        "span",
        "chunk_index_in_book",
        "literature_type_guess",
        "boundary_evidence_refs",
        "strong_or_hebrew_tags_used",
        "wj_or_red_letter_considered",
        "confidence",
        "decision_id",
        "non_authorizing",
    ];

    for field in REQUIRED_CHUNK_FIELDS {
        if !record.contains_key(*field) {
            failures.push(format!(
                "{}:{line_no}: missing required field {field}",
                path.display()
            ));
        }
    }

    if record.get("non_authorizing") != Some(&JsonValue::Bool(true)) {
        failures.push(format!(
            "{}:{line_no}: non_authorizing must be true",
            path.display()
        ));
    }

    if let Some(expected) = expected_model_id {
        let actual = str_field(record, "model_id").unwrap_or("");
        if actual != expected {
            failures.push(format!(
                "{}:{line_no}: model_id {actual:?} != expected {expected:?}",
                path.display()
            ));
        }
    }

    let book = str_field(record, "book")
        .and_then(normalize_book_id)
        .unwrap_or_default();
    if !allowed_books.is_empty() && !allowed_books.contains(&book) {
        failures.push(format!(
            "{}:{line_no}: book {book:?} not in allowed scope",
            path.display()
        ));
    }
    if !canonical_set.contains(book.as_str()) {
        failures.push(format!(
            "{}:{line_no}: unknown book {book:?}",
            path.display()
        ));
    }

    let span = match str_field(record, "span") {
        Some(value) => match parse_span(value) {
            Ok(span) => {
                if span.book != book {
                    failures.push(format!(
                        "{}:{line_no}: span book {:?} != record book {:?}",
                        path.display(),
                        span.book,
                        book
                    ));
                }
                Some(span)
            }
            Err(err) => {
                failures.push(format!("{}:{line_no}: {err}", path.display()));
                None
            }
        },
        None => {
            failures.push(format!("{}:{line_no}: span must be string", path.display()));
            None
        }
    };

    if let Some(decision_id) = str_field(record, "decision_id") {
        if !seen_decision_ids.insert(decision_id.to_string()) {
            failures.push(format!(
                "{}:{line_no}: duplicate decision_id {decision_id}",
                path.display()
            ));
        }
    }

    let chunk_index = record
        .get("chunk_index_in_book")
        .and_then(JsonValue::as_i64);
    if chunk_index.is_none_or(|value| value < 1) {
        failures.push(format!(
            "{}:{line_no}: chunk_index_in_book must be positive int",
            path.display()
        ));
    }

    let evidence = record
        .get("boundary_evidence_refs")
        .and_then(JsonValue::as_array);
    if evidence.is_none_or(Vec::is_empty) {
        failures.push(format!(
            "{}:{line_no}: boundary_evidence_refs must be non-empty list",
            path.display()
        ));
    }

    if let (Some(index), Some(span)) = (chunk_index, span) {
        by_book
            .entry(book)
            .or_default()
            .push(ChunkEntry { index, span });
    }
}

#[derive(Debug, Clone)]
struct ChunkEntry {
    index: i64,
    span: ParsedSpan,
}

#[derive(Debug, Clone)]
struct ParsedSpan {
    book: String,
    start_chapter: i64,
    start_verse: i64,
    end_chapter: i64,
    end_verse: i64,
}

impl ParsedSpan {
    fn start_key(&self) -> (i64, i64) {
        (self.start_chapter, self.start_verse)
    }

    fn end_key(&self) -> (i64, i64) {
        (self.end_chapter, self.end_verse)
    }
}

fn parse_span(value: &str) -> Result<ParsedSpan, String> {
    let mut endpoints = value.trim().split('-');
    let start = endpoints.next().unwrap_or("");
    let end = endpoints.next();
    if endpoints.next().is_some() {
        return Err(format!("malformed span: {value:?}"));
    }
    let (book, start_chapter, start_verse) =
        parse_span_endpoint(start).ok_or_else(|| format!("malformed span: {value:?}"))?;
    let (end_book, end_chapter, end_verse) = match end {
        Some(endpoint) => {
            parse_span_endpoint(endpoint).ok_or_else(|| format!("malformed span: {value:?}"))?
        }
        None => (book.clone(), start_chapter, start_verse),
    };
    if book != end_book {
        return Err(format!("span crosses books: {value:?}"));
    }
    if (end_chapter, end_verse) < (start_chapter, start_verse) {
        return Err(format!("span end before start: {value:?}"));
    }
    Ok(ParsedSpan {
        book,
        start_chapter,
        start_verse,
        end_chapter,
        end_verse,
    })
}

fn parse_span_endpoint(value: &str) -> Option<(String, i64, i64)> {
    let mut parts = value.split('.');
    let book = normalize_book_id(parts.next()?)?;
    let chapter = parts.next()?.parse::<i64>().ok()?;
    let verse = parts.next()?.parse::<i64>().ok()?;
    if parts.next().is_some() || chapter < 1 || verse < 1 {
        return None;
    }
    Some((book, chapter, verse))
}

fn load_canon_config(path: &Path) -> AnyResult<(Vec<String>, Vec<String>)> {
    let file = File::open(path)?;
    let yaml: YamlValue = serde_yaml::from_reader(file)?;
    let mapping = yaml
        .as_mapping()
        .ok_or("canonical config must be a YAML mapping")?;
    let canonical = scalar_list(mapping, "canonical_66_books")?;
    let excluded = scalar_list(mapping, "excluded_books")?;
    Ok((canonical, excluded))
}

fn scalar_list(mapping: &serde_yaml::Mapping, key: &str) -> AnyResult<Vec<String>> {
    let key_value = YamlValue::String(key.to_string());
    let value = mapping
        .get(&key_value)
        .ok_or_else(|| format!("No values found for {key}"))?;
    let sequence = value
        .as_sequence()
        .ok_or_else(|| format!("{key} must be a YAML sequence"))?;
    let values: Vec<String> = sequence
        .iter()
        .map(|item| {
            item.as_str()
                .map(str::to_string)
                .ok_or_else(|| format!("{key} contains a non-string value"))
        })
        .collect::<Result<_, _>>()?;
    if values.is_empty() {
        return Err(format!("No values found for {key}").into());
    }
    Ok(values)
}

fn validate_canon_config(canonical: &[String], excluded: &[String]) -> AnyResult<()> {
    if canonical.len() != 66 {
        return Err(format!("Expected 66 canonical books, found {}", canonical.len()).into());
    }
    let unique: HashSet<&str> = canonical.iter().map(String::as_str).collect();
    if unique.len() != 66 {
        return Err("Canonical 66-book allow-list contains duplicates".into());
    }
    if canonical.first().map(String::as_str) != Some("Gen")
        || canonical.last().map(String::as_str) != Some("Rev")
    {
        return Err("Canonical 66-book allow-list must run from Gen through Rev".into());
    }
    let excluded_set: HashSet<&str> = excluded.iter().map(String::as_str).collect();
    let missing: Vec<&str> = REQUIRED_EXCLUDED
        .iter()
        .copied()
        .filter(|book| !excluded_set.contains(book))
        .collect();
    if !missing.is_empty() {
        return Err(format!("Missing excluded book ids: {missing:?}").into());
    }
    let overlap: Vec<&str> = canonical
        .iter()
        .map(String::as_str)
        .filter(|book| excluded_set.contains(book))
        .collect();
    if !overlap.is_empty() {
        return Err(format!("Books cannot be both canonical and excluded: {overlap:?}").into());
    }
    Ok(())
}

fn record_book_id(record: &Map<String, JsonValue>) -> Option<String> {
    for key in ["book", "osis_book", "usfm_book", "osis_ref", "passage_id"] {
        let Some(value) = str_field(record, key) else {
            continue;
        };
        let mut raw = value;
        if key == "passage_id" {
            raw = raw.strip_prefix("scripture:").unwrap_or(raw);
        }
        if let Some(book) = normalize_book_id(raw) {
            return Some(book);
        }
    }
    None
}

fn normalize_book_id(book_id: &str) -> Option<String> {
    if book_id.trim().is_empty() {
        return None;
    }
    let first = book_id.split('.').next().unwrap_or(book_id);
    Some(osis_book(first).to_string())
}

fn osis_book(book: &str) -> &str {
    match book {
        "GEN" => "Gen",
        "EXO" => "Exod",
        "LEV" => "Lev",
        "NUM" => "Num",
        "DEU" => "Deut",
        "JOS" => "Josh",
        "JDG" => "Judg",
        "RUT" => "Ruth",
        "1SA" => "1Sam",
        "2SA" => "2Sam",
        "1KI" => "1Kgs",
        "2KI" => "2Kgs",
        "1CH" => "1Chr",
        "2CH" => "2Chr",
        "EZR" => "Ezra",
        "NEH" => "Neh",
        "EST" => "Esth",
        "JOB" => "Job",
        "PSA" => "Ps",
        "PRO" => "Prov",
        "ECC" => "Eccl",
        "SNG" => "Song",
        "ISA" => "Isa",
        "JER" => "Jer",
        "LAM" => "Lam",
        "EZK" => "Ezek",
        "DAN" => "Dan",
        "HOS" => "Hos",
        "JOL" => "Joel",
        "AMO" => "Amos",
        "OBA" => "Obad",
        "JON" => "Jonah",
        "MIC" => "Mic",
        "NAM" => "Nah",
        "HAB" => "Hab",
        "ZEP" => "Zeph",
        "HAG" => "Hag",
        "ZEC" => "Zech",
        "MAL" => "Mal",
        "TOB" => "Tob",
        "JDT" => "Jdt",
        "ESG" => "AddEsth",
        "WIS" => "Wis",
        "SIR" => "Sir",
        "BAR" => "Bar",
        "1MA" => "1Macc",
        "2MA" => "2Macc",
        "1ES" => "1Esd",
        "MAN" => "PrMan",
        "PS2" => "Ps151",
        "3MA" => "3Macc",
        "2ES" => "2Esd",
        "4MA" => "4Macc",
        "DAG" => "AddDan",
        "MAT" => "Matt",
        "MRK" => "Mark",
        "LUK" => "Luke",
        "JHN" => "John",
        "ACT" => "Acts",
        "ROM" => "Rom",
        "1CO" => "1Cor",
        "2CO" => "2Cor",
        "GAL" => "Gal",
        "EPH" => "Eph",
        "PHP" => "Phil",
        "COL" => "Col",
        "1TH" => "1Thess",
        "2TH" => "2Thess",
        "1TI" => "1Tim",
        "2TI" => "2Tim",
        "TIT" => "Titus",
        "PHM" => "Phlm",
        "HEB" => "Heb",
        "JAS" => "Jas",
        "1PE" => "1Pet",
        "2PE" => "2Pet",
        "1JN" => "1John",
        "2JN" => "2John",
        "3JN" => "3John",
        "JUD" => "Jude",
        "REV" => "Rev",
        other => other,
    }
}

fn str_field<'a>(record: &'a Map<String, JsonValue>, key: &str) -> Option<&'a str> {
    record.get(key).and_then(JsonValue::as_str)
}

fn json_truthy(value: Option<&JsonValue>) -> bool {
    match value {
        None | Some(JsonValue::Null) => false,
        Some(JsonValue::Bool(value)) => *value,
        Some(JsonValue::Number(value)) => value.as_f64().is_some_and(|number| number != 0.0),
        Some(JsonValue::String(value)) => !value.is_empty(),
        Some(JsonValue::Array(value)) => !value.is_empty(),
        Some(JsonValue::Object(value)) => !value.is_empty(),
    }
}

fn valid_osis_ref(value: &str) -> bool {
    let mut parts = value.split('-');
    let Some(start) = parts.next() else {
        return false;
    };
    let end = parts.next();
    if parts.next().is_some() {
        return false;
    }
    valid_osis_endpoint(start) && end.is_none_or(valid_osis_endpoint)
}

fn valid_osis_endpoint(value: &str) -> bool {
    let parts: Vec<&str> = value.split('.').collect();
    if parts.len() != 3 {
        return false;
    }
    let book = parts[0];
    let chapter = parts[1];
    let verse = parts[2];
    !book.is_empty()
        && book.chars().all(|ch| ch.is_ascii_alphanumeric())
        && book.chars().any(|ch| ch.is_ascii_alphabetic())
        && !chapter.is_empty()
        && chapter.chars().all(|ch| ch.is_ascii_digit())
        && !verse.is_empty()
        && verse.chars().all(|ch| ch.is_ascii_digit())
}

fn contains_usfm_marker(text: &str) -> bool {
    let bytes = text.as_bytes();
    let mut index = 0usize;
    while index < bytes.len() {
        if bytes[index] == b'\\' {
            let mut next = index + 1;
            if next < bytes.len() && bytes[next] == b'+' {
                next += 1;
            }
            if next < bytes.len() && bytes[next].is_ascii_alphanumeric() {
                return true;
            }
        }
        index += 1;
    }
    false
}

fn emit_summary(path: Option<&Path>, summary: &JsonValue) -> AnyResult<()> {
    if let Some(path) = path {
        if path == Path::new("-") {
            eprintln!("{}", serde_json::to_string_pretty(summary)?);
        } else {
            if let Some(parent) = path.parent() {
                if !parent.as_os_str().is_empty() {
                    std::fs::create_dir_all(parent)?;
                }
            }
            let mut file = File::create(path)?;
            writeln!(file, "{}", serde_json::to_string_pretty(summary)?)?;
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn maps_usfm_to_osis_book_ids() {
        assert_eq!(osis_book("GEN"), "Gen");
        assert_eq!(osis_book("REV"), "Rev");
        assert_eq!(osis_book("Phlm"), "Phlm");
    }

    #[test]
    fn parses_record_book_identity() {
        let mut record = Map::new();
        record.insert(
            "passage_id".to_string(),
            JsonValue::String("scripture:2JN.1.1".to_string()),
        );
        assert_eq!(record_book_id(&record), Some("2John".to_string()));
    }

    #[test]
    fn validates_osis_refs_without_regex_dependency() {
        assert!(valid_osis_ref("Gen.1.1"));
        assert!(valid_osis_ref("2John.1.1-2John.1.3"));
        assert!(!valid_osis_ref("Genesis 1:1"));
        assert!(!valid_osis_ref("Gen.1"));
    }

    #[test]
    fn detects_raw_usfm_markers_in_text() {
        assert!(contains_usfm_marker(r"\p In the beginning"));
        assert!(contains_usfm_marker(r"\+w Logos\+w*"));
        assert!(!contains_usfm_marker("In the beginning"));
    }
}
