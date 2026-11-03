"""Add lane CTL_E5 to append_review_launch_row.py by exact anchors, keeping a .pre_ copy."""
import hashlib
from pathlib import Path
HERE = Path(__file__).resolve().parent
T = HERE.parents[1] / "review/append_review_launch_row.py"
b = T.read_bytes()
s = b.decode("utf-8")
if "CTL_E5" in s:
    raise SystemExit("REFUSED: already patched")
EDITS = [
 ('         "S5": ("cor_fixup3_review_s5_a1", "review_S5",\n',
  '         "CTL_E5": ("cor_controlling_rulings_r5_a1", "controlling_r5",\n'
  '                    "1 Corinthians controlling execution, round 5 (Fable\'s role on claude-opus-5-5, OW-25/OW-30): "\n'
  '                    "rules on every item of 1Cor/review/1cor_controlling_agent_queue_e5.v1.json (S5\'s 14 findings and "\n'
  '                    "the gate for FIXUP-4 and S6); items for Fable\'s end review listed. Writes in OUT only"),\n'
  '         "S5": ("cor_fixup3_review_s5_a1", "review_S5",\n'),
 ('"CTL_E4": "cor_ctl4",\n', '"CTL_E4": "cor_ctl4", "CTL_E5": "cor_ctl5",\n'),
 ('"CTL_E4": "CONTROLLING_BRIEF_E4",\n', '"CTL_E4": "CONTROLLING_BRIEF_E4", "CTL_E5": "CONTROLLING_BRIEF_E5",\n'),
 ('CATCHER["S5"] = (',
  'CATCHER["CTL_E5"] = ("the orchestrator\'s landing check of the deliverable (one ruling per queue id, the gate fields); "\n'
  '                     "the fix-up authors and S6, who act on its gate; Fable at the campaign-end review (OW-28)")\n'
  'CATCHER["S5"] = ('),
]
for old, new in EDITS:
    if s.count(old) != 1:
        raise SystemExit("REFUSED: anchor count %d for %r" % (s.count(old), old[:40]))
    s = s.replace(old, new)
pre = T.with_name(T.name + ".pre_" + hashlib.sha256(b).hexdigest()[:12])
pre.write_bytes(b)
T.write_bytes(s.encode("utf-8"))
print(pre.name, hashlib.sha256(T.read_bytes()).hexdigest()[:12])
