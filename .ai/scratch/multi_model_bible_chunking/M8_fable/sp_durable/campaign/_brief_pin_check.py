#!/usr/bin/env python3
"""Pre-launch pin check (ledger OW-11-l, 2026-09-11): before a brief is launched, every file its input table pins by digest must
still carry that digest on disk.

WHY. SP/Ezek/FIXUP_BRIEF.md pinned SP/Ezek/ezek_p0_retained_lows.v1.json at 85dfd154 when it was built. The orchestrator's
rebinds append then changed the file to 519dda47, and the eleven FIXUP-1 parts launched minutes later on the stale table. One
part's own digest check found the mismatch. The in-flight pin guard could not help, because nothing was in flight at the
append. A brief is not launched while any pin disagrees with disk.

Reads the rows '| `SP\\<path>` | `<64 hex>` |', the shape the landing tools parse. Exit 0 when every pinned file exists with its
digest; 1 on any drift or missing file; 2 on a usage error or a brief with no table rows. Read-only.

Usage: _brief_pin_check.py --brief <path> [--brief <path> ...]
       _brief_pin_check.py --selftest"""
import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

SP = Path(__file__).resolve().parent.parent
ROW = re.compile(r"^\| `SP\\(.+?)` \| `([0-9a-f]{64})` \|$")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def check(sp, brief):
    out = {"brief": str(brief), "pins": 0, "drift": [], "missing": []}
    for line in Path(brief).read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if not m:
            continue
        out["pins"] += 1
        p = sp / m.group(1).replace("\\", "/")
        if not p.is_file():
            out["missing"].append(m.group(1))
        elif sha(p) != m.group(2):
            out["drift"].append({"path": m.group(1), "pinned": m.group(2), "on_disk": sha(p)})
    out["verdict"] = "NO_TABLE" if not out["pins"] else ("DRIFT" if out["drift"] or out["missing"] else "MATCH")
    return out


def selftest():
    with tempfile.TemporaryDirectory() as td:
        sp = Path(td) / "sp_durable"
        (sp / "Book").mkdir(parents=True)
        f = sp / "Book" / "a.json"
        f.write_text("{}", encoding="utf-8")
        good = sp / "Book" / "GOOD.md"
        good.write_text("| path | sha256 |\n|---|---|\n| `SP\\Book\\a.json` | `%s` |\n" % sha(f), encoding="utf-8")
        stale = sp / "Book" / "STALE.md"
        stale.write_text("| `SP\\Book\\a.json` | `%s` |\n" % ("0" * 64), encoding="utf-8")
        gone = sp / "Book" / "GONE.md"
        gone.write_text("| `SP\\Book\\b.json` | `%s` |\n" % sha(f), encoding="utf-8")
        none = sp / "Book" / "NONE.md"
        none.write_text("reads SP\\Book\\a.json\n", encoding="utf-8")
        vectors = [("every pin matches", good, "MATCH"), ("a pinned file changed after the brief was built", stale, "DRIFT"),
                   ("a pinned file is missing", gone, "DRIFT"), ("a brief with no table rows", none, "NO_TABLE")]
        results = [{"vector": n, "want": w, "got": check(sp, b)["verdict"]} for n, b, w in vectors]
        f.write_text('{"changed": true}', encoding="utf-8")
        results.append({"vector": "the matching brief after its file changes", "want": "DRIFT", "got": check(sp, good)["verdict"]})
    failed = [r for r in results if r["got"] != r["want"]]
    print(json.dumps({"selftest": "m8_brief_pin_check", "vectors": len(results), "failed": failed,
                      "verdict": "GREEN" if not failed else "RED"}, indent=1))
    return 0 if not failed else 1


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", action="append", default=[])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.brief:
        print("usage: --brief <path> [...] | --selftest", file=sys.stderr)
        return 2
    outs = [check(SP, b) for b in a.brief]
    verdict = ("NO_TABLE" if any(o["verdict"] == "NO_TABLE" for o in outs)
               else "DRIFT" if any(o["verdict"] == "DRIFT" for o in outs) else "MATCH")
    print(json.dumps({"briefs": outs, "verdict": verdict}, ensure_ascii=False, indent=1))
    return {"MATCH": 0, "DRIFT": 1, "NO_TABLE": 2}[verdict]


if __name__ == "__main__":
    raise SystemExit(main())
