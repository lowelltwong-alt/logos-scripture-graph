#!/usr/bin/env python3
"""Re-point Ezekiel's derived-record generators at rows_v10_final.jsonl and regenerate (v10 hold round, OW-30).

WHY. Fable's one authorized ruling (fable_end_review/atlas_hold_ruling.v1.json) released six item-22 holds, dropped the
high-graded M8-Ezek-082 from the feed and kept M8-Ezek-113 held, which rows_v10_final now records in the corpus. Its
standing precedent says the feed follows the corpus: a row is in the feed only if graded low or medium_low, and it is
held exactly when its corpus row is held. The generator and checker decided both from the second reading's
STOP/GRADE_QUESTION items; they now decide them from the corpus. The judged score keeps the second reading's own act,
because its rule text names that act, and the judged dimension never reaches the feed.

HOW (the v9 repoint pattern). Every input and every current output is pinned by digest, and the pin guard must be CLEAR.
Each edited tool is saved as <name>.pre_<sha12> and edited by exact strings, each occurring exactly once. Outputs
regenerated in place are first copied to .pre_<sha12>; the two write-new sidecar outputs are renamed to .pre_<sha12> so
their generator can write them fresh. Then: gen_atlas_rows, --check, check_atlas_rows, --selftest, gen_sidecars,
--check, and the expected-shape asserts (101 feed rows, held exactly M8-Ezek-113, M8-Ezek-082 absent). Any failure
restores every file from the saved bytes. The report lists which atlas and sidecar rows changed, and in which fields.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parents[2]
SP, D = EZ.parent, EZ / "deliverables"
V10, V10_PIN = EZ / "rows_v10_final.jsonl", "106f355324fb867055e4f1ec25cc30ced8607b69a7ce0489b9d953e30e18608b"
V9_PIN = "a80b6e6712aa43bf3d8652255b4655a934af08a9cd3e036f9b320a37bbd1098c"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
env = dict(os.environ, PYTHONUTF8="1")

CHECK_HELD_OLD = '''    held_ids = {r["decision_id"] for r in shipped if r["decision_id"] in stop | gq}
    want = {r["span"] for r in shipped if str(r.get("confidence")) in ("low", "medium_low")} | \\
           {r["span"] for r in shipped if r["decision_id"] in held_ids}
'''
CHECK_HELD_NEW = '''    # AMENDED 2026-09-23 (v10 hold round, OW-30): a row is held exactly when its corpus row is held, and the selection
    # is low/medium_low only. The second reading's STOP/GRADE_QUESTION items no longer decide either; Fable's ruling
    # resolved each of them against the corpus (Ezek/fable_end_review/atlas_hold_ruling.v1.json).
    held_ids = {r["decision_id"] for r in shipped if r.get("candidate_hold_state") is not None}
    want = {r["span"] for r in shipped if str(r.get("confidence")) in ("low", "medium_low")}
    res["second_reading_items_no_longer_decide"] = {"ok": None, "detail":
        "DISCLOSED, not a failure: the second reading refused or grade-questioned %d rows; the corpus holds %d"
        % (len({r["decision_id"] for r in shipped if r["decision_id"] in stop | gq}), len(held_ids))}
'''
CHECK_MIRROR_OLD = '''          % (len(held_spans), len(held_marked), len(deferred), sorted(held_marked ^ held_spans)[:3]))
'''
CHECK_MIRROR_NEW = '''          % (len(held_spans), len(held_marked), len(deferred), sorted(held_marked ^ held_spans)[:3]))

    def unmirrored(r):
        c = by_span.get(r["span"])
        return c is None or (r.get("chunk_review_status"), r.get("candidate_hold_state"),
                             r.get("review_packet_final_state")) != (
            c.get("review_status"), c.get("candidate_hold_state"),
            "accepted_candidate" if c.get("candidate_hold_state") is None else "held_lower_confidence")
    off_corpus = [r["span"] for r in feed_rows if unmirrored(r)]
    check("feed_mirrors_the_corpus_hold", not off_corpus,
          "rows whose review status, hold state or packet state differ from the corpus row: %d %s"
          % (len(off_corpus), off_corpus[:3]))
'''
TAMPER_OLD = '''def tamper_drop(rows):
'''
TAMPER_NEW = '''def tamper_packet_state(rows):
    r = next((x for x in rows if x.get("candidate_hold_state")), rows[0])
    r["review_packet_final_state"] = ("accepted_candidate" if r["review_packet_final_state"] == "held_lower_confidence"
                                      else "held_lower_confidence")
    return rows


def tamper_drop(rows):
'''
GENS = {
    D / "gen_atlas_rows.py": ("9e91588fbd740a2ec3703d84b020905334195de1b987c14246196ff0270b19e6", [
        ('ROWS = EZ / "rows_v9_final.jsonl"  # v9 fix round 2026-09-23; was repair/rows_v7_cwo24.jsonl (the preimage)',
         'ROWS = EZ / "rows_v10_final.jsonl"  # v10 hold round 2026-09-23 (OW-30); was rows_v9_final.jsonl (a80b6e67),\n'
         '# and before that repair/rows_v7_cwo24.jsonl (the preimage)'),
        ('        if str(r.get("confidence")) not in SELECT and rid not in stop and rid not in gq:\n',
         '        if str(r.get("confidence")) not in SELECT:  # OW-30: low/medium_low only (was: OR referred)\n'),
        ('        held = rid in stop or rid in gq\n',
         '        held = r.get("candidate_hold_state") is not None  # OW-30: held exactly when the corpus row is held\n'
         '        referred = rid in stop or rid in gq  # the second reading\'s own act; it feeds the judged score only\n'),
        ('(2 if feat["zone"] else 0) + (2 if held else 0)', '(2 if feat["zone"] else 0) + (2 if referred else 0)'),
        ('(confidence low or medium_low, OR referred by the second "\n          "reading at any grade)"',
         '(confidence low or medium_low; held exactly "\n          "when the corpus row is held, OW-30)"'),
        ('medium_low + 1 refused-at-high = 102.\n',
         'medium_low + 1 refused-at-high = 102.\n'
         'AMENDED 2026-09-23 (v10 hold round, OW-30): the widened rule above is retired. Fable\'s one authorized ruling\n'
         '(Ezek/fable_end_review/atlas_hold_ruling.v1.json) resolved every referred row against the corpus: six holds\n'
         'released, the refused-at-high row dropped from the feed, one row kept held in the corpus (rows_v10_final). The\n'
         'selection is now low/medium_low only, and a row is held exactly when its corpus row is held: 11 + 90 = 101.\n'
         'The judged score still counts the second reading\'s refusal or grade question, as its rule text says.\n')]),
    D / "check_atlas_rows.py": ("069f0e6a026228f287f6fded84446634eba085c47395174573d61bcb4c54b5ea", [
        ('ROWS_IN = EZ / "rows_v9_final.jsonl"  # v9 fix round 2026-09-23; was repair/rows_v7_cwo24.jsonl',
         'ROWS_IN = EZ / "rows_v10_final.jsonl"  # v10 hold round 2026-09-23 (OW-30); was rows_v9_final.jsonl, and\n'
         '# before that repair/rows_v7_cwo24.jsonl'),
        ('  - every row the second reading refused to act on, or whose grade it questioned, is held - and no other row is;\n',
         '  - every row held in the corpus is held in the feed, and no other row is, and every feed row mirrors its corpus\n'
         '    row\'s review status, hold state and packet state (AMENDED 2026-09-23, v10 hold round, OW-30: the held set\n'
         '    was the second reading\'s STOP/GRADE_QUESTION set, and the selection added it at any grade);\n'),
        (CHECK_HELD_OLD, CHECK_HELD_NEW),
        ('"grades the shared feed has never carried: %s; all referred by the second reading: %s"',
         '"grades the shared feed has never carried: %s; all held in the corpus: %s"'),
        ('"referred by the second reading %d, marked held %d, deferred %d, difference %s"',
         '"held in the corpus %d, marked held %d, deferred %d, difference %s"'),
        (CHECK_MIRROR_OLD, CHECK_MIRROR_NEW),
        (TAMPER_OLD, TAMPER_NEW),
        ('           ("held_rows_are_exactly_the_referred_ones", tamper_unhold),\n',
         '           ("held_rows_are_exactly_the_referred_ones", tamper_unhold),\n'
         '           ("feed_mirrors_the_corpus_hold", tamper_packet_state),\n')]),
    D / "gen_sidecars.py": ("f25575206fb60ef36258cac78381a4dd0dcf2aab84c63ddc56bc15ecd5dd89a0", [
        ('CORPUS = EZ / "rows_v9_final.jsonl"  # v9 fix round 2026-09-23; was rows_v8_final.jsonl (b2160ad6)\n'
         'CORPUS_PIN = "%s"' % V9_PIN,
         'CORPUS = EZ / "rows_v10_final.jsonl"  # v10 hold round 2026-09-23 (OW-30); was rows_v9_final.jsonl (a80b6e67)\n'
         'CORPUS_PIN = "%s"' % V10_PIN),
        ('ATLAS_SRC = EZ / "rows_v9_final.jsonl"  # the atlas generator now reads the final corpus (v9 fix round)\n'
         'ATLAS_SRC_PIN = "%s"' % V9_PIN,
         'ATLAS_SRC = EZ / "rows_v10_final.jsonl"  # the atlas generator reads the final corpus (v10 hold round)\n'
         'ATLAS_SRC_PIN = "%s"' % V10_PIN),
        ("AMENDED 2026-09-23 (v9 fix round): the atlas rows",
         "AMENDED 2026-09-23 (v10 hold round, OW-30): the corpus and the atlas source are rows_v10_final.jsonl, which\n"
         "changes only P10-016's hold fields; the atlas rows now follow the corpus hold.\n"
         "AMENDED 2026-09-23 (v9 fix round): the atlas rows")]),
    EZ / "repair2" / "close_check_mirror.py": ("bdbad6da5667f5e827d7798ab5af51de63771076ca7a17bc6cbae4f30c9a1c5c", [
        ('              + [(EZ / "rows_v9_final.jsonl", "M8/sp_durable/Ezek/rows_v9_final.jsonl"),\n',
         '              + [(EZ / "rows_v10_final.jsonl", "M8/sp_durable/Ezek/rows_v10_final.jsonl"),\n'),
        ('    "suite": ([(EZ / "rows_v9_final.jsonl", "suite/rows_v9_final.jsonl")],\n'
         '              [str(EZ / "tools" / "run_validator_suite.py"), "suite/rows_v9_final.jsonl"],\n'
         '              "suite/rows_v9_final.jsonl.validator_report.json", EZ / "rows_v9_final.jsonl.validator_report.json"),\n',
         '    "suite": ([(EZ / "rows_v10_final.jsonl", "suite/rows_v10_final.jsonl")],\n'
         '              [str(EZ / "tools" / "run_validator_suite.py"), "suite/rows_v10_final.jsonl"],\n'
         '              "suite/rows_v10_final.jsonl.validator_report.json", EZ / "rows_v10_final.jsonl.validator_report.json"),\n'),
        ('checker reads it and it is the corpus the close tool pins. The earlier tool is kept as .pre_<sha12>.\n',
         'checker reads it and it is the corpus the close tool pins. The earlier tool is kept as .pre_<sha12>.\n'
         'AMENDED 2026-09-23 (v10 hold round, OW-30): both plans now carry rows_v10_final.jsonl, for the same reason.\n')])}
REGEN = {D / "atlas_candidate_feed_rows.jsonl": "6adc037d01ce02d4991162959e1b364bfe771915760a7875e6eae0d2de4d0f38",
         D / "Ezek_atlas_dimensions.v1.jsonl": "54c766dbff939f921dca0fe1b3d7a4006ff7014a8524487c1521cfee0e34632d",
         D / "atlas_rows_check.v1.json": "78545043f69dc015086d98062b40f1e654d8729f2e984256fb5d35afa592b178"}
WNEW = {EZ / "sidecar_src_ezek.jsonl": "9cea1004faedab89167a15479cd730e863e2938f476ec76b4f8d8f37af294c27",
        D / "Ezek_sidecar_derivation.v1.jsonl": "2001b502cda2653f06fa19c7af1ddfa64a0c642a6b1278b991b2cb314ca09175"}
ALL = {**{p: v[0] for p, v in GENS.items()}, **REGEN, **WNEW, V10: V10_PIN}

g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek"]
                   + sum((["--target", str(p.relative_to(SP)).replace("\\", "/")] for p in ALL), []),
                   cwd=str(SP), capture_output=True, text=True, encoding="utf-8", env=env)
gv = json.loads(g.stdout)
if gv["verdict"] != "CLEAR" or gv["in_flight"]:
    raise SystemExit("REFUSED by pin guard: %s %s" % (gv["verdict"], gv["in_flight"]))
saved = {}
for p, pin in ALL.items():
    b = p.read_bytes()
    if sha(b) != pin:
        raise SystemExit("REFUSED: %s is not at its pinned digest" % p.name)
    saved[p] = b
for p in list(GENS) + list(REGEN) + list(WNEW):
    keep = p.with_name(p.name + ".pre_" + ALL[p][:12])
    if keep.exists() and keep.read_bytes() != saved[p]:
        raise SystemExit("REFUSED: %s exists with different bytes" % keep.name)
    keep.write_bytes(saved[p])


def rollback(why):
    for p, b in saved.items():
        p.write_bytes(b)
    raise SystemExit("ROLLED BACK: " + why)


for p, (_, edits) in GENS.items():
    s = saved[p].decode("utf-8")
    # The tools are stored with CRLF line ends (MEASURED 2026-09-23; the v9 anchors were single-line). The anchors are
    # written with LF, so they are translated to the file's own line end, and a file with mixed line ends is refused.
    crlf = s.count("\r\n")
    if crlf and crlf != s.count("\n"):
        rollback("%s has mixed line ends (%d CRLF of %d LF)" % (p.name, crlf, s.count("\n")))
    nl = "\r\n" if crlf else "\n"
    edits = [(o.replace("\n", nl), n.replace("\n", nl)) for o, n in edits]
    for old, new in edits:
        if s.count(old) != 1:
            rollback("%s: an anchor occurs %d times: %r" % (p.name, s.count(old), old[:60]))
        s = s.replace(old, new)
    p.write_bytes(s.encode("utf-8"))
for p in WNEW:
    p.unlink()


def run(script, *args):
    r = subprocess.run([sys.executable, "-B", str(D / script)] + list(args), cwd=str(D), capture_output=True,
                       text=True, encoding="utf-8", env=env)
    return r.returncode, (r.stdout + r.stderr).strip()


steps = {}
for script, args, want in (("gen_atlas_rows.py", (), None), ("gen_atlas_rows.py", ("--check",), "DETERMINISTIC: MATCH"),
                           ("check_atlas_rows.py", (), None), ("check_atlas_rows.py", ("--selftest",), "SELFTEST: PASS"),
                           ("gen_sidecars.py", (), None), ("gen_sidecars.py", ("--check",), "MATCH")):
    rc, out = run(script, *args)
    steps[" ".join((script,) + args)] = out.splitlines()[-1][:160] if out else ""
    if rc or (want and want not in out):
        rollback("%s %s failed (rc %d): %s" % (script, args, rc, out[-700:]))
chk = json.loads((D / "atlas_rows_check.v1.json").read_text(encoding="utf-8"))
if chk.get("FAILED") or chk.get("input_rows_sha256") != V10_PIN:
    rollback("atlas check not clean over v10: %s %s" % (chk.get("FAILED"), chk.get("input_rows_sha256")))
feed = [json.loads(l) for l in (D / "atlas_candidate_feed_rows.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
held = sorted(x["chunk_decision_id"] for x in feed if x.get("candidate_hold_state"))
ids = {x["chunk_decision_id"] for x in feed}
shape = {"feed_rows": len(feed), "held": held, "082_absent": "M8-Ezek-082" not in ids,
         "grades": sorted({x["confidence"] for x in feed})}
if shape != {"feed_rows": 101, "held": ["M8-Ezek-113"], "082_absent": True, "grades": ["low", "medium_low"]}:
    rollback("the regenerated feed is not the ruled shape: %s" % shape)


def rowdiff(old_b, new_p, key):
    o = {r[key]: r for r in (json.loads(l) for l in old_b.decode("utf-8").splitlines() if l.strip())}
    n = {r[key]: r for r in (json.loads(l) for l in new_p.read_text(encoding="utf-8").splitlines() if l.strip())}
    out = {k: sorted(f for f in set(o[k]) | set(n[k]) if o[k].get(f) != n[k].get(f)) for k in o if k in n}
    return {"rows_old": len(o), "rows_new": len(n), "only_old": sorted(set(o) - set(n)), "only_new": sorted(set(n) - set(o)),
            "changed": {k: v for k, v in out.items() if v}}


print(json.dumps({"steps": steps, "shape": shape,
                  "atlas_rows": rowdiff(saved[D / "atlas_candidate_feed_rows.jsonl"], D / "atlas_candidate_feed_rows.jsonl",
                                        "chunk_decision_id"),
                  "sidecar": rowdiff(saved[EZ / "sidecar_src_ezek.jsonl"], EZ / "sidecar_src_ezek.jsonl", "writer_decision_id"),
                  "digests": {p.name: sha(p.read_bytes()) for p in list(GENS) + list(REGEN) + list(WNEW)},
                  "atlas_check": {k: chk.get(k) for k in ("VERDICT", "checks_passed", "checks_run", "input_rows_sha256")}},
                 ensure_ascii=False, indent=1))
