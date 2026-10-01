#!/usr/bin/env python3
"""E-55 sibling (1): seven Ezekiel launch rows carry the lane's OWN runtime id in parent_agent_id, and none of the
seven is in _transcript_map.ezek.json. This amends both, never editing a line in place (E-44).

  receipts  : one m8_attempt_receipt_amendment.v1 row appended per execution, carrying agent_id = the runtime id and
              parent_agent_id = "orchestrator". NO tokens_reported: census v4 sums amendment token ints, so a token
              field here would double-count.
  map       : one new top-level key per execution, added through campaign/_guarded_json_patch.py (add-only, the
              precedent of step2_reconciliation/_transcript_map_patch_receipt.json). Every field is copied from the
              receipt row; nothing is inferred.

Protocol (safe-structured-registry-mutation): address each execution exactly once -> pin whole-file sha256 and the
expected-before values -> candidate built by appending bytes, parsed independently, compared semantically -> in-flight
pin guard per target -> exclusive sidecar lock, digest recheck under the lock, .pre_<sha12> copy, atomic replace ->
postvalidate (census v4's own id resolution, replicated) with exact-preimage rollback.

Dry run is the default. --apply is the mutation boundary.
"""
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
EZ = SP / "Ezek"
MAP = EZ / "_transcript_map.ezek.json"
OUT = Path(__file__).with_name("amend_identity_E55s1.receipt.json")
MAP_RECEIPT = Path(__file__).with_name("amend_identity_E55s1.map_patch_receipt.json")
AID = re.compile(r"a[0-9a-f]{15,20}")
BY = "orchestrator (claude-opus-5-5), session 910cbe15-396b-4a0e-82f6-8aa1e2edf1e4"
REASON = ("E-55 sibling (1): the lane's runtime id was recorded in parent_agent_id. 200 other rows hold "
          "\"orchestrator\" there. This row restates the identity in the right fields. The original line is unedited.")

# (receipt file rel EZ, execution_id, runtime id expected in parent_agent_id today)
TARGETS = [
    ("ezek_merged_close_attempt_receipts.jsonl", "ezek_merged_close_lane_a_a1#e1", "a2040ee3f85015b45"),
    ("ezek_merged_close_attempt_receipts.jsonl", "ezek_merged_close_lane_b_a1#e1", "a75da61617c35aca9"),
    ("ezek_close_audit_attempt_receipts.jsonl", "ezek_close_audit_lane_a_a1#e1", "a6b0d88ea3d72bfde"),
    ("ezek_close_audit_attempt_receipts.jsonl", "ezek_close_audit_lane_b_a1#e1", "a9d7aae5ecddffbe8"),
    ("ezek_close_audit_attempt_receipts.jsonl", "ezek_close_audit_lane_a_a1#e2", "a8779d9785b355135"),
    ("ezek_close_audit_attempt_receipts.jsonl", "ezek_close_audit_lane_b_a1#e2", "a820a104a53bc70f2"),
    ("ezek_close_audit_attempt_receipts.jsonl", "ezek_fable_dispatch_probe_a1#e1", "ab7e0fb137fddb461"),
]
MAP_FIELDS = ("attempt_id", "execution_id", "book", "lane", "role", "brief", "brief_sha256", "launched_at")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def fail(msg):
    raise SystemExit("REFUSED: " + msg)


def rows_of(b):
    out = []
    for n, l in enumerate(b.decode("utf-8").splitlines(), 1):
        if l.strip():
            try:
                out.append(json.loads(l))
            except ValueError:
                fail(f"line {n} is not JSON")
    return out


