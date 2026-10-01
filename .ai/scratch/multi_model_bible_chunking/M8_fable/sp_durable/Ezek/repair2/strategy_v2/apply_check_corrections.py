#!/usr/bin/env python3
"""Apply the distinct checker's exact corrections to the strategy v2 candidate, re-verify, then PROMOTE it to the book's
durable strategy v2. The checker returned not_fit with two minor defects, each carrying find/replace strings it asserted
unique; this applies them by exact-string replacement with a uniqueness assertion per correction, so a moved target is a
refusal rather than a silent first-match edit.

After the edits it re-runs the checker's two measurable claims itself:
  - every parashah-mark mention in the corrected lines carries 'single witness';
  - the year-word sweep's own numbers now read 14 formulae + 4 durations + 1 false hit, and 26:10 is no longer called a
    duration.
Then the corrected candidate is copied to Ezek/book_strategy_Ezek.v2.md (v1 is never touched), and both digests print.

usage: python apply_check_corrections.py [--apply]
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
CAND = EZ / "author" / "strategy_v2" / "book_strategy_Ezek.v2.md"
CHECK = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
             r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_strategy_v2_check\strategy_v2_check.json")
DURABLE = EZ / "book_strategy_Ezek.v2.md"
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731
chk = json.loads(CHECK.read_text(encoding="utf-8"))
if chk["verdict"] != "not_fit":
    raise SystemExit("REFUSED: the check verdict is %r; this tool applies a not_fit's corrections" % chk["verdict"])
text = CAND.read_text(encoding="utf-8")
pre = sha(CAND.read_bytes())
applied = []
for d in chk["defects"]:
    for c in d.get("corrections") or []:
        find, repl = c["find"], c["replace"]
        n = text.count(find)
        if n != 1:
            raise SystemExit("REFUSED: %s find-string occurs %d times, not once:\n  %r" % (d["id"], n, find[:90]))
        text = text.replace(find, repl)
        applied.append({"defect": d["id"], "chars_before": len(find), "chars_after": len(repl)})
# the checker's own two claims, re-measured here on the corrected text
for phrase in ("Parashah marks (single witness):", "the samekh at 43:9 (single witness) is 103 verses",
               "the pe recorded at MT 3:16 (single witness)"):
    if phrase not in text:
        raise SystemExit("POSTCHECK FAILED: %r is absent after the edits" % phrase)
if "4 are durations (4:6, 29:11, 29:12," not in text or "5 are durations (4:6, 26:10" in text:
    raise SystemExit("POSTCHECK FAILED: the year-word sweep sentence still reads as before")
print(json.dumps({"candidate": CAND.name, "preimage_sha256": pre, "corrections_applied": applied,
                  "postimage_sha256_computed": sha(text.encode("utf-8")), "apply": "--apply" in sys.argv}, indent=1))
if "--apply" not in sys.argv:
    raise SystemExit(0)
backup = CAND.with_suffix(CAND.suffix + ".pre_" + pre[:12])
if not backup.exists():
    shutil.copy2(CAND, backup)
CAND.write_text(text, encoding="utf-8", newline="\n")
post = sha(CAND.read_bytes())
if DURABLE.exists() and DURABLE.read_bytes() != CAND.read_bytes():
    raise SystemExit("REFUSED: %s already exists with different bytes (E-41)" % DURABLE.name)
DURABLE.write_bytes(CAND.read_bytes())
print(json.dumps({"corrected_candidate_sha256": post, "promoted_to": "Ezek/" + DURABLE.name,
                  "promoted_sha256": sha(DURABLE.read_bytes()), "v1_untouched_sha256": sha((EZ / "book_strategy_Ezek.md").read_bytes()),
                  "backup": backup.name}, indent=1))
