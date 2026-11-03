"""Repoint the resume cursor line by exact old phase, under a pin; the rest of the file stays byte-identical.
usage: carry_resume.py --pin SHA --old PHASE --text-file FILE (FILE holds the whole new cursor line, no newline)"""
import argparse, hashlib, os
from pathlib import Path
HERE = Path(__file__).resolve().parent
res = HERE.parents[3] / "RESUME_PROMPT_CURRENT.md"
ap = argparse.ArgumentParser()
for k in ("--pin", "--old", "--text-file"):
    ap.add_argument(k, required=True)
a = ap.parse_args()
sha = lambda b: hashlib.sha256(b).hexdigest()
b = res.read_bytes()
if sha(b) != a.pin:
    raise SystemExit("REFUSED: resume is at %s" % sha(b)[:12])
key = ("cursor: phase = %s " % a.old).encode("utf-8")
if b.count(key) != 1:
    raise SystemExit("REFUSED: cursor count %d" % b.count(key))
new = Path(a.text_file).read_bytes().rstrip(b"\n")
if b"\r" in new or b"\n" in new or not new.startswith(b"cursor: phase = "):
    raise SystemExit("REFUSED: new line form")
start = b.index(key)
end = b.index(b"\n", start)
t = res.with_suffix(res.suffix + ".tmp_carry")
t.write_bytes(b[:start] + new + b[end:])
os.replace(t, res)
print(sha(res.read_bytes()))
