use serde_json::json;
use serde_yaml::Value as YamlValue;
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};
use std::env;
use std::fs::{self, File};
use std::io::{BufWriter, Cursor, Read, Write};
use std::path::{Path, PathBuf};
use zip::ZipArchive;

const SCHEMA_VERSION: &str = "rust_observation_substrate.v1";
const SCANNER: &str = "tools/usfm_observation_scanner";
const SCANNER_VERSION: &str = "0.1.0";

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

#[derive(Debug)]
struct ScanArgs {
    source: PathBuf,
    canon: PathBuf,
    marker_coverage: PathBuf,
    book_genres: PathBuf,
    out: PathBuf,
    no_text: bool,
}

#[derive(Debug, Default, Clone)]
struct BookObservation {
    book_id: String,
    usfm_code: String,
    source_entry: String,
    source_class: String,
    sha256_short: String,
    bytes_read: usize,
    char_count: usize,
    line_count: usize,
    chapter_count: usize,
    verse_count: usize,
    marker_counts: BTreeMap<String, usize>,
    strong_h_count: usize,
    strong_g_count: usize,
    feature_flags: BTreeSet<String>,
}

#[derive(Debug, Clone)]
struct VerseObservation {
    book_id: String,
    osis_ref: String,
    chapter: u32,
    verse: u32,
    source_entry: String,
    source_line_start: usize,
    source_line_end: usize,
    marker_counts: BTreeMap<String, usize>,
    strong_ids: BTreeSet<String>,
    feature_flags: BTreeSet<String>,
}

#[derive(Debug, Clone)]
struct ChapterSpan {
    book_id: String,
    chapter: u32,
    start_verse: u32,
    end_verse: u32,
    verse_count: usize,
    marker_counts: BTreeMap<String, usize>,
    risk_flags: BTreeSet<String>,
}

#[derive(Debug, Clone)]
struct RiskSignal {
    signal_id: String,
    book_id: String,
    osis_ref: String,
    signal_kind: String,
    evidence_markers: Vec<String>,
}

#[derive(Debug, Clone)]
struct MarkerAnomaly {
    anomaly_id: String,
    source_entry: String,
    book_id: String,
    marker: String,
    reason: String,
}

fn main() {
    if let Err(exc) = run() {
        eprintln!("usfm_observation_scanner failed: {exc}");
        std::process::exit(1);
    }
}

fn run() -> Result<()> {
    let args = parse_args()?;
    scan(args)
}

fn parse_args() -> Result<ScanArgs> {
    let mut iter = env::args().skip(1);
    let command = iter.next().ok_or("expected command: scan")?;
    if command != "scan" {
        return Err(format!("unsupported command {command:?}; expected scan").into());
    }

    let mut source = None;
    let mut canon = None;
    let mut marker_coverage = None;
    let mut book_genres = None;
    let mut out = None;
    let mut no_text = false;

    while let Some(flag) = iter.next() {
        match flag.as_str() {
            "--source" => source = Some(PathBuf::from(iter.next().ok_or("--source requires a value")?)),
            "--canon" => canon = Some(PathBuf::from(iter.next().ok_or("--canon requires a value")?)),
            "--marker-coverage" => {
                marker_coverage = Some(PathBuf::from(iter.next().ok_or("--marker-coverage requires a value")?))
            }
            "--book-genres" => book_genres = Some(PathBuf::from(iter.next().ok_or("--book-genres requires a value")?)),
            "--out" => out = Some(PathBuf::from(iter.next().ok_or("--out requires a value")?)),
            "--no-text" => no_text = true,
            other => return Err(format!("unknown argument {other:?}").into()),
        }
    }

    if !no_text {
        return Err("--no-text is required; T412 ledgers must not emit Bible text".into());
    }

    Ok(ScanArgs {
        source: source.ok_or("--source is required")?,
        canon: canon.ok_or("--canon is required")?,
        marker_coverage: marker_coverage.ok_or("--marker-coverage is required")?,
        book_genres: book_genres.ok_or("--book-genres is required")?,
        out: out.ok_or("--out is required")?,
        no_text,
    })
}

