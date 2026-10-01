#!/usr/bin/env python3
"""Shared plumbing for Ezekiel's deterministic corpus-wide-order sweeps (CWO-EZ-01, -02, -04, -05, -09), ordered by the
controlling agent in ezek_controlling_rulings_a1#e2.

Each order runs as its OWN sweep (E-18): one input rows file, one output rows file, and one manifest carrying both
digests and every per-row change, old -> new. An input is never overwritten, and an existing output or manifest with
different bytes is never replaced. Manifests carry no timestamps, so a re-run over the same input is byte-identical.
A sweep that changes a span, drops a row, or reorders rows aborts, because boundaries belong to the author wave.
Nothing here judges content.
"""
import hashlib
import json
import sys
from pathlib import Path

EZ = Path(__file__).resolve().parent
REPAIR = EZ / "repair"
RULINGS = EZ / "ezek_controlling_agent_rulings.v1.json"
REPORT_V1 = EZ / "writer" / "draft_rows_combined.suite_view.jsonl.validator_report.json"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha(p) -> str:
    return sha_bytes(Path(p).read_bytes())


def load_rows(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def dump_rows(rows) -> bytes:
    return ("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n").encode("utf-8")


SHAPE_KEYS = ("decision_id", "span", "chunk_index_in_book", "writer_part", "parent_collection")


def assert_same_shape(before, after, keys=SHAPE_KEYS):
    assert len(before) == len(after), "row count changed"
    for a, b in zip(before, after):
        for k in keys:
            assert a[k] == b[k], "%s changed %s on %s; boundaries belong to the author wave" % ("sweep", k, a["decision_id"])


def write_sweep(cwo_id, in_path, out_path, rows_in, rows_out, changes, extra, shape_keys=SHAPE_KEYS, ordered_by=None):
    """Write the output rows and the manifest; refuse to replace differing bytes; return the manifest dict.
    `shape_keys` narrows the shape assertion only for an order whose object IS one of those keys (CWO-EZ-12 re-labels
    parent_collection, and asserts the parent id itself); `ordered_by` names a later controlling execution and its file."""
    assert_same_shape(rows_in, rows_out, shape_keys)
    REPAIR.mkdir(exist_ok=True)
    out = Path(out_path)
    body = dump_rows(rows_out)
    if out.exists() and out.read_bytes() != body:
        raise SystemExit("ABORT: %s exists with different bytes; a sweep output is never replaced" % out.name)
    manifest = {
        "schema": "m8_cwo_sweep_manifest.v1", "cwo": cwo_id, "book": "Ezek",
        "ordered_by": ({"execution": ordered_by[0], "rulings_file": "Ezek/" + Path(ordered_by[1]).name,
                        "rulings_sha256": sha(ordered_by[1])} if ordered_by else
                       {"execution": "ezek_controlling_rulings_a1#e2", "rulings_file": "Ezek/" + RULINGS.name,
                        "rulings_sha256": sha(RULINGS)}),
        "executed_by": "orchestrator (claude-opus-5), deterministic sweep, OW-11 authorized",
        "input": {"path": str(Path(in_path).relative_to(EZ)).replace("\\", "/"), "sha256": sha(in_path), "rows": len(rows_in)},
        "output": {"path": str(out.relative_to(EZ)).replace("\\", "/"), "sha256": sha_bytes(body), "rows": len(rows_out)},
        "rows_changed": len({c["row"] for c in changes}), "change_count": len(changes), "changes": changes,
    }
    manifest.update(extra)
    manifest["limit"] = "a deterministic sweep proves what it changed and that it changed nothing else; it judges no content"
    mp = REPAIR / (out.stem + ".manifest.json")
    mtext = json.dumps(manifest, ensure_ascii=False, indent=1)
    if mp.exists() and mp.read_text(encoding="utf-8") != mtext:
        raise SystemExit("ABORT: %s exists with different content; never replaced" % mp.name)
    out.write_bytes(body)
    mp.write_text(mtext, encoding="utf-8", newline="\n")
    return manifest


def summary(manifest):
    s = {k: manifest[k] for k in ("cwo", "input", "output", "rows_changed", "change_count")}
    for k, v in manifest.items():
        if k.startswith("routed_to_author_wave") or k.startswith("assert"):
            s[k] = len(v) if isinstance(v, list) else v
    return s


if __name__ == "__main__":
    sys.exit("shared module; run a _cwo*.py sweep")
