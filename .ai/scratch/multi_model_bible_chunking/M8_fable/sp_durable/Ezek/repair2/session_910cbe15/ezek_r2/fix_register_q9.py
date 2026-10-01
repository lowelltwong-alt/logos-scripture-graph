#!/usr/bin/env python3
"""#e15 Q9(b): add the three register arms, each a FLOOR under the rule and not the rule.

The ruling's answer to Q9(a) is the part that matters for me: section 8 bars REFERENTS BY CLASS, and the
checker's patterns are a floor under that rule, not the rule. So "the division plan" - the phrase I introduced
to replace the barred word "strategy" - is barred, because it refers to the same file. My 30 register edits are
my defect and are undone in the prose pass by stating the rule's SUBSTANCE.

The three arms, verbatim from the order:
  (i)   BARE-ID: a bare rule id near a rule word, plus the literal ruling tokens;
  (ii)  REPAIR-NARRATION: a row telling its reader about its own repair history;
  (iii) ARTIFACT-REFERENT: a phrase naming a record, census, plan, digest or key path as an object.

The ruling also states where the line falls for evidence references, and this is the sentence the prose pass
works from: "the row names the WITNESS and its layers ... and states counts with the sweep convention; it never
names a record, census, plan, inventory, worklist, digest or key. OW-18 provenance survives: the tier word and
the witness are stated; the FILE is not."
"""
import hashlib
import json
import py_compile
import shutil
import subprocess
import sys
from pathlib import Path

TOOLS = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable"
             r"\sp_durable\Ezek\tools")
SRC = TOOLS / "check_register.py"
HERE = Path(__file__).resolve().parent
pre = SRC.read_bytes()
PIN = hashlib.sha256(pre).hexdigest()
(HERE / ("check_register.preimage_%s.py" % PIN[:12])).write_bytes(pre)
t = pre.decode("utf-8")

ARMS = r'''    # ---- #e15 Q9(b): three arms, each a FLOOR under section 8's rule that BARRED REFERENTS ARE BARRED BY
    # CLASS. The checker's patterns are not the rule; a paraphrase of a barred referent is barred too, which
    # is why the orchestrator's own replacement phrase "the division plan" appears in arm (iii).
    "bare_rule_id": re.compile(
        r"\b(?:A\d{1,2}|C\d|D\d{1,2}|R\d{1,2})\b(?=[^.;]{0,40}\b(?:disclosure|disclose[sd]?|weigh(?:ed|ing)?|"
        r"order(?:ed|s)?|limb|class|rule)\b)"
        r"|\b(?:disclosure|disclose[sd]?|weigh(?:ed|ing)?|order(?:ed|s)?|limb|class|rule)\b[^.;]{0,40}?"
        r"\b(?:A\d{1,2}|C\d|D\d{1,2}|R\d{1,2})\b"
        r"|\bCUT-RULE\b|\bCONF-CAL\b|\bDEF-A4[A-Z-]*\b|\bMARKS-3D\b|\bOSS-VOCAB\b"
        r"|\blimb \([ab]\)|#e\d+(?:\s*Q\d+)?", re.I),
    "repair_narration": re.compile(
        r"\bis withdrawn\b|\bwas (?:measured|found) (?:false|FALSE)\b|"
        r"\bearlier (?:denial|form|version|reading|claim)\b|\breworded because\b|"
        r"\bno longer (?:claims|asserts)\b|\bcorrected (?:from|here)\b|"
        r"\brecorded (?:rather than|not) (?:silently )?absorbed\b|\bthe audit\b|\bsuperseded\b", re.I),
    "artifact_referent": re.compile(
        r"\bthe division plan\b|\bpinned\b|\bdigest\b|\bthe (?:device|verse) census\b|"
        r"\bthe section-mark record\b|\bthe (?:marks|kq|paseq) (?:record|layer|input)\b|"
        r"\b[a-z]+_[a-z_]+\.[a-z_]+(?:\.[a-z_]+)+\b|"
        r"(?:strategy|plan)\b[^.;]{0,30}?\bline \d+|\bline \d+[^.;]{0,30}?\b(?:strategy|plan)\b", re.I),
'''
anchor = '    "ledger_id": re.compile(r"\\bE-\\d{2}\\b"),'
assert t.count(anchor) == 1
t = t.replace(anchor, ARMS + anchor, 1)

# selftest fixtures for the three arms, added to the existing fire list
FIRE = '''        ("bare_rule_id", row(device_notes="the samekh is disclosed under A10 at this seam")),
        ("bare_rule_id", row(device_notes="a close held per CUT-RULE limb (b)")),
        ("repair_narration", row(strongest_rejected_alternative="the earlier denial is withdrawn")),
        ("artifact_referent", row(device_notes="MEASURED from the section-mark record at its pinned digest")),
        ("artifact_referent", row(device_notes="the question the division plan holds for this chapter")),
        ("artifact_referent", row(device_notes="a rule the plan states at line 351")),
'''
anchor2 = '        ("ledger_id", row(device_notes="a cap disclosed (E-02)")),'
assert t.count(anchor2) == 1
t = t.replace(anchor2, FIRE + anchor2, 1)

STAGE = HERE / "check_register.candidate.py"
STAGE.write_text(t, encoding="utf-8", newline="\n")
py_compile.compile(str(STAGE), doraise=True)
tmp = SRC.with_suffix(".py.tmpQ9")
shutil.copy2(STAGE, tmp)
tmp.replace(SRC)
post = hashlib.sha256(SRC.read_bytes()).hexdigest()

sel = subprocess.run([sys.executable, str(SRC), "--selftest"], capture_output=True, text=True,
                     cwd=str(TOOLS), encoding="utf-8", errors="replace")
rows = TOOLS.parent / "repair" / "rows_v7_cwo24.jsonl"
run = subprocess.run([sys.executable, str(SRC), str(rows)], capture_output=True, text=True,
                     cwd=str(TOOLS), encoding="utf-8", errors="replace")
try:
    rep = json.loads(run.stdout)
    base = {"flag_count": rep.get("flag_count"), "status": rep.get("status"),
            "by_class": rep.get("by_class")}
except Exception:
    base = {"unparsed": (run.stdout or run.stderr)[-400:]}
try:
    s = json.loads(sel.stdout)
    selftest = {"failed": s.get("failed"), "vectors": s.get("vectors")}
except Exception:
    selftest = {"tail": (sel.stdout or sel.stderr)[-300:]}
print(json.dumps({"preimage": PIN, "postimage": post,
                  "selftest": selftest,
                  "BASELINE over the current rows, with the new arms": base}, indent=1, ensure_ascii=False))
