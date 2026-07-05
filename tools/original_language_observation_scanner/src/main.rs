use roxmltree::{Document, Node};
use serde::Deserialize;
use serde_json::{json, Value as JsonValue};
use serde_yaml::Value as YamlValue;
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};
use std::env;
use std::fs::{self, File};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::{Path, PathBuf};

const SCHEMA_VERSION: &str = "original_language_observation_scanner.v1";
const TASK_ID: &str = "T435";
const SOURCE_ID: &str = "sblgnt";
const LANGUAGE: &str = "greek";
const SCANNER: &str = "tools/original_language_observation_scanner";
const SCANNER_VERSION: &str = "0.1.0";

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

#[derive(Debug)]
struct ScanArgs {
    source_view: PathBuf,
    manifest: PathBuf,
    included: PathBuf,
    out: PathBuf,
    no_authority: bool,
    no_text: bool,
    book: Option<String>,
    refs: Option<RefFilter>,
    shadow_t433: Option<PathBuf>,
}

#[derive(Debug, Clone)]
struct RefFilter {
    book_id: String,
    start_chapter: u32,
    start_verse: u32,
    end_chapter: u32,
    end_verse: u32,
    raw: String,
}

#[derive(Debug, Clone, Deserialize)]
struct IncludedRow {
    book_id: String,
    classification: String,
    contains_source_provided_lemmas: bool,
    contains_source_provided_morphology: bool,
    contains_source_provided_strongs: bool,
    sha256: String,
    size_bytes: usize,
    source_archive_path: String,
    view_path: String,
}

#[derive(Debug, Default, Clone)]
struct VerseStats {
    book_id: String,
    osis_ref: String,
    chapter: u32,
    verse: u32,
    token_count: usize,
    first_token_index: Option<usize>,
    last_token_index: Option<usize>,
    editorial_shape_count: usize,
}

#[derive(Debug, Default, Clone)]
struct BookTotals {
    verse_count: usize,
    token_count: usize,
    paragraph_count: usize,
    title_count: usize,
    nonempty_prefix_count: usize,
    nonempty_suffix_count: usize,
    editorial_shape_count: usize,
    bytes_read: usize,
    char_count: usize,
    line_count: usize,
}

fn main() {
    if let Err(exc) = run() {
        eprintln!("original_language_observation_scanner failed: {exc}");
        std::process::exit(1);
    }
}

fn run() -> Result<()> {
    let args = parse_args()?;
    scan_sblgnt(args)
}

fn parse_args() -> Result<ScanArgs> {
    let mut iter = env::args().skip(1);
    let command = iter.next().ok_or("expected command: scan-sblgnt")?;
    if command != "scan-sblgnt" {
        return Err(format!("unsupported command {command:?}; expected scan-sblgnt").into());
    }

    let mut source_view = None;
    let mut manifest = None;
    let mut included = None;
    let mut out = None;
    let mut no_authority = false;
    let mut no_text = false;
    let mut book = None;
    let mut refs = None;
    let mut shadow_t433 = None;

    while let Some(flag) = iter.next() {
        match flag.as_str() {
            "--source-view" => {
                source_view = Some(PathBuf::from(
                    iter.next().ok_or("--source-view requires a value")?,
                ))
            }
            "--manifest" => {
                manifest = Some(PathBuf::from(
                    iter.next().ok_or("--manifest requires a value")?,
                ))
            }
            "--included" => {
                included = Some(PathBuf::from(
                    iter.next().ok_or("--included requires a value")?,
                ))
            }
            "--out" => out = Some(PathBuf::from(iter.next().ok_or("--out requires a value")?)),
            "--no-authority" => no_authority = true,
            "--no-text" => no_text = true,
            "--book" => book = Some(iter.next().ok_or("--book requires a value")?),
            "--refs" => {
                refs = Some(parse_ref_filter(
                    &iter.next().ok_or("--refs requires a value")?,
                )?)
            }
            "--shadow-t433" => {
                shadow_t433 = Some(PathBuf::from(
                    iter.next().ok_or("--shadow-t433 requires a value")?,
                ))
            }
            other => return Err(format!("unknown argument {other:?}").into()),
        }
    }

    if !no_authority {
        return Err(
            "--no-authority is required; T435-A observations cannot authorize downstream truth"
                .into(),
        );
    }
    if !no_text {
        return Err("--no-text is required; T435-A ledgers must not emit source text".into());
    }
    if let (Some(book_id), Some(filter)) = (&book, &refs) {
        if book_id != &filter.book_id {
            return Err(format!("--book {book_id} does not match --refs {}", filter.raw).into());
        }
    }

    Ok(ScanArgs {
        source_view: source_view.ok_or("--source-view is required")?,
        manifest: manifest.ok_or("--manifest is required")?,
        included: included.ok_or("--included is required")?,
        out: out.ok_or("--out is required")?,
        no_authority,
        no_text,
        book,
        refs,
        shadow_t433,
    })
}

