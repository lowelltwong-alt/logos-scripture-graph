use serde_json::{json, Value};
use serde_yaml::Value as YamlValue;
use std::collections::BTreeSet;
use std::env;
use std::fs::{self, File};
use std::io::{BufRead, BufReader};
use std::path::{Path, PathBuf};

type Result<T> = std::result::Result<T, String>;

const REQUIRED_EXCLUDED: &[&str] = &[
    "FRT", "GLO", "Tob", "Jdt", "AddEsth", "Wis", "Sir", "Bar", "1Macc", "2Macc",
    "1Esd", "PrMan", "Ps151", "3Macc", "2Esd", "4Macc", "AddDan",
];

fn main() {
    match run(env::args().skip(1).collect()) {
        Ok(()) => {}
        Err(err) => {
            eprintln!("logos_fast_validators failed: {err}");
            std::process::exit(1);
        }
    }
}

fn run(args: Vec<String>) -> Result<()> {
    let (command, rest) = args
        .split_first()
        .ok_or_else(|| "expected command: jsonl-scan, canonical-scope, canonical-qa, or chunk-map".to_string())?;
    match command.as_str() {
        "jsonl-scan" => jsonl_scan(rest),
        "canonical-scope" => canonical_scope(rest),
        "canonical-qa" => canonical_qa(rest),
        "chunk-map" => Err("chunk-map is intentionally deferred until T424-D".to_string()),
        other => Err(format!("unsupported command {other:?}")),
    }
}

#[derive(Debug)]
struct JsonlArgs {
    paths: Vec<PathBuf>,
    translation_id: String,
    require_canon: bool,
    summary_json: Option<PathBuf>,
}

#[derive(Default)]
struct JsonlState {
    ids: BTreeSet<String>,
    passages: BTreeSet<String>,
    witnesses: Vec<(String, Option<String>)>,
    record_count: usize,
    failures: Vec<String>,
}

fn jsonl_scan(args: &[String]) -> Result<()> {
    let args = parse_jsonl_args(args)?;
    let mut state = JsonlState::default();

    for path in &args.paths {
        if !path.exists() {
            push_failure(&mut state.failures, format!("Missing JSONL file: {}", path.display()));
            continue;
        }
        scan_jsonl_file(path, &args, &mut state)?;
    }

    for (witness_id, passage_id) in &state.witnesses {
        match passage_id {
            Some(id) if state.passages.contains(id) => {}
            Some(id) => push_failure(
                &mut state.failures,
                format!("{witness_id}: points to missing ScripturePassage {id}"),
            ),
            None => push_failure(
                &mut state.failures,
                format!("{witness_id}: points to missing ScripturePassage <missing>"),
            ),
        }
    }

    let summary = json!({
        "schema_version": "logos_fast_validators.v1",
        "command": "jsonl-scan",
        "non_authorizing": true,
        "record_count": state.record_count,
        "unique_id_count": state.ids.len(),
        "passage_count": state.passages.len(),
        "witness_count": state.witnesses.len(),
        "path_count": args.paths.len(),
        "failure_count": state.failures.len(),
    });
    emit_summary(&args.summary_json, &summary)?;

    if !state.failures.is_empty() {
        println!("JSONL VALIDATION FAILED");
        for failure in &state.failures {
            println!("- {failure}");
        }
        return Err(format!("{} JSONL validation failure(s)", state.failures.len()));
    }
    println!("JSONL validation passed for {} records.", state.ids.len());
    Ok(())
}

