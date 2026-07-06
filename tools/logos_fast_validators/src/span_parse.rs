use crate::reports::{timed_check, AnyResult, CheckReport};
use serde_json::json;
use std::fs::File;
use std::io::Write;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone)]
pub(crate) struct SpanParseInput {
    pub spans: Vec<String>,
    pub summary_json: Option<PathBuf>,
}

impl SpanParseInput {
    pub(crate) fn parse_args(args: &[String]) -> AnyResult<Self> {
        let mut spans = Vec::new();
        let mut summary_json = None;
        let mut index = 0;
        while index < args.len() {
            match args[index].as_str() {
                "--summary-json" => {
                    index += 1;
                    summary_json = Some(PathBuf::from(
                        args.get(index).ok_or("--summary-json requires a value")?,
                    ));
                }
                value if value.starts_with('-') => {
                    return Err(format!("unknown span-parse flag: {value}").into());
                }
                value => spans.push(value.to_string()),
            }
            index += 1;
        }
        if spans.is_empty() {
            return Err("span-parse requires at least one span".into());
        }
        Ok(Self {
            spans,
            summary_json,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct ParsedSpan {
    book: String,
    start_chapter: u32,
    start_verse: u32,
    end_chapter: u32,
    end_verse: u32,
}

pub(crate) fn run_check(input: SpanParseInput) -> CheckReport {
    timed_check("span_parse", || run_span_parse(input))
}

fn run_span_parse(input: SpanParseInput) -> AnyResult<()> {
    let mut failures = Vec::new();
    let mut parsed = Vec::new();
    for span in &input.spans {
        match parse_span(span) {
            Ok(parsed_span) => parsed.push((span.clone(), parsed_span)),
            Err(err) => failures.push(format!("{span}: {err}")),
        }
    }
    let summary = json!({
        "validator": "logos_fast_validators span-parse",
        "status": if failures.is_empty() { "passed" } else { "failed" },
        "spans": input.spans.len(),
        "parsed": parsed.len(),
        "failures": failures.len(),
        "authority": "deterministic_structure_check_only",
        "non_authorizing": true,
    });
    emit_summary(input.summary_json.as_deref(), &summary)?;
    if failures.is_empty() {
        println!(
            "Fast span parse validation passed for {} span(s).",
            parsed.len()
        );
        Ok(())
    } else {
        println!("FAST SPAN PARSE VALIDATION FAILED");
        for failure in failures.iter().take(100) {
            println!("- {failure}");
        }
        Err(format!("{} span-parse failure(s)", failures.len()).into())
    }
}

fn parse_span(value: &str) -> Result<ParsedSpan, String> {
    let mut endpoints = value.trim().split('-');
    let start = endpoints.next().unwrap_or("");
    let end = endpoints.next();
    if endpoints.next().is_some() {
        return Err("malformed span".to_string());
    }
    let (book, start_chapter, start_verse) = parse_endpoint(start)?;
    let (end_book, end_chapter, end_verse) = match end {
        Some(endpoint) => parse_endpoint(endpoint)?,
        None => (book.clone(), start_chapter, start_verse),
    };
    if book != end_book {
        return Err("span crosses books".to_string());
    }
    if (end_chapter, end_verse) < (start_chapter, start_verse) {
        return Err("span end before start".to_string());
    }
    Ok(ParsedSpan {
        book,
        start_chapter,
        start_verse,
        end_chapter,
        end_verse,
    })
}

fn parse_endpoint(value: &str) -> Result<(String, u32, u32), String> {
    let mut parts = value.split('.');
    let book = parts.next().unwrap_or("");
    let chapter = parts.next().unwrap_or("");
    let verse = parts.next().unwrap_or("");
    if parts.next().is_some()
        || book.is_empty()
        || !book.chars().all(|ch| ch.is_ascii_alphanumeric())
        || !book.chars().any(|ch| ch.is_ascii_alphabetic())
    {
        return Err("malformed endpoint".to_string());
    }
    let chapter = chapter
        .parse::<u32>()
        .map_err(|_| "chapter must be a positive integer".to_string())?;
    let verse = verse
        .parse::<u32>()
        .map_err(|_| "verse must be a positive integer".to_string())?;
    if chapter == 0 || verse == 0 {
        return Err("chapter and verse must be positive".to_string());
    }
    Ok((book.to_string(), chapter, verse))
}

fn emit_summary(path: Option<&Path>, summary: &serde_json::Value) -> AnyResult<()> {
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
    fn parses_single_and_range_spans() {
        assert!(parse_span("Gen.1.1").is_ok());
        assert!(parse_span("2John.1.1-2John.1.3").is_ok());
    }

    #[test]
    fn rejects_cross_book_or_inverted_spans() {
        assert!(parse_span("Gen.1.1-Exod.1.1").is_err());
        assert!(parse_span("Phlm.1.7-Phlm.1.1").is_err());
    }
}