fn parse_ref_filter(raw: &str) -> Result<RefFilter> {
    let (start, end) = raw
        .split_once('-')
        .ok_or("--refs must use span form, for example Phlm.1.1-Phlm.1.3")?;
    let (book_id, start_chapter, start_verse) = parse_osis(start)?;
    let (end_book, end_chapter, end_verse) = parse_osis(end)?;
    if book_id != end_book {
        return Err("--refs must stay inside one book".into());
    }
    Ok(RefFilter {
        book_id,
        start_chapter,
        start_verse,
        end_chapter,
        end_verse,
        raw: raw.to_string(),
    })
}

fn parse_osis(raw: &str) -> Result<(String, u32, u32)> {
    let parts: Vec<&str> = raw.split('.').collect();
    if parts.len() != 3 {
        return Err(format!("invalid OSIS ref {raw:?}").into());
    }
    Ok((
        parts[0].to_string(),
        parts[1].parse::<u32>()?,
        parts[2].parse::<u32>()?,
    ))
}

fn scan_sblgnt(args: ScanArgs) -> Result<()> {
    fs::create_dir_all(&args.out)?;

    let manifest = read_yaml(&args.manifest)?;
    let source_manifest_path = string_field(&manifest, "source_manifest")?;
    let source_archive = string_field(&manifest, "source_archive")?;
    let source_archive_sha256 = string_field(&manifest, "source_archive_sha256")?;
    let expected_book_count = usize_field(&manifest, "expected_book_count")?;
    let book_scope = string_sequence(&manifest, "book_scope")?;
    let source_manifest = read_yaml(Path::new(&source_manifest_path))?;
    let license = string_field(&source_manifest, "license")?;
    let source_url = string_field(&source_manifest, "source_url")?;
    let version_or_commit = string_field(&source_manifest, "resolved_commit")?;

    let mut included_rows = read_included_rows(&args.included)?;
    included_rows.sort_by_key(|row| {
        book_scope
            .iter()
            .position(|book| book == &row.book_id)
            .unwrap_or(usize::MAX)
    });

    let mut file_rows = Vec::new();
    let mut verse_rows = Vec::new();
    let mut token_rows = Vec::new();
    let mut editorial_rows = Vec::new();
    let mut scanned_books = BTreeSet::new();

    for row in &included_rows {
        if let Some(book_filter) = &args.book {
            if book_filter != &row.book_id {
                continue;
            }
        }
        let path = Path::new(&row.view_path);
        if !path.starts_with(&args.source_view) {
            return Err(format!(
                "{} is outside --source-view {}",
                row.view_path,
                normalize_path(&args.source_view)
            )
            .into());
        }
        if row.classification != "included_canonical_bible_text" {
            return Err(format!(
                "{} is not an included canonical Bible text row",
                row.view_path
            )
            .into());
        }
        if row.contains_source_provided_strongs
            || row.contains_source_provided_lemmas
            || row.contains_source_provided_morphology
        {
            return Err("T435-A SBLGNT scanner expects no source-provided Strong's, lemma, or morphology fields".into());
        }
        let bytes = fs::read(path)?;
        let actual_sha = sha256_hex(&bytes);
        if actual_sha != row.sha256 {
            return Err(format!(
                "{} checksum mismatch: {} != {}",
                row.view_path, actual_sha, row.sha256
            )
            .into());
        }
        let text = String::from_utf8(bytes.clone())?;
        let doc = Document::parse(&text)?;
        let mut book_totals = BookTotals {
            bytes_read: bytes.len(),
            char_count: text.chars().count(),
            line_count: text.lines().count(),
            ..BookTotals::default()
        };
        let before_verses = verse_rows.len();
        let before_tokens = token_rows.len();
        let before_editorial = editorial_rows.len();
        scan_book_xml(
            row,
            &doc,
            &args,
            &license,
            &source_manifest_path,
            &mut book_totals,
            &mut verse_rows,
            &mut token_rows,
            &mut editorial_rows,
        )?;
        if verse_rows.len() > before_verses {
            scanned_books.insert(row.book_id.clone());
            file_rows.push(file_observation_row(
                row,
                &book_totals,
                &source_manifest_path,
                &source_archive,
                &source_archive_sha256,
                &license,
                &source_url,
                &version_or_commit,
                verse_rows.len() - before_verses,
                token_rows.len() - before_tokens,
                editorial_rows.len() - before_editorial,
            ));
        }
    }

    let output_files = vec![
        "scan_manifest.json",
        "source_view_file_observations.jsonl",
        "verse_token_observations.jsonl",
        "source_token_shape_index.jsonl",
        "editorial_layer_shape_index.jsonl",
        "t433_shadow_parity.json",
    ];

    write_jsonl(
        &args.out.join("source_view_file_observations.jsonl"),
        &file_rows,
    )?;
    write_jsonl(
        &args.out.join("verse_token_observations.jsonl"),
        &verse_rows,
    )?;
    write_jsonl(
        &args.out.join("source_token_shape_index.jsonl"),
        &token_rows,
    )?;
    write_jsonl(
        &args.out.join("editorial_layer_shape_index.jsonl"),
        &editorial_rows,
    )?;
    let parity = shadow_parity(&args, &token_rows, &editorial_rows)?;
    write_pretty_json(&args.out.join("t433_shadow_parity.json"), &parity)?;
    write_scan_manifest(
        &args,
        &output_files,
        &manifest,
        expected_book_count,
        scanned_books.len(),
        &file_rows,
        &verse_rows,
        &token_rows,
        &editorial_rows,
        &parity,
    )?;

    println!(
        "T435-A SBLGNT observation scan wrote {} book rows, {} verse rows, {} token-shape rows, {} editorial-shape rows to {}",
        file_rows.len(),
        verse_rows.len(),
        token_rows.len(),
        editorial_rows.len(),
        normalize_path(&args.out)
    );
    Ok(())
}

