#!/usr/bin/env python3
"""Orchestrator book-close for Song (owner-scoped allowlisted lane writes):
renumber+freeze, sidecars (12 rows x3, full schemas per lesson e), worktree
installs (book_chunks, whole map append, receipts, sidecar appends),
manifest advance to 22/66 current_book Isa. Deterministic; every install
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
assert len(rows) == 38
for i, r in enumerate(rows, 1):
    r["decision_id"] = f"M8-Song-{i:03d}"
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
    "book": "Song", "frozen": "2026-08-26", "rows": 38,
    "chunks_sha256": chunks_sha, "rows_v3_sha256": rows_v3_sha,
    "lineage": "draft(41) -> rows_v1(31 phase-1 cures) -> rows_v2(boss B-1..B-5: -3 dissolved = 38) -> rows_v3(20 micro-fix cures + 4 postcheck-blocker cures)"},
    indent=1), encoding="utf-8", newline="\n")

# 3. sidecars — 12 low-band rows (postcheck census), bespoke text
by_wid = {r["writer_decision_id"]: r for r in rows}
LOWBAND = [
 ("P01-002", "opening enallage plus unmarked chorus intrusion",
  "the 3ms-to-2ms shift inside MT 1:2 and the 1cp of MT 1:4 are argued rather than settled by any tier-1 form; the 1:4 suffix form is 2fs in form and 2ms only on a pausal reading, left unsettled with no morphology layer staged",
  "voice-attribution layers must not inherit a settled speaker map for the book's opening"),
 ("P01-007", "bracket-completion close severing a first-person run",
  "the closing seam is carried by bracket completion rather than a voice-shift marker, and the woman's first-person run beginning inside MT 2:3 is severed at verse granularity, disclosed; the boss ruling forbids raising confidence on the bracket warrant",
  "adjacent-unit retrieval should co-surface Song.2.4-2.6 whenever this exchange is hit"),
 ("P01-012", "unattributed foxes couplet",
  "no tier-1 form marks the verse's speaker (no gender on the plural imperative, no address-vocabulary anchor, no daughters vocative); the isolation itself, not any one attribution guess, is what the bytes cannot settle",
  "speaker-attribution downstream must treat the verse as voice-open"),
 ("P01-016", "closest-fit unit_type on a third-person processional",
  "MT 3:6-3:10 is processional description rather than direct address, and the only addressee shift surfaces at the closing imperative in MT 3:11; the classification is a disclosed closest-fit application",
  "type-filtered retrieval may mis-bucket the palanquin processional"),
 ("P01-019", "transitional verse settled only by its reply",
  "the single-verse invitation's function depends on the reply in the immediately following verse, which is argued separately on its own bytes — the unit's role rests on material outside its span",
  "retrieval should co-surface Song.5.1 when this verse is hit"),
 ("P02-006", "boss-adopted inclusio span with an unmarked internal join",
  "the internal MT 6:7|6:8 join carries no marked seam; the span wider than the mechanically derived body-part run rests on the byte-tier inclusio brackets plus the absence of address forms at MT 6:8-6:10",
  "cluster granularity is convergence-sensitive; the narrower praise-only cut remains a defensible rival"),
 ("P02-008", "the merkavot-ammi-nadiv crux",
  "MT 6:12 is the book's hardest line: the speaker's identity and the syntax of the nafshi clause are held open rather than decided, and the OSHB exegesis note there is single-witness apparatus, not a text-level seam",
  "no downstream reading may inherit a settled construal of MT 6:12"),
 ("P02-009", "offset-zone seam verse carrying two holds",
  "the dance-of-Mahanaim construal is held open, and the voice assignment of the gaze clause is weighed between the 1cp form with its 2fs suffix and the 2mp prefix-conjugation form in the same clause, undecided; this is the seam verse MT 7:1 = WEB 6:13",
  "dual-cite discipline is required downstream, and voice-assignment layers must treat the clause as open"),
 ("P02-018", "shalhevet-yah crux inside a contested merged frame",
  "the MT 8:6 construal (intensive flame versus divine element) is held with the one-word/divided-token fact disclosed; the merged 8:5-8:7 frame is itself contested, and MT 8:5 carries an intra-verse turn disclosed rather than resolved",
  "theological downstream readings must not inherit a settled divine-name occurrence at 8:6"),
 ("P02-019", "speaker-group identification by content inference",
  "the 1cp possessive fixes plurality but no tier-1 form names the brothers; the kinship link to MT 1:6 carries the identification across the book by content only",
  "entity attribution must treat the speaker group as inferred, not named"),
 ("P02-020", "attribution forms sitting later than the seam",
  "the seam pronoun fixes only person and number; the gender-marked forms that actually carry the attribution (the feminine participle and the 3ms suffix) stand later in the verse rather than at the seam itself",
  "seam-anchored sampling may miss the attribution warrant unless the whole verse is read"),
 ("P02-021", "vineyard-mashal attribution at skeleton tier",
  "the female attribution rests on a vineyard-lexeme recurrence with MT 1:6 that holds at skeleton tier only (the first vowel differs), the row's own disclosed tier limit, plus a referential Solomon contrast that is argued rather than settled",
  "tier-sensitive convergence should re-weigh the attribution"),
]
assert len(LOWBAND) == 12
base_states = {"review_packet_final_state": "accepted_candidate",
               "chunk_review_status": "candidate_review_complete",
               "candidate_hold_state": None, "non_authorizing": True}
lc, fq, ac = [], [], []
for wid, concern, why, risk in LOWBAND:
    r = by_wid[wid]
    assert r["confidence"] in ("medium_low", "low"), f"{wid} not low-band: {r['confidence']}"
    core = {"model_id": "M8_fable", "book": "Song", "span": r["span"],
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
(WT / "book_chunks" / "Song").mkdir(exist_ok=True)
tgt = WT / "book_chunks" / "Song" / "chunks.jsonl"
tgt.write_bytes(chunks.read_bytes())
assert sha(tgt) == chunks_sha, "sha mismatch after book_chunks install"

wm = WT / "whole_bible_chunk_map.jsonl"
before = len([l for l in wm.read_text(encoding="utf-8").splitlines() if l.strip()])
with wm.open("a", encoding="utf-8", newline="\n") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
after = len([l for l in wm.read_text(encoding="utf-8").splitlines() if l.strip()])
assert (before, after) == (3684, 3722), f"whole map count {before}->{after}"

for fname, data in (("low_confidence_register.jsonl", lc),
                    ("frontier_escalation_queue.jsonl", fq),
                    ("atlas_candidate_feed.jsonl", ac)):
    p = WT / fname
    n0 = len([l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()])
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        for r in data:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    n1 = len([l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()])
    assert n1 == n0 + 12, f"{fname} append {n0}->{n1}"

# 5. receipt
conf = Counter(r["confidence"] for r in rows)
ut = Counter(r["unit_type"] for r in rows)
pc = Counter(r["parent_collection"].split()[0] for r in rows)
receipt = {
    "book": "Song", "model_id": "M8_fable", "mesh_revision": "m8-mesh-r3-full",
    "rows": 38, "chunks": 38, "parents": dict(pc),
    "verses_covered": "117/117",
    "chunk_file_sha256": chunks_sha, "rows_v3_sha256": rows_v3_sha,
    "confidence_final": {**dict(conf), "basis": "computed directly from rows_v3.jsonl (frozen); boss-ordered caps preserved"},
    "unit_type_distribution": dict(ut),
    "numbering_disclosure": {
        "status": "NOT identity (the expected non-identity CONFIRMED at Phase 0)",
        "crosswalk": "MT 7:1 = WEB 6:13; MT 7:2-14 = WEB 7:1-13; all other chapters identity; totals 117=117",
        "proof": "per-chapter counts under the rule set; 104 crosswalk content anchors (18 in the offset zone); identity-falsification probe (18 failures in the zone); six seam byte-assertions; the single anchor miss byte-reviewed (the mixed-wine hapax); OSHB KJV-variance layer EMPTY/inert for this book",
        "tier0_rule": "owner-ratified offset-zone dual-cite rule machine-enforced on every structured ref touching WEB 6:13 / WEB ch 7 / MT ch 7"},
    "voice_attribution_disclosure": {
        "policy": "owner-ruled MODERATE (2026-08-25): in-verse gender/vocative markers + attested formula anchors = tier-1; continuity inference = tier-2 corroboration, never sole driver; WEB [SPEAKER] headings tier-4 always (31 sites cataloged for audit only)",
        "note": "every voice-shift seam claim quotes a gender-marked or formula-anchor Hebrew form with tier label; postcheck verified zero heading-leaning"},
    "waves": {"writer": "2 parts (41 draft rows)",
              "primary": "12 packets (6 clusters x LF sonnet + OL opus, FULL dual-blind — no scoping)",
              "peer": "7 attempts (6 clusters + 1 follow-on; 48 rulings)",
              "boss": "5 rulings over 2 attempts / 3 adopted changes / 2 disclosure cures / 0 owner escalations",
              "author": "2 phase-1 batches (39 orders) + 2 phase-2 batches (boss consequences) + 2 micro-fix batches (34 spot cures) + 1 final batch (4 postcheck cures)",
              "spot": "6 lanes (34 findings) + 1 postcheck agent (BLOCKING x2 -> cured -> READY_TO_FREEZE)"},
    "defect_ledger_totals": {
        "peer_wave": {"challenge_items": 59, "rulings": 48, "upheld": 32, "refined": 14, "refuted": 0, "escalated": 2},
        "boss": {"ruled": 5, "adopt_change": 3, "disclosure_cure": 2,
                 "note": "B-5 arose from a phase-1 author correctly refusing a disguised boundary change in a peer remedy (the Eccl-B-5 pattern); refusal ratified"},
        "spot_wave": {"findings": 34, "all_cured": True},
        "postcheck": {"blocking": 2, "cured": 2, "warn_flags_judged": 55, "genuine": 0}},
    "full_mesh_disclosure": {
        "policy": "owner-ruled 2026-08-25: FULL dual-blind primaries over all rows (no scoped mesh); decorrelation LF sonnet / OL opus",
        "untouched_audit_result": "all 3 mesh-support-only rows were 100% audited post-repair at full depth: 0 boundary errors, 0 texture defects (beats the Prov/Eccl ~25% texture row-rate) — no unreviewed population remains in this book",
        "residual_risk": "limited to defect classes no wave models: all 55 standing universals WARN flags were individually re-judged heuristic false positives at postcheck"},
    "tool_patches": {"inherited": "p1-p4 (Prov/Eccl lineage; the Phase-0 p4 pre-listing prevented any rev-round ngram regression this book)",
                     "phase0_adaptation_gaps_caught": "leading-underscore literal (pmarks_ residue) + lowercase rule-name strings — both fixed at Phase 0 and recorded for the next adaptation",
                     "orchestrator_triage_gap_caught": "boundary-proposal keyword net missed an 'extend the exchange' phrasing; caught by author discipline; next-book law: content-read every remedy"},
    "usage_measured_subagent_tokens": {
        "writers": 685000, "primaries": 2022000, "peers": 1278000,
        "boss": 415000, "authors_phase1": 730000, "authors_phase2": 462000,
        "spot_wave": 1283000, "micro_fix": 521000, "final_fix": 152000,
        "postcheck": 259000,
        "total": 7807000,
        "note": "owner gate authorized ~7M with a mandatory check-in before crossing 8M; measured 7.81M stays under the 8M line; the ~0.8M overrun above the soft figure is disclosed here and in CYCLE_STATE_CLOSE (the Eccl disclosure pattern). Environment absorbed 8 infrastructure kills (3 connection-lost, 1 process-exit x3 agents counted as 3, 2 stream-watchdog stalls) with zero work loss (resume-in-place)."},
    "non_authorizing": True,
}
(WT / "receipts" / "Song_completion.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

# 6. manifest advance
mp = WT / "marathon_progress.yaml"
t = mp.read_text(encoding="utf-8")
assert "  Song:\n" not in t and "current_book: Song" in t and "books_completed: 21" in t
t = t.replace("books_completed: 21", "books_completed: 22", 1)
t = t.replace("current_book: Song", "current_book: Isa", 1)
t = t.replace("  Eccl:\n    status: complete\n", "  Eccl:\n    status: complete\n  Song:\n    status: complete\n", 1)
mp.write_text(t, encoding="utf-8", newline="\n")

mm = WT / "model_manifest.yaml"
t2 = mm.read_text(encoding="utf-8")
assert "books_completed: 21" in t2 and "current_book: Song" in t2
t2 = t2.replace("books_completed: 21", "books_completed: 22", 1)
t2 = t2.replace("current_book: Song", "current_book: Isa", 1)
mm.write_text(t2, encoding="utf-8", newline="\n")

print(json.dumps({"chunks_sha256": chunks_sha, "rows": 38,
                  "whole_map": f"{before}->{after}",
                  "sidecars_appended": 12,
                  "confidence": dict(conf), "unit_type": dict(ut), "parents": dict(pc),
                  "manifests": "advanced to 22/66, current_book Isa",
                  "status": "INSTALLED"}, ensure_ascii=False, indent=1))
