use crate::legacy;
use crate::reports::{timed_check, CheckReport};

#[derive(Debug, Clone)]
pub(crate) struct CanonicalScopeInput {
    pub args: Vec<String>,
}

impl CanonicalScopeInput {
    pub(crate) fn new(args: Vec<String>) -> Self {
        Self { args }
    }
}

pub(crate) fn run_check(input: CanonicalScopeInput) -> CheckReport {
    timed_check("canonical_scope", || legacy::canonical_scope(&input.args))
}