#[allow(clippy::too_many_arguments)]
fn scan_book_xml(
    row: &IncludedRow,
    doc: &Document,
    args: &ScanArgs,
    license: &str,
    source_manifest_path: &str,
    totals: &mut BookTotals,
    verse_rows: &mut Vec<JsonValue>,
    token_rows: &mut Vec<JsonValue>,
    editorial_rows: &mut Vec<JsonValue>,
) -> Result<()> {
    totals.title_count = doc
        .descendants()
        .filter(|node| node.has_tag_name("title"))
        .count();
    add_paragraph_observations(
        row,
        doc,
        args,
        license,
        source_manifest_path,
        totals,
        editorial_rows,
    )?;

    let mut current_ref: Option<String> = None;
    let mut verse_stats: BTreeMap<String, VerseStats> = BTreeMap::new();
    let mut verse_order = Vec::new();
    let mut token_index = 0usize;
    let mut verse_token_counts: BTreeMap<String, usize> = BTreeMap::new();
    let mut last_token_shape_id_by_ref: BTreeMap<String, String> = BTreeMap::new();

    for node in doc.descendants() {
        if node.has_tag_name("verse-number") {
            let Some(osis_ref) = verse_number_to_osis(&row.book_id, &node)? else {
                current_ref = None;
                continue;
            };
            if ref_allowed(&osis_ref, args.refs.as_ref())? {
                let (_, chapter, verse) = parse_osis(&osis_ref)?;
                current_ref = Some(osis_ref.clone());
                if !verse_stats.contains_key(&osis_ref) {
                    verse_order.push(osis_ref.clone());
                    verse_stats.insert(
                        osis_ref.clone(),
                        VerseStats {
                            book_id: row.book_id.clone(),
                            osis_ref: osis_ref.clone(),
                            chapter,
                            verse,
                            ..VerseStats::default()
                        },
                    );
                }
                let shape_row = editorial_shape_row(
                    row,
                    "versification",
                    "verse-number",
                    &osis_ref,
                    node.text().unwrap_or(""),
                    None,
                    license,
                    source_manifest_path,
                    editorial_rows.len(),
                );
                editorial_rows.push(shape_row);
                if let Some(stats) = verse_stats.get_mut(&osis_ref) {
                    stats.editorial_shape_count += 1;
                }
                totals.editorial_shape_count += 1;
            } else {
                current_ref = None;
            }
            continue;
        }

        let Some(osis_ref) = current_ref.clone() else {
            continue;
        };
        if node.has_tag_name("w") {
            let text = node.text().unwrap_or("");
            let verse_token_index = verse_token_counts.entry(osis_ref.clone()).or_insert(0);
            *verse_token_index += 1;
            let source_token_shape_id = format!(
                "sblgnt:{}:{}:{:06}",
                row.book_id, osis_ref, *verse_token_index
            );
            token_rows.push(token_shape_row(
                row,
                &osis_ref,
                &source_token_shape_id,
                token_index,
                *verse_token_index,
                text,
                license,
                source_manifest_path,
            ));
            last_token_shape_id_by_ref.insert(osis_ref.clone(), source_token_shape_id);
            let stats = verse_stats
                .get_mut(&osis_ref)
                .ok_or("source token encountered before verse stats")?;
            stats.token_count += 1;
            stats.first_token_index.get_or_insert(token_index);
            stats.last_token_index = Some(token_index);
            token_index += 1;
            totals.token_count += 1;
        } else if node.has_tag_name("prefix") || node.has_tag_name("suffix") {
            let marker_content = node.text().unwrap_or("");
            if marker_content.is_empty() {
                continue;
            }
            if node.has_tag_name("prefix") {
                totals.nonempty_prefix_count += 1;
            } else {
                totals.nonempty_suffix_count += 1;
            }
            let applies_to = if node.has_tag_name("suffix") {
                last_token_shape_id_by_ref.get(&osis_ref).cloned()
            } else {
                None
            };
            editorial_rows.push(editorial_shape_row(
                row,
                "punctuation",
                node.tag_name().name(),
                &osis_ref,
                marker_content,
                applies_to.as_deref(),
                license,
                source_manifest_path,
                editorial_rows.len(),
            ));
            if let Some(stats) = verse_stats.get_mut(&osis_ref) {
                stats.editorial_shape_count += 1;
            }
            totals.editorial_shape_count += 1;
        }
    }

    for osis_ref in verse_order {
        let stats = verse_stats
            .remove(&osis_ref)
            .ok_or("verse order referenced missing stats")?;
        verse_rows.push(verse_observation_row(
            row,
            &stats,
            license,
            source_manifest_path,
        ));
    }
    totals.verse_count = verse_rows
        .iter()
        .filter(|item| {
            item.get("book_id").and_then(JsonValue::as_str) == Some(row.book_id.as_str())
        })
        .count();
    Ok(())
}

