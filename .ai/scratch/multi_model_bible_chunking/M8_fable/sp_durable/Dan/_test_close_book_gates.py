#!/usr/bin/env python3
"""Gate tests for Daniel's _close_book.py. Non-authorizing. Never runs --close.

Each defect case builds its own private mirror of the M8 tree under --dest (which must lie outside the M8 tree and must
not exist yet), plants ONE defect, runs the tool with --m8-root on the mirror and requires the named gate(s) to be UNMET.
One clean mirror must show zero unmet gates. A close refuses on any unmet gate, so an UNMET gate is the refusal; the close
mode itself is never run here (see NOT_RUN).

The mirror is built from exactly named paths: no directory scan, no glob. Every file the test writes is tracked and removed
by name afterwards (unless --keep).

REAL copies (by exact path from --m8-root): the corpus, its lineage manifest and source, the suite report, the parity
record, dan_lib and its three data files, the routed items, the landed-outputs manifest, the two boss audit records, the
grader carrier (as a base), marathon_progress.yaml, model_manifest.yaml. The packet generator is the deliverable itself.
FIXTURES of the right FORM, each marked as a fixture (inputs that do not exist yet, or are forbidden to this builder):
see FIXTURES below.

Usage: _test_close_book_gates.py --m8-root M8 --dest DIR --result FILE [--tool F] [--gen F] [--keep] [--only SUBSTR]
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
PIN = "783a0e9ac2c8fe4c942b3b8f7dd65efaefdb28f6fcb55fdde42b500a5c395e09"
MODEL = "claude-opus-5-5"
D = "sp_durable/Dan/"
REAL = [D + "rows_v1_final.jsonl", D + "rows_v1_final.manifest.json", D + "fixup/draft_rows_fixup10_applied.jsonl",
        D + "rows_v1_final.jsonl.validator_report.json", D + "cwo/cwo_parity.rows_v1_final.json", D + "tools/dan_lib.py",
        D + "verse_inventory.json", D + "web_mt_verse_check.json", D + "dan_language_zones.json",
        D + "fable_end_review/routed_items.v1.jsonl", D + "close/dan_landed_outputs_manifest.v2.json",
        D + "review/boss/dan_boss_audit.v1.json", D + "review/boss/supp_e2/dan_boss_audit_b8_b14.json",
        "marathon_progress.yaml", "model_manifest.yaml"]
CARRIER = "sp_durable/campaign/grader_models.v2.json"
FIXTURES = [
    CARRIER + " (the real carrier plus a FIXTURE book_close_shapes.Dan)",
    "sp_durable/campaign/gen_grader_models_v2.py (FIXTURE: prints MATCH)", D + "_cwo_parity_dan.py (FIXTURE: prints the MATCH line)",
    D + "sidecar_src_dan.jsonl (FIXTURE rows over the corpus's low and medium_low rows)",
    D + "deliverables/gen_sidecars.py (FIXTURE: prints MATCH)", D + "deliverables/atlas_candidate_feed_rows.jsonl (FIXTURE)",
    D + "scholar_record/ four files (FIXTURE)", D + "merged_close/ lanes A and B and landing_manifest.v1.json (FIXTURE)",
    D + "dan_merged_close_attempt_receipts.jsonl (FIXTURE)",
    D + "close/FIXTURE_landed.json with three fixture outputs and three fixture receipt files, passed by --fixture-landed",
    "the four shared feed files, each one FIXTURE row of Ezekiel's form",
    D + "fable_end_review/Dan_fable_end_packet.v1.json (written in the mirror by the real generator over the fixture sidecars)"]
NOT_RUN = ["--close in any form: this builder never runs the close mode, not even on a mirror",
           "commit(): the lock, the under-lock recheck, the atomic replace and the rollback are untested by this builder; "
           "the opt-in --with-close-machinery cases exist for the orchestrator and were NOT RUN",
           "the tool's default root (installed at <M8>/sp_durable/Dan): only --m8-root was exercised"]
LANE_FILES = ("postcheck.json", "final_check.json", "items_20_23.json", "named_questions.json", "lane_meta.json", "final_message.md")
ATT = {"A": "dan_merged_close_lane_a_a1", "B": "dan_merged_close_lane_b_a1"}
SHARED = ("low_confidence_register.jsonl", "frontier_escalation_queue.jsonl", "atlas_candidate_feed.jsonl", "whole_bible_chunk_map.jsonl")
STUB = '# FIXTURE stand-in for a tool of the tree\nimport sys\nprint(%r)\nsys.exit(%d)\n'
CACHE = {}


def shab(b):
    return hashlib.sha256(b).hexdigest()


def jb(o):
    return (json.dumps(o, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def lb(rows):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8")


class Mirror:
    def __init__(self, root, real, tool, gen):
        self.root, self.tool, self.files, self.dirs = Path(root), tool, [], []
        os.makedirs(self.root)                                   # must not exist yet: no stale mirror is ever reused
        self.dirs.append(self.root)
        for rel in REAL:
            self.put(rel, CACHE.setdefault(rel, None) or CACHE.__setitem__(rel, (real / rel).read_bytes()) or CACHE[rel])
        rows = self.rows()
        car = json.loads(CACHE.setdefault(CARRIER, (real / CARRIER).read_bytes()).decode("utf-8-sig"))
        ws = "FIXTURE weakness statement: one blind pair on one model family; the transcript audit is owed."
        car.setdefault("book_close_shapes", {})["Dan"] = {
            "fixture": True, "shape": "FIXTURE merged_verdict_close", "directive": "OW-26",
            "transcript_audit": "OWED, NOT MET", "weakness_statement": ws, "weakness_statement_sha256": shab(ws.encode())}
        self.put(CARRIER, jb(car))
        self.put("sp_durable/campaign/gen_grader_models_v2.py", (STUB % ("MATCH", 0)).encode())
        self.put(D + "_cwo_parity_dan.py", (STUB % (json.dumps({"check": "MATCH", "status": "GREEN", "fixture": True}), 0)).encode())
        self.put(D + "deliverables/gen_sidecars.py", (STUB % ("MATCH", 0)).encode())
        low = [(i, r) for i, r in enumerate(rows, 1) if r["confidence"] in ("low", "medium_low")]
        self.put(D + "sidecar_src_dan.jsonl", lb([{
            "fixture": True, "writer_decision_id": r["writer_decision_id"], "concern_type": "FIXTURE concern",
            "why_low_confidence": "FIXTURE why " + r["writer_decision_id"], "why_frontier_review_needed": "FIXTURE need",
            "possible_downstream_risk": "FIXTURE risk", "suggested_reviewer": "FIXTURE reviewer",
            "proposed_atlas_action": "FIXTURE action"} for _, r in low]))
        feed = lb([{"fixture": True, "model_id": "M8_fable", "book": "Dan", "span": r["span"],
                    "chunk_decision_id": "M8-Dan-%03d" % i, "confidence": r["confidence"],
                    "review_packet_final_state": "accepted_candidate", "chunk_review_status": r["review_status"],
                    "candidate_hold_state": None, "non_authorizing": True} for i, r in low])
        self.put(D + "deliverables/atlas_candidate_feed_rows.jsonl", feed)
        rec = b"FIXTURE scholar record\n"
        self.put(D + "scholar_record/gen_scholar_record.py", b"# FIXTURE\n")
        self.put(D + "scholar_record/check_scholar_record.py", b"# FIXTURE\n")
        self.put(D + "scholar_record/DANIEL_SCHOLAR_RECORD.v1.md", rec)
        self.put(D + "scholar_record/scholar_record_check.v1.json", jb({
            "fixture": True, "schema": "dan_scholar_record_check.v1", "book": "Dan",
            "document": {"name": "DANIEL_SCHOLAR_RECORD.v1.md", "sha256": shab(rec)},
            "generator": {"name": "gen_scholar_record.py", "sha256": shab(b"# FIXTURE\n")},
            "checker": {"name": "check_scholar_record.py", "sha256": shab(b"# FIXTURE\n")},
            "checks": [{"check": "fixture_check", "passed": True}], "checks_total": 1, "checks_passed": 1, "FAILED": [],
            "VERDICT": "PASS"}))
        land = {"schema": "dan_merged_close_landing.v1", "fixture": True, "lanes": {}}
        for L, att in ATT.items():
            body = {
                "postcheck.json": {"fixture": True, "verdict": "fit_to_assemble", "residual": [], "blocking": []},
                "final_check.json": {
                    "fixture": True, "model": MODEL, "grader_role": "grader_fallback (OW-25)", "verdict": "fit_to_close",
                    "corpus_sha256": PIN, "residual": [], "stage1_findings_disposition": [],
                    "transcript_coverage": {"attempts_with_no_transcript": 0, "bytes_audited_by_stage1": 0,
                                            "reconcile_verdict": "NOT_RUN", "statement": "stage-1 transcript audit OWED, NOT MET"},
                    "close_gate_assessment": [
                        {"gate": "item 5", "met": True},
                        {"gate": "fable end review", "met": False, "type": "DEFERRED_OW28_FABLE_END_REVIEW"},
                        {"gate": "transcript audit", "met": False, "type": "OWED_TRANSCRIPT_AUDIT"}]},
                "items_20_23.json": {"fixture": True, "item_20": {"fit_to_accept": True}, "item_21": {"fit_to_accept": True},
                                     "item_22": {"fit_to_accept": True, "feed_sha256": shab(feed)}, "item_23": {"fit_to_accept": True}},
                "named_questions.json": {"fixture": True, "NQ-1": {"answer": "FIXTURE"}, "NQ-2": {"answer": "FIXTURE"}},
                "lane_meta.json": {"fixture": True, "model": MODEL, "grader_role": "grader_fallback",
                                   "e19_selfreport": "FIXTURE: ran no listing and no glob"}}
            ent = {"attempt_id": att, "files": {}}
            for fn in LANE_FILES:
                b = b"FIXTURE final message\n" if fn.endswith(".md") else jb(body[fn])
                rel = "lane_%s/%s" % (L.lower(), fn)
                self.put(D + "merged_close/" + rel, b)
                ent["files"][fn] = {"durable": rel, "sha256": shab(b)}
            land["lanes"][L] = ent
        self.put(D + "merged_close/landing_manifest.v1.json", jb(land))
        self.put(D + "dan_merged_close_attempt_receipts.jsonl", lb([
            {"fixture": True, "attempt_id": att, "record_kind": "completion", "outcome": "COMPLETED", "model_actual": MODEL}
            for att in ATT.values()]))
        outs, recs = [], []
        for n in ("out1.json", "out2.json", "final_message_fixture.md"):
            b = ("FIXTURE landed output %s\n" % n).encode()
            self.put(D + "fixture_out/" + n, b)
            outs.append({"execution_id": "fixture#e1", "attempt_id": "fixture", "outcome": "LANDED",
                         "path": D + "fixture_out/" + n, "sha256": shab(b), "bytes": len(b)})
        for n in ("r1.jsonl", "r2.jsonl", "r3.jsonl"):
            b = ("{\"fixture\": \"%s\"}\n" % n).encode()
            self.put(D + "fixture_out/" + n, b)
            recs.append({"path": D + "fixture_out/" + n, "sha256": shab(b)})
        self.put(D + "close/FIXTURE_landed.json", jb({"fixture": True, "outputs": outs, "receipt_files": recs}))
        for n in SHARED:
            self.put(n, lb([{"fixture": True, "model_id": "M8_fable", "book": "Ezek", "span": "Ezek.1.1-Ezek.1.3",
                             "chunk_decision_id": "M8-Ezek-001", "non_authorizing": True}]))
        gen_b = CACHE.setdefault("gen", Path(gen).read_bytes())
        self.put(D + "fable_end_review/gen_fable_end_packet.py", gen_b)
        pk = D + "fable_end_review/Dan_fable_end_packet.v1.json"
        if "packet" not in CACHE:
            p = subprocess.run([sys.executable, "-B", str(self.p(D + "fable_end_review/gen_fable_end_packet.py")), "--write"],
                               capture_output=True, text=True, encoding="utf-8", env=ENV)
            if p.returncode != 0:
                raise SystemExit("packet generator failed in the mirror: " + (p.stderr or p.stdout)[-300:])
            CACHE["packet"] = self.p(pk).read_bytes()
            self.files.append(self.p(pk))
        else:
            self.put(pk, CACHE["packet"])

    def p(self, rel):
        return self.root / rel

    def put(self, rel, b):
        p = self.p(rel)
        q, miss = p.parent, []
        while not q.exists():
            miss.append(q)
            q = q.parent
        for q in reversed(miss):
            q.mkdir()
            self.dirs.append(q)
        p.write_bytes(b)
        if p not in self.files:
            self.files.append(p)

    def get(self, rel):
        return self.p(rel).read_bytes()

    def rm(self, rel):
        self.p(rel).unlink()
        self.files.remove(self.p(rel))

    def sub(self, rel, old, new):
        b = self.get(rel)
        assert old in b, (rel, old)
        self.put(rel, b.replace(old, new, 1))

    def jedit(self, rel, fn):
        o = json.loads(self.get(rel).decode("utf-8-sig"))
        fn(o)
        self.put(rel, jb(o))

    def ledit(self, rel, fn):
        rows = [json.loads(l) for l in self.get(rel).decode("utf-8").split("\n") if l.strip()]
        r2 = fn(rows)
        self.put(rel, lb(rows if r2 is None else r2))

    def rows(self):
        return [json.loads(l) for l in self.get(D + "rows_v1_final.jsonl").decode("utf-8").split("\n") if l.strip()]

    def row(self, i, **kv):
        self.ledit(D + "rows_v1_final.jsonl", lambda rows: rows[i].update(kv))

    def lane(self, L, fn, mut):
        rel = D + "merged_close/lane_%s/%s" % (L.lower(), fn)
        self.jedit(rel, mut)
        s = shab(self.get(rel))
        self.jedit(D + "merged_close/landing_manifest.v1.json", lambda o: o["lanes"][L]["files"][fn].update(sha256=s))

    def args(self, **kw):
        a = {"--acf": "lam_pattern", "--next-book": "1Cor", "--fixture-landed": str(self.p(D + "close/FIXTURE_landed.json"))}
        a.update(kw)
        out = ["--m8-root", str(self.root)]
        for k, v in a.items():
            if v is not None:
                out += [k, v]
        return out

    def run(self, argv):
        p = subprocess.run([sys.executable, "-B", str(self.tool)] + argv, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", env=ENV)
        try:
            rep = json.loads(p.stdout)
        except ValueError:
            rep = None
        return p.returncode, rep, (p.stderr or "").strip()[-300:]

    def digest(self):
        return {str(p.relative_to(self.root).as_posix()): shab(p.read_bytes()) for p in self.files}

    def clean(self):
        for p in self.files:
            try:
                p.unlink()
            except OSError:
                pass
        for q in reversed(self.dirs):
            try:
                q.rmdir()
            except OSError:
                pass


ENV = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}
CASES = []


def case(name, expect, fn, **kw):
    CASES.append((name, [expect] if isinstance(expect, str) else list(expect), fn, kw))


def lg(L, s):
    return "lane %s: %s" % (L, s)


G_GROUP = "%s: every gate of this group could be evaluated"
ROWSF, MANF, SRCF = D + "rows_v1_final.jsonl", D + "rows_v1_final.manifest.json", D + "fixup/draft_rows_fixup10_applied.jsonl"
SUITE, PAR, SIDE = D + "rows_v1_final.jsonl.validator_report.json", D + "cwo/cwo_parity.rows_v1_final.json", D + "sidecar_src_dan.jsonl"
FEED, PKT = D + "deliverables/atlas_candidate_feed_rows.jsonl", D + "fable_end_review/Dan_fable_end_packet.v1.json"
LANDING, SCH = D + "merged_close/landing_manifest.v1.json", D + "scholar_record/"
G_COV = ["low_confidence_register rows meet the coverage validator's per-book rule",
         "frontier_escalation_queue rows meet the coverage validator's per-book rule"]
G_SHAPE = "carrier grants Daniel the OW-26 shape (book_close_shapes.Dan: shape, directive, transcript_audit, weakness_statement)"
G_RET = "every landed output is on disk with the manifest's digest and byte count"
G_RCP = "the three attempt-receipt files the landed manifest names are on disk, whole and LF-only"
G_NEXT = "--next-book given and valid (the owner's choice; OW-11 names no book after Daniel)"
G_PC = "postcheck fit_to_assemble, no high or medium residual"
G_FC = "OW-6 final check fit_to_close over THIS corpus, no high or medium residual"
G_TA = "transcript audit recorded OWED, NOT run"
G_CGA = "close-gate assessment present; every unmet entry is typed deferred (OW-28) or owed (transcript audit)"
G_DEF = "the deferred Fable review and the owed transcript audit are both recorded, and neither as met"
G_SIX = "six durable outputs match the landing manifest"
G_TWO = "two distinct blind lanes, both landed and both read"

# ---- corpus
case("corpus byte changed", "corpus pinned", lambda m: m.row(0, boundary_rationale="PLANTED"))
case("corpus CRLF line", "corpus is LF-only (E-73)", lambda m: m.sub(ROWSF, b"\n", b"\r\n"))
case("corpus row dropped", "corpus has 75 rows, every one of book Dan", lambda m: m.ledit(ROWSF, lambda r: r[:-1]))
case("corpus row of another book", "corpus has 75 rows, every one of book Dan", lambda m: m.row(9, book="Ezek"))
case("a row carries a hold", "every row candidate_review_complete with null hold fields; no row carries a hold",
     lambda m: m.row(4, candidate_hold_state="held_lower_confidence"))
case("a row not review-complete", "every row candidate_review_complete with null hold fields; no row carries a hold",
     lambda m: m.row(4, review_status="candidate"))
case("a hold field absent", "every row candidate_review_complete with null hold fields; no row carries a hold",
     lambda m: m.ledit(ROWSF, lambda r: r[7].pop("candidate_hold_basis") and None))
case("chunk index broken", "chunk_index 1..N", lambda m: m.row(2, chunk_index_in_book=99))
case("writer id repeated", "writer_decision_id unique and present", lambda m: m.row(1, writer_decision_id="W1-1"))
case("tiling gap", "tiling contiguous over 357 WEB verses in 12 chapters", lambda m: m.row(1, span=m.rows()[2]["span"]))
case("language label wrong", "language layer: each row's `language` is what dan_lib.language_of gives over its span",
     lambda m: m.row(0, language="A"))
case("parent run split", "each parent collection one contiguous run, PA..PJ in order",
     lambda m: m.row(0, parent_collection=m.rows()[74]["parent_collection"]))
case("numbering zone changed in dan_lib", ["dan_lib pinned", "numbering zone as measured: chapters 3-6, 66 WEB verses whose MT reference differs"],
     lambda m: m.put(D + "tools/dan_lib.py", m.get(D + "tools/dan_lib.py") + b"\nZONE_CHAPTERS = [3, 4, 5]\n"))
case("dan_lib byte changed", "dan_lib pinned", lambda m: m.put(D + "tools/dan_lib.py", m.get(D + "tools/dan_lib.py") + b"# planted\n"))
case("dan_lib absent (unevaluable is UNMET)", G_GROUP % "dan_lib", lambda m: m.rm(D + "tools/dan_lib.py"))
# ---- lineage
case("lineage manifest byte changed", "lineage manifest pinned", lambda m: m.put(MANF, m.get(MANF) + b"\n"))
case("lineage manifest row count", "lineage manifest names this corpus and its source", lambda m: m.jedit(MANF, lambda o: o.update(rows=74)))
case("lineage source changed", ["lineage source pinned", "the corpus differs from its source only where the manifest says (three status fields per row)"],
     lambda m: m.ledit(SRCF, lambda r: r[3].update(boundary_rationale="PLANTED")))
case("manifest change list wrong", "the corpus differs from its source only where the manifest says (three status fields per row)",
     lambda m: m.jedit(MANF, lambda o: o["changed"][sorted(o["changed"])[0]].append("span")))
case("manifest basis digest wrong", "lineage manifest's basis names the pinned boss audit records",
     lambda m: m.jedit(MANF, lambda o: o["basis"]["boss_audit_e1"].update(sha256="0" * 64)))
case("lineage source absent (unevaluable is UNMET)", G_GROUP % "lineage", lambda m: m.rm(SRCF))
# ---- boss audit
case("boss e1 condition not met", ["boss audit e1 pinned", "boss audit: conditions B1..B17 all MET across e1 and e2 (REPORTED)"],
     lambda m: m.jedit(D + "review/boss/dan_boss_audit.v1.json", lambda o: o["conditions"][2].update(verdict="NOT_MET")))
case("boss e2 answers another condition", ["boss audit e2 pinned", "boss audit e2 answers exactly B8 and B14"],
     lambda m: m.jedit(D + "review/boss/supp_e2/dan_boss_audit_b8_b14.json", lambda o: o["conditions"].append({"id": "B9", "verdict": "MET"})))
# ---- sidecars
case("sidecar source absent", "sidecar source present (sidecar_src_dan.jsonl)", lambda m: m.rm(SIDE))
case("sidecar row missing", ["sidecar set == low/medium_low rows", "atlas feed option lam_pattern meets the coverage validator's per-book rule"] + G_COV,
     lambda m: m.ledit(SIDE, lambda r: r[1:]))
case("sidecar row repeated", "sidecar set == low/medium_low rows", lambda m: m.ledit(SIDE, lambda r: r + r[:1]))
case("sidecar field empty", "sidecar fields present", lambda m: m.ledit(SIDE, lambda r: r[0].update(concern_type="")))
case("sidecar boilerplate", "why_low_confidence not boilerplate",
     lambda m: m.ledit(SIDE, lambda r: r[0].update(why_low_confidence=r[1]["why_low_confidence"])))
case("gen_sidecars check MISMATCH", "gen_sidecars.py --check MATCH",
     lambda m: m.put(D + "deliverables/gen_sidecars.py", (STUB % ("MISMATCH", 1)).encode()))
case("gen_sidecars absent", "gen_sidecars.py --check MATCH", lambda m: m.rm(D + "deliverables/gen_sidecars.py"))
# ---- evidence
case("suite not GREEN", ["suite report pinned", "suite GREEN over this corpus"], lambda m: m.jedit(SUITE, lambda o: o["summary"].update(hard_status="RED")))
case("suite over another file", "suite GREEN over this corpus", lambda m: m.jedit(SUITE, lambda o: o.update(rows_file="rows_v0.jsonl")))
case("normalize fixed a string", "normalize dry-run clean", lambda m: m.jedit(SUITE, lambda o: o["hebrew_normalize_dryrun"].update(fixed=1)))
case("citation sweep degraded", "Hebrew/Aramaic quote bytes and tier labels GREEN (citation sweep)",
     lambda m: m.jedit(SUITE, lambda o: o["citation_sweep"].update(nfd_degraded_count=1)))
case("WEB quote flagged", "WEB quote fidelity GREEN", lambda m: m.jedit(SUITE, lambda o: o["web_quotes"].update(flag_count=2)))
case("language zones not GREEN", "language zones GREEN", lambda m: m.jedit(SUITE, lambda o: o["language_zones"].update(status="RED")))
case("parity not GREEN", ["CWO parity record pinned", "CWO parity GREEN for THIS corpus"], lambda m: m.jedit(PAR, lambda o: o.update(status="RED")))
case("parity over another corpus", "CWO parity GREEN for THIS corpus", lambda m: m.jedit(PAR, lambda o: o.update(post_corpus_sha256="0" * 64)))
case("parity tool DIFFERS", "CWO parity record reproduces (_cwo_parity_dan.py --check MATCH, GREEN)",
     lambda m: m.put(D + "_cwo_parity_dan.py", (STUB % (json.dumps({"check": "DIFFERS", "status": "GREEN"}), 1)).encode()))
case("suite report absent (unevaluable is UNMET)", G_GROUP % "evidence", lambda m: m.rm(SUITE))
# ---- carrier
case("carrier generator MISMATCH", "grader carrier still transcribes the ledger (gen_grader_models_v2.py --check MATCH)",
     lambda m: m.put("sp_durable/campaign/gen_grader_models_v2.py", (STUB % ("MISMATCH", 1)).encode()))
case("carrier fallback not in force", "grader carrier states the measured fallback (OW-25)",
     lambda m: m.jedit(CARRIER, lambda o: o.update(fallback_in_force=False)))
case("carrier downgrade statement edited", ["grader carrier states the measured fallback (OW-25)", "receipt carries the carrier's downgrade statement"],
     lambda m: m.jedit(CARRIER, lambda o: o.update(downgrade_statement="PLANTED")))
case("carrier has no Dan shape", [G_SHAPE, "carrier's Daniel weakness statement matches its recorded digest", "receipt carries the OW-26 weakness statement"],
     lambda m: m.jedit(CARRIER, lambda o: o["book_close_shapes"].pop("Dan")))
case("carrier shape says the audit is MET", G_SHAPE, lambda m: m.jedit(CARRIER, lambda o: o["book_close_shapes"]["Dan"].update(transcript_audit="MET")))
case("carrier shape directive wrong", G_SHAPE, lambda m: m.jedit(CARRIER, lambda o: o["book_close_shapes"]["Dan"].update(directive="OW-6")))
case("carrier weakness digest wrong", "carrier's Daniel weakness statement matches its recorded digest",
     lambda m: m.jedit(CARRIER, lambda o: o["book_close_shapes"]["Dan"].update(weakness_statement_sha256="0" * 64)))
case("carrier absent (unevaluable is UNMET)", G_GROUP % "carrier", lambda m: m.rm(CARRIER))
# ---- lanes
case("landing manifest absent", ["landing manifest present (merged_close/landing_manifest.v1.json)", G_TWO], lambda m: m.rm(LANDING))
case("lane A file changed after landing", [lg("A", G_SIX), G_TWO],
     lambda m: m.put(D + "merged_close/lane_a/postcheck.json", m.get(D + "merged_close/lane_a/postcheck.json") + b"\n"))
case("lane B attempt id wrong", lg("B", G_SIX), lambda m: m.jedit(LANDING, lambda o: o["lanes"]["B"].update(attempt_id="dan_other_a1")))
case("lane B is lane A again (one lane landed twice)", lg("B", G_SIX),
     lambda m: m.jedit(LANDING, lambda o: o["lanes"].update(B=o["lanes"]["A"])))
case("lane A completion receipt FAILED", lg("A", "completion receipt COMPLETED on " + MODEL),
     lambda m: m.ledit(D + "dan_merged_close_attempt_receipts.jsonl", lambda r: r[0].update(outcome="FAILED")))
case("lane B ran on another model", lg("B", "completion receipt COMPLETED on " + MODEL),
     lambda m: m.ledit(D + "dan_merged_close_attempt_receipts.jsonl", lambda r: r[1].update(model_actual="claude-sonnet-5")))
case("receipts file absent", [lg("A", "completion receipt COMPLETED on " + MODEL), lg("B", "completion receipt COMPLETED on " + MODEL)],
     lambda m: m.rm(D + "dan_merged_close_attempt_receipts.jsonl"))
case("lane A postcheck not fit", lg("A", G_PC), lambda m: m.lane("A", "postcheck.json", lambda o: o.update(verdict="not_fit")))
case("lane B postcheck medium residual", lg("B", G_PC),
     lambda m: m.lane("B", "postcheck.json", lambda o: o.update(residual=[{"severity": "medium", "what": "PLANTED"}])))
case("lane A final check names Fable", lg("A", "final check names the carrier's model"),
     lambda m: m.lane("A", "final_check.json", lambda o: o.update(model="claude-fable-5-1")))
case("lane B final check not a fallback grader", lg("B", "final check names the carrier's model"),
     lambda m: (m.lane("B", "final_check.json", lambda o: o.update(grader_role="grader")),
                m.lane("B", "lane_meta.json", lambda o: o.update(grader_role="grader"))))
case("lane B final check conditional", lg("B", G_FC), lambda m: m.lane("B", "final_check.json", lambda o: o.update(verdict="fit_to_close_with_conditions")))
case("lane A final check over another corpus", lg("A", G_FC), lambda m: m.lane("A", "final_check.json", lambda o: o.update(corpus_sha256="0" * 64)))
case("lane A final check high residual", lg("A", G_FC),
     lambda m: m.lane("A", "final_check.json", lambda o: o.update(residual=[{"severity": "high", "what": "PLANTED"}])))
case("lane A transcript audit claimed run", lg("A", G_TA),
     lambda m: m.lane("A", "final_check.json", lambda o: o["transcript_coverage"].update(reconcile_verdict="PASS")))
case("lane B transcript bytes audited", lg("B", G_TA),
     lambda m: m.lane("B", "final_check.json", lambda o: o["transcript_coverage"].update(bytes_audited_by_stage1=10)))
case("lane A untyped unmet assessment entry", lg("A", G_CGA),
     lambda m: m.lane("A", "final_check.json", lambda o: o["close_gate_assessment"].append({"gate": "item 20", "met": False})))
case("lane B assessment absent", [lg("B", G_CGA), lg("B", G_DEF)],
     lambda m: m.lane("B", "final_check.json", lambda o: o.pop("close_gate_assessment")))
case("lane A records the deferred review as met (DEFERRED is never MET)", lg("A", G_DEF),
     lambda m: m.lane("A", "final_check.json", lambda o: o["close_gate_assessment"][1].update(met=True)))
case("lane B omits the owed transcript audit", lg("B", G_DEF),
     lambda m: m.lane("B", "final_check.json", lambda o: o["close_gate_assessment"].pop()))
case("lane B item 21 not accepted", lg("B", "items 20-23 fit_to_accept"),
     lambda m: m.lane("B", "items_20_23.json", lambda o: o["item_21"].update(fit_to_accept=False)))
case("lane A item 22 judged other feed bytes", lg("A", "item 22 judged the feed bytes on disk"),
     lambda m: m.lane("A", "items_20_23.json", lambda o: o["item_22"].update(feed_sha256="0" * 64)))
case("lane A named question unanswered", lg("A", "every named question answered"),
     lambda m: m.lane("A", "named_questions.json", lambda o: o["NQ-2"].update(answer="")))
case("lane B no e19 self-report", lg("B", "e19 self-report present"), lambda m: m.lane("B", "lane_meta.json", lambda o: o.pop("e19_selfreport")))
case("lanes answered different questions", "both lanes answered the same named questions",
     lambda m: m.lane("B", "named_questions.json", lambda o: o.update({"NQ-3": {"answer": "FIXTURE"}})))
# ---- scholar record
case("scholar check record absent", "scholar record installed (generator, checker, record, check record)",
     lambda m: m.rm(SCH + "scholar_record_check.v1.json"))
case("scholar check says FAIL", "scholar record check says PASS", lambda m: m.jedit(SCH + "scholar_record_check.v1.json", lambda o: o.update(VERDICT="FAIL")))
case("scholar sub-check not passed", "scholar record check says PASS",
     lambda m: m.jedit(SCH + "scholar_record_check.v1.json", lambda o: o["checks"][0].update(passed=False)))
case("scholar check lists a failure", "scholar record check says PASS",
     lambda m: m.jedit(SCH + "scholar_record_check.v1.json", lambda o: o.update(FAILED=["fixture_check"])))
case("scholar check counts disagree", "scholar record check says PASS",
     lambda m: m.jedit(SCH + "scholar_record_check.v1.json", lambda o: o.update(checks_passed=0)))
case("scholar record edited after its check", "scholar record check is bound to the record's bytes",
     lambda m: m.put(SCH + "DANIEL_SCHOLAR_RECORD.v1.md", b"PLANTED\n"))
case("scholar checker edited after its check", "scholar record check is bound to the record's bytes",
     lambda m: m.put(SCH + "check_scholar_record.py", b"# PLANTED\n"))
# ---- fable end packet
case("routed items changed", ["routed items pinned", "fable end packet reproduces (--check MATCH)"],
     lambda m: m.put(D + "fable_end_review/routed_items.v1.jsonl", m.get(D + "fable_end_review/routed_items.v1.jsonl") + b"\n"))
case("packet absent", "fable end packet and its generator installed", lambda m: m.rm(PKT))
case("packet row dropped", ["fable end packet reproduces (--check MATCH)", "fable end packet over this corpus, rows == low/medium_low"],
     lambda m: m.jedit(PKT, lambda o: o["row_ids"].pop()))
case("packet routed count wrong", "fable end packet carries the 46 routed items", lambda m: m.jedit(PKT, lambda o: o.update(routed_items_count=45)))
case("sidecars changed after the packet", ["fable end packet reproduces (--check MATCH)", "fable end packet carries the installed sidecars"],
     lambda m: m.ledit(SIDE, lambda r: r[0].update(possible_downstream_risk="PLANTED")))
case("packet says MET", "fable end packet records DEFERRED and no held row", lambda m: m.jedit(PKT, lambda o: o.update(status="MET")))
case("packet names a held row", "fable end packet records DEFERRED and no held row", lambda m: m.jedit(PKT, lambda o: o.update(held_rows={"W1-001": {}})))
# ---- retention
case("landed manifest changed", ["landed-outputs manifest pinned", "fable end packet reproduces (--check MATCH)"],
     lambda m: m.put(D + "close/dan_landed_outputs_manifest.v2.json", m.get(D + "close/dan_landed_outputs_manifest.v2.json") + b"\n"))
case("a landed output changed", G_RET, lambda m: m.put(D + "fixture_out/out1.json", b"PLANTED\n"))
case("a landed output absent", G_RET, lambda m: m.rm(D + "fixture_out/out2.json"))
case("an attempt-receipt file grew since the manifest: retained as it is, disclosed, not a refusal", [],
     lambda m: m.put(D + "fixture_out/r2.jsonl", m.get(D + "fixture_out/r2.jsonl") + b"{\"later\": 1}\n"), zero=True)
case("an attempt-receipt file absent", G_RCP, lambda m: m.rm(D + "fixture_out/r2.jsonl"))
case("an attempt-receipt file with a CR byte", G_RCP, lambda m: m.put(D + "fixture_out/r3.jsonl", b"{}\r\n"))
case("only two attempt-receipt files named", G_RCP, lambda m: m.jedit(D + "close/FIXTURE_landed.json", lambda o: o["receipt_files"].pop()))
case("a landed path outside Daniel (E-65)", G_RET,
     lambda m: m.jedit(D + "close/FIXTURE_landed.json", lambda o: o["outputs"][0].update(path="sp_durable/Ezek/x.json")))
case("an output not LANDED", G_RET, lambda m: m.jedit(D + "close/FIXTURE_landed.json", lambda o: o["outputs"][0].update(outcome="REJECTED")))
case("the real landed manifest without its 141 outputs on disk", G_RET, lambda m: None, args={"--fixture-landed": None})
# ---- targets
case("chunks already written", "book_chunks/Dan/chunks.jsonl absent", lambda m: m.put("book_chunks/Dan/chunks.jsonl", b"{}\n"))
case("receipt already written", "receipts/Dan_completion.json absent", lambda m: m.put("receipts/Dan_completion.json", b"{}\n"))
case("retention manifest already written", "retention manifest absent", lambda m: m.put(D + "dan_retention_manifest.v1.jsonl", b"{}\n"))
case("a close lock is held", "no close lock is held", lambda m: m.put("_close_book.Dan.lock", b"x\n"))
for _n in SHARED:
    case("%s already holds a Dan row" % _n, "%s holds no Dan row" % _n,
         lambda m, n=_n: m.put(n, m.get(n) + lb([{"model_id": "M8_fable", "book": "Dan"}])))
for _n in SHARED[:2]:
    case("%s has a CRLF" % _n, "%s is LF-only and ends with a newline" % _n, lambda m, n=_n: m.put(n, m.get(n).replace(b"\n", b"\r\n")))
for _n in SHARED[2:]:
    case("%s lacks its final newline" % _n, "%s is LF-only and ends with a newline" % _n, lambda m, n=_n: m.put(n, m.get(n)[:-1]))
case("a shared file absent (unevaluable is UNMET)", G_GROUP % "targets", lambda m: m.rm(SHARED[3]))
case("progress already counts 27", "marathon_progress anchors", lambda m: m.sub("marathon_progress.yaml", b"books_completed: 26", b"books_completed: 27"))
case("progress already lists Dan", "marathon_progress anchors",
     lambda m: m.sub("marathon_progress.yaml", b"current_book: Dan\n", b"  Dan:\n    status: complete\ncurrent_book: Dan\n"))
case("progress file has CRLF", ["marathon_progress anchors", "every close write is LF-only"],
     lambda m: m.put("marathon_progress.yaml", m.get("marathon_progress.yaml").replace(b"\n", b"\r\n")))
case("model manifest names another current book", "model_manifest anchors", lambda m: m.sub("model_manifest.yaml", b"current_book: Dan", b"current_book: Hos"))
case("model manifest already counts 27", "model_manifest anchors", lambda m: m.sub("model_manifest.yaml", b"books_completed: 26", b"books_completed: 27"))
# ---- the owner's choices
case("no --next-book", G_NEXT, lambda m: None, args={"--next-book": None})
case("--next-book Dan", G_NEXT, lambda m: None, args={"--next-book": "Dan"})
case("--next-book a closed book", G_NEXT, lambda m: None, args={"--next-book": "Ezek"})
case("--next-book not a book code", G_NEXT, lambda m: None, args={"--next-book": "x y"})
case("no --acf", "--acf chosen (the owner's choice between lam_pattern and item22)", lambda m: None, args={"--acf": None})
# ---- item-22 feed
case("item-22 feed absent", "item-22 feed installed; its rows name only chunks of this book", lambda m: m.rm(FEED))
case("item-22 feed row of another book (E-65)", "item-22 feed installed; its rows name only chunks of this book",
     lambda m: m.ledit(FEED, lambda r: r[0].update(book="Ezek")))
case("item-22 feed misses a low row", "atlas feed option item22 meets the coverage validator's per-book rule",
     lambda m: m.ledit(FEED, lambda r: r[1:]), args={"--acf": "item22"})
case("item-22 feed stale span", "atlas feed option item22 meets the coverage validator's per-book rule",
     lambda m: m.ledit(FEED, lambda r: r[0].update(span="Dan.1.1-Dan.1.2")), args={"--acf": "item22"})
case("item-22 chosen but feed absent", "atlas feed option item22 meets the coverage validator's per-book rule",
     lambda m: m.rm(FEED), args={"--acf": "item22"})


def unmet_names(rep):
    return [u["gate"] if isinstance(u, dict) else u for u in (rep or {}).get("unmet", [])]


def unit_cases(tool):
    spec = importlib.util.spec_from_file_location("close_book_under_test", str(tool))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    by = {"M8-Dan-001": {"span": "Dan.1.1-Dan.1.7", "confidence": "low", "review_status": "candidate_review_complete", "candidate_hold_state": None},
          "M8-Dan-002": {"span": "Dan.1.8-Dan.1.16", "confidence": "medium_low", "review_status": "candidate_review_complete", "candidate_hold_state": None}}
    low = set(by)

    def row(i, **kv):
        r = by[i]
        return {"chunk_decision_id": i, "span": r["span"], "confidence": r["confidence"], "chunk_review_status": r["review_status"],
                "candidate_hold_state": None, "review_packet_final_state": "accepted_candidate", **kv}
    a, b = row("M8-Dan-001"), row("M8-Dan-002")
    out = []
    for name, opt, key in (("coverage: exact set is clean", [a, b], None), ("coverage: duplicate counted", [a, b, b], "duplicates"),
                           ("coverage: missing row named", [a], "missing"),
                           ("coverage: orphan row named", [a, b, {**a, "chunk_decision_id": "M8-Dan-099"}], "orphan"),
                           ("coverage: stale confidence named", [a, row("M8-Dan-002", confidence="medium")], "stale"),
                           ("coverage: stale final state named", [a, row("M8-Dan-002", review_packet_final_state="held_lower_confidence")], "stale")):
        c = mod.coverage(opt, by, low)
        ok = mod.cov_ok(c) if key is None else (bool(c[key]) and not mod.cov_ok(c))
        out.append({"name": name, "kind": "unit", "pass": bool(ok), "detail": {k: (v if isinstance(v, int) else len(v)) for k, v in c.items()}})
    return out, mod


def close_machinery_cases(mod, dest):
    """OPT-IN, for the orchestrator. NOT RUN by the builder: it calls the close writer (on a scratch tree only)."""
    out = []
    root = dest / "close_machinery"
    os.makedirs(root)
    mod.bind(root)
    (root / "old.txt").write_bytes(b"old\n")
    mod.commit([("new/a.txt", b"a\n", None), ("old.txt", b"old\nmore\n", b"old\n")])
    out.append({"name": "commit: writes whole files and removes its lock", "kind": "close-machinery",
                "pass": (root / "new/a.txt").read_bytes() == b"a\n" and (root / "old.txt").read_bytes() == b"old\nmore\n"
                and not (root / mod.LOCK_NAME).exists()})
    for name, plan in (("commit: refuses a target that changed since the gates read it", [("b.txt", b"b\n", None), ("old.txt", b"x\n", b"old\n")]),
                       ("commit: refuses a CR byte", [("c.txt", b"c\r\n", None)])):
        try:
            mod.commit(plan)
            ok = False
        except SystemExit:
            ok = not (root / plan[0][0]).exists() and (root / "old.txt").read_bytes() == b"old\nmore\n" and not (root / mod.LOCK_NAME).exists()
        out.append({"name": name, "kind": "close-machinery", "pass": ok})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m8-root", required=True)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--result", required=True)
    ap.add_argument("--tool", default=str(HERE / "_close_book.py"))
    ap.add_argument("--gen", default=str(HERE / "fable_end_review" / "gen_fable_end_packet.py"))
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--with-close-machinery", action="store_true")
    a = ap.parse_args()
    real, dest, tool = Path(a.m8_root).resolve(), Path(a.dest).resolve(), Path(a.tool).resolve()
    if dest == real or real in dest.parents:
        raise SystemExit("REFUSED: --dest is inside the M8 tree")
    os.makedirs(dest)                                            # must be new
    tests = []

    def add(name, kind, ok, **kw):
        tests.append({"name": name, "kind": kind, "pass": bool(ok), **kw})

    # ---- the clean mirror
    m = Mirror(dest / "clean", real, tool, a.gen)
    before = m.digest()
    rc, rep, err = m.run(m.args())
    clean_gates = []
    add("clean mirror: zero unmet gates (lam_pattern)", "clean", rc == 0 and rep is not None and rep["gates_unmet"] == 0,
        gates_total=(rep or {}).get("gates_total"), unmet=unmet_names(rep), stderr=err)
    rc, rep2, err = m.run(m.args(**{"--acf": "item22"}))
    add("clean mirror: zero unmet gates (item22)", "clean", rc == 0 and rep2 is not None and rep2["gates_unmet"] == 0,
        unmet=unmet_names(rep2), stderr=err)
    outs = []
    for tag in ("dry_a", "dry_b"):
        rc, r3, err = m.run(m.args(**{"--dry-report": str(dest / tag)}))
        outs.append((rc, r3))
    names = sorted((outs[0][1] or {}).get("previews", {})) + ["dry_report.json"]
    same = [n for n in names if (dest / "dry_a" / n).read_bytes() == (dest / "dry_b" / n).read_bytes()] if outs[0][1] else []
    add("dry report: every gate listed MET, every preview written, second run byte-identical", "dry",
        outs[0][0] == 0 and outs[1][0] == 0 and len(names) >= 11 and same == names, files=len(names), identical=len(same))
    if outs[0][1]:
        full = json.loads((dest / "dry_a" / "dry_report.json").read_bytes().decode("utf-8"))
        clean_gates = [g["gate"] for g in full["gates"]]
        add("dry report: gates carry status and evidence; no CR in any preview", "dry",
            all(g["status"] == "MET" and g["met"] is True for g in full["gates"]) and len(clean_gates) == len(set(clean_gates))
            and not any(b"\r" in (dest / "dry_a" / n).read_bytes() for n in names), gates=len(clean_gates))
        rcp = json.loads((dest / "dry_a" / "Dan_completion.preview.json").read_bytes().decode("utf-8"))
        add("receipt preview: DEFERRED and OWED are recorded, never MET", "dry",
            rcp["fable_end_review"]["status"] == "DEFERRED (OW-28)" and rcp["transcript_audit"] == "OWED, NOT MET"
            and rcp["fable_end_review"]["packet_sha256"] == shab(m.get(PKT)) and rcp["rows"] == 75 and rcp["verses_covered"] == 357
            and full["deferred_never_met"]["transcript_audit"] == "OWED, NOT MET" and full["test_hooks_in_use"] == ["--fixture-landed"])
        ch = [json.loads(l) for l in (dest / "dry_a" / "chunks.preview.jsonl").read_bytes().decode("utf-8").split("\n") if l]
        add("chunks preview: 75 rows, decision ids M8-Dan-001..075", "dry",
            [c["decision_id"] for c in ch] == ["M8-Dan-%03d" % i for i in range(1, 76)])
        pv = (dest / "dry_a" / "marathon_progress.preview.yaml").read_bytes().decode("utf-8")
        mv = (dest / "dry_a" / "model_manifest.preview.yaml").read_bytes().decode("utf-8")
        add("carrier previews: 27 books, Dan complete, current_book is the owner's choice", "dry",
            pv.endswith("  Dan:\n    status: complete\ncurrent_book: 1Cor\n") and pv.count("books_completed: 27\n") == 1
            and mv.count("books_completed: 27\n") == 1 and mv.count("current_book: 1Cor\n") == 1 and "current_book: Dan" not in mv)
    add("dry report changed nothing in the mirror", "dry", m.digest() == before and not any(
        m.p(x).exists() for x in ("book_chunks/Dan/chunks.jsonl", "receipts/Dan_completion.json",
                                  D + "dan_retention_manifest.v1.jsonl", "_close_book.Dan.lock")), files=len(before))
    rc, _, err = m.run(m.args(**{"--dry-report": str(m.p("dry_inside"))}))
    add("--dry-report inside the tree is refused and writes nothing", "refusal", rc != 0 and "REFUSED" in err and not m.p("dry_inside").exists(), stderr=err[-120:])
    p = subprocess.run([sys.executable, "-B", str(tool)], capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
    add("run from outside a tree without --m8-root is refused", "refusal", p.returncode != 0 and "REFUSED" in (p.stderr or ""))
    dry_files = [dest / t / n for t in ("dry_a", "dry_b") for n in names]
    if not a.keep:
        m.clean()
        for f in dry_files:
            try:
                f.unlink()
            except OSError:
                pass
        for t in ("dry_a", "dry_b"):
            try:
                (dest / t).rmdir()
            except OSError:
                pass

    # ---- one mirror, one planted defect, per case
    planted = set()
    for i, (name, expect, fn, kw) in enumerate(CASES):
        if a.only and a.only not in name:
            continue
        m = Mirror(dest / ("case_%03d" % i), real, tool, a.gen)
        try:
            fn(m)
            rc, rep, err = m.run(m.args(**kw.get("args", {})))
            un = unmet_names(rep)
            ok = rep is not None and all(e in un for e in expect) and (bool(expect) or kw.get("zero"))
            if kw.get("zero"):
                ok = ok and rep["gates_unmet"] == 0 and len(rep.get("receipt_files_changed_since_the_manifest") or []) == 1
            planted.update(expect)
            add(name, "defect", ok, expect=expect, unmet_count=len(un), also_unmet=[u for u in un if u not in expect][:8],
                **({} if ok else {"stderr": err}))
        except Exception as e:  # noqa: BLE001
            add(name, "defect", False, expect=expect, error="%s: %s" % (type(e).__name__, e))
        finally:
            if not a.keep:
                m.clean()
    units, mod = unit_cases(tool)
    tests += units
    if a.with_close_machinery:
        tests += close_machinery_cases(mod, dest)
    failed = [t["name"] for t in tests if not t["pass"]]
    result = {
        "command": "python -B " + " ".join([Path(sys.argv[0]).name] + sys.argv[1:]),
        "tool_sha256": shab(tool.read_bytes()), "generator_sha256": shab(Path(a.gen).read_bytes()),
        "tests_total": len(tests), "passed": len(tests) - len(failed), "failed": failed,
        "gates_in_clean_run": len(clean_gates),
        "clean_gates_with_no_planted_defect": sorted({g.replace("lane B:", "lane A:") for g in clean_gates} - {
            g.replace("lane B:", "lane A:") for g in planted}) if not a.only else "not computed (--only)",
        "clean_gates_note": "lane A and lane B gates are one gate run twice; a defect planted in either lane counts for both",
        "planted_gates_not_in_clean_run": sorted(g for g in planted if g not in clean_gates and "could be evaluated" not in g
                                                 and not g.startswith("atlas feed option item22")),
        "fixtures": FIXTURES, "real_copies": REAL, "not_run": NOT_RUN + ([] if a.with_close_machinery else ["--with-close-machinery cases"]),
        "limit": "A defect case passes when every expected gate is UNMET; other gates may be UNMET too (also_unmet). The tool was "
                 "never run in close mode; refusal is shown by the unmet gate, which the close path refuses on.",
        "tests": tests}
    Path(a.result).write_bytes(jb(result))
    print(json.dumps({k: result[k] for k in ("tests_total", "passed", "failed", "gates_in_clean_run",
                                             "clean_gates_with_no_planted_defect", "planted_gates_not_in_clean_run")}, ensure_ascii=False, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