fn parse_jsonl_args(args: &[String]) -> Result<JsonlArgs> {
    let mut paths = Vec::new();
    let mut translation_id = "eng-web".to_string();
    let mut require_canon = false;
    let mut summary_json = None;
    let mut index = 0;
    while index < args.len() {
        match args[index].as_str() {
            "--translation-id" => {
                index += 1;
                translation_id = args.get(index).ok_or("--translation-id requires a value")?.clone();
            }
            "--require-canon" => require_canon = true,
            "--summary-json" => {
                index += 1;
                summary_json = Some(PathBuf::from(args.get(index).ok_or("--summary-json requires a value")?));
            }
            value if value.starts_with("--") => return Err(format!("unknown jsonl-scan argument {value:?}")),
            value => paths.push(PathBuf::from(value)),
        }
        index += 1;
    }
    if paths.is_empty() {
        return Err("jsonl-scan requires at least one path".to_string());
    }
    Ok(JsonlArgs {
        paths,
        translation_id,
        require_canon,
        summary_json,
    })
}

fn scan_jsonl_file(path: &Path, args: &JsonlArgs, state: &mut JsonlState) -> Result<()> {
    let file = File::open(path).map_err(|err| format!("{}: {err}", path.display()))?;
    for (zero_based, raw_line) in BufReader::new(file).lines().enumerate() {
        let line_no = zero_based + 1;
        let line = raw_line.map_err(|err| format!("{}:{line_no}: {err}", path.display()))?;
        if line.trim().is_empty() {
            continue;
        }
        let record: Value = match serde_json::from_str(&line) {
            Ok(value) => value,
            Err(err) => {
                push_failure(
                    &mut state.failures,
                    format!("{}:{line_no}: invalid JSON: {err}", path.display()),
                );
                continue;
            }
        };
        state.record_count += 1;
        validate_jsonl_record(path, line_no, &record, args, state);
    }
    Ok(())
}

fn validate_jsonl_record(
    path: &Path,
    line_no: usize,
    record: &Value,
    args: &JsonlArgs,
    state: &mut JsonlState,
) {
    let prefix = format!("{}:{line_no}", path.display());
    let rid = str_field(record, "id");
    match rid {
        None => push_failure(&mut state.failures, format!("{prefix}: missing id")),
        Some(id) if state.ids.contains(id) => {
            push_failure(&mut state.failures, format!("{prefix}: duplicate id {id}"))
        }
        Some(id) => {
            state.ids.insert(id.to_string());
        }
    }

    for key in ["source_sha256", "license"] {
        if str_field(record, key).unwrap_or("").is_empty() {
            push_failure(&mut state.failures, format!("{prefix}: missing {key}"));
        }
    }

    if let Some(osis_ref) = str_field(record, "osis_ref") {
        if !valid_osis_ref(osis_ref) {
            push_failure(
                &mut state.failures,
                format!("{prefix}: malformed OSIS reference {osis_ref}"),
            );
        }
    }

    if str_field(record, "type") == Some("ScripturePassage") {
        if let Some(id) = rid {
            state.passages.insert(id.to_string());
        }
        if args.require_canon && record.get("canon_profiles").is_none() {
            push_failure(
                &mut state.failures,
                format!(
                    "{prefix}: ScripturePassage {} missing canon_profiles (CANON-1)",
                    rid.unwrap_or("<missing-id>")
                ),
            );
        }
    }

    if str_field(record, "type") == Some("TranslationWitness") {
        let witness_id = rid.unwrap_or("<missing-id>").to_string();
        state
            .witnesses
            .push((witness_id, str_field(record, "passage_id").map(str::to_string)));
        if contains_raw_usfm_marker(str_field(record, "text").unwrap_or("")) {
            push_failure(
                &mut state.failures,
                format!("{prefix}: TranslationWitness.text contains raw USFM marker"),
            );
        }
        if str_field(record, "translation_id") != Some(args.translation_id.as_str()) {
            push_failure(
                &mut state.failures,
                format!(
                    "{prefix}: unexpected translation_id {}",
                    str_field(record, "translation_id").unwrap_or("<missing>")
                ),
            );
        }
    }

    if let Some(translation_id) = str_field(record, "translation_id") {
        if translation_id != args.translation_id {
            push_failure(
                &mut state.failures,
                format!(
                    "{prefix}: generated output translation_id {translation_id} != expected {}",
                    args.translation_id
                ),
            );
        }
    }

    if let Some(relation_type) = str_field(record, "relation_type") {
        if relation_type != "editorial_cross_reference" {
            push_failure(
                &mut state.failures,
                format!("{prefix}: disallowed relation_type {relation_type}"),
            );
        }
    }
}