fn add_paragraph_observations(
    row: &IncludedRow,
    doc: &Document,
    args: &ScanArgs,
    license: &str,
    source_manifest_path: &str,
    totals: &mut BookTotals,
    editorial_rows: &mut Vec<JsonValue>,
) -> Result<()> {
    for paragraph in doc.descendants().filter(|node| node.has_tag_name("p")) {
        let mut refs = Vec::new();
        for verse_node in paragraph
            .descendants()
            .filter(|node| node.has_tag_name("verse-number"))
        {
            let Some(osis_ref) = verse_number_to_osis(&row.book_id, &verse_node)? else {
                continue;
            };
            if ref_allowed(&osis_ref, args.refs.as_ref())? {
                refs.push(osis_ref);
            }
        }
        if refs.is_empty() {
            continue;
        }
        totals.paragraph_count += 1;
        let span_ref = if refs.len() == 1 {
            refs[0].clone()
        } else {
            format!("{}-{}", refs.first().unwrap(), refs.last().unwrap())
        };
        editorial_rows.push(editorial_shape_row(
            row,
            "paragraphing",
            "p",
            &span_ref,
            "",
            None,
            license,
            source_manifest_path,
            editorial_rows.len(),
        ));
        totals.editorial_shape_count += 1;
    }
    Ok(())
}

fn verse_number_to_osis(book_id: &str, node: &Node) -> Result<Option<String>> {
    let Some(id) = node.attribute("id") else {
        return Ok(None);
    };
    let Some((_, chapter_verse)) = id.rsplit_once(' ') else {
        return Ok(None);
    };
    let Some((chapter, verse)) = chapter_verse.split_once(':') else {
        return Ok(None);
    };
    Ok(Some(format!("{book_id}.{chapter}.{verse}")))
}

fn ref_allowed(osis_ref: &str, filter: Option<&RefFilter>) -> Result<bool> {
    let Some(filter) = filter else {
        return Ok(true);
    };
    let (book, chapter, verse) = parse_osis(osis_ref)?;
    if book != filter.book_id {
        return Ok(false);
    }
    let current = (chapter, verse);
    let start = (filter.start_chapter, filter.start_verse);
    let end = (filter.end_chapter, filter.end_verse);
    Ok(current >= start && current <= end)
}

