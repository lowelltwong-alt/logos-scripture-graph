#!/usr/bin/env python3
"""Build Daniel's low-confidence sidecar (sidecar_src_dan.jsonl) and its derivation record.

One sidecar row per final row graded low or medium_low, keyed by writer_decision_id (the key the close tool
compares). Six fields are required non-empty: concern_type, why_low_confidence, why_frontier_review_needed,
possible_downstream_risk, suggested_reviewer, proposed_atlas_action. Every why_low_confidence must be unique.

Nothing is written by hand. Five of the six fields are the atlas row's own values, rebuilt here by the atlas
generator (imported from the file beside this one) and refused if the atlas file on disk differs from the rebuild.
why_frontier_review_needed is TRANSCRIBED from the row's own prose: the first sentence that can travel and is not
already in why_low_confidence, taken from strongest_rejected_alternative, else from boundary_rationale; if neither
has one, a COMPOSED sentence built from the row's measured facts, and labelled composed in the derivation record.

Usage: gen_sidecars.py [--dan-root DIR] [--out-root DIR] [--check] [--replace]
       writes <out-root>/sidecar_src_dan.jsonl and <out-root>/deliverables/Dan_sidecar_derivation.v1.jsonl
       --check    rebuilds, compares bytes, writes nothing; the last line printed is MATCH (exit 0) or DIFFERS
       --replace  allow overwriting an existing file whose bytes differ
No clock, no randomness, no directory scan.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIDE_FIELDS = ("concern_type", "why_low_confidence", "why_frontier_review_needed", "possible_downstream_risk",
               "suggested_reviewer", "proposed_atlas_action")
SOURCES = (("strongest_rejected_alternative", "Rival reading on record: "),
           ("boundary_rationale", "Boundary warrant on record: "))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load_generator():
    spec = importlib.util.spec_from_file_location("dan_gen_atlas_rows", str(HERE / "gen_atlas_rows.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(dan_root, out_root):
    gen = load_generator()
    feed, dims, rows = gen.build(dan_root)
    feed_bytes = gen.dump(feed)
    on_disk = (out_root / "deliverables" / "atlas_candidate_feed_rows.jsonl").read_bytes()
    if sha(on_disk) != sha(feed_bytes):
        raise SystemExit("REFUSED: the atlas rows on disk differ from a rebuild; run gen_atlas_rows.py first")
    by_cid = {"M8-Dan-%03d" % r["chunk_index_in_book"]: r for r in rows}
    unit = {d["chunk_decision_id"]: d for d in dims if d.get("record") == "unit"}
    side, deriv = [], []
    for f in feed:
        r, u = by_cid[f["chunk_decision_id"]], unit[f["chunk_decision_id"]]
        why = f["why_low_confidence"]
        frontier, src_field, tier = None, None, None
        for field, prefix in SOURCES:
            for s in gen.clean_sentences(r.get(field), 10 ** 6)[0]:
                if s not in why:
                    frontier, src_field, tier = prefix + s, field, "TRANSCRIBED"
                    break
            if frontier:
                break
        if not frontier:
            m = u["measured"]
            frontier = ("Composed from measured facts: %s is recorded at %s confidence, %d open question%s on record "
                        "name it, and the two blind lanes' verdicts %s." % (
                            f["span"], f["confidence"], len(u["dependency"]["open_questions_naming_this_unit"]),
                            "" if len(u["dependency"]["open_questions_naming_this_unit"]) == 1 else "s",
                            "differ" if m["contested_between_blind_lanes"]["verdicts_differ"] else "do not differ"))
            src_field, tier = None, "COMPOSED"
        row = {"writer_decision_id": r["writer_decision_id"], "decision_id": r["decision_id"],
               "chunk_decision_id": f["chunk_decision_id"], "span": f["span"], "confidence": f["confidence"],
               "concern_type": f["concern_type"], "why_low_confidence": why,
               "why_frontier_review_needed": frontier, "possible_downstream_risk": f["possible_downstream_risk"],
               "suggested_reviewer": f["suggested_reviewer"], "proposed_atlas_action": f["proposed_atlas_action"]}
        empty = [k for k in SIDE_FIELDS if not str(row[k] or "").strip()]
        if empty:
            raise SystemExit("REFUSED: %s has empty %s" % (r["writer_decision_id"], empty))
        side.append(row)
        deriv.append({
            "schema": "dan_sidecar_derivation.v1", "writer_decision_id": r["writer_decision_id"],
            "chunk_decision_id": f["chunk_decision_id"], "span": f["span"],
            "why_low_confidence": {"tier": "COMPOSED" if (u["derivation"] or {}).get("composed_not_derived") else "TRANSCRIBED",
                                   "taken_from": "the atlas row, which takes it from the row's own prose",
                                   "atlas_derivation": u["derivation"], "sha256": sha(why.encode("utf-8"))},
            "why_frontier_review_needed": {"tier": tier, "row_field": src_field,
                                           "rule": "first sentence that can travel and is not already in "
                                                   "why_low_confidence, from strongest_rejected_alternative, else "
                                                   "boundary_rationale, else composed from measured facts",
                                           "sha256": sha(frontier.encode("utf-8"))},
            "concern_type": {"tier": "MEASURED priority over the atlas unit record's measured block",
                             "inputs": {"holds_a_verse_whose_chapter_differs_between_numberings":
                                        u["measured"]["holds_a_verse_whose_chapter_differs_between_numberings"],
                                        "at_or_holding_a_language_change": u["measured"]["at_or_holding_a_language_change"],
                                        "blind_lanes_verdicts_differ": u["measured"]["contested_between_blind_lanes"]["verdicts_differ"],
                                        "onset_seam_evidence_on_both_faces": u["measured"]["seam_evidence"]["onset"]["evidence_on_both_faces"],
                                        "routed_open_questions": u["dependency"]["routed_open_questions_naming_this_unit"]}},
            "possible_downstream_risk": {"tier": "COMPOSED from the atlas unit record's dependency block",
                                         "classes": u["dependency"]["classes"]},
            "suggested_reviewer": {"tier": "ASSIGNED_BY_RULE", "rule": "human_owner where a verse's chapter differs "
                                   "between the numberings; convergence where the blind lanes differ or a routed "
                                   "question names the unit; otherwise literary_form_reviewer"},
            "proposed_atlas_action": {"tier": "CONSTANT", "value": "consider_only"}})
    whys = [s["why_low_confidence"] for s in side]
    if len(set(whys)) != len(whys):
        raise SystemExit("REFUSED: why_low_confidence is not unique across the sidecar")
    want = {r["writer_decision_id"] for r in rows if r["confidence"] in gen.SELECT}
    if {s["writer_decision_id"] for s in side} != want or len(side) != len(want):
        raise SystemExit("REFUSED: sidecar ids are not exactly the low and medium_low rows")
    return gen.dump(side), gen.dump(deriv), side, deriv


def main():
    dan_root, out_root = HERE.parent, None
    for flag in ("--dan-root", "--out-root"):
        if flag in sys.argv:
            v = Path(sys.argv[sys.argv.index(flag) + 1])
            if flag == "--dan-root":
                dan_root = v
            else:
                out_root = v
    out_root = out_root or dan_root
    a, b, side, deriv = build(dan_root, out_root)
    targets = ((out_root / "sidecar_src_dan.jsonl", a), (out_root / "deliverables" / "Dan_sidecar_derivation.v1.jsonl", b))
    if "--check" in sys.argv:
        ok = True
        for p, data in targets:
            on = sha(p.read_bytes()) if p.is_file() else "ABSENT"
            ok = ok and on == sha(data)
            print("%-34s on_disk %s  rebuilt %s" % (p.name, on[:12], sha(data)[:12]))
        print("MATCH" if ok else "DIFFERS")
        sys.exit(0 if ok else 1)
    for p, data in targets:
        if p.is_file() and sha(p.read_bytes()) != sha(data) and "--replace" not in sys.argv:
            raise SystemExit("REFUSED: %s exists with different bytes; pass --replace to overwrite" % p.name)
    for p, data in targets:
        p.write_bytes(data)
        print("%-34s %d bytes  sha256 %s" % (p.name, len(data), sha(data)))
    tiers = {}
    for d in deriv:
        k = "%s/%s" % (d["why_frontier_review_needed"]["tier"], d["why_frontier_review_needed"]["row_field"])
        tiers[k] = tiers.get(k, 0) + 1
    print("rows %d  why_frontier_review_needed sources %s  unique why_frontier %d"
          % (len(side), json.dumps(dict(sorted(tiers.items()))), len({s["why_frontier_review_needed"] for s in side})))


if __name__ == "__main__":
    main()
