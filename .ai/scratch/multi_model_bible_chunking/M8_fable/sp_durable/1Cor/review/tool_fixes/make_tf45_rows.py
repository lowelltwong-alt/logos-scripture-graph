"""Builds the TF-4 and TF-5 tool_fix_install rows from digests measured now. Run once, after both installs, from anywhere.
usage: make_tf45_rows.py OUTDIR TF5_PRE_SHA12
"""
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
TF = Path(__file__).resolve().parent
R = TF.parent
SPD = R.parents[1]
out = Path(sys.argv[1])


def rp(p):
    return "sp_durable/" + Path(p).relative_to(SPD).as_posix()


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fref(p):
    return {"path": rp(p), "sha256": sha(p)}


rows_f = SPD / "1Cor" / "fixup" / "draft_rows_fixup2_applied.jsonl"
sweep = R / "cwo_sweep_1cor.py"
pre4, pre5 = R / "cwo_sweep_1cor.py.pre_bb71fd0bc134", R / ("cwo_sweep_1cor.py.pre_" + sys.argv[2])
base = {"schema": "m8_attempt_receipt.v1", "record_kind": "tool_fix_install", "book": "1Cor", "parent_agent_id": "orchestrator"}
tf4 = {**base, "ordered_by": "cor_controlling_rulings_r3_a1#e1 S3-03; held to before FIXUP-3 by cor_controlling_rulings_r4_a1#e1 GATE-E4",
       "rulings_file": fref(R / "1cor_controlling_agent_rulings_E3.v1.json"), "rows_tested": fref(rows_f), "tool_fix_id": "TF-4 (S3-03 / CWO-1COR-05)",
       "outcome": "INSTALLED - CWO-1COR-05 added to cwo_sweep_1cor.py as an addition, its PD3 copied from the reference bytes. "
                  "The eleven plants of cwo05_ref.py pass through the sweep itself (7 hit, 4 clear as expected); the sweep's hits equal the "
                  "reference's on the applied rows, 11 hits in 10 rows; A, B, CWO02 and CWO04 output equal the pre-TF-4 tool's on those rows. "
                  "The first draft carried a backspace for a word boundary in PD3 (a heredoc mangled it) and matched nothing; the baseline "
                  "comparison caught that, and PD3 was then copied from the reference. The reference was recovered after the scratchpad purge by "
                  "resuming its E3 author, digest-equal.",
       "tools": {"cwo_sweep_1cor.py": {"path": rp(sweep), "after_sha256": sha(pre5), "before_sha256": sha(pre4), "pre_copy": rp(pre4)}},
       "tests": {"script": fref(R / "tools" / "test_cwo05.py"), "reference": fref(R / "tools" / "cwo05_ref.py"),
                 "result": fref(TF / "fixtures_tf4.result.json"), "verdict": "GREEN", "red_on_pre_tool": "KeyError CWO05"}}
tf5 = {**base, "ordered_by": "cor_controlling_rulings_r4_a1#e1 R4-UNCERTAINTY order to tool_fix, GATE-E4",
       "rulings_file": fref(R / "1cor_controlling_agent_rulings_E4.v1.json"), "rows_tested": fref(rows_f), "tool_fix_id": "TF-5 (CWO-1COR-06, CWO-1COR-07)",
       "outcome": "INSTALLED - CWO-1COR-06 and CWO-1COR-07 added to cwo_sweep_1cor.py as added sections, copied line by line from the reference bytes by "
                  "mk_tf5.py; only the reference's path constant and the two load lines that use it changed. Ten of ten E4 plants pass through the sweep "
                  "itself, and the sweep's lists equal the reference's on every one of the eleven row sets. On the applied rows 18 hits in 17 rows (on_sign 5, "
                  "wording_absent_from_sbl 13, range_token 3) and 63 unlisted in 25 rows, equal to the E4 baseline. A, B, CWO02, CWO04 and CWO05 output is equal "
                  "to the pre-TF-5 tool's on the applied rows and the combined draft; no HARD member is narrowed. Four mutants all RED.",
       "tools": {"cwo_sweep_1cor.py": {"path": rp(sweep), "after_sha256": sha(sweep), "before_sha256": sha(pre5), "pre_copy": rp(pre5)}},
       "tests": {"script": fref(R / "tools" / "test_cwo0607.py"), "builder": fref(TF / "mk_tf5.py"), "reference": fref(R / "tools" / "cwo06_ref.py"),
                 "plants": fref(R / "tools" / "plants06.py"), "mutants": fref(TF / "mutants_tf5.py"), "mutants_result": fref(TF / "mutants_tf5.result.json"),
                 "result": fref(TF / "fixtures_tf5.result.json"), "verdict": "GREEN", "red_on_pre_tool": "KeyError CWO06"}}
(out / "tf4.json").write_text(json.dumps(tf4, ensure_ascii=False), encoding="utf-8", newline="\n")
(out / "tf5.json").write_text(json.dumps(tf5, ensure_ascii=False), encoding="utf-8", newline="\n")
print(tf4["tools"], tf5["tools"])
