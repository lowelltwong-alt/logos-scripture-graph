#!/usr/bin/env python3
"""CWO-EZ-01 (ruling R1): boundary_evidence_refs to the canonical STRING form, losslessly, as its own sweep.

R1 fixed the canonical form: a list of strings, one witness-prefixed ref per entry, then a parenthesised disclosure
('oshb:Ezek.C.V (...)' or 'web:Ezek.C.V (...)', dual inside the zone). Predicate: every OBJECT entry (p03 67, p09 33,
p11 56).

The transform is deterministic:
  - an object {ref, disclosure?, device?, source?, hebrew?} becomes "<ref> (<key>: <value>; ...)", keys in the fixed
    order disclosure, device, source, hebrew. R1 allows a Hebrew splice inside the parenthesis; its byte truth is
    checked by the normalizer and citation_sweep afterwards, never assumed here;
  - p03's object refs are BARE Ezek.C.V. Each gets the prefix oshb:. That supplies no fact the entry lacked. Every p03
    ref is asserted to lie in identity numbering (outside WEB 20:45-21:32 and MT ch 21), where the coordinates are the
    same in both witnesses. Every p03 disclosure cites an MT-byte device: a formula or a parashah mark. The choice is
    recorded per entry in the manifest;
  - a string entry is copied unchanged. A string entry that is not witness-prefixed lies outside this order's predicate,
    so it is LISTED for the author wave and never rewritten.
Lossless: every original string value (the ref and each key's value) must appear verbatim in its new string.

Usage: _cwo01_refs_form.py --in writer/draft_rows_combined.jsonl --out repair/rows_s1_cwo01.jsonl
"""
import argparse
import json
import re
import sys

from _sweep_common import EZ, load_rows, summary, write_sweep

sys.stdout.reconfigure(encoding="utf-8")
ORDER = ("disclosure", "device", "source", "hebrew")
KNOWN = set(ORDER) | {"ref"}
PREFIXED = re.compile(r"^(web|oshb):Ezek\.\d+\.\d+")
BARE = re.compile(r"^Ezek\.(\d+)\.(\d+)")


def in_zone_chapter(ch, v):
    return ch == 21 or (ch == 20 and v >= 45)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    in_p, out_p = EZ / a.inp, EZ / a.out
    rows_in = load_rows(in_p)
    rows_out, changes, unprefixed_strings = [], [], []
    for r in rows_in:
        new_refs = []
        for i, x in enumerate(r.get("boundary_evidence_refs", [])):
            if isinstance(x, str):
                if not PREFIXED.match(x):
                    unprefixed_strings.append({"row": r["decision_id"], "index": i, "entry": x})
                new_refs.append(x)
                continue
            if not isinstance(x, dict) or "ref" not in x or set(x) - KNOWN:
                raise SystemExit("ABORT %s[%d]: object outside the known shape: %r" % (r["decision_id"], i, x))
            ref = x["ref"]
            prefix_note = None
            if not PREFIXED.match(ref):
                m = BARE.match(ref)
                if not m:
                    raise SystemExit("ABORT %s[%d]: ref neither witness-prefixed nor bare Ezek.C.V: %r" % (r["decision_id"], i, ref))
                if r["writer_part"] != "p03":
                    raise SystemExit("ABORT %s[%d]: a bare ref outside p03 was not expected: %r" % (r["decision_id"], i, ref))
                if in_zone_chapter(int(m.group(1)), int(m.group(2))):
                    raise SystemExit("ABORT %s[%d]: bare ref inside the numbering zone; a prefix would be a guess" % (r["decision_id"], i))
                ref = "oshb:" + ref
                prefix_note = "bare ref in identity numbering; oshb: prefix (coordinates equal in both witnesses; MT-byte device cited)"
            parts = ["%s: %s" % (k, x[k]) for k in ORDER if k in x]
            s = ref + (" (" + "; ".join(parts) + ")" if parts else "")
            lost = [v for v in x.values() if isinstance(v, str) and v not in s]
            if lost:
                raise SystemExit("ABORT %s[%d]: lossless check failed: %r" % (r["decision_id"], i, lost))
            new_refs.append(s)
            changes.append({"row": r["decision_id"], "field": "boundary_evidence_refs", "index": i,
                            "old": x, "new": s, **({"prefix": prefix_note} if prefix_note else {})})
        nr = dict(r)
        nr["boundary_evidence_refs"] = new_refs
        rows_out.append(nr)
    by_part = {}
    for c in changes:
        p = next(r["writer_part"] for r in rows_in if r["decision_id"] == c["row"])
        by_part[p] = by_part.get(p, 0) + 1
    m = write_sweep("CWO-EZ-01", in_p, out_p, rows_in, rows_out, changes, {
        "predicate": "every object entry in boundary_evidence_refs",
        "object_entries_converted_by_part": by_part,
        "assert_no_object_entries_remain": all(isinstance(x, str) for r in rows_out for x in r["boundary_evidence_refs"]),
        "routed_to_author_wave_unprefixed_string_entries": unprefixed_strings,
    })
    print(json.dumps(summary(m) | {"object_entries_converted_by_part": by_part}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
