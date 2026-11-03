#!/usr/bin/env python3
"""Build <BOOK>'s landed-outputs manifest from its receipt files, in the form of Dan/close/dan_landed_outputs_manifest.v2.json.

  python -B _build_landed_manifest.py --book BOOK [--m8-root DIR] [--params FILE] [--out FILE] (--write | --check)

Every output a completion receipt row lists with a digest is looked for under sp_durable and re-hashed there. A row's path is
often the lane's scratch directory, which is not durable, so the durable path comes from, in order:
  1. the path itself, when it holds `sp_durable/`;
  2. an install row of the receipt files carrying the same digest (its `installed_path`);
  3. the path, or its last name when it is absolute, under each directory the parameter LANDED_ROOTS names.
  4. any file with this digest under a directory LANDED_ROOTS names, at whatever name it now carries.
A candidate counts only when its bytes have the listed digest: nothing is guessed, and a scratch path is never opened. What finds
no such file goes in `not_matching` with its reason, and an entry's `outcome` is LANDED only for a matching re-hash; the row's
own word is kept as `receipt_outcome` (TRANSCRIBED).

No clock, no randomness, and no directory scan beyond the roots a parameter names: every other input is a path read from a parameter or a receipt row. Non-authorizing.
  --check  regenerate and compare bytes with the installed manifest; writes nothing; exit 0 only on MATCH
  --write  whole, LF, through a temporary file and an atomic replace; other bytes are first kept as <name>.pre_<sha12> (E-44)
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
HEX64 = set("0123456789abcdef")


def shab(b):
    return hashlib.sha256(b).hexdigest()


def is_digest(v):
    return isinstance(v, str) and len(v) == 64 and set(v) <= HEX64


def load(a):
    m8 = Path(a.m8_root).resolve() if a.m8_root else HERE.parent.parent
    bk = m8 / "sp_durable" / a.book
    p = Path(a.params) if a.params else bk / "close" / "close_params.v1.json"
    doc = json.loads(p.read_bytes().decode("utf-8"))
    if doc.get("schema") != "m8_close_params.v1" or doc.get("book") != a.book:
        raise SystemExit("REFUSED: %s is not the close parameters of %s" % (p, a.book))
    return m8, bk, doc["constants"]


def listed(row):
    """(path, sha256) for each output the row lists with a digest. A form with no digest yields nothing; the row is counted."""
    o = row.get("outputs")
    pairs = []
    if isinstance(o, list):
        for x in o:
            if isinstance(x, dict) and is_digest(x.get("sha256")):
                pairs.append((str(x.get("path") or x.get("file") or ""), x["sha256"]))
    elif isinstance(o, dict):
        for k, v in o.items():
            if is_digest(v):
                pairs.append((k, v))
            elif isinstance(v, dict) and is_digest(v.get("sha256")):
                pairs.append((str(v.get("path") or k), v["sha256"]))
    return pairs


def norm(path):
    return path.replace("\\", "/")


def root_index(m8, book, roots):
    """digest -> (sp_durable path, bytes) for every file under a named root: a kept file may carry a later name (.pre_<sha>, .a1)."""
    index = {}
    for root in roots:
        if root:
            for f in sorted((m8 / "sp_durable" / book / root).rglob("*")):
                if f.is_file():
                    b = f.read_bytes()
                    index.setdefault(shab(b), (f.relative_to(m8).as_posix(), len(b)))
    return index


def durable_of(m8, book, path, digest, installs, roots, index):
    """The sp_durable path holding these bytes and how it was found, or (None, reason)."""
    p = norm(path)
    tried = []
    if "sp_durable/" in p:
        tried.append(("the listed path", p[p.index("sp_durable/"):]))
    for rel in installs.get(digest, []):
        tried.append(("an install row", norm(rel)))
    tail = p.rsplit("/", 1)[-1] if (len(p) > 1 and p[1] == ":") or p.startswith("/") else p
    if "sp_durable/" not in p:
        for root in roots:
            tried.append(("LANDED_ROOTS", "/".join(x for x in ("sp_durable", book, root, tail) if x)))
    seen_other = False
    for how, rel in tried:
        if not rel.startswith("sp_durable/%s/" % book):
            continue
        try:
            b = (m8 / rel).read_bytes()
        except OSError:
            continue
        if shab(b) == digest:
            return rel, how, len(b)
        seen_other = True
    if digest in index:
        return index[digest][0], "the digest under LANDED_ROOTS", index[digest][1]
    return None, ("a file is at the named place with other bytes" if seen_other else "no durable file with this digest at any named place"), None


def build(a, m8, bk, C):
    pre = "sp_durable/%s/" % a.book
    files, rows = [], []
    for rel in C["RECEIPT_FILES"]:
        b = (m8 / rel).read_bytes()
        if b"\r" in b:
            raise SystemExit("REFUSED: CR byte in %s (E-73)" % rel)
        files.append({"path": rel, "sha256": shab(b)})
        rows += [(rel, json.loads(x)) for x in b.decode("utf-8").split("\n") if x.strip()]
    installs = {}
    for _, r in rows:
        if is_digest(r.get("output_sha256")) and r.get("installed_path"):
            installs.setdefault(r["output_sha256"], []).append(r["installed_path"])
    launch = {r.get("execution_id"): r for _, r in rows if r.get("record_kind") == "launch"}  # a completion row amends its launch row
    outputs, not_matching, by_path, undigested, completions = [], [], {}, 0, 0
    index = root_index(m8, a.book, C["LANDED_ROOTS"])
    for rel, r in rows:
        if r.get("record_kind") != "completion":
            continue
        completions += 1
        pairs = listed(r)
        undigested += 0 if pairs else 1
        for path, digest in pairs:
            where, how, size = durable_of(m8, a.book, path, digest, installs, C["LANDED_ROOTS"], index)
            ex = r.get("execution_id") or r.get("amends_execution_id")
            lr = launch.get(ex) or {}
            ids = {"execution_id": ex, "attempt_id": r.get("attempt_id")}
            if where is None:
                not_matching.append(dict(ids, listed_path=path, sha256=digest, reason=how, receipts=rel, receipt_outcome=r.get("outcome")))
                continue
            if where in by_path:
                by_path[where].setdefault("also_listed_by", []).append(ex)
                continue
            e = dict(ids, lane=r.get("lane") or lr.get("lane"), role=r.get("role") or lr.get("role") or r.get("grader_role") or lr.get("grader_role"),
                     outcome="LANDED", path=where, sha256=digest,
                     bytes=size, receipts=rel, receipt_outcome=r.get("outcome"), found_by=how)
            by_path[where] = e
            outputs.append(e)
    return {"schema": "%s_landed_outputs_manifest.v1" % a.book.lower(), "book": a.book,
            "what": "every output a completion receipt row lists with a digest, re-hashed on disk when this was built",
            "tier": "MEASURED (digests) over TRANSCRIBED receipt rows", "receipt_files": files,
            "completion_rows": completions, "completion_rows_listing_no_digest": undigested,
            "outputs": outputs, "not_matching": not_matching}, pre


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--m8-root")
    ap.add_argument("--params")
    ap.add_argument("--out")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", action="store_true")
    a = ap.parse_args()
    m8, bk, C = load(a)
    doc, _ = build(a, m8, bk, C)
    b = (json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    out = Path(a.out) if a.out else bk / C["LANDED_REL"]
    info = {"sha256": shab(b), "bytes": len(b), "outputs": len(doc["outputs"]), "not_matching": len(doc["not_matching"]),
            "completion_rows": doc["completion_rows"], "completion_rows_listing_no_digest": doc["completion_rows_listing_no_digest"]}
    try:
        cur = out.read_bytes()
    except FileNotFoundError:
        cur = None
    print(json.dumps(info))
    if a.check:
        print("MATCH" if cur == b else "MISMATCH")
        return 0 if cur == b else 1
    if cur != b:
        out.parent.mkdir(parents=True, exist_ok=True)
        if cur is not None:
            with open(out.with_name(out.name + ".pre_" + shab(cur)[:12]), "xb") as fh:
                fh.write(cur)
        tmp = out.with_name(out.name + ".tmp")
        tmp.write_bytes(b)
        os.replace(tmp, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
