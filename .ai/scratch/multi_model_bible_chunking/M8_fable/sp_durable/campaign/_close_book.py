#!/usr/bin/env python3
"""Book-agnostic book close. Ported from sp_durable/Dan/_close_book.py (sha256 48f2337e...e5). Non-authorizing.

The tool is run by the orchestrator, never by a lane. Every constant of the Daniel tool now comes from
<BOOK>/close/close_params.v1.json, written by campaign/_make_close_params.py with every pin MEASURED from disk.

MODES
  --dry-report DIR   evaluate every gate, write a preview of every close write into DIR (DIR must lie outside the M8 tree),
                     change nothing in the tree. Deterministic: no clock, no randomness, no directory scan.
  --close            the only mode that writes into the tree. Refuses unless every gate is MET; takes an exclusive lock;
                     writes each file whole, LF bytes, through a temporary file and an atomic replace; rolls every write
                     back on any failure. Runs only on the tree this file is installed in (never with --m8-root).
  (neither)          evaluate every gate and print the summary.

ARGUMENTS
  --book BOOK        the book to close; required
  @usage.json        optional positional: a JSON file whose "tokens" object is copied into the receipt (REPORTED)
  --m8-root DIR      evaluate another M8 tree (the gate tests' private mirrors). Default: found from this file's location.
  --acf OPT          lam_pattern | item22: which rows are appended to atlas_candidate_feed.jsonl
  --next-book NAME   the value current_book takes after this book
  --fixture-landed F dry-mode TEST HOOK: verify retention against F instead of the pinned landed-outputs manifest. The
                     report names the hook when used, and --close refuses it.
  --params F         dry-mode TEST HOOK: read the parameters from F instead of <BOOK>/close/close_params.v1.json. The report
                     names the hook when used, and --close refuses it.

LAW CARRIED FROM EZEKIEL AND DANIEL
  * A gate that cannot be evaluated is UNMET, never skipped: every gate group runs inside guard(), and an exception
    becomes an UNMET gate that names it.
  * DEFERRED is never MET (OW-28): the campaign-end Fable review is recorded DEFERRED with its packet digest. The
    stage-1 transcript audit is recorded OWED, NOT MET (OW-26). Neither is counted as a met gate anywhere.
  * No Fable call is made or implied by this tool (OW-30).
  * Digests are taken on LF bytes only (E-73): every close write is refused if it carries a CR byte.

WHAT THE PORT ADDS (each is listed with its reason in build_notes.json)
  * A pin the parameter maker could not measure is the literal "PENDING", and a gate of its own stays UNMET while any exists.
  * A gate family with no subject in a book is off only through FAMILIES, with a reason. The switch prints as a gate line
    with that reason; a switch with no reason is UNMET; the bytes must still bear the switch out.
  * Outside --close an unreadable corpus no longer stops the run: every other group is still evaluated, and a gate that would
    otherwise pass on no rows is UNMET. --close still refuses exactly as Daniel's tool does.
"""
import argparse
import collections
import hashlib
import importlib
import itertools
import json
import os
import re
import subprocess
import sys
import types
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
PARAMS_REL = "close/close_params.v1.json"
PENDING = "PENDING"
# Every name below is read from the parameters: REQUIRED lists all of them, and an absent one is a refusal.
REQUIRED = (
    "BOOK", "BOOK_NAME", "BOOKS_BEFORE", "BOOKS_AFTER", "PREV_BOOK", "MODEL_ID", "DECISION_ID_FORM", "CORPUS", "CORPUS_PIN",
    "LOOKUP", "ROWS", "VERSES", "CHAPTERS", "ZONE", "ZONE_MOVED", "ZONE_LABEL", "PARENTS", "PARENTS_LABEL", "LANGUAGE_COUNTS",
    "LANGUAGE_CODES", "LANGUAGE_MIXED", "LOW_ROWS", "MANIFEST", "MANIFEST_PIN", "BUILT_FROM", "BUILT_FROM_PIN",
    "LINEAGE_FIELDS", "SUITE_PIN", "SUITE_NORMALIZE_KEY", "PARITY_PIN", "PARITY_TOOL", "PARITY_ARGS", "LANDED_REL",
    "LANDED_PIN", "LANDED_OUTPUTS", "LANDED_RECEIPT_FILES", "BOSS", "BOSS_E2_SUPERSEDES", "BOSS_E2_LABEL", "BOSS_CONDITIONS",
    "BOSS_CONDITIONS_LABEL", "ROUTED_REL", "ROUTED_PIN", "ROUTED_ITEMS", "CARRIER_REL", "CARRIER_GEN_REL", "CARRIER_FACTS",
    "SHAPE_GRANTED_BY", "HOLD_FIELDS", "LANES", "MERGED_RECEIPTS_REL", "LANDING_REL", "LANE_FILES", "UNMET_TYPES",
    "SCHOLAR_FILES", "SIDE_FIELDS", "SIDECAR", "GEN_SIDECARS_REL", "FEED_REL", "SHARED", "RETENTION", "PACKET_REL",
    "PACKET_GEN", "PACKET_GEN_ARGS", "NEXT_BOOK_PATTERN", "NEXT_BOOK_EXPECTED", "NEXT_BOOK_LABEL", "NEXT_PLACEHOLDER",
    "LOCK_NAME", "NOT_EVALUATED", "FAMILIES", "TEXT")
# Set only for a book whose controlling rounds ordered them; absent, the gates they drive do not exist for that book.
OPTIONAL = {"DUE_AT_CLOSE": None, "CLOSE_EVIDENCE_REL": None, "CLOSE_EVIDENCE_PIN": None, "READ_RECORD": None}
FAMILY_NAMES = ("language_layer", "numbering_zone")
BOOK_RE = re.compile(r"^[1-3]?[A-Z][A-Za-z]{1,7}$")
LANG_ON = ZONE_ON = None
PRE = None

