#!/usr/bin/env python3
"""Build <BOOK>/rows_v1_final.jsonl and <BOOK>/rows_v1_final.manifest.json from the book's fixup-applied rows, so the close
tool's lineage gates can pass. The manifest is in the form of Dan/rows_v1_final.manifest.json. Book-agnostic.

  python -B _build_final_rows.py --book BOOK --from REL --written STAMP --holds TEXT --boss-rows TAG=CONFIRM,RETURN
         [--merge TEXT] [--m8-root DIR] [--params FILE] [--out-root DIR] (--write | --check)

  --from       the source rows, relative to the M8 tree; must be the parameters' BUILT_FROM at its pin
  --written    the manifest's time stamp, in UTC (YYYY-MM-DDTHH:MM:SSZ). This tool has no clock.
  --holds      the manifest's sentence on holds; this tool cannot measure why a book has none
  --boss-rows  the boss audit's row counts, per record that states them (the record's form is the auditor's, not this tool's)
  --merge      how two boss records are joined; required when the parameters name two
  --out-root   where the files go (default: the book directory)
  --check      regenerate both files and compare bytes with what is there; writes nothing; exit 0 only on MATCH
  --write      write both under an exclusive lock, whole, LF, through a temporary file and an atomic replace. An existing file
               with other bytes is first kept beside it as <name>.pre_<sha12> (E-44); any failure rolls both back.

Every row changes in exactly the fields HOLD_FIELDS names and in no other; a row that would differ otherwise is refused. A value
this tool cannot measure is a named argument, never a default. No clock, no randomness, no directory scan. Non-authorizing.
"""
import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
PENDING = "PENDING"
STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def shab(b):
    return hashlib.sha256(b).hexdigest()


def refuse(msg):
    raise SystemExit("REFUSED: %s" % msg)


def pinned(p, pin):
    b = Path(p).read_bytes()
    if shab(b) != pin:
        refuse("%s is not the pinned bytes (%s, want %s)" % (Path(p).name, shab(b)[:16], str(pin)[:16]))
    if b"\r" in b:
        refuse("CR byte in %s (E-73: digests are recorded on LF bytes only)" % Path(p).name)
    return b


def load(a):
    m8 = Path(a.m8_root).resolve() if a.m8_root else HERE.parent.parent
    bk = m8 / "sp_durable" / a.book
    p = Path(a.params) if a.params else bk / "close" / "close_params.v1.json"
    doc = json.loads(p.read_bytes().decode("utf-8"))
    if doc.get("schema") != "m8_close_params.v1" or doc.get("book") != a.book:
        refuse("%s is not the close parameters of %s" % (p, a.book))
    C = doc["constants"]
    open_ = [n for n in ("BUILT_FROM_PIN", "ROWS", "BOSS_CONDITIONS") if C[n] == PENDING] + \
            [t for t, _, pin in C["BOSS"] if pin == PENDING]
    if open_:
        refuse("PENDING in the parameters: %s" % open_)
    return m8, bk, C


def final_rows(src_b, C):
    """(bytes of the final file, changed map, the one source status). Each row keeps its keys in order; the hold fields follow
    review_status, as in Daniel's file."""
    want = sorted(C["HOLD_FIELDS"])
    if want != sorted(C["LINEAGE_FIELDS"]):
        refuse("HOLD_FIELDS and LINEAGE_FIELDS name different fields")
    if any(C["HOLD_FIELDS"][k] is not None for k in want if k.startswith("candidate_hold")):
        refuse("HOLD_FIELDS carries a hold; a book with held rows needs its hold ruling in this tool first")
    rows = [json.loads(x) for x in src_b.decode("utf-8").split("\n") if x.strip()]
    if len(rows) != C["ROWS"]:
        refuse("%d source rows, want %s" % (len(rows), C["ROWS"]))
    ids = [r.get("writer_decision_id") for r in rows]
    if len(set(ids)) != len(ids) or None in ids:
        refuse("writer_decision_id is absent or repeats")
    out, changed, before = [], {}, set()
    for r in rows:
        before.add(r.get("review_status"))
        if "review_status" not in r or any(k in r for k in want if k != "review_status"):
            refuse("row %s has no review_status, or already carries a hold field" % r["writer_decision_id"])
        new = {}
        for k, v in r.items():
            if k == "review_status":
                new.update(C["HOLD_FIELDS"])
            else:
                new[k] = v
        d = sorted(k for k in set(r) | set(new) if (k in r) != (k in new) or r.get(k) != new.get(k))
        if d != want:
            refuse("row %s changes %s, want %s" % (r["writer_decision_id"], d, want))
        changed[r["writer_decision_id"]] = d
        out.append(json.dumps(new, ensure_ascii=False))
    if len(before) != 1:
        refuse("the source rows carry %d review_status values" % len(before))
    return ("\n".join(out) + "\n").encode("utf-8"), changed, before.pop()


