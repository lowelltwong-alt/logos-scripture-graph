#!/usr/bin/env python3
"""OW-10: a repair is CURED only when verification results are bound to the EXACT resulting artifact, and a
distinct checker has reviewed it. A self-reported "passed" is not sufficient and this tool refuses it.

THE FAILURE THIS EXISTS TO STOP. This campaign has twice accepted a cure on the author's word. The Lamentations
stage-1 audit found "a test reported as run and passed that the record does not show ... the digits happen to be
right because they were copied from verified sources, not because the claimed test was run", and Jeremiah shipped a
cure round that installed pairing defects while labelling the items cured. In both cases the prose said PASSED. The
gap was never in the wording; it was that nothing tied the claimed test to the bytes that actually shipped.

THE BINDING RULE. A verification run proves something about the artifact it READ. If the artifact changed after the
run - another cure landed, a later apply rewrote the file - the old result proves nothing about what shipped. So
every verification entry must carry `artifact_sha256_at_run`, and at least one must equal BOTH the artifact's
claimed digest AND the digest the artifact has on disk right now. Three digests must agree: what was verified, what
was claimed, what is there.

WHAT IS NOT ACCEPTED, ever:
  - a verification entry with no machine result (no exit status, no output artifact with a digest);
  - a verification whose `artifact_sha256_at_run` does not match the shipped artifact;
  - a distinct-checker entry naming the cure author's own attempt, or its own execution;
  - the strings "passed", "cured", "verified" standing alone in place of any of the above.

This tool does not replace the distinct-checker review required by the standing second-generation-sweep rule. It
asserts that the review HAPPENED and was done by someone else, and it adds the artifact binding that review alone
never provided.

Usage:
  _cure_verification.py --claims <path.jsonl> [--root <dir>]   verify every cure claim; exit 1 on any refusal
  _cure_verification.py --selftest                             run the built-in vectors
"""
import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

HEX64 = re.compile(r"[0-9a-f]{64}")   # S1-19(d)
BARE_WORDS = {"passed", "pass", "cured", "verified", "ok", "green", "done", "fixed", "confirmed"}


def sha_file(p):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except Exception:
        return None