fn scan(args: ScanArgs) -> Result<()> {
    fs::create_dir_all(&args.out)?;

    let canonical_books = read_canonical_books(&args.canon)?;
    let canonical_book_set: BTreeSet<String> = canonical_books.iter().cloned().collect();
    let known_markers = read_marker_registry(&args.marker_coverage)?;
    let genres = read_book_genres(&args.book_genres)?;
    let source_bytes = fs::read(&args.source)?;
    let source_sha256_short = sha256_short(&source_bytes);
    let source_path = normalize_path(&args.source);

    let mut archive = ZipArchive::new(Cursor::new(source_bytes.clone()))?;
    let mut entries = Vec::new();
    for index in 0..archive.len() {
        let file = archive.by_index(index)?;
        let name = file.name().to_string();
        if name.to_ascii_lowercase().ends_with(".usfm") || name.to_ascii_lowercase().ends_with(".sfm") {
            entries.push(name);
        }
    }
    entries.sort();

    let mut books = Vec::new();
    let mut verses = Vec::new();
    let mut spans: BTreeMap<(String, u32), ChapterSpan> = BTreeMap::new();
    let mut risk_signals = Vec::new();
    let mut strong_index: BTreeMap<(String, String, String), usize> = BTreeMap::new();
    let mut anomalies = Vec::new();

    for entry in &entries {
        let mut file = archive.by_name(entry)?;
        let mut bytes = Vec::new();
        file.read_to_end(&mut bytes)?;
        let text = String::from_utf8_lossy(&bytes).to_string();
        let (book, book_verses, book_anomalies) = scan_book(
            entry,
            &bytes,
            &text,
            &canonical_book_set,
            &known_markers,
            &genres,
        );
        for anomaly in book_anomalies {
            anomalies.push(anomaly);
        }
        for verse in &book_verses {
            let chapter_key = (verse.book_id.clone(), verse.chapter);
            let span = spans.entry(chapter_key).or_insert_with(|| ChapterSpan {
                book_id: verse.book_id.clone(),
                chapter: verse.chapter,
                start_verse: verse.verse,
                end_verse: verse.verse,
                verse_count: 0,
                marker_counts: BTreeMap::new(),
                risk_flags: BTreeSet::new(),
            });
            span.start_verse = span.start_verse.min(verse.verse);
            span.end_verse = span.end_verse.max(verse.verse);
            span.verse_count += 1;
            merge_counts(&mut span.marker_counts, &verse.marker_counts);
            for flag in &verse.feature_flags {
                if is_risk_flag(flag) {
                    span.risk_flags.insert(flag.clone());
                    risk_signals.push(RiskSignal {
                        signal_id: format!("{}-{}-{}", verse.osis_ref, flag, risk_signals.len() + 1),
                        book_id: verse.book_id.clone(),
                        osis_ref: verse.osis_ref.clone(),
                        signal_kind: flag.clone(),
                        evidence_markers: markers_for_flag(flag),
                    });
                }
            }
            for strong_id in &verse.strong_ids {
                let key = (strong_id.clone(), verse.book_id.clone(), verse.osis_ref.clone());
                *strong_index.entry(key).or_insert(0) += 1;
            }
        }
        verses.extend(book_verses);
        books.push(book);
    }

    let canonical_rank: BTreeMap<String, usize> = canonical_books
        .iter()
        .enumerate()
        .map(|(index, book)| (book.clone(), index))
        .collect();
    books.sort_by(|left, right| {
        canonical_rank
            .get(&left.book_id)
            .copied()
            .unwrap_or(usize::MAX)
            .cmp(&canonical_rank.get(&right.book_id).copied().unwrap_or(usize::MAX))
            .then(left.source_entry.cmp(&right.source_entry))
    });

    let output_files = vec![
        "scan_manifest.json",
        "book_observations.jsonl",
        "verse_observations.jsonl",
        "span_observation_features.jsonl",
        "risk_signal_index.jsonl",
        "strong_occurrence_index.jsonl",
        "marker_anomalies.jsonl",
    ];

    write_manifest(
        &args,
        &output_files,
        &source_path,
        &source_sha256_short,
        entries.len(),
        canonical_books.len(),
    )?;
    write_books(&args.out.join("book_observations.jsonl"), &books)?;
    write_verses(&args.out.join("verse_observations.jsonl"), &verses)?;
    write_spans(&args.out.join("span_observation_features.jsonl"), spans.values())?;
    write_risks(&args.out.join("risk_signal_index.jsonl"), &risk_signals)?;
    write_strongs(&args.out.join("strong_occurrence_index.jsonl"), &strong_index)?;
    write_anomalies(&args.out.join("marker_anomalies.jsonl"), &anomalies)?;

    println!(
        "Wrote no-text observation substrate: {} books, {} verses, {} source files -> {}",
        books.len(),
        verses.len(),
        entries.len(),
        args.out.display()
    );
    Ok(())
}