def boss_basis(a, bk, C):
    """basis: the first record's counts and each later record's verdicts, every verdict REPORTED; a join short of all MET is refused."""
    rows = {}
    for x in a.boss_rows or []:
        m = re.fullmatch(r"([A-Za-z0-9_]+)=(\d+),(\d+)", x)
        if not m:
            refuse("--boss-rows wants TAG=CONFIRM,RETURN, not %r" % x)
        rows[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    basis, verdict = {}, {}
    for i, (tag, rel, pin) in enumerate(C["BOSS"]):
        b = pinned(bk / rel, pin)
        conds = {c.get("id"): c.get("verdict") for c in json.loads(b.decode("utf-8")).get("conditions") or []}
        verdict.update(conds)
        e = {"path": "sp_durable/%s/%s" % (a.book, rel), "sha256": shab(b)}
        if i == 0:
            if tag not in rows:
                refuse("--boss-rows names no counts for %s" % tag)
            e.update(conditions_met=sum(1 for v in conds.values() if v == "MET"),
                     not_testable=[k for k, v in conds.items() if v == "NOT_TESTABLE"])
            other = {k: v for k, v in conds.items() if v not in ("MET", "NOT_TESTABLE")}
            if other:
                e["other_verdicts"] = other
            e.update(rows_confirm=rows[tag][0], rows_return=rows[tag][1])
        else:
            e["conditions"] = conds
        basis["boss_audit_" + tag] = e
    if sorted(verdict) != sorted(C["BOSS_CONDITIONS"]) or any(v != "MET" for v in verdict.values()):
        refuse("the boss records do not join to all conditions MET: %s" % {k: v for k, v in verdict.items() if v != "MET"})
    if len(C["BOSS"]) > 1:
        if not a.merge:
            refuse("two boss records are named: --merge states how they are joined")
        basis["merge"] = a.merge
        basis["tier"] = "REPORTED (the auditor's verdicts) joined by script"
    else:
        basis["tier"] = "REPORTED (the auditor's verdicts)"
    return basis


def build(a, m8, bk, C):
    if a.from_rel != C["BUILT_FROM"]:
        refuse("--from is not the parameters' BUILT_FROM (%s)" % C["BUILT_FROM"])
    if not STAMP.match(a.written or ""):
        refuse("--written wants YYYY-MM-DDTHH:MM:SSZ")
    if not (a.holds or "").strip():
        refuse("--holds is required")
    src_b = pinned(m8 / C["BUILT_FROM"], C["BUILT_FROM_PIN"])
    rows_b, changed, was = final_rows(src_b, C)
    now = C["HOLD_FIELDS"]["review_status"]
    man = {
        "schema": "%s_rows_final_manifest.v1" % a.book.lower(), "book": a.book, "built_from": C["BUILT_FROM"],
        "built_from_sha256": shab(src_b), "names": "sp_durable/%s/%s" % (a.book, C["CORPUS"]), "sha256": shab(rows_b),
        "rows": C["ROWS"], "changed": changed,
        "change_rule": "review_status %s -> %s; candidate_hold_state and candidate_hold_basis added as null; every other key and "
                       "value byte-equal after JSON round trip" % (was, now),
        "basis": boss_basis(a, bk, C), "holds": a.holds, "written": a.written}
    return rows_b, (json.dumps(man, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def commit(plan, lock):
    """All or nothing: every file to a temporary name, previous bytes kept (E-44), then replaced; a failure restores them."""
    fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    done, tmps = [], []
    try:
        for p, b in plan:
            t = p.with_name(p.name + ".buildtmp")
            t.write_bytes(b)
            tmps.append(t)
        for (p, b), t in zip(plan, tmps):
            try:
                cur = p.read_bytes()
            except FileNotFoundError:
                cur = None
            if cur is not None and cur != b:
                with open(p.with_name(p.name + ".pre_" + shab(cur)[:12]), "xb") as fh:
                    fh.write(cur)
            os.replace(t, p)
            done.append((p, cur))
            if shab(p.read_bytes()) != shab(b):
                raise OSError("read-back differs for %s" % p.name)
    except BaseException:
        for p, cur in reversed(done):
            if cur is None:
                p.unlink()
            else:
                p.write_bytes(cur)
        for t in tmps:
            if t.exists():
                t.unlink()
        raise
    finally:
        os.close(fd)
        os.unlink(str(lock))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--from", dest="from_rel", required=True)
    ap.add_argument("--written", required=True)
    ap.add_argument("--holds", required=True)
    ap.add_argument("--boss-rows", action="append")
    ap.add_argument("--merge")
    ap.add_argument("--m8-root")
    ap.add_argument("--params")
    ap.add_argument("--out-root")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", action="store_true")
    a = ap.parse_args()
    m8, bk, C = load(a)
    root = Path(a.out_root).resolve() if a.out_root else bk
    rows_b, man_b = build(a, m8, bk, C)
    rows_p, man_p = root / C["CORPUS"], root / C["MANIFEST"]
    info = {"rows_sha256": shab(rows_b), "manifest_sha256": shab(man_b), "rows": C["ROWS"]}
    if a.check:
        same = rows_p.is_file() and man_p.is_file() and rows_p.read_bytes() == rows_b and man_p.read_bytes() == man_b
        print(json.dumps(info))
        print("MATCH" if same else "MISMATCH")
        return 0 if same else 1
    commit([(rows_p, rows_b), (man_p, man_b)], root / ("_build_final_rows.%s.lock" % a.book))
    print(json.dumps(info))
    return 0


if __name__ == "__main__":
    sys.exit(main())
