#!/usr/bin/env python3
"""Collect every ruling that routes an item to the end review into <Book>/fable_end_review/routed_items.v1.jsonl.

A ruling is taken when its `decision` or one of its `orders` names `fable_end_review`. Each field is TRANSCRIBED; `order`
keeps only the order sentences that name the route, and `decision` is whole. Same output shape as Daniel's file, so the
end-review packet generator reads it unchanged. Book-agnostic (TE-7): it takes the book's close params.

usage (from SP): python -B campaign/close_kit/gen_routed_items.py --params <Book>/close/close_params.v1.json [--check]
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(__file__).resolve().parents[2]
ROUTE = "fable_end_review"
STATUS = "OWED (OW-28: Fable reviews at the campaign's end; OW-30: no Fable call without new owner authorization)"


def orders_of(rule):
    o = rule.get("orders") or []
    return [o] if isinstance(o, str) else [x if isinstance(x, str) else json.dumps(x, ensure_ascii=False) for x in o]


def items(book, rulings):
    out, seen = [], set()
    for rel in rulings:
        d = json.loads((SP / rel).read_text(encoding="utf-8"))
        source = "%s#%s" % (d["attempt_id"], d["execution_id"]) if "#" not in str(d["execution_id"]) else d["execution_id"]
        for rule in d["rulings"]:
            named = [x for x in orders_of(rule) if ROUTE in x]
            if not named and ROUTE not in str(rule.get("decision", "")):
                continue
            if rule["id"] in seen:
                raise SystemExit("REFUSED: ruling id %s appears twice" % rule["id"])
            seen.add(rule["id"])
            out.append({"schema": "m8_fable_end_review_item.v1", "book": book, "id": rule["id"], "from": source,
                        "ruling": rule["ruling"], "decision": rule["decision"], "order": " ".join(named), "status": STATUS})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--expect-before", help="sha256 of the list this run may replace, when a later ruling adds items")
    a = ap.parse_args()
    p = json.loads((SP / a.params).read_text(encoding="utf-8"))
    rows = items(p["book"], p["rulings"])
    data = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8")
    target = SP / p["book"] / "fable_end_review" / "routed_items.v1.jsonl"
    if a.check:
        print("MATCH" if target.is_file() and target.read_bytes() == data else "DIFFERS")
        return
    if target.exists() and target.read_bytes() != data:
        if hashlib.sha256(target.read_bytes()).hexdigest() != a.expect_before:
            raise SystemExit("REFUSED: %s exists with different bytes" % target.name)
    target.parent.mkdir(exist_ok=True)
    target.write_bytes(data)
    print(json.dumps({"items": len(rows), "ids": [r["id"] for r in rows]}))


if __name__ == "__main__":
    main()