fn scan_book(
    entry: &str,
    bytes: &[u8],
    text: &str,
    canonical_books: &BTreeSet<String>,
    known_markers: &BTreeSet<String>,
    genres: &BTreeMap<String, String>,
) -> (BookObservation, Vec<VerseObservation>, Vec<MarkerAnomaly>) {
    let mut anomalies = Vec::new();
    let usfm_code = find_usfm_code(text).unwrap_or_else(|| {
        anomalies.push(MarkerAnomaly {
            anomaly_id: format!("{entry}:missing-id"),
            source_entry: entry.to_string(),
            book_id: "UNKNOWN".to_string(),
            marker: "id".to_string(),
            reason: "missing USFM id line".to_string(),
        });
        "UNKNOWN".to_string()
    });
    let book_id = usfm_to_osis(&usfm_code).unwrap_or(&usfm_code).to_string();
    let source_class = if canonical_books.contains(&book_id) {
        "canonical_66"
    } else {
        "excluded_or_appendix"
    };
    let mut book = BookObservation {
        book_id: book_id.clone(),
        usfm_code: usfm_code.clone(),
        source_entry: entry.to_string(),
        source_class: source_class.to_string(),
        sha256_short: sha256_short(bytes),
        bytes_read: bytes.len(),
        char_count: text.chars().count(),
        line_count: text.lines().count(),
        chapter_count: 0,
        verse_count: 0,
        marker_counts: BTreeMap::new(),
        strong_h_count: 0,
        strong_g_count: 0,
        feature_flags: BTreeSet::new(),
    };
    if let Some(genre) = genres.get(&book_id) {
        book.feature_flags.insert(format!("genre_{genre}"));
    }

    let mut verses = Vec::new();
    let mut current_chapter = 0_u32;
    let mut current: Option<VerseObservation> = None;

    for (zero_based_line, line) in text.lines().enumerate() {
        let line_no = zero_based_line + 1;
        let markers = markers_in_line(line);
        for marker in &markers {
            *book.marker_counts.entry(marker.clone()).or_insert(0) += 1;
            if !known_markers.contains(marker) {
                anomalies.push(MarkerAnomaly {
                    anomaly_id: format!("{entry}:{line_no}:{marker}"),
                    source_entry: entry.to_string(),
                    book_id: book_id.clone(),
                    marker: marker.clone(),
                    reason: "marker not declared in config/ingest/usfm_marker_coverage.yaml".to_string(),
                });
            }
        }

        if let Some(chapter) = parse_number_after_marker(line, "c") {
            current_chapter = chapter;
            book.chapter_count += 1;
        }

        if let Some(verse_number) = parse_number_after_marker(line, "v") {
            if let Some(prev) = current.take() {
                verses.push(prev);
            }
            current = Some(VerseObservation {
                book_id: book_id.clone(),
                osis_ref: format!("{book_id}.{current_chapter}.{verse_number}"),
                chapter: current_chapter,
                verse: verse_number,
                source_entry: entry.to_string(),
                source_line_start: line_no,
                source_line_end: line_no,
                marker_counts: BTreeMap::new(),
                strong_ids: BTreeSet::new(),
                feature_flags: BTreeSet::new(),
            });
            book.verse_count += 1;
        }

        let strong_ids = strong_ids_in_line(line);
        for strong_id in &strong_ids {
            if strong_id.starts_with('H') {
                book.strong_h_count += 1;
            } else if strong_id.starts_with('G') {
                book.strong_g_count += 1;
            }
        }

        for flag in feature_flags(&markers, &strong_ids, genres.get(&book_id)) {
            book.feature_flags.insert(flag);
        }

        if let Some(verse) = current.as_mut() {
            verse.source_line_end = line_no;
            for marker in &markers {
                *verse.marker_counts.entry(marker.clone()).or_insert(0) += 1;
            }
            for strong_id in strong_ids {
                verse.strong_ids.insert(strong_id);
            }
            for flag in feature_flags(&markers, &verse.strong_ids.iter().cloned().collect::<Vec<_>>(), genres.get(&book_id)) {
                verse.feature_flags.insert(flag);
            }
        }
    }

    if let Some(prev) = current.take() {
        verses.push(prev);
    }

    (book, verses, anomalies)
}

