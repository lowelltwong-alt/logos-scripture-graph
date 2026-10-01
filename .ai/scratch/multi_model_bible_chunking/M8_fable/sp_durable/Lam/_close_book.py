"""Lamentations book close (the Jer close re-keyed to Lam): gated on the postcheck verdict fit_to_assemble + validated
sidecars + the CWO parity record GREEN + the OW-6 claude-fable-5-1 final-checker verdict fit_to_close over the audited corpus
(with its stage-1 transcript-audit packets present and their high findings dispositioned); assembles the final corpus into book_chunks/Lam/chunks.jsonl with ids
M8-Lam-NNN, appends the three sidecars + the whole-Bible map, writes receipts/Lam_completion.json carrying the
CAMPAIGN_CLOSE_GATE item-5/6/8 evidence block (CWO execution parity digits; Hebrew quote bytes + tier labels; WEB
quote/gloss fidelity; normalization counts; review-packet retention with hashes; appeals; final review_status; role
separation; B-8 + E-23 digits), and marks complete -> Ezek (canonical order; OWNER_REPAIR_ADVANCE_2026-09-06). Also
adds the book_completion entries the Jer close omitted (Jer) and this close's own (Lam) to marathon_progress.yaml,
anchored on the exact Isa block. Run from SP/Lam.
Usage: python _close_book.py [@usage.json] [--corpus rows_v5.jsonl] [--postcheck postcheck_01.json] [--e23 _e23_post.json] [--final-check final_check_01.json]"""
import collections, hashlib, json, re, subprocess, sys
from pathlib import Path
SP = Path(__file__).resolve().parent
sys.path.insert(0, str(SP / "tools"))
import lam_lib  # noqa: E402
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
usage = json.load(open(sys.argv[1][1:], encoding="utf-8")) if len(sys.argv) > 1 and sys.argv[1].startswith("@") else {}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def argv(k, d): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
CORPUS = argv("--corpus", "rows_v5.jsonl"); POSTCHECK = argv("--postcheck", "postcheck_01.json"); E23 = argv("--e23", "_e23_post.json")
# --- gates ---
post = json.load(open(SP / "postcheck" / POSTCHECK, encoding="utf-8-sig"))
assert post.get("verdict") == "fit_to_assemble", f"postcheck verdict: {post.get('verdict')}"
assert not [r for r in post.get("residual", []) if r.get("severity") in ("high", "medium")], "medium/high residuals in the postcheck"
rows = [json.loads(l) for l in open(SP / CORPUS, encoding="utf-8") if l.strip()]
N = len(rows)
assert all(r["review_status"] == "candidate_review_complete" for r in rows), "review_status not final on every row"
assert [r["chunk_index_in_book"] for r in rows] == list(range(1, N + 1))
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
# 2026-09-07: the gate used to read a FIXED parity path and assert GREEN without checking which corpus that
# parity covered - it would have passed a record reconciling rows_v7 while closing rows_v9. The record is now
# resolved BY the corpus being closed and must say it covers exactly that corpus.
parity_path = SP / "cwo" / f"cwo_parity.{CORPUS.replace('.jsonl', '')}.json"
assert parity_path.is_file(), (
    f"no CWO parity record for the corpus being closed ({CORPUS}); expected {parity_path.name}. "
    "Re-run _cwo_parity.py over the final corpus: a parity record is a statement about ONE corpus.")
parity = json.load(open(parity_path, encoding="utf-8"))
assert parity.get("post_corpus_sha256") == sha(SP / CORPUS), (
    f"the parity record {parity_path.name} reconciles a different corpus "
    f"({str(parity.get('post_corpus_sha256'))[:16]}) than the one being closed ({sha(SP / CORPUS)[:16]})")
