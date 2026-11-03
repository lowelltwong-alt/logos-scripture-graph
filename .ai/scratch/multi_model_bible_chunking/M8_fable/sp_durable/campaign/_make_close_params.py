"""Write <BOOK>/close/close_params.v1.json from <BOOK>/close/close_spec.v1.json, every pin MEASURED from disk at this run.

  python -B _make_close_params.py --book BOOK [--allow-pending] [--m8-root DIR] [--spec FILE] [--out FILE]

The spec is short and hand-written: `facts` are copied as they stand (TRANSCRIBED), `measure` names the inputs whose digests
and counts this tool reads from the bytes. An absent input is refused; with --allow-pending it is recorded as the literal
"PENDING", and the close tool treats "PENDING" as UNMET. A fact written "PENDING" in the spec needs --allow-pending too.
No clock, no randomness, no directory scan: every input is a path named in the spec. Non-authorizing.
"""
import argparse
import collections
import hashlib
import importlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PENDING = "PENDING"
FACTS = ("BOOK_NAME", "BOOKS_BEFORE", "BOOKS_AFTER", "PREV_BOOK", "MODEL_ID", "DECISION_ID_FORM", "ZONE", "ZONE_LABEL",
         "PARENTS_LABEL", "LANGUAGE_CODES", "LANGUAGE_MIXED", "LINEAGE_FIELDS", "SUITE_NORMALIZE_KEY", "PARITY_TOOL", "PARITY_ARGS",
         "BOSS_E2_SUPERSEDES", "BOSS_E2_LABEL", "BOSS_CONDITIONS", "BOSS_CONDITIONS_LABEL", "CARRIER_REL", "CARRIER_GEN_REL",
         "CARRIER_FACTS", "SHAPE_GRANTED_BY", "HOLD_FIELDS", "LANES", "MERGED_RECEIPTS_REL", "LANDING_REL", "LANE_FILES",
         "UNMET_TYPES", "SCHOLAR_FILES", "SIDE_FIELDS", "SIDECAR", "GEN_SIDECARS_REL", "FEED_REL", "SHARED", "RETENTION",
         "PACKET_REL", "PACKET_GEN", "PACKET_GEN_ARGS", "NEXT_BOOK_PATTERN", "NEXT_BOOK_EXPECTED", "NEXT_BOOK_LABEL",
         "NEXT_PLACEHOLDER", "LOCK_NAME", "NOT_EVALUATED", "FAMILIES", "TEXT", "RECEIPT_FILES", "LANDED_ROOTS", "CWO")
MEASURE = ("corpus", "manifest", "built_from", "lookup", "landed_rel", "boss", "routed_rel", "parent_label_len")
ABSENT = []


def digest(p, name):
    """The file's sha256, or PENDING with the name recorded for the refusal."""
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except OSError:
        ABSENT.append(name)
        return PENDING


def jsonl(p):
    return [json.loads(x) for x in Path(p).read_bytes().decode("utf-8").split("\n") if x.strip()]


def row_facts(rows, keylen):
    """Counts of the row file the corpus is built from: the corpus gates then test the final file against these."""
    parents = [str(r.get("parent_collection"))[:keylen] for r in rows]
    runs = [k for i, k in enumerate(parents) if i == 0 or parents[i - 1] != k]
    return {"ROWS": len(rows), "PARENTS": runs,
            "LANGUAGE_COUNTS": dict(sorted(collections.Counter(str(r.get("language")) for r in rows).items())),
            "LOW_ROWS": sum(1 for r in rows if r.get("confidence") in ("low", "medium_low"))}