fn write_manifest(
    args: &ScanArgs,
    output_files: &[&str],
    source_path: &str,
    source_sha256_short: &str,
    source_file_count: usize,
    canonical_book_count: usize,
) -> Result<()> {
    let manifest = json!({
        "type": "RustObservationScanManifest",
        "schema_version": SCHEMA_VERSION,
        "scanner": SCANNER,
        "scanner_version": SCANNER_VERSION,
        "non_authorizing": true,
        "no_text": args.no_text,
        "source_path": source_path,
        "source_sha256_short": source_sha256_short,
        "canonical_book_count": canonical_book_count,
        "source_file_count": source_file_count,
        "canon_path": normalize_path(&args.canon),
        "marker_coverage_path": normalize_path(&args.marker_coverage),
        "book_genres_path": normalize_path(&args.book_genres),
        "output_files": output_files,
        "authority": {
            "authorizes_chunk_output_change": false,
            "authorizes_reviewed_gold_promotion": false,
            "authorizes_child_spans": false,
            "authorizes_route_behavior_change": false,
            "authorizes_evaluator_change": false,
            "authorizes_graph_edges": false,
            "authorizes_retrieval_truth": false,
            "authorizes_embedding_or_vector_work": false,
            "authorizes_boundary_import": false,
            "authorizes_theology_authority_change": false
        }
    });
    fs::write(args.out.join("scan_manifest.json"), serde_json::to_string_pretty(&manifest)? + "\n")?;
    Ok(())
}

fn write_books(path: &Path, books: &[BookObservation]) -> Result<()> {
    let mut writer = BufWriter::new(File::create(path)?);
    for book in books {
        let row = json!({
            "type": "RustObservationBook",
            "schema_version": SCHEMA_VERSION,
            "non_authorizing": true,
            "no_text": true,
            "book_id": &book.book_id,
            "usfm_code": &book.usfm_code,
            "source_entry": &book.source_entry,
            "source_class": &book.source_class,
            "sha256_short": &book.sha256_short,
            "bytes_read": book.bytes_read,
            "char_count": book.char_count,
            "line_count": book.line_count,
            "chapter_count": book.chapter_count,
            "verse_count": book.verse_count,
            "marker_counts": &book.marker_counts,
            "strong_h_count": book.strong_h_count,
            "strong_g_count": book.strong_g_count,
            "feature_flags": book.feature_flags.iter().cloned().collect::<Vec<_>>()
        });
        writeln!(writer, "{}", serde_json::to_string(&row)?)?;
    }
    Ok(())
}

fn write_verses(path: &Path, verses: &[VerseObservation]) -> Result<()> {
    let mut writer = BufWriter::new(File::create(path)?);
    let mut sorted = verses.to_vec();
    sorted.sort_by(|a, b| a.book_id.cmp(&b.book_id).then(a.chapter.cmp(&b.chapter)).then(a.verse.cmp(&b.verse)));
    for verse in sorted {
        let row = json!({
            "type": "RustObservationVerse",
            "schema_version": SCHEMA_VERSION,
            "non_authorizing": true,
            "no_text": true,
            "book_id": verse.book_id,
            "osis_ref": verse.osis_ref,
            "chapter": verse.chapter,
            "verse": verse.verse,
            "source_entry": verse.source_entry,
            "source_line_start": verse.source_line_start,
            "source_line_end": verse.source_line_end,
            "marker_counts": verse.marker_counts,
            "strong_ids": verse.strong_ids.into_iter().collect::<Vec<_>>(),
            "feature_flags": verse.feature_flags.into_iter().collect::<Vec<_>>()
        });
        writeln!(writer, "{}", serde_json::to_string(&row)?)?;
    }
    Ok(())
}

