use serde_json::{json, Map, Value as JsonValue};
use serde_yaml::Value as YamlValue;
use std::collections::{BTreeSet, HashSet};
use std::env;
use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader, Write};
use std::path::{Path, PathBuf};

type AnyResult<T> = Result<T, Box<dyn Error>>;

const REQUIRED_EXCLUDED: &[&str] = &[
    "FRT", "GLO", "Tob", "Jdt", "AddEsth", "Wis", "Sir", "Bar", "1Macc", "2Macc", "1Esd",
    "PrMan", "Ps151", "3Macc", "2Esd", "4Macc", "AddDan",
];

fn main() {
    if let Err(err) = run() {
        eprintln!("logos_fast_validators failed: {err}");
        std::process::exit(1);
    }
}

fn run() -> AnyResult<()> {
    let mut args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        return Err("missing command: expected jsonl-scan, canonical-scope, canonical-qa, or chunk-map".into());
    }
    let command = args.remove(0);
    match command.as_str() {
        "jsonl-scan" => jsonl_scan(&args),
        "canonical-scope" => canonical_scope(&args),
        "canonical-qa" => canonical_qa(&args),
        "chunk-map" => Err("chunk-map is intentionally deferred until T424-D".into()),
        "-h" | "--help" | "help" => {
            print_help();
            Ok(())
        }
        other => Err(format!("unknown command: {other}").into()),
    }
}

fn print_help() {
    println!("logos_fast_validators commands:");
    println!("  jsonl-scan [--translation-id ID] [--require-canon] [--summary-json PATH] FILE...");
    println!("  canonical-scope [--canon PATH] [--summary-json PATH] [FILE...]");
    println!("  canonical-qa [--summary-json PATH]");
    println!("  chunk-map  # deferred until T424-D");
}

fn jsonl_scan(args: &[String]) -> AnyResult<()> {
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
            value if value.starts_with('-') => return Err(format!("unknown jsonl-scan flag: {value}").into()),
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
                failures.push(format!("{}:{line_no}: JSONL row is not an object", path.display()));
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
        if require_canon && record.get("canon_profiles").is_none() {
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
        if let (Some(id), Some(passage_id)) = (rid, str_field(record, "passage_id")) {
            witnesses.push((id.to_string(), passage_id.to_string()));
        }
    }

    if let Some(actual) = str_field(record, "translation_id") {
        if actual != expected_translation {
            failures.push(format!(
                "{}:{line_no}: generated output translation_id {actual} != expected {expected_translation}",
                path.display()
            ));
        }
    }

    if let Some(relation_type) = str_field(record, "relation_type") {
        if relation_type != "editorial_cross_reference" {
            failures.push(format!(
                "{}:{line_no}: disallowed relation_type {relation_type}",
                path.display()
            ));
        }
    }
}

fn canonical_scope(args: &[String]) -> AnyResult<()> {
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
                failures.push(format!("{}:{line_no}: JSONL row is not an object", path.display()));
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
                Some(book) if excluded_set.contains(book.as_str()) || !canonical_set.contains(book.as_str()) => {
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

fn canonical_qa(args: &[String]) -> AnyResult<()> {
    let mut summary_json: Option<PathBuf> = None;
    let mut index = 0;
    while index < args.len() {
        match args[index].as_str() {
            "--summary-json" => {
                index += 1;
                summary_json = Some(PathBuf::from(
                    args.get(index).ok_or("--summary-json requires a value")?,
                ));
            }
            value if value.starts_with('-') => return Err(format!("unknown canonical-qa flag: {value}").into()),
            value => return Err(format!("canonical-qa does not accept positional path yet: {value}").into()),
        }
        index += 1;
    }
    let summary = json!({
        "validator": "logos_fast_validators canonical-qa",
        "status": "scaffold",
        "authoritative_validator": "scripts/qa_canonical_corpus.py",
        "non_authorizing": true,
    });
    emit_summary(summary_json.as_deref(), &summary)?;
    println!("canonical-qa scaffold present; Python qa_canonical_corpus.py remains authoritative.");
    Ok(())
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
        record.insert("passage_id".to_string(), JsonValue::String("scripture:2JN.1.1".to_string()));
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
