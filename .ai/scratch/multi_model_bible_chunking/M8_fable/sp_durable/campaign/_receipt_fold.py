#!/usr/bin/env python3
"""The one amend fold for every reader of *_attempt_receipts.jsonl (2026-09-24).

WHY. Readers disagreed on what a receipt row is.
  - `_orchestration_metrics.py` folded amending rows into the execution they name (E-60), but it read tokens only from
    `tokens_reported`. The v9 and v10 landing rows carry theirs as `tokens_notification_unit` and `tokens_spend_unit`,
    so the metrics recorded 0 tokens for those 5 Ezekiel executions (672,075 notification-unit tokens and 1,191,606
    spend-unit tokens, MEASURED by summing the rows).
  - `_capture_index.py`, `_census_tf6_candidate.py`, `_transcript_coverage_census.py` and `_book_close_status_ow12.py`
    either do not fold at all or count amending rows as executions.
Every reader now takes its rules from this module, so a new field is taught once.

THE RULES (the precedent is `_orchestration_metrics.fold()`, whose behaviour on every row it already read is kept):
  - An amending row (it carries amends_execution_id, or its schema ends in `_amendment.v1`) is never an execution. It
    applies to the one execution whose execution_id it names. A missing or non-unique target is counted, and nothing
    is applied.
  - A completion row's outcome and form_defects replace the launch row's. Its model_actual replaces a launch
    placeholder (absent, or starting with PENDING). A non-null agent_id or parent_agent_id on an amending row replaces
    the target's (the E-55s1 identity amendments).
  - The notification unit (the ceiling unit, OW-28) and the spend unit (usage fields, E-55) are kept apart and never
    added together. The notification unit comes from `tokens_reported` when the row's token_note does not mark it as
    census spend, or else from `tokens_notification_unit`. The spend unit comes from `tokens_reported` when the note
    marks it as census spend, or else from `tokens_spend_unit`. A string value (UNAVAILABLE, and the like) is never a
    number.
  - An amending row's notification tokens fill an execution that has none of its own. Its spend tokens are summed into
    `_spend`. `tool_uses` fills an execution that has none.

usage: python -B _receipt_fold.py --selftest
"""
import json
import sys
from collections import defaultdict
from pathlib import Path


def is_amending(r):
    return bool(r.get("amends_execution_id")) or str(r.get("schema", "")).endswith("_amendment.v1")


def spend_unit(r):
    # an amendment measured from the transcript as input + cache_creation + output (census spend), not the runtime
    # notification; it is reported apart and never added to the notification-unit total
    n = str(r.get("token_note", ""))
    return "cache_creation" in n or "census-unit spend" in n


def segment_only(r):
    n = str(r.get("token_note", "")).upper()
    return "SEGMENT" in n and "NOT A SEGMENT" not in n


def _int(v):
    return v if isinstance(v, int) and not isinstance(v, bool) else None


def notification_tokens(r):
    v = _int(r.get("tokens_reported"))
    if v is not None and not spend_unit(r):
        return v
    return _int(r.get("tokens_notification_unit"))


def spend_tokens(r):
    v = _int(r.get("tokens_reported"))
    if v is not None and spend_unit(r):
        return v
    return _int(r.get("tokens_spend_unit"))


def _placeholder(v):
    return v is None or str(v).upper().startswith("PENDING")


def fold(rows):
    """Return (executions, stats). Each execution is a copy of its own row with its amending rows applied; the copy
    carries `tokens_notification` (int or None), `_spend` (int, when any spend-unit tokens exist), `_partial` (when a
    segment-only note applies) and `_amended_by` (the count of amending rows applied). The input rows are never
    modified."""
    execs = [dict(r) for r in rows if not is_amending(r)]
    by_ex = defaultdict(list)
    for r in execs:
        if r.get("execution_id"):
            by_ex[r["execution_id"]].append(r)
    stats = {"amending_rows": 0, "applied": 0, "target_missing": 0, "target_not_unique": 0}
    pending = defaultdict(list)
    for a in rows:
        if not is_amending(a):
            continue
        stats["amending_rows"] += 1
        tgt = by_ex.get(a.get("amends_execution_id"), [])
        if len(tgt) != 1:
            stats["target_not_unique" if tgt else "target_missing"] += 1
            continue
        stats["applied"] += 1
        pending[id(tgt[0])].append(a)
    for t in execs:
        am = pending.get(id(t), [])
        own = notification_tokens(t)
        spend = spend_tokens(t)
        note_toks = []
        for a in am:
            if a.get("record_kind") == "completion":
                for f in ("outcome", "form_defects"):
                    if f in a:
                        t[f] = a[f]
                if "model_actual" in a and _placeholder(t.get("model_actual")):
                    t["model_actual"] = a["model_actual"]
            for f in ("agent_id", "parent_agent_id"):
                if a.get(f) is not None:
                    t[f] = a[f]
            if _int(t.get("tool_uses")) is None and _int(a.get("tool_uses")) is not None:
                t["tool_uses"] = a["tool_uses"]
            s = spend_tokens(a)
            if s is not None:
                spend = (spend or 0) + s
            n = notification_tokens(a)
            if n is not None and own is None:
                note_toks.append(n)
            if segment_only(a):
                t["_partial"] = True
        t["tokens_notification"] = own if own is not None else (sum(note_toks) if note_toks else None)
        if spend is not None:
            t["_spend"] = spend
        if segment_only(t):
            t["_partial"] = True
        t["_amended_by"] = len(am)
    return execs, stats


