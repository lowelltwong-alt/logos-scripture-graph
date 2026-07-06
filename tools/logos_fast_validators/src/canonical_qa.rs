use crate::legacy;
use crate::reports::{timed_check, CheckReport};

#[derive(Debug, Clone)]
pub(crate) struct CanonicalQaInput {
    pub args: Vec<String>,
}

impl CanonicalQaInput {
    pub(crate) fn new(args: Vec<String>) -> Self {
        Self { args }
    }
}

pub(crate) fn run_check(input: CanonicalQaInput) -> CheckReport {
    timed_check("canonical_qa", || legacy::canonical_qa(&input.args))
}
