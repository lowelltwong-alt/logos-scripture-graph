mod bundle;
mod canonical_qa;
mod canonical_scope;
mod chunk_map;
mod jsonl_scan;
mod legacy;
mod reports;
mod span_parse;
mod word_tokens;

use reports::{fail_if_failed, AnyResult};
use std::env;

fn main() {
    if let Err(err) = run() {
        eprintln!("logos_fast_validators failed: {err}");
        std::process::exit(1);
    }
}

fn run() -> AnyResult<()> {
    let mut args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        return Err("missing command: expected jsonl-scan, canonical-scope, canonical-qa, word-token-signals, chunk-map, span-parse, or bundle".into());
    }
    let command = args.remove(0);
    match command.as_str() {
        "jsonl-scan" => {
            fail_if_failed(jsonl_scan::run_check(jsonl_scan::JsonlScanInput::new(args)))
        }
        "canonical-scope" => fail_if_failed(canonical_scope::run_check(
            canonical_scope::CanonicalScopeInput::new(args),
        )),
        "canonical-qa" => fail_if_failed(canonical_qa::run_check(
            canonical_qa::CanonicalQaInput::new(args),
        )),
        "word-token-signals" => fail_if_failed(word_tokens::run_check(
            word_tokens::WordTokenInput::new(args),
        )),
        "chunk-map" => fail_if_failed(chunk_map::run_check(chunk_map::ChunkMapInput::new(args))),
        "span-parse" => fail_if_failed(span_parse::run_check(
            span_parse::SpanParseInput::parse_args(&args)?,
        )),
        "bundle" => bundle::run(&args),
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
    println!("  canonical-qa [--canon PATH] [--canonical-root PATH] [--skip-word-tokens] [--summary-json PATH]");
    println!("  word-token-signals [--translation-id ID] [--summary-json PATH] FILE...");
    println!("  chunk-map [--model-id ID] [--require-full-bible] [--book BOOK] [--canon PATH] [--summary-json PATH] FILE");
    println!("  span-parse [--summary-json PATH] SPAN...");
    println!("  bundle [--canonical-root PATH] [--canon PATH] [--translation-id ID] [--skip-word-tokens] [--summary-json PATH]");
}