fn write_spans<'a, I>(path: &Path, spans: I) -> Result<()>
where
    I: IntoIterator<Item = &'a ChapterSpan>,
{
    let mut writer = BufWriter::new(File::create(path)?);
    for span in spans {
        let osis_start = format!("{}.{}.{}", span.book_id, span.chapter, span.start_verse);
        let osis_end = format!("{}.{}.{}", span.book_id, span.chapter, span.end_verse);
        let row = json!({
            "type": "RustObservationSpanFeature",
            "schema_version": SCHEMA_VERSION,
            "non_authorizing": true,
            "no_text": true,
            "span_id": format!("{}-chapter-{}", span.book_id, span.chapter),
            "book_id": &span.book_id,
            "osis_start": osis_start,
            "osis_end": osis_end,
            "span_kind": "chapter_observed_feature_rollup",
            "verse_count": span.verse_count,
            "marker_counts": &span.marker_counts,
            "risk_flags": span.risk_flags.iter().cloned().collect::<Vec<_>>()
        });
        writeln!(writer, "{}", serde_json::to_string(&row)?)?;
    }
    Ok(())
}

fn write_risks(path: &Path, signals: &[RiskSignal]) -> Result<()> {
    let mut writer = BufWriter::new(File::create(path)?);
    for signal in signals {
        let row = json!({
            "type": "RustObservationRiskSignal",
            "schema_version": SCHEMA_VERSION,
            "non_authorizing": true,
            "no_text": true,
            "signal_id": &signal.signal_id,
            "book_id": &signal.book_id,
            "osis_ref": &signal.osis_ref,
            "signal_kind": &signal.signal_kind,
            "evidence_markers": &signal.evidence_markers
        });
        writeln!(writer, "{}", serde_json::to_string(&row)?)?;
    }
    Ok(())
}

fn write_strongs(path: &Path, strong_index: &BTreeMap<(String, String, String), usize>) -> Result<()> {
    let mut writer = BufWriter::new(File::create(path)?);
    for ((strong_id, book_id, osis_ref), occurrence_count) in strong_index {
        let row = json!({
            "type": "RustObservationStrongOccurrence",
            "schema_version": SCHEMA_VERSION,
            "non_authorizing": true,
            "no_text": true,
            "strong_id": strong_id,
            "book_id": book_id,
            "osis_ref": osis_ref,
            "language_layer": if strong_id.starts_with('H') { "hebrew" } else { "greek" },
            "occurrence_count": occurrence_count
        });
        writeln!(writer, "{}", serde_json::to_string(&row)?)?;
    }
    Ok(())
}

fn write_anomalies(path: &Path, anomalies: &[MarkerAnomaly]) -> Result<()> {
    let mut writer = BufWriter::new(File::create(path)?);
    for anomaly in anomalies {
        let row = json!({
            "type": "RustObservationMarkerAnomaly",
            "schema_version": SCHEMA_VERSION,
            "non_authorizing": true,
            "no_text": true,
            "anomaly_id": &anomaly.anomaly_id,
            "source_entry": &anomaly.source_entry,
            "book_id": &anomaly.book_id,
            "marker": &anomaly.marker,
            "reason": &anomaly.reason
        });
        writeln!(writer, "{}", serde_json::to_string(&row)?)?;
    }
    Ok(())
}

fn read_canonical_books(path: &Path) -> Result<Vec<String>> {
    let value = read_yaml(path)?;
    let seq = yaml_get(&value, "canonical_66_books")
        .and_then(YamlValue::as_sequence)
        .ok_or("canonical_66_books must be a YAML sequence")?;
    Ok(seq.iter().filter_map(YamlValue::as_str).map(str::to_string).collect())
}