def lookup_facts(lk, bk, numbering_on):
    """VERSES and CHAPTERS from the book's lookup, and the moved-verse count from its numbering map."""
    p = bk / lk["path"]
    if not p.is_file():
        return {"VERSES": PENDING, "CHAPTERS": PENDING, "ZONE_MOVED": PENDING}
    if lk["kind"] == "inventory":
        inv = json.loads(p.read_text(encoding="utf-8"))
        if inv.get("numbering_face") != lk["face"]:                # the inventory's obligation: assert the face, never infer it
            raise SystemExit("REFUSED: %s declares numbering face %r, the spec expects %r" % (p.name, inv.get("numbering_face"), lk["face"]))
        counts = {int(c): int(v) for c, v in inv["chapters"].items()}
        if sum(counts.values()) != inv.get("total_verses"):
            raise SystemExit("REFUSED: %s does not add up to its total_verses" % p.name)
        if numbering_on:
            raise SystemExit("REFUSED: an inventory lookup has no numbering map, and the numbering_zone family is on")
        return {"VERSES": inv["total_verses"], "CHAPTERS": len(counts), "ZONE_MOVED": 0}
    if lk["kind"] != "module":
        raise SystemExit("REFUSED: lookup.kind is neither module nor inventory")
    sys.path.insert(0, str(p.parent))
    lib = importlib.import_module(lk["module"])
    moved = sum(1 for c in sorted(lib.LAST_VERSE) for v in range(1, lib.LAST_VERSE[c] + 1) if lib.web_to_mt(c, v) != (c, v))
    return {"VERSES": lib.TOTAL_VERSES, "CHAPTERS": len(lib.LAST_VERSE), "ZONE_MOVED": moved}


