use crate::legacy;
use crate::reports::{timed_check, CheckReport};

#[derive(Debug, Clone)]
pub(crate) struct WordTokenInput {
    pub args: Vec<String>,
}

impl WordTokenInput {
    pub(crate) fn new(args: Vec<String>) -> Self {
        Self { args }
    }
}

pub(crate) fn run_check(input: WordTokenInput) -> CheckReport {
    timed_check("word_token_signals", || {
        legacy::word_token_signals(&input.args)
    })
}
