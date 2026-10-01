#!/usr/bin/env python3
"""Compute the boss audit's coverage set, deterministically, from the #e13 ruling's own words.

THE RULING: "one Fable execution (two if E-29 size requires) reads the peers' 145 reconciliations at FULL
coverage for the 14 both-support rows, every peer decline/reversal of a primary challenge or HIGH, every section-7
held region, every reconciliation resting on a now-REPORTED figure, and P08-012, plus an every-fifth sample of
the rest."

Each set is derived and its basis stated. Where a set cannot be derived by script it is named UNKNOWN and handed
to the boss to determine, rather than guessed at by the orchestrator - the boss reads the strategy anyway.
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
REVIEWS = EZ / "reviews"
SCOPE1 = EZ / "peer_round_scoping.v1.json"
SCOPE2 = EZ / "peer_round_scoping.v2.json"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
RULING = EZ / "ezek_controlling_agent_ruling_e13.v1.json"
P7 = EZ / "peer_figure_rederivation_p7.v2.json"
OUT = EZ / "boss_audit_scoping.v1.json"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
all_ids = [r["decision_id"] for r in rows]
conf_now = {r["decision_id"]: r.get("confidence") for r in rows}

# ---- (1) the 14 both-support rows, from the v1 classification which carries peer_class
s1 = json.loads(SCOPE1.read_text(encoding="utf-8"))
both_support = sorted(r["row_id"] for r in s1["rows"] if r.get("peer_class") == "BOTH_SUPPORT")

# ---- (2) peer declines and reversals, from the peer packets' own span/verdict fields
s2 = json.loads(SCOPE2.read_text(encoding="utf-8"))
group_rows = {g["peer_group"]: g["rows"] for g in s2["peer_groups"]}
# A FIRST version of this pattern included "stands", which appears in nearly every peer item ("OL stands", "the
# row stands"), and matched 133 of 145 rows - collapsing the ruling's every-fifth sample to ONE row and turning a
# scoped audit into a 98.6% read. A superset is defensible; a pattern that matches nearly everything is not a
# superset, it is a failure to scope. Narrowed to language that actually marks a DECLINE of a proposal or a
# REVERSAL of a lane, and still labelled INFERRED because it reads prose.
DECLINE = re.compile(
    r"\bi decline\b|\bdeclined?\s+(?:to|the|LF|OL|both)\b|\bno change proposed\b|\bdo not sustain\b"
    r"|\bdoes not carry\b|\bdoes not hold\b|\brefused?\b|\boverturn|\bis refuted\b|\bi retract\b",
    re.I)
declines = {}
for gid in group_rows:
    pkt = REVIEWS / ("peer_%s.json" % gid.replace("peer_", ""))
    d = json.loads(pkt.read_text(encoding="utf-8"))
    it = d.get("items")
    items = (list(it.values()) if isinstance(it, dict) else it) or []
    keys = (list(it.keys()) if isinstance(it, dict) else [x.get("row_id") for x in items])
    for k, x in zip(keys, items):
        if not isinstance(x, dict):
            continue
        blob = json.dumps(x, ensure_ascii=False)
        rid = x.get("row_id") or k
        if DECLINE.search(blob):
            declines.setdefault(rid, []).append(gid)
declines_rows = sorted(declines)

# ---- (3) every HIGH row, since a decline against a HIGH is in the set and HIGH rows carry the most weight
high_rows = sorted(r for r, c in conf_now.items() if str(c).lower() == "high")

# ---- (4) rows whose reconciliation rests on a figure P7 left UNKNOWN: every row of peers 01-06
p7 = json.loads(P7.read_text(encoding="utf-8"))
unknown_groups = [g["peer_group"] for g in p7["per_group"] if g.get("verdict") == "UNKNOWN"]
reported_figure_rows = sorted({r for g in unknown_groups for r in group_rows[g]})

# ---- (5) the row the ruling names explicitly
named = ["P08-012"]

full = sorted(set(both_support) | set(declines_rows) | set(high_rows) | set(reported_figure_rows) | set(named))
rest = [r for r in all_ids if r not in set(full)]
sample = rest[::5]

doc = {
    "schema": "m8_boss_audit_scoping.v1",
    "precondition": "P8 of the #e13 ruling",
    "built_at": datetime.now(timezone.utc).isoformat(),
    "bound_to": {"ruling": RULING.name, "ruling_sha256": sha(RULING),
                 "rows": "repair/rows_v7_cwo24.jsonl", "rows_sha256": sha(ROWS),
                 "p7": P7.name, "p7_sha256": sha(P7),
                 "scoping_v1": SCOPE1.name, "scoping_v2": SCOPE2.name},
    "full_coverage_sets": {
        "both_support_rows": {"rows": both_support, "n": len(both_support),
                              "basis": "EXTRACTED from peer_round_scoping.v1.json peer_class == BOTH_SUPPORT",
                              "why": "the ruling's own weighting, and peer_09 measured these as the LEAST "
                                     "audited rows in the book"},
        "peer_decline_or_reversal": {"rows": declines_rows, "n": len(declines_rows),
                                     "basis": "INFERRED by pattern over each peer item's own text; a superset by "
                                              "design, because a missed decline is worse than an extra row",
                                     "per_row_groups": declines},
        "high_confidence_rows": {"rows": high_rows, "n": len(high_rows),
                                 "basis": "MEASURED from the rows file's confidence field at the pinned digest",
                                 "note": "the ruling moves 12 of these; the boss reads them as they stand, and "
                                         "the author wave applies the moves afterwards"},
        "rows_resting_on_a_REPORTED_figure": {"rows": reported_figure_rows, "n": len(reported_figure_rows),
                                             "basis": "every row of the peer groups P7 left UNKNOWN: %s"
                                                      % ", ".join(unknown_groups),
                                             "why": "P7 proved the parse and corroborated the one named test, and "
                                                    "could not settle the per-group comparisons because the arm "
                                                    "has no exemption where the peers exercised judgement"},
        "named_by_the_ruling": {"rows": named, "basis": "the ruling names it for re-weighing"},
    },
    "section_7_held_regions": {
        "rows": "UNKNOWN",
        "basis": ("the ruling requires full coverage of every section-7 held region. The orchestrator did not "
                  "derive this set: it would have to read the strategy's section 7 and map its held questions to "
                  "rows, and the controlling agent's own ruling records that it read only lines 356-366 and "
                  "386-403 of that section and left whether chapters 29 and 32 are named as UNKNOWN. Guessing "
                  "the set here would put a wrong row list in front of the boss."),
        "handed_to_the_boss": True,
    },
    "coverage": {
        "rows_total": len(all_ids),
        "full_coverage_rows": len(full),
        "full_coverage_share": round(len(full) / len(all_ids), 3),
        "remaining_rows": len(rest),
        "every_fifth_sample_of_the_rest": sample,
        "sample_n": len(sample),
        "rows_the_boss_reads": len(full) + len(sample),
        "rows_the_boss_reads_share": round((len(full) + len(sample)) / len(all_ids), 3),
        "note": ("the section-7 set is additive and UNKNOWN here, so the boss's actual coverage is at least this "
                 "and the sample must be recomputed over whatever remains after it adds that set"),
    },
    "full_coverage_row_list": full,
    "honest_limits": [
        "The decline/reversal set is INFERRED by pattern over the peers' own prose and is deliberately a "
        "superset: an extra row costs reading time, a missed decline costs a confirmation nobody made.",
        "The section-7 set is UNKNOWN and handed over rather than guessed.",
        "This file scopes reading. It adjudicates nothing and carries no verdict on any row.",
    ],
}
OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"written": OUT.name, "sha256": sha(OUT)[:32],
                  "both_support": len(both_support), "declines": len(declines_rows),
                  "high": len(high_rows), "reported_figure_rows": len(reported_figure_rows),
                  "full_coverage_rows": len(full), "sample": len(sample),
                  "rows_the_boss_reads": len(full) + len(sample),
                  "share": doc["coverage"]["rows_the_boss_reads_share"],
                  "section_7": "UNKNOWN - handed to the boss"}, indent=1, ensure_ascii=False))