def check_claim(c, root):
    """Returns (verdict, [reasons]). ACCEPTED only when every binding holds."""
    reasons = []
    cid = c.get("cure_id") or "(unnamed cure)"
    if not (c.get("author_attempt_id") or c.get("author_execution_id")):
        # S1-19(a): with no author named, the distinct-checker test below has nothing to compare and would pass vacuously
        reasons.append("%s: names no author_attempt_id or author_execution_id, so the checker cannot be shown distinct" % cid)
    for label_, value_ in (("artifact_sha256", c.get("artifact_sha256")),
                           ("distinct_checker.artifact_sha256_at_review", (c.get("distinct_checker") or {}).get("artifact_sha256_at_review")
                            if isinstance(c.get("distinct_checker"), dict) else None)):
        if value_ is not None and not HEX64.fullmatch(str(value_)):
            reasons.append("%s: %s %r is not a 64-hex digest (S1-19(d))" % (cid, label_, str(value_)[:20]))

    art = c.get("artifact_path")
    if not art:
        return "REFUSED", ["%s: no artifact_path; a cure that names no resulting artifact cannot be bound to one"
                           % cid]
    live = sha_file(Path(root) / art)
    if live is None:
        return "REFUSED", ["%s: artifact %s does not exist or cannot be read" % (cid, art)]

    # R6 (ezek_controlling_rulings_a1#e2): a cure on a BRIEF-CLASS artifact - a document agents read as instructions or
    # facts (.md) - must record the sweep it ran for OTHER statements about the corrected object. A correction that does
    # not sweep its own siblings leaves a contradiction behind (the 2026-09-10 TOOLKIT.md flagged-regions line was one).
    if str(art).lower().endswith(".md"):
        ss = c.get("sibling_sweep")
        if not isinstance(ss, dict) or not ss.get("key_phrases") or not isinstance(ss.get("statements_reviewed"), int):
            reasons.append("%s: brief-class artifact without a sibling-sweep record (key_phrases swept and "
                           "statements_reviewed); a correction must sweep its own sibling statements" % cid)

    claimed = c.get("artifact_sha256")
    if not claimed:
        reasons.append("%s: no artifact_sha256; the claim does not pin the bytes it says it cured" % cid)
    elif claimed != live:
        reasons.append("%s: artifact_sha256 %s does not match the file on disk %s; the artifact changed after the "
                       "claim was written, so the claim describes bytes that did not ship"
                       % (cid, claimed[:16], live[:16]))

    # ---- verification bound to the exact artifact ----
    ver = c.get("verification") or []
    if not ver:
        reasons.append("%s: no verification entries. A self-reported outcome is not verification." % cid)
    bound = []
    for i, v in enumerate(ver):
        tag = "%s: verification[%d]" % (cid, i)
        if isinstance(v, str):
            reasons.append("%s is a bare string%s; a verification entry must name the tool it ran, the artifact "
                           "digest it ran against, and a machine result"
                           % (tag, " (%r)" % v if v.strip().lower() in BARE_WORDS else ""))
            continue
        at_run = v.get("artifact_sha256_at_run")
        osha = v.get("output_sha256")
        osha_ok = isinstance(osha, str) and HEX64.fullmatch(osha) is not None
        for label_, value_ in (("output_sha256", osha), ("artifact_sha256_at_run", v.get("artifact_sha256_at_run"))):
            if value_ is not None and not HEX64.fullmatch(str(value_)):
                reasons.append("%s %s %r is not a 64-hex digest (S1-19(d))" % (tag, label_, str(value_)[:20]))
        has_machine_result = (v.get("exit") is not None) or osha_ok or bool(v.get("counts"))
        if not v.get("tool"):
            reasons.append("%s names no tool" % tag)
        if not has_machine_result:
            reasons.append("%s carries no machine result (exit status, output digest, or counts); a prose verdict "
                           "is the thing this gate exists to reject" % tag)
        if not at_run:
            reasons.append("%s does not record artifact_sha256_at_run, so nothing ties it to any particular bytes"
                           % tag)
        elif at_run != live:
            reasons.append("%s ran against %s but the artifact on disk is %s; this result proves nothing about "
                           "what shipped" % (tag, at_run[:16], live[:16]))
        elif has_machine_result and v.get("tool"):
            bound.append(v)
    if ver and not bound:
        reasons.append("%s: no verification result is bound to the shipped artifact" % cid)

    # ---- distinct-checker review ----
    dc = c.get("distinct_checker")
    author = c.get("author_attempt_id") or c.get("author_execution_id")
    if not dc:
        reasons.append("%s: no distinct_checker; the standing rule requires a checker distinct from the repair "
                       "author and this claim names none" % cid)
    elif isinstance(dc, str):
        reasons.append("%s: distinct_checker is a bare string; it must name the checking attempt and its verdict"
                       % cid)
    else:
        ch_a = dc.get("attempt_id")
        ch_x = dc.get("execution_id")
        if not ch_a and not ch_x:
            reasons.append("%s: distinct_checker names no attempt or execution" % cid)
        # The review must be bound to the shipped bytes for the SAME reason the verification is. A checker that
        # reviewed an earlier draft proves something about that draft. This gate shipped without the binding on
        # the checker side and its author's own first live claim was exactly the failing case: the artifacts were
        # edited AFTER the distinct checker ran, on findings the checker itself had raised.
        rev = dc.get("artifact_sha256_at_review")
        if not rev:
            reasons.append("%s: distinct_checker records no artifact_sha256_at_review, so nothing ties the "
                           "review to any particular bytes" % cid)
        elif rev != live:
            reasons.append("%s: distinct_checker reviewed %s but the artifact on disk is %s; that review "
                           "describes bytes that did not ship" % (cid, rev[:16], live[:16]))
        if author and ch_a and ch_a == author:
            reasons.append("%s: distinct_checker names the repair author's own attempt (%s); an author confirming "
                           "their own cure is the self-report this gate rejects" % (cid, ch_a))
        if author and ch_x and ch_x.split("#")[0] == str(author).split("#")[0]:
            reasons.append("%s: distinct_checker execution %s belongs to the repair author's own job" % (cid, ch_x))
        if not dc.get("verdict"):
            reasons.append("%s: distinct_checker records no verdict" % cid)
        if not dc.get("evidence_path"):
            reasons.append("%s: distinct_checker names no evidence path" % cid)

    return ("ACCEPTED" if not reasons else "REFUSED"), reasons