def resolved(rows, ex):
    """census v4 lines 64-68 and 95, replicated: ids an execution resolves to from amending rows only, and the
    amendment token sum. parent_agent_id is excluded on purpose - the point is that the ids no longer need it."""
    ids, tok = set(), 0
    for r in rows:
        if r.get("amends_execution_id") != ex:
            continue
        ids |= {r[k] for k in ("agent_id", "runtime_agent_id") if isinstance(r.get(k), str) and AID.fullmatch(r[k])}
        if str(r.get("schema", "")).endswith("_amendment.v1") and isinstance(r.get("tokens_reported"), int):
            tok += r["tokens_reported"]
    return ids, tok


def build(now):
    files = {}
    for rel, _, _ in TARGETS:
        if rel not in files:
            b = (EZ / rel).read_bytes()
            files[rel] = {"path": EZ / rel, "before": b, "sha_before": sha(b), "rows": rows_of(b), "add": []}
    map_raw = MAP.read_bytes()
    tmap = json.loads(map_raw.decode("utf-8"))
    if (json.dumps(tmap, ensure_ascii=False, indent=1) + "\n").encode("utf-8") != map_raw:
        fail("the map does not round-trip byte-exact, so the guarded tool's write would move unrelated bytes")
    map_ids = {v.get("agent_id") for v in tmap.values() if isinstance(v, dict)}
    # the identity domain is every receipt file census v4 reads, not only the two this plan writes
    domain = {p.relative_to(EZ).as_posix(): rows_of(p.read_bytes())
              for p in sorted(EZ.rglob("*_attempt_receipts.jsonl")) if ".pre_" not in p.name}
    edits, plan_rows = [], []
    for rel, ex, rid in TARGETS:
        f = files[rel]
        # ---- address
        hits = [(r_, rr) for r_, rows in domain.items() for rr in rows
                if rr.get("execution_id") == ex and not rr.get("amends_execution_id")]
        if len(hits) != 1 or hits[0][0] != rel:
            fail(f"{ex}: {len(hits)} attempt rows in {len(domain)} receipt files, expected exactly 1 in {rel}")
        row = hits[0][1]
        # ---- expected-before
        if row.get("parent_agent_id") != rid:
            fail(f"{ex}: parent_agent_id is {row.get('parent_agent_id')!r}, expected {rid!r}")
        if "agent_id" in row or "runtime_agent_id" in row:
            fail(f"{ex}: the launch row already carries agent_id/runtime_agent_id")
        ids, _ = resolved(f["rows"], ex)
        if ids:
            fail(f"{ex}: an amending row already resolves it to {sorted(ids)}")
        # map key: the attempt id for execution 1, "<attempt>_e<n>" after (the ezek_controlling_rulings_a1_e11
        # precedent). Retries share an attempt id, so keying on it alone collided (E-60).
        n = int(ex.rsplit("#e", 1)[1])
        key = row["attempt_id"] if n == 1 else f"{row['attempt_id']}_e{n}"
        if key in tmap or rid in map_ids:
            fail(f"{ex}: the map already holds key {key!r} or id {rid}")
        amend = {"schema": "m8_attempt_receipt_amendment.v1", "amends_schema": row.get("schema"),
                 "amends_execution_id": ex, "book": row.get("book"), "original_line_unedited": True,
                 "agent_id": rid, "parent_agent_id": "orchestrator",
                 "amends_fields": {"parent_agent_id": {"was": rid, "is": "orchestrator"},
                                   "agent_id": {"was": None, "is": rid}},
                 "reason": REASON, "recorded_at": now, "recorded_by": BY}
        f["add"].append(amend)
        entry = {k: row[k] for k in MAP_FIELDS if k in row}
        entry["agent_id"] = rid
        entry["model_ordered"] = row.get("model")
        if row.get("previous_execution_id"):
            entry["previous_execution_id"] = row["previous_execution_id"]
        entry["note"] = (f"added {now[:10]} from Ezek/{rel} (execution {ex}) by repair2/amend_identity_E55s1.py. The "
                         "launch row recorded this runtime id in parent_agent_id (E-55 sibling 1).")
        edits.append({"key": key, "expect_before": "__ABSENT__", "set": entry,
                      "why": "transcript-map entry for an Ezekiel execution missing from the pointer index (E-55 sibling 1)"})
        plan_rows.append((rel, ex, rid, row.get("outcome")))
    keys = [e["key"] for e in edits]
    if len(set(keys)) != len(keys):
        fail(f"the plan addresses a map key more than once: {sorted({k for k in keys if keys.count(k) > 1})}")
    # ---- candidates, parsed independently and compared semantically
    for f in files.values():
        b = f["before"]
        f["cand"] = b + (b"" if b.endswith(b"\n") else b"\n") + "".join(
            json.dumps(a, ensure_ascii=False) + "\n" for a in f["add"]).encode("utf-8")
        f["sha_cand"] = sha(f["cand"])
        cr = rows_of(f["cand"])
        if cr[:len(f["rows"])] != f["rows"] or cr[len(f["rows"]):] != f["add"]:
            fail(f"{f['path'].name}: candidate is not the original rows plus exactly the planned rows")
        for rel, ex, rid, _ in TARGETS_IN(f["path"].name):
            ids, tok = resolved(cr, ex)
            _, tok0 = resolved(f["rows"], ex)
            if ids != {rid} or tok != tok0:
                fail(f"{ex}: candidate resolves to {sorted(ids)} tokens {tok0}->{tok}, expected {{{rid}}} unchanged")
    return files, {"target": str(MAP), "expect_file_sha256": sha(map_raw), "edits": edits,
                   "receipt": str(MAP_RECEIPT)}, sha(map_raw), plan_rows


