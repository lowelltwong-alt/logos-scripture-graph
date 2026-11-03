#!/usr/bin/env python3
"""Gate tests for the book-agnostic campaign/_close_book.py. Ported from sp_durable/Dan/_test_close_book_gates.py. Non-authorizing.

Each defect case builds its own private mirror of the M8 tree under --dest (which must lie outside the M8 tree and must not exist
yet), plants ONE defect, runs the tool with --m8-root on the mirror and requires the named gate(s) to be UNMET. One clean mirror
must show zero unmet gates. The port adds what the port of the tool adds: a PENDING pin, a gate-family switch without a reason, a
switch the bytes do not bear out, an unreadable corpus. It also proves --close on PRIVATE MIRRORS ONLY: a copy of the tool is
installed in the mirror, because --close refuses --m8-root, so it cannot be pointed at any other tree from here.

Book-agnostic: every name and count comes from the book's close parameters. A pinned input that exists is copied by exact path; a
pin still PENDING means the input does not exist yet, and a FIXTURE of the right FORM, marked as a fixture, stands in for it, with
its measured digest written into the mirror's own parameter file only. The mirror's parameters always run the mirror's copies of
the campaign tools. No directory scan, no glob, no clock, no randomness.

Usage: _test_close_book_gates.py --book BOOK --m8-root M8 --dest DIR --result FILE [--params F] [--tool F] [--gen F]
         [--carrier-base REL] [--extra-real REL]... [--keep] [--only SUBSTR] [--jobs N]
  --carrier-base  the carrier the mirror's carrier is built on (a template of FORM: the fixture shape replaces the book's)
  --extra-real    a book-relative data file a `module` lookup reads; repeat it. Named here because a lookup's data is not a parameter.
"""
import argparse
import concurrent.futures
import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
PENDING = "PENDING"
ap = argparse.ArgumentParser()
ap.add_argument("--book", required=True)
ap.add_argument("--m8-root", required=True)
ap.add_argument("--dest", required=True)
ap.add_argument("--result", required=True)
ap.add_argument("--params")
ap.add_argument("--tool", default=str(HERE / "_close_book.py"))
ap.add_argument("--gen", default=str(HERE / "gen_fable_end_packet.py"))
ap.add_argument("--carrier-base", default="sp_durable/campaign/grader_models.v2.json")
ap.add_argument("--extra-real", action="append", default=[])
ap.add_argument("--keep", action="store_true")
ap.add_argument("--only")
ap.add_argument("--jobs", type=int, default=6)
A = ap.parse_args()
BOOK, REAL_ROOT = A.book, Path(A.m8_root).resolve()
PARAMS_PATH = Path(A.params).resolve() if A.params else REAL_ROOT / "sp_durable" / BOOK / "close" / "close_params.v1.json"
DOC = json.loads(PARAMS_PATH.read_bytes().decode("utf-8"))
if DOC.get("schema") != "m8_close_params.v1" or DOC.get("book") != BOOK:
    raise SystemExit("REFUSED: %s is not the close parameters of %s" % (PARAMS_PATH, BOOK))
C = DOC["constants"]
D = "sp_durable/%s/" % BOOK
MODEL = C["CARRIER_FACTS"]["declared_fallback_model"]
LOOKUP = C["LOOKUP"]
LANG_ON = C["FAMILIES"]["language_layer"].get("enabled") is True
ROUTED_N = 2 if C["ROUTED_ITEMS"] == PENDING else C["ROUTED_ITEMS"]
NKEY = "FIXTURE_normalize_dryrun" if C["SUITE_NORMALIZE_KEY"] == PENDING else C["SUITE_NORMALIZE_KEY"]
NEXT = C["NEXT_BOOK_EXPECTED"] or "1Cor"
ATT = dict(C["LANES"])
SF = C["SCHOLAR_FILES"]
LANE_FILES = C["LANE_FILES"]
SHARED = C["SHARED"]
STUB = '# FIXTURE stand-in for a tool of the tree\nimport sys\nprint(%r)\nsys.exit(%d)\n'
ROWSF, MANF, SRCF = D + C["CORPUS"], D + C["MANIFEST"], C["BUILT_FROM"]
SUITE, PAR = ROWSF + ".validator_report.json", D + "cwo/cwo_parity.%s.json" % C["CORPUS"].replace(".jsonl", "")
SIDE, FEED, PKT = D + C["SIDECAR"], D + C["FEED_REL"], D + C["PACKET_REL"]
LANDING, SCH, LIBF = D + C["LANDING_REL"], D + "scholar_record/", D + LOOKUP["path"]
LDIR = LANDING.rsplit("/", 1)[0] + "/"
MRCP, ROUTEDF, LANDEDF, GENSIDE = D + C["MERGED_RECEIPTS_REL"], D + C["ROUTED_REL"], D + C["LANDED_REL"], D + C["GEN_SIDECARS_REL"]
CARRIER, CGEN = "sp_durable/" + C["CARRIER_REL"], "sp_durable/" + C["CARRIER_GEN_REL"]
PARTOOL, GENF, TOOLF = "sp_durable/campaign/_cwo_parity.py", "sp_durable/campaign/gen_fable_end_packet.py", "sp_durable/campaign/_close_book.py"
PARF, BOSS1 = D + "close/close_params.v1.json", D + C["BOSS"][0][1]
FIXL = D + "close/FIXTURE_landed.json"
CHUNKS, RECEIPT = "book_chunks/%s/chunks.jsonl" % BOOK, "receipts/%s_completion.json" % BOOK
B_BEFORE = ("books_completed: %d" % C["BOOKS_BEFORE"]).encode()
B_AFTER = ("books_completed: %d" % C["BOOKS_AFTER"]).encode()
CUR_LINE = ("current_book: %s\n" % BOOK).encode()
LISTED = ("  %s:\n    status: complete\ncurrent_book: %s\n" % (BOOK, BOOK)).encode()
G_GROUP = "%s: every gate of this group could be evaluated"
G_PEND = "no parameter is PENDING (every pin measured from disk)"
G_LIB = "%s pinned" % LOOKUP["label"]
G_N = "corpus has %s rows, every one of book %s" % (C["ROWS"], BOOK)
G_TILE = "tiling contiguous over %s WEB verses in %s chapters" % (C["VERSES"], C["CHAPTERS"])
G_LANG = ("language layer: each row's `language` is what %s.language_of gives over its span" % LOOKUP["label"] if LANG_ON
          else "language layer off: every row carries the one declared language value")
G_ZOFF = "numbering zone off: the lookup moves no verse and the parameters declare no zone"
G_LOFF = "language layer off: every row carries the one declared language value"
G_ZONE = "numbering zone as measured: chapters %s, %s WEB verses whose MT reference differs" % (C["ZONE_LABEL"], C["ZONE_MOVED"])
G_PARENT = "each parent collection one contiguous run, %s in order" % C["PARENTS_LABEL"]
G_B1P = "boss audit %s pinned" % C["BOSS"][0][0]
G_BOSS = "boss audit: conditions %s (REPORTED)" % C["BOSS_CONDITIONS_LABEL"]
G_QB, G_ROUTED = C["TEXT"]["quote_bytes_gate"], "fable end packet carries the %s routed items" % ROUTED_N
G_PAR_T = "CWO parity record reproduces (_cwo_parity.py --check MATCH, GREEN)"
G_CGEN = "grader carrier still transcribes the ledger (%s --check MATCH)" % Path(C["CARRIER_GEN_REL"]).name
G_WK = "carrier's %s weakness statement matches its recorded digest" % C["BOOK_NAME"]
G_COV = ["low_confidence_register rows meet the coverage validator's per-book rule",
         "frontier_escalation_queue rows meet the coverage validator's per-book rule"]
G_SHAPE = "carrier grants %s the OW-26 shape (book_close_shapes.%s: shape, directive, transcript_audit, weakness_statement)" % (C["BOOK_NAME"], BOOK)
G_RET = "every landed output is on disk with the manifest's digest and byte count"
G_RCP = "the three attempt-receipt files the landed manifest names are on disk, whole and LF-only"
G_NEXT = "--next-book given and valid (%s)" % C["NEXT_BOOK_LABEL"]
G_PC = "postcheck fit_to_assemble, no high or medium residual"
G_FC = "OW-6 final check fit_to_close over THIS corpus, no high or medium residual"
G_TA = "transcript audit recorded OWED, NOT run"
G_CGA = "close-gate assessment present; every unmet entry is typed deferred (OW-28) or owed (transcript audit)"
G_DEF = "the deferred Fable review and the owed transcript audit are both recorded, and neither as met"
G_SIX = "six durable outputs match the landing manifest"
G_TWO = "two distinct blind lanes, both landed and both read"
G_LF = "every close write is LF-only"
G_I22 = "item-22 feed installed; its rows name only chunks of this book"
ENV = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}
FIXTURES, REAL_COPIES = [], []
CASES = []


