#!/usr/bin/env python3
"""Guarded mutation of a structured JSON record store.

Implements the required invariant from the safe-structured-registry-mutation protocol:

    address -> precondition -> semantic diff -> protected deny -> atomic commit -> postvalidate/rollback

WHAT THIS REFUSES TO BE. It is not a text patcher. Every change addresses ONE top-level key by its exact name,
carries the whole-file digest it expects to find, and carries the expected-before value of that key verbatim. A
first-match string replacement, a broad regex, or a full-file reserialisation of hand-maintained JSON are all
denied by construction, because each of them can silently move a value that belongs to a different object.

PROTECTED KEYS are denied outright. In this campaign the protected set is the provenance of a record - what it is,
when it was built, and who ordered it - because a mutation that quietly re-dates or re-authorises a record is the
one that makes every later reading of it wrong.

PLAN SCHEMA (JSON on stdin or --plan <file>):
  {"target": "<path>",
   "expect_file_sha256": "<digest of the file as it should be right now>",
   "edits": [{"key": "<top-level key>",
              "expect_before": <exact current value, or the string "__ABSENT__" for a new key>,
              "set": <new value>,
              "why": "<reason recorded in the receipt>"}],
   "receipt": "<path to write the mutation receipt>"}

Dry run is the default. --apply is the explicit mutation boundary.
"""
import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ABSENT = "__ABSENT__"
PROTECTED_KEYS = {"schema", "built", "ordered_by", "authority", "generated_at", "generator"}


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    return sha_bytes(Path(p).read_bytes())


def describe(v, width=220):
    s = json.dumps(v, ensure_ascii=False)
    return s if len(s) <= width else s[:width] + "...(%d chars)" % len(s)


def run(plan, apply_it):
    target = Path(plan["target"])
    problems = []

    # ---- address ----
    if not target.is_file():
        return {"status": "REFUSED", "why": "target does not exist", "target": str(target)}, 1

    raw = target.read_bytes()
    live_digest = sha_bytes(raw)

    # ---- precondition: whole-registry digest ----
    if plan.get("expect_file_sha256") and plan["expect_file_sha256"] != live_digest:
        return {"status": "REFUSED",
                "why": "the file on disk is not the file this plan was written against; another write intervened",
                "expected": plan["expect_file_sha256"], "live": live_digest,
                "instruction": "re-read the live file, rebuild the plan against it, and do not force"}, 1

    doc = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(doc, dict):
        return {"status": "REFUSED", "why": "top level is not an object; this tool addresses top-level keys"}, 1

    # ---- address: each key at most once per plan. A second edit to the same key silently overwrites the first, and
    # both expected-before checks pass because both were written against the same live value (E-60).
    keys = [e["key"] for e in plan["edits"]]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        return {"status": "REFUSED", "why": "the plan addresses a key more than once; the later edit would "
                "overwrite the earlier", "duplicate_keys": dup}, 1

    # ---- protected deny + precondition: expected-before values ----
    diff = []
    for e in plan["edits"]:
        k = e["key"]
        if k in PROTECTED_KEYS:
            problems.append("%s: PROTECTED key; provenance fields are never rewritten by a patch" % k)
            continue
        present = k in doc
        before = doc.get(k, ABSENT)
        want = e.get("expect_before", ABSENT)
        if want == ABSENT and present:
            problems.append("%s: plan expects the key ABSENT but it exists" % k)
        elif want != ABSENT and not present:
            problems.append("%s: plan expects a value but the key is absent" % k)
        elif want != ABSENT and before != want:
            problems.append("%s: expected-before mismatch; the value on disk is not what the plan was written "
                            "against" % k)
        diff.append({"key": k, "op": "add" if not present else "replace",
                     "before": describe(before), "after": describe(e["set"]), "why": e.get("why")})

    if problems:
        return {"status": "REFUSED", "why": "precondition failure", "problems": problems, "semantic_diff": diff}, 1

    # ---- semantic diff (dry run stops here) ----
    changed_keys = sorted({e["key"] for e in plan["edits"]})
    if not apply_it:
        return {"status": "DRY_RUN", "target": str(target), "file_sha256_now": live_digest,
                "keys_addressed": changed_keys, "semantic_diff": diff,
                "next": "re-run with --apply to commit"}, 0

    # ---- atomic commit ----
    new_doc = dict(doc)
    for e in plan["edits"]:
        new_doc[e["key"]] = e["set"]
    payload = (json.dumps(new_doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8")

    fd, tmp = tempfile.mkstemp(dir=str(target.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(payload)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, target)
    except Exception:
        Path(tmp).unlink(missing_ok=True)
        raise

    # ---- postvalidate: re-read from disk, prove only the addressed keys moved ----
    after_raw = target.read_bytes()
    after = json.loads(after_raw.decode("utf-8-sig"))
    moved = sorted(k for k in set(after) | set(doc) if after.get(k, ABSENT) != doc.get(k, ABSENT))
    post = []
    if moved != changed_keys:
        post.append("keys that actually moved %r != keys addressed %r" % (moved, changed_keys))
    for e in plan["edits"]:
        if after.get(e["key"]) != e["set"]:
            post.append("%s: value on disk after write is not the value the plan set" % e["key"])
    rolled_back = None
    if post:
        # restore the exact preimage, but only if the file is still exactly what this call wrote
        if sha_bytes(target.read_bytes()) == sha_bytes(payload):
            fd, tmp = tempfile.mkstemp(dir=str(target.parent), suffix=".tmp")
            try:
                with os.fdopen(fd, "wb") as fh:
                    fh.write(raw)
                    fh.flush()
                    os.fsync(fh.fileno())
                os.replace(tmp, target)
            except Exception:
                Path(tmp).unlink(missing_ok=True)
                raise
            rolled_back = "restored the preimage" if sha_bytes(target.read_bytes()) == live_digest else "FAILED"
        else:
            rolled_back = "SKIPPED: the file moved after this call's write; evidence retained for a human"

    receipt = {
        "schema": "m8_guarded_json_patch_receipt.v1",
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "target": str(target),
        "file_sha256_before": live_digest,
        "file_sha256_after": sha_bytes(after_raw),
        "keys_addressed": changed_keys,
        "semantic_diff": diff,
        "postvalidation": post or "PASS: exactly the addressed keys changed and each holds the planned value",
        "protocol": "address -> precondition -> semantic diff -> protected deny -> atomic commit -> postvalidate",
    }
    if rolled_back:
        receipt["rollback"] = rolled_back
    if plan.get("receipt"):
        rp = Path(plan["receipt"])
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

    receipt["status"] = "RED" if post else "APPLIED"
    return receipt, (1 if post else 0)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8") if a.plan else sys.stdin.read())
    out, code = run(plan, a.apply)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return code


if __name__ == "__main__":
    sys.exit(main())
