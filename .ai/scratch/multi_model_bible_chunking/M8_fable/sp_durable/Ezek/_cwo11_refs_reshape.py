#!/usr/bin/env python3
"""CWO-EZ-11 (ezek_controlling_rulings_a1#e3, ruling R1F-1), run as its own deterministic sweep over the APPLIED rows.

Predicate: every boundary_evidence_refs entry that opens on a witness-prefixed ref and does not match ruling R1's strict
shape (a ref, an optional dual, then a parenthesised disclosure).

  (1) SPLIT. An entry whose head (the text before its first parenthesis) carries more than one ref or dual becomes one
      entry per ref or dual, each followed by the original tail verbatim. citation_sweep validates only an entry's FIRST
      ref and keys the tail's mark, paseq and K/Q claims to it, so a second ref in the same entry was unguarded.
  (2) RE-SHAPE. An entry with non-empty text between its opening ref (or dual) and its first parenthesis becomes
      ref [+ dual] + ' (' + rest + ')', losslessly.

Not touched and reported:
  - an entry whose '=' is followed by a WEB quotation instead of a ref (p06's author order owns those);
  - an entry whose head carries non-connector words BETWEEN two refs, since a split would drop them.

Lossless assertions:
  - every ref and dual of an old entry reappears in the new entries;
  - a split carries the tail byte for byte;
  - a re-shape strips back to the original text.
Row count, order, spans and parents are unchanged (_sweep_common).
Afterwards, every entry outside the strict shape must be a reported one.

Usage: _cwo11_refs_reshape.py --in <applied rows> --out <swept rows>   (both under SP/Ezek)
"""
import argparse
import json
import re
import sys

from _sweep_common import EZ, load_rows, summary, write_sweep

sys.stdout.reconfigure(encoding="utf-8")
RULINGS_E3 = EZ / "ezek_controlling_agent_rulings_e3.v1.json"
REF_ONE = r"(?:oshb|web):Ezek\.\d+\.\d+(?:-Ezek\.\d+\.\d+)?"
GROUP = re.compile(r"%s(?:\s*=\s*%s)?" % (REF_ONE, REF_ONE))            # one ref, or one dual
CANON = re.compile(r"^%s(?:\s*=\s*%s)?(?:\s+\(.*\))?$" % (REF_ONE, REF_ONE), re.S)
OPENS = re.compile(r"^(?:oshb|web):Ezek\.\d+\.\d+")
WEB_QUOTE_EQ = re.compile(r"^%s\s*=\s*[\"“']" % REF_ONE)
CONNECTOR = re.compile(r"^[\s,;&]*(?:and)?[\s,;&]*$", re.I)


def reshape(entry):
    """(status, new_entries, why) where status is None (outside the predicate), 'split', 'reshaped' or 'reported'."""
    s = entry.strip()
    if not OPENS.match(s) or CANON.match(s):
        return None, [entry], None
    if WEB_QUOTE_EQ.match(s):
        return "reported", [entry], "'=' followed by a WEB quotation, not a ref (p06's author order)"
    paren = s.find("(")
    head, tail = (s[:paren], s[paren:]) if paren != -1 else (s, "")
    groups = list(GROUP.finditer(head))
    lead = groups[0]
    if len(groups) > 1:
        between = [head[groups[i].end():groups[i + 1].start()] for i in range(len(groups) - 1)]
        if not all(CONNECTOR.match(b) for b in between):
            return "reported", [entry], "words between refs in the head; a split would drop them"
        trailing = head[groups[-1].end():].strip()
        rest = (trailing + " " + tail).strip() if trailing else tail
        new = [g.group(0) + ((" (" + rest + ")") if trailing else ((" " + tail) if tail else "")) for g in groups]
        assert all(tail in n for n in new), "a split lost the tail"
        return "split", new, None
    rest = s[lead.end():].strip()
    new = lead.group(0) + " (" + rest + ")"
    assert new[len(lead.group(0)) + 2:-1] == rest, "re-shape is not lossless"
    return "reshaped", [new], None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    in_p, out_p = EZ / a.inp, EZ / a.out
    rows_in = load_rows(in_p)
    rows_out, changes, reported = [], [], []
    counts = {"split": 0, "reshaped": 0}
    for r in rows_in:
        nr = dict(r)
        new_refs = []
        for i, e in enumerate(r.get("boundary_evidence_refs") or []):
            status, new, why = reshape(e) if isinstance(e, str) else (None, [e], None)
            if status in ("split", "reshaped"):
                counts[status] += 1
                old_groups = [g.group(0) for g in GROUP.finditer(e.split("(", 1)[0])]
                assert all(any(g in n for n in new) for g in old_groups), "a ref was lost"
                changes.append({"row": r["decision_id"], "field": "boundary_evidence_refs[%d]" % i, "op": status, "old": e, "new": new})
            elif status == "reported":
                reported.append({"row": r["decision_id"], "field": "boundary_evidence_refs[%d]" % i, "entry": e, "why": why})
            new_refs.extend(new)
        nr["boundary_evidence_refs"] = new_refs
        rows_out.append(nr)
    left = [(r["decision_id"], e) for r in rows_out for e in r.get("boundary_evidence_refs") or []
            if isinstance(e, str) and OPENS.match(e.strip()) and not CANON.match(e.strip())]
    reported_set = {(x["row"], x["entry"]) for x in reported}
    m = write_sweep("CWO-EZ-11 (boundary_evidence_refs split and re-shape)", in_p, out_p, rows_in, rows_out, changes, {
        "narrowed_predicate_label": "every boundary_evidence_refs entry of every row of the applied rows file that opens on a "
                                    "witness-prefixed ref and does not match the strict R1 shape",
        "split_entries": counts["split"], "reshaped_entries": counts["reshaped"],
        "reported_not_touched": reported,
        "assert_lossless": True,
        "assert_only_reported_entries_remain_outside_the_strict_shape": set(left) <= reported_set,
        "outside_strict_shape_after": len(left)}, ordered_by=("ezek_controlling_rulings_a1#e3", RULINGS_E3))
    print(json.dumps(summary(m) | {"split": counts["split"], "reshaped": counts["reshaped"], "reported": len(reported),
                                   "outside_strict_shape_after": len(left)}, ensure_ascii=False, indent=1))
    if not set(left) <= reported_set:
        raise SystemExit("ABORT-AFTER-WRITE: entries outside the strict shape that were neither swept nor reported: %s" % (sorted(set(left) - reported_set)[:5],))


if __name__ == "__main__":
    main()
