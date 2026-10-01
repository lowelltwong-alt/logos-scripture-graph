"""Isaiah book close: assemble rows_v3 into the M8 worktree, append sidecars +
whole-Bible map, write the completion receipt, and mark-complete -> Jer.

Gated: refuses to run unless reviews/postcheck_isa.json says fit_to_assemble and
both sidecar_src files validate against the low-band row set. Run from SP/Isa.
Usage: python tools/_close_book.py <usage_tokens_json>  (a JSON string with the
measured wave budgets to embed in the receipt).
"""
import collections, hashlib, json, re, sys
from pathlib import Path

SP = Path(__file__).resolve().parent.parent
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
if len(sys.argv) > 1 and sys.argv[1].startswith("@"):
    usage = json.load(open(sys.argv[1][1:], encoding="utf-8"))
elif len(sys.argv) > 1:
    usage = json.loads(sys.argv[1])
else:
    usage = {}

# --- gates ---
post = json.load(open(SP / "reviews/postcheck_isa.json", encoding="utf-8"))
assert post.get("verdict") == "fit_to_assemble", f"postcheck verdict: {post.get('verdict')}"
assert not post.get("blocking_findings"), post["blocking_findings"]

rows = [json.loads(l) for l in open(SP / "rows_v3.jsonl", encoding="utf-8")]
assert len(rows) == 223
low_ids = {r["writer_decision_id"] for r in rows if r["confidence"] in ("medium_low", "low")}
side = []
for f in ("sidecar_src_1.jsonl", "sidecar_src_2.jsonl"):
    side += [json.loads(l) for l in open(SP / f, encoding="utf-8")]
side_ids = [s["writer_decision_id"] for s in side]
assert len(side_ids) == len(set(side_ids)), "duplicate sidecar rows"
assert set(side_ids) == low_ids, f"sidecar set mismatch: missing {sorted(low_ids-set(side_ids))} extra {sorted(set(side_ids)-low_ids)}"
for s in side:
    for k in ("concern_type", "why_low_confidence", "why_frontier_review_needed",
              "possible_downstream_risk", "suggested_reviewer", "proposed_atlas_action"):
        assert s.get(k), f"sidecar {s['writer_decision_id']} missing {k}"
texts = [s["why_low_confidence"] for s in side]
assert len(texts) == len(set(texts)), "boilerplate: duplicated why_low_confidence text"

# --- frame non-straddle re-check + final ids ---
FRAME_STARTS = sorted({(1, 1), (1, 2), (13, 1), (28, 1), (36, 1), (40, 1), (49, 1), (56, 1)})
def sspan(r):
    m = re.match(r"^Isa\.(\d+)\.(\d+)-Isa\.(\d+)\.(\d+)$", r["span"])
    return (int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))
final = []
for i, r in enumerate(rows, 1):
    s, e = sspan(r)
    assert max(b for b in FRAME_STARTS if b <= s) == max(b for b in FRAME_STARTS if b <= e), r["span"]
    assert r["chunk_index_in_book"] == i
    fr = dict(r)
    fr["decision_id"] = f"M8-Isa-{i:03d}"
    final.append(fr)
by_wid = {r["writer_decision_id"]: r for r in final}

# --- write chunks.jsonl (worktree) + sha verify ---
outdir = M8 / "book_chunks" / "Isa"
outdir.mkdir(parents=True, exist_ok=True)
chunk_path = outdir / "chunks.jsonl"
payload = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in final)
chunk_path.write_text(payload, encoding="utf-8", newline="\n")
sha_chunks = hashlib.sha256(chunk_path.read_bytes()).hexdigest()
assert [json.loads(l)["decision_id"] for l in chunk_path.read_text(encoding="utf-8").splitlines()] \
    == [f"M8-Isa-{i:03d}" for i in range(1, 224)]

# --- sidecar appends (chunk order) ---
side_by_id = {s["writer_decision_id"]: s for s in side}
lcr, feq, acf = [], [], []
for r in final:
    wid = r["writer_decision_id"]
    if wid not in side_by_id:
        continue
    s = side_by_id[wid]
    common = {"model_id": "M8_fable", "book": "Isa", "span": r["span"],
              "chunk_decision_id": r["decision_id"], "confidence": r["confidence"],
              "review_packet_final_state": "accepted_candidate",
              "chunk_review_status": "candidate_review_complete",
              "candidate_hold_state": None, "non_authorizing": True,
              "observed_substrate_signals": r["observed_substrate_signals"]}
    lcr.append({**common, "why_low_confidence": s["why_low_confidence"]})
    feq.append({**common, "concern_type": s["concern_type"],
                "why_frontier_review_needed": s["why_frontier_review_needed"]})
    acf.append({**common, "concern_type": s["concern_type"],
                "why_low_confidence": s["why_low_confidence"]})
for name, out in (("low_confidence_register.jsonl", lcr),
                  ("frontier_escalation_queue.jsonl", feq),
                  ("atlas_candidate_feed.jsonl", acf)):
    p = M8 / name
    existing = p.read_text(encoding="utf-8")
    assert '"book": "Isa"' not in existing, f"{name} already has Isa rows"
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        for row in out:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

# --- whole_bible_chunk_map append ---
map_path = M8 / "whole_bible_chunk_map.jsonl"
existing = map_path.read_text(encoding="utf-8")
assert '"book": "Isa"' not in existing, "map already has Isa rows"
with map_path.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(payload)

