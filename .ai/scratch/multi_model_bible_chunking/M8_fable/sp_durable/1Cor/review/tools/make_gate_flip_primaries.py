"""Build the primaries_may_launch gate_flip row ordered by GATE-E3 (cor_controlling_rulings_r3_a1#e1). GATE-E3 makes the
flip effective only through a receipt citing the E3 rulings' sha256, the FIXUP-2 rows' sha256 and lane_cap.py's output;
all three are MEASURED here at build time (lane_cap.py is run by this script). Refuses if a digest differs from the pin
or lane_cap reports anything in flight. Writes rows_gate_flip_primaries.jsonl beside this script only.
usage: make_gate_flip_primaries.py --recorded-at ISO
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LC = HERE.parent / "lane_cap.py"
SP = Path("C:/wt/logos-t423-m8-fable/.ai/scratch/multi_model_bible_chunking/M8_fable/sp_durable")
BK = SP / "1Cor"
at = sys.argv[sys.argv.index("--recorded-at") + 1]
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
rel = lambda p: "sp_durable/" + p.relative_to(SP).as_posix()
RUL = BK / "review/1cor_controlling_agent_rulings_E3.v1.json"
ROWS = BK / "fixup/draft_rows_fixup2_applied.jsonl"
PIN = {RUL: "a7f32674dee0b0e27f25803729f93142cefdaf2847f9d7122010397e992efe70",
       ROWS: "75933a142375d8736ae71cdcc7f0e0b9052c36ea4ac4b87ccacf676ae50c6fbe"}
bad = [rel(p) for p, s in PIN.items() if h(p) != s]
if bad:
    sys.exit("REFUSED digest mismatch: %s" % bad)
g = json.loads(RUL.read_text(encoding="utf-8"))["gate"]
if g.get("primaries_may_launch") is not True or g.get("fixup_may_launch") is not False:
    sys.exit("REFUSED gate fields: %r" % {k: g.get(k) for k in ("primaries_may_launch", "fixup_may_launch")})
r = subprocess.run([sys.executable, "-B", str(LC), "--book-dir", str(BK)], capture_output=True, text=True)
lc = json.loads(r.stdout)
if r.returncode != 0 or lc.get("count") != 0:
    sys.exit("REFUSED lane_cap rc=%d out=%r" % (r.returncode, r.stdout))
row = {"schema": "m8_attempt_receipt.v1", "record_kind": "gate_flip", "book": "1Cor", "parent_agent_id": "orchestrator",
       "ordered_by": "cor_controlling_rulings_r3_a1#e1 GATE-E3", "gate": "primaries_may_launch",
       "from": False, "to": True,
       "basis": [{"rulings_file": {"path": rel(RUL), "sha256": PIN[RUL]}},
                 {"rows_file": {"path": rel(ROWS), "sha256": PIN[ROWS]}},
                 {"lane_cap": {"tool": "orchestrator scratch lane_cap.py --book-dir sp_durable/1Cor", "sha256": h(LC),
                               "exit_code": r.returncode, "output": lc,
                               "measured": "by this row's builder, at build time (just before recorded_at)"}}],
       "scope": ("The two blind primary lanes and the RECEPTION_TRADITION third lens, all on "
                 "draft_rows_fixup2_applied.jsonl (sha above), at most three in flight (lane_cap.py), nothing else for 1Cor "
                 "in flight; no lane sees another lane's output nor S1-S3's classes; model-family decorrelation "
                 "UNAVAILABLE; a 2-1 split goes to Fable's end review. fixup_may_launch stays false; TF-4 (CWO-1COR-05) "
                 "is due before the next fix-up."),
       "recorded_at": at}
out = HERE / "rows_gate_flip_primaries.jsonl"
out.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print("wrote", out.name, h(out)[:12], "lane_cap", json.dumps(lc))
