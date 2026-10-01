#!/usr/bin/env python3
"""Clear the register-bleed the wave introduced, TESTING each pass against check_register itself.

THE DEFECT IS MINE. The register sweep forbids campaign-internal vocabulary in row prose - a row is a
scholar-facing record, and the pre-wave corpus carried ZERO such flags across 145 rows. My author brief never
named the rule and actively told authors to cite rules by name in their weighings. The wave produced 96 flags.

WHAT THE AUTHORS WERE DOING, because it matters for how this is fixed: they were naming their sources, which
OW-18 asks for. The campaign's settled practice reconciles the two - a row cites the WITNESS by reference and
states its evidence tier, WITHOUT naming the file the measurement was run over. So the repair keeps every claim
and every tier and removes only the internal filename or rule label.

HOW THIS PASS IS DIFFERENT FROM MY BRIEF. It is measured against the CHECKER, not against my reading of it: the
script applies its substitutions to an in-memory copy, runs check_register over that copy, and reports what is
left. Nothing is applied until the check is clean or the residue is named. That is the discipline whose absence
caused this whole class.
"""
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import guarded_apply as GA                                                     # noqa: E402

HERE = Path(__file__).resolve().parent
EZ = GA.EZ
PRE = "9da4b940834c9045dd47cf7c7248715986120cc47d263807f72a4323fe6f7bc2"
CHECKER = EZ / "tools" / "check_register.py"

# Each substitution keeps the CLAIM and its TIER and removes only the internal label.
SUBS = [
    # --- source files: the row cites the witness, not the file the sweep ran over
    (r"\bEzek_oshb\.txt\b", "the pointed Hebrew witness"),
    (r"\bEzek_oshb\b", "the pointed Hebrew witness"),
    (r"\bEzek_web(?:_clean)?\.txt\b", "the English witness"),
    (r"\bEzek_web(?:_clean)?\b", "the English witness"),
    (r"\bpmarks_Ezek\.json\b", "the section-mark record"),
    (r"\bpmarks_Ezek\b", "the section-mark record"),
    (r"\bpmarks\b", "the section-mark record"),
    (r"\bverse_inventory\.json\b", "the verse census"),
    (r"\bverse_inventory\b", "the verse census"),
    (r"\bezek_device_inventory(?:\.v2)?\.json\b", "the device census"),
    (r"\bezek_device_inventory\b", "the device census"),
    (r"\bweb_mt_offset_map\.json\b", "the numbering crosswalk"),
    (r"\bweb_mt_offset_map\b", "the numbering crosswalk"),
    (r"\bverse_map_(?:oshb|web)\.json\b", "the staged verse text"),
    (r"\bverse_map_(?:oshb|web)\b", "the staged verse text"),
    (r"\bv2\.json\b", "the device census"),
    (r"\bbook_strategy_Ezek\.md\b", "the division plan"),
    (r"\bbook_strategy_Ezek\b", "the division plan"),
    (r"\bbook_strategy\b", "the division plan"),
    # --- rule labels: state the substance instead of naming the rule
    (r"\bUnder the precedence rule\b", "A licensed text signal outranks a section mark, so"),
    (r"\bunder the precedence rule\b", "a licensed text signal outranking a section mark"),
    (r"\bthe over-split guard\b", "the bar on a row under three verses that is not a complete word-event unit"),
    (r"\bits over-split guard\b", "its bar on a row under three verses that is not a complete word-event unit"),
    (r"\bunder the MARKS-3D direction convention\b",
     "reading each section mark as standing on the verse it follows"),
    (r"\bthe MARKS-3D direction convention\b", "the reading of a mark as standing on the verse it follows"),
    (r"\bMARKS-3D\b", "the mark-disclosure duty"),
    # --- section citations of the division plan
    (r"§\s*(\d+)", lambda m: "the division plan's held question"),
    (r"\bper the strategy\b", "per the division plan"),
    (r"\bstrategy['’]s\b", "division plan's"),
    (r"\bthe strategy\b", "the division plan"),
    # --- positional and process talk
    (r"\brow below\b", "the adjoining unit"),
    (r"\bthis wave\b", "this repair"),
]


def apply_subs(text):
    out = text
    for pat, repl in SUBS:
        out = re.sub(pat, repl, out)
    return out


SCAN = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")
LIST_SCAN = ("boundary_evidence_refs", "observed_substrate_signals", "strong_or_hebrew_tags_used")

rows = GA.load_rows()
edits, changed_fields = [], Counter()
for r in rows:
    rid = r["decision_id"]
    newvals = {}
    for f in SCAN:
        v = r.get(f)
        if isinstance(v, str):
            nv = apply_subs(v)
            if nv != v:
                newvals[f] = nv
                changed_fields[f] += 1
    for f in LIST_SCAN:
        v = r.get(f)
        if isinstance(v, list):
            nv = [apply_subs(x) if isinstance(x, str) else x for x in v]
            if nv != v:
                newvals[f] = nv
                changed_fields[f] += 1
    for f, nv in newvals.items():
        edits.append({"row_id": rid, "field": f, "op": "set", "expected_before": r[f], "value": nv,
                      "sweep": "vocab",
                      "why": "register: the row cites the witness and keeps its evidence tier; the internal "
                             "file name or rule label is removed"})

print(json.dumps({"edits": len(edits), "rows": len({e["row_id"] for e in edits}),
                  "by_field": dict(changed_fields)}, indent=1))

# ---- TEST against the checker on an in-memory copy BEFORE applying anything
work = json.loads(json.dumps(rows))
by_id = {r["decision_id"]: i for i, r in enumerate(work)}
for e in edits:
    work[by_id[e["row_id"]]][e["field"]] = e["value"]
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "candidate.jsonl"
    p.write_bytes(GA.dump_rows(work))
    res = subprocess.run([sys.executable, str(CHECKER), str(p)], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    try:
        rep = json.loads(res.stdout)
    except Exception:
        rep = {"parse_error": (res.stdout or res.stderr)[-500:]}
print()
print("check_register over the CANDIDATE corpus: flag_count=%s status=%s"
      % (rep.get("flag_count"), rep.get("status")))
print("  by_class:", rep.get("by_class"))
residue = rep.get("flags") or []
seen = set()
for f in residue[:40]:
    k = (f.get("class"), f.get("match"))
    if k in seen:
        continue
    seen.add(k)
    print("   RESIDUE %-30s %-34r %s" % (f.get("class"), f.get("match"), f.get("context", "")[:70]))

if "--apply" not in sys.argv:
    print("\n(test only; pass --apply to mutate)")
    raise SystemExit(0)

sim = GA.simulate_plan([("vocab", edits)], PRE)
if not sim["ok"]:
    raise SystemExit("REFUSED: simulation failed")
RECEIPTS = EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl"
rec = GA.apply_edits(edits, PRE, "author_wave_register_repair", ordered_count=len(edits), apply=True)
rec["what_this_was"] = ("register repair: internal file names and rule labels removed from row prose, every "
                        "claim and evidence tier kept. The authors were naming their sources, which OW-18 asks "
                        "for; the campaign's practice is to cite the WITNESS and state the tier without naming "
                        "the file.")
rec["whose_defect"] = ("the orchestrator's: the author brief never named the register rule and told authors to "
                       "cite rules by name")
rec["register_flags_before"] = 96
rec["register_flags_after"] = rep.get("flag_count")
with RECEIPTS.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
print(json.dumps({k: rec[k] for k in ("sweep", "e18_parity_digits", "rows_touched",
                                      "register_flags_before", "register_flags_after",
                                      "preimage_sha256", "postimage_sha256_measured_from_disk")}, indent=1))