fn read_marker_registry(path: &Path) -> Result<BTreeSet<String>> {
    let value = read_yaml(path)?;
    let mut markers = BTreeSet::new();
    for section in ["markers", "forward_declared"] {
        if let Some(mapping) = yaml_get(&value, section).and_then(YamlValue::as_mapping) {
            for key in mapping.keys() {
                if let Some(marker) = key.as_str() {
                    markers.insert(marker.to_ascii_lowercase());
                }
            }
        }
    }
    Ok(markers)
}

fn read_book_genres(path: &Path) -> Result<BTreeMap<String, String>> {
    let value = read_yaml(path)?;
    let mut genres = BTreeMap::new();
    if let Some(mapping) = yaml_get(&value, "genres").and_then(YamlValue::as_mapping) {
        for (key, value) in mapping {
            if let (Some(book), Some(genre)) = (key.as_str(), value.as_str()) {
                genres.insert(book.to_string(), genre.to_string());
            }
        }
    }
    Ok(genres)
}

fn read_yaml(path: &Path) -> Result<YamlValue> {
    let file = File::open(path)?;
    Ok(serde_yaml::from_reader(file)?)
}

fn yaml_get<'a>(value: &'a YamlValue, key: &str) -> Option<&'a YamlValue> {
    value.as_mapping()?.get(&YamlValue::String(key.to_string()))
}

fn find_usfm_code(text: &str) -> Option<String> {
    for line in text.lines() {
        if let Some(rest) = line.strip_prefix("\\id ") {
            return rest.split_whitespace().next().map(str::to_string);
        }
    }
    None
}

fn parse_number_after_marker(line: &str, marker: &str) -> Option<u32> {
    let prefix = format!("\\{marker} ");
    let rest = line.strip_prefix(&prefix)?;
    let digits: String = rest.chars().take_while(|ch| ch.is_ascii_digit()).collect();
    if digits.is_empty() {
        None
    } else {
        digits.parse().ok()
    }
}

fn markers_in_line(line: &str) -> Vec<String> {
    let chars: Vec<char> = line.chars().collect();
    let mut markers = Vec::new();
    let mut index = 0;
    while index < chars.len() {
        if chars[index] == '\\' {
            index += 1;
            if index < chars.len() && chars[index] == '+' {
                index += 1;
            }
            let start = index;
            while index < chars.len() && chars[index].is_ascii_alphanumeric() {
                index += 1;
            }
            if index > start {
                let marker: String = chars[start..index].iter().collect();
                markers.push(marker.to_ascii_lowercase());
            }
        } else {
            index += 1;
        }
    }
    markers
}

fn strong_ids_in_line(line: &str) -> Vec<String> {
    let mut ids = Vec::new();
    let mut rest = line;
    while let Some(start) = rest.find("strong=\"") {
        let after = &rest[start + "strong=\"".len()..];
        let Some(end) = after.find('"') else {
            break;
        };
        for token in after[..end].split(|ch: char| !ch.is_ascii_alphanumeric()) {
            if token.len() >= 2
                && matches!(token.as_bytes()[0], b'H' | b'G')
                && token.as_bytes()[1..].iter().all(u8::is_ascii_digit)
            {
                ids.push(token.to_string());
            }
        }
        rest = &after[end + 1..];
    }
    ids
}

fn feature_flags(markers: &[String], strong_ids: &[String], genre: Option<&String>) -> BTreeSet<String> {
    let marker_set: BTreeSet<&str> = markers.iter().map(String::as_str).collect();
    let mut flags = BTreeSet::new();
    if marker_set.contains("wj") {
        flags.insert("has_wj".to_string());
    }
    if marker_set.contains("sp") {
        flags.insert("has_speaker_label".to_string());
    }
    if marker_set.iter().any(|m| matches!(*m, "f" | "fr" | "ft" | "fl" | "fq")) {
        flags.insert("has_footnote".to_string());
    }
    if marker_set.contains("fqa") {
        flags.insert("has_variant_reading".to_string());
    }
    if marker_set.iter().any(|m| matches!(*m, "x" | "xo" | "xt")) {
        flags.insert("has_crossref".to_string());
    }
    if marker_set.iter().any(|m| matches!(*m, "q1" | "q2" | "q3" | "qs" | "b" | "d")) {
        flags.insert("has_poetry_or_liturgy_marker".to_string());
    }
    if marker_set.iter().any(|m| matches!(*m, "s1" | "ms1" | "mt1" | "mt2" | "mt3")) {
        flags.insert("has_heading_marker".to_string());
    }
    if strong_ids.iter().any(|id| id.starts_with('H')) {
        flags.insert("has_strong_h".to_string());
    }
    if strong_ids.iter().any(|id| id.starts_with('G')) {
        flags.insert("has_strong_g".to_string());
    }
    if let Some(genre) = genre {
        flags.insert(format!("genre_{genre}"));
    }
    flags
}