#[allow(clippy::too_many_arguments)]
fn file_observation_row(
    row: &IncludedRow,
    totals: &BookTotals,
    source_manifest_path: &str,
    source_archive: &str,
    source_archive_sha256: &str,
    license: &str,
    source_url: &str,
    version_or_commit: &str,
    verse_count: usize,
    token_count: usize,
    editorial_shape_count: usize,
) -> JsonValue {
    json!({
        "id": format!("t435:file-observation:sblgnt:{}", row.book_id),
        "type": "SblgntSourceViewFileObservation",
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "source_id": SOURCE_ID,
        "source_manifest": source_manifest_path,
        "canonical_source_view_manifest": "data/candidate/original_language_evidence/canonical_source_views/sblgnt/canonical_source_view_manifest.yaml",
        "source_archive_path": row.source_archive_path,
        "source_archive": source_archive,
        "source_archive_sha256": source_archive_sha256,
        "source_view_path": row.view_path,
        "source_file_sha256": row.sha256,
        "license": license,
        "source_url": source_url,
        "version_or_commit": version_or_commit,
        "language": LANGUAGE,
        "book_id": row.book_id,
        "classification": row.classification,
        "bytes_read": totals.bytes_read,
        "size_bytes_from_included_ledger": row.size_bytes,
        "char_count": totals.char_count,
        "line_count": totals.line_count,
        "title_count": totals.title_count,
        "paragraph_count": totals.paragraph_count,
        "verse_count": verse_count,
        "token_shape_count": token_count,
        "editorial_shape_count": editorial_shape_count,
        "nonempty_prefix_count": totals.nonempty_prefix_count,
        "nonempty_suffix_count": totals.nonempty_suffix_count,
        "contains_source_provided_lemmas": false,
        "contains_source_provided_morphology": false,
        "contains_source_provided_strongs": false,
        "evidence_mode": "observed_source_view_shape",
        "inferred_vs_observed": "observed",
        "text_storage_policy": no_text_policy(),
        "trust_zone": "candidate",
        "status": "observation_shadow",
        "confidence": "high",
        "authority": authority(),
        "non_authorizations": non_authorizations()
    })
}

fn verse_observation_row(
    row: &IncludedRow,
    stats: &VerseStats,
    license: &str,
    source_manifest_path: &str,
) -> JsonValue {
    json!({
        "id": format!("t435:verse-token-observation:sblgnt:{}", stats.osis_ref),
        "type": "SblgntVerseTokenObservation",
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "source_id": SOURCE_ID,
        "source_manifest": source_manifest_path,
        "canonical_source_view_manifest": "data/candidate/original_language_evidence/canonical_source_views/sblgnt/canonical_source_view_manifest.yaml",
        "source_archive_path": row.source_archive_path,
        "source_view_path": row.view_path,
        "source_file_sha256": row.sha256,
        "license": license,
        "language": LANGUAGE,
        "book_id": stats.book_id,
        "osis_ref": stats.osis_ref,
        "chapter": stats.chapter,
        "verse": stats.verse,
        "token_shape_count": stats.token_count,
        "first_token_index": stats.first_token_index,
        "last_token_index": stats.last_token_index,
        "editorial_shape_count": stats.editorial_shape_count,
        "contains_source_provided_lemmas": false,
        "contains_source_provided_morphology": false,
        "contains_source_provided_strongs": false,
        "evidence_mode": "observed_source_view_shape",
        "inferred_vs_observed": "observed",
        "text_storage_policy": no_text_policy(),
        "trust_zone": "candidate",
        "status": "observation_shadow",
        "confidence": "high",
        "authority": authority(),
        "non_authorizations": non_authorizations()
    })
}

#[allow(clippy::too_many_arguments)]
fn token_shape_row(
    row: &IncludedRow,
    osis_ref: &str,
    source_token_shape_id: &str,
    token_index: usize,
    verse_token_index: usize,
    content: &str,
    license: &str,
    source_manifest_path: &str,
) -> JsonValue {
    json!({
        "id": format!("t435:source-token-shape:sblgnt:{}:{:06}", osis_ref, verse_token_index),
        "type": "SblgntSourceTokenShapeObservation",
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "source_id": SOURCE_ID,
        "source_manifest": source_manifest_path,
        "canonical_source_view_manifest": "data/candidate/original_language_evidence/canonical_source_views/sblgnt/canonical_source_view_manifest.yaml",
        "source_archive_path": row.source_archive_path,
        "source_view_path": row.view_path,
        "source_file_sha256": row.sha256,
        "license": license,
        "language": LANGUAGE,
        "book_id": row.book_id,
        "osis_ref": osis_ref,
        "source_token_shape_id": source_token_shape_id,
        "token_index": token_index,
        "verse_token_index": verse_token_index,
        "content_sha256_short": sha256_short(content.as_bytes()),
        "content_char_count": content.chars().count(),
        "content_byte_count": content.len(),
        "lemma": JsonValue::Null,
        "morphology": JsonValue::Null,
        "strong_id": JsonValue::Null,
        "contains_source_provided_lemmas": false,
        "contains_source_provided_morphology": false,
        "contains_source_provided_strongs": false,
        "evidence_mode": "observed_source_view_shape",
        "inferred_vs_observed": "observed",
        "text_storage_policy": no_text_policy(),
        "trust_zone": "candidate",
        "status": "observation_shadow",
        "confidence": "high",
        "authority": authority(),
        "non_authorizations": non_authorizations()
    })
}

