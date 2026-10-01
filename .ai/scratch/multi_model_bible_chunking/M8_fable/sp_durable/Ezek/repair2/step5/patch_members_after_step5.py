#!/usr/bin/env python3
"""Two suite-member defects found in step 5, fixed together AFTER both step-5 adjudications have landed (the running
agents pinned both files). Exact-once replacements; per-file backup; selftests must pass after, or both files are
restored byte-for-byte.

1. check_register.py - its selftest SANCTIONED two referents #e15 Q9(a) bars ("this extract"; "the inventory does not
   carry ..."): a row "never names a record, census, plan, inventory, worklist, digest or key". Found by step-5 half-2
   lane B and routed by the half-2 adjudicator (R-05). The same shape as E-40, one layer down: the tool kept the older
   sanction. Arm (iii) gains the referents the step-5 lanes and adjudicator named (extract, inventory, census, worklist,
   disclosure layer, 'N-list' labels, the operative category/classification label), the two wrong GREEN vectors become
   FIRE vectors, and the witness-naming forms Q9(a) prescribes become the GREEN vectors.
2. check_universals.py - a clause 6 v2 seam pair ("47.4/47.5") matched the sweep arm's N/N fraction, so every claim
   in a sentence carrying a seam pair was silently treated as sourced ("one-faced only" at 47:5 vanished from the
   report while still written). Seam pairs are masked before the sweep test; a --selftest with both fixtures is added.

usage: python patch_members_after_step5.py [--apply]
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

EZ = Path(__file__).resolve().parents[2]
T = EZ / "tools"
REG, UNI = T / "check_register.py", T / "check_universals.py"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
APPLY = "--apply" in sys.argv

REG_EDITS = [
    (r'''        r"(?:strategy|plan)\b[^.;]{0,30}?\bline \d+|\bline \d+[^.;]{0,30}?\b(?:strategy|plan)\b", re.I),''',
     r'''        r"(?:strategy|plan)\b[^.;]{0,30}?\bline \d+|\bline \d+[^.;]{0,30}?\b(?:strategy|plan)\b|"
        # step-5 additions (#e15 Q9(a): never a record, census, plan, inventory, worklist, digest or key)
        r"\b(?:this|the|that) extract\b|\bthe (?:[\w-]+ )?inventory\b|\bthe census\b|\bthe worklist\b|"
        r"\bthe (?:[\w/-]+ )?disclosure layer\b|\(\d+-list\)|\b\d+-list\b|\boperative[- ](?:category|classification)\b", re.I),'''),
    ('''        ("sanctioned: the witness's count layer", row(device_notes="the bytes are unsourceable from this extract")),\n''',
     '''        ("sanctioned: the witness named, not a file", row(device_notes="the position within the verse is unsourceable from this witness")),\n'''),
    ('''        ("sanctioned: the inventory's layer", row(device_notes="the inventory does not carry intra-verse position")),\n''',
     '''        ("sanctioned: the count shorthand", row(device_notes="a recognition close (sweep: 64 verses) at 13:14")),\n'''),
    ('''        ("strategy_citation", row(device_notes="cited per the strategy file")),\n''',
     '''        ("strategy_citation", row(device_notes="cited per the strategy file")),
        ("artifact_referent", row(device_notes="the bytes are unsourceable from this extract")),
        ("artifact_referent", row(device_notes="the inventory does not carry intra-verse position")),
        ("artifact_referent", row(boundary_evidence_refs=["oshb:Ezek.24.24 [DISCLOSURE-device] checked against the mark inventory"])),
        ("artifact_referent", row(device_notes="a strict utterance member (81-list)")),
        ("artifact_referent", row(strongest_rejected_alternative="the operative classification treats this as law")),
        ("artifact_referent", row(device_notes="disclosed per the ketiv/qere disclosure layer")),
'''),
]
UNI_EDITS = [
    ('''            s2 = re.sub(r"“[^”]*”", lambda m: " " * len(m.group(0)), s2)\n''',
     '''            s2 = re.sub(r"“[^”]*”", lambda m: " " * len(m.group(0)), s2)
            # a clause 6 v2 seam pair ('47.4/47.5') is not a count: masked before the sweep arm reads it as N/N
            s2 = SEAM_PAIR.sub(lambda m: " " * len(m.group(0)), s2)
'''),
    ('''def main() -> int:\n    flags = []\n''',
     '''SEAM_PAIR = re.compile(r"(?<![\\d.])\\d{1,2}\\.\\d{1,3}/\\d{1,2}\\.\\d{1,3}(?![\\d.])")


def selftest() -> int:
    """A seam pair never sources a claim; a real sweep citation still does (both must hold)."""
    import tempfile
    cases = [("a seam pair does not hide 'only'", ["oshb:Ezek.47.5 [WARRANT-rival:far] 47.4/47.5 one-faced only"], 1),
             ("a sweep citation still sources 'only'", ["the only such close (sweep: 5 verses) at 13:9"], 0)]
    failed = []
    for name, strings, want in cases:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "fixture.json"
            p.write_text(json.dumps({"x": strings}), encoding="utf-8")
            r = subprocess.run([sys.executable, "-B", __file__, str(p)], capture_output=True, text=True, encoding="utf-8",
                               env=dict(os.environ, PYTHONUTF8="1"))
            got = json.loads(r.stdout)["flag_count"]
        if got != want:
            failed.append("%s (got %d, want %d)" % (name, got, want))
    print(json.dumps({"selftest": "check_universals seam-pair mask", "cases": len(cases), "failed": failed}, indent=1))
    return 1 if failed else 0


def main() -> int:
    if "--selftest" in sys.argv[1:]:
        return selftest()
    flags = []
'''),
]


def patch(p, edits):
    s = p.read_text(encoding="utf-8")
    for old, new in edits:
        n = s.count(old)
        if n != 1:
            raise SystemExit("REFUSED: anchor found %d times in %s: %r" % (n, p.name, old[:80]))
        s = s.replace(old, new)
    return s


new_reg, new_uni = patch(REG, REG_EDITS), patch(UNI, UNI_EDITS)
if "import subprocess" not in new_uni:
    new_uni = new_uni.replace("import re\n", "import os\nimport re\nimport subprocess\n", 1)
print(json.dumps({"check_register_before": sha(REG), "check_universals_before": sha(UNI), "simulated": True}, indent=1))
if not APPLY:
    raise SystemExit(0)
bk = {}
for p, new in ((REG, new_reg), (UNI, new_uni)):
    b = p.with_name(p.name + ".pre_" + sha(p)[:12])
    shutil.copy2(p, b)
    bk[p] = b
    p.write_text(new, encoding="utf-8", newline="\n")
env = dict(os.environ, PYTHONUTF8="1")
ok = True
for p in (REG, UNI):
    r = subprocess.run([sys.executable, "-B", str(p), "--selftest"], cwd=str(T), capture_output=True, text=True, encoding="utf-8", env=env)
    out = r.stdout[r.stdout.find("{"):]
    failed = json.loads(out).get("failed")
    print(p.name, "selftest exit", r.returncode, "failed", failed)
    ok = ok and r.returncode == 0 and not failed
if not ok:
    for p, b in bk.items():
        shutil.copy2(b, p)
    raise SystemExit("REFUSED: a selftest failed; both members RESTORED from their backups")
print(json.dumps({"check_register_after": sha(REG), "check_universals_after": sha(UNI),
                  "backups": {p.name: b.name for p, b in bk.items()}}, indent=1))