#[derive(Debug)]
struct ScopeArgs {
    jsonl_paths: Vec<PathBuf>,
    canon: PathBuf,
    summary_json: Option<PathBuf>,
}

fn canonical_scope(args: &[String]) -> Result<()> {
    let args = parse_scope_args(args)?;
    let canonical_books = read_yaml_list(&args.canon, "canonical_66_books")?;
    let excluded_books = read_yaml_list(&args.canon, "excluded_books")?;
    validate_canon_config(&canonical_books, &excluded_books)?;

    let canonical_set: BTreeSet<String> = canonical_books.iter().cloned().collect();
    let excluded_set: BTreeSet<String> = excluded_books.iter().cloned().collect();
    let mut record_count = 0_usize;
    let mut failures = Vec::new();

    for path in &args.jsonl_paths {
        if !path.exists() {
            push_failure(&mut failures, format!("Missing JSONL file: {}", path.display()));
            continue;
        }
        let file = File::open(path).map_err(|err| format!("{}: {err}", path.display()))?;
        for (zero_based, raw_line) in BufReader::new(file).lines().enumerate() {
            let line_no = zero_based + 1;
            let line = raw_line.map_err(|err| format!("{}:{line_no}: {err}", path.display()))?;
            if line.trim().is_empty() {
                continue;
            }
            let record: Value = match serde_json::from_str(&line) {
                Ok(value) => value,
                Err(err) => {
                    push_failure(
                        &mut failures,
                        format!("{}:{line_no}: invalid JSON: {err}", path.display()),
                    );
                    continue;
                }
            };
            record_count += 1;
            let book = record_book_id(&record);
            let record_id = str_field(&record, "id").unwrap_or("<missing-id>");
            match book {
                None => push_failure(
                    &mut failures,
                    format!(
                        "{}:{line_no}: {record_id} is missing canonical book identity",
                        path.display()
                    ),
                ),
                Some(book) if excluded_set.contains(&book) || !canonical_set.contains(&book) => push_failure(
                    &mut failures,
                    format!(
                        "{}:{line_no}: {record_id} uses non-66 canonical-scope book {book}",
                        path.display()
                    ),
                ),
                Some(_) => {}
            }
        }
    }

    let summary = json!({
        "schema_version": "logos_fast_validators.v1",
        "command": "canonical-scope",
        "non_authorizing": true,
        "canonical_book_count": canonical_books.len(),
        "jsonl_path_count": args.jsonl_paths.len(),
        "record_count": record_count,
        "failure_count": failures.len(),
    });
    emit_summary(&args.summary_json, &summary)?;

    if !failures.is_empty() {
        for failure in &failures {
            println!("- {failure}");
        }
        return Err(format!("{} canonical-scope validation failure(s)", failures.len()));
    }
    if args.jsonl_paths.is_empty() {
        println!("Canonical 66 scope config validation passed.");
    } else {
        println!(
            "Canonical 66 scope validation passed for {} JSONL file(s).",
            args.jsonl_paths.len()
        );
    }
    Ok(())
}

fn parse_scope_args(args: &[String]) -> Result<ScopeArgs> {
    let mut canon = PathBuf::from("config/canon/canonical_66_books.yaml");
    let mut summary_json = None;
    let mut jsonl_paths = Vec::new();
    let mut index = 0;
    while index < args.len() {
        match args[index].as_str() {
            "--canon" => {
                index += 1;
                canon = PathBuf::from(args.get(index).ok_or("--canon requires a value")?);
            }
            "--summary-json" => {
                index += 1;
                summary_json = Some(PathBuf::from(args.get(index).ok_or("--summary-json requires a value")?));
            }
            value if value.starts_with("--") => return Err(format!("unknown canonical-scope argument {value:?}")),
            value => jsonl_paths.push(PathBuf::from(value)),
        }
        index += 1;
    }
    Ok(ScopeArgs {
        jsonl_paths,
        canon,
        summary_json,
    })
}

