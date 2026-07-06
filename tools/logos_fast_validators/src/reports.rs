use serde_json::{json, Value as JsonValue};
use std::error::Error;
use std::fs::File;
use std::io::Write;
use std::path::Path;
use std::time::Instant;

pub(crate) type AnyResult<T> = Result<T, Box<dyn Error>>;

#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum CheckStatus {
    Passed,
    Failed,
}

impl CheckStatus {
    fn as_str(&self) -> &'static str {
        match self {
            CheckStatus::Passed => "passed",
            CheckStatus::Failed => "failed",
        }
    }
}

#[derive(Debug, Clone)]
pub(crate) struct CheckReport {
    pub check_id: &'static str,
    pub status: CheckStatus,
    pub message: String,
    pub elapsed_ms: u128,
}

impl CheckReport {
    pub(crate) fn passed(check_id: &'static str, elapsed_ms: u128) -> Self {
        Self {
            check_id,
            status: CheckStatus::Passed,
            message: "ok".to_string(),
            elapsed_ms,
        }
    }

    pub(crate) fn failed(check_id: &'static str, message: String, elapsed_ms: u128) -> Self {
        Self {
            check_id,
            status: CheckStatus::Failed,
            message,
            elapsed_ms,
        }
    }

    pub(crate) fn is_failed(&self) -> bool {
        self.status == CheckStatus::Failed
    }

    pub(crate) fn to_json(&self) -> JsonValue {
        json!({
            "check_id": self.check_id,
            "status": self.status.as_str(),
            "message": self.message,
            "elapsed_ms": self.elapsed_ms,
        })
    }
}

pub(crate) fn timed_check<F>(check_id: &'static str, f: F) -> CheckReport
where
    F: FnOnce() -> AnyResult<()>,
{
    let start = Instant::now();
    match f() {
        Ok(()) => CheckReport::passed(check_id, start.elapsed().as_millis()),
        Err(err) => CheckReport::failed(check_id, err.to_string(), start.elapsed().as_millis()),
    }
}

pub(crate) fn fail_if_failed(report: CheckReport) -> AnyResult<()> {
    if report.is_failed() {
        Err(format!("{} failed: {}", report.check_id, report.message).into())
    } else {
        Ok(())
    }
}

pub(crate) fn emit_bundle_summary(path: Option<&Path>, reports: &[CheckReport]) -> AnyResult<()> {
    let failed = reports.iter().filter(|report| report.is_failed()).count();
    let summary = json!({
        "validator": "logos_fast_validators bundle",
        "status": if failed == 0 { "passed" } else { "failed" },
        "checks": reports.iter().map(CheckReport::to_json).collect::<Vec<_>>(),
        "failed": failed,
        "total": reports.len(),
        "authority": "deterministic_structure_check_only",
        "non_authorizing": true,
    });
    if let Some(path) = path {
        if path == Path::new("-") {
            eprintln!("{}", serde_json::to_string_pretty(&summary)?);
        } else {
            if let Some(parent) = path.parent() {
                if !parent.as_os_str().is_empty() {
                    std::fs::create_dir_all(parent)?;
                }
            }
            let mut file = File::create(path)?;
            writeln!(file, "{}", serde_json::to_string_pretty(&summary)?)?;
        }
    }
    Ok(())
}

pub(crate) fn fail_if_any_failed(reports: &[CheckReport]) -> AnyResult<()> {
    let failed: Vec<&CheckReport> = reports.iter().filter(|report| report.is_failed()).collect();
    if failed.is_empty() {
        Ok(())
    } else {
        let joined = failed
            .iter()
            .map(|report| format!("{}: {}", report.check_id, report.message))
            .collect::<Vec<_>>()
            .join("; ");
        Err(format!("{} bundled check(s) failed: {joined}", failed.len()).into())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn report_json_keeps_check_identity() {
        let report = CheckReport::failed("chunk_map", "bad span".to_string(), 7);
        let json = report.to_json();
        assert_eq!(json["check_id"], "chunk_map");
        assert_eq!(json["status"], "failed");
        assert_eq!(json["elapsed_ms"], 7);
    }
}
