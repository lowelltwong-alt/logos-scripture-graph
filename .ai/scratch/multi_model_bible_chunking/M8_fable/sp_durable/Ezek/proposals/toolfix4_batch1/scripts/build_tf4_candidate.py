"""Build the TOOLFIX-4 verifier candidate (ezek_controlling_rulings_a1#e8 ruling T6-01) from the INSTALLED verifier, pinned at a61ec7ff,
by count-checked replacements: exactly one occurrence each, or nothing is written. It writes the candidate beside this script as
_cure_verification.tf4.py, compiles it, and records every replacement (label, old, new) in replacements_tf4.json, so the stage
script can prove the diff is confined to the ruled regions. Nothing under SP is written.

Usage: build_tf4_candidate.py"""
import hashlib
import json
import py_compile
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SRC = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\_cure_verification.py")
SRC_SHA = "a61ec7ff85aee3782b1e23fb6b6338398be773769f4936d235a71cd7c11b6042"
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_cure_verification.tf4.py"

TF4_VECTORS = r'''def tf4_vectors(tmp):
    """TOOLFIX-4 (ezek_controlling_rulings_a1#e8 ruling T6-01): rule (7)'s counts shapes, E8-01, T6-A1 to T6-A10 as T6 ran them, and the
    GREEN controls. A claim vector may carry a fifth element: a reason substring the refusal must contain (a pinned reason class)."""
    tmp = Path(tmp)
    art = tmp / "rows_tf4.jsonl"
    art.write_text('{"row":4}\n', encoding="utf-8")
    d = sha_file(art)
    dc = {"attempt_id": "chk_a1", "verdict": "confirmed", "evidence_path": "e.json", "artifact_sha256_at_review": d}
    good = {"cure_id": "TF4", "author_attempt_id": "auth_a1", "artifact_path": art.name, "artifact_sha256": d,
            "verification": [{"tool": "t.py", "artifact_sha256_at_run": d, "exit": 0}], "distinct_checker": dc}

    def counts_only(c):
        return dict(good, verification=[{"tool": "t.py", "artifact_sha256_at_run": d, "counts": c}])

    no_mr = "counts carries no machine result: checks must be a positive integer and passed an integer (T6-01)"
    return [
        ("claim", "tf4_t6_a1_zero_counts_no_machine_result", counts_only({"checks": 0, "passed": 0, "failed": 0}), "REFUSED", no_mr),
        ("claim", "tf4_t6_a2_checks_zero_alone_no_machine_result", counts_only({"checks": 0}), "REFUSED", no_mr),
        ("claim", "tf4_t6_a3_failed_zero_alone_no_machine_result", counts_only({"failed": 0}), "REFUSED", no_mr),
        ("claim", "tf4_checks_without_passed_no_machine_result", counts_only({"checks": 5, "failed": 0}), "REFUSED", no_mr),
        ("claim", "tf4_passed_alone_no_machine_result", counts_only({"passed": 5}), "REFUSED", no_mr),
        ("claim", "tf4_e8_01_negative_counts_refused", counts_only({"checks": -1, "passed": -1, "failed": 0}), "REFUSED", "is negative (T6-01)"),
        ("claim", "tf4_bound_and_failed_reason_class_pinned", counts_only({"checks": 5, "passed": 3, "failed": 2}), "REFUSED", "passed 3 of 5 checks"),
        ("claim", "tf4_green_counts_11_11_0_no_exit", counts_only({"checks": 11, "passed": 11, "failed": 0}), "ACCEPTED"),
        ("claim", "tf4_green_exit0_counts_passed_null_binds_through_exit",
         dict(good, verification=[{"tool": "t.py", "artifact_sha256_at_run": d, "exit": 0, "counts": {"checks": 28, "passed": None, "failed": 0}}]),
         "ACCEPTED"),
        ("claim", "tf4_t6_a4_nbsp_author_refused", dict(good, author_attempt_id="\u00a0"), "REFUSED"),
        ("claim", "tf4_t6_a5_red_disclosed_false_refusal",
         dict(good, distinct_checker=dict(dc, verdict="fit_to_accept; the wall carvings show a red ochre pigment")), "REFUSED"),
        ("claim", "tf4_t6_a6_rejected_disclosed_false_refusal",
         dict(good, distinct_checker=dict(dc, verdict="fit_to_accept (no findings rejected as out of scope)")), "REFUSED"),
        ("claim", "tf4_t6_a7_blockers_disclosed_false_refusal",
         dict(good, distinct_checker=dict(dc, verdict="fit_to_accept; no blockers remain")), "REFUSED"),
        ("claim", "tf4_t6_a8_uppercase_artifact_digest_refused", dict(good, artifact_sha256=d.upper()), "REFUSED"),
        ("claim", "tf4_t6_a9_float_counts_refused", counts_only({"checks": 28.0, "passed": 28.0, "failed": 0.0}), "REFUSED"),
        ("claim", "tf4_t6_a10_exit_minus_one_refused", dict(good, verification=[{"tool": "t.py", "artifact_sha256_at_run": d, "exit": -1}]),
         "REFUSED"),
    ]


'''