assert not parity["exact_arm_residual"] and parity.get("status") == "GREEN", "CWO parity not GREEN"
# --- OW-6 FINAL-CHECKER GATE (owner directive 2026-09-07; CAMPAIGN_CLOSE_GATE item 10) ---
FINAL = argv("--final-check", "final_check_01.json")
fc_path = SP / "final_check" / FINAL
assert fc_path.is_file(), f"OW-6 final-checker packet missing: {fc_path} - no book closes without a claude-fable-5-1 fit_to_close verdict"
fc = json.load(open(fc_path, encoding="utf-8-sig"))
assert fc.get("model") == "claude-fable-5-1", f"final checker model {fc.get('model')!r} != claude-fable-5-1 (the gate names the model)"
assert fc.get("verdict") == "fit_to_close", f"OW-6 final-checker verdict: {fc.get('verdict')}"
assert not [r for r in fc.get("residual", []) if r.get("severity") in ("high", "medium")], "high/medium residuals in the final check"
fc_corpus_sha = hashlib.sha256((SP / CORPUS).read_bytes()).hexdigest()
assert fc.get("corpus_sha256") == fc_corpus_sha, f"the final checker audited a different corpus ({str(fc.get('corpus_sha256'))[:16]} != {fc_corpus_sha[:16]})"
stage1 = sorted((SP / "final_check").glob("transcript_audit_*.json"))
assert stage1, "OW-6 stage-1 transcript-audit packets missing (the reasoning transcripts must be audited before the close)"
s1 = [json.load(open(p_, encoding="utf-8-sig")) for p_ in stage1]
s1_high = [f for pk in s1 for t in pk.get("per_transcript", []) for f in t.get("findings", []) if f.get("severity") == "high"]
s1_med = [f for pk in s1 for t in pk.get("per_transcript", []) for f in t.get("findings", []) if f.get("severity") == "medium"]
# every stage-1 HIGH and MEDIUM finding must be dispositioned by the final checker, each with a reason (a count test,
# not a text match: text matching across two agents' prose is brittle and would silently pass a partial disposition)
disp = [d for d in fc.get("stage1_findings_disposition", []) if d.get("disposition") in ("confirmed", "false_positive", "superseded") and d.get("reason")]
assert len(disp) >= len(s1_high) + len(s1_med), (
    f"final checker dispositioned {len(disp)} stage-1 findings but the transcript audits raised "
    f"{len(s1_high)} high + {len(s1_med)} medium; every one needs a disposition with a reason")
confirmed_high = [d for d in disp if d.get("disposition") == "confirmed"]
assert not confirmed_high or fc.get("residual"), "the final checker confirmed a stage-1 finding but recorded no residual for it"
# OW-6 requires the close to rest on the REAL record, so the checker must state how much of that record
# survives. A verdict that stays silent about missing reasoning implies a completeness the evidence lacks.
_tc = fc.get("transcript_coverage") or {}
assert isinstance(_tc.get("attempts_with_no_transcript"), int), (
    "the final checker did not state transcript coverage; OW-6 closes on the real record, not an implied one")
assert (_tc.get("statement") or "").strip(), "transcript_coverage.statement is empty"
assert _tc.get("reconcile_verdict") == "GREEN", (
    "final checker reports stage-1 reconciliation " + str(_tc.get("reconcile_verdict")))
# stage-1 coverage must be real: every audited slice reports what it read
for pk, p_ in zip(s1, stage1):
    assert pk.get("model") == "claude-fable-5-1", f"{p_.name}: transcript auditor model {pk.get('model')!r} != claude-fable-5-1"
    # the two-pass contract: the mechanical pass must account for 100% of the slice, and nothing can be read
    # closely that was not processed. Separate digits exist so an auditor cannot pass off an index as a reading.
    _ba, _bp, _bc = pk.get("bytes_assigned"), pk.get("bytes_processed"), pk.get("bytes_read_closely")
    assert isinstance(_bp, int) and isinstance(_ba, int) and _bp >= _ba > 0, (
        f"{p_.name}: bytes_processed={_bp} does not account for bytes_assigned={_ba}")
    assert isinstance(_bc, int) and 0 <= _bc <= _bp, (
        f"{p_.name}: bytes_read_closely={_bc} is not within bytes_processed={_bp}")
    assert pk.get("per_transcript"), f"{p_.name}: no per-transcript findings section"
    # a whitespace-only string is truthy; the stage-2 coverage check already strips, and this one must too,
    # or an auditor can satisfy the gate with a single space
    assert (pk.get("coverage_statement") or "").strip(), f"{p_.name}: no coverage statement"
# a coverage STATEMENT is not coverage: reconcile every packet against the slice plan and the manifest, or the
# gate can only confirm that an auditor said something. This is the control that was missing on 2026-09-07.
_rec = subprocess.run([sys.executable, "-B", str(SP / "_final_check_reconcile.py")], cwd=str(SP),
                      capture_output=True, text=True)
assert _rec.returncode == 0, ("OW-6 stage-1 reconciliation FAILED; the close is refused:\n"
                              + (_rec.stdout or "") + (_rec.stderr or ""))
# --- poem non-straddle re-check, parent parity, tiling arithmetic + final ids ---
POEM_STARTS = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
def sspan(r):
    m = re.match(r"^Lam\.(\d+)\.(\d+)-Lam\.(\d+)\.(\d+)$", r["span"]); return (int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))
