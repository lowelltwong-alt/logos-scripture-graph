use crate::legacy;
use crate::reports::{timed_check, CheckReport};

#[derive(Debug, Clone)]
pub(crate) struct JsonlScanInput {
    pub args: Vec<String>,
}

impl JsonlScanInput {
    pub(crate) fn new(args: Vec<String>) -> Self {
        Self { args }
    }
}

pub(crate) fn run_check(input: JsonlScanInput) -> CheckReport {
    timed_check("jsonl_scan", || legacy::jsonl_scan(&input.args))
}
