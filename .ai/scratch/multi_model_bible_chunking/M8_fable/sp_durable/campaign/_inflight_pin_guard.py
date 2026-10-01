#!/usr/bin/env python3
"""In-flight pin guard: before appending to or mutating a record, check whether an execution that is still RUNNING has a
brief or orders file that pins that record by digest.

WHY (ledger OW-11-i, 2026-09-11). The orchestrator appended two cure-claim lines to SP/Ezek/ezek_cure_claims.v1.jsonl while
the distinct reviewer S1 was running with that file pinned in its brief. S1 caught the change and verified it, but the
reviewer's binding to its launch bytes was broken by the orchestrator's own write. A record that a running review has
pinned is not written until that review lands, unless the deviation is recorded first.

IN FLIGHT means the book's transcript map names an execution_id that no *_attempt_receipts.jsonl under the book records.
PINNED means a file that names that execution carries the target's path on a line with a 64-hex digest. The files
searched are the book's top-level *.md briefs and its orders JSON files. A file naming the full execution id
('<attempt>#eN') is preferred, and so is one naming a template id this execution fills with its ordinal (`x_<part>_a1_e1`
for x_p01_a1#e1). Only when no file names the execution that way is the attempt used: the bare attempt id, alone or inside a
file name such as `orders_<attempt>.json`, or a template id without an ordinal that the attempt id fills (OW-11-l,
2026-09-11: SP/Ezek/FIXUP_BRIEF.md named its eleven executions only through a template, so its pins were invisible here).

AND an execution's OWN BRIEF is pinned by it, with everything that brief's input table pins, for the life of the
execution - whether or not the brief names the execution (OW-14 L-0035, corrected 2026-09-15). The brief path comes from
the launch record: a `brief` (or `orders`) field on the book's transcript-map entry. WHY: SP/Ezek/PRIMARY_BRIEF_LF.md is
shared by all 22 literary-form primaries, names none of them and does not list itself, so a running primary had NO
visible pins at all - not its brief, not the corpus row file it binds, not the cluster plan. The guard read CLEAR on
every one of them with eight executions in flight. A brief a running agent is reading is never edited, and the tool that
is supposed to enforce that must be at least as strict as the playbook line, not weaker.

AND a LAUNCH RECEIPT is a launch record, never a landing (2026-09-22). A receipt line with `record_kind: "launch"` names an
execution that is IN FLIGHT until a later line that is not a launch record names the same execution by `execution_id` or
`amends_execution_id`. Its `brief`/`orders` field counts as that execution's own brief, exactly like the transcript-map
field, and a `sp_durable/` prefix on it is read as SP. WHY: the two Ezekiel merged-close lanes were recorded ONLY by
launch receipts in ezek_merged_close_attempt_receipts.jsonl, with no transcript-map entry. The guard read every line of a
receipts file as a landing, so both lanes counted as landed before they had started, and it read CLEAR on the corpus and
on the M8 ledger that their briefs pin by digest, for every target, all session. A pin written `SP\\..\\X` (a file outside
SP, such as the M8 ledger) is also matched now: pinned paths and targets are both normalised to SP-relative posix paths
with `..` segments resolved.

AND a row lands an execution only if it carries an OUTCOME (2026-09-24). A row that is not a launch record lands the
execution it names by `execution_id` or `amends_execution_id` only when its `outcome` is non-empty and does not open with
RUNNING. WHY: an amendment row (a token-field correction, say) names its execution by `amends_execution_id` and carries
no outcome. Written while that execution was running, it would have landed it here and released every pin of its brief.
MEASURED before the change, over every book directory under SP: 0 executions were landed only by rows without an
outcome, so no verdict moved.

Usage: _inflight_pin_guard.py --book Ezek --target <path> [--target <path> ...]
       _inflight_pin_guard.py --selftest
Exit 0 CLEAR, 1 PINNED, 2 usage or input error. Read-only."""
import argparse
import json
import os
import posixpath
import re
import sys
import tempfile
from pathlib import Path

SP = Path(__file__).resolve().parent.parent
DIGEST = re.compile(r"\b[0-9a-f]{64}\b")
PATHISH = re.compile(r"(?:SP[\\/])?((?:[A-Za-z0-9_.-]+[\\/])*[A-Za-z0-9_.#%-]+\.(?:jsonl|json|md|py|txt))")
TEMPLATE = re.compile(r"[A-Za-z0-9_]*<[A-Za-z]+>[A-Za-z0-9_]*")   # a template id such as ezek_author_fixup_<part>_a1_e1


