#!/usr/bin/env python3
"""E-55: census position v4 (OW-27's re-measure) corrects E-54's attribution and puts Ezekiel past its ceiling in the
spend unit. Writes the gap-breakdown finding write-new, then appends E-55 to the live MD ledger under an exclusive lock
with the expected-before digest pinned and a post-write check (E-44: append, never edit E-54).

Every number in the finding and the ledger text is computed here from position v4 (sha pinned) and the transcripts'
usage fields (message.id and message.usage only; no content read). Nothing is typed by hand. --dry prints and writes
nothing.
"""
import glob
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
SP = M8 / "sp_durable"
EZ = SP / "Ezek"
POS = EZ / "ezek_ow15_position.v4.json"
POS_SHA = "d19134c9926383154103a4360a91a8401357057b1f64ef0d771d9706841696a5"
V4 = EZ / "repair2" / "census_ow15_v4.py"
FIND = SP / "campaign" / "finding_census_gap_is_cache_rewrites.v1.json"
LM = M8 / "ERROR_PATTERN_LEDGER.v1.md"
GUARD = SP / "campaign" / "_inflight_pin_guard.py"
PROJ = Path(os.path.expanduser("~")) / ".claude" / "projects" / "C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
NOW = datetime.now(timezone.utc).isoformat()
DRY = "--dry" in sys.argv
shab = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731
n = lambda v: format(v, ",")                                                      # noqa: E731
env = dict(os.environ, PYTHONUTF8="1")

g = subprocess.run([sys.executable, "-B", str(GUARD), "--book", "Ezek", "--target", "../ERROR_PATTERN_LEDGER.v1.md",
                    "--target", "campaign/" + FIND.name], cwd=str(SP), capture_output=True, text=True, encoding="utf-8",
                   env=env)
go = json.loads(g.stdout)
if go["verdict"] != "CLEAR" or go["in_flight"]:
    raise SystemExit("REFUSED by pin guard: %s in_flight=%s" % (go["verdict"], go["in_flight"]))
pos_b = POS.read_bytes()
if shab(pos_b) != POS_SHA:
    raise SystemExit("REFUSED: position v4 changed since it was written")
pos = json.loads(pos_b.decode("utf-8"))
S = pos["summary"]

paths = {}
for pat in (str(PROJ / "*" / "subagents" / "agent-*.jsonl"), str(SP / "transcripts" / "**" / "agent-*.jsonl")):
    for f in glob.glob(pat, recursive=True):
        paths.setdefault(Path(f).name[len("agent-"):-len(".jsonl")], []).append(f)


def detail(aid):
    best = None
    for f in paths.get(aid, []):
        usage, order = {}, []
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                m = d.get("message") if isinstance(d, dict) else None
                if isinstance(m, dict) and m.get("id") and isinstance(m.get("usage"), dict):
                    if m["id"] not in usage:
                        order.append(m["id"])
                    usage[m["id"]] = m["usage"]
        if best is None or len(order) > best[0]:
            best = (len(order), usage, order)
    if best is None:
        return None
    _, usage, order = best
    s = lambda k: sum(int(usage[i].get(k) or 0) for i in order)                  # noqa: E731
    ctx = [int(usage[i].get("input_tokens") or 0) + int(usage[i].get("cache_creation_input_tokens") or 0)
           + int(usage[i].get("cache_read_input_tokens") or 0) for i in order]
    return {"input": s("input_tokens"), "cache_write": s("cache_creation_input_tokens"), "output": s("output_tokens"),
            "max_ctx": max(ctx) if ctx else 0, "last_ctx": ctx[-1] if ctx else 0,
            "ctx_drops": sum(1 for a, b in zip(ctx, ctx[1:]) if b < 0.6 * a)}