order = [(ch, v) for ch in sorted(lam_lib.LAST_VERSE) for v in range(1, lam_lib.LAST_VERSE[ch] + 1)]; lin = {cv: i for i, cv in enumerate(order)}
assert len(order) == 154
final, covered = [], 0
for i, r in enumerate(rows, 1):
    s, e = sspan(r)
    poem_s = max(b for b in POEM_STARTS if b <= s); poem_e = max(b for b in POEM_STARTS if b <= e)
    assert poem_s == poem_e, f"row straddles a poem seam: {r['span']}"
    assert r["parent_collection"].startswith(f"F{poem_s[0]} "), f"{r['decision_id']} parent {r['parent_collection']!r} != poem F{poem_s[0]}"
    assert r["chunk_index_in_book"] == i
    covered += lin[e] - lin[s] + 1
    fr = dict(r); fr["decision_id"] = f"M8-Lam-{i:03d}"; final.append(fr)
assert covered == 154, covered
# --- write chunks.jsonl ---
outdir = M8 / "book_chunks" / "Lam"; outdir.mkdir(parents=True, exist_ok=True)
chunk_path = outdir / "chunks.jsonl"
assert not chunk_path.exists(), "book_chunks/Lam/chunks.jsonl already exists"
payload = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in final)
chunk_path.write_text(payload, encoding="utf-8", newline="\n"); sha_chunks = sha(chunk_path)
assert [json.loads(l)["decision_id"] for l in chunk_path.read_text(encoding="utf-8").splitlines()] == [f"M8-Lam-{i:03d}" for i in range(1, N + 1)]
# --- sidecars ---
side_by_id = {s["writer_decision_id"]: s for s in side}; lcr, feq, acf = [], [], []
for r in final:
    wid = r["writer_decision_id"]
    if wid not in side_by_id: continue
    s = side_by_id[wid]
    common = {"model_id": "M8_fable", "book": "Lam", "span": r["span"], "chunk_decision_id": r["decision_id"], "confidence": r["confidence"],
              "review_packet_final_state": "accepted_candidate", "chunk_review_status": "candidate_review_complete", "candidate_hold_state": None,
              "non_authorizing": True, "observed_substrate_signals": r["observed_substrate_signals"]}
    lcr.append({**common, "why_low_confidence": s["why_low_confidence"]})
    feq.append({**common, "concern_type": s["concern_type"], "why_frontier_review_needed": s["why_frontier_review_needed"]})
    acf.append({**common, "concern_type": s["concern_type"], "why_low_confidence": s["why_low_confidence"]})
for name, out in (("low_confidence_register.jsonl", lcr), ("frontier_escalation_queue.jsonl", feq), ("atlas_candidate_feed.jsonl", acf)):
    p = M8 / name; existing = p.read_text(encoding="utf-8"); assert '"book": "Lam"' not in existing, f"{name} already has Lam rows"
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        for row in out: fh.write(json.dumps(row, ensure_ascii=False) + "\n")
map_path = M8 / "whole_bible_chunk_map.jsonl"; assert '"book": "Lam"' not in map_path.read_text(encoding="utf-8")
with map_path.open("a", encoding="utf-8", newline="\n") as fh: fh.write(payload)
# --- packet retention enumeration (durable copies) ---
D = M8 / "sp_durable" / "Lam"
ret = {}
for sub in ("writer", "reviews", "author", "cwo", "spot", "postcheck"):
    d = D / sub
    if d.is_dir():
        ret[sub] = {p.name: sha(p) for p in sorted(d.iterdir()) if p.is_file()}
for n in ("draft_rows_combined.jsonl", "rows_v2.jsonl", "rows_v3.jsonl", "rows_v4.jsonl", "rows_v5.jsonl", "rows_v6.jsonl", "cwo_orders.v1.json", "remedy_docket.v1.json", "author_overrides.json", "freeze/CYCLE_STATE.md"):
    if (D / n).is_file(): ret[n] = sha(D / n)
e23 = json.load(open(SP / E23, encoding="utf-8"))
b8 = {}
p = SP / "spot" / "spot_S4.json"
if p.is_file():
    d = json.load(open(p, encoding="utf-8-sig")); b8["S4"] = {"lane_digits": d.get("lane_digits"), "findings": len(d.get("findings", [])), "clean": d.get("clean")}