def shab(b):
    return hashlib.sha256(b).hexdigest()


def jb(o):
    return (json.dumps(o, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def lb(rows):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8")


def real(rel):
    if rel not in REAL_COPIES:
        REAL_COPIES.append(rel)
    return (REAL_ROOT / rel).read_bytes()


def fx(note):
    if note not in FIXTURES:
        FIXTURES.append(note)


def build_base(dest, closeable):
    """{relative path: bytes} of a mirror whose every gate should pass, and its parameter document."""
    P = copy.deepcopy(DOC)
    K, B = P["constants"], {}
    K.update(PARITY_TOOL="campaign/_cwo_parity.py", PARITY_ARGS=["--book", BOOK, "--check"],
             PACKET_GEN="campaign/gen_fable_end_packet.py", PACKET_GEN_ARGS=["--book", BOOK, "--check"])
    fx(PARF + " (the book's parameters, with the digests of the fixtures below, and PARITY_TOOL and PACKET_GEN at the mirror's campaign copies)")
    for k in ("rulings", "hand_record"):
        if K["CWO"].get(k) == PENDING:
            K["CWO"][k] = "FIXTURE"
            fx(PARF + " CWO.%s (PENDING on the real tree; a marked fixture value here, read only by the stub parity tool of the mirror)" % k)
    B[SRCF], B[LIBF] = real(SRCF), real(LIBF)
    for rel in A.extra_real:
        B[D + rel] = real(D + rel)
    for i, (tag, rel, pin) in enumerate(K["BOSS"]):
        if pin == PENDING:
            b = jb({"fixture": True, "conditions": [{"id": "B%d" % n, "verdict": "MET"} for n in (1, 2, 3)]})
            K["BOSS"][i][2], K["BOSS_CONDITIONS"] = shab(b), ["B1", "B2", "B3"]
            fx(D + rel + " (FIXTURE boss audit, three conditions MET)")
        else:
            b = real(D + rel)
        B[D + rel] = b
    if K["CORPUS_PIN"] == PENDING:
        src = [json.loads(x) for x in B[SRCF].decode("utf-8").split("\n") if x.strip()]
        out = []
        for r in src:
            new = {}
            for k, v in r.items():
                if k == "review_status":
                    new.update(K["HOLD_FIELDS"])
                else:
                    new[k] = v
            out.append(new)
        B[ROWSF] = lb(out)
        K["CORPUS_PIN"] = shab(B[ROWSF])
        B[MANF] = jb({"fixture": True, "names": ROWSF, "sha256": K["CORPUS_PIN"], "rows": K["ROWS"], "built_from": SRCF,
                      "built_from_sha256": K["BUILT_FROM_PIN"], "change_rule": "FIXTURE",
                      "changed": {r["writer_decision_id"]: K["LINEAGE_FIELDS"] for r in out},
                      "basis": {"boss_audit_" + t: {"sha256": p} for t, _, p in K["BOSS"]}})
        K["MANIFEST_PIN"] = shab(B[MANF])
        fx(ROWSF + " (FIXTURE: the real source rows with the hold fields, as the row builder makes them)")
        fx(MANF + " (FIXTURE of the lineage manifest's form)")
    else:
        B[ROWSF], B[MANF] = real(ROWSF), real(MANF)
    rows = [json.loads(x) for x in B[ROWSF].decode("utf-8").split("\n") if x.strip()]
    if K["SUITE_PIN"] == PENDING:
        B[SUITE] = jb({"fixture": True, "rows_file": K["CORPUS"], "summary": {"hard_status": "GREEN", "nfd_hard_e01": False},
                       NKEY: {"ok": True, "fixed": 0, "defect_count": 0},
                       "citation_sweep": {"status": "GREEN", "nfd_degraded_count": 0, "rows": K["ROWS"]},
                       "web_quotes": {"status": "GREEN", "flag_count": 0}, "language_zones": {"status": "GREEN", "flag_count": 0}})
        K["SUITE_PIN"], K["SUITE_NORMALIZE_KEY"] = shab(B[SUITE]), NKEY
        fx(SUITE + " (FIXTURE of the suite report's form; its normalize key is a fixture name)")
    else:
        B[SUITE] = real(SUITE)
    if K["PARITY_PIN"] == PENDING:
        B[PAR] = jb({"fixture": True, "post_corpus_sha256": K["CORPUS_PIN"], "status": "GREEN", "exact_arm_residual": [], "routed_open": []})
        K["PARITY_PIN"] = shab(B[PAR])
        fx(PAR + " (FIXTURE of the parity record's form)")
    else:
        B[PAR] = real(PAR)
    car = json.loads(real(A.carrier_base).decode("utf-8-sig"))
    ws = "FIXTURE weakness statement: one blind pair on one model family; the transcript audit is owed."
    car.setdefault("book_close_shapes", {})[BOOK] = {
        "fixture": True, "shape": "FIXTURE merged_verdict_close", "directive": "OW-26", "granted_by": K["SHAPE_GRANTED_BY"],
        "transcript_audit": "OWED, NOT MET", "weakness_statement": ws, "weakness_statement_sha256": shab(ws.encode())}
    B[CARRIER] = jb(car)
    fx(CARRIER + " (the carrier named by --carrier-base, as a template of FORM, plus a FIXTURE book_close_shapes entry)")
    B[CGEN] = (STUB % ("MATCH", 0)).encode()
    B[PARTOOL] = (STUB % (json.dumps({"check": "MATCH", "status": "GREEN", "fixture": True}), 0)).encode()
    B[GENSIDE] = (STUB % ("MATCH", 0)).encode()
    fx(CGEN + ", " + PARTOOL + " and " + GENSIDE + " (FIXTURE stubs printing MATCH: the real parity tool's sweep cannot run in a mirror)")
    low = [(i, r) for i, r in enumerate(rows, 1) if r["confidence"] in ("low", "medium_low")]
    B[SIDE] = lb([dict({"fixture": True, "writer_decision_id": r["writer_decision_id"]},
                       **{f: "FIXTURE %s %s" % (f, r["writer_decision_id"]) for f in K["SIDE_FIELDS"]}) for _, r in low])
    B[FEED] = lb([{"fixture": True, "model_id": K["MODEL_ID"], "book": BOOK, "span": r["span"],
                   "chunk_decision_id": K["DECISION_ID_FORM"] % i, "confidence": r["confidence"],
                   "review_packet_final_state": "accepted_candidate", "chunk_review_status": r["review_status"],
                   "candidate_hold_state": None, "non_authorizing": True} for i, r in low])
    fx(SIDE + " and " + FEED + " (FIXTURE rows over the corpus's low and medium_low rows)")
    rec = b"FIXTURE scholar record\n"
    B[SCH + SF[0]], B[SCH + SF[1]], B[SCH + SF[2]] = b"# FIXTURE\n", b"# FIXTURE\n", rec
    B[SCH + SF[3]] = jb({
        "fixture": True, "book": BOOK, "document": {"name": SF[2], "sha256": shab(rec)},
        "generator": {"name": SF[0], "sha256": shab(b"# FIXTURE\n")}, "checker": {"name": SF[1], "sha256": shab(b"# FIXTURE\n")},
        "checks": [{"check": "fixture_check", "passed": True}], "checks_total": 1, "checks_passed": 1, "FAILED": [], "VERDICT": "PASS"})
    fx(SCH + " four files (FIXTURE)")
    land = {"fixture": True, "lanes": {}}
    for L, att in ATT.items():
        body = {
            "postcheck.json": {"fixture": True, "verdict": "fit_to_assemble", "residual": [], "blocking": []},
            "final_check.json": {
                "fixture": True, "model": MODEL, "grader_role": "grader_fallback (OW-25)", "verdict": "fit_to_close",
                "corpus_sha256": K["CORPUS_PIN"], "residual": [], "stage1_findings_disposition": [],
                "transcript_coverage": {"attempts_with_no_transcript": 0, "bytes_audited_by_stage1": 0,
                                        "reconcile_verdict": "NOT_RUN", "statement": "stage-1 transcript audit OWED, NOT MET"},
                "close_gate_assessment": [
                    {"gate": "item 5", "met": True},
                    {"gate": "fable end review", "met": False, "type": K["UNMET_TYPES"][0]},
                    {"gate": "transcript audit", "met": False, "type": K["UNMET_TYPES"][1]}]},
            "items_20_23.json": {"fixture": True, "item_20": {"fit_to_accept": True}, "item_21": {"fit_to_accept": True},
                                 "item_22": {"fit_to_accept": True, "feed_sha256": shab(B[FEED])}, "item_23": {"fit_to_accept": True}},
            "named_questions.json": {"fixture": True, "NQ-1": {"answer": "FIXTURE"}, "NQ-2": {"answer": "FIXTURE"}},
            "lane_meta.json": {"fixture": True, "model": MODEL, "grader_role": "grader_fallback",
                               "e19_selfreport": "FIXTURE: ran no listing and no glob"}}
        ent = {"attempt_id": att, "files": {}}
        for fn in LANE_FILES:
            b = b"FIXTURE final message\n" if fn.endswith(".md") else jb(body[fn])
            rel = "lane_%s/%s" % (L.lower(), fn)
            B[LDIR + rel] = b
            ent["files"][fn] = {"durable": rel, "sha256": shab(b)}
        land["lanes"][L] = ent
    B[LANDING] = jb(land)
    B[MRCP] = lb([{"fixture": True, "attempt_id": att, "record_kind": "completion", "outcome": "COMPLETED", "model_actual": MODEL}
                  for att in ATT.values()])
    fx(LDIR + " lanes A and B, the landing manifest, and " + MRCP + " (FIXTURE)")
    outs, recs = [], []
    for n in ("out1.json", "out2.json", "final_message_fixture.md"):
        b = ("FIXTURE landed output %s\n" % n).encode()
        B[D + "fixture_out/" + n] = b
        outs.append({"execution_id": "fixture#e1", "attempt_id": "fixture", "outcome": "LANDED",
                     "path": D + "fixture_out/" + n, "sha256": shab(b), "bytes": len(b)})
    for n in ("r1.jsonl", "r2.jsonl", "r3.jsonl"):
        b = ("{\"fixture\": \"%s\"}\n" % n).encode()
        B[D + "fixture_out/" + n] = b
        recs.append({"path": D + "fixture_out/" + n, "sha256": shab(b)})
    B[FIXL] = jb({"fixture": True, "outputs": outs, "receipt_files": recs})
    fx(FIXL + " with three fixture outputs and three fixture receipt files, passed by --fixture-landed")
    if closeable:
        B[LANDEDF] = B[FIXL]
        K.update(LANDED_PIN=shab(B[FIXL]), LANDED_OUTPUTS=3, LANDED_RECEIPT_FILES=3)
        fx(LANDEDF + " (close-mode mirrors only: the fixture landed manifest stands as the pinned one, so no test hook is needed)")
    elif K["LANDED_PIN"] == PENDING:
        B[LANDEDF] = jb({"fixture": True, "outputs": [dict(outs[0], path=D + "fixture_out/not_on_disk.json")], "receipt_files": recs})
        K.update(LANDED_PIN=shab(B[LANDEDF]), LANDED_OUTPUTS=1, LANDED_RECEIPT_FILES=3)
        fx(LANDEDF + " (FIXTURE of the landed manifest's form, naming one output not on disk)")
    else:
        B[LANDEDF] = real(LANDEDF)
    if K["ROUTED_PIN"] == PENDING:
        B[ROUTEDF] = lb([{"fixture": True, "id": "FIXTURE-%d" % i, "book": BOOK, "from": "fixture#e1", "ruling": "FIXTURE"}
                         for i in range(1, ROUTED_N + 1)])
        K.update(ROUTED_PIN=shab(B[ROUTEDF]), ROUTED_ITEMS=ROUTED_N)
        fx(ROUTEDF + " (FIXTURE routed items)")
    else:
        B[ROUTEDF] = real(ROUTEDF)
    for n in SHARED:
        B[n] = lb([{"fixture": True, "model_id": K["MODEL_ID"], "book": "FIXTURE", "span": "FIXTURE",
                    "chunk_decision_id": "FIXTURE-001", "non_authorizing": True}])
    fx("the four shared feed files, each one FIXTURE row")
    B["marathon_progress.yaml"] = ("# FIXTURE of the right form\nbooks_completed: %d\ncompleted:\n  %s:\n    status: complete\ncurrent_book: %s\n"
                                   % (K["BOOKS_BEFORE"], K["PREV_BOOK"], BOOK)).encode()
    B["model_manifest.yaml"] = ("# FIXTURE of the right form\nbooks_completed: %d\ncurrent_book: %s\n" % (K["BOOKS_BEFORE"], BOOK)).encode()
    fx("marathon_progress.yaml and model_manifest.yaml (FIXTURES holding the anchors as they stand before this book's close)")
    B[GENF] = Path(A.gen).read_bytes()
    B[TOOLF] = Path(A.tool).read_bytes()
    B[PARF] = jb(P)
    m = Mirror(dest / ("base_c" if closeable else "base"), B)
    p = subprocess.run([sys.executable, "-B", str(m.p(GENF)), "--book", BOOK, "--write"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=ENV)
    if p.returncode != 0:
        raise SystemExit("packet generator failed in the mirror: " + (p.stderr or p.stdout)[-300:])
    B[PKT] = m.p(PKT).read_bytes()
    m.files.append(m.p(PKT))
    fx(PKT + " (written in the mirror by the real generator over the fixture inputs)")
    m.clean()
    return B


class Mirror:
    def __init__(self, root, base):
        self.root, self.files, self.dirs = Path(root), [], []
        os.makedirs(self.root)                                   # must not exist yet: no stale mirror is ever reused
        self.dirs.append(self.root)
        for rel, b in base.items():
            self.put(rel, b)

    def p(self, rel):
        return self.root / rel

    def put(self, rel, b):
        p = self.p(rel)
        q, miss = p.parent, []
        while q not in self.dirs and q != self.root:
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

    def param(self, fn):
        self.jedit(PARF, lambda o: fn(o["constants"]))

    def ledit(self, rel, fn):
        rows = [json.loads(l) for l in self.get(rel).decode("utf-8").split("\n") if l.strip()]
        r2 = fn(rows)
        self.put(rel, lb(rows if r2 is None else r2))

    def rows(self):
        return [json.loads(l) for l in self.get(ROWSF).decode("utf-8").split("\n") if l.strip()]

    def row(self, i, **kv):
        self.ledit(ROWSF, lambda rows: rows[i].update(kv))

    def lane(self, L, fn, mut):
        rel = LDIR + "lane_%s/%s" % (L.lower(), fn)
        self.jedit(rel, mut)
        s = shab(self.get(rel))
        self.jedit(LANDING, lambda o: o["lanes"][L]["files"][fn].update(sha256=s))

    def args(self, **kw):
        a = {"--acf": "lam_pattern", "--next-book": NEXT, "--fixture-landed": str(self.p(FIXL))}
        a.update(kw)
        out = ["--book", BOOK, "--m8-root", str(self.root)]
        for k, v in a.items():
            if v is not None:
                out += [k, v]
        return out

    def run(self, argv, tool=None):
        p = subprocess.run([sys.executable, "-B", str(tool or Path(A.tool).resolve())] + argv, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", env=ENV)
        try:
            rep = json.loads(p.stdout)
        except ValueError:
            rep = None
        return p.returncode, rep, (p.stderr or "").strip()[-300:]

    def installed(self, *extra, **kw):
        """The tool's copy inside this mirror, with no --m8-root: the only way --close can run at all."""
        a = {"--acf": "lam_pattern", "--next-book": NEXT}
        a.update(kw)
        argv = ["--book", BOOK] + list(extra)
        for k, v in a.items():
            if v is not None:
                argv += [k, v]
        return self.run(argv, self.p(TOOLF))

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


def case(name, expect, fn, **kw):
    CASES.append((name, [expect] if isinstance(expect, str) else list(expect), fn, kw))


def lg(L, s):
    return "lane %s: %s" % (L, s)


# ---- corpus
case("corpus byte changed", "corpus pinned", lambda m: m.row(0, boundary_rationale="PLANTED"))
case("corpus CRLF line", "corpus is LF-only (E-73)", lambda m: m.sub(ROWSF, b"\n", b"\r\n"))
case("corpus row dropped", G_N, lambda m: m.ledit(ROWSF, lambda r: r[:-1]))
case("corpus row of another book", G_N, lambda m: m.row(9, book="Ezek"))
case("a row carries a hold", "every row candidate_review_complete with null hold fields; no row carries a hold",
     lambda m: m.row(4, candidate_hold_state="held_lower_confidence"))
case("a row not review-complete", "every row candidate_review_complete with null hold fields; no row carries a hold",
     lambda m: m.row(4, review_status="candidate"))
case("a hold field absent", "every row candidate_review_complete with null hold fields; no row carries a hold",
     lambda m: m.ledit(ROWSF, lambda r: r[7].pop("candidate_hold_basis") and None))
case("chunk index broken", "chunk_index 1..N", lambda m: m.row(2, chunk_index_in_book=99))
case("writer id repeated", "writer_decision_id unique and present", lambda m: m.row(1, writer_decision_id=m.rows()[0]["writer_decision_id"]))
case("tiling gap", G_TILE, lambda m: m.row(1, span=m.rows()[2]["span"]))
case("language label wrong", G_LANG, lambda m: m.row(0, language="Z"))
case("parent run split", G_PARENT,
     lambda m: m.row(0, parent_collection=m.rows()[-1]["parent_collection"]))
if LOOKUP["kind"] == "module":
    case("numbering zone changed in the lookup module", [G_LIB, G_ZONE],
         lambda m: m.put(LIBF, m.get(LIBF) + b"\nZONE_CHAPTERS = [3, 4, 5]\n"))
case("lookup byte changed", G_LIB, lambda m: m.put(LIBF, m.get(LIBF) + b"\n"))
case("lookup absent (unevaluable is UNMET)", G_GROUP % LOOKUP["label"], lambda m: m.rm(LIBF))
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
# Plant on a condition no later record answers: a superseding MET would rightly hide it (1Cor e2 answers B3).
_E1_ONLY = [k for k in C["BOSS_CONDITIONS"] if len(C["BOSS"]) < 2 or k not in C["BOSS_E2_SUPERSEDES"]]
case("boss e1 condition not met", [G_B1P, G_BOSS],
     lambda m: m.jedit(BOSS1, lambda o: next(x for x in o["conditions"] if x.get("id") == _E1_ONLY[0]).update(verdict="NOT_MET")))
if len(C["BOSS"]) > 1:
    case("boss e2 answers another condition", ["boss audit %s pinned" % C["BOSS"][1][0], "boss audit %s answers exactly %s" % (C["BOSS"][1][0], C["BOSS_E2_LABEL"])],
         lambda m: m.jedit(D + C["BOSS"][1][1], lambda o: o["conditions"].append({"id": "B9", "verdict": "MET"})))
# ---- sidecars
case("sidecar source absent", "sidecar source present (%s)" % C["SIDECAR"], lambda m: m.rm(SIDE))
case("sidecar row missing", ["sidecar set == low/medium_low rows", "atlas feed option lam_pattern meets the coverage validator's per-book rule"] + G_COV,
     lambda m: m.ledit(SIDE, lambda r: r[1:]))
case("sidecar row repeated", "sidecar set == low/medium_low rows", lambda m: m.ledit(SIDE, lambda r: r + r[:1]))
case("sidecar field empty", "sidecar fields present", lambda m: m.ledit(SIDE, lambda r: r[0].update(concern_type="")))
case("sidecar boilerplate", "why_low_confidence not boilerplate",
     lambda m: m.ledit(SIDE, lambda r: r[0].update(why_low_confidence=r[1]["why_low_confidence"])))
case("gen_sidecars check MISMATCH", "gen_sidecars.py --check MATCH",
     lambda m: m.put(GENSIDE, (STUB % ("MISMATCH", 1)).encode()))
case("gen_sidecars absent", "gen_sidecars.py --check MATCH", lambda m: m.rm(GENSIDE))
# ---- evidence
case("suite not GREEN", ["suite report pinned", "suite GREEN over this corpus"], lambda m: m.jedit(SUITE, lambda o: o["summary"].update(hard_status="RED")))
case("suite over another file", "suite GREEN over this corpus", lambda m: m.jedit(SUITE, lambda o: o.update(rows_file="rows_v0.jsonl")))
case("normalize fixed a string", "normalize dry-run clean", lambda m: m.jedit(SUITE, lambda o: o[NKEY].update(fixed=1)))
case("citation sweep degraded", G_QB,
     lambda m: m.jedit(SUITE, lambda o: o["citation_sweep"].update(nfd_degraded_count=1)))
case("WEB quote flagged", "WEB quote fidelity GREEN", lambda m: m.jedit(SUITE, lambda o: o["web_quotes"].update(flag_count=2)))
if LANG_ON:
    case("language zones not GREEN", "language zones GREEN", lambda m: m.jedit(SUITE, lambda o: o["language_zones"].update(status="RED")))
case("parity not GREEN", ["CWO parity record pinned", "CWO parity GREEN for THIS corpus"], lambda m: m.jedit(PAR, lambda o: o.update(status="RED")))
case("parity over another corpus", "CWO parity GREEN for THIS corpus", lambda m: m.jedit(PAR, lambda o: o.update(post_corpus_sha256="0" * 64)))
case("parity tool DIFFERS", G_PAR_T,
     lambda m: m.put(PARTOOL, (STUB % (json.dumps({"check": "DIFFERS", "status": "GREEN"}), 1)).encode()))
case("suite report absent (unevaluable is UNMET)", G_GROUP % "evidence", lambda m: m.rm(SUITE))
# ---- carrier
case("carrier generator MISMATCH", G_CGEN,
     lambda m: m.put(CGEN, (STUB % ("MISMATCH", 1)).encode()))
case("carrier fallback not in force", "grader carrier states the measured fallback (OW-25)",
     lambda m: m.jedit(CARRIER, lambda o: o.update(fallback_in_force=False)))
case("carrier downgrade statement edited", ["grader carrier states the measured fallback (OW-25)", "receipt carries the carrier's downgrade statement"],
     lambda m: m.jedit(CARRIER, lambda o: o.update(downgrade_statement="PLANTED")))
case("carrier has no shape for the book", [G_SHAPE, G_WK, "receipt carries the OW-26 weakness statement"],
     lambda m: m.jedit(CARRIER, lambda o: o["book_close_shapes"].pop(BOOK)))
case("carrier shape says the audit is MET", G_SHAPE, lambda m: m.jedit(CARRIER, lambda o: o["book_close_shapes"][BOOK].update(transcript_audit="MET")))
case("carrier shape directive wrong", G_SHAPE, lambda m: m.jedit(CARRIER, lambda o: o["book_close_shapes"][BOOK].update(directive="OW-6")))
case("carrier weakness digest wrong", G_WK,
     lambda m: m.jedit(CARRIER, lambda o: o["book_close_shapes"][BOOK].update(weakness_statement_sha256="0" * 64)))
case("carrier absent (unevaluable is UNMET)", G_GROUP % "carrier", lambda m: m.rm(CARRIER))
# ---- lanes
case("landing manifest absent", ["landing manifest present (merged_close/landing_manifest.v1.json)", G_TWO], lambda m: m.rm(LANDING))
case("lane A file changed after landing", [lg("A", G_SIX), G_TWO],
     lambda m: m.put(LDIR + "lane_a/postcheck.json", m.get(LDIR + "lane_a/postcheck.json") + b"\n"))
case("lane B attempt id wrong", lg("B", G_SIX), lambda m: m.jedit(LANDING, lambda o: o["lanes"]["B"].update(attempt_id="dan_other_a1")))
case("lane B is lane A again (one lane landed twice)", lg("B", G_SIX),
     lambda m: m.jedit(LANDING, lambda o: o["lanes"].update(B=o["lanes"]["A"])))
case("lane A completion receipt FAILED", lg("A", "completion receipt COMPLETED on " + MODEL),
     lambda m: m.ledit(MRCP, lambda r: r[0].update(outcome="FAILED")))
case("lane B ran on another model", lg("B", "completion receipt COMPLETED on " + MODEL),
     lambda m: m.ledit(MRCP, lambda r: r[1].update(model_actual="claude-sonnet-5")))
case("receipts file absent", [lg("A", "completion receipt COMPLETED on " + MODEL), lg("B", "completion receipt COMPLETED on " + MODEL)],
     lambda m: m.rm(MRCP))
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
G_DUE = "close evidence pinned, holding a value for every item due at the close act, none UNAVAILABLE"
G_READ = "final check accounts for every corpus row, read whole or held by byte equality, and reads every changed row and its neighbours"
DUE_TYPE, DUE_ITEMS, CE = "DUE_AT_CLOSE_ACT", [16, 18, 19], "close/close_evidence.v1.json"
DUE_SOURCE = {"path": "planted/source.json", "sha256": "0" * 64, "locator": "key planted"}
DUE_VALUES = {"item_%d" % i: {"value": "planted %d" % i, "tier": "MEASURED", "source": DUE_SOURCE} for i in DUE_ITEMS}


def _due(m, values=DUE_VALUES, pin=None):
    b = jb({"values": values})
    m.put(D + CE, b)
    m.param(lambda k: k.update(DUE_AT_CLOSE={"type": DUE_TYPE, "items": DUE_ITEMS}, CLOSE_EVIDENCE_REL=CE, CLOSE_EVIDENCE_PIN=pin or shab(b)))


def _entries(m, *ent):
    for L in ("A", "B"):
        m.lane(L, "final_check.json", lambda o: o["close_gate_assessment"].extend(ent))


def _due_entries(m):
    _entries(m, *[{"item": str(i), "met": False, "type": DUE_TYPE, "evidence": "falls due at the close act"} for i in DUE_ITEMS])


def _due_fix(m, values=DUE_VALUES, pin=None):
    _due(m, values, pin)
    _due_entries(m)


def _read(m, base=None, read=None, held=None, keep=None):
    """base: mutate the first-attempt copy. read/held default to every row read."""
    rows = m.rows()
    ids = [r["decision_id"] for r in rows]
    b = m.get(ROWSF)
    if base is not None:
        bl = [json.loads(l) for l in b.decode("utf-8").split("\n") if l.strip()]
        base(bl)
        b = lb(bl)
    rel = "close/rows_first_read.jsonl"
    m.put(D + rel, b)
    m.param(lambda k: k.update(READ_RECORD={"base_rows_rel": rel, "base_rows_pin": shab(b)}))
    r, h = (ids if read is None else read(ids)), ([] if held is None else held(ids))
    for L in ("A", "B"):
        m.lane(L, "final_check.json", lambda o: o.update(rows_read=r, rows_held_by_byte_equality=h))


case("due at close: the three items accepted with their values", [], _due_fix, clean=True)
case("due at close: an item outside the list refused", lg("A", G_CGA),
     lambda m: (_due_fix(m), _entries(m, {"item": "17", "met": False, "type": DUE_TYPE})))
case("due at close: a wrong type refused", lg("B", G_CGA),
     lambda m: (_due(m), _entries(m, {"item": "16", "met": False, "type": "NOT_DUE_YET"})))
case("due at close: a value missing is unmet", G_DUE,
     lambda m: _due_fix(m, {k: v for k, v in DUE_VALUES.items() if k != "item_18"}))
case("due at close: a value UNAVAILABLE is unmet", G_DUE,
     lambda m: _due_fix(m, dict(DUE_VALUES, item_19={"value": "none", "tier": "UNAVAILABLE"})))
case("due at close: a stale evidence pin is unmet", G_DUE, lambda m: _due_fix(m, DUE_VALUES, "0" * 64))
case("due at close: the word UNAVAILABLE as a value under another tier is unmet", G_DUE,
     lambda m: _due_fix(m, dict(DUE_VALUES, item_16={"value": "UNAVAILABLE", "tier": "MEASURED", "source": DUE_SOURCE})))
case("due at close: a value with an empty source is unmet", G_DUE,
     lambda m: _due_fix(m, dict(DUE_VALUES, item_18={"value": "planted 18", "tier": "MEASURED", "source": {}})))
case("due at close: the deferred review as met stays refused", lg("A", G_DEF),
     lambda m: (_due_fix(m), m.lane("A", "final_check.json", lambda o: o["close_gate_assessment"][1].update(met=True))))
case("due at close: the type does not stand in for the owed audit", lg("B", G_DEF),
     lambda m: (_due_fix(m), m.lane("B", "final_check.json", lambda o: o["close_gate_assessment"].__delitem__(2))))
case("due at close: a book without the key refuses the type", lg("A", G_CGA),
     lambda m: _entries(m, {"item": "16", "met": False, "type": DUE_TYPE}))
case("read record: every row read accepted", [], lambda m: _read(m), clean=True)
case("read record: changed row read, rest held by byte equality, accepted", [],
     lambda m: _read(m, base=lambda rows: rows[5].update(boundary_rationale="OLDER"),
                     read=lambda ids: ids[4:7], held=lambda ids: ids[:4] + ids[7:]), clean=True)
case("read record: a row unaccounted", lg("A", G_READ), lambda m: _read(m, read=lambda ids: ids[1:]))
case("read record: a held row that changed", lg("B", G_READ),
     lambda m: _read(m, base=lambda rows: rows[5].update(boundary_rationale="OLDER"),
                     read=lambda ids: ids[:5] + ids[6:], held=lambda ids: [ids[5]]))
case("read record: a seam neighbour of a changed row not read", lg("A", G_READ),
     lambda m: _read(m, base=lambda rows: rows[5].update(boundary_rationale="OLDER"),
                     read=lambda ids: ids[5:7], held=lambda ids: ids[:5] + ids[7:]))
case("read record: the first-attempt copy not its pin", lg("A", G_READ),
     lambda m: (_read(m), m.param(lambda k: k["READ_RECORD"].update(base_rows_pin="0" * 64))))
case("read record: no base rows named is unmet, not passed", lg("B", G_READ),
     lambda m: (_read(m), m.param(lambda k: k["READ_RECORD"].pop("base_rows_rel"))))
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
     lambda m: m.rm(SCH + SF[3]))
case("scholar check says FAIL", "scholar record check says PASS", lambda m: m.jedit(SCH + SF[3], lambda o: o.update(VERDICT="FAIL")))
case("scholar sub-check not passed", "scholar record check says PASS",
     lambda m: m.jedit(SCH + SF[3], lambda o: o["checks"][0].update(passed=False)))
case("scholar check lists a failure", "scholar record check says PASS",
     lambda m: m.jedit(SCH + SF[3], lambda o: o.update(FAILED=["fixture_check"])))
case("scholar check counts disagree", "scholar record check says PASS",
     lambda m: m.jedit(SCH + SF[3], lambda o: o.update(checks_passed=0)))
case("scholar record edited after its check", "scholar record check is bound to the record's bytes",
     lambda m: m.put(SCH + SF[2], b"PLANTED\n"))
case("scholar checker edited after its check", "scholar record check is bound to the record's bytes",
     lambda m: m.put(SCH + SF[1], b"# PLANTED\n"))
# ---- fable end packet
case("routed items changed", ["routed items pinned", "fable end packet reproduces (--check MATCH)"],
     lambda m: m.put(ROUTEDF, m.get(ROUTEDF) + b"\n"))
case("packet absent", "fable end packet and its generator installed", lambda m: m.rm(PKT))
case("packet row dropped", ["fable end packet reproduces (--check MATCH)", "fable end packet over this corpus, rows == low/medium_low"],
     lambda m: m.jedit(PKT, lambda o: o["row_ids"].pop()))
case("packet routed count wrong", G_ROUTED, lambda m: m.jedit(PKT, lambda o: o.update(routed_items_count=ROUTED_N - 1)))
case("sidecars changed after the packet", ["fable end packet reproduces (--check MATCH)", "fable end packet carries the installed sidecars"],
     lambda m: m.ledit(SIDE, lambda r: r[0].update(possible_downstream_risk="PLANTED")))
case("packet says MET", "fable end packet records DEFERRED and no held row", lambda m: m.jedit(PKT, lambda o: o.update(status="MET")))
case("packet names a held row", "fable end packet records DEFERRED and no held row", lambda m: m.jedit(PKT, lambda o: o.update(held_rows={"W1-001": {}})))
# ---- retention
case("landed manifest changed", ["landed-outputs manifest pinned", "fable end packet reproduces (--check MATCH)"],
     lambda m: m.put(LANDEDF, m.get(LANDEDF) + b"\n"))
case("a landed output changed", G_RET, lambda m: m.put(D + "fixture_out/out1.json", b"PLANTED\n"))
case("a landed output absent", G_RET, lambda m: m.rm(D + "fixture_out/out2.json"))
case("an attempt-receipt file grew since the manifest: retained as it is, disclosed, not a refusal", [],
     lambda m: m.put(D + "fixture_out/r2.jsonl", m.get(D + "fixture_out/r2.jsonl") + b"{\"later\": 1}\n"), zero=True)
case("an attempt-receipt file absent", G_RCP, lambda m: m.rm(D + "fixture_out/r2.jsonl"))
case("an attempt-receipt file with a CR byte", G_RCP, lambda m: m.put(D + "fixture_out/r3.jsonl", b"{}\r\n"))
case("only two attempt-receipt files named", G_RCP, lambda m: m.jedit(D + "close/FIXTURE_landed.json", lambda o: o["receipt_files"].pop()))
case("a landed path outside the book (E-65)", G_RET,
     lambda m: m.jedit(D + "close/FIXTURE_landed.json", lambda o: o["outputs"][0].update(path="sp_durable/Ezek/x.json")))
case("an output not LANDED", G_RET, lambda m: m.jedit(D + "close/FIXTURE_landed.json", lambda o: o["outputs"][0].update(outcome="REJECTED")))
case("the pinned landed manifest without its outputs on disk", G_RET, lambda m: None, args={"--fixture-landed": None})
# ---- targets
case("chunks already written", CHUNKS + " absent", lambda m: m.put(CHUNKS, b"{}\n"))
case("receipt already written", RECEIPT + " absent", lambda m: m.put(RECEIPT, b"{}\n"))
case("retention manifest already written", "retention manifest absent", lambda m: m.put(D + C["RETENTION"], b"{}\n"))
case("a close lock is held", "no close lock is held", lambda m: m.put(C["LOCK_NAME"], b"x\n"))
for _n in SHARED:
    case("%s already holds a row of the book" % _n, "%s holds no %s row" % (_n, BOOK),
         lambda m, n=_n: m.put(n, m.get(n) + lb([{"model_id": "M8_fable", "book": BOOK}])))
for _n in SHARED[:2]:
    case("%s has a CRLF" % _n, "%s is LF-only and ends with a newline" % _n, lambda m, n=_n: m.put(n, m.get(n).replace(b"\n", b"\r\n")))
for _n in SHARED[2:]:
    case("%s lacks its final newline" % _n, "%s is LF-only and ends with a newline" % _n, lambda m, n=_n: m.put(n, m.get(n)[:-1]))
case("a shared file absent (unevaluable is UNMET)", G_GROUP % "targets", lambda m: m.rm(SHARED[3]))
case("progress already counts the book", "marathon_progress anchors", lambda m: m.sub("marathon_progress.yaml", B_BEFORE, B_AFTER))
case("progress already lists the book", "marathon_progress anchors",
     lambda m: m.sub("marathon_progress.yaml", CUR_LINE, LISTED))
case("progress file has CRLF", ["marathon_progress anchors", "every close write is LF-only"],
     lambda m: m.put("marathon_progress.yaml", m.get("marathon_progress.yaml").replace(b"\n", b"\r\n")))
case("model manifest names another current book", "model_manifest anchors", lambda m: m.sub("model_manifest.yaml", CUR_LINE, b"current_book: Hos\n"))
case("model manifest already counts the book", "model_manifest anchors", lambda m: m.sub("model_manifest.yaml", B_BEFORE, B_AFTER))
# ---- the owner's choices
case("no --next-book", G_NEXT, lambda m: None, args={"--next-book": None})
case("--next-book the book itself", G_NEXT, lambda m: None, args={"--next-book": BOOK})
case("--next-book a closed book", G_NEXT, lambda m: None, args={"--next-book": C["PREV_BOOK"]})
case("--next-book not a book code", G_NEXT, lambda m: None, args={"--next-book": "x y"})
case("no --acf", "--acf chosen (the owner's choice between lam_pattern and item22)", lambda m: None, args={"--acf": None})
# ---- item-22 feed
case("item-22 feed absent", "item-22 feed installed; its rows name only chunks of this book", lambda m: m.rm(FEED))
case("item-22 feed row of another book (E-65)", "item-22 feed installed; its rows name only chunks of this book",
     lambda m: m.ledit(FEED, lambda r: r[0].update(book="Ezek")))
case("item-22 feed misses a low row", "atlas feed option item22 meets the coverage validator's per-book rule",
     lambda m: m.ledit(FEED, lambda r: r[1:]), args={"--acf": "item22"})
case("item-22 feed stale span", "atlas feed option item22 meets the coverage validator's per-book rule",
     lambda m: m.ledit(FEED, lambda r: r[0].update(span="%s.99.1-%s.99.2" % (BOOK, BOOK))), args={"--acf": "item22"})
case("item-22 chosen but feed absent", "atlas feed option item22 meets the coverage validator's per-book rule",
     lambda m: m.rm(FEED), args={"--acf": "item22"})


# ---- what the port adds
def _fam(name, v):
    return lambda m: m.param(lambda k: k["FAMILIES"].update({name: v}))


case("a PENDING pin refuses", [G_PEND, "corpus pinned"], lambda m: m.param(lambda k: k.update(CORPUS_PIN=PENDING)))
case("a PENDING nested in a list refuses", [G_PEND, G_B1P], lambda m: m.param(lambda k: k["BOSS"][0].__setitem__(2, PENDING)))
case("a PENDING in a name the close tool does not read refuses", G_PEND, lambda m: m.param(lambda k: k["CWO"].update(rulings=PENDING)))
case("a PENDING count refuses", [G_PEND, "fable end packet carries the PENDING routed items"], lambda m: m.param(lambda k: k.update(ROUTED_ITEMS=PENDING)))
case("a gate-family switch without a reason refuses", "gate family language_layer switched off without a reason",
     _fam("language_layer", {"enabled": False}))
case("a gate-family switch with a blank reason refuses", "gate family numbering_zone switched off without a reason",
     _fam("numbering_zone", {"enabled": False, "reason": "   "}))
case("a gate family not stated refuses", "gate family numbering_zone is stated in the parameters",
     lambda m: m.param(lambda k: k["FAMILIES"].pop("numbering_zone")))
case("a gate family's switch not a boolean refuses", "gate family language_layer is stated in the parameters",
     _fam("language_layer", {"enabled": "no", "reason": "PLANTED"}))
case("a language switch the corpus does not bear out refuses", G_LOFF,
     lambda m: m.param(lambda k: (k["FAMILIES"].update(language_layer={"enabled": False, "reason": "PLANTED"}),
                                  k.update(LANGUAGE_COUNTS={"PLANTED": 1}))))
case("a numbering switch the parameters do not bear out refuses", G_ZOFF,
     lambda m: m.param(lambda k: (k["FAMILIES"].update(numbering_zone={"enabled": False, "reason": "PLANTED"}),
                                  k.update(ZONE_MOVED=1))))
case("a numbering switch that declares a zone refuses", G_ZOFF,
     lambda m: m.param(lambda k: (k["FAMILIES"].update(numbering_zone={"enabled": False, "reason": "PLANTED"}),
                                  k.update(ZONE=[3]))))
case("an unreadable corpus passes no row-based gate",
     [G_GROUP % "corpus", G_LF, G_I22, "atlas feed option lam_pattern meets the coverage validator's per-book rule"] + G_COV,
     lambda m: m.rm(ROWSF))
case("a boss condition NOT_TESTABLE stays UNMET", [G_B1P, G_BOSS],
     lambda m: m.jedit(BOSS1, lambda o: o["conditions"][1].update(verdict="NOT_TESTABLE")))
case("a boss condition missing refuses", [G_B1P, G_BOSS], lambda m: m.jedit(BOSS1, lambda o: o["conditions"].pop()))
case("carrier shape granted by another ruling", G_SHAPE,
     lambda m: m.jedit(CARRIER, lambda o: o["book_close_shapes"][BOOK].update(granted_by="OW-99")))
case("the lookup's kind unknown (unevaluable is UNMET)", G_GROUP % LOOKUP["label"], lambda m: m.param(lambda k: k["LOOKUP"].update(kind="other")))
if LOOKUP["kind"] == "inventory":
    case("the inventory's numbering face is another", "verse inventory declares the %s numbering face" % LOOKUP["face"],
         lambda m: (m.jedit(LIBF, lambda o: o.update(numbering_face="PLANTED")),
                    m.param(lambda k: k["LOOKUP"].update(pin=shab(m.get(LIBF))))))
if C["NEXT_BOOK_EXPECTED"]:
    case("--next-book not the book the parameters name", G_NEXT, lambda m: None, args={"--next-book": "Rev"})

CLOSE_DEFECTS = [
    ("the corpus changed by one byte", lambda m: m.row(0, boundary_rationale="PLANTED"), {}),
    ("a PENDING pin", lambda m: m.param(lambda k: k.update(SUITE_PIN=PENDING)), {}),
    ("a gate-family switch without a reason", _fam("numbering_zone", {"enabled": False}), {}),
    ("a lane's final check conditional", lambda m: m.lane("B", "final_check.json", lambda o: o.update(verdict="fit_to_close_with_conditions")), {}),
    ("the deferred review recorded as met", lambda m: m.lane("A", "final_check.json", lambda o: o["close_gate_assessment"][1].update(met=True)), {}),
    ("a due-at-close value missing", lambda m: _due_fix(m, {}), {}),
    ("a close lock held", lambda m: m.put(C["LOCK_NAME"], b"x\n"), {}),
    ("no --acf", lambda m: None, {"--acf": None}),
    ("no --next-book", lambda m: None, {"--next-book": None}),
    ("the corpus unreadable", lambda m: m.rm(ROWSF), {})]
TARGETS = [CHUNKS, RECEIPT, D + C["RETENTION"]]


def unmet_names(rep):
    return [u["gate"] if isinstance(u, dict) else u for u in (rep or {}).get("unmet", [])]


def unit_cases(tool):
    spec = importlib.util.spec_from_file_location("close_book_under_test", str(tool))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    id1, id2, id9 = (C["DECISION_ID_FORM"] % n for n in (1, 2, 99))
    by = {id1: {"span": "%s.1.1-%s.1.7" % (BOOK, BOOK), "confidence": "low", "review_status": "candidate_review_complete", "candidate_hold_state": None},
          id2: {"span": "%s.1.8-%s.1.16" % (BOOK, BOOK), "confidence": "medium_low", "review_status": "candidate_review_complete", "candidate_hold_state": None}}
    low = set(by)

    def row(i, **kv):
        r = by[i]
        return {"chunk_decision_id": i, "span": r["span"], "confidence": r["confidence"], "chunk_review_status": r["review_status"],
                "candidate_hold_state": None, "review_packet_final_state": "accepted_candidate", **kv}
    a, b = row(id1), row(id2)
    out = []
    for name, opt, key in (("coverage: exact set is clean", [a, b], None), ("coverage: duplicate counted", [a, b, b], "duplicates"),
                           ("coverage: missing row named", [a], "missing"),
                           ("coverage: orphan row named", [a, b, {**a, "chunk_decision_id": id9}], "orphan"),
                           ("coverage: stale confidence named", [a, row(id2, confidence="medium")], "stale"),
                           ("coverage: stale final state named", [a, row(id2, review_packet_final_state="held_lower_confidence")], "stale")):
        c = mod.coverage(opt, by, low)
        ok = mod.cov_ok(c) if key is None else (bool(c[key]) and not mod.cov_ok(c))
        out.append({"name": name, "kind": "unit", "pass": bool(ok), "detail": {k: (v if isinstance(v, int) else len(v)) for k, v in c.items()}})
    return out, mod


def close_machinery_cases(mod, dest):
    """commit() on a scratch tree under --dest."""
    out = []
    root = dest / "close_machinery"
    os.makedirs(root)
    mod.bind(root, BOOK)
    mod.load_params(DOC, BOOK)
    (root / "old.txt").write_bytes(b"old\n")
    mod.commit([("new/a.txt", b"a\n", None), ("old.txt", b"old\nmore\n", b"old\n")])
    out.append({"name": "commit: writes whole files and removes its lock", "kind": "close-machinery",
                "pass": (root / "new/a.txt").read_bytes() == b"a\n" and (root / "old.txt").read_bytes() == b"old\nmore\n"
                and not (root / mod.LOCK_NAME).exists()})
    for name, plan in (("commit: refuses a target that changed since the gates read it", [("b.txt", b"b\n", None), ("old.txt", b"x\n", b"old\n")]),
                       ("commit: refuses a CR byte", [("c.txt", b"c\r\n", None)]),
                       ("commit: a failure in a later write rolls the earlier ones back",
                        [("d.txt", b"d\n", None), ("old.txt", b"o2\n", b"old\nmore\n"), ("old.txt/e.txt", b"e\n", None)])):
        try:
            mod.commit(plan)
            ok, said = False, ""
        except SystemExit as e:
            said = str(e)
            ok = not (root / plan[0][0]).exists() and (root / "old.txt").read_bytes() == b"old\nmore\n" and not (root / mod.LOCK_NAME).exists()
        out.append({"name": name, "kind": "close-machinery", "pass": ok, "said": said[:120]})
    lock = root / mod.LOCK_NAME
    lock.write_bytes(b"x\n")
    try:
        mod.commit([("f.txt", b"f\n", None)])
        ok = False
    except OSError:
        ok = not (root / "f.txt").exists() and lock.read_bytes() == b"x\n"
    out.append({"name": "commit: refuses while another close holds the lock", "kind": "close-machinery", "pass": ok})
    shutil.rmtree(root)
    return out


def run_case(item, dest, base):
    i, (name, expect, fn, kw) = item
    m = Mirror(dest / ("case_%03d" % i), base)
    try:
        fn(m)
        rc, rep, err = m.run(m.args(**kw.get("args", {})))
        un = unmet_names(rep)
        ok = rep is not None and all(e in un for e in expect) and (bool(expect) or kw.get("zero") or kw.get("clean"))
        if kw.get("clean"):
            ok = ok and rep["gates_unmet"] == 0
        if kw.get("zero"):
            ok = ok and rep["gates_unmet"] == 0 and len(rep.get("receipt_files_changed_since_the_manifest") or []) == 1
        return {"name": name, "kind": "defect", "pass": bool(ok), "expect": expect, "unmet_count": len(un),
                "also_unmet": [u for u in un if u not in expect][:8], **({} if ok else {"stderr": err})}
    except Exception as e:  # noqa: BLE001
        return {"name": name, "kind": "defect", "pass": False, "expect": expect, "error": "%s: %s" % (type(e).__name__, e)}
    finally:
        if not A.keep:
            m.clean()


def close_cases(dest, base, add):
    """--close, on private mirrors only, through the copy of the tool installed in each mirror."""
    m = Mirror(dest / "close_clean", base)
    rc, rep, err = m.installed()
    add("installed in a mirror, no test hook: zero unmet gates", "close-mode", rc == 0 and rep is not None and rep["gates_unmet"] == 0
        and rep["test_hooks_in_use"] == [], unmet=unmet_names(rep), stderr=err)
    m.clean()
    for name, fn, kw in CLOSE_DEFECTS:
        m = Mirror(dest / "close_defect", base)
        fn(m)
        before = m.digest()
        rc, rep, err = m.installed("--close", **kw)
        add("--close refuses: " + name, "close-mode", rc != 0 and "REFUSED" in err and (rep is None or rep["gates_unmet"] >= 1)
            and m.digest() == before and not any(m.p(x).exists() for x in TARGETS), rc=rc, unmet=len(unmet_names(rep)), stderr=err[-100:])
        m.clean()
    for name, extra in (("--m8-root", ("--m8-root", ".")), ("--fixture-landed", ("--fixture-landed", "x")), ("--params", ("--params", "x")),
                        ("--dry-report", ("--dry-report", "x"))):
        m = Mirror(dest / "close_hook", base)
        before = m.digest()
        rc, _, err = m.installed("--close", *extra)
        add("--close refuses a test hook or another tree: " + name, "close-mode", rc != 0 and "REFUSED" in err and m.digest() == before, stderr=err[-100:])
        m.clean()
    m = Mirror(dest / "close_ok", base)
    shared_before = {n: m.get(n) for n in SHARED}
    rc, rep, err = m.installed("--close")
    made = list(TARGETS)
    for rel in made:
        if m.p(rel).exists():
            m.files.append(m.p(rel))
    m.dirs += [m.p("book_chunks"), m.p("book_chunks/" + BOOK), m.p("receipts")]
    wrote = {rel: m.get(rel) for rel in made if m.p(rel).exists()}
    grown = all(m.get(n).startswith(shared_before[n]) and len(m.get(n)) > len(shared_before[n]) for n in SHARED)
    prog = m.get("marathon_progress.yaml").decode("utf-8")
    add("--close on a clean mirror: every target written whole, LF, the shared files appended, the carriers moved, the lock gone", "close-mode",
        rc == 0 and rep is not None and rep.get("status") == "CLOSED" and len(wrote) == 3 and grown
        and not any(b"\r" in v for v in wrote.values()) and not m.p(C["LOCK_NAME"]).exists()
        and sum(1 for x in wrote[CHUNKS].split(b"\n") if x) == C["ROWS"] and prog.endswith("  %s:\n    status: complete\ncurrent_book: %s\n" % (BOOK, NEXT)),
        rc=rc, wrote=sorted(wrote), stderr=err[-160:])
    before = m.digest()
    rc, rep, err = m.installed("--close")
    add("--close a second time refuses and changes nothing", "close-mode", rc != 0 and "REFUSED" in err and m.digest() == before, stderr=err[-100:])
    if not A.keep:
        m.clean()


def main():
    dest = Path(A.dest).resolve()
    if dest == REAL_ROOT or REAL_ROOT in dest.parents:
        raise SystemExit("REFUSED: --dest is inside the M8 tree")
    os.makedirs(dest)                                            # must be new
    tests = []
    tool, gen = Path(A.tool).resolve(), Path(A.gen).resolve()

    def add(name, kind, ok, **kw):
        tests.append({"name": name, "kind": kind, "pass": bool(ok), **kw})

    base = build_base(dest, False)
    # ---- the clean mirror
    m = Mirror(dest / "clean", base)
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
        rcp = json.loads((dest / "dry_a" / ("%s_completion.preview.json" % BOOK)).read_bytes().decode("utf-8"))
        add("receipt preview: DEFERRED and OWED are recorded, never MET", "dry",
            rcp["fable_end_review"]["status"] == "DEFERRED (OW-28)" and rcp["transcript_audit"] == "OWED, NOT MET"
            and rcp["fable_end_review"]["packet_sha256"] == shab(m.get(PKT)) and rcp["rows"] == C["ROWS"] and rcp["verses_covered"] == C["VERSES"]
            and full["deferred_never_met"]["transcript_audit"] == "OWED, NOT MET" and full["test_hooks_in_use"] == ["--fixture-landed"])
        ch = [json.loads(l) for l in (dest / "dry_a" / "chunks.preview.jsonl").read_bytes().decode("utf-8").split("\n") if l]
        add("chunks preview: every row, decision ids in the book's form", "dry",
            [c["decision_id"] for c in ch] == [C["DECISION_ID_FORM"] % i for i in range(1, C["ROWS"] + 1)])
        pv = (dest / "dry_a" / "marathon_progress.preview.yaml").read_bytes().decode("utf-8")
        mv = (dest / "dry_a" / "model_manifest.preview.yaml").read_bytes().decode("utf-8")
        ba = "books_completed: %d\n" % C["BOOKS_AFTER"]
        add("carrier previews: the count moves, the book is complete, current_book is the next book", "dry",
            pv.endswith("  %s:\n    status: complete\ncurrent_book: %s\n" % (BOOK, NEXT)) and pv.count(ba) == 1
            and mv.count(ba) == 1 and mv.count("current_book: %s\n" % NEXT) == 1 and ("current_book: %s" % BOOK) not in mv)
        off = [n for n, f in sorted(C["FAMILIES"].items()) if f.get("enabled") is False]
        add("every switched-off family prints as a MET gate line carrying its reason, and the report states the switches", "dry",
            all("gate family %s switched off: %s" % (n, C["FAMILIES"][n]["reason"]) in clean_gates for n in off)
            and full["gate_families"] == C["FAMILIES"], switched_off=off)
    add("dry report changed nothing in the mirror", "dry", m.digest() == before and not any(
        m.p(x).exists() for x in TARGETS + [C["LOCK_NAME"]]), files=len(before))
    rc, _, err = m.run(m.args(**{"--dry-report": str(m.p("dry_inside"))}))
    add("--dry-report inside the tree is refused and writes nothing", "refusal", rc != 0 and "REFUSED" in err and not m.p("dry_inside").exists(), stderr=err[-120:])
    p = subprocess.run([sys.executable, "-B", str(tool), "--book", BOOK], capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
    add("run from outside a tree without --m8-root is refused", "refusal", p.returncode != 0 and "REFUSED" in (p.stderr or ""))
    for name, fn in (("parameters of another book are refused", lambda m: m.jedit(PARF, lambda o: o["constants"].update(BOOK="Rev"))),
                     ("parameters lacking a name are refused", lambda m: m.jedit(PARF, lambda o: o["constants"].pop("VERSES"))),
                     ("a parameter file of another schema is refused", lambda m: m.jedit(PARF, lambda o: o.update(schema="other"))),
                     ("no parameter file is refused", lambda m: m.rm(PARF))):
        keep = m.get(PARF) if m.p(PARF).exists() else None
        fn(m)
        rc, _, err = m.run(m.args())
        add(name, "refusal", rc != 0 and "REFUSED" in err, stderr=err[-120:])
        m.put(PARF, keep)
    rc, _, err = m.run(m.args() + [])
    p2 = subprocess.run([sys.executable, "-B", str(tool), "--book", "not a book", "--m8-root", str(m.root)], capture_output=True, text=True,
                        encoding="utf-8", errors="replace", env=ENV)
    add("--book not a book name is refused", "refusal", p2.returncode != 0 and "REFUSED" in (p2.stderr or ""))
    dry_files = [dest / t / n for t in ("dry_a", "dry_b") for n in names]
    if not A.keep:
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
    picked = [(i, c) for i, c in enumerate(CASES) if not A.only or A.only in c[0]]
    planted = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=A.jobs) as ex:
        for t in ex.map(lambda it: run_case(it, dest, base), picked):
            tests.append(t)
            planted.update(t["expect"])
    units, mod = unit_cases(tool)
    tests += units
    tests += close_machinery_cases(mod, dest)
    close_cases(dest, build_base(dest, True), add)
    failed = [t["name"] for t in tests if not t["pass"]]
    kinds = {}
    for t in tests:
        kinds[t["kind"]] = kinds.get(t["kind"], 0) + 1
    result = {
        "command": "python -B " + " ".join([Path(sys.argv[0]).name, "--book", BOOK]), "book": BOOK,
        "tool_sha256": shab(tool.read_bytes()), "generator_sha256": shab(gen.read_bytes()), "params_sha256": shab(PARAMS_PATH.read_bytes()),
        "tests_total": len(tests), "passed": len(tests) - len(failed), "failed": failed, "by_kind": kinds,
        "gates_in_clean_run": len(clean_gates),
        "clean_gates_with_no_planted_defect": sorted({g.replace("lane B:", "lane A:") for g in clean_gates} - {
            g.replace("lane B:", "lane A:") for g in planted}) if not A.only else "not computed (--only)",
        "clean_gates_note": "lane A and lane B gates are one gate run twice; a defect planted in either lane counts for both",
        "planted_gates_not_in_clean_run": sorted(g for g in planted if g not in clean_gates and "could be evaluated" not in g
                                                 and not g.startswith(("atlas feed option item22", "gate family"))),
        "fixtures": FIXTURES, "real_copies": REAL_COPIES,
        "not_run": ["--close on the real tree, ever", "the real parity tool's sweep inside a mirror (it reads the real tree; a stub stands in)",
                    "the real carrier generator, sidecar generator and scholar checker (stubs or fixtures stand in)"],
        "limit": "A defect case passes when every expected gate is UNMET; other gates may be UNMET too (also_unmet). Fixtures show FORM, "
                 "not content: a clean run here says nothing about the book's real inputs, which do not all exist yet.",
        "tests": tests}
    Path(A.result).write_bytes(jb(result))
    if not A.keep:
        try:
            dest.rmdir()
        except OSError:
            pass
    print(json.dumps({k: result[k] for k in ("tests_total", "passed", "failed", "by_kind", "gates_in_clean_run",
                                             "clean_gates_with_no_planted_defect", "planted_gates_not_in_clean_run")}, ensure_ascii=False)[:2600])
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
