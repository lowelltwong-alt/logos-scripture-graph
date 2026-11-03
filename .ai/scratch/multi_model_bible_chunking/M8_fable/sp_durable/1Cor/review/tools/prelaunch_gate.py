"""Pre-send gate (E-69 and its sibling): run as the LAST command before an Agent call. Re-runs _launch_message_check on the
message file and _brief_pin_check on the brief the message names, NOW, so a pinned input that changed after the build
(an append to the ledger, a tool fix) is caught before the lane is launched, not by the lane or the recorder. On a double
MATCH it prints the message's sha256 and then the message bytes: the Agent prompt is copied from exactly that output,
and nothing may be written between this gate and the Agent call. Any failure prints GATE: REFUSED and exits 1.
usage: prelaunch_gate.py --book Dan --message PATH"""
import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
ap = argparse.ArgumentParser()
ap.add_argument("--book", required=True)
ap.add_argument("--message", required=True)
A = ap.parse_args()
# lane cap (OW-31/OW-32), counted before the launch, not by the post-launch recorder (2026-10-20 finding)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lane_cap import CAP, in_flight  # noqa: E402
live = in_flight(SP / A.book)
if len(live) >= CAP:
    raise SystemExit("GATE: REFUSED - %d lanes already in flight for %s (cap %d; record each landing first): %s"
                     % (len(live), A.book, CAP, ", ".join(live)))
msg = Path(A.message).read_bytes()
text = msg.decode("utf-8")
briefs = [ln.split("BRIEF: ", 1)[1].rsplit(" sha256 ", 1) for ln in text.splitlines() if ln.startswith("BRIEF: ")]
if len(briefs) != 1 or len(briefs[0]) != 2:
    raise SystemExit("GATE: REFUSED - the message must name exactly one 'BRIEF: <path> sha256 <hex>' line")
bpath, bsha = briefs[0][0], briefs[0][1].strip()
if len(bsha) != 64 or hashlib.sha256(Path(bpath).read_bytes()).hexdigest() != bsha:
    raise SystemExit("GATE: REFUSED - the brief's sha256 is not the digest the message names")
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
lc = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_launch_message_check.py"), "--book", A.book,
                     "--message", A.message], capture_output=True, text=True, encoding="utf-8", env=env)
pc = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_brief_pin_check.py"), "--brief", bpath],
                    capture_output=True, text=True, encoding="utf-8", env=env, cwd=SP)
if lc.returncode != 0 or pc.returncode != 0:
    raise SystemExit("GATE: REFUSED - launch check rc %d, brief pin check rc %d\n%s\n%s"
                     % (lc.returncode, pc.returncode, lc.stdout[-400:], pc.stdout[-400:]))
print("GATE: PASS message sha256 %s brief sha256 %s" % (hashlib.sha256(msg).hexdigest(), bsha))
print("=====BEGIN PROMPT=====")
print(text.rstrip("\r\n").replace("\r\n", "\n"))
print("=====END PROMPT=====")
