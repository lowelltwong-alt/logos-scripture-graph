#!/usr/bin/env python3
"""Daniel book close. Ported from sp_durable/Ezek/_close_book.py (sha256 b5697556...831c). Non-authorizing.

The tool is run by the orchestrator, never by a lane, and --close is the owner's act (OW-11; Daniel is the last book that
authorization names, so the close is followed by the OW-9 hard stop and the next book is the owner's choice).

MODES
  --dry-report DIR   evaluate every gate, write a preview of every close write into DIR (DIR must lie outside the M8 tree),
                     change nothing in the tree. Deterministic: no clock, no randomness, no directory scan.
  --close            the only mode that writes into the tree. Refuses unless every gate is MET; takes an exclusive lock;
                     writes each file whole, LF bytes, through a temporary file and an atomic replace; rolls every write
                     back on any failure. Runs only on the tree this file is installed in (never with --m8-root).
  (neither)          evaluate every gate and print the summary.

ARGUMENTS
  @usage.json        optional positional: a JSON file whose "tokens" object is copied into the receipt (REPORTED)
  --m8-root DIR      evaluate another M8 tree (the gate tests' private mirrors). Default: found from this file's location.
  --acf OPT          lam_pattern | item22: which rows are appended to atlas_candidate_feed.jsonl (owner's choice)
  --next-book NAME   the value current_book takes after Daniel (owner's choice; OW-11 names no book after Daniel)
  --fixture-landed F dry-mode TEST HOOK: verify retention against F instead of the pinned landed-outputs manifest. The
                     report names the hook when used, and --close refuses it.

LAW CARRIED FROM EZEKIEL
  * A gate that cannot be evaluated is UNMET, never skipped: every gate group runs inside guard(), and an exception
    becomes an UNMET gate that names it.
  * DEFERRED is never MET (OW-28): the campaign-end Fable review is recorded DEFERRED with its packet digest. The
    stage-1 transcript audit is recorded OWED, NOT MET (OW-26). Neither is counted as a met gate anywhere.
  * No Fable call is made or implied by this tool (OW-30).
  * Digests are taken on LF bytes only (E-73): every close write is refused if it carries a CR byte.

WHAT DIFFERS FROM EZEKIEL (each is listed with its reason in build_notes.json)
  * No held row, no hold ruling, no v8/v9/v10 lineage, no delta lanes, no docket, no typed-dispositions file. Instead:
    every row must be candidate_review_complete with null hold fields, no exception; one lineage hop is proven against
    rows_v1_final.manifest.json; and the single blind pair must itself return fit_to_assemble and fit_to_close over this
    corpus with no high or medium residual, all of items 20-23, and only deferred-or-owed unmet assessment entries.
  * The retention manifest is built from the pinned manifest of landed outputs plus the three attempt-receipt files it
    names (no directory walk).
  * The grader carrier cannot be byte-pinned: adding book_close_shapes.Dan changes its digest. Its generator's --check,
    its measured constants and both statement digests are gated instead, and its digest is recorded in the receipt.
  * Added: the language layer, the boss audit record (REPORTED), the scholar record, the parity tool's --check.

EDIT POINTS the orchestrator must confirm before the close (all are ASSUMED names, marked below): LANES, MERGED_RECEIPTS,
LANDED/LANDED_PIN if a later landed-outputs manifest supersedes v2, UNMET_TYPES (the vocabulary the lanes must use).
"""
import argparse
import collections
import hashlib
import itertools
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
BOOK = "Dan"
BOOKS_BEFORE, BOOKS_AFTER = 26, 27

# --- verified constants. MEASURED 2026-10-12/13 by work/pin_check.py, work/probe2.py, work/probe3.py of dan_close_tool_a1 ---
CORPUS = "rows_v1_final.jsonl"
CORPUS_PIN = "783a0e9ac2c8fe4c942b3b8f7dd65efaefdb28f6fcb55fdde42b500a5c395e09"
DAN_LIB_PIN = "1f397a7a08aba99cad67b0a59378eafa961130559bd8d07a7a9ed9d2f3043361"
ROWS, VERSES, CHAPTERS = 75, 357, 12
ZONE = [3, 4, 5, 6]
ZONE_MOVED = 66                      # WEB verses whose MT reference differs (Dan.4.1 .. Dan.6.28)
PARENTS = ["PA", "PB", "PC", "PD", "PE", "PF", "PG", "PH", "PI", "PJ"]
LANGUAGE_COUNTS = {"A": 44, "H": 30, "mixed": 1}
LOW_ROWS = 49
MANIFEST = "rows_v1_final.manifest.json"
MANIFEST_PIN = "21568cd63a0dc34f1ae9e18bc590907c723eac89565132dcb5354c10c4cb9bdb"
BUILT_FROM = "sp_durable/Dan/fixup/draft_rows_fixup10_applied.jsonl"
BUILT_FROM_PIN = "ccf8040c65e92019d405ba79f9c837fa2c4594d82fc0245143b99e93770a88c6"
LINEAGE_FIELDS = ["candidate_hold_basis", "candidate_hold_state", "review_status"]
SUITE_PIN = "dc9e5d1b6f05cd9069d83f580e519eeb501329ae2490e7ff9bb58a31e4f4c811"
PARITY_PIN = "9a626802359a9096e507cb1dfcc910e1ac9ed7f9526a6765483a19d3ef1e4250"
LANDED_REL = "close/dan_landed_outputs_manifest.v2.json"
LANDED_PIN = "5fadae2c09ab3bdc9a51184e40f72bc13a1b0e0182a39c070bebde99d9be9449"
LANDED_OUTPUTS, LANDED_RECEIPT_FILES = 141, 3
BOSS = (("e1", "review/boss/dan_boss_audit.v1.json", "ea70f94e48aed5d24f0adb604c3215a8f6e95ccf940b59da89147de3636a13c3"),
        ("e2", "review/boss/supp_e2/dan_boss_audit_b8_b14.json", "d186bac7af0e1f8763ee307c54955575cdde96625698f182290c30545472672c"))
BOSS_E2_SUPERSEDES = ["B14", "B8"]
ROUTED_PIN = "42efe601b731e212ba60bc9b19fd9b3199d86e8d5a152bb7571f8e956376b0d6"
ROUTED_ITEMS = 46
CARRIER_FACTS = {"ow13_grader_model": "claude-fable-5-1", "declared_fallback_model": "claude-opus-5-5",
                 "fallback_in_force": True,
                 "downgrade_statement_sha256": "aef1c672b4882fb590bbde30f05d7630333f3b281d21d62da52488ebec46e2a3"}
HOLD_FIELDS = {"review_status": "candidate_review_complete", "candidate_hold_state": None, "candidate_hold_basis": None}
# ASSUMED (edit points): Ezekiel's naming carried to Daniel. Confirm against the launched lanes before the close.
LANES = (("A", "dan_merged_close_lane_a_a1"), ("B", "dan_merged_close_lane_b_a1"))
MERGED_RECEIPTS_REL = "dan_merged_close_attempt_receipts.jsonl"
LANE_FILES = ("postcheck.json", "final_check.json", "items_20_23.json", "named_questions.json", "lane_meta.json",
              "final_message.md")
# an unmet entry of a lane's close_gate_assessment must carry one of these in `type`; both are recorded, neither is MET
UNMET_TYPES = ("DEFERRED_OW28_FABLE_END_REVIEW", "OWED_TRANSCRIPT_AUDIT")
SCHOLAR_FILES = ("gen_scholar_record.py", "check_scholar_record.py", "DANIEL_SCHOLAR_RECORD.v1.md",
                 "scholar_record_check.v1.json")