lf = json.load(open(SP / "lf_support_sample.json", encoding="utf-8")) if (SP / "lf_support_sample.json").is_file() else {}
conf = collections.Counter(r["confidence"] for r in final); ut = collections.Counter(r["unit_type"] for r in final)
receipt = {"book": "Lam", "model_id": "M8_fable", "mesh_revision": "m8-mesh-r3 + OW-1/OW-2/OW-3/OW-4/OW-5 + OWNER_REPAIR_ADVANCE_2026-09-06",
    "rows": N, "chunks": N, "parents": sorted({r["parent_collection"] for r in final}), "verses_covered": covered,
    "chunk_file_sha256": sha_chunks, "final_corpus": CORPUS, "final_corpus_sha256": sha(SP / CORPUS),
    "corpus_lineage_sha256": {n: sha(SP / n) for n in ("draft_rows_combined.jsonl", "rows_v2.jsonl", "rows_v3.jsonl", "rows_v4.jsonl", "rows_v5.jsonl", "rows_v6.jsonl") if (SP / n).is_file()},
    "confidence_final": dict(conf.most_common()), "unit_type_distribution": dict(ut.most_common()),
    "numbering_disclosure": "IDENTITY book: WEB = MT verse-for-verse in every chapter (22/22/66/22/22 = 154), byte-proven in web_mt_offset_map.json; no zone, no split, no fold; Lam.N.0 never exists. Hebrew throughout (1,564 H-prefixed morph codes, 0 A-prefixed).",
    "acrostic_disclosure": "The acrostic spine is tier-1: chs 1, 2, 4 one verse per letter; ch 3 uniform triplets; ch 5 not acrostic; letter order a byte fact (ch 1 ayin-then-pe; chs 2, 3, 4 PE-THEN-AYIN). Row seams sit on letter/triplet boundaries unless a disclosed tier-1 reason cuts inside; every ch 1-4 row discloses the letters it covers; rows never straddle the poem seams 1:1 / 2:1 / 3:1 / 4:1 / 5:1 (re-checked at this close).",
    "voice_attribution_disclosure": "Held undecided throughout (strategy §7): the speaker/addressee-shift edges (narrator / personified city / the geber / the communal we; YHWH / daughter of Zion-Jerusalem / the wall / Edom), the ch-3 hope-meditation internal seams, the ch-5 discourse seams of the non-acrostic poem, and every whole-poem cap; chunking rows never decide them. Parashah (5 PE + 84 SAMEKH / 89 vv) is tier-3 single-witness corroboration only; paseq count-only (11 segs / 10 vv); K/Q 22 notes / 20 verses (doubled 4:3, 5:7) disclosed on every splice.",
    "staging_erratum_disclosure": "lam_device_inventory.json divine_names/elohim_any named Lam.1.16 and Lam.5.17; both verses carry the demonstrative, not the divine name; recorded in the errata file and disclosed to every lane; no row rests on the false entry.",
    "waves": usage.get("waves", {}),
    "campaign_close_gate_evidence": {
        "item5_cwo_execution_parity": {"record": "sp_durable/Lam/cwo/" + parity_path.name, "sha256": sha(parity_path), "corpus_reconciled": parity.get("post_corpus_sha256"), "parity": {k: {"arm": v["arm"], "ordered_rows": v["ordered_rows"], "pre_wave_candidates": v["pre_wave_candidates"], "post_wave_candidates": v["post_wave_candidates"], "dispositions": v["dispositions"]} for k, v in parity["parity"].items()}, "exact_arm_residual": parity["exact_arm_residual"], "status": parity["status"]},
        "item5_hebrew_quote_bytes_and_tier_labels": {"citation_sweep_status": suite["citation_sweep"].get("status"), "problems": len(suite["citation_sweep"].get("problems", [])), "nfd_degraded_count": suite["citation_sweep"].get("nfd_degraded_count"), "rows": suite["citation_sweep"].get("rows")},
        "item5_web_quote_gloss_fidelity": {"web_quotes_status": suite["web_quotes"].get("status"), "flag_count": suite["web_quotes"].get("flag_count"), "note": "FLAGS dispositioned by the spot wave (declared-FP classes or cured in the micro round); the postcheck re-verified the cured rows"},
        "item5_unicode_normalization": {"ok": norm.get("ok"), "fixed": norm.get("fixed"), "defect_count": norm.get("defect_count"), "count_read_not_status_line": True},
        "item5_review_packet_retention": {"durable_root": "sp_durable/Lam", "enumerated_with_sha256": ret},
        "item5_appeals": {"append_only_appeal_state": "no appeal filed during the Lamentations cycle; none held", "enumerated": []},
        "item5_final_review_status": {"candidate_review_complete": sum(1 for r in final if r["review_status"] == "candidate_review_complete"), "draft": sum(1 for r in final if r["review_status"] == "draft"), "deferred_labels": []},
        "item5_second_generation_role_separation": "every repair wave (author wave, CWO wave, micro round, any fix round) was followed by a fresh full sweep by _wave_repair_sweep.py / the validator suite (deterministic, distinct from the authors) and by model review distinct from the producers (spot wave; postcheck); producer/catcher roles recorded per attempt in the item-6 receipts",
        "item4_prospective_e23": {"rows_checked": e23.get("rows_checked"), "flag_count": e23.get("flag_count"), "rows": sorted({f.get("decision_id") or f.get("row_id") for f in e23.get("flags", [])}), "lane": "spot S5 dispositioned every flag (driver vs defensive mention)"},
        "item1_b8_lf_support_audit": {"frame": f"rows LF verdict=support, retired dropped: {lf.get('frame_size')}", "sample": f"{lf.get('sample_rule')}: {lf.get('sample_size')}", "lanes": b8},
        "item10_ow6_final_checker": {"packet": "final_check/" + FINAL, "sha256": sha(fc_path), "model": fc.get("model"), "verdict": fc.get("verdict"),
            "corpus_sha256_audited": fc.get("corpus_sha256"), "digits": fc.get("digits"), "escalation": fc.get("escalation"),
            "stage1_transcript_audits": [{"packet": p_.name, "sha256": sha(p_), "transcripts_read_fully": json.load(open(p_, encoding="utf-8-sig")).get("transcripts_read_fully"), "slice_digits": json.load(open(p_, encoding="utf-8-sig")).get("slice_digits")} for p_ in stage1],
            "authority": "OW-6 (owner directive 2026-09-07): no book closes without a claude-fable-5-1 final checker verdict of fit_to_close over the whole book, its audit logs and every subagent artifact including captured reasoning transcripts"},
        "item8_ow3": "audit != repair; proposals validated adversarially; both-sides seam law; dependency-applicability records; honest effort reporting (ordered, not verified); pre-feedback baseline preserved (corpus lineage hashes above)"},
    "defect_ledger_totals": usage.get("defect_ledger_totals", {}), "full_mesh_disclosure": "Anthropic-family mesh (sonnet writers/authors/CWO/micro + LF primaries; opus OL primaries/peers/boss/spot/postcheck; haiku sidecar authoring; fable orchestrator). Intra-mesh agreement is corroboration, never cross-provider evidence.",
    "tool_patches": usage.get("tool_patches", ""), "usage_measured_subagent_tokens": usage.get("tokens", {}), "non_authorizing": True}
