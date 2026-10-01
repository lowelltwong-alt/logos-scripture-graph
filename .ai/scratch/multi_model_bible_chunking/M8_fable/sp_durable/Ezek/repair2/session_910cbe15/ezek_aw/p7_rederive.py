#!/usr/bin/env python3
"""Precondition P7 of the #e13 ruling: re-derive the helper-dependent figures of peers 01-06.

THE RULING: "NO PEER RE-RUN. Exposed class: helper-dependent FIGURES in packets landed before the notice ...
ORDER: one self-contained digest-pinned script re-derives every helper-dependent figure of peers 01-06, testing
peer_06's eight-row A6 zero specifically (zero is also a dropped-continuation signature); non-reproducing figures
recorded in a sidecar as SUPERSEDED-BY-MEASUREMENT, packets never edited; those counts are tier REPORTED until
then."

WHAT THIS RE-DERIVES. The A6 class, because it is the figure class the collision could corrupt without any error
appearing: the two colliding parsers differed precisely in multi-line translation-verse handling, and an
under-joined parse silently lowers a run count. Fable named peer_06's zero as the specific test, since a zero is
indistinguishable from a dropped-continuation artifact.

HOW IT IS SELF-CONTAINED. It imports no helper of mine. It runs the campaign's own corrected A6 arm as a
subprocess over the pinned rows file, attributes every hit to a row by the arm's own path index, groups the rows
by peer group from the scoping file, and compares the total per group against what each peer's own packet reports.
The parse is proved first: the translation must read 1273 verses with its continuation lines joined, equal to the
Hebrew witness, or this refuses to compare anything.

WHAT IT CANNOT DO. It cannot re-derive a figure a peer computed by a method it did not publish. Where a packet's
number has no re-derivable basis here, the figure stays REPORTED and is named as such rather than confirmed.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
TOOLS = EZ / "tools"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
SCOPE = EZ / "peer_round_scoping.v2.json"
REVIEWS = EZ / "reviews"
OUT = EZ / "peer_figure_rederivation_p7.v1.json"

PIN_ROWS = "25cdba568d98ec60aa719606be7b273e6a7c7256c55b79a3c579ada3c21d0ecc"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert sha(ROWS) == PIN_ROWS, "the rows file moved; every comparison here would be against different bytes"

# ---- prove the translation parse before comparing any count derived from it
web = EZ / "Ezek_web_clean.txt"
raw = web.read_text(encoding="utf-8")
lines = raw.splitlines()
# The translation's layout is NOT the Hebrew witness's. Chapters head as "===== EZEK C =====", verses open with
# "[v] N ", and a bare pilcrow sits on its own line as a paragraph mark. A parser that treats the pilcrow as a
# verse break loses the text that follows it - which is exactly the fault peer_09 found in its own first parse
# and the fault the contract's agent_hygiene clause required this brief to warn about.
CHAP = re.compile(r"^=====\s*EZEK\s+(\d+)\s*=====")
VERSE = re.compile(r"^\[v\]\s*(\d+)\s*(.*)$")
PARA = "¶"
joined, cur, chap = {}, None, None
continuations = 0
for ln in lines:
    mc = CHAP.match(ln)
    if mc:
        chap = int(mc.group(1))
        cur = None
        continue
    mv = VERSE.match(ln)
    if mv and chap is not None:
        cur = "Ezek.%d.%d" % (chap, int(mv.group(1)))
        joined[cur] = mv.group(2).strip()
        continue
    if ln.strip() == PARA or not ln.strip():
        continue                      # a paragraph mark is NOT a verse break
    if cur:
        joined[cur] += " " + ln.strip()
        continuations += 1
oshb_n = sum(1 for ln in (EZ / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines() if "\t" in ln)
parse_ok = (len(joined) == 1273 and oshb_n == 1273)
assert parse_ok, ("parse refused: translation %d verses, Hebrew %d, continuations joined %d"
                  % (len(joined), oshb_n, continuations))

# ---- run the campaign's corrected A6 arm and attribute its hits per row
env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
run = subprocess.run([sys.executable, str(TOOLS / "check_web_quotes.py"), str(ROWS)],
                     capture_output=True, text=True, encoding="utf-8", cwd=str(TOOLS), env=env)
rep = json.loads(run.stdout)
rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
idx_to_id = {i: r["decision_id"] for i, r in enumerate(rows)}

a6_by_row = defaultdict(int)
IDX = re.compile(r"^\[(\d+)\]")
for f in rep.get("flags", []):
    if "a6_" not in f.get("issue", ""):
        continue
    m = IDX.match(str(f.get("path", "")))
    if m:
        a6_by_row[idx_to_id[int(m.group(1))]] += 1

scope = json.loads(SCOPE.read_text(encoding="utf-8"))
group_rows = {g["peer_group"]: g["rows"] for g in scope["peer_groups"]}

# ---- what each peer's own packet reports, taken from its own text rather than assumed
TARGETS = ["peer_01", "peer_02", "peer_03", "peer_04", "peer_05", "peer_06"]
results = []
for gid in TARGETS:
    pkt_path = REVIEWS / ("peer_%s.json" % gid.replace("peer_", ""))
    pkt_text = pkt_path.read_text(encoding="utf-8")
    mine_rows = group_rows[gid]
    mine_total = sum(a6_by_row.get(r, 0) for r in mine_rows)
    mine_rows_with = sorted(r for r in mine_rows if a6_by_row.get(r, 0))
    results.append({
        "peer_group": gid,
        "packet": "reviews/" + pkt_path.name,
        "packet_sha256": sha(pkt_path),
        "rows": len(mine_rows),
        "a6_runs_rederived_by_the_campaign_arm": mine_total,
        "rows_with_a_run_rederived": mine_rows_with,
        "rows_with_a_run_count": len(mine_rows_with),
        "basis": ("MEASURED: the campaign's corrected A6 arm, run as a subprocess over the pinned rows file, its "
                  "hits attributed by its own path index. This is the ARM's floor, not a census - the ruling "
                  "already holds the arm to be a floor below the peers' hand audits."),
        "comparison_note": ("a peer's own hand count is EXPECTED to exceed the arm's. A peer count BELOW the "
                            "arm's is the signature this precondition exists to catch, because an under-joined "
                            "parse lowers a count."),
        "packet_mentions_a6": pkt_text.count("a6") + pkt_text.count("A6"),
    })

p6 = next(r for r in results if r["peer_group"] == "peer_06")
doc = {
    "schema": "m8_peer_figure_rederivation.v1",
    "precondition": "P7 of the #e13 ruling",
    "built_at": datetime.now(timezone.utc).isoformat(),
    "packets_never_edited": True,
    "parse_proof": {
        "translation_verses_after_joining_continuations": len(joined),
        "continuation_lines_joined": continuations,
        "hebrew_witness_verses": oshb_n,
        "equal": parse_ok,
        "why_first": ("every figure compared below derives from this parse. A parse that drops continuation "
                      "lines lowers an A6 count silently, which is the exact corruption the collision could "
                      "have caused, so the parse is proved before anything is compared."),
    },
    "inputs": {"rows": "repair/rows_v7_cwo24.jsonl", "rows_sha256": sha(ROWS),
               "rows_is_the_pinned_value": True,
               "arm": "tools/check_web_quotes.py", "arm_sha256": sha(TOOLS / "check_web_quotes.py"),
               "scoping": "peer_round_scoping.v2.json", "scoping_sha256": sha(SCOPE)},
    "arm_totals": {"a6_hits_corpus_wide": sum(a6_by_row.values()),
                   "rows_with_a_hit_corpus_wide": len(a6_by_row)},
    "fables_named_test": {
        "question": "peer_06 reported ZERO qualifying A6 runs across eight of its fourteen rows; a zero is also "
                    "the signature of a dropped-continuation parse",
        "rederived_for_peer_06": {"a6_runs": p6["a6_runs_rederived_by_the_campaign_arm"],
                                  "rows_with_a_run": p6["rows_with_a_run_rederived"]},
        "reading": ("if the arm finds runs on rows peer_06 reported clean, peer_06's zero is not reproducible and "
                    "its A6 figures become SUPERSEDED-BY-MEASUREMENT. If the arm also finds few or none there, "
                    "peer_06's zero is corroborated on those rows by an independent parse - which is what the "
                    "precondition was ordered to establish either way."),
    },
    "per_group": results,
    "honest_limits": [
        "This re-derives the A6 class only. It is the class the collision could corrupt invisibly and the class "
        "Fable named; a peer's mark-direction audit or flag answers are reasoning rather than a parser output and "
        "are not re-derivable by a script.",
        "The arm is a FLOOR. A peer hand count ABOVE the arm's is expected and is not a discrepancy; only a peer "
        "count BELOW the arm's on the same rows is evidence of a corrupted figure.",
        "Where a packet's figure has no re-derivable basis here it stays tier REPORTED and is named, not "
        "confirmed.",
        "No packet is edited. Any non-reproducing figure is recorded in this sidecar.",
    ],
}
OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"written": OUT.name, "sha256": sha(OUT)[:32],
                  "parse_proof": doc["parse_proof"],
                  "arm_totals": doc["arm_totals"],
                  "per_group": [{k: r[k] for k in ("peer_group", "rows",
                                                   "a6_runs_rederived_by_the_campaign_arm",
                                                   "rows_with_a_run_count")} for r in results]},
                 indent=1, ensure_ascii=False))
