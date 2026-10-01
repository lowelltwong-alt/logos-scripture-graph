#!/usr/bin/env python3
"""The Ezekiel sweep-chain record (ezek_controlling_rulings_a1#e4, S1-ROUTING and gate: 'S1-17 chain link named and bound into
the sweep-chain record, or the break recorded with S1's digest reconstruction as compensation; S1-16 and S1-18 recorded').

Built from the bytes, never from memory:
  - every SP/Ezek/repair/*.manifest.json is read, and its input and output digests are checked against the files on disk;
  - the chain is walked BACKWARD by digest from the chain head (each input must be some manifest's output) to an origin that no
    manifest produces; manifests off that path are listed as a superseded branch;
  - S1-17: the manifest whose output is rows_v2_swept_r2.jsonl (1f11a1...) and whose input is rows_s4_cwo05_r2.jsonl (f468e2...)
    is named as the link S1 could not see;
  - S1-16: P11-002 is compared field by field between the authored apply's input and output rows, and the manifest's lists
    naming it are counted;
  - S1-18: the counts-only curly-quote class in rows_s3_cwo02_r2.manifest.json is recorded, S1's indirect check (no curly quote
    touching Hebrew in the r3 rows) is re-run, and the forward rule is stated.

DRY RUN is the default. --apply writes repair/sweep_chain.v1.json after the in-flight pin guard; differing bytes are never
replaced.

Usage: _sweep_chain_record_ezek.py --head repair/rows_v3_cwo12.jsonl --expect-head <sha256> [--apply]"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
SP = EZ.parent
REPAIR = EZ / "repair"
OUT = REPAIR / "sweep_chain.v1.json"
S1_17 = {"input_prefix": "f468e2624baa", "output_prefix": "1f11a1a2091e"}
CURLY_TOUCHING_HEBREW = re.compile(r"[“”][֐-׿]|[֐-׿][“”]")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rows(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


def rel(path):
    """A manifest path relative to SP/Ezek: the sweeps write 'repair/...', the authored apply writes 'Ezek/repair/...'."""
    return path[len("Ezek/"):] if isinstance(path, str) and path.startswith("Ezek/") else path


def io_of(m):
    """(input dict, output dict) from a manifest, for the shapes the repair lane has written: the sweeps' input/output and the
    authored apply's input_rows/output."""
    def norm(x, path_key, sha_key):
        if isinstance(x, dict) and x.get("sha256"):
            return {"path": rel(x.get("path")), "sha256": x["sha256"], "rows": x.get("rows")}
        if m.get(sha_key):
            return {"path": rel(m.get(path_key)), "sha256": m[sha_key], "rows": None}
        return None
    return norm(m.get("input") or m.get("input_rows"), "input_path", "input_sha256"), norm(m.get("output"), "output_path", "output_sha256")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--head", required=True)
    ap.add_argument("--expect-head", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    head = EZ / a.head
    if sha(head) != a.expect_head:
        raise SystemExit("ABORT: %s is not the expected chain head" % a.head)
    manifests, unrecognized = [], []
    for mp in sorted(REPAIR.glob("*.manifest.json")):
        m = json.loads(mp.read_text(encoding="utf-8"))
        i, o = io_of(m)
        if not (i and o):
            unrecognized.append({"manifest": mp.name, "keys": sorted(m)})
            continue
        def on_disk(d):
            p = EZ / d["path"] if d.get("path") else None
            return None if not (p and p.is_file()) else sha(p) == d["sha256"]
        manifests.append({"manifest": "repair/" + mp.name, "manifest_sha256": sha(mp), "cwo": m.get("cwo") or m.get("schema"),
                          "ordered_by": m.get("ordered_by"), "input": i, "output": o,
                          "input_on_disk_matches": on_disk(i), "output_on_disk_matches": on_disk(o)})
    by_out = {}
    for x in manifests:
        by_out.setdefault(x["output"]["sha256"], []).append(x)
    ambiguous = {k: [x["manifest"] for x in v] for k, v in by_out.items() if len(v) > 1}
    path, cur, seen = [], a.expect_head, set()
    while cur in by_out and cur not in seen:
        seen.add(cur)
        link = by_out[cur][0]
        path.append(link)
        cur = link["input"]["sha256"]
    path.reverse()
    origin = path[0]["input"] if path else None
    on_path = {x["manifest"] for x in path}
    s1_17 = [x for x in path if x["input"]["sha256"].startswith(S1_17["input_prefix"]) and x["output"]["sha256"].startswith(S1_17["output_prefix"])]

    authored = next((x for x in manifests if x["manifest"].endswith("rows_v3_authored.manifest.json")), None)
    s1_16 = {"found": False}
    if authored:
        am = json.loads((EZ / authored["manifest"]).read_text(encoding="utf-8"))
        rin = {r["decision_id"]: r for r in rows(EZ / authored["input"]["path"])} if authored["input"].get("path") else {}
        rout = {r["decision_id"]: r for r in rows(EZ / authored["output"]["path"])} if authored["output"].get("path") else {}
        pid = next((d for d, r in rout.items() if r.get("writer_decision_id") == "P11-002" or d == "P11-002"), None)
        lists = {k: len(v) for k, v in am.items() if isinstance(v, list) and any("P11-002" in json.dumps(e, ensure_ascii=False) for e in v)}
        # the apply renumbers chunk_index_in_book book-wide (manifest key chunk_index_renumbered), so a replace is a no-op when
        # no OTHER field changed
        def changed_fields(d):
            a_, b_ = rin.get(d) or {}, rout.get(d) or {}
            return sorted(k for k in set(a_) | set(b_) if a_.get(k) != b_.get(k))
        replaced = [d for d in (am.get("replaced") or []) if isinstance(d, str)]
        no_ops = [d for d in replaced if d in rin and d in rout and not [k for k in changed_fields(d) if k != "chunk_index_in_book"]]
        s1_16 = {"found": pid is not None, "decision_id": pid, "fields_changed": changed_fields(pid) if pid else None,
                 "no_op_except_chunk_index_renumbering": bool(pid) and pid in no_ops,
                 "manifest_lists_naming_it": lists, "replaced": len(replaced), "replaced_no_ops": no_ops,
                 "chunk_index_renumbered_key": am.get("chunk_index_renumbered"),
                 "disposition": "recorded as a no-op replace, as #e4 S1-ROUTING orders ('record P11-002 as a no-op replace (134, of which 1 no-op)')"}
    s3r2 = next((x for x in manifests if x["manifest"].endswith("rows_s3_cwo02_r2.manifest.json")), None)
    r3 = next((x for x in manifests if x["manifest"].endswith("rows_v2_swept_r3.manifest.json")), None)
    s1_18 = {"manifest": s3r2["manifest"] if s3r2 else None}
    if s3r2:
        sm = json.loads((EZ / s3r2["manifest"]).read_text(encoding="utf-8"))
        counts_only = [c for c in sm.get("changes", []) if isinstance(c, dict) and "count" in c and "old" not in c]
        s1_18["counts_only_change_records"] = len(counts_only)
        s1_18["counts_only_total"] = sum(c.get("count", 0) for c in counts_only if isinstance(c.get("count"), int))
    if r3:
        touching = sum(1 for r in rows(EZ / r3["output"]["path"]) for s in strings(r) if CURLY_TOUCHING_HEBREW.search(s))
        s1_18.update({"r3_rows": r3["output"]["path"], "r3_sha256": r3["output"]["sha256"], "strings_in_r3_with_a_curly_quote_touching_hebrew": touching})
    s1_18["disposition"] = ("S1's indirect check is re-run above as compensation for the counts-only records; forward rule (#e4 S1-ROUTING): every "
                            "future sweep manifest records old and new bytes per change (_cwo13_format_cleanup.py and _cwo18_gloss_quotes.py do)")

    problems = []
    if not path or path[-1]["output"]["sha256"] != a.expect_head:
        problems.append("no manifest produces the chain head")
    if ambiguous:
        problems.append("more than one manifest produces the same output digest: %s" % ambiguous)
    if len(s1_17) != 1:
        problems.append("the S1-17 link is not exactly one manifest on the path (found %d)" % len(s1_17))
    bad_disk = [x["manifest"] for x in path if x["input_on_disk_matches"] is False or x["output_on_disk_matches"] is False]
    if bad_disk:
        problems.append("on-path manifests whose files on disk do not carry the recorded digests: %s" % bad_disk)
    record = {
        "schema": "m8_sweep_chain_record.v1", "book": "Ezek",
        "ordered_by": "ezek_controlling_rulings_a1#e4 S1-ROUTING (S1-16, S1-17, S1-18) and gate.conditions_before_primaries",
        "built_by": "orchestrator (claude-opus-5) under OW-11; deterministic, from the manifests and the bytes on disk",
        "chain_head": {"path": a.head, "sha256": a.expect_head},
        "origin": origin, "links": path,
        "superseded_branch_manifests": [x for x in manifests if x["manifest"] not in on_path],
        "unrecognized_manifests": unrecognized,
        "S1-17": {"link_named": s1_17[0]["manifest"] if len(s1_17) == 1 else None,
                  "cwo": s1_17[0]["cwo"] if len(s1_17) == 1 else None,
                  "binds": "rows_s4_cwo05_r2.jsonl (f468e2...) -> rows_v2_swept_r2.jsonl (1f11a1...)",
                  "disposition": "named and bound into this record, so the chain has no unseen link"},
        "S1-16": s1_16, "S1-18": s1_18, "problems": problems,
        "limit": "a digest chain proves which bytes followed which; it judges no content",
    }
    text = json.dumps(record, ensure_ascii=False, indent=1)
    summary = {"links": len(path), "origin": origin, "head_reached": bool(path) and path[-1]["output"]["sha256"] == a.expect_head,
               "s1_17": record["S1-17"]["link_named"], "s1_16": {k: s1_16.get(k) for k in ("decision_id", "fields_changed", "no_op_except_chunk_index_renumbering",
                                                                                        "manifest_lists_naming_it", "replaced", "replaced_no_ops",
                                                                                        "chunk_index_renumbered_key")},
               "s1_18": {k: v for k, v in s1_18.items() if k != "disposition"}, "superseded_branch": len(record["superseded_branch_manifests"]),
               "unrecognized": unrecognized, "problems": problems, "chain": [(x["manifest"], x["cwo"], x["output"]["sha256"][:12]) for x in path]}
    if not a.apply or problems:
        print(json.dumps({"mode": "DRY_RUN" if not problems else "REFUSED"} | summary, ensure_ascii=False, indent=1))
        raise SystemExit(1 if problems else 0)
    g = subprocess.run([sys.executable, str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek", "--target", str(OUT)],
                       capture_output=True, text=True, encoding="utf-8")
    if g.returncode != 0:
        raise SystemExit("ABORT: %s is pinned by an in-flight execution:\n%s" % (OUT.name, g.stdout))
    if OUT.exists() and OUT.read_text(encoding="utf-8") != text:
        raise SystemExit("ABORT: %s exists with different content; never replaced" % OUT.name)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print(json.dumps({"mode": "APPLIED", "path": "Ezek/repair/" + OUT.name, "sha256": sha(OUT)} | summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