M8 = SP = BK = None
GATES = []


def bind(root, book):
    global M8, SP, BK, PRE
    M8 = root
    SP = M8 / "sp_durable"
    BK = SP / book
    PRE = "sp_durable/%s/" % book


def load_params(doc, book):
    """Every constant comes from the parameters. A wrong book, or an absent name, is a refusal and not a default."""
    c = doc.get("constants") if isinstance(doc, dict) else None
    if not isinstance(c, dict) or doc.get("schema") != "m8_close_params.v1":
        raise SystemExit("REFUSED: the parameter file is not m8_close_params.v1")
    miss = [k for k in REQUIRED if k not in c]
    if miss:
        raise SystemExit("REFUSED: the parameters lack: " + ", ".join(miss))
    if c["BOOK"] != book:
        raise SystemExit("REFUSED: the parameters are for book %s, not %s" % (c["BOOK"], book))
    globals().update({k: c[k] for k in REQUIRED})
    globals().update({k: c.get(k, v) for k, v in OPTIONAL.items()})
    globals()["ALL_CONSTANTS"] = c                     # the PENDING gate reads every name, also those only other tools read


def pending_names(x, name):
    """Every place in the parameters that holds the literal PENDING."""
    if x == PENDING:
        return [name]
    if isinstance(x, dict):
        return [p for k, v in sorted(x.items()) for p in pending_names(v, "%s.%s" % (name, k))]
    if isinstance(x, list):
        return [p for i, v in enumerate(x) for p in pending_names(v, "%s[%d]" % (name, i))]
    return []


def family_state(name):
    """True when the family runs; False when a named switch with a reason turns it off; None when the switch is invalid."""
    f = FAMILIES.get(name) if isinstance(FAMILIES, dict) else None
    if not isinstance(f, dict) or f.get("enabled") not in (True, False):
        gate("gate family %s is stated in the parameters" % name, False, "no valid entry")
        return None
    if f["enabled"] is True:
        return True
    reason = str(f.get("reason") or "").strip()
    if not reason:
        gate("gate family %s switched off without a reason" % name, False, "a switch carries its reason")
        return None
    gate("gate family %s switched off: %s" % (name, reason), True, reason)
    return False


