#!/usr/bin/env python3
"""Phase 2 step 1 (orchestrator, deterministic; Lam's _phase2_build_clusters.py lineage, sized to Ezekiel): build the
pre-primaries review cluster plan (full dual-blind LF sonnet + OL opus per cluster) and the per-row declared-FP flag
digest the primaries pressure-test.

Differences from Lam, each forced by Ezekiel's data rather than chosen:
  - the rows file and its validator report are ARGUMENTS, because the controlling agent may order a repair of the draft
    rows before primaries; the plan must be built over the rows primaries will actually review;
  - the row id is decision_id (P01-002 form), the id every Tier-0 member reports; the pattern is ASSERTED per row,
    never assumed, and writer_decision_id is carried beside it;
  - clusters record parent_collection as well as writer part, because two Ezekiel parts straddle a parent seam.
Contiguous book-order clusters of <=8 rows; the row total is READ, never assumed; sizes are the most even split into
ceil(N/8). Refuses to overwrite an existing plan with different content unless --replace is given.

Usage: _phase2_build_clusters_ezek.py --rows <rows.jsonl> --report <rows validator report .json> [--replace]
"""
import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
RID = re.compile(r"P\d{2}-\d{3}")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--replace", action="store_true")
    a = ap.parse_args()
    rows_p, rep_p = Path(a.rows), Path(a.report)
    rows = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    N = len(rows)
    assert N >= 8, "unexpectedly few rows: %d" % N
    for i, r in enumerate(rows, 1):
        assert r["chunk_index_in_book"] == i, "row %d carries chunk_index_in_book %s" % (i, r["chunk_index_in_book"])
        assert RID.fullmatch(str(r.get("decision_id", ""))), "row %d decision_id %r is not P##-### form" % (i, r.get("decision_id"))
        assert r["book"] == "Ezek" and re.fullmatch(r"Ezek\.\d+\.\d+-Ezek\.\d+\.\d+", r["span"]), r["span"]
    ids = [r["decision_id"] for r in rows]
    assert len(set(ids)) == N, "duplicate decision_id"
    k = math.ceil(N / 8)
    base, extra = divmod(N, k)
    sizes = [base + 1] * extra + [base] * (k - extra)
    assert sum(sizes) == N and max(sizes) <= 8

    clusters, pos = [], 0
    for n, size in enumerate(sizes, 1):
        chunk = rows[pos:pos + size]
        pos += size
        parts, parents = [], []
        for r in chunk:
            if r["writer_part"] not in parts:
                parts.append(r["writer_part"])
            if r["parent_collection"] not in parents:
                parents.append(r["parent_collection"])
        clusters.append({"id": "c%02d" % n, "row_ids": [r["decision_id"] for r in chunk],
                         "writer_decision_ids": [r["writer_decision_id"] for r in chunk],
                         "span": "%s-%s" % (chunk[0]["span"].split("-")[0], chunk[-1]["span"].split("-")[1]),
                         "parts": parts, "parents": parents})
    assert pos == N
    plan = {"built": "pre-primaries cluster plan (full dual-blind LF sonnet + OL opus per cluster; Ezek, m8-mesh-r3)",
            "rows_file": {"path": str(rows_p), "sha256": sha(rows_p.read_bytes())},
            "rows_total": N, "clusters_total": len(clusters),
            "sizes": " + ".join("%d x %d" % (sizes.count(s), s) for s in sorted(set(sizes), reverse=True)),
            "clusters": clusters}

    rep = json.loads(rep_p.read_text(encoding="utf-8-sig"))
    row_id_by_index = {r["chunk_index_in_book"]: r["decision_id"] for r in rows}
    known = set(ids)

    def find_row_id(entry):
        if isinstance(entry, dict):
            path = entry.get("path")
            if isinstance(path, str):
                m = re.match(r"\[(\d+)\]", path)
                if m and int(m.group(1)) + 1 in row_id_by_index:
                    return row_id_by_index[int(m.group(1)) + 1]
            for kk in ("decision_id", "writer_decision_id", "row_id", "row"):
                v = entry.get(kk)
                if isinstance(v, str) and v in known:
                    return v
                if isinstance(v, int) and v in row_id_by_index:
                    return row_id_by_index[v]
            for v in entry.values():
                if isinstance(v, str):
                    m = RID.search(v)
                    if m and m.group(0) in known:
                        return m.group(0)
        elif isinstance(entry, str):
            m = RID.search(entry)
            if m and m.group(0) in known:
                return m.group(0)
        return None

    sources = [("web_quotes", ["flags", "neighbor_only_warns"]), ("refs_mirror", ["flags", "orphan_ref_warns"]),
               ("mark_symmetry", ["flags", "warns"]), ("universals", ["flags"]), ("register", ["flags"]),
               ("citation_sweep", ["prose_dual_warns", "kq_web_quote_warns"])]
    by_row, unresolved, total = {}, [], 0
    for member, keys in sources:
        for key in keys:
            for entry in rep.get(member, {}).get(key, []) or []:
                total += 1
                rid = find_row_id(entry)
                item = {"member": member, "kind": key, "flag": entry}
                (by_row.setdefault(rid, []) if rid else unresolved).append(item)
    digest = {"built": ("declared-FP queues from the FLAGS members of the validator report (writer-dispositioned, NOT "
                        "orchestrator-accepted; primaries pressure-test them)"),
              "report": {"path": str(rep_p), "sha256": sha(rep_p.read_bytes())},
              "total_flags": total, "rows_with_flags": len(by_row), "unresolved_count": len(unresolved),
              "by_row": {rid: by_row[rid] for rid in sorted(by_row)}, "unresolved": unresolved}

    outputs = {"review_clusters.json": plan, "flags_by_row.json": digest}
    for name, obj in outputs.items():
        p = HERE / name
        text = json.dumps(obj, ensure_ascii=False, indent=1)
        if p.exists() and p.read_text(encoding="utf-8") != text and not a.replace:
            raise SystemExit("ABORT: %s exists with different content; rerun with --replace only if the rows changed" % name)
    for name, obj in outputs.items():
        (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({"rows_total": N, "clusters_total": len(clusters), "sizes": plan["sizes"],
                      "spans_first_last": [clusters[0]["span"], clusters[-1]["span"]],
                      "clusters_crossing_a_parent": [c["id"] for c in clusters if len(c["parents"]) > 1],
                      "flags_total": total, "rows_with_flags": len(by_row), "unresolved": len(unresolved)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
