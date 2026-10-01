"""S1-08 (a)(b)(c) + optional U-QUOTE-LABEL fixtures (dan_controlling_agent_rulings_E1). Runs the INSTALLED SP members on
SCRATCH copies only (tf/s108_fx/), never on an SP path (E-67). Prints one JSON result; ALL_PASS gates the install."""
import copy
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
TOOLS = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Dan\tools")
ROWS = TOOLS.parent / "fixup" / "draft_rows_fixup1_applied.jsonl"
sys.path.insert(0, str(TOOLS))
from dan_lib import collate_hebrew, kq_split_bytes, load_pmarks  # noqa: E402

D = HERE / "s108_fx"
D.mkdir(exist_ok=True)
rows = [json.loads(x) for x in ROWS.read_text(encoding="utf-8").splitlines() if x.strip()]
byid = {r["decision_id"]: r for r in rows}


def run(tool, rows_):
    p = D / ("rows_%s.jsonl" % tool.replace(".py", ""))
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows_), encoding="utf-8")
    r = subprocess.run([sys.executable, "-B", str(TOOLS / tool), str(p)], capture_output=True, text=True,
                       encoding="utf-8", env=dict(os.environ, PYTHONUTF8="1"), cwd=str(D))
    out = r.stdout
    return json.loads(out[out.index("{"):])


res = {}
# ---- (a) universals ----
syn_a = copy.deepcopy(byid["W6-001"])
syn_a["decision_id"] = "SYN-A"
syn_a["device_notes"] = syn_a["device_notes"] + " This is the last vision of the book."
u = run("check_universals.py", rows + [syn_a])
res["a_no_top_level_parent_collection_flags"] = not any(f["path"].endswith("].parent_collection") for f in u["flags"])
res["a_synthetic_device_notes_still_flags"] = any(f["path"] == "[%d].device_notes" % len(rows) for f in u["flags"])

# ---- (b) citation_sweep K/Q arm ----
vt = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))["Dan.9.24"]["text"]
pm = load_pmarks()
kforms = [kq_split_bytes(n, vt)[0].replace("/", "") for n in pm["kq"]["Dan.9.24"]]
word = next(w for w in vt.split() if any(k and collate_hebrew(k, w) != "none" for k in kforms))
syn_b = copy.deepcopy(byid["W5-005"])
syn_b["decision_id"] = "SYN-B"
syn_b["strong_or_hebrew_tags_used"][0] = word + " (oshb:Dan.9.24)"
c = run("citation_sweep.py", rows + [syn_b])
res["b_W5_005_no_longer_warns"] = not any(w.startswith("W5-005:") for w in c["prose_dual_warns"])
res["b_synthetic_ketiv_quote_warns"] = any(w.startswith("SYN-B:") and "Dan.9.24" in w for w in c["prose_dual_warns"])
res["b_citation_status_unchanged_class"] = c["status"]

# ---- (c) check_marks paseq ----
syn_c1 = copy.deepcopy(byid["W4-008"])
syn_c1["decision_id"] = "SYN-C1"
syn_c1["device_notes"] = "A paseq after the first word of 8:3 marks the ram."
syn_c2 = copy.deepcopy(byid["W4-008"])
syn_c2["decision_id"] = "SYN-C2"
syn_c2["observed_substrate_signals"] = syn_c2["observed_substrate_signals"] + ["paseq at 1:1"]
m = run("check_marks.py", rows + [syn_c1, syn_c2])
pw = [w["decision_id"] for w in m["warns"] if w["rule"] == "paseq_position_warn"]
fp = [(f["decision_id"], f["claim"]) for f in m["flags"] if f["rule"] == "paseq_false_presence"]
res["c_W4_008_W6_014_no_warn"] = "W4-008" not in pw and "W6-014" not in pw
res["c_synthetic_position_claim_warns"] = "SYN-C1" in pw
res["c_synthetic_paseq_1_1_flagged"] = ("SYN-C2", "paseq at 1:1") in fp
res["c_no_real_row_false_presence"] = not [x for x in fp if not x[0].startswith("SYN-")]

# ---- U-QUOTE-LABEL web_quotes ----
w = run("check_web_quotes.py", rows)
res["u_parent_collection_label_not_flagged"] = not any(f["path"].endswith("].parent_collection") for f in w["flags"])
syn_u = copy.deepcopy(byid["W4-001"])
syn_u["decision_id"] = "SYN-U"
syn_u["parent_collection"] = "PG (The four beasts and one like a son of man, coming with the clouds of the sky)"
w2 = run("check_web_quotes.py", rows + [syn_u])
res["u_info_synthetic_label_flags"] = [f.get("quote") for f in w2["flags"] if f["path"] == "[%d].parent_collection" % len(rows)]
res["ALL_PASS"] = all(v for k, v in res.items() if not k.startswith(("u_info", "b_citation_status")))
print(json.dumps(res, ensure_ascii=False))