def TARGETS_IN(name):
    return [(r, e, i, None) for r, e, i in TARGETS if r == name]


def guard(path):
    rel = path.relative_to(SP).as_posix()
    p = subprocess.run([sys.executable, str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek",
                        "--target", rel], cwd=str(SP), capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    return p.returncode, (p.stdout.strip().splitlines() or [""])[-1][:200]


def atomic_write(path, data):
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except Exception:
        Path(tmp).unlink(missing_ok=True)
        raise


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    apply_it = "--apply" in sys.argv[1:]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    files, plan, map_sha, plan_rows = build(now)
    spec = importlib.util.spec_from_file_location("gjp", SP / "campaign" / "_guarded_json_patch.py")
    gjp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gjp)
    dry, code = gjp.run(plan, False)
    if code or dry.get("status") != "DRY_RUN":
        fail(f"map dry run: {dry.get('status')} {dry.get('problems') or dry.get('why')}")
    print("PLAN")
    for rel, ex, rid, outcome in plan_rows:
        print(f"  {ex:36} {rid}  append amendment -> {rel[:30]}")
    for e in plan["edits"]:
        print(f"  map add {e['key']:34} -> {e['set']['execution_id']}")
    for f in files.values():
        print(f"  {f['path'].name}: rows {len(f['rows'])} -> {len(f['rows']) + len(f['add'])}  "
              f"sha {f['sha_before'][:12]} -> {f['sha_cand'][:12]}")
    print(f"  map: keys +{len(plan['edits'])}  sha {map_sha[:12]}  guarded dry run {dry['status']}")
    guards = {str(p): guard(p) for p in [f["path"] for f in files.values()] + [MAP]}
    for p, (c, last) in guards.items():
        print(f"  pin guard {Path(p).name}: exit {c} {last}")
    if not apply_it:
        print("DRY RUN - nothing written. Re-run with --apply.")
        return 0
    if any(c for c, _ in guards.values()):
        fail("an in-flight pin guard refused")

    locks, done, result = [], [], {}
    try:
        for p in [f["path"] for f in files.values()] + [MAP]:
            lk = Path(str(p) + ".lock")
            fd = os.open(str(lk), os.O_CREAT | os.O_EXCL | os.O_WRONLY)   # never auto-clear an existing lock
            os.write(fd, f"{BY} {now}\n".encode("utf-8"))
            os.close(fd)
            locks.append(lk)
        for f in files.values():
            if sha(f["path"].read_bytes()) != f["sha_before"]:
                fail(f"{f['path'].name} moved between plan and lock")
        if sha(MAP.read_bytes()) != map_sha:
            fail("the map moved between plan and lock")
        for f in list(files.values()):
            pre = f["path"].with_name(f["path"].name + ".pre_" + f["sha_before"][:12])
            if not pre.exists():
                pre.write_bytes(f["before"])
            atomic_write(f["path"], f["cand"])
            done.append(f)
        map_before = MAP.read_bytes()
        pre = MAP.with_name(MAP.name + ".pre_" + map_sha[:12])
        if not pre.exists():
            pre.write_bytes(map_before)
        mres, mcode = gjp.run(plan, True)

        # ---- postvalidate
        post = []
        for f in files.values():
            now_b = f["path"].read_bytes()
            if sha(now_b) != f["sha_cand"]:
                post.append(f"{f['path'].name}: digest after write is not the candidate's")
            rr = rows_of(now_b)
            for _, ex, rid, _ in TARGETS_IN(f["path"].name):
                ids, tok = resolved(rr, ex)
                if ids != {rid} or tok != resolved(f["rows"], ex)[1]:
                    post.append(f"{ex}: resolves to {sorted(ids)} after write")
        if mcode or mres.get("status") != "APPLIED":
            post.append(f"map patch {mres.get('status')}: {mres.get('postvalidation') or mres.get('why')}")
        tmap = json.loads(MAP.read_text(encoding="utf-8"))
        for e in plan["edits"]:
            if tmap.get(e["key"]) != e["set"]:
                post.append(f"map key {e['key']} not as planned")
        if post:
            for f in done:
                if sha(f["path"].read_bytes()) == f["sha_cand"]:
                    atomic_write(f["path"], f["before"])
                else:
                    post.append(f"{f['path'].name}: NOT rolled back - digest is neither candidate nor preimage")
            if mres.get("file_sha256_after") and sha(MAP.read_bytes()) == mres["file_sha256_after"]:
                atomic_write(MAP, map_before)
            fail(f"postvalidation failed, rolled back where the digest allowed: {post}")
        result = {"schema": "m8_identity_amendment_receipt.v1", "applied_at": now, "by": BY, "reason": REASON,
                  "files": [{"path": str(f["path"]), "sha256_before": f["sha_before"], "sha256_after": f["sha_cand"],
                             "rows_appended": len(f["add"]),
                             "preimage": f["path"].name + ".pre_" + f["sha_before"][:12]} for f in files.values()],
                  "map": {"path": str(MAP), "sha256_before": map_sha, "sha256_after": mres.get("file_sha256_after"),
                          "keys_added": [e["key"] for e in plan["edits"]], "patch_receipt": str(MAP_RECEIPT),
                          "preimage": MAP.name + ".pre_" + map_sha[:12]},
                  "executions": [{"execution_id": ex, "runtime_id": rid, "file": rel} for rel, ex, rid, _ in plan_rows],
                  "postvalidation": "PASS: every execution resolves to exactly its runtime id through an amending row "
                                    "(census v4 logic), amendment token sums unchanged, map holds exactly the planned "
                                    "keys",
                  "pin_guards": {Path(p).name: c for p, (c, _) in guards.items()}}
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    finally:
        for lk in locks:
            lk.unlink(missing_ok=True)
    print(f"APPLIED - receipt {OUT.name}")
    for f in result["files"]:
        print(f"  {Path(f['path']).name}: {f['sha256_before'][:12]} -> {f['sha256_after'][:12]} +{f['rows_appended']}")
    print(f"  map: {result['map']['sha256_before'][:12]} -> {str(result['map']['sha256_after'])[:12]} "
          f"+{len(result['map']['keys_added'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