def rel(p, sp):
    """An SP-relative posix path; a file outside SP on the same drive gets `..` segments (the M8 ledger is `../X`)."""
    p = Path(p)
    try:
        return p.resolve().relative_to(sp.resolve()).as_posix()
    except ValueError:
        try:
            return Path(os.path.relpath(p.resolve(), sp.resolve())).as_posix()
        except ValueError:   # another drive
            return str(p).replace("\\", "/").removeprefix("SP/")


def norm(r):
    return posixpath.normpath(r.replace("\\", "/"))


def receipt_rows(sp, book):
    """(file name, row) for every row of every *_attempt_receipts.jsonl under the book."""
    for f in sorted((sp / book).rglob("*_attempt_receipts.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                yield f.name, json.loads(line)


def launch_records(sp, book):
    """(source name, record) for every launch record: a transcript-map entry, or a receipt row with record_kind launch."""
    for m in sorted((sp / book).glob("_transcript_map*.json")):
        for v in json.loads(m.read_text(encoding="utf-8-sig")).values():
            if isinstance(v, dict) and v.get("execution_id"):
                yield m.name, v
    for name, r in receipt_rows(sp, book):
        if r.get("record_kind") == "launch" and r.get("execution_id"):
            yield name, r


def lands(r):
    """A row lands the execution it names only if it is not a launch record and its outcome is non-empty, not RUNNING."""
    o = str(r.get("outcome") or "").strip()
    return r.get("record_kind") != "launch" and bool(o) and not o.upper().startswith("RUNNING")


def in_flight(sp, book):
    launched = {v["execution_id"] for _, v in launch_records(sp, book)}
    landed = set()
    for _, r in receipt_rows(sp, book):
        if not lands(r):
            continue   # a launch receipt says the execution STARTED, and an outcome-less amendment says nothing of its end
        landed.update(x for x in (r.get("execution_id"), r.get("amends_execution_id")) if x)
    return sorted(x for x in launched if x not in landed)


def under_sp(v, sp):
    """A launch record's brief path, normalised to an SP-relative posix path. Accepts `SP\\Book\\B.md`, `Book/B.md`,
    `sp_durable/Book/B.md` (a path relative to M8) and an absolute path inside SP."""
    s = str(v).replace("\\", "/").strip().removeprefix("SP/").removeprefix("sp_durable/")
    p = Path(s)
    return rel(p, sp) if p.is_absolute() else norm(p.as_posix())


def own_briefs(sp, book):
    """execution_id -> {SP-relative brief path: {the launch-record files that record it}}, from the launch record's
    `brief` or `orders` field, in a transcript map or a launch receipt. Read by pins_for so that the brief AND its whole
    input table count as that execution's pins."""
    out = {}
    for src, v in launch_records(sp, book):
        for field in ("brief", "brief_path", "orders", "orders_path"):
            got = v.get(field)
            for one in ([got] if isinstance(got, str) else (got or [])):
                # only a path-shaped value: a launch receipt's `orders` may be prose ("inline 12 lines: ...")
                if isinstance(one, str) and PATHISH.fullmatch(one.strip().replace("\\", "/").split(":/")[-1]):
                    out.setdefault(v["execution_id"], {}).setdefault(under_sp(one, sp), set()).add(src)
    return out


def fills_template(text, xid, with_ordinal):
    """True when TEXT carries a template id (a placeholder such as <part>) that this execution fills: with its _eN ordinal when
    with_ordinal, else as the bare attempt id (OW-11-l)."""
    aid, _, n = xid.partition("#e")
    if with_ordinal and not n:
        return False
    want = ("%s_e%s" % (aid, n)) if with_ordinal else aid
    for tok in set(TEMPLATE.findall(text)):
        if re.fullmatch(re.sub(r"<[A-Za-z]+>", "[A-Za-z0-9]+", re.escape(tok)), want):
            return True
    return False


def pins_for(sp, book, xid, own=None):
    own = own or {}
    files = sorted((sp / book).glob("*.md")) + sorted((sp / book).rglob("orders*.json"))
    texts = {f: f.read_text(encoding="utf-8", errors="replace") for f in files}
    for r in own:   # an execution's own brief is read even when it is neither a top-level *.md nor an orders*.json
        p = sp / r
        if p not in texts and p.is_file():
            texts[p] = p.read_text(encoding="utf-8", errors="replace")
    naming = [f for f, t in texts.items() if xid in t or fills_template(t, xid, True)]
    if not naming:
        aid = xid.split("#")[0]
        naming = [f for f, t in texts.items() if re.search(r"(?<![A-Za-z0-9])(?:[a-z]+_)?%s(?![A-Za-z0-9_])" % re.escape(aid), t)
                  or fills_template(t, xid, False)]
    naming = sorted(set(naming) | {sp / r for r in own if (sp / r) in texts}, key=lambda q: q.as_posix())
    # the brief itself is pinned by the launch record, whether or not it lists itself with a digest
    pinned = {r: {"%s (launch record: this execution's own brief)" % s for s in srcs} for r, srcs in own.items()}
    for f in naming:
        if f.suffix == ".json":
            # an orders file keeps a path and its digest as sibling keys on separate lines (and escapes backslashes in
            # its raw text), so it is parsed: a dict pins every path-like string value when one of its values is a digest
            try:
                stack = [json.loads(texts[f])]
            except json.JSONDecodeError:
                stack = []
            while stack:
                o = stack.pop()
                if isinstance(o, dict):
                    vals = [v for v in o.values() if isinstance(v, str)]
                    if any(DIGEST.fullmatch(v.strip()) for v in vals):
                        for v in vals:
                            m = PATHISH.fullmatch(v.strip())
                            if m:
                                pinned.setdefault(norm(m.group(1)), set()).add(f.name)
                    stack.extend(o.values())
                elif isinstance(o, list):
                    stack.extend(o)
            continue
        # a pin written SP-relative with `..` (the M8 ledger is `SP\..\ERROR_PATTERN_LEDGER.v1.md`) is normalised and
        # detected; limitation: a pin written as an ABSOLUTE path is still not recognised
        for line in texts[f].splitlines():
            if DIGEST.search(line):
                for m in PATHISH.finditer(line):
                    pinned.setdefault(norm(m.group(1)), set()).add(f.name)
    return pinned


def check(sp, book, targets):
    flight = in_flight(sp, book)
    own = own_briefs(sp, book)
    out = {"book": book, "in_flight": flight, "targets": {}}
    for t in targets:
        r = rel(t, sp)
        by = []
        for xid in flight:
            hit = pins_for(sp, book, xid, own.get(xid)).get(r)
            if hit:
                by.append({"execution_id": xid, "pinned_in": sorted(hit)})
        out["targets"][r] = {"verdict": "PINNED" if by else "CLEAR", "pinned_by": by}
    out["verdict"] = "PINNED" if any(v["verdict"] == "PINNED" for v in out["targets"].values()) else "CLEAR"
    return out


def selftest():
    d64 = "a" * 64
    with tempfile.TemporaryDirectory() as td:
        sp = Path(td) / "sp_durable"
        b = sp / "Book"
        (b / "receipts").mkdir(parents=True)
        tmap = {"x_a1_wave2": {"execution_id": "x_a1#e2", "agent_id": "a1"}, "y_a1": {"execution_id": "y_a1#e1"},
                "z_a1": {"execution_id": "z_a1#e1"}, "old_entry": {"agent_id": "a0"},
                "s_p01_a1": {"execution_id": "s_p01_a1#e1"}, "n_a1": {"execution_id": "n_a1#e1"},
                # L-0035: two in-flight executions reading ONE brief that names neither of them and does not list
                # itself, recorded only by the launch record's `brief` field - in a backslash and a posix spelling
                "n1_a1": {"execution_id": "n1_a1#e1", "brief": "SP\\Book\\BRIEF_SHARED_NOID.md"},
                "n2_a1": {"execution_id": "n2_a1#e1", "brief": "Book/BRIEF_SHARED_NOID.md"},
                "lnd_a1": {"execution_id": "lnd_a1#e1", "brief": "Book/BRIEF_LANDED_ONLY.md"}}
        (b / "_transcript_map.book.json").write_text(json.dumps(tmap), encoding="utf-8")
        (b / "receipts" / "r_attempt_receipts.jsonl").write_text(
            json.dumps({"execution_id": "y_a1#e1", "outcome": "COMPLETED"}) + "\n"
            + json.dumps({"execution_id": "lnd_a1#e1", "outcome": "COMPLETED"}) + "\n",
            encoding="utf-8")
        (b / "BRIEF_X.md").write_text("execution id `x_a1#e2`\n| `SP\\Book\\pinned.jsonl` | `%s` |\n" % d64, encoding="utf-8")
        (b / "BRIEF_X_OLD.md").write_text("execution id `x_a1#e1`\n| `SP\\Book\\old.jsonl` | `%s` |\n" % d64, encoding="utf-8")
        (b / "BRIEF_Y.md").write_text("execution id `y_a1#e1`\n| `SP\\Book\\y.jsonl` | `%s` |\n" % d64, encoding="utf-8")
        (b / "orders_z.json").write_text(json.dumps({"attempt_id": "z_a1", "inputs": [{"path": "SP\\Book\\z.jsonl", "sha256": d64}]}, indent=1),
                                         encoding="utf-8")
        (b / "BRIEF_NODIGEST.md").write_text("execution id `x_a1#e2`\nreads SP\\Book\\nodigest.jsonl\n", encoding="utf-8")
        (b / "BRIEF_SHARED.md").write_text("your subdirectory `OUT\\s_<part>_a1_e1\\`\n| `SP\\Book\\shared.jsonl` | `%s` |\n" % d64,
                                           encoding="utf-8")
        (b / "BRIEF_SHARED_E2.md").write_text("your subdirectory `OUT\\s_<part>_a1_e2\\`\n| `SP\\Book\\shared2.jsonl` | `%s` |\n" % d64,
                                              encoding="utf-8")
        (b / "BRIEF_N.md").write_text("orders file `SP\\Book\\orders_n_a1.json`\n| `SP\\Book\\named.jsonl` | `%s` |\n" % d64, encoding="utf-8")
        # a brief that names NO execution and does not list itself: invisible to every rule above it
        (b / "BRIEF_SHARED_NOID.md").write_text("| `SP\\Book\\corpus.jsonl` | `%s` |\n" % d64, encoding="utf-8")
        (b / "BRIEF_LANDED_ONLY.md").write_text("| `SP\\Book\\landedonly.jsonl` | `%s` |\n" % d64, encoding="utf-8")
        # 2026-09-22: executions recorded ONLY by launch receipts (no transcript-map entry), with M8-relative brief
        # paths; one of them has since landed through a completion row that amends it
        (b / "ml").mkdir()
        (b / "ml" / "ml_attempt_receipts.jsonl").write_text("".join(json.dumps(r) + "\n" for r in (
            {"execution_id": "ml_a1#e1", "attempt_id": "ml_a1", "record_kind": "launch", "outcome": "RUNNING",
             "brief": "sp_durable/Book/BRIEF_ML.md", "orders": "inline 12 lines: verify brief sha, read it whole"},
            {"execution_id": "ml2_a1#e1", "attempt_id": "ml2_a1", "record_kind": "launch", "outcome": "RUNNING",
             "brief": "sp_durable/Book/BRIEF_ML2.md"},
            {"amends_execution_id": "ml2_a1#e1", "attempt_id": "ml2_a1", "record_kind": "completion",
             "outcome": "COMPLETED"},
            # 2026-09-24: a RUNNING execution amended twice, by a row with no outcome and by one whose outcome is
            # RUNNING; neither lands it
            {"execution_id": "ml3_a1#e1", "attempt_id": "ml3_a1", "record_kind": "launch", "outcome": "RUNNING",
             "brief": "sp_durable/Book/BRIEF_ML3.md"},
            {"amends_execution_id": "ml3_a1#e1", "attempt_id": "ml3_a1", "tokens_notification_unit": 1},
            {"execution_id": "ml3_a1#e1", "attempt_id": "ml3_a1", "record_kind": "amendment", "outcome": "RUNNING"})),
            encoding="utf-8")
        (b / "BRIEF_ML3.md").write_text("| `SP\\Book\\ml3corpus.jsonl` | `%s` |\n" % d64, encoding="utf-8")
        (b / "BRIEF_ML.md").write_text("| `SP\\Book\\mlcorpus.jsonl` | `%s` |\n| `SP\\..\\LEDGER.md` | `%s` |\n" % (d64, d64),
                                       encoding="utf-8")
        (b / "BRIEF_ML2.md").write_text("| `SP\\Book\\ml2corpus.jsonl` | `%s` |\n" % d64, encoding="utf-8")
        vectors = [
            ("pinned by an in-flight execution's brief", "Book/pinned.jsonl", "PINNED"),
            ("pinned only by an earlier execution's brief", "Book/old.jsonl", "CLEAR"),
            ("pinned by a landed execution", "Book/y.jsonl", "CLEAR"),
            ("named without a digest", "Book/nodigest.jsonl", "CLEAR"),
            ("attempt-id fallback in an orders file", "Book/z.jsonl", "PINNED"),
            ("not pinned anywhere", "Book/other.jsonl", "CLEAR"),
            ("pinned by a shared brief through a template id with this ordinal", "Book/shared.jsonl", "PINNED"),
            ("a shared brief whose template carries another ordinal", "Book/shared2.jsonl", "CLEAR"),
            ("an attempt id inside a file name the brief names", "Book/named.jsonl", "PINNED"),
            # the L-0035 shape, which every rule above misses
            ("the shared brief an in-flight execution is recorded as reading", "Book/BRIEF_SHARED_NOID.md", "PINNED"),
            ("a file in that shared brief's input table", "Book/corpus.jsonl", "PINNED"),
            ("a brief only a LANDED execution was reading", "Book/BRIEF_LANDED_ONLY.md", "CLEAR"),
            ("a file in a landed execution's brief table", "Book/landedonly.jsonl", "CLEAR"),
            # the 2026-09-22 shape: a launch receipt is not a landing, and its brief field is an own-brief pin
            ("a file pinned by a brief recorded only on a launch receipt", "Book/mlcorpus.jsonl", "PINNED"),
            ("the brief a launch receipt names (M8-relative sp_durable/ path)", "Book/BRIEF_ML.md", "PINNED"),
            ("a file outside SP pinned as SP\\..\\X", "../LEDGER.md", "PINNED"),
            ("a launch-receipt execution landed by an amending completion row", "Book/ml2corpus.jsonl", "CLEAR"),
            # the 2026-09-24 shape: only a row with an outcome lands
            ("a running execution amended by rows with no outcome or a RUNNING one", "Book/ml3corpus.jsonl", "PINNED"),
            ("the own brief of that amended running execution", "Book/BRIEF_ML3.md", "PINNED"),
        ]
        results = []
        for name, tgt, want in vectors:
            got = check(sp, "Book", [sp / tgt])["targets"][tgt]["verdict"]
            results.append({"vector": name, "want": want, "got": got, "ok": got == want})
        ml_own = sorted(own_briefs(sp, "Book").get("ml_a1#e1", {}))
        results.append({"vector": "a prose `orders` value on a launch receipt is not taken as a brief path",
                        "want": "['Book/BRIEF_ML.md']", "got": str(ml_own), "ok": ml_own == ["Book/BRIEF_ML.md"]})
        shared = check(sp, "Book", [sp / "Book/BRIEF_SHARED_NOID.md"])["targets"]["Book/BRIEF_SHARED_NOID.md"]
        ids = sorted(x["execution_id"] for x in shared["pinned_by"])
        results.append({"vector": "every reader of one shared brief is named, not just the first",
                        "want": "['n1_a1#e1', 'n2_a1#e1']", "got": str(ids), "ok": ids == ["n1_a1#e1", "n2_a1#e1"]})
        with (b / "receipts" / "r_attempt_receipts.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"execution_id": "x_a1#e2", "outcome": "COMPLETED"}) + "\n")
            fh.write(json.dumps({"execution_id": "n1_a1#e1", "outcome": "FAILED_BY_RUNTIME_WATCHDOG"}) + "\n")
            fh.write(json.dumps({"execution_id": "n2_a1#e1", "outcome": "COMPLETED"}) + "\n")
        got = check(sp, "Book", [sp / "Book/pinned.jsonl"])["targets"]["Book/pinned.jsonl"]["verdict"]
        results.append({"vector": "the same pin after the execution lands", "want": "CLEAR", "got": got, "ok": got == "CLEAR"})
        after = check(sp, "Book", [sp / "Book/BRIEF_SHARED_NOID.md", sp / "Book/corpus.jsonl"])["targets"]
        for tgt in ("Book/BRIEF_SHARED_NOID.md", "Book/corpus.jsonl"):
            got = after[tgt]["verdict"]
            results.append({"vector": "own-brief pin released when both readers land: %s" % tgt, "want": "CLEAR",
                            "got": got, "ok": got == "CLEAR"})
    failed = [r for r in results if not r["ok"]]
    print(json.dumps({"selftest": "m8_inflight_pin_guard", "vectors": len(results), "failed": failed,
                      "verdict": "GREEN" if not failed else "RED"}, indent=1))
    return 0 if not failed else 1


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--book")
    ap.add_argument("--target", action="append", default=[])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.book or not a.target:
        print("usage: --book <Book> --target <path> [...] | --selftest", file=sys.stderr)
        return 2
    out = check(SP, a.book, a.target)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if out["verdict"] == "CLEAR" else 1


if __name__ == "__main__":
    raise SystemExit(main())