#[allow(clippy::too_many_arguments)]
fn editorial_shape_row(
    row: &IncludedRow,
    layer_kind: &str,
    marker: &str,
    osis_ref: &str,
    content: &str,
    applies_to: Option<&str>,
    license: &str,
    source_manifest_path: &str,
    index: usize,
) -> JsonValue {
    json!({
        "id": format!("t435:editorial-shape:sblgnt:{}:{}:{:06}", osis_ref, marker, index + 1),
        "type": "SblgntEditorialShapeObservation",
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "layer_kind": layer_kind,
        "source_marker_or_field": marker,
        "source_id": SOURCE_ID,
        "source_manifest": source_manifest_path,
        "canonical_source_view_manifest": "data/candidate/original_language_evidence/canonical_source_views/sblgnt/canonical_source_view_manifest.yaml",
        "source_archive_path": row.source_archive_path,
        "source_view_path": row.view_path,
        "source_file_sha256": row.sha256,
        "license": license,
        "book_id": row.book_id,
        "osis_ref": osis_ref,
        "applies_to_source_token_shape_id": applies_to,
        "marker_content_sha256_short": if content.is_empty() { JsonValue::Null } else { json!(sha256_short(content.as_bytes())) },
        "marker_content_char_count": content.chars().count(),
        "marker_content_byte_count": content.len(),
        "editorial_origin": "source_edition",
        "is_editorial_not_autograph_certainty": true,
        "evidence_mode": "observed_source_view_shape",
        "inferred_vs_observed": "observed",
        "text_storage_policy": no_text_policy(),
        "trust_zone": "candidate",
        "status": "observation_shadow",
        "confidence": "high",
        "authority": editorial_authority(),
        "non_authorizations": non_authorizations()
    })
}

fn shadow_parity(
    args: &ScanArgs,
    token_rows: &[JsonValue],
    editorial_rows: &[JsonValue],
) -> Result<JsonValue> {
    let Some(root) = &args.shadow_t433 else {
        return Ok(json!({
            "object_type": "t433_shadow_parity",
            "schema_version": SCHEMA_VERSION,
            "status": "not_run",
            "reason": "--shadow-t433 not provided",
            "authority": authority(),
            "non_authorizations": non_authorizations()
        }));
    };
    let manifest = read_yaml(&root.join("manifest.yaml"))?;
    let expected_tokens = usize_field_path(&manifest, &["counts", "source_language_tokens"])?;
    let expected_editorial = usize_field_path(&manifest, &["counts", "editorial_layers"])?;
    let refs = ["Phlm.1.1", "Phlm.1.2", "Phlm.1.3"];
    let rust_tokens = token_rows
        .iter()
        .filter(|row| {
            refs.contains(
                &row.get("osis_ref")
                    .and_then(JsonValue::as_str)
                    .unwrap_or(""),
            )
        })
        .count();
    let rust_editorial = editorial_rows
        .iter()
        .filter(|row| {
            let osis_ref = row
                .get("osis_ref")
                .and_then(JsonValue::as_str)
                .unwrap_or("");
            refs.contains(&osis_ref) || osis_ref == "Phlm.1.1-Phlm.1.3"
        })
        .count();
    let status = if rust_tokens == expected_tokens && rust_editorial == expected_editorial {
        "pass"
    } else {
        "fail"
    };
    Ok(json!({
        "object_type": "t433_shadow_parity",
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "compared_span": "Phlm.1.1-Phlm.1.3",
        "rust_source_token_shapes": rust_tokens,
        "t433_source_language_tokens": expected_tokens,
        "rust_editorial_shapes": rust_editorial,
        "t433_editorial_layers": expected_editorial,
        "same_scope": true,
        "note": "Rust T435-A compares no-text observed SBLGNT shape counts against T433 candidate pilot row counts; it does not replace T433 rows or authorize alignment truth.",
        "authority": authority(),
        "non_authorizations": non_authorizations()
    }))
}