REPL = [
    ("docstring: rule (7) and the T6-02 disclosure",
     "      unclassified - a classification only, never a refusal.\n\nThis tool does not replace",
     "      unclassified - a classification only, never a refusal.\n\n"
     "TOOLFIX-4 (ezek_controlling_rulings_a1#e8 ruling T6-01, on T6-01 and E8-01):\n"
     "  (7) a counts object carries a machine result only when checks is present as a positive integer and passed is present as an\n"
     "      integer; any other counts object (empty, all-zero, checks 0, checks or passed absent, failed 0 alone) carries none, and the\n"
     "      entry then binds only through an integer exit or a 64-hex output_sha256. A negative counts member is refused with its own\n"
     "      reason.\n"
     "  Disclosed (T6-02, ruled no change): REFUSE's red, reject* and blocker* forms can refuse a benign accepting verdict that uses\n"
     "  those words in another sense. Refusal is the safe direction; recorded verdicts are worded from ACCEPT with no REFUSE token, and\n"
     "  the selftest pins the refusals as *_disclosed_false_refusal vectors.\n\n"
     "This tool does not replace"),
    ("counts loop: negative refusal and rule (7)",
     '                for k in COUNT_KEYS:\n'
     '                    val = counts.get(k)\n'
     '                    if val is None:\n'
     '                        continue\n'
     '                    if is_int(val):\n'
     '                        cvals[k] = val\n'
     '                    else:\n'
     '                        reasons.append("%s counts.%s %r is neither an integer nor null (T5-01)" % (tag, k, val))\n'
     '        has_machine_result = exit_ok or bool(cvals) or osha_ok\n',
     '                for k in COUNT_KEYS:\n'
     '                    val = counts.get(k)\n'
     '                    if val is None:\n'
     '                        continue\n'
     '                    if not is_int(val):\n'
     '                        reasons.append("%s counts.%s %r is neither an integer nor null (T5-01)" % (tag, k, val))\n'
     '                    elif val < 0:\n'
     '                        reasons.append("%s counts.%s %d is negative (T6-01)" % (tag, k, val))   # E8-01\n'
     '                    else:\n'
     '                        cvals[k] = val\n'
     '        # T6-01 rule (7): counts are a machine result only with a positive integer checks and an integer passed\n'
     '        counts_mr = cvals.get("checks", 0) > 0 and "passed" in cvals\n'
     '        has_machine_result = exit_ok or counts_mr or osha_ok\n'),
    ("no-machine-result reason names the counts shape",
     '        if not has_machine_result:\n'
     '            reasons.append("%s carries no machine result (an integer exit status, integer counts, or an output digest); a "\n'
     '                           "prose verdict is the thing this gate exists to reject" % tag)\n',
     '        if not has_machine_result:\n'
     '            reasons.append("%s carries no machine result (an integer exit status, integer counts, or an output digest); a "\n'
     '                           "prose verdict is the thing this gate exists to reject%s"\n'
     '                           % (tag, "; counts carries no machine result: checks must be a positive integer and passed an integer "\n'
     '                                   "(T6-01)" if isinstance(counts, dict) and counts else ""))\n'),
    ("evaluate: a pinned reason class",
     '    if vec[0] == "claim":\n'
     '        got, reasons = mod.check_claim(vec[2], tmp)\n'
     '        return {"vector": vec[1], "expected": vec[3], "got": got, "ok": got == vec[3], "first_reason": reasons[0] if reasons else None}\n',
     '    if vec[0] == "claim":\n'
     '        got, reasons = mod.check_claim(vec[2], tmp)\n'
     '        want_reason = vec[4] if len(vec) > 4 else None   # TOOLFIX-4: a pinned reason class, not only the verdict\n'
     '        ok = got == vec[3] and (want_reason is None or any(want_reason in r for r in reasons))\n'
     '        return {"vector": vec[1], "expected": vec[3], "got": got, "ok": ok, "first_reason": reasons[0] if reasons else None,\n'
     '                **({"expected_reason": want_reason} if want_reason else {})}\n'),
    ("tf4 vectors",
     "def evaluate(mod, vec, tmp):\n",
     TF4_VECTORS + "def evaluate(mod, vec, tmp):\n"),
    ("selftest runs the tf4 vectors",
     '    for v in tf3_vectors(tf3_dir):\n'
     '        r = evaluate(this, v, tf3_dir)\n'
     '        failed += not r["ok"]\n'
     '        results.append(r)\n',
     '    for v in tf3_vectors(tf3_dir):\n'
     '        r = evaluate(this, v, tf3_dir)\n'
     '        failed += not r["ok"]\n'
     '        results.append(r)\n'
     '    # TOOLFIX-4 (ezek_controlling_rulings_a1#e8 ruling T6-01): rule (7), E8-01, T6-A1 to T6-A10 and the GREEN controls\n'
     '    tf4_dir = tmp / "tf4"\n'
     '    tf4_dir.mkdir()\n'
     '    for v in tf4_vectors(tf4_dir):\n'
     '        r = evaluate(this, v, tf4_dir)\n'
     '        failed += not r["ok"]\n'
     '        results.append(r)\n'),
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


if sha(SRC) != SRC_SHA:
    raise SystemExit("ABORT: the installed verifier is %s..., not a61ec7ff" % sha(SRC)[:16])
text = SRC.read_text(encoding="utf-8")
for label, old, new in REPL:
    n = text.count(old)
    if n != 1:
        raise SystemExit("ABORT: %s: expected exactly 1 occurrence, found %d; nothing written" % (label, n))
    text = text.replace(old, new)
tmp = OUT.with_name(OUT.name + ".tmp")
tmp.write_text(text, encoding="utf-8", newline="\n")
py_compile.compile(str(tmp), doraise=True)
tmp.replace(OUT)
(ROOT / "replacements_tf4.json").write_text(json.dumps([{"label": l, "old": o, "new": n} for l, o, n in REPL], ensure_ascii=False, indent=1),
                                            encoding="utf-8", newline="\n")
print(json.dumps({"candidate": str(OUT), "sha256": sha(OUT), "replacements": [r[0] for r in REPL]}, indent=1))
