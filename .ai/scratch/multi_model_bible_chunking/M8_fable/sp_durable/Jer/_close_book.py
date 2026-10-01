"""Jeremiah book close (adapted from the Isa close): gated on the postcheck verdict fit_to_assemble + validated sidecars;
assembles rows_v5 into book_chunks/Jer/chunks.jsonl with ids M8-Jer-NNN, appends the three sidecars + the whole-Bible map,
writes receipts/Jer_completion.json carrying the CAMPAIGN_CLOSE_GATE item-5/6/8 evidence block (CWO execution parity
digits; Hebrew quote bytes + tier labels; WEB quote/gloss fidelity; normalization counts; review-packet retention with
hashes; appeals; final review_status; role separation; B-8 + E-23 digits), and marks complete -> Lam. Run from SP/Jer.
Usage: python _close_book.py @usage.json"""
import collections, glob, hashlib, json, re, sys
from pathlib import Path
SP = Path(__file__).resolve().parent
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
usage = json.load(open(sys.argv[1][1:], encoding="utf-8")) if len(sys.argv) > 1 and sys.argv[1].startswith("@") else {}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
# --- gates ---
CORPUS = sys.argv[sys.argv.index("--corpus") + 1] if "--corpus" in sys.argv else "rows_v5.jsonl"
POSTCHECK = sys.argv[sys.argv.index("--postcheck") + 1] if "--postcheck" in sys.argv else "postcheck_01.json"
post = json.load(open(SP / "postcheck" / POSTCHECK, encoding="utf-8-sig"))
assert post.get("verdict") == "fit_to_assemble", f"postcheck verdict: {post.get('verdict')}"
assert not [r for r in post.get("residual", []) if r.get("severity") in ("high", "medium")], "medium/high residuals in the postcheck"
rows = [json.loads(l) for l in open(SP / CORPUS, encoding="utf-8") if l.strip()]
assert len(rows) == 275 and all(r["review_status"] == "candidate_review_complete" for r in rows)
low_ids = {r["writer_decision_id"] for r in rows if r["confidence"] in ("medium_low", "low")}
side = []
for f in sorted(SP.glob("sidecar_src_*.jsonl")):
    side += [json.loads(l) for l in open(f, encoding="utf-8-sig") if l.strip()]
side_ids = [s["writer_decision_id"] for s in side]
assert len(side_ids) == len(set(side_ids)), "duplicate sidecar rows"
assert set(side_ids) == low_ids, f"sidecar set mismatch: missing {sorted(low_ids-set(side_ids))} extra {sorted(set(side_ids)-low_ids)}"
for s in side:
    for k in ("concern_type", "why_low_confidence", "why_frontier_review_needed", "possible_downstream_risk", "suggested_reviewer", "proposed_atlas_action"):
        assert s.get(k), f"sidecar {s['writer_decision_id']} missing {k}"
texts = [s["why_low_confidence"] for s in side]; assert len(texts) == len(set(texts)), "boilerplate: duplicated why_low_confidence text"
suite = json.load(open(SP / (CORPUS + ".validator_report.json"), encoding="utf-8-sig"))
assert suite["summary"]["hard_status"] == "GREEN" and not suite["summary"]["nfd_hard_e01"]
norm = suite["hebrew_normalize_dryrun"]; assert norm.get("fixed", 0) == 0 and norm.get("defect_count", 0) == 0
parity = json.load(open(SP / "cwo" / "cwo_parity.v1.json", encoding="utf-8"))
assert not parity["exact_arm_residual"]
# --- frame non-straddle re-check + final ids ---
FRAME_STARTS = sorted({(1, 1), (1, 4), (7, 1), (11, 1), (18, 1), (21, 1), (25, 1), (30, 1), (34, 1), (40, 1), (46, 1), (52, 1)})
def sspan(r):
    m = re.match(r"^Jer\.(\d+)\.(\d+)-Jer\.(\d+)\.(\d+)$", r["span"]); return (int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))
final = []
for i, r in enumerate(rows, 1):
    s, e = sspan(r)
    assert max(b for b in FRAME_STARTS if b <= s) == max(b for b in FRAME_STARTS if b <= e), r["span"]
    assert r["chunk_index_in_book"] == i
    fr = dict(r); fr["decision_id"] = f"M8-Jer-{i:03d}"; final.append(fr)
