#!/usr/bin/env python3
"""Validate one author lane's deliverable: digest parity, accounting, and every edit against the live rows.

WHAT THIS CHECKS, and why each check is here rather than trusted:

  1. DIGEST PARITY against the digest the agent reported. Stale digests were a real failure earlier in this
     book, and the cure (digest after the final write) is only verified if someone measures it.
  2. ITEM ACCOUNTING. Every worklist item on the lane's rows must appear in items_discharged,
     items_discharged_without_edit, or items_NOT_discharged. An item in NONE of them is a silent drop, which
     the brief calls the worst kind of defect - and the whole point of E-31/E-32 is that a worker's own report
     of its coverage is an unverified claim until something compares it to the ORDER.
  3. PROTECTED FIELDS. No edit may address a seam or an identity. The harness refuses these anyway; checking
     here means the lane's author hears about it as a finding rather than as a batch rejection.
  4. EVERY EDIT VALIDATES against the live rows, per sweep, in the ruling's order - via simulate_plan, so an
     edit that legitimately expects an earlier sweep's output is accepted while a genuine mismatch is caught.
  5. ROLE TOKENS. Every A4 append must carry exactly one token from the member's own vocabulary, and no other.
  6. THE ROTATION RULE, measured rather than asserted: annotations distinct, at most six words.

WHAT IT DOES NOT CHECK: whether the new prose is TRUE. That is the spot wave's job against the bytes, and a
tool that tried would encode a judgement it cannot audit.
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import guarded_apply as GA                                                    # noqa: E402

EZ = GA.EZ
sys.path.insert(0, str(EZ / "tools"))
from check_refs_mirror import ROLE_VOCABULARY                                 # noqa: E402

SWEEP_ORDER = ["confidence", "grounds", "marks", "a4", "a6", "disclosures", "vocab"]
PIN = "25cdba568d98ec60aa719606be7b273e6a7c7256c55b79a3c579ada3c21d0ecc"


def validate(lane, path, reported_sha=None):
    p = Path(path)
    measured = hashlib.sha256(p.read_bytes()).hexdigest()
    d = json.loads(p.read_text(encoding="utf-8"))
    edits = d.get("edits") or []
    man = json.loads((Path(__file__).resolve().parent / "lane_manifest.json").read_text(encoding="utf-8"))
    lane_file = next(m["file"] for m in man["lanes"] if m["lane"] == lane)
    lw = json.loads((Path(__file__).resolve().parent / "lanes" / lane_file).read_text(encoding="utf-8"))
    ordered_items = lw["your_worklist_items"]

    accounted = set()
    for k in ("items_discharged", "items_discharged_without_edit", "items_NOT_discharged"):
        for x in (d.get(k) or []):
            accounted.add(json.dumps(x, sort_keys=True) if isinstance(x, (dict, list)) else str(x))
    # the ORDER's own count is the denominator, never the lane's self-report
    n_claimed = len(accounted)

    protected = [(e.get("row_id"), e.get("field")) for e in edits if e.get("field") in GA.PROTECTED]

    # role tokens on A4 appends
    tok_re = re.compile(r"\[([A-Za-z-]+)\]")
    a4 = [e for e in edits if str(e.get("sweep")) == "a4"]

    def new_entries(e):
        """The reference entries an edit ADDS. An append_ref adds one string; a set-on-refs replaces the whole
        list, so the additions are the entries not present in expected_before. A lane may need the latter when
        a quotation repair falls inside an existing entry while citation entries are also being added."""
        if e.get("op") == "append_ref":
            return [str(e.get("value", ""))]
        v = e.get("value")
        if isinstance(v, list):
            before = set(e.get("expected_before") or [])
            return [str(x) for x in v if str(x) not in before]
        return [str(v)]

    bad_tokens, untokened, annotations = [], [], []
    for e in a4:
        for v in new_entries(e):
            toks = tok_re.findall(v)
            if not toks:
                # NOT a verdict: a quotation repair carries no citation token and is legitimately untokened
                untokened.append({"row": e.get("row_id"), "entry": v[:110],
                                  "question": "no ROLE token - verify this is a quotation repair rather than a "
                                              "missed citation token"})
            elif len(toks) != 1 or toks[0] not in ROLE_VOCABULARY:
                bad_tokens.append({"row": e.get("row_id"), "entry": v[:110], "tokens_found": toks})
            else:
                annotations.append((e.get("row_id"), toks[0], v.split("]", 1)[1].strip()))
    too_long = [(r, t, a) for r, t, a in annotations if len(a.split()) > 6]
    per_token = Counter(t for _, t, _ in annotations)
    distinct_per_token = {tk: len({a for _, tt, a in annotations if tt == tk}) for tk in per_token}
    # THE FLOOR THE BRIEF ACTUALLY SETS: at least 4 distinct formulations per token where the token has 4 or
    # more entries. Repeats below that are not a breach, and an all-distinct rule is one my validator invented.
    floor_misses = {tk: distinct_per_token[tk] for tk, n in per_token.items()
                    if n >= 4 and distinct_per_token[tk] < 4}
    repeats = [a for a, n in Counter(a for _, _, a in annotations).items() if n > 1 and a]

    # simulate the lane's own edits, sweep by sweep in the ruling's order
    by_sweep = {}
    for e in edits:
        by_sweep.setdefault(str(e.get("sweep", "?")), []).append(e)
    unknown_sweeps = [s for s in by_sweep if s not in SWEEP_ORDER]
    plan = [(s, by_sweep[s]) for s in SWEEP_ORDER if s in by_sweep]
    try:
        sim = GA.simulate_plan(plan, PIN)
    except GA.Refused as ex:
        sim = {"ok": False, "refused": str(ex)}

    out = {
        "lane": lane,
        "digest": {"measured": measured, "reported": reported_sha,
                   "parity": ("EXACT" if reported_sha and measured == reported_sha
                              else "NOT COMPARED - no digest supplied" if not reported_sha else "MISMATCH")},
        "accounting": {
            "items_in_the_order": len(ordered_items),
            "items_the_lane_accounted_for": n_claimed,
            "discharged_with_an_edit": len(d.get("items_discharged") or []),
            "discharged_without_an_edit": len(d.get("items_discharged_without_edit") or []),
            "not_discharged": len(d.get("items_NOT_discharged") or []),
            "counts_reconcile": n_claimed >= len(ordered_items),
            "note": ("the lane minted its own item ids because the worklist carries none - a defect in my "
                     "worklist, recorded separately - so this compares COUNTS against the order and relies on "
                     "the lane's item_identification block for the mapping"),
            "mapping_block_present": [k for k in d if "item_identification" in k or "item_id" in k] or "NONE - the per-item trace relies on this lane's own id scheme, which is my worklist's defect and not the lane's",
        },
        "protected_field_edits": protected,
        "edits": {"total": len(edits), "by_sweep": {k: len(v) for k, v in sorted(by_sweep.items())},
                  "by_op": dict(Counter(str(e.get("op")) for e in edits)),
                  "unknown_sweeps": unknown_sweeps},
        "role_tokens": {"a4_edits": len(a4), "reference_entries_added": len(annotations) + len(untokened),
                        "malformed": bad_tokens,
                        "untokened_entries_to_verify": untokened,
                        "distribution": dict(per_token)},
        "rotation_rule": {"annotations": len(annotations), "over_six_words": too_long,
                          "distinct_formulations_per_token": distinct_per_token,
                          "tokens_below_the_four_formulation_floor": floor_misses,
                          "repeated_formulations": repeats,
                          "repeats_are_not_a_breach": ("the brief requires at least 4 distinct formulations per "
                                                       "token where the token has 4 or more entries, not that "
                                                       "every formulation be unique. Repeats are reported "
                                                       "because a repeated annotation preceded by the same "
                                                       "token can form a duplicated seven-word sequence; the "
                                                       "validator suite's duplicate gate is what measures "
                                                       "that, and it runs after the apply.")},
        "simulation": sim,
        "escalations": len(d.get("escalations") or []),
    }
    problems = []
    if out["digest"]["parity"] == "MISMATCH":
        problems.append("digest parity")
    if protected:
        problems.append("an edit addresses a PROTECTED field")
    if bad_tokens:
        problems.append("%d reference entries carry a malformed or unknown ROLE token" % len(bad_tokens))
    if too_long:
        problems.append("%d annotations exceed six words" % len(too_long))
    if floor_misses:
        problems.append("%d token classes fall below the four-formulation floor with four or more entries: %r"
                        % (len(floor_misses), floor_misses))
    if unknown_sweeps:
        problems.append("unknown sweep names: %r" % unknown_sweeps)
    if not sim.get("ok"):
        problems.append("the lane's own edits do not validate in sweep order")
    if not out["accounting"]["counts_reconcile"]:
        problems.append("the lane accounted for fewer items than the order carries")
    out["PROBLEMS"] = problems
    out["VERDICT"] = "OK" if not problems else "ATTENTION"
    return out


if __name__ == "__main__":
    lane, path = sys.argv[1], sys.argv[2]
    rep = sys.argv[3] if len(sys.argv) > 3 else None
    r = validate(lane, path, rep)
    dest = Path(__file__).resolve().parent / ("validate_%s.json" % lane)
    dest.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    slim = dict(r)
    slim["simulation"] = {k: v for k, v in (r.get("simulation") or {}).items() if k != "sweeps"}
    if (r.get("simulation") or {}).get("sweeps"):
        slim["simulation"]["sweeps"] = [{kk: vv for kk, vv in s.items() if kk != "problems"}
                                        for s in r["simulation"]["sweeps"]]
    print(json.dumps(slim, ensure_ascii=False, indent=1))
