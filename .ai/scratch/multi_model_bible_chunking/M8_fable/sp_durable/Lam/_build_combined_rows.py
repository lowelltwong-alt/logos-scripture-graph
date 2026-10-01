#!/usr/bin/env python3
"""Compose the Lamentations writer wave into draft_rows_combined.jsonl (orchestrator, deterministic): the three part files
in part order (p01, p02, p03), every part's own tiling re-checked over its range, chunk_index_in_book renumbered 1..N in
canonical order (decision ids untouched), whole-book tiling Lam.1.1-Lam.5.22 checked, the validator suite run over the
combined file (its report lands beside it, an allowed artifact). Refuses to overwrite. Usage: _build_combined_rows.py"""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; TOOLS = HERE / "tools"; OUT = HERE / "draft_rows_combined.jsonl"
assert not OUT.exists(), "draft_rows_combined.jsonl already exists"
parts = json.loads((HERE / "writer_parts.json").read_text(encoding="utf-8"))["writer_parts"]
rows = []
for p in parts:
    f = HERE / "writer" / f"writer_{p['part']}.jsonl"; assert f.is_file(), f"missing {f}"
    til = subprocess.run([sys.executable, str(TOOLS / "check_tiling.py"), str(f), "--range", p["span"]], capture_output=True, text=True, encoding="utf-8")
    assert til.returncode == 0, f"part {p['part']} tiling RED: {(til.stdout or til.stderr)[-400:]}"
    pr = [json.loads(l) for l in f.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    assert all(r["writer_part"] == p["part"] and r["book"] == "Lam" for r in pr), "part/book field mismatch"
    rows += pr
ids = [r["decision_id"] for r in rows]; assert len(ids) == len(set(ids)), "duplicate decision_id across parts"
for i, r in enumerate(rows, 1): r["chunk_index_in_book"] = i
OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
til = subprocess.run([sys.executable, str(TOOLS / "check_tiling.py"), str(OUT), "--range", "Lam.1.1-Lam.5.22"], capture_output=True, text=True, encoding="utf-8")
suite = subprocess.run([sys.executable, str(TOOLS / "run_validator_suite.py"), str(OUT)], capture_output=True, text=True, encoding="utf-8", cwd=str(HERE))
try: s = json.loads(suite.stdout)
except json.JSONDecodeError: s = {"unparseable": suite.stdout[-300:] + suite.stderr[-300:]}
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps({"rows": len(rows), "parts": [p["part"] for p in parts], "tiling_whole_book": "GREEN" if til.returncode == 0 else (til.stdout or til.stderr)[-300:],
                  "suite": {k: s.get(k) for k in ("hard_status", "nfd_hard_e01", "triage_flags", "per_check")} if "unparseable" not in s else s}, ensure_ascii=False, indent=1))
sys.exit(0 if til.returncode == 0 and s.get("hard_status") == "GREEN" else 1)
