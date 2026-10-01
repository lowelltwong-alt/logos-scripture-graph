#!/usr/bin/env python3
"""Orchestrator tool: a validator-input VIEW of the combined writer rows, for the Tier-0 suite ONLY.

Why it exists. Three writer parts (p03, p09, p11) wrote boundary_evidence_refs as objects; the other eight wrote
strings, which is the form every Tier-0 tool reads. The brief's schema line ("list of refs, each with its
disclosure") did not fix the form, and the landing validator accepted both, so neither form is a writer error. Which
form is canonical for this book is a controlling-agent item. Until it is ruled, this view lets the suite read every
row instead of crashing on the object form:

  - a string ref is copied unchanged;
  - an object ref becomes one string, "<ref> (<key>: <value>; ...)", over its non-Hebrew keys in a fixed order;
  - an object ref's "hebrew" value is copied into the row's synthetic field _view_ref_hebrew as
    "<hebrew> (<ref>; source: <source>; disclosure: <disclosure>)". The Hebrew-binding and normalization arms skip
    boundary_evidence_refs, so without this copy that Hebrew would go unchecked. Ref and disclosure travel with it,
    because the binding arm reads both from the same field;
  - nothing else changes. A ref missing its witness prefix is NOT given one - that would invent a fact.

The view is never an input to any later round and never replaces the rows file. The input digest is pinned. Unknown
object keys abort. A lossless assertion proves every original string value survives verbatim in its view row. Writes
the view and a manifest carrying both digests.
Usage: _build_suite_view_ezek.py
"""
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
SRC = EZ / "writer" / "draft_rows_combined.jsonl"
SRC_SHA256 = "7b1a16ba5f07aa3443df2be423d6b1618319163720c8c3673409ff06198c6c0e"
OUT = EZ / "writer" / "draft_rows_combined.suite_view.jsonl"
MANIFEST = EZ / "writer" / "draft_rows_combined.suite_view.manifest.json"
ORDER = ("disclosure", "device", "source")
KNOWN = set(ORDER) | {"ref", "hebrew"}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def leaves(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from leaves(v)
    elif isinstance(o, list):
        for v in o:
            yield from leaves(v)
    elif isinstance(o, str):
        yield o


def main() -> int:
    raw = SRC.read_bytes()
    if sha(raw) != SRC_SHA256:
        raise SystemExit("ABORT: %s is not the pinned combined rows (sha256 %s)" % (SRC.name, sha(raw)))
    rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
    out, flattened, copied = [], {}, {}
    for r in rows:
        rid = r.get("writer_decision_id")
        view = dict(r)
        refs, hebrew = [], []
        for x in r.get("boundary_evidence_refs", []):
            if isinstance(x, str):
                refs.append(x)
                continue
            if not isinstance(x, dict) or "ref" not in x or set(x) - KNOWN:
                raise SystemExit("ABORT %s: unexpected ref object %r" % (rid, x))
            parts = ["%s: %s" % (k, x[k]) for k in ORDER if k in x]
            refs.append(x["ref"] + (" (" + "; ".join(parts) + ")" if parts else ""))
            flattened[r["writer_part"]] = flattened.get(r["writer_part"], 0) + 1
            if "hebrew" in x:
                hebrew.append("%s (%s; source: %s; disclosure: %s)"
                              % (x["hebrew"], x["ref"], x.get("source", "unstated"), x.get("disclosure", "none")))
                copied[r["writer_part"]] = copied.get(r["writer_part"], 0) + 1
        view["boundary_evidence_refs"] = refs
        if hebrew:
            view["_view_ref_hebrew"] = hebrew
        blob = json.dumps(view, ensure_ascii=False)
        lost = [s for s in leaves(r) if s not in blob and json.dumps(s, ensure_ascii=False)[1:-1] not in blob]
        if lost:
            raise SystemExit("ABORT lossless check failed on %s: %r" % (rid, lost[:2]))
        out.append(view)
    body = ("\n".join(json.dumps(v, ensure_ascii=False) for v in out) + "\n").encode("utf-8")
    OUT.write_bytes(body)
    manifest = {
        "schema": "m8_suite_view_manifest.v1", "book": "Ezek", "built_by": "orchestrator (claude-opus-5)",
        "input": {"path": "writer/draft_rows_combined.jsonl", "sha256": sha(raw), "rows": len(rows)},
        "output": {"path": "writer/draft_rows_combined.suite_view.jsonl", "sha256": sha(body), "rows": len(out)},
        "object_refs_flattened_by_part": flattened,
        "hebrew_copied_to__view_ref_hebrew_by_part": copied,
        "use": "Tier-0 suite input only. Never an input to any later round; the rows file is unchanged.",
        "known_side_effect": ("a disclosure copied beside its Hebrew can be counted twice by FLAGS members that walk "
                              "every string; hard members are unaffected"),
        "open_item": "the canonical boundary_evidence_refs form for Ezek is a controlling-agent ruling",
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps(manifest, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
