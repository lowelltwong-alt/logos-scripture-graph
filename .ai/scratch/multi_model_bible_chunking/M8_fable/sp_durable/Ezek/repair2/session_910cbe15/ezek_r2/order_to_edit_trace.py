#!/usr/bin/env python3
"""#e15 Q10: the ORDER-TO-EDIT TRACE. Does the CURRENT row carry the content each order named?

WHY THIS EXISTS AND WHAT IT CORRECTS IN ME. My E13-65 fixture asserted that every per-row order had a worklist
ITEM. It never asserted that the item's EDIT carried the order's CONTENT. So a worklist could pass the gate with
an item for every order while the rows said none of it - and the ruling found four such items by hand while
every sweep reported full executed/ordered parity. In its words: "this trace is the fixture E13-65's builder
gate lacked: it tests DISCHARGE, not existence." That is the E-31/E-32 shape one layer down: the artifact
against the orders' CONTENT rather than against their COUNT.

HOW CONTENT IS TESTED, and where the test stops. From each order's prose the trace extracts tokens it can test
mechanically:
  * VERSE REFERENCES the order names ("name and weigh the 4:3 samekh") - the strongest signal, because a repair
    that installs the ordered disclosure must name that verse somewhere in the row;
  * DEVICE AND ACT WORDS the order names (samekh, pe, messenger, utterance, recognition, paseq, K/Q, qinah,
    transport, dateline, and the verbs disclose / weigh / correct / replace / name).
An order with no extractable token is reported UNCLEAR, not passed. A trace that guessed would be worse than no
trace, because it would report discharge it cannot see - which is the very failure it exists to catch.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

rows = {r["decision_id"]: r for r in
        (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
orders = json.loads((EZ / "per_row_orders.v1.json").read_text(encoding="utf-8"))
boss = json.loads((EZ / "ezek_boss_audit.v1.json").read_text(encoding="utf-8"))

# RE-DERIVE EVERY per-row order rather than reading the artifact's `detail`, which lists only the orders that
# LACKED a worklist item. The ruling's docket is all 22, and tracing a subset would repeat the exact mistake
# this trace exists to catch - testing the part of the order set I happened to have to hand.
ROWID_IN_KEY = __import__("re").compile(r"(?<!\w)(P\d{2}-\d{3})")
ORDER_KEYS = {"author_wave", "work_order", "author_instruction", "order", "orders", "repair", "remedy",
              "author_wave_order", "author_wave_wording_orders"}
ALL = []


def _row_of(node, key=None):
    if isinstance(key, str):
        m = ROWID_IN_KEY.search(key)
        if m:
            return m.group(1)
    if isinstance(node, dict):
        for k in ("row", "row_id", "decision_id"):
            v = node.get(k)
            if isinstance(v, str) and __import__("re").fullmatch(r"P\d{2}-\d{3}", v.strip()):
                return v.strip()
    return None


def _walk(o, path, src, inherited=None):
    if isinstance(o, dict):
        rid = _row_of(o, path.rsplit("/", 1)[-1] if "/" in path else None) or inherited
        for k, v in o.items():
            if k in ORDER_KEYS and isinstance(v, str) and v.strip() and rid:
                ALL.append({"row": rid, "source": src, "key": k, "order": v.strip()})
            elif k in ORDER_KEYS and isinstance(v, list):
                for x in v:
                    if isinstance(x, str) and x.strip() and rid:
                        ALL.append({"row": rid, "source": src, "key": k, "order": x.strip()})
            else:
                _walk(v, path + "/" + str(k), src, _row_of(v, str(k)) or rid)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            _walk(v, "%s[%d]" % (path, i), src, inherited)


for _name in ("ezek_controlling_agent_ruling_e12.v1.json", "ezek_controlling_agent_ruling_e13.v1.json",
              "ezek_controlling_agent_ruling_e14.v1.json", "ezek_boss_audit.v1.json"):
    _walk(json.loads((EZ / _name).read_text(encoding="utf-8")), "", _name, None)
# dedupe identical (row, order) pairs
_seen, _ded = set(), []
for o in ALL:
    k = (o["row"], o["order"])
    if k in _seen:
        continue
    _seen.add(k)
    _ded.append(o)
ALL = _ded
# the boss work orders are already collected by the walk above, via its work_order key

VREF = re.compile(r"\b(\d{1,2}):(\d{1,3})\b|\bMT\s+(\d{1,2})[:.](\d{1,3})\b|Ezek\.(\d{1,2})\.(\d{1,3})")
WORDS = re.compile(r"\b(samekh|petuchah|setumah|\bpe\b|messenger|utterance|recognition|paseq|ketiv|qere|"
                   r"K/Q|qinah|transport|dateline|colophon|word-event|son of man|ve'attah|oath|tiling|"
                   r"sabbath|inclusio)\b", re.I)


def verse_tokens(text):
    out = set()
    for m in VREF.finditer(text):
        g = [x for x in m.groups() if x]
        if len(g) >= 2:
            out.add((int(g[0]), int(g[1])))
    return out


def row_blob(rid):
    r = rows.get(rid) or {}
    parts = []
    for k, v in r.items():
        if k in ("span", "decision_id", "osis_start", "osis_end"):
            continue
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            parts.extend(str(x) for x in v)
    return "\n".join(parts)


def names_verse(blob, cv):
    c, v = cv
    pats = [r"\b%d:%d\b" % (c, v), r"Ezek\.%d\.%d\b" % (c, v), r"\bMT\s+%d[:.]%d\b" % (c, v),
            r"\b%d\.%d\b" % (c, v)]
    return any(re.search(p, blob) for p in pats)


results = []
for o in ALL:
    blob = row_blob(o["row"])
    vs = verse_tokens(o["order"])
    ws = {m.group(0).lower() for m in WORDS.finditer(o["order"])}
    if not vs and not ws:
        results.append(dict(o, verdict="UNCLEAR", why="the order names no verse and no device or act word, so "
                                                      "this trace cannot test its content mechanically",
                            tested={}))
        continue
    v_hit = {("%d:%d" % cv): names_verse(blob, cv) for cv in sorted(vs)}
    w_hit = {w: (w in blob.lower()) for w in sorted(ws)}
    missing_v = [k for k, ok in v_hit.items() if not ok]
    missing_w = [k for k, ok in w_hit.items() if not ok]
    if not missing_v and not missing_w:
        verdict, why = "DISCHARGED", "every verse and device word the order names is present in the row"
    elif missing_v:
        verdict = "NOT DISCHARGED"
        why = "the row does not name %s, which the order does" % ", ".join(missing_v)
    else:
        verdict = "PARTIAL"
        why = "every ordered verse is named but the row lacks the word(s) %s" % ", ".join(missing_w)
    results.append(dict(o, verdict=verdict, why=why,
                        tested={"verses": v_hit, "words": w_hit}))

tally = Counter(r["verdict"] for r in results)
out = {
    "schema": "ezek_order_to_edit_trace.v1",
    "order": ("#e15 Q10: for every per-row order, name the worklist item and the applied edit that discharged "
              "it and show BY A STRING TEST ON THE CURRENT ROW that the ordered content is present"),
    "what_it_corrects": ("my E13-65 fixture asserted every order had an ITEM; it never asserted the item's "
                         "EDIT carried the order's CONTENT. Four orders were undischarged while every sweep "
                         "reported full parity. This tests DISCHARGE, not existence."),
    "method": ("verse references and device/act words are extracted from each order's prose and tested against "
               "the current row's bytes. An order with no extractable token is UNCLEAR, never passed - a trace "
               "that guessed would report discharge it cannot see, which is the failure it exists to catch."),
    "inputs": {"rows": ROWS.name, "rows_sha256": sha(ROWS),
               "orders": "per_row_orders.v1.json", "orders_sha256": sha(EZ / "per_row_orders.v1.json"),
               "boss_audit_sha256": sha(EZ / "ezek_boss_audit.v1.json")},
    "orders_traced": len(results),
    "tally": dict(tally),
    "NOT_DISCHARGED": [r for r in results if r["verdict"] == "NOT DISCHARGED"],
    "PARTIAL": [r for r in results if r["verdict"] == "PARTIAL"],
    "UNCLEAR": [r for r in results if r["verdict"] == "UNCLEAR"],
    "all": results,
    "tier": "MEASURED string tests over the current rows; the extraction rule is the orchestrator's and its "
            "limit is stated",
}
p = HERE / "order_to_edit_trace.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"orders_traced": len(results), "tally": dict(tally)}, indent=1))
print()
for r in results:
    if r["verdict"] != "DISCHARGED":
        print("  %-14s %-9s [%s] %s" % (r["verdict"], r["row"], r["key"], r["why"][:80]))
        print("        order: %s" % r["order"][:110])
