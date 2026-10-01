#!/usr/bin/env python3
r"""OW-3 bounded re-adjudication slice builder (owner directive 2026-09-04, items
2 and 3). Selects, from the COMPLETED Isaiah LF-support routing queue (146 items
in receipts/OW2_isa_lf_remediation_docket.v1.json — the pre-feedback baseline,
read-only), the BOUNDED subset that depends on an onset-only / own-seam warrant
assumption (the seam-warrant classes) plus the two owner-named validation items
(P07-002#1 replacement-claim validation; P09-005#1 characterization), joins each
with its full audit finding (from the frozen ow2lf packets), its prior
adjudication (verdict + grounds, preserved as prior_adjudication), the shipped
row with BOTH neighbors, and an item-specific re-adjudication_instruction; groups
by row; packs <= 8 items per slice in frame order. Placeholder tokens in the
frozen proposals are carried WITH their collate-proven byte resolutions (never
edited in the baseline). Emits slices/slice_ow3re_NN.json for the Fable-5-high
lane (READJUDICATION_BRIEF_OW3.md; verifier _ow2adj_verify.py, pinned + unchanged).
Usage: _build_ow3_readj_slices.py --resolutions <path to _placeholder_resolutions.json>
"""
import argparse
import glob
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
DOCKET = M8 / "receipts" / "OW2_isa_lf_remediation_docket.v1.json"
MAX_ITEMS = 8
SEAM_CLASSES = {"no_tier1_at_own_seam", "front_seam_warrant_not_tier1", "unwarranted_front_seam",
                "front_seam_warrant_absent", "non_tier1_seam_warrant", "rear_seam_unwarranted",
                "tier3_only_back_seam_warrant", "warrant_gap_close_seam",
                "engagement_class_opening_seam_not_byte_engaged", "undisclosed_rival_construal_at_opening_seam",
                "rear_seam_warrant_byte_false", "front_seam_warrant_byte_false"}
SEAM_CLASS_PREFIX = re.compile(r"front-seam warrant rests|seam warrant", re.I)
NAMED = {"P07-002#1", "P09-005#1"}
SPAN_PAT = re.compile(r"respan|re-span|new span|span set|merge|merging|split|absorb|"
                      r"boundary (?:change|move|relocat)|move the seam|retire", re.I)

BOTH_SIDES = ("Apply the both-sides seam law: weigh the adjacent unit's close (for a front seam) or onset (for a "
              "rear seam) from bytes BEFORE ruling; if the filed finding's ground was onset-only, re-rule on the "
              "complete test under the strategy (§6: refrains close units; frame onsets; addressee shifts; "
              "imperative/vocative summons; formula onsets).")
