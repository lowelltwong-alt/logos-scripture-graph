#!/usr/bin/env python3
"""OW-15 census, v4: re-measure every Ezekiel attempt from its own transcript's usage fields (E-54, OW-27).

WHY v4. E-54 MEASURED that the completion notification's subagent_tokens - the figure most receipts carry - is the LAST
request's context size, not spend. Rows for executions that compacted or resumed undercount, and v3's LOWER_BOUND sums
them. v4 keeps v3's attempt resolution unchanged (a row carrying amends_execution_id, or an *_amendment.v1 schema, is
never itself an attempt) and adds, per attempt, the spend measured from the runtime's subagent transcript:
input + cache_creation + output tokens, deduplicated by message id (the last usage seen for an id wins). Cache reads are
reported beside it and never added. Only message.id and message.usage are touched; no content is read or printed.

JOINS. An attempt's runtime agent id comes from its own receipt (agent_id / runtime_agent_id), from any row amending it,
or from the transcript map entry naming its execution id. Transcripts are looked up by file name in every World View
session's subagents directory and in the preserved copies under sp_durable/transcripts. When several attempts share one
agent id (a continued agent), the transcript is attributed ONCE to the group, never once per attempt.

SELF-TEST. The two OW-26 merged lanes were measured by hand on 2026-09-23 (576,419 and 855,552). v4 refuses to report
if it does not reproduce both exactly.

v3's bytes and its position file are RETAINED unedited. --write emits ezek_ow15_position.v4.json write-new; without it
the script prints the summary only.
"""
import glob
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
EZ = SP / "Ezek"
PROJ = Path(os.path.expanduser("~")) / ".claude" / "projects" / "C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
OUT = EZ / "ezek_ow15_position.v4.json"
NOW = datetime.now(timezone.utc).isoformat()
AID = re.compile(r"a[0-9a-f]{15,20}")
SELFTEST = {"ezek_merged_close_lane_b_a1#e1": 576419, "ezek_merged_close_lane_a_a1#e1": 855552}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731