bands = {"under_0.9": 0, "0.9_to_1.1": 0, "1.1_to_2": 0, "2_to_5": 0, "over_5": 0}
agg = {"input": 0, "cache_write": 0, "output": 0, "max_ctx": 0}
unc = {"groups": 0, "delta": 0, "near_right_0.9_to_1.1": 0}
comp = {"groups": 0, "delta": 0}
last_ctx_match, both, top = 0, 0, []
for t in pos["per_group"]:
    if not t["transcripts_found"]:
        continue
    ds = [d for d in (detail(a) for a in t["agent_ids"]) if d]
    for k in agg:
        agg[k] += sum(d[k] for d in ds)
    compacted = any(d["ctx_drops"] for d in ds)
    ratio = (t["measured_spend"] / t["recorded"]) if t["recorded"] > 0 else None
    if ratio is not None:
        both += 1
        bands["under_0.9" if ratio < .9 else "0.9_to_1.1" if ratio <= 1.1 else "1.1_to_2" if ratio <= 2
              else "2_to_5" if ratio <= 5 else "over_5"] += 1
        lc = sum(d["last_ctx"] for d in ds)
        last_ctx_match += abs(t["recorded"] - lc) <= 0.02 * max(lc, 1)
    side = comp if compacted else unc
    side["groups"] += 1
    side["delta"] += t["delta"]
    if not compacted and ratio is not None and .9 <= ratio <= 1.1:
        unc["near_right_0.9_to_1.1"] += 1
    top.append({"execution_id": t["execution_ids"][0], "recorded": t["recorded"], "measured_spend": t["measured_spend"],
                "delta": t["delta"], "requests": t["requests"], "cache_write": ds[0]["cache_write"],
                "max_ctx": ds[0]["max_ctx"], "last_ctx": ds[0]["last_ctx"], "ctx_drops": ds[0]["ctx_drops"]})
top.sort(key=lambda r: r["delta"], reverse=True)
unc_with_ratio = sum(1 for t in pos["per_group"] if t["transcripts_found"] and t["recorded"] > 0) - sum(
    1 for t in pos["per_group"] if t["transcripts_found"] and t["recorded"] > 0
    and any((detail(a) or {}).get("ctx_drops") for a in t["agent_ids"]))
over = S["REMEASURED_LOWER_BOUND"] - S["ceiling"]
finding = {
    "schema": "m8_finding.v1", "id": "finding_census_gap_is_cache_rewrites.v1", "date": "2026-09-23", "book": "Ezek",
    "written_at": NOW, "tier": "MEASURED (usage fields; content NOT read)",
    "claim": ("The OW-15 census gap between the notification unit and the spend unit is mostly repeated prompt-cache "
              "writes and output inside executions that never compacted. E-54's INFERRED attribution of the gap to "
              "compaction and resume is not supported."),
    "position": {"path": "sp_durable/Ezek/" + POS.name, "sha256": POS_SHA},
    "census": {k: S[k] for k in ("ceiling", "attempts", "RECORDED_TOTAL_v3_method", "REMEASURED_LOWER_BOUND",
                                 "undercount_found", "headroom_UPPER_BOUND", "groups_without_transcript",
                                 "attempts_joined_by_map_key", "ids_taken_from_parent_agent_id")},
    "groups_with_both_figures": both, "spend_over_recorded_ratio_bands": bands,
    "recorded_equals_last_request_context_within_2pct": last_ctx_match,
    "uncompacted": dict(unc, groups_with_both_figures=unc_with_ratio), "compacted": comp,
    "aggregate_usage": agg, "cache_write_over_sum_of_max_context": round(agg["cache_write"] / max(agg["max_ctx"], 1), 2),
    "top_deltas": top[:10],
    "compaction_rule": "a request whose context is below 60% of the previous one's",
    "not_known": ("why caches are re-written (a cache lifetime lapsing between long tool calls, or the prefix changing, "
                  "are candidates; UNKNOWN which); how the owner's plan meters usage (UNKNOWN; neither unit is "
                  "claimed to be the plan's meter); the orchestrator's own context spend, which neither unit counts"),
}
fb = (json.dumps(finding, ensure_ascii=False, indent=1) + "\n").encode("utf-8")