fn canonical_qa(args: &[String]) -> Result<()> {
    let mut summary_json = None;
    let mut index = 0;
    while index < args.len() {
        match args[index].as_str() {
            "--summary-json" => {
                index += 1;
                summary_json = Some(PathBuf::from(args.get(index).ok_or("--summary-json requires a value")?));
            }
            value => return Err(format!("unknown canonical-qa argument {value:?}")),
        }
        index += 1;
    }
    let summary = json!({
        "schema_version": "logos_fast_validators.v1",
        "command": "canonical-qa",
        "non_authorizing": true,
        "implemented": false,
        "python_authority": "scripts/qa_canonical_corpus.py",
        "note": "T424 leaves semantic canonical corpus QA in Python; Rust may add a parity-proven subset later."
    });
    emit_summary(&summary_json, &summary)?;
    println!("canonical-qa Rust scaffold present; Python QA remains authoritative.");
    Ok(())
}

fn read_yaml_list(path: &Path, key: &str) -> Result<Vec<String>> {
    let file = File::open(path).map_err(|err| format!("{}: {err}", path.display()))?;
    let value: YamlValue = serde_yaml::from_reader(file).map_err(|err| format!("{}: {err}", path.display()))?;
    let seq = value
        .as_mapping()
        .and_then(|map| map.get(YamlValue::String(key.to_string())))
        .and_then(YamlValue::as_sequence)
        .ok_or_else(|| format!("{}: {key} must be a YAML sequence", path.display()))?;
    let mut values = Vec::new();
    for item in seq {
        if let Some(value) = item.as_str() {
            values.push(value.to_string());
        }
    }
    if values.is_empty() {
        return Err(format!("{}: no values found for {key}", path.display()));
    }
    Ok(values)
}

fn validate_canon_config(canonical_books: &[String], excluded_books: &[String]) -> Result<()> {
    if canonical_books.len() != 66 {
        return Err(format!("Expected 66 canonical books, found {}", canonical_books.len()));
    }
    let unique: BTreeSet<&String> = canonical_books.iter().collect();
    if unique.len() != 66 {
        return Err("Canonical 66-book allow-list contains duplicates".to_string());
    }
    if canonical_books.first().map(String::as_str) != Some("Gen")
        || canonical_books.last().map(String::as_str) != Some("Rev")
    {
        return Err("Canonical 66-book allow-list must run from Gen through Rev".to_string());
    }
    let excluded: BTreeSet<&str> = excluded_books.iter().map(String::as_str).collect();
    let missing: Vec<&str> = REQUIRED_EXCLUDED
        .iter()
        .copied()
        .filter(|book| !excluded.contains(book))
        .collect();
    if !missing.is_empty() {
        return Err(format!("Missing excluded book ids: {missing:?}"));
    }
    let canonical: BTreeSet<&str> = canonical_books.iter().map(String::as_str).collect();
    let overlap: Vec<&str> = excluded.intersection(&canonical).copied().collect();
    if !overlap.is_empty() {
        return Err(format!("Books cannot be both canonical and excluded: {overlap:?}"));
    }
    Ok(())
}

fn record_book_id(record: &Value) -> Option<String> {
    for key in ["book", "osis_book", "usfm_book", "osis_ref", "passage_id"] {
        let Some(mut value) = str_field(record, key) else {
            continue;
        };
        if key == "passage_id" {
            value = value.strip_prefix("scripture:").unwrap_or(value);
        }
        let normalized = normalize_book_id(value);
        if !normalized.is_empty() {
            return Some(normalized);
        }
    }
    None
}

