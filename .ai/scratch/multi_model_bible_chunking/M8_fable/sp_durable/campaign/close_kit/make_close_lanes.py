#!/usr/bin/env python3
"""Turn the close kit into one book's lane specs and close-table rows (TE-1, TE-7: data, not a new brief per book).

usage: make_close_lanes.py --params <Book>/close/close_params.v1.json --expect-before SHA [--lanes D1,D2] [--dry-run]

Run from SP. Writes <Book>/review/lane_spec_<lane>.json write-once and adds the lane to <Book>/close/close_lanes.v1.json
under the digest pin, one exact identity, without reserializing another row. A rulings pin is added for each file named in
the params. A lane already in the table refuses; so does a token left unfilled.
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
SP = HERE.parent.parent
KEYS = ["attempt_id", "execution_id", "verdict", "deliverables", "verification", "unresolved_uncertainty"]


def fill(text, t):
    for k, v in t.items():
        text = text.replace("{%s}" % k, v)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--expect-before", required=True, help="sha256 of the book's close table")
    ap.add_argument("--lanes", default="D1,D2,D3,D5")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    kit = json.loads((HERE / "close_kit_lanes.v1.json").read_text(encoding="utf-8"))
    p = json.loads((SP / a.params).read_text(encoding="utf-8"))
    B, b = p["book"], p["book_lower"]
    t = {"B": B, "b": b, "p": p["attempt_prefix"], "N": p["book_name"], "method": p["method_record"], "boss": p["boss_record"],
         "b_manifest_v1": "%s/close/%s_landed_outputs_manifest.frozen_for_close_lanes.v1.json" % (B, b)}
    table = SP / B / "close" / "close_lanes.v1.json"
    raw = table.read_bytes()
    if hashlib.sha256(raw).hexdigest() != a.expect_before:
        raise SystemExit("REFUSED: close table pin mismatch")
    d = json.loads(raw.decode("utf-8"))
    tail = b"\n  }\n }\n}\n"
    if not raw.endswith(tail):
        raise SystemExit("REFUSED: close table tail not as read")
    new_rows, specs = {}, {}
    for lane in a.lanes.split(","):
        if lane in d["lanes"]:
            raise SystemExit("REFUSED: %s is already in the close table" % lane)
        k = kit["lanes"][lane]
        attempt = fill(k["attempt"], t)
        new_rows[lane] = {"attempt": attempt, "review_lane": "close_" + lane, "out_dir": "%s_close_%s" % (p["attempt_prefix"], lane),
                          "brief": "BRIEF_" + lane, "deliverable": lane + "_result.json", "keys": KEYS, "verdict_key": "verdict",
                          "verdicts": ["delivered", "delivered_with_gaps"], "role": fill(k["role"], t), "catcher": fill(k["catcher"], t)}
        pins = [[fill(c, t) for c in row] for row in k["pins"] + kit["common_pins"]]
        pins += [[r, "read", "the controlling rulings of one round"] for r in p["rulings"]]
        missing_tok = [x for row in pins for x in row if "{" in x]
        if missing_tok:
            raise SystemExit("REFUSED: unfilled token in a pin of %s: %r" % (lane, missing_tok[0]))
        task_fill = {"BOOK_NAME": p["book_name"], "BOOK_UPPER": p["book_upper"], "BOOK_LOWER": b, "BOOK": B,
                     "PORT_RULE": fill(kit["port_rule"], t), "GROUND": p["ground"].get(lane, "")}
        spec = {"lane": lane, "attempt": attempt, "template": "BRIEF_CLOSE.template.md", "title": k["title"], "task": k["task"],
                "task_fill": task_fill, "budget": k["budget"], "out_dir": new_rows[lane]["out_dir"], "deliverable": lane + "_result.json",
                "work": k["work"], "pins": pins}
        if k.get("other_book_ok"):
            spec["other_book_ok"] = k["other_book_ok"]
        if p.get("unpinned_note"):
            spec["unpinned_note"] = p["unpinned_note"]
        specs[lane] = spec
    if a.dry_run:
        print(json.dumps({l: {"attempt": s["attempt"], "pins": len(s["pins"])} for l, s in specs.items()}))
        return 0
    for lane, spec in specs.items():
        f = SP / B / "review" / ("lane_spec_%s.json" % lane)
        if f.exists():
            raise SystemExit("REFUSED: %s exists" % f.name)
    for lane, spec in specs.items():
        (SP / B / "review" / ("lane_spec_%s.json" % lane)).write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    text = json.dumps(new_rows, indent=1, ensure_ascii=False)[2:-2]
    text = "\n".join(" " + x for x in text.split("\n"))
    new = raw[:-len(tail)] + b"\n  },\n" + text.encode("utf-8") + b"\n }\n}\n"
    d2 = json.loads(new.decode("utf-8"))
    if {k: d2["lanes"][k] for k in d["lanes"]} != d["lanes"] or {k: d2["lanes"][k] for k in new_rows} != new_rows:
        raise SystemExit("REFUSED: semantic check failed")
    tmp = table.with_name(table.name + ".tmp")
    tmp.write_bytes(new)
    os.replace(tmp, table)
    print(json.dumps({"lanes": list(new_rows), "close_table_sha256": hashlib.sha256(new).hexdigest()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