#[allow(clippy::too_many_arguments)]
fn write_scan_manifest(
    args: &ScanArgs,
    output_files: &[&str],
    manifest: &YamlValue,
    expected_book_count: usize,
    scanned_book_count: usize,
    file_rows: &[JsonValue],
    verse_rows: &[JsonValue],
    token_rows: &[JsonValue],
    editorial_rows: &[JsonValue],
    parity: &JsonValue,
) -> Result<()> {
    let payload = json!({
        "object_type": "t435_sblgnt_observation_scan_manifest",
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "scanner": SCANNER,
        "scanner_version": SCANNER_VERSION,
        "command": "scan-sblgnt",
        "source_id": SOURCE_ID,
        "language": LANGUAGE,
        "source_view": normalize_path(&args.source_view),
        "canonical_source_view_manifest": normalize_path(&args.manifest),
        "included_files": normalize_path(&args.included),
        "source_manifest": string_field(manifest, "source_manifest")?,
        "source_archive": string_field(manifest, "source_archive")?,
        "source_archive_sha256": string_field(manifest, "source_archive_sha256")?,
        "source_view_status": string_field(manifest, "status")?,
        "scan_scope": {
            "book": args.book,
            "refs": args.refs.as_ref().map(|filter| filter.raw.clone()),
        },
        "no_authority": args.no_authority,
        "no_text": args.no_text,
        "expected_book_count": expected_book_count,
        "scanned_book_count": scanned_book_count,
        "row_counts": {
            "source_view_file_observations": file_rows.len(),
            "verse_token_observations": verse_rows.len(),
            "source_token_shape_index": token_rows.len(),
            "editorial_layer_shape_index": editorial_rows.len(),
        },
        "output_files": output_files,
        "t433_shadow_parity_status": parity.get("status").and_then(JsonValue::as_str).unwrap_or("unknown"),
        "evidence_mode": "observed_source_view_shape",
        "trust_zone": "candidate",
        "status": "observation_shadow",
        "text_storage_policy": no_text_policy(),
        "authority": authority(),
        "non_authorizations": non_authorizations()
    });
    write_pretty_json(&args.out.join("scan_manifest.json"), &payload)
}

fn read_yaml(path: &Path) -> Result<YamlValue> {
    let text = fs::read_to_string(path)?;
    Ok(serde_yaml::from_str(&text)?)
}

fn read_included_rows(path: &Path) -> Result<Vec<IncludedRow>> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let mut rows = Vec::new();
    for line in reader.lines() {
        let line = line?;
        if line.trim().is_empty() {
            continue;
        }
        rows.push(serde_json::from_str::<IncludedRow>(&line)?);
    }
    Ok(rows)
}

fn string_field(value: &YamlValue, key: &str) -> Result<String> {
    value
        .get(key)
        .and_then(YamlValue::as_str)
        .map(ToString::to_string)
        .ok_or_else(|| format!("manifest field {key:?} must be a string").into())
}