# --- receipt ---
conf = collections.Counter(r["confidence"] for r in final)
ut = collections.Counter(r["unit_type"] for r in final)
receipt = {
    "book": "Isa", "model_id": "M8_fable", "mesh_revision": "m8-mesh-r3",
    "rows": 223, "chunks": 223,
    "parents": sorted({r["parent_collection"] for r in final}),
    "verses_covered": 1292,
    "chunk_file_sha256": sha_chunks,
    "rows_v3_sha256": hashlib.sha256((SP / "rows_v3.jsonl").read_bytes()).hexdigest(),
    "confidence_final": dict(conf.most_common()),
    "unit_type_distribution": dict(ut.most_common()),
    "numbering_disclosure": ("NOT an identity book - TWO offset zones with different shapes, "
        "byte-proven: ZONE A renumbering (MT 8:23 = WEB 9:1; MT 9:1-20 = WEB 9:2-21); "
        "ZONE B split (MT 63:19 spans WEB 63:19 + WEB 64:1; MT 64:1-11 = WEB 64:2-12; "
        "WEB 1292 vs MT 1291). Tier-0 dual-cite rule enforced corpus-wide; web_to_mt "
        "deterministic, mt_to_web_all authoritative at the split."),
    "voice_attribution_disclosure": ("Held classics undecided throughout: the servant referent "
        "(every servant_song and named-referent row), the 7:14 almah construal, the MT 9:5-6 "
        "throne-names referent, the 40:1-11 herald voices, the 61:1-3 anointed speaker, and "
        "the 66:23-24 coda-vs-close question. Chunking rows never decide them."),
    "waves": {"writers": "18 parts / 225 draft rows / suite hard-GREEN",
              "primaries": "29 clusters x dual-blind LF+OL = 58 packets, 450 verdicts, census GREEN",
              "peer": "15 peers / 202 rulings = 124 uphold / 76 refine / 2 refute / 0 escalate",
              "boss": "boss_isa_r1: 8/8 ruled, 3 adopted changes (B-2 respan, B-3 + B-5 merges -> 223 rows), 5 cures, 0 owner escalations",
              "author": "14 agents / 30 attempts / 200 orders (198 replace + 2 retire), census GREEN",
              "rev_round": "validator suite (hard-GREEN) + 6-lane spot wave (seams clean, zones clean, 2nd-gen 19 findings, B-8 audit)",
              "micro": "5 agents / 51 row-edits + deterministic systemic pass (74 Hebrew-quote fixes, 150 ref re-prefixes, 1 staged-name strike)",
              "postcheck": "validator suite + one model postcheck agent: fit_to_assemble"},
    "defect_ledger_totals": {
        "error_pattern_classes": "E-01..E-17 + B8-RECORD (ERROR_PATTERN_LEDGER.v1.md / error_pattern_ledger.v1.jsonl)",
        "kills_campaign_isa": "31 lifetime, ZERO work lost (E-13 api-filter-misfire 7, E-14 connection/stall/orchestrator-exit 24 incl. two 5-agent clusters)",
        "credited_errata": "peer-ledger prose errors caught by authors (P05-011 token, P07-001 class, inventory yeshayahu digit); boss docket enumeration corrections (cap 6->12, NFD 11->13)",
        "b8_lf_support_audit": ("sample n=31 of frame 155 (20.0%): defect-any 19/31 = 61.3%; "
            "LF-attributable ~12/31 = 38.7% incl. 1 high (tier-4 punctuation driving a boundary, "
            "pre-merge P09-003); second-generation ~7/31 = 22.6%. The LF-support audit lane runs "
            "by default in future books.")},
    "full_mesh_disclosure": ("Anthropic-family mesh (sonnet writers/authors/micro + LF primaries; "
        "opus OL primaries/peers/boss/spot-verify/postcheck; haiku sidecar authoring; fable "
        "orchestrator). Intra-mesh agreement is corroboration, never cross-provider evidence."),
    "tool_patches": ("i1 letter-name whitelist; i2 koh-amar classifier rebuild (divine 44 / royal 4); "
        "i3 qadosh defective-spelling inventory (25 sites); i4 ngram7 fixed-value exclusions; "
        "deterministic passes: NFC normalize (B-7, fixed=0 end-state), micro systemic (quote/register/ref-prefix). "
        "Owner items for future books: nfd_degraded->hard, Tier-0 cap gate, unclosed-quote detector (E-15), "
        "universals dampener patch (E-16)."),
    "usage_measured_subagent_tokens": usage,
    "non_authorizing": True,
}
rec_path = M8 / "receipts" / "Isa_completion.json"
rec_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")

# --- mark complete -> Jer ---
prog_path = M8 / "marathon_progress.yaml"
prog = prog_path.read_text(encoding="utf-8")
assert "books_completed: 22" in prog
assert re.search(r"  Isa:\n    status: in_progress", prog)
prog = prog.replace("books_completed: 22", "books_completed: 23")
prog = prog.replace("  Isa:\n    status: in_progress", "  Isa:\n    status: complete")
prog = re.sub(r"current_book: Isa\b", "current_book: Jer", prog)
prog_path.write_text(prog, encoding="utf-8", newline="\n")
man_path = M8 / "model_manifest.yaml"
man = man_path.read_text(encoding="utf-8")
man = man.replace("books_completed: 22", "books_completed: 23").replace("current_book: Isa", "current_book: Jer")
man_path.write_text(man, encoding="utf-8", newline="\n")

print(json.dumps({"status": "CLOSED", "chunks": 223, "chunk_sha256_16": sha_chunks[:16],
                  "sidecar_rows_appended": len(lcr), "map_appended": 223,
                  "receipt": str(rec_path), "progress": "Isa complete -> Jer (23/66)"}, indent=1))