SUPERSESSION_KEYS = ("supersedes_cure_id", "recorded", "ordered_by", "why", "old_artifact_sha256")
# T3-01 (ezek_controlling_rulings_a1#e3): ordered_by names the ordering EXECUTION and the RULING that ordered the retirement
# S1-19(c): the ordering id is bounded against a hyphen too ('test-adversarial#e1' once matched as 'adversarial#e1')
ORDERED_BY = re.compile(r"(?<![\w-])(?P<xid>[a-z0-9_]+#e\d+)(?![\w-]).*?\bruling\s+(?P<rid>[A-Za-z0-9][A-Za-z0-9-]*)")
SUPERSEDING_VERBS = {"adopt", "amend", "close"}


RULING_TEXT = {}   # S1-19(e): (execution_id, ruling_id) -> the ruling's full text


def load_rulings(paths):
    """{execution_id: {ruling_id: verb}} from controlling-rulings files, for the optional --rulings cross-check."""
    out = {}
    for p in paths or []:
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        out.setdefault(d.get("execution_id"), {}).update({r.get("id"): r.get("ruling") for r in d.get("rulings", [])})
        RULING_TEXT.update({(d.get("execution_id"), r.get("id")): json.dumps(r, ensure_ascii=False) for r in d.get("rulings", [])})
    return out


def classify_supersession(x):
    """S1-19(e), V3-W (#e4): which forward-rule form a supersession record takes. 'ruling_names_retired_cure' when the ordering
    ruling's text (from --rulings) names the retired cure id; 'r5_with_trigger' when it cites R5 and its why names an install
    receipt or a digest change; otherwise 'unclassified'. A classification only, never a refusal."""
    m = ORDERED_BY.search(str(x.get("ordered_by", "")))
    target = str(x.get("supersedes_cure_id", ""))
    if m and re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(target), RULING_TEXT.get((m.group("xid"), m.group("rid")), "")):
        return "ruling_names_retired_cure"
    if m and m.group("rid") == "R5" and re.search(r"receipt|->|\u2192", str(x.get("why", ""))):
        return "r5_with_trigger"
    return "unclassified"


