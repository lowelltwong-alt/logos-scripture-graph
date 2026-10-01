#!/usr/bin/env python3
"""Re-point Ezekiel's derived-record generators at rows_v9_final.jsonl and regenerate (v9 fix round, 2026-09-23).

WHY. Both close lanes flagged (low) that the atlas deliverable and the sidecar source were derived from
repair/rows_v7_cwo24.jsonl, the preimage of the final corpus, while the feed asserts candidate_review_complete. The v9
round changed three rows (P03-001 prose, P06-015 signals, P10-016 refs), and the atlas row for P06-015 copies its signals.
So the atlas generator, its checker and the sidecar generator now read the v9 corpus itself.

HOW. Every input and every current output is pinned by digest. The pin guard must be CLEAR. Each generator is saved as
<name>.pre_<sha12> and edited by exact strings, each of which must occur exactly once. Outputs regenerated in place
(atlas rows, dimensions, atlas check) are first copied to .pre_<sha12>; the two write-new sidecar outputs are renamed to
.pre_<sha12> (a suffix after .jsonl, so the close tool's sidecar_src_*.jsonl glob never sees them) so their generator can
write them fresh. Then: gen_atlas_rows, gen_atlas_rows --check, check_atlas_rows (and --selftest), gen_sidecars,
gen_sidecars --check. Any failure restores every file from the saved bytes. The report lists which atlas and sidecar rows
changed, and in which fields, against the old outputs.
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
V9, V9_PIN = EZ / "rows_v9_final.jsonl", "a80b6e6712aa43bf3d8652255b4655a934af08a9cd3e036f9b320a37bbd1098c"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
env = dict(os.environ, PYTHONUTF8="1")
GENS = {
    D / "gen_atlas_rows.py": ("ce34aaa4ae791a31d7c87f1db7c2866bf25f87184deb34475bf75ec4a945107e", [
        ('ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"',
         'ROWS = EZ / "rows_v9_final.jsonl"  # v9 fix round 2026-09-23; was repair/rows_v7_cwo24.jsonl (the preimage)')]),
    D / "check_atlas_rows.py": ("2347dd8b8e94624e43e9a9e0881182ce978741e0c311b9b62d9728ac410160d3", [
        ('ROWS_IN = EZ / "repair" / "rows_v7_cwo24.jsonl"',
         'ROWS_IN = EZ / "rows_v9_final.jsonl"  # v9 fix round 2026-09-23; was repair/rows_v7_cwo24.jsonl')]),
    D / "gen_sidecars.py": ("2f78fd8eb31d3cc5a676950ee69f601445713a482efbeb6b8462e29036f31566", [
        ('CORPUS = EZ / "rows_v8_final.jsonl"\nCORPUS_PIN = "b2160ad6281184dc1dedf15a764bc058bc79a181928ed6323dbc332ec09cb0e7"',
         'CORPUS = EZ / "rows_v9_final.jsonl"  # v9 fix round 2026-09-23; was rows_v8_final.jsonl (b2160ad6)\n'
         'CORPUS_PIN = "%s"' % V9_PIN),
        ('ATLAS_SRC = EZ / "repair" / "rows_v7_cwo24.jsonl"\n'
         'ATLAS_SRC_PIN = "e24048cc869f1493ac5d65a7e37fd6457909d2848da31583e9d55211601611a7"',
         'ATLAS_SRC = EZ / "rows_v9_final.jsonl"  # the atlas generator now reads the final corpus (v9 fix round)\n'
         'ATLAS_SRC_PIN = "%s"' % V9_PIN),
        ("The corpus is pinned. The atlas rows were built over rows_v7_cwo24 (e24048cc).",
         "AMENDED 2026-09-23 (v9 fix round): the atlas rows are now built over the final corpus itself, so the equality\n"
         "check below compares the corpus with itself. What follows is the history before that.\n"
         "The corpus is pinned. The atlas rows were built over rows_v7_cwo24 (e24048cc).")])}
REGEN = {D / "atlas_candidate_feed_rows.jsonl": "b9de6b3c7905c790f950e7574a6f256a2c8377fb2816625683fc9d84ab348739",
         D / "Ezek_atlas_dimensions.v1.jsonl": "417fb54332990a913011bf03d507cfd0221d1e927e62c0daf10d095a566768c2",
         D / "atlas_rows_check.v1.json": "d84658968d232d5a284aac7c1b152a530208b5da70f3a02dbeea748cfaaa3506"}
WNEW = {EZ / "sidecar_src_ezek.jsonl": "9cea1004faedab89167a15479cd730e863e2938f476ec76b4f8d8f37af294c27",
        D / "Ezek_sidecar_derivation.v1.jsonl": "2001b502cda2653f06fa19c7af1ddfa64a0c642a6b1278b991b2cb314ca09175"}
ALL = {**{p: v[0] for p, v in GENS.items()}, **REGEN, **WNEW, V9: V9_PIN}

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
    for old, new in edits:
        if s.count(old) != 1:
            rollback("%s: an anchor occurs %d times" % (p.name, s.count(old)))
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
        rollback("%s %s failed (rc %d): %s" % (script, args, rc, out[-500:]))
chk = json.loads((D / "atlas_rows_check.v1.json").read_text(encoding="utf-8"))
if chk.get("FAILED") or chk.get("input_rows_sha256", V9_PIN) != V9_PIN:
    rollback("atlas check not clean over v9: %s" % chk.get("FAILED"))


def rowdiff(old_b, new_p, key):
    o = {r[key]: r for r in (json.loads(l) for l in old_b.decode("utf-8").splitlines() if l.strip())}
    n = {r[key]: r for r in (json.loads(l) for l in new_p.read_text(encoding="utf-8").splitlines() if l.strip())}
    out = {k: sorted(f for f in set(o[k]) | set(n[k]) if o[k].get(f) != n[k].get(f)) for k in o if k in n}
    return {"rows_old": len(o), "rows_new": len(n), "only_old": sorted(set(o) - set(n)), "only_new": sorted(set(n) - set(o)),
            "changed": {k: v for k, v in out.items() if v}}


print(json.dumps({"steps": steps,
                  "atlas_rows": rowdiff(saved[D / "atlas_candidate_feed_rows.jsonl"], D / "atlas_candidate_feed_rows.jsonl",
                                        "chunk_decision_id"),
                  "sidecar": rowdiff(saved[EZ / "sidecar_src_ezek.jsonl"], EZ / "sidecar_src_ezek.jsonl", "writer_decision_id"),
                  "digests": {p.name: sha(p.read_bytes()) for p in list(GENS) + list(REGEN) + list(WNEW)},
                  "atlas_check": {k: chk.get(k) for k in ("VERDICT", "checks_passed", "checks_run", "input_rows_sha256")}},
                 ensure_ascii=False, indent=1))