fn usize_field(value: &YamlValue, key: &str) -> Result<usize> {
    value
        .get(key)
        .and_then(YamlValue::as_i64)
        .and_then(|item| usize::try_from(item).ok())
        .ok_or_else(|| format!("manifest field {key:?} must be a non-negative integer").into())
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

fn sha256_hex(bytes: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    hex::encode(hasher.finalize())
}

fn sha256_short(bytes: &[u8]) -> String {
    sha256_hex(bytes).chars().take(16).collect()
}

fn normalize_path(path: &Path) -> String {
    path.to_string_lossy().replace('\\', "/")
}

fn no_text_policy() -> JsonValue {
    json!({
        "stores_source_text": false,
        "stores_manuscript_transcription": false,
        "stores_manuscript_image": false,
        "no_text": true,
        "storage_note": "T435-A stores observed shape counts, offsets, hashes, and lineage only; no source wording is emitted."
    })
}

fn authority() -> JsonValue {
    json!({
        "authorizes_source_language_truth": false,
        "authorizes_lexical_truth": false,
        "authorizes_word_level_alignment_truth": false,
        "authorizes_strongs_as_source_text": false,
        "authorizes_preferred_reading": false,
        "authorizes_source_tradition_preference": false,
        "authorizes_textual_critical_decision": false,
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

fn editorial_authority() -> JsonValue {
    json!({
        "authorizes_autograph_certainty": false,
        "authorizes_speaker_resolution": false,
        "authorizes_source_language_truth": false,
        "authorizes_preferred_reading": false,
        "authorizes_source_tradition_preference": false,
        "authorizes_chunk_boundary": false,
        "authorizes_theology_authority": false
    })
}

fn non_authorizations() -> Vec<&'static str> {
    vec![
        "source_language_truth",
        "lexical_truth",
        "word_level_alignment_truth",
        "strongs_number_as_source_text",
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
    fn parses_span_filter() {
        let filter = parse_ref_filter("Phlm.1.1-Phlm.1.3").expect("span parses");
        assert_eq!(filter.book_id, "Phlm");
        assert!(ref_allowed("Phlm.1.2", Some(&filter)).unwrap());
        assert!(!ref_allowed("Phlm.1.4", Some(&filter)).unwrap());
    }

    #[test]
    fn sblgnt_phlm_fixture_counts_match_t433_shape() {
        let xml = r#"<book id="Phm"><title>ΠΡΟΣ ΦΙΛΗΜΟΝΑ</title><p><verse-number id="Philemon 1:1">1:1</verse-number><w>Παῦλος</w><suffix></suffix><w>δέσμιος</w><suffix></suffix><verse-number id="Philemon 1:2">2</verse-number><prefix> ⸀</prefix><w>ἀδελφῇ</w><suffix>· </suffix><verse-number id="Philemon 1:3">3</verse-number><w>χάρις</w><suffix>. </suffix></p></book>"#;
        let doc = Document::parse(xml).expect("fixture XML parses");
        let row = IncludedRow {
            book_id: "Phlm".to_string(),
            classification: "included_canonical_bible_text".to_string(),
            contains_source_provided_lemmas: false,
            contains_source_provided_morphology: false,
            contains_source_provided_strongs: false,
            sha256: "fixture".to_string(),
            size_bytes: xml.len(),
            source_archive_path: "archive/Phlm.xml".to_string(),
            view_path: "data/candidate/original_language_evidence/canonical_source_views/sblgnt/files/Phlm.xml".to_string(),
        };
        let args = ScanArgs {
            source_view: PathBuf::from(
                "data/candidate/original_language_evidence/canonical_source_views/sblgnt",
            ),
            manifest: PathBuf::from("manifest.yaml"),
            included: PathBuf::from("included_files.jsonl"),
            out: PathBuf::from("build/test"),
            no_authority: true,
            no_text: true,
            book: Some("Phlm".to_string()),
            refs: Some(parse_ref_filter("Phlm.1.1-Phlm.1.3").unwrap()),
            shadow_t433: None,
        };
        let mut totals = BookTotals::default();
        let mut verse_rows = Vec::new();
        let mut token_rows = Vec::new();
        let mut editorial_rows = Vec::new();
        scan_book_xml(
            &row,
            &doc,
            &args,
            "CC-BY-4.0",
            "data/raw/original_language/greek/sblgnt/source_manifest.yaml",
            &mut totals,
            &mut verse_rows,
            &mut token_rows,
            &mut editorial_rows,
        )
        .expect("fixture scans");

        assert_eq!(verse_rows.len(), 3);
        assert_eq!(token_rows.len(), 4);
        assert_eq!(editorial_rows.len(), 7);
        assert!(token_rows
            .iter()
            .all(|row| row.get("strong_id") == Some(&JsonValue::Null)));
    }

    #[test]
    fn token_rows_do_not_emit_source_wording() {
        let row = IncludedRow {
            book_id: "Phlm".to_string(),
            classification: "included_canonical_bible_text".to_string(),
            contains_source_provided_lemmas: false,
            contains_source_provided_morphology: false,
            contains_source_provided_strongs: false,
            sha256: "fixture".to_string(),
            size_bytes: 10,
            source_archive_path: "archive/Phlm.xml".to_string(),
            view_path: "data/candidate/original_language_evidence/canonical_source_views/sblgnt/files/Phlm.xml".to_string(),
        };
        let payload = token_shape_row(
            &row,
            "Phlm.1.1",
            "sblgnt:Phlm:Phlm.1.1:000001",
            0,
            1,
            "Παῦλος",
            "CC-BY-4.0",
            "data/raw/original_language/greek/sblgnt/source_manifest.yaml",
        );
        assert!(payload.get("surface_text").is_none());
        assert!(payload.get("normalized_text").is_none());
        assert_eq!(payload["content_char_count"], 6);
        assert_eq!(payload["text_storage_policy"]["stores_source_text"], false);
    }
}
