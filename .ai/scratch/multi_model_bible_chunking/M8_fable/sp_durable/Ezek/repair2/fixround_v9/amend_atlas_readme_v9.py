#!/usr/bin/env python3
"""Amend the atlas deliverable's README for the v9 re-point (E-44: amend, never edit). The tables stay as history.

One section is inserted before '## Files' (the anchor must occur exactly once). It gives the new input and the new
digests, measured here from disk, and names the one row that changed. The README is saved as .pre_<sha12>. The atlas
mirror check is then re-run: its record must still reproduce the shipped one byte for byte, or the README is restored.
usage: amend_atlas_readme_v9.py --dest <scratch dir outside M8>
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EZ = HERE.parents[1]
SP, D = EZ.parent, EZ / "deliverables"
R = D / "README.md"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
ap = argparse.ArgumentParser()
ap.add_argument("--dest", required=True)
a = ap.parse_args()
env = dict(os.environ, PYTHONUTF8="1")
g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek",
                    "--target", "Ezek/deliverables/README.md"], cwd=str(SP), capture_output=True, text=True,
                   encoding="utf-8", env=env)
if json.loads(g.stdout)["verdict"] != "CLEAR":
    raise SystemExit("REFUSED by pin guard")
before = R.read_bytes()
# GAP, disclosed: the 2026-09-23 run did NOT check the README's expected-before digest (this line was a no-op then).
# The exact before bytes are kept as README.md.pre_88dee234d672 (sha256 88dee234d672...). Any re-run is pinned here.
if sha(before) != "88dee234d67254501d6087c9e077de382821732453c4467075f8181d328af1d8":
    raise SystemExit("REFUSED: README.md is not at its expected-before digest")
files = [(D / "atlas_candidate_feed_rows.jsonl", "6adc037d01ce02d4991162959e1b364bfe771915760a7875e6eae0d2de4d0f38"),
         (D / "Ezek_atlas_dimensions.v1.jsonl", "54c766dbff939f921dca0fe1b3d7a4006ff7014a8524487c1521cfee0e34632d"),
         (D / "gen_atlas_rows.py", "9e91588fbd740a2ec3703d84b020905334195de1b987c14246196ff0270b19e6"),
         (D / "check_atlas_rows.py", "069f0e6a026228f287f6fded84446634eba085c47395174573d61bcb4c54b5ea"),
         (D / "atlas_rows_check.v1.json", "78545043f69dc015086d98062b40f1e654d8729f2e984256fb5d35afa592b178"),
         (EZ / "rows_v9_final.jsonl", "a80b6e6712aa43bf3d8652255b4655a934af08a9cd3e036f9b320a37bbd1098c")]
rows = []
for p, pin in files:
    b = p.read_bytes()
    if sha(b) != pin:
        raise SystemExit("REFUSED: %s is not at its pinned digest" % p.name)
    rows.append("| `%s` | %s | `%s` |" % (str(p.relative_to(EZ.parent)).replace("\\", "/").replace("Ezek/deliverables/", "")
                                         if p.parent == D else "Ezek/" + p.name, format(len(b), ","), pin))
sec = ("## AMENDED 2026-09-23 - v9 fix round (read this before the tables below)\n\n"
       "The generator and checker now read the final corpus, `Ezek/rows_v9_final.jsonl`, not the preimage\n"
       "`Ezek/repair/rows_v7_cwo24.jsonl`. Both merged-close lanes found (low) that the rows asserted\n"
       "`candidate_review_complete` while being built from an image in which every row was still `pending`.\n"
       "Regenerating over v9 changed ONE row: `M8-Ezek-079` (writer row P06-015), field `observed_substrate_signals`,\n"
       "which now copies the corrected signals of the corpus row (lane B's SIGNAL_OUT_OF_SPAN, cured by measurement in\n"
       "`repair2/fixround_v9/signals_v9.report.json`). The other 101 rows are unchanged. The sidecar source regenerated\n"
       "byte-identical. The tables below are the 2026-09-21 build and are kept as history; these are the current bytes:\n\n"
       "| File | Bytes | sha256 |\n|---|---|---|\n" + "\n".join(rows) + "\n\n"
       "The earlier files are kept beside these as `<name>.pre_<sha12>`. Re-pointing tool:\n"
       "`repair2/fixround_v9/repoint_generators_v9.py`.\n\n")
src = before.decode("utf-8")
anchor = "\n## Files\n"
if src.count(anchor) != 1 or "AMENDED 2026-09-23 - v9" in src:
    raise SystemExit("REFUSED: anchor count %d or already amended" % src.count(anchor))
new = src.replace(anchor, "\n" + sec + "## Files\n")
keep = R.with_name(R.name + ".pre_" + sha(before)[:12])
if keep.exists() and keep.read_bytes() != before:
    raise SystemExit("REFUSED: %s exists with different bytes" % keep.name)
keep.write_bytes(before)
R.write_bytes(new.encode("utf-8"))
m = subprocess.run([sys.executable, "-B", str(EZ / "repair2" / "close_check_mirror.py"), "--dest", a.dest, "--check",
                    "atlas"], capture_output=True, text=True, encoding="utf-8", env=env)
out = json.loads(m.stdout) if m.stdout.strip().startswith("{") else {}
if not out.get("bytes_equal_to_shipped") or out.get("exit"):
    R.write_bytes(before)
    raise SystemExit("ROLLED BACK: the atlas check record no longer reproduces: %s" % json.dumps(out)[:500])
print(json.dumps({"README": [sha(before), sha(R.read_bytes())], "kept": keep.name,
                  "atlas_mirror": {"exit": out.get("exit"), "bytes_equal": out.get("bytes_equal_to_shipped")}}, indent=1))