fn is_risk_flag(flag: &str) -> bool {
    matches!(
        flag,
        "has_wj"
            | "has_speaker_label"
            | "has_footnote"
            | "has_variant_reading"
            | "has_crossref"
            | "has_poetry_or_liturgy_marker"
    )
}

fn markers_for_flag(flag: &str) -> Vec<String> {
    match flag {
        "has_wj" => vec!["wj"],
        "has_speaker_label" => vec!["sp"],
        "has_footnote" => vec!["f", "fr", "ft", "fl", "fq"],
        "has_variant_reading" => vec!["fqa"],
        "has_crossref" => vec!["x", "xo", "xt"],
        "has_poetry_or_liturgy_marker" => vec!["q1", "q2", "q3", "qs", "b", "d"],
        _ => vec![],
    }
    .into_iter()
    .map(str::to_string)
    .collect()
}

fn merge_counts(target: &mut BTreeMap<String, usize>, source: &BTreeMap<String, usize>) {
    for (key, value) in source {
        *target.entry(key.clone()).or_insert(0) += value;
    }
}

fn sha256_short(bytes: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    let digest = hex::encode(hasher.finalize());
    digest[..16].to_string()
}

fn normalize_path(path: &Path) -> String {
    path.to_string_lossy().replace('\\', "/")
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
        "FRT" => "FRT",
        "GLO" => "GLO",
        _ => return None,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn markers_in_line_finds_standard_and_nested_markers() {
        let line = r"\v 1 \wj Jesus \wj* said";
        let markers = markers_in_line(line);
        assert!(markers.contains(&"v".to_string()));
        assert!(markers.contains(&"wj".to_string()));
    }

    #[test]
    fn strong_ids_in_line_parses_greek_and_hebrew() {
        let line = r#"\v 1 word <w strong="G2424"/> <w strong="H7225"/>"#;
        let ids = strong_ids_in_line(line);
        assert!(ids.contains(&"G2424".to_string()));
        assert!(ids.contains(&"H7225".to_string()));
    }

    #[test]
    fn parse_number_after_marker_reads_chapter_and_verse() {
        assert_eq!(parse_number_after_marker(r"\c 1", "c"), Some(1));
        assert_eq!(parse_number_after_marker(r"\v 16", "v"), Some(16));
        assert_eq!(parse_number_after_marker(r"\p text", "p"), None);
    }

    #[test]
    fn usfm_to_osis_maps_t411_candidate_books() {
        assert_eq!(usfm_to_osis("2JN"), Some("2John"));
        assert_eq!(usfm_to_osis("PHM"), Some("Phlm"));
        assert_eq!(usfm_to_osis("JON"), Some("Jonah"));
        assert_eq!(usfm_to_osis("XXX"), None);
    }

    #[test]
    fn feature_flags_and_risk_separate_strong_from_interpretive() {
        let markers = vec!["f".to_string(), "wj".to_string()];
        let strong = vec!["G2424".to_string(), "H7225".to_string()];
        let flags = feature_flags(&markers, &strong, None);
        assert!(flags.contains("has_footnote"));
        assert!(flags.contains("has_wj"));
        assert!(flags.contains("has_strong_g"));
        assert!(flags.contains("has_strong_h"));
        assert!(is_risk_flag("has_footnote"));
        assert!(is_risk_flag("has_wj"));
        assert!(!is_risk_flag("has_strong_g"));
        assert!(!is_risk_flag("has_strong_h"));
    }
}
