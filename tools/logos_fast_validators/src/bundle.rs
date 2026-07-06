use crate::canonical_qa::{self, CanonicalQaInput};
use crate::canonical_scope::{self, CanonicalScopeInput};
use crate::reports::{emit_bundle_summary, fail_if_any_failed, AnyResult, CheckReport};
use crate::word_tokens::{self, WordTokenInput};
use std::path::{Path, PathBuf};

const PASSAGES_REL: &str = "scripture/passages/passages.jsonl";
const WITNESSES_REL: &str = "translations/eng-web/translation_witnesses.jsonl";
const WORD_TOKENS_REL: &str = "translations/eng-web/word_tokens.jsonl";
const SIDECAR_RELS: &[&str] = &[
    "translations/eng-web/boundary_claims.jsonl",
    "translations/eng-web/footnotes.jsonl",
    "translations/eng-web/editorial_cross_references.jsonl",
    "translations/eng-web/section_headings.jsonl",
];

#[derive(Debug, Clone)]
pub(crate) struct BundleInput {
    pub canonical_root: PathBuf,
    pub canon: PathBuf,
    pub translation_id: String,
    pub include_word_tokens: bool,
    pub summary_json: Option<PathBuf>,
}

impl BundleInput {
    pub(crate) fn parse_args(args: &[String]) -> AnyResult<Self> {
        let mut canonical_root = PathBuf::from("data/canonical");
        let mut canon = PathBuf::from("config/canon/canonical_66_books.yaml");
        let mut translation_id = "eng-web".to_string();
        let mut include_word_tokens = true;
        let mut summary_json = None;
        let mut index = 0;
        while index < args.len() {
            match args[index].as_str() {
                "--canonical-root" => {
                    index += 1;
                    canonical_root =
                        PathBuf::from(args.get(index).ok_or("--canonical-root requires a value")?);
                }
                "--canon" => {
                    index += 1;
                    canon = PathBuf::from(args.get(index).ok_or("--canon requires a value")?);
                }
                "--translation-id" => {
                    index += 1;
                    translation_id = args
                        .get(index)
                        .ok_or("--translation-id requires a value")?
                        .to_string();
                }
                "--skip-word-tokens" => include_word_tokens = false,
                "--summary-json" => {
                    index += 1;
                    summary_json = Some(PathBuf::from(
                        args.get(index).ok_or("--summary-json requires a value")?,
                    ));
                }
                value if value.starts_with('-') => {
                    return Err(format!("unknown bundle flag: {value}").into());
                }
                value => {
                    return Err(format!("bundle does not accept positional path: {value}").into())
                }
            }
            index += 1;
        }
        Ok(Self {
            canonical_root,
            canon,
            translation_id,
            include_word_tokens,
            summary_json,
        })
    }
}

pub(crate) fn run(args: &[String]) -> AnyResult<()> {
    let input = BundleInput::parse_args(args)?;
    let reports = run_checks(&input);
    emit_bundle_summary(input.summary_json.as_deref(), &reports)?;
    if reports.iter().all(|report| !report.is_failed()) {
        println!(
            "Fast validation bundle passed for {} check(s).",
            reports.len()
        );
    } else {
        println!("FAST VALIDATION BUNDLE FAILED");
        for report in reports.iter().filter(|report| report.is_failed()) {
            println!("- {}: {}", report.check_id, report.message);
        }
    }
    fail_if_any_failed(&reports)
}

pub(crate) fn run_checks(input: &BundleInput) -> Vec<CheckReport> {
    let mut reports = Vec::new();

    let mut canonical_qa_args = vec![
        "--canon".to_string(),
        input.canon.display().to_string(),
        "--canonical-root".to_string(),
        input.canonical_root.display().to_string(),
    ];
    if !input.include_word_tokens {
        canonical_qa_args.push("--skip-word-tokens".to_string());
    }
    reports.push(canonical_qa::run_check(CanonicalQaInput::new(
        canonical_qa_args,
    )));

    let mut scope_args = vec!["--canon".to_string(), input.canon.display().to_string()];
    for rel in canonical_scope_rels(input.include_word_tokens) {
        scope_args.push(input.canonical_root.join(rel).display().to_string());
    }
    reports.push(canonical_scope::run_check(CanonicalScopeInput::new(
        scope_args,
    )));

    if input.include_word_tokens {
        let word_tokens_path = input.canonical_root.join(WORD_TOKENS_REL);
        reports.push(word_tokens::run_check(WordTokenInput::new(vec![
            "--translation-id".to_string(),
            input.translation_id.clone(),
            word_tokens_path.display().to_string(),
        ])));
    }

    reports
}

fn canonical_scope_rels(include_word_tokens: bool) -> Vec<&'static str> {
    let mut rels = vec![PASSAGES_REL, WITNESSES_REL];
    rels.extend(SIDECAR_RELS.iter().copied());
    if include_word_tokens {
        rels.push(WORD_TOKENS_REL);
    }
    rels
}

#[allow(dead_code)]
fn as_repo_path(root: &Path, rel: &str) -> PathBuf {
    root.join(rel)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn default_bundle_keeps_word_token_check_enabled() {
        let input = BundleInput::parse_args(&[]).expect("default bundle args");
        assert!(input.include_word_tokens);
        assert_eq!(input.translation_id, "eng-web");
    }

    #[test]
    fn canonical_scope_bundle_rels_include_word_tokens_when_enabled() {
        let rels = canonical_scope_rels(true);
        assert!(rels.contains(&WORD_TOKENS_REL));
        assert!(rels.contains(&PASSAGES_REL));
    }
}