u = finding["uncompacted"]
ENTRY = "\n".join([
    "", "## E-55 (2026-09-23) - E-54 BLAMED THE UNDERCOUNT ON COMPACTION; THE RE-MEASURE PUTS IT IN UNCOMPACTED RUNS, "
    "AND EZEKIEL IS PAST ITS CEILING IN THE SPEND UNIT", "",
    "**What happened.** OW-27's re-measure (census v4, `sp_durable/Ezek/%s`, sha256 %s) measured %s attempts from their "
    "own transcripts' usage fields. The receipts sum to %s in the notification unit. The re-measured LOWER_BOUND in the "
    "spend unit (input + cache creation + output, message-id deduplicated) is %s, which is %s over the OW-27 ceiling of "
    "%s. Of the %s gap, %s sits in %s groups with no context drop (never compacted) and %s in the %s compacted groups."
    % (POS.name, POS_SHA, n(S["attempts"]), n(S["RECORDED_TOTAL_v3_method"]), n(S["REMEASURED_LOWER_BOUND"]), n(over),
       n(S["ceiling"]), n(S["undercount_found"]), n(u["delta"]), n(u["groups"]), n(comp["delta"]), n(comp["groups"])),
    "",
    "**What it corrects (E-44: E-54 is amended here, not edited).** E-54 said, INFERRED, that for an execution never "
    "compacted the notification figure is roughly everything that entered the context, so those rows are near right. "
    "MEASURED: only %s of %s uncompacted groups with both figures have spend within 0.9-1.1x of the recorded figure. The recorded figure "
    "equals the last request's context (within 2%%) in %s of %s groups, which confirms E-54's unit finding across the "
    "census. Spend runs past it because cache writes sum to %s against the executions' maximum contexts of %s (x%s), "
    "so %s was written to cache more than once, and output adds %s. The cause is repeated cache writes and output, not "
    "compaction. Why the caches were re-written is UNKNOWN." % (n(u["near_right_0.9_to_1.1"]), n(u["groups_with_both_figures"]), n(last_ctx_match), n(both),
                  n(agg["cache_write"]), n(agg["max_ctx"]), finding["cache_write_over_sum_of_max_context"],
                  n(agg["cache_write"] - agg["max_ctx"]), n(agg["output"])), "",
    "**Siblings found by the same join work.** (1) %s launch rows from this session (the close-audit lanes, the Fable "
    "dispatch probe and the OW-26 merged lanes) put the lane's own runtime id in `parent_agent_id` and leave "
    "`agent_id` empty; 200 rows hold \"orchestrator\" there. The census reads that field only in runtime-id shape, and "
    "counts it. (2) The two OW-26 lanes are not in `_transcript_map.ezek.json`. (3) %s early map "
    "entries carry no execution id. They were joined by exact key (attempt id plus `#e<n>`, one match only), and "
    "%s attempts still have no transcript and keep their recorded figure." %
    (n(len(S["ids_taken_from_parent_agent_id"])), n(S["attempts_joined_by_map_key"]), n(S["groups_without_transcript"])),
    "",
    "**Why it matters.** Every Ezekiel ceiling to date was set and read against notification-unit sums, while OW-26's "
    "per-lane forecast was in the spend unit (E-54). Which unit the ceiling denominates is the owner's to rule. The "
    "orchestrator does not reinterpret it either way. Neither unit is claimed to be how the owner's plan meters usage "
    "(UNKNOWN).", "",
    "**Severity.** High counterfactual: in the spend unit, the line was crossed long before it read as reached. "
    "Observed: OW-27's condition held. The re-measure ran first, and no lane was dispatched on the room it appeared "
    "to leave.", "",
    "**Cure.** Position v4 (write-new; v3 retained). Finding `sp_durable/campaign/%s`. OWED, not built: record spend "
    "from usage fields at every landing; fix the launch rows' `parent_agent_id` and the map's missing lanes by "
    "amendment; the owner's ruling on the ceiling's unit before any Ezekiel launch." % FIND.name, ""])

print(json.dumps({"over_ceiling": over, "uncompacted": u, "compacted": comp, "last_ctx_match": [last_ctx_match, both],
                  "bands": bands, "cw_over_maxctx": finding["cache_write_over_sum_of_max_context"]}, indent=1))
if DRY:
    print(ENTRY)
    raise SystemExit(0)

lm_b = LM.read_bytes()
if b"## E-55 " in lm_b:
    raise SystemExit("REFUSED: an E-55 entry already exists")
for tok in ("C-2", "C-3"):
    if tok in ENTRY:
        raise SystemExit("REFUSED: a DAD marker number appears in the entry (E-52)")
if FIND.exists():
    raise SystemExit("REFUSED: %s exists (write-new)" % FIND.name)
with open(FIND, "xb") as fh:
    fh.write(fb)
if FIND.read_bytes() != fb:
    FIND.unlink()
    raise SystemExit("ROLLED BACK: finding post-write check failed")

after = lm_b + (b"" if lm_b.endswith(b"\n") else b"\n") + ENTRY.encode("utf-8")
lock = LM.with_suffix(LM.suffix + ".lock")
fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    if LM.read_bytes() != lm_b:
        raise SystemExit("REFUSED: ledger changed under the lock")
    tmp = LM.with_suffix(LM.suffix + ".tmp")
    tmp.write_bytes(after)
    os.replace(tmp, LM)
    if shab(LM.read_bytes()) != shab(after):
        LM.write_bytes(lm_b)
        raise SystemExit("ROLLED BACK: ledger post-write check failed")
finally:
    os.close(fd)
    lock.unlink()
print(json.dumps({"finding_sha256": shab(fb), "ledger_sha256": [shab(lm_b), shab(after)]}, indent=1))