# --- write chunks.jsonl ---
outdir = M8 / "book_chunks" / "Jer"; outdir.mkdir(parents=True, exist_ok=True)
chunk_path = outdir / "chunks.jsonl"
assert not chunk_path.exists(), "book_chunks/Jer/chunks.jsonl already exists"
payload = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in final)
chunk_path.write_text(payload, encoding="utf-8", newline="\n"); sha_chunks = sha(chunk_path)
assert [json.loads(l)["decision_id"] for l in chunk_path.read_text(encoding="utf-8").splitlines()] == [f"M8-Jer-{i:03d}" for i in range(1, 276)]
# --- sidecars ---
side_by_id = {s["writer_decision_id"]: s for s in side}; lcr, feq, acf = [], [], []
for r in final:
    wid = r["writer_decision_id"]
    if wid not in side_by_id: continue
    s = side_by_id[wid]
    common = {"model_id": "M8_fable", "book": "Jer", "span": r["span"], "chunk_decision_id": r["decision_id"], "confidence": r["confidence"],
              "review_packet_final_state": "accepted_candidate", "chunk_review_status": "candidate_review_complete", "candidate_hold_state": None,
              "non_authorizing": True, "observed_substrate_signals": r["observed_substrate_signals"]}
    lcr.append({**common, "why_low_confidence": s["why_low_confidence"]})
    feq.append({**common, "concern_type": s["concern_type"], "why_frontier_review_needed": s["why_frontier_review_needed"]})
    acf.append({**common, "concern_type": s["concern_type"], "why_low_confidence": s["why_low_confidence"]})
for name, out in (("low_confidence_register.jsonl", lcr), ("frontier_escalation_queue.jsonl", feq), ("atlas_candidate_feed.jsonl", acf)):
    p = M8 / name; existing = p.read_text(encoding="utf-8"); assert '"book": "Jer"' not in existing, f"{name} already has Jer rows"
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        for row in out: fh.write(json.dumps(row, ensure_ascii=False) + "\n")
map_path = M8 / "whole_bible_chunk_map.jsonl"; assert '"book": "Jer"' not in map_path.read_text(encoding="utf-8")
with map_path.open("a", encoding="utf-8", newline="\n") as fh: fh.write(payload)
# --- packet retention enumeration (durable copies) ---
D = M8 / "sp_durable" / "Jer"
ret = {}
for sub in ("writer", "reviews", "author", "cwo", "spot", "postcheck"):
    d = D / sub
    if d.is_dir():
        ret[sub] = {p.name: sha(p) for p in sorted(d.iterdir()) if p.is_file()}
for n in ("rows_v2.jsonl", "rows_v3.jsonl", "rows_v4.jsonl", "rows_v5.jsonl", "rows_v6.jsonl", "draft_rows_combined.jsonl", "cwo_orders.v1.json", "freeze/CYCLE_STATE.md"):
    if (D / n).is_file(): ret[n] = sha(D / n)
e23 = json.load(open(SP / "_e23_post.json", encoding="utf-8"))
b8 = {}
for sn in ("S5", "S6"):
    p = SP / "spot" / f"spot_{sn}.json"
    if p.is_file():
        d = json.load(open(p, encoding="utf-8-sig")); b8[sn] = {"lane_digits": d.get("lane_digits"), "findings": len(d.get("findings", [])), "clean": d.get("clean")}