def run(claims_path, root, rulings=None):
    """Claims files are append-only. R5 (ezek_controlling_rulings_a1#e2): a claim that no longer binds is never edited;
    a later line {"record_type": "supersession", "supersedes_cure_id", "recorded", "ordered_by", "why",
    "old_artifact_sha256"} retires it, and the claim reads SUPERSEDED, not REFUSED.

    T3-01 (ezek_controlling_rulings_a1#e3): a supersession record is honoured only when it is TRUE to the file, not merely
    well-formed. Its old_artifact_sha256 must equal the artifact_sha256 of the claim it retires, cross-checked against the
    claims in the same file, and its ordered_by must name '<attempt_id>#e<N> ... ruling <id>'. With rulings files given
    (--rulings), the named execution must exist and must have ruled that id adopt, amend or close. A record failing any
    check is REFUSED and retires nothing: the claim it named keeps its own verdict."""
    lines = [json.loads(l) for l in Path(claims_path).read_text(encoding="utf-8").splitlines() if l.strip()]
    claims = [x for x in lines if x.get("record_type") != "supersession"]
    claim_digest = {c.get("cure_id"): c.get("artifact_sha256") for c in claims}
    counts = {}
    for c in claims:
        counts[c.get("cure_id")] = counts.get(c.get("cure_id"), 0) + 1
    dup = {k for k, n in counts.items() if n > 1}   # S1-19(b): one cure id, one claim line
    known = load_rulings(rulings) if rulings else None
    supers, out, refused, superseded = {}, [], 0, 0
    classes = []
    for x in lines:
        if x.get("record_type") != "supersession":
            continue
        target = x.get("supersedes_cure_id")
        missing = [k for k in SUPERSESSION_KEYS if not x.get(k)]
        why = ["supersession record lacks %s" % ", ".join(missing)] if missing else []
        if not missing:
            if target not in claim_digest:
                why.append("the record retires %s, which is no claim in this file" % target)
            elif x["old_artifact_sha256"] != claim_digest[target]:
                why.append("old_artifact_sha256 %s is not the artifact_sha256 %s of the claim it retires"
                           % (str(x["old_artifact_sha256"])[:16], str(claim_digest[target])[:16]))
            m = ORDERED_BY.search(str(x["ordered_by"]))
            if not m:
                why.append("ordered_by %r names no '<attempt_id>#e<N> ... ruling <id>'" % x["ordered_by"])
            elif known is not None:
                verb = known.get(m.group("xid"), {}).get(m.group("rid"))
                if verb not in SUPERSEDING_VERBS:
                    why.append("the rulings given do not show %s ruling %s as adopt, amend or close (found %r)"
                               % (m.group("xid"), m.group("rid"), verb))
            if not HEX64.fullmatch(str(x["old_artifact_sha256"])):
                why.append("old_artifact_sha256 %r is not a 64-hex digest (S1-19(d))" % str(x["old_artifact_sha256"])[:20])
            if target in dup:
                why.append("the record retires %s, which appears on more than one claim line (S1-19(b))" % target)
        classes.append({"supersedes_cure_id": target, "ordered_by": x.get("ordered_by"), "ordered_by_class": classify_supersession(x)})
        if why:
            refused += 1
            out.append({"cure_id": target, "record": "supersession", "verdict": "REFUSED", "reasons": why})
        else:
            supers[target] = x
    for c in claims:
        if c.get("cure_id") in dup:
            refused += 1
            out.append({"cure_id": c.get("cure_id"), "verdict": "REFUSED",
                        "reasons": ["%s appears on more than one claim line; a retired claim is superseded, never repeated "
                                    "(S1-19(b))" % c.get("cure_id")]})
            continue
        if c.get("cure_id") in supers:
            superseded += 1
            out.append({"cure_id": c.get("cure_id"), "verdict": "SUPERSEDED", "reasons": [],
                        "superseded_by": supers[c["cure_id"]].get("successor"), "why": supers[c["cure_id"]]["why"]})
            continue
        verdict, reasons = check_claim(c, root)
        refused += verdict == "REFUSED"
        out.append({"cure_id": c.get("cure_id"), "verdict": verdict, "reasons": reasons})
    return {"claims": len(claims), "accepted": sum(1 for o in out if o["verdict"] == "ACCEPTED"),
            "refused": refused, "superseded": superseded, "supersession_records": len(supers),
            "results": out, "supersession_classes": classes, "rulings_checked": known is not None,
            "verdict": "GREEN" if not refused else "RED"}