rec_path = M8 / "receipts" / "Lam_completion.json"; assert not rec_path.exists()
rec_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
# --- mark complete -> Ezek (canonical order) ---
prog_path = M8 / "marathon_progress.yaml"; prog = prog_path.read_text(encoding="utf-8")
assert "books_completed: 24" in prog and "current_book: Lam" in prog
ISA = "  Isa:\n    status: complete\ncurrent_book: Lam"
assert prog.count(ISA) == 1, "Isa block anchor not unique"
assert "  Jer:\n" not in prog and "  Lam:\n" not in prog
prog = prog.replace(ISA, "  Isa:\n    status: complete\n  Jer:\n    status: complete\n  Lam:\n    status: complete\ncurrent_book: Lam")
prog = prog.replace("books_completed: 24", "books_completed: 25"); prog = re.sub(r"current_book: Lam\b", "current_book: Ezek", prog)
prog_path.write_text(prog, encoding="utf-8", newline="\n")
back = prog_path.read_text(encoding="utf-8"); assert "books_completed: 25" in back and "current_book: Ezek" in back and "  Jer:\n    status: complete\n  Lam:\n    status: complete\n" in back
man_path = M8 / "model_manifest.yaml"; man = man_path.read_text(encoding="utf-8")
assert "books_completed: 24" in man and "current_book: Lam" in man
man = man.replace("books_completed: 24", "books_completed: 25").replace("current_book: Lam", "current_book: Ezek"); man_path.write_text(man, encoding="utf-8", newline="\n")
print(json.dumps({"status": "CLOSED", "chunks": N, "verses_covered": covered, "chunk_sha256_16": sha_chunks[:16], "sidecar_rows_appended": len(lcr), "map_appended": N, "receipt": str(rec_path), "progress": "Lam complete -> Ezek (25/66); book_completion entries Jer + Lam added"}, indent=1))
