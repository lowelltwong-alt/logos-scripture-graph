"""One landing command (TOKEN_ECONOMY_RULES TE-5): build the landing row, append it under pin, install the deliverable,
then append the learning-log line and the CYCLE_STATE note under their pins. Every step is the existing tool; this only
chains them and carries each digest forward. Prints one JSON line. Any refusal stops the chain where it stands.

usage (cwd SP):
  python -B campaign/_land_lane.py --book 1Cor --kind ctl --round 5 --agent-id ID --tokens N --tool-uses N
      --duration-ms N --outcome DELIVERED --summary TEXT [--note TEXT ...] --install-name FILE --expect-before SHA
      [--log-line-file F --log-pin SHA] [--cycle-text-file F --cycle-pin SHA] [--dry-run]
  --kind review uses tools/make_review_landing.py with --lane LANE instead of --round.
"""
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path

sys.dont_write_bytecode = True
SP = Path(__file__).resolve().parents[1]
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")


def run(args):
    p = subprocess.run([sys.executable, "-B"] + [str(a) for a in args], cwd=str(SP), env=ENV, capture_output=True, text=True, encoding="utf-8")
    out = (p.stdout or "").strip().splitlines()
    last = out[-1] if out else ""
    try:
        j = json.loads(last)
    except Exception:
        j = None
    if p.returncode != 0 or j is None:
        print(json.dumps({"stopped_at": str(args[0]), "rc": p.returncode, "stdout_tail": last[:300], "stderr_tail": (p.stderr or "")[-300:]}))
        sys.exit(1)
    return j


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def append_under_pin(target, pin, textfile):
    b = Path(target).read_bytes(); have = hashlib.sha256(b).hexdigest()
    if have != pin:
        print(json.dumps({"stopped_at": "append " + str(target), "pin_have": have, "pin_expected": pin})); sys.exit(1)
    add = Path(textfile).read_bytes().replace(b"\r\n", b"\n")
    if not b.endswith(b"\n"):
        b += b"\n"
    tmp = str(target) + ".tmp_land"
    Path(tmp).write_bytes(b + add); os.replace(tmp, target)
    return hashlib.sha256(Path(target).read_bytes()).hexdigest()


ap = argparse.ArgumentParser()
ap.add_argument("--book", required=True); ap.add_argument("--kind", choices=["ctl", "review"], required=True)
ap.add_argument("--round", type=int); ap.add_argument("--lane")
for k in ("--agent-id", "--outcome", "--summary", "--install-name", "--expect-before"):
    ap.add_argument(k, required=True)
for k in ("--tokens", "--tool-uses", "--duration-ms"):
    ap.add_argument(k, required=True, type=int)
ap.add_argument("--execution", type=int, default=1); ap.add_argument("--note", action="append", default=[])
ap.add_argument("--log-line-file"); ap.add_argument("--log-pin")
ap.add_argument("--cycle-text-file"); ap.add_argument("--cycle-pin")
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()
for f in (a.log_line_file, a.cycle_text_file):
    if f and not Path(f).is_file():
        sys.exit("REFUSED before any write: %s does not exist" % f)

R = SP / a.book / "review"
tools = R / "tools"
lower = a.book.lower()
receipts = R / ("%s_review_attempt_receipts.jsonl" % lower)
if sha(receipts) != a.expect_before:
    print(json.dumps({"stopped_at": "precheck", "receipts_have": sha(receipts)})); sys.exit(1)
if a.kind == "ctl":
    if a.round is None:
        sys.exit("--round required for ctl")
    maker = [tools / "make_ctl_landing.py", "--round", a.round]
    eid = "%s_controlling_rulings_r%d_a1#e%d" % ("cor" if a.book == "1Cor" else lower, a.round, a.execution)
    row_out = R / ("landing_row_ctl_r%d_e%d.json" % (a.round, a.execution))
else:
    if not a.lane:
        sys.exit("--lane required for review")
    maker = [tools / "make_review_landing.py", "--lane", a.lane]
    eid = None  # the maker prints row_built
    row_out = R / ("landing_row_%s_e%d.json" % (a.lane, a.execution))
maker += ["--agent-id", a.agent_id, "--tokens", a.tokens, "--tool-uses", a.tool_uses, "--duration-ms", a.duration_ms,
          "--outcome", a.outcome, "--summary", a.summary, "--out", row_out, "--execution", a.execution]
for n in a.note:
    maker += ["--note", n]
built = run(maker)
if built.get("problems"):
    print(json.dumps({"stopped_at": "row_build", "problems": built["problems"]})); sys.exit(1)
eid = built.get("row_built") or eid
result = {"row_built": eid, "gate": built.get("gate"), "rulings": built.get("rulings")}
if a.dry_run:
    result["dry_run"] = True; print(json.dumps(result)); sys.exit(0)
landed = run([R / "append_review_landing_row.py", "--row-file", row_out, "--expect-before", a.expect_before])
rec = landed["receipts"][1]
inst = run([R / "install_review_output.py", "--execution", eid, "--name", a.install_name, "--expect-before", rec])
result.update({"receipts_after_landing": rec, "installed": inst})
if a.log_line_file:
    result["learning_log_sha"] = append_under_pin(SP.parent / "orchestration_learning_log.v1.jsonl", a.log_pin, a.log_line_file)
if a.cycle_text_file:
    result["cycle_state_sha"] = append_under_pin(SP / a.book / "freeze" / "CYCLE_STATE.md", a.cycle_pin, a.cycle_text_file)
result["receipts_sha_final"] = sha(receipts); result["receipts_lines"] = sum(1 for _ in open(receipts, "rb"))
print(json.dumps(result))
