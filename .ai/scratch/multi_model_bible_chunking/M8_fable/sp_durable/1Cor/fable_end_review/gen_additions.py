"""Write the 1 Corinthians end-review additions file (R8-ROUTING, plus R9-PF, R9-SPANS and R9-GATE-TOOLS).

routed_items.v1.jsonl stays byte-unchanged (R8-ROUTING). Every item's words are sliced from the pinned rulings
files; the generator refuses if a slice is not found exactly once. Run with --check to compare without writing.
"""
import hashlib
import json
import sys
from pathlib import Path

BK = Path(__file__).resolve().parents[1]
OUT = BK / "fable_end_review" / "routed_items_additions.v1.jsonl"
PINS = {
    "E8": ("review/1cor_controlling_agent_rulings_E8.v1.json",
           "5ff790b9725c0413915350b9121ea22643952bd751f730224578a1448d089fd7"),
    "E9": ("review/1cor_controlling_agent_rulings_E9.v1.json",
           "66fa2020b76c3c702906501723cc4c5f997e897a74725d0b1ac120bfd5eda37c"),
}
STATUS = "OWED (OW-28: Fable reviews at the campaign's end; OW-30: no Fable call without new owner authorization)"

# (item id, rulings file, ruling id, exact slice of that ruling's decision or of one of its orders)
ITEMS = [
    ("ADD-R8-01", "E8", "R8-ROUTING", "R7-NOT-TESTABLE reading (0 tokens in routed items)"),
    ("ADD-R8-02", "E8", "R8-ROUTING", "S8 and lens on repair bytes (PF-1, PF-4)"),
    ("ADD-R8-03", "E8", "R8-ROUTING", "the two flags at lanes' NQ-9 and NQ-14, including that v7 section 9 rule 2 is "
                                      "unmet in the strategy (repair, round, fix-up, fixup all 0 hits)"),
    ("ADD-R8-04", "E8", "R8-ROUTING", "W5-014 seam"),
    ("ADD-R8-05", "E8", "R8-ROUTING", "W2-014 and W2-015 open pair"),
    ("ADD-R8-06", "E8", "R8-ROUTING", "WEB term"),
    ("ADD-R8-07", "E8", "R8-ROUTING", "byte-equality construction and blindness"),
    ("ADD-R8-08", "E8", "R8-ROUTING", "item 24 strings"),
    ("ADD-R8-09", "E8", "R8-ROUTING", "the DUE_AT_CLOSE tool change"),
    ("ADD-R9-PF-08", "E9", "R9-PF", "PF-8: no v8 byte change at this close (R8-GATE-24-25). The l.955 sentence on the "
                                    "boss audit and D1, D2 and D5 is stated as REPORTED (orchestrator) in the close "
                                    "evidence under item_24 and is corrected at the next method version."),
    ("ADD-R9-PF-09", "E9", "R9-PF", "PF-9: correct at the next method version; routed to end review."),
    ("ADD-R9-PF-12", "E9", "R9-PF", "PF-12: the orchestrator records, in the close evidence, either the confirmation "
                                    "with its source or a disclosure that none exists (UNAVAILABLE). Routed to end "
                                    "review."),
    ("ADD-R9-PF-13", "E9", "R9-PF", "The validator report's missing corpus sha is cured at this close by recording the "
                                    "rows sha beside the report in the close evidence. Any tool change goes to end "
                                    "review."),
    ("ADD-R9-SPANS", "E9", "R9-SPANS", "Record: R5-S5-11 is amended by id at R9-SPANS for W3-003 and W3-006 only. The "
                                       "agreement among lanes and controllers on this book is one model family (OW-19)."),
    ("ADD-R9-TOOLS", "E9", "R9-GATE-TOOLS", "campaign/_close_book.py: in close_evidence_gate, count an item as missing "
                                            "when value is None, empty or the string 'UNAVAILABLE', when tier is "
                                            "'UNAVAILABLE', or when source is absent or empty."),
]
# Orchestrator disclosure (not a ruling slice): GATE-E9 s2 condition 6 ordering.
DISCLOSURE = {
    "id": "ADD-ORCH-01", "from": "orchestrator", "ruling": "disclosure",
    "decision": "GATE-E9 s2 condition 6 required this additions file to be written and pinned before the _a2 lanes were "
                "reissued. The lanes were launched at 2026-11-03T06:39:17Z before it existed; the close-evidence half "
                "of the condition was met (0b42eae2 in the carrier). Neither _a2 brief pins or reads this file, so the "
                "lanes' inputs are unchanged; the order the gate set was not kept. Disclosed to the owner in the "
                "pre-close report.",
    "order": None,
}


def build():
    src = {}
    for k, (rel, pin) in PINS.items():
        b = (BK / rel).read_bytes()
        h = hashlib.sha256(b).hexdigest()
        if h != pin:
            raise SystemExit("REFUSED: %s is %s, pinned %s" % (rel, h[:12], pin[:12]))
        src[k] = json.loads(b)
    rows = []
    for iid, f, rid, sl in ITEMS:
        r = [x for x in src[f]["rulings"] if x["id"] == rid]
        if len(r) != 1:
            raise SystemExit("REFUSED: ruling %s not unique in %s" % (rid, f))
        r = r[0]
        texts = [r["decision"]] + [o["order"] for o in r.get("orders", [])]
        hits = sum(t.count(sl) for t in texts)
        if hits != 1:
            raise SystemExit("REFUSED: %s slice found %d times in %s" % (iid, hits, rid))
        order = [o for o in r.get("orders", []) if o["to"] == "fable_end_review"]
        rows.append({"schema": "m8_fable_end_review_item.v1", "book": "1Cor", "id": iid,
                     "from": src[f]["execution_id"], "ruling_id": rid, "ruling": r["ruling"], "decision": sl,
                     "order": json.dumps(order[0], ensure_ascii=False) if order else None,
                     "source": "%s sha256 %s" % PINS[f], "status": STATUS})
    d = dict(DISCLOSURE)
    d.update({"schema": "m8_fable_end_review_item.v1", "book": "1Cor", "ruling_id": None,
              "source": "1Cor/review/1cor_review_attempt_receipts.jsonl launch rows cor_merged_close_lane_{a,b}_a2#e1",
              "status": STATUS})
    rows.append(d)
    return "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows).encode("utf-8")


if __name__ == "__main__":
    new = build()
    if "--check" in sys.argv:
        cur = OUT.read_bytes() if OUT.exists() else b""
        print("MATCH" if cur == new else "DIFFERS", hashlib.sha256(new).hexdigest())
        raise SystemExit(0 if cur == new else 1)
    if OUT.exists():
        raise SystemExit("REFUSED: %s exists; use --check" % OUT.name)
    tmp = OUT.with_suffix(".jsonl.tmp")
    tmp.write_bytes(new)
    tmp.replace(OUT)
    print(len(new.splitlines()), "items", hashlib.sha256(new).hexdigest())
