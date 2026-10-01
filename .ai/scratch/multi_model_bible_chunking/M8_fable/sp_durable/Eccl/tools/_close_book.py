#!/usr/bin/env python3
"""Orchestrator book-close for Eccl (owner-scoped allowlisted lane writes):
renumber+freeze, sidecars (19 rows x3, full schemas per lesson e), worktree
installs (book_chunks, whole map append, receipts, sidecar appends),
manifest advance to 21/66 current_book Song. Deterministic; every install
sha/count-verified."""
import hashlib
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path
from collections import Counter

SPBOOK = Path(__file__).resolve().parent.parent
WT = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def wjsonl(p, rows):
    with p.open("w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

# 1. renumber + deliverable
rows = [json.loads(l) for l in (SPBOOK / "rows_v3.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
assert len(rows) == 86
for i, r in enumerate(rows, 1):
    r["decision_id"] = f"M8-Eccl-{i:03d}"
    r["chunk_index_in_book"] = i
deliv = SPBOOK / "deliverables"; deliv.mkdir(exist_ok=True)
chunks = deliv / "chunks.jsonl"
wjsonl(chunks, rows)
chunks_sha = sha(chunks)
rows_v3_sha = sha(SPBOOK / "rows_v3.jsonl")

# 2. freeze
frz = SPBOOK / "freeze"
wjsonl(frz / "rows_v3_frozen.jsonl", [json.loads(l) for l in (SPBOOK / "rows_v3.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()])
(frz / "FREEZE_RECORD.json").write_text(json.dumps({
    "book": "Eccl", "frozen": "2026-08-20", "rows": 86,
    "chunks_sha256": chunks_sha, "rows_v3_sha256": rows_v3_sha,
    "lineage": "draft(85) -> rows_v1(66 phase-1 cures) -> rows_v2(boss B-1..B-5: -4 retired +5 added = 86) -> rows_v3(19 micro-fix cures + oss normalization)"},
    indent=1), encoding="utf-8", newline="\n")

# 3. sidecars — 19 low-band rows (postcheck census), bespoke text
by_wid = {r["writer_decision_id"]: r for r in rows}
LOWBAND = [
 ("P01-007", "asyndetic-break cohesion inside an eight-verse quest accumulation",
  "whether the genuine asyndetic clause break at web:Eccl.2.4 warrants splitting the lexically-bound royal-projects unit",
  "retrieval over a wide span may surface project-list verses without their governing first-person frame"),
 ("P01-016", "unresolved rhetorical-question close",
  "the unit closes on a genuinely unanswered who-knows question at web:Eccl.3.21, unlike the resolved parallel at 2:19; the seam with 3:22 depends on how the question functions",
  "mortality-argument queries may need the 3:22 resolution verse alongside this span"),
 ("P01-023", "unit_type deviation argued from form",
  "wisdom_poem applied against the parent monologue default on formal grounds (no first-person verb; numeric progression); classification is contestable",
  "type-filtered retrieval may mis-bucket the companionship poem"),
 ("P01-024", "unresolved two-youths referents",
  "the youth and successor figures are a genuine scholarly crux left unidentified rather than resolved by conjecture",
  "entity-linking or figure-tracking layers must not treat any identification as settled"),
 ("p02-003", "ketiv/qere construal crux in the offset zone",
  "MT 5:8 (= WEB 5:9) is a live syntax-construal dispute compounded by a K/Q note; WEB's rendering already picks one side",
  "translation-dependent readings diverge; dual-cite discipline required downstream"),
 ("p02-004", "compressed clause plus ketiv/qere",
  "the pair's second verse (MT 5:10 = WEB 5:11) carries a K/Q note inside an already compressed clause",
  "quotation or paraphrase layers may inherit the construal choice silently"),
 ("p02-013", "boss-capped cluster with skeleton-tier driver",
  "the bet-avel bracket cohesion driver collates at skeleton tier only (prefixed form at one end) and adjacent-pair cohesion is thin; cluster stands under the tier-disclosure standard (boss B-1/B-4)",
  "cluster granularity is the convergence-sensitive judgment; an atomic re-cut remains a defensible rival"),
 ("p02-019", "thin cluster driver (grammatical dependency)",
  "the saying_cluster rests on a causal-clause dependency rather than a repeated phrase — a thinner-than-typical driver, disclosed",
  "same class as the other tier-disclosed clusters; convergence should weigh the driver kind"),
 ("p02-020", "operative-category deviation in the sentence zone",
  "admonition_unit applied inside the single_saying-default zone on an imperative-frame warrant (operative-category law)",
  "zone-based sampling must not assume the default type here"),
 ("p02-023", "zone-edge form deviation",
  "single_saying applied one verse outside the designated sentence zone, argued from bare aphoristic form",
  "zone-boundary heuristics will miscount this row"),
 ("p02-026", "feminine amar-qohelet + one-among-a-thousand crux",
  "the 7:27 frame verb is pointed feminine against the expected masculine (byte-fact) and 7:28's one-among-a-thousand line is genuinely unresolved; bounded on a find-root chain",
  "theological or anthropological downstream readings of 7:28 must not inherit a settled construal"),
 ("P03-005", "arguable closing seam with disclosed catchword bridge",
  "the 9:16|9:17 seam is genuinely arguable; a catchword bridge into v.17 is disclosed as a live counter-reading",
  "adjacent-unit retrieval should co-surface 9:17 when this span is hit"),
 ("P03-015", "boss-confirmed cluster with accent-stripped one-directional driver",
  "the shared lexeme collates at accent-stripped tier only and in one direction; cluster confirmed under the tier-disclosure standard (boss B-4)",
  "cluster granularity is convergence-sensitive"),
 ("P03-016", "cluster phrase at accent-stripped tier",
  "the cohesion phrase collates at accent-stripped tier, not byte-identical; disclosed per the standard",
  "same convergence class"),
 ("P03-017", "continuation-fold hazard verse",
  "held chiefly for the WEB continuation-paragraph fold at this verse (quotation hazard), not for the boundary call",
  "any WEB quotation layer must use the folded verse text verbatim"),
 ("P03-B3", "boss-merged span containing the bread-on-waters crux",
  "one admonition_unit over 11:1-6 by boss adoption (B-3); the span contains the long-disputed bread-on-waters referent (commerce vs charity), disclosed not resolved",
  "wide-span retrieval and the unresolved referent compound; convergence should re-examine the merger"),
 ("P03-025", "live alternative seam at a person shift",
  "a disclosed live alternative seam at the third-to-second-person register shift between 11:8 and 11:9",
  "units on either side of the shift may be re-cut at convergence"),
 ("P03-026", "disputed aging-imagery lexemes + ketiv/qere",
  "vv. 4-6 carry uncommon, genuinely disputed figurative lexemes compounded by the K/Q crux at 12:6 (two distinct roots)",
  "imagery interpretation layers must not inherit one figurative mapping as settled"),
 ("P03-028", "one-shepherd referent crux",
  "the referent of the one shepherd (12:11) is a long-disputed crux, disclosed honestly rather than resolved",
  "theological attribution downstream must treat the referent as open"),
]
assert len(LOWBAND) == 19
base_states = {"review_packet_final_state": "accepted_candidate",
               "chunk_review_status": "candidate_review_complete",
               "candidate_hold_state": None, "non_authorizing": True}
lc, fq, ac = [], [], []
for wid, concern, why, risk in LOWBAND:
    r = by_wid[wid]
    assert r["confidence"] in ("medium_low", "low"), f"{wid} not low-band: {r['confidence']}"
    core = {"model_id": "M8_fable", "book": "Eccl", "span": r["span"],
            "chunk_decision_id": r["decision_id"], "confidence": r["confidence"],
            **base_states, "observed_substrate_signals": r["observed_substrate_signals"]}
    lc.append({**core, "why_low_confidence": why})
    fq.append({**core, "concern_type": concern,
               "why_frontier_review_needed": why,
               "suggested_reviewer": "convergence", "promotion_authority": "none"})
    ac.append({**core, "concern_type": concern, "why_low_confidence": why,
               "possible_downstream_risk": risk,
               "suggested_reviewer": "convergence",
               "proposed_atlas_action": "consider_only",
               "atlas_promotion_authority": "none"})
lowband_ids = {w for w, *_ in LOWBAND}
actual_lowband = {r["writer_decision_id"] for r in rows if r["confidence"] in ("medium_low", "low")}
assert lowband_ids == actual_lowband, f"low-band roster mismatch: {sorted(actual_lowband ^ lowband_ids)}"
wjsonl(deliv / "low_confidence_register_rows.jsonl", lc)
wjsonl(deliv / "frontier_escalation_queue_rows.jsonl", fq)
wjsonl(deliv / "atlas_candidate_feed_rows.jsonl", ac)

# 4. worktree installs
(WT / "book_chunks" / "Eccl").mkdir(exist_ok=True)
tgt = WT / "book_chunks" / "Eccl" / "chunks.jsonl"
tgt.write_bytes(chunks.read_bytes())
assert sha(tgt) == chunks_sha, "sha mismatch after book_chunks install"

wm = WT / "whole_bible_chunk_map.jsonl"
before = len([l for l in wm.read_text(encoding="utf-8").splitlines() if l.strip()])
with wm.open("a", encoding="utf-8", newline="\n") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
after = len([l for l in wm.read_text(encoding="utf-8").splitlines() if l.strip()])
assert (before, after) == (3598, 3684), f"whole map count {before}->{after}"

for fname, data in (("low_confidence_register.jsonl", lc),
                    ("frontier_escalation_queue.jsonl", fq),
                    ("atlas_candidate_feed.jsonl", ac)):
    p = WT / fname
    n0 = len([l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()])
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        for r in data:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    n1 = len([l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()])
    assert n1 == n0 + 19, f"{fname} append {n0}->{n1}"

# 5. receipt
conf = Counter(r["confidence"] for r in rows)
ut = Counter(r["unit_type"] for r in rows)
receipt = {
    "book": "Eccl", "model_id": "M8_fable", "mesh_revision": "m8-mesh-r3-full",
    "rows": 86, "chunks": 86, "parents": {"F1": 3, "M": 80, "F2": 3},
    "verses_covered": "222/222",
    "chunk_file_sha256": chunks_sha, "rows_v3_sha256": rows_v3_sha,
    "confidence_final": {**dict(conf), "basis": "computed directly from rows_v3.jsonl (frozen); four rows carry boss-ordered medium_low caps (B-1, B-3 spec, B-4)"},
    "unit_type_distribution": dict(ut),
    "numbering_disclosure": {
        "status": "NOT identity (expected-identity REFUTED at Phase 0)",
        "crosswalk": "MT 4:17 = WEB 5:1; MT 5:1-19 = WEB 5:2-20; all other chapters identity; totals 222=222",
        "proof": "per-chapter counts under the rule set; 113 crosswalk content anchors (11 in the offset zone); identity-falsification probe (7 failures in ch 5); seam byte-review; OSHB KJV-variance layer EMPTY/inert for this book",
        "tier0_rule": "owner-ratified offset-zone dual-cite rule machine-enforced on every structured ref touching WEB ch 5 / MT 4:17-5:19"},
    "waves": {"writer": "3 parts (85 draft rows)",
              "primary": "22 packets (11 clusters x LF sonnet + OL opus, FULL dual-blind — no scoping)",
              "peer": "13 attempts (11 clusters + 3 follow-ons; 89 rulings)",
              "boss": "5 rulings / 3 adopted changes / 2 cures / 0 owner escalations (incl. the B-4 tier-disclosure standard)",
              "author": "3 phase-1 batches (84 orders) + 2 phase-2 batches (boss consequences) + 2 micro-fix batches (19 spot cures)",
              "spot": "6 lanes (26 findings) + 1 final postcheck agent (READY_TO_FREEZE, 0 blocking)"},
    "defect_ledger_totals": {
        "peer_wave": {"challenges_adjudicated": 102, "rulings": 89, "upheld": 77, "refined": 12, "refuted": 0, "escalated": 0},
        "boss": {"ruled": 5, "adopt_change": 3, "disclosure_cure": 2},
        "spot_wave": {"findings": 26, "all_cured": True}},
    "full_mesh_disclosure": {
        "policy": "owner-ruled 2026-08-19: FULL dual-blind primaries over all rows (no scoped mesh); cross-model decorrelation restored (LF sonnet / OL opus)",
        "untouched_audit_result": "all 12 mesh-support-only rows were 100% audited post-repair (not sampled): 0 boundary errors; texture/prose defects on 3 rows (25% row-rate), ALL cured in the micro-fix wave — no unreviewed population remains in this book",
        "residual_risk": "limited to defect classes no wave models: the 17 standing universals WARN flags were individually re-judged heuristic false positives at postcheck"},
    "tool_patches": {"inherited": "p1-p3 (Prov lineage)",
                     "p4": "ngram7 mandated-fixed-value field exclusion (wj_or_red_letter_considered, review_status) — rows_v1 rev-round finding, same class as p2",
                     "oss_normalization": "deterministic field-scoped strip-and-rename of staged-inventory filenames/stems to the dotted signal-key taxonomy (86 entries, 0 residual file refs; spot s5 census 62/86 rows)"},
    "usage_measured_subagent_tokens": {
        "writers": 1401000, "primaries": 3647000, "peers": 3107000,
        "boss": 400000, "authors_phase1": 1465000, "authors_phase2": 536000,
        "spot_wave": 1262000, "micro_fix": 493000, "postcheck": 222000,
        "total": 12533000,
        "note": "owner-authorized full finish (~11.6M estimate); measured overrun ~0.9M disclosed; environment absorbed 6 infrastructure kills with zero work loss (resume-in-place)"},
    "non_authorizing": True,
}
(WT / "receipts" / "Eccl_completion.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

# 6. manifest advance
mp = WT / "marathon_progress.yaml"
t = mp.read_text(encoding="utf-8")
assert "  Eccl:\n" not in t and "current_book: Eccl" in t and "books_completed: 20" in t
t = t.replace("books_completed: 20", "books_completed: 21", 1)
t = t.replace("current_book: Eccl", "current_book: Song", 1)
t = t.replace("  Prov:\n    status: complete\n", "  Prov:\n    status: complete\n  Eccl:\n    status: complete\n", 1)
mp.write_text(t, encoding="utf-8", newline="\n")

mm = WT / "model_manifest.yaml"
t2 = mm.read_text(encoding="utf-8")
assert "books_completed: 20" in t2 and "current_book: Eccl" in t2
t2 = t2.replace("books_completed: 20", "books_completed: 21", 1)
t2 = t2.replace("current_book: Eccl", "current_book: Song", 1)
mm.write_text(t2, encoding="utf-8", newline="\n")

print(json.dumps({"chunks_sha256": chunks_sha, "rows": 86,
                  "whole_map": f"{before}->{after}",
                  "sidecars_appended": 19,
                  "confidence": dict(conf), "unit_type": dict(ut),
                  "manifests": "advanced to 21/66, current_book Song",
                  "status": "INSTALLED"}, ensure_ascii=False, indent=1))