def jl(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


PARENT_FIELD_IDS = set()


def ids_in(r):
    out = {str(r[k]) for k in ("agent_id", "runtime_agent_id") if isinstance(r.get(k), str) and AID.fullmatch(r[k])}
    # The OW-26 merged-close launch rows carry the lane's OWN runtime id in parent_agent_id (a naming slip; 200 other
    # rows hold "orchestrator" there). Accepted only when it has the runtime-id shape, and counted.
    v = r.get("parent_agent_id")
    if isinstance(v, str) and AID.fullmatch(v):
        out.add(v)
        PARENT_FIELD_IDS.add(v)
    return out


# ---- v3's attempt resolution, unchanged
receipt_files = sorted(p for p in EZ.rglob("*_attempt_receipts.jsonl") if ".pre_" not in p.name)
amend_tokens, amend_partial, amend_declared, amend_ids = {}, set(), set(), {}
attempts = []
for p in receipt_files:
    for r in jl(p):
        ex = r.get("amends_execution_id")
        if ex:
            amend_ids.setdefault(ex, set()).update(ids_in(r))
        if str(r.get("schema", "")).endswith("_amendment.v1"):
            v = r.get("tokens_reported")
            if isinstance(v, str) and "UNAVAILABLE" in v.upper():
                amend_declared.add(ex)
            if isinstance(v, int):
                amend_tokens[ex] = amend_tokens.get(ex, 0) + v
                note = str(r.get("token_note", "")).upper()
                if "SEGMENT" in note and "NOT A SEGMENT" not in note:
                    amend_partial.add(ex)
        if ex or str(r.get("schema", "")).endswith("_amendment.v1"):
            continue
        attempts.append((p.relative_to(EZ).as_posix(), r))

rows = []
for rel, r in attempts:
    ex, v = r.get("execution_id"), r.get("tokens_reported")
    if isinstance(v, int):
        rec, state = v, "measured_in_full"
    elif ex in amend_tokens:
        rec, state = amend_tokens[ex], ("measured_only_in_part" if ex in amend_partial else "measured_in_full")
    else:
        note = str(v) + " " + str(r.get("token_note", ""))
        rec = 0
        state = ("unmeasured_declared" if ex in amend_declared or "UNAVAILABLE" in note.upper()
                 or "no token count is recorded" in note else "unmeasured_UNDECLARED")
    rows.append({"receipts": rel, "execution_id": ex, "recorded": rec, "recorded_state": state,
                 "agent_ids": ids_in(r) | amend_ids.get(ex, set())})

# ---- the transcript map joins execution ids to agent ids
tmap = json.loads((EZ / "_transcript_map.ezek.json").read_text(encoding="utf-8"))
by_ex = {}
for k, e in tmap.items():
    if isinstance(e, dict) and isinstance(e.get("agent_id"), str) and AID.fullmatch(e["agent_id"]):
        by_ex.setdefault(e.get("execution_id") or ("__key__" + k), set()).add(e["agent_id"])
for row in rows:
    row["agent_ids"] |= by_ex.get(row["execution_id"], set())
# Early map entries carry no execution_id; their map key is the attempt id (e.g. ezek_writer_p01_a1). Such an entry joins
# a receipt attempt only when that attempt has no agent id yet, its execution id is "<key>#e<n>", and exactly one
# attempt matches. Counted in KEY_JOINS.
KEY_JOINS = {}
for k in [k[len("__key__"):] for k in by_ex if k.startswith("__key__")]:
    hit = [row for row in rows if not row["agent_ids"] and isinstance(row["execution_id"], str)
           and re.fullmatch(re.escape(k) + r"#e\d+", row["execution_id"])]
    if len(hit) == 1:
        hit[0]["agent_ids"] |= by_ex["__key__" + k]
        KEY_JOINS[hit[0]["execution_id"]] = sorted(by_ex["__key__" + k])
joined = set().union(*(row["agent_ids"] for row in rows))
map_orphans = sorted(a for s in by_ex.values() for a in s if a not in joined)

# ---- transcripts by file name
paths = {}
for pat in (str(PROJ / "*" / "subagents" / "agent-*.jsonl"), str(SP / "transcripts" / "**" / "agent-*.jsonl")):
    for f in glob.glob(pat, recursive=True):
        paths.setdefault(Path(f).name[len("agent-"):-len(".jsonl")], []).append(f)


def measure(f):
    usage = {}
    with open(f, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message") if isinstance(d, dict) else None
            if isinstance(m, dict) and m.get("id") and isinstance(m.get("usage"), dict):
                usage[m["id"]] = m["usage"]
    g = lambda k: sum(int(u.get(k) or 0) for u in usage.values())               # noqa: E731
    return {"spend": g("input_tokens") + g("cache_creation_input_tokens") + g("output_tokens"),
            "cache_read": g("cache_read_input_tokens"), "requests": len(usage)}


def best(aid):
    ms = [dict(measure(f), path=f) for f in paths.get(aid, [])]
    if not ms:
        return None, []
    ms.sort(key=lambda m: (m["requests"], m["spend"]), reverse=True)
    return ms[0], sorted({(m["requests"], m["spend"]) for m in ms})


# ---- group attempts that share an agent id, measure each group once
groups, seen = [], {}
for i, row in enumerate(rows):
    hit = {seen[a] for a in row["agent_ids"] if a in seen}
    if hit:
        gi = min(hit)
        for other in sorted(hit - {gi}, reverse=True):
            groups[gi] |= groups[other]
            groups[other] = set()
            for j in groups[gi]:
                for a in rows[j]["agent_ids"]:
                    seen[a] = gi
    else:
        gi = len(groups)
        groups.append(set())
    groups[gi].add(i)
    for a in row["agent_ids"]:
        seen[a] = gi

recorded_total = sum(r["recorded"] for r in rows)
remeasured_total, table, copies_disagree, no_transcript, shared = 0, [], [], [], []
for g in (g for g in groups if g):
    members = [rows[i] for i in sorted(g)]
    aids = sorted(set().union(*(m["agent_ids"] for m in members)))
    rec = sum(m["recorded"] for m in members)
    meas, found = {"spend": 0, "cache_read": 0, "requests": 0}, 0
    for a in aids:
        b, variants = best(a)
        if b:
            found += 1
            for k in ("spend", "cache_read", "requests"):
                meas[k] += b[k]
            if len(variants) > 1:
                copies_disagree.append({"agent_id": a, "copies_requests_spend": variants})
    use = meas["spend"] if found else rec
    remeasured_total += use
    entry = {"execution_ids": [m["execution_id"] for m in members], "agent_ids": aids, "recorded": rec,
             "recorded_states": sorted({m["recorded_state"] for m in members}),
             "transcripts_found": found, "measured_spend": meas["spend"] if found else None,
             "cache_read": meas["cache_read"] if found else None, "requests": meas["requests"] if found else None,
             "counted": use, "delta": (use - rec)}
    table.append(entry)
    if len(members) > 1:
        shared.append(entry["execution_ids"])
    if not found:
        no_transcript.append({"execution_ids": entry["execution_ids"], "agent_ids": aids,
                              "recorded": rec, "states": entry["recorded_states"]})

for ex, want in SELFTEST.items():
    got = next((t["measured_spend"] for t in table if t["execution_ids"] == [ex]), None)
    if got != want:
        raise SystemExit("SELFTEST FAILED: %s measured %r, hand measurement %d - method mismatch, nothing written"
                         % (ex, got, want))

orphan_spend = {a: (best(a)[0] or {}).get("spend") for a in map_orphans}
carrier = json.loads((SP / "campaign" / "budget_ceilings.v1.json").read_text(encoding="utf-8"))
ceiling = carrier["books"]["Ezek"]["ceiling"]
states = {}
for t in table:
    k = ("transcript" if t["transcripts_found"] else "receipt_only") + ":" + "+".join(t["recorded_states"])
    states[k] = states.get(k, 0) + 1
summary = {
    "ceiling": ceiling, "attempts": len(rows), "groups": len([g for g in groups if g]),
    "groups_sharing_an_agent": len(shared), "RECORDED_TOTAL_v3_method": recorded_total,
    "REMEASURED_LOWER_BOUND": remeasured_total, "undercount_found": remeasured_total - recorded_total,
    "headroom_UPPER_BOUND": ceiling - remeasured_total, "groups_by_state": states,
    "groups_without_transcript": len(no_transcript),
    "unmeasured_without_transcript": sum(1 for t in no_transcript if all(s.startswith("unmeasured") for s in t["states"])),
    "copies_disagree": len(copies_disagree), "map_agents_without_receipt": len(map_orphans),
    "map_agents_without_receipt_spend": sum(v for v in orphan_spend.values() if v),
    "ids_taken_from_parent_agent_id": sorted(PARENT_FIELD_IDS),
    "attempts_joined_by_map_key": len(KEY_JOINS),
}
print(json.dumps(summary, indent=1))
if "--write" in sys.argv:
    if OUT.exists():
        raise SystemExit("REFUSED: %s exists (write-new; make v5)" % OUT.name)
    out = {"schema": "ezek_ow15_position.v4", "restated_at": NOW,
           "ceiling": {"value": ceiling, "carrier": "sp_durable/campaign/budget_ceilings.v1.json",
                       "carrier_sha256": sha(SP / "campaign" / "budget_ceilings.v1.json"), "owner_answer": "OW-27"},
           "summary": summary,
           "method": ("spend = input + cache_creation + output per unique message id in the runtime subagent transcript; "
                      "cache_read reported, never added; content NOT read; a group of attempts sharing an agent is "
                      "counted once; an attempt with no transcript keeps its recorded figure (v3 method)"),
           "selftest": {"hand_measured_2026_09_23": SELFTEST, "reproduced": True},
           "groups_without_transcript": no_transcript, "copies_disagree": copies_disagree,
           "map_agents_without_receipt": orphan_spend, "joined_by_map_key": KEY_JOINS, "per_group": table,
           "limits": ("an execution with no receipt and no map entry is invisible here; the orchestrator's own context "
                      "spend is not counted (the ceiling is subagent tokens); the map-without-receipt spend is reported "
                      "beside the bound and NOT added to it until each is attributed"),
           "inputs_sha256": {"transcript_map": sha(EZ / "_transcript_map.ezek.json"),
                             "receipt_files": {p.relative_to(EZ).as_posix(): sha(p) for p in receipt_files}},
           "tier": "MEASURED for every transcript figure; recorded figures keep the tier their receipts state"}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print("WRITTEN", OUT.name, sha(OUT))