def selftest():
    tmp = Path(tempfile.mkdtemp())
    art = tmp / "rows_v1.jsonl"
    art.write_text('{"row":1}\n', encoding="utf-8")
    d = sha_file(art)
    good = {"cure_id": "C1", "author_attempt_id": "ezek_micro_m01_a1", "artifact_path": "rows_v1.jsonl",
            "artifact_sha256": d,
            "verification": [{"tool": "_wave_repair_sweep.py", "artifact_sha256_at_run": d, "exit": 0,
                              "output_sha256": "a" * 64}],
            "distinct_checker": {"attempt_id": "ezek_sweep_s01_a1", "verdict": "confirmed",
                                 "evidence_path": "sweep_s01.json", "artifact_sha256_at_review": d}}
    vectors = [
        ("bound result + distinct checker", good, "ACCEPTED"),
        ("self-reported pass only", dict(good, verification=["passed"]), "REFUSED"),
        ("no verification at all", dict(good, verification=[]), "REFUSED"),
        ("verified stale bytes", dict(good, verification=[dict(good["verification"][0],
                                                               artifact_sha256_at_run="0" * 64)]), "REFUSED"),
        ("prose verdict, no machine result", dict(good, verification=[{"tool": "eyeball",
                                                                       "artifact_sha256_at_run": d}]), "REFUSED"),
        ("author checked their own cure", dict(good, distinct_checker={"attempt_id": "ezek_micro_m01_a1",
                                                                       "verdict": "cured",
                                                                       "evidence_path": "x.json"}), "REFUSED"),
        ("no distinct checker", {k: v for k, v in good.items() if k != "distinct_checker"}, "REFUSED"),
        ("checker reviewed STALE bytes", dict(good, distinct_checker=dict(
            good["distinct_checker"], artifact_sha256_at_review="2" * 64)), "REFUSED"),
        ("checker review not bound to any bytes", dict(good, distinct_checker={
            k: v for k, v in good["distinct_checker"].items() if k != "artifact_sha256_at_review"}), "REFUSED"),
        ("artifact digest does not match disk", dict(good, artifact_sha256="1" * 64), "REFUSED"),
        ("S1-19(a) a claim naming no author", {k: v for k, v in good.items() if k != "author_attempt_id"}, "REFUSED"),
        ("S1-19(d) an output digest that is not a digest",
         dict(good, verification=[{"tool": "t.py", "artifact_sha256_at_run": d, "output_sha256": "not-a-digest"}]), "REFUSED"),
        ("S1-19(d) an artifact digest that is not a digest", dict(good, artifact_sha256="not-a-digest"), "REFUSED"),
    ]
    # R6 vectors: a brief-class (.md) artifact needs a sibling-sweep record
    md = tmp / "TOOLKIT.md"
    md.write_text("brief\n", encoding="utf-8")
    dm = sha_file(md)
    good_md = dict(good, artifact_path="TOOLKIT.md", artifact_sha256=dm,
                   verification=[dict(good["verification"][0], artifact_sha256_at_run=dm)],
                   distinct_checker=dict(good["distinct_checker"], artifact_sha256_at_review=dm))
    vectors += [
        ("R6 brief-class artifact without a sibling sweep", good_md, "REFUSED"),
        ("R6 brief-class artifact with a sibling sweep",
         dict(good_md, sibling_sweep={"key_phrases": ["K/Q cluster", "measurements"], "statements_reviewed": 3}), "ACCEPTED"),
    ]
    results, failed = [], 0
    for name, claim, expect in vectors:
        got, reasons = check_claim(claim, tmp)
        ok = got == expect
        failed += not ok
        results.append({"vector": name, "expected": expect, "got": got, "ok": ok,
                        "first_reason": reasons[0] if reasons else None})
    # R5 and T3-01 vectors, file level. A stale claim is retired only by a supersession record that is true to the file;
    # a refused record retires nothing, so the stale claim then reads REFUSED on its own (refused count 2).
    stale = dict(good, cure_id="OLD", artifact_sha256="3" * 64)
    genuine = {"record_type": "supersession", "supersedes_cure_id": "OLD", "recorded": "2026-09-11",
               "ordered_by": "test_rulings_a1#e2 ruling R5", "why": "artifact changed", "successor": "OLD-v2",
               "old_artifact_sha256": "3" * 64}   # the shape of the real EZEK-P0-CURE-toolkit record
    rf = tmp / "rulings.json"
    rf.write_text(json.dumps({"execution_id": "test_rulings_a1#e2",
                              "rulings": [{"id": "R5", "ruling": "adopt"}, {"id": "R9", "ruling": "reject"}]}), encoding="utf-8")
    for name, extra, rulings, want in (
            ("R5 stale claim retired by a supersession record true to the file", genuine, None, ("SUPERSEDED", 0)),
            ("R5 malformed supersession record is refused",
             {"record_type": "supersession", "supersedes_cure_id": "OLD"}, None, ("REFUSED", 2)),
            ("T3-01 a record whose old digest is not the retired claim's is refused",
             dict(genuine, old_artifact_sha256="f" * 64, ordered_by="test-adversarial#e1 ruling X"), None, ("REFUSED", 2)),
            ("T3-01 a well-formed record whose ordered_by names no execution id is refused",
             dict(genuine, ordered_by="test-adversarial"), None, ("REFUSED", 2)),
            ("T3-01 a record retiring a cure id absent from the file is refused",
             dict(genuine, supersedes_cure_id="NOT-HERE"), None, ("REFUSED", 2)),
            ("S1-19(c) an ordering id joined by a hyphen is refused",
             dict(genuine, ordered_by="test-adversarial#e1 ruling R5"), None, ("REFUSED", 2)),
            ("S1-19(d) a supersession whose old digest is not a digest is refused",
             dict(genuine, old_artifact_sha256="3" * 63 + "z"), None, ("REFUSED", 2)),
            ("T3-01 --rulings confirms the ordering ruling", genuine, [rf], ("SUPERSEDED", 0)),
            ("T3-01 --rulings refuses a ruling that did not adopt, amend or close",
             dict(genuine, ordered_by="test_rulings_a1#e2 ruling R9"), [rf], ("REFUSED", 2))):
        cf = tmp / "claims_r5.jsonl"
        cf.write_text(json.dumps(stale) + "\n" + json.dumps(extra) + "\n", encoding="utf-8")
        rep = run(cf, tmp, rulings)
        old_verdicts = [o["verdict"] for o in rep["results"] if o["cure_id"] == "OLD"]
        ok = (want[0] in old_verdicts and rep["refused"] == want[1]
              and (want[0] == "SUPERSEDED" or "SUPERSEDED" not in old_verdicts))
        failed += not ok
        results.append({"vector": name, "expected": want, "got": (old_verdicts, rep["refused"]), "ok": ok})
    cf = tmp / "claims_dup.jsonl"
    cf.write_text(json.dumps(dict(good, cure_id="DUP", artifact_sha256="4" * 64)) + "\n" + json.dumps(dict(good, cure_id="DUP")) + "\n",
                  encoding="utf-8")
    rep = run(cf, tmp, None)
    dv = [o["verdict"] for o in rep["results"] if o["cure_id"] == "DUP"]
    ok = dv == ["REFUSED", "REFUSED"] and rep["refused"] == 2
    failed += not ok
    results.append({"vector": "S1-19(b) two claim lines with one cure id are both refused", "got": dv, "ok": ok})
    rf2 = tmp / "rulings_names.json"
    rf2.write_text(json.dumps({"execution_id": "test_rulings_a1#e3", "rulings": [{"id": "V9", "ruling": "adopt", "decision": "retire OLD"}]}),
                   encoding="utf-8")
    cf = tmp / "claims_cls.jsonl"
    for name, rec_, rulings_, want in (
            ("S1-19(e) a ruling that names the retired cure id", dict(genuine, ordered_by="test_rulings_a1#e3 ruling V9"), [rf2],
             "ruling_names_retired_cure"),
            ("S1-19(e) R5 with its install receipt named", dict(genuine, why="install receipt X.json replaced the file"), [rf],
             "r5_with_trigger"),
            ("S1-19(e) neither form is classified, never refused", dict(genuine, why="changed"), [rf], "unclassified")):
        cf.write_text(json.dumps(stale) + "\n" + json.dumps(rec_) + "\n", encoding="utf-8")
        rep = run(cf, tmp, rulings_)
        got = [c_["ordered_by_class"] for c_ in rep["supersession_classes"]]
        ok = got == [want] and rep["superseded"] == 1
        failed += not ok
        results.append({"vector": name, "expected": want, "got": got, "ok": ok})
    return {"vectors": len(results), "failed": failed, "results": results,
            "verdict": "GREEN" if not failed else "RED"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims")
    ap.add_argument("--root", default=".")
    ap.add_argument("--rulings", nargs="*", help="controlling-rulings files: cross-check each supersession record's ordering ruling")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--require-rulings", action="store_true", help="a gating run: refuse when no --rulings is given (S1-19)")
    a = ap.parse_args()
    if a.selftest:
        d = selftest()
        print(json.dumps(d, ensure_ascii=False, indent=1))
        return 1 if d["failed"] else 0
    if not a.claims:
        print(json.dumps({"status": "REFUSED", "why": "--claims or --selftest is required"}))
        return 1
    if a.require_rulings and not a.rulings:
        print(json.dumps({"status": "REFUSED", "why": "--require-rulings was given without --rulings"}))
        return 1
    d = run(a.claims, a.root, a.rulings)
    print(json.dumps(d, ensure_ascii=False, indent=1))
    return 1 if d["refused"] else 0


if __name__ == "__main__":
    sys.exit(main())