conf = collections.Counter(r["confidence"] for r in final); ut = collections.Counter(r["unit_type"] for r in final)
receipt = {"book": "Jer", "model_id": "M8_fable", "mesh_revision": "m8-mesh-r3 + OW-1/OW-2/OW-3/OW-4/OW-5 + OWNER_REPAIR_ADVANCE_2026-09-06",
    "rows": 275, "chunks": 275, "parents": sorted({r["parent_collection"] for r in final}), "verses_covered": 1364,
    "chunk_file_sha256": sha_chunks, "final_corpus": CORPUS, "final_corpus_sha256": sha(SP / CORPUS), "rows_v5_sha256": sha(SP / "rows_v5.jsonl"), "rows_v3_sha256": sha(SP / "rows_v3.jsonl"), "rows_v2_sha256": sha(SP / "rows_v2.jsonl"),
    "confidence_final": dict(conf.most_common()), "unit_type_distribution": dict(ut.most_common()),
    "numbering_disclosure": "NOT an identity book - EXACTLY ONE offset zone, pure renumbering, NO split, byte-proven: MT 8:23 = WEB 9:1; MT 9:1-25 = WEB 9:2-26; every other chapter identity; WEB 1364 / MT 1364. Tier-0 one-zone dual-cite rule enforced corpus-wide; injective crosswalk. The single Aramaic verse MT 10:11 = WEB 10:11 disclosed on every row over it.",
    "voice_attribution_disclosure": "Held classics undecided throughout: the 27:1 defective-Jehoiakim setting crux; the confessions' speaker-frame edges (incl. 8:18-9:1 in the zone and 10:23-25); the 25:13 hinge and the cup-oracle scope; the 30-33 consolation core's internal seams; 33:14-26 LXX-absent as metadata only; the 39:4-13 overlap with ch 52; the OAN stanza seams in 50-51; the ch-25 pivot to the nations. Chunking rows never decide them.",
    "waves": usage.get("waves", {}),
    "campaign_close_gate_evidence": {
        "item5_cwo_execution_parity": {"record": "sp_durable/Jer/cwo/cwo_parity.v1.json", "sha256": sha(SP / "cwo" / "cwo_parity.v1.json"), "parity": {k: {"arm": v["arm"], "ordered_rows": v["ordered_rows"], "post_wave_candidates": v["post_wave_candidates"]} for k, v in parity["parity"].items()}, "exact_arm_residual": parity["exact_arm_residual"]},
        "item5_hebrew_quote_bytes_and_tier_labels": {"citation_sweep_status": suite["citation_sweep"].get("status"), "problems": len(suite["citation_sweep"].get("problems", [])), "nfd_degraded_count": suite["citation_sweep"].get("nfd_degraded_count"), "rows": suite["citation_sweep"].get("rows")},
        "item5_web_quote_gloss_fidelity": {"web_quotes_status": suite["web_quotes"].get("status"), "flag_count": suite["web_quotes"].get("flag_count"), "note": "FLAGS dispositioned by the spot wave (declared-FP classes or cured in the micro round); the postcheck re-verified the cured rows"},
        "item5_unicode_normalization": {"ok": norm.get("ok"), "fixed": norm.get("fixed"), "defect_count": norm.get("defect_count"), "count_read_not_status_line": True},
        "item5_review_packet_retention": {"durable_root": "sp_durable/Jer", "enumerated_with_sha256": ret},
        "item5_appeals": {"append_only_appeal_state": "no appeal filed during the Jeremiah cycle; none held", "enumerated": []},
        "item5_final_review_status": {"candidate_review_complete": sum(1 for r in final if r["review_status"] == "candidate_review_complete"), "draft": sum(1 for r in final if r["review_status"] == "draft"), "deferred_labels": []},
        "item5_second_generation_role_separation": "every repair wave (author waves 1-3, CWO wave + correction + systemic layer, micro round) was followed by a fresh full sweep by _wave_repair_sweep.py / the validator suite (deterministic, distinct from the authors) and by model review distinct from the producers (spot wave; postcheck); producer/catcher roles recorded per attempt in the item-6 receipts",
        "item4_prospective_e23": {"rows_checked": e23.get("rows_checked"), "flag_count": e23.get("flag_count"), "rows": sorted({f.get("decision_id") for f in e23.get("flags", [])}), "lane": "spot S7 dispositioned every flag (driver vs defensive mention)"},
        "item1_b8_lf_support_audit": {"frame": "rows LF verdict=support, retired dropped: 194", "sample": "every 5th of the id-sorted frame: 39", "lanes": b8},
        "item8_ow3": "audit != repair; proposals validated adversarially; both-sides seam law; dependency-applicability records v1-v5; honest effort reporting (ordered, not verified); pre-feedback baseline preserved (rows_v2 / rows_v3 hashes above)"},
    "defect_ledger_totals": usage.get("defect_ledger_totals", {}), "full_mesh_disclosure": "Anthropic-family mesh (sonnet writers/authors/CWO/micro + LF primaries; opus OL primaries/peers/boss/spot/postcheck; haiku sidecar authoring; fable orchestrator). Intra-mesh agreement is corroboration, never cross-provider evidence.",
    "tool_patches": usage.get("tool_patches", ""), "usage_measured_subagent_tokens": usage.get("tokens", {}), "non_authorizing": True}
rec_path = M8 / "receipts" / "Jer_completion.json"; assert not rec_path.exists()
rec_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
# --- mark complete -> Lam ---
prog_path = M8 / "marathon_progress.yaml"; prog = prog_path.read_text(encoding="utf-8")
assert "books_completed: 23" in prog and "current_book: Jer" in prog
prog = prog.replace("books_completed: 23", "books_completed: 24"); prog = re.sub(r"current_book: Jer\b", "current_book: Lam", prog)
if re.search(r"  Jer:\n    status: in_progress", prog): prog = prog.replace("  Jer:\n    status: in_progress", "  Jer:\n    status: complete")
prog_path.write_text(prog, encoding="utf-8", newline="\n")
man_path = M8 / "model_manifest.yaml"; man = man_path.read_text(encoding="utf-8")
man = man.replace("books_completed: 23", "books_completed: 24").replace("current_book: Jer", "current_book: Lam"); man_path.write_text(man, encoding="utf-8", newline="\n")
print(json.dumps({"status": "CLOSED", "chunks": 275, "chunk_sha256_16": sha_chunks[:16], "sidecar_rows_appended": len(lcr), "map_appended": 275, "receipt": str(rec_path), "progress": "Jer complete -> Lam (24/66)"}, indent=1))
