use crate::legacy;
use crate::reports::{timed_check, CheckReport};

#[derive(Debug, Clone)]
pub(crate) struct ChunkMapInput {
    pub args: Vec<String>,
}

impl ChunkMapInput {
    pub(crate) fn new(args: Vec<String>) -> Self {
        Self { args }
    }
}

pub(crate) fn run_check(input: ChunkMapInput) -> CheckReport {
    timed_check("chunk_map", || legacy::chunk_map(&input.args))
}
