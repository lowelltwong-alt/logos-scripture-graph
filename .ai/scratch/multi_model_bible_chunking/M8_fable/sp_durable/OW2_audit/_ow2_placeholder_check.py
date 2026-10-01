#!/usr/bin/env python3
r"""Placeholder-rejection check (OW-3 item 3, owner directive 2026-09-04): any
unexpanded template token of the form {name} inside a review packet, docket or
proposal is a defect — such text must be resolved from source bytes before any
application. Two modes:
  --gate FILE...    fail (exit 1) if any listed packet carries a placeholder
                    (wave-close gate for every NEW packet in every lane);
  --report          scan every packet under ./reviews plus the receipts dockets
                    and list hits (exit 0) — the pre-OW-3 item-1 packets are a
                    frozen baseline: their hits are RECORDED, never edited.
Standalone so the item-1 verifiers pinned in receipts/OW2_isa_lf_audit.json stay
byte-identical; the unpinned item-2/3 verifiers carry the same arm inline.
"""
import glob
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
PLACEHOLDER = re.compile(r"\{[A-Za-z][A-Za-z0-9_\-\.:]*\}|\{[0-9][A-Za-z0-9_\-\.:]*\}")


def scan(path: Path):
    txt = path.read_text(encoding="utf-8", errors="replace")
    hits = []
    for m in PLACEHOLDER.finditer(txt):
        hits.append({"token": m.group(0), "context": txt[max(0, m.start() - 90):m.end() + 60].replace("\n", " ")})
    return hits


def main() -> int:
    args = sys.argv[1:]
    if args and args[0] == "--gate":
        bad = {}
        for f in args[1:]:
            h = scan(Path(f))
            if h:
                bad[f] = h
        print(json.dumps({"placeholder_gate": "FAIL" if bad else "PASS", "files": len(args) - 1, "hits": bad},
                         ensure_ascii=False, indent=1))
        return 1 if bad else 0
    files = sorted(glob.glob(str(HERE / "reviews" / "*.json"))) + \
        sorted(glob.glob(str(M8 / "receipts" / "*docket*.json")))
    report = {}
    for f in files:
        h = scan(Path(f))
        if h:
            report[Path(f).name] = [x["token"] for x in h]
    print(json.dumps({"placeholder_report": "HITS" if report else "CLEAN", "files_scanned": len(files),
                      "hits": report}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