def read_receipts(paths):
    """Every row of every receipts file, in file order, each tagged with `_file` (the path as given)."""
    out = []
    for p in paths:
        for line in Path(p).read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                r["_file"] = str(p)
                out.append(r)
    return out


def selftest():
    fails = []
    L = lambda e, **k: dict({"record_kind": "launch", "execution_id": e, "attempt_id": e.split("#")[0],  # noqa: E731
                             "model_actual": "PENDING - read at landing", "outcome": "RUNNING"}, **k)
    rows = [
        L("v10a#e1", agent_id="a1", parent_agent_id=None),
        {"record_kind": "completion", "amends_execution_id": "v10a#e1", "attempt_id": "v10a", "outcome": "COMPLETED",
         "model_actual": "claude-opus-5-5", "tokens_notification_unit": 154052, "tokens_spend_unit": 195173,
         "tool_uses": 40},
        L("old#e1", tokens_reported=1000, tool_uses=5),
        {"schema": "m8_attempt_receipt_amendment.v1", "amends_execution_id": "old#e1", "tokens_reported": 555,
         "token_note": "census-unit spend: input + cache_creation + output"},
        L("id#e1", agent_id=None, parent_agent_id="rt9"),
        {"amends_execution_id": "id#e1", "agent_id": "rt9", "parent_agent_id": "orchestrator"},
        L("fail#e1"),
        {"record_kind": "completion", "amends_execution_id": "fail#e1", "attempt_id": "fail", "outcome": "FAILED_BY_RUNTIME_WATCHDOG",
         "model_actual": "UNAVAILABLE", "tokens_notification_unit": "UNAVAILABLE - no usage block"},
        L("fill#e1"),
        {"amends_execution_id": "fill#e1", "tokens_reported": 777, "token_note": "runtime notification"},
        {"amends_execution_id": "nobody#e1", "tokens_reported": 1},
        L("dup#e1"), L("dup#e1"),
        {"amends_execution_id": "dup#e1", "tokens_reported": 2},
    ]
    before = json.dumps(rows, sort_keys=True)
    ex, st = fold(rows)
    by = {}
    for e in ex:
        by.setdefault(e["execution_id"], e)
    checks = [
        ("an amending row is never an execution", len(ex) == 7),
        ("stats", st == {"amending_rows": 7, "applied": 5, "target_missing": 1, "target_not_unique": 1}),
        ("v10 notification-unit field is read", by["v10a#e1"]["tokens_notification"] == 154052),
        ("v10 spend-unit field is kept apart", by["v10a#e1"]["_spend"] == 195173),
        ("completion outcome replaces RUNNING", by["v10a#e1"]["outcome"] == "COMPLETED"),
        ("completion model_actual replaces PENDING", by["v10a#e1"]["model_actual"] == "claude-opus-5-5"),
        ("tool_uses fill", by["v10a#e1"]["tool_uses"] == 40),
        ("own notification tokens kept", by["old#e1"]["tokens_notification"] == 1000),
        ("census spend never added to notification", by["old#e1"]["_spend"] == 555),
        ("identity amendment applied", (by["id#e1"]["agent_id"], by["id#e1"]["parent_agent_id"]) == ("rt9", "orchestrator")),
        ("a string token value is never a number", by["fail#e1"]["tokens_notification"] is None and "_spend" not in by["fail#e1"]),
        ("failed landing outcome applied", by["fail#e1"]["outcome"] == "FAILED_BY_RUNTIME_WATCHDOG"),
        ("an amendment fills an execution with no tokens", by["fill#e1"]["tokens_notification"] == 777),
        ("a non-unique target gets nothing", all(e.get("tokens_notification") is None for e in ex if e["execution_id"] == "dup#e1")),
        ("input rows never modified", json.dumps(rows, sort_keys=True) == before),
    ]
    fails += [n for n, ok in checks if not ok]
    # parity with the precedent on every real receipt: the metrics fold's notification tokens and _spend must equal
    # this fold's on every execution, except where the metrics fold cannot read a v9/v10 unit field
    sp = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _orchestration_metrics as om  # noqa: E402
    real = read_receipts(sorted(sp.rglob("*_attempt_receipts.jsonl")))
    old_ex, old_st = om.fold([dict(r) for r in real])
    new_ex, new_st = fold(real)
    diffs = []
    if old_st != new_st:
        fails.append("parity: fold stats differ %s vs %s" % (old_st, new_st))
    for o, n in zip(old_ex, new_ex):
        ot = o.get("tokens_reported") if isinstance(o.get("tokens_reported"), int) else None
        if (ot, o.get("_spend")) != (n["tokens_notification"], n.get("_spend")):
            diffs.append(n.get("execution_id"))
    unit_rows = {r["amends_execution_id"] for r in real if is_amending(r) and
                 (_int(r.get("tokens_notification_unit")) is not None or _int(r.get("tokens_spend_unit")) is not None)}
    if len(old_ex) != len(new_ex) or set(diffs) != unit_rows:
        fails.append("parity: differences %s are not exactly the unit-field executions %s" % (sorted(diffs), sorted(unit_rows)))
    print(json.dumps({"selftest": "FAIL" if fails else "PASS", "checks": len(checks) + 2, "failed": fails,
                      "parity_executions": len(new_ex), "parity_diffs_all_unit_field": sorted(diffs)}, indent=1))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1:] == ["--selftest"]:
        raise SystemExit(selftest())
    raise SystemExit(__doc__)