SIDE_FIELDS = ("concern_type", "why_low_confidence", "why_frontier_review_needed", "possible_downstream_risk",
               "suggested_reviewer", "proposed_atlas_action")
SHARED = ("low_confidence_register.jsonl", "frontier_escalation_queue.jsonl", "atlas_candidate_feed.jsonl",
          "whole_bible_chunk_map.jsonl")
PROG_ANCHOR = "  Ezek:\n    status: complete\ncurrent_book: Dan\n"
NEXT_BOOK_RE = re.compile(r"^[1-3]?[A-Z][A-Za-z]{1,7}$")
NEXT_PLACEHOLDER = "<NEXT_BOOK: the owner's choice, pass --next-book>"
LOCK_NAME = "_close_book.Dan.lock"
NOT_EVALUATED = [
    "item 5 appeals: no appeal file is read by this tool",
    "items 13-14: capture index, cure verification and census are the orchestrator's close-packet duties",
    "item 15 (OW-11): the authorization is the owner's; this tool only refuses to write unless every gate is MET",
    "item 16: the book-close status update", "item 17: model roles beyond the grader carrier",
    "item 18: the orchestration playbook, learning log and metrics", "item 19: quality over budget",
    "item 21 and item 23 beyond each lane's items_20_23 verdict", "the public README refresh and push"]

M8 = SP = DAN = None
GATES = []


def bind(root):
    global M8, SP, DAN
    M8 = root
    SP = M8 / "sp_durable"
    DAN = SP / BOOK


def gate(name, ok, detail=""):
    GATES.append({"gate": name, "met": bool(ok), "status": "MET" if ok else "UNMET", "detail": str(detail)[:400]})
    return bool(ok)


def guard(group, fn, default):
    """A gate group that raises is UNMET by name; it is never skipped."""
    try:
        return fn()
    except Exception as e:  # noqa: BLE001
        gate("%s: every gate of this group could be evaluated" % group, False, "%s: %s" % (type(e).__name__, e))
        return default


def shab(b):
    return hashlib.sha256(b).hexdigest()


def sha(p):
    return shab(Path(p).read_bytes())


def sha_or_none(p):
    return sha(p) if Path(p).is_file() else None


def jl(p):
    return [json.loads(l) for l in Path(p).read_bytes().decode("utf-8-sig").split("\n") if l.strip()]


def jload(p):
    return json.loads(Path(p).read_bytes().decode("utf-8-sig"))


def dump(objs):
    return "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs).encode("utf-8")


def hi_med(xs):
    return [r for r in (xs or []) if isinstance(r, dict) and r.get("severity") in ("high", "medium")]


