"""Fixture test of make_primary_landing.py: a contract-valid c01 OL deliverable must give no problems; a broken one
(missing row, severity on a support, no severity on a challenge, bad tier, summary mismatch, one triage id, an assembled
Greek phrase, a CR byte) must give each of those problems. Fixtures and outputs go under fx_landing/ beside this script.
Prints a JSON verdict."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FX = HERE / "fx_landing"
FX.mkdir(exist_ok=True)
plan = json.loads(Path("C:/wt/logos-t423-m8-fable/.ai/scratch/multi_model_bible_chunking/M8_fable/sp_durable/1Cor/"
                       "review_clusters.json").read_text(encoding="utf-8"))
ids = plan["clusters"][0]["row_ids"]
RP_PHRASE = "χάρις ὑμῖν καὶ εἰρήνη"
item = lambda r: {"row_id": r, "verdict": "support", "claim": "seam holds at %s" % r, "tier": "MEASURED",
                  "decision": "keep", "evidence": ["1Cor.1.3 " + RP_PHRASE]}
good = {"attempt_id": "cor_primary_ol_c01_a1", "execution_id": "cor_primary_ol_c01_a1#e1", "book": "1Cor",
        "role": "primary_OL", "cluster": "c01", "model_ordered": "x",
        "rows_file": {"path": "1Cor/fixup/draft_rows_fixup2_applied.jsonl",
                      "sha256": "75933a142375d8736ae71cdcc7f0e0b9052c36ea4ac4b87ccacf676ae50c6fbe"},
        "artifacts_reviewed": [], "rows_reviewed": list(ids), "items": [item(r) for r in ids],
        "triage_answers": [{"id": "TRIAGE-1COR-01", "in_my_cluster": False}, {"id": "TRIAGE-1COR-02"}],
        "summary": {"supports": len(ids), "challenges": 0, "by_severity": {"high": 0, "medium": 0, "low": 0}},
        "unresolved_uncertainty": [], "e19_selfreport": "no listing, no glob", "limit": "x"}
bad = json.loads(json.dumps(good))
bad["items"] = bad["items"][1:]
bad["rows_reviewed"] = bad["rows_reviewed"][1:]
bad["items"][0]["severity"] = "low"
bad["items"][1].update(verdict="challenge")
bad["items"][2]["tier"] = "CONFIRMED"
bad["items"][3]["evidence"] = ["χάρις καὶ εἰρήνη ὑμῖν"]
bad["triage_answers"] = bad["triage_answers"][:1]
res = {}
for name, d, cr in (("good", good, False), ("bad", bad, True)):
    p = FX / ("%s.json" % name)
    s = json.dumps(d, ensure_ascii=False) + ("\r\n" if cr else "\n")
    p.write_bytes(s.encode("utf-8"))
    r = subprocess.run([sys.executable, "-B", str(HERE / "make_primary_landing.py"), "--lane", "OL", "--cluster", "c01",
                        "--agent-id", "fx", "--tokens", "0", "--tool-uses", "0", "--duration-ms", "0", "--outcome",
                        "fixture", "--summary", "fixture", "--file", str(p), "--out", str(FX / ("%s.row.json" % name))],
                       capture_output=True, text=True, encoding="utf-8")
    row = json.loads((FX / ("%s.row.json" % name)).read_text(encoding="utf-8"))
    res[name] = row["orchestrator_verification"]["problems"]
want = ["CR bytes", "rows_reviewed differs", "no item for W1-001", "severity on a support", "severity None on a challenge",
        "tier 'CONFIRMED'", "summary", "triage_answers ids", "Greek phrase not in RP or SBLGNT"]
miss = [w for w in want if not any(w in p for p in res["bad"])]
ok = res["good"] == [] and not miss
print(json.dumps({"verdict": "PASS" if ok else "FAIL", "good_problems": res["good"], "bad_missing": miss,
                  "bad_n": len(res["bad"])}, ensure_ascii=False))