fn normalize_book_id(book_id: &str) -> String {
    let first = book_id.split('.').next().unwrap_or(book_id);
    usfm_to_osis(first).unwrap_or(first).to_string()
}

fn str_field<'a>(record: &'a Value, key: &str) -> Option<&'a str> {
    record.get(key).and_then(Value::as_str)
}

fn push_failure(failures: &mut Vec<String>, message: String) {
    if failures.len() < 200 {
        failures.push(message);
    } else if failures.len() == 200 {
        failures.push("additional validation failures suppressed".to_string());
    }
}

fn valid_osis_ref(value: &str) -> bool {
    let parts: Vec<&str> = value.split('-').collect();
    if parts.len() > 2 {
        return false;
    }
    parts.iter().all(|part| valid_single_osis_ref(part))
}

fn valid_single_osis_ref(value: &str) -> bool {
    let parts: Vec<&str> = value.split('.').collect();
    if parts.len() != 3 {
        return false;
    }
    valid_book_token(parts[0])
        && !parts[1].is_empty()
        && parts[1].chars().all(|ch| ch.is_ascii_digit())
        && !parts[2].is_empty()
        && parts[2].chars().all(|ch| ch.is_ascii_digit())
}

fn valid_book_token(value: &str) -> bool {
    let mut chars = value.chars();
    let Some(first) = chars.next() else {
        return false;
    };
    (first.is_ascii_alphabetic() || first.is_ascii_digit()) && chars.all(|ch| ch.is_ascii_alphanumeric())
}

fn contains_raw_usfm_marker(value: &str) -> bool {
    let chars: Vec<char> = value.chars().collect();
    let mut index = 0;
    while index < chars.len() {
        if chars[index] != '\\' {
            index += 1;
            continue;
        }
        index += 1;
        if index < chars.len() && chars[index] == '+' {
            index += 1;
        }
        if index < chars.len() && chars[index].is_ascii_alphanumeric() {
            return true;
        }
    }
    false
}

fn emit_summary(path: &Option<PathBuf>, summary: &Value) -> Result<()> {
    if let Some(path) = path {
        let text = serde_json::to_string_pretty(summary).map_err(|err| err.to_string())? + "\n";
        if path.as_os_str() == "-" {
            eprint!("{text}");
        } else {
            if let Some(parent) = path.parent() {
                fs::create_dir_all(parent).map_err(|err| format!("{}: {err}", parent.display()))?;
            }
            fs::write(path, text).map_err(|err| format!("{}: {err}", path.display()))?;
        }
    }
    Ok(())
}

fn usfm_to_osis(usfm: &str) -> Option<&'static str> {
    Some(match usfm {
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
        _ => return None,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn usfm_codes_normalize_to_osis() {
        assert_eq!(normalize_book_id("GEN"), "Gen");
        assert_eq!(normalize_book_id("2JN"), "2John");
        assert_eq!(normalize_book_id("Phlm.1.1"), "Phlm");
    }

    #[test]
    fn osis_refs_accept_single_and_range_forms() {
        assert!(valid_osis_ref("John.3.16"));
        assert!(valid_osis_ref("1Cor.8.1-1Cor.10.33"));
        assert!(!valid_osis_ref("John 3:16"));
        assert!(!valid_osis_ref("John.3"));
    }

    #[test]
    fn usfm_marker_detector_finds_raw_markup() {
        assert!(contains_raw_usfm_marker(r"hello \w word\w*"));
        assert!(!contains_raw_usfm_marker("plain text"));
    }

    #[test]
    fn record_book_identity_uses_passage_id_and_osis_ref() {
        let by_passage = json!({"passage_id": "scripture:Gen.1.1"});
        let by_ref = json!({"osis_ref": "Rev.22.21"});
        assert_eq!(record_book_id(&by_passage), Some("Gen".to_string()));
        assert_eq!(record_book_id(&by_ref), Some("Rev".to_string()));
    }
}
