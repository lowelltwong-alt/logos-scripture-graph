#!/usr/bin/env python3
"""Deterministic boss-docket builder — Jer boss round (m8-mesh-r3).

Consumes remedy_docket.v1.json + draft_rows_combined.jsonl and emits
boss_docket.json (master) + boss_docket_b1..b4.json (per-agent slices).

Item selection basis (orchestrator scan of all 215 remedies, 2026-08-31):
- 22 remedies carry a CONCRETE named boundary/respan/merge/split proposal
  flagged "PROPOSAL requiring explicit boss/owner adoption" (P10-012 and
  P10-013 name the SAME seam from both sides -> ONE paired item).
- Guard-only clauses ("any respan would be a proposal") without a named
  alternative span create NO item; their cures are author work.
- Plus: CWO-5 policy question (closure-key scope), the single-refute
  calibration direction item (P13-006 exemplar), the zero-escalation
  record, the Tier-0 coverage verification, and the sample-lane defect
  ratification (P06-009).
Every named id is hard-asserted against the docket and the frozen corpus.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCKET = HERE / "remedy_docket.v1.json"
ROWS = HERE / "draft_rows_combined.jsonl"

d = json.load(open(DOCKET, encoding="utf-8"))
dk = d["docket"]
rows = [json.loads(l) for l in open(ROWS, encoding="utf-8")]
by_id = {r["decision_id"]: r for r in rows}
by_idx = {r["chunk_index_in_book"]: r for r in rows}
assert len(rows) == 276 and len(by_id) == 276, "corpus shape"

# (agent, item_id, kind, row_ids, question)
ITEMS = [
    ("b1", "B1-1", "span_proposal", ["P01-012"],
     "Rule the proposed re-span at Jer.3.14 (peer: PROPOSAL only, boss adoption required). ADOPT with the exact new span set, unit_type and parent of every resulting row, and the tiling consequence (1364/1364 must survive) - or DECLINE and let the disclosure/splice cures stand as author work."),
    ("b1", "B1-2", "span_proposal", ["P02-001"],
     "Rule the proposed cut at Jer.4.7 (peer: PROPOSAL only). ADOPT with exact spans/unit_type/parent/tiling, or DECLINE."),
    ("b1", "B1-3", "span_proposal", ["P02-007"],
     "Rule the proposed cut at Jer.4.31 separating the death-cry from the formula-opened oracle (peer: PROPOSAL ONLY, flagged for boss adoption). ADOPT with exact spec, or DECLINE."),
    ("b1", "B1-4", "span_proposal", ["P02-017"],
     "Rule whether Jer.6.8 is cut into its own row (peer: NOT ordered, needs explicit adoption). ADOPT with exact spec, or DECLINE."),
    ("b1", "B1-5", "span_proposal", ["P02-021"],
     "Rule the 6:19/6:20 boundary question (peer: any re-cut there is a PROPOSAL requiring explicit adoption). ADOPT an exact re-cut, or DECLINE."),
    ("b1", "B1-6", "span_proposal", ["P03-008"],
     "Rule the example respan the peer names: opening the unit after the seg and the neum-YHWH tag at oshb:Jer.9.2 = web:Jer.9.3 (OFFSET ZONE - dual-cite discipline mandatory). ADOPT with exact spec, or DECLINE."),
    ("b2", "B2-1", "span_proposal", ["P04-011"],
     "Rule the boundary PROPOSAL (boss adoption required): merge 12:1-6 into one petition-and-reply row. ADOPT with exact merged span/unit_type/parent + which row retires + tiling consequence, or DECLINE."),
    ("b2", "B2-2", "span_proposal", ["P05-014"],
     "Rule the proposed split at 15:19 (peer: boundary PROPOSAL requiring explicit adoption). ADOPT with exact spec, or DECLINE."),
    ("b2", "B2-3", "span_proposal", ["P06-004"],
     "Rule the proposed merge of 16:16-18 into the preceding row (peer: boundary PROPOSAL requiring explicit adoption). ADOPT with exact spec + retirement + tiling, or DECLINE."),
    ("b2", "B2-4", "span_proposal", ["P06-008"],
     "Rule the proposed respan folding 17:12-13 into the petition (peer: BOUNDARY PROPOSAL requiring explicit boss adoption; the remedy cures the row as spanned). ADOPT with exact spec, or DECLINE."),
    ("b2", "B2-5", "span_proposal", ["P06-012"],
     "Rule the proposed fold of 18:13-18:17 back into the potter unit as the divine reply to the refusal at 18:12 (peer: BOUNDARY PROPOSAL requiring explicit boss adoption). ADOPT with exact spec + retirement + tiling, or DECLINE."),
    ("b2", "B2-6", "span_proposal", ["P07-008"],
     "Rule the proposed split at 22:5|22:6 (peer: boundary PROPOSAL requiring explicit adoption). ADOPT with exact spec, or DECLINE."),
    ("b2", "B2-7", "sample_defect_ratification", ["P06-009"],
     "Ratify the sample-lane defect on BOTH-SUPPORT row P06-009 into an author work order: the seam argument omits the identical shaming-verb form closing MT 17:13 and opening MT 17:18 (skeleton-tier inclusio candidate the row never engages). Confirm the defect from bytes and write the exact author work order + cure test, or rule no_action with grounds."),
    ("b3", "B3-1", "span_proposal", ["P10-012", "P10-013"],
     "PAIRED RULING - ONE seam, raised independently from both sides: close the P10-012 unit at 29:19 and open the P10-013 unit at 29:20 (instead of the current 29:20|29:21 seam). Rule the pair as ONE decision: ADOPT the seam move with both rows' exact new spans + tiling consequence, or DECLINE for both. A split verdict (adopt one side only) is incoherent - forbidden."),
    ("b3", "B3-2", "span_proposal", ["P11-002"],
     "Resolve the peer's CONDITIONAL: if the row's rejection of the 30:8 cut cannot be re-grounded on bytes, the alternative becomes a boundary PROPOSAL (cut at Jer.30.8). Decide the condition yourself from bytes: either the rejection RE-GROUNDS (disclosure cure stands, no respan) or rule the cut ADOPT/DECLINE explicitly."),
    ("b3", "B3-3", "span_proposal", ["P11-005"],
     "Resolve the peer's CONDITIONAL at Jer.31.3 (same shape as B3-2): re-ground the rejection on bytes, or rule the proposed cut ADOPT/DECLINE explicitly."),
    ("b3", "B3-4", "span_proposal", ["P11-012"],
     "Rule whether the seam at oshb:Jer.31.29 should be cut (peer: boundary proposal for adoption, not author work). ADOPT with exact spec, or DECLINE."),
    ("b3", "B3-5", "span_proposal", ["P14-008"],
     "Rule the boundary PROPOSAL: fold Jer.38.21-Jer.38.23 into Jer.38.14-Jer.38.20 as one unit closing at the mark keyed to MT 38:23. ADOPT with exact spec + retirement + tiling, or DECLINE."),
    ("b3", "B3-6", "calibration_record", [],
     "CALIBRATION DIRECTION ITEM (census direction (a)): the peer round returned 1 refute in 216 rulings (215 sustained). Weigh TRUE primaries challenge precision vs an UNDER-USED refutation bar, using P13-006's refuting grounds (embedded below; full packet at reviews/peer_11_r2.json) as the calibration exemplar of what a byte-grounded refutation looks like. Record the direction consequence for the downstream lanes (spot wave + postcheck sampling posture). NO reweighting of any adjudicated row."),
    ("b4", "B4-1", "span_proposal", ["P18-006"],
     "Rule the Jer.49.19|Jer.49.20 cut question (peer: any change to the span, including adopting that cut, is a PROPOSAL for adoption). ADOPT with exact spec, or DECLINE. Note the cross-lens factual tension the primaries recorded over what pmarks carries at 49:19 - arbitrate against the inventory bytes."),
    ("b4", "B4-2", "span_proposal", ["P18-009"],
     "Rule the respan PROPOSAL with TWO options: (i) Jer.49.28-Jer.49.33 entire, or (ii) a cut at Jer.49.29|Jer.49.30 where the discriminators actually sit. ADOPT exactly one option with full spec + tiling, or DECLINE both."),
    ("b4", "B4-3", "span_proposal", ["P18-026"],
     "Rule the PROPOSAL: respan Jer.50.33-Jer.50.38 as one koh-amar-headed unit, absorbing this row into the one before it, as against keeping the cut with the ordered disclosures. ADOPT with exact spec + retirement + tiling, or DECLINE."),
    ("b4", "B4-4", "span_proposal", ["P19-006"],
     "Rule the 51:26|51:27 seam itself (peer: PROPOSAL requiring explicit adoption, NOT author work). ADOPT an exact change, or DECLINE."),
    ("b4", "B4-5", "span_proposal", ["P20-002"],
     "Rule the proposed cut at 52:6 (peer: boundary proposal requiring explicit adoption). ADOPT with exact spec, or DECLINE."),
    ("b4", "B4-6", "cwo_policy", ["P09-002"],
     "CWO-5 POLICY RULING (boss-decidable; census direction (c)): the signal-field contract does not say whether a declared closure key may name a device outside the unit's own span. Ten units declare the closure key; six end on a verse carrying none of the book's 162 neum tokens. Enumerate the declaring rows deterministically from the frozen corpus (sweep observed_substrate_signals for the closure-classed key), then rule ONE scope policy: (i) a closure key must be attested in the unit's own span (bind-or-drop, per the P09-002 cure shape), or (ii) qualified out-of-span closure keys are permitted with mandatory disclosure. Name the policy, the exact consequence rows, and the cure test each must pass."),
    ("b4", "B4-7", "escalation_record", [],
     "ZERO-ESCALATION RECORD (census direction (b)): 0 escalations in 216 peer rulings - no owner-policy question was contested (Hananiah frame-ownership, neum-closure precedence, Babylon stanza policy, the held-open 27:1 crux all stayed inside the ruled granularity). Verify from the docket totals (embedded) and record whether any span item YOU ruled this round actually required owner-law reinterpretation (if one did, that item itself carries the owner_escalation - this record then notes it)."),
    ("b4", "B4-8", "tier0_coverage", [],
     "TIER-0 COVERAGE VERIFICATION (census direction (d)): the Isa-lineage deterministic boss sweeps (B-6 whole-chapter cap, B-7 NFD) are already Tier-0 members of the Jer suite. VERIFY coverage rather than re-running models: run tools/cap_sweep.py and tools/normalize_hebrew_in_json.py --dry-run over the frozen draft_rows_combined.jsonl, read the COUNTS (not the status line), and record them. If either sweep surfaces a violation the writer gate missed, enumerate the rows as author work orders."),
]

agents = {}
for a, iid, kind, rids, q in ITEMS:
    agents.setdefault(a, []).append((iid, kind, rids, q))
assert [len(v) for k, v in sorted(agents.items())] == [6, 7, 6, 8], "slice shape"
assert sum(len(v) for v in agents.values()) == 27, "item count"

def row_pack(rid):
    r = by_id[rid]
    idx = r["chunk_index_in_book"]
    pack = {"row": r}
    if idx - 1 in by_idx:
        pack["prev_row"] = by_idx[idx - 1]
    if idx + 1 in by_idx:
        pack["next_row"] = by_idx[idx + 1]
    return pack

master = {"schema": "jer_boss_docket.v1",
          "built_from": "remedy_docket.v1.json + draft_rows_combined.jsonl",
          "items_total": 27, "agents": {}}
for a in sorted(agents):
    items = []
    for iid, kind, rids, q in agents[a]:
        it = {"item_id": iid, "kind": kind, "row_ids": rids, "question": q,
              "docket_entries": {}, "rows": {}}
        for rid in rids:
            if kind == "sample_defect_ratification":
                # both-support row: lives in sample_lane_defects, not the
                # challenged-row docket
                pass
            else:
                assert rid in dk, f"{rid} not in remedy docket"
                it["docket_entries"][rid] = dk[rid]
            assert rid in by_id, f"{rid} not in corpus"
            it["rows"][rid] = row_pack(rid)
        if kind == "calibration_record":
            it["refuted_exemplar"] = d["refuted"][0]
            it["totals"] = d["totals"]
        if kind == "sample_defect_ratification":
            it["sample_lane_defect"] = d["sample_lane_defects"][0]
        if kind == "cwo_policy":
            it["cwo"] = d["corpus_wide_orders"][4]
            assert it["cwo"]["id"] == "CWO-5"
        if kind == "escalation_record":
            it["totals"] = d["totals"]
        items.append(it)
    slice_doc = {"schema": "jer_boss_docket_slice.v1", "agent": a,
                 "attempt_id": f"jer_boss_{a}_a1",
                 "output_file": f"reviews/boss_jer_{a}.json",
                 "items": items}
    out = HERE / f"boss_docket_{a}.json"
    json.dump(slice_doc, open(out, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    master["agents"][a] = {"attempt_id": slice_doc["attempt_id"],
                           "output_file": slice_doc["output_file"],
                           "item_ids": [i["item_id"] for i in items],
                           "row_ids": sorted({r for i in items for r in i["row_ids"]})}
json.dump(master, open(HERE / "boss_docket.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(json.dumps(master, indent=1))