INSTRUCTIONS = {
    "P01-012#1": ("Reconcile Isa strategy §6 ('refrains close units') with the onset-only diagnosis: the preceding "
                  "shipped row M8-Isa-011 (Isa.2.12-2.17) byte-splices the 2:17 closing refrain, and 2:11 carries the "
                  "same refrain closing the prior stanza — collate both sites and state the tier. Assess support for "
                  "the 2:17|2:18 boundary from BOTH sides (the refrain close on the left; the opening bytes of 2:18 on "
                  "the right) and only then rule the HIGH and the merger proposal afresh. Do not adopt or reject a "
                  "boundary because a reviewer suggested this check; re-derive it. " + BOTH_SIDES),
    "P07-002#1": ("The challenge to the 'wholly third person' sentence stands or falls on its own bytes (re-derive "
                  "MT 24:14-15). SEPARATELY validate the proposal's replacement claim — 'one sung praise-reaction "
                  "with a single referent group across the couplet' — from independent source bytes (the couplet "
                  "and its neighbors, the pronoun/verb persons, the addressee forms): if the bytes do not fully "
                  "support a single referent group, QUALIFY the replacement (say exactly what the bytes support) "
                  "rather than letting an unsupported replacement warrant ride into a repair."),
    "P02-010#1": ("The proposal's unexpanded placeholder {718_ext} resolves from source bytes to the verse-initial "
                  "onset of oshb:Isa.7.18 (see placeholder_resolutions; collate-proven byte tier at staging). Rule "
                  "with the resolved text. This item and P02-011#1 are ONE source occurrence — the shared "
                  "7:17|7:18 seam — requiring two row repairs: rule them coherently. " + BOTH_SIDES),
    "P02-011#1": ("The proposal's unexpanded placeholder {718_ext} resolves from source bytes to the verse-initial "
                  "onset of oshb:Isa.7.18 (see placeholder_resolutions; collate-proven byte tier at staging). Rule "
                  "with the resolved text. This item and P02-010#1 are ONE source occurrence — the shared "
                  "7:17|7:18 seam — requiring two row repairs: rule them coherently. " + BOTH_SIDES),
    "P09-005#1": ("Characterize the defect precisely: distinguish INADEQUATE TREATMENT of the row's acknowledged "
                  "imperative/vocative signals (the row itself quotes the 33:13 summons and names its formal class) "
                  "from TOTAL OMISSION; state which the bytes show. The split remains a PROPOSAL — rule it afresh "
                  "under the both-sides law (the MT 33:12 SAMEKH, the 33:13 verse-initial summons, and the "
                  "neighbouring 34:1 onset). " + BOTH_SIDES),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--resolutions", required=True)
    ns = ap.parse_args()
    resolutions = json.load(open(ns.resolutions, encoding="utf-8"))
    docket = json.load(open(DOCKET, encoding="utf-8"))
    items = docket["items"]
    subset = [i for i in items if i["class"] in SEAM_CLASSES or SEAM_CLASS_PREFIX.search(i["class"]) or i["item_id"] in NAMED]
    ids = [i["item_id"] for i in subset]
    assert len(ids) == len(set(ids))
    # full findings from the frozen audit packets (routed-item numbering rule = the verifier's rule)
    findings = {}
    for f in sorted(glob.glob(str(HERE / "reviews" / "ow2lf_b*.json"))):
        pk = json.load(open(f, encoding="utf-8"))
        for r in pk["rows"]:
            k = 0
            for fd in r.get("findings") or []:
                sc = fd.get("proposed_change")
                ex = fd.get("span_change")
                is_span = (bool(ex) if isinstance(ex, bool) else bool(sc) and bool(SPAN_PAT.search(str(sc))))
                if fd["severity"] in ("medium", "high") or is_span:
                    k += 1
                    findings[f"{r['row_id']}#{k}"] = dict(fd, span_change=is_span)
    # row context from the frozen audit slices
    context = {}
    for f in sorted(glob.glob(str(HERE / "slices" / "slice_b*.json"))):
        sl = json.load(open(f, encoding="utf-8"))
        for it in sl["items"]:
            context[it["row_id"]] = it
    row_order = []
    row_items = {}
    for i in subset:
        iid = i["item_id"]
        rid = i["row_id"]
        fd = findings[iid]
        q = {"item_id": iid, "row_id": rid, "audit_batch": i["audit_batch"], "severity": i["filed_severity"],
             "class": i["class"], "claim": i["claim"], "grounds": fd.get("grounds"),
             "span_change": bool(i.get("span_change_proposed")), "proposed_change": fd.get("proposed_change"),
             "prior_adjudication": {"batch": i.get("adjudication_batch"), "verdict": i["verdict"],
                                    "final_severity": i["final_severity"], "span_ruling": i.get("span_ruling"),
                                    "grounds": i.get("adjudicator_grounds"),
                                    "note": "pre-feedback baseline (OW-2 item 1, 2026-09-03) — preserved, not edited"},
             "readjudication_instruction": INSTRUCTIONS.get(iid, BOTH_SIDES)}
        ph = re.findall(r"\{[A-Za-z0-9][A-Za-z0-9_\-\.:]*\}", json.dumps(fd, ensure_ascii=False))
        if ph:
            q["placeholder_resolutions"] = {p: resolutions[p] for p in sorted(set(ph)) if p in resolutions}
            assert len(q["placeholder_resolutions"]) == len(set(ph)), f"unresolved placeholder in {iid}: {ph}"
        if rid not in row_items:
            row_items[rid] = []
            row_order.append((context[rid]["shipped_row"]["chunk_index_in_book"], rid))
        row_items[rid].append(q)
    row_order.sort()
    groups, cur, n = [], [], 0
    for _, rid in row_order:
        k = len(row_items[rid])
        if cur and n + k > MAX_ITEMS:
            groups.append(cur)
            cur, n = [], 0
        cur.append(rid)
        n += k
    if cur:
        groups.append(cur)
    report = []
    for i, rids in enumerate(groups, 1):
        name = f"ow3re_{i:02d}"
        doc = {"schema": "m8_ow3_readj_slice.v1", "batch": name, "book": "Isa",
               "attempt_id": f"ow2adj_re_{i:02d}_a1", "output_file": f"reviews/ow2adj_re_{i:02d}.json",
               "lane": "OW-3 bounded re-adjudication (post-feedback; the OW-2 item-1 baseline is preserved)",
               "item_ids": [q["item_id"] for rid in rids for q in row_items[rid]],
               "rows": [{"row_id": rid, "audit_batch": context[rid]["audit_batch"] if "audit_batch" in context[rid] else row_items[rid][0]["audit_batch"],
                         "queue_items": row_items[rid],
                         "context": {"shipped_row": context[rid]["shipped_row"],
                                     "prev_row": context[rid].get("prev_row"), "next_row": context[rid].get("next_row")}}
                        for rid in rids]}
        out = HERE / "slices" / f"slice_{name}.json"
        out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        report.append({"slice": name, "rows": len(rids), "items": len(doc["item_ids"]), "bytes": out.stat().st_size})
    print(json.dumps({"subset_items": len(ids), "subset_rows": len(row_order), "item_ids": ids,
                      "slices": report, "placeholders_resolved": sorted(resolutions)}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
