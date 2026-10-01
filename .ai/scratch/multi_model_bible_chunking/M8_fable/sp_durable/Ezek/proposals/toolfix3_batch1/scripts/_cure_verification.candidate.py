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
  - a verification entry with no machine result (no integer exit status, no integer counts, no output digest);
  - a verification whose `artifact_sha256_at_run` does not match the shipped artifact;
  - a verification bound to the shipped bytes that FAILED (a non-zero exit, a non-zero failed count, passed short of
    checks, or a verdict beginning red, fail or refus);
  - a distinct-checker entry naming the cure author's own attempt or job, under any spelling of the id;
  - a distinct-checker verdict that is not an accepting verdict;
  - the strings "passed", "cured", "verified" standing alone in place of any of the above.

TOOLFIX-3 (ezek_controlling_rulings_a1#e6 ruling T5-VERIFIER, on T5-01, T5-02 and T5-03):
  (1) a machine result is an exit that is an int and not a bool, a counts object whose checks/passed/failed are ints where
      present (a null member is absent), or a 64-hex output_sha256; a non-int exit or a counts member that is neither an int
      nor null is refused with its own reason. An entry is BOUND only when it is a machine result, names a tool, ran against
      the live digest AND is passing; a bound-but-failing entry is refused and never counts toward bound.
  (2) the distinct_checker verdict, casefolded, must CONTAIN an accepting form (ACCEPT) and no refusing form (REFUSE).
  (3) ids compare after strip and casefold; an author field empty after strip is missing; the job stems of both author
      fields and of both checker fields may not intersect.
  (4) cure ids are stripped before the duplicate test and the retirement lookup; every '<execution>#e<N> ... ruling <id>'
      pair in ordered_by is read, the execution id standing at the start or after whitespace, ';', ',' or '('; under
      --rulings every pair must resolve to a superseding ruling: adopt, amend or close always, ratify or ratify_with_changes
      only when that ruling's decision or orders place the retired cure id within 200 characters of supersession,
      supersede or retire. The classification is ruling_orders_retirement, ruling_mentions_cure_id, r5_with_trigger or
      unclassified - a classification only, never a refusal.

This tool does not replace the distinct-checker review required by the standing second-generation-sweep rule. It
asserts that the review HAPPENED and was done by someone else, and it adds the artifact binding that review alone
never provided.

Usage:
  _cure_verification.py --claims <path.jsonl> [--root <dir>] [--rulings <files>...] [--require-rulings]
  _cure_verification.py --selftest                             run the built-in vectors
"""
import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

HEX64 = re.compile(r"[0-9a-f]{64}")   # S1-19(d)
BARE_WORDS = {"passed", "pass", "cured", "verified", "ok", "green", "done", "fixed", "confirmed"}
# T5-VERIFIER (2): the checker's verdict must contain an accepting form and no refusing form
ACCEPT = re.compile(r"\b(fit_to_accept|fit_with_changes|confirmed|accept(?:ed|able)?)\b")
REFUSE = re.compile(r"\b(not_fit|not fit|unfit|refut\w*|reject\w*|blocker\w*|red)\b")
FAILING_VERDICT_PREFIXES = ("red", "fail", "refus")   # T5-VERIFIER (1)
COUNT_KEYS = ("checks", "passed", "failed")


def sha_file(p):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except Exception:
        return None


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def norm_id(x):
    """T5-VERIFIER (3): an id compares after strip and casefold; a non-string or an empty-after-strip field is missing ("")."""
    return x.strip().casefold() if isinstance(x, str) else ""


def check_claim(c, root):
    """Returns (verdict, [reasons]). ACCEPTED only when every binding holds."""
    reasons = []
    cid = str(c.get("cure_id") or "").strip() or "(unnamed cure)"
    a_att, a_exe = norm_id(c.get("author_attempt_id")), norm_id(c.get("author_execution_id"))
    if not (a_att or a_exe):
        # S1-19(a): with no author named, the distinct-checker test below has nothing to compare and would pass vacuously.
        # T5-02: a field that is empty after strip names no author.
        reasons.append("%s: names no author_attempt_id or author_execution_id (a field empty after strip is missing), so the "
                       "checker cannot be shown distinct" % cid)
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
        if not isinstance(v, dict):
            reasons.append("%s is not an object" % tag)
            continue
        at_run = v.get("artifact_sha256_at_run")
        osha = v.get("output_sha256")
        osha_ok = isinstance(osha, str) and HEX64.fullmatch(osha) is not None
        for label_, value_ in (("output_sha256", osha), ("artifact_sha256_at_run", v.get("artifact_sha256_at_run"))):
            if value_ is not None and not HEX64.fullmatch(str(value_)):
                reasons.append("%s %s %r is not a 64-hex digest (S1-19(d))" % (tag, label_, str(value_)[:20]))
        # T5-VERIFIER (1): only an integer exit and integer counts are machine results
        ex = v.get("exit")
        exit_ok = is_int(ex)
        if ex is not None and not exit_ok:
            reasons.append("%s exit %r is not an integer; a word or a boolean is not an exit status (T5-01)" % (tag, ex))
        counts, cvals = v.get("counts"), {}
        if counts is not None:
            if not isinstance(counts, dict):
                reasons.append("%s counts is not an object (T5-01)" % tag)
            else:
                for k in COUNT_KEYS:
                    val = counts.get(k)
                    if val is None:
                        continue
                    if is_int(val):
                        cvals[k] = val
                    else:
                        reasons.append("%s counts.%s %r is neither an integer nor null (T5-01)" % (tag, k, val))
        has_machine_result = exit_ok or bool(cvals) or osha_ok
        if not v.get("tool"):
            reasons.append("%s names no tool" % tag)
        if not has_machine_result:
            reasons.append("%s carries no machine result (an integer exit status, integer counts, or an output digest); a "
                           "prose verdict is the thing this gate exists to reject" % tag)
        if not at_run:
            reasons.append("%s does not record artifact_sha256_at_run, so nothing ties it to any particular bytes"
                           % tag)
        elif at_run != live:
            reasons.append("%s ran against %s but the artifact on disk is %s; this result proves nothing about "
                           "what shipped" % (tag, at_run[:16], live[:16]))
        elif has_machine_result and v.get("tool"):
            failing = []
            if exit_ok and ex != 0:
                failing.append("exit %d" % ex)
            if "failed" in cvals and cvals["failed"] != 0:
                failing.append("failed %d" % cvals["failed"])
            if "passed" in cvals and "checks" in cvals and cvals["passed"] != cvals["checks"]:
                failing.append("passed %d of %d checks" % (cvals["passed"], cvals["checks"]))
            verdict_ = v.get("verdict")
            if verdict_ is not None and str(verdict_).strip().casefold().startswith(FAILING_VERDICT_PREFIXES):
                failing.append("verdict %r" % verdict_)
            if failing:
                reasons.append("%s is bound to the shipped bytes and FAILED (%s); a failing run cures nothing (T5-01)"
                               % (tag, "; ".join(failing)))
            else:
                bound.append(v)
    if ver and not bound:
        reasons.append("%s: no passing verification result is bound to the shipped artifact" % cid)

    # ---- distinct-checker review ----
    dc = c.get("distinct_checker")
    author = a_att or a_exe
    if not dc:
        reasons.append("%s: no distinct_checker; the standing rule requires a checker distinct from the repair "
                       "author and this claim names none" % cid)
    elif isinstance(dc, str):
        reasons.append("%s: distinct_checker is a bare string; it must name the checking attempt and its verdict"
                       % cid)
    elif not isinstance(dc, dict):
        reasons.append("%s: distinct_checker is not an object" % cid)
    else:
        ch_a, ch_x = norm_id(dc.get("attempt_id")), norm_id(dc.get("execution_id"))
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
        if author and ch_x and ch_x.split("#")[0] == author.split("#")[0]:
            reasons.append("%s: distinct_checker execution %s belongs to the repair author's own job" % (cid, ch_x))
        # T5-02: the job stems of BOTH author fields against the job stems of BOTH checker fields
        shared = sorted({f.split("#")[0] for f in (a_att, a_exe) if f} & {f.split("#")[0] for f in (ch_a, ch_x) if f})
        if shared:
            reasons.append("%s: the distinct_checker and the repair author share the job %s (ids compared after strip and "
                           "casefold, both fields on each side; T5-02)" % (cid, ", ".join(shared)))
        verdict = dc.get("verdict")
        if not verdict:
            reasons.append("%s: distinct_checker records no verdict" % cid)
        else:
            vt = str(verdict).casefold()
            acc, ref = ACCEPT.search(vt), REFUSE.search(vt)
            if not acc or ref:
                reasons.append("%s: distinct_checker verdict %r is not an accepting verdict: %s (T5-01)"
                               % (cid, verdict, ("it carries the refusing form %r" % ref.group(0)) if ref
                                  else "it carries no accepting form"))
        if not dc.get("evidence_path"):
            reasons.append("%s: distinct_checker names no evidence path" % cid)

    return ("ACCEPTED" if not reasons else "REFUSED"), reasons


SUPERSESSION_KEYS = ("supersedes_cure_id", "recorded", "ordered_by", "why", "old_artifact_sha256")
# T3-01 (ezek_controlling_rulings_a1#e3): ordered_by names the ordering EXECUTION and the RULING that ordered the retirement.
# T5-VERIFIER (4): the execution id stands at the start or after whitespace, ';', ',' or '(' (S1-19(c) refused a hyphen; '.' and
# '/' are refused too), and EVERY pair is read with finditer.
ORDERED_BY = re.compile(r"(?<![^\s;,(])(?P<xid>[a-z0-9_]+#e\d+)(?![\w-]).*?\bruling\s+(?P<rid>[A-Za-z0-9][A-Za-z0-9-]*)")
SUPERSEDING_VERBS = {"adopt", "amend", "close"}
RATIFYING_VERBS = {"ratify", "ratify_with_changes"}   # T5-VERIFIER (4): superseding only when the ruling orders the retirement
RETIRE_WORDS = re.compile(r"supersession|supersede|retire", re.I)
RETIRE_WINDOW = 200


RULING_TEXT = {}         # S1-19(e): (execution_id, ruling_id) -> the ruling's full text
RULING_ORDER_TEXT = {}   # T5-VERIFIER (4): (execution_id, ruling_id) -> its decision and orders text


def load_rulings(paths):
    """{execution_id: {ruling_id: verb}} from controlling-rulings files, for the optional --rulings cross-check."""
    out = {}
    for p in paths or []:
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        xid = d.get("execution_id")
        for r in d.get("rulings", []):
            out.setdefault(xid, {})[r.get("id")] = r.get("ruling")
            RULING_TEXT[(xid, r.get("id"))] = json.dumps(r, ensure_ascii=False)
            orders = r.get("orders") or []
            RULING_ORDER_TEXT[(xid, r.get("id"))] = "\n".join(
                [str(r.get("decision") or "")] + [str(o.get("order") if isinstance(o, dict) else o) for o in orders])
    return out


def id_pattern(target):
    return re.compile(r"(?<![\w-])%s(?![\w-])" % re.escape(target))


def pairs_of(x):
    return [(m.group("xid"), m.group("rid")) for m in ORDERED_BY.finditer(str(x.get("ordered_by", "")))]


def orders_retirement(xid, rid, target):
    """True when the ruling's decision or orders place the retired cure id within 200 characters of supersession, supersede
    or retire (T5-VERIFIER (4))."""
    if not target:
        return False
    text = RULING_ORDER_TEXT.get((xid, rid), "")
    ids = [m.span() for m in id_pattern(target).finditer(text)]
    words = [m.span() for m in RETIRE_WORDS.finditer(text)]
    return any(max(a0, b0) - min(a1, b1) <= RETIRE_WINDOW for a0, a1 in ids for b0, b1 in words)


def classify_supersession(x):
    """S1-19(e), V3-W (#e4), T5-VERIFIER (4): which forward-rule form a supersession record takes, over every ordering pair:
    'ruling_orders_retirement' when an ordering ruling's decision or orders place the retired id within 200 characters of
    supersession/supersede/retire; else 'ruling_mentions_cure_id' when an ordering ruling's text names the id anywhere; else
    'r5_with_trigger' when a pair cites R5 and the why names an install receipt or a digest change; otherwise 'unclassified'.
    A classification only, never a refusal."""
    target = str(x.get("supersedes_cure_id", "")).strip()
    pairs = pairs_of(x)
    if target and any(orders_retirement(xid, rid, target) for xid, rid in pairs):
        return "ruling_orders_retirement"
    if target and any(id_pattern(target).search(RULING_TEXT.get(p, "")) for p in pairs):
        return "ruling_mentions_cure_id"
    if any(rid == "R5" for _, rid in pairs) and re.search(r"receipt|->|→", str(x.get("why", ""))):
        return "r5_with_trigger"
    return "unclassified"


def run(claims_path, root, rulings=None):
    """Claims files are append-only. R5 (ezek_controlling_rulings_a1#e2): a claim that no longer binds is never edited;
    a later line {"record_type": "supersession", "supersedes_cure_id", "recorded", "ordered_by", "why",
    "old_artifact_sha256"} retires it, and the claim reads SUPERSEDED, not REFUSED.

    T3-01 (ezek_controlling_rulings_a1#e3): a supersession record is honoured only when it is TRUE to the file, not merely
    well-formed. Its old_artifact_sha256 must equal the artifact_sha256 of the claim it retires, cross-checked against the
    claims in the same file, and its ordered_by must name '<attempt_id>#e<N> ... ruling <id>'. With rulings files given
    (--rulings), EVERY named pair must resolve to a superseding ruling (T5-VERIFIER (4)). A record failing any check is
    REFUSED and retires nothing: the claim it named keeps its own verdict."""
    RULING_TEXT.clear()
    RULING_ORDER_TEXT.clear()
    lines = [json.loads(l) for l in Path(claims_path).read_text(encoding="utf-8").splitlines() if l.strip()]
    claims = [x for x in lines if x.get("record_type") != "supersession"]
    key = lambda v: str(v if v is not None else "").strip()   # noqa: E731  T5-VERIFIER (4): cure ids compare stripped
    claim_digest = {key(c.get("cure_id")): c.get("artifact_sha256") for c in claims}
    counts = {}
    for c in claims:
        counts[key(c.get("cure_id"))] = counts.get(key(c.get("cure_id")), 0) + 1
    dup = {k for k, n in counts.items() if n > 1}   # S1-19(b): one cure id, one claim line
    known = load_rulings(rulings) if rulings else None
    supers, out, refused, superseded = {}, [], 0, 0
    classes = []
    for x in lines:
        if x.get("record_type") != "supersession":
            continue
        target = key(x.get("supersedes_cure_id"))
        missing = [k for k in SUPERSESSION_KEYS if not x.get(k) or (k == "supersedes_cure_id" and not target)]
        why = ["supersession record lacks %s" % ", ".join(missing)] if missing else []
        if not missing:
            if target not in claim_digest:
                why.append("the record retires %s, which is no claim in this file" % target)
            elif x["old_artifact_sha256"] != claim_digest[target]:
                why.append("old_artifact_sha256 %s is not the artifact_sha256 %s of the claim it retires"
                           % (str(x["old_artifact_sha256"])[:16], str(claim_digest[target])[:16]))
            pairs = pairs_of(x)
            if not pairs:
                why.append("ordered_by %r names no '<attempt_id>#e<N> ... ruling <id>' with the id at the start or after "
                           "whitespace, ';', ',' or '('" % x["ordered_by"])
            elif known is not None:
                for xid, rid in pairs:
                    verb = known.get(xid, {}).get(rid)
                    if verb in SUPERSEDING_VERBS or (verb in RATIFYING_VERBS and orders_retirement(xid, rid, target)):
                        continue
                    if verb in RATIFYING_VERBS:
                        why.append("%s ruling %s is %s and its decision and orders do not order %s retired (the id within %d "
                                   "characters of supersession, supersede or retire)" % (xid, rid, verb, target, RETIRE_WINDOW))
                    else:
                        why.append("the rulings given do not show %s ruling %s as adopt, amend or close (found %r)"
                                   % (xid, rid, verb))
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
        cid = key(c.get("cure_id"))
        if cid in dup:
            refused += 1
            out.append({"cure_id": cid, "verdict": "REFUSED",
                        "reasons": ["%s appears on more than one claim line (ids compared stripped); a retired claim is "
                                    "superseded, never repeated (S1-19(b))" % cid]})
            continue
        if cid in supers:
            superseded += 1
            out.append({"cure_id": cid, "verdict": "SUPERSEDED", "reasons": [],
                        "superseded_by": supers[cid].get("successor"), "why": supers[cid]["why"]})
            continue
        verdict, reasons = check_claim(c, root)
        refused += verdict == "REFUSED"
        out.append({"cure_id": cid, "verdict": verdict, "reasons": reasons})
    return {"claims": len(claims), "accepted": sum(1 for o in out if o["verdict"] == "ACCEPTED"),
            "refused": refused, "superseded": superseded, "supersession_records": len(supers),
            "results": out, "supersession_classes": classes, "rulings_checked": known is not None,
            "verdict": "GREEN" if not refused else "RED"}


def tf3_vectors(tmp):
    """T5-VERIFIER (5): T5's evasions and edges, each with its expectation, the rule vectors pinning (1)-(4), and the GREEN
    controls. Returned as data, so a staging harness can evaluate the same vectors against another verifier module (the
    DISCRIMINATING column). A 'claim' vector is (kind, name, claim, expected verdict); a 'file' vector is
    (kind, name, lines, rulings files or None, {"target", "verdicts" of the target's claim lines, "refused", optional "class"})."""
    tmp = Path(tmp)
    art = tmp / "rows_tf3.jsonl"
    art.write_text('{"row":3}\n', encoding="utf-8")
    d = sha_file(art)
    v0 = {"tool": "t.py", "artifact_sha256_at_run": d, "exit": 0}
    dc = {"attempt_id": "chk_a1", "verdict": "confirmed", "evidence_path": "e.json", "artifact_sha256_at_review": d}
    good = {"cure_id": "TF3", "author_attempt_id": "auth_a1", "artifact_path": art.name, "artifact_sha256": d,
            "verification": [v0], "distinct_checker": dc}
    no_attempt = {k: v for k, v in good.items() if k != "author_attempt_id"}
    vec = [
        # T5's eight evasions (T5-01, T5-02, T5-03): each read ACCEPTED on the installed verifier
        ("claim", "s1_19a_whitespace_author", dict(good, author_attempt_id=" "), "REFUSED"),
        ("claim", "author_exec_only_checker_bare_attempt_same_job",
         dict(no_attempt, author_execution_id="auth_a1#e1", distinct_checker=dict(dc, attempt_id="auth_a1")), "REFUSED"),
        ("claim", "author_attempt_and_exec_differ_checker_is_exec_job",
         dict(good, author_attempt_id="a_a1", author_execution_id="b_a1#e1",
              distinct_checker={k: v for k, v in dict(dc, execution_id="b_a1#e2").items() if k != "attempt_id"}), "REFUSED"),
        ("claim", "case_variant_of_author_as_checker", dict(good, distinct_checker=dict(dc, attempt_id="AUTH_A1")), "REFUSED"),
        ("claim", "failing_run_exit_1_accepted", dict(good, verification=[dict(v0, exit=1, verdict="RED")]), "REFUSED"),
        ("claim", "exit_is_the_word_passed", dict(good, verification=[dict(v0, exit="passed")]), "REFUSED"),
        ("claim", "checker_verdict_not_fit", dict(good, distinct_checker=dict(dc, verdict="not_fit")), "REFUSED"),
        # rule vectors pinning each branch of (1)-(3)
        ("claim", "tf3_rule_exit_bool_true", dict(good, verification=[dict(v0, exit=True)]), "REFUSED"),
        ("claim", "tf3_rule_counts_failed_nonzero", dict(good, verification=[dict(v0, counts={"checks": 28, "passed": 27, "failed": 1})]), "REFUSED"),
        ("claim", "tf3_rule_counts_passed_short_of_checks", dict(good, verification=[dict(v0, counts={"checks": 28, "passed": 27})]), "REFUSED"),
        ("claim", "tf3_rule_counts_member_a_string", dict(good, verification=[dict(v0, counts={"checks": "28", "passed": 28, "failed": 0})]), "REFUSED"),
        ("claim", "tf3_rule_counts_only_no_exit_failing", dict(good, verification=[{"tool": "t.py", "artifact_sha256_at_run": d,
                                                                                     "counts": {"checks": 5, "passed": 4, "failed": 1}}]), "REFUSED"),
        ("claim", "tf3_rule_verdict_failed_prefix_with_exit_0", dict(good, verification=[dict(v0, verdict="FAILED 2 of 28")]), "REFUSED"),
        ("claim", "tf3_rule_one_passing_one_failing_entry", dict(good, verification=[v0, dict(v0, exit=2)]), "REFUSED"),
        ("claim", "tf3_rule_checker_verdict_no_accepting_form", dict(good, distinct_checker=dict(dc, verdict="looks good")), "REFUSED"),
        ("claim", "tf3_rule_checker_verdict_accepting_and_refusing", dict(good, distinct_checker=dict(dc, verdict="fit_to_accept; blocker open")), "REFUSED"),
        ("claim", "tf3_rule_checker_verdict_red_word", dict(good, distinct_checker=dict(dc, verdict="confirmed but RED at 41:20")), "REFUSED"),
        ("claim", "tf3_rule_both_author_fields_blank", dict(good, author_attempt_id="  ", author_execution_id=""), "REFUSED"),
        ("claim", "tf3_rule_checker_execution_padded_same_job", dict(good, distinct_checker=dict(dc, attempt_id="", execution_id=" Auth_a1#e3 ")), "REFUSED"),
        # GREEN controls
        ("claim", "tf3_green_exit0_counts_28_28_0", dict(good, verification=[dict(v0, counts={"checks": 28, "passed": 28, "failed": 0})]), "ACCEPTED"),
        ("claim", "tf3_green_counts_passed_null_exit0_t5_13_shape",
         dict(good, verification=[dict(v0, counts={"checks": 28, "passed": None, "failed": 0})]), "ACCEPTED"),
        ("claim", "tf3_green_verdict_toolkit_md_fit_to_accept",
         dict(good, distinct_checker=dict(dc, verdict="toolkit_md fit_to_accept (full-file review, ruling T1 item 1)")), "ACCEPTED"),
        ("claim", "tf3_green_verdict_fit_with_changes", dict(good, distinct_checker=dict(dc, verdict="fit_with_changes; artifact fit=true")), "ACCEPTED"),
        ("claim", "tf3_green_distinct_jobs_both_fields",
         dict(good, author_attempt_id="a_a1", author_execution_id="a_a1#e1", distinct_checker=dict(dc, attempt_id="b_a1", execution_id="b_a1#e1")),
         "ACCEPTED"),
        ("claim", "tf3_green_verdict_cured_word_is_not_red", dict(good, distinct_checker=dict(dc, verdict="fit_to_accept; D3=cured")), "ACCEPTED"),
    ]
    stale = dict(good, cure_id="OLD", artifact_sha256="3" * 64)
    rec = {"record_type": "supersession", "supersedes_cure_id": "OLD", "recorded": "2026-09-11", "ordered_by": "test_rulings_a1#e2 ruling R5",
           "why": "artifact changed", "successor": "OLD-v2", "old_artifact_sha256": "3" * 64}

    def rulings_file(name, xid, rulings):
        p = tmp / name
        p.write_text(json.dumps({"execution_id": xid, "rulings": rulings}), encoding="utf-8")
        return p

    rf2 = rulings_file("tf3_rulings_e2.json", "test_rulings_a1#e2", [{"id": "R5", "ruling": "adopt"}, {"id": "R9", "ruling": "reject"}])
    rf3 = rulings_file("tf3_rulings_e3.json", "test_rulings_a1#e3", [{"id": "V9", "ruling": "adopt", "decision": "retire OLD"}])
    rf4 = rulings_file("tf3_rulings_e4.json", "test_rulings_a1#e4", [
        {"id": "W1", "ruling": "ratify_with_changes", "decision": "the batch stands",
         "orders": [{"to": "orchestrator", "order": "append a supersession record for OLD"}]},
        {"id": "W2", "ruling": "ratify_with_changes", "decision": "OLD stays under review", "orders": []},
        {"id": "W3", "ruling": "ratify", "decision": "OLD is fine. " + "x" * 240 + " A later supersession is not ordered here."}])
    rf5 = rulings_file("tf3_rulings_e5.json", "test_rulings_a1#e5",
                       [{"id": "V8", "ruling": "adopt", "decision": "write the claim OLD-v2 once T9 reviews OLD's successor bytes"}])
    superseded = {"target": "OLD", "verdicts": ["SUPERSEDED"], "refused": 0}
    refused = {"target": "OLD", "verdicts": ["REFUSED"], "refused": 2}
    vec += [
        ("file", "s1_19b_dup_cure_id_trailing_space", [dict(good, cure_id="DUP ", artifact_sha256="4" * 64), dict(good, cure_id="DUP")], None,
         {"target": "DUP", "verdicts": ["REFUSED", "REFUSED"], "refused": 2}),
        ("file", "compound_ordered_by_second_bogus", [stale, dict(rec, ordered_by="test_rulings_a1#e2 ruling R5; bogus_a1#e9 ruling ZZ9")], [rf2], refused),
        ("file", "s1_19c_period_prefix", [stale, dict(rec, ordered_by=".test_rulings_a1#e2 ruling R5")], [rf2], refused),
        ("file", "s1_19c_slash_prefix", [stale, dict(rec, ordered_by="/test_rulings_a1#e2 ruling R5")], [rf2], refused),
        ("file", "e_names_only_as_successor_overbroad", [stale, dict(rec, ordered_by="test_rulings_a1#e5 ruling V8")], [rf5],
         dict(superseded, **{"class": "ruling_mentions_cure_id"})),
        ("file", "ratify_with_changes_verb_ordering_retirement", [stale, dict(rec, ordered_by="test_rulings_a1#e4 ruling W1")], [rf4],
         dict(superseded, **{"class": "ruling_orders_retirement"})),
        ("file", "ratify_with_changes_verb_mentioning_only", [stale, dict(rec, ordered_by="test_rulings_a1#e4 ruling W2")], [rf4], refused),
        ("file", "tf3_rule_ratify_retire_word_beyond_200_characters", [stale, dict(rec, ordered_by="test_rulings_a1#e4 ruling W3")], [rf4], refused),
        ("file", "tf3_rule_supersedes_id_trailing_space_retires", [stale, dict(rec, supersedes_cure_id="OLD ")], [rf2], superseded),
        ("file", "tf3_rule_ordered_by_after_paren_and_comma", [stale, dict(rec, ordered_by="(test_rulings_a1#e2 ruling R5), test_rulings_a1#e3 ruling V9")],
         [rf2, rf3], superseded),
        ("file", "tf3_green_two_pair_ordered_by_both_adopt", [stale, dict(rec, ordered_by="test_rulings_a1#e2 ruling R5; test_rulings_a1#e3 ruling V9")],
         [rf2, rf3], superseded),
    ]
    return vec


def evaluate(mod, vec, tmp):
    """Evaluate one tf3 vector with a verifier module's check_claim and run (this module, or another for discrimination)."""
    tmp = Path(tmp)
    if vec[0] == "claim":
        got, reasons = mod.check_claim(vec[2], tmp)
        return {"vector": vec[1], "expected": vec[3], "got": got, "ok": got == vec[3], "first_reason": reasons[0] if reasons else None}
    _, name, lines, rulings, want = vec
    cf = tmp / ("claims_%s.jsonl" % re.sub(r"\W", "_", name))
    cf.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
    rep = mod.run(cf, tmp, rulings)
    verdicts = [o["verdict"] for o in rep["results"] if str(o["cure_id"]).strip() == want["target"] and o.get("record") != "supersession"]
    classes = [c_.get("ordered_by_class") for c_ in rep.get("supersession_classes", [])]
    ok = verdicts == want["verdicts"] and rep["refused"] == want["refused"] and ("class" not in want or classes == [want["class"]])
    return {"vector": name, "expected": want, "got": {"verdicts": verdicts, "refused": rep["refused"], "classes": classes}, "ok": ok}


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
    # T5-VERIFIER (4) renamed the first class: a ruling whose decision retires the id is 'ruling_orders_retirement'
    for name, rec_, rulings_, want in (
            ("S1-19(e) a ruling that names the retired cure id", dict(genuine, ordered_by="test_rulings_a1#e3 ruling V9"), [rf2],
             "ruling_orders_retirement"),
            ("S1-19(e) R5 with its install receipt named", dict(genuine, why="install receipt X.json replaced the file"), [rf],
             "r5_with_trigger"),
            ("S1-19(e) neither form is classified, never refused", dict(genuine, why="changed"), [rf], "unclassified")):
        cf.write_text(json.dumps(stale) + "\n" + json.dumps(rec_) + "\n", encoding="utf-8")
        rep = run(cf, tmp, rulings_)
        got = [c_["ordered_by_class"] for c_ in rep["supersession_classes"]]
        ok = got == [want] and rep["superseded"] == 1
        failed += not ok
        results.append({"vector": name, "expected": want, "got": got, "ok": ok})
    # TOOLFIX-3 (T5-VERIFIER (5)): T5's vectors, the rule vectors and the GREEN controls
    this = SimpleNamespace(check_claim=check_claim, run=run)
    tf3_dir = tmp / "tf3"
    tf3_dir.mkdir()
    for v in tf3_vectors(tf3_dir):
        r = evaluate(this, v, tf3_dir)
        failed += not r["ok"]
        results.append(r)
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