def family_reason(name):
    return "NOT APPLICABLE: " + str(((FAMILIES or {}).get(name) or {}).get("reason"))


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
    p = subprocess.run([sys.executable, "-B", str(script)] + list(args), cwd=str(BK), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    out = (p.stdout or "").strip().splitlines()
    return p.returncode, (out[-1] if out else "")


def coverage(opt, by_id, low_ids):
    """The coverage validator's per-book feed rule, as the close tools measure it, over one option's rows."""
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
def corpus_gates(lib):
    cp = BK / CORPUS
    b = cp.read_bytes()
    gate("corpus pinned", shab(b) == CORPUS_PIN, shab(b)[:16])
    gate("corpus is LF-only (E-73)", b"\r" not in b and b.endswith(b"\n"))
    rows = jl(cp)
    n = len(rows)
    gate("corpus has %s rows, every one of book %s" % (ROWS, BOOK), n == ROWS and all(r.get("book") == BOOK for r in rows), n)
    held = {r.get("writer_decision_id"): {k: r.get(k, "ABSENT") for k in HOLD_FIELDS} for r in rows
            if any(k not in r or r[k] != v for k, v in HOLD_FIELDS.items())}
    gate("every row candidate_review_complete with null hold fields; no row carries a hold", not held,
         dict(sorted(held.items())[:3]))
    gate("chunk_index 1..N", [r.get("chunk_index_in_book") for r in rows] == list(range(1, n + 1)), n)
    wids = [r.get("writer_decision_id") for r in rows]
    gate("writer_decision_id unique and present", all(wids) and len(set(wids)) == n, n - len(set(wids)))
    order = [(c, v) for c in sorted(lib.LAST_VERSE) for v in range(1, lib.LAST_VERSE[c] + 1)]
    lin = {cv: i for i, cv in enumerate(order)}
    prev, bad, covered, lang_bad, lang = -1, [], 0, [], collections.Counter()
    for r in rows:
        m = re.match(r"^%s\.(\d+)\.(\d+)-%s\.(\d+)\.(\d+)$" % (re.escape(BOOK), re.escape(BOOK)), str(r.get("span")))
        s = lin.get((int(m.group(1)), int(m.group(2)))) if m else None
        e = lin.get((int(m.group(3)), int(m.group(4)))) if m else None
        if s is None or e is None or s != prev + 1 or e < s:
            bad.append(r.get("writer_decision_id"))
            continue
        covered += e - s + 1
        prev = e
        lang[str(r.get("language"))] += 1
        if LANG_ON is True:
            langs = {lib.language_of(c, v) for c, v in order[s:e + 1]}
            want = (LANGUAGE_CODES.get(next(iter(langs))) if len(langs) == 1 else None) or LANGUAGE_MIXED
            if r.get("language") != want:
                lang_bad.append((r.get("writer_decision_id"), r.get("language"), want))
    gate("tiling contiguous over %s WEB verses in %s chapters" % (VERSES, CHAPTERS),
         not bad and covered == lib.TOTAL_VERSES == len(order) == VERSES and prev == len(order) - 1
         and len(lib.LAST_VERSE) == CHAPTERS, {"covered": covered, "breaks": bad[:5]})
    if LANG_ON is True:
        gate("language layer: each row's `language` is what %s.language_of gives over its span" % LOOKUP["label"],
             not lang_bad and not bad and dict(sorted(lang.items())) == LANGUAGE_COUNTS,
             {"counts": dict(sorted(lang.items())), "bad": lang_bad[:3]})
    else:                                   # the switch must be true of the bytes: one language value, the declared one
        gate("language layer off: every row carries the one declared language value",
             not bad and len(lang) == 1 and dict(sorted(lang.items())) == LANGUAGE_COUNTS, dict(sorted(lang.items())))
    runs = [k for k, _ in itertools.groupby(str(r.get("parent_collection")) for r in rows)]
    kl = len(PARENTS[0])
    gate("each parent collection one contiguous run, %s in order" % PARENTS_LABEL,
         len(runs) == len(set(runs)) and [p[:kl] for p in runs] == PARENTS, [p[:kl] for p in runs])
    moved = [(c, v) for c, v in order if lib.web_to_mt(c, v) != (c, v)]
    if ZONE_ON is True:
        gate("numbering zone as measured: chapters %s, %s WEB verses whose MT reference differs" % (ZONE_LABEL, ZONE_MOVED),
             sorted(lib.ZONE_CHAPTERS) == ZONE and len(moved) == ZONE_MOVED, {"moved": len(moved)})
    else:                                   # the switch must be true of the lookup: nothing moves, and no zone is declared
        gate("numbering zone off: the lookup moves no verse and the parameters declare no zone",
             not moved and not ZONE and ZONE_MOVED == 0, {"moved": len(moved)})
    return rows, moved


def lineage_gates(rows):
    """The final file is its source plus exactly the manifest's (row, field) changes. An absent field and a null field
    are different: the diff is presence-aware."""
    mp = BK / MANIFEST
    gate("lineage manifest pinned", sha(mp) == MANIFEST_PIN, sha(mp)[:16])
    man = jload(mp)
    gate("lineage manifest names this corpus and its source", man.get("names") == PRE + CORPUS
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
        p = BK / rel
        gate("boss audit %s pinned" % tag, sha(p) == pin, sha(p)[:16])
        recs[tag] = {"file": PRE + rel, "sha256": sha(p)}
        got = {c.get("id"): c.get("verdict") for c in jload(p).get("conditions") or []}
        if len(BOSS) > 1 and tag == BOSS[1][0]:                  # applies only when a second record is named
            gate("boss audit %s answers exactly %s" % (tag, BOSS_E2_LABEL), sorted(got) == BOSS_E2_SUPERSEDES, sorted(got))
        verdict.update(got)
    gate("boss audit: conditions %s (REPORTED)" % BOSS_CONDITIONS_LABEL,
         isinstance(BOSS_CONDITIONS, list) and bool(BOSS_CONDITIONS) and sorted(verdict) == sorted(BOSS_CONDITIONS)
         and all(v == "MET" for v in verdict.values()), {k: v for k, v in verdict.items() if v != "MET"})
    return recs


def sidecar_gates(rows):
    low = {r["writer_decision_id"] for r in rows if r["confidence"] in ("medium_low", "low")}
    sp = BK / SIDECAR
    present = gate("sidecar source present (%s)" % SIDECAR, sp.is_file(), sp.name)
    side = jl(sp) if present else []
    ids = [s.get("writer_decision_id") for s in side]
    gate("sidecar set == low/medium_low rows", present and len(ids) == len(set(ids)) and set(ids) == low
         and len(low) == LOW_ROWS, {"missing": sorted(low - set(ids))[:3], "extra": sorted(set(ids) - low)[:3], "rows": len(ids)})
    gate("sidecar fields present", present and all(s.get(k) for s in side for k in SIDE_FIELDS))
    gate("why_low_confidence not boilerplate", present and len({s.get("why_low_confidence") for s in side}) == len(side))
    rc, tail = run(BK / GEN_SIDECARS_REL, "--check")
    gate("gen_sidecars.py --check MATCH", rc == 0 and tail == "MATCH", tail[:200])
    return side


def evidence_gates():
    sp_ = BK / (CORPUS + ".validator_report.json")
    gate("suite report pinned", sha(sp_) == SUITE_PIN, sha(sp_)[:16])
    suite = jload(sp_)
    sm, norm = suite.get("summary") or {}, suite.get(SUITE_NORMALIZE_KEY) or {}
    gate("suite GREEN over this corpus", sm.get("hard_status") == "GREEN" and sm.get("nfd_hard_e01") is False
         and Path(str(suite.get("rows_file"))).name == CORPUS, {"summary": sm, "rows_file": suite.get("rows_file")})
    gate("normalize dry-run clean", norm.get("fixed") == 0 and norm.get("defect_count") == 0,
         {"fixed": norm.get("fixed"), "defect_count": norm.get("defect_count")})
    cs, wq, lz = (suite.get(k) or {} for k in ("citation_sweep", "web_quotes", "language_zones"))
    gate(TEXT["quote_bytes_gate"], cs.get("status") == "GREEN"
         and cs.get("nfd_degraded_count") == 0 and cs.get("rows") == ROWS, {k: cs.get(k) for k in ("status", "nfd_degraded_count", "rows")})
    gate("WEB quote fidelity GREEN", wq.get("status") == "GREEN" and wq.get("flag_count") == 0,
         {k: wq.get(k) for k in ("status", "flag_count")})
    if LANG_ON is True:
        gate("language zones GREEN", lz.get("status") == "GREEN" and lz.get("flag_count") == 0, {k: lz.get(k) for k in ("status", "flag_count")})
    pp = BK / "cwo" / ("cwo_parity.%s.json" % CORPUS.replace(".jsonl", ""))
    gate("CWO parity record pinned", sha(pp) == PARITY_PIN, sha(pp)[:16])
    par = jload(pp)
    gate("CWO parity GREEN for THIS corpus", par.get("post_corpus_sha256") == CORPUS_PIN and par.get("status") == "GREEN"
         and par.get("exact_arm_residual") == [] and par.get("routed_open") == [], {"record": pp.name, "status": par.get("status")})
    rc, tail = run(SP / PARITY_TOOL, *PARITY_ARGS)
    try:
        chk = json.loads(tail)
    except ValueError:
        chk = {}
    gate("CWO parity record reproduces (%s --check MATCH, GREEN)" % Path(PARITY_TOOL).name, rc == 0 and chk.get("check") == "MATCH"
         and chk.get("status") == "GREEN", tail[:200])
    return suite, pp, par


def carrier_gates():
    cp = SP / CARRIER_REL
    c = jload(cp)
    rc, tail = run(SP / CARRIER_GEN_REL, "--check")
    gate("grader carrier still transcribes the ledger (%s --check MATCH)" % Path(CARRIER_GEN_REL).name, rc == 0 and tail == "MATCH", tail[:200])
    gate("grader carrier states the measured fallback (OW-25)", all(c.get(k) == v for k, v in CARRIER_FACTS.items())
         and shab(str(c.get("downgrade_statement", "")).encode("utf-8")) == CARRIER_FACTS["downgrade_statement_sha256"],
         {k: c.get(k) for k in ("ow13_grader_model", "declared_fallback_model", "fallback_in_force")})
    model = c["declared_fallback_model"] if c.get("fallback_in_force") else c["ow13_grader_model"]
    shape = (c.get("book_close_shapes") or {}).get(BOOK) or {}
    gate("carrier grants %s the OW-26 shape (book_close_shapes.%s: shape, directive, transcript_audit, weakness_statement)" % (BOOK_NAME, BOOK),
         bool(shape.get("shape")) and shape.get("directive") == "OW-26" and shape.get("transcript_audit") == "OWED, NOT MET"
         and shape.get("granted_by") == SHAPE_GRANTED_BY
         and bool(shape.get("weakness_statement")), sorted(shape))
    gate("carrier's %s weakness statement matches its recorded digest" % BOOK_NAME, bool(shape.get("weakness_statement"))
         and shab(str(shape.get("weakness_statement")).encode("utf-8")) == shape.get("weakness_statement_sha256"))
    return c, model, shape, sha(cp)


def gate_item(g):
    """The gate item number an assessment entry opens with, or None."""
    m = re.match(r"\s*(?:item[ _]*)?(\d+)\b", str(g.get("item") or g.get("gate") or g.get("id") or ""), re.I)
    return int(m.group(1)) if m else None


def due_at_close(g):
    """R8-GATE-DUE-AT-CLOSE: an item that falls due at the close act itself. The type never joins UNMET_TYPES."""
    return bool(DUE_AT_CLOSE) and isinstance(g, dict) and g.get("met") is False \
        and g.get("type") == DUE_AT_CLOSE["type"] and gate_item(g) in DUE_AT_CLOSE["items"]


def close_evidence_gate():
    """The test the lanes could not make moves here: the close-evidence file holds each due item's value."""
    if not DUE_AT_CLOSE:
        return
    p = BK / str(CLOSE_EVIDENCE_REL)
    pinned = p.is_file() and sha(p) == CLOSE_EVIDENCE_PIN
    vals = (jload(p).get("values") or {}) if pinned else {}
    def absent(v):
        # R9-GATE-TOOLS: the word UNAVAILABLE fails wherever it is written, and a value with no source is not evidence.
        return v.get("value") in (None, "", "UNAVAILABLE") or v.get("tier") == "UNAVAILABLE" or not v.get("source")
    miss = [i for i in DUE_AT_CLOSE["items"] if absent(vals.get("item_%d" % i) or {})]
    gate("close evidence pinned, holding a value for every item due at the close act, none UNAVAILABLE",
         pinned and not miss, {"pinned": pinned, "missing": miss})


def read_record_gate(L, fc):
    """R8-PAIR: every corpus row is read whole by this lane or held by byte equality to the rows its first attempt read,
    and every changed row and both its seam neighbours are read."""
    if READ_RECORD is None:
        return
    def by_id(raw):
        lines = [l for l in raw.split(b"\n") if l.strip()]
        return {json.loads(l)["decision_id"]: l for l in lines}
    now = by_id((BK / CORPUS).read_bytes())
    base_rel = READ_RECORD.get("base_rows_rel")
    bp = BK / str(base_rel) if base_rel else None
    # R9-GATE-TOOLS: a READ_RECORD with no base rows names nothing to compare, so the gate is unmet rather than passed.
    base_ok = bp is not None and bp.is_file() and sha(bp) == READ_RECORD.get("base_rows_pin")
    base = by_id(bp.read_bytes()) if base_ok else {}
    read, held = set(fc.get("rows_read") or []), set(fc.get("rows_held_by_byte_equality") or [])
    ids = list(now)
    changed = [i for i, k in enumerate(ids) if base.get(k) != now[k]] if bp is not None else []
    must = {ids[j] for i in changed for j in (i - 1, i, i + 1) if 0 <= j < len(ids)}
    bad = {"unaccounted": sorted(set(ids) - read - held), "unknown": sorted((read | held) - set(ids)),
           "both": sorted(read & held), "held_but_changed": sorted(held & {ids[i] for i in changed}),
           "not_read": sorted(must - read)}
    gate("lane %s: final check accounts for every corpus row, read whole or held by byte equality, and reads every changed row and its neighbours" % L,
         base_ok and not any(bad.values()), {"base_pinned": base_ok, **{k: v[:6] for k, v in bad.items()}})


def lane_gates(model, fallback, feed_sha):
    """One blind pair (OW-19 floor). The close has no delta round, so the pair itself must be fit: nothing is docketed away."""
    close_evidence_gate()
    lanes = {}
    landing = BK / LANDING_REL
    land = jload(landing) if landing.is_file() else None
    if not gate("landing manifest present (%s)" % LANDING_REL, land is not None, landing.name):
        gate("two distinct blind lanes, both landed and both read", False, "no landing manifest")
        return lanes, None
    rp = BK / MERGED_RECEIPTS_REL
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
        untyped = [g for g in unmet if not (isinstance(g, dict) and g.get("met") is False and g.get("type") in UNMET_TYPES)
                   and not due_at_close(g)]
        read_record_gate(L, fc)
        gate("lane %s: close-gate assessment present; every unmet entry is typed deferred (OW-28) or owed (transcript audit)" % L,
             bool(cga) and not untyped, {"entries": len(cga), "unmet": len(unmet), "untyped": len(untyped)})
        typed = [g.get("type") for g in unmet if isinstance(g, dict) and not due_at_close(g)]
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
        lanes[L] = {"attempt_id": att, "files": {k: [(PRE + LANDING_REL).rsplit("/", 1)[0] + "/" + v.relative_to(landing.parent).as_posix(),
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
    d = BK / "scholar_record"
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
    return {"record": PRE + "scholar_record/" + SCHOLAR_FILES[2], "record_sha256": rec_sha,
            "check": PRE + "scholar_record/" + SCHOLAR_FILES[3], "check_sha256": sha(d / SCHOLAR_FILES[3]),
            "check_said": said, "tier": "REPORTED by the installed checker's record; the checker is not run by this tool"}


def fable_gates(rows, side_sha):
    """OW-28: the least-confident rows and the routed items wait for the campaign-end review. The packet must reproduce,
    be built over this corpus, and hold exactly the low and medium_low rows with their installed sidecars."""
    gen, pkp = SP / PACKET_GEN, BK / PACKET_REL
    rp = BK / ROUTED_REL
    gate("routed items pinned", sha(rp) == ROUTED_PIN, sha(rp)[:16])
    have = gate("fable end packet and its generator installed", gen.is_file() and pkp.is_file())
    rc, tail = run(gen, *PACKET_GEN_ARGS) if have else (1, "absent")
    gate("fable end packet reproduces (--check MATCH)", rc == 0 and tail == "MATCH", tail[:200])
    pk = jload(pkp) if have else {}
    low = sorted(r["decision_id"] for r in rows if r["confidence"] in ("low", "medium_low"))
    gate("fable end packet over this corpus, rows == low/medium_low", pk.get("corpus_sha256") == CORPUS_PIN
         and sorted(pk.get("row_ids") or []) == low, {"rows": len(pk.get("row_ids") or []), "want": len(low)})
    gate("fable end packet carries the %s routed items" % ROUTED_ITEMS, pk.get("routed_items_count") == ROUTED_ITEMS
         and len(pk.get("routed_item_ids") or []) == ROUTED_ITEMS, pk.get("routed_items_count"))
    gate("fable end packet carries the installed sidecars", side_sha is not None
         and (pk.get("sidecar_source") or {}).get("sha256") == side_sha, str((pk.get("sidecar_source") or {}).get("sha256"))[:16])
    gate("fable end packet records DEFERRED and no held row", str(pk.get("status", "")).startswith("DEFERRED (OW-28)")
         and pk.get("held_rows") == {}, str(pk.get("status"))[:40])
    return pk, sha_or_none(pkp)


def retention_gates(fixture):
    """Retention rows: every landed output and the three attempt-receipt files, by the paths the manifest names."""
    lp = BK / LANDED_REL
    gate("landed-outputs manifest pinned", sha(lp) == LANDED_PIN, sha(lp)[:16])
    m = jload(fixture if fixture else lp)
    pre = PRE
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
    gate("the %s attempt-receipt files the landed manifest names are on disk, whole and LF-only" % {3: "three"}.get(LANDED_RECEIPT_FILES, LANDED_RECEIPT_FILES),
         not rbad and len(recs) == len(rset) == LANDED_RECEIPT_FILES,
         {"receipt_files": len(recs), "bad": rbad[:3], "digest_moved_since_the_manifest": [x["path"] for x in drift]})
    return dump(out), out, drift


def target_gates(next_book):
    gate("book_chunks/%s/chunks.jsonl absent" % BOOK, not (M8 / "book_chunks" / BOOK / "chunks.jsonl").exists())
    gate("receipts/%s_completion.json absent" % BOOK, not (M8 / "receipts" / ("%s_completion.json" % BOOK)).exists())
    gate("retention manifest absent", not (BK / RETENTION).exists())
    gate("no close lock is held", not (M8 / LOCK_NAME).exists(), LOCK_NAME)
    shared = {}
    for n in SHARED:
        b = (M8 / n).read_bytes()
        shared[n] = b
        gate("%s holds no %s row" % (n, BOOK), ('"book": "%s"' % BOOK) not in b.decode("utf-8"))
        gate("%s is LF-only and ends with a newline" % n, b"\r" not in b and (not b or b.endswith(b"\n")))
    pb, mb = (M8 / "marathon_progress.yaml").read_bytes(), (M8 / "model_manifest.yaml").read_bytes()
    prog, man = pb.decode("utf-8"), mb.decode("utf-8")
    anchor = "  %s:\n    status: complete\ncurrent_book: %s\n" % (PREV_BOOK, BOOK)
    gate("marathon_progress anchors", prog.count(anchor) == 1 and prog.endswith(anchor)
         and prog.count("books_completed: %d\n" % BOOKS_BEFORE) == 1 and ("  %s:\n" % BOOK) not in prog and b"\r" not in pb)
    gate("model_manifest anchors", man.count("books_completed: %d\n" % BOOKS_BEFORE) == 1
         and man.count("current_book: %s\n" % BOOK) == 1 and b"\r" not in mb)
    gate("--next-book given and valid (%s)" % NEXT_BOOK_LABEL,
         bool(next_book) and bool(re.match(NEXT_BOOK_PATTERN, next_book or "")) and next_book != BOOK
         and (NEXT_BOOK_EXPECTED is None or next_book == NEXT_BOOK_EXPECTED)
         and ("  %s:\n" % next_book) not in prog, next_book)
    return prog, man, shared, pb, mb, anchor


# ------------------------------------------------------------------ close ------------------------------------------------
def commit(plan):
    """plan: [(relative path, new bytes, bytes the gates read or None when the file must be absent)]. All or nothing."""
    lock = M8 / LOCK_NAME
    fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    done, made = [], []
    try:
        os.write(fd, ("%s close in progress\n" % BOOK).encode("utf-8"))
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
    ap.add_argument("--book", required=True)
    ap.add_argument("--params", help="dry-mode TEST HOOK: a parameter file other than <BOOK>/close/close_params.v1.json")
    ap.add_argument("--dry-report")
    ap.add_argument("--close", action="store_true")
    ap.add_argument("--m8-root")
    ap.add_argument("--acf", choices=("lam_pattern", "item22"))
    ap.add_argument("--next-book")
    ap.add_argument("--fixture-landed", help="dry-mode TEST HOOK: a landed-outputs manifest other than the pinned one")
    a = ap.parse_args()
    own = HERE.parent.parent
    if not BOOK_RE.match(a.book):
        raise SystemExit("REFUSED: --book is not a book name")
    if a.close and (a.m8_root or a.fixture_landed or a.dry_report or a.params):
        raise SystemExit("REFUSED: --close runs only on the tree this tool is installed in, with no test hook and no --dry-report")
    bind(Path(a.m8_root).resolve() if a.m8_root else own, a.book)
    if not a.m8_root and SP / "campaign" != HERE:
        raise SystemExit("REFUSED: this file is not installed at <M8>/sp_durable/campaign; pass --m8-root to evaluate a tree")
    params_path = Path(a.params).resolve() if a.params else BK / PARAMS_REL
    if not params_path.is_file():
        raise SystemExit("REFUSED: no parameter file at %s" % params_path)
    load_params(jload(params_path), a.book)
    dry = None
    if a.dry_report:
        dry = Path(a.dry_report).resolve()
        for root in (M8, own if (own / "sp_durable" / "campaign") == HERE else M8):
            if dry == root or root in dry.parents:
                raise SystemExit("REFUSED: --dry-report is inside the M8 tree")
    usage = jload(a.usage[1:]) if a.usage and a.usage.startswith("@") else {}
    hooks = (["--fixture-landed"] if a.fixture_landed else []) + (["--params"] if a.params else [])
    global LANG_ON, ZONE_ON
    pend = [p for k in sorted(ALL_CONSTANTS) for p in pending_names(ALL_CONSTANTS[k], k)]
    gate("no parameter is PENDING (every pin measured from disk)", not pend, pend[:40])
    LANG_ON, ZONE_ON = family_state(FAMILY_NAMES[0]), family_state(FAMILY_NAMES[1])

    def imp():
        p = BK / LOOKUP["path"]
        gate("%s pinned" % LOOKUP["label"], sha(p) == LOOKUP["pin"], sha(p)[:16])
        if LOOKUP["kind"] == "module":
            sys.path.insert(0, str(p.parent))
            return importlib.import_module(LOOKUP["module"])
        if LOOKUP["kind"] != "inventory":
            raise ValueError("LOOKUP.kind is neither module nor inventory")
        inv = jload(p)
        gate("verse inventory declares the %s numbering face" % LOOKUP["face"], inv.get("numbering_face") == LOOKUP["face"],
             inv.get("numbering_face"))
        return types.SimpleNamespace(LAST_VERSE={int(c): int(v) for c, v in inv["chapters"].items()},
                                     TOTAL_VERSES=inv["total_verses"], ZONE_CHAPTERS=[],
                                     web_to_mt=lambda c, v: (c, v), language_of=None)
    lib = guard(LOOKUP["label"], imp, None)
    rows, moved = guard("corpus", lambda: corpus_gates(lib), (None, []))
    corpus_read = rows is not None
    if rows is None and not a.close:
        rows = []                                   # every other group is still evaluated; no gate passes on no rows
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
    feed_p = BK / FEED_REL
    feed_sha = sha_or_none(feed_p)
    lanes, landing_sha = guard("lanes", lambda: lane_gates(model, carrier.get("fallback_in_force"), feed_sha), ({}, None))
    scholar = guard("scholar record", scholar_gates, {})
    pk, pk_sha = guard("fable end packet", lambda: fable_gates(rows, sha_or_none(BK / SIDECAR)), ({}, None))
    ret_bytes, ret, drift = guard("retention", lambda: retention_gates(Path(a.fixture_landed).resolve() if a.fixture_landed else None),
                                  (b"", [], []))
    prog, mant, shared, pb, mb, anchor = guard("targets", lambda: target_gates(a.next_book), (None, None, {}, None, None, None))
    gate("--acf chosen (the owner's choice between lam_pattern and item22)", a.acf is not None, a.acf)

    # --- payloads ---
    final = []
    for i, r in enumerate(rows, 1):
        fr = dict(r)
        fr["decision_id"] = DECISION_ID_FORM % i
        final.append(fr)
    payload = dump(final)
    by = {s.get("writer_decision_id"): s for s in side}
    lcr, feq, acf_lam = [], [], []
    for r in final:
        s = by.get(r["writer_decision_id"])
        if not s:
            continue
        common = {"model_id": MODEL_ID, "book": BOOK, "span": r["span"], "chunk_decision_id": r["decision_id"],
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
    gate("item-22 feed installed; its rows name only chunks of this book", acf_item22 is not None and corpus_read
         and all(x.get("book") == BOOK and x.get("chunk_decision_id") in by_id for x in acf_item22),
         "%s sha256 %s" % (FEED_REL, str(feed_sha)[:16]))
    opts = {"lam_pattern": acf_lam, "item22": acf_item22}
    cov = {k: (coverage(v, by_id, low_ids) if v is not None else None) for k, v in opts.items()}
    acf = opts.get(a.acf)
    if a.acf:
        gate("atlas feed option %s meets the coverage validator's per-book rule" % a.acf,
             cov[a.acf] is not None and cov_ok(cov[a.acf]) and bool(final), cov_brief(cov[a.acf]) if cov[a.acf] else "option unavailable")
    for k, v in (("low_confidence_register", lcr), ("frontier_escalation_queue", feq)):
        c = coverage(v, by_id, low_ids)
        gate("%s rows meet the coverage validator's per-book rule" % k, cov_ok(c) and bool(final), cov_brief(c))
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
    chunks_rel, ret_rel, rec_rel = "book_chunks/%s/chunks.jsonl" % BOOK, PRE + RETENTION, "receipts/%s_completion.json" % BOOK
    receipt = {
        "book": BOOK, "model_id": MODEL_ID,
        "mesh_revision": TEXT["mesh_revision"],
        "rows": len(final), "chunks": len(final), "parents": sorted({r["parent_collection"] for r in final}),
        "verses_covered": VERSES, "chapters": CHAPTERS, "chunk_file_sha256": shab(payload),
        "final_corpus": CORPUS, "final_corpus_sha256": CORPUS_PIN,
        "corpus_lineage_sha256": {BUILT_FROM + " (the source)": BUILT_FROM_PIN, PRE + MANIFEST: MANIFEST_PIN,
                                  PRE + CORPUS: CORPUS_PIN,
                                  "change_rule": man.get("change_rule"), "fields_changed_in_every_row": LINEAGE_FIELDS},
        "holds": "none: every row is candidate_review_complete with null hold fields (MEASURED by the close tool's gate)",
        "confidence_final": order(conf), "unit_type_distribution": order(ut), "language_distribution": order(lang),
        "language_layer": TEXT["language_layer"] if LANG_ON is True else family_reason(FAMILY_NAMES[0]),
        "numbering_disclosure": {"web_verses_whose_mt_reference_differs": len(moved),
                                 "first": "%s.%d.%d" % ((BOOK,) + moved[0]) if moved else None,
                                 "last": "%s.%d.%d" % ((BOOK,) + moved[-1]) if moved else None, "zone_chapters": ZONE,
                                 "spans_are_in": "WEB versification", "computed_by": TEXT["numbering_computed_by"]}
        if ZONE_ON is True else {"not_applicable": family_reason(FAMILY_NAMES[1]), "spans_are_in": "WEB versification"},
        "grader_fallback": {"model": carrier.get("declared_fallback_model"), "replaces": carrier.get("ow13_grader_model"),
                            "statement": carrier.get("downgrade_statement"),
                            "carrier": "sp_durable/" + CARRIER_REL, "carrier_sha256": carrier_sha},
        "ow26_merged_verdict_close": {"directive": shape.get("directive"), "shape": shape.get("shape"),
                                      "weakness_statement": shape.get("weakness_statement"),
                                      "transcript_audit": "OWED, NOT MET"},
        "transcript_audit": "OWED, NOT MET",
        "fable_end_review": {"status": "DEFERRED (OW-28)", "reviewer": "claude-fable-5-1, at the campaign's end",
                             "packet": PRE + PACKET_REL,
                             "packet_sha256": pk_sha, "rows": pk.get("row_ids"),
                             "routed_items": pk.get("routed_items_count"), "routed_items_sha256": ROUTED_PIN,
                             "deferred_assessment_entries": {L: [u for u in v["unmet"] if u["type"] == UNMET_TYPES[0]]
                                                             for L, v in fcs.items()},
                             "limit": "DEFERRED is never MET. No Fable call is made without a new owner authorization (OW-30)."},
        "boss_audit": {"tier": "REPORTED", "records": boss, "conditions": TEXT["boss_conditions"]},
        "scholar_record": scholar,
        "campaign_close_gate_evidence": {
            "item5_cwo_execution_parity": {"record": PRE + "cwo/" + pp.name if pp else None,
                                           "sha256": sha_or_none(pp) if pp else None,
                                           "corpus_reconciled": par.get("post_corpus_sha256"), "status": par.get("status"),
                                           "exact_arm_residual": par.get("exact_arm_residual"), "routed_open": par.get("routed_open")},
            TEXT["quote_bytes_receipt_key"]: sg("citation_sweep", ("status", "nfd_degraded_count", "rows")),
            "item5_web_quote_gloss_fidelity": sg("web_quotes", ("status", "flag_count")),
            "item5_unicode_normalization": sg(SUITE_NORMALIZE_KEY, ("ok", "fixed", "defect_count")),
            **({"item5_language_zones": sg("language_zones", ("status", "flag_count"))} if LANG_ON is True else {}),
            "item5_suite_report_sha256": SUITE_PIN,
            "item5_review_packet_retention": {"manifest": ret_rel, "files": len(ret),
                                              "bytes": sum(o["bytes"] for o in ret), "manifest_sha256": shab(ret_bytes),
                                              "built_from": PRE + LANDED_REL, "built_from_sha256": LANDED_PIN,
                                              "scope": "the landed outputs that manifest lists and the three attempt-receipt "
                                                       "files it names; not a walk of the review directory",
                                              "attempt_receipt_files_changed_since_that_manifest": drift},
            "item5_final_review_status": dict(sorted(collections.Counter(str(r.get("review_status")) for r in final).items())),
            "item10_ow6_final_check_merged": {
                "landing_manifest": PRE + LANDING_REL, "landing_manifest_sha256": landing_sha,
                "lanes": {L: {"attempt_id": v["attempt_id"], "files": v["files"], "model": v["final_check"].get("model"),
                              "postcheck_verdict": v["postcheck"].get("verdict"), "final_check_verdict": v["final_check"].get("verdict"),
                              "corpus_sha256_audited": v["final_check"].get("corpus_sha256"),
                              "transcript_coverage": v["final_check"].get("transcript_coverage"),
                              "unmet_assessment_entries": v["unmet"],
                              "items_20_23": {i: (v["items"].get(i) or {}).get("fit_to_accept") for i in
                                              ("item_20", "item_21", "item_22", "item_23")}} for L, v in fcs.items()},
                "authority": TEXT["item10_authority"]},
        },
        "shared_feed_rows": {"low_confidence_register": len(lcr), "frontier_escalation_queue": len(feq),
                             "atlas_candidate_feed": {"source": a.acf, "rows": len(acf) if acf is not None else None}},
        "not_evaluated_by_this_tool": NOT_EVALUATED,
        TEXT["authority_key"]: TEXT["authority_text"],
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
        new_prog = prog.replace(anchor, "  %s:\n    status: complete\n  %s:\n    status: complete\ncurrent_book: %s\n" % (PREV_BOOK, BOOK, next_book))
        new_prog = new_prog.replace("books_completed: %d\n" % BOOKS_BEFORE, "books_completed: %d\n" % BOOKS_AFTER)
        new_man = mant.replace("books_completed: %d\n" % BOOKS_BEFORE, "books_completed: %d\n" % BOOKS_AFTER).replace(
            "current_book: %s\n" % BOOK, "current_book: %s\n" % next_book)
    writes = {chunks_rel: payload, ret_rel: ret_bytes,
              rec_rel: rec_bytes,
              "APPEND low_confidence_register.jsonl": dump(lcr), "APPEND frontier_escalation_queue.jsonl": dump(feq),
              "APPEND whole_bible_chunk_map.jsonl": payload}
    if acf is not None:
        writes["APPEND atlas_candidate_feed.jsonl"] = dump(acf)
    if new_prog is not None:
        writes["EDIT marathon_progress.yaml"] = new_prog.encode("utf-8")
        writes["EDIT model_manifest.yaml"] = new_man.encode("utf-8")
    gate("every close write is LF-only", bool(payload) and all(b"\r" not in v for v in writes.values()))
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
              "corpus_read": corpus_read, "params_sha256": sha(params_path),
              "gate_families": FAMILIES,
              "tool_sha256": sha(Path(__file__).resolve()),
              "receipt_files_changed_since_the_manifest": drift,
              "deferred_never_met": {"fable_end_review": "DEFERRED (OW-28)", "packet_sha256": pk_sha,
                                     "transcript_audit": "OWED, NOT MET"},
              "next_book": a.next_book, "not_evaluated_by_this_tool": NOT_EVALUATED}

    if dry is not None:
        dry.mkdir(parents=True, exist_ok=True)
        pre = {"%s_completion.preview.json" % BOOK: rec_bytes, RETENTION.replace(".v1.jsonl", ".preview.jsonl"): ret_bytes,
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

    # --- CLOSE (the act's authority is the book's, TEXT.authority_text). Every target was proven absent or anchored above; commit() proves it
    # again under the lock. Order as the close tools have always written: chunks, retention, the four appends, the receipt, the carriers.
    plan = [(chunks_rel, payload, None),
            (ret_rel, ret_bytes, None),
            ("low_confidence_register.jsonl", shared[SHARED[0]] + dump(lcr), shared[SHARED[0]]),
            ("frontier_escalation_queue.jsonl", shared[SHARED[1]] + dump(feq), shared[SHARED[1]]),
            ("atlas_candidate_feed.jsonl", shared[SHARED[2]] + dump(acf), shared[SHARED[2]]),
            ("whole_bible_chunk_map.jsonl", shared[SHARED[3]] + payload, shared[SHARED[3]]),
            (rec_rel, rec_bytes, None),
            ("marathon_progress.yaml", new_prog.encode("utf-8"), pb),
            ("model_manifest.yaml", new_man.encode("utf-8"), mb)]
    commit(plan)
    print(json.dumps({"status": "CLOSED", "chunks": len(final), "receipt_sha256": shab(rec_bytes),
                      "progress": "%s complete -> %s (%d/66)" % (BOOK, a.next_book, BOOKS_AFTER), "acf": a.acf,
                      "written": [p[0] for p in plan]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
