"""Deterministic A/B plus policy-triggered C routing."""

from __future__ import annotations

from typing import Any


DEFAULT_CRITICAL_FLAGS = {
    "diacritic_disagreement", "script_disagreement", "punctuation_disagreement",
    "missing_line_suspected",
}


def route_third_engine(comparison: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    mode = policy.get("third_engine_mode", "on_critical_or_threshold")
    if mode not in {"disabled", "always", "on_disagreement", "on_critical_or_threshold"}:
        raise ValueError(f"unknown third_engine_mode: {mode}")
    rows = comparison.get("pairwise") or []
    flags = {flag for row in rows for flag in row.get("flags", []) if flag != "none"}
    rate = max((float(row.get("character_disagreement_rate", 0)) for row in rows), default=0.0)
    threshold = float(policy.get("third_engine_disagreement_threshold", 0.08))
    critical = set(policy.get("critical_flags") or DEFAULT_CRITICAL_FLAGS)
    reasons: list[str] = []
    if mode == "always":
        reasons.append("policy_always")
    elif mode == "on_disagreement" and flags:
        reasons.append("engine_disagreement")
    elif mode == "on_critical_or_threshold":
        if flags & critical:
            reasons.append("critical_disagreement")
        if rate >= threshold:
            reasons.append("disagreement_threshold")
    return {
        "run_third_engine": bool(reasons), "reasons": reasons or ["policy_not_triggered"],
        "observed_flags": sorted(flags), "max_character_disagreement_rate": round(rate, 6),
        "threshold": threshold, "third_engine_is_tiebreaker": False,
        "human_review_may_still_be_required": True,
    }