def run(script, *args):
    """Run a named tool of the tree with --check style arguments; returns (exit code, last stdout line)."""
    if not Path(script).is_file():
        return 1, "absent: " + Path(script).name
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}
    p = subprocess.run([sys.executable, "-B", str(script)] + list(args), cwd=str(DAN), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    out = (p.stdout or "").strip().splitlines()
    return p.returncode, (out[-1] if out else "")


def coverage(opt, by_id, low_ids):
    """The coverage validator's per-book feed rule, as Ezekiel's close tool measures it, over one option's rows."""
    ids = [x.get("chunk_decision_id") for x in opt]
    stale = [x["chunk_decision_id"] for x in opt if x.get("chunk_decision_id") in low_ids and (any(
        x.get(f) != by_id[x["chunk_decision_id"]].get(g) for f, g in (
            ("span", "span"), ("confidence", "confidence"), ("chunk_review_status", "review_status"),
            ("candidate_hold_state", "candidate_hold_state"))) or x.get("review_packet_final_state") != (
        "accepted_candidate" if by_id[x["chunk_decision_id"]].get("candidate_hold_state") is None
        else "held_lower_confidence"))]
    return {"duplicates": len(ids) - len(set(ids)), "missing": sorted(low_ids - set(ids)),
            "orphan": sorted(str(i) for i in set(ids) - low_ids), "stale": sorted(stale)}


def cov_ok(c):
    return not (c["duplicates"] or c["missing"] or c["orphan"] or c["stale"])


def cov_brief(c):
    return {k: (v if isinstance(v, int) else v[:4]) for k, v in c.items()}


# ------------------------------------------------------------------ gates ------------------------------------------------
def corpus_gates(dan_lib):
    cp = DAN / CORPUS
    b = cp.read_bytes()
    gate("corpus pinned", shab(b) == CORPUS_PIN, shab(b)[:16])
    gate("corpus is LF-only (E-73)", b"\r" not in b and b.endswith(b"\n"))
    rows = jl(cp)
    n = len(rows)
    gate("corpus has %d rows, every one of book Dan" % ROWS, n == ROWS and all(r.get("book") == BOOK for r in rows), n)
    held = {r.get("writer_decision_id"): {k: r.get(k, "ABSENT") for k in HOLD_FIELDS} for r in rows
            if any(k not in r or r[k] != v for k, v in HOLD_FIELDS.items())}
    gate("every row candidate_review_complete with null hold fields; no row carries a hold", not held,
         dict(sorted(held.items())[:3]))
    gate("chunk_index 1..N", [r.get("chunk_index_in_book") for r in rows] == list(range(1, n + 1)), n)
    wids = [r.get("writer_decision_id") for r in rows]
    gate("writer_decision_id unique and present", all(wids) and len(set(wids)) == n, n - len(set(wids)))
    order = [(c, v) for c in sorted(dan_lib.LAST_VERSE) for v in range(1, dan_lib.LAST_VERSE[c] + 1)]
    lin = {cv: i for i, cv in enumerate(order)}
    prev, bad, covered, lang_bad, lang = -1, [], 0, [], collections.Counter()
    for r in rows:
        m = re.match(r"^Dan\.(\d+)\.(\d+)-Dan\.(\d+)\.(\d+)$", str(r.get("span")))
        s = lin.get((int(m.group(1)), int(m.group(2)))) if m else None
        e = lin.get((int(m.group(3)), int(m.group(4)))) if m else None
        if s is None or e is None or s != prev + 1 or e < s:
            bad.append(r.get("writer_decision_id"))
            continue
        covered += e - s + 1
        prev = e
        langs = {dan_lib.language_of(c, v) for c, v in order[s:e + 1]}
        want = "H" if langs == {"Hebrew"} else ("A" if langs == {"Aramaic"} else "mixed")
        lang[str(r.get("language"))] += 1
        if r.get("language") != want:
            lang_bad.append((r.get("writer_decision_id"), r.get("language"), want))
    gate("tiling contiguous over %d WEB verses in %d chapters" % (VERSES, CHAPTERS),
         not bad and covered == dan_lib.TOTAL_VERSES == len(order) == VERSES and prev == len(order) - 1
         and len(dan_lib.LAST_VERSE) == CHAPTERS, {"covered": covered, "breaks": bad[:5]})
    gate("language layer: each row's `language` is what dan_lib.language_of gives over its span",
         not lang_bad and not bad and dict(sorted(lang.items())) == LANGUAGE_COUNTS,
         {"counts": dict(sorted(lang.items())), "bad": lang_bad[:3]})
    runs = [k for k, _ in itertools.groupby(str(r.get("parent_collection")) for r in rows)]
    gate("each parent collection one contiguous run, PA..PJ in order",
         len(runs) == len(set(runs)) and [p[:2] for p in runs] == PARENTS, [p[:2] for p in runs])
    moved = [(c, v) for c, v in order if dan_lib.web_to_mt(c, v) != (c, v)]
    gate("numbering zone as measured: chapters 3-6, %d WEB verses whose MT reference differs" % ZONE_MOVED,
         sorted(dan_lib.ZONE_CHAPTERS) == ZONE and len(moved) == ZONE_MOVED, {"moved": len(moved)})
    return rows, moved


def lineage_gates(rows):
    """The final file is its source plus exactly the manifest's (row, field) changes. An absent field and a null field
    are different: the diff is presence-aware."""
    mp = DAN / MANIFEST
    gate("lineage manifest pinned", sha(mp) == MANIFEST_PIN, sha(mp)[:16])
    man = jload(mp)
    gate("lineage manifest names this corpus and its source", man.get("names") == "sp_durable/Dan/" + CORPUS
         and man.get("sha256") == CORPUS_PIN and man.get("rows") == ROWS and man.get("built_from") == BUILT_FROM
         and man.get("built_from_sha256") == BUILT_FROM_PIN, {k: str(man.get(k))[:40] for k in ("names", "built_from", "rows")})
    src = M8 / BUILT_FROM
    gate("lineage source pinned", sha(src) == BUILT_FROM_PIN, sha(src)[:16])
    old, changed, bad = jl(src), man.get("changed") or {}, []
    for a, b in zip(old, rows):
        d = sorted(k for k in set(a) | set(b) if (k in a) != (k in b) or a.get(k) != b.get(k))
        if a.get("writer_decision_id") != b.get("writer_decision_id") or d != sorted(changed.get(b.get("writer_decision_id"), [])) \
                or d != LINEAGE_FIELDS:
            bad.append((b.get("writer_decision_id"), d[:4]))
    gate("the corpus differs from its source only where the manifest says (three status fields per row)",
         len(old) == len(rows) == len(changed) and not bad, {"old": len(old), "bad": bad[:3]})
    basis = man.get("basis") or {}
    gate("lineage manifest's basis names the pinned boss audit records",
         all((basis.get("boss_audit_" + t) or {}).get("sha256") == pin for t, _, pin in BOSS))
    return man


def boss_gates():
    """REPORTED: the audit is a lane's record. The tool checks only that the pinned records say what the close cites."""
    verdict, recs = {}, {}
    for tag, rel, pin in BOSS:
        p = DAN / rel
        gate("boss audit %s pinned" % tag, sha(p) == pin, sha(p)[:16])
        recs[tag] = {"file": "sp_durable/Dan/" + rel, "sha256": sha(p)}
        got = {c.get("id"): c.get("verdict") for c in jload(p).get("conditions") or []}
        if tag == "e2":
            gate("boss audit e2 answers exactly B8 and B14", sorted(got) == BOSS_E2_SUPERSEDES, sorted(got))
        verdict.update(got)
    want = ["B%d" % i for i in range(1, 18)]
    gate("boss audit: conditions B1..B17 all MET across e1 and e2 (REPORTED)",
         sorted(verdict, key=lambda x: int(x[1:]) if x[1:].isdigit() else 0) == want and all(v == "MET" for v in verdict.values()),
         {k: v for k, v in verdict.items() if v != "MET"})
    return recs


def sidecar_gates(rows):
    low = {r["writer_decision_id"] for r in rows if r["confidence"] in ("medium_low", "low")}
    sp = DAN / "sidecar_src_dan.jsonl"
    present = gate("sidecar source present (sidecar_src_dan.jsonl)", sp.is_file(), sp.name)
    side = jl(sp) if present else []
    ids = [s.get("writer_decision_id") for s in side]
    gate("sidecar set == low/medium_low rows", present and len(ids) == len(set(ids)) and set(ids) == low
         and len(low) == LOW_ROWS, {"missing": sorted(low - set(ids))[:3], "extra": sorted(set(ids) - low)[:3], "rows": len(ids)})
    gate("sidecar fields present", present and all(s.get(k) for s in side for k in SIDE_FIELDS))
    gate("why_low_confidence not boilerplate", present and len({s.get("why_low_confidence") for s in side}) == len(side))
    rc, tail = run(DAN / "deliverables" / "gen_sidecars.py", "--check")
    gate("gen_sidecars.py --check MATCH", rc == 0 and tail == "MATCH", tail[:200])
    return side


def evidence_gates():
    sp_ = DAN / (CORPUS + ".validator_report.json")
    gate("suite report pinned", sha(sp_) == SUITE_PIN, sha(sp_)[:16])
    suite = jload(sp_)
    sm, norm = suite.get("summary") or {}, suite.get("hebrew_normalize_dryrun") or {}
    gate("suite GREEN over this corpus", sm.get("hard_status") == "GREEN" and sm.get("nfd_hard_e01") is False
         and Path(str(suite.get("rows_file"))).name == CORPUS, {"summary": sm, "rows_file": suite.get("rows_file")})
    gate("normalize dry-run clean", norm.get("fixed") == 0 and norm.get("defect_count") == 0,
         {"fixed": norm.get("fixed"), "defect_count": norm.get("defect_count")})
    cs, wq, lz = (suite.get(k) or {} for k in ("citation_sweep", "web_quotes", "language_zones"))
    gate("Hebrew/Aramaic quote bytes and tier labels GREEN (citation sweep)", cs.get("status") == "GREEN"
         and cs.get("nfd_degraded_count") == 0 and cs.get("rows") == ROWS, {k: cs.get(k) for k in ("status", "nfd_degraded_count", "rows")})
    gate("WEB quote fidelity GREEN", wq.get("status") == "GREEN" and wq.get("flag_count") == 0,
         {k: wq.get(k) for k in ("status", "flag_count")})
    gate("language zones GREEN", lz.get("status") == "GREEN" and lz.get("flag_count") == 0, {k: lz.get(k) for k in ("status", "flag_count")})
    pp = DAN / "cwo" / ("cwo_parity.%s.json" % CORPUS.replace(".jsonl", ""))
    gate("CWO parity record pinned", sha(pp) == PARITY_PIN, sha(pp)[:16])
    par = jload(pp)
    gate("CWO parity GREEN for THIS corpus", par.get("post_corpus_sha256") == CORPUS_PIN and par.get("status") == "GREEN"
         and par.get("exact_arm_residual") == [] and par.get("routed_open") == [], {"record": pp.name, "status": par.get("status")})
    rc, tail = run(DAN / "_cwo_parity_dan.py", "--check")
    try:
        chk = json.loads(tail)
    except ValueError:
        chk = {}
    gate("CWO parity record reproduces (_cwo_parity_dan.py --check MATCH, GREEN)", rc == 0 and chk.get("check") == "MATCH"
         and chk.get("status") == "GREEN", tail[:200])
    return suite, pp, par


def carrier_gates():
    cp = SP / "campaign" / "grader_models.v2.json"
    c = jload(cp)
    rc, tail = run(SP / "campaign" / "gen_grader_models_v2.py", "--check")
    gate("grader carrier still transcribes the ledger (gen_grader_models_v2.py --check MATCH)", rc == 0 and tail == "MATCH", tail[:200])
    gate("grader carrier states the measured fallback (OW-25)", all(c.get(k) == v for k, v in CARRIER_FACTS.items())
         and shab(str(c.get("downgrade_statement", "")).encode("utf-8")) == CARRIER_FACTS["downgrade_statement_sha256"],
         {k: c.get(k) for k in ("ow13_grader_model", "declared_fallback_model", "fallback_in_force")})
    model = c["declared_fallback_model"] if c.get("fallback_in_force") else c["ow13_grader_model"]
    shape = (c.get("book_close_shapes") or {}).get(BOOK) or {}
    gate("carrier grants Daniel the OW-26 shape (book_close_shapes.Dan: shape, directive, transcript_audit, weakness_statement)",
         bool(shape.get("shape")) and shape.get("directive") == "OW-26" and shape.get("transcript_audit") == "OWED, NOT MET"
         and bool(shape.get("weakness_statement")), sorted(shape))
    gate("carrier's Daniel weakness statement matches its recorded digest", bool(shape.get("weakness_statement"))
         and shab(str(shape.get("weakness_statement")).encode("utf-8")) == shape.get("weakness_statement_sha256"))
    return c, model, shape, sha(cp)


def lane_gates(model, fallback, feed_sha):
    """One blind pair (OW-19 floor). Daniel has no delta round, so the pair itself must be fit: nothing is docketed away."""
    lanes = {}
    landing = DAN / "merged_close" / "landing_manifest.v1.json"
    land = jload(landing) if landing.is_file() else None
    if not gate("landing manifest present (merged_close/landing_manifest.v1.json)", land is not None, landing.name):
        gate("two distinct blind lanes, both landed and both read", False, "no landing manifest")
        return lanes, None
    rp = DAN / MERGED_RECEIPTS_REL
    recs = jl(rp) if rp.is_file() else []
    for L, att in LANES:
        ent = (land.get("lanes") or {}).get(L) or {}
        files, ok = {}, True
        for fn in LANE_FILES:
            f = (ent.get("files") or {}).get(fn) or {}
            p = landing.parent / str(f.get("durable")) if f.get("durable") else None
            good = p is not None and ".." not in str(f.get("durable")) and p.is_file() and sha(p) == f.get("sha256")
            ok &= good
            files[fn] = p if good else None
        gate("lane %s: six durable outputs match the landing manifest" % L, ok and ent.get("attempt_id") == att,
             {"attempt_id": ent.get("attempt_id"), "bad": [k for k, v in files.items() if v is None]})
        done = [r for r in recs if r.get("attempt_id") == att and r.get("record_kind") == "completion"]
        gate("lane %s: completion receipt COMPLETED on %s" % (L, model), len(done) == 1
             and done[0].get("outcome") == "COMPLETED" and done[0].get("model_actual") == model,
             [(d.get("outcome"), d.get("model_actual")) for d in done])
        if not ok:
            lanes[L] = None
            gate("lane %s: its verdict gates could be evaluated" % L, False, "lane files do not match the landing manifest")
            continue
        pc, fc = jload(files["postcheck.json"]), jload(files["final_check.json"])
        it, nq, meta = jload(files["items_20_23.json"]), jload(files["named_questions.json"]), jload(files["lane_meta.json"])
        gate("lane %s: postcheck fit_to_assemble, no high or medium residual" % L, pc.get("verdict") == "fit_to_assemble"
             and not hi_med(pc.get("residual")) and not pc.get("blocking"),
             {"verdict": pc.get("verdict"), "hi_med": len(hi_med(pc.get("residual"))), "blocking": pc.get("blocking")})
        gate("lane %s: final check names the carrier's model" % L, fc.get("model") == model == meta.get("model")
             and (not fallback or "grader_fallback" in str(fc.get("grader_role", "")) + str(meta.get("grader_role", ""))),
             {"fc": fc.get("model"), "meta": meta.get("model"), "role": fc.get("grader_role") or meta.get("grader_role")})
        gate("lane %s: OW-6 final check fit_to_close over THIS corpus, no high or medium residual" % L,
             fc.get("verdict") == "fit_to_close" and fc.get("corpus_sha256") == CORPUS_PIN and not hi_med(fc.get("residual")),
             {"verdict": fc.get("verdict"), "corpus": str(fc.get("corpus_sha256"))[:16], "hi_med": len(hi_med(fc.get("residual")))})
        tc = fc.get("transcript_coverage") or {}
        gate("lane %s: transcript audit recorded OWED, NOT run" % L,
             isinstance(tc.get("attempts_with_no_transcript"), int) and tc.get("bytes_audited_by_stage1") == 0
             and tc.get("reconcile_verdict") == "NOT_RUN" and "OWED" in str(tc.get("statement", "")).upper()
             and fc.get("stage1_findings_disposition") == [],
             {k: tc.get(k) for k in ("attempts_with_no_transcript", "bytes_audited_by_stage1", "reconcile_verdict")})
        cga = fc.get("close_gate_assessment")
        cga = list(cga.values()) if isinstance(cga, dict) else (cga or [])
        unmet = [g for g in cga if not (isinstance(g, dict) and g.get("met") is True)]
        untyped = [g for g in unmet if not (isinstance(g, dict) and g.get("met") is False and g.get("type") in UNMET_TYPES)]
        gate("lane %s: close-gate assessment present; every unmet entry is typed deferred (OW-28) or owed (transcript audit)" % L,
             bool(cga) and not untyped, {"entries": len(cga), "unmet": len(unmet), "untyped": len(untyped)})
        typed = [g.get("type") for g in unmet if isinstance(g, dict)]
        met_typed = [g for g in cga if isinstance(g, dict) and g.get("met") is True and g.get("type") in UNMET_TYPES]
        gate("lane %s: the deferred Fable review and the owed transcript audit are both recorded, and neither as met" % L,
             all(t in typed for t in UNMET_TYPES) and not met_typed, {"typed_unmet": sorted(set(map(str, typed))), "met": len(met_typed)})
        gate("lane %s: items 20-23 fit_to_accept" % L,
             all((it.get("item_%d" % i) or {}).get("fit_to_accept") is True for i in range(20, 24)),
             {i: (it.get("item_%d" % i) or {}).get("fit_to_accept") for i in range(20, 24)})
        gate("lane %s: item 22 judged the feed bytes on disk" % L, feed_sha is not None
             and (it.get("item_22") or {}).get("feed_sha256") == feed_sha, str((it.get("item_22") or {}).get("feed_sha256"))[:16])
        nqs = sorted(k for k in nq if re.match(r"^NQ-\d+$", k))
        gate("lane %s: every named question answered" % L, bool(nqs) and all((nq.get(k) or {}).get("answer") for k in nqs), len(nqs))
        gate("lane %s: e19 self-report present" % L, bool(meta.get("e19_selfreport")), str(meta.get("e19_selfreport"))[:120])
        lanes[L] = {"attempt_id": att, "files": {k: ["sp_durable/Dan/merged_close/" + v.relative_to(landing.parent).as_posix(),
                                                     sha(v)] for k, v in files.items()},
                    "postcheck": pc, "final_check": fc, "items": it, "meta": meta, "named_questions": len(nqs),
                    "unmet": [{"gate": g.get("gate") or g.get("item") or g.get("id"), "type": g.get("type")}
                              for g in unmet if isinstance(g, dict)]}
    both = all(lanes.get(L) for L, _ in LANES)
    gate("two distinct blind lanes, both landed and both read", both and len({a for _, a in LANES}) == 2)
    if both:
        n = {L: lanes[L]["named_questions"] for L, _ in LANES}
        gate("both lanes answered the same named questions", len(set(n.values())) == 1, n)
    return lanes, sha(landing)


def scholar_gates():
    d = DAN / "scholar_record"
    have = {n: (d / n).is_file() for n in SCHOLAR_FILES}
    gate("scholar record installed (generator, checker, record, check record)", all(have.values()),
         [n for n, v in have.items() if not v])
    if not all(have.values()):
        gate("scholar record check says PASS", False, "not installed")
        gate("scholar record check is bound to the record's bytes", False, "not installed")
        return {}
    chk = jload(d / SCHOLAR_FILES[3])
    rec_sha = sha(d / SCHOLAR_FILES[2])
    # the check record's form was MEASURED on the installed file (work/probe4.py): VERDICT, FAILED, checks[].passed,
    # checks_total, checks_passed, and document / generator / checker each with name and sha256
    checks = chk.get("checks") or []
    said = {"VERDICT": chk.get("VERDICT"), "FAILED": len(chk.get("FAILED")) if isinstance(chk.get("FAILED"), list) else "ABSENT",
            "checks_total": chk.get("checks_total"), "checks_passed": chk.get("checks_passed")}
    gate("scholar record check says PASS", chk.get("VERDICT") == "PASS" and chk.get("FAILED") == [] and bool(checks)
         and chk.get("checks_total") == chk.get("checks_passed") == len(checks)
         and all(isinstance(c, dict) and c.get("passed") is True for c in checks), said)
    bound = {k: (chk.get(k) or {}).get("sha256") == sha(d / n) and (chk.get(k) or {}).get("name") == n
             for k, n in (("document", SCHOLAR_FILES[2]), ("generator", SCHOLAR_FILES[0]), ("checker", SCHOLAR_FILES[1]))}
    gate("scholar record check is bound to the record's bytes", all(bound.values()), bound)
    return {"record": "sp_durable/Dan/scholar_record/" + SCHOLAR_FILES[2], "record_sha256": rec_sha,
            "check": "sp_durable/Dan/scholar_record/" + SCHOLAR_FILES[3], "check_sha256": sha(d / SCHOLAR_FILES[3]),
            "check_said": said, "tier": "REPORTED by the installed checker's record; the checker is not run by this tool"}


def fable_gates(rows, side_sha):
    """OW-28: the least-confident rows and the routed items wait for the campaign-end review. The packet must reproduce,
    be built over this corpus, and hold exactly the low and medium_low rows with their installed sidecars."""
    gen, pkp = DAN / "fable_end_review" / "gen_fable_end_packet.py", DAN / "fable_end_review" / "Dan_fable_end_packet.v1.json"
    rp = DAN / "fable_end_review" / "routed_items.v1.jsonl"
    gate("routed items pinned", sha(rp) == ROUTED_PIN, sha(rp)[:16])
    have = gate("fable end packet and its generator installed", gen.is_file() and pkp.is_file())
    rc, tail = run(gen, "--check") if have else (1, "absent")
    gate("fable end packet reproduces (--check MATCH)", rc == 0 and tail == "MATCH", tail[:200])
    pk = jload(pkp) if have else {}
    low = sorted(r["decision_id"] for r in rows if r["confidence"] in ("low", "medium_low"))
    gate("fable end packet over this corpus, rows == low/medium_low", pk.get("corpus_sha256") == CORPUS_PIN
         and sorted(pk.get("row_ids") or []) == low, {"rows": len(pk.get("row_ids") or []), "want": len(low)})
    gate("fable end packet carries the %d routed items" % ROUTED_ITEMS, pk.get("routed_items_count") == ROUTED_ITEMS
         and len(pk.get("routed_item_ids") or []) == ROUTED_ITEMS, pk.get("routed_items_count"))
    gate("fable end packet carries the installed sidecars", side_sha is not None
         and (pk.get("sidecar_source") or {}).get("sha256") == side_sha, str((pk.get("sidecar_source") or {}).get("sha256"))[:16])
    gate("fable end packet records DEFERRED and no held row", str(pk.get("status", "")).startswith("DEFERRED (OW-28)")
         and pk.get("held_rows") == {}, str(pk.get("status"))[:40])
    return pk, sha_or_none(pkp)


def retention_gates(fixture):
    """Retention rows: every landed output and the three attempt-receipt files, by the paths the manifest names."""
    lp = DAN / LANDED_REL
    gate("landed-outputs manifest pinned", sha(lp) == LANDED_PIN, sha(lp)[:16])
    m = jload(fixture if fixture else lp)
    pre = "sp_durable/%s/" % BOOK
    ents = [(o.get("path"), o.get("sha256"), o.get("bytes")) for o in m.get("outputs") or []]
    recs = [(o.get("path"), o.get("sha256"), None) for o in m.get("receipt_files") or []]
    out, bad, rbad, drift = [], [], [], []
    rset = {str(r[0]) for r in recs}
    for rel, want, nbytes in sorted(ents + recs, key=lambda x: str(x[0])):
        rel = str(rel)
        is_rec = rel in rset
        sink = rbad if is_rec else bad
        if not rel.startswith(pre) or ".." in rel or "\\" in rel:
            sink.append(rel + ": not under " + pre)
            continue
        try:
            b = (M8 / rel).read_bytes()
        except OSError:
            sink.append(rel + ": unreadable")
            continue
        if is_rec:
            # An attempt-receipt file is append-only and keeps growing after the landed-outputs manifest was written
            # (MEASURED 2026-10-13: the review receipts file no longer has the manifest's digest). It is retained with
            # the bytes it has at close; a digest that moved is disclosed, not gated. It must be whole lines of LF bytes.
            if b"\r" in b or not b.endswith(b"\n"):
                rbad.append(rel + ": CR byte or no final newline")
                continue
            if shab(b) != want:
                drift.append({"path": rel, "sha256_in_landed_manifest": want, "sha256_now": shab(b), "bytes_now": len(b)})
        elif shab(b) != want or (nbytes is not None and len(b) != nbytes):
            bad.append(rel + ": bytes differ")
            continue
        out.append({"path": rel[len(pre):], "bytes": len(b), "sha256": shab(b)})
    paths = [e[0] for e in ents + recs]
    gate("every landed output is on disk with the manifest's digest and byte count",
         not bad and len(paths) == len(set(paths)) and bool(ents)
         and (fixture is not None or len(ents) == LANDED_OUTPUTS) and all(o.get("outcome") == "LANDED" for o in m.get("outputs") or []),
         {"outputs": len(ents), "bad": bad[:3]})
    gate("the three attempt-receipt files the landed manifest names are on disk, whole and LF-only",
         not rbad and len(recs) == len(rset) == LANDED_RECEIPT_FILES,
         {"receipt_files": len(recs), "bad": rbad[:3], "digest_moved_since_the_manifest": [x["path"] for x in drift]})
    return dump(out), out, drift


def target_gates(next_book):
    gate("book_chunks/Dan/chunks.jsonl absent", not (M8 / "book_chunks" / BOOK / "chunks.jsonl").exists())
    gate("receipts/Dan_completion.json absent", not (M8 / "receipts" / "Dan_completion.json").exists())
    gate("retention manifest absent", not (DAN / "dan_retention_manifest.v1.jsonl").exists())
    gate("no close lock is held", not (M8 / LOCK_NAME).exists(), LOCK_NAME)
    shared = {}
    for n in SHARED:
        b = (M8 / n).read_bytes()
        shared[n] = b
        gate("%s holds no Dan row" % n, '"book": "Dan"' not in b.decode("utf-8"))
        gate("%s is LF-only and ends with a newline" % n, b"\r" not in b and (not b or b.endswith(b"\n")))
    pb, mb = (M8 / "marathon_progress.yaml").read_bytes(), (M8 / "model_manifest.yaml").read_bytes()
    prog, man = pb.decode("utf-8"), mb.decode("utf-8")
    gate("marathon_progress anchors", prog.count(PROG_ANCHOR) == 1 and prog.endswith(PROG_ANCHOR)
         and prog.count("books_completed: %d\n" % BOOKS_BEFORE) == 1 and "  Dan:\n" not in prog and b"\r" not in pb)
    gate("model_manifest anchors", man.count("books_completed: %d\n" % BOOKS_BEFORE) == 1
         and man.count("current_book: Dan\n") == 1 and b"\r" not in mb)
    gate("--next-book given and valid (the owner's choice; OW-11 names no book after Daniel)",
         bool(next_book) and bool(NEXT_BOOK_RE.match(next_book or "")) and next_book != BOOK
         and ("  %s:\n" % next_book) not in prog, next_book)
    return prog, man, shared, pb, mb


# ------------------------------------------------------------------ close ------------------------------------------------
def commit(plan):
    """plan: [(relative path, new bytes, bytes the gates read or None when the file must be absent)]. All or nothing."""
    lock = M8 / LOCK_NAME
    fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    done, made = [], []
    try:
        os.write(fd, b"Dan close in progress\n")
        os.close(fd)
        for rel, new, old in plan:                       # nothing moved under us between the gates and the lock
            p = M8 / rel
            if b"\r" in new:
                raise RuntimeError("CR byte in the bytes for " + rel)
            if (old is None and p.exists()) or (old is not None and p.read_bytes() != old):
                raise RuntimeError("target changed since the gates read it: " + rel)
        for rel, new, old in plan:
            p = M8 / rel
            miss, q = [], p.parent
            while not q.exists():
                miss.append(q)
                q = q.parent
            for q in reversed(miss):
                q.mkdir()
                made.append(q)
            tmp = p.with_name(p.name + ".closetmp")
            with open(tmp, "xb") as fh:
                fh.write(new)
                fh.flush()
                os.fsync(fh.fileno())
            done.append((p, old))
            os.replace(tmp, p)
        for rel, new, old in plan:
            if sha(M8 / rel) != shab(new):
                raise RuntimeError("read-back digest differs: " + rel)
    except BaseException as e:  # noqa: BLE001
        errs = []
        for p, old in reversed(done):
            try:
                tmp = p.with_name(p.name + ".closetmp")
                if tmp.exists():
                    tmp.unlink()
                if old is None:
                    if p.exists():
                        p.unlink()
                else:
                    rb = p.with_name(p.name + ".rollbacktmp")
                    rb.write_bytes(old)
                    os.replace(rb, p)
            except OSError as e2:
                errs.append("%s: %s" % (p.name, e2))
        for q in reversed(made):
            try:
                q.rmdir()
            except OSError as e2:
                errs.append("%s: %s" % (q.name, e2))
        raise SystemExit("ROLLED BACK (%s: %s); rollback errors: %s" % (type(e).__name__, e, errs or "none"))
    finally:
        try:
            lock.unlink()
        except OSError:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("usage", nargs="?")
    ap.add_argument("--dry-report")
    ap.add_argument("--close", action="store_true")
    ap.add_argument("--m8-root")
    ap.add_argument("--acf", choices=("lam_pattern", "item22"))
    ap.add_argument("--next-book")
    ap.add_argument("--fixture-landed", help="dry-mode TEST HOOK: a landed-outputs manifest other than the pinned one")
    a = ap.parse_args()
    own = HERE.parent.parent
    if a.close and (a.m8_root or a.fixture_landed or a.dry_report):
        raise SystemExit("REFUSED: --close runs only on the tree this tool is installed in, with no test hook and no --dry-report")
    bind(Path(a.m8_root).resolve() if a.m8_root else own)
    if not a.m8_root and DAN != HERE:
        raise SystemExit("REFUSED: this file is not installed at <M8>/sp_durable/Dan; pass --m8-root to evaluate a tree")
    dry = None
    if a.dry_report:
        dry = Path(a.dry_report).resolve()
        for root in (M8, own if (own / "sp_durable" / BOOK) == HERE else M8):
            if dry == root or root in dry.parents:
                raise SystemExit("REFUSED: --dry-report is inside the M8 tree")
    usage = jload(a.usage[1:]) if a.usage and a.usage.startswith("@") else {}
    hooks = ["--fixture-landed"] if a.fixture_landed else []

    def imp():
        gate("dan_lib pinned", sha(DAN / "tools" / "dan_lib.py") == DAN_LIB_PIN, sha(DAN / "tools" / "dan_lib.py")[:16])
        sys.path.insert(0, str(DAN / "tools"))
        import dan_lib                                                                # noqa: E402
        return dan_lib
    dan_lib = guard("dan_lib", imp, None)
    rows, moved = guard("corpus", lambda: corpus_gates(dan_lib), (None, []))
    if rows is None:
        unmet = [g for g in GATES if not g["met"]]
        print(json.dumps({"mode": "CLOSE" if a.close else "DRY", "gates_total": len(GATES), "gates_unmet": len(unmet),
                          "unmet": unmet, "note": "the corpus could not be read; no other gate was evaluated"}, ensure_ascii=False, indent=1))
        raise SystemExit("REFUSED: the corpus could not be read; nothing written")
    man = guard("lineage", lambda: lineage_gates(rows), {})
    boss = guard("boss audit", boss_gates, {})
    side = guard("sidecars", lambda: sidecar_gates(rows), [])
    suite, pp, par = guard("evidence", evidence_gates, ({}, None, {}))
    carrier, model, shape, carrier_sha = guard("carrier", carrier_gates, ({}, None, {}, None))
    feed_p = DAN / "deliverables" / "atlas_candidate_feed_rows.jsonl"
    feed_sha = sha_or_none(feed_p)
    lanes, landing_sha = guard("lanes", lambda: lane_gates(model, carrier.get("fallback_in_force"), feed_sha), ({}, None))
    scholar = guard("scholar record", scholar_gates, {})
    pk, pk_sha = guard("fable end packet", lambda: fable_gates(rows, sha_or_none(DAN / "sidecar_src_dan.jsonl")), ({}, None))
    ret_bytes, ret, drift = guard("retention", lambda: retention_gates(Path(a.fixture_landed).resolve() if a.fixture_landed else None),
                                  (b"", [], []))
    prog, mant, shared, pb, mb = guard("targets", lambda: target_gates(a.next_book), (None, None, {}, None, None))
    gate("--acf chosen (the owner's choice between lam_pattern and item22)", a.acf is not None, a.acf)

    # --- payloads ---
    final = []
    for i, r in enumerate(rows, 1):
        fr = dict(r)
        fr["decision_id"] = "M8-%s-%03d" % (BOOK, i)
        final.append(fr)
    payload = dump(final)
    by = {s.get("writer_decision_id"): s for s in side}
    lcr, feq, acf_lam = [], [], []
    for r in final:
        s = by.get(r["writer_decision_id"])
        if not s:
            continue
        common = {"model_id": "M8_fable", "book": BOOK, "span": r["span"], "chunk_decision_id": r["decision_id"],
                  "confidence": r["confidence"], "review_packet_final_state": "accepted_candidate"
                  if r.get("candidate_hold_state") is None else "held_lower_confidence",
                  "chunk_review_status": r["review_status"], "candidate_hold_state": r.get("candidate_hold_state"),
                  "non_authorizing": True, "observed_substrate_signals": r["observed_substrate_signals"]}
        lcr.append({**common, "why_low_confidence": s.get("why_low_confidence")})
        feq.append({**common, "concern_type": s.get("concern_type"), "why_frontier_review_needed": s.get("why_frontier_review_needed")})
        acf_lam.append({**common, "concern_type": s.get("concern_type"), "why_low_confidence": s.get("why_low_confidence")})
    by_id = {r["decision_id"]: r for r in final}
    low_ids = {k for k, r in by_id.items() if r["confidence"] in ("low", "medium_low")}
    acf_item22 = guard("item-22 feed", lambda: jl(feed_p) if feed_sha else None, None)
    gate("item-22 feed installed; its rows name only chunks of this book", acf_item22 is not None
         and all(x.get("book") == BOOK and x.get("chunk_decision_id") in by_id for x in acf_item22),
         "deliverables/atlas_candidate_feed_rows.jsonl sha256 %s" % str(feed_sha)[:16])
    opts = {"lam_pattern": acf_lam, "item22": acf_item22}
    cov = {k: (coverage(v, by_id, low_ids) if v is not None else None) for k, v in opts.items()}
    acf = opts.get(a.acf)
    if a.acf:
        gate("atlas feed option %s meets the coverage validator's per-book rule" % a.acf,
             cov[a.acf] is not None and cov_ok(cov[a.acf]), cov_brief(cov[a.acf]) if cov[a.acf] else "option unavailable")
    for k, v in (("low_confidence_register", lcr), ("frontier_escalation_queue", feq)):
        c = coverage(v, by_id, low_ids)
        gate("%s rows meet the coverage validator's per-book rule" % k, cov_ok(c), cov_brief(c))
    shapes = collections.defaultdict(set)
    for x in guard("shared feed shapes", lambda: jl(M8 / "atlas_candidate_feed.jsonl"), []):
        shapes["%d_fields" % len(x)].add(str(x.get("book")))

    fcs = {L: v for L, v in sorted(lanes.items()) if v}
    conf = collections.Counter(r["confidence"] for r in final)
    ut = collections.Counter(str(r.get("unit_type")) for r in final)
    lang = collections.Counter(str(r.get("language")) for r in final)
    order = lambda c: dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))                 # noqa: E731
    sg = lambda k, ks: {x: (suite.get(k) or {}).get(x) for x in ks}                            # noqa: E731
    next_book = a.next_book if a.next_book else NEXT_PLACEHOLDER
    receipt = {
        "book": BOOK, "model_id": "M8_fable",
        "mesh_revision": "m8-mesh-r3 with the owner rulings in force at this close (ERROR_PATTERN_LEDGER.v1.md); grader "
                         "fallback OW-25; merged-verdict close OW-26; campaign-end Fable review deferred OW-28",
        "rows": len(final), "chunks": len(final), "parents": sorted({r["parent_collection"] for r in final}),
        "verses_covered": VERSES, "chapters": CHAPTERS, "chunk_file_sha256": shab(payload),
        "final_corpus": CORPUS, "final_corpus_sha256": CORPUS_PIN,
        "corpus_lineage_sha256": {BUILT_FROM + " (the source)": BUILT_FROM_PIN, "sp_durable/Dan/" + MANIFEST: MANIFEST_PIN,
                                  "sp_durable/Dan/" + CORPUS: CORPUS_PIN,
                                  "change_rule": man.get("change_rule"), "fields_changed_in_every_row": LINEAGE_FIELDS},
        "holds": "none: every row is candidate_review_complete with null hold fields (MEASURED by the close tool's gate)",
        "confidence_final": order(conf), "unit_type_distribution": order(ut), "language_distribution": order(lang),
        "language_layer": "H = Hebrew, A = Aramaic (2:4b to 7:28), mixed = a span holding both; derived by dan_lib.language_of",
        "numbering_disclosure": {"web_verses_whose_mt_reference_differs": len(moved),
                                 "first": "Dan.%d.%d" % moved[0] if moved else None,
                                 "last": "Dan.%d.%d" % moved[-1] if moved else None, "zone_chapters": ZONE,
                                 "spans_are_in": "WEB versification", "computed_by": "dan_lib.web_to_mt at close"},
        "grader_fallback": {"model": carrier.get("declared_fallback_model"), "replaces": carrier.get("ow13_grader_model"),
                            "statement": carrier.get("downgrade_statement"),
                            "carrier": "sp_durable/campaign/grader_models.v2.json", "carrier_sha256": carrier_sha},
        "ow26_merged_verdict_close": {"directive": shape.get("directive"), "shape": shape.get("shape"),
                                      "weakness_statement": shape.get("weakness_statement"),
                                      "transcript_audit": "OWED, NOT MET"},
        "transcript_audit": "OWED, NOT MET",
        "fable_end_review": {"status": "DEFERRED (OW-28)", "reviewer": "claude-fable-5-1, at the campaign's end",
                             "packet": "sp_durable/Dan/fable_end_review/Dan_fable_end_packet.v1.json",
                             "packet_sha256": pk_sha, "rows": pk.get("row_ids"),
                             "routed_items": pk.get("routed_items_count"), "routed_items_sha256": ROUTED_PIN,
                             "deferred_assessment_entries": {L: [u for u in v["unmet"] if u["type"] == UNMET_TYPES[0]]
                                                             for L, v in fcs.items()},
                             "limit": "DEFERRED is never MET. No Fable call is made without a new owner authorization (OW-30)."},
        "boss_audit": {"tier": "REPORTED", "records": boss, "conditions": "B1..B17 MET across e1 and e2 (e2 answers B8 and B14)"},
        "scholar_record": scholar,
        "campaign_close_gate_evidence": {
            "item5_cwo_execution_parity": {"record": "sp_durable/Dan/cwo/" + pp.name if pp else None,
                                           "sha256": sha_or_none(pp) if pp else None,
                                           "corpus_reconciled": par.get("post_corpus_sha256"), "status": par.get("status"),
                                           "exact_arm_residual": par.get("exact_arm_residual"), "routed_open": par.get("routed_open")},
            "item5_hebrew_quote_bytes_and_tier_labels": sg("citation_sweep", ("status", "nfd_degraded_count", "rows")),
            "item5_web_quote_gloss_fidelity": sg("web_quotes", ("status", "flag_count")),
            "item5_unicode_normalization": sg("hebrew_normalize_dryrun", ("ok", "fixed", "defect_count")),
            "item5_language_zones": sg("language_zones", ("status", "flag_count")),
            "item5_suite_report_sha256": SUITE_PIN,
            "item5_review_packet_retention": {"manifest": "sp_durable/Dan/dan_retention_manifest.v1.jsonl", "files": len(ret),
                                              "bytes": sum(o["bytes"] for o in ret), "manifest_sha256": shab(ret_bytes),
                                              "built_from": "sp_durable/Dan/" + LANDED_REL, "built_from_sha256": LANDED_PIN,
                                              "scope": "the landed outputs that manifest lists and the three attempt-receipt "
                                                       "files it names; not a walk of the review directory",
                                              "attempt_receipt_files_changed_since_that_manifest": drift},
            "item5_final_review_status": dict(sorted(collections.Counter(str(r.get("review_status")) for r in final).items())),
            "item10_ow6_final_check_merged": {
                "landing_manifest": "sp_durable/Dan/merged_close/landing_manifest.v1.json", "landing_manifest_sha256": landing_sha,
                "lanes": {L: {"attempt_id": v["attempt_id"], "files": v["files"], "model": v["final_check"].get("model"),
                              "postcheck_verdict": v["postcheck"].get("verdict"), "final_check_verdict": v["final_check"].get("verdict"),
                              "corpus_sha256_audited": v["final_check"].get("corpus_sha256"),
                              "transcript_coverage": v["final_check"].get("transcript_coverage"),
                              "unmet_assessment_entries": v["unmet"],
                              "items_20_23": {i: (v["items"].get(i) or {}).get("fit_to_accept") for i in
                                              ("item_20", "item_21", "item_22", "item_23")}} for L, v in fcs.items()},
                "authority": "OW-6 as amended for Daniel by OW-25 (declared fallback grader) and OW-26 (merged-verdict close; "
                             "stage-1 transcript audit OWED, NOT MET). One blind pair on one model family: one voice (OW-19)"},
        },
        "shared_feed_rows": {"low_confidence_register": len(lcr), "frontier_escalation_queue": len(feq),
                             "atlas_candidate_feed": {"source": a.acf, "rows": len(acf) if acf is not None else None}},
        "not_evaluated_by_this_tool": NOT_EVALUATED,
        "ow11": "Daniel is the last book the OW-11 authorization names. After this close the orchestration stops (OW-9); "
                "the next book is the owner's choice and was passed to this tool as --next-book.",
        "full_mesh_disclosure": "Anthropic-family mesh. Under OW-25 every role, graders included, runs on the declared "
                                "fallback model; author and grader share one set of weights. Intra-mesh agreement is "
                                "corroboration, never cross-provider evidence.",
        "usage_measured_subagent_tokens": usage.get("tokens", {}),
        "non_authorizing": True,
    }
    gate("receipt carries the carrier's downgrade statement", bool(carrier.get("downgrade_statement"))
         and shab(str(receipt["grader_fallback"]["statement"]).encode("utf-8")) == CARRIER_FACTS["downgrade_statement_sha256"])
    gate("receipt carries the OW-26 weakness statement", bool(receipt["ow26_merged_verdict_close"]["weakness_statement"])
         and receipt["ow26_merged_verdict_close"]["weakness_statement"] ==
         ((carrier.get("book_close_shapes") or {}).get(BOOK) or {}).get("weakness_statement"))
    rec_bytes = (json.dumps(receipt, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    new_prog = new_man = None
    if prog is not None:
        new_prog = prog.replace(PROG_ANCHOR, "  Ezek:\n    status: complete\n  Dan:\n    status: complete\ncurrent_book: %s\n" % next_book)
        new_prog = new_prog.replace("books_completed: %d\n" % BOOKS_BEFORE, "books_completed: %d\n" % BOOKS_AFTER)
        new_man = mant.replace("books_completed: %d\n" % BOOKS_BEFORE, "books_completed: %d\n" % BOOKS_AFTER).replace(
            "current_book: Dan\n", "current_book: %s\n" % next_book)
    writes = {"book_chunks/Dan/chunks.jsonl": payload, "sp_durable/Dan/dan_retention_manifest.v1.jsonl": ret_bytes,
              "receipts/Dan_completion.json": rec_bytes,
              "APPEND low_confidence_register.jsonl": dump(lcr), "APPEND frontier_escalation_queue.jsonl": dump(feq),
              "APPEND whole_bible_chunk_map.jsonl": payload}
    if acf is not None:
        writes["APPEND atlas_candidate_feed.jsonl"] = dump(acf)
    if new_prog is not None:
        writes["EDIT marathon_progress.yaml"] = new_prog.encode("utf-8")
        writes["EDIT model_manifest.yaml"] = new_man.encode("utf-8")
    gate("every close write is LF-only", all(b"\r" not in v for v in writes.values()))
    unmet = [g for g in GATES if not g["met"]]
    report = {"mode": "CLOSE" if a.close else "DRY", "book": BOOK, "gates_total": len(GATES), "gates_unmet": len(unmet),
              "unmet": [g["gate"] for g in unmet],
              "would_write": {k: {"bytes": len(v), "sha256": shab(v)} for k, v in writes.items()},
              "acf_options": {"rows": {k: (len(v) if v is not None else None) for k, v in opts.items()},
                              "coverage": {k: ({"meets_rule": cov_ok(v), **{f: (x if isinstance(x, int) else len(x))
                                                                          for f, x in v.items()}} if v else None)
                                           for k, v in cov.items()},
                              "shared_feed_shapes_by_book": {k: sorted(v) for k, v in sorted(shapes.items())}},
              "grader_model_from_carrier": model, "test_hooks_in_use": hooks,
              "tool_sha256": sha(Path(__file__).resolve()),
              "receipt_files_changed_since_the_manifest": drift,
              "deferred_never_met": {"fable_end_review": "DEFERRED (OW-28)", "packet_sha256": pk_sha,
                                     "transcript_audit": "OWED, NOT MET"},
              "next_book": a.next_book, "not_evaluated_by_this_tool": NOT_EVALUATED}

    if dry is not None:
        dry.mkdir(parents=True, exist_ok=True)
        pre = {"Dan_completion.preview.json": rec_bytes, "dan_retention_manifest.preview.jsonl": ret_bytes,
               "chunks.preview.jsonl": payload, "low_confidence_register.append.preview.jsonl": dump(lcr),
               "frontier_escalation_queue.append.preview.jsonl": dump(feq),
               "whole_bible_chunk_map.append.preview.jsonl": payload,
               "atlas_candidate_feed.append.lam_pattern.preview.jsonl": dump(acf_lam),
               "gates.json": (json.dumps(GATES, ensure_ascii=False, indent=1) + "\n").encode("utf-8")}
        if acf_item22 is not None:
            pre["atlas_candidate_feed.append.item22.preview.jsonl"] = dump(acf_item22)
        if new_prog is not None:
            pre["marathon_progress.preview.yaml"] = new_prog.encode("utf-8")
            pre["model_manifest.preview.yaml"] = new_man.encode("utf-8")
        report["previews"] = {k: {"bytes": len(v), "sha256": shab(v)} for k, v in sorted(pre.items())}
        pre["dry_report.json"] = (json.dumps({**report, "gates": GATES}, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
        for k, v in sorted(pre.items()):
            (dry / k).write_bytes(v)
    if not a.close:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return 0
    if unmet or acf is None or new_prog is None:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        raise SystemExit("REFUSED: %d gate(s) unmet; nothing written" % len(unmet))

    # --- CLOSE: the owner's act (OW-11 / OW-25). Every target was proven absent or anchored above; commit() proves it
    # again under the lock. Order as Ezekiel's tool wrote: chunks, retention, the four appends, the receipt, the carriers.
    plan = [("book_chunks/Dan/chunks.jsonl", payload, None),
            ("sp_durable/Dan/dan_retention_manifest.v1.jsonl", ret_bytes, None),
            ("low_confidence_register.jsonl", shared[SHARED[0]] + dump(lcr), shared[SHARED[0]]),
            ("frontier_escalation_queue.jsonl", shared[SHARED[1]] + dump(feq), shared[SHARED[1]]),
            ("atlas_candidate_feed.jsonl", shared[SHARED[2]] + dump(acf), shared[SHARED[2]]),
            ("whole_bible_chunk_map.jsonl", shared[SHARED[3]] + payload, shared[SHARED[3]]),
            ("receipts/Dan_completion.json", rec_bytes, None),
            ("marathon_progress.yaml", new_prog.encode("utf-8"), pb),
            ("model_manifest.yaml", new_man.encode("utf-8"), mb)]
    commit(plan)
    print(json.dumps({"status": "CLOSED", "chunks": len(final), "receipt_sha256": shab(rec_bytes),
                      "progress": "Dan complete -> %s (%d/66)" % (a.next_book, BOOKS_AFTER), "acf": a.acf,
                      "written": [p[0] for p in plan]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