def write_atomic(path, data):
    if b"\r" in data:
        raise SystemExit("REFUSED: a CR byte in the output")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".maketmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", required=True)
    ap.add_argument("--allow-pending", action="store_true")
    ap.add_argument("--m8-root")
    ap.add_argument("--spec")
    ap.add_argument("--out")
    a = ap.parse_args()
    if not re.match(r"^[1-3]?[A-Z][A-Za-z]{1,7}$", a.book):
        raise SystemExit("REFUSED: --book is not a book name")
    m8 = Path(a.m8_root).resolve() if a.m8_root else HERE.parent.parent
    sp, bk = m8 / "sp_durable", m8 / "sp_durable" / a.book
    spec_p = Path(a.spec).resolve() if a.spec else bk / "close" / "close_spec.v1.json"
    spec_b = spec_p.read_bytes()
    spec = json.loads(spec_b.decode("utf-8"))
    if spec.get("schema") != "m8_close_spec.v1" or spec.get("book") != a.book:
        raise SystemExit("REFUSED: the spec is not m8_close_spec.v1 for book %s" % a.book)
    facts, meas = spec.get("facts") or {}, spec.get("measure") or {}
    miss = [k for k in FACTS if k not in facts] + [k for k in MEASURE if k not in meas]
    if miss:
        raise SystemExit("REFUSED: the spec lacks: " + ", ".join(miss))
    c = {"BOOK": a.book}
    c.update({k: facts[k] for k in FACTS})
    where = {k: "TRANSCRIBED from the spec" for k in FACTS}
    pre = "sp_durable/%s/" % a.book

    def pin(name, rel, path):
        c[name] = digest(path, rel)
        where[name] = "MEASURED: sha256 of %s" % rel

    c["CORPUS"], c["MANIFEST"], c["BUILT_FROM"] = meas["corpus"], meas["manifest"], meas["built_from"]
    where.update(dict.fromkeys(("CORPUS", "MANIFEST", "BUILT_FROM"), "TRANSCRIBED from the spec"))
    pin("CORPUS_PIN", pre + meas["corpus"], bk / meas["corpus"])
    pin("MANIFEST_PIN", pre + meas["manifest"], bk / meas["manifest"])
    pin("BUILT_FROM_PIN", meas["built_from"], m8 / meas["built_from"])
    if c["BUILT_FROM_PIN"] == PENDING:
        c.update(dict.fromkeys(("ROWS", "PARENTS", "LANGUAGE_COUNTS", "LOW_ROWS"), PENDING))
    else:
        c.update(row_facts(jsonl(m8 / meas["built_from"]), int(meas["parent_label_len"])))
    where.update(dict.fromkeys(("ROWS", "PARENTS", "LANGUAGE_COUNTS", "LOW_ROWS"), "MEASURED: counted from %s" % meas["built_from"]))

    lk = dict(meas["lookup"])
    lk["pin"] = digest(bk / lk["path"], pre + lk["path"])
    c["LOOKUP"] = lk
    where["LOOKUP"] = "MEASURED pin of %s; the rest TRANSCRIBED from the spec" % (pre + lk["path"])
    fam = (facts["FAMILIES"].get("numbering_zone") or {}) if isinstance(facts["FAMILIES"], dict) else {}
    c.update(lookup_facts(lk, bk, fam.get("enabled") is True))
    where.update(dict.fromkeys(("VERSES", "CHAPTERS", "ZONE_MOVED"), "MEASURED: read from %s" % (pre + lk["path"])))

    stem = meas["corpus"].replace(".jsonl", "")
    pin("SUITE_PIN", pre + meas["corpus"] + ".validator_report.json", bk / (meas["corpus"] + ".validator_report.json"))
    pin("PARITY_PIN", pre + "cwo/cwo_parity.%s.json" % stem, bk / "cwo" / ("cwo_parity.%s.json" % stem))

    c["LANDED_REL"] = meas["landed_rel"]
    where["LANDED_REL"] = "TRANSCRIBED from the spec"
    pin("LANDED_PIN", pre + meas["landed_rel"], bk / meas["landed_rel"])
    if c["LANDED_PIN"] == PENDING:
        c["LANDED_OUTPUTS"], c["LANDED_RECEIPT_FILES"] = PENDING, PENDING
    else:
        m = json.loads((bk / meas["landed_rel"]).read_text(encoding="utf-8"))
        c["LANDED_OUTPUTS"], c["LANDED_RECEIPT_FILES"] = len(m["outputs"]), len(m["receipt_files"])
    where.update(dict.fromkeys(("LANDED_OUTPUTS", "LANDED_RECEIPT_FILES"), "MEASURED: counted from %s" % (pre + meas["landed_rel"])))

    c["BOSS"] = [[tag, rel, digest(bk / rel, pre + rel)] for tag, rel in meas["boss"]]
    where["BOSS"] = "MEASURED: sha256 of each named record; tags and paths TRANSCRIBED from the spec"

    c["ROUTED_REL"] = meas["routed_rel"]
    where["ROUTED_REL"] = "TRANSCRIBED from the spec"
    pin("ROUTED_PIN", pre + meas["routed_rel"], bk / meas["routed_rel"])
    c["ROUTED_ITEMS"] = PENDING if c["ROUTED_PIN"] == PENDING else len(jsonl(bk / meas["routed_rel"]))
    where["ROUTED_ITEMS"] = "MEASURED: counted from %s" % (pre + meas["routed_rel"])

    # The close tool's OPTIONAL facts, set only for a book whose controlling rounds ordered them; the close-evidence
    # file is pinned here like any other input, never transcribed.
    for k in ("DUE_AT_CLOSE", "READ_RECORD", "CLOSE_EVIDENCE_REL"):
        if k in facts:
            c[k] = facts[k]
            where[k] = "TRANSCRIBED from the spec"
    if "CLOSE_EVIDENCE_REL" in facts:
        pin("CLOSE_EVIDENCE_PIN", pre + facts["CLOSE_EVIDENCE_REL"], bk / facts["CLOSE_EVIDENCE_REL"])

    def holes(x, name):
        if x == PENDING:
            return [name]
        if isinstance(x, dict):
            return [p for k, v in sorted(x.items()) for p in holes(v, name + "." + str(k))]
        if isinstance(x, list):
            return [p for i, v in enumerate(x) for p in holes(v, "%s[%d]" % (name, i))]
        return []
    pending = sorted(p for k in c for p in holes(c[k], k))
    if pending and not a.allow_pending:
        raise SystemExit("REFUSED: absent input or unstated fact (name them, or pass --allow-pending): "
                         + ", ".join(ABSENT + pending))
    doc = {"schema": "m8_close_params.v1", "book": a.book, "non_authorizing": True,
           "written_by": "campaign/_make_close_params.py", "spec_sha256": hashlib.sha256(spec_b).hexdigest(),
           "note": "every pin below was measured from disk at this run; PENDING is UNMET in the close tool",
           "pending": pending, "absent_inputs": sorted(set(ABSENT)), "constants": c, "where_each_came_from": where}
    out = Path(a.out).resolve() if a.out else bk / "close" / "close_params.v1.json"
    data = (json.dumps(doc, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    write_atomic(out, data)
    print(json.dumps({"written": out.name, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "pending": len(pending)}))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
